# Blaze.LlmGateway — Audit + JARVIS Roadmap

> **Author:** Claude (sonnet-4.6) — 2026-04-26
> **Source of truth for:** current code reality, prioritized phased plan, agent assignments
> **Working directory:** `C:\src\CodebrewRouter`
> **Status:** Living document. Update as phases complete.

---

## Part 0 — Reframe (read this first)

This codebase started its life with a **PRD that called for a LiteLLM-class .NET gateway** powering SaaS products. That direction is now retired.

**Current product goal:** a personal **JARVIS-style developer agent**. The gateway exists *in service of* the agent. The agent stack is:

> RAG → squad → persistent memory → MCP → tools → agents

We are **not** building:
- Virtual API keys / per-tenant budgets
- Spend dashboards or cost-tracking SaaS
- Multi-tenant admin UI
- 100-provider LiteLLM parity

We **are** building:
- A persistent, context-aware personal assistant ("JARVIS, not kidding")
- Cross-conversation memory (episodic + semantic)
- Retrieval over Allen's own code, docs, notes
- Tool use via MCP (file system, build, git, web search, etc.)
- Multi-step agent loops (think → tool → observe → repeat)
- Squad orchestration for multi-agent coding tasks (already 80% scaffolded)

**Yardly remains a secondary downstream product.** Yardly wants vision + chat. That means the gateway's wire DTO must accept multimodal content parts even though Yardly itself is not the focus. Vision passthrough is a small, contained piece of work and can ride along with the Phase-1 bug-fix.

---

## Part 1 — Current state audit

### 1.1 Providers (the real answer: **2 working, 1 broken, 1 internal**)

| Key | Registered? | Working? | Source |
|---|---|---|---|
| `AzureFoundry` | ✅ | ✅ given endpoint+key | [InfrastructureServiceExtensions.cs:24](Blaze.LlmGateway.Infrastructure/InfrastructureServiceExtensions.cs) |
| `FoundryLocal` | ✅ | 🟡 needs localhost:5273 | line 35 — AppHost container is **commented out** |
| `OllamaLocal` | ✅ | 🟡 needs localhost:11434 | line 46 — used as router-brain only, not a `RouteDestination` |
| `GithubModels` | ❌ **never registered** | ❌ **silently broken** | see §1.6 |
| `CodebrewRouter` | ✅ | 🟡 virtual | line 126 — task-classifying facade |

`RouteDestination` enum has 3 values: `AzureFoundry, FoundryLocal, GithubModels` ([Core/RouteDestination.cs](Blaze.LlmGateway.Core/RouteDestination.cs)).

### 1.2 Endpoints

Wired in [LiteLlmEndpoints.cs / ProgramPartial.cs](Blaze.LlmGateway.Api/ProgramPartial.cs):
- `POST /v1/chat/completions` — SSE + non-streaming
- `POST /v1/completions` — legacy text
- `GET /v1/models` — Azure-discovered + configured
- OpenAPI doc at `/openapi/v1.json`, Scalar UI at `/scalar`
- `/health`, `/alive` via `MapDefaultEndpoints()`

No embeddings, no audio, no images, no rerank, no admin, no auth.

### 1.3 Pipeline (MEAI)

```
unkeyed IChatClient
  = LlmRoutingChatClient (DelegatingChatClient ✓)
      .InnerClient = GithubModels ?? AzureFoundry ?? FoundryLocal  ← first-non-null
      .Strategy    = OllamaMetaRoutingStrategy(OllamaLocal) ?? KeywordRoutingStrategy
      .Failover    = ConfiguredFailoverStrategy
      resolves keyed IChatClient by destination string
        ├── AzureFoundry → AzureOpenAIClient → AsIChatClient → UseFunctionInvocation
        ├── FoundryLocal → AzureOpenAIClient → AsIChatClient → UseFunctionInvocation
        └── OllamaLocal  → OllamaApiClient   → AsIChatClient → UseFunctionInvocation
```

`McpToolDelegatingClient` is implemented and inherits `DelegatingChatClient` correctly, but is **fully commented out** in both [Program.cs:46-57](Blaze.LlmGateway.Api/Program.cs) and [InfrastructureServiceExtensions.cs:98-106](Blaze.LlmGateway.Infrastructure/InfrastructureServiceExtensions.cs). MCP is presently dead.

