---
name: webapi-crud
description: Controller conventions, DTOs, and FluentValidation for CRUD endpoints in the BallastLane Web API. Read when building or modifying TasksController, its use cases, or any request/response DTO. Complements the clean-architecture skill (layer boundaries) and the error-handling-backend skill (Result/exception handling).
---

# Web API CRUD — Controllers, DTOs, FluentValidation

This skill covers the mechanics of building a CRUD endpoint end to end for `TaskBoundedContext`, consistent with the confirmed real patterns in the `clean-architecture` skill (bounded contexts, Domain-owned repository interfaces, MediatR use cases).

## Anatomy of One CRUD Operation

For `CreateTask`, the full set of files:

```
Core/BallastLane.Application/UseCases/TaskBoundedContext/CreateTask/
  CreateTaskCommand.cs
  CreateTaskHandler.cs
  CreateTaskValidator.cs
  CreateTaskResponse.cs
Core/BallastLane.Domain/TaskBoundedContext/Repositories/
  ITaskRepository.cs         # if not already defined by an earlier use case
Presentation/BallastLane.WebAPI/Controllers/
  TasksController.cs          # gains one new action
```

## DTOs — Records, Never Domain Entities on the Wire

- **Request and Response DTOs are `record` types**, distinct from `TaskDomain`. A controller never returns `TaskDomain` directly — always map to a response DTO first, even if the shape looks identical today. This keeps the API contract independent of internal entity changes.

```csharp
// Application/UseCases/TaskBoundedContext/CreateTask/CreateTaskCommand.cs
public sealed record CreateTaskCommand(
    string Title,
    string Description,
    DateTime DueDate
) : IRequest<CreateTaskResponse>;

// CreateTaskResponse.cs
public sealed record CreateTaskResponse(
    Guid Id,
    string Title,
    string Status,
    DateTime DueDate
);
```

- **`UserId` is not part of the request body** — it comes from the authenticated principal (the `authToken` cookie, validated by `CookieJwtAuthHandler` per the `security-backend` skill), never trusted from client input. Pull it in the controller via `User.FindFirst(ClaimTypes.NameIdentifier)` and pass it into the command explicitly.

```csharp
// DO
[HttpPost]
[Authorize]
public async Task<IActionResult> Create(CreateTaskRequest request, CancellationToken ct)
{
    var userId = Guid.Parse(User.FindFirst(ClaimTypes.NameIdentifier)!.Value);
    var command = new CreateTaskCommand(request.Title, request.Description, request.DueDate, userId);
    var response = await _mediator.Send(command, ct);
    return CreatedAtAction(nameof(GetById), new { id = response.Id }, response);
}

// DON'T — trusting a client-supplied userId
public sealed record CreateTaskRequest(string Title, Guid UserId); // never do this
```

## Controller Conventions

- **One controller per bounded context's public surface** — `TasksController`, `AuthController` (see `jwt-auth/SKILL.md`). A controller action does exactly three things: extract input (route/body/claims), send to MediatR, map the result to an `IActionResult`. Nothing else.
- **Route convention:** `[Route("api/[controller]")]`, action-level `[Http*]` attributes with explicit sub-routes where needed (`[HttpGet("{id}")]`).
- **`[Authorize]` on every action by default for `TasksController`** — a task always belongs to a user, there's no "public task" concept in this exercise. `AuthController` mixes `[AllowAnonymous]` (register/login/refresh) and `[Authorize]` (logout) per action — see the `security-backend` skill.

```csharp
[Route("api/[controller]")]
[ApiController]
[Authorize]
public class TasksController : ControllerBase
{
    private readonly IMediator _mediator;

    public TasksController(IMediator mediator) => _mediator = mediator;

    [HttpGet]
    public async Task<IActionResult> GetAll(CancellationToken ct)
    {
        var userId = GetCurrentUserId();
        var response = await _mediator.Send(new GetAllTasksQuery(userId), ct);
        return Ok(response);
    }

    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetById(Guid id, CancellationToken ct) { ... }

    [HttpPost]
    public async Task<IActionResult> Create(CreateTaskRequest request, CancellationToken ct) { ... }

    [HttpPut("{id:guid}")]
    public async Task<IActionResult> Update(Guid id, UpdateTaskRequest request, CancellationToken ct) { ... }

    [HttpDelete("{id:guid}")]
    public async Task<IActionResult> Delete(Guid id, CancellationToken ct) { ... }

    private Guid GetCurrentUserId() =>
        Guid.Parse(User.FindFirst(ClaimTypes.NameIdentifier)!.Value);
}
```

## FluentValidation

⚠️ Note (see the `clean-architecture` skill): the real `AuthBoundedContext` use cases (`SignUp`, `LogIn`) do **not** use a dedicated FluentValidation `Validator` — they validate via Domain entity guard clauses and explicit duplicate-checks in the handler. **Task use cases are a good place to actually use FluentValidation**, since Task fields (title length, due date in the future) are exactly the kind of input-shape validation FluentValidation is for — this is a legitimate case where Task and Auth diverge in approach, not an inconsistency to "fix."

```csharp
// Application/UseCases/TaskBoundedContext/CreateTask/CreateTaskValidator.cs
public sealed class CreateTaskValidator : AbstractValidator<CreateTaskCommand>
{
    public CreateTaskValidator()
    {
        RuleFor(x => x.Title).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Description).MaximumLength(2000);
        RuleFor(x => x.DueDate).GreaterThan(DateTime.UtcNow)
            .WithMessage("Due date must be in the future.");
    }
}
```

- **Register validators via assembly scanning** in `Program.cs`/DI extensions, not one-by-one:

```csharp
builder.Services.AddValidatorsFromAssembly(typeof(CreateTaskValidator).Assembly);
```

- **Wire validation into the MediatR pipeline** with a `ValidationBehavior<TRequest, TResponse>` (`IPipelineBehavior<TRequest, TResponse>`) so validation runs automatically before every handler — don't call `validator.Validate()` manually inside each handler.

## Status Codes

| Action | Success | Not Found | Validation Failure |
|---|---|---|---|
| `GET` (list) | 200 + array (empty array if none, never 404) | — | — |
| `GET` (by id) | 200 + resource | 404 | — |
| `POST` | 201 + `Location` header (`CreatedAtAction`) | — | 400 (ProblemDetails) |
| `PUT` | 200 or 204 | 404 | 400 (ProblemDetails) |
| `DELETE` | 204 | 404 | — |

See the `error-handling-backend` skill for how failures map to these codes (Result-pattern vs. the real exception-based handling, and how each reconciles).