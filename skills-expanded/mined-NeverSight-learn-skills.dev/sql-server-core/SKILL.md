---
name: sql-server-core
description: "Guía principal de SQL Server (2019/2022/2025). Cubre T-SQL, arquitectura del motor, tipos de datos, DDL/DML, ediciones, herramientas (SSMS, Azure Data Studio, sqlcmd), bases de datos de sistema, y fundamentos del motor. Actívala para cualquier tarea SQL Server: nuevos desarrollos, revisión de queries, migraciones o diseño de base de datos. Las sub-skills del kit profundizan en dominios específicos."
---

# SQL Server Core Development Guide

Guía canónica para desarrollo en SQL Server. Cubre 2019, 2022 y 2025 (preview, GA Nov 2025). Todo código T-SQL generado sigue estas reglas salvo indicación contraria del usuario.

## Versiones y compatibilidad

| Versión          | Nivel | Lanzamiento | Soporte mainstream | Novedades clave |
|------------------|-------|-------------|-------------------|-----------------|
| SQL Server 2019  | 150   | Nov 2019    | Hasta Feb 2025    | UTF-8, `STRING_AGG`, Big Data Clusters |
| SQL Server 2022  | 160   | Nov 2022    | Hasta Ene 2033    | Ledger, `GREATEST`/`LEAST`, `IS [NOT] DISTINCT FROM`, Query Store en réplicas |
| SQL Server 2025  | 170   | Nov 2025    | —                 | **Vector type**, **regex**, T-SQL regex, PREVIEW_FEATURES |

- **Proyectos nuevos** → SQL Server 2022 (LTS estable). Adoptar 2025 cuando esté GA si se necesita vector/regex.
- **Migraciones** → 2019 → 2022 es seguro. 2019 → 2025 directo posible (compat level).
- **Azure SQL** → DB única o Managed Instance. Compatibilidad casi total con 2022.

---

## Arquitectura del motor

```
┌─────────────────────────────────────────────────┐
│                   Protocol Layer                 │
│     TDS (Tabular Data Stream) — 1433 TCP        │
├─────────────────────────────────────────────────┤
│                 Query Processor                  │
│  Parser → Algebrizer → Optimizer → Executor     │
│  (Parse Tree)  (Query Tree)  (Plan)  (Results)  │
├─────────────────────────────────────────────────┤
│                 Storage Engine                   │
│  Buffer Pool → Data Cache → Plan Cache          │
│  Pages (8KB) → Extents (64KB) → Files → FGs     │
├─────────────────────────────────────────────────┤
│                  Transaction Log                 │
│  WAL (Write-Ahead Logging) — VLFs → Log File    │
└─────────────────────────────────────────────────┘
```

### Páginas y extensiones

- **Página**: unidad mínima de I/O = 8 KB
- **Extensión**: 8 páginas contiguas = 64 KB
- **Tipos de página**: Data, Index, IAM (Index Allocation Map), GAM/SGAM, PFS
- **Fill factor**: % de espacio que se llena al crear/rebuild índice. Default 100 (sin espacio libre). Ajustar a 80-90 para tablas con updates frecuentes.

---

## Tipos de datos

### Numéricos

| Tipo | Rango | Bytes | Cuándo usar |
|------|-------|-------|-------------|
| `BIT` | 0/1/NULL | 1 (hasta 8 por byte) | Booleanos, flags |
| `TINYINT` | 0 a 255 | 1 | Edad, cantidad pequeña |
| `SMALLINT` | -32K a 32K | 2 | Año, status code |
| `INT` | -2B a 2B | 4 | IDs, cantidades generales ✅ |
| `BIGINT` | -9E a 9E | 8 | IDs grandes, contadores |
| `DECIMAL(p,s)` | Precisión fija | 5-17 | **Dinero, valores financieros** ✅ |
| `MONEY` / `SMALLMONEY` | Precisión fija | 8/4 | ⚠️ Evitar — `DECIMAL(19,4)` es mejor |
| `FLOAT` / `REAL` | Aproximado | 4/8 | Solo para cálculos científicos |
| `NUMERIC` | = `DECIMAL` | | Usar `DECIMAL` por claridad |