### 1.4 What's wired correctly (credit where due)

- MEAI middleware pattern — `DelegatingChatClient` everywhere
- Streaming via `GetStreamingResponseAsync` — current API, no legacy `CompleteAsync`
- Keyed DI — keys match `RouteDestination.ToString()`
- `Program.cs` is clean, DI in extension methods
- Aspire AppHost wires GitHub Models resources, optional Open WebUI, Agent Framework DevUI
- Azure Foundry dynamic model discovery via `/openai/v1/models`
- `CodebrewRouterChatClient` has correct streaming first-chunk-probe failover ([CodebrewRouterChatClient.cs:72-139](Blaze.LlmGateway.Infrastructure/CodebrewRouterChatClient.cs))
- xUnit integration tests via `WebApplicationFactory<Program>`
- Squad orchestration scaffolded under [`prompts/squad/`](prompts/squad/) and [`.claude/agents/squad-*`](.claude/agents/)

### 1.5 What's documented but not built

| ADR | Claim | Reality |
|---|---|---|
| [ADR-0001](Docs/design/adr/0001-primary-host-boundary.md) | Gateway + agent runtime co-hosted | No agent runtime exists |
| [ADR-0002](Docs/design/adr/0002-provider-identity-model.md) | Config-driven `ProviderDescriptor` + `ModelProfile` catalog replaces enum | **Not done** — still using enum + static `ProvidersOptions` |
| [ADR-0004](Docs/design/adr/0004-session-state-persistence.md) | SQLite + EF Core `ISessionStore` default | **Not done** — no `DbContext`, no migrations, no `ISessionStore` anywhere |
| [ADR-0006](Docs/design/adr/0006-azure-foundry-agents-integration.md) | `IAgentAdapter` for Foundry hosted + local agents | **Not done** |
| [ADR-0008](Docs/design/adr/0008-cloud-escalation-policy.md) | Default-deny cloud egress with allow-list | Prompt-level guardrail only; no enforcement code |

[`Docs/PRD/blaze-llmgateway-prd.md`](Docs/PRD/blaze-llmgateway-prd.md) still claims 9 providers including Gemini, OpenRouter, GitHub Copilot, OllamaBackup. They were removed in commit `9e39a77`. **Treat the PRD as historical.**

### 1.6 Critical bugs (5 must-fix items)

#### Bug 1: `GithubModels` never registered — silent failover collapse

`CodebrewRouterOptions.FallbackRules` ([CodebrewRouterOptions.cs:22-30](Blaze.LlmGateway.Core/Configuration/CodebrewRouterOptions.cs)) lists `GithubModels` in every rule, and Coding tasks put it **first**. But [`AddLlmProviders`](Blaze.LlmGateway.Infrastructure/InfrastructureServiceExtensions.cs) registers only AzureFoundry/FoundryLocal/OllamaLocal. AppHost calls `builder.AddGitHubModel(...)` and injects `LlmGateway__Providers__GithubModels__ApiKey` env var, but no code reads it. There is no `GithubModelsOptions` class in `ProvidersOptions`.

**Effect:** every CodebrewRouter request logs `⚠️ provider 'GithubModels' not registered — skipping` and silently collapses to AzureFoundry. Tests pass because they mock `AddKeyedSingleton<IChatClient>("GithubModels", mockClient.Object)` in setup.

#### Bug 2: OpenAI wire format wrong

[ChatCompletionsEndpoint.cs:126](Blaze.LlmGateway.Api/ChatCompletionsEndpoint.cs):
```csharp
var chunk = new { id, @object = "text_completion.chunk", ... };
```
Real spec: `"chat.completion.chunk"` for chat streaming, `"chat.completion"` for non-streaming (line 186 wrongly emits `"text_completion"`). Strict OpenAI clients will reject. Also: no role on first delta, no separate finish_reason chunk.

#### Bug 3: Function calling silently dropped

