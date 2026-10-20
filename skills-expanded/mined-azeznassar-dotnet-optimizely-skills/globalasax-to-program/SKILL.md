---
name: globalasax-to-program
version: 1.0.0
category: Migration/Build
description: Rewrite Global.asax application lifecycle events and EPiServer Global class overrides to ASP.NET Core equivalents in Program.cs, middleware, IStartupFilter, and IHostedService. Critical for .NET 4 to .NET 8 migration.
compatibility: .NET 4.x → .NET 8, ASP.NET Core
---

# Global.asax to Program.cs Migration

## Trigger On

- "migrate Global.asax"
- "convert Application_Start"
- "rewrite EPiServer Global"
- "move bootstrap code to Program.cs"
- "convert Application_Error handler"

## Event Mapping

| Global.asax Event | ASP.NET Core Equivalent |
|---|---|
| `Application_Start` | `Program.cs` service registration + `IHostedService.StartAsync` |
| `Application_End` | `IHostedService.StopAsync` or `IApplicationLifetime.ApplicationStopping` |
| `Application_Error` | Exception handling middleware |
| `Application_BeginRequest` | Middleware `app.Use(...)` |
| `Application_EndRequest` | Middleware `app.Use(...)` after `await next()` |
| `Application_AuthenticateRequest` | `app.UseAuthentication()` |
| `Application_AuthorizeRequest` | `app.UseAuthorization()` |
| `Session_Start` | Not directly equivalent — use distributed cache |
| `Session_End` | Not directly equivalent |

## Application_Start → Program.cs

```csharp
// OLD: Global.asax.cs
public class MvcApplication : EPiServer.Global
{
    protected override void RegisterRoutes(RouteCollection routes)
    {
        routes.MapRoute("Default", "{controller}/{action}/{id}",
            new { controller = "Home", action = "Index", id = "" });
    }

    protected void Application_Start()
    {
        AreaRegistration.RegisterAllAreas();
        RouteConfig.RegisterRoutes(RouteTable.Routes);
        FilterConfig.RegisterGlobalFilters(GlobalFilters.Filters);
        BundleConfig.RegisterBundles(BundleTable.Bundles);
    }
}

// NEW: Program.cs
var builder = WebApplication.CreateBuilder(args);

builder.Services
    .AddCms()
    .AddCmsAspNetUi()
    .AddControllersWithViews();

// Global filters → use AddControllersWithViews().AddMvcOptions()
builder.Services.AddControllersWithViews(options =>
{
    options.Filters.Add<MyGlobalFilter>();
});

var app = builder.Build();

// Routes
app.UseEndpoints(endpoints =>
{
    endpoints.MapControllerRoute("default", "{controller=Home}/{action=Index}/{id?}");
    endpoints.MapContent(); // Optimizely routing
});

app.Run();
```

## Application_Error → Exception Middleware

```csharp
// OLD: Global.asax.cs
protected void Application_Error()
{
    var exception = Server.GetLastError();
    Log.Error("Unhandled exception", exception);
    Server.ClearError();
    Response.Redirect("/Error");
}

// NEW: Middleware in Program.cs
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler(errorApp =>
    {
        errorApp.Run(async context =>
        {
            var exceptionFeature = context.Features.Get<IExceptionHandlerFeature>();
            if (exceptionFeature?.Error != null)
            {
                var logger = context.RequestServices
                    .GetRequiredService<ILogger<Program>>();
                logger.LogError(exceptionFeature.Error, "Unhandled exception");
            }
            context.Response.Redirect("/Error");
        });
    });
}
```

## Application_BeginRequest → Middleware

```csharp
// OLD: Global.asax.cs
protected void Application_BeginRequest()
{
    // Set culture from cookie
    var cultureName = Request.Cookies["culture"]?.Value ?? "en";
    Thread.CurrentThread.CurrentCulture = new CultureInfo(cultureName);
}

// NEW: Custom middleware
public class CultureMiddleware
{
    private readonly RequestDelegate _next;

    public CultureMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context)
    {
        var cultureName = context.Request.Cookies["culture"] ?? "en";
        var culture = new CultureInfo(cultureName);
        CultureInfo.CurrentCulture = culture;
        CultureInfo.CurrentUICulture = culture;
        await _next(context);
    }
}

// Register in Program.cs
app.UseMiddleware<CultureMiddleware>();
```

## Startup Work → IHostedService

```csharp
// OLD: Application_Start one-time work
protected void Application_Start()
{
    WarmUpCache();
    RegisterSearchIndexes();
}

// NEW: IHostedService
public class StartupTasksService : IHostedService
{
    private readonly IServiceProvider _serviceProvider;

    public StartupTasksService(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        using var scope = _serviceProvider.CreateScope();
        var cacheService = scope.ServiceProvider.GetRequiredService<ICacheService>();
        await cacheService.WarmUpAsync(cancellationToken);
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}

// Register in Program.cs
builder.Services.AddHostedService<StartupTasksService>();
```

## EPiServer.Global → IInitializableModule

```csharp
// OLD: Overriding EPiServer.Global methods
public class MvcApplication : EPiServer.Global
{
    protected override void RegisterRoutes(RouteCollection routes) { }
    protected override void InitComplete() { /* post-init work */ }
}

// NEW: IInitializableModule
[InitializableModule]
[ModuleDependency(typeof(EPiServer.Web.InitializationModule))]
public class SiteInitializationModule : IInitializableModule
{
    public void Initialize(InitializationEngine context)
    {
        // Post-init work (equivalent to InitComplete)
        var events = context.Locate.ContentEvents();
        events.PublishedContent += OnContentPublished;
    }

    public void Uninitialize(InitializationEngine context)
    {
        var events = context.Locate.ContentEvents();
        events.PublishedContent -= OnContentPublished;
    }

    private void OnContentPublished(object sender, ContentEventArgs e) { }
}
```
