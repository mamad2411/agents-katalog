---
name: openclaw-installer-deployment
description: Deploy and configure OpenClaw AI assistant with multi-model support and messaging channel integrations
triggers:
  - install openclaw ai assistant
  - deploy openclaw bot
  - configure openclaw with anthropic claude
  - set up openclaw telegram bot
  - openclaw multi-channel configuration
  - troubleshoot openclaw installation
  - manage openclaw gateway service
  - configure openclaw with custom api
---

# OpenClaw Installer & Deployment

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenClaw is a private AI assistant deployment tool supporting multiple AI models (Claude, GPT, Gemini, etc.) and messaging platforms (Telegram, Discord, WhatsApp, Slack, WeChat, iMessage, Feishu). This skill covers installation, configuration, service management, and troubleshooting.

## What OpenClaw Does

- **Multi-Model AI**: Supports Anthropic Claude, OpenAI GPT, Google Gemini, OpenRouter, Groq, Mistral AI, and Ollama
- **Multi-Channel**: Integrates with Telegram, Discord, WhatsApp, Slack, WeChat, iMessage (macOS), and Feishu
- **Persistent Memory**: Cross-conversation, cross-platform long-term memory
- **Proactive Features**: Scheduled reminders, morning briefings, alerts
- **Custom Skills**: Define capabilities via Markdown files
- **Remote Control**: Execute system commands, file operations, web browsing

## Installation

### One-Line Install (Recommended)

```bash
# Automatic installation with environment detection
curl -fsSL https://raw.githubusercontent.com/miaoxworld/OpenClawInstaller/main/install.sh | bash
```

The installer automatically:
1. Detects OS and installs dependencies (Node.js v22+)
2. Installs OpenClaw globally via npm
3. Guides core configuration (AI model, identity)
4. Tests API connections
5. Auto-starts OpenClaw gateway service
6. Optional: Opens configuration menu for channels

### Manual Installation

```bash
# Clone repository
git clone https://github.com/miaoxworld/OpenClawInstaller.git
cd OpenClawInstaller

# Add execute permissions
chmod +x install.sh config-menu.sh

# Run installer
./install.sh

# If macOS permissions issue, install OpenClaw first
npm install -g openclaw
```

### Desktop Manager (Alternative)

For GUI-based management, use OpenClaw Manager (Tauri 2.0 + React + TypeScript + Rust):
- Repository: https://github.com/miaoxworld/openclaw-manager
- Features: Real-time monitoring, visual config, cross-platform (macOS/Windows/Linux)

## System Requirements

- **OS**: macOS 12+ / Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **Node.js**: v22 or higher
- **Memory**: Minimum 2GB, recommended 4GB+
- **Disk**: Minimum 1GB

## Configuration

### Directory Structure

```
~/.openclaw/
├── openclaw.json        # Core configuration (auto-managed)
├── env                  # Environment variables (API keys)
├── config-menu.sh       # Interactive configuration script
├── backups/             # Config backups
└── logs/                # Log files
```

### Environment Variables (`~/.openclaw/env`)

```bash
# Anthropic Claude
export ANTHROPIC_API_KEY=sk-ant-xxxxx
export ANTHROPIC_BASE_URL=https://custom-api.example.com  # Optional

# OpenAI GPT
export OPENAI_API_KEY=sk-xxxxx
export OPENAI_BASE_URL=https://custom-api.example.com/v1  # Optional

# Google Gemini
export GEMINI_API_KEY=xxxxx

# OpenRouter
export OPENROUTER_API_KEY=sk-or-xxxxx

# Telegram
export TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
export TELEGRAM_USER_ID=123456789

# Discord
export DISCORD_BOT_TOKEN=xxxxx
export DISCORD_CHANNEL_ID=123456789

# Feishu
export FEISHU_APP_ID=cli_xxxxx
export FEISHU_APP_SECRET=xxxxx
```

### Interactive Configuration Menu

```bash
# Run configuration menu
bash ~/.openclaw/config-menu.sh

# Or download and run directly
curl -fsSL https://raw.githubusercontent.com/miaoxworld/OpenClawInstaller/main/config-menu.sh | bash
```

Menu options:
1. **User Identity**: Name, timezone, language preferences
2. **AI Model**: Configure provider (Anthropic, OpenAI, Gemini, etc.)
3. **Message Channels**: Telegram, Discord, WhatsApp, Feishu, etc.
4. **Quick Tests**: API connectivity, channel verification
5. **Advanced**: Backup/restore, view config, diagnostics

### AI Model Configuration

#### Anthropic Claude (with Custom API Support)

```bash
# Using configuration menu
# 1. Select Anthropic Claude
# 2. Enter custom API URL (leave empty for official API)
# 3. Enter API key
# 4. Select model (recommended: claude-sonnet-4-5-20250929)
```

Environment setup:
```bash
export ANTHROPIC_API_KEY=sk-ant-xxxxx
export ANTHROPIC_BASE_URL=https://your-oneapi-proxy.com  # Optional
```

