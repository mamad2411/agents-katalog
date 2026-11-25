---
name: sql-server-advanced
description: "T-SQL avanzado en SQL Server. Cubre CTEs recursivos, window functions (ROW_NUMBER, RANK, LAG, LEAD, aggregate windows), JSON (OPENJSON, JSON_VALUE, FOR JSON), temporal tables (system-versioned), graph tables, vector search (SQL 2025), full-text search (CONTAINS, FREETEXT), y PIVOT/UNPIVOT. Actívala al implementar queries complejas, reportes analíticos, series de tiempo, o búsquedas avanzadas."
disable-model-invocation: true
---

# SQL Server Advanced T-SQL

Guía de features T-SQL avanzadas para análisis, búsquedas y queries complejas.

---

## Window Functions

### Ranking

```sql
-- ROW_NUMBER: número secuencial por partición
SELECT
    CustomerId,
    TotalAmount,
    ROW_NUMBER() OVER (PARTITION BY CustomerId ORDER BY TotalAmount DESC) AS RowNum
FROM Sales.Orders;

-- RANK: ranking con gaps (1, 1, 3, 4...)
SELECT
    Sku,
    SUM(Quantity) AS TotalSold,
    RANK() OVER (ORDER BY SUM(Quantity) DESC) AS SalesRank
FROM Sales.OrderItems
GROUP BY Sku;

-- DENSE_RANK: ranking sin gaps (1, 1, 2, 3...)
SELECT
    Sku,
    SUM(Quantity) AS TotalSold,
    DENSE_RANK() OVER (ORDER BY SUM(Quantity) DESC) AS SalesRank
FROM Sales.OrderItems
GROUP BY Sku;

-- NTILE: dividir en N grupos (percentiles, cuartiles)
SELECT
    CustomerId,
    TotalAmount,
    NTILE(4) OVER (ORDER BY TotalAmount DESC) AS Quartile
FROM Sales.Orders;
```

### Offset (series de tiempo)

```sql
-- LAG: valor de la fila anterior
SELECT
    CreatedAt,
    TotalAmount,
    LAG(TotalAmount, 1, 0) OVER (ORDER BY CreatedAt) AS PreviousAmount,
    TotalAmount - LAG(TotalAmount, 1, 0) OVER (ORDER BY CreatedAt) AS Change
FROM Sales.Orders
WHERE CustomerId = 'CUST-001'
ORDER BY CreatedAt;

-- LEAD: valor de la fila siguiente
SELECT
    CreatedAt,
    TotalAmount,
    LEAD(TotalAmount, 1, 0) OVER (ORDER BY CreatedAt) AS NextAmount
FROM Sales.Orders
WHERE CustomerId = 'CUST-001';

-- FIRST_VALUE / LAST_VALUE
SELECT DISTINCT
    CustomerId,
    FIRST_VALUE(TotalAmount) OVER (PARTITION BY CustomerId ORDER BY CreatedAt) AS FirstOrderAmount,
    LAST_VALUE(TotalAmount) OVER (PARTITION BY CustomerId ORDER BY CreatedAt
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS LastOrderAmount
FROM Sales.Orders;
```

### Agregación con window

```sql
-- Running total
SELECT
    OrderNumber,
    TotalAmount,
    SUM(TotalAmount) OVER (ORDER BY CreatedAt
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS RunningTotal
FROM Sales.Orders;

-- Moving average (últimas 3 órdenes)
SELECT
    OrderNumber,
    TotalAmount,
    AVG(TotalAmount) OVER (ORDER BY CreatedAt
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MovingAvg3
FROM Sales.Orders;
```

---

## CTEs recursivos

```sql
-- Jerarquía organizacional
WITH OrgChart AS (
    -- Anchor: el CEO
    SELECT EmployeeId, Name, ManagerId, 0 AS Level,
           CAST(Name AS NVARCHAR(MAX)) AS Path
    FROM HR.Employees
    WHERE ManagerId IS NULL

    UNION ALL

    -- Recursive: empleados que reportan al nivel anterior
    SELECT e.EmployeeId, e.Name, e.ManagerId, oc.Level + 1,
           CAST(oc.Path + ' → ' + e.Name AS NVARCHAR(MAX))
    FROM HR.Employees e
    JOIN OrgChart oc ON e.ManagerId = oc.EmployeeId
)
SELECT
    REPLICATE('  ', Level) + Name AS Hierarchy,
    Level,
    Path
FROM OrgChart
ORDER BY Path;

-- Calendar table con CTE recursivo
WITH Calendar AS (
    SELECT CAST('2025-01-01' AS DATE) AS Date
    UNION ALL
    SELECT DATEADD(DAY, 1, Date)
    FROM Calendar
    WHERE Date < '2025-12-31'
)
SELECT Date
FROM Calendar
OPTION (MAXRECURSION 366); -- Limitar recursión
```

