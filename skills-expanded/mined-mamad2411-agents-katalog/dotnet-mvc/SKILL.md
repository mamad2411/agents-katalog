---
name: dotnet-mvc
description: >
  OPT-IN ONLY. ASP.NET Core MVC, Razor, Controllers, server-rendered UI. Use ONLY when the
  user explicitly chose or is building an MVC/Razor/Controllers+Views app, or adds a separate
  MVC web project. Do NOT use for API-only, Minimal API, REST, or this repo’s src/Api (use
  dotnet-api-endpoint). Do NOT use just because the project is "ASP.NET Core" or "web".
metadata:
  author: Claude-DotNet-Ultimate
  version: 1.1.0
  category: web-ui
---

# .NET MVC + Microsoft Standards

## When to use this skill (all must be consistent)

Load **`dotnet-mvc`** only if **at least one** of these is true:

- The user **explicitly** asked for **MVC**, **Razor** (views/pages), **Controllers + Views**, **server-rendered HTML**, or **`AddControllersWithViews`** / **`MapControllerRoute`**.
- The user is **adding** a **separate** `*.Web` MVC project (not the same as Minimal API in `src/Api/`).
- The user is **comparing** MVC vs Minimal API and wants MVC-side guidance.

If the user **started** or **chose** an **API** / **Minimal API** / **REST** solution (as in this repository), use **`dotnet-api-endpoint`**, **`dotnet-cqrs-feature`**, and other non-MVC skills — **not** this skill.

## Do not use this skill (default for API projects)

- **This repository**: HTTP in **`src/Api/`** is **Minimal API** — use **`dotnet-api-endpoint`**, not `dotnet-mvc`.
- **API-only** or **backend-only** work: OpenAPI, JSON endpoints, `MapGet`/`MapPost`, MediatR from Minimal APIs — **not** this skill.
- Vague phrasing like "web app" when the solution is **already API** — follow **`dotnet-api-endpoint`** unless the user **switches** to MVC.
- "Controller" in **MediatR** or **API controller** in another template — if the user means **Minimal API** here, use **`dotnet-api-endpoint`**.

The body below applies to **MVC/Razor** projects only; it is **not** the default path for this monorepo.

---

Use this skill for **controller-based** ASP.NET Core apps, **Razor views/pages**, and typical Microsoft full-stack .NET patterns (DI, EF Core, validation, tests, Azure). It is generalized from the `dotnet-mvc-skill` pack: architecture, naming, controllers, `Program.cs`, repositories, AutoMapper, FluentValidation, and testing.

**This repository (`Claude-DotNet-Ultimate`)** uses **Minimal APIs** in `src/Api/`. For HTTP routes in *this* solution, follow **`dotnet-api-endpoint`**. Use **this** skill only when a **separate** MVC app is intended or the user **explicitly** wants MVC/Controllers/Views.

---

## 1. Project Structure (Microsoft-Recommended)

```
MyApp/
├── MyApp.sln
├── src/
│   ├── MyApp.Web/               ← ASP.NET Core MVC / Razor Pages
│   │   ├── Controllers/
│   │   ├── Views/
│   │   ├── wwwroot/
│   │   ├── Program.cs
│   │   └── appsettings.json
│   ├── MyApp.Application/       ← Business logic / Use Cases (CQRS optional)
│   │   ├── Interfaces/
│   │   ├── Services/
│   │   └── DTOs/
│   ├── MyApp.Domain/            ← Domain entities, value objects
│   │   ├── Entities/
│   │   └── Enums/
│   └── MyApp.Infrastructure/    ← EF Core, external services, repos
│       ├── Data/
│       │   ├── AppDbContext.cs
│       │   └── Migrations/
│       └── Repositories/
└── tests/
    ├── MyApp.UnitTests/
    └── MyApp.IntegrationTests/
```

**Rule:** Always separate concerns across layers. The Web project references Application; Application references Domain; Infrastructure references Domain and Application. Never let Domain reference any other layer.

---

## 2. Microsoft C# Naming Conventions

| Element            | Convention         | Example                        |
|--------------------|--------------------|--------------------------------|
| Namespace          | PascalCase         | `MyApp.Application.Services`  |
| Class              | PascalCase         | `ProductService`               |
| Interface          | I + PascalCase     | `IProductRepository`           |
| Method             | PascalCase         | `GetAllProductsAsync()`        |
| Property           | PascalCase         | `ProductName`                  |
| Private field      | _camelCase         | `_productRepository`           |
| Local variable     | camelCase          | `productList`                  |
| Constant           | PascalCase         | `MaxRetryCount`                |
| Async method       | Suffix Async       | `GetByIdAsync()`               |
| Generic type param | T or TEntity       | `TEntity`                      |

