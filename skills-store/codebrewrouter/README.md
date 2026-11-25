# Blaze.LlmGateway

An intelligent, agentic LLM routing proxy for .NET 10. Blaze.LlmGateway exposes a single OpenAI-compatible API endpoint and transparently routes requests to the best available LLM provider based on intent, availability, and configuration — without requiring any changes from the client.

---

## What It Does

Blaze.LlmGateway sits between your application and multiple LLM providers. Clients send standard OpenAI-compatible chat requests to one endpoint. The gateway classifies the request, selects the most appropriate provider, injects any available MCP tools, and streams the response back — all transparently.

The gateway currently targets three dev providers: **Azure AI Foundry**, **Azure Foundry Local**, and **GitHub Models**. A local Ollama client is retained internally as the routing/classifier brain but is not exposed as a selectable provider.

---

## How Routing Works

Routing is handled in two stages:

**Stage 1 — Meta-routing:** The last user message is sent to a local Ollama "router" model configured to return a provider name. This gives the gateway intent-aware, semantic routing at near-zero cost.

**Stage 2 — Keyword fallback:** If the Ollama router fails or returns an unrecognized response, a keyword strategy scans the message for provider hints (e.g. "foundry local", "github", "azure"). If no match is found, the request falls back to Azure AI Foundry.

---

## Solution Structure

| Project | Purpose |
|---|---|
| Blaze.LlmGateway.Core | Domain types: RouteDestination enum and LlmGatewayOptions configuration. No external dependencies. |
| Blaze.LlmGateway.Infrastructure | MEAI middleware pipeline, routing strategies, MCP connection management, and provider registrations. |
| Blaze.LlmGateway.Api | Minimal API host. Wires DI via extension methods and exposes the POST /v1/chat/completions SSE streaming endpoint. |
| Blaze.LlmGateway.AppHost | .NET Aspire orchestration. Provisions GitHub Models resources and the Agent Framework DevUI playground. Injects all secrets as environment variables. |
| Blaze.LlmGateway.ServiceDefaults | Shared Aspire conventions: OpenTelemetry, HTTP resilience, health checks, and service discovery. |
| Blaze.LlmGateway.Tests | xUnit unit tests with Moq. 95% coverage target. |
| Blaze.LlmGateway.Benchmarks | BenchmarkDotNet project for provider latency and routing overhead analysis. |

---

## MEAI Middleware Pipeline

The gateway uses a layered Microsoft.Extensions.AI (MEAI) middleware pipeline. Requests flow from outermost to innermost:

- **McpToolDelegatingClient** — retrieves available tools from McpConnectionManager and injects them into ChatOptions before the request continues downstream.
- **LlmRoutingChatClient** — resolves the target RouteDestination via IRoutingStrategy, then forwards the request to the appropriate keyed provider client.
- **FunctionInvokingChatClient** — registered per-provider; handles automatic MCP tool call execution and result injection.
- **Keyed provider client** — the actual model call (AzureOpenAIClient, OllamaApiClient, OpenAIClient, or Google GenAI client depending on the destination).

---

## MCP Integration

The gateway integrates with the Model Context Protocol (MCP). McpConnectionManager starts as a hosted service and connects to configured MCP servers over Stdio or HTTP transport, caching the available tools. The microsoft-learn MCP server is wired by default via the Node.js npx transport.

---

## Configuration

All provider credentials and endpoints are managed as .NET Aspire parameters set on the AppHost project. This means no secrets are stored in any project config files — they are injected at runtime as environment variables.

The full LlmGatewayOptions configuration lives under the LlmGateway section, with per-provider settings under LlmGateway:Providers:[ProviderName]. Routing options including the router model name and fallback destination are also configurable via this section.

---

## Observability

The gateway is instrumented with OpenTelemetry via the shared ServiceDefaults project, covering traces, metrics, and logs. All providers participate in distributed tracing through the MEAI pipeline.

---

