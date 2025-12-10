"""
SubagentInvocation model for AI agent usage tracking
"""

from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from backend.database import Base


class InvocationStatus(str, enum.Enum):
    """Status of agent invocation"""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"


class SubagentInvocation(Base):
    """SubagentInvocation model for tracking AI agent usage"""

    __tablename__ = "subagent_invocations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Agent Details
    agent_name = Column(String(255), nullable=False, index=True)
    input_payload = Column(JSONB, nullable=False)
    output = Column(Text, nullable=False)

    # Performance Metrics
    execution_time_ms = Column(Integer, nullable=False)
    tokens_input = Column(Integer, nullable=True)
    tokens_output = Column(Integer, nullable=True)
    cost_usd = Column(Float, nullable=True)

    # Status & Error Handling
    status = Column(
        SQLEnum(InvocationStatus, name="invocation_status"),
        nullable=False,
        default=InvocationStatus.SUCCESS
    )
    error_message = Column(String(1000), nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="subagent_invocations")

    def __repr__(self):
        return f"<SubagentInvocation(id={self.id}, agent={self.agent_name}, status={self.status})>"
