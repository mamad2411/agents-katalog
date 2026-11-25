---
name: dotnet-di
description: ".NET dependency injection patterns and practices"
---

# Seemann: Dependency Injection Done Right

Mark Seemann's core belief: **Dependency injection is a set of principles, not a framework.** Constructor injection is the default. The Composition Root wires everything. Service Locator is an anti-pattern. Get these right, and your code becomes testable, maintainable, and honest about its dependencies.

## The Foundational Principle

> "Dependency Injection is nothing more than a collection of design principles and patterns that enable loose coupling."

DI is not about containers. It's about writing code that declares what it needs and lets someone else provide it.

---

## Core Principles

### 1. Constructor Injection Is the Default

**Not this:**
```csharp
public class OrderService
{
    private IOrderRepository _repo;
    public void SetRepository(IOrderRepository repo) { _repo = repo; }
    public void PlaceOrder(Order order) { _repo.Save(order); }  // Might be null!
}
```

**This:**
```csharp
public class OrderService
{
    private readonly IOrderRepository _repo;
    private readonly ILogger<OrderService> _logger;

    public OrderService(IOrderRepository repo, ILogger<OrderService> logger)
    {
        _repo = repo ?? throw new ArgumentNullException(nameof(repo));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    public void PlaceOrder(Order order)
    {
        _repo.Save(order);   // Always valid
        _logger.LogInformation("Order {Id} placed", order.Id);
    }
}
```

**Why:** Dependencies are **immutable** (`readonly`), object is **never in an invalid state**, dependencies are **visible** in the signature, guard clauses catch nulls **at composition time**.

### 2. Service Lifetimes

```csharp
builder.Services.AddSingleton<ICacheService, RedisCacheService>();
builder.Services.AddScoped<IOrderRepository, SqlOrderRepository>();
builder.Services.AddTransient<IEmailSender, SmtpEmailSender>();
```

| Lifetime | Created | Use for |
|-----------|---------|---------|
| Singleton | Once per app | Caches, config, HttpClientFactory |
| Scoped | Once per request | DbContext, Unit of Work, current user |
| Transient | Every injection | Lightweight, stateless services |

**Decision rule:** Shared state across requests? Singleton. State for one request? Scoped. Stateless? Transient. When in doubt, Scoped.

### 3. Captive Dependency: The Silent Bug

A singleton depending on a scoped service **captures** it forever. The scoped instance never disposes.

**Not this:**
```csharp
public class ProductCache  // Singleton
{
    private readonly AppDbContext _db;  // Scoped -- CAPTURED!
    public ProductCache(AppDbContext db) { _db = db; }
}
```

**This:**
```csharp
public class ProductCache  // Singleton
{
    private readonly IServiceScopeFactory _scopeFactory;
    public ProductCache(IServiceScopeFactory scopeFactory) { _scopeFactory = scopeFactory; }

    public async Task<Product?> GetFreshAsync(int id)
    {
        using var scope = _scopeFactory.CreateScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        return await db.Products.FindAsync(id);
    }
}
```

**Detect it:** `ValidateScopes = true` in development throws on captive dependencies.

**The rule:** A service can only depend on equal or longer lifetimes: Singleton -> Singleton. Scoped -> Singleton, Scoped. Transient -> any.

### 4. Composition Root

All registration in `Program.cs`. Nowhere else resolves from the container.

**Not this (Service Locator):**
```csharp
public class OrderService
{
    public void PlaceOrder(Order order)
    {
        var repo = ServiceLocator.Get<IOrderRepository>();  // Hidden dependency!
        repo.Save(order);
    }
}
```

**This:**
```csharp
// Program.cs -- the ONE place that knows about concrete types
builder.Services.AddOrderingServices();

public static class OrderingServiceExtensions
{
    public static IServiceCollection AddOrderingServices(this IServiceCollection services)
    {
        services.AddScoped<IOrderRepository, SqlOrderRepository>();
        services.AddScoped<IOrderService, OrderService>();
        return services;
    }
}
```

Service Locator hides dependencies, kills compile-time safety, and makes testing require a full container.
### 5. Interface Segregation

