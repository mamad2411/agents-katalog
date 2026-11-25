---
name: hermes-agent-optimization
description: Expert guide for deploying, configuring, and optimizing Hermes AI agents with multi-platform support, MCP integration, and production best practices
triggers:
  - "how do I set up a Hermes agent"
  - "configure Hermes for production"
  - "add Telegram bot to Hermes"
  - "integrate MCP servers with Hermes"
  - "optimize Hermes agent costs"
  - "deploy Hermes to VPS"
  - "create custom Hermes skills"
  - "troubleshoot Hermes agent errors"
---

# Hermes Agent Optimization

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

**Hermes Agent** is an autonomous AI agent framework that orchestrates LLM calls across 20+ platforms (Telegram, Discord, Slack, CLI, webhooks), integrates with MCP servers for tool access, supports multiple LLM providers (Anthropic, OpenAI, Google, local models), and includes durable execution features like Kanban boards and persistent goals.

This skill covers production deployment, multi-platform configuration, cost optimization, security hardening, skill creation, and troubleshooting based on the OnlyTerp/hermes-optimization-guide repository.

## Installation

### Quick Local Setup (5 minutes)

```bash
# Install Hermes (requires Node.js 18+)
npm install -g @nousresearch/hermes-agent

# Initialize config directory
hermes init

# Start interactive setup
hermes configure
```

### Production VPS Setup (One Command)

For Debian 12 / Ubuntu 24.04:

```bash
curl -sSL https://raw.githubusercontent.com/OnlyTerp/hermes-optimization-guide/main/scripts/vps-bootstrap.sh | sudo bash
```

This installs Hermes, Node.js, Caddy reverse proxy, UFW firewall, fail2ban, creates a `hermes` user, sets up systemd services, and symlinks all guide skills.

### Manual Installation

```bash
# Install dependencies
sudo apt update && sudo apt install -y nodejs npm git curl

# Install Hermes globally
npm install -g @nousresearch/hermes-agent

# Create hermes user (production)
sudo useradd -r -m -d /home/hermes -s /bin/bash hermes

# Initialize config
sudo -u hermes hermes init
```

## Configuration Structure

Hermes config lives at `~/.hermes/config.yaml`:

```yaml
# Minimal working config
providers:
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    default_model: claude-3-5-sonnet-20241022

gateways:
  telegram:
    token: ${TELEGRAM_BOT_TOKEN}
    enabled: true

memory:
  provider: lightrag
  storage_path: ~/.hermes/memory

skills:
  directory: ~/.hermes/skills
  auto_load: true

security:
  redact_secrets: true
  approval_mode: auto
```

### Environment Variables

Create `~/.hermes/.env`:

```bash
# LLM Providers
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# Platforms
TELEGRAM_BOT_TOKEN=your_bot_token
DISCORD_BOT_TOKEN=your_discord_token
SLACK_BOT_TOKEN=xoxb-your-slack-token

# Observability
LANGFUSE_SECRET_KEY=your_langfuse_key
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_HOST=https://cloud.langfuse.com

# Optional: Cost optimization
DEEPSEEK_API_KEY=your_deepseek_key
CEREBRAS_API_KEY=your_cerebras_key
```

## Key Commands

### Starting Hermes

```bash
# Interactive TUI mode
hermes

# Headless daemon (production)
hermes daemon

# Web dashboard (runs on http://localhost:3000)
hermes dashboard

# Specific gateway only
hermes --gateway telegram

# Debug mode with verbose logging
DEBUG=hermes:* hermes daemon
```

### Management Commands

```bash
# Update to latest version
hermes update

# Run skill curator (grade and clean skills)
hermes curator

# Backup configuration and data
hermes backup --output ~/hermes-backup-$(date +%F).tar.gz

# Test configuration without starting
hermes validate

# List active sessions
hermes sessions list

# Clear all memory (DESTRUCTIVE)
hermes memory clear
```

