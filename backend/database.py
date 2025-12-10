"""
Database connection and session management
Uses SQLAlchemy with async support for Neon PostgreSQL
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
from backend.config import settings

# Create declarative base for models
Base = declarative_base()

# Create async engine
if settings.is_development:
    # Use NullPool for development (no connection pooling)
    engine = create_async_engine(
        settings.get_database_url(async_driver=True),
        echo=settings.debug,
        poolclass=NullPool,
    )
else:
    # Use connection pooling for production
    engine = create_async_engine(
        settings.get_database_url(async_driver=True),
        echo=settings.debug,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
    )

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session

    Usage in FastAPI:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Try to commit, but gracefully handle if session already rolled back
            try:
                await session.commit()
            except Exception:
                # Session may already be rolled back from error handling in route
                await session.rollback()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database - create all tables

    Call this on application startup
    """
    async with engine.begin() as conn:
        # Import all models here to ensure they're registered
        from backend.models.user import User
        from backend.models.profile import Profile
        from backend.models.chat_message import ChatMessage
        from backend.models.translation import Translation
        from backend.models.subagent_invocation import SubagentInvocation

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Close database connections

    Call this on application shutdown
    """
    await engine.dispose()
