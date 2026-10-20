---
name: prisma-troubleshooting
description: Fix Prisma failures, migration drift, shadow database errors, baselining, failed migrations, connection pool timeouts, and pooling with PgBouncer or serverless. Use when prisma migrate or Prisma Client errors out.
---

# Prisma Troubleshooting

Start with the facts: `npx prisma migrate status` (history vs database) and
`npx prisma validate` (schema sanity). Most fixes below flow from those two.

## Drift detected

Meaning: the database's actual structure no longer matches the migration
history (someone ran manual SQL, or another tool touched the DB).

- Dev database, data disposable:
  `npx prisma migrate reset` (drops, replays all migrations, runs seed).
- Keep the manual change: capture it as a migration instead of fighting it:

```bash
npx prisma migrate diff \
  --from-schema-datamodel prisma/schema.prisma \
  --to-schema-datasource prisma/schema.prisma \
  --script > prisma/migrations/<timestamp>_capture_drift/migration.sql
npx prisma migrate resolve --applied <timestamp>_capture_drift
```

- Never "fix" drift by editing already-applied migration files; checksums
  will mismatch on every other environment.

## Shadow database errors

`migrate dev` creates a temporary shadow database to detect drift and replay
history. Failures:

- `P3014` (cannot create shadow DB): the dev user lacks `CREATEDB` rights.
  Grant it (`ALTER USER dev CREATEDB;`) or, on cloud databases where you
  cannot, provision a second database and point
  `shadowDatabaseUrl = env("SHADOW_DATABASE_URL")` in the datasource block.
- Shadow DB is a DEV-time tool only; `migrate deploy` never needs it, so CI
  and prod need no CREATEDB rights.
- Never point `shadowDatabaseUrl` at a database with data; it gets wiped.

## Baselining an existing database

Adopting migrations on a DB that already has tables (from `db push` or a
pre-Prisma life):

```bash
mkdir -p prisma/migrations/0_init
npx prisma migrate diff --from-empty \
  --to-schema-datamodel prisma/schema.prisma --script \
  > prisma/migrations/0_init/migration.sql
npx prisma migrate resolve --applied 0_init
```

New environments replay `0_init` for real; the existing one records it as
already applied.

## Failed migration mid-apply

`migrate status` shows a failed migration blocking everything.

```bash
npx prisma migrate resolve --rolled-back <name>   # after you manually undid its partial effects
# fix the SQL, then:
npx prisma migrate deploy
```

Or `--applied <name>` if the migration actually completed but recording
failed. On databases without transactional DDL for the statements involved,
inspect what half-applied before choosing.

## Connection pool timeouts (P2024)

`Timed out fetching a new connection from the connection pool.`

1. Too many client instances (serverless spinning one pool per invocation,
   or dev hot-reload leaking clients). Fix: singleton client; in serverless
   set `connection_limit=1` in the URL and use an external pooler.
2. Long transactions or unawaited queries hogging connections; find the slow
   query, keep interactive transactions short.
3. Pool simply too small: `?connection_limit=20&pool_timeout=10` on the URL.
   Default pool size is roughly `num_cpus * 2 + 1`; total across ALL app
   instances must stay under the database's `max_connections`.

## PgBouncer / external poolers

- Transaction-mode PgBouncer: add `?pgbouncer=true` to the Prisma URL
  (disables prepared statements that break in transaction mode).
- Migrations need a DIRECT connection, not the pooler: keep two URLs
  (`DATABASE_URL` pooled for the app via `url`, direct for migrate via
  `directUrl` in the datasource block).
- Prisma Postgres has pooling built in; the `pgbouncer=true` ritual is for
  self-managed setups (see `prisma-postgres`).

## Quick hits

- `P1001 Can't reach database server`: wrong host/port, DB asleep (serverless
  Postgres cold), or firewall. Test with `psql` before blaming Prisma.
- Client types stale after schema change: `npx prisma generate` (and restart
  the TS server).
- Engine/binary platform mismatch in Docker or Lambda: set
  `binaryTargets = ["native", "linux-musl-openssl-3.0.x"]` (match your image)
  in the generator block.
- When behavior contradicts your memory of Prisma, use the MCP docs-search
  tool; the ORM moves fast and flags/attributes change names.
