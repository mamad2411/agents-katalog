# anthropic-sdk-go

Claude SDK for Go — official Go client for the Anthropic API.

**Source**: `github.com/anthropics/anthropic-sdk-go` (imported as `anthropic`)
**Docs**: https://platform.claude.com/docs/en/api/sdks/go
**Go Reference**: https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go
**Requires**: Go 1.24+

---

## Installation

```sh
go get -u 'github.com/anthropics/anthropic-sdk-go@v1.74.0'
```

```go
import (
    "github.com/anthropics/anthropic-sdk-go"       // as anthropic
    "github.com/anthropics/anthropic-sdk-go/option"
)
```

---

## Client

```go
client := anthropic.NewClient(
    option.WithAPIKey("my-anthropic-api-key"), // defaults to ANTHROPIC_API_KEY
)
```

**Key naming differences from Python/TypeScript SDKs:**
- `.New()` instead of `.create()`
- `.Get()` instead of `.retrieve()`
- Params are Go structs, not method chains

---

## Messages

```go
message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaudeOpus4_6,
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Hello")),
    },
})
// message.Content[0].AsAny() → TextBlock, ToolUseBlock, etc.
```

### Streaming

```go
stream := client.Messages.NewStreaming(ctx, anthropic.MessageNewParams{...})
for stream.Next() {
    event := stream.Current()
    // event.AsAny() → RawMessageStartEvent, RawContentBlockDeltaEvent, etc.
}
if err := stream.Err(); err != nil { ... }
```

### Count Tokens

```go
count, err := client.Messages.CountTokens(ctx, anthropic.MessageCountTokensParams{...})
// count.InputTokens
```

### Message Batches

```go
batch, err := client.Messages.Batches.New(ctx, anthropic.MessageBatchNewParams{
    Requests: []anthropic.MessageBatchRequestParam{...},
})
batch, err  = client.Messages.Batches.Get(ctx, batchID, anthropic.MessageBatchGetParams{})
page, err  := client.Messages.Batches.List(ctx, anthropic.MessageBatchListParams{})
deleted, err := client.Messages.Batches.Delete(ctx, batchID, anthropic.MessageBatchDeleteParams{})
_, err       = client.Messages.Batches.Cancel(ctx, batchID, anthropic.MessageBatchCancelParams{})
stream       := client.Messages.Batches.Results(ctx, batchID, anthropic.MessageBatchResultsParams{})
// stream.Next() → stream.Current() of type MessageBatchResult
```

---

## Models

```go
model, err := client.Models.Get(ctx, "claude-opus-4-6", anthropic.ModelGetParams{})
// model is *anthropic.ModelInfo

page, err := client.Models.List(ctx, anthropic.ModelListParams{})
// page is *pagination.Page[anthropic.ModelInfo]
for _, m := range page.Data { fmt.Println(m.ID) }
```

**ModelInfo fields**: `ID`, `DisplayName`, `CreatedAt`, `Type`, `Capabilities`

---

## Files

```go
// Upload
metadata, err := client.Files.Upload(ctx, anthropic.FileUploadParams{
    File: anthropic.F(fileReader),
})

// List
page, err := client.Files.List(ctx, anthropic.FileListParams{})
// page is *pagination.PageCursor[anthropic.FileMetadata]

// Get metadata
meta, err := client.Files.GetMetadata(ctx, fileID, anthropic.FileGetMetadataParams{})

// Download
resp, err := client.Files.Download(ctx, fileID, anthropic.FileDownloadParams{})
// resp is *http.Response — read resp.Body

// Delete
deleted, err := client.Files.Delete(ctx, fileID, anthropic.FileDeleteParams{})
```

---

## Skills (API)

