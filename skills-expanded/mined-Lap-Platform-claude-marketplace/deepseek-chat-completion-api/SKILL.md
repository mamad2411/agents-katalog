---
name: deepseek-chat-completion-api
description: "DeepSeek Chat Completion API skill. Use when working with DeepSeek Chat Completion for chat. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# DeepSeek Chat Completion API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.deepseek.com

## Setup
1. No auth setup needed
3. POST /chat/completions -- create first completions

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### chat
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat/completions | Create Chat Completion |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a completion?" -> POST /chat/completions

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
