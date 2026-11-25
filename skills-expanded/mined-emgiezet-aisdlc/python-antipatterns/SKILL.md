---
name: python-antipatterns
description: Forbidden Python patterns — SQL injection, shell injection, unsafe deserialization, missing timeouts, blocking async calls. Applies when editing Python files.
paths: ["**/*.py"]
user-invocable: false
---

# Python anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-PY-SEC-001 — Pass params as second arg to `execute()`; never build SQL with f-strings or `%`.
- AP-PY-SEC-002 — Use `subprocess.run(['prog', arg1], shell=False)`; never `shell=True` with user input.
- AP-PY-SEC-003 — Use `json` for data exchange; replace `yaml.load` with `yaml.safe_load`.
- AP-PY-SEC-005 — Never use `verify=False`; supply a CA bundle path for internal PKI.
- AP-PY-SEC-007 — Replace `eval`/`exec` with a lookup dict or a safe parser; never eval user input.

## Errors
- AP-PY-SEC-004 — Always pass an explicit `timeout=` to `requests.get` and `httpx.get`.
- AP-PY-SEC-006 — Use `secrets.token_hex()` or `secrets.token_urlsafe()` for all security tokens.
- AP-PY-PERF-001 — Use `select_related`/`prefetch_related` (Django) or `selectinload`/`joinedload` (SQLAlchemy).
- AP-PY-PERF-002 — In `async def`, use `httpx.AsyncClient`, `asyncio.sleep`, and `aiofiles`; never block.
- AP-PY-MAINT-001 — Catch the narrowest exception; log and re-raise; never `except: pass`.
- AP-PY-MAINT-002 — Use `None` as default and initialise mutable defaults inside the function body.

Details for any ID: `reference/<ID>.md`
