---
name: openclaw-deployment-installer
description: Deploy and configure OpenClaw AI assistant with multi-model support and messaging channel integrations
triggers:
  - install openclaw ai assistant
  - deploy openclaw with telegram bot
  - configure openclaw for discord
  - set up openclaw with claude or openai
  - troubleshoot openclaw installation
  - manage openclaw gateway service
  - configure openclaw messaging channels
  - add feishu or whatsapp to openclaw
---

# OpenClaw Deployment & Installer

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenClawInstaller is a one-click deployment tool for **OpenClaw** (aka ClawdBot), a private AI assistant with persistent memory, proactive messaging, and multi-channel support. It supports Anthropic Claude, OpenAI GPT, Google Gemini, and local models via Ollama. Messaging integrations include Telegram, Discord, WhatsApp, Slack, WeChat, iMessage (macOS), and Feishu.

## Installation

### One-Click Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/miaoxworld/OpenClawInstaller/main/install.sh | bash
```

This script:
1. Detects system environment and installs dependencies
2. Installs Node.js v22+ (if needed)
3. Installs OpenClaw via npm
4. Runs onboarding wizard for AI model and identity configuration
5. Tests API connectivity
6. Auto-starts the OpenClaw Gateway service
7. Optionally opens configuration menu for channel setup

### Manual Installation

```bash
# Clone repository
git clone https://github.com/miaoxworld/OpenClawInstaller.git
cd OpenClawInstaller

# Add execute permissions
chmod +x install.sh config-menu.sh

# Run installer
./install.sh

# If permission issues on macOS, install OpenClaw first
npm install -g openclaw
```

### Desktop Manager (GUI Alternative)

For graphical interface, use **OpenClaw Manager** (Tauri 2.0 + React + Rust):
- Download: [github.com/miaoxworld/openclaw-manager](https://github.com/miaoxworld/openclaw-manager)
- Cross-platform: macOS, Windows, Linux
- Features: real-time monitoring, visual config, service management

## System Requirements

- **OS**: macOS 12+, Ubuntu 20.04+, Debian 11+, CentOS 8+
- **Node.js**: v22 or higher
- **Memory**: 2GB minimum, 4GB+ recommended
- **Disk**: 1GB minimum

## Core Commands

### Service Management

```bash
# Start service (background daemon)
openclaw gateway start

# Stop service
openclaw gateway stop

# Restart service
openclaw gateway restart

# Check service status
openclaw gateway status

# Run in foreground (debugging)
openclaw gateway

# View logs
openclaw logs

# Follow logs in real-time
openclaw logs --follow
```

### Configuration Management

```bash
# Open configuration file
openclaw config

# Run onboarding wizard
openclaw onboard

# Diagnose configuration issues
openclaw doctor

# Health check
openclaw health

# Set configuration values
openclaw config set <key> <value>

# Set model
openclaw models set <provider> <model>
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

### Configuration Menu (Interactive)

```bash
# Run configuration menu from installation directory
bash ~/.openclaw/config-menu.sh

# Or download and run directly
curl -fsSL https://raw.githubusercontent.com/miaoxworld/OpenClawInstaller/main/config-menu.sh | bash
```

## AI Model Configuration

### Supported Providers

- **Anthropic Claude**: claude-sonnet-4-5, claude-opus-4-5, claude-haiku-4-5 (supports custom API base URL)
- **OpenAI GPT**: gpt-4o, gpt-4o-mini, gpt-4-turbo (supports custom API base URL with `v1/responses` support)
- **Google Gemini**: gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash
- **OpenRouter**: Multi-model gateway (claude-sonnet-4, gpt-4o, gemini-pro-1.5)
- **Groq**: llama-3.3-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b
- **Mistral AI**: mistral-large-latest, mistral-small-latest, codestral-latest
- **Ollama**: Local deployment (llama3, mistral, etc.)

### Anthropic Claude Setup

```bash
# Environment variables (stored in ~/.openclaw/env)
export ANTHROPIC_API_KEY="your-api-key-here"
export ANTHROPIC_BASE_URL="https://custom-api-endpoint.com"  # Optional

# Configure via CLI
openclaw models set anthropic claude-sonnet-4-5-20250929
```

### OpenAI GPT Setup

⚠️ **Important**: Custom OpenAI API endpoints must support **Responses API** (`v1/responses`), not just Chat Completions (`v1/chat/completions`).

```bash
# Environment variables
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_BASE_URL="https://custom-api-endpoint.com/v1"  # Optional

# Configure via CLI
openclaw models set openai gpt-4o
```

### Custom Provider Configuration