## API Documentation

The API now exposes three complementary documentation surfaces:

| Surface | URL | Purpose |
|---|---|---|
| OpenAPI JSON | `/openapi/v1.json` | Built-in ASP.NET Core OpenAPI document for tooling and machine consumption. |
| Swagger JSON | `/openapi/v1.swagger.json` | Swashbuckle-generated document used by Swagger UI. |
| Swagger UI | `/swagger` | Interactive API explorer and request runner. |
| Scalar | `/scalar` | Polished API reference with a docs-first reading experience. |

Both interactive docs surfaces are available for the API host and are intended to help consumers understand the OpenAI-compatible contract, including the difference between regular JSON responses and streaming SSE responses.

### Sample requests

#### Chat completions (JSON response)

```bash
curl -X POST http://localhost:5022/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      { "role": "system", "content": "You are concise." },
      { "role": "user", "content": "Explain the routing behavior in 3 bullets." }
    ],
    "temperature": 0.2,
    "stream": false
  }'
```

#### Chat completions (streaming SSE)

```bash
curl -N -X POST http://localhost:5022/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "model": "gpt-4",
    "messages": [
      { "role": "user", "content": "Stream a short API summary." }
    ],
    "stream": true
  }'
```

Streaming responses are emitted as `text/event-stream`, with each event prefixed by `data:` and terminated by a final `data: [DONE]` marker.

#### Legacy completions

```bash
curl -X POST http://localhost:5022/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "prompt": "Write a one sentence summary of Blaze.LlmGateway.",
    "maxTokens": 64,
    "stream": false
  }'
```

#### Model catalog

```bash
curl http://localhost:5022/v1/models
```

#### Validation error example

If a required field such as `model` is missing, the gateway returns an OpenAI-style error envelope:

```json
{
  "error": {
    "message": "Missing required field: model",
    "type": "invalid_request_error",
    "code": "missing_field"
  }
}
```

For quick local experimentation, `Blaze.LlmGateway.Api\Blaze.LlmGateway.Api.http` includes ready-to-run requests for the docs endpoints, chat completions, legacy completions, streaming examples, and validation failures.

---

## Dev UI Playgrounds

For interactively testing `/v1/chat/completions` (including streaming and routing) the AppHost orchestrates two ready-made playgrounds as container / executable resources. Both are toggled via `appsettings.json` on the AppHost (or env overrides):

```jsonc
// Blaze.LlmGateway.AppHost/appsettings.json
"DevUI": {
  "OpenWebUI": true,              // default: generic OpenAI-compatible chat UI
  "OpenWebUIImageTag": "v0.10.2",  // Open WebUI container tag
  "AgentFramework": false         // opt-in: Python Agent Framework DevUI
}
```

| Playground | Resource | Prereqs | Good for |
|---|---|---|---|
| **Open WebUI** | container `ghcr.io/open-webui/open-webui:v0.10.2`, port 8080 | Docker Desktop. `OPENAI_API_BASE_URL` is wired at `{api}/v1` automatically. Login disabled for local dev; chats persist in the `blaze-openwebui-data` volume. Override `DevUI:OpenWebUIImageTag` to test another release. | Everyday chat testing, comparing routed responses, multi-turn conversations. |
| **Agent Framework DevUI** | executable `devui` (port 8765) | Python 3.11+ with `pip install agent-framework-devui` (puts `devui` on PATH). AppHost passes the bundled `devui-agents/` directory containing a `gateway_agent` that chats through the gateway. | Trace / telemetry inspection and exercising the Python `agent-framework` SDK against the gateway. |

Once `dotnet run --project Blaze.LlmGateway.AppHost` is up, open the Aspire dashboard and click the `openwebui` (or `agent-devui`) resource URL to reach the playground.

---

## Current Status

The core pipeline (routing, streaming, MCP tool injection, and Aspire orchestration) is operational. The following areas are scaffolded but not yet complete:

