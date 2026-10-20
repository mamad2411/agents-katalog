---
description: Terminal-2 operator lockdown + lane discipline for any Cursor agent
alwaysApply: true
---

# Terminal-2 — read AGENTS.md first

Canonical multi-agent rules: `@AGENTS.md`, then `@PROJECT_BIBLE.md`. Full lockdown: `CLAUDE.md §1–3`
(that file wins on any conflict). This `.mdc` is the Cursor-specific pointer.

## Hard rules (every lane, non-negotiable)
1. **SQL read-only by default.** `SELECT`/`information_schema`/`pg_*`/logs/`list_*`/`get_*` are free.
   Prod mutation (`INSERT`/`UPDATE`/`DELETE`/DDL, `apply_migration`, cron changes, `vault.*`/`auth.*`/
   `cron.*`) needs explicit operator authorization. Authoring a migration file is fine; applying it is gated.
2. **Upstream broker APIs read-only.** Every `*_client.py` is GET-only by construction
   (`ALLOWED_HTTP_METHODS = frozenset({"GET"})` + `_assert_readonly_method()`). Never remove, weaken, or
   widen those tokens — it's a security-CRIT change caught by `scripts/check_readonly.py` +
   `tests/test_readonly_guards.py`. No order/hold/price/inventory writes, ever.
3. **Stay in your lane.** Free rein on UI/wiring within your routed lane; never write across lanes
   silently (even logs/caches). Lane map + ownership: `PROJECT_BIBLE.md §2`.

## Repo conventions
- Canonical docs are a CLOSED set (registry in `README.md`). Never create a new root `*.md`.
- Product code held at 100% line + branch coverage — new code needs tests.
- No raw `innerHTML` outside the shared S4K lib (ESLint-enforced).
- Gates are server-side (`--no-verify` can't skip): `bash bin/check-docs.sh`,
  `python scripts/check_readonly.py`, `npm run lint:all`, and the pytest coverage ratchet.
