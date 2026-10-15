---
name: openclaw-chinese-ai-assistant
description: OpenClaw Chinese localized AI assistant platform with CLI, dashboard, multi-platform chat integration (WhatsApp/Telegram/Discord), and LLM provider support
triggers:
  - set up openclaw chinese version
  - deploy openclaw ai assistant in chinese
  - configure openclaw with claude or chatgpt
  - integrate openclaw with telegram whatsapp discord
  - troubleshoot openclaw gateway issues
  - manage openclaw dashboard and agents
  - install openclaw daemon service
  - update openclaw chinese translation
---

# OpenClaw Chinese AI Assistant Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

OpenClaw Chinese Translation is a fully localized (Simplified Chinese) distribution of OpenClaw, an open-source personal AI assistant platform with 195,000+ GitHub stars. It runs locally on your machine and provides AI assistance through popular chat platforms (WhatsApp, Telegram, Discord) with both CLI and web dashboard interfaces fully translated to Chinese.

**Key Features:**
- Automatic hourly sync with upstream OpenClaw (< 1 hour delay)
- Full Chinese localization for CLI and Dashboard
- Multi-platform support: WhatsApp, Telegram, Discord
- Multiple LLM providers: Claude, OpenAI, compatible APIs
- Tool calling and skill extensions
- Daemon/service mode for background operation
- Web-based management dashboard

## Installation

### Prerequisites

Node.js >= 22 is required. Check version:

```bash
node -v
```

If needed, download from https://nodejs.org/

### Install OpenClaw Chinese

```bash
npm install -g @qingchencloud/openclaw-zh@latest
```

### Verify Installation

```bash
openclaw --version
```

## Initialization and Configuration

### Initial Setup with Daemon

```bash
openclaw onboard --install-daemon
```

This interactive wizard will guide you through:
1. Selecting an LLM provider (Claude, OpenAI, or compatible)
2. Configuring API credentials
3. Setting up chat channels (WhatsApp/Telegram/Discord)
4. Installing gateway as daemon service

### Manual Configuration

View current config:

```bash
openclaw config
```

Edit config file directly (located at `~/.openclaw/config.yml`):

```yaml
llm:
  provider: openai
  api_key: ${OPENAI_API_KEY}
  model: gpt-4
  base_url: https://api.openai.com/v1  # For compatible providers

gateway:
  port: 3000
  host: 0.0.0.0

channels:
  - type: telegram
    token: ${TELEGRAM_BOT_TOKEN}
  - type: discord
    token: ${DISCORD_BOT_TOKEN}
```

### Configure LLM Provider

For OpenAI-compatible providers (like the free gpt.qt.cool):

```bash
openclaw config set llm.provider openai-compatible
openclaw config set llm.base_url https://gpt.qt.cool/v1
openclaw config set llm.api_key ${YOUR_API_KEY}
openclaw config set llm.model gpt-4
```

For Claude:

```bash
openclaw config set llm.provider anthropic
openclaw config set llm.api_key ${ANTHROPIC_API_KEY}
openclaw config set llm.model claude-3-5-sonnet-20241022
```

## Core Commands

### Gateway Management

```bash
# Start gateway (foreground, for debugging)
openclaw gateway run

# Start as daemon (background, recommended)
openclaw gateway start

# Stop daemon
openclaw gateway stop

# Restart gateway
openclaw gateway restart

# Check status
openclaw gateway status

# Install as system service (auto-start on boot)
openclaw gateway install

# Uninstall system service
openclaw gateway uninstall
```

### Dashboard

```bash
# Open web dashboard (auto-opens browser)
openclaw dashboard

# Open on specific port
openclaw dashboard --port 8080

# Access remotely with token
openclaw dashboard --host 0.0.0.0 --token ${DASHBOARD_TOKEN}
```

Dashboard URL: http://localhost:3000 (default)

**Language Setting:** After opening dashboard, go to **Overview** page → scroll to bottom → set **Language** to **简体中文 (Simplified Chinese)** → refresh.

### Skills Management

```bash
# List available skills
openclaw skills list

# Install a skill
openclaw skills install 1password

# Remove a skill
openclaw skills remove 1password

# Update all skills
openclaw skills update
```

### Maintenance

```bash
# Update OpenClaw CLI
openclaw update

# Diagnose issues (auto-fix)
openclaw doctor

# View logs
openclaw logs

# Clear cache
openclaw cache clear
```

## Real-World Usage Examples

### Example 1: Deploy with Custom LLM Provider

```bash
#!/bin/bash

# Set environment variables
export OPENAI_API_KEY="sk-your-key-here"
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF-your-token"

# Install
npm install -g @qingchencloud/openclaw-zh@latest

# Configure programmatically
openclaw config set llm.provider openai-compatible
openclaw config set llm.base_url https://gpt.qt.cool/v1
openclaw config set llm.api_key "${OPENAI_API_KEY}"
openclaw config set llm.model gpt-4

# Add Telegram channel
openclaw config set channels.0.type telegram
openclaw config set channels.0.token "${TELEGRAM_BOT_TOKEN}"

# Start daemon
openclaw gateway start

# Verify running
openclaw gateway status
```

### Example 2: Docker Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  openclaw:
    image: ghcr.io/1186258278/openclaw-chinese:latest
    container_name: openclaw-zh
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - DASHBOARD_TOKEN=${DASHBOARD_TOKEN}
    volumes:
      - ./data:/root/.openclaw
      - ./logs:/var/log/openclaw