- Circuit breaker — no provider health tracking or automatic failover.
- Streaming failover — mid-stream failure handling is not implemented.
- Authentication — no API key or bearer token enforcement on the gateway itself.
- Rate limiting and cost/token tracking are not yet implemented.
- McpConnectionManager and McpToolDelegatingClient have known implementation gaps noted in CLAUDE.md.

---

## Repository Conventions

- All LLM interactions use Microsoft.Extensions.AI abstractions. Raw HttpClient calls to LLM APIs are not permitted.
- New middleware must inherit from DelegatingChatClient.
- Provider clients are resolved via keyed DI using the RouteDestination enum name as the key.
- C# 13/14 features are used throughout: primary constructors, collection expressions, nullable reference types, and full CancellationToken propagation.
- All DI registration logic lives in Infrastructure extension methods, not in Program.cs.

---

## 🚀 Development Squad

This repository ships a **9-agent development squad** for rapid, high-quality feature delivery. The squad enforces architectural guardrails, code quality gates (95% coverage, `-warnaserror`), clean-context reviews, and security audits automatically.

### Quick Launch

**Option 1: Human-Gated Phased Development** (Recommended for complex features)
```bash
/agent squad "Add circuit breaker pattern to LlmRoutingChatClient"
```

**Option 2: Autonomous Parallel Development** (For clear, decomposable tasks)
```bash
/orchestrate "Implement provider health checks in AppHost"
```

### The 9 Agents
- **Conductor** — orchestrates phases and gates decisions
- **Planner** — research, specification, planning
- **Architect** — ADR authoring, MEAI pipeline validation
- **Coder** — C# implementation
- **Tester** — xUnit tests, 95% coverage enforcement
- **Reviewer** — clean-context diff review, quality gate
- **Infra** — AppHost, Aspire, secrets management
- **Security-Review** — ADR-0008 cloud-egress audits
- **Orchestrator** — autonomous parallel loop (no human gates)

### See Also
- **SQUAD_QUICKSTART.md** — Detailed guide with examples and troubleshooting
- **.github/copilot-instructions.md** — Squad architecture and commands
- **CLAUDE.md** — Conventions, guardrails, and agent capabilities
- **Docs/design/adr/0010-parallel-orchestration-path.md** — Why two paths (phased vs. parallel)?

---

## Agent Guidance

### Codex Project Skills

Codex skills for this repository are project-local only and live under `.agents/skills/`. Do not install CodebrewRouter-specific skills into a user-global Codex skill directory unless that is explicitly requested.

The project skill pack has five focused workflows:

- `.agents/skills/codebrewrouter-architecture-routing/` for MEAI pipeline, routing, provider DI, streaming, context sizing, and model catalog work.
- `.agents/skills/codebrewrouter-codebase-onboarding/` for repository maps, architecture summaries, likely-file discovery, and contributor onboarding.
- `.agents/skills/codebrewrouter-mcp-provider-security/` for MCP, provider secrets, cloud egress, tool exposure, supply-chain, and agent governance review.
- `.agents/skills/codebrewrouter-aspire-local-dev/` for AppHost, ServiceDefaults, local inference, model warmup, provider parameters, Open WebUI, and local troubleshooting.
- `.agents/skills/codebrewrouter-logging-contract/` for the existing `[ROUTER-*]` and `[AGENT-*]` logging contract.

The approved design is in `Docs/superpowers/specs/2026-05-22-codebrewrouter-codex-project-skills-design.md`, and the implementation plan is in `Docs/superpowers/plans/2026-05-22-codebrewrouter-codex-project-skills.md`.

### Copilot

For architecture decisions, pipeline changes, routing strategy work, and MCP integration in Copilot, use the repo-scoped Copilot agent defined in `.github/agents/llm-gateway-architect.agent.md`. It has deep familiarity with the MEAI pipeline, all providers, and the project's conventions. Full build, test, and run commands are documented in CLAUDE.md.
