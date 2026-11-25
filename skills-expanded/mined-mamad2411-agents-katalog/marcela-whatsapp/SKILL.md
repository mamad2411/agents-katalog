---
name: marcela-whatsapp
description: Marcela WhatsApp AI Agent for Norfolk AI. Use when building, debugging, or maintaining the Marcela WhatsApp chatbot powered by Gemini 2.5 Flash on Vercel serverless.
metadata:
  author: norfolk-ai
  version: "1.0"
---

# Marcela WhatsApp Agent

## Overview

Marcela is a WhatsApp AI chatbot for Norfolk AI, deployed as a Vercel serverless function. She uses Google Gemini 2.5 Flash via direct HTTP requests and responds to messages via TwiML inline responses.

## Architecture

- **Entry point**: `api/index.py` (Vercel serverless) — mirrors `server.py`
- **LLM**: Gemini 2.5 Flash via direct HTTP (no SDK)
- **Messaging**: Twilio WhatsApp with TwiML inline responses
- **Deployment**: Vercel at `https://marcela-norfolk-ai.vercel.app`

## Key Constraints

1. **No heavy Python SDKs on Vercel** — Twilio SDK and Anthropic SDK both cause dependency conflicts. Use `requests` for direct HTTP calls only.
2. **TwiML responses do not bypass Meta restrictions** — Error 63112 is a Meta/WABA-level block that cannot be fixed with code.
3. **Conversation history is in-memory** — Resets on cold start. Acceptable for serverless.
4. **Message length limit** — WhatsApp messages are truncated to 1500 characters.

## Trigger System (Group Chats)

- `@marcela` or `hey marcela` — normal response
- `/ask <question>` — normal response
- `/quick <question>` — ultra-short 1-3 sentence response
- `/translate <text>` — translation (defaults to English)
- In direct messages, Marcela always responds

## Debugging Checklist

1. Check `https://marcela-norfolk-ai.vercel.app/health` — should return 200 OK
2. Check Twilio message logs for error codes via API
3. Error 63112 = Meta disabled the WABA — fix in Meta Business Suite, not code
4. Error 11200 = Webhook URL unreachable — check Vercel deployment
5. Check Vercel deployment logs for Python errors

## Environment Variables

- `GEMINI_API_KEY` — Google Gemini API key (required)
- `TWILIO_ACCOUNT_SID` — Twilio Account SID
- `TWILIO_AUTH_TOKEN` — Twilio Auth Token
- `WHATSAPP_SENDER` — WhatsApp sender number (format: `whatsapp:+15559178507`)
