# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Goal

A self-hosted Python MCP server that gives Claude full read/write access to a personal Outlook account (hotmail.com / Microsoft personal account) via the Microsoft Graph API. Runs persistently on an Ubuntu server behind a Cloudflare Tunnel, accessible over HTTPS.

The project spec is in [agent-projects/Outlook MCP Server — Project Spec.md](agent-projects/Outlook%20MCP%20Server%20%E2%80%94%20Project%20Spec.md).

## Architecture

```
Claude clients (Claude Code / claude.ai / Cowork on Windows laptop)
        │  HTTPS (Streamable HTTP MCP transport)
        ▼
Cloudflare Tunnel
        ▼
Ubuntu Server — Python MCP Server (FastMCP, port 8000)
        │  Microsoft Graph API (OAuth2 via MSAL)
        ▼
Personal Outlook account
```

**Key components:**
- `server.py` — FastMCP server; registers all tools at startup based on scope toggles. Contains `BearerAuthMiddleware` (Starlette) and all MCP tool definitions inline as decorated closures.
- `config.py` — `Settings(BaseSettings)` via pydantic-settings; loads `.env` automatically.
- `auth/oauth_flow.py` — One-time browser auth to get initial OAuth tokens
- `auth/token_store.py` — Encrypted (Fernet) token persistence + silent MSAL refresh
- `graph/client.py` — `GraphClient` wrapper; `get_graph_client()` factory used at module level in `server.py`
- `graph/mail.py`, `graph/calendar.py`, `graph/contacts.py`, `graph/tasks.py` — Domain-specific Graph API operations
- `run_auth.py` — Standalone script; run once on first setup to authenticate
- `deploy/` — systemd unit file + Cloudflare Tunnel setup notes
- `.env` — Secrets and scope toggles (gitignored); see `.env.example`

**Important: no `src/` directory** — all Python modules live at the repo root. Packages are `auth/` and `graph/`. `server.py`, `config.py`, and `run_auth.py` are top-level scripts.

## Critical Implementation Notes

**MSAL authority URL** — personal Microsoft accounts (`@hotmail.com`, `@outlook.com`) require:
```python
authority="https://login.microsoftonline.com/consumers"
```
Using `common` or `organizations` will fail silently for personal accounts.

**Scope toggle system** — `.env` contains `SCOPE_MAIL_READ`, `SCOPE_CALENDAR_WRITE`, etc. On startup, `server.py` reads these and registers only enabled tool groups. Log which tools were registered and which were skipped.

**Tool registration pattern** — Tools are defined as async closures inside `if settings.scope_*:` blocks in `server.py`, decorated with `@mcp.tool()`. They delegate to `graph/*.py` functions and catch `RuntimeError` → `ValueError` for MCP error surfacing. The module-level `gc` (GraphClient) is captured by closure.

**Graph API pagination** — Graph returns 10–50 items by default. All list tools must handle `@odata.nextLink` pagination transparently.

**Datetime** — All inputs/outputs use ISO 8601 with timezone. Graph API uses UTC internally.

**Error handling** — Surface Graph API errors as meaningful MCP tool errors, not raw stack traces.

**OAuth redirect capture** — `run_auth.py` must spin up a temporary `http://localhost:8400` server to capture the redirect automatically. No manual code copy-pasting.

**Token cache** — File at `TOKEN_CACHE_PATH` must be `chmod 600`, owned by the service user.

**Bearer auth** — Every MCP request must include `Authorization: Bearer {MCP_API_KEY}`. Return HTTP 401 for missing/invalid tokens.

## Virtual Environment

**Always activate before running Python commands:**
```bash
. venv/bin/activate
```

"Module not found" errors mean the venv is not activated.

## Common Commands

```bash
# Setup
python3 -m venv venv && . venv/bin/activate
pip install --upgrade pip && pip install -e '.[dev]'
pre-commit install

# Run the MCP server (requires .env configured)
uvicorn server:app --host 0.0.0.0 --port 8000

# One-time auth setup (opens browser)
python run_auth.py

# Tests
pytest                          # all tests
pytest tests/test_mail.py       # single file
pytest -k "test_list_emails"    # pattern match
pytest -v --cov=. --cov-report=term  # verbose with coverage

# Code quality
make check-all                  # all checks at once (format, lint, type, security, test)
make fix                        # auto-fix format + lint
ruff check --fix .
mypy config.py auth/ graph/     # type check (no src/ dir — modules at root)
bandit -r config.py auth/ graph/ -s B404,B603,B607  # security scan
```

## Code Quality Standards

All code must pass `make check-all` before commit:
1. **Formatting**: `ruff format` (100-char line length)
2. **Linting**: `ruff check` (includes isort, bandit security rules, bugbear, etc.)
3. **Type checking**: `mypy` (configured in `pyproject.toml`; `pyright` configured in `pyrightconfig.json` but not in `make check-all`)
4. **Security**: `bandit` with `-s B404,B603,B607` skips
5. **Tests**: all pass; `pytest-asyncio` with `asyncio_mode = "auto"`. Coverage target: 80% (currently ~59%; `fail_under = 55` in `pyproject.toml` as a floor).

Pre-commit hooks run: trailing-whitespace, end-of-file-fixer, check-yaml/toml/json, detect-private-key, ruff (lint+format), mypy, bandit.

For unavoidable suppressions: `# noqa: <code>`, `# type: ignore[<code>]`, `# nosec` — always add a justification comment.

## Testing Notes

**`conftest.py` `pytest_configure` hook** — `server.py` executes `Settings()` and `get_graph_client()` at module level during import. `tests/conftest.py` patches these before collection so tests run without real Azure credentials. This means `server` module is always pre-imported with all scope toggles set to `False`.

**Async tests** — `asyncio_mode = "auto"` in `pyproject.toml`, so async test functions run automatically without `@pytest.mark.asyncio`.

**Test markers**: `slow`, `integration`, `unit` — deselect slow tests with `-m "not slow"`.

## File Organization

| Folder | Purpose | Git |
|--------|---------|-----|
| `agent-tmp/` | Scratch/debug/intermediates (auto-deleted after 7 days) | No |
| `agent-projects/<project>/` | Active implementation plans | Yes |
| `docs/` | Permanent documentation | Yes |
| `docs/_generated/` | Auto-generated — do not edit manually | Yes |

- Do not create planning documents in the project root.
- Use `agent-tmp/` for all temporary work.
- Plans in `agent-projects/<name>/plan.md` need frontmatter: `status`, `owner`, `created`, `summary`.

## Deployment (Ubuntu Server)

1. `systemd` service in `deploy/outlook-mcp.service` — auto-start on boot, restart on failure
2. Cloudflare Tunnel pointing to `localhost:8000` — provides TLS, no port forwarding needed
3. Add to Claude Code: `claude mcp add --transport http outlook-mcp https://<tunnel-url>/mcp --header "Authorization: Bearer YOUR_MCP_API_KEY"`

## Out of Scope

- Multi-user support
- Attachment upload/download (metadata is fine)
- Calendar sharing / delegate access
- Push notifications / webhooks
