---
name: optimizely-di-registration
version: 1.0.0
category: Migration/Build
description: Register services in Optimizely CMS 12 using IServiceCollection. Covers migration from StructureMap/Castle Windsor/Autofac to built-in ASP.NET Core DI, IConfigurableModule registration, and ServiceLocator usage patterns.
compatibility: Optimizely CMS 12, .NET 6+
---

# Optimizely CMS 12 DI Registration

## Trigger On

- "register a service in CMS 12"
- "migrate StructureMap to IServiceCollection"
- "configure dependency injection Optimizely"
- "replace ServiceLocator"
- "IConfigurableModule registration"

## Documentation

- [Dependency Injection in CMS 12](https://docs.developers.optimizely.com/content-management-system/docs/dependency-injection)
- [Breaking Changes CMS 11 → 12](https://docs.developers.optimizely.com/content-management-system/docs/breaking-changes-in-content-cloud-cms-12)

## Standard Registration in Program.cs

```csharp
builder.Services.AddSingleton<IMyService, MyService>();
builder.Services.AddTransient<IMyRepository, MyRepository>();
builder.Services.AddScoped<IMyUnitOfWork, MyUnitOfWork>();
```

## Registration via IConfigurableModule

```csharp
[InitializableModule]
public class MyDependencyModule : IConfigurableModule
{
    public void ConfigureContainer(ServiceConfigurationContext context)
    {
        context.Services.AddTransient<IMyService, MyService>();
        context.Services.AddSingleton<IMyCache, MyCache>();

        // Intercept/override existing registrations
        context.Services.AddTransient<IContentRenderer, MyCustomRenderer>();
    }

    public void Initialize(InitializationEngine context) { }
    public void Uninitialize(InitializationEngine context) { }
}
```

## Migrating from StructureMap

```csharp
// OLD - StructureMap (CMS 11)
For<IMyService>().Use<MyService>().Singleton();
For<IMyRepository>().Use<MyRepository>().Transient();
For<IMyService>().Use<MyService>().ContainerScoped();

// NEW - IServiceCollection (CMS 12)
services.AddSingleton<IMyService, MyService>();
services.AddTransient<IMyRepository, MyRepository>();
services.AddScoped<IMyService, MyService>();
```

## ServiceLocator — When Still Acceptable

```csharp
// In non-DI contexts only (e.g. static helpers being migrated)
// PREFER constructor injection always

// Correct scope for background/scheduled work:
using var scope = ServiceLocator.Current.CreateServiceLocatorScope();
var service = scope.ServiceProvider.GetRequiredService<IMyService>();

// NOT just:
var service = ServiceLocator.Current.GetInstance<IMyService>(); // unsafe outside web request
```

## Constructor Injection (preferred everywhere)

```csharp
public class ArticlePageController : PageController<ArticlePage>
{
    private readonly IContentRepository _contentRepository;
    private readonly IContentLoader _contentLoader;
    private readonly IUrlResolver _urlResolver;

    public ArticlePageController(
        IContentRepository contentRepository,
        IContentLoader contentLoader,
        IUrlResolver urlResolver)
    {
        _contentRepository = contentRepository;
        _contentLoader = contentLoader;
        _urlResolver = urlResolver;
    }
}
```

## Key Built-in Optimizely Services

| Service Interface | Purpose |
|---|---|
| `IContentRepository` | CRUD on content (save, move, delete) |
| `IContentLoader` | Read-only content access (faster) |
| `IUrlResolver` | Resolve content to URLs and back |
| `IContentTypeRepository` | Content type metadata |
| `ILanguageBranchRepository` | Language branch management |
| `IContentEvents` | Subscribe to publish/save/delete events |
| `IBlobFactory` | Media/file blob storage |
| `IContentVersionRepository` | Version history |
| `IPublishedStateAssessor` | Check published state of content |

## Anti-Patterns

```csharp
// WRONG - StructureMap in CMS 12
ObjectFactory.Configure(x => x.For<IMyService>().Use<MyService>());

// WRONG - Castle Windsor in CMS 12
container.Register(Component.For<IMyService>().ImplementedBy<MyService>());

// WRONG - ServiceLocator inside constructor
public class MyController : Controller
{
    public MyController()
    {
        _service = ServiceLocator.Current.GetInstance<IMyService>(); // use constructor DI
    }
}

// WRONG - Creating scope without disposing
var scope = ServiceLocator.Current.CreateServiceLocatorScope();
var service = scope.ServiceProvider.GetRequiredService<IMyService>();
// missing: scope.Dispose() → use `using`
```