For custom API endpoints (e.g., OneAPI, NewAPI), the installer creates a custom provider in `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "anthropic-custom": {
        "baseUrl": "https://your-api-proxy.com",
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

### Ollama (Local Model) Setup

```bash
# Install Ollama first: https://ollama.ai
ollama pull llama3

# Configure OpenClaw
openclaw models set ollama llama3
```

## Messaging Channel Configuration

### Telegram Bot

1. Create bot with BotFather:
```
# In Telegram, message @BotFather
/newbot
# Follow prompts, get Bot Token
```

2. Get your User ID:
```
# Message @userinfobot
# Copy your User ID
```

3. Configure via menu or manually edit `~/.openclaw/openclaw.json`:
```json
{
  "telegram": {
    "token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
    "userId": "987654321"
  }
}
```

### Discord Bot

1. Create application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Go to Bot section → Reset Token → Copy token
3. **Enable "Message Content Intent"** (critical!)
4. Invite bot via OAuth2 URL Generator (scopes: `bot`, permissions: View Channels, Send Messages, Read Message History)
5. Get Channel ID: Enable Developer Mode → Right-click channel → Copy Channel ID

Configure:
```json
{
  "discord": {
    "token": "your-bot-token",
    "channelId": "1234567890123456789"
  }
}
```

### Feishu (Lark) Bot

No public server required — uses WebSocket long-connection mode.

1. Create app at [Feishu Open Platform](https://open.feishu.cn/)
2. Add "Bot" capability
3. Get **App ID** and **App Secret**
4. Add permissions: `im:message`, `im:message:send_as_bot`, `im:chat:readonly`
5. Publish app
6. Configure event subscription:
   - Use **long-connection mode** (no webhook URL needed)
   - Add event: `im.message.receive_v1`
   - ⚠️ OpenClaw service must be running to save settings

Configure:
```json
{
  "feishu": {
    "appId": "cli_xxxxxxxxx",
    "appSecret": "your-app-secret"
  }
}
```

### WhatsApp

No Business API needed — uses personal account via QR code.

```bash
# Run configuration menu → WhatsApp option
# Scan QR code displayed in terminal
# Restart gateway after login
openclaw gateway restart
```

⚠️ **Note**: WhatsApp Web can only be active on one device. Configuring here will log out existing WhatsApp Web sessions.

## Configuration Files

### Directory Structure

```
~/.openclaw/
├── openclaw.json        # Core configuration (models, channels, skills)
├── env                  # Environment variables (API keys, base URLs)
├── backups/             # Configuration backups
└── logs/                # Log files (managed by OpenClaw)
```

### Environment Variables (`~/.openclaw/env`)

```bash
# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
export ANTHROPIC_BASE_URL="https://custom-endpoint.com"  # Optional

# OpenAI GPT
export OPENAI_API_KEY="sk-xxxxx"
export OPENAI_BASE_URL="https://custom-endpoint.com/v1"  # Optional

# Google Gemini
export GEMINI_API_KEY="your-gemini-key"

# OpenRouter
export OPENROUTER_API_KEY="sk-or-xxxxx"

# Groq
export GROQ_API_KEY="gsk_xxxxx"

# Mistral AI
export MISTRAL_API_KEY="your-mistral-key"
```

### Core Configuration (`~/.openclaw/openclaw.json`)

```json
{
  "models": {
    "default": "claude-sonnet-4-5-20250929",
    "providers": {
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY}",
        "models": ["claude-sonnet-4-5-20250929"]
      }
    }
  },
  "telegram": {
    "token": "${TELEGRAM_BOT_TOKEN}",
    "userId": "123456789"
  },
  "discord": {
    "token": "${DISCORD_BOT_TOKEN}",
    "channelId": "987654321"
  },
  "memory": {
    "enabled": true,
    "maxMessages": 1000
  },
  "skills": {
    "enabled": true,
    "directory": "~/.openclaw/skills"
  }
}
```

## Common Patterns

### Testing API Connection

```bash
# After configuring AI model
openclaw doctor

# Test specific model
openclaw models test anthropic claude-sonnet-4-5-20250929
```

### Adding Custom Skills

```bash
# Skills are Markdown files in ~/.openclaw/skills/
mkdir -p ~/.openclaw/skills

cat > ~/.openclaw/skills/weather.md << 'EOF'
# Weather Information

You can fetch weather information for any city.

## Usage
When user asks about weather:
1. Extract city name
2. Use curl to fetch from weather API
3. Format and present results
EOF

# Restart gateway to load skills
openclaw gateway restart
```

### Monitoring Service Status

```bash
# Check if gateway is running
openclaw gateway status

# View recent logs
openclaw logs --tail 50

