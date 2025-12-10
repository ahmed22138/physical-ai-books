# Physical AI Textbook - Backend API

FastAPI backend providing RAG chatbot, translations, and authentication for the Physical AI & Humanoid Robotics textbook.

## Features

- **RAG Chatbot**: Semantic search over textbook content with GPT-4o-mini responses
- **Vector Database**: Qdrant for fast similarity search
- **Database**: Neon PostgreSQL for structured data
- **Authentication**: JWT-based user authentication (planned)
- **Translations**: AI-powered chapter translations to Urdu (planned)
- **Subagents**: Reusable AI agents for code generation and assessments (planned)

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Database**: Neon PostgreSQL (via SQLAlchemy 2.0)
- **Vector DB**: Qdrant 1.12.1
- **AI/LLM**: OpenAI API (GPT-4o-mini + text-embedding-3-small)
- **Authentication**: JWT tokens (python-jose)
- **Deployment**: Uvicorn ASGI server

## Prerequisites

- Python 3.10+
- Neon PostgreSQL account (or local PostgreSQL)
- Qdrant instance (local or cloud)
- OpenAI API key

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env` and fill in your credentials:

```bash
cp .env .env.local  # Or just edit .env directly
```

**Required environment variables:**

- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `QDRANT_URL`: Qdrant instance URL (default: http://localhost:6333)
- `OPENAI_API_KEY`: Your OpenAI API key

### 3. Set Up Qdrant (Local Development)

```bash
docker run -p 6333:6333 qdrant/qdrant:latest
```

Or use Qdrant Cloud: https://cloud.qdrant.io/

### 4. Initialize Database

The database tables will be created automatically on first startup.

### 5. Ingest Content

Run the content ingestion script to embed lesson files:

```bash
python -m backend.ingest_content
```

This will:
- Read all MDX files from `frontend/docs`
- Chunk content into ~1000 character segments
- Create OpenAI embeddings for each chunk
- Store vectors in Qdrant

Expected output:
```
Ingestion complete!
Total files processed: 13
Total chunks ingested: 150+
```

### 6. Start the Server

```bash
# Development mode (with auto-reload)
python -m backend.main

# Or using uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: **http://localhost:8000**

## API Endpoints

### Health Check
```bash
GET /health
```

Returns status of all services (database, Qdrant, OpenAI).

### Chat Query
```bash
POST /chat
Content-Type: application/json

{
  "query": "What is forward kinematics?",
  "chapter": "week-7-kinematics",
  "selected_text": "optional highlighted text"
}
```

Returns AI-generated response with textbook sources.

### Submit Feedback
```bash
PUT /chat/{message_id}/feedback
Content-Type: application/json

{
  "feedback": "helpful"
}
```

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                  # FastAPI app entry point
├── config.py                # Environment configuration
├── database.py              # Database connection & session
├── schemas.py               # Pydantic request/response models
├── qdrant_client.py         # Qdrant vector database client
├── openai_client.py         # OpenAI API client
├── ingest_content.py        # Content embedding script
├── models/                  # SQLAlchemy models
│   ├── user.py
│   ├── profile.py
│   ├── chat_message.py
│   ├── translation.py
│   └── subagent_invocation.py
├── services/                # Business logic
│   └── rag_service.py       # RAG orchestration
├── routes/                  # API endpoints
│   ├── health.py            # Health check
│   └── chat.py              # Chat endpoints
├── middleware/              # Custom middleware (planned)
└── utils/                   # Utilities (planned)
```

## Environment Variables

See `.env` for all configuration options.

**Key variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `QDRANT_URL` | Qdrant instance URL | http://localhost:6333 |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | Chat model | gpt-4o-mini |
| `OPENAI_EMBEDDING_MODEL` | Embedding model | text-embedding-3-small |
| `QDRANT_COLLECTION_NAME` | Qdrant collection name | textbook_embeddings |
| `QDRANT_VECTOR_SIZE` | Embedding dimensions | 1536 |
| `LOG_LEVEL` | Logging level | INFO |

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black backend/

# Lint
flake8 backend/

# Type checking
mypy backend/
```

### Database Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'backend'"

Make sure you're running commands from the project root:
```bash
cd "E:\🧠 AIDD 30-Day Challenge\New-hackathon"
python -m backend.main
```

### "Connection refused" to Qdrant

Start Qdrant locally:
```bash
docker run -p 6333:6333 qdrant/qdrant:latest
```

### "OpenAI API error"

Verify your API key is set:
```bash
echo $OPENAI_API_KEY  # Mac/Linux
echo %OPENAI_API_KEY% # Windows
```

### "Database connection failed"

Check your Neon PostgreSQL connection string in `.env`.

## Deployment

### Using Docker

```bash
# Build image
docker build -t textbook-backend .

# Run container
docker run -p 8000:8000 --env-file .env textbook-backend
```

### Using Railway

```bash
railway login
railway init
railway up
```

### Using Render

Create a new Web Service and connect to your GitHub repo. Render will auto-detect FastAPI.

## License

See project root LICENSE file.

## Contributing

See project root CONTRIBUTING.md file.

## Support

For issues, please open a GitHub issue or contact the maintainers.
