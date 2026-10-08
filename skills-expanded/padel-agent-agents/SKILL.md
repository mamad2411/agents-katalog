# AGENTS.md

Agent reference for the Playtomic Agent project. See [README.md](README.md) for general info.

## Planning & Roadmap

Before starting any task, read in order:

1. [docs/product/ROADMAP.md](docs/product/ROADMAP.md) — what to build now / next / later
2. [docs/product/BACKLOG.md](docs/product/BACKLOG.md) — detailed items with acceptance criteria
3. `docs/tech/AGENT_TASK_<ID>.md` — per-task implementation spec (when one exists)

Product context (why we build what we build):
- [docs/product/STRATEGY.md](docs/product/STRATEGY.md)
- [docs/product/PRODUCT.md](docs/product/PRODUCT.md)

---

## Project Structure

```
src/playtomic_agent/
├── web/
│   ├── agent.py        # create_playtomic_agent(), _build_system_prompt()
│   └── api.py          # FastAPI POST /api/chat, SSE streaming
├── whatsapp/
│   ├── server.py       # neonize entry point, on_message handler, user_locks
│   ├── agent.py        # create_whatsapp_agent(), respond tool, WAResponse, extract_response()
│   └── storage.py      # UserStorage (SQLite), UserState dataclass
├── tools.py            # All @tool-decorated LangChain tools
├── llm.py              # Gemini instance (shared by both agents)
├── config.py           # Settings (pydantic-settings, reads .env)
├── context.py          # ContextVar per-request: language, country, timezone
├── models.py           # Club, Court, Slot pydantic models
└── client/
    ├── api.py          # PlaytomicClient
    ├── cli.py          # playtomic-agent CLI (search / slots)
    ├── utils.py        # geocoding, booking link helpers
    └── exceptions.py   # ClubNotFoundError, SlotNotFoundError, APIError, …
web/                    # React 18 + Vite frontend (port 8080, port 5001 = LangGraph Studio / debug server)
data/                   # Runtime data (gitignored)
  whatsapp_session.db   # neonize SQLite session (auto-created)
  whatsapp_users.db     # per-user WhatsApp state (auto-created, SQLite)
tests/                  # pytest suite
```

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `LLM_PROVIDER` | no | `gemini` | LLM backend: `gemini` or `nvidia` |
| `GEMINI_API_KEY` | if provider=gemini | — | Google Gemini API key |
| `NVIDIA_API_KEY` | if provider=nvidia | — | NVIDIA API key (`nvapi-…`) |
| `NVIDIA_BASE_URL` | no | — | Base URL for a self-hosted NVIDIA NIM |
| `DEFAULT_MODEL` | no | provider default | Override model ID (e.g. `meta/llama-3.3-70b-instruct`) |
| `DEFAULT_TIMEZONE` | no | `Europe/Berlin` | Agent timezone |
| `PLAYTOMIC_API_BASE_URL` | no | `https://api.playtomic.io/v1` | Playtomic API base |
| `WHATSAPP_SESSION_DB` | WhatsApp only | `data/whatsapp_session.db` | neonize session file |
| `WHATSAPP_STORAGE_PATH` | WhatsApp only | `data/whatsapp_users.db` | per-user state file (SQLite) |

## Commands

```bash
# Run web backend
uvicorn playtomic_agent.web.api:app --reload --port 8082

# Run WhatsApp agent (scan QR on first run)
whatsapp-agent
LOG_LEVEL=DEBUG whatsapp-agent

# Tests & quality
pytest tests/ -v
ruff format src/ tests/
ruff check src/ tests/
mypy src/

# CLI (test tools without agent)
playtomic-cli search --name "Lemon Padel"
playtomic-cli slots --club-slug lemon-padel-club --date 2026-02-25 --json
```

## Architecture

### Web Channel

```
Frontend (React) → POST /api/chat (FastAPI)
  → set_request_region() [ContextVar]
  → create_playtomic_agent(profile, language).stream()
  → SSE events: tool_start | tool_end | message | profile_suggestion | suggestion_chips | error
```

### WhatsApp Channel

```
WhatsApp → neonize on_message handler
  → UserStorage.load(sender_id)           # load history + profile + language
  → create_whatsapp_agent(profile, lang)
  → asyncio.to_thread(agent.invoke(...))  # offload sync call
  → set_wa_invocation_state(user_state)  # ContextVar injection for update_user_profile
  → extract_response() / extract_final_text() (fallback)
  → UserStorage.save()
  → _dispatch_wa_response() / wa_client.send_message()
```

Concurrency: per-user `asyncio.Lock` in `user_locks` dict prevents overlapping replies.
neonize runs its own asyncio loop (`event_global_loop`) in a daemon thread.

## Web vs. WhatsApp Agent

| | Web (`web/agent.py`) | WhatsApp (`whatsapp/agent.py`) |
|---|---|---|
| Tools | full set incl. `suggest_next_steps` | core tools only; no `suggest_next_steps` |
| Output | Markdown | **plain text only** |
| Language | per-request `ContextVar` | detected on first msg, persisted in `UserState.language` |
| Profile storage | browser `localStorage` | `data/whatsapp_users.db` (SQLite) |
| Response mode | SSE streaming | single `send_message()` after full invoke |

