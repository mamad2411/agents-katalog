---
name: aspnet-ef-core
description: Entity Framework Core en contexto ASP.NET. Cubre ciclo de vida del DbContext (Scoped), DbContextFactory para Blazor y workers, migraciones en aplicaciones web, connection resiliency, health checks de BD, context pooling, queries optimizadas para web (split queries, AsNoTracking, paginación), y patrones anti-N+1. Actívala al configurar EF Core en aplicaciones web, optimizar queries de endpoints, o trabajar con Blazor + EF Core.
disable-model-invocation: true
---

# EF Core en ASP.NET

Guía de Entity Framework Core específicamente en el contexto de aplicaciones web ASP.NET. Para EF Core general, ver `dotnet-ef-core`.

---

## Ciclo de vida del DbContext

### Scoped (web apps normales)

```csharp
// ✅ Registro Scoped: un DbContext por request HTTP
builder.Services.AddDbContext<AppDbContext>(options =>
{
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("Default"),
        sqlOptions =>
        {
            sqlOptions.EnableRetryOnFailure(
                maxRetryCount: 3,
                maxRetryDelay: TimeSpan.FromSeconds(10),
                errorNumbersToAdd: null);

            sqlOptions.CommandTimeout(30);
            sqlOptions.MigrationsAssembly(typeof(AppDbContext).Assembly.FullName);
        });

    // Logging de queries en development
    if (builder.Environment.IsDevelopment())
        options.EnableSensitiveDataLogging()
               .EnableDetailedErrors();
});

// Pooling (mejor rendimiento en web apps)
builder.Services.AddDbContextPool<AppDbContext>(options =>
{
    options.UseSqlServer(connectionString);
}, poolSize: 128); // Ajustar según carga
```

### DbContextFactory (Blazor, workers, background services)

```csharp
// ✅ Para Blazor Server/WASM y BackgroundService donde
// no existe el concepto de "request" HTTP
builder.Services.AddDbContextFactory<AppDbContext>(options =>
    options.UseSqlServer(connectionString));

// Consumo
@inject IDbContextFactory<AppDbContext> DbFactory

@code {
    protected override async Task OnInitializedAsync()
    {
        await using var db = await DbFactory.CreateDbContextAsync();
        var orders = await db.Orders.AsNoTracking().ToListAsync();
        // DbContext se dispone al salir del método
    }
}

// En BackgroundService
public class OrderExpirationService : BackgroundService
{
    private readonly IDbContextFactory<AppDbContext> _dbFactory;

    public OrderExpirationService(IDbContextFactory<AppDbContext> dbFactory)
        => _dbFactory = dbFactory;

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            await using var db = await _dbFactory.CreateDbContextAsync(ct);

            await db.Orders
                .Where(o => o.Status == OrderStatus.Pending && o.CreatedAt < DateTime.UtcNow.AddHours(-24))
                .ExecuteUpdateAsync(s => s.SetProperty(o => o.Status, OrderStatus.Expired), ct);

            await Task.Delay(TimeSpan.FromMinutes(5), ct);
        }
    }
}
```

---

## Migraciones en Web Apps

### Aplicar migraciones al iniciar

```csharp
// ✅ Para apps pequeñas/medianas
var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    await db.Database.MigrateAsync(); // Aplica migraciones pendientes
    // O EnsureCreatedAsync() para desarrollo rápido (no migraciones)
}

// ⚠️ En producción: mejor generar script y aplicar manualmente
// dotnet ef migrations script --idempotent --output migrate.sql
```

### Health check de BD

```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>(
        name: "database",
        tags: ["database", "ready"],
        customTestQuery: async (db, ct) =>
        {
            // Verifica que la BD responde con un query liviano
            await db.Database.ExecuteSqlRawAsync("SELECT 1", ct);
        });
```

---

## Connection Resiliency

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
{
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        // Retry automático para errores transitorios
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(10),
            errorNumbersToAdd: null); // Agrega números de error custom si es necesario
    });
});

// Para PostgreSQL
options.UseNpgsql(connectionString, npgOptions =>
{
    npgOptions.EnableRetryOnFailure(3, TimeSpan.FromSeconds(10), null);
});
```

---

## Queries optimizadas para web

### LeftJoin y RightJoin (.NET 10)

```csharp
// ✅ LeftJoin — antes requería GroupJoin + DefaultIfEmpty + SelectMany
var ordersWithPayments = await db.Orders
    .LeftJoin(db.Payments, o => o.Id, p => p.OrderId, (o, p) => new
    {
        o.Id, o.Total,
        Payment = p != null ? new { p.Amount, p.Status } : null
    })
    .ToListAsync(ct);

