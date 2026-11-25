# Nduna Bot

Telegram bot for customer support and delivery assistance.

## Overview

**Platform**: Telegram
**Status**: Production Ready
**Language**: Python

## Features

- Order tracking
- Route queries with ETA
- Restaurant search
- Support tickets
- Promotions

## Commands

```
/start - Welcome message
/help - Available commands
/order <id> - Track order
/nearby - Find restaurants
/eta <from> <to> - Calculate delivery time
/support <message> - Create ticket
/promo - Current promotions
```

## Configuration

```yaml
bot:
  token: ${TELEGRAM_BOT_TOKEN}
  webhook_url: ${WEBHOOK_URL}
  admin_chat_id: ${ADMIN_CHAT_ID}
  
integrations:
  backend: ${API_URL}
  glitchtip: ${GLITCHTIP_DSN}
  route_memory: ${ROUTE_MEMORY_API}
```

## Deployment

```bash
cd agents/nduna
docker-compose up -d
```
