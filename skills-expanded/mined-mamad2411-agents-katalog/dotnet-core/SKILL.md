---
name: dotnet-core
description: "Guía principal de desarrollo .NET (C#, .NET 9/10). Cubre convenciones de código, features modernas de C# 12-14, sistema de proyectos, hosting, DI, configuración, middleware, logging, serialización y herramientas del ecosistema. Actívala para cualquier tarea .NET: nuevas features, revisión de código, arquitectura, migraciones o debugging. Las sub-skills del kit profundizan en dominios específicos."
---

# .NET Core Development Guide

Guía canónica para desarrollo .NET. Cubre .NET 9 (STS, soporte hasta Nov 2026) y .NET 10 (LTS, hasta Nov 2028). Todo código generado sigue estas reglas salvo indicación contraria explícita del usuario.

## Versiones y targets

| Versión   | Tipo | Lanzamiento      | Fin de soporte   |
|-----------|------|------------------|------------------|
| .NET 8    | LTS  | Nov 2023         | Nov 2026         |
| .NET 9    | STS  | Nov 2024         | Nov 2026         |
| .NET 10   | LTS  | Nov 2025         | Nov 2028         |

- **Proyectos nuevos** → .NET 10 (LTS). Solo usar .NET 9 si hay dependencia bloqueante.
- **Migraciones** → Priorizar .NET 10. Saltar .NET 8 → .NET 10 directamente.
- **C# 14** en .NET 10; **C# 13** en .NET 9. Ajustar `<LangVersion>` solo si se requiere compatibilidad.

---

## Features modernas de C# (12 → 14)

### Tabla de adopción

| Feature                          | C#   | .NET | Usar  | Notas |
|----------------------------------|------|------|-------|-------|
| Primary constructors             | 12   | 8    | ✅    | Ideal para DTOs, commands, queries |
| Collection expressions           | 12   | 8    | ✅    | `[1, 2, 3]` sobre `new List<int> { 1, 2, 3 }` |
| `ref readonly` params            | 12   | 8    | ⬜    | Solo en código de alto rendimiento |
| Default lambda parameters        | 12   | 8    | ✅    | `(int x = 0) => x + 1` |
| Inline arrays                    | 12   | 8    | ⬜    | Rendimiento extremo |
| `params` collections             | 13   | 9    | ✅    | `params Span<T>`, `params List<T>` |
| `field` keyword (semi-auto)      | 13-14| 9-10 | ✅    | Lógica simple en properties sin backing field manual |
| `\e` escape                      | 13   | 9    | ✅    | `\e` = `\u001b` (ESC) |
| `ref struct` in generics         | 13   | 9    | ⬜    | Anti-constraint, solo alto rendimiento |
| **Extension members**            | 14   | 10   | ✅    | **Headline C# 14**: propiedades, operadores y estáticos en tipos existentes |
| Null-conditional assignment      | 14   | 10   | ✅    | `obj?.Prop = valor`, `list?[i] = x` en lado izquierdo |
| `partial` properties/indexers    | 14   | 10   | ✅    | Source generators |
| `Span<T>` unification            | 14   | 10   | ✅    | `Span` sobre `string` implícito |
| Implicit span conversions        | 14   | 10   | ✅    | |
| `params Span<T>`                 | 14   | 10   | ✅    | Sin allocaciones |
| `field` keyword estable          | 14   | 10   | ✅    | |
| `nameof` en unbound generics     | 14   | 10   | ✅    | `nameof(List<>)` ahora compila |

### Ejemplos prácticos

```csharp
// ✅ Primary constructors para inyectar dependencias y DTOs
public class CreateOrderHandler(
    IOrderRepository repository,
    IUnitOfWork unitOfWork,
    ILogger<CreateOrderHandler> logger) : IRequestHandler<CreateOrderCommand, OrderDto>
{
    public async Task<OrderDto> Handle(CreateOrderCommand command, CancellationToken ct)
    {
        logger.LogInformation("Creating order for customer {CustomerId}", command.CustomerId);
        // repository y unitOfWork disponibles sin campos manuales
    }
}

// ✅ Extension members (C# 14) — propiedades y operadores en tipos existentes
public static implicit extension OrderExtensions for Order
{
    public bool IsHighValue => Total.Amount > 1000;
    public static Order CreateFromTemplate(OrderTemplate template) => /* ... */;
}

// ✅ Null-conditional assignment (C# 14)
customer?.Address = newAddress; // Asigna solo si customer no es null
orders?[i] = updatedOrder;     // Asigna solo si orders no es null

// ✅ Collection expressions everywhere
int[] primes = [2, 3, 5, 7, 11];
List<string> names = ["Alice", "Bob"];
Span<int> span = [1, 2, 3];

// ✅ field keyword para validación simple
public class CreateOrderCommand
{
    public string CustomerId { get; set => field = value?.Trim()
        ?? throw new ArgumentNullException(nameof(value)); }

    public int Quantity { get; set => field = value > 0
        ? value : throw new ArgumentException("Must be positive"); }
}

// ✅ partial properties (C# 14) — source generators
public partial class ConfigModel
{
    public partial string ConnectionString { get; set; }
    // El generator produce la implementación con lógica de decrypt, etc.
}
```

