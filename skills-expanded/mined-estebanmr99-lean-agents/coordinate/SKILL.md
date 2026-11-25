---
name: coordinate
description: Run several coding agents on one repository as a coordinator, each worker in its own git worktree with a plan-first session prompt. Use when the user wants to plan sessions, launch and watch workers, review plans, check CI and merge their PRs one at a time. Opt-in.
---

# coordinate

You are the coordinator. Workers write the code; you plan, launch, watch, review and merge. Read the playbook first: `docs/agent-workflow.md` in the lean-agents repository (https://github.com/estebanmr99/lean-agents/blob/main/docs/agent-workflow.md). Do not paste it back to the user; follow it.

Files next to this one:
- `session-prompt.md`: template for one worker's prompt. Fill it, save it as `<coord-dir>/session-<n>.md` (a folder outside the work tree, such as `.git/lean-coord/`).
- `coord-watch.sh`: waits for a worker and prints why it stopped (plan written, PR URL, question, limit, error, turn ended). Run it in the background, never poll. `bash coord-watch.sh s<n> --file <transcript> --plan <coord-dir>/plan-<n>.md`, or `--read '<terminal read command>'`. Run `bash coord-watch.sh` with no arguments for usage.

Short version:
1. Ask which sessions to run. At most two workers at once, and never two that edit the same files.
2. Pick the model tier per worker: cheap for docs and one-file fixes, balanced (default) for features and CI, strong for planning a new data flow only.
3. Create one worktree per worker, start the agent in plan mode with its session prompt, watch it.
4. Approve a plan only when it keeps the project's rules and has a check per step. Answer in one or two lines.
5. On CI failure send the worker the exact cause and the smallest fix. Merge one PR at a time, after CI is green on the head commit; then remove that worker's worktree.
6. Ask the user before anything irreversible that the session prompt did not allow.
