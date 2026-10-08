# Mycelium — Cursor rules

## Project context

Read the canonical brief before coding or planning:

- **Primary:** `prompts/system/CORE_PROMPT.md` (foundational principles + operating model)
- **Architecture & Current Direction:** `docs/architecture.md`

Additional prompts live under `prompts/`:

- `prompts/cursor/` — Cursor-specific task prompts and handoff system
- `prompts/grok-build/` — Grok / build-agent prompts
- `docs/` — architecture and human documentation

## Enforce from the brief

- LangGraph (Python): explicit graphs, nodes, edges; Postgres checkpointer for state
- Python 3.12+, Pydantic, full type hints; no god-agents
- Layout: `src/agents/`, `src/graphs/`, `src/tools/`, `src/models/`, `src/persistence/`, `tests/`
- LangSmith tracing; small reviewable diffs; clean architecture over hacks

## Workflow

1. Align with `prompts/system/CORE_PROMPT.md`
2. Propose a short plan for non-trivial work
3. Implement incrementally with types, tests where appropriate, and tracing hooks

## Cursor Agent Handoffs (Cheat Sheet)

When the user says any of these:
- "Work on the next task"
- "Pick up the next task"
- "Start the next prompt"

**You must:**
1. Scan `prompts/cursor/next/`
2. Pick the oldest file (sort alphabetically)
3. **Move it immediately** to `prompts/cursor/in-progress/` (this claims the task)
4. Read and execute the prompt
5. Create output in `prompts/cursor/done/<task-name>/` with at least:
   - `prompt.md` (copy of the original)
   - `output.md` (clear summary of what was done + decisions)
6. **Remove only the specific file you claimed** from `prompts/cursor/in-progress/`.
   - Do **not** delete, move, or touch any other files present in `in-progress/`.
   - "Helpful" cleanup of other files will break parallel execution.
   - Note unexpected files in your output but leave them alone.

**Scope Discipline (Critical):**
If a prompt defines explicit scope boundaries, stay inside them. If you believe out-of-scope changes are necessary, stop and document the issue instead of making the changes.

Full details: `prompts/WORKFLOW.md`

Never work on a file while it's still in `prompts/cursor/next/`. The move to `in-progress/` is mandatory.
