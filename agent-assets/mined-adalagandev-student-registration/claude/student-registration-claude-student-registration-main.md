
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A small full-stack student-registration app whose real purpose is to **refresh React skills**. The code is intentionally written as study material — see `frontend/src/App.jsx`, which opens with a React keyword/syntax glossary. This shapes how you should edit it (see Conventions).

- **Frontend:** React 18 + Vite, plain JavaScript (no TypeScript).
- **Backend (active):** Java 17 + Spring Boot + Spring Data JPA + SQLite, in `backend-java/`. **This is the backend to use going forward** — new backend work happens here. It serves the API on port 5000.
- **Backend (legacy reference):** the original Python + Flask + SQLite app in `backend/` (single file, no ORM). The Java backend (SR-106) is a faithful 1:1 port of it; `backend/` is kept only as a reference and is no longer the default. Both read the same `backend/students.db` and `backend/uploads/`, so run only ONE at a time — default to Java.

## Commands

Two processes, run in separate terminals from their own directories.

**Backend — Java (primary)** (from `backend-java/`, needs JDK 17+ and Maven):
```powershell
mvn spring-boot:run              # serves http://localhost:5000 (working dir is backend-java/)
mvn -q -DskipTests package       # build a runnable fat jar into target/
mvn test                         # run the JUnit + MockMvc API-parity suite
```

**Backend — Python (legacy reference, optional)** (from `backend/`):
```powershell
python -m venv venv ; venv\Scripts\Activate.ps1   # optional, first time
pip install -r requirements.txt
python app.py        # serves http://localhost:5000, debug auto-reload on
```
Run either the Java OR the Python backend, not both — they share port 5000 and the same `backend/students.db` + `backend/uploads/`. **Default to Java.** `mvn spring-boot:run` uses `backend-java/` as its working directory, which is why `application.properties` resolves the DB at `../backend/students.db`.

**Frontend** (from `frontend/`):
```powershell
npm install          # first time
npm run dev          # serves http://localhost:5173 (Vite)
npm run build        # production build into frontend/dist/
npm run preview      # serve the built dist/ locally
```

The frontend expects the backend running on port 5000 (hardcoded in `frontend/src/api.js`). There is **no test runner and no linter** configured — do not invent `npm test`/`npm run lint`.

## Architecture

**Backend (`backend-java/`) — Spring Boot, the active backend (SR-106):**
- Layered, not single-file: `web/` controllers (thin) → `service/` (all business logic + validation) → `repository/` (Spring Data JPA) → `entity/` (`@Entity` mapped to the existing snake_case columns via `@Column(name=...)`). `dto/` holds the wire shapes; `StudentDto.from()` is the camelCase boundary (the `row_to_dict()` equivalent).
- SQLite lives in `backend/students.db`; uploaded PDFs in `backend/uploads/<student_id>/` (paths from `application.properties`). Two tables: `students` and `documents` (FK to student). The `documents` row records both the stored on-disk name and the original display name.
- **Schema migration** is Hibernate `ddl-auto=update` (in `application.properties`), which creates/adds missing tables/columns and leaves existing data untouched. Add a new student field to the `Student` entity + `StudentDto` (the camelCase boundary) — Hibernate adds the column.
- **All errors go through `web/GlobalExceptionHandler`**, which emits exactly `{"error": "<msg>"}` — the frontend calls `response.json()` unconditionally and reads `error`, so no error path may return non-JSON. Services throw `web/ApiException(status, msg)`.
- **Server is the source of truth for validation and `registeredAt`** — never trust client-supplied values. Program changes are gated: `/api/students/<id>/program-change` requires `multipart/form-data` with 1–2 PDFs (≤25 MB each). Fidelity details that are easy to break live in `service/`: `Timestamps.nowUtcSeconds()` (UTC, seconds, no `Z`), `FileStorageService.secureFilename()` (werkzeug port) + timestamp-prefixed stored name, and `ProgramChangeService`'s validation ORDER (program/file checks return 400 **before** the student-existence 404). The per-file 25 MB check is done in app code (400), so multipart `max-file-size` is deliberately left at 55 MB.
- The JUnit + MockMvc suite in `src/test/java/` locks in the API contract; run `mvn test`.

