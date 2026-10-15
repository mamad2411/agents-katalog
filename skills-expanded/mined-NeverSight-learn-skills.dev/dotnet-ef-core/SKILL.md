---
name: dotnet-ef-core
description: Entity Framework Core 10. Cubre DbContext, configuraciones, relaciones, queries optimizadas, migraciones, raw SQL, interceptors, performance (split queries, compiled queries, AsNoTracking, indexes), manejo de concurrencia, y patrones avanzados (shadow properties, owned types, TPH/TPT, value converters). Actívala al diseñar modelos de datos, optimizar queries, trabajar con migraciones o definir estrategias de persistencia.
disable-model-invocation: true
---

# Entity Framework Core

Guía completa de EF Core 10. Asume SQL Server como provider por defecto, pero los patrones aplican a PostgreSQL, MySQL, etc.

---

## DbContext

### Configuración mínima

```csharp
public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Aplica todas las configuraciones del assembly automáticamente
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }

    protected override void ConfigureConventions(ModelConfigurationBuilder configurationBuilder)
    {
        // Convenciones globales (.NET 6+)
        configurationBuilder
            .Properties<string>()
            .HaveMaxLength(200);

        configurationBuilder
            .Properties<decimal>()
            .HavePrecision(18, 4);
    }
}
```

### Registro en DI

```csharp
// SQL Server con connection string
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default"),
        sqlOptions =>
        {
            sqlOptions.MigrationsAssembly(typeof(AppDbContext).Assembly.FullName);
            sqlOptions.EnableRetryOnFailure(maxRetryCount: 3);
            sqlOptions.CommandTimeout(30);
        }));

// Pooling para alto rendimiento
services.AddDbContextPool<AppDbContext>(options =>
    options.UseSqlServer(connectionString));
```

---

## Configuraciones (IEntityTypeConfiguration<T>)

```csharp
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        // Tabla
        builder.ToTable("Orders", "sales");

        // PK
        builder.HasKey(o => o.Id);
        builder.Property(o => o.Id)
            .HasConversion(id => id.Value, value => new OrderId(value)); // Value Object como PK

        // Columnas
        builder.Property(o => o.CustomerId)
            .IsRequired()
            .HasMaxLength(50);

        builder.ComplexProperty(o => o.Total, money =>
        {
            money.Property(m => m.Amount).HasColumnName("TotalAmount").HasPrecision(18, 4);
            money.Property(m => m.Currency).HasColumnName("Currency").HasMaxLength(3);
        });

        // Índices
        builder.HasIndex(o => o.CustomerId).HasDatabaseName("IX_Orders_CustomerId");
        builder.HasIndex(o => new { o.Status, o.CreatedAt })
            .HasDatabaseName("IX_Orders_Status_CreatedAt")
            .HasFilter("[Status] = 'Pending'"); // Filtered index

        // Relaciones
        builder.HasMany(o => o.Items)
            .WithOne()
            .HasForeignKey(i => i.OrderId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasOne<Customer>()
            .WithMany()
            .HasForeignKey(o => o.CustomerId)
            .HasPrincipalKey(c => c.Id);

        // Owned types (value objects embebidos)
        builder.OwnsOne(o => o.ShippingAddress, address =>
        {
            address.Property(a => a.Street).HasMaxLength(200);
            address.Property(a => a.City).HasMaxLength(100);
            address.Property(a => a.ZipCode).HasMaxLength(10);
        });

        // Shadow property
        builder.Property<DateTime>("LastModified").HasDefaultValueSql("GETUTCDATE()");

        // Query filter (soft delete)
        builder.HasQueryFilter(o => o.Status != OrderStatus.Deleted);
    }
}
```

---

## Relaciones

### One-to-Many

```csharp
public class Order
{
    public Guid Id { get; set; }
    public List<OrderItem> Items { get; set; } = [];
}

public class OrderItem
{
    public Guid Id { get; set; }
    public Guid OrderId { get; set; } // FK shadow o explícita
    public string Sku { get; set; }
}

// Config
builder.HasMany(o => o.Items)
    .WithOne()
    .HasForeignKey(i => i.OrderId)
    .IsRequired();
```

### Many-to-Many (.NET 5+ sin entidad join explícita)

