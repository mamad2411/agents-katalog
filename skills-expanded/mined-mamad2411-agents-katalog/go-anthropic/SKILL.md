---
name: go-anthropic
description: Use when calling Anthropic's Messages API from Go via anthropic-sdk-go — streaming, tool use, prompt caching, retries.
metadata:
  added: 2026-05-19
  last_reviewed: 2026-05-19
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-19"
  related: [claude-api, go-essentials, go-concurrency, go-langchaingo, agent-design]
---

# Go Anthropic SDK

**Iron Law: every call carries a `context.Context` with a deadline. One `anthropic.Client` per process — reuse it. Read `*resp.Usage` on every success and feed it to your cost meter. Validate structured outputs against a schema (the SDK won't enforce it). For the underlying API concepts (caching breakpoints, thinking, tool-use shapes): see [[claude-api]] — this skill is Go-ergonomic only.**

**Versions:** `github.com/anthropics/anthropic-sdk-go` v1+ (Anthropic-maintained, GA). Pin a tagged release in `go.mod`; do NOT track `main`. Go 1.22+. _Param shape uses `param.Field[T]` / `param.Opt[T]` for optionals — that pattern matters for how you set vs unset values._

## Why this SDK (vs raw HTTP, vs [[go-langchaingo]])

| Approach                     | Verdict                                                                                                                                            |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **anthropic-sdk-go**         | full Anthropic feature set — caching, thinking, tool use, batches, files — with typed params/responses. Use for Claude-first workloads.            |
| **langchaingo**              | provider abstraction across OpenAI/Anthropic/Ollama. Use when you need to swap providers; lags this SDK by 1-2 quarters on new Anthropic features. |
| **net/http + encoding/json** | viable for one-shot calls; falls over the moment streaming or caching shape changes.                                                               |

## Client init

```go
import (
    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

var client = anthropic.NewClient(
    // option.WithAPIKey(...) defaults to ANTHROPIC_API_KEY env var
    option.WithMaxRetries(2),                 // SDK retries 429/5xx with jittered backoff
    option.WithRequestTimeout(60*time.Second), // per-request deadline
)
```

**One client per process**, stored in a package var or injected via DI. The SDK keeps an `http.Client` pool — instantiating per-request exhausts local ports. For a custom transport (proxy, mTLS), pass `option.WithHTTPClient(custom)`; defaults are fine otherwise.

## Sync messages

```go
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()

resp, err := client.Messages.New(ctx, anthropic.MessageNewParams{
    Model:     anthropic.ModelClaudeSonnet4_6,    // pin specific version, not "latest"
    MaxTokens: 1024,
    System: []anthropic.TextBlockParam{
        { Text: "You are a careful code reviewer." },
    },
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Review this diff: ...")),
    },
    Temperature: anthropic.Float(0.2),  // param.Opt — use anthropic.Float / anthropic.Int helpers
})
if err != nil {
    var apiErr *anthropic.Error
    if errors.As(err, &apiErr) {
        slog.Error("anthropic api error", "type", apiErr.Type, "status", apiErr.StatusCode, "msg", apiErr.Message)
    }
    return fmt.Errorf("messages.new: %w", err)
}

slog.Info("usage", "in", resp.Usage.InputTokens, "out", resp.Usage.OutputTokens,
    "cache_read", resp.Usage.CacheReadInputTokens, "cache_create", resp.Usage.CacheCreationInputTokens)
```

`resp.Content` is `[]anthropic.ContentBlockUnion` — walk it with `.AsAny()` and a type switch, or use the typed `As*()` helpers. **Always check `resp.StopReason`** — `"tool_use"` means you owe a tool result before the next user turn.

## Streaming + accumulator

```go
ctx, cancel := context.WithTimeout(ctx, 60*time.Second)
defer cancel()

stream := client.Messages.NewStreaming(ctx, anthropic.MessageNewParams{ /* same params */ })
acc := anthropic.Message{}

for stream.Next() {
    event := stream.Current()
    if err := acc.Accumulate(event); err != nil {
        return fmt.Errorf("accumulate: %w", err)
    }

    switch evt := event.AsAny().(type) {
    case anthropic.ContentBlockDeltaEvent:
        if td, ok := evt.Delta.AsAny().(anthropic.TextDelta); ok {
            fmt.Print(td.Text)   // stream to UI / SSE
        }
    case anthropic.MessageStopEvent:
        // terminal — acc now holds the full message
    }
}
if err := stream.Err(); err != nil {
    return fmt.Errorf("stream: %w", err)
}
// acc.Content holds the assembled blocks; acc.Usage has totals
```

`Accumulator.Accumulate` assembles partial blocks into the final `Message`. **Buffer `input_json_delta` chunks via the accumulator — don't `json.Unmarshal` partial JSON yourself.** The accumulator does it on `content_block_stop`.

## Tool use

```go
type SearchArgs struct {
    Query string `json:"query" jsonschema_description:"Full-text query"`
    Limit int    `json:"limit,omitempty" jsonschema:"minimum=1,maximum=50,default=10"`
}

tools := []anthropic.ToolUnionParam{
    {OfTool: &anthropic.ToolParam{
        Name:        "search_issues",
        Description: anthropic.String("Search the issue tracker."),
        InputSchema: anthropic.ToolInputSchemaParam{
            Properties: map[string]any{
                "query": map[string]any{"type":"string","minLength":1,"maxLength":200},
                "limit": map[string]any{"type":"integer","minimum":1,"maximum":50,"default":10},
            },
            Required: []string{"query"},
            // additionalProperties:false is critical — set via raw schema if helper lacks it
        },
    }},
}

resp, _ := client.Messages.New(ctx, anthropic.MessageNewParams{
    Model: anthropic.ModelClaudeSonnet4_6, MaxTokens: 1024,
    Tools: tools,
    ToolChoice: anthropic.ToolChoiceParamOfAuto(),
    Messages: messages,
})

// Loop: collect tool_use blocks, run them, feed tool_results back.
for resp.StopReason == anthropic.StopReasonToolUse {
    var results []anthropic.ContentBlockParamUnion
    for _, block := range resp.Content {
        if tu, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
            var args SearchArgs
            if err := json.Unmarshal(tu.Input, &args); err != nil {
                results = append(results, anthropic.NewToolResultBlock(tu.ID, "bad args: "+err.Error(), true))
                continue
            }
            out, err := runSearch(ctx, args)            // your tool
            isErr := err != nil
            text := out
            if isErr { text = err.Error() }
            results = append(results, anthropic.NewToolResultBlock(tu.ID, text, isErr))
        }
    }
    messages = append(messages, resp.ToParam(), anthropic.NewUserMessage(results...))
    resp, _ = client.Messages.New(ctx, anthropic.MessageNewParams{ /* same shape, updated messages */ })
}
```

**Tool failures go to `tool_result` with `is_error: true`** — the model recovers by trying different args. Never bubble a Go error to the caller for an _expected_ tool failure; only return Go errors for the _Anthropic call_ failing.

## Prompt caching

Cache control is set on individual `TextBlockParam`s:

```go
System: []anthropic.TextBlockParam{
    {Text: "You are a senior engineer."},
    {Text: largeStableDocs,
     CacheControl: anthropic.CacheControlEphemeralParam{Type: "ephemeral", TTL: anthropic.String("5m")}},
},
```

After the call, read `resp.Usage.CacheReadInputTokens` to confirm hits. See [[claude-api]] for breakpoint placement rules.

## Extended thinking

```go
Thinking: anthropic.ThinkingConfigParamOfEnabled(2000),  // budget_tokens
```

The `thinking` blocks come back in `resp.Content` alongside `text` blocks. **Pass `resp.ToParam()` straight back into the next turn** — it preserves the thinking signature; `Message.ToParam()` is the right way to round-trip an assistant turn including thinking blocks.

## Cancellation + cost guardrails

Pair every `MaxTokens` with `context.WithTimeout`. Cap concurrency with a buffered chan (`sem := make(chan struct{}, 8)`) — unlimited goroutines = rate-limit storm. The SDK's retries respect cancellation; `errors.Is(err, context.Canceled)` discriminates user-cancel from API errors.

## Anti-patterns

- One client per request — `http.Client` pool churns, local ports exhaust
- Reading `resp.Content[0].Text` without checking the block type — panics on `tool_use` or `thinking` blocks
- Forgetting to pass `resp.ToParam()` back into the next turn — drops thinking signature, model loses continuity
- `JSON.Unmarshal` on partial `input_json_delta` chunks — invalid JSON; use the accumulator
- `option.WithMaxRetries(10)` with no jitter cap — turns 429 storms into doom loops; default 2 is fine
- Calling `cancel()` only on the happy path — leak; always `defer cancel()`
- Hardcoding `ANTHROPIC_API_KEY` — load from env or a secrets manager ([[secrets-vault]] / [[secrets-kms]])
- Pinning `anthropic.ModelClaudeSonnet4_6` everywhere and never re-evaluating — re-eval against the matrix as Haiku/Opus shift

## Red flags

| Thought                                           | Reality                                                      |
| ------------------------------------------------- | ------------------------------------------------------------ |
| "I'll just `goroutine` per request, no semaphore" | rate-limit storm; cap concurrency                            |
| "Use `resp.Content[0].Text` directly"             | crashes on tool_use / thinking blocks; type-switch the union |
| "Strip thinking blocks before next turn"          | breaks model continuity; use `resp.ToParam()`                |
| "Retry forever on 429"                            | the right answer is backoff + budget — cap retries           |
| "Streaming partial JSON parses fine"              | no — accumulator buffers until `content_block_stop`          |

## Hand-off

For the wire-level concepts (cache breakpoint rules, model matrix, full JSON shapes): [[claude-api]]. For agent-loop architecture above the SDK (tool design, memory tiers, planning, evals): [[agent-design]]. For Go concurrency primitives used here (`context`, semaphores, errgroup): [[go-concurrency]]. For cross-provider abstraction: [[go-langchaingo]].
