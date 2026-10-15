---
name: engineering-excellence
description: Audits code for KISS, YAGNI, DRY, SOLID, and testability; maintains living engineering notes under .heyeddi/docs/engineering/. Use when refactoring, before merge, or when the user asks for simple scalable design, architecture notes, reuse catalog, or engineering ADRs — not for visual UX (use ux-flow-auditor) or CI gates (use pre-merge-gate).
version: 1.0.0
---

# Engineering Excellence

Simple solutions that scale — documented so the next agent does not over-build or repeat work.

**All artifacts go under `.heyeddi/docs/`** — never repo root.

## When to use

- After a feature ships — capture how it works
- Before adding abstractions — check reuse catalog
- Refactor / architecture review — KISS, YAGNI, SOLID
- User asks: "don't over-engineer", "document the system", "engineering notes"

## Subagents (default)

See `reference/subagents.md`. Delegate `audit_engineering.py` and doc init to **Task `shell`**. Main chat interprets findings and updates living docs.

## Pipeline

```
init_engineering_docs   → .heyeddi/docs/engineering/{architecture,reuse-catalog,decisions}.md
implement / refactor
audit_engineering       → .heyeddi/docs/engineering-audit-<date>.md
append_decision         → ADR when trade-off is non-obvious
```

## Instructions

1. **First time in project:** `python scripts/init_engineering_docs.py --project-root <root>`
2. **While coding:** read `reuse-catalog.md` before new components/composables/services
3. **After meaningful change:** update `architecture.md` module map and add reuse rows
4. **Non-obvious trade-off:** `append_decision.py --title … --context … --decision …`
5. **Before merge (non-trivial):** `audit_engineering.py --check` (add `--strict` for warns)

## Principles (how we enforce)

| Principle | Skill behavior |
|-----------|----------------|
| **KISS** | Warn on oversized files; prefer flat modules |
| **YAGNI** | Flag abstraction names without clear reuse |
| **DRY** | Maintain `reuse-catalog.md`; chain `@no-duplicate-ui` for UI |
| **SOLID** | Warn on fat routers; views thin, services fat |
| **Testable** | Note views missing smoke specs |

## `.heyeddi/` outputs

| Path | Purpose |
|------|---------|
| `.heyeddi/docs/engineering/architecture.md` | System map, data flow, boundaries |
| `.heyeddi/docs/engineering/reuse-catalog.md` | What exists — do not rebuild |
| `.heyeddi/docs/engineering/decisions.md` | Engineering ADRs (not design log) |
| `.heyeddi/docs/engineering-audit-<date>.md` | Point-in-time audit report |

Design decisions stay in `.heyeddi/design.md` Decision log — do not mix.

## Chain

- `@project-engineering` — scaffold first
- `@composable-patterns` / `@backend-type-bridger` — after architecture notes exist
- `@pre-merge-gate` — final CI; this skill is advisory + docs