**Not this:**
```csharp
public interface IUserService  // 8 methods -- GetById, Create, Delete, Verify, Reset...
{
    bool ValidateCredentials(string email, string password);
    // ... 7 more methods
}

public class LoginHandler
{
    private readonly IUserService _users;  // Only needs ValidateCredentials!
    public LoginHandler(IUserService users) => _users = users;
}
```

**This:**
```csharp
public interface ICredentialValidator
{
    bool Validate(string email, string password);
}

public class LoginHandler
{
    private readonly ICredentialValidator _validator;  // Exactly what it needs
    public LoginHandler(ICredentialValidator validator) => _validator = validator;
}
```

Constructor tells the truth. Tests mock only what's needed. Unrelated changes don't ripple.

### 6. Factory Pattern with DI

For runtime instance creation, inject a factory -- not `IServiceProvider`.

**Func<T> factory:**
```csharp
builder.Services.AddTransient<INotificationSender, EmailNotificationSender>();
builder.Services.AddSingleton<Func<INotificationSender>>(
    sp => () => sp.GetRequiredService<INotificationSender>());
```

**Custom factory when creation needs parameters:**
```csharp
public class ReportGeneratorFactory : IReportGeneratorFactory
{
    private readonly IServiceProvider _sp;
    public ReportGeneratorFactory(IServiceProvider sp) => _sp = sp;

    public IReportGenerator Create(ReportFormat format) => format switch
    {
        ReportFormat.Pdf => _sp.GetRequiredService<PdfReportGenerator>(),
        ReportFormat.Excel => _sp.GetRequiredService<ExcelReportGenerator>(),
        _ => throw new ArgumentOutOfRangeException(nameof(format))
    };
}
```

Confine `IServiceProvider` to factory classes. Never inject it into business logic.

### 7. Options Pattern

**Not this:**
```csharp
public class EmailSender
{
    public EmailSender(IConfiguration config)  // God object, magic strings
    {
        var host = config["Smtp:Host"];
        var port = int.Parse(config["Smtp:Port"]);
    }
}
```

**This:**
```csharp
public class SmtpSettings
{
    public string Host { get; set; } = "";
    public int Port { get; set; } = 587;
}

// Program.cs
builder.Services.Configure<SmtpSettings>(builder.Configuration.GetSection("Smtp"));

// Usage
public class EmailSender
{
    private readonly SmtpSettings _settings;
    public EmailSender(IOptions<SmtpSettings> options) { _settings = options.Value; }
}
```

**Named options** for multiple instances: `Configure<ApiSettings>("GitHub", section)`, resolve with `IOptionsMonitor<T>.Get("GitHub")`.

`IOptions<T>` = singleton, read once. `IOptionsSnapshot<T>` = scoped, refreshes per request. `IOptionsMonitor<T>` = singleton, refreshes on change.

### 8. Keyed Services (.NET 8+)

**Not this:**
```csharp
public INotificationSender Create(string channel) => channel switch
{
    "email" => new EmailSender(),  // Newing up = untestable
    "sms" => new SmsSender(),
    _ => throw new ArgumentException(channel)
};
```

**This:**
```csharp
builder.Services.AddKeyedScoped<INotificationSender, EmailSender>("email");
builder.Services.AddKeyedScoped<INotificationSender, SmsSender>("sms");
builder.Services.AddKeyedScoped<INotificationSender, PushSender>("push");

public class OrderNotifier
{
    public OrderNotifier(
        [FromKeyedServices("email")] INotificationSender email,
        [FromKeyedServices("sms")] INotificationSender sms)
    { }
}
```

### 9. Decorator Pattern

Wrap services with cross-cutting concerns without modifying them.

```csharp
// Core
public class SqlOrderRepository : IOrderRepository { /* DB queries */ }

// Caching decorator
public class CachedOrderRepository : IOrderRepository
{
    private readonly IOrderRepository _inner;
    private readonly IMemoryCache _cache;

    public CachedOrderRepository(IOrderRepository inner, IMemoryCache cache)
    { _inner = inner; _cache = cache; }

    public async Task<Order?> GetByIdAsync(int id) =>
        await _cache.GetOrCreateAsync($"order:{id}",
            _ => _inner.GetByIdAsync(id));

    public async Task SaveAsync(Order order)
    { await _inner.SaveAsync(order); _cache.Remove($"order:{order.Id}"); }
}
```