### Texto

| Tipo | Longitud | Uso |
|------|----------|-----|
| `CHAR(n)` | 1-8000, fija | Códigos de longitud fija (ISO3, SKU) |
| `VARCHAR(n)` | 1-8000, variable | Nombres, descripciones cortas |
| `VARCHAR(MAX)` | Hasta 2GB | Texto largo, JSON, XML |
| `NCHAR(n)` | = `CHAR` × 2 | Unicode longitud fija |
| `NVARCHAR(n)` | = `VARCHAR` × 2 | ✅ **Default para texto** en apps modernas |
| `NVARCHAR(MAX)` | Hasta 2GB | Texto Unicode largo |

### Fecha/hora

| Tipo | Rango | Precisión | Bytes |
|------|-------|-----------|-------|
| `DATE` | 0001-01-01 a 9999-12-31 | Día | 3 |
| `TIME(p)` | 00:00:00 a 23:59:59.999 | 0-7 (100ns) | 3-5 |
| `SMALLDATETIME` | 1900-2079 | Minuto | 4 |
| `DATETIME` | 1753-9999 | 3.33ms | 8 |
| `DATETIME2(p)` | 0001-9999 | 0-7 | 6-8 |
| `DATETIMEOFFSET` | = `DATETIME2` + tz | 0-7 | 8-10 |

✅ **Usar `DATETIME2` por defecto.** `DATETIME` es legacy y tiene precisión pobre.

### Otros

| Tipo | Uso |
|------|-----|
| `UNIQUEIDENTIFIER` | GUIDs. Usar `NEWSEQUENTIALID()` para PKs clustered |
| `ROWVERSION` / `TIMESTAMP` | Concurrencia optimista |
| `SQL_VARIANT` | ⚠️ Evitar — tipo genérico, sin soporte en EF Core bien |
| `XML` | Datos XML con esquema. Menos común, usar JSON |
| `GEOMETRY` / `GEOGRAPHY` | Datos espaciales |
| `HIERARCHYID` | Jerarquías (org charts, árboles) |
| `VECTOR(n)` | ⚠️ SQL 2025 preview — embeddings vectoriales |

---

## DDL — Creación de objetos

### Tablas

```sql
-- ✅ PK nombrada explícitamente, constraints con nombre
CREATE TABLE Sales.Orders (
    Id              UNIQUEIDENTIFIER    NOT NULL DEFAULT NEWSEQUENTIALID(),
    OrderNumber     INT                 NOT NULL,
    CustomerId      NVARCHAR(50)        NOT NULL,
    Status          NVARCHAR(20)        NOT NULL DEFAULT 'Pending',
    TotalAmount     DECIMAL(18,4)       NOT NULL DEFAULT 0,
    Currency        NCHAR(3)            NOT NULL DEFAULT 'MXN',
    CreatedAt       DATETIME2(3)        NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedAt       DATETIME2(3)        NOT NULL DEFAULT SYSUTCDATETIME(),
    RowVersion      ROWVERSION          NOT NULL,

    CONSTRAINT PK_Orders PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT CK_Orders_Status CHECK (Status IN ('Pending','Confirmed','Shipped','Delivered','Cancelled')),
    CONSTRAINT CK_Orders_TotalAmount CHECK (TotalAmount >= 0),
    CONSTRAINT CK_Orders_Currency CHECK (Currency IN ('MXN','USD','EUR'))
);

-- Índices
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId_Status
    ON Sales.Orders (CustomerId, Status)
    INCLUDE (TotalAmount, CreatedAt);

CREATE NONCLUSTERED INDEX IX_Orders_CreatedAt
    ON Sales.Orders (CreatedAt DESC);
```

