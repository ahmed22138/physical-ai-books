"""
Configuration management for Physical AI Textbook Backend
Loads environment variables and provides typed settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "Physical AI Textbook API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # Database (Neon PostgreSQL)
    database_url: str = "postgresql://user:password@localhost:5432/textbook"
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Qdrant Vector Database
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "textbook_embeddings"
    qdrant_vector_size: int = 1536  # OpenAI text-embedding-3-small dimension

    # OpenAI API
    openai_api_key: str = "sk-..."
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 1000

    # Authentication & Security
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60  # 1 hour
    jwt_refresh_expiration_days: int = 7  # 7 days

    better_auth_secret: Optional[str] = None

    # Password Hashing
    bcrypt_rounds: int = 12

    # CORS
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Rate Limiting
    rate_limit_chat: int = 100  # requests per minute per user
    rate_limit_translate: int = 50
    rate_limit_agent: int = 20

    # Caching
    cache_ttl_chat: int = 3600  # 1 hour
    cache_ttl_translation: int = 1209600  # 14 days
    redis_url: Optional[str] = None

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Content Path
    content_path: str = "../frontend/docs"

    # API Keys for External Services (if needed)
    railway_api_token: Optional[str] = None
    render_api_key: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def get_database_url(self, async_driver: bool = False) -> str:
        """Get database URL with optional async driver"""
        if async_driver and "postgresql://" in self.database_url:
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://")
        return self.database_url

    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Uses lru_cache to ensure settings are loaded only once
    """
    return Settings()


# Export singleton instance
settings = get_settings()
