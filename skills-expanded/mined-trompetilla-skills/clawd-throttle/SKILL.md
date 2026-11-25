---
name: clawd-throttle
description: Automatically routes LLM requests to the cheapest capable model based on prompt complexity. Classifies prompts on 8 dimensions in under 1ms, supports 8 providers and 27+ models across three routing modes (eco, standard, performance). Works as both an MCP server and an HTTP reverse proxy compatible with any OpenAI/Anthropic client.
homepage: https://github.com/liekzejaws/clawd-throttle
metadata: {"openclaw":{"emoji":"🏎️","requires":{"bins":["node"]},"install":[{"id":"clawd-throttle","kind":"node","script":"scripts/setup.sh","label":"Setup Clawd Throttle (API keys + routing mode)"}]}}
---

# Clawd Throttle

Route every LLM request to the cheapest model that can handle it. Stop
paying Opus prices for "hello" and "summarize this."

## Supported Providers

| Provider | Models | Input $/MTok | Output $/MTok |
|----------|--------|-------------|---------------|
| **Anthropic** | Opus 4.6, Opus 4.5, Sonnet 4.5, Haiku 4.5, Haiku 3.5 | $0.80–$15.00 | $4.00–$75.00 |
| **OpenAI** | GPT-5.2, GPT-5.1, GPT-5-mini, GPT-5-nano, GPT-4o, GPT-4o-mini, o3 | $0.05–$2.50 | $0.40–$14.00 |
| **Google** | Gemini 2.5 Pro, 2.5 Flash, 2.0 Flash Lite | $0.02–$1.25 | $0.10–$10.00 |
| **DeepSeek** | DeepSeek V3, DeepSeek R1 | $0.30–$0.70 | $1.20–$2.50 |
| **xAI** | Grok 4, Grok 3, Grok 3 Mini, Grok 4.1 Fast | $0.20–$3.00 | $0.50–$15.00 |
| **Moonshot** | Kimi K2.5, K2 Thinking | $0.60 | $3.00 |
| **Mistral** | Mistral Large, Small, Codestral | $0.10–$2.00 | $0.30–$6.00 |
| **Ollama** | Any local model | $0.00 | $0.00 |

All API keys are **optional**. Configure one or more providers — Clawd Throttle routes to the best available model.

## How It Works

1. Your prompt arrives (via MCP tool call or HTTP proxy endpoint)
2. The classifier scores it on **8 dimensions** (token count, code presence,
   reasoning markers, simplicity indicators, multi-step patterns, question
   count, system prompt complexity, conversation depth) in **under 1 millisecond**
3. The composite score maps to a tier: **simple** (≤0.30), **standard**, or **complex** (≥0.65)
4. The router picks the first model from a preference list whose provider is configured
5. The request is proxied to the selected provider's API
6. The routing decision and cost are logged to a local JSONL file (prompt content is never stored)

## Routing Modes

Uses **preference lists** — ordered arrays of models per (mode, tier). The router picks the first model whose provider has a configured API key.

| Mode | Simple | Standard | Complex |
|------|--------|----------|---------|
| **eco** | Ollama, Flash Lite, GPT-5-nano | Flash, GPT-4o-mini, DeepSeek V3 | DeepSeek R1, Kimi K2.5, Sonnet |
| **standard** | Flash, GPT-4o-mini, DeepSeek V3 | Kimi K2.5, Sonnet, GPT-5.1 | Opus 4.5, GPT-5.2, Grok 4 |
| **performance** | Haiku 4.5, GPT-5-mini, Kimi K2.5 | Sonnet, GPT-5.1, Grok 3 | Opus 4.6, GPT-5.2, o3 |

## HTTP Proxy Mode

Drop-in reverse proxy that accepts **OpenAI** and **Anthropic** API formats. Point any client at it — no code changes needed.

```bash
npm start -- --http         # MCP + HTTP proxy
npm start -- --http-only    # HTTP proxy only (port 8484)
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v1/messages` | Anthropic Messages API format |
| POST | `/v1/chat/completions` | OpenAI Chat Completions format |
| GET | `/health` | Health check |
| GET | `/stats` | Routing stats and cost savings |

### Response Headers

Every response includes routing metadata:

| Header | Description |
|--------|-------------|
| `X-Throttle-Model` | Model that handled the request |
| `X-Throttle-Tier` | Classified tier (simple/standard/complex) |
| `X-Throttle-Score` | Raw classifier score (0.00–1.00) |

## MCP Tools

| Tool | Description |
|------|-------------|
| `route_request` | Send prompt to cheapest capable model, get response + routing metadata |
| `classify_prompt` | Analyze complexity without making an API call (diagnostic) |
| `get_routing_stats` | Cost savings, model distribution, tier breakdown |
| `set_mode` | Change routing mode at runtime (eco/standard/performance) |
| `get_config` | View current config (keys redacted) |
| `get_recent_routing_log` | Inspect recent routing decisions |

## Overrides

- **Heartbeats/summaries**: "ping", "summarize this" → always cheapest
- **Force model**: `/opus`, `/deepseek`, `/grok`, `/kimi`, `/mistral`, `/local`, `/gpt-5`, `/o3`
- **HTTP header**: `X-Throttle-Force-Model: deepseek`
- **Sub-agents**: Pass `parentRequestId` to step down one tier automatically

## Setup

```bash
npm install
npm run setup:unix     # macOS/Linux — prompts for API keys + mode
npm run setup          # Windows
npm start              # MCP stdio server
```

At least one provider API key is required (or Ollama running locally).

### Environment Variables

| Variable | Provider |
|----------|----------|
| `ANTHROPIC_API_KEY` | Anthropic |
| `OPENAI_API_KEY` | OpenAI |
| `GOOGLE_AI_API_KEY` | Google AI |
| `DEEPSEEK_API_KEY` | DeepSeek |
| `XAI_API_KEY` | xAI/Grok |
| `MOONSHOT_API_KEY` | Moonshot/Kimi |
| `MISTRAL_API_KEY` | Mistral |
| `OLLAMA_BASE_URL` | Ollama (default: http://localhost:11434/v1) |

## Privacy

- Prompt content is **never stored** — only SHA-256 hashes in logs
- All data stays local in `~/.config/clawd-throttle/`
- API keys stored in your local config or environment

## Requirements

- Node.js 18+
- At least one LLM provider API key (or Ollama)
