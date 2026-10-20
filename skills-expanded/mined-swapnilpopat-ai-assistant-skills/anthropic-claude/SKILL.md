---
name: anthropic-claude
description: Build production integrations with Anthropic Claude (Claude 4.5 Sonnet, Claude Opus 4, Claude Haiku 4) via the Messages API — system prompts, multi-turn conversations, tool use (function calling), prompt caching, extended thinking, vision, batched requests, and streaming. Use when wiring Claude into backends, agentic workflows, or evaluating it against other foundation models. Requires ANTHROPIC_API_KEY.
---

# Anthropic Claude

Integrate Claude models with first-class patterns for tool use, prompt caching, extended thinking, streaming, and safe production operation.

## Stack Baseline (2026)

| Concern | Choice | Notes |
|---|---|---|
| Default model | `claude-sonnet-4-5` | Best balance of cost / capability for most workloads |
| Frontier model | `claude-opus-4` | Long-horizon agents, complex reasoning |
| Cheap/fast | `claude-haiku-4` | Classification, routing, high-throughput |
| Endpoint | `POST /v1/messages` | Stateless; you supply the conversation each call |
| API version header | `anthropic-version: 2023-06-01` | Required on every request |
| SDKs | `@anthropic-ai/sdk` ≥0.40 (Node), `anthropic` ≥0.40 (Python) | First-party; typed |
| Auth | `x-api-key: $ANTHROPIC_API_KEY` | Workspace-scoped key recommended |
| Tool use | `tools: [...]` + `tool_choice` | Multi-turn; client executes & returns `tool_result` |
| Prompt caching | `cache_control: {type: "ephemeral"}` on stable prefix | 5 min TTL; up to 90% input cost reduction |
| Extended thinking | `thinking: {type: "enabled", budget_tokens: 16000}` | Visible reasoning trace; opus/sonnet only |
| Vision | Image blocks (`image/jpeg`, `png`, `gif`, `webp`) up to 5 MB / 8000×8000 | Base64 or URL |
| Streaming | `stream: true` SSE | Lower TTFT for chat UX |
| Batches | `POST /v1/messages/batches` | 50% cost discount, 24 h SLA |
| Rate limits | Per-org RPM/TPM tiers | Honor `retry-after` header |
| Safety | Built-in safety; you must still validate tool inputs and outputs | |

## When to Use

- Adding LLM features (chat, summarization, extraction, classification) to a backend.
- Building an agent loop that calls tools (search, code exec, internal APIs).
- Cost optimization via prompt caching of large system prompts / docs.
- Bulk document/data processing via the Batches API.
- Evaluating Claude head-to-head with OpenAI/Gemini for a specific task.

## Prerequisites

- `ANTHROPIC_API_KEY` exported (workspace-scoped, never in client bundles).
- Decision on which model tier (Haiku / Sonnet / Opus) and whether streaming is needed.
- Tool schemas defined as JSON Schema if using tool use.
- Logging + redaction strategy for prompts/responses (PII handling).
- Token budget and per-request cost ceiling agreed.

## Instructions

1. **Basic Messages call** (stateless; you pass full history each time):
   ```python
   from anthropic import Anthropic
   client = Anthropic()  # reads ANTHROPIC_API_KEY

   resp = client.messages.create(
       model="claude-sonnet-4-5",
       max_tokens=1024,
       system="You are a precise technical writer. Cite sources inline.",
       messages=[
           {"role": "user", "content": "Summarize the SLSA v1.0 provenance spec in 5 bullets."},
       ],
   )
   print(resp.content[0].text)
   print(resp.usage)  # input_tokens, output_tokens, cache_*_tokens
   ```
2. **Streaming** for chat UX (lowest TTFT):
   ```python
   with client.messages.stream(
       model="claude-sonnet-4-5",
       max_tokens=2048,
       messages=[{"role": "user", "content": "Explain mTLS in one paragraph."}],
   ) as stream:
       for text in stream.text_stream:
           print(text, end="", flush=True)
       final = stream.get_final_message()
   ```
3. **Tool use** (function calling) — model proposes a tool call; you execute and return `tool_result`:
   ```python
   tools = [{
       "name": "get_weather",
       "description": "Current weather for a city.",
       "input_schema": {
           "type": "object",
           "properties": {"city": {"type": "string"}, "unit": {"type": "string", "enum": ["c", "f"]}},
           "required": ["city"],
       },
   }]

   messages = [{"role": "user", "content": "What's the weather in Berlin in C?"}]
   while True:
       resp = client.messages.create(
           model="claude-sonnet-4-5",
           max_tokens=1024,
           tools=tools,
           messages=messages,
       )
       if resp.stop_reason != "tool_use":
           print(next(b.text for b in resp.content if b.type == "text"))
           break
       # Execute every tool_use block the model emitted
       tool_results = []
       for block in resp.content:
           if block.type == "tool_use":
               result = run_tool(block.name, block.input)  # your implementation
               tool_results.append({
                   "type": "tool_result",
                   "tool_use_id": block.id,
                   "content": result,
               })
       messages.append({"role": "assistant", "content": resp.content})
       messages.append({"role": "user", "content": tool_results})
   ```
