# Project Guide

## Product constraints

- Read `product-spec.md` before changing behavior or scope.
- Keep Cardinal a single-board, local-first MVP.
- Preserve `openapi.yaml` as the contract between frontend and backend.
- Use React and TypeScript in `frontend/`.
- Use FastAPI, SQLAlchemy, SQLite, and uv in `backend/`.

## Commands

- `make install` — install frontend and backend dependencies.
- `make test` — run all test suites.
- `make frontend` — start the frontend development server.
- `make backend` — start the backend on port 8091.

## Development rules

- Centralize network calls in `frontend/src/services/cards.ts`.
- Keep database access behind SQLAlchemy sessions; do not add SQLite-specific queries.
- Add or update tests whenever behavior changes.
- Run the full test suite before committing.
- Keep commits focused and do not commit generated databases or dependency folders.