`ChatCompletionRequest.Tools` is parsed ([OpenAiModels.cs:45](Blaze.LlmGateway.Api/OpenAiModels.cs)), but `ChatCompletionsEndpoint.HandleAsync` never reads `req.Tools` and never sets `options.Tools`. MEAI's `FunctionInvokingChatClient` is wired but receives no tools. **This blocks every JARVIS use case.**

#### Bug 4: Vision can't be represented on the wire

`ChatMessageDto.Content` is a scalar `string`. OpenAI vision is `content: [{type:"text",text}, {type:"image_url",image_url:{url}}]`. The deserializer throws on a vision-formatted request. Even if it didn't, the conversion at [line 67](Blaze.LlmGateway.Api/ChatCompletionsEndpoint.cs) flattens to text. MEAI's `ChatMessage.Contents` (`IList<AIContent>` with `TextContent`/`UriContent`/`DataContent`) supports vision natively — the gateway DTO is what blocks it.

#### Bug 5: Streaming failover is dead code

[LlmRoutingChatClient.cs:56-82](Blaze.LlmGateway.Infrastructure/LlmRoutingChatClient.cs) — the streaming path calls `targetClient.GetStreamingResponseAsync` and yields. Any exception bubbles up and kills the stream. `TryFailoverStreamingAsync` (line 135) exists but is **never called**. The non-streaming path correctly calls `TryFailoverAsync`. The `codebrewRouter` virtual model has its own correct streaming-failover (with first-chunk probe), so `model: "codebrewRouter"` is actually fine — but the default `/v1/chat/completions` path is not.

### 1.7 What's missing for JARVIS specifically

| Capability | Status | Why JARVIS needs it |
|---|---|---|
| Persistent session store | ❌ | conversation continuity |
| Semantic memory (vector) | ❌ | "remember this" / "what did I say about X last week" |
| Document ingestion + chunking | ❌ | RAG |
| Embedding client | ❌ | RAG + memory |
| MCP tool execution | ❌ disabled | tools = the agent's hands |
| Function calling forwarding | ❌ Bug #3 | tools again |
| Vision passthrough | ❌ Bug #4 | screen capture, Yardly |
| Agent runtime (`IAgentAdapter`) | ❌ ADR-0006 stub | multi-step reasoning loops |
| Microsoft Agent Framework integration | ❌ research only | the agent loop primitive |
| Persona / system-prompt store | ❌ | "JARVIS personality" |
| Voice I/O | ❌ | stretch — actual JARVIS UX |

---

