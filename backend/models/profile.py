"""
Profile model for user personalization
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from backend.database import Base


class ExperienceLevel(str, enum.Enum):
    """Experience level enum"""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    EXPERT = "Expert"


class Profile(Base):
    """Profile model for user personalization"""

    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Background Questions
    software_experience = Column(
        SQLEnum(ExperienceLevel, name="experience_level"),
        nullable=False,
        default=ExperienceLevel.BEGINNER
    )
    hardware_experience = Column(Boolean, nullable=False, default=False)

    # Personalization Settings
    personalization_level = Column(
        SQLEnum(ExperienceLevel, name="personalization_level"),
        nullable=False,
        default=ExperienceLevel.BEGINNER
    )
    preferred_language = Column(String(10), nullable=False, default="en")

    # Progress Tracking
    completed_chapters = Column(ARRAY(String), nullable=True, default=list)

    # Timestamps
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Profile(user_id={self.user_id}, level={self.personalization_level}, lang={self.preferred_language})>"
