---

name: schema-change
description: Change a database schema in Gateweave Agents with a proper migration - the D1 database (users, sessions, workspaces, via Better Auth) or the per-workspace registry Durable Object (projects, repositories, agents, assets). Use when adding or altering tables, columns or indexes.
---

# Change a schema

Two databases, two owners. Pick the right one first.

| Data                                          | Database              | Schema file                                         | Package                      |
| --------------------------------------------- | --------------------- | --------------------------------------------------- | ---------------------------- |
| Users, sessions, workspaces, members, invites | D1                    | `apps/web/src/server/db/auth-schema.ts` (generated) | `@gateweave/agents-web`      |
| Projects, repositories, agents, assets        | Durable Object SQLite | `packages/registry/src/db/schema.ts`                | `@gateweave/agents-registry` |

Migrations are append-only. Never edit or delete a migration that has been merged; write a new
one that moves the schema forward.

## Registry (Durable Object)

1. Edit `packages/registry/src/db/schema.ts`. If the change shows in what the registry returns,
   update the entities in `packages/model` too.
2. Generate the migration:

   ```sh
   pnpm --filter @gateweave/agents-registry db:generate
   ```

   This writes `drizzle/NNNN_*.sql`, updates `drizzle/meta/` and regenerates
   `drizzle/migrations.js`. Commit all of them.
3. Read the generated SQL. SQLite cannot alter some columns in place, so Drizzle may rebuild the
   table; make sure existing rows survive. For what Drizzle cannot express, such as an FTS5
   table, make an empty migration with `db:generate --custom --name <name>` and write its SQL by
   hand, as `0040_memory_search.sql` does.
4. Migrations run in the `RegistryDO` constructor inside `blockConcurrencyWhile`, the first time
   each workspace wakes up after a deploy. They must be fast and must never fail on existing data.
5. Run `pnpm --filter @gateweave/agents-registry test`.

## D1 (Better Auth)

The D1 schema is generated from the Better Auth configuration
(`apps/web/src/server/auth/config.ts`). Don't edit `auth-schema.ts` by hand.

1. Change the Better Auth configuration, for example a plugin or `additionalFields`.
2. Regenerate the Drizzle schema, then the migration:

   ```sh
   pnpm --filter @gateweave/agents-web auth:schema
   pnpm --filter @gateweave/agents-web db:generate
   ```
3. Read the SQL in `apps/web/migrations/`, then apply it locally and run the app:

   ```sh
   pnpm --filter @gateweave/agents-web db:migrate:local
   ```
4. Deploys apply D1 migrations before the new code goes live (`apps/web/scripts/deploy.mjs`), for
   Gateweave Cloud and self-hosters alike. Old code still runs against the new schema until the
   deploy finishes, so say in the pull request whether it can.

## Verify

```sh
pnpm verify
```
