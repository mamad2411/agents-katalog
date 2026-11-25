---
name: verify-codex-exec
description: "Use when a user asks whether managed codex_exec is available for their current account, requests a codex_exec readiness check, or wants to run the canonical managed Codex smoke test."
metadata:
  category: tool-based
  tool-list:
    - "codex_exec"
  tag:
    - "aevatar"
    - "codex"
    - "managed-sandbox"
    - "smoke-test"
    - "diagnostics"
version: "1.0"
---

# Verify Codex Exec

## Purpose

Prove whether the current authenticated account can complete a real managed
`codex_exec` run. Loading this skill, reading configuration, or observing a
healthy service is not proof.

## Required Check

1. Confirm `codex_exec` exists in the current tool set. If it is absent, do not
   call another tool or simulate success.
2. Invoke `codex_exec` exactly once with:

```json
{
  "target": {
    "kind": "managed_sandbox"
  },
  "workspace": {
    "kind": "empty_git"
  },
  "prompt": "Reply with exactly CODEX_EXEC_READY",
  "timeout_secs": 180
}
```

Do not alter the target, workspace, prompt, or timeout. Do not retry
automatically. Do not ask the user for a token, agent key, credential, service
ID, provider, model route, or sandbox setting.

## Verdict

Return `AVAILABLE` only when all of these are true:

- the tool call completed;
- its result is a JSON object with `status` equal to `succeeded`;
- `target` equals `managed_sandbox`;
- `exit_code` equals `0`;
- trimmed `output` equals exactly `CODEX_EXEC_READY`.

Start the final answer with `AVAILABLE`, then explain in the user's language
that managed `codex_exec` works for this account. Include `target` and
`elapsed_ms` when present.

For every other result, never claim success:

- start with `UNAVAILABLE` when the tool is absent, disabled, the user is
  ineligible, or credential readiness fails;
- start with `INCONCLUSIVE` for timeout, malformed result, execution failure,
  or unexpected output.

Include the stable `code` or `error_code` and `diagnostic_id` when present.
Explain the category briefly in the user's language. Do not print a raw
upstream response when those stable fields are available.

Never expose access tokens, agent keys, request headers, credentials, or secret
references.
