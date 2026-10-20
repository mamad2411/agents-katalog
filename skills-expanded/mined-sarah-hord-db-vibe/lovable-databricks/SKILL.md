---
name: lovable-databricks
description: Connect Lovable.dev apps to Databricks — SQL warehouses for analytics, Unity Catalog for governed data access, and Lakebase PostgreSQL as a primary backend. Covers setup, query patterns, and architecture guidance.
---

# Lovable → Databricks Integration Skill

Connect a [Lovable.dev](https://lovable.dev) app to Databricks data infrastructure. Three integration patterns:

| Pattern | When to use |
|---------|-------------|
| **SQL Warehouse** | Analytics dashboards, BI queries, large-scale data reads |
| **Unity Catalog** | Governed data access, table discovery, lineage-aware queries |
| **Lakebase** | App backend database (transactional, replacing Supabase PostgreSQL) |

---

## Pattern 1 — SQL Warehouse (Analytics)

Use when your Lovable app needs to query Databricks tables for charts, reports, or dashboards.

### Architecture

```
Lovable App (React)
  └── API route / Edge Function
        └── Databricks SQL Connector (JDBC/REST)
              └── SQL Warehouse
                    └── Unity Catalog tables
```

### Backend setup (Node.js / Vercel edge function)

```bash
npm install @databricks/sql
```

```typescript
// lib/databricks.ts
import { DBSQLClient } from '@databricks/sql';

const client = new DBSQLClient();

export async function queryWarehouse(sql: string, params?: Record<string, unknown>) {
  const conn = await client.connect({
    host: process.env.DATABRICKS_HOST!,       // e.g. adb-1234.azuredatabricks.net
    path: process.env.DATABRICKS_HTTP_PATH!,   // /sql/1.0/warehouses/abc123
    token: process.env.DATABRICKS_TOKEN!,
  });

  const session = await conn.openSession({ initialCatalog: process.env.DATABRICKS_CATALOG });
  const query = await session.executeStatement(sql, { queryTimeout: 30 });
  const result = await query.fetchAll();
  await query.close();
  await session.close();
  await conn.close();
  return result;
}
```

```typescript
// pages/api/metrics.ts (Next.js) or routes/metrics.ts (Remix)
import { queryWarehouse } from '@/lib/databricks';

export async function GET() {
  const rows = await queryWarehouse(`
    SELECT date_trunc('day', event_time) AS day, count(*) AS events
    FROM catalog.schema.events
    WHERE event_time >= current_date - INTERVAL 30 DAYS
    GROUP BY 1 ORDER BY 1
  `);
  return Response.json(rows);
}
```

### Environment variables

```env
DATABRICKS_HOST=adb-XXXXXXXXXX.XX.azuredatabricks.net
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/YOUR_WAREHOUSE_ID
DATABRICKS_TOKEN=dapi...
DATABRICKS_CATALOG=main
DATABRICKS_SCHEMA=default
```

### Where to get credentials

1. **Host**: Databricks workspace → Settings → Workspace URL (strip `https://`)
2. **HTTP Path**: SQL Warehouses → your warehouse → Connection Details → HTTP Path
3. **Token**: Settings → Developer → Personal access tokens → Generate new token
4. **Catalog/Schema**: Unity Catalog Explorer → pick the target catalog and schema

---

## Pattern 2 — Unity Catalog (Governed Access)

Use when data governance, lineage, or table discovery matters for your app.

### List available catalogs and schemas

```typescript
// Discover what data is available
const catalogs = await queryWarehouse(`SHOW CATALOGS`);
const schemas = await queryWarehouse(`SHOW SCHEMAS IN my_catalog`);
const tables = await queryWarehouse(`SHOW TABLES IN my_catalog.my_schema`);
```

### Read table with column metadata

```typescript
const schema = await queryWarehouse(`DESCRIBE TABLE my_catalog.my_schema.my_table`);
const sample = await queryWarehouse(`SELECT * FROM my_catalog.my_schema.my_table LIMIT 100`);
```

### Row-level security via Unity Catalog

If your Unity Catalog has row filters, they apply automatically — no app-level filtering needed:

```sql
-- UC handles this transparently based on the token identity
SELECT * FROM catalog.schema.customer_orders
-- Users only see their own orders if a row filter is defined in UC
```

### Unity Catalog REST API (for metadata-heavy apps)

```typescript
// List catalogs via REST (useful for admin UIs)
const res = await fetch(`https://${process.env.DATABRICKS_HOST}/api/2.1/unity-catalog/catalogs`, {
  headers: { Authorization: `Bearer ${process.env.DATABRICKS_TOKEN}` }
});
const { catalogs } = await res.json();
```

---

## Pattern 3 — Lakebase (Transactional Backend)

Use Lakebase as a PostgreSQL-compatible primary database for your Lovable app. Best for replacing Supabase.

> To **migrate** an existing Lovable+Supabase app to Lakebase, use `/lovable-migrate` instead.

### Create a new Lakebase database

```bash
# Using Databricks CLI
databricks lakebase databases create --name my_app_db --workspace-id YOUR_WORKSPACE_ID
```

Or via the REST API:

```bash
curl -X POST https://$DATABRICKS_HOST/api/2.0/lakebase/instances \
  -H "Authorization: Bearer $DATABRICKS_TOKEN" \
  -d '{"name": "my_app_db", "capacity": "CU_1"}'
