---
name: codex-sidecar
description: Use a persistent Codex sidecar thread from the local `codex-sidecar` CLI for design review, implementation advice, debugging, and context-preserving follow-up questions while keeping the current agent as the primary executor.
---

# Codex Sidecar

Use the local `codex-sidecar` CLI to consult a persistent Codex thread as a side reviewer / design partner without leaving the current session.

## Workflow

1. Run `codex-sidecar status`.
2. If the session is stopped, run `codex-sidecar start`.
3. Send focused questions with `codex-sidecar ask "<message>"`.
4. Use `codex-sidecar reset` when the user wants to drop the sidecar's prior context.
5. Use `codex-sidecar stop` when the user wants to end the sidecar session and clear local state.

## How to Ask

- Keep the current agent as the executor. Use the sidecar for second opinions, review, debugging hypotheses, or alternative designs.
- Include the relevant task, constraints, and file paths in the `ask` message. Do not assume the sidecar can inspect your current unshared reasoning.
- For code review, ask for concrete risks, likely regressions, and missing tests.
- For design questions, ask for tradeoffs and a recommendation under the current constraints.

## Failure Handling

- If `ask` fails with a resume/state error, run `codex-sidecar status` first.
- If the state file is corrupted or the thread cannot be resumed, run `codex-sidecar reset`.
- If you need a hard cleanup, run `codex-sidecar stop`, then `codex-sidecar start`.
