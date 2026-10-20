# GitHub Copilot instructions — Terminal-2

**Read [`../AGENTS.md`](../AGENTS.md) first, then [`../PROJECT_BIBLE.md`](../PROJECT_BIBLE.md).**
`AGENTS.md` is the canonical multi-agent entry point; this file is the Copilot-specific pointer to it.
The full operator lockdown lives in `../CLAUDE.md §1–3` — where anything disagrees, `CLAUDE.md` wins.

## Never suggest code that:
- Adds a non-GET call, or removes/weakens `ALLOWED_HTTP_METHODS` / `_assert_readonly_method()`, in any
  `*_client.py` broker client (they are GET-only *by construction* — a price/inventory/order mutation is
  a security-CRIT change; `scripts/check_readonly.py` + `tests/test_readonly_guards.py` fail the build).
- Mutates prod data — `INSERT`/`UPDATE`/`DELETE`/DDL, `apply_migration`, cron changes, `vault.*`/`auth.*`/
  `cron.*` touches — without the operator explicitly authorizing it. Reads are always fine.
- Writes across a lane boundary silently (see the lane map in `AGENTS.md`), or creates a new root `*.md`
  (the canonical doc set is CLOSED — registry in `README.md`).
- Uses raw `innerHTML` outside the shared S4K lib (ESLint bans it — `npm run lint:all`).

## Before proposing a commit
Product code (`server.py`, `core/`, `routers/`, `d2_dashboard`, `*_client.py`, `render_webhook.py`) is
held at **100% line + branch coverage** — new code needs tests. Run the gate:
`AUTH_DISABLED=true SUPABASE_URL=https://example.invalid SUPABASE_SERVICE_ROLE_KEY=test-key TEVO_TOKEN=test TEVO_SECRET=test PYTHONPATH=. pytest tests/ --cov --cov-branch --cov-fail-under=100`
