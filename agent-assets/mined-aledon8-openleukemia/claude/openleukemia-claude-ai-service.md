# AI Service Instructions

This directory contains the FastAPI service for Python-native workloads: ML inference, document extraction, OCR or parsing workflows, model-facing APIs, and compute-heavy jobs.

## Commands

Run from `ai-service/`:

```sh
python -m uvicorn app.main:app --reload
python -m ruff check .
python -m pytest
python -m mypy app
```

## Rules

- Keep route handlers thin and focused on HTTP concerns.
- Put reusable behavior in `app/domains/` services and schemas.
- Use explicit Pydantic request and response models.
- Preserve strict typing and keep `mypy app` clean.
- Treat extraction results as candidate data until validated or confirmed.
- Keep generated explanations non-diagnostic and patient-safe.
- For endpoint changes, define the request/response contract and tests before broad implementation.