## Part 2 — Architectural vision

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 5: Interfaces (Blazor chat, voice, Open WebUI, DevUI) │
├──────────────────────────────────────────────────────────────┤
│  Layer 4: JARVIS persona (system prompt + memory + identity) │
├──────────────────────────────────────────────────────────────┤
│  Layer 3: Agent runtime (IAgentAdapter, ReAct loop, Squad)   │
├──────────────────────────────────────────────────────────────┤
│  Layer 2: Tools + RAG (MCP, file ops, web, vector retrieval) │
├──────────────────────────────────────────────────────────────┤
│  Layer 1: Substrate (sessions, memory, embeddings, vectors)  │
├──────────────────────────────────────────────────────────────┤
│  Layer 0: Gateway (MEAI pipeline, providers, /v1, streaming) │
└──────────────────────────────────────────────────────────────┘
```

Each layer reuses the layer below it. The gateway (Layer 0) must be solid before Layer 1 is worth building. Layer 1 is the substrate everything else hangs from. **Don't skip layers.**

---

## Part 3 — Phased roadmap (priority order)

Each phase ends with `dotnet build --no-incremental -warnaserror` clean and tests passing. Each phase is small enough to land in a single session of focused work (1–4 hours).

### **Phase 1 — Stop the bleeding** [agent: `gateway-bugfix`]

**Goal:** the gateway speaks correct OpenAI on the wire, all 3 providers actually work, function calling and vision are representable. Without this, JARVIS cannot exist.

| # | Task | Files |
|---|---|---|
| 1.1 | Add `GithubModelsOptions` to `ProvidersOptions` | `Blaze.LlmGateway.Core/Configuration/LlmGatewayOptions.cs` |
| 1.2 | Register `GithubModels` keyed `IChatClient` (`OpenAIClient` against `https://models.inference.ai.azure.com` w/ PAT) | `Blaze.LlmGateway.Infrastructure/InfrastructureServiceExtensions.cs` |
| 1.3 | Read `LlmGateway__Providers__GithubModels__ApiKey` env var; fail-loud if missing AND key referenced in chains | same |
| 1.4 | Fix `object` strings: `"chat.completion.chunk"` (streaming) and `"chat.completion"` (non-streaming) | `Blaze.LlmGateway.Api/ChatCompletionsEndpoint.cs` |
| 1.5 | Emit `role: "assistant"` on first delta chunk; emit final chunk with `finish_reason: "stop"` and empty delta | same |
| 1.6 | Make `ChatMessageDto.Content` polymorphic — accept `string` OR `IList<ContentPart>` via custom `JsonConverter` | `Blaze.LlmGateway.Api/OpenAiModels.cs` (+ new `ChatMessageDtoConverter.cs`) |
| 1.7 | Convert content parts → `ChatMessage.Contents` (`TextContent`, `UriContent`, `DataContent`) in endpoint conversion | `ChatCompletionsEndpoint.cs` |
| 1.8 | Forward `req.Tools` → `ChatOptions.Tools` (translate to MEAI `AIFunction` declarations) | same |
| 1.9 | Wire `LlmRoutingChatClient.GetStreamingResponseAsync` to call `TryFailoverStreamingAsync` on first-chunk failure (mirror `CodebrewRouterChatClient` probe pattern) | `Blaze.LlmGateway.Infrastructure/LlmRoutingChatClient.cs` |
| 1.10 | Tier-A integration test: real keyed DI (NOT mocked), against gpt-4o-mini, sends a tool definition + image URL, asserts 200 + correct `object` field | `Blaze.LlmGateway.Tests/ChatCompletionsRealRoutingTests.cs` (new) |
| 1.11 | Update [CLAUDE.md](CLAUDE.md) "Known Incomplete Areas" — strike completed items | `CLAUDE.md` |

**Definition of done:**
- Build green w/ `-warnaserror`
- New test passes against a real GitHub Models endpoint (or VCR fixture)
- `curl -X POST /v1/chat/completions` with `{model: "codebrewRouter", messages: [{role:"user", content:[{type:"text"...},{type:"image_url"...}]}]}` returns valid SSE w/ `chat.completion.chunk` objects
- Logs show GithubModels actually being tried for Coding tasks

---

### **Phase 2 — Memory substrate (sessions + structured memory)** [agent: `jarvis-memory-architect`]

**Goal:** JARVIS remembers across conversations. Two memory types:
1. **Session memory** — full message history per `session_id`
2. **Structured memory** — key-value notes JARVIS chose to write to itself ("Allen prefers tabs", "the apartment WiFi password is X", "Yardly lives at /apartments/yardly")

| # | Task | Files |
|---|---|---|
| 2.1 | Pick & document storage: SQLite + EF Core (matches ADR-0004) | `Docs/design/adr/0004-*.md` (update as built, not aspirational) |
| 2.2 | New project `Blaze.LlmGateway.Persistence` | `Blaze.LlmGateway.Persistence/*` (new) |
| 2.3 | `JarvisDbContext` with `Sessions`, `Messages`, `MemoryItems` tables | `Blaze.LlmGateway.Persistence/JarvisDbContext.cs` |
| 2.4 | `ISessionStore` + `EfCoreSessionStore` with `LoadAsync`, `AppendAsync`, `TruncateForContextWindowAsync` | `Blaze.LlmGateway.Persistence/ISessionStore.cs`, `EfCoreSessionStore.cs` |
| 2.5 | `SessionDelegatingChatClient` — middleware that prepends loaded history when request includes `X-Jarvis-Session-Id` header | `Blaze.LlmGateway.Infrastructure/SessionDelegatingChatClient.cs` |
| 2.6 | `IMemoryStore` + `EfCoreMemoryStore` w/ `RememberAsync(key, value, tags)`, `RecallAsync(query)`, `ForgetAsync(key)` | `Blaze.LlmGateway.Persistence/IMemoryStore.cs` |
| 2.7 | Built-in tools `remember`, `recall`, `forget` exposed as MEAI `AIFunction` declarations | `Blaze.LlmGateway.Infrastructure/JarvisTools/MemoryTools.cs` (new folder) |
| 2.8 | Aspire AppHost wires SQLite database resource | `Blaze.LlmGateway.AppHost/Program.cs` |
| 2.9 | Migrations: `dotnet ef migrations add InitialJarvisSchema` | `Blaze.LlmGateway.Persistence/Migrations/*` |
| 2.10 | Tests: round-trip session save/load; memory remember/recall; context-window truncation | `Blaze.LlmGateway.Tests/MemorySubstrateTests.cs` |

