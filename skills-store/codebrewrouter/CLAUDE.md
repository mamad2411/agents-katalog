# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Blaze.LlmGateway** is a .NET 10 intelligent LLM routing proxy built on `Microsoft.Extensions.AI` (MEAI). It exposes an OpenAI-compatible `POST /v1/chat/completions` streaming endpoint and routes requests across 9 LLM providers using a meta-routing strategy (Ollama-based classifier with keyword fallback).

## Commands

```bash
# Build entire solution (treat warnings as errors)
dotnet build --no-incremental -warnaserror

# Run all tests with coverage
dotnet test --no-build --collect:"XPlat Code Coverage"

# Run a single test class
dotnet test --no-build --filter "FullyQualifiedName~LlmRoutingChatClientTests"

# Run the API directly
dotnet run --project Blaze.LlmGateway.Api

# Run via Aspire orchestration (recommended for local dev)
dotnet run --project Blaze.LlmGateway.AppHost

# Run benchmarks
dotnet run --project Blaze.LlmGateway.Benchmarks --configuration Release
```

## Local Development Secrets

All provider credentials are injected via Aspire parameters. Set them once on the AppHost project:

```bash
dotnet user-secrets set "Parameters:azure-foundry-endpoint"  "<https://your-resource.openai.azure.com/>" --project Blaze.LlmGateway.AppHost
dotnet user-secrets set "Parameters:azure-foundry-api-key"   "<key>"   --project Blaze.LlmGateway.AppHost
dotnet user-secrets set "Parameters:github-models-api-key"   "<PAT>"   --project Blaze.LlmGateway.AppHost
```

## Architecture

### Project Responsibilities

| Project | Role |
|---|---|
| `Core` | Domain types only — `RouteDestination` enum, `LlmGatewayOptions` config classes. Zero external deps. |
| `Infrastructure` | Routing middleware, MCP integration, routing strategies. All MEAI pipeline components live here. |
| `Api` | `Program.cs` wires DI, registers providers via extension methods, exposes the SSE endpoint. |
| `AppHost` | .NET Aspire orchestration — provisions GitHub Models resources, Agent Framework DevUI playground, and wires secrets as environment variables. |
| `ServiceDefaults` | Shared Aspire conventions — OpenTelemetry, HTTP resilience, service discovery. |
| `Tests` | xUnit + Moq unit tests. 95% coverage target. |
| `Benchmarks` | BenchmarkDotNet for provider latency and routing overhead. |

### MEAI Middleware Pipeline (outermost → innermost)

```
McpToolDelegatingClient       ← injects MCP tools into ChatOptions (unkeyed IChatClient)
  └── LlmRoutingChatClient    ← resolves target provider via IRoutingStrategy
        └── [Keyed IChatClient].UseFunctionInvocation()  ← per-provider, actual model call
```

`FunctionInvokingChatClient` is registered individually on each keyed provider via `.AsBuilder().UseFunctionInvocation().Build()`, not as a shared pipeline layer. The unkeyed `IChatClient` registered in `AddLlmInfrastructure` is the `McpToolDelegatingClient` wrapping `LlmRoutingChatClient`.

New middleware must inherit from `DelegatingChatClient` — never implement `IChatClient` directly.

### Routing

- **Primary:** `OllamaMetaRoutingStrategy` — sends the prompt to a local Ollama "router" model that classifies which `RouteDestination` to use. Ollama is retained internally as the classifier brain only; it is not a selectable destination.
- **Fallback:** `KeywordRoutingStrategy` — parses keywords from the last user message (e.g. "foundry local" → FoundryLocal, "github" → GithubModels, "azure" → AzureFoundry). Default destination: AzureFoundry.

### codebrewRouter prompt-cleanup pre-stage

When a request hits the `"CodebrewRouter"` virtual keyed client, `CodebrewRouterChatClient` runs a one-shot prompt-optimization step **before** classification and **before** the downstream provider call. The cleaner is `IPromptCleaner`:

- `GemmaPromptCleaner` (default): uses the keyed `OllamaLocal` (gemma4:e4b) client to rewrite the **last user message** into a tighter, token-efficient form. The cleaned text replaces the last user message in the list passed to both the task classifier and every downstream provider attempt — so the optimization benefit reaches the paid LLM call.
- `NoopPromptCleaner`: registered when `LlmGateway:PromptCleanup:Enabled = false` or `OllamaLocal` is unavailable; passes the prompt through unchanged.

Failure semantics mirror `OllamaTaskClassifier`: any exception opens a circuit breaker (`PromptCleanupOptions.CooldownMinutes`, default 5 min) during which cleanup is skipped. Empty / inflated rewrites are also rejected and the original is forwarded. Short prompts (< `MinLengthChars`, default 80 chars) skip the cleaner entirely to avoid round-trip overhead.

