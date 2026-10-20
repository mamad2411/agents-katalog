# RxLink API — Claude Code Guidelines

## Prescription lifecycle (PrescriptionStatusId maps to PrescriptionStatus table):

Borrador — Default status when a doctor creates a prescription. Not clinically valid yet.
Activo — Set when the doctor explicitly signs the prescription via the sign button. Required before a nurse can dispense it.
Suspendido — The doctor can suspend an Activo prescription at any time before it is dispensed. This is temporary; the doctor can reactivate it back to Activo.
Cancelado — The doctor can permanently cancel a prescription that has not yet been dispensed. This action is irreversible and invalidates the prescription.
Dispensado — Set by a nurse (Enfermero) through the dispensing module, only possible when the prescription is Activo.
Finalizado — Applied when today's date exceeds ValidUntil AND the prescription was already Dispensado.
Caducado — Applied when today's date exceeds ValidUntil AND the prescription was NOT dispensed (i.e., still Activo or Suspendido).

Allowed transitions:
Borrador   → Activo      (doctor signs)
Borrador   → Cancelado   (doctor cancels)
Activo     → Suspendido  (doctor suspends)
Activo     → Cancelado   (doctor cancels — irreversible)
Activo     → Dispensado  (nurse dispenses)
Activo     → Caducado    (ValidUntil exceeded, not dispensed)
Suspendido → Activo      (doctor reactivates)
Suspendido → Cancelado   (doctor cancels — irreversible)
Suspendido → Caducado    (ValidUntil exceeded, not dispensed)
Dispensado → Finalizado  (ValidUntil exceeded, already dispensed)

## Repository layout

| Path | Purpose |
|------|---------|
| `src/RxLinkApi/Controllers/` | HTTP controllers (extend `FunctionalController`) |
| `src/Application.Core.Interfaces/` | Application-layer service contracts |
| `src/Application.Core.Services/` | Business logic — pure Result pipelines |
| `src/Application.Core.DTOs/` | Request / Response / Error DTOs |
| `src/Infrastructure.Core.Interfaces/` | Repository contracts |
| `src/Infrastructure.Core.Services/` | Repository implementations + SQL string files |
| `src/Infrastructure.Core.DTOs/` | Repository-level error types |
| `src/Infrastructure.Core.Models/` | Raw DB row models (`*Row`) |

**Database project**: `/home/Gianfranco/repos/rxlink-db/` — migrations, scripts, schema docs.
Always check it for column names, stored procedure signatures, and UUID/code conventions before writing SQL.

---

## No integer IDs — ever

The database uses `SERIAL` primary keys internally, but **they must never cross the API boundary**.

- Every table also has a `<TableName>Code UUID` column that is the sole public identifier.
- All DTOs, route parameters, and response bodies use the `*Code` (`Guid`) field.
- Route parameters must be typed `{code:guid}`, never `{id:int}`.
- Repository methods accept and return `Guid` codes; SQL resolves the internal PK.

```csharp
// Correct
[HttpPut("{code:guid}")]
public Task<IActionResult> Update(Guid code, ...) => ...

// Wrong — never expose integer IDs
[HttpPut("{id:int}")]
public Task<IActionResult> Update(int id, ...) => ...
```

---

## Functional style — mandatory

All layers use **BindSharp** (`Result<T, TError>`) for error handling. Never break the pipeline with `try/catch` or early returns.

### Layer patterns

**Repository** — wrap every DB call in `Result.TryAsync`; map the caught exception to a typed repository error:

```csharp
public async Task<Result<UserRow?, UserRepositoryError>> InsertAsync(...) =>
    await Result.TryAsync(
        operation: async () => await ExecuteFirstOrDefaultAsync<object, UserRow>(
            _connection, UserRepositorySql.Insert, new { ... }),
        errorFactory: UserRepositoryError (ex) => new InsertUserError(ex.Message, ex)
    );
```

**Application service** — chain repository results with `MapErrorAsync` → `EnsureNotNullAsync` → `MapAsync`:

```csharp
public Task<Result<UserResponse, UserError>> UpdateAsync(Guid code, UpdateUserRequest request) =>
    _repository.UpdateAsync(code, ...)
        .MapErrorAsync(UserError (error) => new UserDataAccessError(error.Message, error.Details, error.Exception))
        .EnsureNotNullAsync(new UserNotFoundError())
        .MapAsync(MapToResponse);
```

**Controller** — delegate Result→HTTP conversion to `FunctionalController` helpers; never call `.Match` directly:

```csharp
// Read — no caller identity needed
public Task<IActionResult> GetPage([FromQuery] UserPageRequest request) =>
    ExecuteAsync(
        operation: () => _userService.GetPageAsync(request),
        errorMapper: _errorMapper,
        operationName: nameof(GetPage)
    );

// Mutation — inject the caller's UUID from the JWT sub claim
public Task<IActionResult> Deactivate(Guid code) =>
    ExecuteAuthenticatedAsync(
        operation: userCode => _userService.DeactivateAsync(code, userCode),
        errorMapper: _errorMapper,
        operationName: nameof(Deactivate),
        successMapper: _ => NoContent()
    );
```

