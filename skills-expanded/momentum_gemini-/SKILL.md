# Project Context for Cursor AI

This project follows the detailed instructions in `.github/instructions/copilot-instructions.md`.

Please refer to that file for complete project context, architecture, and coding guidelines.

## Quick Reference

**Project**: Momentum — AI-Based Student Productivity Assistant

**Tech Stack**:
- Frontend: React + Vite, TailwindCSS, shadcn/ui
- Backend: Node.js (Express) + Prisma ORM + PostgreSQL
- AI Service: FastAPI (Python) + Gemini API + ChromaDB + LangChain

**Key Rules**:
- Backend orchestrates Frontend ↔ AI ↔ Postgres (never direct AI calls from backend)
- AI Service handles all AI reasoning and ChromaDB operations
- Frontend only calls Express backend (never AI service directly)
- Use Prisma for all database operations
- Always return structured JSON from AI endpoints

For complete details, see: `.github/instructions/copilot-instructions.md`

## 📚 Documentation & Context7 Usage

**CRITICAL**: Always use Context7 MCP tools to check official documentation before implementing features:

1. **Before implementing any LangChain feature**:
   - Use `mcp_Context7_resolve-library-id` to find the library ID
   - Use `mcp_Context7_get-library-docs` to get up-to-date documentation
   - Examples: "langchain", "chromadb", "google-genai", "fastapi"

2. **Before implementing ChromaDB operations**:
   - Check ChromaDB documentation via Context7 for latest API patterns
   - Verify embedding dimensions and collection management

3. **Before implementing Gemini API calls**:
   - Check Google GenAI SDK documentation via Context7
   - Verify model names, API structure, and response formats

4. **Always verify**:
   - Package versions match documentation
   - API patterns are current (not deprecated)
   - Best practices from official docs

**Why Context7**: Ensures you're using the latest, correct patterns and avoiding deprecated APIs.

## 🧠 LangChain & ChromaDB Implementation Guide

Since the user is learning LangChain and ChromaDB, always:

1. **Use LangChain for document processing**:
   - Text splitters for chunking documents
   - Document loaders for various file types
   - Chain patterns for RAG (Retrieval Augmented Generation)

2. **Use ChromaDB for vector storage**:
   - Store embeddings with metadata (user_id, type, timestamp)
   - Query with filters for user-specific retrieval
   - Use proper collection management

3. **Integration Pattern**:
   ```
   Document → LangChain Text Splitter → Embeddings (Gemini) → ChromaDB → Retrieval → RAG Chain
   ```

4. **Always explain** what each LangChain/ChromaDB component does when implementing

See `momentum-ai/AI_IMPLEMENTATION_GUIDE.md` for detailed examples and patterns.

## 🧪 Test Credentials

**ALWAYS use these test credentials for development and testing:**
- **Email**: `test@example.com`
- **Password**: `test123`

Use these credentials when:
- Testing authentication endpoints
- Creating test users
- Running integration tests
- Demonstrating features
- Debugging authentication issues

## Terminal & OS Rules

- Before running any command, explicitly check and set the working directory.
  - Prefer `Get-Location` to confirm, and `Set-Location`/`cd` to change.
- Before attempting to start any dev server or backend/AI service, first ask the user if it is already running and which ports are in use. Do not start processes without explicit confirmation.
- For the `momentum-ai` service:
  - Ensure the Python 3.11 virtual environment is created at `momentum-ai\.venv`.
  - Always activate the venv in the current terminal before running any Python-related tasks:
    - `cd momentum-ai`
    - `\.venv\Scripts\Activate.ps1`
  - If the venv is not active, activate it first; do not proceed with Python or uvicorn commands until active.
  - Use uvicorn with:
    - `uvicorn ai_service:app --reload --port 8001`