```csharp
public class Student
{
    public int Id { get; set; }
    public List<Course> Courses { get; set; } = [];
}

public class Course
{
    public int Id { get; set; }
    public List<Student> Students { get; set; } = [];
}

// EF Core crea StudentCourse automáticamente
// Si se necesita payload en la tabla join → crear entidad explícita

public class Enrollment // Join con payload
{
    public int StudentId { get; set; }
    public int CourseId { get; set; }
    public DateTime EnrolledAt { get; set; }
    public decimal Grade { get; set; }
}
```

### One-to-One

```csharp
builder.HasOne(o => o.Invoice)
    .WithOne(i => i.Order)
    .HasForeignKey<Invoice>(i => i.OrderId);
```

---

## Queries optimizadas

### Proyección (lo más importante)

```csharp
// ❌ Traer todas las columnas cuando solo necesitas 2
var orders = await db.Orders
    .Include(o => o.Items)
    .Include(o => o.Customer)
    .ToListAsync(ct); // SELECT * en 3 tablas

// ✅ Proyección a DTO — solo las columnas necesarias
var orders = await db.Orders
    .Where(o => o.Status == OrderStatus.Pending)
    .Select(o => new OrderSummaryDto(
        o.Id,
        o.CustomerId,
        o.Total.Amount,
        o.CreatedAt))
    .ToListAsync(ct); // SELECT o.Id, o.CustomerId, o.TotalAmount, o.CreatedAt FROM Orders
```

### AsNoTracking

```csharp
// ✅ Siempre para queries de solo lectura
var orders = await db.Orders
    .AsNoTracking()
    .Where(o => o.Status == OrderStatus.Pending)
    .ToListAsync(ct);

// ✅ AsNoTrackingWithIdentityResolution — tracking sin overhead de cambio
// Útil cuando necesitas que el mismo registro sea la misma instancia
var orders = await db.Orders
    .AsNoTrackingWithIdentityResolution()
    .Include(o => o.Items)
    .ToListAsync(ct);
```

### Split queries (evitar explosión cartesiana)

```csharp
// ❌ Include múltiple genera JOIN explosivo
var orders = await db.Orders
    .Include(o => o.Items)
    .Include(o => o.Discounts)
    .Include(o => o.Taxes)
    .ToListAsync(ct);

// ✅ Split query — queries separadas por cada Include
var orders = await db.Orders
    .Include(o => o.Items)
    .Include(o => o.Discounts)
    .Include(o => o.Taxes)
    .AsSplitQuery()
    .ToListAsync(ct);

// O global para todas las queries
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString, o => o.UseQuerySplittingBehavior(QuerySplittingBehavior.SplitQuery)));
```

### Compiled queries (rendimiento extremo)

```csharp
// Compilada una vez, ejecutada N veces
private static readonly Func<AppDbContext, Guid, CancellationToken, Task<Order?>> GetOrderById =
    EF.CompileAsyncQuery((AppDbContext db, Guid id, CancellationToken ct) =>
        db.Orders.AsNoTracking().FirstOrDefault(o => o.Id == id));

// Uso
var order = await GetOrderById(db, orderId, ct);
```

### LeftJoin y RightJoin (.NET 10)

```csharp
// ✅ LeftJoin — antes requería GroupJoin + DefaultIfEmpty + SelectMany
var ordersWithPayments = await db.Orders
    .LeftJoin(db.Payments, o => o.Id, p => p.OrderId, (o, p) => new
    {
        o.Id,
        o.Total,
        Payment = p != null ? new { p.Amount, p.Status } : null
    })
    .ToListAsync(ct);

// ✅ RightJoin
var productsWithOrders = await db.Products
    .RightJoin(db.OrderItems, p => p.Id, oi => oi.ProductId, (p, oi) => new { p, oi })
    .ToListAsync(ct);

// Se traducen a LEFT JOIN / RIGHT JOIN SQL nativos.
```

### Like y Full-Text Search

```csharp
// EF.Functions.Like para búsquedas con patrón
var results = await db.Orders
    .Where(o => EF.Functions.Like(o.CustomerId, $"%{searchTerm}%"))
    .ToListAsync(ct);

// Full-Text Search con raw SQL (no hay API de alto nivel en EF Core)
var results = await db.Orders
    .FromSql($"SELECT * FROM Orders WHERE CONTAINS(Notes, {searchTerm})")
    .ToListAsync(ct);
```

---