**Definition of done:**
- Send a message with `X-Jarvis-Session-Id: foo`, get reply, send another, see prior context honored
- Have JARVIS call `remember("preferred_editor", "Visual Studio")`, in a new conversation ask "what editor do I use", get correct answer

---

### **Phase 3 — MCP + tools (the agent's hands)** [agent: `jarvis-tools-architect`]

**Goal:** un-disable MCP, ship JARVIS with a useful initial tool kit.

| # | Task | Files |
|---|---|---|
| 3.1 | Re-enable `McpConnectionManager` + `McpToolDelegatingClient` registration | `Blaze.LlmGateway.Api/Program.cs`, `Blaze.LlmGateway.Infrastructure/InfrastructureServiceExtensions.cs` |
| 3.2 | Replace placeholder `AppendMcpTools` with proper `HostedMcpServerTool` mapping (consult `prompts/squad/skills/` and Microsoft Agent Framework samples) | `Blaze.LlmGateway.Infrastructure/McpToolDelegatingClient.cs` |
| 3.3 | Configure MCP servers in `appsettings.json` under `Mcp:Servers` (microsoft-learn, filesystem, git) | `appsettings.json` |
| 3.4 | Built-in non-MCP tools (`AIFunction` declarations): `read_file`, `write_file`, `list_directory`, `run_shell`, `search_web`, `git_status`, `git_log`, `git_diff` | `Blaze.LlmGateway.Infrastructure/JarvisTools/*.cs` |
| 3.5 | Per-request tool filtering via `X-Jarvis-Tools: a,b,c` header | `ChatCompletionsEndpoint.cs` |
| 3.6 | MCP server health monitoring + reconnect (kill the placeholder `StartAsync`) | `McpConnectionManager.cs` |
| 3.7 | Tests: mock MCP server returning a known tool, assert tool appears in `ChatOptions.Tools`, assert tool result round-trips through `FunctionInvokingChatClient` | `Blaze.LlmGateway.Tests/McpIntegrationTests.cs` |

**Definition of done:**
- Send a chat asking "list files in C:\src\CodebrewRouter\Docs", JARVIS uses `list_directory` tool, returns actual contents
- microsoft-learn MCP returns docs in a real chat

---

### **Phase 4 — RAG (the agent's reference)** [agent: `jarvis-memory-architect` continued]

**Goal:** JARVIS can answer "what does the architecture doc say about routing?" by retrieving from a vector store seeded with this repo + Allen's docs.

| # | Task | Files |
|---|---|---|
| 4.1 | Decide vector store. **Recommendation: SQLite-vec** for v1 (zero infra, single-process, scales to ~1M vectors fine for personal use). Qdrant via Aspire is a Phase 4.5 swap if needed. | `Docs/design/adr/0011-vector-store-choice.md` (new ADR) |
| 4.2 | Add `Microsoft.Extensions.AI` embedding client. Use Azure OpenAI `text-embedding-3-small` (cheap, fast, 1536-dim). | `InfrastructureServiceExtensions.cs` |
| 4.3 | `IDocumentIngestor` — chunks (sentence-aware, ~500 tokens, 50 token overlap), embeds, stores | `Blaze.LlmGateway.Infrastructure/Rag/DocumentIngestor.cs` |
| 4.4 | `IRetriever.SearchAsync(query, k=5)` — embeds query, returns top-k chunks with metadata | `IRetriever.cs`, `SqliteVecRetriever.cs` |
| 4.5 | MCP tool: `search_knowledge(query)` — exposes retrieval to the agent | `Blaze.LlmGateway.Infrastructure/JarvisTools/KnowledgeTools.cs` |
| 4.6 | Initial corpora ingestion script: ingest `Docs/**/*.md`, `prompts/squad/**/*.md`, all `.cs` files in this repo | `scripts/ingest-corpus.ps1` |
| 4.7 | Tests: ingest a fixture markdown set, query, assert relevant chunk in top-5 | `Blaze.LlmGateway.Tests/RagTests.cs` |

