"""
Chat endpoints for RAG chatbot
Handles queries and feedback
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from uuid import UUID
import logging

from backend.schemas import (
    ChatQueryRequest,
    ChatQueryResponse,
    ChatSource,
    ChatFeedbackRequest,
    ChatFeedbackResponse,
    ErrorResponse
)
from backend.models.chat_message import ChatMessage
from backend.database import get_db
from backend.services.rag_service import rag_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "",
    response_model=ChatQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Query RAG chatbot",
    description="Submit a query to the RAG chatbot and receive an answer grounded in textbook content",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid query format"},
        503: {"model": ErrorResponse, "description": "Service unavailable"}
    }
)
async def query_chatbot(
    request: ChatQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Query the RAG chatbot

    - **query**: User question (10-500 characters)
    - **selected_text**: Optional highlighted text from chapter
    - **chapter**: Optional chapter context to filter results
    - **stream**: Whether to stream response (not yet implemented)

    Returns response with sources and confidence score
    """
    try:
        # Validate query length
        if len(request.query) < 10 or len(request.query) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "InvalidQueryError",
                    "message": "Query must be between 10 and 500 characters",
                    "status": 400,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )

        # Process RAG query
        logger.info(f"Processing RAG query: {request.query[:50]}...")
        rag_result = await rag_service.query(
            query=request.query,
            chapter_filter=request.chapter,
            selected_text=request.selected_text
        )

        # Convert sources to schema format
        sources = [
            ChatSource(
                chapter=source["chapter"],
                section=source["section"],
                quote=source["quote"]
            )
            for source in rag_result["sources"]
        ]

        # Try to save ChatMessage record (optional - gracefully handle DB unavailable)
        message_id = None
        created_at = datetime.utcnow()

        try:
            chat_message = ChatMessage(
                user_id=None,  # TODO: Add authentication to get user_id
                query=request.query,
                selected_text=request.selected_text,
                chapter=request.chapter,
                response=rag_result["response"],
                sources=[{
                    "chapter": s.chapter,
                    "section": s.section,
                    "quote": s.quote
                } for s in sources],
                confidence=rag_result["confidence"],
                response_time_ms=rag_result["response_time_ms"],
                tokens_used=rag_result.get("tokens_used", 0),
                feedback=None,
                created_at=created_at
            )

            db.add(chat_message)
            await db.commit()
            await db.refresh(chat_message)

            message_id = chat_message.id
            logger.info(f"Chat message saved with ID: {message_id}")
        except Exception as db_error:
            logger.warning(f"Failed to save chat message to database: {db_error}")
            # Continue without database - generate a temporary ID
            from uuid import uuid4
            message_id = uuid4()

        # Build response
        response = ChatQueryResponse(
            id=message_id,
            query=request.query,
            response=rag_result["response"],
            sources=sources,
            confidence=rag_result["confidence"],
            response_time_ms=rag_result["response_time_ms"],
            feedback=None,
            created_at=created_at
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat query failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "ServiceUnavailable",
                "message": "The chatbot service is temporarily unavailable. Please try again later.",
                "status": 503,
                "retry_after": 30
            }
        )


@router.put(
    "/{message_id}/feedback",
    response_model=ChatFeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit feedback on chatbot response",
    description="Record user feedback on the quality of a chatbot response",
    responses={
        404: {"model": ErrorResponse, "description": "Message not found"}
    }
)
async def submit_feedback(
    message_id: UUID,
    request: ChatFeedbackRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Submit feedback on a chatbot response

    - **message_id**: UUID of the chat message
    - **feedback**: One of 'helpful', 'not_helpful', 'incorrect'

    Updates the feedback field for the message
    """
    try:
        # Find message
        result = await db.execute(
            select(ChatMessage).where(ChatMessage.id == message_id)
        )
        chat_message = result.scalar_one_or_none()

        if not chat_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "MessageNotFound",
                    "message": f"Chat message with ID {message_id} not found",
                    "status": 404
                }
            )

        # Update feedback
        chat_message.feedback = request.feedback
        await db.commit()

        logger.info(f"Feedback '{request.feedback}' recorded for message {message_id}")

        # Build response
        response = ChatFeedbackResponse(
            id=chat_message.id,
            feedback=chat_message.feedback,
            updated_at=datetime.utcnow()
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to submit feedback: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "Failed to submit feedback. Please try again.",
                "status": 500
            }
        )
