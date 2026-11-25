---
name: postgresql-advanced
description: "T-SQL avanzado en PostgreSQL. Cubre CTEs recursivos (WITH RECURSIVE), window functions (ROW_NUMBER, RANK, LAG, LEAD), JSON/JSONB (operadores, indexación GIN, jsonb_path_query), full-text search (tsvector, tsquery), arrays, range types, dominio y tipos custom, y extensiones pgvector para AI/RAG. Actívala al implementar queries complejas, reportes analíticos, búsquedas avanzadas, o pipelines de embeddings."
disable-model-invocation: true
---

# PostgreSQL Advanced Features

Guía de features avanzadas de PostgreSQL para análisis, búsquedas y datos complejos.

---

## Window Functions

### Ranking

```sql
-- ROW_NUMBER
SELECT
    customer_id,
    total_amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY total_amount DESC) AS rank
FROM sales.orders;

-- RANK (con gaps)
SELECT
    customer_id,
    SUM(total_amount) AS lifetime_value,
    RANK() OVER (ORDER BY SUM(total_amount) DESC) AS customer_rank
FROM sales.orders
GROUP BY customer_id;

-- DENSE_RANK (sin gaps)
-- NTILE(N): dividir en N grupos (cuartiles, deciles)
SELECT
    customer_id,
    lifetime_value,
    NTILE(4) OVER (ORDER BY lifetime_value DESC) AS quartile
FROM customer_lifetime_values;
```

### Offset

```sql
-- LAG: valor anterior en la serie
SELECT
    DATE_TRUNC('day', created_at) AS day,
    SUM(total_amount) AS daily_total,
    LAG(SUM(total_amount), 1, 0) OVER (ORDER BY DATE_TRUNC('day', created_at)) AS previous_day,
    SUM(total_amount) - LAG(SUM(total_amount), 1, 0) OVER (ORDER BY DATE_TRUNC('day', created_at)) AS change
FROM sales.orders
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY day;

-- LEAD: valor siguiente
-- FIRST_VALUE / LAST_VALUE
SELECT DISTINCT
    customer_id,
    FIRST_VALUE(total_amount) OVER (PARTITION BY customer_id ORDER BY created_at) AS first_order_amount,
    LAST_VALUE(total_amount) OVER (PARTITION BY customer_id ORDER BY created_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_order_amount
FROM sales.orders;
```

### Window aggregates

```sql
-- Running total
SELECT
    order_number,
    total_amount,
    SUM(total_amount) OVER (ORDER BY created_at) AS running_total
FROM sales.orders;

-- Moving average (7 días)
SELECT
    DATE_TRUNC('day', created_at) AS day,
    SUM(total_amount) AS daily_total,
    AVG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC('day', created_at)
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM sales.orders
GROUP BY DATE_TRUNC('day', created_at);
```

---

## CTEs recursivos (WITH RECURSIVE)

```sql
-- Jerarquía de empleados
WITH RECURSIVE org_chart AS (
    SELECT employee_id, name, manager_id, 1 AS level,
           name::TEXT AS path
    FROM hr.employees
    WHERE manager_id IS NULL

    UNION ALL

    SELECT e.employee_id, e.name, e.manager_id, oc.level + 1,
           oc.path || ' → ' || e.name
    FROM hr.employees e
    JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT REPEAT('  ', level - 1) || name AS hierarchy, level, path
FROM org_chart
ORDER BY path;

-- Generar series de fechas
WITH RECURSIVE dates AS (
    SELECT DATE '2025-01-01' AS date
    UNION ALL
    SELECT date + INTERVAL '1 day'
    FROM dates
    WHERE date < '2025-12-31'
)
SELECT date FROM dates;

-- Navegación de árbol de categorías
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 AS depth, ARRAY[name] AS path
    FROM catalog.categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT c.id, c.name, c.parent_id, ct.depth + 1,
           ct.path || c.name
    FROM catalog.categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY path;
```

---

## JSON / JSONB

### JSONB: el tipo que debes usar

