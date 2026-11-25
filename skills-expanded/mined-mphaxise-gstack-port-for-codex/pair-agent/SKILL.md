---
name: pair-agent
description: Codex paired-agent workflow. Use when the user explicitly wants a subagent, parallel agent, paired review, shared browser work, or another tool on a clearly owned subtask.
---

# Pair Agent

Use this skill when the user explicitly wants a paired agent, subagent, shared browser work, or a clearly scoped collaboration path.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Define the subtask and ownership boundary clearly.
2. Choose the collaboration path:
   - Codex subagent for independent read-heavy exploration, review, triage, or summarization
   - main-thread tool/browser work when the task is short or tightly coupled
   - external app/MCP/tool only when the current session exposes it
3. Share only the context needed for that subtask.
4. Keep browser, sandbox, and approval coordination explicit when external tools are involved.
5. Merge the result back into the main workflow cleanly.

## Guardrails

- Do not split work without a clear ownership boundary.
- Do not spawn a subagent unless the user explicitly requested paired or parallel agent work.
- Remember that subagents inherit the current sandbox and approval settings.
- Be explicit about what environment or browser access is actually available.
- Prefer collaboration that reduces ambiguity instead of creating parallel confusion.
