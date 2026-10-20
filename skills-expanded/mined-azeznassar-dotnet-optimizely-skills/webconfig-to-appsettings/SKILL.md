---
name: webconfig-to-appsettings
version: 1.0.0
category: Migration/Build
description: Convert legacy web.config and web.*.config transform files to ASP.NET Core appsettings.json, appsettings.{Environment}.json, and environment variable patterns. Covers connection strings, appSettings, custom config sections, and Optimizely-specific config.
compatibility: .NET 4.x → .NET 8, ASP.NET Core
---

# web.config to appsettings.json Migration

## Trigger On

- "convert web.config"
- "migrate config to appsettings.json"
- "move connection strings to appsettings"
- "replace ConfigurationManager"
- "migrate app settings"

## Documentation

- [Configuration in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/)
- [Migrate from ASP.NET to ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/migration/proper-to-2x/)

## Pattern Map

### Connection Strings

```xml
<!-- OLD: web.config -->
<connectionStrings>
  <add name="EPiServerDB"
       connectionString="Server=.;Database=MyCms;Trusted_Connection=True;"
       providerName="System.Data.SqlClient" />
  <add name="EPiServerAzureBlobs"
       connectionString="DefaultEndpointsProtocol=https;AccountName=..." />
</connectionStrings>
```

```json
// NEW: appsettings.json
{
  "ConnectionStrings": {
    "EPiServerDB": "Server=.;Database=MyCms;Trusted_Connection=True;",
    "EPiServerAzureBlobs": "DefaultEndpointsProtocol=https;AccountName=..."
  }
}
```

```csharp
// Access in code
var conn = configuration.GetConnectionString("EPiServerDB");
```

### appSettings Keys

```xml
<!-- OLD: web.config -->
<appSettings>
  <add key="MySetting" value="SomeValue" />
  <add key="FeatureFlag:NewCheckout" value="true" />
</appSettings>
```

```json
// NEW: appsettings.json
{
  "MySetting": "SomeValue",
  "FeatureFlag": {
    "NewCheckout": true
  }
}
```

```csharp
// OLD access
var val = ConfigurationManager.AppSettings["MySetting"];

// NEW access
var val = configuration["MySetting"];
// or with Options pattern:
builder.Services.Configure<MyOptions>(configuration.GetSection("MyOptions"));
```

### Custom Config Sections

```xml
<!-- OLD: web.config custom section -->
<configuration>
  <configSections>
    <section name="myApp" type="MyApp.Config.MyAppSection, MyApp" />
  </configSections>
  <myApp>
    <api endpoint="https://api.example.com" timeout="30" retries="3" />
  </myApp>
</configuration>
```

```json
// NEW: appsettings.json + Options pattern
{
  "MyApp": {
    "Api": {
      "Endpoint": "https://api.example.com",
      "TimeoutSeconds": 30,
      "Retries": 3
    }
  }
}
```

```csharp
// Options class
public class ApiOptions
{
    public string Endpoint { get; set; }
    public int TimeoutSeconds { get; set; }
    public int Retries { get; set; }
}

// Registration in Program.cs
builder.Services.Configure<ApiOptions>(
    builder.Configuration.GetSection("MyApp:Api"));

// Usage via injection
public class ApiClient
{
    private readonly ApiOptions _options;
    public ApiClient(IOptions<ApiOptions> options)
    {
        _options = options.Value;
    }
}
```

### Environment Transforms

```xml
<!-- OLD: web.Release.config transform -->
<connectionStrings>
  <add name="EPiServerDB"
    connectionString="#{ProdConnectionString}#"
    xdt:Transform="SetAttributes"
    xdt:Locator="Match(name)" />
</connectionStrings>
```

```json
// NEW: appsettings.Production.json (committed, no secrets)
{
  "Logging": {
    "LogLevel": { "Default": "Warning" }
  }
}
```

```bash
# NEW: Secrets via environment variables (never committed)
# Variable name uses __ as section separator on Linux, : on Windows
EPiServer__ConnectionStrings__EPiServerDB="Server=prod;..."
# Or via dotnet user-secrets (dev only):
dotnet user-secrets set "ConnectionStrings:EPiServerDB" "Server=.;..."
```

### Logging Config

```xml
<!-- OLD: web.config log4net -->
<log4net>
  <appender name="RollingFile" type="log4net.Appender.RollingFileAppender">
    <file value="logs/app.log" />
    <level value="WARN" />
  </appender>
</log4net>
```

```json
// NEW: appsettings.json with Serilog
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Warning",
      "Override": {
        "EPiServer": "Warning",
        "Microsoft": "Warning"
      }
    },
    "WriteTo": [
      { "Name": "Console" },
      { "Name": "File", "Args": { "path": "logs/app.log" } }
    ]
  }
}
```

### Optimizely-Specific Config

```xml
<!-- OLD: EPiServer section in web.config -->
<episerver>
  <sites>
    <site siteId="..." name="MySite" />
  </sites>
</episerver>
```

```json
// NEW: Configured in appsettings.json + DB
{
  "Episerver": {
    "ConnectionStrings": {
      "EPiServerDB": "..."
    }
  }
}
// Site config moves to CMS Admin → Config → Manage Websites
```

## File Removal Checklist

After migration, these files should be removed or emptied:

- `web.config` — keep minimal version for IIS handler config only
- `web.Debug.config`
- `web.Release.config`
- `Web.config` transforms
- `packages.config` → migrate to `PackageReference` in `.csproj`

## Anti-Patterns

```csharp
// WRONG - ConfigurationManager in .NET 8
var val = ConfigurationManager.AppSettings["Key"]; // removed from ASP.NET Core

// WRONG - Hardcoded connection strings
private const string ConnStr = "Server=prod;..."; // use IConfiguration

// WRONG - Secrets in appsettings.json committed to source control
{
  "ConnectionStrings": {
    "EPiServerDB": "Server=prod;Password=mypassword123;" // ❌ never commit secrets
  }
}
```