### Systemd Service (Production)

```bash
# Install service
sudo cp /path/to/templates/systemd/hermes.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hermes
sudo systemctl start hermes

# View logs
sudo journalctl -u hermes -f

# Restart after config changes
sudo systemctl restart hermes
```

## Setting Up Platforms

### Telegram Bot

1. Create bot with [@BotFather](https://t.me/BotFather)
2. Get token and add to `.env`
3. Configure in `config.yaml`:

```yaml
gateways:
  telegram:
    enabled: true
    token: ${TELEGRAM_BOT_TOKEN}
    allowed_users:
      - 123456789  # Your Telegram user ID
    features:
      voice_enabled: true
      document_upload: true
      inline_mode: true
```

### Discord Bot

1. Create application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Enable Message Content Intent
3. Configure:

```yaml
gateways:
  discord:
    enabled: true
    token: ${DISCORD_BOT_TOKEN}
    command_prefix: "!"
    allowed_roles:
      - "AI Assistant Users"
    allowed_guilds:
      - "1234567890123456789"
```

### Slack App

```yaml
gateways:
  slack:
    enabled: true
    bot_token: ${SLACK_BOT_TOKEN}
    app_token: ${SLACK_APP_TOKEN}
    signing_secret: ${SLACK_SIGNING_SECRET}
    socket_mode: true
```

### CLI (Always Available)

```bash
# Direct CLI conversation
hermes chat "explain quantum computing"

# Pipe input
echo "summarize this" | hermes chat

# File processing
hermes chat "analyze this code" < script.py
```

## Model Routing & Cost Optimization

### Smart Router Configuration

```yaml
models:
  router:
    enabled: true
    strategy: cost_optimized  # or: balanced, performance, local_first
    
  profiles:
    cheap:
      provider: cerebras
      model: llama-3.3-70b
      max_context: 8192
      cost_per_1m_tokens: 0.60
      
    balanced:
      provider: anthropic
      model: claude-3-5-haiku-20241022
      max_context: 200000
      cost_per_1m_tokens: 1.00
      
    premium:
      provider: anthropic
      model: claude-3-5-sonnet-20241022
      max_context: 200000
      cost_per_1m_tokens: 3.00
      
    local:
      provider: lm_studio
      model: qwen-2.5-coder-32b
      endpoint: http://localhost:1234/v1
      max_context: 32768
      
  routing_rules:
    - if: "token_count < 2000"
      use: cheap
    - if: "requires_code_execution"
      use: premium
    - if: "user_priority == high"
      use: premium
    - default: balanced
```

### Provider Setup Examples

**Anthropic (Claude):**
```yaml
providers:
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    default_model: claude-3-5-sonnet-20241022
    max_tokens: 4096
    temperature: 0.7
```

**OpenAI:**
```yaml
providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    default_model: gpt-4o-2024-11-20
    organization: ${OPENAI_ORG_ID}
```

**Google (Gemini):**
```yaml
providers:
  google:
    api_key: ${GOOGLE_API_KEY}
    default_model: gemini-2.0-flash-exp
    safety_settings:
      harassment: BLOCK_NONE
      hate_speech: BLOCK_NONE
```

**Local LM Studio:**
```yaml
providers:
  lm_studio:
    endpoint: http://localhost:1234/v1
    default_model: qwen-2.5-coder-32b-instruct
    timeout: 300000
```

## MCP Server Integration

MCP (Model Context Protocol) servers provide tools/resources to Hermes.

### Configuration

```yaml
mcp:
  servers:
    filesystem:
      command: npx
      args:
        - "-y"
        - "@modelcontextprotocol/server-filesystem"
        - "/home/user/projects"
      transport: stdio
      
    github:
      command: npx
      args:
        - "-y"
        - "@modelcontextprotocol/server-github"
      env:
        GITHUB_PERSONAL_ACCESS_TOKEN: ${GITHUB_TOKEN}
      transport: stdio
      
    brave_search:
      command: npx
      args:
        - "-y"
        - "@modelcontextprotocol/server-brave-search"
      env:
        BRAVE_API_KEY: ${BRAVE_API_KEY}
      transport: stdio
      
    postgres:
      command: docker
      args:
        - "run"
        - "-i"
        - "--rm"
        - "mcp/postgres"
      env:
        DATABASE_URL: ${DATABASE_URL}
      transport: stdio
```

### Testing MCP Servers

```bash
# List available MCP tools
hermes mcp list

# Test specific server
hermes mcp test filesystem

# Interactive MCP inspector
npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-filesystem /tmp
```

## Creating Custom Skills

Skills live in `~/.hermes/skills/` as markdown files.

### Skill Template

```markdown
---
name: example-skill
description: Does something useful
triggers:
  - "how do I use example"
  - "explain example tool"
dependencies:
  - "example-npm-package"
---

# Example Skill

## What it does
Brief explanation.

## Usage

```bash
npm install example-npm-package
```

```javascript
const example = require('example-npm-package');
example.doThing();
```

## Common patterns
- Pattern 1
- Pattern 2
```

### Installing Skills from Guide

```bash
# Clone the optimization guide
git clone https://github.com/OnlyTerp/hermes-optimization-guide.git

# Symlink all guide skills
ln -s $(pwd)/hermes-optimization-guide/skills/* ~/.hermes/skills/

# Or individual skill
ln -s $(pwd)/hermes-optimization-guide/skills/mcp-filesystem.md ~/.hermes/skills/
```

### Skill Curator

```bash
# Run curator to grade and clean skills
hermes curator

# Curator runs automatically every 7 days by default
# Configure in config.yaml:
curator:
  enabled: true
  schedule: "0 3 * * 0"  # Weekly Sunday 3am
  grade_threshold: 6  # Archive skills below this score
  review_provider: anthropic
  review_model: claude-3-5-haiku-20241022
```

## Durable Execution Features

### Kanban Boards (v0.13+)

```yaml
tenacity:
  kanban:
    enabled: true
    boards:
      - name: development
        lanes:
          - todo
          - in_progress
          - review
          - done
        heartbeat_interval: 60
        retry_budget: 3
        
  checkpoints:
    enabled: true
    directory: ~/.hermes/checkpoints
    max_size_mb: 500
    pruning:
      enabled: true
      keep_last_n: 10
```

Usage:
```
User: "Add feature X to project Y and deploy"
Agent creates Kanban card → moves through lanes → reports status
```

### Persistent Goals

```
/goal set "Deploy the new API endpoint to production"
/goal list
/goal pause goal_abc123
/goal resume goal_abc123
/goal clear goal_abc123
```

Goals persist across sessions and keep the agent focused until completion.

### Cron Jobs (No-Agent Watchdogs)

```yaml
cron:
  jobs:
    - name: disk_space_check
      schedule: "*/30 * * * *"  # Every 30 min
      command: "df -h | grep -E '9[0-9]%|100%'"
      no_agent: true  # Just run command, don't involve LLM
      alert_on: stderr
      
    - name: backup
      schedule: "0 2 * * *"  # Daily 2am
      command: "hermes backup --output /backups/hermes-$(date +%F).tar.gz"
      no_agent: true
```

## Security Configuration

### Production Security Settings

```yaml
security:
  # Redact secrets in logs (default: true in v0.13+)
  redact_secrets: true
  
  # Approval modes: auto, manual, quarantine
  approval_mode: manual
  
  # Tool restrictions
  tool_allowlist:
    - read_file
    - write_file
    - execute_command
    - mcp_*
    
  tool_denylist:
    - dangerous_tool
    
  # Command execution sandbox
  sandbox:
    enabled: true
    allowed_directories:
      - /home/hermes/workspace
      - /tmp/hermes
    forbidden_commands:
      - rm -rf /
      - dd if=
      - mkfs
      
  # Rate limiting
  rate_limits:
    requests_per_minute: 60
    tokens_per_hour: 500000
    
  # Webhook signature verification
  webhooks:
    require_signatures: true
    allowed_ips:
      - 192.168.1.0/24
```

### Platform-Specific Security

**Telegram:**
```yaml
gateways:
  telegram:
    allowed_users:
      - 123456789
    block_groups: true  # Only allow DMs
    require_authorization: true
```

**Discord:**
```yaml
gateways:
  discord:
    allowed_roles:
      - "Admin"
      - "Developer"
    allowed_guilds:
      - "1234567890"  # Specific server ID
    reject_dms: true
```

**Webhooks:**
```yaml
gateways:
  webhook:
    port: 3001
    path: /webhook
    secret: ${WEBHOOK_SECRET}
    verify_signatures: true
    require_api_key: true
    api_keys:
      - ${WEBHOOK_API_KEY_1}
```

## Observability & Monitoring

### Langfuse Integration

```yaml
observability:
  langfuse:
    enabled: true
    public_key: ${LANGFUSE_PUBLIC_KEY}
    secret_key: ${LANGFUSE_SECRET_KEY}
    host: https://cloud.langfuse.com
    trace_all: true
    capture_io: true
    
  logging:
    level: info  # debug, info, warn, error
    file: ~/.hermes/logs/hermes.log
    max_size_mb: 100
    max_files: 10
```

### Prometheus Metrics

```yaml
observability:
  prometheus:
    enabled: true
    port: 9090
    path: /metrics
```

Key metrics:
- `hermes_requests_total` - Total requests by platform/status
- `hermes_tokens_used` - Token consumption by model
- `hermes_cost_usd` - Estimated cost
- `hermes_latency_seconds` - Response times

### Dashboard Analytics

Access at `http://localhost:3000` after running `hermes dashboard`:

- Real-time session view
- Token/cost tracking
- Model performance comparison
- Platform activity charts
- Skill usage statistics
- Error rate monitoring

## Troubleshooting

### Common Issues

**1. "Cannot find module '@nousresearch/hermes-agent'"**
```bash
# Reinstall globally
npm uninstall -g @nousresearch/hermes-agent
npm install -g @nousresearch/hermes-agent

# Or use npx
npx @nousresearch/hermes-agent
```

**2. Telegram bot not responding**
```bash
# Check token validity
curl https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe

# Verify webhook isn't set (conflicts with polling)
curl https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/deleteWebhook

# Check logs
DEBUG=hermes:telegram hermes daemon
```

**3. MCP server connection fails**
```bash
# Test server directly
npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-filesystem /tmp

# Check permissions
ls -la ~/.hermes/mcp-servers/

# Verify environment variables
env | grep -E 'GITHUB|BRAVE|DATABASE'
```

**4. Out of memory errors**
```yaml
# Reduce context window
providers:
  anthropic:
    max_tokens: 2048  # Down from 4096
    
# Enable context compression
memory:
  compression:
    enabled: true
    target_tokens: 4000
```

**5. High costs**
```bash
# Check token usage
hermes stats

# Enable cost-optimized routing
models:
  router:
    strategy: cost_optimized

# Use local models for simple tasks
providers:
  lm_studio:
    default_model: qwen-2.5-coder-32b-instruct
```

**6. Skills not loading**
```bash
# Verify directory
ls -la ~/.hermes/skills/

# Check skill syntax
hermes validate ~/.hermes/skills/my-skill.md

# Force reload
hermes --reload-skills
```

### Debug Mode

```bash
# Full debug output
DEBUG=hermes:* hermes daemon

# Specific subsystems
DEBUG=hermes:telegram,hermes:mcp hermes daemon

# Save debug logs
DEBUG=hermes:* hermes daemon 2>&1 | tee debug.log
```

### Validation Commands

```bash
# Validate config
hermes validate

# Test provider connectivity
hermes test-providers

# Check MCP servers
hermes mcp list

# Verify skills
hermes skills validate-all
```

## Real-World Patterns

### Pattern 1: Multi-Model Routing

```yaml
# Use cheap models for simple tasks, premium for complex
models:
  router:
    enabled: true
    rules:
      - if: "token_count < 1000 and !contains(user_input, 'code')"
        use: cerebras  # $0.60/1M tokens
      - if: "contains(user_input, 'write code')"
        use: claude_sonnet
      - if: "contains(user_input, 'analyze image')"
        use: gemini_flash
      - default: claude_haiku
```

### Pattern 2: Secure Webhook Handler

```yaml
gateways:
  webhook:
    enabled: true
    port: 3001
    path: /webhook
    secret: ${WEBHOOK_SECRET}
    handlers:
      github:
        events:
          - push
          - pull_request
        action: "trigger_skill:github-pr-reviewer"
      stripe:
        verify_signature: true
        action: "trigger_skill:payment-processor"
```

### Pattern 3: Automated Code Review

```yaml
cron:
  jobs:
    - name: review_prs
      schedule: "0 */2 * * *"  # Every 2 hours
      command: "hermes chat 'Review open GitHub PRs in repo org/project'"
      provider: anthropic
      model: claude-3-5-sonnet-20241022
      
skills:
  # Link github-pr-reviewer.md skill
```

### Pattern 4: Cost-Optimized Local First

```yaml
models:
  router:
    strategy: local_first
    fallback_on_error: true
    
providers:
  lm_studio:
    endpoint: http://localhost:1234/v1
    default_model: qwen-2.5-coder-32b-instruct
    timeout: 60000
    
  anthropic:  # Fallback for complex tasks
    api_key: ${ANTHROPIC_API_KEY}
    default_model: claude-3-5-haiku-20241022
```

### Pattern 5: Multi-Platform Broadcast

```bash
# Send message to all platforms
hermes broadcast "System maintenance in 10 minutes"

# Platform-specific routing in config.yaml
gateways:
  telegram:
    broadcast_channels:
      - "@myteamupdates"
  discord:
    broadcast_channels:
      - "1234567890"  # Channel ID
  slack:
    broadcast_channels:
      - "#general"
```

## Reference Architecture

**Solo Developer Setup:**
- Hermes on local machine
- Telegram bot for mobile access
- LM Studio for local models
- MCP filesystem + GitHub servers
- Monthly cost: ~$10 (API only)

**Small Team Setup:**
- Hermes on VPS (Hetzner CX22)
- Telegram + Discord + Slack
- Claude Haiku primary, Cerebras fallback
- Langfuse for observability
- Monthly cost: ~$50 (VPS + API)

**Production Setup:**
- Hermes cluster behind load balancer
- All platforms enabled
- Multi-region model routing
- Langfuse + Prometheus + Grafana
- Redis session storage
- Automated backups to S3
- Monthly cost: $200-500 (infrastructure + API)

## Additional Resources

- [Official Hermes Docs](https://github.com/NousResearch/hermes-agent)
- [Optimization Guide](https://github.com/OnlyTerp/hermes-optimization-guide)
- [MCP Server List](https://github.com/punkpeye/awesome-mcp-servers)
- [Skill Examples](https://github.com/OnlyTerp/hermes-optimization-guide/tree/main/skills)
- [Discord Community](https://discord.gg/hermes-agent)

## Quick Reference

```bash
# Essential commands
hermes                    # Start TUI
hermes daemon            # Start headless
hermes dashboard         # Start web UI
hermes update            # Update to latest
hermes curator           # Grade skills
hermes backup            # Backup data
hermes validate          # Check config

# Debugging
DEBUG=hermes:* hermes daemon
hermes test-providers
hermes mcp list
hermes sessions list

# Management
systemctl restart hermes
journalctl -u hermes -f
hermes stats
```
