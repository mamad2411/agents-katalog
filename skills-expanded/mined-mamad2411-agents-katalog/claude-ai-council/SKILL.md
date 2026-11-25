---
name: claude-ai-council
description: "Run the local AI Council planning workflow from Claude Code. Use when the user asks Claude to create a council plan, run AI Council, consult Codex/Claude together, produce final-plan.md, or monitor an existing council run."
---

# Claude AI Council

Use the local `ai-council` MCP tools to run a planning-only Council workflow. Do not implement the plan or edit production source.

## Workflow

1. Collect the task, workspace, optional task ID, acceptance criteria, constraints, and any requested artifacts.
2. Before calling `run_council`, explain that the workflow sends task and repository context to external model services operated by OpenAI and Anthropic, then get explicit user approval.
3. Call `run_council` with the collected task details and `confirmExternalModelUse: true`.
4. Store the returned `runId`, `taskId`, `state`, and latest event ID if provided.
5. Repeatedly call `get_council_status` with:
   - `runId`
   - `afterEventId`
   - `waitForChangeMs`
6. Continue until `isTerminal` is true.
7. For `COMPLETE`, report the `final-plan.md` path and summarize where it was written.
8. For `FAILED_VALIDATION`, report the validation failure details and the preserved draft path when available.
9. For `STALE_REPOSITORY`, explain that the repository changed during planning and the run must be restarted against the current code.
10. For `INTERRUPTED`, explain that the daemon or worker was interrupted and report the last known state.
11. For `CANCELLED` or `TIMED_OUT`, report the terminal state and last useful artifacts.

## Rules

- Use `consult_peer` only for explicit one-off peer consultation, not for internal Council workflow stages.
- Do not pass `confirmExternalModelUse: true` unless the user explicitly approved sending task and repository context to OpenAI and Anthropic model services for this run.
- Do not call `promote_final_plan` unless the user explicitly asks to promote the completed final plan.
- When promoting, pass `confirm: true`; keep `overwrite: false` unless the user explicitly requests overwrite.
- If `get_diagnostics` reports missing CLI support, stop and report the actionable remediation.
