---
applyTo: "**/*.cs"
description: C# and .NET authoring standards.
---

# C# Instructions

- Enable nullable reference types and treat warnings as errors.
- Every `IDisposable` is consumed with `using` or disposed in `finally`. Async resources use `await using`.
- Flow `CancellationToken` through every async call chain. Do not swallow `OperationCanceledException`.
- Never use `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` on async code.
- Use `HttpClient` through `IHttpClientFactory`. Do not construct and dispose it per call.
- Prefer dependency injection over static state and service locators.
- Use `ILogger` with structured message templates. Never interpolate secrets or personal data into logs.
- Use parameterized queries or an ORM. Never build SQL by concatenation.
- Prefer `sealed` classes and immutable records for data carriers.
- Validate arguments at public entry points and throw the specific framework exception type.
- Keep methods short and single-purpose. Split any method that needs section comments.
