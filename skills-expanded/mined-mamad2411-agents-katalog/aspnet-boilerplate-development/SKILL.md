---
name: aspnet-boilerplate-development
description: Expert guidance for ASP.NET Boilerplate (ABP) and .NET 10.0 development for the EAF (Enterprise Application Foundation) middleware modules. Covers N-Layer Architecture, dependency injection with Castle Windsor, multi-tenancy, authorization, caching, background jobs, Entity Framework Core, EAF-specific middleware modules (Serilog, KeyVault, OpenTelemetry, SQL Server/SQLite cache), and ABP best practices. Use this skill when developing EAF middleware modules, working with ABP framework, implementing repositories/application services, or troubleshooting ABP-related issues. Do NOT use for general .NET development, non-ABP projects, or frontend development.
---

# ASP.NET Boilerplate Development Skill - EAF Middleware

You are an expert in ASP.NET Boilerplate (ABP), .NET 10.0, and the EAF (Enterprise Application Foundation) middleware modules. You write functional, maintainable, performant, and scalable code following ABP and .NET best practices.

## Project Context

The EAF project is based on ASP.NET Boilerplate (ABP) framework with custom middleware modules located in the `src` directory. These modules provide enterprise-grade functionality for ABP-based applications.

### Current State
- **.NET Version**: 10.0
- **ABP Version**: Custom EAF implementation based on ABP
- **Database**: SQL Server and SQLite support
- **Architecture**: N-Layer Architecture (Domain, Application, Infrastructure layers)

### EAF Middleware Modules (src/)
- `Eaf.Castle.Serilog` - Serilog logging integration with Castle Windsor
- `Eaf.KeyVault` - Azure Key Vault integration
- `Eaf.KeyVault.AspNetCore` - Azure Key Vault ASP.NET Core integration
- `Eaf.Log4NetServiceBus` - Log4Net with Service Bus integration
- `Eaf.Middleware.Application` - Application layer middleware
- `Eaf.Middleware.AzureActiveDirectory` - Azure AD integration
- `Eaf.Middleware.Core` - Core middleware abstractions
- `Eaf.Middleware.Ldap` - LDAP authentication integration
- `Eaf.Middleware.Web.Core` - Web core middleware
- `Eaf.Middleware.Worker` - Background worker middleware
- `Eaf.OpenTelemetry` - OpenTelemetry observability
- `Eaf.SqlServerCache` - SQL Server distributed cache
- `Eaf.SqliteCache` - SQLite distributed cache

## ASP.NET Boilerplate Best Practices

### N-Layer Architecture

#### Domain Layer
- **Entities**: Inherit from `Entity`, `AggregateRoot`, or `FullAuditedEntity`
- **Repositories**: Use `IRepository<TEntity, TKey>` for data access
- **Domain Services**: Business logic that doesn't fit in entities
- **Specifications**: Encapsulate query logic
- **Domain Events**: Event-driven architecture with `IDomainEventHandler`
- **Value Objects**: Immutable objects without identity

```csharp
// Entity example
public class User : FullAuditedAggregateRoot<Guid>
{
    public string Name { get; set; }
    public string Email { get; set; }
}

// Repository usage
public class UserAppService : ApplicationService
{
    private readonly IRepository<User, Guid> _userRepository;
    
    public UserAppService(IRepository<User, Guid> userRepository)
    {
        _userRepository = userRepository;
    }
}
```

#### Application Layer
- **Application Services**: Inherit from `ApplicationService` or `IApplicationService`
- **DTOs**: Data Transfer Objects for input/output
- **Validation**: Use `DataAnnotations` or FluentValidation
- **Authorization**: Use `[AbpAuthorize]` attribute
- **Feature Management**: Use `[RequiresFeature]` attribute
- **Audit Logging**: Automatic with `IAuditingStore`

```csharp
// Application Service example
public class UserAppService : ApplicationService, IUserAppService
{
    private readonly IRepository<User, Guid> _userRepository;
    
    [AbpAuthorize("Pages.Users.Create")]
    public async Task CreateUserDto CreateUser(CreateUserDto input)
    {
        var user = ObjectMapper.Map<User>(input);
        await _userRepository.InsertAsync(user);
        return ObjectMapper.Map<UserDto>(user);
    }
}
```

#### Infrastructure Layer
- **Entity Framework**: Use `EfCoreRepositoryBase` for custom repositories
- **Migrations**: Use EF Core migrations
- **Background Jobs**: Hangfire or Quartz integration
- **SignalR**: Real-time notifications
- **Caching**: `ICacheManager` for distributed caching

### Dependency Injection

ABP uses Castle Windsor for dependency injection. Follow these patterns:

