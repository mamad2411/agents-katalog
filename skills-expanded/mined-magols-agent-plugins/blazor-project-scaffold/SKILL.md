---
name: blazor-project-scaffold
description: 'Scaffold a new C#/.NET 8+ Blazor project with standard folder structure, DI setup, Program.cs, _Imports.razor, and authentication. Covers template selection, project configuration, and layout.'
---

# Blazor Project Scaffold

Your goal is to scaffold a well-structured Blazor + C# project following .NET 8+ conventions.

## Step 1: Determine the Hosting Model

Ask the user (or infer from context) which hosting model to use:

| Template Command | Model | Use When |
|-----------------|-------|----------|
| `dotnet new blazor` | **Blazor Web App** (recommended default) | New projects — supports SSR + per-component interactive render modes |
| `dotnet new blazorserver` | **Blazor Server only** | Legacy or when WASM download is not acceptable |
| `dotnet new blazorwasm` | **Blazor WASM only** | Fully client-side, offline-capable apps |
| `dotnet new blazor -int None` | **Static SSR only** | Content sites, no JS interactivity needed |

**Default recommendation**: `dotnet new blazor --name <AppName> --interactivity Auto --auth Individual`

## Step 2: .csproj Configuration

Ensure the project file includes:

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>YourApp</RootNamespace>
  </PropertyGroup>
</Project>
```

For WASM client project, use `Microsoft.NET.Sdk.BlazorWebAssembly`.

## Step 3: Standard Folder Structure

```
YourApp/
├── Components/              # Shared reusable components
│   ├── Layout/
│   │   ├── MainLayout.razor
│   │   ├── MainLayout.razor.css
│   │   └── NavMenu.razor
│   └── _Imports.razor
├── Pages/                   # Routable page components
│   ├── Home.razor
│   └── Error.razor
├── Services/                # Business logic and data access interfaces + implementations
│   └── IWeatherService.cs
├── Models/                  # DTOs, domain models, view models
│   └── WeatherForecast.cs
├── Data/                    # EF Core DbContext, migrations (if using EF)
│   └── AppDbContext.cs
├── wwwroot/                 # Static assets
│   ├── css/
│   ├── js/
│   └── favicon.ico
├── Program.cs
├── appsettings.json
├── appsettings.Development.json
└── YourApp.csproj
```

## Step 4: Program.cs Builder Pattern

```csharp
using YourApp.Components;
using YourApp.Services;

var builder = WebApplication.CreateBuilder(args);

// Add Blazor services
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()    // Include if using Interactive Server
    .AddInteractiveWebAssemblyComponents(); // Include if using WASM/Auto

// Register application services
builder.Services.AddScoped<IWeatherService, WeatherService>();

// Add HttpClient for WASM (client project)
// builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode()
    .AddAdditionalAssemblies(typeof(YourApp.Client._Imports).Assembly);

app.Run();
```

## Step 5: _Imports.razor

```razor
@using System.Net.Http
@using System.Net.Http.Json
@using Microsoft.AspNetCore.Components.Forms
@using Microsoft.AspNetCore.Components.Routing
@using Microsoft.AspNetCore.Components.Web
@using Microsoft.AspNetCore.Components.Web.Virtualization
@using Microsoft.JSInterop
@using YourApp
@using YourApp.Components
@using YourApp.Models
@using YourApp.Services
```

## Step 6: appsettings.json Structure

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=YourApp;Trusted_Connection=True"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*"
}
```

## Step 7: Authentication (Optional)

For **Individual Accounts** (ASP.NET Core Identity):

```bash
dotnet new blazor --name YourApp --auth Individual --interactivity Auto
```

Adds: Identity tables, login/register pages, `[Authorize]` middleware.

For **OIDC / Entra ID**:

```bash
dotnet add package Microsoft.Identity.Web
```

Then in `Program.cs`:

```csharp
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"));
builder.Services.AddControllersWithViews()
    .AddMicrosoftIdentityUI();
```

## Step 8: CSS Framework Integration

**Bootstrap** (default, included in template): Already configured in `wwwroot/`.

**Tailwind CSS**:

```bash
npm init -y
npm install -D tailwindcss
npx tailwindcss init
```

In `tailwind.config.js`:

```js
content: ["./Components/**/*.{razor,html}", "./Pages/**/*.razor"]
```

Add build step to `.csproj`:

```xml
<Target Name="BuildTailwind" BeforeTargets="Build">
  <Exec Command="npx tailwindcss -i ./wwwroot/css/app.css -o ./wwwroot/css/app.min.css" />
</Target>
```

## Checklist

- [ ] TargetFramework is `net9.0` (or latest stable)
- [ ] `<Nullable>enable</Nullable>` set
- [ ] Services registered with correct lifetimes (Scoped for stateful per-user services)
- [ ] `UseAntiforgery()` called before `MapRazorComponents`
- [ ] `_Imports.razor` includes all shared namespaces
- [ ] `Pages/` contains only routable components (`@page` directive)
- [ ] `Components/` contains only reusable non-routable components
- [ ] Static assets in `wwwroot/`
