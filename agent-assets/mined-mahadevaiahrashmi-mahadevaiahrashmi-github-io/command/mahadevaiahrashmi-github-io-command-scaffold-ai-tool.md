<!-- agent-notes: { ctx: "AI/data-centric tool scaffold workflow", deps: [CLAUDE.md], state: active, last: "sato@2026-02-12" } -->
Scaffold an AI / data-centric tool: $ARGUMENTS

You are setting up this repository as an AI or data-centric application. Follow these steps:

## 0. Template Setup

Swap the storefront README for the project placeholder, move scaffolds into place, and clean up template-only files:

```bash
# Swap README: replace storefront with project placeholder
if [ -f README-template.md ]; then
  mv README-template.md README.md
fi

# Move stub docs from scaffolds/ to docs/ root
mv docs/scaffolds/*.md docs/ 2>/dev/null
rmdir docs/scaffolds 2>/dev/null

# Remove samples directory (only useful on the template repo itself)
rm -rf samples/ 2>/dev/null

# Remove template-specific ADRs (not relevant to inheriting projects)
rm -rf docs/adrs/template/

# Remove template research/comparison docs
rm -f docs/research/how-we-compare-*.md docs/research/agent-teams-comparison.md
rm -f docs/research/squad-vs-vteam-*.md docs/research/ux-gap-analysis-*.md
rm -f docs/research/what-*-can-learn-from-*.md docs/research/what-we-learn-from-*.md
```

## 1. Gather Requirements

Ask the user to choose their tech stack. Present these options:

**API framework:**
- **FastAPI** — Async, auto-generated OpenAPI docs, great Python ecosystem (Recommended)
- **Flask** — Simpler, synchronous, huge ecosystem
- **None (library/CLI only)** — No web server needed

**Visualization / UI layer:**
- **Streamlit** — Rapid prototyping, data apps, minimal frontend code (Recommended for quick iteration)
- **Gradio** — Great for ML model demos and HuggingFace integration
- **Dash (Plotly)** — More control, production-quality dashboards
- **React frontend (separate app)** — Full custom UI, more work but more flexibility
- **None** — API-only or CLI-only, no UI needed

**AI / ML tooling (ask which apply):**
- **LLM integration** — Anthropic SDK, OpenAI SDK, LangChain, LlamaIndex, or direct API calls
- **ML framework** — PyTorch, scikit-learn, HuggingFace Transformers
- **Data processing** — Pandas, Polars, DuckDB
- **Vector store** — ChromaDB, Pinecone, pgvector, FAISS
- **None / Other** — Let the user specify

**Package / environment management:**
- **uv** (Recommended — fast, modern, handles Python versions too)
- **poetry**
- **pip + venv**

**Testing:**
- **pytest** (Recommended)
- **pytest + httpx** for async API testing (if using FastAPI)

**Additional options to ask about:**
- Do they need a database? (PostgreSQL, SQLite, Redis)
- Do they need background task processing? (Celery, ARQ, simple queue)
- Do they need containerization? (Dockerfile, docker-compose)
- CI pipeline (GitHub Actions)?
- Environment variable management? (.env with pydantic-settings)

## 2. Create an ADR

Once choices are made, create an ADR at `docs/adrs/` documenting:
- The chosen frameworks, AI/ML tools, and infrastructure
- Why these were selected
- Trade-offs

## 3. Scaffold the Project

Based on the choices, create the project structure. General shape:

### FastAPI + Visualization layer
```
src/<project_name>/
    __init__.py
    main.py             # FastAPI app factory / entry point
    api/
        __init__.py
        routes/
            __init__.py
            health.py    # Health check endpoint
    core/
        __init__.py
        config.py        # Settings via pydantic-settings
    services/
        __init__.py      # Business logic / AI pipeline modules
    models/
        __init__.py      # Pydantic models / DB models
ui/
    app.py               # Streamlit/Gradio/Dash entry point (if applicable)
tests/
    __init__.py
    conftest.py
    test_health.py
    test_services/
        __init__.py
pyproject.toml
```

### Library / pipeline only (no API)
```
src/<project_name>/
    __init__.py
    pipeline.py
    config.py
tests/
    __init__.py
    test_pipeline.py
pyproject.toml
```

### In all cases, also:
- Update `CLAUDE.md` with the chosen tech stack and conventions
- Update `README.md` with project description, architecture overview, setup instructions
- Add a `.gitignore` appropriate for Python (include common data/model file patterns)
- Add a `.env.example` with placeholder config values (never commit actual secrets)
- Create a starter test
- If Docker was requested, create `Dockerfile` and optionally `docker-compose.yml`
- If CI was requested, create `.github/workflows/ci.yml`
- Configure linting (ruff) and formatting (ruff format)
- Add agent-notes to all new files per `docs/methodology/agent-notes.md`

## 4. Verify

Install dependencies and run the test suite to confirm the scaffold works. Fix any issues.

## 5. Summary

Tell the user what was created and the key commands.
