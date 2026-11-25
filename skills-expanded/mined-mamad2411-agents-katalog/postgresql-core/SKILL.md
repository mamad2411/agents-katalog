---
name: postgresql-core
description: "Guía principal de PostgreSQL (16/17/18): PL/pgSQL, tipos de datos, DDL/DML, esquemas, psql/pgAdmin/DBeaver y extensiones. Úsala para cualquier tarea PostgreSQL: desarrollos, queries, migraciones o diseño de base de datos."
---

# PostgreSQL Core Development Guide

Guía canónica para desarrollo en PostgreSQL. Cubre versiones 16, 17 y 18 (Sep 2025). Todo código PL/pgSQL generado sigue estas reglas salvo indicación contraria.

## Versiones y compatibilidad

| Versión | Lanzamiento | Fin de soporte | Novedades clave |
|---------|-------------|----------------|-----------------|
| PostgreSQL 16 | Sep 2023 | Nov 2028 | `SQL/JSON` constructors, `ANY_VALUE`, I/O combiner, `pg_stat_io` |
| PostgreSQL 17 | Sep 2024 | Nov 2029 | Incremental backup, `MERGE` con `RETURNING`, mejoras vacuum, `json_table` |
| PostgreSQL 18 | Sep 2025 | Nov 2030 | **Async I/O** (3x lectura), **skip scan**, `uuidv7()`, `NOT NULL` sin table scan, virtual generated columns |

- **Proyectos nuevos** → PostgreSQL 18. Async I/O y skip scan valen la pena para cargas OLTP.
- **Migraciones** → 16 → 17 → 18 usa `pg_upgrade --link` (minutos). Estadísticas preservadas desde PG 18.
- **Cloud** → Amazon RDS, Aurora, Cloud SQL, Azure PostgreSQL, Supabase.

---

## Arquitectura del motor

```
┌──────────────────────────────────────────────┐
│            Client (libpq / Npgsql)             │
├──────────────────────────────────────────────┤
│              Postmaster Process                │
│    └─ Fork per connection → Backend Process   │
├──────────────────────────────────────────────┤
│              Query Processing                  │
│  Parser → Analyzer → Rewriter → Planner → Executor
├──────────────────────────────────────────────┤
│                 Storage Engine                 │
│  Pages (8KB) → Tuples → Heap Files → Tablespaces
│  MVCC: Xmin/Xmax + visibility map             │
├──────────────────────────────────────────────┤
│        WAL (Write-Ahead Logging)              │
│  Redo log. pg_wal/. 16MB segments.            │
├──────────────────────────────────────────────┤
│            Background Processes                │
│  Autovacuum, WAL Writer, BGWriter, Checkpointer│
└──────────────────────────────────────────────┘
```

### MVCC (Multi-Version Concurrency Control)

PostgreSQL nunca sobrescribe filas. Cada UPDATE crea una nueva versión (tuple). Las antiguas son limpiadas por VACUUM.

- `xmin`: ID de transacción que creó el tuple.
- `xmax`: ID de transacción que eliminó/actualizó el tuple (0 = visible).
- Las queries ven solo los tuples activos/committed al inicio de su transacción.

---

## Tipos de datos

### Numéricos

| Tipo | Rango | Bytes | Cuándo usar |
|------|-------|-------|-------------|
| `SMALLINT` | -32K a 32K | 2 | Edad, año |
| `INTEGER` | -2B a 2B | 4 | IDs, cantidades generales ✅ |
| `BIGINT` | -9E a 9E | 8 | IDs grandes, contadores |
| `NUMERIC(p,s)` | Precisión exacta | Variable | ✅ **Dinero, valores financieros** |
| `DECIMAL(p,s)` | = `NUMERIC` | Variable | Sinónimo ANSI |
| `REAL` | 6 dígitos decimales | 4 | Cálculos científicos |
| `DOUBLE PRECISION` | 15 dígitos | 8 | Cálculos científicos |
| `MONEY` | Precisión fija con locale | 8 | ⚠️ Evitar — usa `NUMERIC(19,4)` |

### Texto

| Tipo | Uso |
|------|-----|
| `TEXT` | Longitud ilimitada. ✅ **Default para texto** |
| `VARCHAR(n)` | Con límite. Usar solo si el límite es requisito de negocio |
| `CHAR(n)` | Espacios al final (padded). ⚠️ Evitar, usar `TEXT` o `VARCHAR` |
| `"char"` | 1 byte. Tipo interno. |

✅ Regla: `TEXT` por defecto. `VARCHAR(n)` solo si el límite es una regla de negocio estricta.

### Fecha/hora

