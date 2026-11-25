---
name: postgres-schema-inspection
description: Inspect PostgreSQL database schemas — list tables, columns, types, defaults, row counts. Handles read-only users with restricted schema permissions where information_schema is blocked.
---

# PostgreSQL Schema Inspection

Use when you need to explore an unfamiliar PostgreSQL database: list tables, discover column definitions, estimate row counts, find indexes. Works even with restricted read-only users that can't access `information_schema` or SELECT from tables.

## Trigger conditions
- User shares PostgreSQL credentials and asks you to "analyze the structure" or "look at the tables"
- You need to discover what tables/columns exist in a remote PostgreSQL database
- The user provides limited read-only credentials (may lack `information_schema` access)

## Step 1: Connect and list all tables

Use `pg_class` JOIN `pg_namespace` — this works even when `information_schema.tables` returns empty for non-public schemas:

```python
cur.execute("""
    SELECT n.nspname, c.relname, c.reltuples::bigint
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
      AND c.relkind = 'r'
    ORDER BY n.nspname, c.relname
""")
```

`reltuples` is an estimate — use `pg_stat_user_tables.n_live_tup` for accurate row counts (Step 4).

## Step 2: Get column details per table

Use the three-way JOIN `pg_class → pg_attribute → pg_attrdef` to get columns, types, nullability, and defaults:

```python
cur.execute("""
    SELECT c.relname,
           a.attname,
           pg_catalog.format_type(a.atttypid, a.atttypmod),
           CASE WHEN a.attnotnull THEN 'NOT NULL' ELSE 'NULL' END,
           COALESCE(pg_get_expr(d.adbin, d.adrelid), '')
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    JOIN pg_attribute a ON a.attrelid = c.oid
    LEFT JOIN pg_attrdef d ON d.adrelid = c.oid AND d.adnum = a.attnum
    WHERE n.nspname = %s
      AND c.relkind = 'r'
      AND a.attnum > 0
      AND NOT a.attisdropped
    ORDER BY c.relname, a.attnum
""", (schema_name,))
```

Filter: `a.attnum > 0` excludes system columns (oid, xmin, etc.), `NOT a.attisdropped` excludes dropped columns.

## Step 3: Find indexes on key tables

```python
cur.execute("""
    SELECT indexname, indexdef
    FROM pg_indexes
    WHERE schemaname = %s AND tablename = %s
    ORDER BY indexname
""", (schema_name, table_name))
```

## Step 4: Get accurate row counts

`pg_stat_user_tables` gives live/dead tuple counts even when `SELECT COUNT(*)` is denied:

```python
cur.execute("""
    SELECT schemaname, relname, n_live_tup, n_dead_tup, last_analyze
    FROM pg_stat_user_tables
    ORDER BY schemaname, relname
""")
```

## Step 5: Discover views and their definitions

`pg_views` exposes view SQL even when you can't SELECT from the view:

```python
cur.execute("""
    SELECT schemaname, viewname, definition
    FROM pg_views
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    ORDER BY viewname
""")
```

Also check for materialized views (`relkind = 'm'` in pg_class) and SECURITY DEFINER functions (`p.prosecdef = true` in pg_proc) — these may bypass normal permissions.

## Step 6: Permission diagnostic (when data access is denied)

When a read-only user can see metadata but not SELECT data, run this diagnostic battery:

```python
# Schema-level access
for schema in ['wecom', 'ops', 'dashboard', 'public']:
    cur.execute("SELECT has_schema_privilege(%s, 'USAGE')", (schema,))
    print(f"  {schema}: {cur.fetchone()[0]}")

# Table/view-level access
for obj in ['public.messages', 'wecom.messages']:
    cur.execute("SELECT has_table_privilege(%s, 'SELECT')", (obj,))
    print(f"  {obj}: {cur.fetchone()[0]}")

# Role membership (inherited permissions)
cur.execute("""
    SELECT r.rolname, array_agg(m.rolname)
    FROM pg_roles r
    LEFT JOIN pg_auth_members am ON am.member = r.oid
    LEFT JOIN pg_roles m ON m.oid = am.roleid
    WHERE r.rolname = current_user
    GROUP BY r.rolname
""")

# Check for RLS policies
cur.execute("SELECT * FROM pg_policies")

# Check default privileges
cur.execute("SELECT * FROM pg_default_acl")
```

