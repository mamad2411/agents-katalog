# CodebrewRouter (Blaze.LlmGateway)

.NET 10 LLM Gateway — an intelligent LLM routing proxy built on `Microsoft.Extensions.AI`.

## Codex Project Skills

Codex skills for this repository are project-local only. Keep them under `.agents/skills/` and do not install or copy them into `$CODEX_HOME/skills` or any other user-global skill directory unless the user explicitly asks for a global install.

Project skill pack:

- `.agents/skills/codebrewrouter-architecture-routing/` — MEAI pipeline, keyed provider DI, routing strategies, streaming, provider identity, failover, context sizing, and model catalog behavior.
- `.agents/skills/codebrewrouter-codebase-onboarding/` — repository mapping, architecture explanation, likely-file discovery, docs/ADR summaries, and contributor onboarding.
- `.agents/skills/codebrewrouter-mcp-provider-security/` — MCP configuration, provider secrets, cloud egress, tool exposure, supply-chain, and agent governance review.
- `.agents/skills/codebrewrouter-aspire-local-dev/` — Aspire AppHost, ServiceDefaults, local model startup, local inference, provider parameters, Open WebUI, Agent Framework DevUI, and local troubleshooting.
- `.agents/skills/codebrewrouter-logging-contract/` — existing router and agent logging contract guard for `[ROUTER-*]` and `[AGENT-*]` tags.

The design is documented in `Docs/superpowers/specs/2026-05-22-codebrewrouter-codex-project-skills-design.md`; the implementation plan is in `Docs/superpowers/plans/2026-05-22-codebrewrouter-codex-project-skills.md`.

## Custom Agent

A repo-scoped Copilot custom agent is available at `.github/agents/llm-gateway-architect.agent.md`.

Invoke it in Copilot CLI with: `/agent llm-gateway-architect`

The agent is deeply familiar with the MEAI pipeline, all 5 LLM providers, MCP infrastructure, resilient failover routing (circuit breaker, fallback chains, throttle detection), and all project conventions.

---

## Scaffolding History

The following steps were used to initially scaffold this solution (kept for reference):

### codebrewrouter

You are an expert .NET 10 Enterprise Architect. Scaffold a new C# solution named `Blaze.LlmGateway` that acts as an intelligent, agentic LLM routing proxy using the `Microsoft.Extensions.AI` framework.

**Requirements:**
1. **Framework:** .NET 10 exactly. Use top-level statements and Minimal APIs.
2. **Architecture:** Clean Architecture with three projects: `Blaze.LlmGateway.Api`, `Blaze.LlmGateway.Core`, and `Blaze.LlmGateway.Infrastructure`.
3. **Packages:** Add the following to the `Infrastructure` project:
   - `Microsoft.Extensions.AI`
   - `Microsoft.Extensions.AI.OpenAI`
   - `Microsoft.Extensions.AI.Ollama`
   - `Google.Generative.AI`
   - `ModelContextProtocol`

**Step 1: Core Definitions**
In the `Core` project, create an enum `RouteDestination { AzureFoundry, Ollama, GithubModels, Gemini, OpenRouter }`.

**Step 2: MCP Infrastructure**
In the `Infrastructure` project:
1. Create an `McpConnectionManager` singleton that connects to configured MCP servers (support both Stdio and HTTP transports) during application startup and caches the available tools.
2. Create an `McpToolDelegatingClient` (inheriting from `DelegatingChatClient`). This middleware must intercept incoming requests, retrieve available tools from the `McpConnectionManager`, map them to `HostedMcpServerTool` instances, and append them to `ChatOptions.Tools`.

**Step 3: The Router Middleware**
In the `Infrastructure` project, create `LlmRoutingChatClient` inheriting from `DelegatingChatClient`.
- Inject `IServiceProvider` (or use `[FromKeyedServices]`) to resolve the target `IChatClient` dynamically.
- Override `CompleteAsync` and `CompleteStreamingAsync`.
- Implement a basic heuristic/switch statement that maps the incoming prompt content to a specific `RouteDestination`, retrieves the matching `IChatClient`, and forwards the request.

