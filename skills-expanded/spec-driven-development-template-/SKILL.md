# Harbor + Spec-Driven Development (SDD)

`.context/` is the single source of truth. App code lives in `src/`. Follow `.context/AGENT.md`.

## Context mode (read first)

Open `.context/project.json` → `agent_context.mode`:

- **`full`** — Load as much `.context/` as practical. No L0–L3 gating. Checklist optional.
- **`layered`** — L0→L3 + Context Checklist intake + `task_routes`.

For eval tasks in `evals/tasks/`, rebuild session/checklist per feature slug.

## If mode is `layered`

**Phase A:** Write `.context/session/CONTEXT_CHECKLIST.md`  
**Phase B:** Load includes (+ rules/active specs)  
**Phase C:** Draft `spec` | `implementation_prompt` | `implementation`

## Specs

Use `.context/specs/_templates/`. Register in `sync-manifest.yaml`.
