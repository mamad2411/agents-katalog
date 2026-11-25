---
name: agent-cli
description: Execute lean TODO tasks through native CLI models with independent product review and targeted repairs; no procedural contract chain for new work.
---

# Agent CLI: native execution

Use the same short TODO -> maker/reviewer -> product checks path as Agent Fleet.
This skill is the entrypoint for delegation, not a trigger for a large contract.

Choose real supported CLI/model candidates from the available pool.
For one small delegated task, run `agent-graph/scripts/todo_pair.py --todo
<todo.json> --run-dir <absolute-evidence-dir>`: one maker, checks and independent
reviewer, with targeted repair. This path does not start a graph scheduler.
For larger work with real independent branches/dependencies, invoke
`todo_graph.py run` once. Do not add a second orchestrator or model polling.

For read-only one-off planning/research call agent-graph/scripts/todo_fleet.py
directly with --request and --output; see references/planning-request.json in
agent-graph. No graph is needed to ask the strong planner for the first TODO.
Give the smallest necessary context and explicit deliverable.
For code use the prepared isolated worktree; actual product acceptance belongs
to an independent reviewer, not to the command's exit code.
Never invent CLI flags, silently substitute models or bypass provider permissions.