## Raw SQL

```csharp
// Query: retorna entidades tracked
var orders = await db.Orders
    .FromSql($"SELECT * FROM Orders WHERE Status = {status}")
    .ToListAsync(ct);

// Query: retorna tipos no mapeados
var summaries = await db.Database
    .SqlQuery<OrderSummary>($"SELECT Id, TotalAmount FROM Orders WHERE CreatedAt > {since}")
    .ToListAsync(ct);

// Execute: INSERT/UPDATE/DELETE sin resultados
var rows = await db.Database
    .ExecuteSqlAsync($"UPDATE Orders SET Status = {newStatus} WHERE CreatedAt < {cutoff}");
// rows = número de filas afectadas

// ExecuteDelete / ExecuteUpdate (bulk, sin cargar entidades) — .NET 7+
await db.Orders
    .Where(o => o.Status == OrderStatus.Pending && o.CreatedAt < cutoff)
    .ExecuteUpdateAsync(s => s
        .SetProperty(o => o.Status, OrderStatus.Expired)
        .SetProperty(o => o.LastModified, DateTime.UtcNow),
        ct);
```

### SQL parametrizado — siempre

```csharp
// ✅ Interpolación parametriza automáticamente en FromSql
var id = Guid.NewGuid();
var orders = await db.Orders.FromSql($"SELECT * FROM Orders WHERE Id = {id}").ToListAsync(ct);
// EF Core genera: SELECT * FROM Orders WHERE Id = @p0

// ✅ FormattableString para queries dinámicas seguras
FormattableString query = $"SELECT * FROM Orders WHERE Status = {status}";
if (customerId is not null)
    query = $"{query} AND CustomerId = {customerId}";
var orders = await db.Orders.FromSql(query).ToListAsync(ct);
```

---

## Migraciones

### Workflow

```bash
# Crear migración
dotnet ef migrations add AddOrderShippingAddress -s src/MiApp.Api -p src/MiApp.Infrastructure

# Generar script SQL (para revisión)
dotnet ef migrations script -s src/MiApp.Api -p src/MiApp.Infrastructure -o migrate.sql

# Aplicar migraciones
dotnet ef database update -s src/MiApp.Api -p src/MiApp.Infrastructure
```

### Migraciones en producción

```csharp
// Aplicar migraciones al iniciar (solo para apps pequeñas/medianas)
var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    await db.Database.MigrateAsync(); // Aplica migraciones pendientes
}

// Para producción: generar script y ejecutar manualmente o vía CI/CD
// dotnet ef migrations script --idempotent → genera script con IF NOT EXISTS
```

### Migraciones sin downtime

- **Add column**: `ALTER TABLE ADD COLUMN` no bloquea lecturas/escrituras
- **Add column NOT NULL**: agregar como nullable, backfill, luego hacer NOT NULL en otra migración
- **Rename column**: riesgo. Mejor: add new column, copiar datos, eliminar old column en migración posterior
- **Drop column**: mantener una versión, eliminar en migración siguiente (por si hay rollback)

---

## Interceptors

```csharp
// Auditable interceptor
public class AuditableInterceptor : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken ct = default)
    {
        var db = eventData.Context!;
        var now = DateTime.UtcNow;

        foreach (var entry in db.ChangeTracker.Entries<IAuditable>())
        {
            switch (entry.State)
            {
                case EntityState.Added:
                    entry.Property(nameof(IAuditable.CreatedAt)).CurrentValue = now;
                    break;
                case EntityState.Modified:
                    entry.Property(nameof(IAuditable.UpdatedAt)).CurrentValue = now;
                    break;
            }
        }

        return new(result);
    }
}

// Registrar interceptor
services.AddDbContext<AppDbContext>((sp, options) =>
{
    options.UseSqlServer(connectionString);
    options.AddInterceptors(sp.GetRequiredService<AuditableInterceptor>());
});
```

### Dispatch domain events interceptor

```csharp
public class DomainEventInterceptor(IPublisher publisher) : SaveChangesInterceptor
{
    public override async ValueTask<int> SavedChangesAsync(
        SaveChangesCompletedEventData eventData,
        int result,
        CancellationToken ct = default)
    {
        if (eventData.Context is not null)
            await DispatchDomainEvents(eventData.Context, ct);

        return result;
    }

    private async Task DispatchDomainEvents(DbContext db, CancellationToken ct)
    {
        var events = db.ChangeTracker
            .Entries<IAggregateRoot>()
            .SelectMany(e => e.Entity.DomainEvents)
            .ToList();

        foreach (var domainEvent in events)
            await publisher.Publish(domainEvent, ct);
    }
}
```

