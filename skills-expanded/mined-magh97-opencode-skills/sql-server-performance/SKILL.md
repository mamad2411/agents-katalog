---
name: sql-server-performance
description: "Rendimiento y tuning de queries en SQL Server. Cubre execution plans, índices (clustered, nonclustered, columnstore, filtered), Query Store, estadísticas, wait stats, parameter sniffing y PSP optimization (SQL 2025), In-Memory OLTP, y estrategias de optimización de queries. Actívala al diagnosticar queries lentas, diseñar índices, o resolver problemas de rendimiento."
disable-model-invocation: true
---

# SQL Server Performance & Query Tuning

Guía de rendimiento y optimización de queries SQL Server. El objetivo: encontrar la peor query o índice faltante antes de agregar hardware.

---

## Execution Plans (Planes de Ejecución)

### Obtener el plan

```sql
-- Plan estimado (sin ejecutar)
-- SSMS: CTRL+L o botón "Display Estimated Execution Plan"

-- Plan real (ejecutando)
SET STATISTICS XML ON;
SELECT * FROM Sales.Orders WHERE CustomerId = @customerId;
SET STATISTICS XML OFF;

-- Plan desde Query Store
SELECT * FROM sys.query_store_plan WHERE query_id = 42;

-- Plan desde DMVs
SELECT * FROM sys.dm_exec_query_stats
CROSS APPLY sys.dm_exec_query_plan(plan_handle)
WHERE creation_time > DATEADD(HOUR, -24, GETDATE());
```

### Lectura del plan (derecha → izquierda)

```
Clustered Index Scan (PK_Orders)  ←  Filter (Status = 'Pending')  ←  SELECT
        ↑ arranca aquí                     ↑ operador
```

- **Scan**: Lee todas las filas. Malo en tablas grandes.
- **Seek**: Lee filas específicas vía índice. ✅ Bueno.
- **Key Lookup**: Seek en nonclustered + lookup en clustered. Costoso en batch.
- **Nested Loops**: Join fila por fila. Bueno para pocas filas externas.
- **Hash Match**: Hash table en memoria. Bueno para grandes datasets sin índice.
- **Merge Join**: Inputs ordenados. Requiere índices en ambos lados.
- **Sort**: Ordenamiento explícito. Costoso. Agregar índice que ya esté ordenado.
- **Spool**: Tabla temporal interna. Señal de query mal escrita.

### Operadores a evitar

| Operador | Significado | Acción |
|----------|-------------|--------|
| **Table Scan** | Sin índice clustered | Crear PK clustered |
| **Clustered Index Scan** | Leyendo toda la tabla | Agregar índice filtered/covering |
| **Key Lookup** excesivo | Índice nonclustered incompleto | `INCLUDE` columnas o clustered index en la columna correcta |
| **Sort** | Ordenando sin índice | Crear índice con el orden requerido |
| **Spool** | Temp table implícita | Reescribir query |
| **Implicit Conversion** | `NVARCHAR` vs `VARCHAR` | Usar mismo tipo en columna y variable |
| **Compute Scalar costoso** | Cálculo por fila | Precalcular o columna persistida |

---

## Índices

### Clustered Index

La tabla misma. Uno por tabla. Define el orden físico.

```sql
-- ✅ Clustered en columna que es:
--   - Estrecha (INT, BIGINT, UNIQUEIDENTIFIER con NEWSEQUENTIALID)
--   - Única o casi única
--   - Incremental (reduce fragmentación)
--   - Usada en queries de rango

ALTER TABLE Sales.Orders
ADD CONSTRAINT PK_Orders PRIMARY KEY CLUSTERED (Id);
-- Id es UNIQUEIDENTIFIER con NEWSEQUENTIALID() → OK
```

❌ Mal clustered: `GUID` con `NEWID()` (fragmentación masiva), columna ancha (`NVARCHAR(2000)`), columna que cambia frecuentemente.

