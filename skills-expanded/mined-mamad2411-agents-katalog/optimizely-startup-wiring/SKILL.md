---
name: optimizely-startup-wiring
version: 1.0.0
category: Migration/Build
description: Generate correct Optimizely CMS 12 Program.cs and service registration. Covers AddCms(), middleware pipeline order, routing, and essential service registrations. Use when bootstrapping a fresh CMS 12 project.
compatibility: Optimizely CMS 12, EPiServer.CMS.Web 12.x, .NET 6+
---

# Optimizely CMS 12 Startup Wiring

## Trigger On

- "set up Program.cs for Optimizely"
- "configure CMS 12 startup"
- "wire up AddCms"
- "migrate Global.asax / Startup.cs to CMS 12"
- "configure middleware pipeline"
- any new CMS 12 project bootstrap task

## Documentation

- [Initialization in CMS 12](https://docs.developers.optimizely.com/content-management-system/docs/initialization)
- [Dependency Injection in CMS 12](https://docs.developers.optimizely.com/content-management-system/docs/dependency-injection)
- [Configuring CMS](https://docs.developers.optimizely.com/content-management-system/docs/configuring-cms)

## Required NuGet Packages

```xml
<PackageReference Include="EPiServer.CMS.Web" Version="12.*" />
<PackageReference Include="EPiServer.CMS.TinyMce" Version="*" />
<PackageReference Include="EPiServer.CMS.UI.AspNetCore" Version="12.*" />
<PackageReference Include="EPiServer.Hosting" Version="*" />
<PackageReference Include="Microsoft.Extensions.Hosting" Version="*" />
```

## Minimal Program.cs

```csharp
using EPiServer.Cms.UI.AspNetCore;
using EPiServer.DependencyInjection;
using EPiServer.Web.Routing;

var builder = WebApplication.CreateBuilder(args);

builder.Services
    .AddCmsAspNetUi()
    .AddCms()
    .AddAlloy()              // or your site's extension method
    .AddTinyMce();

builder.Services
    .AddControllersWithViews();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

app.UseEndpoints(endpoints =>
{
    endpoints.MapControllerRoute(
        name: "default",
        pattern: "{controller}/{action}/{id?}");
    endpoints.MapControllers();
    endpoints.MapContent();   // Optimizely content routing
});

app.Run();
```

## Full Production Program.cs

```csharp
using EPiServer.Cms.UI.AspNetCore;
using EPiServer.DependencyInjection;
using EPiServer.Framework.Cache;
using EPiServer.Web.Routing;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// --- Optimizely CMS Core ---
builder.Services.AddCms();
builder.Services.AddCmsAspNetUi();

// --- UI / Editor ---
builder.Services.AddTinyMce();
builder.Services.Configure<TinyMceConfiguration>(config =>
{
    config.Default()
        .AddPlugin("link image")
        .Toolbar("formatselect | bold italic | link image | bullist numlist");
});

// --- MVC ---
builder.Services
    .AddControllersWithViews()
    .AddRazorRuntimeCompilation();  // remove in production

// --- Scheduled Jobs ---
builder.Services.Configure<SchedulerOptions>(o => { o.Enabled = true; });

// --- Site-specific registrations ---
builder.Services.AddSingleton<IMyService, MyService>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

app.UseEndpoints(endpoints =>
{
    endpoints.MapControllerRoute("default", "{controller}/{action}/{id?}");
    endpoints.MapControllers();
    endpoints.MapContent();
});

app.Run();
```

## appsettings.json Structure

```json
{
  "Episerver": {
    "ConnectionStrings": {
      "EPiServerDB": "Server=.;Database=MyCmsDb;Trusted_Connection=True;"
    }
  },
  "EPiServer": {
    "CMS": {
      "Scheduler": {
        "Enabled": true
      }
    }
  },
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "EPiServer": "Warning"
    }
  }
}
```

## Middleware Order Rules

The following order is REQUIRED — deviating causes auth or routing failures:

1. `UseExceptionHandler` / `UseDeveloperExceptionPage`
2. `UseHsts`
3. `UseHttpsRedirection`
4. `UseStaticFiles`
5. `UseRouting`
6. `UseAuthentication`   ← must be before Authorization
7. `UseAuthorization`    ← must be after Authentication
8. `UseEndpoints`        ← must include `MapContent()` for CMS routing

## Common Mistakes

```csharp
// WRONG - MapContent() missing, pages won't route
app.UseEndpoints(endpoints =>
{
    endpoints.MapDefaultControllerRoute();
    // missing: endpoints.MapContent()
});

// WRONG - UseAuthentication after UseAuthorization
app.UseAuthorization();
app.UseAuthentication(); // too late

// WRONG - Old Startup.cs style with IInitializableHttpModule
// IInitializableHttpModule is REMOVED in CMS 12
// Replace with IStartupFilter or IHostedService

// WRONG - Global.asax Application_Start
// No equivalent - all logic moves to Program.cs or IInitializableModule
```

## IInitializableModule (still supported)

```csharp
[InitializableModule]
[ModuleDependency(typeof(EPiServer.Web.InitializationModule))]
public class MySiteInitialization : IInitializableModule
{
    public void Initialize(InitializationEngine context)
    {
        // Wire up events, register handlers
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

## IConfigurableModule (for DI registration in modules)

```csharp
[InitializableModule]
public class DependencyRegistrationModule : IConfigurableModule
{
    public void ConfigureContainer(ServiceConfigurationContext context)
    {
        context.Services.AddTransient<IMyService, MyService>();
    }

    public void Initialize(InitializationEngine context) { }
    public void Uninitialize(InitializationEngine context) { }
}
```