**Always prefer `async/await` over `.Result` or `.Wait()`.**

In **this** repo, `CLAUDE.md` also asks for **explicit types** (no `var` for built-in types like `int`, `string`)—apply that when editing code here.

---

## 3. Controller Standards

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;

    public ProductsController(
        IProductService productService,
        ILogger<ProductsController> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<ProductDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll()
    {
        var products = await _productService.GetAllAsync();
        return Ok(products);
    }

    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(int id)
    {
        var product = await _productService.GetByIdAsync(id);
        if (product is null) return NotFound();
        return Ok(product);
    }
}
```

**Rules:**
- Controllers are thin — no business logic
- Always inject via constructor
- Always document `[ProducesResponseType]`
- Use `IActionResult` or `ActionResult<T>`
- Validate inputs with `ModelState.IsValid` for MVC, `[ApiController]` handles it for APIs

For **MVC (views)** use `Controller` (not `ControllerBase`), return `View()` / `View(model)`, and use `[ValidateAntiForgeryToken]` on POST actions that render forms.

---

## 4. Dependency Injection (Program.cs / .NET 6+)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// --- Services ---
builder.Services.AddControllersWithViews();  // MVC
// builder.Services.AddControllers();        // API only

// EF Core
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Custom services
builder.Services.AddScoped<IProductRepository, ProductRepository>();
builder.Services.AddScoped<IProductService, ProductService>();

// AutoMapper
builder.Services.AddAutoMapper(typeof(MappingProfile));

var app = builder.Build();

// --- Middleware pipeline ---
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
```

**DI Lifetime Rules:**
| Lifetime    | Use When                                      |
|-------------|-----------------------------------------------|
| `Transient` | Lightweight, stateless services               |
| `Scoped`    | Per-request (e.g. EF Core DbContext, repos)   |
| `Singleton` | Caches, configuration wrappers, thread-safe   |

---

## 5. Entity Framework Core

### DbContext

```csharp
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Product> Products { get; set; }
    public DbSet<Category> Categories { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
        base.OnModelCreating(modelBuilder);
    }
}
```

### Entity Configuration (Fluent API over Data Annotations)

```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.HasKey(p => p.Id);
        builder.Property(p => p.Name).IsRequired().HasMaxLength(200);
        builder.Property(p => p.Price).HasColumnType("decimal(18,2)");
        builder.HasOne(p => p.Category)
               .WithMany(c => c.Products)
               .HasForeignKey(p => p.CategoryId);
    }
}
```

### Migrations

```bash
# Add migration
dotnet ef migrations add InitialCreate --project MyApp.Infrastructure --startup-project MyApp.Web

# Apply migrations
dotnet ef database update --project MyApp.Infrastructure --startup-project MyApp.Web
```

---

## 6. Repository Pattern

```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task AddAsync(T entity);
    void Update(T entity);
    void Delete(T entity);
    Task SaveChangesAsync();
}

public class Repository<T> : IRepository<T> where T : class
{
    protected readonly AppDbContext _context;

    public Repository(AppDbContext context) => _context = context;

    public async Task<T?> GetByIdAsync(int id) =>
        await _context.Set<T>().FindAsync(id);

    public async Task<IEnumerable<T>> GetAllAsync() =>
        await _context.Set<T>().ToListAsync();

    public async Task AddAsync(T entity) =>
        await _context.Set<T>().AddAsync(entity);

    public void Update(T entity) => _context.Set<T>().Update(entity);

    public void Delete(T entity) => _context.Set<T>().Remove(entity);

    public async Task SaveChangesAsync() =>
        await _context.SaveChangesAsync();
}
```

> **Note:** The **this** solution also defines generic `IReadRepository` / `IWriteRepository` with specifications. See `docs/GenericRepositories.md` when working in that codebase.

---

## 7. AutoMapper (DTO Mapping)

```csharp
// DTO
public record ProductDto(int Id, string Name, decimal Price, string CategoryName);

// Profile
public class MappingProfile : Profile
{
    public MappingProfile()
    {
        CreateMap<Product, ProductDto>()
            .ForMember(dest => dest.CategoryName,
                       opt => opt.MapFrom(src => src.Category.Name));

        CreateMap<CreateProductRequest, Product>();
    }
}
```

---

## 8. Validation with FluentValidation

```csharp
public class CreateProductValidator : AbstractValidator<CreateProductRequest>
{
    public CreateProductValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required.")
            .MaximumLength(200);

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Price must be positive.");
    }
}

// Register in Program.cs
builder.Services.AddFluentValidationAutoValidation();
builder.Services.AddValidatorsFromAssemblyContaining<CreateProductValidator>();
```

---

## 9. Global Error Handling

