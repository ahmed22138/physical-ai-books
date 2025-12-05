# Physical AI & Humanoid Robotics: Embodied Intelligence in the Real World

An AI-native interactive textbook built with Docusaurus, FastAPI, RAG chatbot, and advanced AI features including personalization, multi-language support, and reusable AI agents.

## Project Overview

This project delivers a comprehensive educational platform for learning Physical AI and Humanoid Robotics through:

- **12 interactive lessons** covering 4 core modules (Introduction, Perception, Control, Integration)
- **RAG-powered chatbot** for content-based Q&A with semantic search
- **AI-native interactive components** (code generators, assessment creators, visualizers)
- **Personalized learning** adapted to user background and expertise level
- **Multi-language support** including Urdu translation
- **Reusable AI agents** for code generation, assessments, and diagrams

## Tech Stack

### Frontend
- **Framework**: Docusaurus 3 + MDX
- **Deployment**: GitHub Pages
- **Styling**: Tailwind CSS with dark mode
- **Components**: React with custom interactive elements

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: Neon PostgreSQL
- **Vector Store**: Qdrant
- **LLM**: OpenAI API (ChatKit, GPT-4)
- **Authentication**: Better-Auth
- **Deployment**: Railway/Render

### Tools & Services
- **Vector Embeddings**: OpenAI text-embedding-3-small
- **Translations**: OpenAI GPT-4
- **Agents**: Claude subagents via OpenAI API
- **Authentication**: Better-Auth with JWT

## Directory Structure

```
.
├── frontend/                          # Docusaurus frontend
│   ├── docs/                          # Lesson content (MDX)
│   │   ├── 01-introduction/           # Module 1
│   │   ├── 02-perception/             # Module 2
│   │   ├── 03-control/                # Module 3
│   │   ├── 04-integration/            # Module 4
│   │   └── resources/                 # Hardware, glossary, etc.
│   ├── src/
│   │   ├── components/                # React components (ChatBot, etc.)
│   │   ├── css/                       # Styling
│   │   └── pages/                     # Custom pages
│   ├── static/                        # Images, fonts, etc.
│   ├── sidebars.js                    # Sidebar configuration
│   ├── docusaurus.config.js           # Docusaurus config
│   └── package.json
│
├── backend/                           # FastAPI backend
│   ├── models/                        # Database models
│   ├── services/                      # Business logic
│   ├── routes/                        # API endpoints
│   ├── middleware/                    # Authentication, CORS, etc.
│   ├── config/                        # Configuration
│   ├── main.py                        # FastAPI app entry point
│   └── requirements.txt
│
├── specs/                             # Design specifications
│   └── 1-ai-textbook/                 # Feature specs and plans
│       ├── spec.md                    # Feature specification
│       ├── plan.md                    # Implementation plan
│       ├── tasks.md                   # Task breakdown
│       ├── data-model.md              # Database schema
│       └── contracts/                 # API contracts
│
├── .github/workflows/
│   └── deploy.yml                     # GitHub Pages CI/CD
│
├── .env.example                       # Environment template
├── .gitignore
└── README.md
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- Git
- Cloud accounts (Neon, Qdrant, OpenAI, Railway/Render)

### Frontend Setup

```bash
cd frontend
npm install
npm run start        # Local development on http://localhost:3000
npm run build        # Build for production
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload  # Local development on http://localhost:8000
```

### Environment Configuration

1. Copy `.env.example` to `.env`
2. Fill in all required variables:
   - Database URL (Neon PostgreSQL)
   - Qdrant URL and API key
   - OpenAI API key
   - GitHub Pages settings
   - Other service credentials

### Deployment

**Frontend (GitHub Pages)**:
```bash
cd frontend
npm run build
# Push to main branch - GitHub Actions handles deployment
```

**Backend (Railway/Render)**:
- Connect git repo to Railway or Render
- Set environment variables
- Deploy automatically on push

## Features

### Phase 1: Core Learning (Days 1-8)
- ✅ 12 interactive lessons (60+ pages)
- ✅ Learning outcomes per chapter
- ✅ 30+ formative assessments (quizzes, prompts)
- ✅ 4 summative module assessments
- ✅ Capstone project with rubric
- ✅ Hardware requirements table (5 options)

### Phase 2: RAG Chatbot (Days 9-12)
- ✅ FastAPI backend with REST API
- ✅ Qdrant vector embeddings for all chapters
- ✅ OpenAI ChatKit integration
- ✅ `/chat` endpoint with source citations
- ✅ Selected text query support
- ✅ Chat component embedded in lessons

### Phase 3: Bonus Features (Days 13-16)

**Better-Auth + Personalization (Day 14-15)**:
- ✅ User signup with background questions
- ✅ Profile storage in Neon PostgreSQL
- ✅ Personalization button per chapter
- ✅ Content complexity toggle (Beginner → Expert)

**Reusable Subagents (Day 13)**:
- ✅ ROS 2 code generator
- ✅ Assessment generator
- ✅ Diagram generator

**Urdu Translation (Day 16)**:
- ✅ `/translate` endpoint
- ✅ Translation caching (14-day TTL)
- ✅ "Translate to Urdu" button on all chapters
- ✅ Language toggle UI

## API Endpoints

### Chatbot
- `POST /chat` - Query RAG chatbot
- `PUT /chat/{id}/feedback` - Submit feedback

### Authentication
- `POST /auth/signup` - Create account
- `POST /auth/signin` - Login
- `GET /user/profile` - Get user profile
- `PUT /user/profile/personalization` - Update preferences

### Translations
- `POST /translate` - Translate chapter to target language

### Agents
- `POST /agent/invoke` - Call AI subagent

### Health
- `GET /health` - Service health check

## Performance Targets

- **Site Load**: <3 seconds (Time to First Byte)
- **Chatbot Response**: <2 seconds
- **Translation**: <5 seconds (first request, cached after)
- **Concurrent Users**: 100+ without degradation
- **Cross-browser**: 95% compatibility (Chrome, Firefox, Safari)

## Testing

```bash
# Frontend E2E tests
cd frontend
npm run test

# Backend unit tests
cd backend
pytest tests/

# All tests
make test
```

## Documentation

- `specs/1-ai-textbook/spec.md` - Feature specification
- `specs/1-ai-textbook/plan.md` - Implementation plan
- `specs/1-ai-textbook/tasks.md` - Task breakdown
- `specs/1-ai-textbook/data-model.md` - Database schema
- `ARCHITECTURE.md` - Architecture decisions (coming soon)
- `DEPLOYMENT.md` - Deployment guide (coming soon)

## Contributing

See `CONTRIBUTING.md` for development workflow and guidelines.

## License

This project is educational and open-source. See LICENSE file for details.

## Support

- 📚 [Docusaurus Docs](https://docusaurus.io)
- 🚀 [FastAPI Docs](https://fastapi.tiangolo.com)
- 🔍 [Qdrant Docs](https://qdrant.tech/documentation/)
- 🤖 [OpenAI API Docs](https://platform.openai.com/docs)

## Team

Built with 🤖 Claude Code as part of the AIDD 30-Day Challenge Hackathon.

---

**Status**: Phase 1 Setup Complete ✅
**Next**: Phase 2 Content Creation (Days 3-8)