| Tipo | Bytes | Uso |
|------|-------|-----|
| `DATE` | 4 | Solo fecha |
| `TIME` | 8 | Solo hora |
| `TIMESTAMP` / `TIMESTAMP WITHOUT TIME ZONE` | 8 | ✅ Fecha+hora sin TZ |
| `TIMESTAMPTZ` / `TIMESTAMP WITH TIME ZONE` | 8 | ✅ **Recomendado.** Guarda en UTC, muestra en TZ de sesión |
| `INTERVAL` | 16 | Duración (1 day, 2 hours) |

```sql
-- ✅ Usar TIMESTAMPTZ por defecto
CREATE TABLE Orders (
    Id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    CreatedAt   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UpdatedAt   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- uuidv7 (PG 18) — time-ordered UUID, mejor para PKs clustered
CREATE TABLE Orders (
    Id          UUID DEFAULT uuidv7() PRIMARY KEY,
    ...
);
```

### Otros

| Tipo | Uso |
|------|-----|
| `BOOLEAN` | `true`, `false`, `NULL` |
| `UUID` | GUIDs. `gen_random_uuid()` o `uuidv7()` (PG 18) |
| `JSON` | Almacena texto JSON (sin indexación) |
| `JSONB` | ✅ JSON binario indexable |
| `ARRAY` | `INTEGER[]`, `TEXT[]`, `JSONB[]` |
| `HSTORE` | Key-value pairs (extensión) |
| `BYTEA` | Datos binarios |
| `CIDR` / `INET` / `MACADDR` | Redes e IPs |
| `RANGE` | Rangos: `int4range`, `tsrange`, `daterange` |
| `GEOMETRY` / `GEOGRAPHY` | PostGIS (extensión) |
| `VECTOR` | Extensión pgvector |
| `DOMAIN` | Tipo con constraints reutilizables |

---

## DDL

### Tablas

```sql
CREATE SCHEMA sales;

CREATE TABLE sales.orders (
    id              UUID DEFAULT uuidv7() PRIMARY KEY,
    order_number    INT GENERATED ALWAYS AS IDENTITY,
    customer_id     TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'Pending',
    total_amount    NUMERIC(18,4) NOT NULL DEFAULT 0
        CHECK (total_amount >= 0),
    currency        TEXT NOT NULL DEFAULT 'MXN'
        CHECK (currency IN ('MXN','USD','EUR')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    deleted_at      TIMESTAMPTZ
);

-- Índices
CREATE INDEX idx_orders_customer_id_status
    ON sales.orders (customer_id, status)
    INCLUDE (total_amount, created_at); -- PostgreSQL 11+ covering

CREATE INDEX idx_orders_created_at
    ON sales.orders (created_at DESC);

-- Partial index (filtered)
CREATE INDEX idx_orders_pending
    ON sales.orders (created_at)
    WHERE status = 'Pending';

-- Constraint unique
ALTER TABLE sales.orders
    ADD CONSTRAINT uq_orders_order_number UNIQUE (order_number);
```

### Schemas

```sql
CREATE SCHEMA sales;
CREATE SCHEMA catalog;
CREATE SCHEMA audit;

-- search_path: orden en que PostgreSQL busca objetos
SET search_path TO sales, catalog, public;
```

### Sequences y GENERATED AS IDENTITY

```sql
-- ✅ IDENTITY (PostgreSQL 10+) — recomendado sobre SERIAL
CREATE TABLE sales.orders (
    order_number INT GENERATED ALWAYS AS IDENTITY
        (START WITH 1000 INCREMENT BY 1 NO CYCLE),
    ...
);

-- Seriales legacy (solo para compatibilidad)
-- SMALLSERIAL, SERIAL, BIGSERIAL → internamente crean SEQUENCE
```

---

## DML

### INSERT

```sql
-- INSERT básico
INSERT INTO sales.orders (customer_id, total_amount)
VALUES ('CUST-001', 149.99);

-- INSERT múltiple
INSERT INTO sales.order_items (order_id, sku, quantity, unit_price)
VALUES
    (@orderId, 'SKU-1', 2, 100.00),
    (@orderId, 'SKU-2', 1,  50.00);

-- INSERT con RETURNING (capturar IDs generados)
INSERT INTO sales.orders (customer_id, total_amount)
VALUES ('CUST-001', 149.99)
RETURNING id, order_number;

-- ON CONFLICT (upsert) — preferido sobre MERGE
INSERT INTO catalog.products (sku, name, price)
VALUES ('SKU-1', 'Widget', 29.99)
ON CONFLICT (sku) DO UPDATE SET
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    updated_at = now();

-- INSERT ... SELECT
INSERT INTO sales.orders_archive
SELECT * FROM sales.orders WHERE created_at < now() - INTERVAL '2 years';
```

### UPDATE