Config file (`~/.openclaw/openclaw.json`):
```json
{
  "models": {
    "providers": {
      "anthropic-custom": {
        "baseUrl": "https://your-oneapi-proxy.com",
        "apiKey": "${ANTHROPIC_API_KEY}",
        "models": [
          {
            "id": "claude-sonnet-4-5-20250929",
            "name": "claude-sonnet-4-5-20250929",
            "api": "anthropic-messages",
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

#### OpenAI GPT (with Custom API Support)

**Important**: Custom API must support OpenAI Responses API (`v1/responses`), not just Chat Completions API.

```bash
# Environment variables
export OPENAI_API_KEY=sk-xxxxx
export OPENAI_BASE_URL=https://your-api-proxy.com/v1
```

#### Ollama (Local Deployment)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3

# Configure in menu: select Ollama, enter model name (llama3)
```

### Channel Configuration

#### Telegram Bot

```bash
# 1. Create bot with @BotFather on Telegram
# 2. Send /newbot and follow prompts
# 3. Copy Bot Token
# 4. Get User ID from @userinfobot
# 5. Configure via menu or set env vars:

export TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
export TELEGRAM_USER_ID=123456789
```

#### Discord Bot

```bash
# 1. Create app at https://discord.com/developers/applications
# 2. Go to Bot → Reset Token (copy token)
# 3. Enable "Message Content Intent" (critical!)
# 4. Invite bot: OAuth2 → URL Generator
#    - Scopes: bot
#    - Permissions: View Channels, Send Messages, Read Message History
# 5. Get Channel ID: Enable Developer Mode → Right-click channel → Copy ID

export DISCORD_BOT_TOKEN=xxxxx
export DISCORD_CHANNEL_ID=123456789
```

#### Feishu (Lark) Bot

```bash
# 1. Create app at https://open.feishu.cn/
# 2. Add "Bot" capability
# 3. Add permissions: im:message, im:message:send_as_bot, im:chat:readonly
# 4. Publish app
# 5. Configure event subscription:
#    - Use "Long Connection" (WebSocket)
#    - Add event: im.message.receive_v1
#    - No webhook URL needed
# 6. Add bot to group chat

export FEISHU_APP_ID=cli_xxxxx
export FEISHU_APP_SECRET=xxxxx
```

