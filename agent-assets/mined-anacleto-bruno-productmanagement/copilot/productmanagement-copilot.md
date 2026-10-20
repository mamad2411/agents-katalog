# Coding Rules for {ProjectName} Functions

## Overview
This document outlines the coding standards, patterns, and conventions for the {ProjectName}Functions project built on .NET 9.0 Azure Functions v4 with Isolated Worker Model.

## Technology Stack

### Core Technologies
- **.NET 9.0** - Target framework
- **Azure Functions v4** - Isolated Worker Model
- **PostgreSQL** - Primary database with Entity Framework Core
- **Redis** - Caching layer
- **Docker** - Containerization

---

## Code Quality Standards

### SOLID Principles
- **Single Responsibility**: Each class should have one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Derived classes must be substitutable for base classes
- **Interface Segregation**: Clients shouldn't depend on interfaces they don't use
- **Dependency Inversion**: Depend on abstractions, not concretions

### Code Quality Standards
- **Always prefer interfaces** over concrete types in dependencies
- **Use async/await** for all database operations
- **Implement pagination** for all list queries
- **Add proper error handling** with Result pattern
- **Use FluentValidation** for input validation
- **Maintain separation of concerns** across layers

### Error Handling
```csharp
public async Task<Result<User>> GetUserAsync(int id)
{
    try
    {
        if (id <= 0)
            return Result<User>.Failure("Invalid user ID");
            
        var user = await _repository.GetByIdAsync(id);
        return user != null 
            ? Result<User>.Success(user)
            : Result<User>.Failure("User not found");
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error retrieving user with ID {UserId}", id);
        return Result<User>.Failure("An error occurred while retrieving the user");
    }
}
```

### Logging Standards
- Use structured logging with Serilog
- Include correlation IDs for request tracking
- Log at appropriate levels: Trace, Debug, Information, Warning, Error, Critical
- Include relevant context in log messages

### Performance Guidelines
- Use async/await for I/O operations
- Implement caching for frequently accessed data
- Use connection pooling for database connections
- Implement pagination for large data sets
- Use streaming for large file operations

---

## Security Guidelines

### Authentication & Authorization
- Validate all input parameters
- Implement proper CORS policies
- Use HTTPS for all external communications

### Data Protection
- Sanitize HTML content using `HtmlSanitizer`
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Encrypt sensitive data at rest and in transit

### Secret Management
- Store secrets in Azure Key Vault
- Use managed identities when possible
- Never commit secrets to source control
- Rotate secrets regularly

---

## Docker & Deployment

### Dockerfile Standards
- Use multi-stage builds for optimization
- Follow least privilege principle
- Minimize layer count
- Use specific base image versions

### Environment Variables
- Use environment variables for configuration
- Provide default values where appropriate
- Document all required environment variables

---
## Architecture Patterns

### Clean Architecture
Maintain clear separation of concerns across layers:

```
{ProjectName}/
├── Functions/          # Azure Function endpoints (Presentation Layer)
├── Services/           # Business logic (Application Layer)
├── Infrastructure/     # External concerns (Infrastructure Layer)
├── Entities/          # Domain models (Domain Layer)
├── Dtos/              # Data Transfer Objects
├── Models/            # View models and request/response models
├── Helpers/           # Utility classes and extensions
├── Constants/         # Application constants
└── Enumerations/      # Enum definitions
```

### Dependency Flow Rules
- **Functions** → **Services** → **Infrastructure** → **Entities**
- **DTOs** can be used across all layers
- **Models** should primarily be used in Functions and Services
- **Entities** should not reference upper layers

---

## Naming Conventions

### Namespaces
- Use **lowercase** for namespace segments: `{ProjectName}.services`
- Follow project structure: `{ProjectName}.{FolderName}`

### Classes and Interfaces
- **PascalCase** for all class names: `ProductService`, `UserRepository`
- **Interface prefix**: Interfaces must start with `I`: `IProductService`, `IUserRepository`
- **Descriptive names**: Avoid abbreviations, use full descriptive names

### Methods and Properties
- **PascalCase** for public members: `GetUserAsync`, `IsActive`
- **camelCase** for private fields: `_connectionString`, `_logger`
- **Async suffix**: All async methods must end with `Async`: `ProcessDataAsync`

