# Cline Context Rules — Customer Support Agent

## Project Overview
A multi-agent customer support system using Retrieval-Augmented Generation (RAG) with DeepSeek LLM, ChromaDB vector store, and FastAPI backend.

## Architecture

### Agent Pipeline (in order)
1. **RouterAgent** — Intent classification (billing/shipping/technical/account/product/general) + sentiment analysis (positive/neutral/negative) + priority assignment
2. **RetrievalAgent** — Embeds query → searches ChromaDB → evaluates result relevance → optionally falls back to Tavily web search
3. **ResponseAgent** — Synthesizes answer from retrieved context + citations. Returns JSON with reply, confidence, followups, escalation flags
4. **QualityAgent** — Reviews response for hallucination risk, accuracy, tone, completeness. Pass/fail with confidence score
5. **EscalationAgent** — Creates support ticket in SQLite DB if confidence < 0.7 or quality check fails

### Tech Stack
- **Backend**: FastAPI (Python 3.10+)
- **LLM**: DeepSeek API (OpenAI-compatible, `deepseek-chat` model)
- **Vector Store**: ChromaDB (local persistence in `data/chromadb/`)
- **Embeddings**: sentence-transformers (`all-MiniLM-L6-v2`) — local, no API key needed
- **Database**: SQLite via SQLAlchemy (`data/support.db`)
- **Frontend**: Server-rendered HTML (Jinja2 templates in `app/ui/templates/`)

### Key Files
- `app/agents/base_agent.py` — Base LLM agent with `llm_call()`, `llm_call_stream()`, `llm_call_json()`
- `app/agents/orchestrator.py` — Coordinates the 5-agent pipeline. Entry point is `process_message()` and `process_message_stream()`
- `app/api/chat.py` — FastAPI endpoints: `POST /api/chat`, `POST /api/chat/stream`
- `app/rag/vector_store.py` — ChromaDB wrapper (uses `collection_name = "knowledge_base"`)
- `app/rag/embeddings.py` — SentenceTransformer encoder
- `app/rag/knowledge_loader.py` — Ingests `.md` files from `data/knowledge_base/` into ChromaDB
- `app/config.py` — All config from `.env` (API keys, model names, thresholds)
- `app/models/db_models.py` — SQLAlchemy models: `SupportTicket`, `ConversationLog`, `KnowledgeDoc`
- `app/models/schemas.py` — Pydantic models: `ChatRequest`, `ChatResponse`, `TicketCreate`, etc.
- `data/knowledge_base/` — Markdown files organized by category (account, billing, shipping, technical)

### Key Features Implemented
- **Conversation history/memory** — Per-session in-memory context with summarization (`app/context/memory.py`)
- **Document Upload** — Upload PDF/MD/TXT files via admin dashboard, auto-extract, chunk, embed into ChromaDB
- **Auth + Multi-Tenant** — JWT login/register, Tenant/User models, admin login UI, tenant-scoped data isolation
- **Embeddable Widget** — Script-tag embeddable chat widget with suggestion bubbles and followup chips
- **Enterprise Demo Page** — Full landing page showcasing widget integration
- **Testing** — 64 tests across 6 files covering config, models, ticket system, memory, and API
- **Pipeline visualization** — SSE streaming shows each agent stage in real-time

### Missing / Not Yet Implemented
- **Docker** — No containerization setup
- **CI/CD** — No pipeline configured
- **Agent Pipeline Visualization** — Visual pipeline in the UI

### Configuration (.env)
- `DEEPSEEK_API_KEY` — Required for LLM calls
- `DEFAULT_LLM_PROVIDER` / `DEFAULT_LLM_MODEL` — LLM config
- `EMBEDDING_PROVIDER` / `EMBEDDING_MODEL` — Embedding config (default: sentence-transformers/all-MiniLM-L6-v2)
- `AGENT_CONFIDENCE_THRESHOLD` — Escalation threshold (default: 0.7)
- `TAVILY_API_KEY` — Optional, for web search fallback

### Coding Conventions
- `snake_case` for Python functions/variables
- `PascalCase` for classes
- Type hints used throughout
- Pydantic for API schemas, SQLAlchemy for DB models
- FastAPI route handlers use `async def` where possible
- Orchestrator is a singleton managed by `get_orchestrator()` in `app/api/chat.py`
- All agents inherit from `BaseAgent`
- Config values come from `app.config` module (not direct env var access)

### Common Gotchas
- DeepSeek uses OpenAI-compatible API — `openai` Python package with custom `base_url`
- `llm_call_json()` uses `response_format={"type": "json_object"}` — requires DeepSeek API support
- ChromaDB persists to `data/chromadb/` — if vector store gets corrupted, delete the directory and re-ingest
- The quality agent runs a review AFTER response generation — can cause escalations even when response is good
- Session IDs are currently only used for logging, not for conversations state

### Current State (as of July 2026)
- Core agent pipeline: Complete and working
- RAG with ChromaDB: Complete
- Web fallback (Tavily): Implemented
- Admin dashboard: Basic implementation exists
- Streaming responses: Implemented via SSE
- Conversation memory: NOT implemented (each call is stateless)