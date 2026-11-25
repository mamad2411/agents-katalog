---
name: execute-code-change
description: Implement a code change end to end. Use when the user asks to execute, implement, fix, modify, update, refactor, clean up, or add behavior in the repo. Can follow an existing plan or perform a small direct implementation safely.
---

# Execute Code Change

## Purpose

Implement a safe, source-grounded code change with verification and documentation updates when needed.

## Execution Modes

### Mode A: Plan-first execution
Use when:
- The user provides a plan.
- `plan-code-change` was already run.
- A ticket or implementation plan exists.

Procedure:
1. Read the plan.
2. Validate the plan against current files.
3. Identify any stale assumptions or missing files.
4. Execute the smallest safe slice.
5. Add/update tests when behavior changes.
6. Update docs when behavior, API, database, architecture, deployment, project structure, testing, or AI workflow changes.
7. Run the smallest relevant verification.
8. Report deviations from the plan.

### Mode B: Direct execution
Use when:
- The user directly asks to implement, fix, update, refactor, or clean up.
- No separate plan exists.
- The change is small or medium-risk.

Procedure:
1. Do a brief internal planning pass.
2. Read `AGENTS.md`.
3. Use `.ai/context-routing.md` if present.
4. Use maps/indexes/tools only for discovery.
5. Read exact source files, nearby tests, contracts, and docs before editing.
6. Confirm the smallest safe implementation that follows existing patterns.
7. Edit narrowly.
8. Add/update tests when behavior changes.
9. Update docs when needed.
10. Run the smallest relevant verification command.
11. Summarize files changed, behavior changed, verification, and remaining risks.

## Escalate to `plan-code-change` first when

- The change spans multiple modules.
- Requirements are unclear.
- Public API behavior changes.
- Auth/security behavior changes.
- Data migrations are involved.
- Deployment/runtime behavior changes.
- The blast radius is unknown.
- The user explicitly asks to plan first.

## Boundaries

- Do not bypass project guardrails in `AGENTS.md`.
- Do not expose secrets or sensitive data.
- Do not run destructive commands, migrations, deployments, force pushes, resets, or cleanups without explicit approval.
- Do not claim verification passed unless it actually ran.
- Do not edit from generated context alone.

## Required Output

- Execution mode used.
- Relevant files/docs inspected.
- Files changed.
- Behavior changed or structure changed.
- Tests/verification run, including command and result.
- Docs updated or skipped with reason.
- Deviations from plan, if any.
- Remaining risks, assumptions, and handoffs.
