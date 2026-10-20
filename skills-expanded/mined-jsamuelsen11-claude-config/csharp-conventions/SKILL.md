---
name: csharp-conventions
description:
  This skill should be used when working on C# or .NET projects, writing C# code, reviewing C# code,
  or applying modern C# 12+ idioms and patterns.
version: 0.1.0
---

# C# Code Style and Idiomatic Patterns

This skill defines comprehensive conventions for writing modern C# 12+ code following .NET community
standards, Microsoft design guidelines, and idiomatic patterns for .NET 8+ projects.

## File-Scoped Namespaces

### Always Use File-Scoped Namespaces

File-scoped namespaces reduce indentation by one level and are the standard in modern .NET.

```csharp
// CORRECT: File-scoped namespace
namespace Catalog.Domain.Models;

public class Product
{
    public required Guid Id { get; init; }
    public required string Name { get; set; }
}
```

```csharp
// WRONG: Block-scoped namespace adds unnecessary nesting
namespace Catalog.Domain.Models
{
    public class Product
    {
        public required Guid Id { get; init; }
        public required string Name { get; set; }
    }
}
```

## Records for DTOs and Value Objects

### Use Records for Immutable Data Carriers

Prefer records over classes for DTOs, API responses, events, and value objects. Records provide
structural equality, `with` expressions, and deconstruction automatically.

```csharp
// CORRECT: Record for an API response
public record ProductResponse(
    Guid Id,
    string Name,
    decimal Price,
    string Category,
    DateTimeOffset CreatedAt);
```

```csharp
// WRONG: Full class for a simple data carrier
public class ProductResponse
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string Category { get; set; } = string.Empty;
    public DateTimeOffset CreatedAt { get; set; }
}
```

### Use Record Compact Constructors for Validation

```csharp
// CORRECT: Compact constructor validates parameters
public record OrderItem(string ProductId, int Quantity, decimal UnitPrice)
{
    public OrderItem
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(ProductId);
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(Quantity);
        ArgumentOutOfRangeException.ThrowIfNegative(UnitPrice);
    }
}
```

```csharp
// WRONG: Canonical constructor duplicates field assignments
public record OrderItem(string ProductId, int Quantity, decimal UnitPrice)
{
    public OrderItem(string productId, int quantity, decimal unitPrice)
        : this(productId, quantity, unitPrice)
    {
        if (quantity <= 0) throw new ArgumentException("Invalid quantity");
    }
}
```

### When Not to Use Records

Do not use records for:

- EF Core entities (records have reference equality issues with change tracking)
- Classes with complex mutable state
- Classes that need inheritance beyond simple hierarchies

```csharp
// CORRECT: EF Core entity as a class
public class Product
{
    public required Guid Id { get; init; }
    public required string Name { get; set; }
    public decimal Price { get; set; }
    public byte[] RowVersion { get; set; } = [];
}
```

## Primary Constructors

### Use Primary Constructors for Dependency Injection

