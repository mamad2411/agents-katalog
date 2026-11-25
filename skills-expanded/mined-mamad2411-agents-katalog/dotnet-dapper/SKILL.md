---
name: dotnet-dapper
description: "Dapper 2.1 en .NET 10. Cubre queries y comandos tipados, mapeo one-to-many (splitOn), stored procedures, transacciones, bulk operations, multi-mapping, y estrategia híbrida EF Core + Dapper (EF para writes, Dapper para reads). Actívala cuando el proyecto use Dapper como ORM, al optimizar queries de alto rendimiento, o al decidir entre EF Core y Dapper."
---

# Dapper — Micro-ORM para .NET

Guía de Dapper 2.1.79 (Mayo 2026) en .NET 10. Control total del SQL sin el overhead de un ORM completo.

---

## Setup

```bash
dotnet add package Dapper
dotnet add package Microsoft.Data.SqlClient  # SQL Server
dotnet add package Npgsql                    # PostgreSQL
```

```csharp
// Program.cs — registrar IDbConnection
builder.Services.AddScoped<IDbConnection>(sp =>
{
    var connectionString = sp.GetRequiredService<IConfiguration>()
        .GetConnectionString("Default");
    return new SqlConnection(connectionString);
});
```

---

## Queries básicas

```csharp
public class OrderRepository(IDbConnection db) : IOrderRepository
{
    // ✅ Query<T> — SELECT que retorna lista tipada
    public async Task<IEnumerable<Order>> GetByCustomerAsync(
        string customerId, CancellationToken ct)
    {
        const string sql = """
            SELECT Id, OrderNumber, CustomerId, Status, TotalAmount, CreatedAt
            FROM Sales.Orders
            WHERE CustomerId = @customerId
            ORDER BY CreatedAt DESC
            """;

        return await db.QueryAsync<Order>(sql, new { customerId });
    }

    // ✅ QueryFirstOrDefaultAsync — SELECT que retorna 1 o default
    public async Task<Order?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        const string sql = """
            SELECT Id, OrderNumber, CustomerId, Status, TotalAmount
            FROM Sales.Orders
            WHERE Id = @id
            """;

        return await db.QueryFirstOrDefaultAsync<Order>(sql, new { id });
    }

    // ✅ QuerySingleAsync — SELECT que DEBE retornar exactamente 1 fila
    public async Task<OrderStats> GetStatsAsync(string customerId, CancellationToken ct)
    {
        const string sql = """
            SELECT COUNT(*) AS OrderCount, SUM(TotalAmount) AS TotalSpent
            FROM Sales.Orders
            WHERE CustomerId = @customerId
            """;

        return await db.QuerySingleAsync<OrderStats>(sql, new { customerId });
    }

    // ✅ ExecuteAsync — INSERT/UPDATE/DELETE
    public async Task<int> CreateAsync(Order order, CancellationToken ct)
    {
        const string sql = """
            INSERT INTO Sales.Orders (Id, OrderNumber, CustomerId, Status, TotalAmount)
            VALUES (@Id, @OrderNumber, @CustomerId, @Status, @TotalAmount)
            """;

        return await db.ExecuteAsync(sql, order);
    }

    // ✅ ExecuteScalarAsync — INSERT con retorno de valor
    public async Task<int> GetNextOrderNumberAsync(CancellationToken ct)
    {
        const string sql = "SELECT NEXT VALUE FOR Sales.OrderNumbers";
        return await db.ExecuteScalarAsync<int>(sql);
    }
}
```

---

## Parámetros

```csharp
// ✅ Objeto anónimo (la forma más común)
await db.QueryAsync<Order>(sql, new { customerId, status = "pending" });

// ✅ DynamicParameters (para SPs con OUTPUT, TVPs, o direcciones)
var parameters = new DynamicParameters();
parameters.Add("@customerId", customerId);
parameters.Add("@status", "pending");
parameters.Add("@orderId", dbType: DbType.Guid, direction: ParameterDirection.Output);

await db.ExecuteAsync("Sales.usp_CreateOrder", parameters,
    commandType: CommandType.StoredProcedure);

var orderId = parameters.Get<Guid>("@orderId");

// ✅ Table-Valued Parameters (SQL Server)
var table = new DataTable();
table.Columns.Add("Sku", typeof(string));
table.Columns.Add("Quantity", typeof(int));
table.Columns.Add("UnitPrice", typeof(decimal));

foreach (var item in items)
    table.Rows.Add(item.Sku, item.Quantity, item.UnitPrice);

var parameters = new DynamicParameters();
parameters.Add("@items", table.AsTableValuedParameter("Sales.OrderItemType"));

await db.ExecuteAsync("Sales.usp_CreateOrderWithItems", parameters,
    commandType: CommandType.StoredProcedure);

// ✅ Lista de IDs con IN (Dapper expande automáticamente)
var ids = new[] { Guid.NewGuid(), Guid.NewGuid() };
await db.QueryAsync<Order>(
    "SELECT * FROM Sales.Orders WHERE Id IN @ids",
    new { ids });
// Genera: WHERE Id IN (@ids1, @ids2)
```

