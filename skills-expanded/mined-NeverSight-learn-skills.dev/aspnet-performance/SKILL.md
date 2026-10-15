---
name: aspnet-performance
description: Rendimiento y optimización de aplicaciones ASP.NET Core. Cubre response caching, output caching, response compression, static file caching, CDN, minificación y bundling, lazy loading en Blazor, streaming, Kestrel tuning, y profiling con MiniProfiler y Application Insights. Actívala al optimizar tiempos de carga, reducir ancho de banda, o preparar una aplicación para producción.
disable-model-invocation: true
---

# Rendimiento en ASP.NET Core

Optimización de aplicaciones web ASP.NET. Menos latencia, menos ancho de banda, mejor UX.

---

## Response Caching

### Output caching (recomendado)

```csharp
// Configurar
builder.Services.AddOutputCache(options =>
{
    options.DefaultExpirationTimeSpan = TimeSpan.FromMinutes(1);
});

app.UseOutputCache();

// Endpoint cacheado
app.MapGet("/api/products", GetAllProducts)
    .CacheOutput(policy => policy
        .Expire(TimeSpan.FromMinutes(5))
        .SetVaryByQuery("category", "page"));

// Cache con Redis en producción
builder.Services.AddStackExchangeRedisOutputCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
});
```

### Response caching (legacy, usa headers HTTP)

```csharp
[ResponseCache(Duration = 300, Location = ResponseCacheLocation.Any, VaryByQueryKeys = ["category"])]
public IActionResult Index() => View();
```

### Static files caching

```csharp
app.UseStaticFiles(new StaticFileOptions
{
    OnPrepareResponse = ctx =>
    {
        // Assets versionados (app.123abc.js) → cache 1 año
        if (ctx.File.Name.Contains('.'))
        {
            var extension = Path.GetExtension(ctx.File.Name).ToLowerInvariant();
            if (extension is ".js" or ".css" or ".woff2" or ".svg")
            {
                ctx.Context.Response.Headers.Append(
                    "Cache-Control", "public,max-age=31536000,immutable");
            }
        }
        // Archivos no versionados → cache corto con revalidación
        else
        {
            ctx.Context.Response.Headers.Append(
                "Cache-Control", "public,max-age=60,must-revalidate");
        }
    }
});
```

---

## Response Compression

```csharp
builder.Services.AddResponseCompression(options =>
{
    options.EnableForHttps = true;
    options.Providers.Add<BrotliCompressionProvider>();
    options.Providers.Add<GzipCompressionProvider>();

    // MIME types a comprimir
    options.MimeTypes = ResponseCompressionDefaults.MimeTypes.Concat([
        "application/json",
        "text/html",
        "text/plain",
        "text/css",
        "application/javascript",
        "application/xml",
        "image/svg+xml"
    ]);
});

// Configurar Brotli
builder.Services.Configure<BrotliCompressionProviderOptions>(options =>
{
    options.Level = CompressionLevel.Fastest; // Prod: Optimal
});

// Aplicar TEMPRANO en el pipeline
var app = builder.Build();
app.UseResponseCompression(); // Antes de UseStaticFiles y UseRouting
```

---

## Minificación y Bundling

### Build-time con Webpack/Vite (JS/CSS)

```json
// package.json
{
  "scripts": {
    "build": "vite build",
    "watch": "vite build --watch"
  },
  "devDependencies": {
    "vite": "^6.0.0"
  }
}
```

### Librería .NET para minification

```csharp
// Paquete: WebMarkupMin.AspNetCore
builder.Services.AddWebMarkupMin(options =>
{
    options.AllowMinificationInDevelopmentEnvironment = false;
    options.AllowCompressionInDevelopmentEnvironment = false;
})
.AddHtmlMinification()
.AddXmlMinification();

app.UseWebMarkupMin();
```

### Bundling con ASP.NET Core (built-in .NET 10)

```csharp
// .NET 10 incluye mejor soporte para bundling de static assets.
// Usar MapStaticAssets en vez de UseStaticFiles:
app.MapStaticAssets(); // En vez de UseStaticFiles()

// Procesa automáticamente minificación, fingerprinting y compresión
// en build-time, sin necesidad de Webpack/Vite para assets simples.
```

---

## Lazy Loading y Code Splitting

### Blazor lazy loading

```csharp
// Registrar assemblies para lazy loading
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

// Componente lazy
@page "/reports"
@attribute [Authorize]

<Router AppAssembly="typeof(Program).Assembly"
        AdditionalAssemblies="lazyLoadedAssemblies" />

// En el componente que quiere lazy load:
@inject LazyAssemblyLoader AssemblyLoader

@code {
    private async Task LoadReportsAsync()
    {
        var assemblies = await AssemblyLoader.LoadAssembliesAsync(
            ["MiApp.Reports.dll"]);
        // Ahora los componentes de MiApp.Reports están disponibles
    }
}
```

### JavaScript module lazy loading

```javascript
// Cargar módulo solo cuando se necesita
const chartModule = await import('./charts.js');
chartModule.renderChart(data);
```

---

## Streaming y Chunked Responses

```csharp
// Streaming de datos grandes (evita cargar todo en memoria)
app.MapGet("/api/orders/export", ExportOrders);

async Task ExportOrders(HttpContext context, AppDbContext db, CancellationToken ct)
{
    context.Response.ContentType = "text/csv";
    context.Response.Headers.Append("Content-Disposition", "attachment; filename=orders.csv");

    await context.Response.WriteAsync("Id,Customer,Total,Date\n", ct);

    await foreach (var order in db.Orders
        .AsNoTracking()
        .AsAsyncEnumerable()
        .WithCancellation(ct))
    {
        await context.Response.WriteAsync(
            $"{order.Id},{order.CustomerId},{order.Total.Amount},{order.CreatedAt:O}\n", ct);
        await context.Response.Body.FlushAsync(ct);
    }
}
```

