---
name: optimizely-dependency-mapper
version: 1.0.0
category: Migration/Audit
description: Map legacy EPiServer/Optimizely CMS 11 NuGet packages to their CMS 12 equivalents. Flags packages with no replacement, renamed packages, and packages absorbed into the core. Run during audit phase before fresh build.
compatibility: Targets EPiServer CMS 10/11 packages.csproj or packages.config for CMS 12 migration.
---

# Optimizely Dependency Mapper

## Trigger On

- "map my NuGet packages to CMS 12"
- "which EPiServer packages changed in v12"
- "update my package references for Optimizely 12"
- "audit dependencies for migration"

## Documentation

- [Breaking Changes CMS 11 → 12](https://docs.developers.optimizely.com/content-management-system/docs/breaking-changes-in-content-cloud-cms-12)
- [Get Started CMS 12](https://docs.developers.optimizely.com/content-management-system/docs/getting-started)

## Package Mapping Table

### Core CMS Packages

| CMS 11 Package | CMS 12 Package | Notes |
|---|---|---|
| `EPiServer.CMS` | `EPiServer.CMS` 12.x | Meta-package, still valid |
| `EPiServer.CMS.Core` | `EPiServer.CMS.Core` 12.x | Core models unchanged |
| `EPiServer.CMS.Web` | `EPiServer.CMS.Web` 12.x | Now ASP.NET Core based |
| `EPiServer.CMS.AspNetCore` | Merged into `EPiServer.CMS.Web` | Remove, use CMS.Web |
| `EPiServer.Framework` | `EPiServer.Framework` | Unchanged namespace |
| `EPiServer.Hosting` | `EPiServer.Hosting` | Required, add explicitly |

### UI Packages

| CMS 11 Package | CMS 12 Package | Notes |
|---|---|---|
| `EPiServer.CMS.UI` | `EPiServer.CMS.UI.AspNetCore` 12.x | Renamed for ASP.NET Core |
| `EPiServer.CMS.UI.Core` | `EPiServer.CMS.UI.AspNetCore` | Merged |
| `EPiServer.Shell` | `EPiServer.CMS.UI.AspNetCore` | Merged |

### Editor Packages

| CMS 11 Package | CMS 12 Package | Notes |
|---|---|---|
| `EPiServer.CMS.TinyMCE` | `EPiServer.CMS.TinyMce` 12.x | Note lowercase 'c' in v12 |

### Search Packages

| CMS 11 Package | CMS 12 Package | Notes |
|---|---|---|
| `EPiServer.Find` | `EPiServer.Find` 14+ | Works with CMS 12 |
| `EPiServer.Search` | Deprecated | Migrate to Find or Elasticsearch |

### Infrastructure

| CMS 11 Package | CMS 12 Package | Notes |
|---|---|---|
| `EPiServer.Azure` | `EPiServer.Azure` | Updated for ASP.NET Core |
| `EPiServer.CMS.AspNetCore.TagHelpers` | Included in `EPiServer.CMS.Web` | Remove separate ref |

### Removed / No Replacement

| CMS 11 Package | Status | Alternative |
|---|---|---|
| `EPiServer.MvcQuickNav` | ❌ Removed | Use CMS 12 OPE |
| `EPiServer.CMS.AspNet` | ❌ Removed | Use `EPiServer.CMS.Web` |
| `EPiServer.Logging.Log4Net` | ❌ Removed | Use `Microsoft.Extensions.Logging` + Serilog/NLog |
| `EPiServer.Logging.NLog` | ❌ Removed | Use `Microsoft.Extensions.Logging` + NLog provider |
| `EPiServer.CMS.Web.MVCVisitorGroups` | ❌ Removed | Built into CMS 12 |

### IoC / DI Containers (all removed)

| CMS 11 Package | CMS 12 Status | Migration |
|---|---|---|
| `EPiServer.ServiceLocation.StructureMap` | ❌ Removed | Use built-in `IServiceCollection` |
| `EPiServer.ServiceLocation.Autofac` | ❌ Removed | Use Autofac's `IServiceCollection` bridge if needed |
| `EPiServer.ServiceLocation.Windsor` | ❌ Removed | Use built-in `IServiceCollection` |

## Recommended Minimal CMS 12 Package Set

```xml
<ItemGroup>
  <!-- Core CMS -->
  <PackageReference Include="EPiServer.CMS" Version="12.*" />
  <PackageReference Include="EPiServer.CMS.Web" Version="12.*" />
  <PackageReference Include="EPiServer.CMS.UI.AspNetCore" Version="12.*" />
  <PackageReference Include="EPiServer.CMS.TinyMce" Version="*" />

  <!-- Logging (no longer in EPiServer packages) -->
  <PackageReference Include="Serilog.AspNetCore" Version="*" />
  <PackageReference Include="Serilog.Sinks.Console" Version="*" />

  <!-- Search (if using Find) -->
  <PackageReference Include="EPiServer.Find" Version="14.*" />
</ItemGroup>
```

## Namespace Changes to Find/Replace

| Old Namespace | New Namespace |
|---|---|
| `EPiServer.ServiceLocation` | `Microsoft.Extensions.DependencyInjection` |
| `EPiServer.Logging` | `Microsoft.Extensions.Logging` |
| `EPiServer.Web.Mvc` | `EPiServer.Web.Mvc` (unchanged but now ASP.NET Core) |
| `EPiServer.Framework.Configuration` | `Microsoft.Extensions.Configuration` |
