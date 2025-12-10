"""
ChatMessage model for RAG chatbot interactions
"""

from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from backend.database import Base


class ChatMessage(Base):
    """ChatMessage model for RAG chatbot history"""

    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Query Details
    query = Column(Text, nullable=False)
    selected_text = Column(Text, nullable=True)
    chapter = Column(String(255), nullable=True, index=True)

    # Response Details
    response = Column(Text, nullable=False)
    sources = Column(JSONB, nullable=False, default=list)  # Array of {chapter, section, quote}

    # Metrics
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    response_time_ms = Column(Integer, nullable=False)
    tokens_used = Column(Integer, nullable=True)

    # Feedback
    feedback = Column(String(50), nullable=True)  # 'helpful', 'not_helpful', 'incorrect'

    # Timestamp
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="chat_messages")

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, query={self.query[:50]}..., confidence={self.confidence})>"
