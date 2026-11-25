---
name: zno-review
description: Use when the user writes /zno-review or wants to review code before merging. Audits across 5 dimensions - security, performance, error handling, SOLID/DRY, and project conventions - and outputs findings as blocking items, suggestions, and reminders.
---

# Zno-Review — Code Self-Review

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Identify the scope: recent uncommitted changes, a specific branch diff, or files the user specifies.
2. Audit across 5 dimensions:
   - **Security**: SQL injection, XSS, auth bypass, credential leaks, insecure deserialization.
   - **Performance**: N+1 queries, missing pagination, redundant requests, oversized bundles, missing indexes.
   - **Error handling**: swallowed errors, empty catch blocks, unhandled promise rejections, missing user feedback.
   - **SOLID/DRY**: duplicated logic, oversized functions, deep coupling, single-responsibility violations.
   - **Project conventions**: naming, directory placement, existing patterns, consistency with the design tokens in `docs/product/15-frontend-design-tokens.json`.
3. Output findings in 3 tiers:
   - 🔴 Blocking (must fix before merge)
   - 🟡 Suggestion (recommended, not blocking)
   - 🔵 Reminder (optional improvement)
4. For blocking items, propose fixes or explain the fix direction.
5. Do not merge or push. Only report findings; apply fixes only if the user confirms.
6. If the review leads to changes, update `docs/development/03-feature-changelog.md` with the review status.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/tech-gate.md` — performance-aware design checklist.
- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules.
