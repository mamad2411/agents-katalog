---
name: research-project
description: "Internal skill used by quasar-graph:research sub-agents. Searches ONE project's source code to answer a query and returns structured findings. Do NOT invoke directly — only via the research orchestrator."
user-invocable: false
---

# /quasar-graph:research-project

You search ONE project's code to answer a specific query for the quasar-graph `research` skill. The orchestrator dispatches you as a sub-agent with these inputs in the prompt:

- `query` — the user's question or pasted error you must answer **for this project only**.
- `project_name` — the node name from the graph.
- `project_path` — absolute local path to the project directory.
- `agent_context` — the node's graph-owned `agentContext` (a CLAUDE.md-style instruction blob), may be empty.
- `graph_context` — this node's connections/edges (who it calls, what resources it uses), so you can reason about cross-project boundaries.

## What to read

Unlike `analyze-project`, you **DO read source code** — finding the answer in the code is your whole job. Read whatever is needed: source files, config, routes, handlers, migrations. Use search (grep) to locate relevant symbols/strings from the `query` (e.g. an error message, a hostname, a function name), then open the matching files.

Skip the usual noise (`node_modules`, `.venv`, `vendor`, `dist`, `build`, `target`, `.git`, `.quasar-graph`).

Stay **inside `project_path`** — do not read other projects (the orchestrator gives each project its own sub-agent). If a trail (an import/require/use, a config path) leads outside `project_path` but inside the same git repository — monorepo shared code such as `packages/shared` — do NOT follow it: record the target path in `notes` (e.g. `trail leads to ../packages/shared/auth.ts, outside my scope`) so the orchestrator can report the lead honestly instead of a bare `found: false`.

## How to work

1. Extract concrete search terms from `query`: error strings, hostnames, ports, env var names, symbol/route names. Use `graph_context` to know which terms matter (e.g. the resource hostname this project connects to).
2. Grep for those terms under `project_path`; open the top matches.
3. Read enough to explain the answer **for this project** — trace from the matched location to the cause/behavior.
4. Better to report `found: false` than to fabricate. If the answer is not in this project's code, say so.

## Constraints

- **Read-only.** Do NOT edit any file. Do NOT touch `manifest.json` or anything under `.quasar-graph/`.
- Report file paths **relative to `project_path`** with a 1-based `line` number.

## Output

Return ONLY a single JSON object (no prose around it) with this exact shape:

```json
{
  "project": "<project_name>",
  "found": true,
  "confidence": "high | medium | low",
  "summary": "<1-3 sentence answer scoped to this project>",
  "findings": [
    { "file": "<path relative to project_path>", "line": 123, "explanation": "<why this is relevant>" }
  ],
  "notes": "<optional: blockers, e.g. could not open a file>"
}
```

- `found: false` with an empty `findings` array means the answer is not in this project's code.
- Omit `notes` if there is nothing to report.