// ✅ RightJoin
var productsWithOrders = await db.Products
    .RightJoin(db.OrderItems, p => p.Id, oi => oi.ProductId, (p, oi) => new { p, oi })
    .ToListAsync(ct);
```

### Proyección: lo más importante

```csharp
// ❌ Traer todo con Include
var orders = await db.Orders
    .Include(o => o.Items)
    .Include(o => o.Discounts)
    .Include(o => o.Customer)
    .ToListAsync(ct);

// ✅ Proyección: solo las columnas necesarias
var orders = await db.Orders
    .Where(o => o.Status == OrderStatus.Pending)
    .Select(o => new OrderSummaryDto(
        o.Id, o.CustomerId, o.Total.Amount, o.CreatedAt))
    .ToListAsync(ct);
// SQL: SELECT o.Id, o.CustomerId, o.TotalAmount, o.CreatedAt FROM Orders WHERE o.Status = 1
```

### AsNoTracking para lecturas

```csharp
// ✅ Siempre en GET endpoints
var orders = await db.Orders
    .AsNoTracking()
    .Where(o => o.CustomerId == customerId)
    .ToListAsync(ct);

// ⚠️ Solo usar tracking cuando vas a modificar
var order = await db.Orders.FirstOrDefaultAsync(o => o.Id == id, ct);
order.Status = OrderStatus.Cancelled;
await db.SaveChangesAsync(ct);
```

### Split queries para evitar producto cartesiano

```csharp
// ❌ Múltiples includes generan JOIN explosivo
var orders = await db.Orders
    .Include(o => o.Items)
    .Include(o => o.Discounts)
    .ToListAsync(ct);

// ✅ Split queries: una query por cada Include
var orders = await db.Orders
    .Include(o => o.Items)
    .Include(o => o.Discounts)
    .AsSplitQuery()
    .ToListAsync(ct);
```

---

## Paginación web

### Keyset pagination (cursor-based)

```csharp
// ✅ Mejor rendimiento, evita OFFSET
app.MapGet("/api/orders", async (
    [FromQuery] Guid? cursor,       // LastOrderId del request anterior
    [FromQuery] int limit = 20,
    AppDbContext db,
    CancellationToken ct) =>
{
    var query = db.Orders.AsNoTracking().OrderByDescending(o => o.CreatedAt);

    if (cursor.HasValue)
    {
        var cursorOrder = await db.Orders.FindAsync([cursor.Value], ct);
        if (cursorOrder is not null)
            query = query.Where(o => o.CreatedAt < cursorOrder.CreatedAt);
    }

    var orders = await query
        .Take(limit + 1) // +1 para saber si hay más
        .Select(o => new OrderDto(o.Id, o.CustomerId, o.Total.Amount, o.CreatedAt))
        .ToListAsync(ct);

    var hasMore = orders.Count > limit;
    if (hasMore) orders.RemoveAt(orders.Count - 1);

    var nextCursor = orders.Count > 0 ? orders[^1].Id : (Guid?)null;

    return Results.Ok(new { orders, nextCursor, hasMore });
});
```

### Offset pagination (tradicional)

```csharp
// ⬜ Aceptable para páginas bajas
var total = await db.Orders.CountAsync(o => o.CustomerId == customerId, ct);
var orders = await db.Orders
    .Where(o => o.CustomerId == customerId)
    .OrderByDescending(o => o.CreatedAt)
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .Select(o => new OrderDto(o.Id, o.CustomerId, o.Total.Amount, o.CreatedAt))
    .ToListAsync(ct);
```

---

## Anti-N+1 en Web Apps

### Evitar N+1 con Include

```csharp
// ❌ N+1: 1 query para orders + N queries para items
var orders = await db.Orders.ToListAsync(ct);
foreach (var order in orders)
{
    var items = await db.OrderItems
        .Where(i => i.OrderId == order.Id).ToListAsync(ct); // N queries
}

// ✅ Eager loading
var orders = await db.Orders
    .Include(o => o.Items)
    .ToListAsync(ct);

// ✅ O mejor: proyección
var orders = await db.Orders
    .Select(o => new OrderDto
    {
        Id = o.Id,
        Items = o.Items.Select(i => new ItemDto(i.Sku, i.Quantity)).ToList()
    })
    .ToListAsync(ct);
