---
name: pvecloud-basic-admin
description: "Use only when the task explicitly mentions the historical basic-admin foundation, basic-admin plan/progress docs, or drift between old stage notes and the current admin surface. This helper forces current page scope back to owner docs instead of historical phase notes."
---

# pveCloud Basic Admin

## Purpose

This skill is a narrow historical-scope helper.
It prevents old basic-admin notes from being treated as the current admin contract.

Project truth still lives in:

- `docs/admin/architecture.md`
- `docs/admin/pages/README.md`
- `docs/admin/routing-permissions.md`
- `docs/server/api/`
- `docs/server/database/design.md`
- `server/migrations/`
- `docs/progress/`
- the task-relevant analysis or plan document that explicitly mentions basic-admin

## Boundary

- Historical basic-admin progress, gap, or plan notes can explain why a scope changed.
- They do not override current owner docs, migrations, API docs, or config examples.
- Current admin page scope must come from `docs/admin/pages/README.md`.
- Current route and permission semantics must come from `docs/admin/routing-permissions.md`.
- Removed or not-yet-opened admin pages must not be recreated unless owner docs are updated first and the maintainer confirms reopening them.

## When This Skill Applies

Use this helper only when the task explicitly touches the historical basic-admin stage, including:

- removed admin pages, reopened admin menus, or confusion between backend capability, historical phase notes, and current frontend page scope
- basic-admin gap, plan, or progress documents

Do not load this helper for unrelated current-stage work or ordinary admin implementation tasks. Historical progress can explain why a scope changed, but current contracts still live in the owner docs and machine contracts.

When this helper applies, read:

1. `AGENTS.md`
2. `.codex/skills/pvecloud-document-first/SKILL.md`
3. `docs/progress/MASTER.md`
4. The task-mentioned basic-admin analysis, plan, or progress document
5. `docs/admin/pages/README.md` when page scope matters
6. `docs/admin/routing-permissions.md` when route or permission scope matters
7. The relevant server or admin frontend architecture docs

## Working Rules

- Keep backend and frontend scope separate in your head.
- Do not confuse "backend capability still exists" with "frontend page should still exist".
- Keep the admin frontend aligned with the current documented surface unless docs explicitly reopen it.

## Verification Baseline

Backend work:

```powershell
cd server
go test ./...
```

Admin frontend work:

```powershell
cd admin
bun run build
```