4. **Prompt caching** for stable, large prefixes (system prompt, docs, tool defs). Mark the *last* block of the cacheable prefix:
   ```python
   resp = client.messages.create(
       model="claude-sonnet-4-5",
       max_tokens=1024,
       system=[
           {"type": "text", "text": LARGE_STYLE_GUIDE,
            "cache_control": {"type": "ephemeral"}},
       ],
       messages=[{"role": "user", "content": user_q}],
   )
   # resp.usage.cache_creation_input_tokens / cache_read_input_tokens
   ```
   Cache hits cost ~10% of normal input tokens; misses cost ~125%. Worth it when prefix is reused >2×.
5. **Extended thinking** for hard reasoning (visible chain-of-thought):
   ```python
   resp = client.messages.create(
       model="claude-opus-4",
       max_tokens=4096,
       thinking={"type": "enabled", "budget_tokens": 16000},
       messages=[{"role": "user", "content": HARD_PROBLEM}],
   )
   for block in resp.content:
       if block.type == "thinking":
           log.debug("reasoning: %s", block.thinking)
       elif block.type == "text":
           print(block.text)
   ```
6. **Vision** — pass images as base64 or URL blocks alongside text:
   ```python
   {"role": "user", "content": [
       {"type": "image", "source": {"type": "url", "url": "https://.../diagram.png"}},
       {"type": "text", "text": "What is this diagram showing?"},
   ]}
   ```
7. **Batches** for non-interactive bulk work (50% cheaper, ≤24 h):
   ```python
   batch = client.messages.batches.create(requests=[
       {"custom_id": f"doc-{i}",
        "params": {"model": "claude-haiku-4", "max_tokens": 512,
                   "messages": [{"role": "user", "content": doc}]}}
       for i, doc in enumerate(docs)
   ])
   # Poll batch.id for status; download results when "ended"
   ```
8. **Robust client wrapper** — retries with backoff, honor `retry-after`, redact PII before logging, cap `max_tokens` and total context. The SDK retries transient 5xx / 429 by default; configure `max_retries` and `timeout` explicitly.
9. **Cost & latency telemetry** — record `usage.input_tokens`, `usage.output_tokens`, `usage.cache_read_input_tokens`, `usage.cache_creation_input_tokens`, model name, and end-to-end latency per call. Alert on cost-per-request anomaly.
10. **Eval before swap** — when changing model or prompt, run a fixed eval set (≥50 cases) measuring task accuracy, cost, and latency p50/p95. Don't ship on vibes.

## Common Pitfalls

| Pitfall | Impact | Fix |
|---|---|---|
| API key in browser/client bundle | Immediate abuse, quota theft | Server-side only; signed proxy for browser apps |
| Sending full history every turn unnecessarily | Quadratic token cost | Summarize / window old turns; cache stable prefix |
| Forgetting to append `assistant` + `tool_result` turn after tool use | Infinite loop or invalid request | Always append both before next `create` |
| `max_tokens` too high "just in case" | Latency + cost; truncation isn't free | Set per-task realistic ceiling |
| Not handling `stop_reason` values | Silent truncation (`max_tokens`) treated as success | Check `stop_reason in {"end_turn","tool_use","max_tokens","stop_sequence"}` |
| Caching tiny prefixes | Cache write cost > savings | Cache only ≥1024-token stable prefixes reused ≥2× |
| Logging raw user prompts | PII / secrets leak in observability stack | Redact before log; sample only |
| Treating extended-thinking output as user-visible | Confusing UX; leaks reasoning | Render only `text` blocks; keep `thinking` server-side |
| Trusting tool inputs from the model | SSRF / SQL injection / arbitrary file access | Validate against `input_schema`; allowlist hosts/paths |
| Ignoring `retry-after` on 429 | Rate-limit ban | Exponential backoff respecting header |
| Mixing model versions in the same eval | Apples-to-oranges results | Pin model string per eval run |

## Output Format

Report to caller:

1. Final model & parameters used (model, max_tokens, temperature, thinking budget, tool list).
2. Token usage breakdown (input, output, cache_read, cache_creation) and estimated cost.
3. Stop reason and (for tool use) the tool-call trace.
4. Latency end-to-end and time-to-first-token if streamed.
5. Any safety/refusal signals and how they were handled.

## Authoritative References

- Messages API: https://docs.anthropic.com/en/api/messages
- Tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- Prompt caching: https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
- Extended thinking: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- Vision: https://docs.anthropic.com/en/docs/build-with-claude/vision
- Streaming: https://docs.anthropic.com/en/api/streaming
- Message Batches: https://docs.anthropic.com/en/docs/build-with-claude/batch-processing
- Rate limits: https://docs.anthropic.com/en/api/rate-limits
- Models overview: https://docs.anthropic.com/en/docs/about-claude/models