Available `FunctionalController` helpers: `ExecuteAsync`, `Execute`, `ExecuteAuthenticatedAsync`, `ExecuteWithRoleAsync`, `ExecuteNoContent`, `ExecuteCreated`, `ExecuteWithStatus`.

---

## BindSharp — Railway-Oriented Error Handling

> **BindSharp** is a `netstandard2.0` Railway-Oriented Programming (ROP) library for .NET.
> It replaces `try/catch` pyramids with composable, linear pipelines using the `Result<T, TError>` type.
> Every operation either continues on the **success track** or is short-circuited on the **failure track**.

Always include both usings — extension methods live in a separate namespace:

```csharp
using BindSharp;            // Result<T,TError>, Unit, FunctionalResult, AsyncFunctionalResult, Result (static)
using BindSharp.Extensions; // Tap/TapError, Do/DoAsync, Ensure, ToResult, Using, AsTask
```

### Core type: `Result<T, TError>`

| Property    | Meaning                                   |
|-------------|-------------------------------------------|
| `IsSuccess` | `true` when the operation succeeded       |
| `IsFailure` | `true` when the operation failed          |
| `Value`     | The success value — throws if `IsFailure` |
| `Error`     | The error value — throws if `IsSuccess`   |

#### Creating results

```csharp
var ok  = Result<int, string>.Success(42);
var err = Result<int, string>.Failure("Something went wrong");

// Implicit conversions (preferred)
public Result<User, string> FindUser(int id)
{
    if (id <= 0) return "Invalid ID";   // implicitly Failure
    return _db.Find(id);                // implicitly Success
}
```

#### `Unit` — for void-like operations

```csharp
public async Task<Result<Unit, string>> DeleteUserAsync(int id) =>
    await Result.TryAsync(
        async () => { await _repo.DeleteAsync(id); return Unit.Value; },
        ex => $"Delete failed: {ex.Message}"
    );
```

---

### Bridging exception-based APIs: `Try` / `TryAsync`

Use as the **entry point** whenever wrapping code that may throw.

```csharp
var parsed = Result.Try(
    () => int.Parse(input),
    ex => $"Invalid number: {ex.Message}"
);

// Exception-first: log raw exception, then map to friendly message
var result = Result.Try(() => File.ReadAllText("data.txt"))
    .TapError(ex => _logger.LogError(ex, "Read failed"))
    .MapError(ex => ex switch {
        FileNotFoundException       => "File not found",
        UnauthorizedAccessException => "Permission denied",
        _                           => "Failed to read file"
    });

// Async
var response = await Result.TryAsync(
    async () => await _http.GetStringAsync(url),
    ex => $"HTTP error: {ex.Message}"
);
```

---

### Method reference

#### `Map` / `MapAsync` — transform success value (cannot fail)

```csharp
Result<int, string> doubled = Result<int, string>.Success(5).Map(x => x * 2);

var user = await GetIdAsync().MapAsync(async id => await FetchUserAsync(id));
```

#### `Bind` / `BindAsync` — chain fallible operations (prevents `Result<Result<T>>` nesting)

```csharp
var result = await GetOrderAsync()
    .BindAsync(o => ValidateOrder(o))
    .BindAsync(async o => await SaveAsync(o));
```

#### `BindIf` / `BindIfAsync` — conditional continuation

```csharp
var result = await GetOrderAsync()
    .BindIfAsync(
        order => order.NeedsApproval,
        async order => await RequestApprovalAsync(order)
    );
```

#### `MapError` / `MapErrorAsync` — transform error type

```csharp
var result = await FetchAsync()
    .MapErrorAsync(UserError (error) => new UserDataAccessError(error.Message, error.Details, error.Exception));
```

#### `Match` / `MatchAsync` — terminal: collapse to a plain value

Both branches must return the same type.

```csharp
IActionResult response = await pipeline
    .MatchAsync(
        data  => Ok(data),
        error => BadRequest(error)
    );
```

---

### Side effects (do not modify the result)

#### `Tap` / `TapAsync` — on success

```csharp
var result = await GetUserAsync()
    .TapAsync(async u => await _audit.LogAsync(u))
    .MapAsync(u => u.Id);
```

#### `TapError` / `TapErrorAsync` — on failure

```csharp
var result = await FetchAsync()
    .TapErrorAsync(async err => await _alerting.NotifyAsync(err));
```

#### `Do` / `DoAsync` — on either branch

```csharp
await pipeline
    .DoAsync(
        async data  => await _db.LogSuccessAsync(data),
        async error => await _alerting.NotifyAsync(error)
    );
```

---

### Validation

#### `Ensure` / `EnsureAsync` — inline guard clauses

```csharp
var validated = Result<int, string>.Success(5)
    .Ensure(x => x > 0,   "Must be positive")
    .Ensure(x => x < 100, "Must be under 100");
```

#### `EnsureNotNull` / `EnsureNotNullAsync` — null safety