### Nonclustered Index

```sql
-- Índice para cubrir queries frecuentes
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId_Status
    ON Sales.Orders (CustomerId, Status)
    INCLUDE (TotalAmount, CreatedAt, Currency)
    WHERE (Status <> 'Deleted') -- Filtered index
    WITH (FILLFACTOR = 90);

-- Columnas clave (key): CustomerId, Status → WHERE/JOIN/GROUP BY primero
-- INCLUDE: TotalAmount, CreatedAt, Currency → SELECT (covering, evita Key Lookup)
-- Filtered: WHERE Status <> 'Deleted' → índice más pequeño y rápido
```

### Tipos de índices

| Tipo | Cuándo usarlo |
|------|--------------|
| **Clustered** | PK, tabla misma. Uno por tabla. |
| **Nonclustered** | Queries frecuentes con WHERE específico. Varios por tabla. |
| **Unique** | Constraints de unicidad. Puede ser clustered o nonclustered. |
| **Filtered** | Filtro WHERE reduce tamaño. Ej: `WHERE Status = 'Pending'`. |
| **Covering (INCLUDE)** | Incluye columnas del SELECT evitando Key Lookup. |
| **Columnstore** (CCI) | Data warehouse, agregaciones masivas. Compresión 10x. |
| **Full-Text** | Búsqueda de texto natural: `CONTAINS(Notes, 'keyword')`. |
| **XML** | Índices sobre columnas XML (primary + secondary). |
| **Spatial** | Índices sobre GEOMETRY/GEOGRAPHY. |

### Missing Index (DMVs)

```sql
-- Índices sugeridos por el motor
SELECT
    migs.avg_user_impact,
    migs.avg_total_user_cost,
    migs.user_seeks,
    mid.statement AS TableName,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_groups mig
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.index_group_handle
JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
WHERE database_id = DB_ID('MiApp')
ORDER BY avg_user_impact DESC;
```

### Mantenimiento de índices

```sql
-- Reorganizar (online, baja carga) — fragmentación 5-30%
ALTER INDEX IX_Orders_CustomerId_Status ON Sales.Orders REORGANIZE;

-- Rebuild (offline, alta carga) — fragmentación > 30%
ALTER INDEX IX_Orders_CustomerId_Status ON Sales.Orders REBUILD
    WITH (ONLINE = ON, FILLFACTOR = 90); -- ONLINE requiere Enterprise
```

---

## Estadísticas

```sql
-- Actualizar estadísticas (el motor lo hace automático, pero...)
UPDATE STATISTICS Sales.Orders;
UPDATE STATISTICS Sales.Orders IX_Orders_CustomerId_Status WITH FULLSCAN;

-- Ver cuándo se actualizaron por última vez
SELECT
    name,
    STATS_DATE(object_id, stats_id) AS LastUpdated,
    rows_sampled,
    rows
FROM sys.stats
CROSS APPLY sys.dm_db_stats_properties(object_id, stats_id)
WHERE object_id = OBJECT_ID('Sales.Orders');

-- ⚠️ AUTO_UPDATE_STATS usa sampleo. Para tablas grandes y distribución skew:
-- Usar UPDATE STATISTICS WITH FULLSCAN periódicamente (job semanal).
```

---

## Query Store

"Flight recorder" de SQL Server. Habilítalo siempre.

