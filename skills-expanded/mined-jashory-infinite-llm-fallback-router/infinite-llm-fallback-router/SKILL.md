---
name: infinite-llm-fallback-router
description: Zero-dependency multi-provider LLM failover proxy & 9Router patch kit. Chains OpenAI, Anthropic (/v1/messages), Gemini, Groq, and OpenRouter endpoints with automatic HTTP 429/5xx cooldown failover and SSE streaming. Use when setting up resilient local LLM routing for Claude Code, Antigravity, Cursor, or Cline.
---

# Infinite LLM Auto-Fallback Router (`infinite-llm-fallback-router`)

When the user asks to install, configure, or start the Infinite LLM Fallback Router from this repository:

## 1. One-Command Installation (Agent & CLI)
Run the included cross-platform installer:
```bash
python install.py
```
Or install as a global CLI command via `pip` / `uv`:
```bash
pip install .
```

## 2. Starting the Local Proxy Server
```bash
python ~/.infinite-llm-router/llm_fallback_router.py --port 20128
```
- **OpenAI Endpoint**: `http://127.0.0.1:20128/v1/chat/completions`
- **Anthropic Endpoint (for Claude Code)**: `http://127.0.0.1:20128/v1/messages`
- **Live Telemetry**: `http://127.0.0.1:20128/stats`

## 3. Connecting Claude Code / Cursor / Antigravity
Set your client's base URL to the local router so it never stops on HTTP 429 quota walls:
```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:20128"
export OPENAI_BASE_URL="http://127.0.0.1:20128/v1"
```