Configure via `LlmGateway:PromptCleanup` in `appsettings.json`.

### Providers (Keyed DI keys)

Three selectable destinations registered as keyed `IChatClient` services: `"AzureFoundry"`, `"FoundryLocal"`, `"GithubModels"`. A fourth keyed client, `"OllamaLocal"`, is registered as an internal classifier brain for `OllamaMetaRoutingStrategy` / `OllamaTaskClassifier` but is **not** in `RouteDestination` and is **not** exposed via `/v1/models`. The `"CodebrewRouter"` virtual keyed client is a task-routing facade over the three real providers.

SDK mappings (must be followed exactly):
- Azure Foundry / FoundryLocal → `AzureOpenAIClient` → `.AsChatClient()`
- GitHub Models → `OpenAIClient` (custom endpoint) → `.AsChatClient()`
- OllamaLocal (internal classifier) → `OllamaApiClient` → `.AsChatClient()`

## Architectural Rules

1. **MEAI is the law.** Never use raw `HttpClient` for LLM calls. Always use `IChatClient`, `ChatMessage`, `ChatOptions`, `ChatRole` from `Microsoft.Extensions.AI`.
2. **MCP tool execution** is handled entirely by MEAI's `FunctionInvokingChatClient`. Never write custom tool-calling loops.
3. **Streaming by default.** The `/v1/chat/completions` endpoint must use `GetStreamingResponseAsync` (the current MEAI API) and SSE. The old `CompleteAsync`/`CompleteStreamingAsync` names no longer exist.
4. **Keyed DI** for all provider resolution. Use `IServiceProvider.GetKeyedService<IChatClient>("ProviderName")` inside router middleware.
5. **Keep `Program.cs` clean.** Extract DI setup into extension methods.
6. **Code style:** Primary constructors, collection expressions (`[]`), nullable reference types enabled, `CancellationToken` propagated throughout.

## Known Incomplete Areas

**Phase 1 (Stop the Bleeding) — ✅ COMPLETE:**
- ✅ Bug 1: GithubModels registration — **DONE**
- ✅ Bug 2: OpenAI wire format — **DONE** (chat.completion.chunk + role/finish_reason + proper chunk sequencing)
- ✅ Bug 3: Function calling forward — **DONE** (tools translated to AIFunctions via AIFunctionFactory.Create)
- ✅ Bug 4: Vision support — **DONE** (multimodal content via ChatMessageContentConverter)
- ✅ Bug 5: Streaming failover — **DONE** (first-chunk probe pattern with fallback chain)

**Other Known Gaps:**
- `McpConnectionManager.StartAsync()` — placeholder; MCP tool connections not fully wired.
- `McpToolDelegatingClient.AppendMcpTools` — needs mapping to `HostedMcpServerTool` instances.
- No circuit breaker — high-priority resilience enhancement for Phase 2.
- Tool invocation handlers — placeholder in TranslateTools; actual tool execution routed to MCP or external handlers (Phase 2).
- Integration test (Tier-A) with real GitHub Models endpoint — scaffolded, awaits credentials for full E2E validation.
- **OpenCodeGo model tokenizers (Phase 3b):** Native Qwen tokenizer loading via `Yuniko.Software.Qwen3Tokenizer` and HuggingFace JSON loading for DeepSeek/GLM models are marked for future implementation. Currently all 14 models gracefully fall back to gpt-4o encoding with logged accuracy warnings (~75-99% depending on model family). No exceptions are thrown; production-safe degradation.

## Squad Orchestration

This repository ships two complementary squad execution paths (ADR-0009 + ADR-0010):

### Phased Conductor (human-gated)
- **Command:** `/agent squad`
- **Execution:** Sequential phases with human gates between each boundary (Planner → Architect → Coder → Tester → Reviewer → Security-Review).
- **Use when:** Task is exploratory, high-risk, or you want human feedback at each phase.
- **Output:** `Docs/squad/runs/<ts>-<slug>/` with reasoning log + handoffs.

### Orchestrator (autonomous)
- **Command:** `/orchestrate --prd <path>`
- **Execution:** Autonomous PRD-driven loop: decompose → parallel worktrees → dispatch subagents → monitor → merge → quality-gate.
- **Use when:** PRD is complete, task decomposes into parallel non-overlapping streams, and you want fully autonomous execution.
- **Output:** Same layout as Conductor, plus `.worktrees/<task>/` for isolated development.