```sql
-- UPDATE con RETURNING
UPDATE sales.orders
SET status = 'Cancelled',
    cancelled_at = now()
WHERE id = @orderId
  AND status = 'Pending'
RETURNING id, order_number, status, updated_at;

-- UPDATE con CTE
WITH expired AS (
    SELECT id FROM sales.orders
    WHERE status = 'Pending'
      AND created_at < now() - INTERVAL '24 hours'
)
UPDATE sales.orders o
SET status = 'Expired'
FROM expired e
WHERE o.id = e.id;
```

### DELETE

```sql
-- Soft delete (recomendado)
UPDATE sales.orders
SET status = 'Deleted', deleted_at = now()
WHERE id = @orderId;

-- DELETE con RETURNING
DELETE FROM sales.orders
WHERE status = 'Deleted' AND deleted_at < now() - INTERVAL '90 days'
RETURNING id;
```

### MERGE (PostgreSQL 15+)

```sql
MERGE INTO catalog.products p
USING (VALUES ('SKU-1', 'Updated Widget', 39.99)) AS src (sku, name, price)
ON p.sku = src.sku
WHEN MATCHED THEN
    UPDATE SET name = src.name, price = src.price
WHEN NOT MATCHED THEN
    INSERT (sku, name, price) VALUES (src.sku, src.name, src.price);
-- PostgreSQL 17+: MERGE con RETURNING
```

---

## Herramientas

### psql

```bash
# Conectar
psql -h localhost -U app_user -d miapp

# Comandos comunes (\?)
\dt sales.*          # Listar tablas del schema sales
\d+ sales.orders     # Describir tabla con detalles
\di+                 # Listar índices con detalles
\df sales.*          # Listar funciones
\dv                  # Listar vistas
\du                  # Listar usuarios/roles
\conninfo            # Info de conexión
\timing              # Mostrar tiempo de ejecución
\e                   # Abrir editor externo
\i script.sql        # Ejecutar archivo
\o output.txt        # Redirigir output a archivo
```

### pgAdmin y DBeaver

- **pgAdmin**: GUI web oficial. Completo pero pesado.
- **DBeaver**: Multi-engine (PG, SQL Server, MySQL). Ligero y potente.
- **DataGrip**: JetBrains. Excelente autocompletado y refactoring SQL.

---

## Variables y control de flujo en PL/pgSQL

```sql
DO $$
DECLARE
    order_count INT;
    customer_id TEXT := 'CUST-001';
BEGIN
    SELECT COUNT(*) INTO order_count
    FROM sales.orders WHERE customer_id = customer_id;

    IF order_count = 0 THEN
        RAISE NOTICE 'No orders for %', customer_id;
    ELSIF order_count < 10 THEN
        RAISE NOTICE 'Customer % has few orders: %', customer_id, order_count;
    ELSE
        RAISE NOTICE 'Customer % has % orders', customer_id, order_count;
    END IF;
END $$;
```

---

## Funciones del sistema útiles

```sql
-- String
SELECT customer_id || ' - ' || name FROM customers;  -- Concatenación
SELECT CONCAT(first_name, ' ', last_name);
SELECT FORMAT('Order #%s for customer %s', order_number, customer_id);
SELECT STRING_AGG(tag, ', ' ORDER BY tag) FROM tags; -- Aggregar strings
SELECT SPLIT_PART('a,b,c', ',', 2);                  -- 'b'
SELECT LEFT(email, 5), RIGHT(phone, 4);
SELECT TRIM('  text  '), LTRIM, RTRIM;
SELECT REPLACE(description, 'old', 'new');
SELECT TRANSLATE('123-456', '-', '');                 -- '123456'
SELECT REGEXP_REPLACE(phone, '[^\d]', '', 'g');       -- Solo dígitos

-- Numérico
SELECT GREATEST(a, b, c), LEAST(a, b, c);
SELECT ROUND(123.456, 2), CEIL(123.1), FLOOR(123.9);

-- Fecha/hora
SELECT now(), CURRENT_TIMESTAMP, CURRENT_DATE, CURRENT_TIME;
SELECT date_trunc('hour', created_at);
SELECT date_part('year', created_at);
SELECT EXTRACT(MONTH FROM created_at);
SELECT created_at + INTERVAL '7 days';
SELECT AGE(now(), created_at);                        -- Duración

-- NULL handling
SELECT COALESCE(NULL, NULL, 'default');
SELECT NULLIF(value, 0);

-- Cast
SELECT CAST('123' AS INT);
SELECT '123'::INT;
SELECT try_cast('abc' AS INT);                        -- PG 18: NULL en vez de error
```

---

## Convenciones de código

### Naming

