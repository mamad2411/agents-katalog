---
name: streaming-ux-patterns
description: Build LLM streaming UX (SSE/WebSocket) that feels fast, supports cancellation, surfaces tool calls cleanly, and handles partial JSON. Use when wiring an LLM backend to a chat UI, IDE assistant, or any UX where perceived latency matters.
source: self
date_added: 2026-05-01
---

# Streaming UX Patterns

LLM features live or die on perceived latency. Streaming converts a 30 s wait into a 200 ms time-to-first-token. Done wrong, it leaks tokens, breaks on cancellation, and confuses users.

## When to Use

- Chat, code assistants, search answers — anywhere output > 1-2 sentences.
- Output drives downstream UI updates (tool-call rendering, citations, partial JSON).
- Users complain "it feels slow" even when total latency is fine.
- Bills include output for cancelled requests no one read.

## Transport: SSE vs WebSocket vs Fetch

| Transport | Use when |
| --- | --- |
| **SSE (Server-Sent Events)** | Default. One-way streaming, plays well with HTTP infra, easy retry/resume |
| **WebSocket** | Bi-directional realtime needed (voice agents, collaborative editing) |
| **Fetch streaming (ReadableStream)** | Modern browsers; same as SSE but no auto-reconnect — wrap it |
| **Long-poll / chunked HTTP** | Legacy clients only |

Default: SSE. Add WebSocket only when you need client→server streaming during the response (voice, interrupt-while-thinking).

## Server-Side Pattern

```
1. Open the response stream early (set headers, flush)
2. Iterate provider stream tokens
3. For each token: write event, flush, check client-disconnect
4. On client disconnect: cancel provider stream IMMEDIATELY
5. On error: emit a typed error event before closing
6. Always emit a terminal "done" event with final usage
```

Critical: **cancel the upstream LLM call on client disconnect**. Otherwise you pay for tokens nobody reads.

## Event Schema

Don't stream raw text. Stream typed events so the UI can render different things differently.

```
event: token        data: {"text": "Hello"}
event: tool_call    data: {"id": "t1", "name": "search", "args_partial": "{\"q\": \"hel"}
event: tool_result  data: {"id": "t1", "summary": "found 3 results"}
event: citation     data: {"id": "c4", "source": "doc#42"}
event: usage        data: {"input": 1200, "output": 87, "cached_input": 1100}
event: done         data: {"reason": "stop"}
event: error        data: {"code": "rate_limit", "retry_after": 30}
```

Stable event names; clients ignore unknown ones (forward-compatible).

## Cancellation

User-initiated cancellation must:
1. Signal the server (close SSE connection, send WebSocket cancel frame, or `AbortController.abort()`).
2. Server propagates to the LLM provider stream.
3. Server still emits a `done` event with partial usage (so cost is tracked).
4. UI keeps the partial output; doesn't blank it.

Test it. The "stop" button working is one of the biggest trust signals in chat UX.

## Backpressure and Buffering

- Don't buffer the entire response server-side then stream. Pass through.
- Disable proxy/CDN buffering on the streaming route (`X-Accel-Buffering: no` for nginx).
- For very fast token streams, batch into ~50ms frames to avoid event-storm overhead in the browser.
- Watch for slow consumers; cap server-side queue per connection.

## Partial JSON / Structured Output

When the model emits structured output, stream it usefully:

- Use a partial-JSON parser (`partial-json`, `json-stream`, `clarinet`) to extract complete fields as they arrive.
- Order schema fields by user-visibility: stream `answer` before `metadata`.
- Render fields incrementally: title appears, then summary, then citations.
- Validate on `done` against the strict schema; if invalid, surface a recoverable error.

## Tool-Call Rendering

- Show tool calls as they happen, not after. "Searching documentation…" beats a blank screen.
- Stream tool **arguments** as they're built; show them collapsed by default, expandable on click.
- Stream tool **result summaries** (not raw output) — both for UX and for cost (raw outputs blow up history).
- Distinguish read-only vs mutating tools visually; mutations may need confirmation UI.

## Markdown / Code Streaming

- Use a streaming-safe Markdown renderer (e.g., `streaming-markdown`, `marked` with incremental mode).
- Don't reparse the whole buffer per token — incremental parsers exist.
- Code fences: detect language as it streams; apply syntax highlight on the closing fence (or a debounce) — re-highlighting per token jitters.
- Math (`$...$`, `$$...$$`): only render once the closing delimiter arrives.

## Time-to-First-Token (TTFT)

This is the metric users feel.

- Skip pre-stream blocking work (auth/RAG/rerank) where possible — do it concurrently with starting the stream.
- For RAG: kick off retrieval and the LLM call in parallel when the system prompt doesn't depend on retrieval.
- Warm prompt cache (see `prompt-caching-patterns`) — cuts TTFT 30-70%.
- Budget: TTFT < 1 s for chat, < 300 ms for autocomplete; alert on regression.

## Optimistic UI and Idempotency

- Echo the user's message immediately; don't wait for server ack.
- Assign a client-side request ID; resend with same ID on reconnect — server uses it to dedupe.
- On reconnect mid-stream, support a `Last-Event-ID` resume (SSE provides this natively) when the provider supports it; otherwise restart from the last user turn.

## Errors Mid-Stream

- Emit a typed `error` event, not raw text.
- Keep partial output visible; offer "regenerate" rather than wiping the UI.
- Distinguish recoverable (rate limit, transient) from terminal (auth, content policy) so UX can act.
- Don't leak provider error detail to end users; log it server-side.

## Cost and Observability

- Always emit a final `usage` event with input/output/cached tokens so the client can attribute cost.
- Server-side: record `cancelled_at_token` so cancellation savings are measurable.
- Track TTFT, total stream duration, tokens-per-second, cancellation rate.

## Anti-Patterns

- Returning the full response then animating it locally — defeats the point and hides real latency.
- Raw text events with no schema; UI guesses what to render.
- Forgetting to cancel upstream on client disconnect — silent budget leak.
- Buffering through a proxy that flushes only on close.
- Re-rendering a 5k-line code block on every token — pegs the CPU.
- Showing nothing until the first complete sentence — kills perceived speed.
- Hiding tool calls; users think the assistant is stuck.
- Not handling reconnect; lost stream looks like a crash.

## Quick Wins Checklist

- [ ] SSE (or WebSocket if needed) with proxy buffering disabled
- [ ] Typed event schema (token, tool_call, tool_result, usage, done, error)
- [ ] Client disconnect cancels upstream LLM call
- [ ] Partial-JSON parser for structured output
- [ ] Streaming-safe Markdown / code rendering
- [ ] TTFT measured and dashboarded; < 1 s target for chat
- [ ] Stop button tested end-to-end
- [ ] Final `usage` event drives cost telemetry

## References

- HTML Living Standard: Server-Sent Events
- OpenAI, Anthropic, Gemini streaming docs
- `partial-json`, `streaming-markdown`, `eventsource-parser` libraries
- Related skills: `chat-ui-patterns` (planned), `agent-loop-budgeting`, `structured-output-design`, `tool-use-design`, `frontend-performance`