Full guide: [docs/feishu-setup.md](https://github.com/miaoxworld/OpenClawInstaller/blob/main/docs/feishu-setup.md)

#### WhatsApp (QR Code Login)

```bash
# 1. Select WhatsApp in config menu
# 2. Scan QR code in terminal
# 3. Login succeeds, restart gateway
# Note: Only one WhatsApp Web session allowed
```

## Service Management

### Core Commands

```bash
# Start gateway (background daemon)
openclaw gateway start

# Stop gateway
openclaw gateway stop

# Restart gateway
openclaw gateway restart

# Check status
openclaw gateway status

# Run in foreground (debug mode)
source ~/.openclaw/env && openclaw gateway

# View logs
openclaw logs

# Tail logs in real-time
openclaw logs --follow
```

### Configuration Commands

```bash
# Open config file
openclaw config

# Run onboarding wizard
openclaw onboard

# Diagnose configuration issues
openclaw doctor

# Health check
openclaw health
```

### Data Management

```bash
# Export conversation history
openclaw export --format json

# Clear memory
openclaw memory clear

# Backup data
openclaw backup
```

## Common Patterns

### Post-Install Startup

```bash
# After installation, load environment and start service
source ~/.openclaw/env
openclaw gateway start

# Verify it's running
openclaw gateway status
```

### Adding a New AI Model

```bash
# Run config menu
bash ~/.openclaw/config-menu.sh

# Select: [2] AI Model Configuration
# Choose provider (e.g., Anthropic Claude)
# Enter custom API URL if using proxy (or leave empty)
# Enter API key
# Select model from list
# Restart gateway

openclaw gateway restart
```

### Adding a New Channel

```bash
# Run config menu
bash ~/.openclaw/config-menu.sh

# Select: [3] Message Channel Configuration
# Choose channel (e.g., Telegram)
# Enter required credentials (token, user ID)
# Restart gateway

openclaw gateway restart
```

### Testing API Connection

```bash
# Using config menu
bash ~/.openclaw/config-menu.sh
# Select: [4] Quick Tests → [1] Test API Connection

# Or manually check health
openclaw health
```

### Switching AI Models

```bash
# Edit environment variables
nano ~/.openclaw/env

# Change API key and base URL
export ANTHROPIC_API_KEY=new-key
export ANTHROPIC_BASE_URL=https://new-proxy.com

# Update model in config (or use menu)
openclaw models set anthropic-custom claude-sonnet-4-5-20250929

# Restart
openclaw gateway restart
```

## Troubleshooting

### Installation Issues

```bash
# Check Node.js version (must be v22+)
node --version

# If Node.js version is old, install via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc  # or ~/.zshrc
nvm install 22
nvm use 22

# Reinstall OpenClaw
npm install -g openclaw
```

### Gateway Won't Start

```bash
# Check if service is already running
openclaw gateway status

# Stop existing service
openclaw gateway stop

# Check for port conflicts (default: 3000)
lsof -i :3000
# Kill conflicting process if needed
kill -9 <PID>

# Run diagnostics
openclaw doctor

# Start in foreground to see errors
source ~/.openclaw/env
openclaw gateway
```

### API Connection Failures

```bash
# Verify environment variables are loaded
source ~/.openclaw/env
env | grep ANTHROPIC  # or OPENAI, GEMINI, etc.

# Test API manually with curl
curl -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":1024,"messages":[{"role":"user","content":"Hi"}]}' \
     ${ANTHROPIC_BASE_URL:-https://api.anthropic.com}/v1/messages

# Check OpenClaw diagnostics
openclaw doctor
```

### Channel Not Responding

```bash
# Telegram: Verify bot token and user ID
curl https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe

# Discord: Check Message Content Intent is enabled
# (Must be set in Discord Developer Portal)

# Feishu: Ensure long connection event subscription is configured
# and OpenClaw gateway is running before saving Feishu config

# View logs for errors
openclaw logs --follow
```

### WhatsApp QR Code Not Showing

```bash
# Ensure terminal supports Unicode
# Try a different terminal emulator

# Check if WhatsApp is already logged in elsewhere
# (Only one Web session allowed)

# Restart gateway and try again
openclaw gateway restart
```

### Custom API Proxy Issues

```bash
# Anthropic: Ensure base URL doesn't include /v1
# Correct:   https://api.example.com
# Incorrect: https://api.example.com/v1

# OpenAI: Must support v1/responses endpoint, not just v1/chat/completions
# Test with:
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     ${OPENAI_BASE_URL}/responses

# If 404, your proxy doesn't support Responses API
```

### Configuration Reset

```bash
# Backup current config
openclaw backup

# Remove config files
rm -rf ~/.openclaw/openclaw.json ~/.openclaw/env

# Re-run installer or onboarding
openclaw onboard

# Or use interactive menu
curl -fsSL https://raw.githubusercontent.com/miaoxworld/OpenClawInstaller/main/config-menu.sh | bash
```

### Memory/Performance Issues

```bash
# Check memory usage
openclaw health

# Clear old memories
openclaw memory clear

# Restart gateway
openclaw gateway restart

# For macOS: Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=4096"
openclaw gateway start
```

## Real-World Examples

### Complete Setup Flow

```bash
# 1. Install OpenClaw
curl -fsSL https://raw.githubusercontent.com/miaoxworld/OpenClawInstaller/main/install.sh | bash

# 2. Configure Anthropic Claude with custom API
bash ~/.openclaw/config-menu.sh
# → [2] AI Model Configuration
# → [1] Anthropic Claude
# → Enter custom API: https://my-oneapi.com
# → Enter API key: sk-ant-xxxxx
# → Select model: claude-sonnet-4-5-20250929

# 3. Configure Telegram
# (Get token from @BotFather, user ID from @userinfobot)
# → [3] Message Channel Configuration
# → [1] Telegram Bot
# → Enter bot token: 123456:ABC-DEF...
# → Enter user ID: 123456789

# 4. Start service
openclaw gateway start

# 5. Test by messaging your Telegram bot
```

### Multi-Channel Setup

```bash
# Configure multiple channels for the same AI backend
source ~/.openclaw/env

# Set up Telegram
export TELEGRAM_BOT_TOKEN=xxxxx
export TELEGRAM_USER_ID=xxxxx

# Set up Discord
export DISCORD_BOT_TOKEN=xxxxx
export DISCORD_CHANNEL_ID=xxxxx

# Set up Feishu
export FEISHU_APP_ID=cli_xxxxx
export FEISHU_APP_SECRET=xxxxx

# Restart to apply all channels
openclaw gateway restart

# Now OpenClaw responds on all platforms with shared memory
```

### Custom Skills Definition

OpenClaw supports custom skills via Markdown files. Example structure:

```markdown
# Custom Skill: Weather Check

Trigger phrases:
- "what's the weather"
- "check weather"

Actions:
1. Call weather API
2. Format response
3. Send to user
```

Skills are typically stored in `~/.openclaw/skills/` (check OpenClaw documentation for exact format).

## Key Takeaways

1. **Use the installer script** for automatic environment setup
2. **Configure via menu** (`config-menu.sh`) for interactive guided setup
3. **Load environment** (`source ~/.openclaw/env`) before manual commands
4. **Custom APIs**: Anthropic/OpenAI support custom base URLs (OneAPI, NewAPI, etc.)
5. **OpenAI proxies**: Must support `v1/responses` endpoint (Responses API)
6. **Feishu**: Use long connection mode (no webhook needed)
7. **WhatsApp**: Only one Web session allowed per account
8. **Service management**: Use `openclaw gateway start/stop/restart/status`
9. **Troubleshooting**: Run `openclaw doctor` for diagnostics
10. **Multi-channel**: All channels share the same AI backend and memory

For latest updates and issues: https://github.com/miaoxworld/OpenClawInstaller