---

## JSON en SQL Server

### Parse JSON → filas

```sql
-- OPENJSON: convertir JSON a tabla
DECLARE @json NVARCHAR(MAX) = N'[
    {"sku":"SKU1","name":"Widget","price":29.99},
    {"sku":"SKU2","name":"Gadget","price":49.99}
]';

SELECT Sku, Name, Price
FROM OPENJSON(@json)
WITH (
    Sku   NVARCHAR(50) '$.sku',
    Name  NVARCHAR(100) '$.name',
    Price DECIMAL(10,2) '$.price'
);

-- JSON anidado
DECLARE @orderJson NVARCHAR(MAX) = N'{
    "orderId": "abc-123",
    "customer": {"id": "CUST-1", "name": "Acme Inc"},
    "items": [
        {"sku": "SKU1", "qty": 2, "price": 100.00},
        {"sku": "SKU2", "qty": 1, "price": 50.00}
    ]
}';

SELECT
    JSON_VALUE(@orderJson, '$.orderId') AS OrderId,
    JSON_VALUE(@orderJson, '$.customer.name') AS CustomerName
FROM (SELECT 1) AS Dummy;

SELECT Sku, Qty, Price
FROM OPENJSON(@orderJson, '$.items')
WITH (
    Sku   NVARCHAR(50) '$.sku',
    Qty   INT '$.qty',
    Price DECIMAL(10,2) '$.price'
);
```

### Generar JSON desde filas

```sql
-- FOR JSON AUTO: estructura según joins
SELECT o.OrderNumber, o.CustomerId, oi.Sku, oi.Quantity
FROM Sales.Orders o
JOIN Sales.OrderItems oi ON o.Id = oi.OrderId
WHERE o.Id = @orderId
FOR JSON AUTO, WITHOUT_ARRAY_WRAPPER;
-- {"OrderNumber":1001,"CustomerId":"CUST-1","oi":[{"Sku":"SKU1","Quantity":2}]}

-- FOR JSON PATH: control total sobre estructura
SELECT
    o.OrderNumber,
    o.CustomerId,
    Items = (
        SELECT oi.Sku, oi.Quantity, oi.UnitPrice
        FROM Sales.OrderItems oi
        WHERE oi.OrderId = o.Id
        FOR JSON PATH
    )
FROM Sales.Orders o
WHERE o.Id = @orderId
FOR JSON PATH, WITHOUT_ARRAY_WRAPPER;

-- JSON_MODIFY: actualizar valor dentro de JSON
UPDATE Sales.Orders
SET Metadata = JSON_MODIFY(Metadata, '$.tags', JSON_QUERY('["vip","rush"]'))
WHERE Id = @orderId;
```

---

## Temporal Tables (System-Versioned)

```sql
-- Tabla con historial automático
CREATE TABLE Sales.Orders (
    Id               UNIQUEIDENTIFIER NOT NULL,
    OrderNumber      INT NOT NULL,
    CustomerId       NVARCHAR(50) NOT NULL,
    Status           NVARCHAR(20) NOT NULL,
    TotalAmount      DECIMAL(18,4) NOT NULL,

    -- Columnas de sistema
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN NOT NULL,
    ValidTo   DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN NOT NULL,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo),

    CONSTRAINT PK_Orders PRIMARY KEY (Id)
)
WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = Sales.OrdersHistory));

-- Query point-in-time
SELECT * FROM Sales.Orders
FOR SYSTEM_TIME AS OF '2025-11-15 10:00:00';

-- Query en rango de tiempo
SELECT Id, Status
FROM Sales.Orders
FOR SYSTEM_TIME FROM '2025-11-01' TO '2025-11-15';

-- Ver cambios entre dos momentos
SELECT Id, Status, ValidFrom
FROM Sales.Orders
FOR SYSTEM_TIME BETWEEN '2025-11-01' AND '2025-11-15';
```

---

## Graph Tables (SQL 2017+)

