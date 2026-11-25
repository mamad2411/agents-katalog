---
name: wechat-ai-bridge
description: Set up WeChat ↔ AI Agent bridges using WeClaw (fastclaw-ai/weclaw). Install, configure agents (Claude Code, Codex, etc.), login via QR code, and manage the bridge daemon.
tags: [wechat, weclaw, clawbot, ai-agent, bridge, messaging]
---

# WeChat AI Agent Bridge

Set up a bridge between WeChat (PC version) and AI agents using [WeClaw](https://github.com/fastclaw-ai/weclaw). WeClaw uses the official Tencent `@tencent-weixin/openclaw-weixin` iLink API to let PC WeChat forward messages to/from AI agents.

## Installation

### One-liner (if GitHub is accessible)
```bash
curl -sSL https://raw.githubusercontent.com/fastclaw-ai/weclaw/main/install.sh | sh
```

### Manual install (when corporate network blocks GitHub)
GitHub downloads may fail with `SSL_ERROR_SYSCALL` on restrictive networks. Use the HTTP proxy:

```bash
export https_proxy=http://127.0.0.1:1082
export http_proxy=http://127.0.0.1:1082
mkdir -p ~/.local/bin
curl -sSL -o ~/.local/bin/weclaw "https://github.com/fastclaw-ai/weclaw/releases/download/v0.7.1/weclaw_darwin_arm64"
chmod +x ~/.local/bin/weclaw
```

Latest version URL pattern: `https://github.com/fastclaw-ai/weclaw/releases/download/v{VERSION}/weclaw_darwin_arm64`

Check if `~/.local/bin` is in PATH:
```bash
echo $PATH | tr ':' '\n' | grep .local/bin
```

## Configuration

Config file: `~/.weclaw/config.json`

### Agents
WeClaw supports three agent modes:

| Mode | Description | Examples |
|------|-------------|----------|
| CLI | Spawns new process per message | `claude -p`, `codex exec` |
| ACP | Long-running subprocess (fastest) | Claude ACP, Codex ACP |
| HTTP | OpenAI-compatible API | OpenClaw HTTP fallback |

### Example: Claude Code via CCX Proxy
```json
{
  "default_agent": "claude",
  "agents": {
    "claude": {
      "type": "cli",
      "command": "/opt/homebrew/bin/claude",
      "args": ["-p", "--dangerously-skip-permissions", "--output-format", "json"],
      "env": {
        "ANTHROPIC_BASE_URL": "http://localhost:3000",
        "ANTHROPIC_API_KEY": "061127",
        "ANTHROPIC_MODEL": "claude-sonnet-4-6",
        "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "deepseek-v4-flash",
        "CLAUDE_CODE_SIMPLE": "1"
      }
    }
  }
}
```

### Example: Codex CLI
```json
{
  "agents": {
    "codex": {
      "type": "cli",
      "command": "/opt/homebrew/bin/codex",
      "args": ["exec", "--sandbox", "none"]
    }
  }
}
```

### Aliases
Define shortcuts for WeChat commands:
```json
{
  "agents": {
    "claude": { "aliases": ["cc", "ai"] },
    "codex": { "aliases": ["cx"] }
  }
}
```

## Login & Start

### First-time setup
1. **⚠️  Tell user to get phone ready first** — QR codes expire in ~2 minutes. Say "请准备好手机微信，我来生成二维码" before running `weclaw login`.

2. **Login** (needs PTY for QR code display):
   ```bash
   weclaw login
   ```
   → Shows QR code in terminal. Scan with phone WeChat.
   → Use `pty=true` in terminal tool if running background (QR codes don't render without PTY).
   → Set a generous terminal timeout (120s+) since login blocks until user scans or QR expires.
   → **On expiry**: `weclaw login` again with fresh QR — same process.

3. **Start bridge**:
   ```bash
   weclaw start
   ```

### Commands
```bash
weclaw start          # Start bridge (background daemon)
weclaw login          # Add more WeChat accounts
weclaw status         # Check if running
weclaw stop           # Stop bridge
weclaw restart        # Restart
weclaw send --to "user@chat" --text "msg"   # Push message
weclaw version        # Check version
weclaw update         # Update to latest
```

## WeChat Chat Commands

Once the bridge is running, send these in WeChat:

| Command | Effect |
|---------|--------|
| `你好` | Send to default agent |
| `/cc 写个函数` | Route to specific agent by alias |
| `/claude` | Switch default agent |
| `/new` | Start fresh session |
| `/info` | Show current agent |
| `/help` | Show help |

## HTTP API

When `weclaw start` is running, a local API listens on `127.0.0.1:18011`:
```bash
# Push message
curl -X POST http://127.0.0.1:18011/api/send \
  -H "Content-Type: application/json" \
  -d '{"to": "user_id@im.wechat", "text": "Hello from API"}'
```

## Pitfalls

- **QR code doesn't render** in background terminal without PTY. Always use `pty=true` with background or run `weclaw login` in foreground.
- **GitHub API/SSL fails** on corporate networks — use the HTTP proxy or try `gh` CLI (which has its own auth and may work through blocked networks).
- **`weclaw start` blocks on QR code** on first run. Run `weclaw login` first to authenticate, then `weclaw start` runs in the background cleanly.
- **Model mapping**: When using Claude Code through a 3P proxy (CCX), you must set both `ANTHROPIC_MODEL` (the model name Claude Code requests) AND `ANTHROPIC_DEFAULT_SONNET_MODEL_NAME` (the name the proxy uses to route). The proxy translates one to the other.
- **`--foreground`** flag keeps the process visible; omit it for background daemon mode.
- **Content length**: WeChat has message length limits. Long agent responses may be truncated.