```csharp
// Constructor injection
public class MyService : ITransientDependency
{
    private readonly IRepository<User, Guid> _userRepository;
    private readonly ISettingManager _settingManager;
    
    public MyService(IRepository<User, Guid> userRepository, ISettingManager settingManager)
    {
        _userRepository = userRepository;
        _settingManager = settingManager;
    }
}

// Dependency lifecycles
- ITransientDependency: Created each time
- ISingletonDependency: Single instance
- IScopedDependency: Per request scope
```

### Common ABP Services

#### Session Management
```csharp
public class MyService : ITransientDependency
{
    private readonly IAbpSession _abpSession;
    
    public MyService(IAbpSession abpSession)
    {
        _abpSession = abpSession;
    }
    
    public Guid GetCurrentUserId()
    {
        return _abpSession.UserId ?? Guid.Empty;
    }
}
```

#### Setting Management
```csharp
public class MyService : ITransientDependency
{
    private readonly ISettingManager _settingManager;
    
    public async Task<string> GetSettingAsync()
    {
        return await _settingManager.GetSettingValueAsync("MyApp.MySetting");
    }
}
```

#### Caching
```csharp
public class MyService : ITransientDependency
{
    private readonly ICacheManager _cacheManager;
    
    public async Task<User> GetUserAsync(Guid id)
    {
        var cache = _cacheManager.GetCache("Users");
        return await cache.GetAsync(id.ToString(), () => GetUserFromDb(id));
    }
}
```

#### Logging
```csharp
public class MyService : ITransientDependency
{
    private readonly ILogger _logger;
    
    public MyService(ILogger logger)
    {
        _logger = logger;
    }
    
    public void DoSomething()
    {
        _logger.Info("Doing something...");
        _logger.Error("Error occurred", ex);
    }
}
```

### Multi-Tenancy

EAF supports multi-tenancy. Use data filters:

```csharp
// Disable tenant filter for host operations
using (_unitOfWorkManager.Current.DisableFilter(AbpDataFilters.MayHaveTenant))
{
    var hostUsers = await _userRepository.GetAllListAsync();
}

// Set tenant context
using (_unitOfWorkManager.Current.SetTenantId(tenantId))
{
    var tenantUsers = await _userRepository.GetAllListAsync();
}
```

### Authorization

```csharp
// Permission definition
public class AppPermissions
{
    public const string Pages_Users = "Pages.Users";
    public const string Pages_Users_Create = "Pages.Users.Create";
    public const string Pages_Users_Edit = "Pages.Users.Edit";
    public const string Pages_Users_Delete = "Pages.Users.Delete";
}

// Permission usage
[AbpAuthorize(AppPermissions.Pages_Users_Create)]
public async Task CreateUser(CreateUserDto input)
{
    // ...
}

// Check permission programmatically
if (await PermissionChecker.IsGrantedAsync(AppPermissions.Pages_Users_Edit))
{
    // Allow action
}
```

### Background Jobs

```csharp
// Simple background job
public class MyBackgroundJob : BackgroundJob<Args>, ITransientDependency
{
    private readonly IRepository<User, Guid> _userRepository;
    
    public MyBackgroundJob(IRepository<User, Guid> userRepository)
    {
        _userRepository = userRepository;
    }
    
    public override void Execute(Args args)
    {
        var users = _userRepository.GetAllList();
        // Process users
    }
}
```

### Unit of Work

ABP uses Unit of Work pattern automatically:

```csharp
// Automatic UOW in application services
public class UserAppService : ApplicationService
{
    // UOW automatically starts and commits
    public async Task CreateUser(CreateUserDto input)
    {
        var user = ObjectMapper.Map<User>(input);
        await _userRepository.InsertAsync(user);
        // UOW commits here
    }
}

// Manual UOW control
using (var uow = _unitOfWorkManager.Begin())
{
    // Operations
    await uow.CompleteAsync();
}
```

### Object Mapping

Use AutoMapper integrated with ABP:

```csharp
// Define mapping profile
public class MyAutoMapperProfile : Profile
{
    public MyAutoMapperProfile()
    {
        CreateMap<User, UserDto>();
        CreateMap<CreateUserDto, User>();
    }
}

// Use in application service
public class UserAppService : ApplicationService
{
    public async Task<UserDto> CreateUser(CreateUserDto input)
    {
        var user = ObjectMapper.Map<User>(input);
        // ...
        return ObjectMapper.Map<UserDto>(user);
    }
}
```

## EAF-Specific Patterns

### Module Initialization

```csharp
[DependsOn(typeof(AbpKernelModule))]
public class MyEafModule : AbpModule
{
    public override void Initialize()
    {
        IocManager.RegisterAssemblyByConvention(Assembly.GetExecutingAssembly());
    }
}
```