**Comparison:**
| Aspect | Conductor | Orchestrator |
|---|---|---|
| Gating | Human gates at each phase | Fully autonomous |
| Parallelism | Sequential phases | Parallel tasks per phase |
| Execution speed | Slower (human waits) | Faster (no waits) |
| Risk level | Lower (human feedback) | Higher (autonomous) |
| Clean-context review | Per-phase | Post-completion (full log) |

## Squad Guardrails

This repository ships a 9-agent Claude-powered development squad (ADR-0009 + ADR-0010). Source of truth: [`prompts/squad/`](./prompts/squad/). Path-scoped guardrails every squad specialist honors:

- [`prompts/squad/_shared/guardrails.instructions.md`](./prompts/squad/_shared/guardrails.instructions.md) — universal squad rules (MEAI law, streaming, keyed DI, structured-action tags, quality gate).
- [`prompts/squad/_shared/meai-infrastructure.instructions.md`](./prompts/squad/_shared/meai-infrastructure.instructions.md) — scoped to `Blaze.LlmGateway.Infrastructure/**`, `Blaze.LlmGateway.Api/**`, `Blaze.LlmGateway.Core/**`.
- [`prompts/squad/_shared/aspire-apphost.instructions.md`](./prompts/squad/_shared/aspire-apphost.instructions.md) — scoped to `Blaze.LlmGateway.AppHost/**`, `Blaze.LlmGateway.ServiceDefaults/**`.
- [`prompts/squad/_shared/tests.instructions.md`](./prompts/squad/_shared/tests.instructions.md) — scoped to `Blaze.LlmGateway.Tests/**`, `Blaze.LlmGateway.Benchmarks/**`.
- [`prompts/squad/_shared/adr.instructions.md`](./prompts/squad/_shared/adr.instructions.md) — scoped to `Docs/design/adr/**`.
- [`prompts/squad/_shared/cloud-egress.instructions.md`](./prompts/squad/_shared/cloud-egress.instructions.md) — ADR-0008 default-deny, scoped to every C# and `appsettings*.json`.
- [`prompts/squad/_shared/style.instructions.md`](./prompts/squad/_shared/style.instructions.md) — C# style + nullability + build gate.

Protocol and command references:

- Tag vocabulary: [`prompts/squad/protocol/structured-actions.md`](./prompts/squad/protocol/structured-actions.md).
- Handoff envelope: [`prompts/squad/protocol/handoff-envelope.schema.md`](./prompts/squad/protocol/handoff-envelope.schema.md).
- Reasoning log: [`prompts/squad/protocol/reasoning-log.schema.md`](./prompts/squad/protocol/reasoning-log.schema.md).
- Slash commands: `/squad-plan`, `/squad-implement`, `/squad-review`, `/squad-security` (Claude Code) or `/agent squad` (Copilot CLI after `copilot plugin install ./.github/plugins/squad`).

Edit under `prompts/squad/` then run `pwsh ./scripts/sync-squad.ps1` to regenerate the `.github/plugins/squad/` and `.claude/` copies. Never edit the generated copies by hand.

## JARVIS Roadmap Fleet

Above the Squad sits the **JARVIS fleet** — a 6-agent layer that executes the priority-ordered roadmap in [`analysis.md`](./analysis.md). The Conductor reads the roadmap, picks the next-priority phase, and dispatches a JARVIS specialist (which in turn delegates implementation work down to `squad-coder` / `squad-tester` when needed).

Source of truth: [`prompts/jarvis/`](./prompts/jarvis/). Roster:

| Source | Claude agent | Copilot agent | Phase(s) |
|---|---|---|---|
| `conductor.prompt.md` | `jarvis-conductor` | `jarvis.conductor` | Orchestrator |
| `gateway-bugfix.prompt.md` | `gateway-bugfix` | `jarvis.gateway-bugfix` | 1 |
| `memory-architect.prompt.md` | `jarvis-memory-architect` | `jarvis.memory-architect` | 2, 4 |
| `tools-architect.prompt.md` | `jarvis-tools-architect` | `jarvis.tools-architect` | 3 |
| `agent-architect.prompt.md` | `jarvis-agent-architect` | `jarvis.agent-architect` | 5, 6 |
| `vision-architect.prompt.md` | `jarvis-vision-architect` | `jarvis.vision-architect` | 8 |

Invocation:

- **Claude Code:** `> Use the jarvis-conductor agent.` (or jump to a specialist by name).
- **Copilot CLI:** `copilot plugin install ./.github/plugins/jarvis` once, then `/agent jarvis` (or `/agent jarvis.gateway-bugfix` for direct dispatch). Slash commands `/jarvis` and `/jarvis-status` are also wired.

Edit under `prompts/jarvis/` then run `pwsh ./scripts/sync-jarvis.ps1` to regenerate the `.github/plugins/jarvis/` and `.claude/agents/` copies. Never edit the generated copies by hand.
