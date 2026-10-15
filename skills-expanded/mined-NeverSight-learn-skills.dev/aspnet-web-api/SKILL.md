---
name: aspnet-web-api
description: APIs REST con ASP.NET Core (Controllers y Minimal APIs). Cubre diseño RESTful, Content Negotiation, versioning, HATEOAS, OpenAPI/Swagger, CORS, rate limiting, response caching, API Keys, y buenas prácticas de diseño de APIs HTTP. Actívala al diseñar o implementar APIs HTTP, endpoints REST, o migrar APIs de Controllers a Minimal APIs.
disable-model-invocation: true
---

# ASP.NET Core Web APIs

Guía de APIs REST con ASP.NET Core. Cubre dos enfoques: **Controller-based** y **Minimal APIs**. Para gRPC y SignalR, ver `aspnet-signalr`.

---

## Controller-based vs Minimal APIs

| Criterio | Controllers | Minimal APIs |
|----------|-------------|--------------|
| Verbosidad | Alta (atributos, clase) | Baja |
| Performance | Buena | Mejor (menos overhead) |
| AOT | Parcial | ✅ Nativo |
| OpenAPI | Swashbuckle / NSwag | `Microsoft.AspNetCore.OpenApi` |
| Filters | `IActionFilter` | `IEndpointFilter` |
| Model binding | `[FromBody]`, etc. | `[AsParameters]` |
| Organización | Por controller | Por endpoint file |

**Recomendación**: Minimal APIs para proyectos nuevos .NET 9+. Controllers para equipos que ya los dominan.

---

## Controller-based API

```csharp
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class OrdersController : ControllerBase
{
    private readonly IOrderService _orderService;

    public OrdersController(IOrderService orderService) => _orderService = orderService;

    /// <summary>
    /// Gets all orders with optional filtering
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(PaginatedResponse<OrderDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll(
        [FromQuery] OrderFilter filter,
        CancellationToken ct)
    {
        var orders = await _orderService.GetAllAsync(filter, ct);
        return Ok(orders);
    }

    /// <summary>
    /// Gets an order by ID
    /// </summary>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(OrderDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(Guid id, CancellationToken ct)
    {
        var order = await _orderService.GetByIdAsync(id, ct);
        return order is not null ? Ok(order) : NotFound();
    }

    /// <summary>
    /// Creates a new order
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof(OrderDto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<IActionResult> Create(
        [FromBody] CreateOrderRequest request,
        CancellationToken ct)
    {
        var result = await _orderService.CreateAsync(request, ct);
        return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
    }

    /// <summary>
    /// Cancels an order
    /// </summary>
    [HttpPost("{id:guid}/cancel")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status422UnprocessableEntity)]
    public async Task<IActionResult> Cancel(Guid id, CancellationToken ct)
    {
        await _orderService.CancelAsync(id, ct);
        return NoContent();
    }
}
```

---

## Minimal API Endpoints

### Endpoint como static class

```csharp
// Orders/CreateOrderEndpoint.cs
public static class CreateOrderEndpoint
{
    public record Request(string CustomerId, List<OrderItemDto> Items);
    public record Response(Guid OrderId, string Status, decimal Total);

    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapPost("/api/orders", HandleAsync)
            .WithName("CreateOrder")
            .WithTags("Orders")
            .WithSummary("Creates a new order")
            .WithDescription("Creates an order for the given customer and line items.")
            .Produces<Response>(StatusCodes.Status201Created)
            .ProducesValidationProblem()
            .ProducesProblem(StatusCodes.Status409Conflict)
            .RequireAuthorization("orders:create")
            .AddEndpointFilter<ValidationFilter<Request>>();
    }

    private static async Task<IResult> HandleAsync(
        Request request,
        IOrderService orderService,
        LinkGenerator linker,
        HttpContext httpContext,
        CancellationToken ct)
    {
        var result = await orderService.CreateAsync(request.ToCommand(), ct);

        var location = linker.GetPathByName("GetOrder", new { id = result.OrderId });
        return Results.Created(location, new Response(result.OrderId, result.Status, result.Total));
    }
}

// Orders/GetOrderEndpoint.cs
public static class GetOrderEndpoint
{
    public static void Map(IEndpointRouteBuilder app)
    {
        app.MapGet("/api/orders/{id:guid}", HandleAsync)
            .WithName("GetOrder")
            .WithTags("Orders")
            .WithSummary("Gets an order by ID")
            .Produces<OrderDto>()
            .Produces(StatusCodes.Status404NotFound);
    }

    private static async Task<IResult> HandleAsync(
        Guid id,
        IOrderService orderService,
        CancellationToken ct)
    {
        var order = await orderService.GetByIdAsync(id, ct);
        return order is not null ? Results.Ok(order) : Results.NotFound();
    }
}
```