**Registration (manual chaining):**
```csharp
builder.Services.AddScoped<SqlOrderRepository>();
builder.Services.AddScoped<IOrderRepository>(sp =>
    new CachedOrderRepository(
        sp.GetRequiredService<SqlOrderRepository>(),
        sp.GetRequiredService<IMemoryCache>()));
```

**With Scrutor:** `builder.Services.Decorate<IOrderRepository, CachedOrderRepository>();`

### 10. Testing with DI

**Unit tests -- no container needed:**
```csharp
[Fact]
public async Task PlaceOrder_SavesAndNotifies()
{
    var repo = new FakeOrderRepository();
    var notifier = new FakeNotifier();
    var sut = new OrderService(repo, notifier);

    await sut.PlaceOrderAsync(new Order { Id = 1 });

    Assert.Single(repo.SavedOrders);
    Assert.Single(notifier.SentNotifications);
}
```

**Integration tests -- WebApplicationFactory overrides:**
```csharp
public class OrderApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public OrderApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.WithWebHostBuilder(b =>
            b.ConfigureServices(services =>
            {
                services.RemoveAll<DbContextOptions<AppDbContext>>();
                services.AddDbContext<AppDbContext>(o => o.UseInMemoryDatabase("Test"));
                services.AddScoped<IPaymentGateway, FakePaymentGateway>();
            })).CreateClient();
    }

    [Fact]
    public async Task PostOrder_Returns201()
    {
        var response = await _client.PostAsJsonAsync("/api/orders", new { ProductId = 1 });
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    }
}
```

---

## Anti-Patterns

| Anti-Pattern | What It Is | Fix |
|-------------|-----------|-----|
| **Service Locator** | Resolving from container in business logic | Constructor injection |
| **Constructor Over-Injection** | 5+ parameters = class does too much | Extract a service grouping related deps |
| **Ambient Context** | `HttpContext.Current`, `DateTime.Now` | Inject `IHttpContextAccessor`, `IDateTimeProvider` |
| **Bastard Injection** | Default impl in constructor: `repo ?? new SqlRepo()` | Remove default, require explicit injection |
| **Control Freak** | `new`ing dependencies inside the class | Inject via constructor |

---

## Decision Framework

```
SITUATION                                 APPROACH
----------------------------------------------------------------------------------
Default for all dependencies              Constructor injection, readonly fields
Runtime instance creation                 Factory (Func<T> or custom interface)
Same interface, multiple impls            Keyed services (.NET 8) or named options
Configuration values                      IOptions<T> / IOptionsSnapshot<T>
Cross-cutting concerns                    Decorator wrapping inner service
Singleton needs scoped dependency         IServiceScopeFactory, create scope on demand
Which lifetime?                           Scoped unless proven otherwise
Testing business logic                    Pass fakes via constructor, no container
Testing HTTP endpoints                    WebApplicationFactory with service overrides
```

---

## Code Review Checklist

1. **Constructor injection?** All dependencies via constructor, stored in `readonly` fields?
2. **No Service Locator?** No `IServiceProvider` in business logic?
3. **Lifetimes correct?** No singleton depending on scoped (captive dependency)?
4. **Scope validation on?** `ValidateScopes = true` in Development?
5. **Interfaces focused?** No god-interfaces partially consumed?
6. **Options pattern?** No raw `IConfiguration` injection for settings?
7. **Factories for runtime creation?** Not newing up dependencies in methods?
8. **Decorators clean?** Cross-cutting concerns separated from core logic?
9. **Testable?** Class instantiable in tests with fake dependencies?
10. **Composition Root only?** All registrations in `Program.cs` or extensions?

---

## Source Material

- "Dependency Injection Principles, Practices, and Patterns" (2nd Edition, Manning, 2019)
- Mark Seemann's blog: blog.ploeh.dk
- Steven van Deursen (co-author)
- Microsoft docs: Dependency injection in ASP.NET Core

---

*"Dependency Injection is nothing more than a collection of design principles and patterns that enable loose coupling."* -- Mark Seemann
