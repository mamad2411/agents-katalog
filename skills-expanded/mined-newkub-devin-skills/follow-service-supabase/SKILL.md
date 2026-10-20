---
name: follow-service-supabase
description: Use Supabase to build backends with PostgreSQL, Auth, Edge Functions, Realtime, CLI
argument-hint: "[scope]"
related:
  - follow-service-aws-sdk
  - follow-service-cloudflare
  - follow-secret-manager
  - follow-best-practice
  - learn
  - setup-cicd
  - delete
  - run-drizzle-studio
---

## Goal

Use Supabase to build backends with PostgreSQL, Auth, Edge Functions, and Realtime, and manage local development, migrations, and deploy via the Supabase CLI

## Scope

Used for:
- Building backends with PostgreSQL, Auth, Edge Functions, Realtime
- Database management with PostgreSQL
- Authentication and authorization
- Realtime subscriptions
- Edge functions with Deno
- Local development with the Supabase CLI
- Database migrations and type generation
- Secrets, storage, branches, and CI/CD integration

## Execute

### Workflows

> Goal: dispatch to the workflow matching the topic

- Setup: CLI install/login, `supabase init`, `link`, local stack, client init → `workflows/setup-supabase/SKILL.md`
- Config: env vars, `config.toml`, RLS policies, client options → `workflows/config-supabase/SKILL.md`
- Verify: URL/keys valid, auth healthy, queries respond → `workflows/verify-connection/SKILL.md`

### 1. Install And Authenticate

> Goal: Install and set up the Supabase CLI

Latest: `supabase` CLI `2.118.0`, `@supabase/supabase-js@2.117.2` (verified 2026-09-26)

1. Install the Supabase CLI with `bun add -D supabase` or Homebrew/Scoop/standalone binary
2. Check the version with `supabase --version`
3. Log in with `supabase login` to connect your Supabase account
4. Verify authentication with `supabase projects list`
5. Install Docker for local development

### 2. Initialize Project

> Goal: Create and set up the project

1. Initialize the project with `supabase init`
2. Create the `supabase/config.toml` config file
3. Link to the remote project with `supabase link --project-ref <project-id>`
4. Set the project ID and database URL
5. Check project status with `supabase status`

### 3. Local Development

> Goal: Develop and test in the local environment

1. Start the local stack with `supabase start`
2. Stop the local stack with `supabase stop`
3. Check status with `supabase status`
4. Access the local database via Studio at `http://127.0.0.1:54323`
5. Test migrations and seed data locally

### 4. Database Migrations

> Goal: Manage database migrations

1. Create a migration with `supabase migration new migration_name`
2. List migrations with `supabase migration list`
3. Apply migrations with `supabase migration up`
4. Roll back migrations with `supabase migration down`
5. Fetch remote migrations with `supabase migration fetch`

### 5. Database Operations

> Goal: Manage database operations

1. Pull the schema from remote with `supabase db pull`
2. Push the schema to remote with `supabase db push`
3. Reset the database with `supabase db reset`
4. Dump the database with `supabase db dump`
5. Diff schemas with `supabase db diff`

### 6. Type Generation

> Goal: Generate TypeScript types from the database schema

1. Generate types with `supabase gen types typescript --local`
2. Generate types for a specific schema with `--schema public --schema auth`
3. Output types to a file with `--output`
4. Integrate types with ORM or client libraries
5. Regenerate types whenever the schema changes

### 7. Edge Functions

> Goal: Manage Edge Functions

1. Create a function with `supabase functions new function_name`
2. List functions with `supabase functions list`
3. Serve locally with `supabase functions serve`
4. Deploy a function with `supabase functions deploy`
5. Delete a function with `supabase functions delete`

### 8. Secrets And Storage

> Goal: Manage secrets and storage

1. Set a secret with `supabase secrets set KEY=value`
2. List secrets with `supabase secrets list`
3. Delete a secret with `supabase secrets unset KEY`
4. List storage with `supabase storage ls`
5. Copy/move/remove files with `supabase storage cp/mv/rm`

### 9. Branches And Inspection

> Goal: Manage branches and inspect database health

1. Create a branch with `supabase branches create`
2. List/switch/pause/delete branches
3. Inspect bloat with `supabase inspect db bloat`
4. Inspect blocking and long-running queries
5. Generate a report with `supabase inspect report`

### 10. Configuration And API Reference

> Goal: Read configuration and API references

1. Read [references/supabase-cli.md](references/supabase-cli.md) for CLI commands
2. Read [references/supabase-config.md](references/supabase-config.md) for the configuration reference
3. Read [references/supabase-client-api.md](references/supabase-client-api.md) for the Client SDK API reference
4. Read [references/official-resources.md](references/official-resources.md) for official links and resources

## Rules

### 1. Configuration Management

- Use `supabase/config.toml` as the single source of truth
- Set `project_id` and `api_url` correctly
- Never commit sensitive data to version control
- Use environment-specific configs for dev/staging/prod
- Use `.env` files for local development

### 2. Migration Best Practices

- Create migrations for every schema change
- Use descriptive names for migrations
- Test migrations locally before deploy
- Never edit migrations already deployed
- Use `supabase db diff` to review changes

### 3. Type Safety

- Generate types automatically with `supabase gen types`
- Regenerate types whenever the schema changes
- Integrate types with ORM or client libraries
- Use strict type checking

### 4. Secret Security

- Never commit secrets to version control
- Use `supabase secrets set` instead of editing config
- Rotate secrets regularly
- Use environment-specific secrets

### 5. CI/CD Integration

- Use `SUPABASE_ACCESS_TOKEN` for authentication
- Use `supabase db push` in CI for migrations
- Use `supabase functions deploy` for functions
- Test before deploy with `supabase db diff`

- Use /follow-service-aws-sdk if needed
- Use /follow-service-cloudflare if needed
- Use /follow-secret-manager if needed
- Use /follow-best-practice if needed
- Use /learn-from-web if needed
- Use /setup-cicd if needed
- Use /run-drizzle-studio if needed


## Expected Outcome

- Supabase CLI installed and configured correctly
- Local development environment working
- Database migrations managed systematically
- TypeScript types generated automatically
- Edge functions deployed smoothly
- Secrets managed securely
- CI/CD integration working automatically
- A backend built with Supabase using PostgreSQL, Auth, and Realtime