### Constants and Enums
- **PascalCase** for enum values: `Status.Active`, `Priority.High`
- **UPPER_CASE** for constants: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`

### Database Migrations
- **Date-based naming**: `YYYY.MM.DD` format for migration folders
- **Descriptive file names**: `001_CreateUserTable.sql`, `002_AddIndexToUserEmail.sql`

---

## Repository Pattern & Entity Framework

###  Repository Pattern and Structure
Create mixed Repository Structure and entity-specific repositories 

```csharp
public interface IProductRepository : IRepository<Product>
{
    Task<T?> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
    Task DeleteAsync(T entity);
    Task<int> CountAsync();
    Task<int> CountAsync(Expression<Func<T, bool>> predicate);
    Task<IEnumerable<T>> GetPagedAsync(int page, int pageSize);
    Task<IEnumerable<T>> GetPagedAsync(int page, int pageSize, Expression<Func<T, bool>>? predicate = null);

    Task<ProductResponseDto?> GetProductDtoByIdAsync(int id);
    Task<IEnumerable<ProductResponseDto>> GetProductDtosAsync(
        string? searchTerm = null,
        string? category = null,
        decimal? minPrice = null,
        decimal? maxPrice = null,
        string? sortBy = null,
        bool descending = false,
        int page = 1,
        int pageSize = 20);
    Task<int> GetProductCountAsync(string? searchTerm = null, string? category = null);
    Task<bool> ExistsBySkuAsync(string sku, int? excludeId = null);
}

public class ProductRepository : Repository<Product>, IProductRepository
{
    public ProductRepository(DbContext context) : base(context) { }

    public async Task<ProductResponseDto?> GetProductDtoByIdAsync(int id)
    {
        return await _context.Products
            .Where(p => p.Id == id)
            .Select(p => new ProductResponseDto
            {
                Id = p.Id,
                Name = p.Name,
                // ... other properties
            })
            .FirstOrDefaultAsync();
    }
    // ... other implementations
}
```

### Entity Configuration Separation
Use `IEntityTypeConfiguration<T>` to separate entity configurations:

```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.HasKey(p => p.Id);

        builder.Property(p => p.Name)
            .IsRequired()
            .HasMaxLength(255);

        builder.Property(p => p.Price)
            .HasPrecision(18, 2);

        // Performance indexes
        builder.HasIndex(p => p.Name);
        builder.HasIndex(p => p.Sku).IsUnique();

        // Composite indexes for common query patterns
        builder.HasIndex(p => new { p.Category, p.Brand });

        // Configure relationships
        builder.HasMany(p => p.ProductColors)
            .WithOne(pc => pc.Product)
            .HasForeignKey(pc => pc.ProductId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}

// Apply in DbContext
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // Apply all configurations from assembly
    modelBuilder.ApplyConfigurationsFromAssembly(typeof(ProductConfiguration).Assembly);

    // Configure naming convention for PostgreSQL
    foreach (var entity in modelBuilder.Model.GetEntityTypes())
    {
        entity.SetTableName(entity.GetTableName()?.ToLowerInvariant());
        foreach (var property in entity.GetProperties())
        {
            property.SetColumnName(property.GetColumnName().ToLowerInvariant());
        }
    }
}
```

### Query Extensions Pattern
Create fluent query extensions for reusable filtering and sorting:

```csharp
public static class ProductQueryExtensions
{
    public static IQueryable<Product> IncludeRelated(this IQueryable<Product> query)
    {
        return query
            .Include(p => p.ProductColors)
                .ThenInclude(pc => pc.Color)
            .Include(p => p.ProductSizes)
                .ThenInclude(ps => ps.Size);
    }

    public static IQueryable<Product> WhereCategory(this IQueryable<Product> query, string? category)
    {
        return string.IsNullOrEmpty(category)
            ? query
            : query.Where(p => p.Category.ToLower() == category.ToLower());
    }

