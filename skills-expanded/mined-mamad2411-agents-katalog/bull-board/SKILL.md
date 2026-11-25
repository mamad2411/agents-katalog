# Bull-Board 2.0 Cursor Rules

## Canonical Architecture
Use only:
Group → Role → Agent App → Worker → Execution Backend → Runtime(OpenClaw)

## Hard constraints
- Never reintroduce Person model, Person APIs, or bb-person runtime.
- OpenClaw is an external execution runtime backend only.
- Worker is a virtual employee bound to Role + Agent App + Execution Backend.
- Agent App is reusable agent configuration (prompt/model/tool/skill/plugin policy).
- Board is a projection/view; workflow state lives in WorkflowRun / StepRun.
- No legacy compatibility layers or Person migration bridges.
- Bull-Board Console is always system-of-record.

## Stack constraints
- Backend: Go + SQLite + bb CLI + install.sh lifecycle.
- Frontend: React + Vite + TypeScript + TailwindCSS.

## Process constraints
- Update docs before implementation changes.
- Ensure API/schema/docs/code naming all reflect 2.0 nouns.
- Keep dispatch model: resolve worker → agent app → model profile → merged config → execution backend.