```

Run:

```bash
docker-compose up -d
```

### Example 3: Remote Access with Nginx

Nginx config for HTTPS dashboard access:

```nginx
server {
    listen 443 ssl;
    server_name openclaw.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        
        # WebSocket support
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Example 4: Programmatic Agent Creation (JavaScript)

```javascript
// Create custom agent configuration
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const configPath = path.join(process.env.HOME, '.openclaw', 'config.yml');
const config = yaml.load(fs.readFileSync(configPath, 'utf8'));

// Add new agent
config.agents = config.agents || [];
config.agents.push({
  name: 'research-assistant',
  model: 'gpt-4',
  system_prompt: '你是一个专业的研究助手，帮助用户查找和总结信息。',
  skills: ['web-search', 'summarize', 'markdown'],
  max_tokens: 4000,
  temperature: 0.7
});

// Save config
fs.writeFileSync(configPath, yaml.dump(config), 'utf8');
console.log('Agent created successfully');
```

### Example 5: Monitoring Gateway Status

```bash
#!/bin/bash

# Check if gateway is running
if openclaw gateway status | grep -q "running"; then
    echo "Gateway is healthy"
    exit 0
else
    echo "Gateway is down, restarting..."
    openclaw gateway restart
    sleep 5
    if openclaw gateway status | grep -q "running"; then
        echo "Gateway restarted successfully"
        exit 0
    else
        echo "Failed to restart gateway"
        exit 1
    fi
fi
```

## Common Patterns

### Pattern 1: Multi-Model Setup

Configure different models for different tasks:

```yaml
agents:
  - name: fast-assistant
    model: gpt-3.5-turbo
    use_case: quick_questions
  
  - name: deep-thinker
    model: claude-3-opus-20240229
    use_case: complex_reasoning
  
  - name: code-helper
    model: gpt-4
    skills: ['code-interpreter', 'github']
```

### Pattern 2: Environment-Based Config

Use environment variables for secrets:

```bash
# .env file
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=123456:ABC...
WHATSAPP_PHONE_NUMBER=+1234567890
DASHBOARD_TOKEN=secure-random-token-here

# Load in config.yml
llm:
  api_key: ${OPENAI_API_KEY}

channels:
  - type: telegram
    token: ${TELEGRAM_BOT_TOKEN}
  - type: whatsapp
    phone: ${WHATSAPP_PHONE_NUMBER}
```

### Pattern 3: Skill Chains

Combine multiple skills for complex workflows:

```javascript
// Example: Research and summarize workflow
const workflow = {
  steps: [
    { skill: 'web-search', query: '${user_query}' },
    { skill: 'summarize', input: '${search_results}' },
    { skill: 'markdown', format: 'report', input: '${summary}' }
  ]
};
```

## Troubleshooting

### Gateway Won't Start

```bash
# Check if port 3000 is already in use
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Run diagnostics
openclaw doctor

# Check logs
openclaw logs --tail 100

# Try alternative port
openclaw gateway run --port 3001
```

### Dashboard Connection Issues

1. **Cannot access dashboard remotely:**

```bash
# Start with external access
openclaw dashboard --host 0.0.0.0 --token your-secure-token

# Or edit config
openclaw config set gateway.host 0.0.0.0
openclaw config set gateway.dashboard_token your-secure-token
openclaw gateway restart
```

2. **CORS errors:**

```yaml
# config.yml
gateway:
  cors:
    enabled: true
    origins:
      - https://yourdomain.com
      - http://localhost:*
```

### LLM Provider Errors

```bash
# Test API connection
curl https://gpt.qt.cool/v1/models \
  -H "Authorization: Bearer ${OPENAI_API_KEY}"

# Verify config
openclaw config get llm

# Switch provider
openclaw config set llm.provider openai-compatible
openclaw config set llm.base_url https://api.openai.com/v1
```

### Daemon Service Issues (Windows)

If `gateway install` fails on Windows:

```bash
# Use daemon start instead (doesn't require schtasks)
openclaw gateway start

# Or use Docker
docker run -d -p 3000:3000 \
  -v ~/.openclaw:/root/.openclaw \
  ghcr.io/1186258278/openclaw-chinese:latest
```

### Memory/Performance Issues

```bash
# Check resource usage
openclaw gateway status --verbose

# Limit memory (Node.js)
export NODE_OPTIONS="--max-old-space-size=4096"
openclaw gateway restart

# Clear cache
openclaw cache clear
```

### Update Issues

```bash
# Force reinstall
npm uninstall -g @qingchencloud/openclaw-zh
npm install -g @qingchencloud/openclaw-zh@latest

# Clear npm cache if needed
npm cache clean --force
```

## Uninstallation

```bash
# Stop services
openclaw gateway stop
openclaw gateway uninstall  # If installed as service

# Uninstall package
npm uninstall -g @qingchencloud/openclaw-zh

# Remove config (optional)
rm -rf ~/.openclaw
```

## Additional Resources

- Official Chinese Documentation: https://openclaw.qt.cool
- GitHub Repository: https://github.com/1186258278/OpenClawChineseTranslation
- Free AI API Platform: https://gpt.qt.cool
- ClawPanel (GUI Manager): https://github.com/qingchencloud/clawpanel
- ClawApp (Mobile Client): https://github.com/qingchencloud/clawapp
- Detailed Install Guide: docs/INSTALL_GUIDE.md
- Docker Guide: docs/DOCKER_GUIDE.md
- FAQ: docs/FAQ.md
