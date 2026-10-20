---
name: optimizely-route-auditor
version: 1.0.0
category: Migration/Audit
description: Scan a legacy Optimizely/EPiServer codebase for custom route registrations, partial routers, and URL rewriting rules. Produces a migration plan for CMS 12 routing equivalents.
compatibility: Targets EPiServer CMS 10/11 source for CMS 12 migration planning.
---

# Optimizely Route Auditor

## Trigger On

- "audit routing"
- "scan custom routes"
- "find partial routers"
- "inventory URL handlers"
- "check what routing code I have"

## What to Scan For

```csharp
// Partial routers
IPartialRouter<T, TRoutedData>

// Route registration in init modules
RouteTable.Routes.MapRoute(...)
RouteTable.Routes.Add(new Route(...))

// Custom IRouteConstraint
// Friendly URL providers
EPiServer.Web.Routing.Segments.ISegmentMatcher
EPiServer.Web.Routing.IPartialRouter

// Content route mappings
Global.RoutesRegistered event handler
```

## Migration Mapping

| CMS 11 Pattern | CMS 12 Equivalent |
|---|---|
| `RouteTable.Routes.MapRoute(...)` | `app.MapControllerRoute(...)` in `Program.cs` |
| `IPartialRouter<T, TRoutedData>` | `IPartialRouter<T, TRoutedData>` — same interface, register via DI |
| `Global.RoutesRegistered` event | Move to `Program.cs` `UseEndpoints` |
| `EPiServer.Global` route wiring | `MapContent()` in `UseEndpoints` |
| `UrlRewriteModule` (IIS) | ASP.NET Core URL Rewriting Middleware |

## CMS 12 Partial Router Pattern

```csharp
// Register
builder.Services.AddSingleton<IPartialRouter, MyPartialRouter>();

// Implement
public class ProductPartialRouter : IPartialRouter<ProductPage, ProductVariant>
{
    public object RoutePartial(ProductPage content, ISegmentContext segmentContext)
    {
        var segment = segmentContext.GetNextValue(segmentContext.RemainingPath);
        if (string.IsNullOrEmpty(segment.Next)) return null;

        var variant = FindVariant(segment.Next);
        if (variant == null) return null;

        segmentContext.RemainingPath = segment.Remaining;
        return variant;
    }

    public PartialRouteData GetPartialVirtualPath(
        ProductVariant variant,
        string language,
        RouteValueDictionary routeValues,
        RequestContext requestContext)
    {
        return new PartialRouteData
        {
            BasePathRoot = ContentReference.StartPage,
            PartialVirtualPath = variant.Slug
        };
    }
}
```

## Output Format

```json
{
  "routes": [
    {
      "type": "MapRoute",
      "name": "ProductRoute",
      "pattern": "products/{category}/{id}",
      "location": "RouteConfig.cs:42",
      "cms12Migration": "Move to Program.cs UseEndpoints MapControllerRoute"
    },
    {
      "type": "IPartialRouter",
      "className": "ProductPartialRouter",
      "routableType": "ProductPage",
      "routedDataType": "ProductVariant",
      "cms12Migration": "Register via builder.Services.AddSingleton<IPartialRouter, ProductPartialRouter>()"
    }
  ],
  "summary": {
    "totalRoutes": 5,
    "partialRouters": 2,
    "standardRoutes": 3
  }
}
```