**Definition of done:**
- Ask JARVIS "what's our routing strategy", it calls `search_knowledge`, returns a coherent answer cited to `blaze-llmgateway-architecture.md`
- Embedding cost is logged so Allen can see he isn't bleeding $

---

### **Phase 5 — Agent runtime (the brain loop)** [agent: `jarvis-agent-architect`]

**Goal:** real ReAct-style agent loops with multi-step reasoning. Currently every request is a single LLM call. JARVIS needs `think → tool → observe → think → respond`.

| # | Task | Files |
|---|---|---|
| 5.1 | `IAgentAdapter` interface from ADR-0006 — finally implement | `Blaze.LlmGateway.Core/Agents/IAgentAdapter.cs` |
| 5.2 | `LocalAgentAdapter` — wraps a system prompt + tool set + max-iterations into a runnable agent | `Blaze.LlmGateway.Infrastructure/Agents/LocalAgentAdapter.cs` |
| 5.3 | Microsoft Agent Framework integration (consult [`research/https-github-com-microsoft-agent-framework.md`](research/https-github-com-microsoft-agent-framework.md)). Add `Microsoft.Agents.AI` package. | `Blaze.LlmGateway.Infrastructure.csproj` |
| 5.4 | `FoundryAgentAdapter` — wraps an Azure Foundry hosted agent | `Blaze.LlmGateway.Infrastructure/Agents/FoundryAgentAdapter.cs` |
| 5.5 | `IAgentRegistry` — DI-keyed registry of named agents (`developer`, `researcher`, `writer`, `jarvis`) | `Blaze.LlmGateway.Infrastructure/Agents/IAgentRegistry.cs` |
| 5.6 | New endpoint `POST /v1/agents/{name}/invoke` — sync + streaming, emits `AgentEvent`s (think, tool_call, tool_result, final) | `Blaze.LlmGateway.Api/AgentsEndpoint.cs` |
| 5.7 | Aspire DevUI mount via `app.MapDevUI()` from Microsoft Agent Framework — visualizes agent runs | `Program.cs` (gated to Development) |
| 5.8 | Tests: stub agent with one tool, assert think → tool_call → tool_result → final sequence emitted | `Blaze.LlmGateway.Tests/AgentRuntimeTests.cs` |

**Definition of done:**
- `POST /v1/agents/jarvis/invoke` with "summarize the open ADRs and tell me which are stale" runs an actual loop, calling `list_directory` then `read_file` then composing
- Aspire dashboard shows the run trace in DevUI

---

### **Phase 6 — JARVIS persona** [agent: `jarvis-agent-architect` continued]

**Goal:** JARVIS *as a character* — opinionated, persistent, knows Allen.

| # | Task |
|---|---|
| 6.1 | Persona system prompt stored in `MemoryStore` under key `system:jarvis` |
| 6.2 | Bootstrap memory at first run: load `~/.jarvis/profile.yaml` (timezone, name, preferred editor, projects, etc.) into `MemoryStore` |
| 6.3 | Pre-conversation memory injection — every JARVIS request prepends a system message synthesized from relevant memory items + RAG-retrieved context |
| 6.4 | "Wake word" / mode switch: prefix `jarvis:` or `j:` in any chat to invoke the JARVIS agent specifically |
| 6.5 | Memory hygiene tools: `summarize_old_sessions`, `dedupe_memory`, `forget_outdated` — JARVIS runs these on a schedule |

---

### **Phase 7 — Squad orchestration polish** [agent: `jarvis-conductor` + existing Squad]

