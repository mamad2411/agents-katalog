---
name: zavu-rules
description: Foundational context for the Zavu unified messaging API. Always loaded.
---

# Zavu API Context

Zavu is a unified multi-channel messaging API. One API to send messages via SMS, WhatsApp, Telegram, Email, Instagram, and Voice with ML-powered intelligent routing.

## SDK Ecosystem

| Language | Package | Install |
|----------|---------|---------|
| TypeScript | `@zavudev/sdk` | `npm add @zavudev/sdk` |
| Python | `zavudev` | `pip install zavudev` |
| Go | `github.com/zavudev/sdk-go` | `go get github.com/zavudev/sdk-go` |
| PHP | `zavudev/sdk-php` | Composer |
| Ruby | `zavudev/sdk-ruby` | RubyGems |

## Tooling

| Tool | Purpose | Install |
|------|---------|---------|
| `zavu` CLI | Interact with the API from the terminal; manage Zavu Functions (serverless TypeScript on Zavu Cloud) | `npx zavudev@latest` (no install), or `npm install -g zavudev` |
| `@zavudev/functions` | Runtime package for Zavu Functions. Provides `defineAgent`, `defineTool`, `defineFunction` declarative APIs. | Pre-installed in the function runtime — `import { defineAgent } from "@zavudev/functions"` (no install needed). |

The CLI is the primary interface for **Zavu Functions**: serverless TypeScript that runs on Zavu Cloud and lets you declare AI agents + tool handlers in code. See the `functions` skill for full coverage.

### TypeScript Init

```typescript
import Zavudev from '@zavudev/sdk';

const zavu = new Zavudev({
  apiKey: process.env['ZAVUDEV_API_KEY'],
});
```

### Python Init

```python
import os
from zavudev import Zavudev

zavu = Zavudev(api_key=os.environ.get("ZAVUDEV_API_KEY"))
```

### Python Async

```python
from zavudev import AsyncZavudev

zavu = AsyncZavudev(api_key=os.environ.get("ZAVUDEV_API_KEY"))
```

### Go Init

```go
import "github.com/zavudev/sdk-go"

client := zavudev.NewClient(os.Getenv("ZAVUDEV_API_KEY"))
```

### Ruby Init

```ruby
require "zavudev"

client = Zavudev::Client.new(api_key: ENV["ZAVUDEV_API_KEY"])
```

### PHP Init

```php
use Zavudev\Client;

$client = new Client(apiKey: getenv('ZAVUDEV_API_KEY'));
```

## Authentication

- Environment variable: `ZAVUDEV_API_KEY`
- Key prefixes: `zv_live_` (production), `zv_test_` (sandbox)
- Header: `Authorization: Bearer <api_key>`
- Sender override header: `Zavu-Sender: <sender_id>`

## Core Conventions

- **Phone numbers**: Always E.164 format (`+14155551234`)
- **Channels**: `auto`, `sms`, `sms_oneway`, `whatsapp`, `telegram`, `email`, `instagram`, `messenger`, `voice`
- **Message types**: `text`, `image`, `video`, `audio`, `document`, `sticker`, `location`, `contact`, `buttons`, `list`, `cta_url`, `request_contact_info`, `location_request`, `reaction`, `template`
- **Pagination**: Cursor-based. All list endpoints return `{ items: [...], nextCursor: string | null }`
- **Idempotency**: Use `idempotencyKey` on send to prevent duplicate messages

## Error Handling

### TypeScript

```typescript
import Zavudev, { APIError } from '@zavudev/sdk';

try {
  await zavu.messages.send({ to: "+14155551234", text: "Hello" });
} catch (error) {
  if (error instanceof APIError) {
    console.error(error.status, error.message);
  }
}
```

### Python

```python
from zavudev import Zavudev, APIError

try:
    zavu.messages.send(to="+14155551234", text="Hello")
except APIError as e:
    print(e.status_code, e.message)
```

## Key Business Rules

1. **WhatsApp 24h window**: Free-form messages require an open conversation window (user messaged you in last 24h). Use template messages to initiate conversations outside the window.
2. **Verification raises limits; it is not permission to send**: an account sends on every channel, to any destination, from its first minute. Identity verification, a saved payment method, a settled deposit or a paid plan raise the daily ceilings, which return `429 daily_limit_exceeded` when spent. Business verification (KYB) gates 10DLC registration, which every US and Canadian (+1) SMS destination needs (`403 ten_dlc_required`); no channel needs it to send. Every `sms`, `sms_oneway`, `email` and `voice` message is read before it is sent and can be held briefly for review (it stays `queued`) or refused (`RISK_BLOCKED`, `RISK_REJECTED`, `RISK_REVIEW_EXPIRED` on the failed message); repeated refusals suspend an account's sending (`403 sending_suspended`). See the `send-message` skill.
3. **URL verification**: SMS/email messages containing URLs require those URLs to be pre-verified via `/v1/urls`.
4. **URL shorteners blocked**: bit.ly, t.co, etc. are always blocked. Use full destination URLs.
5. **Smart routing**: Channel `auto` uses ML to pick the best channel based on cost, deliverability, and contact preferences.
6. **Fallback**: If WhatsApp fails, messages can automatically fall back to SMS (enabled by default).
7. **Voice agents**: An agent can answer and place phone calls when its `voice` config has `enabled: true`. Place outbound calls via `/v1/calls` and fetch transcripts from `/v1/calls/{callId}`. Requires the Voice Agents feature and a live key. See the `ai-agent` skill.

## MCP Server

For direct API execution from AI assistants:

```bash
claude mcp add --transport stdio zavudev_sdk_api \
  --env ZAVUDEV_API_KEY=$ZAVUDEV_API_KEY -- npx -y @zavudev/sdk-mcp
```

Tools available: `search_docs` (search API docs), `execute` (run TypeScript against authenticated client).

## CLI

The `zavudev/cli` package provides terminal access to all API operations.

## Rate Limits

Check `X-RateLimit-Remaining` header. Use `.withResponse()` (TS) or `.with_raw_response()` (Python) to access response headers.

## Message Statuses

`queued` -> `sending` -> `sent` -> `delivered` -> `read` (success path)
`queued` -> `sending` -> `failed` (failure path)
`received` (inbound messages)
`pending_url_verification` (message with URLs awaiting verification)
