---
name: claude-api
description: Build, debug, and optimize code that calls the Claude (Anthropic) API. Use when writing a step or service that calls Claude — covers picking a surface, the Messages API, choosing a model, prompt caching, tool use, streaming, thinking, and batch.
license: Apache-2.0
compatibility: Tines 3B
---

# Calling the Claude API

Use the official Anthropic SDK for the language you are in (`anthropic` for Python, `@anthropic-ai/sdk` for TypeScript), or raw HTTP only when there is no SDK or the request is explicitly a cURL/REST one. Never mix the two, and never swap in an OpenAI-compatible shim. Read the API key from a 3B credential or connector rather than hardcoding it.

## Connector URLs and authentication

For Anthropic and Microsoft Foundry Claude connectors, pass a placeholder API key; the proxy injects the real key. Keep the saved connector URL including `/v1` for connection tests and credential injection. The official SDK appends `/v1`, so remove only that suffix when constructing its client, preserving gateway prefixes such as `/anthropic`:

```typescript
const client = new Anthropic({
  baseURL: process.env.ANTHROPIC_BASE_URL!.trim().replace(/\/v1\/?$/, ""),
  apiKey: "placeholder",
});
```

```python
client = anthropic.Anthropic(
    base_url=os.environ["ANTHROPIC_BASE_URL"].strip().rstrip("/").removesuffix("/v1"),
    api_key="placeholder",
)
```

Use `ANTHROPIC_BASE_URL` unchanged with `@ai-sdk/anthropic`; for raw HTTP, trim its trailing slash and append `/messages`.

## Pick the simplest surface that works

- **Single call** — classification, summarization, extraction, Q&A. One request, one response.
- **Workflow (call + tool use)** — multi-step logic you orchestrate in code. You control the loop; Claude calls the tools you define.
- **Agent** — Claude decides its own trajectory using your tools. Only reach for this when the task is genuinely open-ended, the value justifies the cost, and errors are recoverable.

Everything goes through `POST /v1/messages`. Tool use and structured outputs are features of that one endpoint, not separate APIs.

## Choosing a model

Use the current Claude models — Fable for the hardest knowledge work and coding, Opus for demanding general work, Sonnet for a balance of speed and intelligence, and Haiku for cheap, fast work. Use the exact model ID string (e.g. `claude-fable-5`, `claude-opus-5-5`, `claude-sonnet-5`, `claude-haiku-4-5`) and **do not append a date suffix**. If you need the live context window or capabilities of a model, query the Models API (`client.models.list()` / `client.models.retrieve(id)`) rather than relying on memory. Don’t silently downgrade a model to save cost — that’s the caller’s decision.

## Prompt caching (do this by default)

Caching is a prefix match: any byte change anywhere in the prefix invalidates everything after it. Render order is `tools` → `system` → `messages`. Put stable content first (frozen system prompt, deterministic tool list) and volatile content (timestamps, per-request IDs, the varying question) last, after your final `cache_control` breakpoint. The minimum cacheable prefix varies by model — 512 tokens for Opus 5.5, Opus 5, and Fable 5, 1024 for Sonnet 5, and 4096 for Haiku 4.5 — and differs again on Bedrock, so check the prompt caching docs for the model you picked. Verify it works by checking `usage.cache_read_input_tokens` across repeated requests — if it stays zero, a silent invalidator (a `datetime.now()` in the system prompt, unsorted JSON, a varying tool list) is breaking the prefix.

## Tool use

Define each tool with a clear name, a JSON-schema input, and a concise description. Either use the SDK’s tool runner to handle the call → execute → loop cycle automatically, or write the loop yourself when you need approval gates or custom logging. Append the model’s full `response.content` back onto the message list each turn — not just the text — or you’ll lose tool-call and thinking state.

## Streaming and thinking

Stream any request that may produce long input or output, or a high `max_tokens`, to avoid request timeouts; use the SDK’s `.get_final_message()` / `.finalMessage()` helper when you only need the final result. For complex work, enable adaptive thinking (`thinking: {type: "adaptive"}`) and tune depth with `output_config: {effort: "low"|"medium"|"high"|"xhigh"|"max"}` where the selected model supports it.

## Batch and files

For large, latency-tolerant jobs use the Batches endpoint (`POST /v1/messages/batches`). Upload large or reused inputs with the Files API instead of inlining them on every request.

---

_Adapted by 3B from Anthropic’s “claude-api” skill (github.com/anthropics/skills), © Anthropic PBC, licensed under Apache-2.0. Modified for 3B; verify model IDs and parameters against the current Anthropic docs._
