# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Project Management MVP: a Kanban board app with an AI chat sidebar that can create/edit/move cards. Single Dockerized app — Next.js frontend statically exported and served by FastAPI at `/`, port `8000`, SQLite storage. See `docs/PLAN.md` for the full staged implementation plan and `docs/SCHEMA.md` for the approved database schema.

MVP scope, by design: hardcoded login (`user`/`password`), one board per user, in-memory sessions (cleared on restart), local SQLite. Do not "fix" these as bugs.

## Commands

### Frontend (`frontend/`)

```bash
npm install
npm run dev              # Next.js dev server on :3000
npm run lint             # ESLint
npm run test:unit        # Vitest unit/component tests
npm run test:unit:watch  # Vitest watch mode
npx vitest run path/to/file.test.ts   # run a single test file
npm run test:coverage    # Vitest with coverage (diagnostic only, not a gate)
npm run build            # Next.js build; must succeed as a static export
npm run test:e2e         # Playwright, against the dev server (or packaged app on :8000 before release)
npm run test:all         # test:unit + test:e2e
```

### Backend (`backend/`)

Uses a local `.venv` (Python 3.9) with `fastapi`, `uvicorn`, `httpx`, `pytest` from `requirements.txt`.

```bash
cd backend
source .venv/bin/activate
pytest                        # all backend tests
pytest tests/test_main.py -k test_name   # a single test
uvicorn app.main:app --reload --port 8000   # run backend directly (serves ./app/static if present)
```

### Full app (Docker)

```bash
scripts/start-mac.sh   # or start-linux.sh / start-windows.ps1
scripts/stop-mac.sh    # or stop-linux.sh / stop-windows.ps1
```

These build the image with `docker build -t pm-app .` and run it with `--env-file .env`, publishing port `8000`. No Docker Compose. The Dockerfile builds the frontend static export first (`frontend/out`), then copies it into `backend/app/static` for FastAPI to serve.

Required env vars (root `.env`, backend-only): `OPENAI_API_KEY`, optional `OPENAI_MODEL` (default `gpt-4.1`), optional `OPENAI_BASE_URL`/`OPENAI_TIMEOUT_SECONDS`, optional `DATABASE_PATH` (defaults to `backend/data/app.db`). Optional `SESSION_COOKIE_SECURE=true` marks the session cookie `secure` when serving over HTTPS. `backend/app/__init__.py` loads the root `.env` at package import, so a local `uvicorn` run picks it up without exporting anything; real environment variables take precedence, so the container's `--env-file` still wins.

## Architecture

### Request flow and layering (backend)

`backend/app/main.py` holds all FastAPI routes and is intentionally thin: it does auth/session handling and delegates everything else. Two service modules do the real work, both raising `BoardError(status_code, detail)` on failure, which routes convert to `HTTPException` via `handle_board_error`:

- `board_service.py` — all direct CRUD on the board (get/rename/create/update/move/delete), each function opening its own `get_connection()`, checking ownership (`_owned_board_id`) and `expected_version` (`_check_version`), mutating, then bumping the board version (`_touch_board`) and returning a freshly reloaded `BoardResponse`.
- `chat_service.py` — parses/validates the OpenAI structured JSON response (`parse_model_output`) and applies the returned operation list (`apply_operations`) inside a single transaction, reusing `board_service`'s private helpers. It fuzzy-matches cards by normalized title when the model doesn't supply an exact `card_id` (see `_normalize_title`) — this exists because the model doesn't always echo IDs verbatim.

`database.py` owns the SQLite connection lifecycle: `get_connection()` is a context manager that creates the DB file/tables if missing (`initialize_database`, idempotent via `INSERT OR IGNORE`/`CREATE TABLE IF NOT EXISTS`), enables `PRAGMA foreign_keys`/WAL, seeds the MVP user + demo board, and commits/rolls back automatically. Every mutation path in `board_service`/`chat_service` opens a fresh connection via this context manager rather than sharing one.

Session state (`sessions: dict[str, tuple[str, float]]` in `main.py`, mapping token to `(user_id, expires_at)`) is process memory, not persisted — a restart logs everyone out. There's no user ID in the DB schema tying to arbitrary API input; every route resolves `user_id` from the signed cookie via `current_user`, and every board query is scoped by it.

### Storage vs. API shape

SQLite is normalized (`users`, `boards`, `columns`, `cards`, with integer `position` for ordering — see `docs/SCHEMA.md`). The API always reconstructs the frontend's `BoardResponse` shape (`columns: [{id, title, cardIds}]`, `cards: {id: {id, title, details}}`) from ordered rows in `get_board`; JSON is a view, not the source of truth. Card moves and AI-driven reordering renumber the *entire* board's cards through temporary negative positions to avoid unique-constraint collisions mid-update (see the "park rows" comments in `board_service.move_card` and `chat_service.apply_operations`).

### Optimistic concurrency

`boards.version` increments on every successful mutation. Mutation endpoints and chat accept `expected_version`; a mismatch raises `409` (`BoardError(409, ...)`). The frontend (`src/lib/api.ts`) passes the current version on every mutating call and reconciles its local board from the response rather than trusting client-side state.

### AI chat operations (`POST /api/chat`)

The backend sends the full current board JSON, the user's message, and the last 20 history entries to OpenAI with a JSON-mode prompt instructing exactly `{"message": "...", "operations": [...]}`. Allowed operation types: `rename_column`, `create_card`, `update_card`, `move_card`, `delete_card`. `chat_service.apply_operations` independently validates every operation (ownership, referenced IDs, required fields) before applying anything — malformed or unauthorized operations reject the whole request without touching the DB (see `parse_model_output` and the per-type validation in `apply_operations`). Never trust or forward model output as-is.

### Frontend structure

- `src/lib/kanban.ts` — board domain types (`BoardData`) and pure transformations (ID creation, card movement math). Keep pure logic here, not in components.
- `src/lib/api.ts` — the only place that calls backend endpoints (`fetch` with `credentials: "include"`); throws `ApiError` with the backend's `detail` message.
- `src/components/KanbanBoard.tsx` — top-level board state/orchestration, drag-and-drop (dnd-kit), reconciles with backend after mutations.
- `src/components/ChatWidget.tsx` — floating AI chat; owns its own message history and triggers a board refresh when `/api/chat` reports `updated: true`.
- `src/components/AuthGate.tsx` — gates the board behind sign-in; persists signed-in state across refreshes until logout.
- The frontend builds as a Next.js **static export** (`output: "export"` in `next.config.ts`) and must never depend on a Next.js server at runtime or expose provider (OpenAI) config/credentials — those stay server-side only.

## Conventions (from AGENTS.md files and docs/PLAN.md)

- Keep it simple: no over-engineering, no speculative abstractions, no unneeded defensive programming.
- When debugging, find the root cause before patching — don't guess-and-check.
- No emojis anywhere in code, docs, or commits.
- Integration tests should exercise the real FastAPI + SQLite boundary with an isolated database (backend tests use a `tmp_path`-based `DATABASE_PATH` via an autouse fixture — see `backend/tests/test_main.py`); component/unit tests should mock the backend and AI calls. Coverage is a diagnostic, not a release gate.
- Color palette (Tailwind/CSS vars in `src/app/globals.css`): accent yellow `#ecad0a`, blue primary `#209dd7`, purple secondary `#753991`, dark navy `#032147`, gray text `#888888`.
