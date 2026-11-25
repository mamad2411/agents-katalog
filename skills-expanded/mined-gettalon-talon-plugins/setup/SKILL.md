---
description: Guide users through setting up the universal Talon Hub server. Use when user asks about hub setup, connecting clients, or when hub tools return errors.
disable-model-invocation: false
allowed-tools: [Bash]
---

# Hub Setup Guide

Help the user set up the Talon Hub universal server so any client can connect to Claude Code via WebSocket.

## Steps

### 1. Verify Installation

The hub MCP server should already be configured. Verify:

```bash
cat ~/.claude/settings.json 2>/dev/null | grep -A 3 "hub" || echo "Not configured"
```

### 2. Check Settings

Hub reads config from `~/.talon/settings.json`:

```bash
cat ~/.talon/settings.json 2>/dev/null || echo "No settings — create with: mkdir -p ~/.talon && echo '{\"servers\":[{\"port\":9090}],\"access\":{\"requireApproval\":false}}' > ~/.talon/settings.json"
```

Key fields:
- `servers` — Hub server instances (`port`, `url`)
- `connections` — Remote hubs/agents to connect on startup
- `transports` — Channel adapter configs (telegram, discord, etc.)
- `access` — `requireApproval`, `allowlist` for agent gating
- `aliases` — Map platform IDs to display names
- `contacts` — Named contacts for `edge send` routing

### 3. Check Server Health

```bash
edge health 2>/dev/null || curl -s http://localhost:9090/health 2>/dev/null || echo "Server not running"
```

### 4. Get Auth Token

Clients need a token to connect:

```bash
cat ~/.talon/hub_token 2>/dev/null || echo "No token file"
```

Or start the server and get one:

```bash
edge server
```

### 5. Connect a Client

Any WebSocket client can connect:

```
ws://localhost:9090/ws?token=TOKEN&mode=full&name=my-client
```

**Mode options:**
- `chat` — Chat only, no hook events
- `monitor` — Read-only view of all events
- `full` — Everything: chat + hooks + permissions
- `custom` — Pick categories: `?mode=custom&categories=tools,permissions,session`

**Available categories:** chat, tools, permissions, session, notifications, subagents, lifecycle, filesystem, worktree, compact, elicitation, prompts

### 6. CLI Reference

| Command | Description |
|---------|-------------|
| `edge status` | Show servers, clients, agents |
| `edge connect <url> [name]` | Connect to remote hub/agent |
| `edge send <target> <msg>` | Send message |
| `edge reload` | Reload settings.json |
| `edge health` | Health snapshot |

### 7. Hook Events

The server receives all 23 Claude Code hook events and forwards them to connected clients based on their mode. Events include:

- **Session:** SessionStart, SessionEnd
- **Tools:** PreToolUse, PostToolUse, PostToolUseFailure
- **Permissions:** PermissionRequest
- **User Input:** UserPromptSubmit
- **Subagents:** SubagentStart, SubagentStop
- **Lifecycle:** Stop, StopFailure, TeammateIdle, TaskCompleted
- **Filesystem:** FileChanged, CwdChanged, ConfigChange, InstructionsLoaded
- **Worktree:** WorktreeCreate, WorktreeRemove
- **Compact:** PreCompact, PostCompact
- **Elicitation:** Elicitation, ElicitationResult

### 8. Troubleshooting

**Server not running:** Start with `edge server` or ensure Claude Code has the hub plugin loaded.

**Connection refused:** Check the port in `~/.talon/settings.json` — default is 9090.

**Invalid token:** Get a fresh token from `~/.talon/hub_token`.

**Config not taking effect:** Run `edge reload` to re-read `~/.talon/settings.json`.
