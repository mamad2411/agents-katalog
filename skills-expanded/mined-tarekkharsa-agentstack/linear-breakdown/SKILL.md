---
name: linear_breakdown
description: Break a large Linear issue into small, shippable tickets with clear scope, estimates, and dependencies.
---

# Linear Breakdown

> Unofficial, agentstack-authored. Not affiliated with or endorsed by Linear.

Use this skill when a Linear issue is too big to ship in one pass and needs to be
split into smaller tickets a team can pick up independently.

## Workflow

1. Read the parent issue end to end. Pull out the user-facing outcome, the
   acceptance criteria, and any constraints (deadlines, owners, affected areas).
2. Decompose by **shippable slice**, not by layer. Each child ticket should be
   something that can land and be verified on its own — avoid "backend ticket" +
   "frontend ticket" pairs that only make sense merged.
3. For every child ticket, write:
   - a title in imperative voice ("Add X", "Migrate Y"),
   - a one-line outcome and explicit acceptance criteria,
   - a rough size (S / M / L) — split anything that reads as L,
   - dependencies on sibling tickets, if any.
4. Order the tickets so the first one delivers value or unblocks the rest. Flag
   the critical path.
5. Link every child back to the parent and keep the parent as the tracking issue.

## Conventions

- Prefer 3–7 children. More than that usually means the slices are too thin.
- Each child should be mergeable within roughly a day of focused work.
- Never invent acceptance criteria the parent does not support — ask instead.

When using the Linear MCP, create the parent's sub-issues rather than detached
issues, and set the team/project to match the parent so the breakdown stays
grouped.