**Step 4: Multi-Provider API Setup (Program.cs)**
In the `Api` project's `Program.cs`, register the following keyed DI services using placeholder API keys and endpoints:
1. **Azure Foundry:** `AzureOpenAIClient` -> `.AsChatClient()`. Key: "AzureFoundry".
2. **Ollama:** `OllamaApiClient` -> `.AsChatClient()`. Key: "Ollama".
3. **GitHub Models:** `OpenAIClient` (endpoint: `https://models.inference.ai.azure.com`) -> `.AsChatClient()`. Key: "GithubModels".
4. **OpenRouter:** `OpenAIClient` (endpoint: `https://openrouter.ai/api/v1`) -> `.AsChatClient()`. Key: "OpenRouter".
5. **Gemini:** `GenerativeAIClient` -> `.AsIChatClient("gemini-2.0-flash")`. Key: "Gemini".

**Step 5: Pipeline Registration & Endpoint**
In `Program.cs`, when registering the `IChatClient` pipeline, ensure the middleware is stacked exactly like this:
1. The base model clients (Keyed DI).
2. `.AsBuilder().UseFunctionInvocation()` (to handle MCP tool execution).
3. The `McpToolDelegatingClient`.
4. The `LlmRoutingChatClient` (registered as the primary, unkeyed `IChatClient`).

Finally, expose a `POST /v1/chat/completions` endpoint that accepts a standard OpenAI-formatted payload, passes it to the primary router, and uses `CompleteStreamingAsync` to stream the result back to the client.

**Step 6: .NET Aspire Integration**
Create a .NET Aspire project (AppHost and ServiceDefaults) and add them to the solution. Configure the AppHost to run the `Api` project and provision/orchestrate any required resources that the solution needs (e.g., caching, external endpoints, or other dependencies).

**Step 7: Testing**
Create comprehensive unit tests using `Moq` to mock dependencies (like `IChatClient` implementations). Additionally, create integration tests to verify the end-to-end pipeline and routing logic.

**Step 8: Benchmarking**
Create a BenchmarkDotNet project (`Blaze.LlmGateway.Benchmarks`) to benchmark the performance and latency of the different models and measure the routing middleware overhead.

## General Conventions

- **Build & Quality:** Always run build and fix all warnings and errors, if any. Always run tests to ensure 100% passing rate and maintain up to 95% code coverage.
- **Dependencies:** Always update NuGet packages to the latest versions to help protect against vulnerabilities.
- **Session Logs:** On every checkin, create or update a session log at `Docs/session-logs/YYYY-MM-DD.md` documenting what was worked on: goals, files changed, config changes, bug fixes, test deltas, and items deferred. Use `Docs/session-logs/2026-07-08.md` as the template.
- Primary constructors, collection expressions (`[]`).
- Keep `Program.cs` clean; extract complex DI into extension methods.

## Logging Contract

- Router request telemetry must use the exact `[ROUTER-*]` tags documented in `Docs/engineering/logging-contract.md`.
- Agent lifecycle telemetry must use `[AGENT-*]` tags from the same contract.
- Logging guardian agents and skills are project-level only; keep them under `.agents/skills/`, `.github/agents/`, and `.opencode/agents/` in this repo.
- Project command name is `/codebrewrouter-logging`.
- OpenCode command: `.opencode/commands/codebrewrouter-logging.md`.
- Copilot CLI project command: `.claude/commands/codebrewrouter-logging.md`; optional plugin package: `.github/plugins/codebrewrouter-logging/`.
- Codex project skill: `.agents/skills/codebrewrouter-logging-contract/`; optional repo-local command package: `plugins/codebrewrouter-logging/`.
- Prefer `RouterLog.Write(...)` for C# router telemetry and update `Blaze.LlmGateway.Tests/RouterLoggingContractTests.cs` when the contract changes.