**Goal:** Allen can say "JARVIS, refactor X using the squad" and the existing 9-agent squad executes the change.

| # | Task |
|---|---|
| 7.1 | Verify `pwsh ./scripts/sync-squad.ps1` is idempotent and current |
| 7.2 | Wire JARVIS itself to invoke the squad via the Conductor when given a coding task |
| 7.3 | Add a `delegate_to_squad` tool to JARVIS's tool set |
| 7.4 | Ensure squad runs are searchable via `search_knowledge` (ingest `Docs/squad/runs/**/reasoning.log.md` into the vector store) |
| 7.5 | Test: ask JARVIS "fix the GithubModels bug using the squad", confirm a squad run appears in `Docs/squad/runs/` |

---

### **Phase 8 — Vision passthrough (Yardly)** [agent: `jarvis-vision-architect`]

**Goal:** Yardly can send images. JARVIS can see screenshots Allen pastes in.

> Most of vision work was actually done in Phase 1.6/1.7 (DTO content parts). This phase polishes:

| # | Task |
|---|---|
| 8.1 | Add `image/png`, `image/jpeg`, `image/webp` MIME validation + max size check |
| 8.2 | Provider capability metadata: tag which keyed clients support vision (gpt-4o ✓, phi-4-mini-instruct ✗) |
| 8.3 | Routing strategy: if request has image content, prefer vision-capable providers |
| 8.4 | `analyze_screenshot` JARVIS tool — agent can call it with a base64 image |
| 8.5 | End-to-end test: POST a real PNG, get a description |

---

### **Phase 9 — Interfaces (Blazor + voice)** [no agent assigned yet — UI specialist]

| # | Task |
|---|---|
| 9.1 | Wire existing Blazor.Web scaffold to `/v1/chat/completions` with SSE |
| 9.2 | Sidebar: session list, memory dump, recent tool calls, agent traces |
| 9.3 | Markdown + code rendering, syntax highlighting |
| 9.4 | (Stretch) Voice I/O — `Azure.AI.Speech` STT/TTS, push-to-talk |
| 9.5 | (Stretch) System tray app for "Hey JARVIS" hotkey |

---

## Part 4 — Squad agents created for this roadmap

Six new agents now live under [`.claude/agents/`](.claude/agents/). They follow the same handoff-envelope + structured-action protocol as the existing Squad (Coder, Tester, Architect, etc.) so they compose cleanly.

| Agent | File | Role | Phases owned |
|---|---|---|---|
| `jarvis-conductor` | [.claude/agents/jarvis-conductor.md](.claude/agents/jarvis-conductor.md) | Reads this file, picks next task in priority order, delegates to specialists. | All — orchestrator |
| `gateway-bugfix` | [.claude/agents/gateway-bugfix.md](.claude/agents/gateway-bugfix.md) | Fixes the 5 critical bugs in §1.6. Tightly scoped. | 1 |
| `jarvis-memory-architect` | [.claude/agents/jarvis-memory-architect.md](.claude/agents/jarvis-memory-architect.md) | Designs + implements sessions, structured memory, vector store, RAG. | 2, 4 |
| `jarvis-tools-architect` | [.claude/agents/jarvis-tools-architect.md](.claude/agents/jarvis-tools-architect.md) | Un-disables MCP, ships built-in tool set, wires `HostedMcpServerTool`. | 3 |
| `jarvis-agent-architect` | [.claude/agents/jarvis-agent-architect.md](.claude/agents/jarvis-agent-architect.md) | Implements `IAgentAdapter`, agent loops, Microsoft Agent Framework integration, persona. | 5, 6 |
| `jarvis-vision-architect` | [.claude/agents/jarvis-vision-architect.md](.claude/agents/jarvis-vision-architect.md) | Vision DTO + multimodal content parts + provider capability routing. | 8 (Phase-1 hooks) |

**How to use them:**

```
# Pick next priority task and dispatch:
> Use the jarvis-conductor agent

# Tackle a specific phase directly:
> Use the gateway-bugfix agent
> Use the jarvis-memory-architect agent

# Combine with existing Squad:
> Use the jarvis-conductor agent — it will delegate to squad-coder + squad-tester for implementation
```