```go
skill, err  := client.Skills.New(ctx, anthropic.SkillNewParams{...})
skill, err   = client.Skills.Get(ctx, skillID, anthropic.SkillGetParams{})
page, err   := client.Skills.List(ctx, anthropic.SkillListParams{})
deleted, err := client.Skills.Delete(ctx, skillID, anthropic.SkillDeleteParams{})

// Versions
ver, err    := client.Skills.Versions.New(ctx, skillID, anthropic.SkillVersionNewParams{...})
ver, err     = client.Skills.Versions.Get(ctx, version, anthropic.SkillVersionGetParams{})
page, err   := client.Skills.Versions.List(ctx, skillID, anthropic.SkillVersionListParams{})
deleted, err := client.Skills.Versions.Delete(ctx, version, anthropic.SkillVersionDeleteParams{})
```

---

## Beta Messages

All Beta endpoints are under `client.Beta.Messages`:

```go
msg, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
    Model:     anthropic.ModelClaudeSonnet4_5_20250929,
    MaxTokens: 1024,
    Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaComputerUse2024_10_22},
    Messages:  []anthropic.BetaMessageParam{
        anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
    },
})

stream := client.Beta.Messages.NewStreaming(ctx, anthropic.BetaMessageNewParams{...})

count, err := client.Beta.Messages.CountTokens(ctx, anthropic.BetaMessageCountTokensParams{...})
```

### Beta Models

```go
model, err := client.Beta.Models.Get(ctx, modelID, anthropic.BetaModelGetParams{})
page, err  := client.Beta.Models.List(ctx, anthropic.BetaModelListParams{})
// returns *anthropic.BetaModelInfo with .Capabilities.Compaction, .Capabilities.Thinking, etc.
```

---

## Tool Helpers (`toolrunner` package)

```go
import "github.com/anthropics/anthropic-sdk-go/packages/toolrunner"
```

### Defining Tools

**Recommended — auto-generate schema from struct:**
```go
type GetWeatherInput struct {
    City  string `json:"city"  jsonschema:"required,description=The city name"`
    Units string `json:"units,omitempty" jsonschema:"enum=celsius,enum=fahrenheit"`
}

weatherTool, err := toolrunner.NewBetaToolFromJSONSchema(
    "get_weather", "Get current weather for a city",
    func(ctx context.Context, input GetWeatherInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
        return anthropic.BetaToolResultBlockParamContentUnion{
            OfText: &anthropic.BetaTextBlockParam{Text: "72°F, sunny"},
        }, nil
    },
)
```

**From JSON bytes:**
```go
weatherTool, err := toolrunner.NewBetaToolFromBytes(
    "get_weather", "Get current weather for a city",
    []byte(`{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}`),
    func(ctx context.Context, input GetWeatherInput) (anthropic.BetaToolResultBlockParamContentUnion, error) {
        ...
    },
)
```

**From explicit schema:**
```go
weatherTool := toolrunner.NewBetaTool(
    "get_weather", "Get current weather for a city",
    anthropic.BetaToolInputSchemaParam{
        Properties: map[string]any{"city": map[string]any{"type": "string"}},
    },
    handler,
)
```

**Raw JSON input:**
```go
rawTool, err := toolrunner.NewBetaToolFromBytes("name", "desc", schemaBytes,
    func(ctx context.Context, input json.RawMessage) (anthropic.BetaToolResultBlockParamContentUnion, error) {
        var data map[string]any
        json.Unmarshal(input, &data)
        ...
    },
)
```

---

## Tool Runner

```go
runner := client.Beta.Messages.NewToolRunner(
    []anthropic.BetaTool{weatherTool},
    anthropic.BetaToolRunnerParams{
        BetaMessageNewParams: anthropic.BetaMessageNewParams{
            Model:     anthropic.ModelClaudeSonnet4_5_20250929,
            MaxTokens: 1024,
            Messages: []anthropic.BetaMessageParam{
                anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("What's the weather in Tokyo?")),
            },
        },
        MaxIterations: 10, // 0 = no limit
    },
)

// Run to completion
message, err := runner.RunToCompletion(context.Background())

// Iterate over all messages
for message, err := range runner.All(ctx) {
    if err != nil { log.Fatal(err) }
    for _, block := range message.Content {
        switch b := block.AsAny().(type) {
        case anthropic.BetaTextBlock:
            fmt.Println("[assistant]:", b.Text)
        case anthropic.BetaToolUseBlock:
            fmt.Printf("[tool call]: %s(%v)\n", b.Name, b.Input)
        }
    }
}

// Step-by-step
for {
    message, err := runner.NextMessage(ctx)
    if err != nil { log.Fatal(err) }
    if message == nil { break }
    // process message...
}
```

