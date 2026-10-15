---
name: postgresql-procedural
description: "Programación procedural en PostgreSQL con PL/pgSQL. Cubre funciones (RETURNS TABLE, SETOF, VOID), procedimientos (CALL/COMMIT), triggers (BEFORE/AFTER/INSTEAD OF), vistas, vistas materializadas, reglas, event triggers, extensiones, y manejo de errores con EXCEPTION. Actívala al implementar lógica de negocio en la base de datos, migrar funciones desde Oracle/SQL Server, o diseñar APIs de datos con PostgreSQL."
disable-model-invocation: true
---

# PostgreSQL Procedural Programming

Guía de programación procedural en PL/pgSQL. Toda lógica de negocio en la BD debe seguir estas convenciones.

---

## Funciones

### Template estándar

```sql
CREATE OR REPLACE FUNCTION sales.create_order(
    p_customer_id   TEXT,
    p_items         JSONB,          -- Array de items como JSON
    p_currency      TEXT DEFAULT 'MXN'
) RETURNS UUID AS $$
DECLARE
    v_order_id      UUID := uuidv7();
    v_order_number  INT;
    v_item          JSONB;
    v_total         NUMERIC(18,4) := 0;
BEGIN
    -- Validación
    IF NOT EXISTS (SELECT 1 FROM catalog.customers WHERE id = p_customer_id) THEN
        RAISE EXCEPTION 'Customer not found: %', p_customer_id
            USING ERRCODE = 'CUSTF';  -- Código de error custom
    END IF;

    -- Calcular total
    FOR v_item IN SELECT * FROM jsonb_array_elements(p_items)
    LOOP
        v_total := v_total + (v_item->>'quantity')::INT * (v_item->>'unit_price')::NUMERIC;
    END LOOP;

    -- Insertar orden
    INSERT INTO sales.orders (id, customer_id, total_amount, currency)
    VALUES (v_order_id, p_customer_id, v_total, p_currency)
    RETURNING order_number INTO v_order_number;

    -- Insertar items
    INSERT INTO sales.order_items (order_id, order_number, sku, quantity, unit_price, line_number)
    SELECT
        v_order_id, v_order_number,
        item->>'sku',
        (item->>'quantity')::INT,
        (item->>'unit_price')::NUMERIC,
        ROW_NUMBER() OVER ()
    FROM jsonb_array_elements(p_items) AS item;

    RETURN v_order_id;
END;
$$ LANGUAGE plpgsql;
```

### Tipos de retorno

| Retorno | Uso |
|---------|-----|
| `RETURNS UUID` | Valor escalar |
| `RETURNS SETOF table_name` | Múltiples filas de una tabla |
| `RETURNS TABLE(col1 type, col2 type)` | Estructura definida inline |
| `RETURNS VOID` | Sin retorno (o usar PROCEDURE) |
| `RETURNS TRIGGER` | Solo para triggers |

### Funciones SQL (sin PL/pgSQL)

Para queries simples que el planner puede optimizar mejor sin overhead procedural:

```sql
CREATE OR REPLACE FUNCTION sales.get_orders_by_customer(p_customer_id TEXT)
RETURNS SETOF sales.orders AS $$
    SELECT * FROM sales.orders WHERE customer_id = p_customer_id;
$$ LANGUAGE SQL STABLE;
-- STABLE: mismo resultado para mismos argumentos en una query (permite optimizaciones)
```

### Function volatility

| Categoría | Significado | Cuándo |
|-----------|-------------|--------|
| `IMMUTABLE` | Mismo resultado para mismos argumentos siempre | `LOWER()`, cálculo matemático |
| `STABLE` | Mismo resultado dentro de una query | `now()`, lookup por PK |
| `VOLATILE` (default) | Puede dar diferente resultado cada vez | `random()`, INSERT/UPDATE/DELETE |

---

## Procedimientos (PostgreSQL 11+)

A diferencia de funciones, los procedimientos pueden manejar transacciones (COMMIT/ROLLBACK).

```sql
CREATE OR REPLACE PROCEDURE sales.archive_old_orders(
    p_days_old INT DEFAULT 365
) AS $$
DECLARE
    v_count INT;
BEGIN
    -- Archivar en lotes para evitar transacciones enormes
    LOOP
        DELETE FROM sales.orders
        WHERE status = 'Delivered'
          AND updated_at < now() - (p_days_old || ' days')::INTERVAL
        LIMIT 1000;

        GET DIAGNOSTICS v_count = ROW_COUNT;
        EXIT WHEN v_count = 0;

        COMMIT;  -- ✅ Permitido en procedimientos
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Llamar procedimiento
CALL sales.archive_old_orders(90);
```

---

## Triggers

### AFTER trigger (auditoría)

```sql
-- Función del trigger
CREATE OR REPLACE FUNCTION audit.log_order_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit.order_changes (order_id, action, new_status, changed_at, changed_by)
        VALUES (NEW.id, 'INSERT', NEW.status, now(), current_user);
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        IF OLD.status IS DISTINCT FROM NEW.status THEN
            INSERT INTO audit.order_changes (order_id, action, old_status, new_status, changed_at, changed_by)
            VALUES (NEW.id, 'UPDATE', OLD.status, NEW.status, now(), current_user);
        END IF;
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit.order_changes (order_id, action, old_status, changed_at, changed_by)
        VALUES (OLD.id, 'DELETE', OLD.status, now(), current_user);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger
CREATE TRIGGER trg_orders_audit
    AFTER INSERT OR UPDATE OR DELETE ON sales.orders
    FOR EACH ROW EXECUTE FUNCTION audit.log_order_changes();
```

