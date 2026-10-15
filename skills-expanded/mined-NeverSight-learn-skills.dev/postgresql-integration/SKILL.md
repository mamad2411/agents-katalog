---
name: postgresql-integration
description: "Integración de PostgreSQL con .NET y aplicaciones. Cubre Npgsql, Entity Framework Core con PostgreSQL (configuración, connection resiliency, pg_trgm, JSONB mapping, vector), Dapper para queries de alto rendimiento, connection pooling (interno y PgBouncer), y mejores prácticas de conexión. Actívala al configurar la capa de datos en aplicaciones .NET, optimizar el acceso a datos, o migrar de SQL Server a PostgreSQL."
disable-model-invocation: true
---

# PostgreSQL Integration with .NET

Guía de integración entre PostgreSQL y aplicaciones .NET. Cubre EF Core, Dapper y Npgsql directo.

---

## Npgsql — El driver

```bash
dotnet add package Npgsql
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL  # EF Core
dotnet add package Npgsql.DependencyInjection             # DI helpers
```

### Connection Strings

```json
{
  "ConnectionStrings": {
    "Default": "Host=localhost;Port=5432;Database=miapp;Username=app_user;Password=***",
    "Pooled": "Host=pgbouncer;Port=6432;Database=miapp;Username=app_user;Password=***;Pooling=false",
    "WithSSL": "Host=server;Database=miapp;Username=app_user;Password=***;SSL Mode=Require;Trust Server Certificate=false"
  }
}
```

| Parámetro | Recomendación |
|-----------|---------------|
| `Host` | FQDN o IP. `localhost` para dev. |
| `Port` | `5432` (PostgreSQL) o `6432` (PgBouncer) |
| `Pooling` | `true` (default). `false` si usas PgBouncer. |
| `SSL Mode` | `Require` en producción. `Disable` en dev local. |
| `Trust Server Certificate` | `false` en producción con CA real. |
| `Max Pool Size` | 100 (default). Ajustar según carga. |
| `Min Pool Size` | 5-10 para evitar cold start. |
| `Application Name` | Nombre de la app para `pg_stat_activity`. |

---

## Entity Framework Core con PostgreSQL

### Configuración

```csharp
builder.Services.AddDbContextPool<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("Default"),
        npgsqlOptions =>
        {
            // Migraciones
            npgsqlOptions.MigrationsAssembly(typeof(AppDbContext).Assembly.FullName);

            // Resiliencia: retry automático en errores transitorios
            npgsqlOptions.EnableRetryOnFailure(
                maxRetryCount: 3,
                maxRetryDelay: TimeSpan.FromSeconds(10),
                errorCodesToAdd: ["57P01"]); // Admin shutdown y otros transient

            // Timeout de comandos
            npgsqlOptions.CommandTimeout(30);

            // Esquema default
            npgsqlOptions.MigrationsHistoryTable("__EFMigrationsHistory", "public");
        }));

// DbContext pool para mejor rendimiento
// AddDbContextPool en vez de AddDbContext
```

### Mapeo de tipos PostgreSQL → .NET

| PostgreSQL | .NET | Notas |
|------------|------|-------|
| `integer` | `int` | |
| `bigint` | `long` | |
| `numeric` | `decimal` | |
| `text` | `string` | |
| `uuid` | `Guid` | |
| `timestamptz` | `DateTime` (UTC) | `DateTime.SpecifyKind(date, DateTimeKind.Utc)` |
| `boolean` | `bool` | |
| `jsonb` | `string`, `JsonDocument`, o tipo propio | Usar `HasColumnType("jsonb")` |
| `integer[]` | `List<int>` | Npgsql mapea arrays automáticamente |
| `tsvector` | `NpgsqlTsVector` | Full-text search |
| `inet` | `IPAddress` | |
| `vector` | `Pgvector.Vector` | pgvector extension |

### JSONB con EF Core

```csharp
// Opción 1: Como string (simple, sin tipado en BD)
public class Product
{
    public string Sku { get; set; }
    public string Name { get; set; }
    [Column(TypeName = "jsonb")]
    public string MetadataJson { get; set; } // Manejar serialización en app
}

// Opción 2: Owned entity (EF Core 8+)
public class Product
{
    public string Sku { get; set; }
    public ProductMetadata Metadata { get; set; }
}

[Owned]
public class ProductMetadata
{
    public string Brand { get; set; }
    public string Color { get; set; }
    public Dimensions Dimensions { get; set; }
}

// Config
builder.OwnsOne(p => p.Metadata, metadata =>
{
    metadata.ToJson("metadata"); // Mapea a columna JSONB automáticamente
    metadata.OwnsOne(m => m.Dimensions);
});
```