```

### Explicit loading (solo si necesario)

```csharp
// Si ya tienes la entidad y necesitas cargar una relación
var order = await db.Orders.FindAsync([id], ct);
await db.Entry(order).Collection(o => o.Items).LoadAsync(ct);
await db.Entry(order).Reference(o => o.Customer).LoadAsync(ct);
```

---

## ExecuteUpdate/ExecuteDelete (batch sin carga)

```csharp
// ✅ Batch update: sin cargar entidades
await db.Orders
    .Where(o => o.Status == OrderStatus.Pending && o.CreatedAt < cutoff)
    .ExecuteUpdateAsync(s => s
        .SetProperty(o => o.Status, OrderStatus.Expired)
        .SetProperty(o => o.LastModified, DateTime.UtcNow),
        ct);

// ✅ Batch delete
await db.Orders
    .Where(o => o.CreatedAt < DateTime.UtcNow.AddDays(-365))
    .ExecuteDeleteAsync(ct);
```

---

## Transactions en Web Apps

```csharp
// Transaction con SaveChanges
await using var transaction = await db.Database.BeginTransactionAsync(ct);

try
{
    db.Orders.Add(order);
    await db.SaveChangesAsync(ct);

    var payment = new Payment { OrderId = order.Id, Amount = order.Total };
    db.Payments.Add(payment);
    await db.SaveChangesAsync(ct);

    await transaction.CommitAsync(ct);
}
catch
{
    await transaction.RollbackAsync(ct);
    throw;
}

// O usar ExecutionStrategy para retry automático
var strategy = db.Database.CreateExecutionStrategy();
await strategy.ExecuteAsync(async () =>
{
    await using var tx = await db.Database.BeginTransactionAsync(ct);
    // operaciones...
    await tx.CommitAsync(ct);
});
```

---

## EF Core en Blazor

```csharp
// ⚠️ Blazor Server: los componentes viven más que un request HTTP.
// NUNCA inyectar DbContext directamente (es Scoped).
// Usar IDbContextFactory siempre.

// ✅ Blazor Server con DbContextFactory
builder.Services.AddDbContextFactory<AppDbContext>(options =>
    options.UseSqlServer(connectionString));

@inject IDbContextFactory<AppDbContext> DbFactory

@code {
    private List<OrderDto>? orders;

    protected override async Task OnInitializedAsync()
    {
        await using var db = await DbFactory.CreateDbContextAsync();

        orders = await db.Orders
            .AsNoTracking()
            .OrderByDescending(o => o.CreatedAt)
            .Take(20)
            .Select(o => new OrderDto(o.Id, o.CustomerId, o.Total.Amount, o.Status))
            .ToListAsync();
    }
}

// ✅ Blazor WASM: EF Core NO corre en WASM (no SQL Server en navegador).
// Llamar a una API que use EF Core en el servidor.
```

---

## Anti-patrones EF Core en ASP.NET

| Anti-patrón | Consecuencia | Corrección |
|-------------|-------------|------------|
| Inyectar DbContext en Singleton | Error runtime | Usar IDbContextFactory |
| DbContext sin Dispose | Memory leak / conexiones abiertas | DI lo maneja (Scoped). En Blazor: dispose explícito. |
| `ToList()` antes de `Where()` | Carga toda la tabla | `Where()` primero |
| `SaveChanges` en loop | N roundtrips | Llamar `SaveChangesAsync` una vez al final |
| Tracking en queries de solo lectura | Overhead de memoria | `AsNoTracking()` en GETs |
| Migraciones sin revisión | SQL destructivo en prod | `migrations script` + revisar SQL |
| Sin retry en producción | Errores transitorios tumban requests | `EnableRetryOnFailure` |
| DbContext en singleton service | Crash en runtime | Usar `IServiceScopeFactory` |
| `Find` fuera de request scope | Tracking innecesario | `FirstOrDefault` con `AsNoTracking` |

---

## Checklist EF Core ASP.NET

- [ ] DbContext registrado como Scoped (API/MVC/Razor Pages)
- [ ] `IDbContextFactory` en Blazor y BackgroundService
- [ ] Connection resiliency con `EnableRetryOnFailure`
- [ ] Migraciones se aplican al iniciar (`MigrateAsync`)
- [ ] Health check de BD configurado
- [ ] `AsNoTracking()` en todos los GET
- [ ] Proyección en vez de `Include` + mapeo manual
- [ ] `AsSplitQuery()` con múltiples Includes
- [ ] `ExecuteUpdate`/`ExecuteDelete` para batch ops
- [ ] Transactions para operaciones multi-tabla
- [ ] Paginación keyset vs offset según caso
- [ ] CancellationToken propagado a toda operación EF
- [ ] `AddDbContextPool` para apps con alta carga
