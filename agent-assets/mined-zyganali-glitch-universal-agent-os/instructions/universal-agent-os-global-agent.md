---
applyTo: "**"
---

# Global Reusable All-Files Instructions

This file is the cross-file behavior lock for Copilot in the English locale pack.
It is intentionally richer than a shell checklist so the donor spine survives across file types and task sizes.

## Mandatory
- Read `/AGENT_OS_RULES.md` first as the package-local canonical donor source.
- Read `/AGENTS.md` and `/.github/copilot-instructions.md` before proposing or editing code.
- `/AGENTS.md` is the single source of truth.
- The root `/AGENT_OS_PLAN_TEMPLATE.md` is the canonical plan template.

## Do not continue if any of the following is missing
- an active or newly created plan in `/plans/`
- an explicit allowlist that covers the files to change
- a clear evidence and gate path for closure

## Repository rules that must be preserved or expanded, never narrowed
- `Tech-Debt Delta = 0`
- no placeholder/stub/demo completion
- no scope drift outside the allowlist
- no billing/auth/telemetry activation by default
- no offline/PWA regression
- no single-language visible UI if the repo requires parity
- no partial plan updates
- no completed plan left in `/plans/`
- use main-agent orchestration with single-writer default and `fallback-to-sequential` when needed

## Copilot-specific discipline
- Start with `MODE`, scope lock, allowlist/denylist, active plan, and first micro-phase.
- In a new repo, align with the user before freezing the roadmap portfolio.
- Write or harden the repo-root planning template before coding.
- Track discovered work explicitly instead of hiding it in prose.
- Keep shared governance, plan, and config files single-writer.

## When live behavior contradicts a static PASS
- reopen the task honestly
- record discovered work in the plan
- update task table, gates, risks, and handoff atomically

## Closure lock
- No closure while a mandatory gate is `FAIL` or `NOT_RUN` without a documented exception.
- Push/deploy/repo-sync work must obey Triple-Sync Lock.
- Completed plans move to archive in the same closure edit.