| Objeto | Convención | Ejemplo |
|--------|------------|---------|
| Tablas | `snake_case`, plural | `orders`, `order_items` |
| Schemas | `snake_case` | `sales`, `catalog`, `audit` |
| Columnas | `snake_case` | `customer_id`, `created_at` |
| PK | `{table}_pkey` (auto) o `pk_{table}` | `orders_pkey` |
| FK | `fk_{table}_{ref}` | `fk_order_items_orders` |
| Índices | `idx_{table}_{cols}` | `idx_orders_customer_id_status` o `ix_orders_customer_id_status` |
| CHECK | `ck_{table}_{rule}` | `ck_orders_status` |
| Funciones | `{schema}.{action}_{entity}` | `sales.create_order()` |
| Procedimientos | `{schema}.{verb}_{entity}` | `sales.archive_old_orders()` |

### Formato PL/pgSQL

```sql
-- ✅ Keywords SQL en MAYÚSCULAS, identificadores en snake_case
CREATE OR REPLACE FUNCTION sales.create_order(
    p_customer_id   TEXT,
    p_total_amount  NUMERIC(18,4)
) RETURNS UUID AS $$
DECLARE
    v_order_id UUID := uuidv7();
BEGIN
    INSERT INTO sales.orders (id, customer_id, total_amount)
    VALUES (v_order_id, p_customer_id, p_total_amount);

    RETURN v_order_id;
END;
$$ LANGUAGE plpgsql;
```

### Reglas de oro

1. **`TEXT` sobre `VARCHAR(n)`** salvo que el límite sea requisito de negocio.
2. **`TIMESTAMPTZ` siempre.** Guarda UTC, la app maneja la presentación.
3. **`uuidv7()` para PKs.** Mejor rendimiento en índices B-tree que `gen_random_uuid()` (UUIDv4).
4. **`GENERATED ALWAYS AS IDENTITY`** sobre `SERIAL`. Es estándar SQL y más seguro.
5. **`ON CONFLICT`** sobre `MERGE` para upserts simples. Menos overhead.
6. **Prefijo `p_` para parámetros.** Evita ambigüedad con columnas.
7. **`now()` para timestamps UTC.** `CURRENT_TIMESTAMP` también devuelve `TIMESTAMPTZ`.
8. **Esquemas para organizar.** No usar `public` para datos de aplicación.
9. **`RETURNING` después de DML.** Evita queries adicionales para recuperar IDs.
10. **Constraints con nombre.** Facilita migraciones y debugging.

---

## Extensiones esenciales

```sql
-- pg_stat_statements: monitoreo de queries
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- pgcrypto: hashing y cifrado
CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- gen_random_uuid(), crypt(), pgp_sym_encrypt()

-- uuid-ossp: UUID generation (obsoleto por gen_random_uuid())
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- pg_trgm: trigram matching para búsquedas difusas
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- hstore: key-value pairs
CREATE EXTENSION IF NOT EXISTS hstore;

-- PostGIS: datos geoespaciales
CREATE EXTENSION IF NOT EXISTS postgis;

-- pgvector: vectores para AI/embeddings
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## Sub-skills del kit

> 📁 Cada sub-skill tiene su propio `SKILL.md` con el detalle; el subagente `.opencode/agent/postgres.md` decide cuál cargar según la tarea.


| Skill | Cuándo cargarla |
|-------|-----------------|
| `postgresql-performance` | EXPLAIN ANALYZE, índices (B-tree, GIN, GiST, BRIN), vacuum, estadísticas, particionamiento |
| `postgresql-architecture` | Tablespaces, MVCC profundo, WAL, replicación (streaming + lógica), particionamiento declarativo |
| `postgresql-security` | Roles, GRANT/REVOKE, RLS, SSL, pg_hba.conf, SCRAM authentication |
| `postgresql-procedural` | Funciones PL/pgSQL, triggers, vistas, vistas materializadas, reglas, event triggers, extensiones |
| `postgresql-advanced` | CTEs recursivos, window functions, JSON/JSONB, full-text search, arrays, range types, pgvector |
| `postgresql-deployment` | Migraciones (Flyway/EF Core), pg_dump/pg_restore, CI/CD, Docker, zero-downtime, pg_upgrade |
| `postgresql-integration` | Npgsql, EF Core con PostgreSQL, Dapper, connection pooling, PgBouncer |

---

## Stack recomendado

| Propósito | Herramienta | Notas |
|-----------|-------------|-------|
| IDE | DBeaver o DataGrip | Multi-engine, potente |
| ORM | EF Core + `Npgsql.EntityFrameworkCore.PostgreSQL` | Provider oficial |
| Micro-ORM | Dapper + Npgsql | Alto rendimiento |
| Migraciones | Flyway o EF Core Migrations | Flyway para control SQL completo |
| Monitoring | `pg_stat_statements` + pgBadger | Built-in + análisis de logs |
| Pooling | PgBouncer | Connection pooling externo |
| Backups | `pg_dump` / `pg_basebackup` / Barman | Según RPO |
| Container | `postgres:18-alpine` | Docker para desarrollo |
