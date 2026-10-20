---
name: extensions-ai-patterns
description: 'Implement Microsoft.Extensions.AI patterns in .NET applications. Use when building chat features with IChatClient abstraction, adding function/tool calling, composing middleware pipelines, wiring telemetry, improving resiliency with retries and timeouts, or testing AI integrations. Covers provider-agnostic patterns for Azure OpenAI, OpenAI, Anthropic, Ollama.'
---

# Microsoft.Extensions.AI Patterns

Use this skill when implementing or refactoring .NET code that relies on `Microsoft.Extensions.AI` abstractions.

## When To Use This Skill

- You need a provider-agnostic `IChatClient` boundary.
- You are adding function/tool calling.
- You need middleware composition (telemetry, retry, caching, policy).
- You need production reliability and observability for AI paths.
- You need testable AI integration patterns.

## Core Principles

1. Keep app code dependent on `IChatClient`, not provider SDK types.
2. Compose behavior with middleware/pipeline layers instead of ad-hoc logic.
3. Pass `CancellationToken` through all async boundaries.
4. Use structured logging and OpenTelemetry correlation for every AI operation.
5. Prefer deterministic validation for tool I/O and structured responses.

## Recommended Package Baseline

- `Microsoft.Extensions.AI`
- Provider package(s), for example `Microsoft.Extensions.AI.OpenAI`
- `Microsoft.Extensions.DependencyInjection`
- `Microsoft.Extensions.Logging`
- `Microsoft.Extensions.Configuration`

## Implementation Workflows

### 1. Abstraction-First Chat Client

1. Register provider-specific implementation in DI.
2. Expose only `IChatClient` to business/application layers.
3. Keep provider configuration in options/config sections.
4. Add a health check path for dependency visibility.

### 2. Pipeline Composition

1. Start from a base `IChatClient`.
2. Add cross-cutting concerns in layers: options defaults, retry/rate limiting, telemetry, caching, policy checks.
3. Ensure failures at each layer are logged with context IDs.
4. Keep pipeline construction centralized and reusable.

### 3. Tool Calling

1. Define narrow, deterministic functions.
2. Validate tool input before execution.
3. Set safe timeouts and exception handling per tool.
4. Return typed output contracts where possible.
5. Add tests for tool success and failure paths.

### 4. Resilience + Safety

1. Apply timeout and retry policies around model calls.
2. Implement fallback behavior for transient outages.
3. Add content filtering and prompt safety controls where required.
4. Track token usage/latency to manage cost and performance.

### 5. Testing Patterns

1. Mock `IChatClient` at unit-test boundaries.
2. Cover prompt-building and response-parsing behavior with deterministic fixtures.
3. Add integration tests for provider wiring and tool execution.
4. Verify cancellation and timeout behavior.

## Gotchas

- Do not leak SDK-specific response types into domain/application layers.
- Do not use `.Result`/`.Wait()` on async AI calls.
- Do not skip cancellation tokens for long-running AI interactions.
- Do not allow unvalidated tool arguments to execute side effects.
- Do not treat generated text as trusted data without validation.

## Troubleshooting

| Symptom | Likely Cause | Action |
|---|---|---|
| Random timeouts | Missing timeout policy or overloaded provider | Add explicit timeout + retry with jitter |
| High latency variance | Unbounded tool calls or large prompts | Add prompt limits and tool execution budget |
| Hard-to-debug failures | Missing correlation IDs and structured logs | Add request IDs and OpenTelemetry spans |
| Vendor lock-in creeping in | SDK types passed across boundaries | Refactor to `IChatClient` abstractions |

## Docs-First Guidance

Before implementing, fetch current docs and sample code:

1. `microsoft_docs_search(query="Microsoft.Extensions.AI IChatClient patterns")`
2. `microsoft_code_sample_search(query="Microsoft.Extensions.AI tool calling", language="csharp")`
3. `microsoft_docs_fetch(url="https://learn.microsoft.com/dotnet/ai/microsoft-extensions-ai")`

## References

- Microsoft.Extensions.AI overview: <https://learn.microsoft.com/dotnet/ai/microsoft-extensions-ai>
- IChatClient guidance: <https://learn.microsoft.com/dotnet/ai/ichatclient>
- Agent Framework overview: <https://learn.microsoft.com/agent-framework/overview/>