```csharp
// Middleware: GlobalExceptionMiddleware.cs
public class GlobalExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<GlobalExceptionMiddleware> _logger;

    public GlobalExceptionMiddleware(RequestDelegate next,
        ILogger<GlobalExceptionMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception occurred.");
            context.Response.StatusCode = StatusCodes.Status500InternalServerError;
            context.Response.ContentType = "application/json";
            var error = new { message = "An unexpected error occurred." };
            await context.Response.WriteAsJsonAsync(error);
        }
    }
}

// Register in Program.cs
app.UseMiddleware<GlobalExceptionMiddleware>();
```

---

## 10. appsettings.json Structure

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=MyAppDb;Trusted_Connection=True;"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  },
  "AppSettings": {
    "JwtSecret": "",
    "TokenExpiryMinutes": 60,
    "AllowedOrigins": ["https://myapp.com"]
  }
}
```

**Never commit secrets.** Use `dotnet user-secrets` locally and Azure Key Vault in production.

---

## 11. Unit Testing (xUnit + Moq)

```csharp
public class ProductServiceTests
{
    private readonly Mock<IProductRepository> _repoMock;
    private readonly Mock<IMapper> _mapperMock;
    private readonly ProductService _service;

    public ProductServiceTests()
    {
        _repoMock = new Mock<IProductRepository>();
        _mapperMock = new Mock<IMapper>();
        _service = new ProductService(_repoMock.Object, _mapperMock.Object);
    }

    [Fact]
    public async Task GetByIdAsync_WhenProductExists_ReturnsDto()
    {
        // Arrange
        var product = new Product { Id = 1, Name = "Widget" };
        var dto = new ProductDto(1, "Widget", 9.99m, "Electronics");
        _repoMock.Setup(r => r.GetByIdAsync(1)).ReturnsAsync(product);
        _mapperMock.Setup(m => m.Map<ProductDto>(product)).Returns(dto);

        // Act
        var result = await _service.GetByIdAsync(1);

        // Assert
        Assert.NotNull(result);
        Assert.Equal("Widget", result.Name);
    }

    [Fact]
    public async Task GetByIdAsync_WhenNotFound_ReturnsNull()
    {
        _repoMock.Setup(r => r.GetByIdAsync(99)).ReturnsAsync((Product?)null);
        var result = await _service.GetByIdAsync(99);
        Assert.Null(result);
    }
}
```

---

## 12. Key NuGet Packages (Microsoft Standards)

| Package                                  | Purpose                          |
|------------------------------------------|----------------------------------|
| `Microsoft.EntityFrameworkCore.SqlServer`| EF Core + SQL Server             |
| `Microsoft.EntityFrameworkCore.Tools`    | Migrations CLI                   |
| `AutoMapper.Extensions.Microsoft.DependencyInjection` | Object mapping     |
| `FluentValidation.AspNetCore`            | Input validation                 |
| `Serilog.AspNetCore`                     | Structured logging               |
| `xunit` + `Moq`                          | Unit testing + mocking           |
| `Microsoft.AspNetCore.Authentication.JwtBearer` | JWT auth                 |
| `Swashbuckle.AspNetCore`                 | Swagger / OpenAPI docs           |
| `Microsoft.Extensions.Caching.StackExchangeRedis` | Redis caching         |

---

## 13. Azure-Ready Checklist

- [ ] Connection strings in Azure App Configuration / Key Vault
- [ ] Managed Identity for DB auth (no passwords in code)
- [ ] Health check endpoint: `app.MapHealthChecks("/health")`
- [ ] Application Insights: `builder.Services.AddApplicationInsightsTelemetry()`
- [ ] Docker support: `Dockerfile` + `.dockerignore`
- [ ] GitHub Actions / Azure DevOps pipeline for CI/CD
- [ ] EF Core migrations run at startup or via pipeline, never manually in prod

---

## Reference Files (Progressive Disclosure)

Read these in `.claude/skills/dotnet-mvc/references/` (or `.qoder/skills/dotnet-mvc/references/`) when you need more depth:

| File | Content |
|------|---------|
| `references/razor-views.md` | Razor syntax, tag helpers, partials, view components |
| `references/identity-auth.md` | Identity, JWT, OAuth2, roles and claims |
| `references/cqrs-mediatr.md` | MediatR, CQRS, pipeline behaviors |
| `references/minimal-api.md` | Minimal APIs vs MVC; link to this repo’s Minimal API skill |
| `references/azure-deploy.md` | Docker, GitHub Actions, health checks, Key Vault, App Service |

For **Qoder** workflows on Microsoft stack, MVC, Razor, or Controllers, load **`dotnet-mvc`** before generating or reviewing that code.
