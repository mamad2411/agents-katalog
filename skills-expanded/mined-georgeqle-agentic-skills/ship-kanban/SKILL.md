---
name: ship-kanban
description: PoketoWork kanban variant of ship — package finished work and update the matching card
type: shipping
version: v0.0
argument-hint: "[--no-plan] [--no-deploy]"
allowed-tools: Bash(poketo *)
invocation: orchestrator
---

# Ship Kanban

Invoke as `$ship-kanban`.

Use this skill only in projects that have opted into a PoketoWork kanban pack.

## Process

1. Follow the base `$ship` workflow exactly, passing through `$ARGUMENTS`.
2. Resolve and validate the project board using `tasks/.kanban-board`, `poketo kanban boards`, and the standard lists: Backlog, Todo, In Progress, Done, Punt.
3. After shipping:
   - Find the completed step card.
   - If the step is checked off, move it to Done and mark it done.
   - If the step is blocked or deferred, move it to Punt and add the reason.
   - If status is unclear, ask the user.
   - Update the card description with commit SHAs.
4. After planning, ensure the next step card exists in Todo: move from Backlog, create if missing, or skip if already Todo or later.
5. Suggest the top Todo card by priority: overdue, starred, then list order. If no Todo cards exist, check Backlog.

Kanban failures are advisory and must not block the base ship workflow.

## Next-Step Routing

In the final response, include either `Recommended next skill: <command>` or the two-line pair `**Next work:** <specific task or "none">` and `**Recommended next command:** <one command or route>`. Route to the matching kanban workflow when board state can advance; otherwise route to the documented non-kanban fallback or say `No follow-up skill recommended` with the reason.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