```

### Connect from Lovable app

```typescript
// lib/db.ts
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  // DATABASE_URL format: postgresql://user:token@host:5432/db
  ssl: { rejectUnauthorized: false }
});

export { pool };
```

```typescript
// Example CRUD
const { rows } = await pool.query(
  'INSERT INTO items (name, value) VALUES ($1, $2) RETURNING *',
  [name, value]
);
```

### .env for Lakebase

```env
DATABASE_URL=postgresql://token:dapi...@your-lakebase-host.databricks.com:5432/my_app_db
```

---

## Architecture Recommendations

### Simple analytics app
```
Lovable (React + Vercel) → API routes → Databricks SQL Warehouse → Unity Catalog
```

### Full-stack app with governed data
```
Lovable (React + Vercel)
  ├── /api/data/*  → Databricks SQL Warehouse (reads)
  └── /api/app/*   → Lakebase PostgreSQL (writes/transactions)
```

### Hybrid (migrate from Supabase, keep analytics)
```
Lovable (React + Vercel)
  ├── DB backend  → Lakebase (migrated from Supabase via /lovable-migrate)
  └── Analytics   → SQL Warehouse (new capability, Supabase had none)
```

---

## What to ask the user

When helping with a Lovable + Databricks integration, ask:

1. **What's the use case?** — Analytics/BI dashboards, or transactional app backend?
2. **Existing Supabase?** — If yes, use `/lovable-migrate` to move to Lakebase first
3. **Databricks workspace type?** — Personal FE-VM, OE workspace, or customer workspace?
4. **Data governance requirements?** — If regulated data, lean into Unity Catalog row filters
5. **Volume?** — High-volume writes → Lakebase; high-volume reads → SQL Warehouse

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `DATABRICKS_TOKEN` auth failures | Rotate PAT in Settings → Developer |
| SQL Warehouse timeout | Increase `queryTimeout`; check warehouse auto-stop setting |
| Unity Catalog permission denied | Check `USE CATALOG` + `SELECT` grants in UC Explorer |
| Lakebase connection refused | Verify workspace has Lakebase enabled (FE-VM recommended) |
| CORS errors on API routes | Add `Access-Control-Allow-Origin` header to API responses |

---

## Related skills

- `/lovable-migrate` — Migrate existing Lovable+Supabase app to Lakebase
- `/databricks-lakebase` — Deep-dive Lakebase provisioning and management
- `/databricks-warehouse-selector` — Pick the right SQL warehouse for your workload
- `/lovable-architect` — Broader Lovable architecture decisions