    public static IQueryable<Product> WherePriceRange(this IQueryable<Product> query, decimal? minPrice, decimal? maxPrice)
    {
        if (minPrice.HasValue)
            query = query.Where(p => p.Price >= minPrice.Value);
        if (maxPrice.HasValue)
            query = query.Where(p => p.Price <= maxPrice.Value);
        return query;
    }

    public static IQueryable<Product> WhereSearch(this IQueryable<Product> query, string? searchTerm)
    {
        if (string.IsNullOrEmpty(searchTerm))
            return query;

        var lowerSearchTerm = searchTerm.ToLower();
        return query.Where(p =>
            p.Name.ToLower().Contains(lowerSearchTerm) ||
            p.Description.ToLower().Contains(lowerSearchTerm) ||
            p.Brand.ToLower().Contains(lowerSearchTerm));
    }

    public static IQueryable<Product> OrderByField(this IQueryable<Product> query, string? sortBy, bool descending = false)
    {
        return sortBy?.ToLower() switch
        {
            "name" => descending ? query.OrderByDescending(p => p.Name) : query.OrderBy(p => p.Name),
            "price" => descending ? query.OrderByDescending(p => p.Price) : query.OrderBy(p => p.Price),
            "createdat" => descending ? query.OrderByDescending(p => p.CreatedAt) : query.OrderBy(p => p.CreatedAt),
            _ => descending ? query.OrderByDescending(p => p.CreatedAt) : query.OrderBy(p => p.CreatedAt)
        };
    }
}
```

### Mapping Extensions Pattern
Create extension methods for clean entity-DTO mapping:

```csharp
public static class MappingExtensions
{
    public static ProductResponseDto ToResponseDto(this Product product)
    {
        return new ProductResponseDto
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Price = product.Price,
            CreatedAt = product.CreatedAt,
            UpdatedAt = product.UpdatedAt
        };
    }

    public static Product ToEntity(this CreateProductRequestDto dto)
    {
        return new Product
        {
            Name = dto.Name,
            Description = dto.Description,
            Price = dto.Price,
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };
    }

    public static void UpdateFromDto(this Product product, UpdateProductRequestDto dto)
    {
        product.Name = dto.Name;
        product.Description = dto.Description;
        product.Price = dto.Price;
        product.UpdatedAt = DateTime.UtcNow;
    }

    public static IEnumerable<ProductResponseDto> ToResponseDtos(this IEnumerable<Product> products)
    {
        return products.Select(p => p.ToResponseDto());
    }
}
```

### DbContext Best Practices
- Implement automatic timestamp handling in `SaveChanges` override
- Use lazy loading judiciously (prefer explicit Include/ThenInclude)
- Configure connection resiliency for cloud environments
- Implement proper naming conventions for database compatibility

### Performance Optimization Patterns

#### Direct DTO Projection
Always prefer direct DTO projection over entity materialization for read operations:

```csharp
// ✅ PREFERRED: Direct projection (no entity tracking overhead)
public async Task<IEnumerable<ProductSummaryDto>> GetProductSummariesAsync()
{
    return await _context.Products
        .Select(p => new ProductSummaryDto
        {
            Id = p.Id,
            Name = p.Name,
            Price = p.Price
        })
        .ToListAsync();
}

// ❌ AVOID: Entity materialization then mapping
public async Task<IEnumerable<ProductSummaryDto>> GetProductSummariesAsync()
{
    var products = await _context.Products.ToListAsync(); // Loads entire entities
    return products.Select(p => p.ToSummaryDto()); // Additional mapping step
}
```

#### Query Optimization Rules
1. **Always use `.AsNoTracking()`** for read-only queries
2. **Project to DTOs** instead of loading full entities
3. **Use specific field selection** rather than loading entire entities
4. **Implement pagination** for all list queries
5. **Add appropriate indexes** for filtering and sorting fields

#### Filtering and Searching Best Practices
```csharp
// ✅ EFFICIENT: Database-level filtering with indexes
public async Task<IEnumerable<ProductDto>> SearchProductsAsync(string searchTerm, int page, int pageSize)
{
    return await _context.Products
        .AsNoTracking()
        .Where(p => p.Name.Contains(searchTerm) || p.Description.Contains(searchTerm))
        .OrderBy(p => p.Name)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Select(p => new ProductDto { /* projection */ })
        .ToListAsync();
}

