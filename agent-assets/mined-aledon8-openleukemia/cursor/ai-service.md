---
description: Python FastAPI AI-service rules
globs:
  - "ai-service/**/*.py"
alwaysApply: false
---

# AI Service Rules

- Keep FastAPI route handlers thin; put reusable behavior in `app/domains`.
- Use explicit Pydantic request and response models.
- Preserve strict typing and keep `python -m mypy app` clean.
- Use `response_model` for route outputs.
- Treat extraction and model outputs as explainable signals or candidate data, not clinical decisions.
- Run `python -m ruff check .` and relevant `python -m pytest` tests for Python changes.
