---
name: backend-stack-dotnet
description: "A .NET backend with ASP.NET Core 8 or 9: minimal APIs or controllers, dependency injection and the options pattern, validation, EF Core with migrations and no N+1, transactions, ProblemDetails errors, authentication and authorisation policies, logging with ILogger or Serilog, health checks, OpenTelemetry, and tests with xUnit, WebApplicationFactory and Testcontainers. Read when the project is an ASP.NET Core backend."
---

# .NET with ASP.NET Core

The generated ASP.NET Core API binds the EF entity from the body and returns
it, calls `.Result` on async methods, injects a scoped `DbContext` into a
singleton, catches every `Exception` to answer `200` with the message, and
reads `Configuration["Stripe:Key"]` wherever it needs it.
The backend rules are in the `backend` skill; these are ASP.NET Core's own.

## 1. Setup

- Keep the project's target framework. .NET 8 (LTS) and .NET 9 are both
  supported until November 2026; .NET 10 (LTS, November 2025) is the one to
  start on or plan the move to. The SDK pinned in `global.json`.
- `Directory.Build.props` sets `Nullable` and `TreatWarningsAsErrors` on and
  `AnalysisLevel` to `latest-recommended`; versions in `Directory.Packages.props`.
- A small service is one API project with feature folders (`Orders/` with
  endpoints, service and DTOs; `Data/` with the `DbContext` and migrations)
  and a test project; split into Api, Application and Infrastructure only
  when it grows. Not four projects and a mediator for ten endpoints.

## 2. Endpoints

Minimal APIs with route groups and typed results for new services;
controllers where the project has them (both run on the same pipeline).

```csharp
public static class OrderEndpoints
{
    public static RouteGroupBuilder MapOrders(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders").RequireAuthorization();
        group.MapGet("/{id:long}", GetOrder);
        group.MapPost("/", PlaceOrder);
        return group;
    }

    static async Task<Results<Ok<OrderResponse>, NotFound>> GetOrder(
        long id, OrderService orders, ClaimsPrincipal user, CancellationToken ct)
    {
        var order = await orders.FindForCustomer(id, user.CustomerId(), ct);
        if (order is null) return TypedResults.NotFound();
        return TypedResults.Ok(order);
    }
}
```

- `TypedResults` and `Results<...>` also describe the responses in the
  OpenAPI document (`AddOpenApi()` and `MapOpenApi()` in .NET 9+).
- DTOs are records. Entities never bind from a body (over-posting) and never
  go out in a response (leaks, cycles, lazy loads).
- `CancellationToken` last in every handler and passed to EF Core and
  `HttpClient`; `async` all the way, never `.Result`, `.Wait()` or
  `async void`.
- Kestrel's `MaxRequestBodySize` is about 30 MB by default: lower it, and
  raise it per endpoint that needs more. `AddRequestTimeouts` and
  `AddRateLimiter` are built in.

## 3. Dependency injection and options

- Lifetimes: singleton (thread-safe: clients, caches), scoped (per request:
  the `DbContext`, the current user), transient (light, stateless). A
  singleton holding a scoped service keeps one instance forever (a captive
  dependency), and a `DbContext` shared between threads corrupts.
  `ValidateScopes` and `ValidateOnBuild` catch it; both are on in
  Development, which is also how `WebApplicationFactory` runs.
- A `BackgroundService` is a singleton: it opens a scope per unit of work
  (`IServiceScopeFactory.CreateAsyncScope()`) and honours `stoppingToken`.
- Options bound and validated at start, the class carrying `[Required]`,
  `[Url]` and `[Range]` on its properties:

```csharp
builder.Services.AddOptions<PaymentsOptions>()
    .Bind(builder.Configuration.GetSection("Payments"))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

- `IOptions<T>` for values fixed at start, `IOptionsMonitor<T>` for values
  that change while running; no `IConfiguration["..."]` in services.
- Secrets: `dotnet user-secrets` in development; environment variables in
  production with `__` between sections (`Payments__ApiKey`), or the
  platform's vault; never `appsettings.json`.

## 4. Validation

- Controllers with `[ApiController]` answer invalid DataAnnotations models
  with a `400` `ValidationProblemDetails` by themselves.
- Minimal APIs: .NET 10 validates DataAnnotations on parameters after
  `builder.Services.AddValidation()`. On 8 and 9, call FluentValidation from
  an endpoint filter or the handler and answer
  `TypedResults.ValidationProblem(result.ToDictionary())`; its old automatic
  MVC integration is deprecated.
- Unknown JSON members are ignored by default; refuse them (`backend-api`)
  with `JsonUnmappedMemberHandling.Disallow` (.NET 8+) set as
  `UnmappedMemberHandling` in `ConfigureHttpJsonOptions`.

## 5. EF Core

- One `DbContext`, scoped per request (`AddDbContext`, or `AddDbContextPool`
  for hot services), Npgsql (`UseNpgsql`) or the project's provider; lazy
  loading proxies off.
- Reads: `AsNoTracking()` and a projection to the DTO in the query, which
  loads only the needed columns and no N+1:

```csharp
var page = await db.Orders.AsNoTracking()
    .Where(o => o.CustomerId == customerId)
    .OrderByDescending(o => o.CreatedAt).ThenByDescending(o => o.Id)
    .Take(25)
    .Select(o => new OrderSummary(o.Id, o.Status, o.Total, o.Items.Count))
    .ToListAsync(ct);
```

- `Include` only when loading entities to change them; several collection
  `Include`s multiply rows, so add `AsSplitQuery()`.
- Race-free updates without loading, the rows affected returned:

```csharp
var reserved = await db.Products
    .Where(p => p.Id == productId && p.Stock >= qty)
    .ExecuteUpdateAsync(s => s.SetProperty(p => p.Stock, p => p.Stock - qty), ct);
if (reserved == 0) throw new ConflictException("out_of_stock");
```

- Concurrency tokens on records two people edit (`[Timestamp]` row version
  on SQL Server, Npgsql's `xmin` through a `[Timestamp] uint Version`);
  `DbUpdateConcurrencyException` becomes a `409`.
- One `SaveChangesAsync` is already a transaction. Several steps go in
  `BeginTransactionAsync(ct)` and `CommitAsync(ct)`; with
  `EnableRetryOnFailure`, that transaction runs inside
  `db.Database.CreateExecutionStrategy().ExecuteAsync(...)` or EF throws.
- Migrations: `dotnet ef migrations add AddOrderStatus`, read before
  committing, applied as a release step with
  `dotnet ef migrations script --idempotent` or a bundle
  (`dotnet ef migrations bundle`), never `Database.Migrate()` at every start.
- Money as `decimal` with `HasPrecision(18, 2)` or a `long` in minor units;
  times as `DateTimeOffset` or UTC `DateTime` (Npgsql refuses other kinds
  for `timestamptz`). Dapper beside EF for reporting SQL.

## 6. Errors as ProblemDetails

`AddProblemDetails()` and `AddExceptionHandler<DomainExceptionHandler>()`,
then `app.UseExceptionHandler()` and `app.UseStatusCodePages()`:

```csharp
sealed class DomainExceptionHandler(IProblemDetailsService problems) : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(HttpContext ctx, Exception ex, CancellationToken ct)
    {
        var (status, code) = ex switch
        {
            NotFoundException => (StatusCodes.Status404NotFound, "not_found"),
            ConflictException c => (StatusCodes.Status409Conflict, c.Code),
            DbUpdateConcurrencyException => (StatusCodes.Status409Conflict, "stale_version"),
            _ => (0, ""),
        };
        if (status == 0) return false; // the generic 500
        ctx.Response.StatusCode = status;
        return await problems.TryWriteAsync(new ProblemDetailsContext
        {
            HttpContext = ctx,
            ProblemDetails = new ProblemDetails { Status = status, Extensions = { ["code"] = code } },
        });
    }
}
```

- Every error, `404`s for unknown routes included, gets the RFC 9457 shape
  with a `traceId`; codes follow `backend-errors`.
- Unhandled exceptions become a `500` problem with no details outside
  Development, logged once by the middleware.

## 7. Authentication and authorisation

- JWT bearer (`AddJwtBearer` with `Authority` and `Audience`), or cookies
  for a same-site browser app (`AddCookie`, or Identity with
  `MapIdentityApi`); never hand-rolled token parsing (`backend-auth`).
- Policies named for actions, and a fallback that closes every endpoint
  without an explicit rule (public ones say `.AllowAnonymous()`):

```csharp
builder.Services.AddAuthorizationBuilder()
    .SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build())
    .AddPolicy("orders.refund", p => p.RequireClaim("scope", "orders.refund"));