---

## Concurrencia

### Optimistic concurrency con RowVersion

```csharp
public class Order
{
    // Timestamp/RowVersion — EF Core lo maneja automáticamente
    [Timestamp]
    public byte[] RowVersion { get; set; } = [];
}

// Config
builder.Property(o => o.RowVersion).IsRowVersion();

// Al guardar, EF Core compara el RowVersion
// Si cambió → DbUpdateConcurrencyException

try
{
    await db.SaveChangesAsync(ct);
}
catch (DbUpdateConcurrencyException ex)
{
    foreach (var entry in ex.Entries)
    {
        var proposed = (Order)entry.Entity;
        var databaseValues = await entry.GetDatabaseValuesAsync(ct);
        // Decidir: gana cliente, gana BD, o merge
        entry.OriginalValues.SetValues(databaseValues);
        // Reintentar
    }
}
```

### Concurrency token alternativo

```csharp
// Guid como token de concurrencia
builder.Property(o => o.Version)
    .IsConcurrencyToken()
    .HasDefaultValue(Guid.NewGuid());

// Cada vez que guardas, generas nuevo GUID
order.Version = Guid.NewGuid();
// EF Core WHERE Version = @oldVersion; si no coincide → concurrencia
```

---

## Performance

### Find vs FirstOrDefault

```csharp
// Find: busca por PK, revisa el tracker primero. Para operaciones frecuentes.
var order = await db.Orders.FindAsync([id], ct);

// FirstOrDefault: siempre va a la BD (si no está tracked). Para queries con filtros.
var order = await db.Orders.FirstOrDefaultAsync(o => o.Id == id, ct);
```

### Paginación eficiente (Keyset / Seek)

```csharp
// ❌ Offset pagination — lento en páginas altas
var page = await db.Orders
    .OrderBy(o => o.CreatedAt)
    .Skip(pageSize * pageNumber)
    .Take(pageSize)
    .ToListAsync(ct);

// ✅ Keyset pagination — usa índice, rendimiento constante
var page = await db.Orders
    .Where(o => o.CreatedAt > lastCreatedAt)
    .OrderBy(o => o.CreatedAt)
    .Take(pageSize)
    .ToListAsync(ct);
```

### Batch updates / deletes (.NET 7+)

```csharp
// ❌ Cargar entidades, modificar, guardar: N roundtrips
var orders = await db.Orders.Where(o => o.Status == OrderStatus.Pending).ToListAsync(ct);
foreach (var o in orders) o.Status = OrderStatus.Expired;
await db.SaveChangesAsync(ct);

// ✅ ExecuteUpdate: 1 roundtrip, sin cargar entidades
await db.Orders
    .Where(o => o.Status == OrderStatus.Pending && o.CreatedAt < cutoff)
    .ExecuteUpdateAsync(s => s.SetProperty(o => o.Status, OrderStatus.Expired), ct);
```

### Plan de consulta: ToQueryString()

```csharp
var query = db.Orders
    .Include(o => o.Items)
    .Where(o => o.Total.Amount > 1000);

Console.WriteLine(query.ToQueryString());
// Muestra el SQL generado — copiar a SSMS y ver plan de ejecución
```

---

## Patrones avanzados

### Vector Search (.NET 10 + SQL Server 2025)

```csharp
// EF Core 10 soporta búsqueda por similitud vectorial
// Requiere SQL Server 2025 o Azure SQL con vector type

// Almacenar embeddings
modelBuilder.Entity<Product>()
    .Property(p => p.DescriptionEmbedding)
    .HasColumnType("vector(1536)"); // 1536-dimensiones (modelo OpenAI Ada)

// Búsqueda por similitud
var queryEmbedding = await embeddingService.GetEmbeddingAsync(searchText);

var results = await db.Products
    .OrderBy(p => EF.Functions.VectorDistance(p.DescriptionEmbedding, queryEmbedding))
    .Take(top: 10)
    .Select(p => new { p.Name, p.Description, p.Price })
    .ToListAsync(ct);
```