### Modifying Runner State

```go
runner.Params.MaxTokens = 2048
runner.Params.MaxIterations = 10
runner.Params.System = []anthropic.BetaTextBlockParam{{Text: "You are helpful."}}
runner.Params.Messages = append(runner.Params.Messages, anthropic.NewBetaUserMessage(...))
runner.AppendMessages(anthropic.NewBetaUserMessage(...)) // convenience method
```

### Inspecting State

```go
lastMsg   := runner.LastMessage()
messages  := runner.Messages()      // copy of conversation history
count     := runner.IterationCount()
completed := runner.IsCompleted()
```

---

## Streaming Tool Runner

```go
runner := client.Beta.Messages.NewToolRunnerStreaming(tools, anthropic.BetaToolRunnerParams{...})

// Iterate all streaming events across all turns
for eventsIterator := range runner.AllStreaming(ctx) {
    for event, err := range eventsIterator {
        if err != nil { log.Fatal(err) }
        switch e := event.AsAny().(type) {
        case anthropic.BetaRawContentBlockDeltaEvent:
            switch delta := e.Delta.AsAny().(type) {
            case anthropic.BetaTextDelta:
                fmt.Print(delta.Text)
            }
        }
    }
}

// Step-by-step streaming
for !runner.IsCompleted() {
    for event, err := range runner.NextStreaming(ctx) {
        // handle events...
    }
}
// After turn: runner.LastMessage()
```

---

## Context Compaction

Requires `compact-2026-09-04` beta:

```go
runner := client.Beta.Messages.NewToolRunner(tools, anthropic.BetaToolRunnerParams{
    BetaMessageNewParams: anthropic.BetaMessageNewParams{
        Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCompact2026_09_04},
        ...
    },
})

for message, err := range runner.All(ctx) {
    if message.Usage.InputTokens > 100_000 {
        runner.CompactBeforeNextTurn(anthropic.BetaCompactionConfigUnionParam{})
    }
}

// Custom summarization instructions
runner.CompactBeforeNextTurn(anthropic.BetaCompactionConfigUnionParam{
    OfSummarize: &anthropic.BetaSummarizeCompactionParam{
        Instructions: anthropic.String("Keep the page URLs found so far."),
    },
})
```

**Notes on compaction:**
- `StopReason == "compaction"` on the compaction response; summary is in first content block
- `Usage.InputTokens` on compaction response = size of history just summarized
- Does not count against `MaxIterations`
- Calling again before it fires replaces the pending compaction
- With streaming runner, read `runner.LastMessage()` after events consumed

---

## Managed Agents / Sessions

```go
// Sessions-side tool runner
runner, err := client.Beta.Sessions.Events.NewToolRunner(
    ctx,
    sessionID,
    anthropic.SessionToolRunnerOptions{
        Tools: []anthropic.BetaTool{...},
        MaxIdle: 30 * time.Second,
    },
)
// Dispatches agent.tool_use → user.tool_result
// Dispatches agent.custom_tool_use → user.custom_tool_result
// Stops when session idle past MaxIdle
```

---

## Self-Hosted Environment Worker

```go
import "github.com/anthropics/anthropic-sdk-go/lib/environments"

worker := environments.NewEnvironmentWorker(client, environments.EnvironmentWorkerOptions{
    EnvironmentID:  "env_...",
    EnvironmentKey: "key_...",
    Tools: []anthropic.BetaTool{...},
})

// Full poll loop
if err := worker.Run(ctx); err != nil { log.Fatal(err) }

// Handle single claimed work item (inside ant worker poll --on-work hook)
if err := worker.HandleItem(ctx, environments.HandleItemOptions{}); err != nil { log.Fatal(err) }

// With explicit IDs (from WorkPoller)
worker.HandleItem(ctx, environments.HandleItemOptions{
    WorkID:        work.ID,
    EnvironmentID: work.EnvironmentID,
    SessionID:     work.Data.ID,
    EnvironmentKey: environmentKey,
})
```