```

- Some providers send every scope in one space-separated `scope` claim,
  which `RequireClaim` never matches: check how yours arrive first.
- Ownership in the query (`Where(o => o.CustomerId == me)`), or
  `IAuthorizationService.AuthorizeAsync(user, order, requirement)` with an
  `AuthorizationHandler<TRequirement, Order>`; another user's id is a `404`.

## 8. Outbound HTTP

```csharp
builder.Services.AddHttpClient<PaymentsClient>((sp, c) =>
    c.BaseAddress = new Uri(sp.GetRequiredService<IOptions<PaymentsOptions>>().Value.BaseUrl))
    .AddStandardResilienceHandler(o => o.Retry.DisableForUnsafeHttpMethods());
```

- `IHttpClientFactory` with typed clients, never `new HttpClient()` per call
  (sockets run out) or one static client forever (DNS changes missed);
  typed clients are transient, never captured in a singleton.
- `AddStandardResilienceHandler` (Microsoft.Extensions.Http.Resilience, on
  Polly 8): a 30 s total timeout, 10 s per attempt, 3 retries with backoff
  and jitter, a circuit breaker. It retries every method by default: keep
  unsafe ones out, as above, unless the provider takes an idempotency key.

## 9. Logging, health and telemetry

- `ILogger<T>` with message templates, never interpolation:
  `logger.LogInformation("Order {OrderId} paid", id)` keeps `OrderId` a
  field. `[LoggerMessage]` source-generated methods on hot paths.
- JSON logs with `builder.Logging.AddJsonConsole()`, or Serilog
  (`builder.Services.AddSerilog(...)` from settings, and
  `app.UseSerilogRequestLogging()` for one line per request).
- Health: `AddHealthChecks().AddDbContextCheck<AppDbContext>(tags: ["ready"])`
  (from `Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore`);
  `/healthz` mapped with `Predicate = _ => false` (the process only),
  `/readyz` with `Predicate = c => c.Tags.Contains("ready")`.
- OpenTelemetry: `AddOpenTelemetry()` with `ConfigureResource`,
  `WithTracing` (ASP.NET Core and `HttpClient` instrumentation),
  `WithMetrics`, and `UseOtlpExporter()` reading
  `OTEL_EXPORTER_OTLP_ENDPOINT`; Aspire's service defaults do the same.
- Shutdown waits `HostOptions.ShutdownTimeout` (30 s by default since .NET
  8) for requests and hosted services.

## 10. Tests

- xUnit and `WebApplicationFactory<Program>` for the whole pipeline (add
  `public partial class Program { }` to `Program.cs`), Postgres from
  Testcontainers:

```csharp
public sealed class ApiFactory : WebApplicationFactory<Program>, IAsyncLifetime
{
    private readonly PostgreSqlContainer _db =
        new PostgreSqlBuilder().WithImage("postgres:17-alpine").Build();

    protected override void ConfigureWebHost(IWebHostBuilder builder) =>
        builder.UseSetting("ConnectionStrings:Default", _db.GetConnectionString());

    public Task InitializeAsync() => _db.StartAsync();
    public new Task DisposeAsync() => _db.DisposeAsync().AsTask();
}
```

  These are xUnit v2 signatures; v3's `IAsyncLifetime` uses `ValueTask`.
- Respawn resets data between tests (`Respawner.CreateAsync` with
  `DbAdapter.Postgres`, then `ResetAsync`); never the in-memory provider or
  SQLite standing in for Postgres.
- `ConfigureTestServices` swaps outbound clients for fakes (or WireMock.Net),
  `TimeProvider` for `FakeTimeProvider`; a test auth handler signs in as a
  given user, and a test per rule proves another user's order is a `404`.

## Check it

`dotnet build` (warnings as errors), `dotnet format --verify-no-changes`,
`dotnet test`; `dotnet ef migrations script --idempotent` shows what will
run. `dotnet run --project src/Shop.Api`, then `curl`: a bad body gives a
`400` problem with every field, another user's id a `404`, `/readyz`
answers. With `Microsoft.EntityFrameworkCore.Database.Command` logged at
`Information` in a test, a list request runs one query, not one per row.

## Avoid

Entities bound from bodies or returned; `.Result`, `.Wait()`, `async void`;
a scoped `DbContext` in a singleton or a background loop without a scope;
`new HttpClient()` per call; `IConfiguration["..."]` in services;
unvalidated options; `Database.Migrate()` racing on every instance;
`Include` chains for read-only lists; `SaveChanges` in a loop; exceptions
turned into `200`; interpolated log templates; secrets in
`appsettings.json`; the in-memory provider in tests of a Postgres app.
