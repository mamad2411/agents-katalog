---
name: error-handling-backend
description: Backend error-handling strategy for BallastLane — Result pattern vs. the codebase's real exception-based handlers, FluentValidation at the boundary, ProblemDetails (RFC 9457) responses, and a global IExceptionHandler. Load this skill when deciding how a handler signals failure, mapping errors to HTTP status codes, or wiring the global exception middleware.
---

# Error Handling — Backend

> ⚠️ **Reconciliation note (read first).** This skill documents a **Result-pattern target design**, but the confirmed real handlers in this codebase (`LogInHandler`, `SignUpHandler`) currently **throw exceptions** for expected failures (`UnauthorizedAccessException`, `InvalidOperationException`, `KeyNotFoundException`). Both are internally consistent approaches — **pick one per bounded context and stay consistent.** The `testing-tdd` skill's example asserts the *real* exception-based pattern (`Assert.ThrowsAsync<KeyNotFoundException>`). If you adopt the Result pattern below for Task use cases, that's a legitimate choice — just don't half-migrate Auth. Decide deliberately.

## Result Pattern in Handlers (target design)

- **DO** return a `Result<T>` from every MediatR handler for expected failure paths (not found, validation, conflict, unauthorized). The controller maps `Result` → HTTP response.
- **DON'T** throw exceptions for expected/predictable failures (a task that doesn't exist, a duplicate user email). Exceptions are for truly exceptional, unrecoverable situations only.

```csharp
// DO
public async Task<Result<TaskResponse>> Handle(GetTaskByIdQuery request, CancellationToken ct)
{
    var task = await _repository.GetByIdAsync(request.Id, ct);
    return task is null
        ? Result<TaskResponse>.NotFound($"Task {request.Id} not found")
        : Result<TaskResponse>.Success(_mapper.Map<TaskResponse>(task));
}
```

- **Typed error codes:** `NotFound`, `Validation`, `Conflict`, `Unauthorized` — map consistently to HTTP status codes in the controller/a shared result-to-`IActionResult` extension.

## FluentValidation at the Boundary

- **Every Command/Query with user input gets a paired `Validator`** in the same use-case folder (`CreateTaskCommand` → `CreateTaskValidator`). Wired through the MediatR pipeline behavior so validation runs before the handler executes. (See the `webapi-crud` skill for the `ValidationBehavior` wiring — and note Auth deliberately validates in the handler/entity instead.)
- **Validation failures return `Result.Validation`** (or, in the exception-based approach, surface as a `ValidationException` the global handler turns into a 400) — keep the handler's happy path clean either way.

```csharp
public sealed class CreateTaskValidator : AbstractValidator<CreateTaskCommand>
{
    public CreateTaskValidator()
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(200);
        RuleFor(x => x.DueDate).GreaterThan(DateTime.UtcNow);
    }
}
```

## ProblemDetails for HTTP Responses

- **DO** return ProblemDetails (RFC 9457) for every HTTP error response — a consistent shape the Angular frontend can parse the same way regardless of which endpoint failed (see the `error-handling-frontend` skill for the consuming side).
- **DON'T** return bare strings or ad-hoc JSON error shapes.

## Exception Handling Boundaries

- **DO** register a global exception handler/middleware in the WebAPI project (`app.UseExceptionHandler()` + `IExceptionHandler`) to catch genuinely unhandled exceptions and return a ProblemDetails 500 without leaking stack traces. In the exception-based approach, this same handler is also where `UnauthorizedAccessException` → 401, `KeyNotFoundException` → 404, `InvalidOperationException` (duplicate) → 409 are mapped.
- **DON'T** catch bare `Exception` anywhere except that outermost boundary.
- **DON'T** catch-and-rethrow without adding context — either handle it (convert to `Result`) or let it propagate to the global handler.

## Quick Reference

| Scenario | Result-pattern approach | Exception-based approach (current real code) |
|---|---|---|
| Task/User not found | `Result.NotFound` | `throw KeyNotFoundException` → 404 |
| Invalid CreateTask/RegisterUser input | `Result.Validation` (FluentValidation) | `ValidationException` → 400 |
| Duplicate user email on register | `Result.Conflict` | `throw InvalidOperationException` → 409 |
| Invalid credentials on login | `Result.Unauthorized` | `throw UnauthorizedAccessException` → 401 |
| Unhandled crash | Global `IExceptionHandler` → ProblemDetails 500 | same |