## Tools (`tools.py`)

| Tool | Purpose |
|------|---------|
| `find_slots` | Main tool — club + date + filters → available slots |
| `find_clubs_by_location` | Geocoding + nearby club search |
| `find_clubs_by_name` | Fuzzy name match with retry |
| `create_booking_link` | Generate Playtomic booking URL |
| `update_user_profile` | Persist a user preference (key/value) |
| `suggest_next_steps` | Emit clickable suggestion chips (web only) |
| `is_weekend` | Check if a date falls on a weekend |

To add a tool: define with `@tool` + `Annotated` params in `tools.py`, add to `TOOLS` list in the relevant `agent.py`.

## User Profile Keys

`preferred_club_slug`, `preferred_club_name`, `preferred_city`, `court_type`, `duration`, `preferred_time`

Web: stored in `localStorage` key `padel-agent-profile`.
WhatsApp: stored in `UserState.profile` → `data/whatsapp_users.db` (SQLite).

## Exceptions (`client/exceptions.py`)

| Exception | Meaning |
|-----------|---------|
| `ClubNotFoundError` | Club not found by slug or name |
| `MultipleClubsFoundError` | Name search returned >1 club |
| `SlotNotFoundError` | No slots match filters |
| `APIError` | Playtomic API 4xx/5xx |

## Patterns & Gotchas

- **ContextVars, not globals** — use `get_language()`, `get_country()`, `get_timezone()` from `context.py` for per-request data.
- **Tool return values** — must be structured `dict`/`list`, not plain strings.
- **Message history** — capped at last 20 messages in both channels.
- **Ruff line length** — 100 chars (not 120). Break lines early.
- **MyPy** — enabled but LangChain/LangGraph packages are exempt. Use `Annotated` for tool params; avoid `# type: ignore` (prefer `pyproject.toml` overrides).
- **Booking URLs** — `time.replace(':', '%3A')` required (handled in `client/utils.py`).
- **WhatsApp language detection** — agent calls `update_user_profile("language", "<code>")` on first message; the WA-specific tool mutates `UserState.language` directly via ContextVar so it persists across sessions.

## Git Conventions

### Branching Strategy

```
feature/fix/… branch
        │
        ▼  PR (CI must pass)
    staging  ──── auto-deploy ──▶  Railway "test" environment
        │
        ▼  PR (CI must pass + manual approval in GitHub)
      main   ──── deploy (gated) ─▶  Railway "production" environment
```

- **Feature work**: always branch off `staging` (`feat/`, `fix/`, `refactor/`, `docs/`, `chore/`). Never branch off `main` directly.
- **Staging**: merge feature branches → `staging` via PR. CI must be green. Triggers auto-deploy to Railway `test`.
- **Production**: merge `staging` → `main` via PR. Requires CI + manual approval of the GitHub `production` environment. Only then does Railway `production` get deployed.
- **Do not push directly** to `staging` or `main` — always use PRs.
- **Merge method**: ALWAYS use **merge commit** (never squash, never rebase) when merging into `staging` or `main`. Squash commits on `staging` create diverged history that breaks the subsequent `staging` → `main` merge.

### Pre-Push Checklist
Before every `git push`, run the following and verify each item:

```bash
git status          # working tree is clean, no unexpected staged/unstaged files
git log --oneline -5  # correct commits on the correct branch
git diff origin/<base-branch>...HEAD -- <changed files>  # diff looks exactly as intended
ruff check src/     # lint passes
```

Also check for **silent merge artifacts**: if you rebased onto a branch that received commits after your branch diverged, inspect the merged result of changed files — git auto-merge can silently inject lines from the other branch into your functions (e.g. a `_url_unquote` call re-appearing inside a function that no longer uses it). The CI GitHub Actions creates a synthetic merge commit, so the file it tests may differ from your local file.

### Conventional Commits
Always use conventional commits (e.g., `feat(scope): description`, `fix:`, `docs:`, `refactor:`).

### Attribution
When the agent is the sole author of a commit:
  - Prefix the commit title with `🤖 `.
  - Add a `Co-Authored-By` trailer: `Co-Authored-By: AI Agent <noreply@agent>`.

Pre-commit hooks run automatically on commit (ruff + mypy).

### One-Time GitHub Setup
Branch Protection unter `Settings → Branches`:
- **`main`** — "Require a pull request before merging" + "Require status checks to pass" (CI-Job)
- **`staging`** — optional: PR-Pflicht empfohlen

Railway deploys per nativer GitHub-Integration (kein Token nötig):
- `staging`-Branch → Railway `staging`-Environment (auto-deploy)
- `main`-Branch → Railway `production`-Environment (auto-deploy nach Merge)

## Documentation

- **Keep it Current**: Update `README.md` and `AGENTS.md` after every major change.
- **Completeness**: Ensure new features (Tools, CLI commands, API endpoints) are documented in the relevant sections of `AGENTS.md`.