---

## Kestrel Tuning

```csharp
builder.WebHost.ConfigureKestrel(options =>
{
    // Límites
    options.Limits.MaxRequestBodySize = 10 * 1024 * 1024; // 10 MB
    options.Limits.MaxConcurrentConnections = 5000;
    options.Limits.MaxConcurrentUpgradedConnections = 100;
    options.Limits.KeepAliveTimeout = TimeSpan.FromMinutes(2);
    options.Limits.RequestHeadersTimeout = TimeSpan.FromSeconds(30);

    // Performance
    options.AddServerHeader = false;
    options.AllowSynchronousIO = false;

    // Endpoints
    options.Listen(IPAddress.Any, 80);
    options.Listen(IPAddress.Any, 443, listenOptions =>
    {
        listenOptions.UseHttps();
        listenOptions.Protocols = HttpProtocols.Http1AndHttp2AndHttp3;
    });
});

// Thread pool config (en app init)
ThreadPool.SetMinThreads(100, 100); // Para apps con alta concurrencia
```

---

## Client-side performance

### Image optimization

```html
@* Usar formatos modernos *@
<picture>
    <source srcset="/images/product.avif" type="image/avif">
    <source srcset="/images/product.webp" type="image/webp">
    <img src="/images/product.jpg" alt="Product" loading="lazy" />
</picture>

@* Lazy loading nativo *@
<img src="product.jpg" loading="lazy" decoding="async" />
```

### Font loading

```html
@* Preload de fuentes críticas *@
<link rel="preload" href="/fonts/roboto.woff2" as="font" type="font/woff2" crossorigin />

@* CSS font-display *@
<style>
@@font-face {
    font-family: 'Roboto';
    src: url('/fonts/roboto.woff2') format('woff2');
    font-display: swap; /* Evita FOIT (flash of invisible text) */
}
</style>
```

### Script loading

```html
@* Async: no bloquea parser, ejecuta cuando esté listo *@
<script src="analytics.js" async></script>

@* Defer: no bloquea parser, ejecuta en orden al terminar *@
<script src="app.js" defer></script>

@* Preload de recursos críticos *@
<link rel="preload" href="/js/critical.js" as="script" />
<link rel="preconnect" href="https://api.miapp.com" />
```

---

## Profiling y Monitoreo

### MiniProfiler

```csharp
builder.Services.AddMiniProfiler(options =>
{
    options.RouteBasePath = "/profiler";
    options.EnableDebugMode = builder.Environment.IsDevelopment();
    options.TrackConnectionOpenClose = true;
})
.AddEntityFramework();

app.UseMiniProfiler();

// En Razor Pages / Views:
@using StackExchange.Profiling
@* <mini-profiler /> @* Widget en la esquina *@
```

### Application Insights

```csharp
builder.Services.AddApplicationInsightsTelemetry(options =>
{
    options.ConnectionString = builder.Configuration["AppInsights:ConnectionString"];
    options.EnableAdaptiveSampling = true; // Reduce volumen en producción
    options.EnableQuickPulseMetricStream = true;
});

// Metric custom
public class OrdersMetrics
{
    private readonly Counter<int> _orderCounter;

    public OrdersMetrics(IMeterFactory meterFactory)
    {
        var meter = meterFactory.Create("MiApp.Orders");
        _orderCounter = meter.CreateCounter<int>("orders.created");
    }

    public void OrderCreated() => _orderCounter.Add(1);
}
```

---

## Memory Management

```csharp
// Evitar memory leaks en web apps

// ❌ Event handler que nunca se desubscribe
public class SomeService
{
    public SomeService()
    {
        StaticClass.SomeEvent += HandleEvent; // Se suscribe para siempre
    }
}

// ✅ Dispose para liberar suscripciones
public class SomeService : IDisposable
{
    public SomeService() => StaticClass.SomeEvent += HandleEvent;
    public void Dispose() => StaticClass.SomeEvent -= HandleEvent;
}

// ❌ Capturar HttpContext en un Task de larga duración
_ = Task.Run(async () =>
{
    await Task.Delay(60_000);
    var user = httpContext.User; // HttpContext ya fue dispuesto
});

// ✅ Capturar solo lo necesario
var userId = httpContext.User.FindFirstValue(ClaimTypes.NameIdentifier);
_ = Task.Run(async () =>
{
    await Task.Delay(60_000);
    // Usar userId, no httpContext
});
```

---

## Checklist de rendimiento web

- [ ] Response compression habilitada (Brotli + Gzip)
- [ ] Static files con cache headers agresivos para assets versionados
- [ ] Output caching en endpoints de solo lectura
- [ ] Redis como backend de output cache y session en producción
- [ ] EF Core con proyección y AsNoTracking en queries
- [ ] Streaming para respuestas grandes (IAsyncEnumerable)
- [ ] Lazy loading de imágenes (<img loading="lazy">)
- [ ] Fuentes web con font-display: swap
- [ ] Scripts async/defer según necesidad
- [ ] Preconnect a orígenes externos conocidos
- [ ] Minificación y bundling en build-time
- [ ] Kestrel límites configurados para producción
- [ ] Application Insights o MiniProfiler para monitoreo
- [ ] Sin memory leaks (event handlers desuscritos, HttpContext no capturado en background tasks)
- [ ] CDN para static assets en producción
- [ ] MapStaticAssets (.NET 10) para fingerprinting y compresión automática
