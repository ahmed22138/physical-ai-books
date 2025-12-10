"""
RAG (Retrieval-Augmented Generation) Service
Orchestrates the RAG pipeline for chatbot responses
"""

from typing import List, Dict, Any, Optional
from backend.qdrant_client import qdrant_service
from backend.openai_client import openai_service
from backend.config import settings
import logging
import time
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class RAGService:
    """Service for RAG chatbot operations"""

    def __init__(self):
        """Initialize RAG service"""
        self.qdrant = qdrant_service
        self.openai = openai_service
        self.top_k_results = 5  # Number of chunks to retrieve
        self.score_threshold = 0.5  # Minimum similarity score (0.5 = 50% similarity)
        self.docs_path = None  # Will be set on first use

    def _get_docs_path(self) -> Path:
        """Get path to docs directory"""
        if self.docs_path is None:
            # Try multiple possible paths
            possible_paths = [
                Path(settings.content_path),  # From config
                Path(__file__).parent.parent.parent / "frontend" / "docs",  # Relative to backend
                Path("frontend") / "docs",  # Relative to project root
            ]

            for path in possible_paths:
                if path.exists():
                    self.docs_path = path
                    logger.info(f"Found docs directory at: {path}")
                    break

            if self.docs_path is None:
                logger.warning("Could not find docs directory")
                self.docs_path = Path("frontend/docs")  # Fallback

        return self.docs_path

    async def _fallback_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Fallback search when Qdrant is unavailable
        Searches markdown files directly with keyword matching
        """
        try:
            docs_path = self._get_docs_path()
            results = []
            query_lower = query.lower()
            query_keywords = set(query_lower.split())

            # Search markdown files
            for md_file in docs_path.rglob("*.md"):
                if md_file.name == "intro.md":
                    continue

                try:
                    content = md_file.read_text(encoding='utf-8')
                    content_lower = content.lower()

                    # Simple keyword matching
                    matches = sum(1 for keyword in query_keywords if keyword in content_lower)
                    if matches > 0:
                        # Extract chapter info from path
                        chapter_id = md_file.stem
                        module = "general"

                        if "01-introduction" in str(md_file):
                            module = "Introduction"
                        elif "02-perception" in str(md_file):
                            module = "Perception"
                        elif "03-control" in str(md_file):
                            module = "Control"
                        elif "04-integration" in str(md_file):
                            module = "Integration"

                        # Take first 2000 characters as context
                        excerpt = content[:2000]

                        results.append({
                            "score": matches / len(query_keywords),  # Simple relevance score
                            "payload": {
                                "chapter_id": chapter_id,
                                "section": module,
                                "text": excerpt
                            }
                        })
                except Exception as e:
                    logger.warning(f"Error reading {md_file}: {e}")

            # Sort by score and return top 3
            results.sort(key=lambda x: x["score"], reverse=True)
            logger.info(f"Fallback search found {len(results)} results for query")
            return results[:3]

        except Exception as e:
            logger.error(f"Fallback search failed: {e}")
            return []

    async def query(
        self,
        query: str,
        chapter_filter: Optional[str] = None,
        selected_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process RAG query and generate response

        Args:
            query: User question
            chapter_filter: Optional chapter to filter results
            selected_text: Optional highlighted text for context

        Returns:
            Dict with response, sources, confidence, response_time_ms
        """
        start_time = time.time()

        try:
            # Step 1: Try Qdrant search first
            search_results = []
            use_fallback = False

            try:
                # Create embedding for query
                query_vector = await self.openai.create_embedding(query)
                logger.info(f"Created query embedding (dimension: {len(query_vector)})")

                # Search Qdrant for similar chunks
                search_results = await self.qdrant.search(
                    query_vector=query_vector,
                    limit=self.top_k_results,
                    score_threshold=self.score_threshold,
                    chapter_filter=chapter_filter
                )

                if not search_results:
                    logger.warning("No results from Qdrant, using fallback search")
                    use_fallback = True
            except Exception as qdrant_error:
                logger.warning(f"Qdrant search failed: {qdrant_error}, using fallback")
                use_fallback = True

            # Step 2: Use fallback search if Qdrant unavailable
            if use_fallback:
                search_results = await self._fallback_search(query)

            if not search_results:
                logger.warning("No relevant content found")
                return {
                    "response": "I couldn't find relevant information in the textbook to answer your question. Please try rephrasing or ask about a different topic.",
                    "sources": [],
                    "confidence": 0.0,
                    "response_time_ms": int((time.time() - start_time) * 1000),
                    "tokens_used": 0
                }

            # Step 3: Extract context chunks
            context_chunks = []
            sources = []

            for result in search_results:
                payload = result["payload"]
                context_chunks.append({
                    "chapter_id": payload.get("chapter_id", ""),
                    "section": payload.get("section", ""),
                    "text": payload.get("text", "")
                })

                sources.append({
                    "chapter": payload.get("chapter_id", ""),
                    "section": payload.get("section", ""),
                    "quote": payload.get("text", "")[:200] + "..."  # First 200 chars
                })

            # Calculate average confidence
            avg_confidence = sum(r["score"] for r in search_results) / len(search_results)

            # Step 4: Generate response using OpenAI
            response_data = await self.openai.generate_rag_response(
                query=query,
                context_chunks=context_chunks,
                selected_text=selected_text
            )

            response_time_ms = int((time.time() - start_time) * 1000)

            logger.info(f"RAG query completed in {response_time_ms}ms with {len(sources)} sources")

            return {
                "response": response_data["content"],
                "sources": sources,
                "confidence": round(avg_confidence, 2),
                "response_time_ms": response_time_ms,
                "tokens_used": response_data["tokens_used"]
            }

        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            raise

    async def ingest_content(
        self,
        content_chunks: List[Dict[str, Any]]
    ) -> bool:
        """
        Ingest content chunks into vector database

        Args:
            content_chunks: List of dicts with keys:
                - id: Unique identifier
                - text: Content text to embed
                - chapter_id: Chapter identifier
                - section: Section name
                - metadata: Additional metadata

        Returns:
            True if successful
        """
        try:
            logger.info(f"Ingesting {len(content_chunks)} content chunks...")

            # Extract texts for batch embedding
            texts = [chunk["text"] for chunk in content_chunks]

            # Create embeddings in batch
            embeddings = await self.openai.create_embeddings_batch(texts)
            logger.info(f"Created {len(embeddings)} embeddings")

            # Prepare points for Qdrant
            points = []
            for chunk, embedding in zip(content_chunks, embeddings):
                points.append({
                    "id": chunk["id"],
                    "vector": embedding,
                    "payload": {
                        "chapter_id": chunk["chapter_id"],
                        "section": chunk.get("section", ""),
                        "text": chunk["text"],
                        "metadata": chunk.get("metadata", {})
                    }
                })

            # Upsert to Qdrant
            success = await self.qdrant.upsert_points(points)

            if success:
                logger.info(f"Successfully ingested {len(points)} chunks")
            else:
                logger.error("Failed to ingest content chunks")

            return success

        except Exception as e:
            logger.error(f"Content ingestion failed: {e}")
            return False

    async def health_check(self) -> Dict[str, str]:
        """
        Check health of RAG service dependencies

        Returns:
            Dict with status of qdrant and openai
        """
        qdrant_healthy = await self.qdrant.health_check()
        openai_healthy = await self.openai.health_check()

        return {
            "qdrant": "ok" if qdrant_healthy else "error",
            "openai": "ok" if openai_healthy else "error"
        }


# Singleton instance
rag_service = RAGService()
