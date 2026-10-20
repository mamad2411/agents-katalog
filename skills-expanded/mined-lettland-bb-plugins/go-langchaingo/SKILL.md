---
name: go-langchaingo
description: Use when integrating LLMs in Go with langchaingo — chains, agents, providers, embeddings, vector stores, Go-ergonomic patterns.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [go-essentials, go-concurrency, go-pgx, security, observability-essentials]
---

# Go langchaingo

**Iron Law: pin the version in `go.mod` and treat the API as unstable until v1. Every LLM call carries a `context.Context` with a deadline. Every secret loads from env/Vault, never literal. Structured outputs need post-hoc schema validation — the SDK won't enforce it.**

**Versions:** Current `v0.1.x` · No LTS series — _Pre-1.0; expect breaking changes between minor versions. Pin to a tagged release in `go.mod`, don't track `main`. The Python `langchain` is several versions ahead — features (structured output, LangGraph) lag here by 6-12 months._

## Why langchaingo (vs raw SDK calls, openai-go, anthropic-sdk-go)

| Approach                         | Verdict                                                                                                                                                                                           |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **langchaingo**                  | provider abstraction (`llms.Model`), chains, agents, vector stores — swap OpenAI ↔ Anthropic ↔ Ollama without rewriting calls. Trade-off: thinner feature coverage per provider than native SDKs. |
| **openai-go / anthropic-sdk-go** | full provider-native feature set (tool use, prompt caching, computer use). Use when you need bleeding-edge features or vendor lock-in is acceptable.                                              |
| **raw HTTP + stdlib**            | trivial one-shot calls; no abstraction tax. Falls apart past 3 endpoints.                                                                                                                         |

For MCP + multi-provider needs, langchaingo's abstraction earns its weight. For a single-provider hot path with caching, drop to the native SDK.

## Provider setup

```go
import (
    "github.com/tmc/langchaingo/llms"
    "github.com/tmc/langchaingo/llms/openai"
    "github.com/tmc/langchaingo/llms/anthropic"
    "github.com/tmc/langchaingo/llms/ollama"
)

llm, err := openai.New(openai.WithToken(os.Getenv("OPENAI_API_KEY")), openai.WithModel("gpt-4o-mini"))
// or: anthropic.New(anthropic.WithToken(...), anthropic.WithModel("claude-3-5-sonnet-latest"))
// or: ollama.New(ollama.WithModel("llama3.2"))                              // local, no token
```

All providers satisfy `llms.Model`. Inject the interface, not the concrete type — that's the whole point of the abstraction.

| Provider                                      | Notes                                                        |
| --------------------------------------------- | ------------------------------------------------------------ |
| `openai`                                      | most mature; tool calling, function calling, JSON mode       |
| `anthropic`                                   | tool use supported; prompt caching needs native SDK          |
| `ollama`                                      | local models; no auth; useful for offline dev + cost-free CI |
| `cohere`                                      | embeddings + rerank shine here                               |
| `googleai` / `vertex` / `bedrock` / `mistral` | Gemini, AWS-hosted, EU-hosted respectively                   |

## Simple call vs chains

```go
// One-shot
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

answer, err := llms.GenerateFromSinglePrompt(ctx, llm,
    "Summarize this changelog entry in one sentence: ...",
    llms.WithTemperature(0.2),
    llms.WithMaxTokens(200),
)
```

For multi-turn or tool-using flows, use `llm.GenerateContent`:

```go
messages := []llms.MessageContent{
    llms.TextParts(llms.ChatMessageTypeSystem, "You are a terse code reviewer."),
    llms.TextParts(llms.ChatMessageTypeHuman, diff),
}
resp, err := llm.GenerateContent(ctx, messages,
    llms.WithTemperature(0.1),
    llms.WithMaxTokens(800),
)
```

Chains (`chains.LLMChain`, `chains.ConversationChain`, `chains.SequentialChain`) wrap prompts + memory + parsing. Useful for repeatable templates; overkill for one-shot calls.

## Structured outputs (and the post-hoc reality)

langchaingo's `outputparser` produces a JSON schema in the prompt; the model usually complies. **Always validate the parsed output server-side** — the model lies sometimes.

```go
type Review struct {
    Verdict string   `json:"verdict"`   // "approve" | "request_changes" | "comment"
    Reasons []string `json:"reasons"`
}

parser, _ := outputparser.NewDefined(Review{})
prompt := fmt.Sprintf("Review this diff.\n%s\n\n%s", parser.GetFormatInstructions(), diff)
raw, err := llms.GenerateFromSinglePrompt(ctx, llm, prompt, llms.WithJSONMode())
if err != nil { return nil, fmt.Errorf("llm: %w", err) }

var r Review
if err := json.Unmarshal([]byte(raw), &r); err != nil {
    return nil, fmt.Errorf("invalid json from llm: %w (raw=%q)", err, raw)
}
switch r.Verdict {                                       // enum check — schema doesn't enforce at runtime
case "approve", "request_changes", "comment":
default: return nil, fmt.Errorf("unexpected verdict: %q", r.Verdict)
}
```

