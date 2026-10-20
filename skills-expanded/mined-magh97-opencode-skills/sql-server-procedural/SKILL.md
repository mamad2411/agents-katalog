---
name: sql-server-procedural
description: "Programación en T-SQL: stored procedures, funciones, triggers, vistas (indexadas), CTEs, TRY/CATCH/THROW y cursores. Úsala al implementar lógica en la base, migrar SPs legacy o diseñar APIs de datos."
disable-model-invocation: true
---

# SQL Server Procedural Programming

Guía de programación procedural en T-SQL. Toda lógica de negocio en la BD debe seguir estas convenciones.

---

## Stored Procedures

### Template estándar

```sql
CREATE OR ALTER PROCEDURE Sales.usp_CreateOrder
    @customerId     NVARCHAR(50),
    @items          Sales.OrderItemType READONLY, -- Table-Valued Parameter
    @orderId        UNIQUEIDENTIFIER OUTPUT,
    @orderNumber    INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON; -- Rollback automático en error

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Validación
        IF NOT EXISTS (SELECT 1 FROM Catalog.Customers WHERE Id = @customerId)
            THROW 50001, 'Customer not found', 1;

        -- Insert order
        SET @orderId = NEWID();
        SET @orderNumber = NEXT VALUE FOR Sales.OrderNumbers;

        INSERT INTO Sales.Orders (Id, OrderNumber, CustomerId, Status)
        VALUES (@orderId, @orderNumber, @customerId, 'Pending');

        -- Insert items
        INSERT INTO Sales.OrderItems (OrderId, Sku, Quantity, UnitPrice)
        SELECT @orderId, Sku, Quantity, UnitPrice FROM @items;

        -- Validate stock
        IF EXISTS (
            SELECT 1 FROM @items i
            JOIN Catalog.Products p ON i.Sku = p.Sku
            WHERE p.Stock < i.Quantity
        )
            THROW 50002, 'Insufficient stock for one or more items', 1;

        -- Deduct stock
        UPDATE Catalog.Products
        SET Stock -= i.Quantity
        FROM Catalog.Products p
        JOIN @items i ON p.Sku = i.Sku;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        THROW; -- Relanza con info original (error_number, message, line)
    END CATCH
END;
```

### Table-Valued Parameters (TVP)

```sql
-- Definir el tipo
CREATE TYPE Sales.OrderItemType AS TABLE (
    Sku        NVARCHAR(50)  NOT NULL,
    Quantity   INT           NOT NULL,
    UnitPrice  DECIMAL(18,4) NOT NULL
);

-- Llamar desde .NET con DataTable o SqlDataRecord
```

### OUTPUT parameters

```sql
-- OUTPUT con INSERTED
INSERT INTO Sales.Orders (...)
OUTPUT inserted.Id, inserted.OrderNumber INTO @outputIds (Id, OrderNumber)
VALUES (...);
```

---

## Funciones

### Tipos y cuándo usarlas

| Tipo | Retorna | Inline? | Performance | Cuándo |
|------|---------|---------|-------------|--------|
| **Inline TVF** | Table | Sí | ✅ Excelente | Views parametrizadas |
| **Multi-statement TVF** | Table | No | ⚠️ Pobre | Evitar. Usar inline TVF. |
| **Scalar** | Valor único | No | ⚠️ Ejecuta por fila | Solo para cálculos simples |

### Inline Table-Valued Function (preferida)

```sql
CREATE OR ALTER FUNCTION Sales.ufn_GetOrdersByCustomer (@customerId NVARCHAR(50))
RETURNS TABLE
AS
RETURN (
    SELECT o.Id, o.OrderNumber, o.Status, o.TotalAmount, o.CreatedAt,
           oi.Sku, oi.Quantity, oi.UnitPrice
    FROM Sales.Orders o
    JOIN Sales.OrderItems oi ON o.Id = oi.OrderId
    WHERE o.CustomerId = @customerId
);
-- El optimizador expande esto inline. Es como una vista parametrizada.

-- Uso
SELECT * FROM Sales.ufn_GetOrdersByCustomer('CUST-001');
```

