---
name: smoke
description: Run the clawback end-to-end smoke test. Starts a mock upstream, spawns the proxy against it, exercises path-mode and hash-mode requests, walks the admin API, and prints the persisted state. Use when verifying the proxy still works after changes.
---

# clawback smoke test

Run `.skills/smoke/scripts/smoke.sh` from the project root:

```bash
.skills/smoke/scripts/smoke.sh
```

Environment variables (optional):

- `CLAWBACK_SMOKE_DIR` — temp dir for state file (default `/tmp/clawback-smoke`)
- `CLAWBACK_SMOKE_UPSTREAM_PORT` — mock upstream port (default `8899`)
- `CLAWBACK_SMOKE_PROXY_PORT` — clawback proxy port (default `8898`)

What the script verifies:

1. Mock Anthropic upstream serves responses with realistic rate-limit headers.
2. Path-mode request (`/my-agent/v1/messages`) strips the agent id and captures session state keyed by `my-agent`.
3. Hash-mode request (`/v1/messages`) captures session state keyed by SHA256 of `{system, tools}`.
4. `GET /_proxy/sessions` lists both sessions with captured metadata.
5. `GET /_proxy/health` returns an ok status with config snapshot.
6. `DELETE /_proxy/sessions/:id` removes one session.
7. The persisted JSON state file reflects the remaining session.

The script traps EXIT to clean up both background processes.
