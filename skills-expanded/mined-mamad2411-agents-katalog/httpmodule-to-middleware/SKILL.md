---
name: httpmodule-to-middleware
version: 1.0.0
category: Migration/Build
description: Convert legacy IHttpModule and IHttpHandler implementations to ASP.NET Core middleware and minimal API handlers. Critical for .NET 4 to .NET 8 migration.
compatibility: .NET 4.x → .NET 8, ASP.NET Core
---

# IHttpModule to ASP.NET Core Middleware

## Trigger On

- "convert IHttpModule"
- "migrate HttpModule to middleware"
- "rewrite IHttpHandler"
- "migrate HTTP handlers"
- "System.Web.IHttpModule conversion"

## IHttpModule → Middleware

```csharp
// OLD: IHttpModule
public class RequestLoggingModule : IHttpModule
{
    public void Init(HttpApplication application)
    {
        application.BeginRequest += OnBeginRequest;
        application.EndRequest += OnEndRequest;
    }

    private void OnBeginRequest(object sender, EventArgs e)
    {
        var app = (HttpApplication)sender;
        // log start
    }

    private void OnEndRequest(object sender, EventArgs e)
    {
        // log end
    }

    public void Dispose() { }
}

// NEW: ASP.NET Core Middleware
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        _logger.LogInformation("Request: {Method} {Path}",
            context.Request.Method, context.Request.Path);

        await _next(context); // = EndRequest equivalent runs after this

        _logger.LogInformation("Response: {StatusCode}",
            context.Response.StatusCode);
    }
}

// Register in Program.cs
app.UseMiddleware<RequestLoggingMiddleware>();
// or as extension method:
app.UseRequestLogging();
```

## Auth Module → UseAuthentication

```csharp
// OLD: Custom auth IHttpModule
public class CustomAuthModule : IHttpModule
{
    public void Init(HttpApplication app)
    {
        app.AuthenticateRequest += OnAuthenticate;
    }
    private void OnAuthenticate(object s, EventArgs e) { /* validate token */ }
}

// NEW: Authentication middleware + custom scheme
builder.Services
    .AddAuthentication("MyScheme")
    .AddScheme<AuthenticationSchemeOptions, MyAuthHandler>("MyScheme", null);

// In pipeline (order matters):
app.UseAuthentication();
app.UseAuthorization();
```

## IHttpHandler → Minimal API / Controller

```csharp
// OLD: IHttpHandler (e.g. image resize handler)
public class ImageResizeHandler : IHttpHandler
{
    public bool IsReusable => false;

    public void ProcessRequest(HttpContext context)
    {
        var width = int.Parse(context.Request.QueryString["w"] ?? "100");
        // process and write image bytes
        context.Response.ContentType = "image/jpeg";
        context.Response.BinaryWrite(imageBytes);
    }
}

// NEW: Minimal API endpoint
app.MapGet("/image-resize", async (int w, int h, string src, HttpContext context) =>
{
    var imageBytes = await ResizeImageAsync(src, w, h);
    return Results.File(imageBytes, "image/jpeg");
});

// Or as a controller action:
[Route("image-resize")]
public class ImageController : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> Resize(int w, int h, string src)
    {
        var bytes = await _imageService.ResizeAsync(src, w, h);
        return File(bytes, "image/jpeg");
    }
}
```

## Short-Circuit Pattern (was HttpModule response end)

```csharp
// OLD: module terminating request early
application.CompleteRequest();
context.Response.End();

// NEW: middleware short-circuit
public async Task InvokeAsync(HttpContext context)
{
    if (ShouldBlock(context))
    {
        context.Response.StatusCode = 403;
        return; // short-circuits - does NOT call _next
    }

    await _next(context);
}
```

## Middleware Registration Patterns

```csharp
// Inline (for simple cases)
app.Use(async (context, next) =>
{
    // before
    await next();
    // after
});

// Named class (preferred for anything non-trivial)
app.UseMiddleware<MyMiddleware>();

// Extension method (cleanest)
public static class MyMiddlewareExtensions
{
    public static IApplicationBuilder UseMyMiddleware(this IApplicationBuilder app)
        => app.UseMiddleware<MyMiddleware>();
}
app.UseMyMiddleware();
```

## Anti-Patterns

```csharp
// WRONG - System.Web types don't exist in ASP.NET Core
using System.Web; // compile error in .NET 8

// WRONG - HttpContext.Current
var ctx = HttpContext.Current; // removed in ASP.NET Core

// WRONG - Response.End() / CompleteRequest()
context.Response.End(); // removed

// WRONG - Registering in web.config
// <modules><add name="MyModule" type="MyModule, MyAssembly" /></modules>
// → register in Program.cs instead
```