`llms.WithJSONMode()` (OpenAI) constrains the model to valid JSON. Schema validation is still your job.

## Tools and agents (ReAct-style)

```go
import (
    "github.com/tmc/langchaingo/agents"
    "github.com/tmc/langchaingo/tools"
)

type weatherTool struct{}
func (weatherTool) Name() string        { return "weather" }
func (weatherTool) Description() string { return "Get weather for a city. Input: city name." }
func (weatherTool) Call(ctx context.Context, input string) (string, error) {
    return fetchWeather(ctx, input)
}

agent := agents.NewOneShotAgent(llm, []tools.Tool{weatherTool{}}, agents.WithMaxIterations(5))
exec := agents.NewExecutor(agent)
out, err := chains.Run(ctx, exec, "What's the weather in Riga?")
```

`agents.WithMaxIterations` is a hard cap — without it a confused model loops until the context deadline. Set it to 3-5 for most tasks.

## Embeddings + vector stores

```go
embedder, _ := embeddings.NewEmbedder(openai.New(openai.WithEmbeddingModel("text-embedding-3-small")))
store, _ := pgvector.New(ctx,
    pgvector.WithConnectionURL(os.Getenv("DATABASE_URL")),
    pgvector.WithEmbedder(embedder),
    pgvector.WithCollectionName("docs"),
)
_, _ = store.AddDocuments(ctx, []schema.Document{{PageContent: "..."}})
hits, _ := store.SimilaritySearch(ctx, "query", 5)
```

| Vector store                       | When                                                               |
| ---------------------------------- | ------------------------------------------------------------------ |
| `pgvector`                         | already running Postgres (see `Skill(go-pgx)`); simplest ops story |
| `chromem-go`                       | pure-Go embedded; no infra; great for a local index inside a CLI   |
| `qdrant` / `weaviate` / `pinecone` | dedicated vector DB; only when scale demands it                    |
| `redis`                            | hybrid cache + vector; fits if Redis already in stack              |

## Streaming responses

```go
_, err := llm.GenerateContent(ctx, messages,
    llms.WithStreamingFunc(func(ctx context.Context, chunk []byte) error {
        fmt.Print(string(chunk))                       // or push to a tea.Cmd for TUIs
        return nil
    }),
)
```

The streaming callback runs on the SDK's goroutine — keep it fast or buffer to a channel. For Bubble Tea (`Skill(go-bubbletea-charm)`), push chunks as messages, don't render directly.

## Go-ergonomic patterns

```go
g, gctx := errgroup.WithContext(ctx)                     // parallel calls
results := make([]string, len(prompts))
for i, p := range prompts {
    i, p := i, p
    g.Go(func() error {
        out, err := llms.GenerateFromSinglePrompt(gctx, llm, p)
        if err != nil { return err }
        results[i] = out; return nil
    })
}
if err := g.Wait(); err != nil { return nil, err }
```

Retry transient 429/5xx with `cenkalti/backoff` (context-aware exponential). Plumb `context.Context` to every call — streaming + cancellation is the only way to bound cost on a runaway generation.

## Anti-patterns

- Tracking `main` instead of pinning a tagged release — your build breaks weekly
- Skipping the `context.Context` deadline — a hung model bills you for the full timeout window
- Storing API keys in code or YAML committed to the repo — use env vars, Vault, or KMS
- Trusting model output without schema validation — `outputparser` is a prompt, not a guarantee
- Running agents without `WithMaxIterations` — infinite loops on confusion
- Logging the full prompt + response at INFO — PII, secrets, prompt-injection payloads land in logs; redact or sample
- Embedding documents one-by-one in a tight loop — batch via `AddDocuments([]schema.Document{...})` for 10-100x throughput
- Using the OpenAI provider against an Azure OpenAI endpoint without `openai.WithAPIType(openai.APITypeAzure)` — silent 404s

## Red flags

| Thought                                        | Reality                                                                                                                 |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| "I'll upgrade langchaingo to the latest"       | Read the changelog first; this library moves fast and breaks Go signatures                                              |
| "The model will return valid JSON"             | Sometimes. Validate every field; reject and retry on malformed                                                          |
| "Tool calling works the same across providers" | Schema shape differs; the abstraction smooths most of it but tool descriptions matter per model                         |
| "I'll add observability later"                 | Token cost + latency per call is the only feedback loop on quality; wire `Skill(observability-essentials)` from day one |

## Hand-off

For pgvector storage and Postgres tuning: `Skill(go-pgx)`. For parallel calls with `errgroup` and cancellation: `Skill(go-concurrency)`. For prompt-injection defenses, secret handling, and PII redaction: `Skill(security)`. For tracing LLM calls and token-cost metrics: `Skill(observability-essentials)`. For Go idioms, error wrapping, modules: `Skill(go-essentials)`.