### Mapeo automático de endpoints

```csharp
// Extensions/EndpointExtensions.cs
public static class EndpointExtensions
{
    public static IEndpointRouteBuilder MapEndpoints(this IEndpointRouteBuilder app)
    {
        var endpointTypes = typeof(Program).Assembly.GetTypes()
            .Where(t => t.IsClass && !t.IsAbstract && t.GetMethod("Map") is not null);

        foreach (var type in endpointTypes)
        {
            type.GetMethod("Map")!.Invoke(null, [app]);
        }

        return app;
    }
}

// Program.cs
app.MapEndpoints();
```

### Endpoint groups (.NET 7+)

```csharp
var orders = app.MapGroup("/api/orders")
    .WithTags("Orders")
    .RequireAuthorization()
    .WithOpenApi();

orders.MapGet("/", GetAll);
orders.MapGet("/{id:guid}", GetById);
orders.MapPost("/", Create).RequireAuthorization("orders:create");
orders.MapPost("/{id:guid}/cancel", Cancel).RequireAuthorization("orders:cancel");
```

---

## Content Negotiation

```csharp
// Por defecto, ASP.NET Core negocia JSON. Agregar XML:
builder.Services.AddControllers()
    .AddXmlSerializerFormatters()
    .AddXmlDataContractSerializerFormatters();

// Respuesta según Accept header:
// GET /api/orders/123  Accept: application/json  → JSON
// GET /api/orders/123  Accept: application/xml   → XML
// GET /api/orders/123  Accept: text/csv          → 406 Not Acceptable

// Custom output formatter (CSV)
public class CsvOutputFormatter : TextOutputFormatter
{
    public CsvOutputFormatter()
    {
        SupportedMediaTypes.Add("text/csv");
        SupportedEncodings.Add(Encoding.UTF8);
    }

    protected override bool CanWriteType(Type? type)
        => typeof(IEnumerable).IsAssignableFrom(type);

    public override async Task WriteResponseBodyAsync(OutputFormatterWriteContext context, Encoding selectedEncoding)
    {
        var response = context.HttpContext.Response;
        // Escribir CSV...
    }
}
```

---

## API Versioning

### URL-based (recomendado para APIs públicas)

```csharp
var v1 = app.MapGroup("/api/v1/orders").WithTags("Orders v1");
v1.MapPost("/", CreateOrderV1);
v1.MapGet("/{id}", GetOrderV1);

var v2 = app.MapGroup("/api/v2/orders").WithTags("Orders v2");
v2.MapPost("/", CreateOrderV2);
v2.MapGet("/{id}", GetOrderV2);
```

### Header-based con Asp.Versioning.Http

```csharp
// NuGet: Asp.Versioning.Http
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = new HeaderApiVersionReader("api-version");
})
.AddMvc()
.AddApiExplorer(options =>
{
    options.GroupNameFormat = "'v'VVV";
    options.SubstituteApiVersionInUrl = true;
});
```

---

## Formato de respuesta estándar

```csharp
// Envoltorio consistente para todas las respuestas
public class ApiResponse<T>
{
    public bool Success { get; init; }
    public T? Data { get; init; }
    public string? Error { get; init; }
    public string? TraceId { get; init; }
    public int StatusCode { get; init; }
}

public class PaginatedResponse<T> : ApiResponse<List<T>>
{
    public int Page { get; init; }
    public int PageSize { get; init; }
    public int Total { get; init; }
    public int TotalPages => (int)Math.Ceiling((double)Total / PageSize);
    public bool HasNext => Page < TotalPages;
    public bool HasPrevious => Page > 1;
}

// Uso
private static IResult Ok<T>(T data) =>
    Results.Ok(new ApiResponse<T>
    {
        Success = true,
        Data = data,
        StatusCode = 200
    });
```

---

## Manejo global de errores