```sql
-- Habilitar
ALTER DATABASE MiApp SET QUERY_STORE = ON (
    OPERATION_MODE = READ_WRITE,
    QUERY_CAPTURE_MODE = AUTO,       -- SQL 2016+
    MAX_STORAGE_SIZE_MB = 1024,
    SIZE_BASED_CLEANUP_MODE = AUTO,
    DATA_FLUSH_INTERVAL_SECONDS = 900
);

-- Top queries por consumo
SELECT TOP 10
    q.query_id,
    qt.query_sql_text,
    SUM(rs.avg_duration * rs.count_executions) AS total_duration_ms,
    AVG(rs.avg_duration) AS avg_duration_ms,
    SUM(rs.count_executions) AS executions
FROM sys.query_store_query q
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
JOIN sys.query_store_query_text qt ON q.query_text_id = qt.query_text_id
WHERE rs.last_execution_time > DATEADD(HOUR, -24, GETDATE())
GROUP BY q.query_id, qt.query_sql_text
ORDER BY total_duration_ms DESC;

-- Regresión de plan (plan se volvió más lento)
SELECT * FROM sys.query_store_plan p
WHERE p.is_forced_plan = 0
  AND EXISTS (
    SELECT 1 FROM sys.query_store_runtime_stats rs
    WHERE rs.plan_id = p.plan_id
      AND rs.avg_duration > rs.max_duration * 0.5
);
```

---

## Parameter Sniffing y PSP

**Problema**: SQL Server genera un plan basado en el primer valor del parámetro. Si el primer valor es atípico, el plan es malo para el resto.

```sql
-- Solución 1: OPTION (RECOMPILE) — para queries con distribución muy variable
SELECT * FROM Sales.Orders
WHERE CustomerId = @customerId
OPTION (RECOMPILE);

-- Solución 2: OPTION (OPTIMIZE FOR UNKNOWN) — estadística promedio
SELECT * FROM Sales.Orders
WHERE Status = @status
OPTION (OPTIMIZE FOR UNKNOWN);

-- Solución 3: OPTION (OPTIMIZE FOR (@status = 'Pending')) — valor típico
SELECT * FROM Sales.Orders
WHERE Status = @status
OPTION (OPTIMIZE FOR (@status = 'Pending'));

-- Solución 4 (SQL 2025): Parameter Sensitive Plan optimization
ALTER DATABASE MiApp SET PARAMETER_SENSITIVE_PLAN_OPTIMIZATION = ON;
-- El motor genera múltiples planes para un mismo query según el valor del parámetro.
-- Automático y transparente. No requiere cambios en el código.
```

---

## Wait Stats

Dónde está perdiendo tiempo el motor. Ejecutar `sp_WhoIsActive` o consultar DMVs.

```sql
-- Top wait types
SELECT TOP 10
    wait_type,
    wait_time_ms / 1000 AS wait_time_s,
    waiting_tasks_count,
    CASE wait_type
        WHEN 'PAGEIOLATCH_SH' THEN 'Leyendo de disco → falta memoria o índices'
        WHEN 'WRITELOG'      THEN 'Log write bottleneck → discos lentos'
        WHEN 'LCK_M_X'       THEN 'Bloqueo exclusivo → transacciones largas'
        WHEN 'CXPACKET'      THEN 'Paralelismo desbalanceado → ajustar MAXDOP'
        WHEN 'SOS_SCHEDULER_YIELD' THEN 'CPU pressure → queries pesadas'
        WHEN 'ASYNC_NETWORK_IO' THEN 'Cliente no consume datos rápido → paginación app'
        ELSE 'Ver docs'
    END AS Description
FROM sys.dm_os_wait_stats
ORDER BY wait_time_ms DESC;
```

---

## In-Memory OLTP (Memory-Optimized Tables)

```sql
-- Habilitar en la DB
ALTER DATABASE MiApp ADD FILEGROUP MemOptimizedFG CONTAINS MEMORY_OPTIMIZED_DATA;
ALTER DATABASE MiApp ADD FILE (NAME='MemOptData', FILENAME='C:\Data\MiApp_MemOpt') TO FILEGROUP MemOptimizedFG;

-- Tabla memory-optimized durable
CREATE TABLE Sales.OrderCache (
    Id       INT NOT NULL PRIMARY KEY NONCLUSTERED,
    Data     NVARCHAR(MAX) NOT NULL,
    UpdatedAt DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME()
) WITH (MEMORY_OPTIMIZED = ON, DURABILITY = SCHEMA_AND_DATA);

-- Natively compiled stored procedure
CREATE PROCEDURE Sales.usp_GetCachedOrder
    @orderId INT NOT NULL
WITH NATIVE_COMPILATION, SCHEMABINDING, EXECUTE AS OWNER
AS BEGIN ATOMIC WITH (TRANSACTION ISOLATION LEVEL = SNAPSHOT, LANGUAGE = N'us_english')
    SELECT Id, Data, UpdatedAt
    FROM Sales.OrderCache
    WHERE Id = @orderId;
END;
```

