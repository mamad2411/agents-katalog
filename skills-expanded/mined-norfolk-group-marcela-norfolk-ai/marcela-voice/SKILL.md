---
name: marcela-voice
description: Marcela Voice AI Agent for Norfolk AI. Use when building, debugging, or maintaining the Marcela voice call agent powered by Gemini 2.5 Flash streaming, Twilio ConversationRelay, Deepgram STT, and ElevenLabs TTS.
metadata:
  author: norfolk-ai
  version: "1.0"
---

# Marcela Voice Agent

## Overview

Marcela Voice is an inbound phone call agent for Norfolk AI. She answers calls, screens callers, transfers qualified calls to Ricardo, and handles general inquiries. The architecture is optimized for sub-500ms response latency using streaming throughout the pipeline.

## Architecture

```
Caller → Twilio → ConversationRelay (Deepgram STT) → WebSocket → Gemini 2.5 Flash (streaming)
Gemini tokens → WebSocket → ConversationRelay (ElevenLabs TTS) → Caller
```

- **Server**: `voice_server.py` — Starlette app serving HTTP + WebSocket on a single port
- **LLM**: Gemini 2.5 Flash via `google-genai` SDK (streaming)
- **STT**: Deepgram nova-3-general via ConversationRelay
- **TTS**: ElevenLabs Flash 2.5 via ConversationRelay
- **Deployment**: Railway (Docker container)

## Key Constraints

1. **Single port only** — Railway exposes one port. HTTP and WebSocket must share it. Starlette handles this natively.
2. **python-multipart required** — Starlette form parsing fails without it. Must be in `requirements.txt`.
3. **Sentence-boundary streaming** — Tokens are buffered and sent at sentence boundaries (`. `, `! `, `? `) for natural speech. Do not send token-by-token.
4. **Output tokens dominate latency** — Reducing output length has ~50x more impact than reducing prompt size.

## Voice Configuration

- Voice: Jessica Anne Bogart (ElevenLabs)
- Speed: 1.05x (slightly faster for energy)
- Stability: 0.55 (more expressive)
- Similarity: 0.80 (good fidelity)
- Style: Mel Robbins-inspired — direct, warm, energetic, motivating

## Multilingual Support

Automatic language detection via Deepgram `multi` mode. Priority languages with dedicated ElevenLabs voices:
- English (en-US)
- Portuguese Brazilian (pt-BR)
- Spanish (es-ES)
- Italian (it-IT)

## Call Screening Rules

The prompt uses a layered system with an explicit priority rule:

1. **Always Transfer**: Existing clients, Ricardo's contacts
2. **Transfer if Qualified**: C-level with genuine AI need, funded startups, enterprise buyers
3. **Never Transfer**: Cold sales, recruiters, spam, surveys
4. **Borderline**: Take message instead of transferring

**Critical rule**: One disqualifying signal overrides all qualifying ones.

## Debugging Checklist

1. Check Railway deployment logs for startup errors
2. Verify `PUBLIC_URL` env var is set correctly (WSS URL)
3. Check that Twilio voice webhook points to `/voice/incoming`
4. WebSocket endpoint is `/ws` on the same host
5. Verify `python-multipart` is in requirements.txt
6. Check Gemini API key is valid

## Environment Variables

- `GEMINI_API_KEY` — Google Gemini API key (required)
- `TWILIO_ACCOUNT_SID` — Twilio Account SID
- `TWILIO_AUTH_TOKEN` — Twilio Auth Token
- `TWILIO_API_KEY` — Twilio API Key (for ConversationRelay)
- `TWILIO_API_SECRET` — Twilio API Secret
- `PUBLIC_URL` — Public WSS URL for ConversationRelay callbacks
- `PORT` — Server port (default: 5005)