### Scalar function (con moderación)

```sql
CREATE OR ALTER FUNCTION Sales.ufn_CalculateTax (@amount DECIMAL(18,4), @rate DECIMAL(5,4))
RETURNS DECIMAL(18,4)
AS
BEGIN
    RETURN ROUND(@amount * @rate, 2);
END;
-- ⚠️ Se ejecuta por cada fila. Para >1000 filas, inline mejor.
```

---

## Triggers

### AFTER Trigger (auditoría)

```sql
CREATE OR ALTER TRIGGER Sales.trg_Orders_Audit
ON Sales.Orders
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Capturar inserts
    INSERT INTO Audit.OrderChanges (OrderId, ActionType, OldStatus, NewStatus, ChangedAt, ChangedBy)
    SELECT
        i.Id,
        'INSERT',
        NULL,
        i.Status,
        SYSUTCDATETIME(),
        SUSER_SNAME()
    FROM inserted i;

    -- Capturar updates
    INSERT INTO Audit.OrderChanges (OrderId, ActionType, OldStatus, NewStatus, ChangedAt, ChangedBy)
    SELECT
        d.Id,
        'UPDATE',
        d.Status,
        i.Status,
        SYSUTCDATETIME(),
        SUSER_SNAME()
    FROM inserted i
    JOIN deleted d ON i.Id = d.Id
    WHERE i.Status <> d.Status;

    -- Capturar deletes
    INSERT INTO Audit.OrderChanges (OrderId, ActionType, OldStatus, NewStatus, ChangedAt, ChangedBy)
    SELECT
        d.Id,
        'DELETE',
        d.Status,
        NULL,
        SYSUTCDATETIME(),
        SUSER_SNAME()
    FROM deleted d;
END;
```

### INSTEAD OF Trigger (lógica de negocio compleja)

```sql
CREATE OR ALTER TRIGGER Sales.trg_Orders_SoftDelete
ON Sales.Orders
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- Convertir DELETE en soft delete
    UPDATE o
    SET Status = 'Deleted', DeletedAt = SYSUTCDATETIME()
    FROM Sales.Orders o
    JOIN deleted d ON o.Id = d.Id;
END;
```

### Reglas de triggers

- ✅ Simples: pocas líneas, una responsabilidad.
- ✅ `SET NOCOUNT ON` al inicio.
- ✅ Manejar multi-fila: `inserted` y `deleted` pueden contener múltiples filas.
- ❌ Sin cursores: usar operaciones basadas en conjuntos.
- ❌ Sin transacciones dentro de triggers.
- ❌ Sin triggers recursivos (pueden deshabilitarse: `RECURSIVE_TRIGGERS OFF`).

---

## Vistas

### Vistas simples

```sql
CREATE OR ALTER VIEW Sales.vw_OrderDetails
AS
SELECT
    o.Id,
    o.OrderNumber,
    o.CustomerId,
    c.Name AS CustomerName,
    o.Status,
    o.TotalAmount,
    o.Currency,
    o.CreatedAt,
    (SELECT COUNT(*) FROM Sales.OrderItems oi WHERE oi.OrderId = o.Id) AS ItemCount
FROM Sales.Orders o
JOIN Catalog.Customers c ON o.CustomerId = c.Id
WHERE o.Status <> 'Deleted';
```

### Vistas indexadas (materializadas)

```sql
CREATE OR ALTER VIEW Sales.vw_OrderSummary
WITH SCHEMABINDING
AS
SELECT
    o.CustomerId,
    o.Status,
    COUNT_BIG(*) AS OrderCount,
    SUM(o.TotalAmount) AS TotalAmount
FROM Sales.Orders o
GROUP BY o.CustomerId, o.Status;

-- Crear índice clustered único (materializa la vista)
CREATE UNIQUE CLUSTERED INDEX IX_vw_OrderSummary
ON Sales.vw_OrderSummary (CustomerId, Status);
```

Vistas indexadas = aggregates pre-calculados. Útiles para dashboards y reportes.

