---
name: streaming
description: Stream for perceived latency, but buffer tool-call JSON until the block closes and don't gate safety on partial output.
---

# Streaming responses

Streaming tokens to the client improves *perceived* latency — the user sees output start almost immediately instead of waiting for the full generation. That UX win comes with two failure modes worth designing around: partial structured output, and moderation timing.

## Tool-call / structured JSON: accumulate, then parse

When a model streams a tool call (or any JSON output), the partial fragments are **not valid JSON mid-stream**. Each delta carries a slice of the serialized arguments; an individual chunk can split a string, a key, or a number anywhere.

- **Accumulate the `partial_json` fragments into a buffer and parse only once the content block closes** (`content_block_stop`). Never `JSON.parse` a single delta.
- Handle truncation explicitly: if the stream stops because the token limit was hit (`stop_reason: "max_tokens"`), the accumulated JSON may be **incomplete and unparseable**. Detect that case and treat the tool call as failed/retryable rather than feeding a half-object downstream.
- Don't render or act on tool arguments until the block is complete — a partially-streamed argument is not a smaller-but-valid argument, it's a syntactically broken string.
- `JSON.parse` on a `partial_json` / streamed-delta field is always a bug, not a judgment call — best enforced mechanically with a lint rule or CI grep so it can't be reintroduced; this rule explains why.

## Moderation: scores arrive after the output, not during it

Streaming means tokens reach the user *before* the full response exists, so any check that needs the complete output — a moderation/safety pass, a full-output classifier, a schema validation of the whole result — **cannot run before the first tokens are already shown.**

- Do not rely solely on streamed deltas for safety gating. If content must be moderated before the user sees it, either don't stream that surface, or stream into a buffer you reveal only after the post-generation check passes.
- Budget for the fact that full-output moderation scores are a *post*-generation signal; design the UX (e.g. redaction-after, stop-and-retract) accordingly.

## Examples

```ts
// BAD — parsing JSON from a single delta; crashes mid-stream
for await (const chunk of stream) {
  if (chunk.type === 'content_block_delta') {
    const args = JSON.parse(chunk.delta.partial_json)  // SyntaxError mid-stream
    callTool(args)
  }
}

// GOOD — accumulate fragments, parse only on block_stop
let buffer = ''
for await (const chunk of stream) {
  if (chunk.type === 'content_block_delta' && chunk.delta.type === 'input_json_delta') {
    buffer += chunk.delta.partial_json
  }
  if (chunk.type === 'content_block_stop') {
    if (stream.finalMessage().stop_reason === 'max_tokens') {
      handleTruncated()  // buffer is incomplete — don't parse
    } else {
      const args = JSON.parse(buffer)
      callTool(args)
    }
    buffer = ''
  }
}
```

## Sources

Anthropic, "Fine-grained tool streaming" — <https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming>: streamed tool-input chunks may not be individually valid JSON and must be accumulated; handle `max_tokens` cutoffs. OpenAI, "Streaming responses" — <https://developers.openai.com/api/docs/guides/streaming-responses>: streaming improves perceived latency but complicates moderation because the full output (and its moderation result) is only available after generation completes.