### Serilog Integration (Eaf.Castle.Serilog)

```csharp
[DependsOn(typeof(AbpCastleSerilogModule))]
public class MyModule : AbpModule
{
    public override void Initialize()
    {
        // Serilog is automatically configured
        // Use ILogger from Castle Windsor
    }
}
```

### Key Vault Integration (Eaf.KeyVault)

```csharp
public class MyService : ITransientDependency
{
    private readonly IEafKeyVaultManager _keyVaultManager;
    
    public MyService(IEafKeyVaultManager keyVaultManager)
    {
        _keyVaultManager = keyVaultManager;
    }
    
    public async Task<string> GetSecretAsync(string secretName)
    {
        return await _keyVaultManager.GetSecretAsync(secretName);
    }
}
```

### OpenTelemetry Integration (Eaf.OpenTelemetry)

```csharp
[DependsOn(typeof(EafOpenTelemetryModule))]
public class MyModule : AbpModule
{
    public override void Initialize()
    {
        // OpenTelemetry is automatically configured
        // Metrics, traces, and logs are collected
    }
}
```

### SQL Server Cache (Eaf.SqlServerCache)

```csharp
[DependsOn(typeof(AbpRedisCacheModule), typeof(EafSqlServerCacheModule))]
public class MyModule : AbpModule
{
    // SQL Server distributed cache is configured
    // Falls back to Redis if available
}
```

## Database Best Practices

### Entity Framework Core

```csharp
// DbContext configuration
public class MyDbContext : AbpDbContext
{
    public DbSet<User> Users { get; set; }
    
    public MyDbContext(DbContextOptions<MyDbContext> options)
        : base(options)
    {
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        
        modelBuilder.Entity<User>(b =>
        {
            b.ToTable("Users");
            b.ConfigureByConvention();
        });
    }
}
```

### Repository Customization

```csharp
public interface IUserRepository : IRepository<User, Guid>
{
    Task<User> GetByEmailAsync(string email);
}

public class UserRepository : EfCoreRepositoryBase<MyDbContext, User, Guid>, IUserRepository
{
    public UserRepository(IDbContextProvider<MyDbContext> dbContextProvider)
        : base(dbContextProvider)
    {
    }
    
    public async Task<User> GetByEmailAsync(string email)
    {
        return await DbSet.FirstOrDefaultAsync(u => u.Email == email);
    }
}
```

## Configuration

### appsettings.json

```json
{
  "ConnectionStrings": {
    "Default": "Server=localhost;Database=EafDb;Trusted_Connection=True"
  },
  "App": {
    "WebSiteRootAddress": "http://localhost:62134/"
  },
  "Redis": {
    "Configuration": "localhost:6379"
  }
}
```

### Module Configuration

```csharp
[DependsOn(typeof(AbpKernelModule))]
public class MyModule : AbpModule
{
    public override void PreInitialize()
    {
        Configuration.Modules.AbpAutoMapper().Configurators.Add(configuration =>
        {
            // Custom AutoMapper configuration
        });
    }
}
```

## Testing

### Unit Tests

```csharp
public class UserAppService_Tests : AbpIntegratedTestBase
{
    private readonly IUserAppService _userAppService;
    
    public UserAppService_Tests()
    {
        _userAppService = Resolve<IUserAppService>();
    }
    
    [Fact]
    public async Task Should_Create_User()
    {
        // Act
        var result = await _userAppService.CreateUser(new CreateUserDto { Name = "Test" });
        
        // Assert
        result.Name.ShouldBe("Test");
    }
}
```

## Common Issues and Solutions

### Circular Dependency
- Use property injection instead of constructor injection
- Split services into smaller, more focused services
- Use lazy initialization with `Lazy<T>`

### Performance Issues
- Use caching for frequently accessed data
- Optimize database queries with projections
- Use `IQueryable` for database-side operations
- Consider background jobs for long-running tasks

### Multi-Tenancy Issues
- Always check tenant context before data access
- Use data filters appropriately
- Test both host and tenant scenarios

## File Naming Conventions

- Entities: `EntityName.cs` in `Entities` folder
- DTOs: `EntityNameDto.cs` in `Dtos` folder
- Application Services: `EntityNameAppService.cs` in `AppServices` folder
- Interfaces: `IEntityName.cs` in same folder as implementation
- Use PascalCase for class names
- Use camelCase for method parameters

## When in Doubt

- Follow ABP conventions over custom patterns
- Check ABP documentation at https://aspnetboilerplate.com/Pages/Documents
- Use dependency injection properly
- Keep services small and focused
- Test thoroughly before committing
- Maintain consistency with existing EAF modules
