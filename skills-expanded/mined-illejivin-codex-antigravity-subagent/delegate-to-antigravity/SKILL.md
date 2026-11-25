---
name: delegate-to-antigravity
description: Delegate a bounded coding, research, review, debugging, or implementation task to the local Google Antigravity CLI (`agy`) and use its response as a second-agent result. Use when the user explicitly asks to use Antigravity as a subagent, requests a second opinion from Antigravity, or asks Codex to offload an independent task to `agy`.
---

# Delegate to Antigravity

Treat Antigravity as an external delegated worker. It is not a native Codex collaboration agent: collect its output, verify it, and remain responsible for the final answer and workspace changes.

## Workflow

1. Prefer the `agy_check` and `agy_delegate` MCP tools when they are available.
2. Otherwise use the bundled `scripts/agy-delegate.mjs` runner. It requires Node.js 20 or newer and a locally installed, authenticated `agy` CLI.
3. Establish availability with `agy_check` or `node <skill-dir>/scripts/agy-delegate.mjs --check`.
4. Make the task concrete and bounded. Include the goal, constraints, expected output, and relevant absolute paths.
5. Default to `mode: plan`. Use `accept-edits` only when the user requested implementation and authorized changes to that workspace.
6. Inspect Antigravity's response and the workspace diff. Run relevant tests independently when it made changes.
7. Report its contribution as delegated analysis, not independently verified fact.

## Bundled runner

For the Skills-only path, write the complete prompt to a temporary UTF-8 file and pass its absolute path to the runner. Do not interpolate an untrusted prompt into shell syntax.

```text
node <skill-dir>/scripts/agy-delegate.mjs --cwd <absolute-workspace> --mode plan --prompt-file <absolute-prompt-file>
```

Delete the temporary prompt file after the runner finishes. The runner accepts `--output-format text|json`, `--timeout-seconds 1..1800`, `--agent`, and `--model`. Do not add or emulate dangerous permission-bypass flags.

If neither the MCP tools nor local process execution is available, explain that this plugin requires a local Codex environment with Node.js and an authenticated `agy` installation.

## Safety

- Never weaken the user's persisted sandbox or permission policy.
- Do not delegate secrets, credentials, private data, destructive operations, releases, deployments, purchases, or external messages without explicit authorization for that scope.
- Use one invocation per independent task. Do not create recursive delegation loops or ask Antigravity to invoke Codex.
- If authentication or interactive approval is required, return control to the user rather than bypassing it.
- Use a finite `timeoutSeconds`; split oversized work into bounded tasks.
