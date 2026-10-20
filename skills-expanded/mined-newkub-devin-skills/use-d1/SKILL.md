---
name: follow-service-cloudflare-use-d1
description: Use Cloudflare D1 — schema migrations, prepared queries, batch, transactions
argument-hint: "[db-name]"
related:
  - follow-service-cloudflare
  - run-test
  - resolve-errors
---

## Goal

Use Cloudflare D1 fully — create db, migrations (local/remote), queries, batch, and transactions via the `env.DB` binding

## Scope

Use when a Worker/Pages needs a SQL database — migration command details live in `references/d1-migrations.md`; binding config → `config-bindings`

## Execute

### 1. Provision And Bind

1. `wrangler d1 create <NAME>` — keep the `database_id`
2. Bind in `wrangler.jsonc`: `d1_databases: [{ binding: "DB", database_name, database_id }]`
3. `wrangler types` regenerate `Env`

### 2. Migrations

> Goal: schema versions stable both locally and remotely

1. Place `.sql` files in `migrations/` in order (`0001_init.sql`)
2. Apply local: `wrangler d1 migrations apply DB --local`; remote: `--remote`
3. Check: `wrangler d1 migrations list DB` — details in `references/d1-migrations.md`
4. Never edit an applied migration — always add a new file

### 3. Query Patterns

> Goal: prepared statements + batch + tx

```ts
// prepared + bind — never string concat
const { results } = await env.DB
  .prepare('SELECT * FROM todos WHERE done = ?1')
  .bind(0)
  .all()

await env.DB.prepare('INSERT INTO todos (title) VALUES (?1)').bind(title).run()

// batch — multiple statements atomic
await env.DB.batch([stmt1, stmt2, stmt3])
```

- Pick `.all()` / `.first()` / `.run()` / `.raw()` according to the shape
- `withSession`/`bookmark` for read-replication consistency (check the latest docs)

### 4. Verify

1. `wrangler dev` and run real queries through local D1
2. `/run-test`; fail → `/resolve-errors` max 3 rounds

## Rules

- Parameterized queries only — never interpolate
- Apply remote migrations before deploying code that uses the new schema (deploy order)
- `env.DB` is missing in `.local` dev when the binding is absent — check the `wrangler types` output

## Expected Outcome

- D1 bound + migrations applied on both local and remote
- Queries safe via prepared+bind, batch used correctly
