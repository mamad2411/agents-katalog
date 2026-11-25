---
name: coppice-splitting
description: When to split work into child tickets with splitTickets and when to return status continued for long-running tasks.
---

**Split (multiple child tickets):**
- Use `splitTickets` when work has multiple independent deliverables or the description would exceed ~2–3 screens.
- Each child must be self-contained: `title`, `description`, and `acceptanceCriteria`. Optional per-child `assignTo` (agent key).
- Parent `updatedDescription` should be a short epic summary, not a copy of all children.
- Do not set both a huge `updatedDescription` and `splitTickets` with duplicate content.

## Coppice platform rules — long tasks (required)

- Prefer `status: "continued"` with `progressNote` when substantial work remains and the session is getting long.
- Use `status: "done"` only when acceptance criteria are met.
- Use `status: "blocked"` when genuinely stuck.