// ❌ INEFFICIENT: Client-side filtering
public async Task<IEnumerable<ProductDto>> SearchProductsAsync(string searchTerm)
{
    var allProducts = await _context.Products.ToListAsync(); // Loads everything
    return allProducts
        .Where(p => p.Name.Contains(searchTerm))
        .Select(p => p.ToDto());
}
```

### Entity Framework Design Rules

#### Repository Implementation Rules
1. **Specialized repositories** should inherit from generic repository
2. **Always implement interface-first** for testability
3. **Use DTO projections** in specialized repository methods
4. **Keep generic repository simple** - complex queries go in specialized repos
5. **Register both generic and specialized** repositories in DI container

```csharp
// Registration in Program.cs
services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
services.AddScoped<IProductRepository, ProductRepository>();
services.AddScoped<IOrderRepository, OrderRepository>();
```

#### Mapping Strategy Rules
1. **Entity to DTO**: Use extension methods (`.ToResponseDto()`)
2. **DTO to Entity**: Use extension methods (`.ToEntity()`)
3. **Entity updates**: Use extension methods (`.UpdateFromDto()`)
4. **Collection mapping**: Use extension methods (`.ToResponseDtos()`)
5. **Complex mappings**: Consider dedicated mapping classes for complex scenarios

#### Configuration Organization
1. **One configuration class per entity** (`IEntityTypeConfiguration<T>`)
2. **Group related configurations** in same namespace/folder
3. **Apply all configurations** using `ApplyConfigurationsFromAssembly()`
4. **Separate database-specific logic** (naming conventions, etc.)

---

## Dependency Injection

### Service Registration Patterns
```csharp
// In Program.cs

// Entity Framework
services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseNpgsql(connectionString);
    // Configure for development
    if (context.HostingEnvironment.IsDevelopment())
    {
        options.EnableSensitiveDataLogging();
        options.EnableDetailedErrors();
    }
});

// Repository Pattern Registration
services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
services.AddScoped<IProductRepository, ProductRepository>();
services.AddScoped<IOrderRepository, OrderRepository>();
services.AddScoped<IUnitOfWork, UnitOfWork>();

// Business Services
services.AddScoped<IProductService, ProductService>();
services.AddScoped<IOrderService, OrderService>();

// Infrastructure Services
services.AddSingleton<ICacheService, RedisCacheService>();
services.AddScoped<IEmailService, EmailService>();

// FluentValidation
services.AddValidatorsFromAssemblyContaining<Program>();
```

### Lifetime Management
- **Scoped**: Services that maintain state per request (Repositories, Business Services)
- **Singleton**: Stateless services, configuration, caching
- **Transient**: Lightweight, stateless utility services

### Constructor Injection
- Always use constructor injection
- Use readonly fields for injected dependencies
- Validate null dependencies in constructors

---

## Configuration Management

### appsettings Structure
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "...",
    "RedisConnection": "..."
  },
  "AzureWebJobsStorage": "...",
  "FeatureFlags": {
    "EnableAdvancedLogging": true,
    "UseRedisCache": true
  },
  "ExternalServices": {
    "ApiBaseUrl": "...",
    "Timeout": "00:00:30"
  }
}
```

### Environment-Specific Configuration
- **appsettings.json** - Base configuration
- **appsettings.Development.json** - Development overrides
- **appsettings.Docker.json** - Docker container settings
- **appsettings.Release.json** - Production overrides

### Configuration Binding
```csharp
public class ExternalServiceConfig
{
    public string ApiBaseUrl { get; set; }
    public TimeSpan Timeout { get; set; }
}

// In Program.cs
services.Configure<ExternalServiceConfig>(
    configuration.GetSection("ExternalServices"));
```

---

## Azure Functions Architecture Patterns

### Clean Function Design Principles

#### Base Class Pattern
- **Create abstract base classes** to eliminate code duplication across functions
- **Implement common infrastructure** for HTTP response handling, error management, and request parsing
- **Use generic base classes** to handle different function types (with/without validation)

