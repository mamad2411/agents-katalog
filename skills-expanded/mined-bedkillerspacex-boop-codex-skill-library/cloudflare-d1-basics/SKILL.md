---
name: cloudflare-d1-basics
description: >
  Use Cloudflare D1 (SQLite at the edge) from Workers: database create/bind, schema
  migrations, prepared statements, batching, backups/export, and limits. Use for owned
  CF accounts building Worker-backed apps — not as a full OLAP warehouse substitute
  (consider ClickHouse/other) or for R2/object storage (cloudflare-r2-public-access).
---

# Cloudflare D1 Basics

## Scope And Authorization

- **In scope:** Cloudflare accounts and Workers/D1 databases you own.
- **Out of scope:** accessing other tenants’ D1; destructive prod DROP without backup plan.
- Prefer separate D1 DBs per environment (dev/stage/prod).
- Redact `wrangler` OAuth tokens and account IDs in public docs as needed.
- Pair with `cloudflare-workers-bindings` and `code-quality-standards`.

## When To Use

- Edge/SQL state for Workers with relational queries.
- Schema migrations, bindings in `wrangler.toml`, local `--local` dev.
- Tokens: D1, SQLite, wrangler d1, prepare/bind, migrations, Worker binding.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Workers bindings matrix (KV/R2/Queues) | `cloudflare-workers-bindings` |
| Object storage public access | `cloudflare-r2-public-access` |
| Zero Trust Access | `cloudflare-access-policies` |
| Heavy analytics OLAP | `clickhouse-*` skills |
| SQL injection defenses general | `sqli-sql-injection` / parameterized queries here |

## Core Concepts

| Concept | Detail |
| --- | --- |
| D1 database | SQLite-compatible managed DB per account |
| Binding | `env.DB` in Worker via wrangler config |
| Sessions/API | `prepare`, `bind`, `first`, `all`, `run`, `batch` |
| Migrations | SQL files applied via wrangler |
| Placement | Edge-oriented; design for locality & limits |

## Workflow

### 1. Confirm scope and success criteria

1. Account, Worker name, env split, data sensitivity, RPO for backups.
2. Success: migrations apply cleanly; Worker CRUD works; secrets not in SQL strings.
3. Rollback: previous migration + export snapshot.

### 2. Create database and bind

```bash
npx wrangler d1 create app-db-prod
# note database_id from output
```

```toml
# wrangler.toml
name = "app-api"
main = "src/index.ts"
compatibility_date = "2024-11-01"

[[d1_databases]]
binding = "DB"
database_name = "app-db-prod"
database_id = "REDACTED-UUID"
migrations_dir = "migrations"
```

### 3. Schema and migrations

```sql
-- migrations/0001_init.sql
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

```bash
npx wrangler d1 migrations apply app-db-prod --remote
npx wrangler d1 migrations apply app-db-prod --local
```

1. Never hand-edit prod schema only; use migration files in git.
2. Avoid unbounded schema churn; SQLite ALTER limitations apply.

### 4. Query from Worker (parameterized)

```typescript
export interface Env {
  DB: D1Database;
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    if (req.method === "GET" && url.pathname === "/users") {
      const email = url.searchParams.get("email");
      if (!email) return new Response("email required", { status: 400 });
      const row = await env.DB.prepare(
        "SELECT id, email, created_at FROM users WHERE email = ?"
      )
        .bind(email)
        .first();
      return Response.json(row ?? {});
    }
    return new Response("not found", { status: 404 });
  },
};
```

**Batch:**

```typescript
await env.DB.batch([
  env.DB.prepare("INSERT INTO users (id, email) VALUES (?, ?)").bind(id, email),
  env.DB.prepare("INSERT INTO audit (user_id, action) VALUES (?, ?)").bind(id, "create"),
]);
```

1. **Always** bind parameters — never string-concatenate user input.
2. Handle `D1_ERROR` / constraint failures explicitly.
3. Mind request CPU/time limits; avoid huge scans in a single Worker invoke.

### 5. Local dev, export, backup

```bash
npx wrangler dev
npx wrangler d1 execute app-db-prod --local --command "SELECT COUNT(*) FROM users"
npx wrangler d1 export app-db-prod --remote --output backup.sql
```

1. Schedule exports for prod RPO; store backups in controlled storage (R2 private).
2. Do not download prod dumps to unmanaged laptops with PII without policy.

### 6. Verify

1. Migration version table present; schema matches repo.
2. Integration test: insert/select/unique constraint.
3. Confirm binding name matches `Env` type and deploy env (prod vs preview).
4. Load sanity: hot query uses index (`EXPLAIN QUERY PLAN` via execute).

### 7. Operate and limits

| Concern | Practice |
| --- | --- |
| Size/perf limits | Design per current CF D1 limits; paginate |
| Multi-tenant | tenant_id columns + strict Worker authz |
| Secrets | In Worker secrets, not D1 rows unless encrypted |
| Preview envs | Separate DB or careful shared dev DB |
| Observability | Log query failures without binding PII |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| SQL | Prepared + bind | `WHERE email = '${email}'` |
| Env | Separate DBs | Prod data in wrangler dev default |
| Schema | Versioned migrations | Clickops only in dashboard |
| Backup | Periodic export tested restore | No export ever |
| Authz | Worker checks session before query | Public Worker + open SQL |

## Output Checklist

- [ ] D1 created per environment with IDs in config (not secrets git-leaked)
- [ ] Migrations in repo and applied
- [ ] Worker binding typed and deployed
- [ ] Parameterized queries only
- [ ] Backup/export path tested
- [ ] Authz around data access verified
- [ ] Limits/performance notes recorded
- [ ] Residual risk (single-region constraints etc.) noted

## Rules

- Owned CF accounts only.
- Treat prod exports as sensitive data.
- Prefer reversible migrations.
- Focus on **D1 basics**; bindings detail and Access/R2 are sibling skills.
