---
name: sql-server-integration
description: "Integración de SQL Server con .NET: EF Core, Dapper, ADO.NET, connection strings, Azure SQL, transacciones distribuidas y mejores prácticas de conexión. Actívala al configurar la capa de datos en apps .NET, optimizar acceso a datos, o migrar código de ADO.NET a EF Core/Dapper. No para migración de esquema (ver sql-server-deployment)."
disable-model-invocation: true
---

# SQL Server Integration with .NET

Guía de integración entre SQL Server y aplicaciones .NET. Cubre los tres stacks principales: EF Core, Dapper y ADO.NET directo.

---

## Connection Strings

```json
// appsettings.json
{
  "ConnectionStrings": {
    "Default": "Server=localhost;Database=MiApp;User Id=app_user;Password=***;TrustServerCertificate=True;",
    "Azure": "Server=tcp:miapp.database.windows.net;Authentication=Active Directory Default;Database=MiApp;",
    "ReadOnly": "Server=secondary;Database=MiApp;ApplicationIntent=ReadOnly;User Id=app_user;Password=***;"
  }
}
```

### Parámetros esenciales

| Parámetro | Recomendación | Motivo |
|-----------|---------------|--------|
| `Server` | FQDN o IP | `localhost` para dev, FQDN para prod |
| `Database` | Nombre de la DB | Siempre explícito |
| `TrustServerCertificate` | `True` (dev), `False` (prod) | Dev sin certificado TLS; prod con CA real |
| `Encrypt` | `True` (default desde v5) | Conexiones TLS |
| `ApplicationIntent` | `ReadOnly` para réplicas legibles | Routing a secundario en Always On |
| `Max Pool Size` | 100-200 según carga | Default 100 |
| `Connect Timeout` | 15 (default) | Subir a 30 si hay latencia de red |
| `MultipleActiveResultSets` | `False` si no se necesita MARS | MARS tiene overhead |
| `Application Name` | Nombre de la app | Identificación en sp_who/monitoreo |

---

## Entity Framework Core con SQL Server

### Configuración

```csharp
// Paquete: Microsoft.EntityFrameworkCore.SqlServer
builder.Services.AddDbContextPool<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default"),
        sqlOptions =>
        {
            // Migraciones
            sqlOptions.MigrationsAssembly(typeof(AppDbContext).Assembly.FullName);

            // Resiliencia: retry automático en errores transitorios
            sqlOptions.EnableRetryOnFailure(
                maxRetryCount: 3,
                maxRetryDelay: TimeSpan.FromSeconds(10),
                errorNumbersToAdd: [997]); // Errores de red adicionales

            // Timeout de comandos
            sqlOptions.CommandTimeout(30);

            // Split queries por defecto (.NET 7+)
            sqlOptions.UseQuerySplittingBehavior(QuerySplittingBehavior.SplitQuery);

            // Compatibilidad con Azure SQL
            // sqlOptions.UseAzureSqlDefaults();
        }));

// DbContext pool (mejor rendimiento)
// AddDbContextPool en vez de AddDbContext
```

### Connection Resiliency

```csharp
// Estrategia de retry personalizada
public class CustomRetryStrategy : SqlServerRetryingExecutionStrategy
{
    public CustomRetryStrategy(DbContext context, int maxRetryCount, TimeSpan maxRetryDelay)
        : base(context, maxRetryCount, maxRetryDelay) { }

    protected override bool ShouldRetryOn(Exception exception)
    {
        if (exception is SqlException sqlEx)
        {
            foreach (SqlError error in sqlEx.Errors)
            {
                switch (error.Number)
                {
                    case 4060: // Cannot use database
                    case 40197: // Azure throttle (error 4815 también)
                    case 40501: // Service busy
                    case 49918: // Not enough resources
                    case 49919: // Cannot process request
                    case 49920: // Service unavailable
                    case 11001: // Host not found (transitorio)
                        return true;
                }
            }
        }
        return base.ShouldRetryOn(exception);
    }
}
```

### Operaciones batch con EF Core

```csharp
// Bulk insert con SqlBulkCopy (recomendado para >1000 filas)
using var bulkCopy = new SqlBulkCopy(connectionString);
bulkCopy.DestinationTableName = "Sales.Orders";
bulkCopy.ColumnMappings.Add(nameof(Order.Id), "Id");
bulkCopy.ColumnMappings.Add(nameof(Order.OrderNumber), "OrderNumber");
// ...
await bulkCopy.WriteToServerAsync(dataTable, ct);

// Alternativa: EF Core ExecuteUpdate/ExecuteDelete (batch SQL)
await db.Orders
    .Where(o => o.Status == OrderStatus.Pending && o.CreatedAt < cutoff)
    .ExecuteUpdateAsync(s => s.SetProperty(o => o.Status, OrderStatus.Expired), ct);
```

