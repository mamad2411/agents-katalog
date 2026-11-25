---
description: Guide users through choosing and configuring a channel adapter (WebSocket, Telegram, Discord, Slack, etc.). Use when user asks about hub setup, switching channels, or configuring TALON_CHANNEL.
disable-model-invocation: false
allowed-tools: [Bash, Read, Edit]
---

# Channel Adapter Setup Guide

Help the user choose and configure which channel adapter to use with the Talon Hub plugin. There are 22 options: the default WebSocket server plus 21 platform-specific adapters.

## Development Mode

During the research preview, hub requires the official allowlist. To use talon-hub:

```bash
claude --dangerously-load-development-channels plugin:hub@gettalon-talon-plugins
```

The `plugin:` prefix tells Claude Code to load this hub plugin and bypass the allowlist check.

## Settings: `~/.talon/settings.json`

The hub reads all configuration from `~/.talon/settings.json`. Create it if it doesn't exist.

### Full schema

```json
{
  "servers": [
    {
      "url": "ws://localhost:9090",
      "port": 9090
    }
  ],
  "connections": [
    {
      "url": "unix:///tmp/talon-9090.sock",
      "name": "remote-hub",
      "transport": "unix"
    }
  ],
  "transports": {
    "telegram": { "botToken": "YOUR_BOT_TOKEN" },
    "discord": { "botToken": "YOUR_DISCORD_TOKEN" },
    "slack": { "botToken": "xoxb-...", "appToken": "xapp-..." },
    "websocket": {}
  },
  "access": {
    "requireApproval": true,
    "forceApprovalAll": false,
    "allowlist": ["agent-name-1", "agent-name-2"],
    "denylist": ["bad-agent"]
  },
  "hooks": [
    { "event": "onMessage", "command": "echo 'message received'" }
  ],
  "contacts": {
    "alice": {
      "name": "Alice",
      "channels": [{ "type": "telegram", "id": "12345", "url": "telegram://12345" }]
    },
    "bob": {
      "name": "Bob",
      "channels": [
        { "type": "slack", "id": "U123", "url": "slack://U123" },
        { "type": "telegram", "id": "67890", "url": "telegram://67890" }
      ]
    }
  },
  "state": {
    "chatRoutes": {},
    "groups": {},
    "targets": {}
  }
}
```

### Field reference

