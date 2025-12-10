"""
Translation model for cached chapter translations
"""

from sqlalchemy import Column, String, Text, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from backend.database import Base


class Translation(Base):
    """Translation model for caching chapter translations"""

    __tablename__ = "translations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Translation Identification
    chapter_id = Column(String(255), nullable=False)
    language = Column(String(10), nullable=False)

    # Content
    content = Column(Text, nullable=False)
    source_language = Column(String(10), nullable=False, default="en")
    translation_model = Column(String(50), nullable=False)

    # Metadata
    translation_metadata = Column(JSONB, nullable=True)  # {source_word_count, target_word_count, api_cost_usd}

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Constraints
    __table_args__ = (
        UniqueConstraint("chapter_id", "language", name="unique_chapter_language"),
    )

    def __repr__(self):
        return f"<Translation(chapter_id={self.chapter_id}, language={self.language})>"
