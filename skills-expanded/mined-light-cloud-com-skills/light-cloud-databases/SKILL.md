---
name: light-cloud-databases
description: Create and use Light Cloud databases (PostgreSQL or MySQL), connect them to an app through environment variables, look at tables, run SQL, check load, and change or delete a database. Use when the user wants a database for their app, asks what is in a database, wants to query or change data or the schema, or asks about environment variables or secrets on a Light Cloud app.
---

# Light Cloud databases and environment variables

Start as every Light Cloud task does: `whoami` for the workspace (`organisation_id`), then `get-workspace-overview` for its apps and databases. Never ask the user for an id.

## Create a database

1. `create-database` with a name. Default: PostgreSQL on the shared pool (tier `shared-dev`). Pass `engine: "mysql"` for MySQL, or a dedicated `tier` such as `db-f1-micro` when the user asks for one.
2. Provisioning takes a while: poll `get-database` until its status is ready.

Databases come with the paid plans; Free has none. A refusal names the plan that includes one and its price: tell the user both and get a yes before `choose-plan`.

A new app that needs a database from the start (WordPress, a SaaS starter): `search-templates` with `runs: "database"` finds templates that create the database and connect it for you.

## Connect it to an app

The app reads the connection string from an environment variable, usually `DATABASE_URL`. Write the code to read it from the environment, never inline.

- **Connector** (remote server): it never returns a connection string, so no password passes through the chat. Ask the user to copy it in the console, on the database's page under Credentials (pick the variant for their stack: Node.js, Python / psql or Prisma), and paste it as `DATABASE_URL` in the app's environment variables there. Don't ask them to paste it into the chat. When they say it is saved, redeploy with `deploy-environment`.
- **Local server**: `get-database-connection-string`, then `set-environment-variables` with it as `DATABASE_URL`, then `deploy-environment`. Don't print the value.
- **CLI**: `lc db url`, then `lc env vars set DATABASE_URL=... --redeploy`.

## Environment variables

- `get-environment-variables`: the names on an environment, values masked.
- `set-environment-variables`: merges. Keys not mentioned are kept; an empty string removes one.
- Running code sees a change only after `deploy-environment`.

Both take an `environment_id`: get it from `get-application` or `list-environments` (production unless the user names another). If the user gives you a secret, put it straight into `set-environment-variables` and never repeat it or write it to a file or commit.

## Look and query (PostgreSQL)

- `get-database-schema`: schemas, tables, columns and row counts. Start here before writing SQL.
- `query-database`: read-only SQL (SELECT, EXPLAIN). It refuses anything that changes data.
- `execute-database-sql`: INSERT, UPDATE, DELETE, CREATE, ALTER, DROP. Show the user the SQL and get a yes before anything that deletes or overwrites data.
- `get-database-metrics`: connections, CPU, memory, storage and query load over `1h`, `6h`, `24h` or `7d`.

Answer with what the rows say, in plain words or a small table; don't paste raw JSON.

## Change or remove

- `update-database`: name, tier, region, storage, high availability. A tier or storage change can take a few minutes.
- `move-database`: into a folder.
- `rotate-database-password`: apps using the old password lose access until `DATABASE_URL` is updated (connector: the user copies the new string in the console; local server: `get-database-connection-string` again). Say so before rotating.
- `delete-database`: deletes the database and all its data, with no undo. Name the database and get a clear yes first.
