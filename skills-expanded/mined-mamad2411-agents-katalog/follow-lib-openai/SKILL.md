---
name: follow-lib-openai
description: Use the openai SDK — chat completions, structured output, streaming, embeddings
argument-hint: "[target-or-scope]"
related:
  - follow-lib-zod
  - follow-secret-manager
  - run-verify
  - run-test

---

## Goal

Use the openai SDK — chat completions, structured output, streaming, embeddings

## Scope

Use when the task involves the `openai` SDK — the OpenAI API client server-side on Node.js 22+/Bun (lib openai)

- Compatible providers (Azure, OpenRouter, Ollama, local LLMs) via `baseURL` → `workflows/config-providers/SKILL.md`
- Other vendors (Anthropic/Claude, etc.) are out of scope — use that vendor's skill
- API keys/org/project are managed via `/follow-secret-manager` — never call the API from the client side
- Structured output schemas use zod — for deeper validation → `/follow-lib-zod`

- Latest: `openai@7.23.0` (verified 2026-09-24) — v7 requires Node.js 22+
- References: [apis](references/apis.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Config | `workflows/config-providers/SKILL.md` — `baseURL`, compatible endpoints, org/project keys | Optimize | `workflows/optimize-tokens/SKILL.md` — prompt sizing, caching, model routing 
### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Create `new OpenAI({apiKey})` — the key comes from the env `OPENAI_API_KEY`
1. Use `chat.completions.create` or the Responses API (`client.responses.create`) — set the `model` and system prompt explicitly
1. Use `zodResponseFormat` from `openai/helpers/zod` with `client.responses.parse`/`chat.completions.parse` for structured output
1. Stream with `stream: true` + iterate chunks — handle tool calls when using function calling

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib openai)

## Rules

- Never call OpenAI from the client — always proxy through the server
- Set timeout + retry + rate-limit handling (429 backoff)
- `openai@7.x` requires Node.js 22+ — check the runtime before upgrading
- Validate structured output with a zod schema
- Log token usage for cost control

- Use `/follow-lib-zod` if writing complex structured output schemas
- Use `/follow-secret-manager` if API keys management is needed
- Use `/run-verify` if needed
- Use `/run-test` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib openai)
- No known security/performance pitfalls (lib openai)
- Lint, typecheck, tests pass