### Schemas

```sql
-- Usar schemas para organizar objetos
CREATE SCHEMA Sales   AUTHORIZATION dbo;
CREATE SCHEMA Catalog AUTHORIZATION dbo;
CREATE SCHEMA Audit   AUTHORIZATION dbo;
```

### Secuencias

```sql
-- ✅ Preferir secuencias sobre IDENTITY para IDs de negocio
CREATE SEQUENCE Sales.OrderNumbers
    START WITH 1000
    INCREMENT BY 1
    NO CYCLE
    CACHE 50; -- Mejora rendimiento en inserts concurrentes

-- Uso
DECLARE @nextOrderNumber INT = NEXT VALUE FOR Sales.OrderNumbers;
```

---

## DML — Manipulación de datos

### INSERT

```sql
-- INSERT simple
INSERT INTO Sales.Orders (OrderNumber, CustomerId, TotalAmount)
VALUES (NEXT VALUE FOR Sales.OrderNumbers, @CustomerId, @Total);

-- INSERT con OUTPUT (capturar IDs generados)
INSERT INTO Sales.OrderItems (OrderId, Sku, Quantity, UnitPrice)
OUTPUT inserted.Id, inserted.LineNumber
VALUES (@OrderId, @Sku, @Qty, @Price);

-- INSERT múltiple
INSERT INTO Sales.OrderItems (OrderId, Sku, Quantity, UnitPrice)
VALUES
    (@OrderId, 'SKU-1', 2, 100.00),
    (@OrderId, 'SKU-2', 1,  50.00);

-- MERGE (upsert) — usar con precaución
MERGE INTO Catalog.Products AS tgt
USING (VALUES (@Sku, @Name, @Price)) AS src (Sku, Name, Price)
    ON tgt.Sku = src.Sku
WHEN MATCHED THEN
    UPDATE SET Name = src.Name, Price = src.Price, UpdatedAt = SYSUTCDATETIME()
WHEN NOT MATCHED THEN
    INSERT (Sku, Name, Price) VALUES (src.Sku, src.Name, src.Price);
-- ⚠️ MERGE tiene bugs históricos en concurrencia. Preferir IF EXISTS + INSERT/UPDATE.
```

### UPDATE

```sql
-- UPDATE con OUTPUT
UPDATE Sales.Orders
SET Status = 'Cancelled',
    CancelledAt = SYSUTCDATETIME(),
    CancellationReason = @Reason
OUTPUT inserted.Id, inserted.Status, inserted.UpdatedAt
WHERE Id = @OrderId
  AND Status = 'Pending'; -- Optimistic concurrency adicional

-- UPDATE multi-tabla (CTE)
;WITH ToExpire AS (
    SELECT o.Status
    FROM Sales.Orders o
    WHERE o.Status = 'Pending'
      AND o.CreatedAt < DATEADD(HOUR, -24, SYSUTCDATETIME())
)
UPDATE ToExpire SET Status = 'Expired';
```

### DELETE

```sql
-- DELETE con OUTPUT
DELETE FROM Sales.Orders
OUTPUT deleted.Id, deleted.OrderNumber, deleted.Status
WHERE Id = @OrderId
  AND Status IN ('Cancelled', 'Expired'); -- Soft delete preferido sobre DELETE físico

-- Soft delete (recomendado)
UPDATE Sales.Orders
SET Status = 'Deleted', DeletedAt = SYSUTCDATETIME()
WHERE Id = @OrderId;

-- TRUNCATE (sin logging de filas, más rápido, no se puede con FK)
TRUNCATE TABLE Staging.ImportBuffer;
```

---

## Herramientas

### SSMS (SQL Server Management Studio)

