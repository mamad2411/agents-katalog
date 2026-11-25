---
name: openclaw-china-docker
description: Deploy and configure OpenClaw AI bot gateway with Chinese IM platforms (Feishu, DingTalk, QQ, WeChat Work) using Docker
triggers:
  - set up openclaw with chinese messaging platforms
  - deploy openclaw docker for feishu and dingtalk
  - configure openclaw china im integration
  - how do i use openclaw docker cn im
  - integrate openclaw with qq bot and wechat work
  - deploy ai bot gateway for chinese platforms
  - configure openclaw with agent reach and aiclient
  - troubleshoot openclaw china docker deployment
---

# OpenClaw China Docker Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill helps you deploy and configure **OpenClaw-China-Docker**, a pre-configured Docker image that integrates OpenClaw AI bot gateway with mainstream Chinese IM platforms including Feishu (Lark), DingTalk, QQ Bot, and WeChat Work (WeCom).

## What is OpenClaw-China-Docker?

OpenClaw-China-Docker is a production-ready Docker image that packages OpenClaw with pre-installed plugins for Chinese IM platforms. It provides:

- **Multi-platform support**: Feishu (official/legacy), DingTalk, QQ Bot, WeChat Work
- **Extended capabilities**: Agent Reach integration (Twitter, Xiaohongshu, Weibo, Douyin)
- **Configuration-driven**: Environment variable based setup with `.env` files
- **Enhanced tooling**: FFmpeg, Playwright, Chinese TTS, OpenCode AI
- **Security**: Docker-in-Docker sandbox mode for code execution
- **Production features**: Data persistence, isolated utility containers

## Installation

### Prerequisites

- Docker and Docker Compose installed
- API keys for AI models (OpenAI, Claude, etc.)
- Bot credentials for desired IM platforms

### Quick Start

```bash
# Clone the repository
git clone https://github.com/justlovemaki/openclaw-china-docker.git
cd openclaw-china-docker

# Copy environment template
cp .env.example .env
# OR use minimal version for quick setup
cp .env.minimal .env

# Edit environment variables
nano .env

# Start services
docker compose up -d

# View logs
docker compose logs -f openclaw

# Stop services
docker compose down
```

### Pull Docker Image Directly

```bash
docker pull justlikemaki/openclaw-docker-cn-im:latest
```

## Core Configuration

### Environment Variables (.env)

The project uses environment variables for configuration. Key sections:

#### AI Model Configuration

```bash
# OpenAI compatible API
OPENCLAW_AI_PROVIDER=openai
OPENCLAW_OPENAI_API_KEY=${OPENAI_API_KEY}
OPENCLAW_OPENAI_BASE_URL=https://api.openai.com/v1
OPENCLAW_OPENAI_MODEL=gpt-4o

# Claude API
OPENCLAW_AI_PROVIDER=anthropic
OPENCLAW_ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
OPENCLAW_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Use AIClient-2-API (recommended for unlimited tokens)
OPENCLAW_OPENAI_BASE_URL=http://your-aiclient-api:8000/v1
```

#### Feishu (Lark) Configuration

```bash
# Official plugin (recommended)
OPENCLAW_FEISHU_ENABLED=true
OPENCLAW_FEISHU_APP_ID=cli_xxx
OPENCLAW_FEISHU_APP_SECRET=xxx
OPENCLAW_FEISHU_VERIFICATION_TOKEN=xxx
OPENCLAW_FEISHU_ENCRYPT_KEY=xxx

# Legacy built-in version
OPENCLAW_FEISHU_OLD_ENABLED=true
OPENCLAW_FEISHU_OLD_APP_ID=cli_xxx
# ... (similar structure)
```

#### DingTalk Configuration

```bash
OPENCLAW_DINGTALK_ENABLED=true
OPENCLAW_DINGTALK_CLIENT_ID=dingxxx
OPENCLAW_DINGTALK_CLIENT_SECRET=xxx
OPENCLAW_DINGTALK_ROBOT_CODE=xxx
```

#### QQ Bot Configuration

```bash
OPENCLAW_QQBOT_ENABLED=true
OPENCLAW_QQBOT_APPID=xxx
OPENCLAW_QQBOT_SECRET=xxx
OPENCLAW_QQBOT_INTENT=1  # Public messages
```

#### WeChat Work (WeCom) Configuration

```bash
OPENCLAW_WECOM_ENABLED=true
OPENCLAW_WECOM_CORP_ID=wwxxx
OPENCLAW_WECOM_AGENT_ID=1000xxx
OPENCLAW_WECOM_SECRET=xxx
OPENCLAW_WECOM_TOKEN=xxx
OPENCLAW_WECOM_ENCODING_AES_KEY=xxx
```

