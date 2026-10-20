# AGENTS.md — rules for ANY coding agent working in this repo

This file exists because **agents other than Claude Code do not auto-load [`CLAUDE.md`](CLAUDE.md).**
If you are Copilot, Codex, Cline, Continue, Cursor, or any other agent: **read this file first**,
then read [`PROJECT_BIBLE.md`](PROJECT_BIBLE.md) before writing anything. The rules below are a
faithful mirror of the operator lockdown in `CLAUDE.md §1–3`; that file remains the canonical source —
where they ever disagree, `CLAUDE.md` wins.

> **Doc version:** v1.0.0 (2026-07-13) — initial multi-agent entry pointer. Mirrors `CLAUDE.md §1–3`
> (hard rules) + the lane map, so agents that don't auto-load `CLAUDE.md` inherit the same guardrails.
> Companion configs: `.github/copilot-instructions.md` (Copilot) · `.cursor/rules/terminal2.mdc` (Cursor).

---

## The three hard rules (non-negotiable, every lane)

**1. SQL data is read-only by default.**
Read freely: `SELECT`, `information_schema`, `pg_*`, logs, MCP `list_*`/`get_*`. **Ask the operator
first** before any `apply_migration`, `INSERT`/`UPDATE`/`DELETE`/DDL on prod, cron schedule changes,
data-mutating edge-function deploys, or any touch to `vault.*` / `auth.*` / `cron.*`. Authoring a
migration *file* under `supabase/migrations/` is fine; **applying** it to prod is separately gated.

**2. Upstream third-party APIs are read-only.**
Applies to every broker client (`*_client.py`: TEvo/EVO, SeatGeek, SeatData, TickPick, Vivid, …).
GET/search/read endpoints only. **Forbidden without explicit operator authorization:** order creation,
holds/locks/reservations, any write/mutation, webhook or account config changes, and — absolutely —
**any price or inventory change to a listing source.** Each client is GET-only *by construction*:
`ALLOWED_HTTP_METHODS = frozenset({"GET"})` + `_assert_readonly_method()` that raises on any non-GET.
**Never remove, weaken, re-inline-then-weaken, or widen those tokens** — `scripts/check_readonly.py`
(CI) and `tests/test_readonly_guards.py` fail the build if you do. This is a security-CRIT surface.

**3. Stay in your lane.**
You have free rein on HTML/JS/UI wiring *within the lane you were routed to* — build and refactor
without per-step approval. But **never write across lanes silently** — even cache files or logs count.
If your change must touch another lane's surface: propose via PR comment to the owner, or surface a
`flag` in `bot_chat`. Lane ownership lives in `PROJECT_BIBLE.md §2`.

---

## Lane map (seven peer lanes, no hierarchy)

| Lane | Surface |
|---|---|
| A1 | Data plane — DB + ingest pipeline + cross-source xref + DB security + crons |
| B1 | Build + guards + governance — CI, drift, freshness, tests, and the docs surface |
| D0 | Terminal (broker view) + orders dashboard |
| D1 | Store / storefront |
| D3 | Broadway |
| D4 | Exos / Bridge |
| D5 | Fantasy (sports FE, `static/fantasy/*`) |

Codes are **surface-ownership labels, not a chain of command** (the hierarchy is dissolved). Push to
`main` is per-task after green CI — no sole-pusher lane. Prod-DB apply is per-task under operator
direction — no central gatekeeper.

---

## Before you push — run the gates locally (they're server-side; `--no-verify` can't skip them)

| Gate | Command |
|---|---|
| Tests + 100% coverage ratchet | `AUTH_DISABLED=true SUPABASE_URL=https://example.invalid SUPABASE_SERVICE_ROLE_KEY=test-key TEVO_TOKEN=test TEVO_SECRET=test PYTHONPATH=. pytest tests/ --cov --cov-branch --cov-fail-under=100` |
| Readonly-guard audit | `python scripts/check_readonly.py` |
| Docs registry | `bash bin/check-docs.sh` |
| Canonical-doc tables | `python scripts/check_md_tables.py` |
| Frontend lint (no raw `innerHTML` outside the S4K lib) | `npm run lint:all` |

**Never create a new root `*.md`** — the canonical doc set is CLOSED (registry in `README.md`).
Add a fact to the doc that already owns it; link, don't duplicate.

## Where to look next
- **How to alternate agents cleanly** (roster, config parity, handoff protocol) → `docs/multi_agent_workflow.md`
- Full playbook, SQL macros, §3 column landmines, §5 cross-source ID architecture → `PROJECT_BIBLE.md`
- What already exists (tables/views/crons/edge fns/vault) → `RESOURCES_BIBLE.md`
- Migration filename/header/apply rules → `MIGRATION_CONVENTIONS.md`
- Build/run the D0 terminal locally → `docs/d0_terminal_build.md`
- What's actionable right now → `KANBAN.md`