```csharp
public class GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext context,
        Exception exception,
        CancellationToken ct)
    {
        var (statusCode, title, detail) = exception switch
        {
            ValidationException ve => (
                StatusCodes.Status400BadRequest,
                "Validation failed",
                ve.Message),

            NotFoundException nf => (
                StatusCodes.Status404NotFound,
                "Resource not found",
                nf.Message),

            DomainException de => (
                StatusCodes.Status422UnprocessableEntity,
                "Business rule violation",
                de.Message),

            UnauthorizedAccessException => (
                StatusCodes.Status403Forbidden,
                "Access denied",
                exception.Message),

            _ => (
                StatusCodes.Status500InternalServerError,
                "Internal server error",
                "An unexpected error occurred. Please try again later.")
        };

        if (statusCode == StatusCodes.Status500InternalServerError)
            logger.LogError(exception, "Unhandled exception: {Message}", exception.Message);

        var problem = new ProblemDetails
        {
            Status = statusCode,
            Title = title,
            Detail = detail,
            Instance = context.Request.Path,
            Type = $"https://httpstatuses.io/{statusCode}"
        };

        if (exception is ValidationException ve2)
            problem.Extensions["errors"] = ve2.Errors;

        context.Response.StatusCode = statusCode;
        context.Response.ContentType = "application/problem+json";
        await context.Response.WriteAsJsonAsync(problem, ct);

        return true;
    }
}

// Program.cs
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();

var app = builder.Build();
app.UseExceptionHandler(); // Sin opciones, usa IExceptionHandler
app.UseStatusCodePages();  // Para 404, 405, etc.
```

---

## OpenAPI / Swagger

### .NET 10 con Microsoft.AspNetCore.OpenApi (OpenAPI 3.1 + YAML)

```csharp
builder.Services.AddOpenApi();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();                     // GET /openapi/v1.json (JSON)
    app.MapOpenApi("/openapi/v1.yaml");   // GET /openapi/v1.yaml (YAML, .NET 10+)
    // app.MapScalarApiReference();        // UI ligera alternativa a Swagger UI
}

// Documentar endpoint
app.MapGet("/api/orders/{id}", GetOrder)
    .WithOpenApi(operation =>
    {
        operation.Summary = "Gets an order";
        operation.Description = "Returns the full order with items and status";
        operation.Parameters[0].Description = "The order unique identifier";

        operation.Responses[StatusCodes.Status200OK.ToString()] = new OpenApiResponse
        {
            Description = "Order found",
            Content = new Dictionary<string, OpenApiMediaType>
            {
                ["application/json"] = new()
                {
                    Example = new OpenApiString("""
                        {"id":"3fa85f64-5717-4562-b3fc-2c963f66afa6","status":"Pending","total":150.00}
                        """)
                }
            }
        };

        return operation;
    });
```

### Transformadores de documento

```csharp
builder.Services.AddOpenApi(options =>
{
    options.AddDocumentTransformer((document, context, ct) =>
    {
        document.Info.Title = "MiApp API";
        document.Info.Version = "v1";
        document.Info.Description = "API for order management";
        document.Servers.Add(new OpenApiServer { Url = "https://api.miapp.com" });
        return Task.CompletedTask;
    });

    options.AddOperationTransformer((operation, context, ct) =>
    {
        // Agregar header de API Key a todas las operaciones
        operation.Parameters.Add(new OpenApiParameter
        {
            Name = "X-API-Key",
            In = ParameterLocation.Header,
            Required = true,
            Schema = new OpenApiSchema { Type = "string" }
        });
        return Task.CompletedTask;
    });
});
```

---

## Validation

.NET 10 introduce validación nativa para Minimal APIs con `AddValidation()`. Para .NET 9 o reglas cross-field complejas, usar FluentValidation.

### Validación nativa (.NET 10)

```csharp
// ✅ AddValidation() — validación por DataAnnotations sin librerías extra
builder.Services.AddValidation();

app.MapPost("/api/orders", (CreateOrderRequest request) =>
{
    // Si request tiene [Required], [Range], [EmailAddress] y falla → 400 automático
    // Errores como ValidationProblemDetails
})
.AddValidation();

// ⚠️ AddValidation() debe llamarse desde el mismo assembly que define los endpoints.
```