---

## Stored Procedures

```csharp
// ✅ Query desde SP
public async Task<IEnumerable<Order>> GetOrdersByStatusAsync(
    string status, CancellationToken ct)
{
    return await db.QueryAsync<Order>(
        "Sales.usp_GetOrdersByStatus",
        new { status },
        commandType: CommandType.StoredProcedure);
}

// ✅ SP con múltiples result sets (QueryMultiple)
public async Task<OrderWithItems?> GetOrderWithItemsAsync(Guid id, CancellationToken ct)
{
    const string sql = "Sales.usp_GetOrderWithItems";

    using var multi = await db.QueryMultipleAsync(sql, new { id },
        commandType: CommandType.StoredProcedure);

    var order = await multi.ReadSingleOrDefaultAsync<Order>();
    if (order is null) return null;

    order.Items = (await multi.ReadAsync<OrderItem>()).ToList();
    return order;
}

// ✅ SP con OUTPUT parameters
public async Task<Guid> CreateOrderWithOutputAsync(CreateOrderInput input, CancellationToken ct)
{
    var parameters = new DynamicParameters();
    parameters.Add("@customerId", input.CustomerId);
    parameters.Add("@totalAmount", input.TotalAmount);
    parameters.Add("@orderId", dbType: DbType.Guid, direction: ParameterDirection.Output);

    await db.ExecuteAsync("Sales.usp_CreateOrder", parameters,
        commandType: CommandType.StoredProcedure);

    return parameters.Get<Guid>("@orderId");
}
```

---

## Multi-mapping (one-to-many, one-to-one)

```csharp
// ✅ One-to-many con splitOn
public async Task<Order?> GetOrderWithItemsMultiMapAsync(Guid id, CancellationToken ct)
{
    const string sql = """
        SELECT o.Id, o.OrderNumber, o.Status, o.TotalAmount,
               oi.Id, oi.Sku, oi.Quantity, oi.UnitPrice
        FROM Sales.Orders o
        JOIN Sales.OrderItems oi ON oi.OrderId = o.Id
        WHERE o.Id = @id
        ORDER BY oi.LineNumber
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
            existing.Items.Add(item);
            return existing;
        },
        new { id },
        splitOn: "Id"  // Columna donde empieza OrderItem
    );

    return orderDict.Values.FirstOrDefault();
}

// ✅ splitOn explícito cuando la columna no es "Id"
const string sql2 = """
    SELECT o.Id, o.OrderNumber, o.CustomerId,
           c.Id AS CustomerId, c.Name
    FROM Sales.Orders o
    JOIN Catalog.Customers c ON o.CustomerId = c.Id
    WHERE o.Id = @id
    """;

await db.QueryAsync<Order, Customer, Order>(
    sql2,
    (order, customer) => { order.Customer = customer; return order; },
    new { id },
    splitOn: "CustomerId"  // Columna donde empieza el segundo tipo
);
```

---

## Transacciones

```csharp
// ✅ Transaction con IDbTransaction
public async Task CreateOrderWithItemsAsync(Order order, IEnumerable<OrderItem> items)
{
    using var transaction = db.BeginTransaction();
    try
    {
        await db.ExecuteAsync(
            "INSERT INTO Sales.Orders (...) VALUES (...)", order,
            transaction: transaction);

        foreach (var item in items)
        {
            await db.ExecuteAsync(
                "INSERT INTO Sales.OrderItems (...) VALUES (...)", item,
                transaction: transaction);
        }

        transaction.Commit();
    }
    catch
    {
        transaction.Rollback();
        throw;
    }
}

// ✅ Unit of Work con DbConnection compartido
public class OrderService
{
    public async Task ProcessAsync(CreateOrderCommand command, CancellationToken ct)
    {
        var connection = new SqlConnection(_connectionString);
        await connection.OpenAsync(ct);

        using var transaction = connection.BeginTransaction();
        try
        {
            var repo = new OrderRepository(connection);
            var paymentRepo = new PaymentRepository(connection);

            var order = await repo.CreateAsync(command.Order, ct, transaction);
            await paymentRepo.RecordAsync(order.Id, command.Payment, ct, transaction);

            transaction.Commit();
        }
        catch
        {
            transaction.Rollback();
            throw;
        }
    }
}
```

---

## Bulk operations (Dapper Plus o raw)

