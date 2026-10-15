---
name: db-migrate
description: Create and apply a Prisma migration safely against the remote (tunneled) PostgreSQL. Use for schema changes - "create a migration", "apply migrations", "add a column/table".
---

# DB migrate

The database is remote; `DATABASE_URL` points at the SSH tunnel's local port (5433). All
commands are `bun --cwd=apps/api run …`.

1. Confirm the tunnel is up (`bunx prisma migrate status` from `apps/api`). If it isn't, ask the
   user to run `bun run db:tunnel` in a separate terminal - don't start it yourself.
2. Edit the schema - split by domain under `apps/api/prisma/schema/*.prisma`.
3. `db:migrate` - creates the migration SQL only (`--create-only`), never applies.
4. Read the generated SQL and confirm it matches intent. Prisma turns renames into drop + add -
   hand-edit to `ALTER` when data must survive.
5. `db:migrate:apply`, then `db:generate`.

Never run `db:reset` without explicit user confirmation - it wipes the remote database.