### FluentValidation filter para Minimal API (.NET 9+, reglas complejas)

```csharp
public class ValidationFilter<T> : IEndpointFilter where T : class
{
    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var validator = context.HttpContext.RequestServices
            .GetRequiredService<IValidator<T>>();

        var argument = context.Arguments.OfType<T>().FirstOrDefault();
        if (argument is null)
            return Results.BadRequest(new { error = "Invalid request body" });

        var result = await validator.ValidateAsync(argument);
        if (!result.IsValid)
            return Results.ValidationProblem(result.ToDictionary());

        return await next(context);
    }
}

// Extension method
public static RouteHandlerBuilder Validate<T>(this RouteHandlerBuilder builder) where T : class
{
    builder.AddEndpointFilter<ValidationFilter<T>>();
    return builder;
}
```

### Validación en Controllers

```csharp
// [ApiController] ya valida ModelState automáticamente.
// Para customización:
builder.Services.Configure<ApiBehaviorOptions>(options =>
{
    options.InvalidModelStateResponseFactory = context =>
    {
        var problem = new ValidationProblemDetails(context.ModelState)
        {
            Instance = context.HttpContext.Request.Path,
            Status = StatusCodes.Status422UnprocessableEntity,
            Detail = "Please refer to the errors property for additional details"
        };

        return new UnprocessableEntityObjectResult(problem);
    };
});
```

---

## CORS en APIs

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("ApiCors", policy =>
    {
        policy.WithOrigins("https://miapp.com", "https://admin.miapp.com")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();

        if (builder.Environment.IsDevelopment())
            policy.WithOrigins("http://localhost:5173");
    });
});

app.UseCors("ApiCors"); // Antes de UseAuthentication y MapControllers/MapEndpoints
```

---

## Rate Limiting

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("api", config =>
    {
        config.PermitLimit = 100;
        config.Window = TimeSpan.FromMinutes(1);
        config.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        config.QueueLimit = 10;
    });

    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
});

app.UseRateLimiter();

// Endpoint con rate limit
app.MapPost("/api/orders", CreateOrder)
    .RequireRateLimiting("api");
```

---

## Response Caching

```csharp
// Cache en memoria para endpoints de lectura
app.MapGet("/api/products", GetAll)
    .CacheOutput(policy => policy
        .Expire(TimeSpan.FromMinutes(5))
        .SetVaryByQuery("category"));

// Cache con Redis en prod
builder.Services.AddStackExchangeRedisOutputCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
});
```

---

## HATEOAS (Hypermedia)

```csharp
public record OrderDto
{
    public required Guid Id { get; init; }
    public required string Status { get; init; }
    public required decimal Total { get; init; }
    public List<Link> Links { get; init; } = [];
}

public record Link(string Rel, string Href, string Method, string? Type = null);

// Generar links en el endpoint
private static OrderDto EnrichWithLinks(OrderDto dto, HttpContext context, LinkGenerator linker)
{
    dto.Links.AddRange([
        new("self", linker.GetPathByName("GetOrder", new { id = dto.Id })!, "GET"),
        new("cancel", linker.GetPathByName("CancelOrder", new { id = dto.Id })!, "POST")
    ]);

    if (dto.Status == "Confirmed")
        dto.Links.Add(new("ship", linker.GetPathByName("ShipOrder", new { id = dto.Id })!, "POST"));

    return dto;
}
```

**⚠️ HATEOAS solo si el cliente lo consume (API pública explorable). Para APIs internas con contrato conocido: YAGNI.**

---

## Paginación, filtrado y ordenamiento

```csharp
// Request tipado
public record OrderListRequest(
    OrderStatus? Status = null,
    string? CustomerId = null,
    DateTime? From = null,
    DateTime? To = null,
    string? SortBy = "createdAt",
    SortDirection SortDirection = SortDirection.Desc,
    int Page = 1,
    int PageSize = 20);

public enum SortDirection { Asc, Desc }

// Endpoint
app.MapGet("/api/orders", async (
    [AsParameters] OrderListRequest request,
    IOrderService service,
    CancellationToken ct) =>
{
    var result = await service.GetFilteredAsync(request, ct);
    return Results.Ok(result);
});
```

---

## API Keys para servicios internos

