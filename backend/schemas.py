"""
Pydantic schemas for request/response validation
Based on API contracts specification
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID


# ==================== Chat Schemas ====================

class ChatQueryRequest(BaseModel):
    """Request schema for POST /chat"""
    query: str = Field(..., min_length=2, max_length=500, description="User question or query")
    selected_text: Optional[str] = Field(None, min_length=50, max_length=5000, description="Highlighted text from chapter")
    chapter: Optional[str] = Field(None, description="Chapter context (e.g., 'week-7-kinematics')")
    stream: bool = Field(False, description="Stream response token-by-token")


class ChatSource(BaseModel):
    """Source citation from textbook"""
    chapter: str = Field(..., description="Chapter identifier")
    section: str = Field(..., description="Section within chapter")
    quote: str = Field(..., description="Relevant excerpt from textbook")


class ChatQueryResponse(BaseModel):
    """Response schema for POST /chat"""
    id: UUID = Field(..., description="Unique message ID")
    query: str = Field(..., description="Echo of original query")
    response: str = Field(..., description="Generated answer")
    sources: List[ChatSource] = Field(default_factory=list, description="Array of citation objects")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    response_time_ms: int = Field(..., description="Generation time in milliseconds")
    feedback: Optional[str] = Field(None, description="User feedback: 'helpful', 'not_helpful', or null")
    created_at: datetime = Field(..., description="ISO 8601 timestamp")


class ChatFeedbackRequest(BaseModel):
    """Request schema for PUT /chat/{message_id}/feedback"""
    feedback: str = Field(..., description="User feedback")

    @field_validator("feedback")
    def validate_feedback(cls, v):
        allowed = ["helpful", "not_helpful", "incorrect"]
        if v not in allowed:
            raise ValueError(f"Feedback must be one of: {allowed}")
        return v


class ChatFeedbackResponse(BaseModel):
    """Response schema for PUT /chat/{message_id}/feedback"""
    id: UUID = Field(..., description="Message ID")
    feedback: str = Field(..., description="Updated feedback")
    updated_at: datetime = Field(..., description="Update timestamp")


# ==================== Translation Schemas ====================

class TranslationRequest(BaseModel):
    """Request schema for POST /translate"""
    chapter_id: str = Field(..., min_length=1, description="Chapter identifier")
    language: str = Field(..., min_length=2, max_length=10, description="Target language (ISO 639-1 code)")
    force_refresh: bool = Field(False, description="Bypass cache and re-translate")


class TranslationResponse(BaseModel):
    """Response schema for POST /translate"""
    chapter_id: str = Field(..., description="Chapter identifier")
    language: str = Field(..., description="Target language code")
    content: str = Field(..., description="Translated markdown content")
    source_language: str = Field("en", description="Original language")
    cached: bool = Field(..., description="Whether response was served from cache")
    translation_model: str = Field(..., description="Model used for translation")
    created_at: datetime = Field(..., description="ISO 8601 timestamp")
    expires_at: Optional[datetime] = Field(None, description="Cache expiration timestamp")


# ==================== Subagent Schemas ====================

class SubagentInvokeRequest(BaseModel):
    """Request schema for POST /agent/invoke"""
    agent_name: str = Field(..., min_length=1, description="Agent identifier")
    context: Dict[str, Any] = Field(..., description="Agent-specific input")
    stream: bool = Field(False, description="Stream output token-by-token")


class SubagentInvokeResponse(BaseModel):
    """Response schema for POST /agent/invoke"""
    id: UUID = Field(..., description="Unique invocation ID")
    agent_name: str = Field(..., description="Agent that was invoked")
    output: str = Field(..., description="Generated output")
    execution_time_ms: int = Field(..., description="Execution time in milliseconds")
    tokens_used: int = Field(..., description="LLM tokens consumed")
    cost_usd: float = Field(..., description="Estimated API cost")
    created_at: datetime = Field(..., description="ISO 8601 timestamp")


# ==================== Authentication Schemas ====================

class SignupRequest(BaseModel):
    """Request schema for POST /auth/signup"""
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (≥8 chars)")
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    software_experience: str = Field(..., description="Software background")
    hardware_experience: bool = Field(..., description="Robot experience")

    @field_validator("software_experience")
    def validate_experience(cls, v):
        allowed = ["Beginner", "Intermediate", "Expert"]
        if v not in allowed:
            raise ValueError(f"Software experience must be one of: {allowed}")
        return v


class SigninRequest(BaseModel):
    """Request schema for POST /auth/signin"""
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints"""
    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User name")
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("Bearer", description="Token type")
    expires_in: int = Field(3600, description="Token expiration in seconds")
    created_at: Optional[datetime] = Field(None, description="Account creation timestamp")


# ==================== User Profile Schemas ====================

class ProfileResponse(BaseModel):
    """Response schema for GET /user/profile"""
    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: str = Field(..., description="User name")
    profile: Dict[str, Any] = Field(..., description="Profile data")
    created_at: datetime = Field(..., description="Account creation timestamp")


class PersonalizationUpdateRequest(BaseModel):
    """Request schema for PUT /user/profile/personalization"""
    personalization_level: str = Field(..., description="Content complexity preference")
    preferred_language: str = Field(..., min_length=2, max_length=10, description="Preferred language code")

    @field_validator("personalization_level")
    def validate_level(cls, v):
        allowed = ["Beginner", "Intermediate", "Expert"]
        if v not in allowed:
            raise ValueError(f"Personalization level must be one of: {allowed}")
        return v


class PersonalizationUpdateResponse(BaseModel):
    """Response schema for PUT /user/profile/personalization"""
    personalization_level: str = Field(..., description="Updated personalization level")
    preferred_language: str = Field(..., description="Updated language preference")
    updated_at: datetime = Field(..., description="Update timestamp")


# ==================== Health Check Schema ====================

class HealthCheckResponse(BaseModel):
    """Response schema for GET /health"""
    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Check timestamp")
    services: Dict[str, str] = Field(..., description="Status of each service (database, qdrant, openai)")
    message: Optional[str] = Field(None, description="Additional status message")


# ==================== Error Schema ====================

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error description")
    status: int = Field(..., description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
