---
name: follow-lib-tanstack-ai
description: Use TanStack AI end to end — provider adapters, chat streaming, tools, client hooks, MCP
argument-hint: "[framework] [provider]"
related:
  - follow-lib-tanstack-ecosystem
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack AI fully — a provider-agnostic AI SDK: server-side `chat()` + adapters, tool calling, streaming, `useChat` client hooks, agent loops

## Scope

For AI features not bound to a single provider (chat, tools, agents, streaming UI) — **0.x**: the API changes fast, always check `https://tanstack.com/ai/latest` before implementing

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the AI package and the provider adapters you need

```bash
bun add @tanstack/ai @tanstack/ai-client @tanstack/ai-react
bun add @tanstack/ai-openai        # or ai-anthropic / ai-ollama / another adapter
```

### 2. Server Chat Endpoint

> Goal: `chat()` + adapter on the server side only

```ts
import { chat, toStreamResponse, toolDefinition } from '@tanstack/ai'
import { openaiText } from '@tanstack/ai-openai'

const getWeather = toolDefinition({
  name: 'get_weather',
  description: 'Get weather for a city',
  inputSchema: z.object({ city: z.string() }),
}).server(async ({ city }) => fetchWeather(city))   // execute server-side

export const POST = async ({ request }) => {
  const { messages } = await request.json()
  const stream = chat({ adapter: openaiText(), messages, tools: [getWeather] })
  return toStreamResponse(stream)
}
```

1. Place it in a Start server function (`createServerFn` → `follow-start`) or the framework's API route
2. API keys live in server-side env only — never leak them into the client bundle

### 3. Client Chat

> Goal: streaming chat UI

```tsx
import { useChat } from '@tanstack/ai-react'

const { messages, sendMessage, isLoading, stop } = useChat({
  connection: fetchServerSentEvents('/api/chat'),
})
```

- `messages` have `parts` — text, tool-call, tool-result — render per part type
- Approval flows: tools requiring confirmation → client-side approval UI before execute
- Switching providers = changing the adapter import on the server side only — the client is untouched

### 4. Advanced

> Goal: cover real use cases

1. **Tools**: `toolDefinition` — server tools (`.server(fn)`), client tools (interactive UI), approval-required tools
2. **Structured output**: `outputSchema` on chat options → typed JSON response
3. **Agent loop**: tools + maxIterations — the model calls tools repeatedly until done
4. **MCP**: connect MCP servers as tool sources (check the latest API — 0.x changes fast)
5. **Headless**: `@tanstack/ai-client` used outside framework UI — custom chat state management

### 5. Verify

> Goal: prove chat streaming and tool calls work before finishing

1. `/run-typecheck` — message/tool types pass
2. Real streaming: all tokens arrive, `stop()` cancels, the tool round-trip succeeds
3. Test another adapter to confirm provider-agnosticism
4. On failure → `/resolve-errors` max 3 rounds

## Rules

- The adapter + `chat()` always live on the server — the client only sees the connection/stream
- Tool schemas use standard schema — types flow through to the model response
- Tools with side effects → `.server()` execution only
- Message `parts` = source of truth — never parse raw text yourself
- 0.x API — pin the exact version; verify every example against the latest docs

## Expected Outcome

- The chat stream works end-to-end (server adapter → client UI)
- Tools execute + approval flows are correct
- A provider swap doesn't affect client code