Primary constructors (C# 12) eliminate constructor boilerplate for service classes.

```csharp
// CORRECT: Primary constructor for DI
public class ProductService(
    IProductRepository repository,
    ILogger<ProductService> logger)
{
    public async Task<Product?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        logger.LogDebug("Fetching product {ProductId}", id);
        return await repository.FindByIdAsync(id, ct);
    }
}
```

```csharp
// WRONG: Manual constructor boilerplate
public class ProductService
{
    private readonly IProductRepository _repository;
    private readonly ILogger<ProductService> _logger;

    public ProductService(
        IProductRepository repository,
        ILogger<ProductService> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public async Task<Product?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        _logger.LogDebug("Fetching product {ProductId}", id);
        return await _repository.FindByIdAsync(id, ct);
    }
}
```

## Nullable Reference Types

### Always Enable Nullable and Handle Nulls Explicitly

Enable nullable reference types project-wide and use annotations to communicate intent.

```csharp
// CORRECT: Explicit nullable handling
public async Task<UserResponse?> FindByEmailAsync(
    string email, CancellationToken ct)
{
    ArgumentException.ThrowIfNullOrWhiteSpace(email);

    var user = await repository.FindByEmailAsync(email, ct);
    return user is null ? null : MapToResponse(user);
}
```

```csharp
// WRONG: Ignoring nullable with null-forgiving operator
public async Task<UserResponse> FindByEmailAsync(string email, CancellationToken ct)
{
    var user = await repository.FindByEmailAsync(email, ct);
    return MapToResponse(user!); // Hides potential NullReferenceException
}
```

### Prefer Pattern Matching for Null Checks

```csharp
// CORRECT: Pattern matching with is
if (result is { Value: > 0 } positiveResult)
{
    Process(positiveResult);
}

if (user is not null)
{
    SendNotification(user);
}
```

```csharp
// WRONG: Comparison operators for null checks
if (result != null && result.Value > 0)
{
    Process(result);
}

if (user != null)
{
    SendNotification(user);
}
```

### Use Guard Clause Methods

```csharp
// CORRECT: .NET 8 guard clause methods
public void Process(Order order, string reason)
{
    ArgumentNullException.ThrowIfNull(order);
    ArgumentException.ThrowIfNullOrWhiteSpace(reason);
    ArgumentOutOfRangeException.ThrowIfNegativeOrZero(order.Total);
}
```

```csharp
// WRONG: Manual null check with throw
public void Process(Order order, string reason)
{
    if (order == null) throw new ArgumentNullException(nameof(order));
    if (string.IsNullOrWhiteSpace(reason))
        throw new ArgumentException("Reason is required", nameof(reason));
}
```

## Async/Await Rules

### Always Propagate CancellationToken

Every async method that does I/O must accept and pass through a `CancellationToken`.

```csharp
// CORRECT: CancellationToken propagated through chain
public async Task<ProductResponse> GetProductAsync(
    Guid id, CancellationToken ct)
{
    var product = await repository.FindByIdAsync(id, ct);
    var reviews = await reviewService.GetReviewsAsync(id, ct);
    return MapToResponse(product, reviews);
}
```

```csharp
// WRONG: CancellationToken not passed to downstream calls
public async Task<ProductResponse> GetProductAsync(Guid id)
{
    var product = await repository.FindByIdAsync(id, default);
    var reviews = await reviewService.GetReviewsAsync(id, default);
    return MapToResponse(product, reviews);
}
```

### Use ValueTask for Hot Paths with Synchronous Results

```csharp
// CORRECT: ValueTask when result is often available synchronously
public ValueTask<Product?> GetByIdAsync(Guid id, CancellationToken ct)
{
    if (cache.TryGetValue(id, out Product? cached))
    {
        return ValueTask.FromResult(cached);
    }
    return new ValueTask<Product?>(LoadFromDatabaseAsync(id, ct));
}
```

```csharp
// WRONG: Task when result is frequently synchronous
public async Task<Product?> GetByIdAsync(Guid id, CancellationToken ct)
{
    if (cache.TryGetValue(id, out Product? cached))
    {
        return cached; // Allocates a Task unnecessarily
    }
    return await LoadFromDatabaseAsync(id, ct);
}
```

### Never Use async void

```csharp
// CORRECT: async Task for async methods
public async Task HandleEventAsync(OrderPlacedEvent e, CancellationToken ct)
{
    await notificationService.SendAsync(e.CustomerId, ct);
}
```

```csharp
// WRONG: async void loses exceptions and cannot be awaited
public async void HandleEvent(OrderPlacedEvent e)
{
    await notificationService.SendAsync(e.CustomerId, default);
}
```

### Avoid .Result and .Wait()

```csharp
// CORRECT: await for async results
var product = await repository.FindByIdAsync(id, ct);
```

```csharp
// WRONG: Blocking on async code causes deadlocks
var product = repository.FindByIdAsync(id, ct).Result;
var product2 = repository.FindByIdAsync(id, ct).GetAwaiter().GetResult();
```

## LINQ Rules

### Prefer Method Syntax for Most Operations

```csharp
// CORRECT: Method syntax for common operations
var activeProducts = products
    .Where(p => p.Status == ProductStatus.Active)
    .OrderBy(p => p.Name)
    .Select(p => new ProductListItem(p.Id, p.Name, p.Price))
    .ToList();
```

```csharp
// WRONG: Query syntax for simple operations
var activeProducts = (
    from p in products
    where p.Status == ProductStatus.Active
    orderby p.Name
    select new ProductListItem(p.Id, p.Name, p.Price)
).ToList();
```

### Use Query Syntax for Joins

```csharp
// CORRECT: Query syntax makes joins readable
var results =
    from product in products
    join category in categories on product.CategoryId equals category.Id
    where product.Price > 100
    select new { product.Name, category.Name };
```

```csharp
// WRONG: Method syntax for complex joins
var results = products
    .Join(categories,
        p => p.CategoryId,
        c => c.Id,
        (p, c) => new { p, c })
    .Where(x => x.p.Price > 100)
    .Select(x => new { x.p.Name, CategoryName = x.c.Name });
```

### Avoid Materializing Prematurely

```csharp
// CORRECT: Defer execution until needed
var query = dbContext.Products
    .Where(p => p.Price > 100)
    .OrderBy(p => p.Name);

// Apply pagination at database level
var results = await query
    .Skip(page * pageSize)
    .Take(pageSize)
    .ToListAsync(ct);
```

```csharp
// WRONG: Materializing before filtering loads entire table
var allProducts = await dbContext.Products.ToListAsync(ct);
var results = allProducts
    .Where(p => p.Price > 100)
    .OrderBy(p => p.Name)
    .Skip(page * pageSize)
    .Take(pageSize)
    .ToList();
```

## Dependency Injection Rules

### Register Services with Correct Lifetimes

```csharp
// CORRECT: Appropriate lifetimes
services.AddSingleton<ISystemClock, SystemClock>();  // Stateless, thread-safe
services.AddScoped<IProductRepository, ProductRepository>(); // Per-request, DbContext
services.AddTransient<IProductValidator, ProductValidator>(); // Lightweight, no state
```

```csharp
// WRONG: DbContext-dependent service as singleton
services.AddSingleton<IProductRepository, ProductRepository>(); // DbContext is scoped!
```

### Use IOptions Pattern for Configuration

```csharp
// CORRECT: IOptions pattern with validation
services.AddOptionsWithValidateOnStart<CatalogOptions>()
    .Bind(configuration.GetSection("Catalog"))
    .ValidateDataAnnotations();
```

```csharp
// WRONG: Reading configuration directly in services
public class ProductService
{
    private readonly string _connectionString;

    public ProductService(IConfiguration config)
    {
        _connectionString = config["ConnectionStrings:Default"]!;
    }
}
```

## Naming Conventions

### PascalCase for Public Members

```csharp
// CORRECT
public class ProductService
{
    public async Task<Product> GetByIdAsync(Guid id, CancellationToken ct) { }
    public string DisplayName { get; set; } = string.Empty;
    public const int MaxPageSize = 100;
}
```

```csharp
// WRONG
public class productService
{
    public async Task<Product> getById(Guid id, CancellationToken ct) { }
    public string displayName { get; set; } = string.Empty;
    public const int MAX_PAGE_SIZE = 100;
}
```

### \_camelCase for Private Fields

```csharp
// CORRECT: Underscore prefix for private fields
public class OrderProcessor
{
    private readonly IOrderRepository _orderRepository;
    private readonly ILogger<OrderProcessor> _logger;
    private int _retryCount;
}
```

```csharp
// WRONG: No prefix or other conventions
public class OrderProcessor
{
    private readonly IOrderRepository orderRepository;
    private readonly ILogger<OrderProcessor> m_logger;
    private int RetryCount;
}
```

### I Prefix for Interfaces

```csharp
// CORRECT
public interface IProductRepository { }
public interface IOrderService { }
```

```csharp
// WRONG
public interface ProductRepository { }
public interface OrderServiceInterface { }
```

### Async Suffix for Async Methods

```csharp
// CORRECT
public async Task<Product> GetByIdAsync(Guid id, CancellationToken ct) { }
public async Task DeleteAsync(Guid id, CancellationToken ct) { }
```

```csharp
// WRONG
public async Task<Product> GetById(Guid id, CancellationToken ct) { }
public async Task Delete(Guid id, CancellationToken ct) { }
```

## Warning Suppression Rules

### Never Suppress Warnings with Pragmas

Code must compile cleanly with `-warnaserror`. Never suppress warnings to make the build pass.

```csharp
// CORRECT: Fix the nullable warning
public string GetDisplayName(User? user)
{
    return user?.DisplayName ?? "Unknown";
}
```

```csharp
// WRONG: Suppressing nullable warning
#pragma warning disable CS8602
public string GetDisplayName(User? user)
{
    return user.DisplayName; // NullReferenceException at runtime
}
#pragma warning restore CS8602
```

### Never Use [SuppressMessage]

```csharp
// CORRECT: Add the null check
public void Process(Order order)
{
    ArgumentNullException.ThrowIfNull(order);
    // process order
}
```

```csharp
// WRONG: Suppressing the analyzer
[SuppressMessage("Usage", "CA1062:Validate arguments of public methods")]
public void Process(Order order)
{
    // Missing null check
}
```

### Acceptable Suppression Location

The only place warning suppressions are acceptable is in `.editorconfig` for project-wide policy
decisions made by the team:

```text
# .editorconfig - project-wide policy
dotnet_diagnostic.CA2007.severity = none
```

## Collection Expressions

### Use Collection Expressions for Initialization

```csharp
// CORRECT: Collection expression (C# 12)
List<string> names = ["Alice", "Bob", "Charlie"];
int[] numbers = [1, 2, 3, 4, 5];
IReadOnlyList<string> empty = [];
```

```csharp
// WRONG: Verbose initialization
List<string> names = new List<string> { "Alice", "Bob", "Charlie" };
int[] numbers = new int[] { 1, 2, 3, 4, 5 };
IReadOnlyList<string> empty = new List<string>();
```

### Use Spread Operator for Combining Collections

```csharp
// CORRECT: Spread operator
List<string> combined = [..baseItems, ..additionalItems, "extra"];
```

```csharp
// WRONG: Manual concatenation
var combined = baseItems.Concat(additionalItems).Append("extra").ToList();
```

## Pattern Matching

### Prefer Switch Expressions Over Switch Statements

```csharp
// CORRECT: Switch expression
public string GetStatusLabel(OrderStatus status) => status switch
{
    OrderStatus.Pending => "Pending Review",
    OrderStatus.Confirmed => "Confirmed",
    OrderStatus.Shipped => "In Transit",
    OrderStatus.Delivered => "Delivered",
    OrderStatus.Cancelled => "Cancelled",
    _ => throw new ArgumentOutOfRangeException(nameof(status))
};
```

```csharp
// WRONG: Switch statement with returns
public string GetStatusLabel(OrderStatus status)
{
    switch (status)
    {
        case OrderStatus.Pending: return "Pending Review";
        case OrderStatus.Confirmed: return "Confirmed";
        case OrderStatus.Shipped: return "In Transit";
        case OrderStatus.Delivered: return "Delivered";
        case OrderStatus.Cancelled: return "Cancelled";
        default: throw new ArgumentOutOfRangeException(nameof(status));
    }
}
```

### Use Property Patterns for Object Matching

```csharp
// CORRECT: Property patterns
if (response is { StatusCode: >= 200 and < 300, Content.Length: > 0 })
{
    ProcessResponse(response);
}
```

```csharp
// WRONG: Multiple conditions
if (response != null && response.StatusCode >= 200
    && response.StatusCode < 300 && response.Content != null
    && response.Content.Length > 0)
{
    ProcessResponse(response);
}
```

## Error Handling

### Throw Specific Exception Types

```csharp
// CORRECT: Specific, meaningful exception types
public async Task<Product> GetByIdAsync(Guid id, CancellationToken ct)
{
    return await repository.FindByIdAsync(id, ct)
        ?? throw new ProductNotFoundException(id);
}
```

```csharp
// WRONG: Generic exceptions
public async Task<Product> GetByIdAsync(Guid id, CancellationToken ct)
{
    var product = await repository.FindByIdAsync(id, ct);
    if (product == null)
        throw new Exception($"Product {id} not found");
    return product;
}
```

### Use IExceptionHandler for Global Error Handling

```csharp
// CORRECT: IExceptionHandler (.NET 8+)
public class GlobalExceptionHandler(
    ILogger<GlobalExceptionHandler> logger) : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext context, Exception exception, CancellationToken ct)
    {
        logger.LogError(exception, "Unhandled exception");
        context.Response.StatusCode = 500;
        await context.Response.WriteAsJsonAsync(
            new ProblemDetails { Status = 500, Title = "Internal Server Error" }, ct);
        return true;
    }
}
```

```csharp
// WRONG: Try-catch in every controller action
[HttpGet("{id}")]
public async Task<IActionResult> GetProduct(Guid id)
{
    try
    {
        var product = await service.GetByIdAsync(id, default);
        return Ok(product);
    }
    catch (Exception ex)
    {
        return StatusCode(500, new { error = ex.Message });
    }
}
```

## Logging

### Use Structured Logging

```csharp
// CORRECT: Structured logging with message templates
logger.LogInformation(
    "Processing order {OrderId} for customer {CustomerId}",
    order.Id, order.CustomerId);
```

```csharp
// WRONG: String interpolation in log messages (defeats structured logging)
logger.LogInformation(
    $"Processing order {order.Id} for customer {order.CustomerId}");
```

### Use Appropriate Log Levels

```csharp
// CORRECT: Appropriate levels
logger.LogDebug("Cache hit for product {ProductId}", id);
logger.LogInformation("Order {OrderId} placed successfully", order.Id);
logger.LogWarning("Retry attempt {Attempt} for payment {PaymentId}", attempt, paymentId);
logger.LogError(exception, "Failed to process order {OrderId}", orderId);
logger.LogCritical(exception, "Database connection lost");
```

```csharp
// WRONG: Everything at Information level
logger.LogInformation("Cache hit for product {ProductId}", id); // Too noisy
logger.LogInformation(exception.ToString()); // Loses structure
```
