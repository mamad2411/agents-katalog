---
name: vue-ai-apps
description: "Building AI/LLM and agent apps with Vue 3 and Nuxt: streaming chat UIs, the Vercel AI SDK (`ai` + `@ai-sdk/vue`), `useChat`, tool calling, structured output, and abort/error handling. Load for AI chatbots, assistant UIs, LLM streaming, or agent frontends in Vue or Nuxt."
version: "1.1.1"
license: MIT
author: github.com/PyModel
---

# Vue AI Apps Workflow

Building the **Vue/Nuxt front end** for LLM and agent features with the Vercel AI SDK. This skill covers the Vue-specific integration; the model layer (`streamText`, `tool`, providers) is shown as shape only — follow the AI SDK docs for the current core API, which moves between minor versions.

Assumes the foundations in `vue-best-practices` (Composition API, `<script setup lang="ts">`, composables). Load that skill for component structure and reactivity.

## Core Principles

- **Keys never reach the client.** The provider API key lives on the server. The browser talks to *your* endpoint, never to the model provider directly.
- **Server streams, client consumes.** A server route runs `streamText`/`streamObject` and returns a stream; the Vue component renders it incrementally. Never block on the full response.
- **Render message *parts*, not a content string.** AI SDK messages are `UIMessage[]` made of typed `parts` (text, tool calls, reasoning). Iterate `message.parts`.
- **Drive UI from `status`, not a boolean.** Disabled inputs, spinners, and the stop button key off the `status` state machine.

## 1) Confirm the stack (required)

- Packages: `ai` (core), `@ai-sdk/vue` (composables), a provider (`@ai-sdk/openai`, `@ai-sdk/anthropic`, …), `zod` for tool/object schemas.
- `useChat` from `@ai-sdk/vue` works against **any** streaming backend. The server snippets here use **Nuxt/Nitro** (`defineEventHandler`, `readBody`); for a non-Nuxt backend, keep the same AI SDK calls in your own route handler.
- This skill targets the **v5+ API**, verified against `ai@7` / `@ai-sdk/vue@4`: messages have `parts`; the hook does not manage input; `status` is `'submitted' | 'streaming' | 'ready' | 'error'`; tool schemas use `inputSchema`; `useObject` is exported as `experimental_useObject`. The pre-v5 API (`ai@4`: `message.content`, hook-managed `input`, `isLoading`, `parameters`) differs — check the installed version first.

## 2) Build the streaming chat UI (required for chat features)

- Reference: [streaming-chat-ui](references/streaming-chat-ui.md)
- Server route streams with `streamText` + `toUIMessageStreamResponse()`.
- Client: `useChat()` returns Vue refs. Own your own `input` ref; call `sendMessage({ text })`. Render `message.parts`.

## 3) Add capabilities only when the feature needs them

- **Tool calling** (agent actions, function calling) → [tool-calling](references/tool-calling.md)
- **Structured output** (stream a typed object, not chat) → [structured-output](references/structured-output.md)

## 4) Handle abort and errors (required before shipping)

- Reference: [error-handling-and-abort](references/error-handling-and-abort.md)
- Wire `stop()`, the `error` ref, and `onError`. A streaming UI without an abort path is not done.

## 5) Final self-check

- Provider key is server-only; no key or provider call in client code.
- Component renders `message.parts`, not `message.content`.
- Input is disabled and a stop button shows while `status` is `submitted`/`streaming`.
- Errors are surfaced to the user and retryable (`clearError()` + `regenerate()`).
- Tool/object schemas validate input with `zod`.
- Core AI SDK calls were checked against the installed SDK version, not assumed.
