---
name: legacy-ioc-to-di
version: 1.0.0
category: Migration/Build
description: Migrate StructureMap, Castle Windsor, and Autofac IoC container registrations to ASP.NET Core built-in IServiceCollection DI. Covers lifetime mapping, named registrations, decorators, and factory patterns.
compatibility: .NET 4.x → .NET 8, ASP.NET Core. StructureMap 4.x, Windsor 5.x, Autofac 4.x → Microsoft.Extensions.DependencyInjection.
---

# Legacy IoC to ASP.NET Core DI

## Trigger On

- "migrate StructureMap"
- "remove Castle Windsor"
- "replace Autofac container"
- "convert IoC registrations"
- "migrate ObjectFactory"
- "DI container migration"

## Lifetime Mapping

| Concept | StructureMap | Windsor | Autofac | ASP.NET Core DI |
|---|---|---|---|---|
| One per request | `.ContainerScoped()` | `LifestylePerWebRequest()` | `.InstancePerRequest()` | `AddScoped<>()` |
| Single instance | `.Singleton()` | `LifestyleSingleton()` | `.SingleInstance()` | `AddSingleton<>()` |
| New each time | `.Transient()` | `LifestyleTransient()` | `.InstancePerDependency()` | `AddTransient<>()` |

## StructureMap Migration

```csharp
// OLD: StructureMap registry
public class MyRegistry : Registry
{
    public MyRegistry()
    {
        For<IMyService>().Use<MyService>().Singleton();
        For<IMyRepository>().Use<MyRepository>().Transient();
        For<IUnitOfWork>().Use<UnitOfWork>().ContainerScoped();
        For<ILogger>().Use(ctx => LogManager.GetLogger("App")).Singleton();
    }
}

// OLD: Bootstrap
ObjectFactory.Configure(c => c.AddRegistry<MyRegistry>());
var service = ObjectFactory.GetInstance<IMyService>();

// NEW: IServiceCollection
builder.Services.AddSingleton<IMyService, MyService>();
builder.Services.AddTransient<IMyRepository, MyRepository>();
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
builder.Services.AddSingleton<ILogger>(sp =>
    LoggerFactory.Create(b => b.AddConsole()).CreateLogger("App"));
```

## Castle Windsor Migration

```csharp
// OLD: Windsor installer
public class ServicesInstaller : IWindsorInstaller
{
    public void Install(IWindsorContainer container, IConfigurationStore store)
    {
        container.Register(
            Component.For<IMyService>().ImplementedBy<MyService>().LifestyleSingleton(),
            Component.For<IMyRepository>().ImplementedBy<MyRepository>().LifestyleTransient(),
            Classes.FromThisAssembly().BasedOn<IController>().LifestyleTransient()
        );
    }
}

// NEW: IServiceCollection
builder.Services.AddSingleton<IMyService, MyService>();
builder.Services.AddTransient<IMyRepository, MyRepository>();
builder.Services.AddControllersWithViews(); // handles controller registration
```

## Autofac Migration

```csharp
// OLD: Autofac module
public class AppModule : Module
{
    protected override void Load(ContainerBuilder builder)
    {
        builder.RegisterType<MyService>().As<IMyService>().SingleInstance();
        builder.RegisterType<MyRepository>().As<IMyRepository>().InstancePerDependency();
        builder.RegisterType<UnitOfWork>().As<IUnitOfWork>().InstancePerRequest();

        // Assembly scanning
        builder.RegisterAssemblyTypes(ThisAssembly)
            .Where(t => t.Name.EndsWith("Service"))
            .AsImplementedInterfaces()
            .InstancePerDependency();
    }
}

// NEW: IServiceCollection
builder.Services.AddSingleton<IMyService, MyService>();
builder.Services.AddTransient<IMyRepository, MyRepository>();
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();

// Assembly scanning equivalent
var serviceTypes = Assembly.GetExecutingAssembly()
    .GetTypes()
    .Where(t => t.Name.EndsWith("Service") && !t.IsAbstract);
foreach (var type in serviceTypes)
{
    foreach (var iface in type.GetInterfaces())
        builder.Services.AddTransient(iface, type);
}
```

## Named / Keyed Registrations

```csharp
// OLD: StructureMap named instances
For<ICache>().Use<MemoryCache>().Named("memory");
For<ICache>().Use<RedisCache>().Named("redis");
var cache = ObjectFactory.GetNamedInstance<ICache>("redis");

// NEW: .NET 8 Keyed Services (AddKeyedSingleton)
builder.Services.AddKeyedSingleton<ICache, MemoryCache>("memory");
builder.Services.AddKeyedSingleton<ICache, RedisCache>("redis");

// Inject with [FromKeyedServices]
public class MyController(
    [FromKeyedServices("redis")] ICache cache) { }
```

## Decorator Pattern

```csharp
// NEW: Decorator via Scrutor (recommended NuGet)
// Install: Scrutor

builder.Services.AddTransient<IMyService, MyService>();
builder.Services.Decorate<IMyService, CachedMyService>();
builder.Services.Decorate<IMyService, LoggedMyService>();

// Or manually:
builder.Services.AddTransient<MyService>();
builder.Services.AddTransient<IMyService>(sp =>
    new CachedMyService(sp.GetRequiredService<MyService>()));
```

## Factory Pattern

```csharp
// NEW: Factory via delegate
builder.Services.AddTransient<IMyService>(sp =>
{
    var config = sp.GetRequiredService<IOptions<MyOptions>>().Value;
    return config.UseV2
        ? new MyServiceV2(sp.GetRequiredService<IMyRepo>())
        : new MyServiceV1(sp.GetRequiredService<IMyRepo>());
});
```

## Anti-Patterns

```csharp
// WRONG - StructureMap ObjectFactory in .NET 8
ObjectFactory.GetInstance<IMyService>(); // removed

// WRONG - Windsor container resolve
container.Resolve<IMyService>(); // Windsor not needed

// WRONG - ServiceLocator anti-pattern (still compiles but avoid)
ServiceLocator.Current.GetInstance<IMyService>(); // use constructor injection

// WRONG - Captive dependency (singleton consuming scoped)
builder.Services.AddSingleton<IMySingleton, MySingleton>();
// MySingleton constructor takes IMyRepository (scoped) → runtime error
// Fix: inject IServiceScopeFactory and create scope manually
```