```sql
-- JSONB: binario, indexable, permite operadores. ✅ Siempre preferir sobre JSON.
CREATE TABLE catalog.products (
    sku       TEXT PRIMARY KEY,
    name      TEXT NOT NULL,
    metadata  JSONB NOT NULL DEFAULT '{}',
    tags      JSONB DEFAULT '[]'
);
```

### Operadores JSONB

```sql
-- ->  : obtener como JSONB (preserva tipo)
SELECT metadata->'dimensions'->'width' FROM catalog.products;

-- ->> : obtener como TEXT
SELECT metadata->>'manufacturer' FROM catalog.products;

-- @>  : contiene (incluye subdocumento completo)
SELECT * FROM catalog.products WHERE metadata @> '{"color": "red"}';

-- <@  : está contenido
SELECT * FROM catalog.products WHERE '{"color": "red"}'::jsonb <@ metadata;

-- ?   : existe key (top-level)
SELECT * FROM catalog.products WHERE metadata ? 'warranty';

-- ?|  : existe alguna key de la lista
SELECT * FROM catalog.products WHERE metadata ?| ARRAY['color','size'];

-- ?&  : existen todas las keys de la lista
SELECT * FROM catalog.products WHERE metadata ?& ARRAY['color','size'];

-- #>  : path como array (más seguro que encadenar ->)
SELECT metadata #> '{dimensions,width}' FROM catalog.products;

-- ||  : merge de JSONB
UPDATE catalog.products
SET metadata = metadata || '{"featured": true}'::jsonb
WHERE sku = 'SKU-1';

-- -   : eliminar key
UPDATE catalog.products
SET metadata = metadata - 'temp_field';

-- #-  : eliminar por path
UPDATE catalog.products
SET metadata = metadata #- '{deprecated,nested}';
```

### Índices GIN para JSONB

```sql
-- Índice para operador @> (contiene)
CREATE INDEX idx_products_metadata ON catalog.products USING GIN (metadata jsonb_path_ops);

-- Consultas que usan el índice
SELECT * FROM catalog.products WHERE metadata @> '{"brand": "Acme"}';

-- Índice GIN para keys (operador ?)
CREATE INDEX idx_products_metadata_keys ON catalog.products USING GIN (metadata);
-- También soporta ?| y ?&
```

### jsonb_path_query (SQL/JSON)

```sql
-- Navegar JSON con JSON Path (similar a XPath para XML)
SELECT sku,
       jsonb_path_query(metadata, '$.dimensions.width') AS width,
       jsonb_path_query(metadata, '$.specs[*].name') AS spec_name
FROM catalog.products;
```

---

## Full-Text Search

```sql
-- Crear columna tsvector (almacena tokens pre-procesados)
ALTER TABLE catalog.products ADD COLUMN search_vector TSVECTOR
    GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(description, '')), 'B')
    ) STORED;

-- Índice GIN para búsqueda full-text
CREATE INDEX idx_products_search ON catalog.products USING GIN (search_vector);

-- Búsqueda básica
SELECT name, description,
       ts_rank(search_vector, query) AS relevance
FROM catalog.products,
     plainto_tsquery('english', 'comfortable running shoes') AS query
WHERE search_vector @@ query
ORDER BY relevance DESC
LIMIT 10;

-- Búsqueda con operadores booleanos
SELECT name FROM catalog.products
WHERE search_vector @@ to_tsquery('english', 'comfortable & (running | walking)');

-- Resaltar matches
SELECT name,
       ts_headline('english', description,
           to_tsquery('english', 'running'), 'StartSel=<mark>, StopSel=</mark>')
FROM catalog.products
WHERE search_vector @@ to_tsquery('english', 'running');

-- Búsqueda difusa (con pg_trgm)
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_products_name_trgm ON catalog.products USING GIN (name gin_trgm_ops);

SELECT name, similarity(name, 'widjet') AS sim
FROM catalog.products
WHERE name % 'widjet'   -- similarity mayor que umbral
ORDER BY sim DESC;
```

---

## Arrays

