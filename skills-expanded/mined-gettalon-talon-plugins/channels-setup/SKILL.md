---
description: "Guide users through setting up the universal Talon Channels server. Use when user asks about channels setup, connecting clients, or when channel tools return errors."
allowed-tools: [Bash]
---

# Channels Setup Guide

Help the user set up the Talon Channels universal server so any client can connect to Claude Code via WebSocket or platform adapters (Telegram, Discord, Slack, etc.).

## Development Mode

During the research preview, channels require an allowlist. To use talon-channels:

```bash
claude --dangerously-load-development-channels plugin:channels@gettalon-talon-plugins
```

The `plugin:` prefix tells Claude Code to load this channel plugin and bypass the allowlist check.

## Channel Types

| Type | Env Var | Required Credentials |
|------|---------|---------------------|
| WebSocket (default) | `websocket` | None (local only) |
| Telegram | `telegram` | `TELEGRAM_BOT_TOKEN` |
| Discord | `discord` | `DISCORD_BOT_TOKEN` |
| Slack | `slack` | `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` |
| iMessage | `imessage` | None (macOS only) |

## Steps

### 1. Check Current Configuration

```bash
# Check what channel is configured
cat ~/.claude/plugins/marketplaces/gettalon-talon-plugins/plugins/talon/.mcp.json 2>/dev/null || echo "Not found"
```

### 2. Configure Channel Type

Set `TALON_CHANNEL` env var in the plugin's `.mcp.json`:

**WebSocket (default):**
```json
{
  "channels": {
    "command": "npx",
    "args": ["-y", "-p", "@gettalon/channels-sdk", "channels"]
  }
}
```

**Telegram:**
```json
{
  "channels": {
    "command": "npx",
    "args": ["-y", "-p", "@gettalon/channels-sdk", "channels"],
    "env": {
      "TALON_CHANNEL": "telegram",
      "TELEGRAM_BOT_TOKEN": "your-bot-token"
    }
  }
}
```

### 3. Check Server Health (WebSocket mode)

```bash
curl -s http://localhost:21568/health 2>/dev/null || echo "Server not running"
```

### 3. Get Auth Token

Clients need a token to connect:

```bash
curl -s -X POST http://localhost:21568/auth/local | python3 -c "import sys,json; print(json.load(sys.stdin).get('token',''))"
```

Or read from discovery file:

```bash
cat ~/.talon/channels_token 2>/dev/null || echo "No token file"
```

### 4. Connect a Client

Any WebSocket client can connect:

```
ws://localhost:21568/ws?token=TOKEN&mode=full&name=my-client
```

**Mode options:**
- `chat` — Chat only, no hook events
- `monitor` — Read-only view of all events
- `full` — Everything: chat + hooks + permissions
- `custom` — Pick categories: `?mode=custom&categories=tools,permissions,session`

**Available categories:** chat, tools, permissions, session, notifications, subagents, lifecycle, filesystem, worktree, compact, elicitation, prompts

### 5. Example: Connect from Node.js

```javascript
import WebSocket from 'ws';

const token = 'YOUR_TOKEN';
const ws = new WebSocket(`ws://localhost:21568/ws?token=${token}&mode=full&name=my-app`);

ws.on('message', (data) => {
  const msg = JSON.parse(data);
  const payload = msg.payload;

  if (payload.type === 'event' && payload.data.type === 'hook_event') {
    console.log('Hook:', payload.data.hook_event_name, payload.data.data);
  }

  if (payload.type === 'stream') {
    console.log('Reply:', payload.event);
  }
});

// Send a chat message
ws.send(JSON.stringify({
  type: 'chat_message',
  text: 'Hello from my app!',
  chat_id: 'my-chat-1',
}));

// Respond to permission request
ws.send(JSON.stringify({
  type: 'permission_verdict',
  request_id: 'req-123',
  behavior: 'allow',
}));
```

### 6. List Connected Clients

```bash
curl -s http://localhost:21568/clients | python3 -m json.tool
```

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

**Server not running:** Make sure Claude Code is started with the channels plugin loaded.

**Connection refused:** Check the port — default is 21568, but may be different if that port was in use. Check `~/.talon/channels_port`.

**Invalid token:** Get a fresh token via `POST /auth/local` or `~/.talon/channels_token`.
