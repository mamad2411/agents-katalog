---
name: mapping-dependencies
description: Maps task dependencies in an Astravue project, finds the critical path and blocked work, and detects circular dependencies before any rescheduling. Use when the user asks about dependencies, blockers, what's blocking what, the critical path, or wants to understand or fix the sequencing of a project.
---

# Mapping Dependencies

Build the dependency graph, then reason over it. The analysis (critical path, blockers, cycles) is deterministic and the most valuable part — teams rarely compute it by hand. This skill is read-only by default; only change dependencies when explicitly asked.

## Workflow

1. **Load the graph**

   - `astravue_list_project_tasks` — the tasks (status, due dates) for the scope
   - `astravue_list_dependencies` — the blocking relationships

   Confirm the project first if unclear (`astravue_list_projects`).

2. **Analyze**

   From the edges, compute:
   - **Cycles** — any A→B→…→A loop. Surface these first; a cyclic graph has no valid order and usually signals a modeling mistake.
   - **Critical path** — the longest chain of dependent tasks. Its length drives the project's earliest finish; slipping any task on it slips the whole project.
   - **Blocked tasks** — tasks whose blockers aren't done yet, especially those blocking many others.

3. **Present the picture**

   Lay out the critical path as an ordered chain, list blocked tasks with what they're waiting on, and call out any cycles loudly. Use `astravue_preview_project_overview` or `astravue_preview_task_list` if a visual view helps the user.

4. **Change dependencies only on request**

   If the user wants to fix sequencing:
   - `astravue_add_dependency` / `astravue_remove_dependency` — adjust edges
   - Re-check for cycles after each change and confirm before applying.

## Important

- Detect and report cycles before anything else — they make ordering and critical-path meaningless.
- The critical path is the longest dependent chain, not the count of dependencies.
- Default to read-only; only add or remove dependencies when the user explicitly asks.
- After any edge change, re-validate that no cycle was introduced.