These agents READ from disk (this `analysis.md`, ADRs, current code). They do not inherit chat context. They emit structured-action tags (`[EDIT]`, `[CHECKPOINT]`, `[BLOCKED]`, `[DONE]`) per the existing protocol at [`prompts/squad/protocol/`](prompts/squad/protocol/).

---

## Part 5 — Research reading list (highest leverage first)

1. **`research/https-github-com-microsoft-agent-framework.md`** — already in repo. Read before Phase 5.
2. **`research/https-github-com-microsoft-agent-framework-samples.md`** — for `MapDevUI` and ReAct loop patterns.
3. **MEAI `IEmbeddingGenerator<string, Embedding<float>>`** — `microsoft_docs_search "Microsoft.Extensions.AI embeddings"`.
4. **SQLite-vec extension** — `https://github.com/asg017/sqlite-vec`. Uses standard `sqlite3` connection, ships as a single file.
5. **MEAI `ChatMessage.Contents` / `AIContent` hierarchy** — needed for vision in Phase 1.
6. **Microsoft Agent Framework `AIAgent` + `AgentThread`** — Phase 5 primitives.
7. **MCP HostedMcpServerTool mapping** — `microsoft_code_sample_search "HostedMcpServerTool"`.
8. **OpenAI Chat Completions streaming exact spec** — for Phase 1 wire compliance.

---

## Part 6 — Anti-goals (what NOT to build, in order of how often it tempts)

1. **Don't add the 6 removed providers** until JARVIS itself works. Provider variety is shallow value compared to memory/tools/agents.
2. **Don't build a full LiteLLM proxy admin UI.** Open WebUI as the chat surface + Aspire dashboard for telemetry are enough.
3. **Don't implement multi-tenancy / virtual keys / spend caps.** Single user. Trust boundary is the host.
4. **Don't write your own tool-calling loop.** MEAI `FunctionInvokingChatClient` already does it. The bug is upstream (Bug #3) — fix that, don't replace MEAI.
5. **Don't replace the squad with something new.** It's already good and Allen has invested heavily. Extend with JARVIS agents (this file does that), don't fork.
6. **Don't build a vector DB from scratch.** SQLite-vec, Qdrant, or Postgres+pgvector. Pick one and move on.
7. **Don't build the Blazor UI before Layer 1-3 work end-to-end via curl.** UI hides bugs.
8. **Don't add Gemini back yet.** Vision via gpt-4o is sufficient for Phase 1 + Yardly.
9. **Don't optimize prematurely.** Routing overhead is not the problem. Memory and tools are the value-add.
10. **Don't write more PRDs.** This file replaces them. Update it as phases land.

---

## Part 7 — Definition of "JARVIS works"

A demo Allen can run, end-to-end:

1. Open browser to Blazor chat.
2. Type: "JARVIS, what was that thing I asked you about Yardly's vision pipeline last week?"
3. JARVIS: calls `search_knowledge` (RAG over past sessions), returns the conversation excerpt + summary.
4. Type: "Add a new ADR for the multimodal DTO change. Use the squad."
5. JARVIS: invokes `delegate_to_squad`, the Conductor runs Architect → Coder → Tester → Reviewer, returns artifact paths.
6. Type: "Show me the diff."
7. JARVIS: calls `git_diff`, renders.
8. Type: "Commit it with a good message."
9. JARVIS: calls `git_log` for style, drafts a message, calls `run_shell` with `git commit`.

Every one of those tools, every one of those agent steps, every memory recall — they're all features in the phases above. **That demo is the north star.**

---

## Part 8 — Update protocol

When a phase lands:
1. Strike the completed tasks in their phase table (markdown checkbox or strikethrough).
2. Update Part 1.6 / 1.7 to remove fixed items.
3. Note completion date next to the phase header.
4. If scope changes, add a "Phase N notes" subsection. Don't rewrite the original plan.

When a new ADR is written:
1. Add to Part 1.5 table.
2. Cross-reference from the affected phase.

When research is consumed:
1. Cross off in Part 5.
2. If it produced architectural changes, write an ADR.