**No backdoors exist**: PostgreSQL's permission model is strict — no USAGE + no SELECT = no data access. `COPY` inherits the same permissions. `pg_stats` MCV/histograms won't help if the table hasn't been ANALYZEd. The only path forward is `GRANT SELECT`.

### The `ALTER DEFAULT PRIVILEGES` trap (common root cause)

When DBA says "I already ran the GRANTs" but `pg_class.relacl` still shows `NULL`, check this chain:

```python
# 1. Who owns the views?
cur.execute("""
    SELECT c.relname, pg_get_userbyid(c.relowner) AS owner, c.relacl
    FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public' AND c.relkind = 'v'
""")
# If owner = 'wecome_role' but DBA ran ALTER DEFAULT PRIVILEGES as 'postgres',
# the default only applies to objects created BY postgres — not wecome_role's objects.
```

**The trap**: `ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT … TO wecom_read_only` is **role-scoped** — it only affects future objects created BY the role that executed the command. If views are owned by `wecome_role` but another role ran `ALTER DEFAULT PRIVILEGES`, it silently does nothing.

**The fix**: Either the view owner or a superuser must run:
```sql
GRANT SELECT ON ALL TABLES IN SCHEMA public TO wecom_read_only;
```
Or grant on specific views:
```sql
GRANT SELECT ON public.messages, public.sessions, public.contacts TO wecom_read_only;
```

**Verification**: After the GRANT, `pg_class.relacl` should change from `NULL` to `{wecome_role=arwdDxt/wecome_role,wecom_read_only=r/wecome_role}`.

Red flags: `seq_scan` >> `n_live_tup` on frequently-queried tables, `seq_tup_read` in the hundreds of millions, empty but heavily-scanned tables (indicates polling).

## Pitfalls

### Permission-denied transaction aborts
When a query fails with "permission denied", psycopg2 puts the connection in an aborted transaction. All subsequent queries fail with `InFailedSqlTransaction`. **Fix**: set `conn.autocommit = True` before the inspection loop, or wrap each query in try/except with `conn.rollback()`.

### `::regclass` cast requires schema USAGE permission
This fails with restricted users:
```python
cur.execute("... WHERE c.oid = 'wecom.messages'::regclass")  # ❌ permission denied
```
Use the JOIN approach instead:
```python
cur.execute("... JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = %s AND c.relname = %s", (schema, table))  # ✅
```

### `information_schema.columns` may return empty
A read-only user may lack `USAGE` on schemas, causing `information_schema.columns` to return no rows even though tables exist. Always fall back to `pg_attribute`.

### `information_schema.table_privileges` may return empty
Same root cause: without `USAGE` on the schema, `information_schema.table_privileges` returns no rows for that schema's objects. Use `has_table_privilege()` (a pg_catalog function, always accessible) or check `pg_class.relacl` directly:

```python
# Always works, even without schema USAGE:
cur.execute("SELECT has_table_privilege(%s, 'SELECT')", (obj_name,))

# Check raw ACL on views (works via pg_class JOIN pg_namespace):
cur.execute("""
    SELECT c.relname, c.relacl
    FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE n.nspname = 'public' AND c.relkind = 'v'
""")
```

### pip may not exist in the venv
If `pip3` and `pip` are not found, install via `ensurepip` or `get-pip.py`:
```bash
python -m ensurepip
# or
curl -sS https://bootstrap.pypa.io/get-pip.py | python
```
