---
name: keelyard
description: Prove work before finishing, undo bad edits, keep context small. Use when changing code in this repo, when a test or edit went wrong and you need to go back, or before telling the user a task is done.
---

# keelyard

keelyard runs as an MCP server (`keelyard`) plus hooks. Every edit is snapshotted; the Stop
hook blocks "done" until there is evidence.

## The loop

1. `proof_requirements(items=[...])`: one checkable item per user ask.
2. `project_map`, `find_symbol(name)`, `outline(path)`, then `read_file(path)`.
3. Edit. Use `run_compact(command)` for tests and builds.
4. `proof_run_tests(phase="after")`.
5. `proof_check(requirement_id, evidence)` for every item. Evidence is a command and its result,
   or a `path:line`.
6. `proof_status()` must return `{"proven": true}`.

## When something goes wrong

- `rewind_list()` shows each step with the files it touched.
- `rewind_diff(step)` shows what a step changed.
- `rewind_to(step)` restores files. It returns `safety_step`; `rewind_to(safety_step)` undoes it.

## Saving context

- Repeat `read_file` calls on an unchanged file return a one-line notice.
- `run_compact` keeps failures and `file:line`, drops passing noise; `recall(output_id)` returns the rest.
- `memory_search(query)` finds how something was solved in an earlier session.
- `swarm_plan(goal)` splits wide work into per-file tasks with focused context; `swarm(tasks)` runs them on a cheap
  model and checks every answer (citations exist, patches pass the tests in a copy). With no helper model it
  returns `subagent_tasks`: send each `subagent_prompt` to your own subagents (Task tool), then `swarm_verify`.
- keelyard adds short notes to your context (a brief, past-session snippets, hints before destructive commands).
  They are advisory and rate-limited; act on them when they apply.

## Without MCP

Every action is also a CLI command with `--json`, e.g. `keelyard proof status --json`.
Exit codes: 0 ok, 1 error, 2 usage error, 3 check not passed.
