---
name: reset-cursor-acp
description: 'Reset a stuck Cursor ACP thread in a thread manager and reload its configuration. Use only when the user explicitly invokes /reset-cursor-acp.'
disable-model-invocation: true
---

# Reset Cursor ACP in a thread manager

For terminal sessions use `cursor-cli`; for general thread-manager control use `<thread-manager-cli>`.

## How resets work

- An ACP integration may start one `cursor-agent acp` subprocess **per thread, on demand**, owned by a worker.
- **There is no global Cursor ACP server.** Do not create one or keep it alive with a watchdog.
- Rules, skills, and `.cursor/mcp.json` reload when a new subprocess starts.
- `<thread-manager-cli> thread stop <id>` releases the runtime and stops its subprocess, preserving history. The next message starts a fresh agent.

## Quick reset

Resolve `scripts/<reset-script>.sh` relative to this `SKILL.md`. Run:

```bash
scripts/<reset-script>.sh <thread-id>      # reset one Cursor thread
scripts/<reset-script>.sh --self           # reset the current thread (<CURRENT_THREAD_ID_ENV>)
scripts/<reset-script>.sh                  # no thread: orphan cleanup + health check only
scripts/<reset-script>.sh --dry-run        # show what would happen
scripts/<reset-script>.sh <id> --kill-all  # also kill live agents of OTHER Cursor threads
```

Find Cursor thread ids with `<thread-manager-cli> status` (current thread) or:

```bash
<thread-manager-cli> thread list --json | python3 -c 'import json,sys; [print(t["id"], t["status"], t["title"]) for t in json.load(sys.stdin) if t.get("providerId")=="acp-cursor"]'
```

The script stops the selected thread, removes orphaned `cursor-agent acp` processes (parent gone or not a bridge worker), reports CLI version/login/update status, and asks for the next message. Other threads stay running unless `--kill-all`.

If sandboxing blocks `ps` with "operation not permitted", rerun the script outside the sandbox.

## Verify

Send one short message to verify a fresh agent responds. If it hangs again, check the causes below before another reset.

## Known causes

- **Old Cursor CLI.** If the health check shows an update, run `<thread-manager-cli> updates apply`, then reset.
- **Expired login.** Symptom "Failed to initialize session services". Fix: `cursor-agent login`, then reset.
- **Pending permission.** Cursor waits for `session/request_permission`. Check and resolve the thread's pending approval before resetting.
- **Resume failure.** For `session/load` → "Session not found", use a fresh session after `<thread-manager-cli> thread stop` rather than retrying the load.
- **Team-level MCP servers** from the Cursor dashboard do not work in ACP mode. Only project or user `.cursor/mcp.json`.
- **Rate limits.** Enable retries with `<plugin-manager> enable <retry-plugin>`.

## Do not

- No launchd KeepAlive, cron, or watchdog for `cursor-agent acp`.
- Never blindly run `pkill -f cursor-agent`; it kills all Cursor threads and the interactive TUI. Use the script, which targets orphans by default.
- Do not restart the thread manager for one stuck thread; use `<thread-manager-cli> thread stop`.
- Do not use `<thread-manager-cli> thread compact`; Cursor does not support it.
