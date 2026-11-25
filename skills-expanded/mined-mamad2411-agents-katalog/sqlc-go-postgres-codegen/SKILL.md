---
name: sqlc-go-postgres-codegen
description: Generate typed Go database access code from SQL files and migrations using sqlc — one source of truth per query, no ORM runtime overhead.
category: devops
version: 1.0.0
tags: [go, postgres, sqlc, codegen, pgx]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Go backend with PostgreSQL, medium-complex queries (joins, CTEs, window functions).
- You want compile-time type safety for query results but don't want an ORM.
- You have up/down SQL migrations and hand-written query SQL.

## Steps

1. Install sqlc (`brew install sqlc` or via Go: `go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest`).
2. Create `server/sqlc.yaml`:
   ```yaml
   version: "2"
   sql:
     - engine: "postgresql"
       queries: "pkg/db/queries/"
       schema:  "migrations/"
       gen:
         go:
           package: "db"
           out: "pkg/db/generated"
           sql_package: "pgx/v5"
           emit_json_tags: true
           emit_empty_slices: true
   ```
3. Write SQL queries in `pkg/db/queries/<domain>.sql` with magic comments:
   ```sql
   -- name: GetWorkspaceBySlug :one
   SELECT * FROM workspaces WHERE slug = $1;

   -- name: ListIssuesByWorkspace :many
   SELECT * FROM issues WHERE workspace_id = $1 ORDER BY created_at DESC LIMIT $2;

   -- name: CreateWorkspace :one
   INSERT INTO workspaces (name, slug) VALUES ($1, $2) RETURNING *;
   ```
4. Add a Makefile target:
   ```makefile
   sqlc:
       cd server && sqlc generate
   ```
5. Run `make sqlc` after editing any `.sql` file. Generated code appears in `pkg/db/generated/` (models, queries, interfaces).
6. Consume generated code:
   ```go
   queries := db.New(pool)
   ws, err := queries.GetWorkspaceBySlug(ctx, "my-team")
   ```

## Example

Typical layout:

```
server/
  sqlc.yaml
  migrations/
    001_init.up.sql
    001_init.down.sql
  pkg/db/
    queries/
      workspace.sql
      issue.sql
    generated/          # gitignored or committed, your call
      models.go
      workspace.sql.go
      issue.sql.go
      db.go
```

## Caveats

- `pgx/v5` is the recommended driver; `database/sql` mode loses some Postgres types.
- Commit the generated code to the repo if you want `go build` to work without `sqlc generate` as a prerequisite; skip it if you run codegen in CI.
- sqlc reads the schema from migrations in order. Don't use `IF NOT EXISTS` or nondeterministic DDL — sqlc can't infer types if the schema is ambiguous.