#### Sandbox Configuration

```bash
# Enable Docker-in-Docker sandbox for code execution
OPENCLAW_SANDBOX_MODE=all  # or 'non-main' or 'none'
```

### Docker Compose Setup

Minimal `docker-compose.yml`:

```yaml
version: '3.8'

services:
  openclaw:
    image: justlikemaki/openclaw-docker-cn-im:latest
    container_name: openclaw-cn-im
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "3000:3000"
    volumes:
      - ./workspace:/openclaw/workspace
      - ./data:/openclaw/data
      # Uncomment for Docker sandbox mode
      # - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - TZ=Asia/Shanghai
```

## Key Commands

### Container Management

```bash
# Start services
docker compose up -d

# View logs (all services)
docker compose logs -f

# View logs (specific service)
docker compose logs -f openclaw

# Restart service
docker compose restart openclaw

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### Enter Container

```bash
# Interactive shell
docker compose exec openclaw bash

# Execute single command
docker compose exec openclaw openclaw --version
```

### Upgrade

```bash
# Pull latest changes
git pull origin main

# Pull latest image
docker compose pull

# Recreate containers
docker compose up -d --force-recreate

# Clean old images
docker image prune -f
```

### Plugin Installation (Feishu Example)

```bash
# Use utility container for one-time operations
docker compose run --rm openclaw-utils bash

# Inside container:
cd /openclaw
npx openclaw plugin:install larksuite/openclaw-lark
```

## Common Patterns

### Pattern 1: Full Setup with Multiple Platforms

```bash
# .env configuration
OPENCLAW_AI_PROVIDER=openai
OPENCLAW_OPENAI_API_KEY=${OPENAI_API_KEY}
OPENCLAW_OPENAI_MODEL=gpt-4o

# Enable multiple IM platforms
OPENCLAW_FEISHU_ENABLED=true
OPENCLAW_DINGTALK_ENABLED=true
OPENCLAW_QQBOT_ENABLED=true
OPENCLAW_WECOM_ENABLED=true

# Configure each platform's credentials...
OPENCLAW_FEISHU_APP_ID=cli_xxx
OPENCLAW_DINGTALK_CLIENT_ID=dingxxx
OPENCLAW_QQBOT_APPID=xxx
OPENCLAW_WECOM_CORP_ID=wwxxx
```

```bash
# Deploy
docker compose up -d

# Monitor all platforms
docker compose logs -f | grep -E 'feishu|dingtalk|qqbot|wecom'
```

### Pattern 2: Integration with AIClient-2-API

```bash
# .env - Use AIClient for unlimited tokens
OPENCLAW_AI_PROVIDER=openai
OPENCLAW_OPENAI_BASE_URL=http://aiclient-api:8000/v1
OPENCLAW_OPENAI_API_KEY=dummy-key  # AIClient doesn't require real key
OPENCLAW_OPENAI_MODEL=gpt-4o

# docker-compose.yml - Add AIClient service
services:
  aiclient-api:
    image: justlikemaki/aiclient-2-api:latest
    ports:
      - "8000:8000"
    volumes:
      - aiclient-data:/app/data
  
  openclaw:
    depends_on:
      - aiclient-api
    # ... rest of openclaw config
```

### Pattern 3: Enable Agent Reach for Web Search

Initialize Agent Reach in conversation:

```
禁止使用web_search，web_fetch 工具， 必须使用 agent-reach 的工具来替代你自带的web_search，web_fetch ，并写入tools和记忆文档中
```

This switches from built-in web tools to Agent Reach for searching Twitter, Xiaohongshu, Weibo, Douyin, etc.

### Pattern 4: Sandbox Mode for Secure Code Execution

```bash
# .env
OPENCLAW_SANDBOX_MODE=all  # Run all code in isolated containers

# docker-compose.yml - MUST mount Docker socket
services:
  openclaw:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

```python
# In chat, OpenClaw can now safely execute:
"""
Create a Python script that analyzes data
"""
# Code runs in isolated container, not on host
```

### Pattern 5: Custom Configuration with openclaw.json

```bash
# Mount custom config instead of using env vars
# docker-compose.yml
services:
  openclaw:
    volumes:
      - ./openclaw.json:/openclaw/openclaw.json
```

