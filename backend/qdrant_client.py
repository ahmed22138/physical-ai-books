"""
Qdrant client for vector database operations
Handles embeddings storage and semantic search
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from qdrant_client.http.exceptions import UnexpectedResponse
from typing import List, Dict, Any, Optional
from backend.config import settings
import logging

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database"""

    def __init__(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = settings.qdrant_vector_size

    async def init_collection(self):
        """
        Initialize Qdrant collection if it doesn't exist

        Creates collection with cosine distance for semantic similarity
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                # Create collection
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection already exists: {self.collection_name}")

        except UnexpectedResponse as e:
            logger.error(f"Failed to initialize Qdrant collection: {e}")
            raise

    async def upsert_points(
        self,
        points: List[Dict[str, Any]]
    ) -> bool:
        """
        Insert or update points in Qdrant

        Args:
            points: List of point dicts with keys:
                - id: Unique identifier (str or int)
                - vector: Embedding vector (List[float])
                - payload: Metadata dict with keys like chapter_id, section, text, etc.

        Returns:
            True if successful, False otherwise
        """
        try:
            point_structs = [
                PointStruct(
                    id=point["id"],
                    vector=point["vector"],
                    payload=point["payload"]
                )
                for point in points
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=point_structs
            )
            logger.info(f"Upserted {len(points)} points to Qdrant")
            return True

        except Exception as e:
            logger.error(f"Failed to upsert points: {e}")
            return False

    async def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: float = 0.7,
        chapter_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant

        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score (0.0 to 1.0)
            chapter_filter: Optional chapter ID to filter results

        Returns:
            List of search results with payload and score
        """
        try:
            # Build filter if chapter specified
            search_filter = None
            if chapter_filter:
                search_filter = Filter(
                    must=[
                        FieldCondition(
                            key="chapter_id",
                            match=MatchValue(value=chapter_filter)
                        )
                    ]
                )

            # Execute search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=search_filter
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                })

            logger.info(f"Found {len(formatted_results)} results with score >= {score_threshold}")
            return formatted_results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def delete_collection(self):
        """Delete the collection (for testing/reset)"""
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")

    async def health_check(self) -> bool:
        """
        Check if Qdrant service is healthy

        Returns:
            True if healthy, False otherwise
        """
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False


# Singleton instance
qdrant_service = QdrantService()
