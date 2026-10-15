---
name: skill-cerebras
description: "Flaskp proxy server from Cerebase to OpenClaw"
---

# Cerebras

Operate Cerebras API as a self-contained local OpenAI-compatible proxy server.

## Overview

This skill runs a local Flask server that proxies requests to the Cerebras inference API (`https://api.cerebras.ai/v1/chat/completions`). It enables compatibility for OpenClaw/LLM workflows that expect `/v1/completions` or default streaming behaviors that Cerebras does not natively support or handle perfectly for the given tools. It seamlessly translates prompts, ensures strict JSON structures, normalizes roles, and optionally streams data back in event-stream format.

## Agent guidance

Treat this skill as the canonical `cerebras` interface for OpenClaw operations relying on rapid inference via Cerebras models. Another OpenClaw/LLM agent should think in terms of:
- `cerebras start`
- `cerebras check` or querying standard `v1/models`

When another OpenClaw/LLM agent uses this skill, prefer this operating style:
- Use `cerebras start` to boot the local proxy server before routing prompts.
- Default to pointing the OpenClaw client to `http://localhost:11434/v1` for models (effectively bypassing the official API base path to utilize the local proxy).
- Do not forget to properly define `CEREBRAS_API_KEY` and `CEREBRAS_MODEL` in the `.env` file prior to starting the skill.

## Installation

**First time setup:**
```bash
cd /path/to/Skill_Cerebras

# Install dependencies if not already installed
pip install -r requirements.txt
```

## First Run Setup

**1. Configure the `.env` file:**
Rename `.env.sample` to `.env` and fill in your Cerebras API key and desired model.
```bash
cp .env.sample .env
```
Inside `.env`:
```env
CEREBRAS_API_KEY=csk-YOUR_API_KEY_HERE
CEREBRAS_MODEL=llama3.1-8b
```

**2. Start the server:**
```bash
python /path/to/Skill_Cerebras/cerebrasProxy.py &
sleep 2
```
The server binds to port `11434` (Ollama default style).

## API Endpoints

### Models
**Check available models:**
```bash
curl -s http://localhost:11434/v1/models
```
Returns a list indicating the current proxy target model configuration.

### Completions & Chat Completions
**Send a chat message (OpenAI compatible payload):**
```bash
curl -s -X POST http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello, Cerebras!"}],
    "stream": false
  }'
```

**Send a legacy completion request (which gets correctly routed internally):**
```bash
curl -s -X POST http://localhost:11434/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello, Cerebras!",
    "stream": false
  }'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CEREBRAS_API_KEY` | None | Your Cerebras platform API Key. |
| `CEREBRAS_MODEL` | llama3.1-8b | The model to use for completion requests. |

## Notes

- Missing tools/tool_choice in payloads will be automatically stripped before forwarding.
- Non-chat completions (`/v1/completions`) automatically format a system/user role prompt map to guarantee compliance with Cerebras `chat/completions` API structure.
- Streaming responses artificially map chunked outputs if `stream: true` is enabled by returning generated tokens progressively.

## File Structure

```
Skill_Cerebras/
├── SKILL.md                 # This file
├── cerebrasProxy.py         # Flask server proxying the requests
├── requirements.txt         # Dependencies
├── .env.sample              # Environment variables template
└── .env                     # Your actual env config (Git ignored)
```

## Command mental model

Map common intents to these actions:
- **cerebras start** → start `python cerebrasProxy.py`
- **cerebras check** → `GET /v1/models` to confirm the proxy is responding.

Use this naming consistently in agent reasoning and replies so the skill is easier to discover and operate.