### Value Converters

```csharp
// Guardar enum como string
builder.Property(o => o.Status)
    .HasConversion<string>()
    .HasMaxLength(20);

// Value Object ↔ columna(s)
builder.ComplexProperty(o => o.Total); // .NET 8+ (antes Owned Type)

// Custom converter
builder.Property(o => o.Tags)
    .HasConversion(
        v => string.Join(',', v),
        v => v.Split(',', StringSplitOptions.RemoveEmptyEntries).ToList())
    .HasMaxLength(500);
```

### Shadow Properties

```csharp
// Definir propiedad que no está en el modelo C#
modelBuilder.Entity<Order>().Property<DateTime>("LastModified");

// Usar en queries
var orders = await db.Orders
    .Where(o => EF.Property<DateTime>(o, "LastModified") > DateTime.UtcNow.AddDays(-7))
    .ToListAsync(ct);

// Actualizar vía interceptor, no en código de negocio
```

### TPH / TPT / TPC Inheritance

```csharp
// TPH (Table Per Hierarchy) — default, todo en una tabla con discriminador
public abstract class Payment { public int Id { get; set; } }
public class CreditCardPayment : Payment { public string LastFour { get; set; } }
public class BankTransferPayment : Payment { public string BankCode { get; set; } }

// Config
modelBuilder.Entity<Payment>()
    .HasDiscriminator<string>("PaymentType")
    .HasValue<CreditCardPayment>("CC")
    .HasValue<BankTransferPayment>("TRANSFER");

// TPT (Table Per Type) — tablas separadas para cada tipo — .NET 5+
modelBuilder.Entity<Payment>().UseTptStrategy();

// TPC (Table Per Concrete Type) — .NET 7+
modelBuilder.Entity<Payment>().UseTpcStrategy();
```

### Global Query Filters

```csharp
// Soft delete automático
builder.HasQueryFilter(o => o.Status != OrderStatus.Deleted);

// Multi-tenant
builder.HasQueryFilter(o => o.TenantId == _currentTenantId);

// Ignorar filtro cuando sea necesario
var allOrders = await db.Orders.IgnoreQueryFilters().ToListAsync(ct);
```

### HiLo / Sequence para keys

```csharp
// Sequences para IDs numéricos (reduce roundtrips vs IDENTITY)
modelBuilder.HasSequence<int>("OrderNumbers", schema: "sales")
    .StartsAt(1000)
    .IncrementsBy(10);

builder.Property(o => o.OrderNumber)
    .HasDefaultValueSql("NEXT VALUE FOR sales.OrderNumbers");
```

---

## Anti-patrones EF Core

| Anti-patrón | Problema | Solución |
|-------------|----------|----------|
| `Include` todo | N+1 inverso (over-fetching) | Proyección con `.Select()` |
| `ToList()` temprano | Trae toda la tabla a memoria | Mantener `IQueryable`, materializar al final |
| `SaveChanges` por entidad | Múltiples roundtrips | Un solo `SaveChangesAsync` al final de la operación |
| Repo genérico `IRepository<T>` | No agrega valor sobre DbSet | Métodos de extensión o repos específicos con queries nombradas |
| `AsNoTracking` nunca usado | Tracking overhead en queries de lectura | Siempre en GETs/lecturas |
| Migraciones sin revisar | SQL generado puede romper en producción | `dotnet ef migrations script` y revisar antes de aplicar |
| `async` sin CancellationToken | Query no cancelable | Pasar `ct` a todos los métodos EF |

---

## Checklist EF Core

- [ ] Configuraciones en clases separadas `IEntityTypeConfiguration<T>`
- [ ] `ApplyConfigurationsFromAssembly` en OnModelCreating
- [ ] `ConfigureConventions` para reglas globales (max length, precision)
- [ ] Proyección con `.Select()` en vez de `.Include()` + mapeo manual
- [ ] `AsNoTracking()` en todas las queries de lectura
- [ ] `AsSplitQuery()` con múltiples Includes
- [ ] `ExecuteUpdate`/`ExecuteDelete` para operaciones batch
- [ ] Concurrent handling con RowVersion o concurrency token
- [ ] Migraciones revisadas con `migrations script` antes de producción
- [ ] Connection resiliency con `EnableRetryOnFailure`
- [ ] CancellationToken propagado a todos los métodos async
