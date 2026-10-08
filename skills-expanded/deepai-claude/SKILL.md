# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Install dependencies
uv sync

# Create .env file from template
cp .env.example .env
# Then add your ANTHROPIC_API_KEY
```

### Running the Application
```bash
# Quick start (recommended)
./run.sh

# Manual start
cd backend && uv run uvicorn app:app --reload --port 8000

# Access points
# - Web interface: http://localhost:8000
# - API docs: http://localhost:8000/docs
```

### Development Workflow
```bash
# Run with auto-reload for development
cd backend && uv run uvicorn app:app --reload --port 8000

# Clear ChromaDB data (useful for testing document processing)
rm -rf backend/chroma_db

# Test API endpoint manually
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is MCP?", "session_id": null}'
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run only API tests
uv run pytest -m api

# Run specific test file
uv run pytest backend/tests/test_api.py

# Run with coverage (if pytest-cov installed)
uv run pytest --cov=backend

# See backend/tests/README.md for detailed testing documentation
```

## Architecture Overview

### System Flow: Query Processing
The RAG system follows a multi-stage pipeline:

1. **Frontend** (script.js) → Sends query + session_id to `/api/query`
2. **FastAPI** (app.py) → Creates/retrieves session, delegates to RAG System
3. **RAG System** (rag_system.py) → Orchestrates the entire process:
   - Retrieves conversation history from Session Manager
   - Calls AI Generator with tools available
4. **AI Generator** (ai_generator.py) → **Two-stage Claude interaction**:
   - **First call**: Claude decides whether to use search tool
   - **Tool execution**: If needed, searches via Tool Manager → Vector Store → ChromaDB
   - **Second call**: Claude generates final answer using search results
5. **Response** → Returns answer + sources through the chain back to frontend

### Key Architectural Patterns

#### Two-Stage AI Response Generation
The system uses a **tool-calling pattern** where Claude makes two API calls:
- Call 1: Claude analyzes query and decides to use `search_course_content` tool
- Tool executes: Semantic search in ChromaDB returns relevant chunks
- Call 2: Claude receives search results and generates contextual answer

#### Dual-Collection ChromaDB Structure
```
ChromaDB (./chroma_db)
├── course_catalog    # Course metadata (title, instructor, lessons JSON)
└── course_content    # Text chunks with embeddings (800 chars, 100 overlap)
```

#### Session-Based Conversation Management
Sessions track conversation history (max 4 messages = 2 exchanges) to maintain context across multiple queries. Session IDs are generated on first query and returned to frontend for subsequent requests.

### Core Components

**RAG System (rag_system.py)**
- Entry point for all query processing
- Orchestrates: Document Processor → Vector Store → AI Generator → Session Manager
- Handles document ingestion from `/docs` directory on startup
- Returns tuple: (answer: str, sources: List[str])

**Vector Store (vector_store.py)**
- Manages two ChromaDB collections with different purposes
- Resolves fuzzy course names using semantic search on catalog
- Performs filtered semantic search on content chunks
- Uses `all-MiniLM-L6-v2` for embeddings

**AI Generator (ai_generator.py)**
- Wraps Anthropic Claude API with tool execution support
- Implements two-stage response pattern (tool_use → tool_result → final)
- System prompt enforces: concise responses, single search per query, no meta-commentary
- Temperature: 0 (deterministic), Max tokens: 800

**Tool Manager (search_tools.py)**
- Registry pattern for tool definitions
- `CourseSearchTool`: Semantic search with course name resolution and lesson filtering
- Tracks sources from last search for frontend display
- Returns formatted results: `[Course Title - Lesson N]\nContent...`

**Document Processor (document_processor.py)**
- Parses structured format: Course metadata → Lesson markers → Content
- Chunking strategy: Sentence-based, 800 chars, 100 char overlap
- Adds contextual prefixes: `"Course X Lesson Y content: [chunk]"`
- Supported formats: .txt, .pdf, .docx

**Session Manager (session_manager.py)**
- In-memory session storage (resets on server restart)
- Maintains sliding window of recent messages (configurable via MAX_HISTORY)
- Formats history as: `"User: question\nAssistant: answer"`

### Configuration (config.py)
Key parameters that affect system behavior:
```python
CHUNK_SIZE: 800          # Characters per chunk
CHUNK_OVERLAP: 100       # Overlap between chunks
MAX_RESULTS: 5           # Search results returned
MAX_HISTORY: 2           # Conversation exchanges kept
EMBEDDING_MODEL: "all-MiniLM-L6-v2"
ANTHROPIC_MODEL: "claude-sonnet-4-20250514"
```

## Document Processing

### Expected Document Format
```
Line 1: Course Title: [title]
Line 2: Course Link: [url]
Line 3: Course Instructor: [instructor]
Line 4+: Content with lesson markers

