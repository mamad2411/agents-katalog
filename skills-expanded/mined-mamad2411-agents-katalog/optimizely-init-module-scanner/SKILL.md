---
name: optimizely-init-module-scanner
version: 1.0.0
category: Migration/Audit
description: Scan a legacy Optimizely/EPiServer codebase for IInitializableModule, IConfigurableModule, IInitializableHttpModule, and scheduled jobs. Produces a migration plan for each, flagging CMS 12 breaking changes.
compatibility: Targets EPiServer/Optimizely CMS 10/11 source for CMS 12 migration planning.
---

# Optimizely Init Module Scanner

## Trigger On

- "scan initialization modules"
- "audit IInitializableModule"
- "find all EPiServer modules"
- "what initialization code do I have"
- "audit scheduled jobs"

## Documentation

- [Initialization System CMS 12](https://docs.developers.optimizely.com/content-management-system/docs/initialization)
- [Creating Initialization Modules](https://docs.developers.optimizely.com/content-management-system/docs/creating-an-initialization-module)
- [Breaking Changes CMS 11 → 12](https://docs.developers.optimizely.com/content-management-system/docs/breaking-changes-in-content-cloud-cms-12)

## What to Scan For

### Interfaces to Find

| Interface | CMS 12 Status | Migration Action |
|---|---|---|
| `IInitializableModule` | ✅ Supported | Keep, works via `AddCms()` → `AddCmsHost()` |
| `IConfigurableModule` | ✅ Supported | Keep, use for DI registration |
| `IInitializableHttpModule` | ❌ Removed | Rewrite as `IStartupFilter` or middleware |
| `ScheduledJobBase` | ✅ Supported | Keep, update DI constructor |
| `HttpApplication` event handlers | ❌ Removed | Rewrite as middleware or `IStartupFilter` |

### Attributes to Find

```
[InitializableModule]
[ModuleDependency(typeof(...))]
[ScheduledPlugIn(DisplayName = "...", GUID = "...")]
```

### Patterns to Flag as Broken

```csharp
// BROKEN in CMS 12 - IInitializableHttpModule removed
public class MyModule : IInitializableHttpModule
{
    public void InitializeHttpEvents(HttpApplication application)
    {
        application.BeginRequest += OnBeginRequest; // ❌
    }
}

// BROKEN in CMS 12 - HttpContext.Current
public void Initialize(InitializationEngine context)
{
    var ctx = HttpContext.Current; // ❌ not available at init time
}

// BROKEN - ServiceLocator pattern outside web request
var service = ServiceLocator.Current.GetInstance<IMyService>();
// Must use CreateServiceLocatorScope() in CMS 12 outside web context
```

## Output Format

```json
{
  "initializationModules": [
    {
      "className": "SearchInitialization",
      "interfaces": ["IInitializableModule", "IConfigurableModule"],
      "dependencies": ["EPiServer.Web.InitializationModule"],
      "actions": ["RegistersSearchIndex", "SubscribesToPublishEvent"],
      "cms12Status": "compatible",
      "migrationNotes": "Move DI registrations to ConfigureContainer, keep event wiring in Initialize"
    },
    {
      "className": "LegacyHttpModule",
      "interfaces": ["IInitializableHttpModule"],
      "cms12Status": "BREAKING",
      "migrationNotes": "Rewrite as ASP.NET Core middleware or IStartupFilter"
    }
  ],
  "scheduledJobs": [
    {
      "className": "NightlyCleanupJob",
      "guid": "A1B2...",
      "restartable": false,
      "usesHttpContextCurrent": false,
      "cms12Status": "compatible"
    }
  ],
  "summary": {
    "totalModules": 8,
    "compatible": 6,
    "requiresRewrite": 2
  }
}
```

## Migration Mapping

### IInitializableHttpModule → IStartupFilter

```csharp
// OLD (CMS 11) - IInitializableHttpModule
public class OldModule : IInitializableHttpModule
{
    public void InitializeHttpEvents(HttpApplication app)
    {
        app.BeginRequest += (s, e) => { /* logic */ };
    }
}

// NEW (CMS 12) - IStartupFilter
public class NewStartupFilter : IStartupFilter
{
    public Action<IApplicationBuilder> Configure(Action<IApplicationBuilder> next)
    {
        return app =>
        {
            app.Use(async (context, nextMiddleware) =>
            {
                // BeginRequest equivalent logic
                await nextMiddleware();
            });
            next(app);
        };
    }
}
// Register in Program.cs:
builder.Services.AddTransient<IStartupFilter, NewStartupFilter>();
```