---

## Sistema de proyectos (.csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">  <!-- o .Sdk para classlib -->

  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <GenerateDocumentationFile>true</GenerateDocumentationFile> <!-- APIs públicas -->
  </PropertyGroup>

</Project>
```

### Configuraciones clave

| Setting | Recomendación | Motivo |
|---------|---------------|--------|
| `Nullable` | `enable` | Obligatorio |
| `ImplicitUsings` | `enable` | Menos boilerplate |
| `AnalysisLevel` | `latest-recommended` | Mejores warnings |
| `EnforceCodeStyleInBuild` | `true` | Estilo como error de build |
| `GenerateDocumentationFile` | `true` (APIs) | Swagger/IntelliSense |
| `TreatWarningsAsErrors` | `true` (CI) | Build roto = no merge |

---

## Hosting y Startup (.NET 9+)

```csharp
// ✅ Minimal hosting — el estándar moderno
var builder = WebApplication.CreateBuilder(args);

// Configuración tipada con validación
builder.Services
    .AddOptions<StripeOptions>()
    .Bind(builder.Configuration.GetSection("Stripe"))
    .ValidateDataAnnotations()
    .ValidateOnStart(); // Falla temprano si la config es inválida

// Keyed DI (.NET 8+)
builder.Services.AddKeyedScoped<IPaymentService, StripePaymentService>("stripe");
builder.Services.AddKeyedScoped<IPaymentService, PayPalPaymentService>("paypal");

// OpenAPI integrada (.NET 9+ blueprint, .NET 10 full)
builder.Services.AddOpenApi();

// Resilience pipeline (Microsoft.Extensions.Resilience)
builder.Services.AddResiliencePipeline("default", pipeline =>
{
    pipeline.AddRetry(new RetryStrategyOptions { MaxRetryAttempts = 3 });
    pipeline.AddTimeout(TimeSpan.FromSeconds(10));
    pipeline.AddCircuitBreaker(new CircuitBreakerStrategyOptions
    {
        FailureRatio = 0.5,
        MinimumThroughput = 10,
        BreakDuration = TimeSpan.FromSeconds(30)
    });
});

// HybridCache (.NET 9+)
builder.Services.AddHybridCache(options =>
{
    options.MaximumPayloadBytes = 1024 * 1024; // 1 MB
});

var app = builder.Build();

// Middleware pipeline
app.UseExceptionHandler();
app.UseStatusCodePages();
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi(); // /openapi/v1.json
}
app.UseAuthentication();
app.UseAuthorization();
app.MapEndpoints();  // Extension method propio
app.Run();
```

---

## Inyección de dependencias

### Lifetimes

| Lifetime     | Cuándo usarlo |
|-------------|---------------|
| `Transient` | Servicios livianos sin estado. Default para la mayoría. |
| `Scoped`    | Por request (DbContext, UnitOfWork). **Siempre en web apps.** |
| `Singleton` | Estado compartido thread-safe. Cache en memoria, config. Cuidado con dependencias scoped. |

### Keyed services (.NET 8+)

```csharp
// Registro
services.AddKeyedScoped<IPaymentProcessor, StripeProcessor>("stripe");
services.AddKeyedScoped<IPaymentProcessor, MercadoPagoProcessor>("mercadopago");

// Consumo
class CheckoutService(
    [FromKeyedServices("stripe")] IPaymentProcessor paymentProcessor)
{
}
```

### Anti-patrones DI

- ❌ Service Locator (`IServiceProvider` salvo en factories/infrastructure)
- ❌ `new DbContext()` fuera de tests
- ❌ Singleton que depende de Scoped
- ❌ Inyectar IConfiguration directamente — usar `IOptions<T>`

---

## Configuración

```csharp
// ✅ Tipada + validada
public class StripeOptions
{
    public const string SectionName = "Stripe";