Converts `Result<T?, TError>` to `Result<T, TError>`.

```csharp
Result<User, string> user = await FindUserAsync(id)
    .EnsureNotNullAsync("User not found");
```

---

### Conversion utilities

#### `ToResult` — nullable to Result

```csharp
Result<User, string> result = _cache.Get(id).ToResult("Not in cache");
```

#### `AsTask` — lift sync result into an async pipeline

```csharp
var final = await ValidateOrder(order)
    .AsTask()
    .BindAsync(async o => await SaveAsync(o));
```

---

### Resource management: `Using` / `UsingAsync`

Guarantees `IDisposable` resources are disposed even on failure.

```csharp
var result = await AcquireConnectionAsync()
    .UsingAsync(async conn => await conn.QueryAsync(sql));
```

---

### Decision guide

| Situation | Use |
|-----------|-----|
| Wrapping code that throws | `Result.Try` / `Result.TryAsync` |
| Transform value, cannot fail | `Map` / `MapAsync` |
| Chain to next fallible step | `Bind` / `BindAsync` |
| Conditional next step | `BindIf` / `BindIfAsync` |
| Transform error type | `MapError` / `MapErrorAsync` |
| Collapse Result to plain value | `Match` / `MatchAsync` |
| Log on success only | `Tap` / `TapAsync` |
| Log on failure only | `TapError` / `TapErrorAsync` |
| Log on either branch | `Do` / `DoAsync` |
| Guard / validate inline | `Ensure` / `EnsureAsync` |
| Null-to-Result | `ToResult`, `EnsureNotNull` / `EnsureNotNullAsync` |
| Disposable resource lifecycle | `Using` / `UsingAsync` |
| No meaningful success value | `Unit` / `Unit.Value` |
| Lift sync result into async chain | `AsTask` |

---

### Anti-patterns

```csharp
// ❌ Never access .Value without checking — throws InvalidOperationException
var value = someResult.Value;
// ✅ Use Match
var value = someResult.Match(v => v, err => defaultValue);

// ❌ Don't use Map when the mapper returns a Result — creates Result<Result<T>>
var nested = someResult.Map(x => ValidateX(x));
// ✅ Use Bind to flatten
var flat = someResult.Bind(x => ValidateX(x));

// ❌ Don't mix try/catch with BindSharp pipelines
try { var r = GetResult().Bind(Step2); ... }
// ✅ Wrap the boundary with Try/TryAsync
var r = Result.Try(() => GetResult()).Bind(Step2);

// ❌ Don't ignore the failure track
if (result.IsSuccess) Use(result.Value);
// ✅ Always handle both tracks
result.Do(value => Use(value), error => Handle(error));
```

---

### Namespace cheat sheet

| Namespace | Contains |
|-----------|----------|
| `BindSharp` | `Result<T,TError>`, `Unit`, `FunctionalResult` (Map, Bind, MapError, Match, BindIf), `AsyncFunctionalResult` (all \*Async variants), `Result` static (Try, TryAsync) |
| `BindSharp.Extensions` | `SideEffectExtensions` (Tap, TapAsync, TapError, TapErrorAsync, Do, DoAsync), `ValidationExtensions` (Ensure, EnsureAsync, EnsureNotNull, EnsureNotNullAsync), `ConversionExtensions` (ToResult, AsTask), `ResourceManagementExtensions` (Using, UsingAsync) |

---

## Error model

Each domain defines a discriminated-union base record and concrete subtypes:

```
Application.Core.DTOs/<Domain>/Errors/
  <Domain>Error.cs            ← abstract base (e.g. UserError)
  <Domain>NotFoundError.cs
  <Domain>DataAccessError.cs

Infrastructure.Core.DTOs/<Domain>/
  <Domain>RepositoryError.cs  ← infrastructure-level error base
```

Repository errors are always mapped to application errors in the service layer via `.MapErrorAsync(...)`.

---

## Naming conventions

| Artifact | Pattern | Example |
|----------|---------|---------|
| Row model | `<Entity>Row` | `UserRow` |
| App service interface | `I<Entity>` | `IUser` |
| Repository interface | `I<Entity>Repository` | `IUserRepository` |
| App service | `<Entity>Service` | `UserService` |
| Repository | `<Entity>Repository` | `UserRepository` |
| SQL strings | `<Entity>RepositorySql` | `UserRepositorySql` |
| Request DTOs | `Create<Entity>Request`, `Update<Entity>Request`, `<Entity>PageRequest` | |
| Response DTOs | `<Entity>Response`, `<Entity>PageResponse` | |

---

## Soft deletes

Records are never hard-deleted. Use `Deactivate` / `Activate` (`PATCH {code}/deactivate`, `PATCH {code}/activate`) to toggle `IsActive`. This preserves FK integrity.


## AI test database

To boot the API or run SQL for real, agents may use the disposable local Postgres described in `/home/Gianfranco/repos/rxlink-sv/docs/ai-test-database.md` (container `pgtest`, port 55432, synthetic data only, approved by the owner). Never use any real/remote connection string or the user's own Postgres on 5432.