| Field | Type | Description |
|-------|------|-------------|
| `servers` | array | Hub server instances to start. Each has `url` and `port`. |
| `connections` | array | Remote hubs or agents to connect to on startup. `url` (ws://, unix://), `name`, optional `transport` and `config`. |
| `transports` | object | Channel adapter configs. Keys are channel types: `telegram`, `websocket`, `discord`, `slack`, etc. Each adapter has its own config fields. |
| `access` | object | Access control. `requireApproval` gates new agents, `allowlist` auto-approves named agents, `denylist` blocks agents. |
| `hooks` | array | Shell commands to run on events. `{ "event": "onMessage", "command": "..." }` |
| `contacts` | object | Named contacts with **many-to-many** channel info. Each contact can have multiple channels. Used for `edge send <name>` routing. |
| `state` | object | Runtime state: `chatRoutes`, `groups`, `targets`. Managed by the hub — don't edit manually. |

### Many-to-many routing

Contacts can have multiple channels. Messages to a contact are routed to their first available channel:

```json
"bob": {
  "name": "Bob",
  "channels": [
    { "type": "telegram", "id": "123", "url": "telegram://123" },
    { "type": "slack", "id": "U456", "url": "slack://U456" },
    { "type": "websocket", "id": "bob-ws", "url": "ws://localhost" }
  ]
}
```

Hub servers can accept multiple transports simultaneously — one hub can serve WebSocket, Telegram, Discord, and Slack all at once.

### Transport config reference

| Transport | Config fields | Also reads env var |
|-----------|--------------|--------------------|
| `telegram` | `botToken`, `allowedChats`, `accessPath`, `downloadPath` | `TELEGRAM_BOT_TOKEN` |
| `discord` | `botToken` | `DISCORD_BOT_TOKEN` |
| `slack` | `botToken`, `appToken` | `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` |
| `whatsapp` | `apiToken`, `phoneNumberId` | `WHATSAPP_API_TOKEN` |
| `signal` | `cliPath`, `phoneNumber` | `SIGNAL_CLI_PATH` |
| `matrix` | `homeserver`, `accessToken` | `MATRIX_HOMESERVER` |
| `websocket` | *(none needed)* | — |
| `irc` | `server`, `nick`, `channel` | `IRC_SERVER` |

### Minimal config (WebSocket only)

```json
{
  "servers": [{ "port": 9090 }],
  "access": { "requireApproval": false }
}
```

### Telegram config

```json
{
  "servers": [{ "port": 9090 }],
  "transports": {
    "telegram": { "botToken": "YOUR_TELEGRAM_BOT_TOKEN" }
  },
  "access": { "requireApproval": false }
}
```

Or use the env var instead of settings.json:

```bash
export TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

The SDK checks `transports.telegram.botToken` first, then falls back to `TELEGRAM_BOT_TOKEN` env var.

### Multi-transport config

One hub serving WebSocket + Telegram + Discord simultaneously:

```json
{
  "servers": [{ "port": 9090 }],
  "transports": {
    "telegram": { "botToken": "YOUR_TELEGRAM_BOT_TOKEN" },
    "discord": { "botToken": "YOUR_DISCORD_BOT_TOKEN" },
    "websocket": {}
  },
  "access": { "requireApproval": false }
}
```

### Multi-connection config

```json
{
  "servers": [{ "port": 9090 }],
  "connections": [
    { "url": "ws://remote-host:9090", "name": "remote-hub" },
    { "url": "unix:///tmp/agent.sock", "name": "local-agent" }
  ],
  "access": { "requireApproval": true, "allowlist": ["trusted-agent"] }
}
```

## CLI: `edge`

After installing the hub, use the `edge` CLI to manage everything:

| Command | Description |
|---------|-------------|
| `edge status` | Show servers, clients, agents, chat routes |
| `edge connect <url> [name]` | Connect to remote hub or agent |
| `edge reload` | Reload settings.json and reconnect |
| `edge send <target> <msg>` | Send message to agent or contact |
| `edge contacts` | List registered contacts |
| `edge health` | Health snapshot |

## Available Channels

| Channel | Env Var Value | Typical Required Env Vars |
|---------|---------------|---------------------------|
| WebSocket (default) | `websocket` | None (runs locally) |
| Telegram | `telegram` | `TELEGRAM_BOT_TOKEN` |
| Discord | `discord` | `DISCORD_BOT_TOKEN` |
| Slack | `slack` | `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN` |
| WhatsApp | `whatsapp` | `WHATSAPP_API_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID` |
| Signal | `signal` | `SIGNAL_CLI_PATH`, `SIGNAL_PHONE_NUMBER` |
| iMessage | `imessage` | None (macOS only, uses local iMessage) |
| IRC | `irc` | `IRC_SERVER`, `IRC_NICK`, `IRC_CHANNEL` |
| Google Chat | `googlechat` | `GOOGLE_CHAT_CREDENTIALS`, `GOOGLE_CHAT_SPACE` |
| LINE | `line` | `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_CHANNEL_SECRET` |
| Feishu | `feishu` | `FEISHU_APP_ID`, `FEISHU_APP_SECRET` |
| Matrix | `matrix` | `MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN` |
| Mattermost | `mattermost` | `MATTERMOST_URL`, `MATTERMOST_TOKEN` |
| MS Teams | `msteams` | `MSTEAMS_APP_ID`, `MSTEAMS_APP_PASSWORD` |
| BlueBubbles | `bluebubbles` | `BLUEBUBBLES_URL`, `BLUEBUBBLES_PASSWORD` |
| Nostr | `nostr` | `NOSTR_PRIVATE_KEY` |
| Nextcloud Talk | `nextcloud-talk` | `NEXTCLOUD_URL`, `NEXTCLOUD_TOKEN` |
| Synology Chat | `synology-chat` | `SYNOLOGY_URL`, `SYNOLOGY_TOKEN` |
| Tlon | `tlon` | `TLON_SHIP_URL`, `TLON_AUTH_CODE` |
| Twitch | `twitch` | `TWITCH_OAUTH_TOKEN`, `TWITCH_CHANNEL` |
| Zalo | `zalo` | `ZALO_OA_ACCESS_TOKEN` |
| Zalo User | `zalouser` | `ZALO_USER_ACCESS_TOKEN` |

## Steps

### 1. Ask Which Channel

Ask the user which platform they want Claude Code to be reachable on. If they are unsure, explain:

- **WebSocket** (default): Best for custom integrations, local dashboards, browser extensions, or any app that can speak WebSocket. No external accounts needed.
- **Platform adapters**: Best when the user wants to interact with Claude Code directly from Telegram, Discord, Slack, etc. Requires API credentials for that platform.

### 2. Check Current Configuration

```bash
cat ~/.talon/settings.json 2>/dev/null || echo "No settings.json found"
```

### 3. Configure

Edit `~/.talon/settings.json` to add transports, connections, and access rules. See the schema above for all options.

### 4. Verify

```bash
edge reload
edge health
```

### 5. Troubleshooting

**"Unknown channel type"**: The `TALON_CHANNEL` value does not match any supported adapter. Check spelling.

**"No creator function found"**: The `@gettalon/channels-sdk` version may not include this adapter yet. Update: `npm install @gettalon/channels-sdk@latest`.

**WebSocket port conflict**: If port 9090 is in use, change `servers[0].port` in settings.json.

**Agent not connecting**: Check `edge status` and `edge health`. Verify the remote URL is reachable.
