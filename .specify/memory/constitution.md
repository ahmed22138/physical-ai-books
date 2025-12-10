# Physical AI & Humanoid Robotics AI-Native Textbook Constitution

## Core Principles

### I. Embodied Intelligence First
The textbook bridges digital AI with physical robots through hands-on learning. All content must include practical robotics applications, hardware considerations, and real-world demonstrations. Theoretical concepts are paired with embodied implementations. No purely abstract material without physical AI context.

### II. Comprehensive Curriculum Coverage
Content must encompass all course modules, weekly breakdowns, learning outcomes, assessments, and hardware requirements as detailed in the hackathon specification. Each chapter maps to specific learning objectives with measurable outcomes. No gaps in required topics; all modules fully developed.

### III. AI-Native Interactive Design
The textbook leverages AI throughout: interactive Docusaurus components, RAG-powered chatbot for Q&A, personalization buttons, multi-language support (Urdu), and integrated agent-based learning tools. Static content is prohibited; all sections include interactive or AI-enhanced elements to support modern learning.

### IV. Original Content & No Plagiarism
All explanations, examples, and course materials are generated originally for this project. Content must be accurate, educationally sound, and properly attributed. AI generation is used as a tool but human expertise validates accuracy and pedagogical value.

### V. Full-Stack Bonus Architecture
Implementation targets base 100 points plus all bonuses: Docusaurus deployment to GitHub Pages, reusable subagents/agent skills, Better-Auth signup/signin with background questions, per-chapter personalization, and per-chapter Urdu translation. Each bonus feature is fully implemented and integrated.

### VI. RAG Chatbot & Knowledge Search
A FastAPI-backed RAG chatbot powered by OpenAI Agents/ChatKit uses Neon PostgreSQL and Qdrant for semantic search. Chatbot supports content-based Q&A and selected text queries, enabling learners to ask questions about specific chapters and concepts in real time.

## Technical Architecture Requirements

- **Frontend**: Docusaurus with interactive components, deployable to GitHub Pages
- **Backend**: FastAPI with OpenAI Agents/ChatKit integration
- **Database**: Neon PostgreSQL for structured data; Qdrant for vector embeddings
- **Authentication**: Better-Auth with background profile questions
- **Content Encoding**: Vector embeddings for semantic search; markdown source of truth
- **Internationalization**: Per-chapter Urdu translation support built-in

## Content Standards

- Educational accuracy: All technical claims validated against current best practices
- Accessibility: Content suitable for learners with varying robotics backgrounds
- Modularity: Each chapter is independently understandable but interconnected
- Assessments: Every module includes formative and summative assessments
- Hardware Mapping: Clear hardware requirements and alternative options documented

## Development Workflow

- Spec-Driven Development: Every feature specified before implementation
- Iterative Delivery: MVP (base 100 points) completed before bonus features
- Testing: All interactive components tested; RAG queries validated for accuracy
- Code Review: All contributions reviewed for alignment with constitution
- Documentation: Every feature includes user-facing docs and architecture notes

## Governance

All development must conform to these principles. The constitution supersedes contradictory practices. Amendments require documentation and approval before implementation. Complexity decisions (e.g., technology choices) must reference this constitution's rationale.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06