    [Required]
    public string ApiKey { get; set; } = string.Empty;

    [Range(1, 1000)]
    public int MaxRetries { get; set; } = 3;
}

// Registro con validación temprana
services.AddOptions<StripeOptions>()
    .Bind(configuration.GetSection(StripeOptions.SectionName))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

### Proveedores de configuración

Por defecto en orden: `appsettings.json` → `appsettings.{Env}.json` → User Secrets (dev) → Env vars → CLI args.

```csharp
// Agregar Azure Key Vault
builder.Configuration.AddAzureKeyVault(
    new Uri("https://myvault.vault.azure.net/"),
    new DefaultAzureCredential());
```

---

## Logging estructurado

```csharp
// ✅ Templates estructurados — nunca interpolación
logger.LogInformation("Order {OrderId} created for customer {CustomerId} with total {Total:C}",
    order.Id, order.CustomerId, order.Total);

// ❌ Interpolación — pierde estructura
logger.LogInformation($"Order {order.Id} créated"); // No

// ✅ Scopes para contexto
using var scope = logger.BeginScope(new { OrderId = order.Id, CorrelationId });
logger.LogInformation("Processing payment...");

// ✅ Source-generated logging (.NET 6+)
[LoggerMessage(Level = LogLevel.Warning, Message = "Payment failed for order {orderId}")]
public static partial void LogPaymentFailed(ILogger logger, string orderId, Exception ex);
```

---

## Minimal APIs: validación nativa (.NET 10)

```csharp
// ✅ AddValidation() — validación nativa por DataAnnotations sin FluentValidation
builder.Services.AddValidation();

// Endpoint con validación automática
app.MapPost("/api/orders", (CreateOrderRequest request) =>
{
    // Si request falla validación → 400 ValidationProblemDetails automático
    // DataAnnotations como [Required], [Range], [EmailAddress] se evalúan nativamente
})
.AddValidation(); // Habilita validación en este endpoint

// ⚠️ AddValidation() debe llamarse desde el mismo assembly que define los endpoints.
// Para reglas cross-field complejas, FluentValidation sigue siendo la opción.
```

## JSON Serialization

### System.Text.Json (default desde .NET 6)

```csharp
// Config global en Program.cs
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter());
    options.SerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull;
});

// Source-generated serializers (.NET 9+)
[JsonSerializable(typeof(List<OrderDto>))]
[JsonSerializable(typeof(OrderDto))]
internal partial class AppJsonContext : JsonSerializerContext
{
}
// Registro: .AddSingleton(AppJsonContext.Default)
// Uso: JsonSerializer.Serialize(order, AppJsonContext.Default.OrderDto)
// Beneficio: AOT-safe, más rápido, sin reflection.
```

### Newtonsoft.Json → solo para compatibilidad legacy

Si el proyecto usa Newtonsoft: migrar a System.Text.Json salvo que uses features no soportadas (polimorfismo complejo, `JToken` dinámico, converters custom complejos).

---

## Middleware y pipeline HTTP

### Middleware custom mínimo

```csharp
public class CorrelationIdMiddleware(RequestDelegate next)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var correlationId = context.Request.Headers["X-Correlation-Id"].FirstOrDefault()
            ?? Guid.NewGuid().ToString("N");

        context.TraceIdentifier = correlationId;
        context.Response.Headers["X-Correlation-Id"] = correlationId;

        using var scope = logger.BeginScope(new { CorrelationId = correlationId });
        await next(context);
    }
}

// Extensión para pipeline limpio
public static class CorrelationIdMiddlewareExtensions
{
    public static IApplicationBuilder UseCorrelationId(this IApplicationBuilder builder)
        => builder.UseMiddleware<CorrelationIdMiddleware>();
}
```

---

## Background services y tareas programadas

