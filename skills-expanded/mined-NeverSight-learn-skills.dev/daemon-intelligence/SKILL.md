---
name: daemon-intelligence
description: >
  Complete reference for building with the Daemon-AI platform API — an AI agent backend
  that provides access to 300+ LLMs via OpenRouter, blockchain intelligence tools (MCP),
  web search, and real-time finance data with USDC payments on Solana.
  
  Use this skill whenever the user wants to: integrate with Daemon-AI API, build an AI agent
  using Daemon-AI, authenticate users via email or Solana wallet, call the chat completions
  endpoint, work with MCP tools (daemon-intel, exa, arkham), consume the finance or discover
  endpoints, manage API keys, or understand the platform's agentic loop pattern.
  
  Also trigger this skill when the user mentions daemonai.io, daemon_<key> API keys, or
  asks how to use any feature of the Daemon-AI platform as a developer or as an AI agent.
---

# Daemon-AI Platform Skill

Daemon-AI (`daemon-ai-backend`) is an **AI agent backend platform** built on Express + TypeScript.
It exposes an OpenAI-compatible API layered on top of OpenRouter, with blockchain tools,
finance data, and USDC-based billing.

**Base URL:** `https://daemon-ai-production.up.railway.app`

---

## Quick orientation

| Who you are | What you need | Where to look |
|---|---|---|
| Developer integrating auth | Register, login, email verify | `references/public-endpoints.md` |
| Developer building an app | Chat, models, agent info, finance | `references/agent-endpoints.md` |
| Building an agentic loop | Tool use, streaming, MCP tools | `references/agentic-patterns.md` |
| AI agent calling the API | Auth flow + chat completions + tools | All three reference files |

---

## Authentication overview

There are **two key auth mechanisms** for public-facing work:

### 1. Agent API Key (`daemon_*`)
Used for all `/v1/*` endpoints (except auth registration/login which are public).

```
Authorization: Bearer daemon_<key>
```

Keys are prefixed with `daemon_` and returned **once** at creation/first login.
Store them securely — they cannot be retrieved again.

### 2. User Session Token
Returned on login. Used for user-management routes (`/v1/agents`).

```
Authorization: Bearer <session_token>
```

Session tokens expire after 30 days.

---

## Endpoint groups

| Group | Auth required | Reference |
|---|---|---|
| Health, Auth, Billing webhook | None | `references/public-endpoints.md` |
| Chat, Models, Agent info/settings | Agent API Key | `references/agent-endpoints.md` |
| Discover, Finance, Chat history | Agent API Key | `references/agent-endpoints.md` |
| MCP server management | Agent API Key | `references/agent-endpoints.md` |
| Agentic loop, streaming, tool use | — | `references/agentic-patterns.md` |

---

## Subscription tiers

| Tier | Condition | Model access | Token limit |
|---|---|---|---|
| Free | Balance < $10 USDC | Whitelisted free models only | 1M tokens/month |
| Paid (Pro) | Balance ≥ $10 USDC | All 300+ OpenRouter models | Custom (default 1M) |

Free models include: `arcee-ai/trinity-large-preview:free`, `stepfun/step-3.5-flash:free`

---

## Rate limits

- **Free tier:** 10 requests / minute per API key
- **Paid tier:** 60 requests / minute per API key

---

## Common response patterns

**Success:**
```json
{ "success": true, "data": { ... } }
```

**Error:**
```json
{ "success": false, "error": "Human-readable message", "code": "MACHINE_CODE" }
```

**Pagination:**
```json
{
  "data": [...],
  "pagination": { "page": 1, "limit": 20, "total": 100, "pages": 5 }
}
```

---

## Reference files

Read these when you need full endpoint details:

- **`references/public-endpoints.md`** — No-auth endpoints: health, register, login, wallet nonce, email verify, billing webhook
- **`references/agent-endpoints.md`** — Agent API key endpoints: chat, models, agent info, finance, discover, chat history, MCP servers, API key management
- **`references/agentic-patterns.md`** — How the agentic loop works, MCP tools available, streaming event format, tool execution, graph data
