# Blaze.LlmGateway (CodebrewRouter)

An intelligent LLM routing proxy built on .NET 10 and `Microsoft.Extensions.AI` (MEAI). It exposes an OpenAI-compatible API and routes requests across multiple LLM providers using a meta-routing strategy.

## Project Overview

*   **Purpose:** Act as a central, intelligent gateway for LLM requests, providing automatic model selection, MCP tool integration, and resilient failover.
*   **Core Framework:** .NET 10.
*   **Key Library:** `Microsoft.Extensions.AI` (MEAI) for all LLM interactions.
*   **Orchestration:** .NET Aspire for local development and resource provisioning (Ollama, GitHub Models, etc.).
*   **Intelligence:** Uses a local Ollama model as a "meta-router" to classify prompts and select the best provider.

## Architecture

The solution follows a clean architecture pattern:

| Project | Responsibility |
| :--- | :--- |
| **Blaze.LlmGateway.Core** | Domain types, enums (`RouteDestination`), and configuration options (`LlmGatewayOptions`). Minimal dependencies. |
| **Blaze.LlmGateway.Infrastructure** | MEAI pipeline components, MCP integration (`McpConnectionManager`), and routing strategies (`OllamaMetaRoutingStrategy`, `KeywordRoutingStrategy`). |
| **Blaze.LlmGateway.Api** | Minimal API exposing `POST /v1/chat/completions`. Handles DI wiring and SSE streaming. |
| **Blaze.LlmGateway.AppHost** | .NET Aspire AppHost for orchestrating containers and external services. |
| **Blaze.LlmGateway.ServiceDefaults** | Shared Aspire configuration for OpenTelemetry, resilience, and service discovery. |
| **Blaze.LlmGateway.Tests** | xUnit tests with a high coverage target (95%). |
| **Blaze.LlmGateway.Benchmarks** | BenchmarkDotNet for performance and latency analysis. |

### MEAI Middleware Pipeline

The gateway implements a custom pipeline:
1.  **LlmRoutingChatClient:** Resolves the target provider via an `IRoutingStrategy`.
2.  **McpToolDelegatingClient:** Injects MCP-sourced tools into `ChatOptions`.
3.  **FunctionInvokingChatClient:** Standard MEAI middleware for automatic tool invocation.
4.  **Keyed Provider Client:** The final model client (Azure, Ollama, Gemini, etc.).

## Building and Running

### Build
```powershell
dotnet build --no-incremental -warnaserror
```

### Run
*   **Via Aspire (Recommended):** `dotnet run --project Blaze.LlmGateway.AppHost`
*   **API Directly:** `dotnet run --project Blaze.LlmGateway.Api`

### Test
*   **All Tests:** `dotnet test --no-build --collect:"XPlat Code Coverage"`
*   **Specific Class:** `dotnet test --no-build --filter "FullyQualifiedName~LlmRoutingChatClientTests"`

### Benchmarks
```powershell
dotnet run --project Blaze.LlmGateway.Benchmarks --configuration Release
```

## Development Conventions

*   **MEAI First:** All LLM calls MUST use `IChatClient`, `ChatMessage`, and `ChatOptions`. Raw `HttpClient` calls to LLMs are discouraged.
*   **Streaming:** The API is streaming-first. Use `CompleteStreamingAsync` and Server-Sent Events (SSE).
*   **Dependency Injection:** Use Keyed DI for provider registration. New middleware should inherit from `DelegatingChatClient`.
*   **Clean Code:** Use C# 13/14 features like primary constructors and collection expressions (`[]`). Keep `Program.cs` clean by using extension methods for DI registration.
*   **Error Handling:** Ensure `CancellationToken` is propagated through the entire pipeline.

## Known Gaps & Roadmap

*   **Resilience:** Circuit breaker implementation is a high priority.
*   **Streaming Failover:** Handling failures midway through a streaming response.
*   **MCP Connectivity:** Full wiring of `McpConnectionManager` to `HostedMcpServerTool` instances.