```csharp
// Example: Base class for functions without input validation
public abstract class BaseFunction
{
    protected readonly ILogger _logger;

    protected BaseFunction(ILogger logger) => _logger = logger;

    protected async Task<HttpResponseData> ExecuteSafelyAsync<TResponse>(
        HttpRequestData request, Func<Task<TResponse>> handler)
    {
        // Centralized error handling and response creation
    }
}

// Example: Base class for functions with input validation
public abstract class BaseFunctionWithValidation<TRequest, TValidator>
    where TRequest : new()
    where TValidator : AbstractValidator<TRequest>, new()
{
    protected async Task<HttpResponseData> ExecuteWithValidationAsync<TResponse>(
        HttpRequestData request, Func<TRequest, Task<TResponse>> handler)
    {
        // Automatic request parsing, validation, and response handling
    }
}
```

#### Infrastructure Helper Classes
- **Centralize HTTP operations** in dedicated helper classes
- **Standardize JSON serialization** with consistent naming conventions
- **Create reusable request/response utilities** for common operations

```csharp
// HTTP Response Helper
public static class HttpResponseHelper
{
    public static Task<HttpResponseData> CreateJsonResponseAsync<T>(
        HttpRequestData request, T data, HttpStatusCode statusCode = HttpStatusCode.OK);

    public static Task<HttpResponseData> CreateErrorResponseAsync(
        HttpRequestData request, string message, HttpStatusCode statusCode);
}

// Request Helper
public static class RequestHelper
{
    public static Task<T> ParseJsonBodyAsync<T>(HttpRequestData request) where T : new();
}
```

### Function Implementation Patterns

#### ✅ RECOMMENDED: Clean Function Pattern
```csharp
public class ProductFunction : BaseFunctionWithValidation<ProductRequestDto, ProductRequestValidator>
{
    private readonly IProductService _productService;

    public ProductFunction(ILogger<ProductFunction> logger, IProductService productService,
        ProductRequestValidator validator) : base(logger, validator)
    {
        _productService = productService;
    }

    [Function("ProcessProduct")]
    public async Task<HttpResponseData> ProcessAsync(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "products")] HttpRequestData req)
    {
        return await ExecuteWithValidationAsync<ProductResponseDto>(req, async productRequest =>
        {
            // Focus only on business logic - infrastructure is handled by base class
            var result = await _productService.ProcessAsync(productRequest);
            return result;
        });
    }
}
```

#### ❌ AVOID: Manual Infrastructure Pattern
```csharp
// Don't implement manual try-catch, JSON parsing, validation, and response creation
public class ProductFunction
{
    [Function("ProcessProduct")]
    public async Task<HttpResponseData> ProcessAsync(HttpRequestData req)
    {
        try
        {
            // Manual JSON parsing
            // Manual validation
            // Manual error handling
            // Manual response creation
        }
        catch (Exception ex)
        {
            // Manual error response
        }
    }
}
```

### Function Implementation Patterns - Detailed Rules

#### Rule 1: Always Use Base Class Methods
**❌ NEVER do this:**
```csharp
[Function("GetProduct")]
public async Task<HttpResponseData> GetAsync(HttpRequestData req)
{
    try 
    {
        // Manual implementation
        var response = req.CreateResponse(HttpStatusCode.OK);
        // ... manual JSON, error handling, etc.
    }
    catch (Exception ex)
    {
        // Manual error handling
    }
}
```

**✅ ALWAYS do this:**
```csharp
[Function("GetProduct")]
public async Task<HttpResponseData> GetAsync(HttpRequestData req)
{
    return await ExecuteSafelyAsync<ProductDto>(req, async () =>
    {
        return await _service.GetProductAsync(id);
    });
}
```

#### Rule 2: Choose the Right Base Method

**For business data operations (most common):**
```csharp
// Use when returning business data - base class handles JSON serialization
return await ExecuteSafelyAsync<TResponse>(req, async () => 
{
    return businessDataObject; // Returns POCO/DTO
});
```

**For custom HTTP responses (health checks, file downloads, etc.):**
```csharp
// Use when you need custom status codes or response formats
return await ExecuteSafelyAsync(req, async () => 
{
    var response = req.CreateResponse(customStatusCode);
    // Custom response logic
    return response; // Returns HttpResponseData
});
```

