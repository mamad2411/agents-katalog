# CLAUDE.md

Instructions for Claude Code when working with this PDF Viewer POC.

## Project Overview

PDF viewer POC built with React 19.1 and FastAPI. Core features:
- Full-text PDF search with highlighting
- Remote PDF loading via URL
- Form field extraction with ground truth comparison
- 50MB file size limit

## Tech Stack

**Frontend**
- React 19.1 + TypeScript
- Material UI v7
- PDF.js
- Vite

**Backend**
- FastAPI (Python 3.11+)
- UV package manager
- Pydantic v2
- System dependency: `libmagic`

## Code Standards

### Python (Backend)

**DO:**
- Use modern syntax: `X | Y` unions, `datetime.UTC`
- Apply decorators for logging: `@log_api_call()`, `@log_file_operation()`
- Use Pydantic v2 computed fields and validators
- Maintain correlation ID propagation across requests
- Keep all code lint-free (ruff, mypy)

**Example API endpoint pattern:**
```python
@log_api_call("operation_name", log_params=True, log_response=True)
@log_file_operation("upload", file_param="file")
async def endpoint_name(...):
    # Implementation
```

**DON'T:**
- Use deprecated syntax (`Union[X, Y]`, `datetime.utcnow()`)
- Skip type hints
- Commit secrets or credentials

### TypeScript/React (Frontend)

**DO:**
- Ensure React 19 Strict Mode compatibility (handle double-renders)
- Use TypeScript strict mode
- Follow Material UI v7 patterns
- Keep all code lint-free (ESLint, TypeScript compiler)

**DON'T:**
- Use deprecated React patterns
- Skip type definitions
- Hardcode environment-specific values

### Testing & Quality

**Before ANY commit:**
1. Run backend tests: `cd backend && uv run pytest`
2. Run frontend tests: `cd frontend && npm test`
3. Check linting: Both backend and frontend must pass
4. Verify zero type errors: `mypy` (backend), `tsc --noEmit` (frontend)

**Pre-commit hooks are enforced** - ensure all checks pass locally.

## Git Workflow

**Branch:** Always use `main` as the primary branch (GitHub default).

**Branch Management:**
- **Primary Branch**: `main` (NOT `master`) - GitHub default branch
- Use only `main` as primary branch
- All feature branches should branch from and merge back to `main`
- Delete merged feature branches immediately
- Keep branch lists clean and minimal
- Use short-lived feature branches (days/weeks, not months)

**Branch hygiene:**
- Keep branches short-lived (days/weeks, not months)
- Delete merged branches immediately
- Minimize active branch count

## Key Files & Locations

**Backend:**
- `backend/app/api/load_url.py` - URL loading endpoint
- `backend/app/decorators.py` - Logging decorators
- `backend/app/models/` - Pydantic models

**Frontend:**
- `frontend/src/hooks/usePDFSearch.ts` - Search functionality
- `frontend/src/components/TestPDFLoader.tsx` - PDF loader component
- `frontend/src/components/PDFViewer/PDFExtractedFields.tsx` - Form extraction UI

**Configuration:**
- Debug logging enabled by default
- CORS: ports 5173-5176
- Environment variables: See [TECHNICAL.md](docs/TECHNICAL.md)

## Additional Documentation

- **Setup & Commands**: [TECHNICAL.md](docs/TECHNICAL.md)
- **Architecture**: [TECHNICAL.md](docs/TECHNICAL.md#project-structure)
- **API Reference**: FastAPI auto-docs at `/docs` endpoint

---

**Author:** Dominic Fahey (domfahey@gmail.com)
**License:** MIT