```csharp
public class ApiKeyAuthenticationHandler(
    IOptionsMonitor<ApiKeyOptions> options,
    ILoggerFactory logger,
    UrlEncoder encoder) : AuthenticationHandler<ApiKeyOptions>(options, logger, encoder)
{
    public const string SchemeName = "ApiKey";
    private const string HeaderName = "X-API-Key";

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        if (!Request.Headers.TryGetValue(HeaderName, out var apiKey))
            return Task.FromResult(AuthenticateResult.NoResult());

        var configuredKey = OptionsMonitor.CurrentValue.ApiKey;
        if (!CryptographicOperations.FixedTimeEquals(
                Encoding.UTF8.GetBytes(apiKey!),
                Encoding.UTF8.GetBytes(configuredKey)))
        {
            return Task.FromResult(AuthenticateResult.Fail("Invalid API Key"));
        }

        var claims = new[] { new Claim(ClaimTypes.Name, "API Service") };
        var identity = new ClaimsIdentity(claims, SchemeName);
        return Task.FromResult(
            AuthenticateResult.Success(new AuthenticationTicket(
                new ClaimsPrincipal(identity), SchemeName)));
    }
}

// Program.cs
builder.Services.AddAuthentication()
    .AddScheme<ApiKeyOptions, ApiKeyAuthenticationHandler>("ApiKey", null);

builder.Services.AddAuthorization();
```

---

## File Upload / Download

```csharp
// Upload
app.MapPost("/api/files/upload", async (
    IFormFile file,
    IWebHostEnvironment env,
    CancellationToken ct) =>
{
    if (file.Length == 0)
        return Results.BadRequest("Empty file");
    if (file.Length > 10 * 1024 * 1024)
        return Results.BadRequest("File too large (max 10MB)");

    var path = Path.Combine(env.ContentRootPath, "Uploads", file.FileName);
    await using var stream = File.Create(path);
    await file.CopyToAsync(stream, ct);

    return Results.Ok(new { file.FileName, file.Length, path });
})
.DisableAntiforgery(); // Solo si es API sin CSRF

// Download
app.MapGet("/api/files/download/{filename}", (string filename) =>
{
    var path = Path.Combine("Uploads", filename);
    if (!File.Exists(path))
        return Results.NotFound();

    var stream = File.OpenRead(path);
    return Results.File(stream, "application/octet-stream", filename);
});
```

---

## Buenas prácticas REST

### URLs

```
✅ GET    /api/orders
✅ GET    /api/orders/{id}
✅ POST   /api/orders
✅ PUT    /api/orders/{id}
✅ PATCH  /api/orders/{id}
✅ DELETE /api/orders/{id}
✅ POST   /api/orders/{id}/cancel       ← acción (verbo)

❌ GET    /api/GetOrders                 ← verbo en URL
❌ POST   /api/orders/create             ← verbo redundante
❌ GET    /api/orders?id=123             ← ID en query string
```

### Status codes

| Código | Cuándo |
|--------|--------|
| 200 OK | GET exitoso |
| 201 Created | POST que crea recurso |
| 204 No Content | DELETE exitoso, POST sin body |
| 400 Bad Request | Input inválido |
| 401 Unauthorized | Sin token / token inválido |
| 403 Forbidden | Token válido pero sin permisos |
| 404 Not Found | Recurso no existe |
| 409 Conflict | Violación de integridad (duplicado) |
| 422 Unprocessable | Regla de negocio violada |
| 429 Too Many Requests | Rate limit excedido |
| 500 Internal Server | Error inesperado |

---

## Checklist de Web API

- [ ] URLs siguen convención REST (recurso, no verbo)
- [ ] Endpoints documentados con `.WithOpenApi()` o XML comments
- [ ] Manejo global de errores con `IExceptionHandler` + `ProblemDetails`
- [ ] Validación con FluentValidation + endpoint filter
- [ ] Paginación, filtrado, ordenamiento en endpoints de lista
- [ ] CORS con orígenes explícitos
- [ ] Rate limiting en endpoints sensibles
- [ ] Response caching en endpoints de solo lectura
- [ ] API versioning definido (URL o header)
- [ ] API Keys comparadas con `FixedTimeEquals`
- [ ] HTTPS forzado
- [ ] Health checks en `/health`
- [ ] CancellationToken propagado a todas las operaciones async
- [ ] OpenAPI solo en development
- [ ] Sin stack traces en producción
