---
name: airlock-run-app
description: Run, launch, boot, or start this project's local dev server when working inside the AirLock IDE — routes to AirLock's managed dev server so the IDE shows and manages it (status, Stop/Restart). Applies ONLY inside AirLock.
user-invocable: true
allowed-tools: Bash, mcp__airlock__start_dev_server, mcp__airlock__stop_dev_server
---

# Run the app in AirLock

Use this when asked to run / launch / boot / start the project's dev server locally.

## 1. Gate — AirLock only

This skill applies ONLY when running inside the AirLock IDE. Verify the marker:

```bash
[ -n "$AIRLOCK_IDE" ] && echo in-airlock || echo not-airlock
```

If it prints `not-airlock` (or the `start_dev_server` MCP tool is not available),
STOP — this skill does not apply. Handle the request with your normal approach;
do not follow the steps below.

## 2. Start through AirLock

Call the `start_dev_server` MCP tool. It runs the project's configured dev command
in a SEPARATE AirLock-owned terminal that survives across turns and that the IDE
shows and manages (status, Stop/Restart).

Do NOT run `npm run dev` (or the dev command) yourself, and do NOT detach or
background it — that is unnecessary here (the AirLock terminal already survives the
harness's turn-end SIGTERM) and it makes the server invisible to the IDE.

## 3. If it needs a command

If `start_dev_server` returns `needsCommand`, ask the user to set the dev command
in the Host section of the AirLock sidebar (it offers a guess). Do not fall back to
a raw shell command.

## 4. Stopping

To stop the dev server, use the `stop_dev_server` MCP tool (or Host → Stop).