- IDE principal para SQL Server. Windows.
- Conexión: Server name, Authentication (Windows/SQL Server), Database.
- Object Explorer: navegar tablas, índices, procedures.
- Query Editor: CTRL+L = plan de ejecución estimado. CTRL+M = plan real.
- Activity Monitor: ver queries en ejecución, bloqueos, esperas.

### Azure Data Studio

- Multi-plataforma (Win, Mac, Linux).
- Extensible (extensiones: PostgreSQL, MySQL).
- Notebooks SQL integrados.
- Charts integrados desde resultados.

### Sqlcmd

```bash
sqlcmd -S localhost -d MiApp -Q "SELECT COUNT(*) FROM Sales.Orders"
sqlcmd -S localhost -d MiApp -i script.sql -o output.txt
```

---

## Bases de datos del sistema

| DB | Propósito |
|----|-----------|
| `master` | Metadatos de la instancia (logins, DBs, config). **Backup obligatorio.** |
| `model` | Template para crear nuevas bases de datos. Objetos aquí → en toda DB nueva. |
| `msdb` | Jobs, alerts, backups history. |
| `tempdb` | Objetos temporales (#tablas), sorts, spools. Se recrea al reiniciar. |
| `Resource` | Binarios del sistema (oculta, solo lectura). |

---

## Transacciones

```sql
-- Transacción explícita
BEGIN TRY
    BEGIN TRANSACTION;

    INSERT INTO Sales.Orders (...) VALUES (...);
    INSERT INTO Sales.OrderItems (...) VALUES (...);

    -- Validación de negocio
    IF EXISTS (SELECT 1 FROM Catalog.Products WHERE Sku = @Sku AND Stock < @Qty)
        THROW 50001, 'Insufficient stock', 1;

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    THROW; -- Relanza el error preservando info original
END CATCH
```

### Niveles de aislamiento

| Nivel | Dirty Read | Non-repeatable | Phantom | Uso |
|-------|------------|----------------|---------|-----|
| `READ UNCOMMITTED` | ✅ | ✅ | ✅ | Solo reportes no críticos |
| `READ COMMITTED` (default) | ❌ | ✅ | ✅ | **Default.** Bueno para la mayoría. |
| `REPEATABLE READ` | ❌ | ❌ | ✅ | Bloquea filas leídas. Poco usado. |
| `SNAPSHOT` | ❌ | ❌ | ❌ | ✅ Mejor para OLTP pesado. Usa tempdb. |
| `SERIALIZABLE` | ❌ | ❌ | ❌ | Máximo aislamiento. Mayor bloqueo. |

```sql
-- Habilitar SNAPSHOT en la base de datos
ALTER DATABASE MiApp SET READ_COMMITTED_SNAPSHOT ON;
-- Ahora READ COMMITTED usa row versioning en vez de locks
```

---

## Funciones del sistema útiles

```sql
-- String
SELECT CONCAT(FirstName, ' ', LastName) FROM Users;      -- Maneja NULL
SELECT STRING_AGG(Tag, ', ') WITHIN GROUP (ORDER BY Tag) -- SQL 2017+
SELECT STRING_SPLIT('a,b,c', ',')                        -- SQL 2016+
SELECT LEFT(CustomerId, 3), RIGHT(Phone, 4)
SELECT TRIM('  text  '), LTRIM(...), RTRIM(...)
SELECT REPLACE(Description, 'old', 'new')
SELECT TRANSLATE('123-456', '-', '') :: → no available, usar REPLACE anidado

-- Numérico
SELECT GREATEST(a, b, c), LEAST(a, b, c)                -- SQL 2022+
SELECT ROUND(123.456, 2), CEILING(123.1), FLOOR(123.9)

-- Fecha/hora
SELECT SYSUTCDATETIME(), SYSDATETIME(), GETDATE(), GETUTCDATE()
SELECT DATEADD(DAY, 7, CreatedAt), DATEDIFF(HOUR, Start, End)
SELECT DATEFROMPARTS(2025, 11, 15)
SELECT DATETRUNC(HOUR, CreatedAt)                        -- SQL 2022+
SELECT DATE_BUCKET(HOUR, 2, CreatedAt)                   -- SQL 2022+

-- NULL handling
SELECT ISNULL(NULL, 'default')                           -- Legacy
SELECT COALESCE(NULL, NULL, 'default')                    -- ✅ Preferido (ANSI, múltiples args)
SELECT NULLIF(0, 0)                                       -- NULL si iguales

-- IS [NOT] DISTINCT FROM (SQL 2022+) — compara tratando NULL = NULL
SELECT * FROM Orders WHERE Status IS NOT DISTINCT FROM @Status;
-- Antes: WHERE Status = @Status OR (Status IS NULL AND @Status IS NULL)

-- Conversión
SELECT CAST('123' AS INT), CONVERT(DATE, '2025-11-15')
SELECT TRY_CAST('abc' AS INT)            -- NULL en vez de error
SELECT TRY_CONVERT(DATE, 'invalid')      -- NULL en vez de error
```

---

## Convenciones de código T-SQL

### Naming

| Objeto | Convención | Ejemplo |
|--------|------------|---------|
| Tablas | `PascalCase`, plural | `Orders`, `OrderItems` |
| Schemas | `PascalCase` | `Sales`, `Catalog`, `Audit` |
| Columnas | `PascalCase` | `CustomerId`, `CreatedAt` |
| PK | `PK_{Table}` | `PK_Orders` |
| FK | `FK_{Table}_{RefTable}` | `FK_OrderItems_Orders` |
| Índices | `IX_{Table}_{Cols}` | `IX_Orders_CustomerId_Status` |
| CHECK | `CK_{Table}_{Rule}` | `CK_Orders_Status` |
| DEFAULT | `DF_{Table}_{Col}` | `DF_Orders_CreatedAt` |
| Stored Procedures | `usp_{Schema}_{Action}{Entity}` | `usp_Sales_CreateOrder` |
| Funciones | `ufn_{Schema}_{Action}{Entity}` | `ufn_Sales_GetOrderTotal` |
| Variables | `@camelCase` | `@customerId`, `@total` |
| Parámetros SP | `@camelCase` | `@orderId`, `@status` |

### Formato

```sql
-- ✅ Keywords en MAYÚSCULAS, columnas en PascalCase
CREATE PROCEDURE Sales.usp_CreateOrder
    @customerId     NVARCHAR(50),
    @totalAmount    DECIMAL(18,4),
    @orderNumber    INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Sales.Orders (OrderNumber, CustomerId, TotalAmount)
    VALUES (NEXT VALUE FOR Sales.OrderNumbers, @customerId, @totalAmount);

    SET @orderNumber = SCOPE_IDENTITY();
END;
```

### Reglas de oro

1. **`SET NOCOUNT ON`** en todo SP. Evita mensajes DONE_IN_PROC al cliente.
2. **Siempre usar `THROW`** (no `RAISERROR`), preserva el stack trace.
3. **`SYSUTCDATETIME()`** para timestamps UTC. `GETDATE()` es dependiente de la zona horaria del servidor.
4. **`NVARCHAR` para texto de usuario.** `VARCHAR` solo para códigos internos o ASCII garantizado.
5. **Nombra todos los constraints.** Evita nombres autogenerados ilegibles.
6. **Usar `COALESCE` sobre `ISNULL`.** Es ANSI y acepta múltiples argumentos.
7. **Usar `;` al final de statements.** Mejora legibilidad y evita bugs con CTEs.
8. **Usar `BEGIN TRY/BEGIN CATCH` y `THROW`.** No `@@ERROR` despues de cada statement.
9. **`WHERE 1=0` para copiar esquema sin datos:** `SELECT * INTO #tmp FROM Orders WHERE 1=0`.
10. **Usar `OUTPUT INSERTED`** en vez de `SCOPE_IDENTITY()` cuando necesites múltiples columnas.

---

## Variables y control de flujo

```sql
-- Variables
DECLARE @orderId UNIQUEIDENTIFIER = NEWID();
DECLARE @status NVARCHAR(20);

-- IF / ELSE
IF EXISTS (SELECT 1 FROM Sales.Orders WHERE Id = @orderId)
BEGIN
    UPDATE Sales.Orders SET Status = 'Cancelled' WHERE Id = @orderId;
END
ELSE
BEGIN
    THROW 50002, 'Order not found', 1;
END;

-- WHILE (evitar — usar operaciones basadas en conjuntos)
DECLARE @i INT = 1;
WHILE @i <= 10
BEGIN
    PRINT @i;
    SET @i += 1;
END;

-- CASE (expresión)
SELECT
    OrderNumber,
    CASE Status
        WHEN 'Pending'   THEN 'Pendiente'
        WHEN 'Shipped'   THEN 'Enviada'
        WHEN 'Delivered' THEN 'Entregada'
        ELSE 'Desconocida'
    END AS StatusDesc
FROM Sales.Orders;
```

---

## Tablas temporales vs variables de tabla

```sql
-- #temp — tabla temporal local. Visible solo en esta sesión.
CREATE TABLE #CartItems (
    Sku      NVARCHAR(50) NOT NULL,
    Quantity INT          NOT NULL
);

-- ##global — visible en todas las sesiones. Evitar.
CREATE TABLE ##GlobalConfig (Key NVARCHAR(100), Value NVARCHAR(MAX));

-- @tableVariable — mejor para datasets pequeños (<100 filas)
DECLARE @OrderIds TABLE (Id UNIQUEIDENTIFIER PRIMARY KEY);

-- ⚠️ @tableVariable no tiene estadísticas. #temp sí (mejor para datasets grandes).
-- Para > 100 filas → usar #temp.
```

---

## Sub-skills del kit

> 📁 Cada sub-skill tiene su guía detallada en `./{nombre}/GUIDE.md`. Usa `read` para cargarla cuando el tema lo requiera.


| Skill | Cuándo cargarla |
|-------|-----------------|
| `sql-server-performance` | Query tuning, execution plans, índices, Query Store, wait stats, parameter sniffing |
| `sql-server-architecture` | Filegroups, backup/restore, HA/DR (Always On), partitioning, data compression |
| `sql-server-security` | Logins, roles, permisos, TDE, Always Encrypted, RLS, data masking |
| `sql-server-procedural` | Stored procedures, funciones, triggers, vistas, error handling avanzado |
| `sql-server-advanced` | CTEs recursivos, window functions, JSON/XML, temporal tables, vector search, full-text |
| `sql-server-deployment` | Migraciones (EF Core/Flyway/DbUp), CI/CD, SSDT/DACPAC, Docker |
| `sql-server-integration` | Integración con .NET/EF Core, Dapper, ADO.NET, connection resiliency |

---

## Stack recomendado por defecto

| Propósito | Herramienta | Notas |
|-----------|-------------|-------|
| IDE | Azure Data Studio o SSMS | ADS para multi-plataforma, SSMS para Windows |
| ORM (desde .NET) | EF Core + `Microsoft.EntityFrameworkCore.SqlServer` | Provider oficial |
| Micro-ORM | Dapper + `Microsoft.Data.SqlClient` | Alto rendimiento, queries manuales |
| Migraciones | EF Core Migrations o Flyway | Flyway para control absoluto del SQL |
| Monitoring | Query Store + sp_WhoIsActive | Query Store built-in desde SQL 2016 |
| CI/CD | SSDT / SqlPackage / GitHub Actions | Dacpac para deploy declarativo |
| Container | `mcr.microsoft.com/mssql/server:2022-latest` | Docker para desarrollo y CI |