### Mapping de arrays

```csharp
// PostgreSQL arrays → List<T> automáticamente
public class Product
{
    public string Sku { get; set; }
    public List<string> Tags { get; set; } = [];  // → text[]
}

// Query: buscar productos con un tag específico
var tagged = await db.Products
    .Where(p => p.Tags.Contains("electronics"))
    .ToListAsync(ct);
// Genera: WHERE p.tags @> ARRAY['electronics']
```

### Full-text search con EF Core

```csharp
// Entidad con tsvector
public class Product
{
    public string Sku { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public NpgsqlTsVector SearchVector { get; set; }  // Generated column
}

// Config
builder.Property(p => p.SearchVector)
    .HasComputedColumnSql(
        @"setweight(to_tsvector('english', coalesce(""Name"", '')), 'A') ||
          setweight(to_tsvector('english', coalesce(""Description"", '')), 'B')",
        stored: true);

builder.HasIndex(p => p.SearchVector)
    .HasMethod("GIN");

// Query
var results = await db.Products
    .Where(p => p.SearchVector.Matches(query))
    .ToListAsync(ct);  // @@ operator
```

### pgvector con EF Core

```bash
dotnet add package Pgvector.EntityFrameworkCore
```

```csharp
// Entidad con embedding
public class ProductEmbedding
{
    public string ProductSku { get; set; }
    public Vector Embedding { get; set; }  // Pgvector.Vector
}

// Config
builder.Property(pe => pe.Embedding)
    .HasColumnType("vector(1536)");
builder.HasIndex(pe => pe.Embedding)
    .HasMethod("ivfflat")
    .HasOperators("vector_cosine_ops")
    .HasStorageParameter("lists", 100);

// Query: búsqueda por similitud
var results = await db.ProductEmbeddings
    .OrderBy(pe => pe.Embedding.CosineDistance(queryVector))
    .Take(10)
    .ToListAsync(ct);
```

---

## Dapper con Npgsql

```bash
dotnet add package Dapper
dotnet add package Npgsql
```

```csharp
// Registrar NpgsqlDataSource (recomendado sobre NpgsqlConnection directo)
builder.Services.AddNpgsqlDataSource(builder.Configuration.GetConnectionString("Default"));

// Uso en repositorio
public class OrderRepository(NpgsqlDataSource dataSource) : IOrderRepository
{
    public async Task<Order?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        const string sql = """
            SELECT o.id, o.order_number, o.customer_id, o.status,
                   o.total_amount, o.currency, o.created_at,
                   oi.id, oi.sku, oi.quantity, oi.unit_price
            FROM sales.orders o
            LEFT JOIN sales.order_items oi ON oi.order_id = o.id
            WHERE o.id = @id
            ORDER BY oi.line_number
            """;

        await using var connection = await dataSource.OpenConnectionAsync(ct);

        var orderDict = new Dictionary<Guid, Order>();
        await connection.QueryAsync<Order, OrderItem, Order>(
            sql,
            (order, item) =>
            {
                if (!orderDict.TryGetValue(order.Id, out var existing))
                {
                    existing = order;
                    existing.Items = [];
                    orderDict[order.Id] = existing;
                }
                if (item is not null)
                    existing.Items.Add(item);
                return existing;
            },
            new { id },
            splitOn: "id"
        );

        return orderDict.Values.FirstOrDefault();
    }

    public async Task CreateAsync(Order order, CancellationToken ct)
    {
        const string sql = """
            INSERT INTO sales.orders (id, customer_id, total_amount, currency, created_at)
            VALUES (@Id, @CustomerId, @TotalAmount, @Currency, @CreatedAt)
            """;

        await using var connection = await dataSource.OpenConnectionAsync(ct);
        await connection.ExecuteAsync(sql, order);
    }

    public async Task<IEnumerable<OrderSummary>> GetByCustomerPaginatedAsync(
        string customerId, int page, int pageSize, CancellationToken ct)
    {
        const string sql = """
            SELECT id, order_number, status, total_amount, created_at
            FROM sales.orders
            WHERE customer_id = @customerId
            ORDER BY created_at DESC
            LIMIT @pageSize OFFSET @offset
            """;

        await using var connection = await dataSource.OpenConnectionAsync(ct);
        return await connection.QueryAsync<OrderSummary>(sql, new
        {
            customerId,
            pageSize,
            offset = (page - 1) * pageSize
        });
    }
}
```

---

## Npgsql directo (alto rendimiento)

