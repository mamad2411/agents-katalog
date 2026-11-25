---
name: sts2-prepare-runtime
description: Prepare a Copilot CLI or agent session for live STS2 play by checking MCP access, explaining persistent setup, and verifying the runtime is ready before piloting starts.
---

# STS2 runtime preparation workflow

Use this skill when the task is to **make the current session ready for live STS2 control**.

## What this skill owns

- checking whether STS2 MCP tools are already attached to the current session
- accepting a working current-session MCP attachment, even if it is only temporary
- explaining or restoring the MCP setup needed for a fresh Copilot CLI session or `/agent` launch
- verifying that the runtime can actually call `get_game_state`
- handing off to `sts2-pilot-run` only after the session is ready

## Operating loop

1. Check whether STS2 MCP is already available
   - confirm the current session exposes `get_game_state`
   - if available, also verify that menu / combat control tools expected by the current task are present
   - if the tools are present, treat the runtime as ready and hand off to `sts2-pilot-run`, whether the attachment came from a temporary session-level MCP add or a persistent startup config

2. If MCP is missing, diagnose the likely class of blocker
   - a fresh session or `/agent` launch did not inherit a prior session's MCP attachment
   - the user may still prefer a temporary attachment for the current live session because it is simpler or faster
   - Copilot CLI does not yet have a persistent STS2 MCP config
   - the game or mod is not running even though the server config exists
   - when filesystem access is available, prefer to repair or create the persistent CLI MCP config directly instead of stopping at instructions for the user

3. Choose the lightest setup that matches the goal
   - if the current session already has STS2 MCP tools attached, do not block play just because the setup is not persistent
   - if the user wants to keep playing in the current conversation, a temporary session-level MCP attachment is acceptable and often the fastest option
   - if the goal is to close the main session and later open a new session or custom agent directly, do **not** rely on another session's runtime state
   - for that cross-session case, ensure Copilot CLI has a persistent MCP configuration available at session start, using `/mcp add` or `~/.copilot/mcp-config.json`
   - the shared VS Code repo reference lives in [../../../.vscode/mcp.json](../../../.vscode/mcp.json) and uses the VS Code-style `servers` key
   - Copilot CLI home config uses `mcpServers` instead
   - the current repo reference is:

```json
{
  "servers": {
    "sts2": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "${workspaceFolder}\\vendor\\STS2MCP\\mcp",
        "python",
        "server.py",
        "--no-trust-env"
      ]
    }
  }
}
```

   - the equivalent Copilot CLI home config shape is:
   - replace the sample directory with the absolute path to your local clone, because Copilot CLI home config may not resolve VS Code workspace variables

```json
{
  "mcpServers": {
    "sts2": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "D:\\path\\to\\sts2-llm\\vendor\\STS2MCP\\mcp",
        "python",
        "server.py",
        "--no-trust-env"
      ]
    }
  }
}
```

4. After setup, verify the runtime instead of assuming success
   - if the current CLI home config is missing or stale and you can edit it, write the `sts2` server entry yourself before escalating
   - if a temporary attachment was added for the current session and `get_game_state` now works, that is enough to proceed with live play
   - separately check whether the local prerequisites look alive (for example the MCP port and game process) so the blocker is narrowed before asking the user to intervene
   - call `get_game_state`
   - if that works, treat the session as ready
   - if it still fails, distinguish `MCP not attached` from `game/mod not running`
   - if the persistent config is now fixed but the current session still lacks tools, say plainly that the remaining step is to start a new session so the MCP attachment is picked up at launch

5. Hand off cleanly
   - once `get_game_state` works, switch to `sts2-pilot-run`
   - if the runtime is still blocked, report the exact blocker and the next concrete setup action

## Constraints

- Do not pretend the runtime is ready without confirming `get_game_state`
- Do not assume a previous main session's MCP attachment will carry into a new session or `/agent`
- Do not reject a working temporary attachment just because it is not persistent
- Do not hand off to `sts2-pilot-run` until the current session can actually read game state