```json
{
  "ai": {
    "provider": "openai",
    "openai": {
      "apiKey": "${OPENAI_API_KEY}",
      "baseURL": "https://api.openai.com/v1",
      "model": "gpt-4o"
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "${FEISHU_APP_ID}",
      "appSecret": "${FEISHU_APP_SECRET}"
    }
  }
}
```

### Pattern 6: Data Persistence

```bash
# docker-compose.yml - Persist important data
services:
  openclaw:
    volumes:
      - ./workspace:/openclaw/workspace  # Work files
      - ./data:/openclaw/data            # Database & state
      - ./logs:/openclaw/logs            # Log files
```

```bash
# Backup data
tar -czf openclaw-backup-$(date +%Y%m%d).tar.gz workspace/ data/

# Restore data
tar -xzf openclaw-backup-20260517.tar.gz
```

## Troubleshooting

### Issue: Container fails to start

```bash
# Check logs
docker compose logs openclaw

# Common causes:
# 1. Missing required env vars
grep "OPENCLAW_.*_ENABLED=true" .env
# Ensure corresponding credentials are set

# 2. Port conflicts
netstat -tlnp | grep 3000
# Change port in docker-compose.yml if needed
```

### Issue: Feishu plugin not working

```bash
# Verify plugin installation
docker compose exec openclaw bash
npx openclaw plugin:list | grep lark

# Reinstall if needed
npx openclaw plugin:install larksuite/openclaw-lark

# Check webhook URL accessibility
curl -X POST http://your-server:3000/api/feishu/webhook
```

### Issue: AI model not responding

```bash
# Test API connectivity
docker compose exec openclaw bash
curl -H "Authorization: Bearer ${OPENCLAW_OPENAI_API_KEY}" \
     ${OPENCLAW_OPENAI_BASE_URL}/models

# Check model name
echo $OPENCLAW_OPENAI_MODEL
# Must match available models from API
```

### Issue: Docker sandbox not working

```bash
# Ensure Docker socket is mounted
docker compose exec openclaw ls -la /var/run/docker.sock
# Should show: srw-rw---- 1 root docker

# Verify sandbox mode
docker compose exec openclaw env | grep SANDBOX
# Should show: OPENCLAW_SANDBOX_MODE=all

# Check Docker accessibility
docker compose exec openclaw docker ps
# Should list containers, not error
```

### Issue: Permission errors in volumes

```bash
# Fix ownership
sudo chown -R 1000:1000 workspace/ data/ logs/

# Or run container with host user
# docker-compose.yml
services:
  openclaw:
    user: "${UID}:${GID}"
```

### Issue: Memory or performance problems

```bash
# Check resource usage
docker stats openclaw

# Limit resources in docker-compose.yml
services:
  openclaw:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          memory: 2G
```

### Issue: Plugin conflicts

```bash
# List installed plugins
docker compose exec openclaw npx openclaw plugin:list

# Remove conflicting plugin
docker compose exec openclaw npx openclaw plugin:uninstall plugin-name

# Clear plugin cache
docker compose exec openclaw rm -rf /openclaw/.openclaw/plugins/.cache
docker compose restart openclaw
```

## Advanced Configuration

### Environment Variable Reference

Key variables (see `.env.example` for complete list):

- `OPENCLAW_AI_PROVIDER`: `openai`, `anthropic`, `google`, etc.
- `OPENCLAW_SANDBOX_MODE`: `all`, `non-main`, `none`
- `OPENCLAW_LOG_LEVEL`: `debug`, `info`, `warn`, `error`
- `OPENCLAW_SERVER_PORT`: Default `3000`
- `OPENCLAW_SERVER_HOST`: Default `0.0.0.0`

### Multi-Stage Deployment

```bash
# Development
cp .env.minimal .env.dev
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
cp .env.example .env.prod
# Configure all platforms
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Health Checks

```yaml
# docker-compose.yml
services:
  openclaw:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Documentation References

- Quick Start: `docs/quick-start.md`
- Configuration: `docs/configuration.md`
- AIClient Integration: `docs/aiclient-2-api.md`
- Advanced Usage: `docs/advanced.md`
- FAQ: `docs/faq.md`
- Developer Notes: `docs/developer-notes.md`

## Best Practices

1. **Always use `.env` files** instead of hardcoding credentials
2. **Enable only needed platforms** to reduce resource usage
3. **Mount volumes** for workspace and data persistence
4. **Use AIClient-2-API** for cost-effective unlimited token usage
5. **Enable sandbox mode** for secure code execution
6. **Monitor logs** regularly with `docker compose logs -f`
7. **Backup data** before upgrades with `tar -czf`
8. **Keep repository synced** with `git pull` before upgrading