```csharp
public async Task BulkInsertOrdersAsync(
    IReadOnlyList<Order> orders, CancellationToken ct)
{
    await using var connection = await _dataSource.OpenConnectionAsync(ct);

    using var writer = await connection.BeginBinaryImportAsync(
        "COPY sales.orders (id, customer_id, total_amount, currency, created_at) FROM STDIN (FORMAT BINARY)",
        ct);

    foreach (var order in orders)
    {
        await writer.StartRowAsync(ct);
        await writer.WriteAsync(order.Id, ct);
        await writer.WriteAsync(order.CustomerId, ct);
        await writer.WriteAsync(order.TotalAmount, ct);
        await writer.WriteAsync(order.Currency, ct);
        await writer.WriteAsync(order.CreatedAt, ct);
    }

    await writer.CompleteAsync(ct);
    // Binary COPY es la forma más rápida de insertar en PostgreSQL.
}
```

---

## Connection Pooling y PgBouncer

```csharp
// Cuando usas PgBouncer, deshabilitar pool en Npgsql
// Connection string: "Host=pgbouncer;Port=6432;...;Pooling=false"

// PgBouncer transaction pooling: la conexión se devuelve al pool
// después de cada transacción, no después de cada sesión.
// Advertencia: SET LOCAL y cursores WITH HOLD no funcionan bien.

// Interno: Npgsql pooling (default Pooling=true)
// "Host=localhost;...;Max Pool Size=100;Min Pool Size=5"
```

---

## Manejo de transacciones

```csharp
// Transacción local con DbContext
await using var transaction = await db.Database.BeginTransactionAsync(ct);
try
{
    order.Approve();
    await db.SaveChangesAsync(ct);
    await db.Payments.AddAsync(new Payment { OrderId = order.Id }, ct);
    await db.SaveChangesAsync(ct);
    await transaction.CommitAsync(ct);
}
catch
{
    await transaction.RollbackAsync(ct);
    throw;
}

// Transacción con Savepoints (Npgsql)
await using var transaction = await db.Database.BeginTransactionAsync(ct);
try
{
    // Primera operación
    await db.SaveChangesAsync(ct);

    // Savepoint
    await transaction.CreateSavepointAsync("AfterFirst", ct);

    try
    {
        // Segunda operación (puede fallar sin romper todo)
        await db.Payments.AddAsync(payment, ct);
        await db.SaveChangesAsync(ct);
    }
    catch
    {
        await transaction.RollbackToSavepointAsync("AfterFirst", ct);
    }

    await transaction.CommitAsync(ct);
}
catch
{
    await transaction.RollbackAsync(ct);
    throw;
}
```

---

## Good practices

```csharp
// 1. NpgsqlDataSource (recomendado sobre raw NpgsqlConnection)
builder.Services.AddNpgsqlDataSource(connectionString);

// 2. Siempre CancellationToken
await db.Orders.FirstOrDefaultAsync(o => o.Id == id, ct); // ✅
await db.Orders.FirstOrDefaultAsync(o => o.Id == id);      // ❌

// 3. AsNoTracking para queries de solo lectura
var orders = await db.Orders.AsNoTracking().ToListAsync(ct);

// 4. Proyección sobre Include
var dtos = await db.Orders
    .Select(o => new { o.Id, o.Status, o.TotalAmount })
    .ToListAsync(ct);

// 5. EF.Functions para operadores PostgreSQL
var matches = await db.Orders
    .Where(o => EF.Functions.ILike(o.CustomerId, "%acme%"))  // LIKE case-insensitive
    .ToListAsync(ct);

// 6. GENERATED ALWAYS AS IDENTITY — EF Core lo maneja como ValueGeneratedOnAdd
builder.Property(o => o.OrderNumber)
    .UseIdentityAlwaysColumn()
    .ValueGeneratedOnAdd();
```

---

## Checklist de integración

- [ ] Npgsql con `EnableRetryOnFailure` configurado
- [ ] DbContext registrado como Scoped o con Pooling
- [ ] `NpgsqlDataSource` para Dapper y operaciones directas
- [ ] `AsNoTracking()` en todas las queries de lectura
- [ ] CancellationToken propagado a todas las operaciones async
- [ ] Connection strings en `appsettings.json` (no hardcoded)
- [ ] SSL Mode configurado para producción
- [ ] PgBouncer evaluado para >200 conexiones concurrentes
- [ ] Binary COPY para bulk inserts (>1000 filas)
- [ ] JSONB mapeado correctamente (Owned entity o ToJson)
- [ ] Arrays mapeados como `List<T>` automáticamente
- [ ] `Application Name` configurado en connection string para monitoreo
- [ ] Transaction savepoints para operaciones complejas