```csharp
// ✅ BackgroundService para tareas recurrentes
public class OrderExpirationService(
    IServiceScopeFactory scopeFactory,
    ILogger<OrderExpirationService> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);

            using var scope = scopeFactory.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

            var expired = await db.Orders
                .Where(o => o.Status == OrderStatus.Pending && o.CreatedAt < DateTime.UtcNow.AddHours(-24))
                .ExecuteUpdateAsync(
                    s => s.SetProperty(o => o.Status, OrderStatus.Expired),
                    stoppingToken);

            logger.LogInformation("Expired {Count} orders", expired);
        }
    }
}

// ✅ PeriodicTimer para intervalos precisos (.NET 6+)
var timer = new PeriodicTimer(TimeSpan.FromMinutes(5));
while (await timer.WaitForNextTickAsync(stoppingToken))
{
    // Más preciso que Task.Delay, no acumula drift
}
```

---

## NativeAOT

.NET 10 mejora NativeAOT significativamente. Consideraciones:

- **Sí**: APIs, workers, CLI tools, servicios con baja latencia de arranque
- **No**: Applications con reflection pesada, `Assembly.Load` dinámico, plugins
- `dotnet publish -p:PublishAot=true`
- Usar source-generated JSON y source-generated logging
- Sin `MakeGenericType`, `MakeGenericMethod` salvo en rd.xml

---

## OpenAPI en .NET 10 (OpenAPI 3.1 + YAML)

```csharp
// Soporte nativo OpenAPI 3.1 y exportación YAML (.NET 10)
builder.Services.AddOpenApi(); // Documento compatible con OpenAPI 3.1

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();                    // GET /openapi/v1.json (JSON)
    app.MapOpenApi("/openapi/v1.yaml"); // GET /openapi/v1.yaml (YAML)
}
```

## Rate Limiting (.NET 7+)

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

    // Por IP
    options.AddPolicy("per-ip", context =>
        RateLimitPartition.GetFixedWindowLimiter(
            context.Connection.RemoteIpAddress?.ToString() ?? "unknown",
            _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 50,
                Window = TimeSpan.FromMinutes(1)
            }));
});

app.UseRateLimiter();

// Endpoint específico
app.MapGet("/api/orders", async (...) => { ... })
   .RequireRateLimiting("api");
```

---

## Convenciones de código

### Naming

| Elemento              | Convención       | Ejemplo                        |
|-----------------------|------------------|--------------------------------|
| Clases, records, structs | PascalCase    | `OrderService`                 |
| Interfaces            | IPascalCase      | `IOrderRepository`             |
| Métodos               | PascalCase       | `CalculateTotalAsync()`        |
| Propiedades           | PascalCase       | `CustomerName`                 |
| Campos privados       | _camelCase       | `_orderRepository`             |
| Variables locales     | camelCase        | `orderTotal`                   |
| Parámetros            | camelCase        | `customerId`                   |
| Constantes            | PascalCase       | `MaxRetryCount`                |
| Métodos async         | Sufijo `Async`   | `GetOrderAsync()`              |
| Records posicionales  | PascalCase       | `OrderDto(int Id, string Name)` |

### Organización de archivos

- Un tipo público por archivo. Nombre = nombre del tipo.
- File-scoped namespaces (`namespace MiApp.Orders;`).
- `global using`s en archivo dedicado `GlobalUsings.cs` del proyecto.
- Orden dentro de una clase: fields → constructor → public methods → private methods.

### Nullable y null-handling

```csharp
// ✅ required + init para DTOs inmutables
public class CreateOrderRequest
{
    public required string CustomerId { get; init; }
    public required string ProductSku { get; init; }
    public int Quantity { get; init; } = 1;
}

// ✅ Guard clauses al inicio
public void Process(Order order)
{
    ArgumentNullException.ThrowIfNull(order);
    if (order.Items.Count == 0)
        throw new ArgumentException("Order must have items", nameof(order));
    // ...
}

// ✅ Null-coalescing para defaults
var discount = order.Discount ?? 0m;
var name = customer.Name ?? "Unknown";
```

---

## Estructura de proyecto (Clean Architecture / Vertical Slices)

```
src/
├── MiApp.Api/                  # ASP.NET Core host, endpoints, middleware
│   ├── Endpoints/
│   │   └── Orders/
│   │       ├── CreateOrder.cs      # Mapea ruta + handler en un archivo
│   │       └── GetOrderById.cs
│   ├── Middleware/
│   ├── appsettings.json
│   └── Program.cs
├── MiApp.Application/          # Casos de uso, DTOs, validadores, interfaces
│   └── Orders/
│       ├── CreateOrder/
│       │   ├── CreateOrderCommand.cs
│       │   ├── CreateOrderHandler.cs
│       │   └── CreateOrderValidator.cs
│       └── GetOrder/
│           ├── GetOrderQuery.cs
│           └── GetOrderHandler.cs
├── MiApp.Domain/               # Entidades, value objects, enums, domain events
│   ├── Orders/
│   │   ├── Order.cs
│   │   ├── OrderItem.cs
│   │   ├── OrderStatus.cs        # enum
│   │   └── OrderCreatedEvent.cs
│   └── Customers/
└── MiApp.Infrastructure/       # EF Core, repos, servicios externos
    ├── Data/
    │   ├── AppDbContext.cs
    │   └── Configurations/       # IEntityTypeConfiguration<T>
    └── Services/
        ├── StripePaymentService.cs
        └── EmailService.cs
