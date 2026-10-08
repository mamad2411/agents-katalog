# MV Face Recognition - AI Agent Guidelines

## Build/Test/Lint Commands

**Python (Root & Backend):**
- `uv run pytest` - Run all tests (use uv as per .clinerules)
- `uv run pytest tests/test_specific.py::test_function` - Run single test
- `uv run black .` - Format code with Black
- `uv run isort .` - Sort imports
- `uv run flake8 .` - Lint code 
- `uv run mypy .` - Type checking

**Frontend (Svelte):**
- `cd frontend && npm run lint` - ESLint + Prettier check
- `cd frontend && npm run format` - Auto-format with Prettier
- `cd frontend && npm run check` - Type check with svelte-check
- `cd frontend && npm run build` - Production build

**MVP Processor:**
- `cd mvp-processor && npm test` - Run Vitest tests
- `cd mvp-processor && npm run test:e2e` - Playwright E2E tests
- `cd mvp-processor && npm run lint` - ESLint check

## Code Style Guidelines

**Python:** Follow PEP 8, use type hints, document functions with docstrings. Import order: stdlib, third-party, local (`from src.core.detector import FaceDetector`). Use numpy arrays for face processing, logging for errors.

**TypeScript/Svelte:** Use strict TypeScript, camelCase naming, reactive statements with `$:`, stores for state (`dashboardStats`, `contestantsStore`). Import from `$lib/` for components and utilities.

**Error Handling:** Python - use logging module, TypeScript - proper try/catch with meaningful messages.

**Use uv and pyproject.toml for Python dependency management** (per .clinerules)