Lesson 0: Introduction
Lesson Link: https://...
[Content for lesson 0]

Lesson 1: Getting Started
[Content for lesson 1]
```

### Adding New Documents
1. Place `.txt`, `.pdf`, or `.docx` files in `/docs` directory
2. Restart server (documents are auto-loaded on startup)
3. Check logs for: `"Added new course: [title] (X chunks)"`

### Document Processing Pipeline
```
Read file → Parse metadata → Extract lessons → Chunk text (sentence-based)
→ Add context prefixes → Generate embeddings → Store in ChromaDB
```

## API Endpoints

### POST /api/query
**Purpose**: Process user questions with RAG
**Request**:
```json
{
  "query": "What is MCP?",
  "session_id": "session_1"  // null for new session
}
```
**Response**:
```json
{
  "answer": "MCP (Model Context Protocol) is...",
  "sources": ["Course Title - Lesson 0"],
  "session_id": "session_1"
}
```

### GET /api/courses
**Purpose**: Get course statistics
**Response**:
```json
{
  "total_courses": 4,
  "course_titles": ["Course 1", "Course 2", ...]
}
```

## Frontend Architecture

**Technology**: Vanilla JavaScript with marked.js for Markdown rendering

**Key State**:
- `currentSessionId`: Tracks conversation session across queries
- Maintained across page lifecycle, resets on page reload

**Message Flow**:
1. User types → `sendMessage()` → POST /api/query
2. Shows loading spinner while waiting
3. Receives response → Renders markdown answer + collapsible sources
4. Saves session_id for next query

## Common Modification Patterns

### Changing Chunk Size/Overlap
Edit `backend/config.py`:
```python
CHUNK_SIZE: int = 1000    # Larger chunks = more context per search result
CHUNK_OVERLAP: int = 200  # More overlap = better context preservation
```
Then clear ChromaDB and restart: `rm -rf backend/chroma_db && ./run.sh`

### Adding New Search Parameters
1. Update `CourseSearchTool.get_tool_definition()` in `search_tools.py`
2. Add parameter to `execute()` method
3. Pass to `vector_store.search()`
4. Update `VectorStore._build_filter()` to handle new parameter

### Modifying AI System Prompt
Edit `AIGenerator.SYSTEM_PROMPT` in `ai_generator.py`. This affects:
- How Claude decides when to search
- Response tone and formatting
- Tool usage patterns

### Customizing Search Results
Edit `CourseSearchTool._format_results()` in `search_tools.py` to change:
- Result formatting (currently: `[Course - Lesson]\nContent`)
- Source citation format
- Number of results displayed

## Important Notes

- **ChromaDB persistence**: Stored in `backend/chroma_db/` (not in version control)
- **Sessions are ephemeral**: In-memory only, reset on server restart
- **Document deduplication**: System checks existing course titles before re-processing
- **Tool usage limit**: System prompt enforces max 1 search per query for efficiency
- **No authentication**: This is a development/demo system without auth layers
- **CORS enabled**: `allow_origins=["*"]` for development convenience
- **Testing framework**: Comprehensive test suite in `backend/tests/` with 28+ API tests, fixtures, and mocks

## Prerequisites

- Python 3.13+
- uv package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Anthropic API key with sufficient credits
- For Windows: Use Git Bash for shell commands