### Agent Toolset

```go
import "github.com/anthropics/anthropic-sdk-go/tools/agenttoolset"

tools := agenttoolset.BetaAgentToolset20260401(env) // []anthropic.BetaTool
// Includes: bash, read, write, edit, glob, grep
// File tools confine to workdir (symlink-aware); bash is unrestricted
```

**Env vars read by HandleItem:**
- `ANTHROPIC_WORK_ID`
- `ANTHROPIC_ENVIRONMENT_ID`
- `ANTHROPIC_SESSION_ID`
- `ANTHROPIC_ENVIRONMENT_KEY`
- `ANTHROPIC_WORK_LAST_HEARTBEAT`

---

## Built-in Tool Types (Beta)

| Type | Param struct |
|------|-------------|
| Bash 20241022 | `BetaToolBash20241022Param` |
| Bash 20250124 | `BetaToolBash20250124Param` |
| Text editor 20241022 | `BetaToolTextEditor20241022Param` |
| Text editor 20250124 | `BetaToolTextEditor20250124Param` |
| Text editor 20250429 | `BetaToolTextEditor20250429Param` |
| Text editor 20250728 | `BetaToolTextEditor20250728Param` |
| Computer use 20241022 | `BetaToolComputerUse20241022Param` |
| Computer use 20250124 | `BetaToolComputerUse20250124Param` |
| Computer use 20251124 | `BetaToolComputerUse20251124Param` |
| Code execution 20250522 | `BetaCodeExecutionTool20250522Param` |
| Code execution 20250825 | `BetaCodeExecutionTool20250825Param` |
| Code execution 20260120 | `BetaCodeExecutionTool20260120Param` |
| Code execution 20260521 | `BetaCodeExecutionTool20260521Param` |
| Web search 20250305 | `BetaWebSearchTool20250305Param` |
| Web search 20260209 | `BetaWebSearchTool20260209Param` |
| Web search 20260318 | `BetaWebSearchTool20260318Param` |
| Web fetch 20250910 | `BetaWebFetchTool20250910Param` |
| Memory 20250818 | `BetaMemoryTool20250818Param` |
| Browser toolset 20260801 | `BetaBrowserToolset20260801Param` |
| Computer toolset 20260801 | `BetaComputerToolset20260801Param` |
| Advisor 20260301 | `BetaAdvisorTool20260301Param` |
| MCP toolset | `BetaMCPToolsetParam` |

---

## Thinking / Extended Thinking

```go
anthropic.BetaThinkingConfigParamUnion{
    OfEnabled: &anthropic.BetaThinkingConfigEnabledParam{
        BudgetTokens: 10000,
    },
}
// or OfAdaptive / OfDisabled
```

Response content block: `BetaThinkingBlock` (`.Thinking` field), `BetaRedactedThinkingBlock`

---

## Prompt Caching

Add `CacheControl` to message content blocks:
```go
anthropic.BetaTextBlockParam{
    Text: "Long system prompt...",
    CacheControl: anthropic.BetaCacheControlEphemeralParam{Type: "ephemeral"},
}
```

Response includes `BetaCacheCreation` in usage: `CacheCreationInputTokens`, `CacheReadInputTokens`

---

## Citations

```go
params.Betas = append(params.Betas, anthropic.AnthropicBetaCitations20250219)
// or include BetaCitationsConfigParam in request
// Response content blocks may include BetaCitationCharLocation, BetaCitationPageLocation, etc.
```

---

## MCP Tool Runner

```go
// Use MCP tools directly in Beta.Messages requests
params.MCPServers = []anthropic.BetaRequestMCPServerURLDefinitionParam{
    {URL: "https://my-mcp-server.example.com", Name: "my_server"},
}
// Response may include BetaMCPToolUseBlock, BetaMCPToolResultBlock
```