```csharp
// ✅ Bulk insert manual (Dapper no tiene Bulk nativo)
public async Task BulkInsertOrdersAsync(IEnumerable<Order> orders, CancellationToken ct)
{
    const string sql = """
        INSERT INTO Sales.Orders (Id, OrderNumber, CustomerId, Status, TotalAmount)
        VALUES (@Id, @OrderNumber, @CustomerId, @Status, @TotalAmount)
        """;

    await db.ExecuteAsync(sql, orders);  // Dapper itera automáticamente
    // ⚠️ Para >1000 filas, usar SqlBulkCopy o Dapper Plus
}

// ✅ SqlBulkCopy para volumen real (>1000 filas)
public async Task BulkInsertLargeAsync(IReadOnlyList<Order> orders, CancellationToken ct)
{
    using var bulk = new SqlBulkCopy((SqlConnection)db)
    {
        DestinationTableName = "Sales.Orders",
        BatchSize = 1000,
    };

    bulk.ColumnMappings.Add(nameof(Order.Id), "Id");
    bulk.ColumnMappings.Add(nameof(Order.OrderNumber), "OrderNumber");
    bulk.ColumnMappings.Add(nameof(Order.CustomerId), "CustomerId");

    var table = new DataTable();
    table.Columns.Add("Id", typeof(Guid));
    table.Columns.Add("OrderNumber", typeof(int));
    table.Columns.Add("CustomerId", typeof(string));

    foreach (var o in orders)
        table.Rows.Add(o.Id, o.OrderNumber, o.CustomerId);

    await bulk.WriteToServerAsync(table, ct);
}
```

---

## Estrategia híbrida: EF Core + Dapper

```csharp
// ✅ EF Core para writes (tracking, relaciones, migraciones)
public class OrderService(AppDbContext db)
{
    public async Task<Order> CreateAsync(Order order, CancellationToken ct)
    {
        db.Orders.Add(order);
        await db.SaveChangesAsync(ct);
        return order;
    }
}

// ✅ Dapper para reads de alto rendimiento (hot paths, reportes)
public class OrderReadRepository(IDbConnection db)
{
    public async Task<IEnumerable<OrderSummary>> GetCustomerOrdersAsync(
        string customerId, CancellationToken ct)
    {
        const string sql = """
            SELECT o.Id, o.OrderNumber, o.Status, o.TotalAmount, o.CreatedAt,
                   COUNT(oi.Id) AS ItemCount
            FROM Sales.Orders o
            LEFT JOIN Sales.OrderItems oi ON oi.OrderId = o.Id
            WHERE o.CustomerId = @customerId
            GROUP BY o.Id, o.OrderNumber, o.Status, o.TotalAmount, o.CreatedAt
            ORDER BY o.CreatedAt DESC
            """;

        return await db.QueryAsync<OrderSummary>(sql, new { customerId });
    }
}

// Registro en DI
builder.Services.AddDbContext<AppDbContext>(...);     // EF Core
builder.Services.AddScoped<IDbConnection>(...);       // Dapper
builder.Services.AddScoped<OrderReadRepository>();    // Read side
```

---

## ¿Dapper o EF Core?

| Criterio | EF Core | Dapper |
|----------|---------|--------|
| **Productividad** | ✅ Alta (LINQ, auto-track, migraciones) | Medio (SQL manual) |
| **Rendimiento reads** | ~5% más lento que Dapper hoy (2026) | ✅ Máximo control |
| **Writes** | ✅ Change tracker, batch updates | SQL manual |
| **Relaciones** | ✅ Navegación automática | Manual con multi-mapping |
| **Migraciones** | ✅ Built-in | No (usar Flyway/DbUp) |
| **Raw SQL** | `FromSql()`, `ExecuteSql()` | ✅ Nativo |
| **Curva aprendizaje** | Media | Baja (si sabes SQL) |

**Regla 2026**: EF Core por defecto. Dapper para:
- Queries de solo lectura en hot paths (>1000 req/s)
- Reportes y agregaciones con SQL complejo
- Stored procedures legacy que no justifican migrar a EF Core
- Equipos que prefieren control absoluto del SQL

---

## Checklist Dapper

- [ ] `IDbConnection` registrado como Scoped en DI
- [ ] Parámetros siempre con objetos anónimos o `DynamicParameters` (nunca concatenación SQL)
- [ ] `splitOn` correcto en multi-mapping (default "Id", override explícito)
- [ ] Transacciones con `BeginTransaction()` + `Commit()`/`Rollback()`
- [ ] Para >1000 filas, usar `SqlBulkCopy` en vez de `ExecuteAsync`
- [ ] `CancellationToken` propagado a todos los métodos async
- [ ] Híbrido: EF Core para writes, Dapper para reads de alto rendimiento
- [ ] Sin concatenar SQL crudo — usar verbatim strings (`"""`) y parámetros