```sql
-- Node table (nodos)
CREATE TABLE Users (
    UserId INT PRIMARY KEY,
    Name NVARCHAR(100)
) AS NODE;

-- Edge table (aristas)
CREATE TABLE Follows (
    Since DATE
) AS EDGE;

-- Insertar nodos
INSERT INTO Users (UserId, Name) VALUES (1, 'Alice'), (2, 'Bob');

-- Insertar arista (usando $node_id de cada nodo)
INSERT INTO Follows ($from_id, $to_id, Since)
SELECT u1.$node_id, u2.$node_id, '2025-01-01'
FROM Users u1, Users u2
WHERE u1.UserId = 1 AND u2.UserId = 2;

-- Query con MATCH
SELECT u1.Name AS Follower, u2.Name AS Followee
FROM Users u1, Follows f, Users u2
WHERE MATCH(u1-(f)->u2);
```

---

## Full-Text Search

```sql
-- Crear catálogo full-text
CREATE FULLTEXT CATALOG ft_Orders AS DEFAULT;

-- Crear índice full-text
CREATE FULLTEXT INDEX ON Sales.Orders(Notes)
    KEY INDEX PK_Orders
    ON ft_Orders
    WITH CHANGE_TRACKING AUTO;

-- Búsqueda
SELECT * FROM Sales.Orders
WHERE CONTAINS(Notes, 'urgent AND (delivery OR shipping)');

-- FREETEXT: búsqueda por significado (menos precisa, más resultados)
SELECT * FROM Sales.Catalog.Products
WHERE FREETEXT(Description, 'comfortable running shoes');

-- CONTAINSTABLE: con ranking de relevancia
SELECT o.OrderNumber, ct.RANK
FROM Sales.Orders o
INNER JOIN CONTAINSTABLE(Sales.Orders, Notes, 'urgent', 10) ct
    ON o.Id = ct.[KEY]
ORDER BY ct.RANK DESC;
```

---

## Vector Search (SQL Server 2025)

```sql
-- Requiere SQL Server 2025 (GA desde Nov 2025)
-- Almacenar vector
ALTER TABLE Catalog.Products
ADD DescriptionEmbedding VECTOR(1536);

-- Actualizar con embedding (desde app o vía external REST call)
UPDATE Catalog.Products
SET DescriptionEmbedding = @embedding -- vector float[1536]
WHERE Sku = @sku;

-- Búsqueda por similitud (cosine distance)
SELECT TOP 10
    Sku, Name, Price,
    VECTOR_DISTANCE('cosine', DescriptionEmbedding, @queryEmbedding) AS Distance
FROM Catalog.Products
ORDER BY Distance ASC;

-- VECTOR_DISTANCE tipos: 'cosine', 'euclidean', 'dot'
```

---

## Regex (SQL Server 2025)

```sql
-- T-SQL regex nativo (SQL Server 2025)
SELECT *
FROM Sales.Orders
WHERE CustomerId REGEXP_LIKE '^CUST-\d{3}$';

-- Extraer match
SELECT REGEXP_SUBSTR(Notes, '\b[A-Z]{3}-\d{4}\b') AS SKU_Mentioned
FROM Sales.Orders;

-- Reemplazar con regex
SELECT REGEXP_REPLACE(Phone, '[^\d]', '') AS CleanPhone
FROM Customers;
```

---

## PIVOT / UNPIVOT

```sql
-- PIVOT: filas → columnas (reportes)
SELECT *
FROM (
    SELECT CustomerId, YEAR(CreatedAt) AS OrderYear, TotalAmount
    FROM Sales.Orders
) src
PIVOT (
    SUM(TotalAmount)
    FOR OrderYear IN ([2023], [2024], [2025])
) pvt;

-- UNPIVOT: columnas → filas (normalizar)
SELECT CustomerId, Quarter, Amount
FROM (
    SELECT CustomerId, Q1, Q2, Q3, Q4
    FROM Sales.QuarterlySummary
) src
UNPIVOT (
    Amount FOR Quarter IN (Q1, Q2, Q3, Q4)
) unpvt;
```

---

## GENERATE_SERIES (SQL 2022+)

```sql
-- Generar números
SELECT value FROM GENERATE_SERIES(1, 100);

-- Generar fechas
SELECT DATEADD(DAY, value, '2025-01-01') AS Date
FROM GENERATE_SERIES(0, 364);
```

---

## Checklist avanzado

- [ ] Window functions dominadas (ROW_NUMBER, RANK, LAG, LEAD, aggregates)
- [ ] CTEs recursivos para jerarquías y series
- [ ] JSON: OPENJSON para API payloads, FOR JSON PATH para respuestas
- [ ] Temporal tables para auditoría punto en el tiempo
- [ ] Full-text search configurado para búsqueda de texto natural
- [ ] Graph tables evaluadas para datos altamente conectados
- [ ] Vector search preparado para AI/RAG pipelines (SQL 2025)
- [ ] PIVOT solo para reportes finales, no en queries intermedias
