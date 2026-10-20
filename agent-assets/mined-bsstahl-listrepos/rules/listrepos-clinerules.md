# C#/.NET Coding Rules for This Agent

## 1. General Principles
- Prioritize **clarity, correctness, and maintainability** over cleverness.  
- Avoid unnecessary abstractions, indirection, or patterns that do not provide clear value.  
- Prefer **explicitness** when it improves readability.  
- Code must be **idiomatic modern C#**.
- Avoid fluff in comments and code; keep everything purposeful.

## 2. Solution & Project Structure
- Use a **Clean Architecture–inspired** layout without dogmatism:
  - `Domain` — pure logic, entities, value objects, interfaces.
  - `Application` — services, handlers, validators.
  - `Infrastructure` — EF Core, external services, persistence.
  - `Api` — minimal API or controllers, DI wiring, configuration.
- Keep projects **small and focused**; each project should have a single responsibility.
- Use **dependency injection** consistently; avoid service locators and static state.
- Avoid creating interfaces unless they:
  - Enable testing, or  
  - Abstract a boundary (I/O, persistence, external services).

## 3. Coding Style
- Use **expression‑bodied members** when they improve readability.
- Use `var` when the type is obvious; otherwise use explicit types.
- Use **nullable reference types** and treat warnings as errors.
- Use **records** for immutable data models.
- Use **pattern matching** where it improves clarity.
- Use **guard clauses** to reduce nesting.
- Avoid magic strings — use constants, enums, or strongly typed options.
- Keep comments minimal; explain **why**, not what.

## 4. LINQ & Collections
- Prefer fluent LINQ for transformations and filtering.
- Avoid LINQ when it obscures intent or harms performance.
- Use `IReadOnlyList<T>` or `IEnumerable<T>` for return types unless mutation is required.
- Avoid unnecessary allocations in hot paths.

## 5. Async & Concurrency
- Use `async`/`await` end‑to‑end; avoid mixing sync and async.
- Do not block on async (`.Result`, `.Wait()`).
- Use `CancellationToken` in all async APIs.
- Prefer `Task` over `ValueTask` unless performance profiling justifies it.

## 6. Error Handling & Reliability
- Use **Polly** for retries, circuit breakers, and resilience when interacting with external systems.
- Avoid swallowing exceptions; log with context.
- Use structured logging (`ILogger<T>`, Serilog sinks, etc.).
- Use domain‑specific exceptions sparingly; prefer error results or discriminated unions when appropriate.

## 7. Configuration & Options
- Use strongly typed configuration via `IOptions<T>` or `IOptionsSnapshot<T>`.
- Validate configuration at startup using `ValidateDataAnnotations()` or custom validators.
- Never hardcode secrets; use environment variables or secret stores.

## 8. API Design
- Prefer **minimal APIs** for small services; controllers for larger or more complex APIs.
- Use clear, consistent routing conventions.
- Use request/response DTOs; do not expose domain entities directly.
- Validate input using FluentValidation or similar.
- Use problem‑details responses for errors.

## 9. Data & Persistence
- Use the repository pattern for all data access
- Prefer document data stores to relational ones
- Use Neo4j as a graph data store when appropriate

## 10. Testing
- Test behavior, not implementation details.
- Use **xUnit** for tests.
- Use **FluentAssertions** for expressive assertions.
- Use mocks when appropriate to isolate layers
- Use test data builders for readability
- Avoid brittle tests

## 11. Performance & Diagnostics
- Use `dotnet-trace`, `dotnet-counters`, and `dotnet-dump` for diagnostics.
- Use async I/O to avoid thread starvation.
- Use Redis caching when appropriate.
- Use health checks for container orchestration.
- Use OpenTelemetry for metrics and tracing when available.

## 12. Source Control & CI/CD (Model‑Relevant Parts)
- Generate code that is **diff‑friendly** and stable across runs.
- Keep generated files deterministic.
- Avoid unnecessary churn in formatting or ordering.
- Follow semantic versioning when generating versioned artifacts.

## 13. Documentation (Model‑Relevant Parts)
- Use Markdown for generated documentation.
- Use ISO 8601 dates when generating timestamps.
- Keep documentation concise and practical.
- Avoid decorative or verbose comments.

## 14. What the Agent Should Never Do
- Do not generate live demo code or UI scaffolding unless explicitly asked.
- Do not produce code with hidden side effects or global state.
- Do not generate comments that restate the code.
- Prefer comments that explain the why of the code over the what
- Resubmit prompts that trigger content warnings without first rewriting the prompt