---

## Dapper

Micro-ORM para queries de alto rendimiento. Control total del SQL.

```bash
dotnet add package Dapper
dotnet add package Microsoft.Data.SqlClient
```

### Configuración básica

```csharp
// Registrar SqlConnection factory
builder.Services.AddScoped<IDbConnection>(sp =>
{
    var connectionString = sp.GetRequiredService<IConfiguration>()
        .GetConnectionString("Default");
    return new SqlConnection(connectionString);
});

// Uso en handler
public class OrderRepository(IDbConnection db) : IOrderRepository
{
    public async Task<Order?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        const string sql = """
            SELECT o.*, oi.*
            FROM Sales.Orders o
            LEFT JOIN Sales.OrderItems oi ON oi.OrderId = o.Id
            WHERE o.Id = @id
            """;

        var orderDict = new Dictionary<Guid, Order>();

        await db.QueryAsync<Order, OrderItem, Order>(
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
            splitOn: "Id" // Columna donde empieza el mapping de OrderItem
        );

        return orderDict.Values.FirstOrDefault();
    }

    public async Task CreateAsync(Order order, CancellationToken ct)
    {
        const string sql = """
            INSERT INTO Sales.Orders (Id, OrderNumber, CustomerId, Status, TotalAmount, CreatedAt)
            VALUES (@Id, @OrderNumber, @CustomerId, @Status, @TotalAmount, @CreatedAt);
            """;

        await db.ExecuteAsync(sql, order);
    }

    public async Task<IEnumerable<OrderSummary>> GetByCustomerAsync(
        string customerId, int page, int pageSize, CancellationToken ct)
    {
        const string sql = """
            SELECT Id, OrderNumber, Status, TotalAmount, CreatedAt
            FROM Sales.Orders
            WHERE CustomerId = @customerId
            ORDER BY CreatedAt DESC
            OFFSET @offset ROWS FETCH NEXT @pageSize ROWS ONLY
            """;

        return await db.QueryAsync<OrderSummary>(sql, new
        {
            customerId,
            offset = (page - 1) * pageSize,
            pageSize
        });
    }

    public async Task BulkUpdateStatusAsync(
        string customerId, string oldStatus, string newStatus, CancellationToken ct)
    {
        const string sql = """
            UPDATE Sales.Orders
            SET Status = @newStatus, UpdatedAt = SYSUTCDATETIME()
            WHERE CustomerId = @customerId AND Status = @oldStatus
            """;

        var affected = await db.ExecuteAsync(sql, new { customerId, oldStatus, newStatus });
        // affected = número de filas actualizadas
    }
}
```

### Stored Procedures con Dapper

```csharp
// Llamar SP con parámetros
var result = await db.ExecuteAsync(
    "Sales.usp_CreateOrder",
    new
    {
        customerId = order.CustomerId,
        items = itemsTable,
        orderId = output,
        orderNumber = output
    },
    commandType: CommandType.StoredProcedure);
```

### One-to-Many mapping

```csharp
// Usando Dapper's QueryAsync con splitOn
const string sql = """
    SELECT o.Id, o.OrderNumber, o.Status,
           oi.Id, oi.Sku, oi.Quantity, oi.UnitPrice
    FROM Sales.Orders o
    JOIN Sales.OrderItems oi ON o.Id = oi.OrderId
    WHERE o.Id = @id
    """;

var orders = await db.QueryAsync<Order, OrderItem, Order>(
    sql,
    (order, item) =>
    {
        order.Items ??= [];
        order.Items.Add(item);
        return order;
    },
    new { id = orderId },
    splitOn: "Id");
```

---

## ADO.NET (Microsoft.Data.SqlClient)