# Watch logs in real-time
openclaw logs --follow

# Health check with detailed output
openclaw health --verbose
```

### Switching AI Models

```bash
# Change to different model
openclaw models set anthropic claude-opus-4-5

# Change to different provider
openclaw models set openai gpt-4o

# Verify current model
openclaw config get models.default
```

### Backup and Restore

```bash
# Backup all configuration and data
openclaw backup --output ~/openclaw-backup-$(date +%Y%m%d).tar.gz

# Restore from backup
openclaw restore ~/openclaw-backup-20260517.tar.gz

# Export conversations only
openclaw export --format json --output ~/conversations.json
```

## Troubleshooting

### Service Won't Start

```bash
# Check for errors
openclaw doctor

# View detailed logs
openclaw logs --level debug

# Verify Node.js version
node --version  # Should be v22+

# Check environment variables
source ~/.openclaw/env
echo $ANTHROPIC_API_KEY
```

### API Key Not Working

```bash
# Test API key manually
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'

# For custom base URL
curl https://your-custom-endpoint.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'
```

### Telegram Bot Not Responding

```bash
# Verify bot token and user ID
cat ~/.openclaw/openclaw.json | grep -A 3 telegram

# Check logs for errors
openclaw logs | grep telegram

# Test bot manually
curl https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe
```

### Discord Bot Not Responding

1. Verify Message Content Intent is enabled in Discord Developer Portal
2. Check bot has permissions in target channel
3. Verify channel ID is correct:
```bash
# Check configuration
openclaw config get discord.channelId

# View logs
openclaw logs | grep discord
```

### Feishu Bot Not Receiving Messages

1. Ensure OpenClaw gateway is running when saving event subscription settings
2. Verify long-connection mode is selected (not webhook)
3. Check permissions are granted and app is published
4. View logs:
```bash
openclaw logs | grep feishu
```

### WhatsApp Connection Lost

```bash
# Re-authenticate by reconfiguring
bash ~/.openclaw/config-menu.sh
# Select WhatsApp → Scan new QR code

# Restart gateway
openclaw gateway restart
```

### Memory/Performance Issues

```bash
# Clear old memory
openclaw memory clear --before 2026-01-01

# Reduce context window in config
openclaw config set memory.maxMessages 500

# Monitor resource usage
openclaw health --verbose
```

### Custom API Endpoint Not Working

For Anthropic:
```bash
# Verify baseUrl format (no /v1 suffix)
echo $ANTHROPIC_BASE_URL  # Should be: https://api.example.com

# Test endpoint
curl $ANTHROPIC_BASE_URL/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01" -d '{"model":"claude-sonnet-4-5-20250929","max_tokens":10,"messages":[{"role":"user","content":"test"}]}'
```

For OpenAI (must support `v1/responses`):
```bash
# Verify endpoint supports Responses API
curl $OPENAI_BASE_URL/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","input":[{"role":"user","content":"test"}],"max_tokens":10}'

# If 404, your endpoint doesn't support Responses API
```

### Clean Reinstall

```bash
# Stop service
openclaw gateway stop

# Backup data
openclaw backup

# Uninstall
npm uninstall -g openclaw
rm -rf ~/.openclaw

# Reinstall
curl -fsSL https://raw.githubusercontent.com/miaoxworld/OpenClawInstaller/main/install.sh | bash
```

## Advanced Configuration

### Multiple AI Models (Fallback)

Edit `~/.openclaw/openclaw.json`:
```json
{
  "models": {
    "default": "claude-sonnet-4-5-20250929",
    "fallback": ["gpt-4o", "gemini-2.0-flash"],
    "providers": {
      "anthropic": { "apiKey": "${ANTHROPIC_API_KEY}" },
      "openai": { "apiKey": "${OPENAI_API_KEY}" },
      "google": { "apiKey": "${GEMINI_API_KEY}" }
    }
  }
}
```

### Scheduled Proactive Messages

```bash
# Create skill for morning briefing
cat > ~/.openclaw/skills/morning-briefing.md << 'EOF'
# Morning Briefing

Every day at 8 AM, send a summary of:
- Today's calendar events
- Weather forecast
- Important reminders

## Schedule
- Time: 08:00
- Timezone: UTC
EOF

openclaw gateway restart
```

### Custom System Prompt

Edit `~/.openclaw/openclaw.json`:
```json
{
  "system": {
    "prompt": "You are a helpful AI assistant named OpenClaw. You have persistent memory across conversations and can proactively send messages. Be concise and friendly."
  }
}
```

This skill covers the essential deployment, configuration, service management, and troubleshooting workflows for OpenClaw using the installer tools.