### BEFORE trigger (validación)

```sql
CREATE OR REPLACE FUNCTION sales.validate_order_before_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Validar total_amount positivo
    IF NEW.total_amount < 0 THEN
        RAISE EXCEPTION 'Total amount must be positive: %', NEW.total_amount;
    END IF;

    -- Set defaults
    NEW.updated_at := now();

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_orders_validate
    BEFORE INSERT OR UPDATE ON sales.orders
    FOR EACH ROW EXECUTE FUNCTION sales.validate_order_before_insert();
```

### INSTEAD OF trigger (vistas actualizables)

```sql
-- Vista que consolida datos de múltiples tablas
CREATE VIEW sales.vw_order_summary AS
SELECT o.id, o.customer_id, o.status, o.total_amount, o.created_at,
       c.name AS customer_name
FROM sales.orders o
JOIN catalog.customers c ON o.customer_id = c.id;

-- Trigger para permitir INSERT a través de la vista
CREATE OR REPLACE FUNCTION sales.insert_through_order_summary()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO sales.orders (customer_id, total_amount)
    VALUES (NEW.customer_id, NEW.total_amount)
    RETURNING id INTO NEW.id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_order_summary_insert
    INSTEAD OF INSERT ON sales.vw_order_summary
    FOR EACH ROW EXECUTE FUNCTION sales.insert_through_order_summary();
```

---

## Vistas materializadas

```sql
-- Vista materializada (resultados cacheados en disco)
CREATE MATERIALIZED VIEW sales.mv_monthly_sales AS
SELECT
    customer_id,
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS order_count,
    SUM(total_amount) AS total_amount
FROM sales.orders
WHERE status NOT IN ('Deleted', 'Cancelled')
GROUP BY customer_id, DATE_TRUNC('month', created_at);

-- Índices en vista materializada
CREATE INDEX idx_mv_monthly_sales_customer
    ON sales.mv_monthly_sales (customer_id, month);

-- Refrescar (recalcula desde cero — bloquea la vista)
REFRESH MATERIALIZED VIEW sales.mv_monthly_sales;

-- Refrescar concurrentemente (requiere índice único)
CREATE UNIQUE INDEX idx_mv_monthly_sales_uniq
    ON sales.mv_monthly_sales (customer_id, month);
REFRESH MATERIALIZED VIEW CONCURRENTLY sales.mv_monthly_sales;
```

---

## Manejo de errores

```sql
CREATE OR REPLACE FUNCTION sales.safe_create_order(
    p_customer_id TEXT,
    p_total_amount NUMERIC
) RETURNS UUID AS $$
DECLARE
    v_order_id UUID;
BEGIN
    -- Intentar insert
    INSERT INTO sales.orders (id, customer_id, total_amount)
    VALUES (uuidv7(), p_customer_id, p_total_amount)
    RETURNING id INTO v_order_id;

    RETURN v_order_id;

EXCEPTION
    WHEN foreign_key_violation THEN
        RAISE EXCEPTION 'Customer does not exist: %', p_customer_id
            USING ERRCODE = 'CUSTF', HINT = 'Verify customer ID in catalog.customers';

    WHEN check_violation THEN
        RAISE EXCEPTION 'Invalid order data: %', SQLERRM;

    WHEN OTHERS THEN
        -- Loggear error desconocido
        RAISE WARNING 'Unexpected error creating order: %', SQLERRM;
        RAISE;
END;
$$ LANGUAGE plpgsql;
```

### Códigos de error comunes

| Código | Significado |
|--------|-------------|
| `23505` | unique_violation |
| `23503` | foreign_key_violation |
| `23514` | check_violation |
| `23502` | not_null_violation |
| `40P01` | deadlock_detected |
| `40001` | serialization_failure |
| `P0001` | raise_exception |

---

## Extensiones para tareas específicas

```sql
-- pg_partman: manejo automático de particiones
CREATE EXTENSION pg_partman;

-- postgres_fdw: foreign data wrapper (conectarse a otras DBs)
CREATE EXTENSION postgres_fdw;
CREATE SERVER remote_pg FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host '10.0.0.5', dbname 'analytics', port '5432');
CREATE USER MAPPING FOR app_user SERVER remote_pg
    OPTIONS (user 'analytics_reader', password '***');

-- plpython3u: funciones en Python
CREATE EXTENSION plpython3u;

CREATE OR REPLACE FUNCTION analytics.sentiment_analysis(text TEXT)
RETURNS TEXT AS $$
    # Código Python con acceso a bibliotecas NLP
    import some_nlp_lib
    return some_nlp_lib.analyze(text)
$$ LANGUAGE plpython3u;
```

---

## Checklist procedural

- [ ] Funciones usan `p_` prefix para parámetros para evitar ambigüedad con columnas
- [ ] Volatility correcto: `IMMUTABLE`, `STABLE`, o `VOLATILE`
- [ ] Triggers simples: un propósito por trigger
- [ ] Triggers manejan `FOR EACH ROW` con `NEW` y `OLD`
- [ ] Procedimientos para operaciones que requieren COMMIT en lotes
- [ ] Vistas materializadas con `REFRESH MATERIALIZED VIEW CONCURRENTLY`
- [ ] Errores con `ERRCODE` semántico, no `OTHERS` genérico
- [ ] `RAISE EXCEPTION` con mensaje descriptivo
- [ ] Funciones SQL puras para queries simples que el planner puede optimizar
- [ ] Extensiones evaluadas antes de escribir código custom (pg_partman, postgres_fdw)