```csharp
// Paquete: Microsoft.Data.SqlClient
public async Task<OrderDto?> GetOrderRawAsync(Guid orderId, CancellationToken ct)
{
    const string sql = """
        SELECT Id, OrderNumber, CustomerId, Status, TotalAmount, CreatedAt
        FROM Sales.Orders
        WHERE Id = @id
        """;

    await using var connection = new SqlConnection(_connectionString);
    await using var command = new SqlCommand(sql, connection);
    command.Parameters.AddWithValue("@id", orderId);

    await connection.OpenAsync(ct);
    await using var reader = await command.ExecuteReaderAsync(ct);

    if (!await reader.ReadAsync(ct))
        return null;

    return new OrderDto(
        reader.GetGuid(0),
        reader.GetInt32(1),
        reader.GetString(2),
        reader.GetString(3),
        reader.GetDecimal(4),
        reader.GetDateTime(5)
    );
}

// Bulk insert con SqlBulkCopy
public async Task BulkInsertOrdersAsync(IReadOnlyList<Order> orders, CancellationToken ct)
{
    using var table = new DataTable();
    table.Columns.Add("Id", typeof(Guid));
    table.Columns.Add("OrderNumber", typeof(int));
    table.Columns.Add("CustomerId", typeof(string));
    table.Columns.Add("Status", typeof(string));
    table.Columns.Add("TotalAmount", typeof(decimal));
    table.Columns.Add("CreatedAt", typeof(DateTime));

    foreach (var order in orders)
        table.Rows.Add(order.Id, order.OrderNumber, order.CustomerId,
            order.Status, order.TotalAmount, order.CreatedAt);

    await using var bulk = new SqlBulkCopy(_connectionString);
    bulk.DestinationTableName = "Sales.Orders";
    bulk.BatchSize = 1000;
    await bulk.WriteToServerAsync(table, ct);
}
```

---

## Azure SQL

### Connection string con DefaultAzureCredential

```csharp
// Paquete: Azure.Identity
builder.Services.AddDbContext<AppDbContext>(options =>
{
    var connection = new SqlConnection(builder.Configuration.GetConnectionString("Azure"));
    connection.AccessToken = await new DefaultAzureCredential()
        .GetTokenAsync(new TokenRequestContext(["https://database.windows.net/.default"]));

    options.UseSqlServer(connection);
});

// O usar Authentication=Active Directory Default en el connection string
// "Server=tcp:...;Authentication=Active Directory Default;Database=...;"
```

### Azure SQL vs SQL Server

| Característica | SQL Server | Azure SQL (Single DB) |
|---------------|------------|-----------------------|
| Administración | Self-managed | Managed (PaaS) |
| TDE | Opcional | Siempre habilitado ✅ |
| Backups | Manual/configurable | Automáticos (7-35 días) |
| HA | Configurable | SLA 99.995% |
| Scaling | Manual | Vertical + auto-scale |
| Cross-DB queries | `USE` / 3-part names | Elastic queries |
| SQL Agent | Disponible | Elastic Jobs |

---

## Manejo de transacciones

### TransactionScope (transacciones distribuidas)

```csharp
// ⚠️ Evitar TransactionScope en la nube. Preferir transacciones locales.
// Si es inevitable:
using var scope = new TransactionScope(TransactionScopeAsyncFlowOption.Enabled);
await orderRepo.CreateAsync(order, ct);
await paymentRepo.RecordPaymentAsync(payment, ct);
scope.Complete();
```

### Transaction local con DbContext

```csharp
await using var transaction = await db.Database.BeginTransactionAsync(ct);
try
{
    order.Approve();
    await db.SaveChangesAsync(ct);

    // Esto usa la misma transacción — una sola conexión
    await db.Payments.AddAsync(new Payment { OrderId = order.Id, ... }, ct);
    await db.SaveChangesAsync(ct);

    await transaction.CommitAsync(ct);
}
catch
{
    await transaction.RollbackAsync(ct);
    throw;
}
```

---

## Performance tips

```csharp
// 1. Siempre pasar CancellationToken
await db.Orders.FirstOrDefaultAsync(o => o.Id == id, ct); // ✅
await db.Orders.FirstOrDefaultAsync(o => o.Id == id);      // ❌

// 2. AsNoTracking para queries de lectura
var orders = await db.Orders.AsNoTracking().ToListAsync(ct);

// 3. Proyección en vez de Include
var dtos = await db.Orders
    .Select(o => new { o.Id, o.Status, o.TotalAmount })
    .ToListAsync(ct);

// 4. DbContext pool
builder.Services.AddDbContextPool<AppDbContext>(...);

// 5. Open connection explícito en Dapper (Dapper ya lo hace internamente)

// 6. Min Pool Size = 5-10 (evita reconexión en carga fría)
// "Min Pool Size=5;Max Pool Size=200;"
```

---

## Checklist de integración

- [ ] Connection resiliency configurada (`EnableRetryOnFailure`)
- [ ] DbContext registrado como Scoped o con Pooling
- [ ] `AsNoTracking()` en todas las queries de lectura
- [ ] CancellationToken propagado a todas las operaciones async
- [ ] Connection strings en `appsettings.json` (no hardcoded)
- [ ] `TrustServerCertificate=True` solo en desarrollo
- [ ] Application Name configurado para monitoreo
- [ ] Min Pool Size configurado para producción (5-10)
- [ ] Bulk insert con SqlBulkCopy para inserts >1000 filas
- [ ] ExecuteUpdate/ExecuteDelete para batch operations (EF Core 7+)
- [ ] TransactionScope evitado en Azure/cloud