**Backend (`backend/app.py`) — legacy Flask reference (no longer the default):**
- The original single-file Flask app the Java backend was ported from. Keep it working for reference/comparison, but do new backend work in `backend-java/`.
- One Flask module with all routes under `/api/...`; a fresh `sqlite3` connection per request (`get_connection`). `init_db()` is the schema path (`CREATE TABLE IF NOT EXISTS` + `PRAGMA table_info` → `ALTER TABLE ... ADD COLUMN`). `row_to_dict()` is the snake_case→camelCase conversion point. Behavior is mirrored 1:1 by the Java backend above.

**Frontend (`frontend/src/`):**
- `api.js` is the **only** place that talks to the backend — all `fetch` calls live there. Components never call `fetch` directly; add a new function here when adding an endpoint.
- `App.jsx` owns all state (student list, status message, active tab, which student is being edited) and passes data + callbacks down as props. Children are presentational: `StudentForm`, `StudentList`, `EditStudentModal`, and the reusable `Modal`.
- State updates are **immutable** (spread/`.map`/`.filter`, never mutation) so React re-renders — follow this pattern.
- `Modal.jsx` renders via `createPortal` into `document.body`. The edit flow has two independent actions: contact-detail edits (`PUT`) and a gated program change (`POST` multipart). Program-change uses `FormData` and deliberately sets **no `Content-Type` header** (the browser must add the multipart boundary).

## Conventions specific to this repo

- **Match the heavy teaching-comment style.** Existing files explain syntax and "why" at a tutorial level; new code should be commented to the same density, and JS/React keywords are often documented inline. Don't strip these comments when editing.
- **Stable, descriptive `id` attributes** are present on essentially every rendered element (e.g. `tab-register`, `student-row-{id}`, `edit-program-submit-btn`), used as handles to target elements in later requests. When adding markup, give it an id following the existing `block-element` / interpolated-`{id}` naming so the set stays complete and unique.
- Theme is driven by CSS custom properties in `frontend/src/styles.css` (`:root` tokens + layered `--surface`/`--surface-2`/`--surface-3`). Re-theme by changing tokens rather than scattering colors.
   
## Agent-driven development

Feature and change work is delegated to the specialist subagent that owns the domain — that agent **writes** the code; the main agent coordinates and handles code outside these domains:

- Service / business-logic classes (`service/`, use-cases, DI, transactions, DTO/domain mapping) → **service-warden**
- API error/exception handling, status-code mapping, validation errors → **exception-warden**
- Unit and integration tests → **test-warden**

A feature that spans domains is split so each agent authors its own layer. Invoke these agents proactively when a prompt lands in their domain — not only for after-the-fact review.

### Authorship stamp

Every class or function an agent authors or substantially rewrites carries an authorship tag on the line directly above its declaration, using the file's line-comment syntax:

```
// @agent: service-warden      (Java / JS)
# @agent: exception-warden        (Python)
```

Keep the tag on edits; change it only when a different agent takes the code over. See `docs/agent-driven-development.md` for rationale and setup details.

## Branch & commit workflow

All work is ticket-driven (`SR-<number>` keys in `bug.md`): every code change is
tied to a ticket, made on a `SR-<n>-<short-desc>` branch off `main`, and committed
with an `SR-<n> ...` message. **This workflow is owned and enforced by the
`ticket-warden` agent** (`.claude/agents/ticket-warden.md`) — invoke it before any
code change to create/assign the ticket and branch. A `.githooks/commit-msg` hook
is the hard backstop that rejects non-`SR-<n>` commits (enable once per clone with
`git config core.hooksPath .githooks`).