#### Rule 3: Validation vs Non-Validation Functions

**Functions WITH input validation:**
```csharp
public class ProductFunctions : BaseFunctionWithValidation<CreateProductDto, CreateProductValidator>
{
    [Function("CreateProduct")]
    public async Task<HttpResponseData> CreateAsync(HttpRequestData req)
    {
        return await ExecuteWithValidationAsync<ProductDto>(req, async (validatedInput) =>
        {
            return await _service.CreateAsync(validatedInput);
        });
    }
}
```

**Functions WITHOUT input validation:**
```csharp
public class ProductFunctions : BaseFunction
{
    [Function("GetProduct")]
    public async Task<HttpResponseData> GetAsync(HttpRequestData req)
    {
        return await ExecuteSafelyAsync<ProductDto>(req, async () =>
        {
            var id = int.Parse(req.Query["id"]);
            return await _service.GetAsync(id);
        });
    }
}
```

### Code Reduction Benefits
- **Eliminate 60-80% of boilerplate code** in function implementations
- **Centralize error handling** - no need for try-catch in every function
- **Automatic input validation** with consistent error responses
- **Standardized JSON serialization** across all endpoints
- **Consistent logging patterns** throughout the application

### Function Design Rules
1. **Always inherit from base classes** - never implement infrastructure manually
2. **Focus functions on business logic only** - let infrastructure handle HTTP concerns
3. **Use dependency injection** for all services and validators
4. **Implement specific, action-oriented function names** (avoid generic names like "Run")
5. **Throw business exceptions** - let base classes handle HTTP error responses
6. **Use HttpRequestData/HttpResponseData** pattern for isolated worker model

### Validation Integration
- **Integrate FluentValidation** seamlessly with base classes
- **Automatic validation error responses** with structured field-level errors
- **Consistent error format** across all validated endpoints
- **Separation of validation logic** from function implementation

### Error Handling Strategy
- **Centralized exception handling** in base classes
- **Structured error responses** with consistent format
- **Automatic logging** of errors with correlation context
- **Business logic exceptions** automatically converted to appropriate HTTP responses
- **Validation errors** automatically formatted as structured responses

---

## Testing Strategy

### Project Structure
Mirror the main project structure in test project:
```
{ProjectName}.Tests/
├── Functions/          # Function endpoint tests
├── Services/           # Business logic tests
├── Infrastructure/     # Infrastructure layer tests
├── Helpers/           # Utility test classes
├── Dtos/              # DTO validation tests
└── Models/            # Model tests
```

### Testing Frameworks
- **xUnit** - Primary testing framework
- **FluentAssertions** - Assertion library
- **FakeItEasy** - Mocking framework (as indicated by TestsBase)
- **Microsoft.EntityFrameworkCore.InMemory** - In-memory database for unit tests

### Test Naming Convention
```csharp
[Fact]
public async Task GetUserAsync_WithValidId_ReturnsUser()
{
    // Method_Scenario_ExpectedResult
}

[Theory]
[InlineData(1, "John")]
[InlineData(2, "Jane")]
public async Task GetUserAsync_WithMultipleIds_ReturnsCorrectUsers(int id, string expectedName)
{
    // Theory tests for multiple inputs
}
```

### Test Categories
1. **Unit Tests**: Test individual components in isolation
2. **API Tests**: End-to-end function testing
3. **Smoke Tests**: Basic functionality verification

---

## Documentation Standards

### Code Documentation
- Use XML documentation comments for public APIs
- Include examples in documentation
- Document complex business logic
- Keep documentation up-to-date with code changes

### README Requirements
- Project description and purpose
- Setup and installation instructions
- Configuration requirements
- API documentation
- Testing instructions
- Deployment procedures

### Task Management Integration
- Commit changes when completing a task in task-manager
- Include task ID and summary in commit message
- Follow format: `task(#ID): Summary of completed work`
- Reference any related issues or pull requests in commit body
- Ensure all automated tests pass before committing

---


*This document should be treated as a living document and updated as the project evolves and new patterns emerge.*