```sql
-- Insertar/actualizar arrays
UPDATE catalog.products SET tags = ARRAY['electronics','sale','new'];

-- Agregar elemento
UPDATE catalog.products SET tags = array_append(tags, 'clearance');

-- Quitar elemento
UPDATE catalog.products SET tags = array_remove(tags, 'sale');

-- @> : contiene todos los elementos
SELECT * FROM catalog.products WHERE tags @> ARRAY['electronics','new'];

-- && : overlap (comparte al menos un elemento)
SELECT * FROM catalog.products WHERE tags && ARRAY['sale','clearance'];

-- ANY: valor está en el array
SELECT * FROM catalog.products WHERE 'electronics' = ANY(tags);

-- unnest: expandir array a filas
SELECT sku, UNNEST(tags) AS tag FROM catalog.products;

-- array_agg: agrupar filas en array
SELECT order_id, ARRAY_AGG(sku ORDER BY sku) AS products
FROM sales.order_items
GROUP BY order_id;
```

---

## Range Types

```sql
-- Tipos nativos: int4range, int8range, numrange, tsrange, tstzrange, daterange
CREATE TABLE hotel.bookings (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    room_id INT NOT NULL,
    dates DATERANGE NOT NULL,
    EXCLUDE USING GIST (room_id WITH =, dates WITH &&)  -- Previene solapamiento
);

INSERT INTO hotel.bookings (room_id, dates)
VALUES (101, daterange('2025-12-01', '2025-12-05', '[)'));

-- Query: verificar si una fecha está en el rango
SELECT * FROM hotel.bookings WHERE dates @> DATE '2025-12-03';

-- Query: rangos que se solapan con un rango dado
SELECT * FROM hotel.bookings
WHERE dates && daterange('2025-12-02', '2025-12-04');
```

---

## pgvector (AI/RAG)

```sql
-- Habilitar extensión
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla con embeddings
CREATE TABLE catalog.product_embeddings (
    product_sku TEXT PRIMARY KEY REFERENCES catalog.products(sku),
    embedding VECTOR(1536)  -- 1536-dim = OpenAI text-embedding-ada-002
);

-- Índice para búsqueda por similitud
CREATE INDEX ON catalog.product_embeddings
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
-- O usar HNSW (más rápido, PG 16+)
CREATE INDEX ON catalog.product_embeddings
    USING hnsw (embedding vector_cosine_ops);

-- Búsqueda por similitud
SELECT p.sku, p.name, p.description,
       1 - (pe.embedding <=> query_embedding::VECTOR) AS similarity
FROM catalog.product_embeddings pe
JOIN catalog.products p ON pe.product_sku = p.sku
ORDER BY pe.embedding <=> query_embedding::VECTOR  -- Cosine distance (<=>)
LIMIT 10;

-- Operadores de distancia:
-- <->  Euclidean distance (L2)
-- <#>  Negative inner product
-- <=>  Cosine distance
```

---

## Virtual Generated Columns (PostgreSQL 18)

```sql
-- Columna virtual calculada al vuelo (PG 18)
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    subtotal NUMERIC(18,4) NOT NULL,
    tax_rate NUMERIC(5,4) NOT NULL DEFAULT 0.16,
    total NUMERIC(18,4) GENERATED ALWAYS AS (subtotal * (1 + tax_rate)) VIRTUAL
);
-- No ocupa espacio en disco, se calcula al leer.
```

---

## Checklist avanzado

- [ ] JSONB para datos semi-estructurados (nunca JSON)
- [ ] Índices GIN en columnas JSONB consultadas con `@>`
- [ ] Full-text search con `tsvector` + índice GIN
- [ ] pg_trgm para búsquedas difusas (`%`)
- [ ] Window functions para análisis de series (LAG, SUM OVER)
- [ ] CTEs recursivos para jerarquías
- [ ] Arrays para tags/listas con operadores nativos
- [ ] Range types para reservas/solapamientos (con EXCLUDE constraint)
- [ ] pgvector para búsqueda semántica/RAG
- [ ] Virtual generated columns (PG 18) para valores calculados
