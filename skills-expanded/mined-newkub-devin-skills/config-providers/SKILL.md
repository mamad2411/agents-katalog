---
name: follow-lib-openai-config-providers
description: Config openai SDK — baseURL, compatible providers, org/project keys
argument-hint: "[provider]"
related:
  - follow-lib-openai
  - follow-secret-manager
  - check-secrets
  - run-verify
  - resolve-errors
---

## Goal

Configure the `openai` SDK with different providers — `baseURL` for OpenAI-compatible endpoints, org/project keys, and env config

## Scope

Use when configuring the `openai` client — covers `baseURL` override for compatible providers (Azure, OpenRouter, Together, local LLMs), `organization`/`project` keys, and secrets handling

## Execute

### 1. Read Current Config

> Goal: inspect the current client config and env vars

1. check whether a `new OpenAI(...)` already exists — merge with the original, never overwrite
2. run `/check-secrets env-vars` — see which of `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_ORG_ID`, `OPENAI_PROJECT_ID` are set
3. identify the provider actually used — official OpenAI or a compatible endpoint

### 2. Configure Client Options

> Goal: set client options per provider

```ts
import OpenAI from 'openai'

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,   // default: env OPENAI_API_KEY
  baseURL: process.env.OPENAI_BASE_URL, // override for compatible providers
  organization: process.env.OPENAI_ORG_ID,
  project: process.env.OPENAI_PROJECT_ID,
  timeout: 60_000,
  maxRetries: 2,
})
```

1. `apiKey` — read from env `OPENAI_API_KEY` (default) or that provider's env var
2. `baseURL` — set for OpenAI-compatible providers such as OpenRouter `https://openrouter.ai/api/v1`, Azure endpoints, local LLM servers (Ollama `http://localhost:11434/v1`, LM Studio) — see the provider docs for the correct URL
3. `organization`/`project` — needed for OpenAI accounts with multiple orgs/projects; use env `OPENAI_ORG_ID`/`OPENAI_PROJECT_ID`
4. always set `timeout` and `maxRetries` — the defaults may not suffice for long requests
5. some providers need extra headers (e.g. OpenRouter `HTTP-Referer`) — use the `defaultHeaders` option; see the provider docs

### 3. Verify Provider Compatibility

> Goal: confirm the endpoint supports the APIs used

1. Compatible providers support nearly all of the Chat Completions API — but the Responses API, structured output, and tools may not be supported by every provider
2. test a simple call first: `client.chat.completions.create({ model, messages })`
3. check the model name matches the provider — model names differ across providers
4. if the provider lacks a needed feature → report the limitation to the user

### 4. Verify

> Goal: smoke test a real client call

1. test one real request — the response is correct with no auth/URL errors
2. run `/run-verify` for lint/typecheck
3. if it breaks → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Never hardcode API keys — env vars only; secrets through `/follow-secret-manager`
- Never call the provider from client-side code — always proxy through the server
- Always set `timeout` + `maxRetries` — handle 429 backoff
- `openai@7.x` requires Node.js 22+ — check the runtime first
- Use `/follow-lib-openai` for the full reference

## Expected Outcome

- Client config points at the right provider via `baseURL`/env
- Org/project keys and timeout/retry fully set
- Smoke test call passes — no auth/URL errors
- No secrets leaked in code