⚠️ Usar In-Memory OLTP solo en puntos calientes extremos (> 10k ops/s).

---

## Buenas prácticas de queries

```sql
-- ✅ Sargable: WHERE que usa índice
SELECT * FROM Orders WHERE CustomerId = @customerId;

-- ❌ No sargable: función sobre columna
SELECT * FROM Orders WHERE YEAR(CreatedAt) = 2025;       -- Scan
SELECT * FROM Orders WHERE CreatedAt >= '2025-01-01'
                     AND CreatedAt <  '2026-01-01';      -- Seek ✅

-- ❌ LEFT(column) LIKE
SELECT * FROM Orders WHERE LEFT(CustomerId, 3) = 'CUS';  -- Scan
SELECT * FROM Orders WHERE CustomerId LIKE 'CUS%';        -- Seek ✅

-- ❌ Columna en expresión
SELECT * FROM Orders WHERE TotalAmount * 1.16 > 1000;    -- Scan
SELECT * FROM Orders WHERE TotalAmount > 1000 / 1.16;    -- Seek ✅

-- ✅ SELECT solo columnas necesarias
SELECT Id, Status, TotalAmount FROM Orders;                -- Seek
SELECT * FROM Orders;                                     -- Key Lookup si índice no covering

-- ✅ EXISTS en vez de COUNT(*)
IF EXISTS (SELECT 1 FROM Orders WHERE CustomerId = @id)   -- Corta en primer match
-- vs
IF (SELECT COUNT(*) FROM Orders WHERE CustomerId = @id) > 0 -- Cuenta todas las filas

-- ✅ UNION ALL sobre UNION (no deduplica)
SELECT CustomerId FROM Orders
UNION ALL
SELECT CustomerId FROM ArchivedOrders;                    -- No sort para deduplicar
```

---

## Configuración de SQL Server

```sql
-- MAXDOP: limitar paralelismo (default 0 = ilimitado)
EXEC sp_configure 'max degree of parallelism', 4;
RECONFIGURE;

-- Cost Threshold for Parallelism: subir de 5 (default) a 25-50
EXEC sp_configure 'cost threshold for parallelism', 50;
RECONFIGURE;

-- Optimize for Ad Hoc Workloads: reduce cache de planes únicos
EXEC sp_configure 'optimize for ad hoc workloads', 1;
RECONFIGURE;
```

---

## Checklist de rendimiento

- [ ] Query Store habilitado en producción
- [ ] Índices covering para las top 10 queries por consumo
- [ ] Estadísticas actualizadas (AUTO_UPDATE_STATS ON + FULLSCAN semanal)
- [ ] No hay Scans de tabla en queries de >1000 filas
- [ ] No hay Key Lookups excesivos en batch queries
- [ ] WHERE usa condiciones sargables (sin YEAR(), LEFT(), cálculos)
- [ ] SELECT no trae columnas innecesarias
- [ ] Parameter sniffing mitigado (RECOMPILE/PSP/Optimize For)
- [ ] MAXDOP entre 2-8 según CPUs, no 0
- [ ] Cost Threshold for Parallelism ≥ 25
- [ ] Plan cache no dominado por ad-hoc (optimize for ad hoc workloads = 1)
- [ ] No hay `SELECT *` en queries productivas
- [ ] Fill factor ajustado para tablas con updates (80-90)