```

---

## Reglas de oro

1. **Una responsabilidad por clase.** Si necesitas "y" en el nombre, divide.
2. **Inyección de dependencias siempre.** `new` solo en entidades, value objects y DTOs.
3. **Async para I/O.** File, network, DB, message broker. No async para CPU-bound puro.
4. **No magic strings/numbers.** Constantes nombradas o enums.
5. **Validación temprana.** Guard clauses al inicio del método. `ArgumentException`, `ValidationException`.
6. **Excepciones custom de dominio.** `OrderNotFoundException`, `InsufficientStockException`. No relanzar `Exception` genérica.
7. **Logging estructurado.** `ILogger<T>` con templates, nunca interpolación. Source-generated loggers donde el rendimiento importe.
8. **CancellationToken en todo async I/O.** Propagar, no ignorar.
9. **Configuración tipada con `IOptions<T>`.** Validar en startup con `ValidateOnStart()`.
10. **Propiedades inmutables con `init` o `required`.** Reduce bugs por mutación accidental.
11. **Source-generated JSON y logging** para AOT-compatibilidad y rendimiento.
12. **`using` statement sobre bloques** para disposables breves.

---

## Sub-skills del kit

> 📁 Cada sub-skill tiene su guía detallada en `./{nombre}/GUIDE.md`. Usa `read` para cargarla cuando el tema lo requiera.


Cada sub-skill profundiza en su dominio:

| Skill                     | Cuándo cargarla                                   |
|---------------------------|---------------------------------------------------|
| `dotnet-patterns`         | Factory, Strategy, Repository, Decorator, Mediator, CQRS, etc. |
| `dotnet-solid`            | SOLID, DRY, KISS, YAGNI con ejemplos .NET         |
| `dotnet-clean-code`       | Refactoring, naming, métodos cortos, deuda técnica |
| `dotnet-architecture`     | N-Capas, Hexagonal, Clean Architecture, Vertical Slices, Modular Monolith |
| `dotnet-testing`          | xUnit, NSubstitute/FakeItEasy, TDD, integration, Fixtures |
| `dotnet-ef-core`          | DbContext, migraciones, LeftJoin/RightJoin, vector search, queries, raw SQL, interceptors, performance |
| `dotnet-dapper`           | Dapper 2.1, queries tipadas, multi-mapping, SPs, transacciones, estrategia híbrida EF Core + Dapper |
| `dotnet-api`              | Minimal APIs, Controllers, versioning, HATEOAS, OpenAPI, gRPC |
| `dotnet-security`         | JWT, OAuth2/OIDC, CORS, CSP, data protection, OWASP |
| `dotnet-performance`      | Caching (HybridCache, IDistributedCache), pooling, Span, async, profiling |

---

## Stack recomendado por defecto

| Propósito          | Herramienta               | Paquete NuGet                          |
|--------------------|---------------------------|----------------------------------------|
| Testing            | xUnit + FluentAssertions  | `xunit` + `FluentAssertions`           |
| Mocking            | NSubstitute               | `NSubstitute`                          |
| ORM                | EF Core 10                | `Microsoft.EntityFrameworkCore`        |
| Logging            | Serilog                    | `Serilog.AspNetCore`                   |
| Validación         | FluentValidation          | `FluentValidation.AspNetCore`          |
| Mapping            | Manual o Mapster          | `Mapster`                              |
| Resilience         | Microsoft.Extensions      | `Microsoft.Extensions.Resilience`      |
| Caching            | HybridCache               | `Microsoft.Extensions.Caching.Hybrid`  |
| OpenAPI            | Microsoft.AspNetCore.OpenApi | `Microsoft.AspNetCore.OpenApi`      |
| Mediator (opcional)| MediatR                   | `MediatR`                              |