---

## Context Management

```go
params.ContextManagement = &anthropic.BetaContextManagementConfigParam{...}
// Triggers automatic compact edits (compact_20260112)
// Returns BetaContextManagementResponse in usage
```

---

## Pagination

Both `Page[T]` (cursor-free) and `PageCursor[T]` (cursor-based) are used:

```go
page, err := client.Models.List(ctx, anthropic.ModelListParams{})
for _, item := range page.Data { ... }
if page.HasNextPage() {
    nextPage, err := page.GetNextPage()
}

// Auto-paginate with iter
iter := client.Models.ListAutoPaging(ctx, anthropic.ModelListParams{})
for iter.Next() {
    model := iter.Current()
    ...
}
if err := iter.Err(); err != nil { ... }
```

---

## Helper Functions

```go
// Build message params
anthropic.NewUserMessage(anthropic.NewTextBlock("text"))
anthropic.NewAssistantMessage(anthropic.NewTextBlock("text"))

// Beta variants
anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("text"))
anthropic.NewBetaAssistantMessage(anthropic.NewBetaTextBlock("text"))

// Pointer helpers
anthropic.String("value")   // *string
anthropic.Int(42)            // *int64
anthropic.Float(3.14)        // *float64
anthropic.Bool(true)         // *bool
```

---

## Model Constants

```go
anthropic.ModelClaudeOpus4_6
anthropic.ModelClaudeSonnet4_5_20250929
anthropic.ModelClaudeHaiku4_5_20251001
// ... all current models available as typed constants
```

---

## Error Handling

```go
msg, err := client.Messages.New(ctx, params)
if err != nil {
    var apiErr *anthropic.Error
    if errors.As(err, &apiErr) {
        fmt.Println(apiErr.StatusCode)
        fmt.Println(apiErr.Message)
    }
    return err
}
```

Tool handler errors are automatically sent back to Claude as `is_error: true` tool results.

---

## Examples Index

All in `examples/` directory of the cloned repo at `/home/user/anthropics/anthropic-sdk-go/examples/`:

| Directory | What it shows |
|-----------|--------------|
| `message/` | Basic message creation |
| `message-streaming/` | Streaming responses |
| `tools/` | Manual tool use loop |
| `tool-runner/` | BetaToolRunner basic usage |
| `tool-runner-streaming/` | BetaToolRunnerStreaming |
| `tools-streaming/` | Streaming with tool calls |
| `tools-streaming-jsonschema/` | Auto-schema from struct |
| `structured-outputs/` | JSON output format |
| `structured-outputs-streaming/` | Streaming structured outputs |
| `structured-outputs-raw/` | Raw JSON structured outputs |
| `message-output-config/` | Output configuration |
| `multimodal/` | Images and documents |
| `file-upload/` | Files API upload/use |
| `agents/` | Simple agentic loop |
| `agents-comprehensive/` | Full agent implementation |
| `agents-with-files/` | Agents using Files API |
| `managed-agents-self-hosted-sandbox-worker/` | EnvironmentWorker full example |
| `managed-agents-worker-dispatch/` | WorkPoller + HandleItem |
| `managed-agents-observe-tool-calls/` | Observing agent tool calls |
| `managed-agents-streaming-deltas/` | Streaming deltas from sessions |
| `mcp-tool-runner/` | MCP tools in tool runner |
| `message-mcp-streaming/` | MCP streaming |
| `bedrock/` | AWS Bedrock integration |
| `bedrock-streaming/` | Bedrock streaming |
| `bedrock-bearer-token/` | Bedrock with bearer token |
| `vertex/` | Google Vertex AI |
| `vertex-streaming/` | Vertex streaming |
| `googlecloud/` | Google Cloud integration |
| `workload-identity-env/` | Workload identity |
| `foundry/` | Foundry integration |
| `config-file-auth/` | Config file authentication |
| `refusal-fallback/` | Handling refusals |