---

## Manejo de errores

```sql
-- THROW (SQL 2012+) — preferido sobre RAISERROR
THROW 50001, 'Customer not found', 1;
-- error_number 50000+ (usuario), message, state (0-255)

-- TRY/CATCH completo
BEGIN TRY
    INSERT INTO Sales.Orders (...) VALUES (...);
END TRY
BEGIN CATCH
    DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
    DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
    DECLARE @ErrorState INT = ERROR_STATE();

    -- Log error
    INSERT INTO Audit.Errors (ErrorMessage, ErrorProcedure, ErrorLine, ErrorTime)
    VALUES (@ErrorMessage, ERROR_PROCEDURE(), ERROR_LINE(), SYSUTCDATETIME());

    -- Relanzar (si es apropiado)
    THROW;
END CATCH;
```

---

## Cursores — cuándo evitarlos

❌ **Nunca usar cursores para operaciones que pueden hacerse con conjuntos (SET-based).**

```sql
-- ❌ Cursor — fila por fila, lento
DECLARE cur CURSOR FOR SELECT Id FROM Sales.Orders WHERE Status = 'Pending';
OPEN cur;
FETCH NEXT FROM cur INTO @orderId;
WHILE @@FETCH_STATUS = 0
BEGIN
    EXEC ProcessOrder @orderId;
    FETCH NEXT FROM cur INTO @orderId;
END;
CLOSE cur;
DEALLOCATE cur;

-- ✅ SET-based — una sola operación, rápido
UPDATE Sales.Orders SET Status = 'Expired'
WHERE Status = 'Pending' AND CreatedAt < DATEADD(HOUR, -24, SYSUTCDATETIME());
```

Único caso justificable: operación que **no puede** hacerse con conjuntos (ej: llamar a SP externo que espera un solo ID por llamada). Aun así, usar `WHILE` + `TOP 1` + `DELETE` es más eficiente que cursor.

---

## Parámetros por defecto y opcionales

```sql
CREATE OR ALTER PROCEDURE Sales.usp_SearchOrders
    @customerId   NVARCHAR(50) = NULL,
    @status       NVARCHAR(20) = NULL,
    @minAmount    DECIMAL(18,4) = NULL,
    @maxAmount    DECIMAL(18,4) = NULL,
    @fromDate     DATETIME2 = NULL,
    @pageSize     INT = 50,
    @page         INT = 1
AS
BEGIN
    SELECT Id, OrderNumber, CustomerId, Status, TotalAmount, CreatedAt
    FROM Sales.Orders
    WHERE (@customerId IS NULL OR CustomerId = @customerId)
      AND (@status IS NULL OR Status = @status)
      AND (@minAmount IS NULL OR TotalAmount >= @minAmount)
      AND (@maxAmount IS NULL OR TotalAmount <= @maxAmount)
      AND (@fromDate IS NULL OR CreatedAt >= @fromDate)
    ORDER BY CreatedAt DESC
    OFFSET (@page - 1) * @pageSize ROWS
    FETCH NEXT @pageSize ROWS ONLY;
END;
-- ⚠️ OPTION (RECOMPILE) recomendado para queries con muchos parámetros opcionales
```

---

## Checklist procedural

- [ ] `SET NOCOUNT ON` en todos los SPs
- [ ] `SET XACT_ABORT ON` para rollback automático en errores
- [ ] Transacciones con `BEGIN TRY/BEGIN CATCH/THROW`
- [ ] Nombres: `usp_Schema_ActionEntity` para SPs, `ufn_Schema_` para funciones
- [ ] Preferir inline TVFs sobre multi-statement y scalar
- [ ] Usar TVPs para pasar listas de datos a SPs
- [ ] Evitar cursores: usar SET-based siempre que sea posible
- [ ] Triggers simples y con manejo multi-fila
- [ ] Validar datos de entrada al inicio del SP
- [ ] `THROW` error numbers > 50000 para errores de negocio
- [ ] Vistas indexadas para agregados de alto consumo
- [ ] Log de errores en tabla de auditoría en CATCH
