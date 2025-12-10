"""
OpenAI client for embeddings and chat completions
Handles AI operations for RAG chatbot and translations
"""

from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional
from backend.config import settings
import logging

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI API operations"""

    def __init__(self):
        """Initialize OpenAI client"""
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.embedding_model = settings.openai_embedding_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens

    async def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding vector for text

        Args:
            text: Text to embed

        Returns:
            Embedding vector (1536 dimensions for text-embedding-3-small)
        """
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding

        except Exception as e:
            logger.error(f"Failed to create embedding: {e}")
            raise

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts in batch

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=texts
            )
            return [item.embedding for item in response.data]

        except Exception as e:
            logger.error(f"Failed to create batch embeddings: {e}")
            raise

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate chat response using OpenAI

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Optional temperature override
            max_tokens: Optional max tokens override

        Returns:
            Dict with 'content', 'tokens_used', 'model'
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )

            return {
                "content": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens if response.usage else 0,
                "model": response.model
            }

        except Exception as e:
            logger.error(f"Failed to generate chat response: {e}")
            raise

    async def generate_rag_response(
        self,
        query: str,
        context_chunks: List[Dict[str, str]],
        selected_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate RAG response with context from retrieved chunks

        Args:
            query: User query
            context_chunks: List of relevant text chunks with metadata
            selected_text: Optional highlighted text from user

        Returns:
            Dict with 'response', 'tokens_used'
        """
        # Build context from chunks
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            chapter = chunk.get("chapter_id", "Unknown")
            section = chunk.get("section", "Unknown")
            text = chunk.get("text", "")
            context_parts.append(f"[Source {i} - {chapter}, Section {section}]\n{text}\n")

        context = "\n".join(context_parts)

        # Build system prompt
        system_prompt = """You are an expert AI assistant for a Physical AI & Humanoid Robotics textbook.
Your role is to answer student questions accurately based on the provided textbook content.

Guidelines:
- Answer based ONLY on the provided context from the textbook
- Be concise but thorough - aim for 2-3 paragraphs
- Use technical terminology appropriately for the student's level
- If the context doesn't contain enough information, say so
- Cite sources naturally in your response (e.g., "As covered in Week 7...")
- For math/code, use clear formatting"""

        # Build user prompt
        user_parts = [f"Question: {query}"]
        if selected_text:
            user_parts.append(f"\nSelected Text Context: {selected_text}")
        user_parts.append(f"\nTextbook Context:\n{context}")

        user_prompt = "\n".join(user_parts)

        # Generate response
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return await self.generate_chat_response(messages, temperature=0.3)

    async def translate_content(
        self,
        content: str,
        target_language: str,
        source_language: str = "en"
    ) -> Dict[str, Any]:
        """
        Translate content to target language

        Args:
            content: Content to translate
            target_language: Target language code (e.g., 'ur', 'es')
            source_language: Source language code (default: 'en')

        Returns:
            Dict with 'translated_content', 'tokens_used'
        """
        language_names = {
            "ur": "Urdu",
            "es": "Spanish",
            "fr": "French",
            "ar": "Arabic",
            "zh": "Chinese",
            "en": "English"
        }

        target_lang_name = language_names.get(target_language, target_language)
        source_lang_name = language_names.get(source_language, source_language)

        system_prompt = f"""You are a professional translator specializing in technical and educational content.
Translate the provided {source_lang_name} robotics textbook chapter to {target_lang_name}.

Guidelines:
- Preserve markdown formatting exactly
- Keep technical terms in English where appropriate (e.g., "ROS", "SLAM", "kinematics")
- Maintain clarity and educational tone
- Preserve code blocks unchanged
- Keep mathematical notation unchanged"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate this chapter:\n\n{content}"}
        ]

        response = await self.generate_chat_response(
            messages,
            temperature=0.3,
            max_tokens=4000
        )

        return {
            "translated_content": response["content"],
            "tokens_used": response["tokens_used"]
        }

    async def health_check(self) -> bool:
        """
        Check if OpenAI API is accessible

        Returns:
            True if healthy, False otherwise
        """
        try:
            # Simple test: create embedding for a short string
            await self.create_embedding("test")
            return True
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False


# Singleton instance
openai_service = OpenAIService()
