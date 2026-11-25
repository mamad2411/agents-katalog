---
name: parallel-sessions
description: Split a job into tasks and run one agent per task in its own git worktree, then merge them one at a time. Use when the user wants several agents working in parallel on one repository.
---

# parallel-sessions

You are the coordinator. Workers do the edits; you read status files and short output tails, never full transcripts.

1. Split the work into tasks that touch different files. Shared files only get new lines.
2. Write one prompt file per task, named `<task>.md` (lowercase, dashes). Put in it:
   - front matter: `role: plan|build|explore|research` (sets the model tier: plan strong, build balanced, explore and research cheap), optional `tier: cheap|balanced|strong` and `check: <command>` (run before its merge);
   - the goal, the files the worker may touch, the checks to run, and "do not push".
3. `$LEAN` is your lean-agents clone; run the helper from inside the target repository. Start the workers: `node $LEAN/scripts/parallel.mjs start a.md b.md`. It uses Orca when installed, otherwise `git worktree`. Add `--profile <name>` to map tiers to another profile's models. Where the agent cannot start in the background it prints the command; ask the user to paste it into a new terminal.
4. Poll with `node $LEAN/scripts/parallel.mjs status`. A worker reports `running`, `blocked: <question>` or `done`. Answer a blocked worker through its terminal, not by reading its log.
5. Merge in the planned order, one worker at a time. Ask the user before each merge, then run `node $LEAN/scripts/parallel.mjs merge <task> --yes`. It rebases the remaining workers; rerun their checks.
6. When all are merged, run `node $LEAN/scripts/parallel.mjs clean`. It never forces: an unmerged worker stays.
