# Database Setup

## Purpose
Sets up PostgreSQL database per `*-grpc` service using Prisma and the project generator.

## Role
Backend Developer

## Phase
Development (when new `*-grpc` service created)

## Triggered By
`server-scaffolding` complete for a new `*-grpc` service.

## Inputs
- Scaffolded `*-grpc` service

## Rule
One database per `*-grpc` service — NO sharing between services.

## Process
1. Run generator for database setup:
   ```
   bun turbo gen → database
   ```
   Creates: `prisma/schema.prisma`, PgAdapter wiring, Helm chart updates.
2. Configure `VaultPgAdapter` in `app.ts` for credentials: use `VaultPgAdapter.fromEnv()` — never hardcode credentials.
3. Set up local database in `docker-compose.yml`: postgres service with correct port, database name, credentials.
4. Create initial migration: `bunx prisma migrate dev --name init`.
5. Verify: `bun turbo gen:prisma` generates Prisma client successfully.

Local dev: `DATABASE_URL` in `.env.local` → local postgres.
Deployed: `DATABASE_URL` from Vault → injected at runtime.

## Outputs
Configured Prisma schema, local docker-compose postgres, initial migration.

## Quality Gates
- [ ] Generator used (not manual Prisma setup)
- [ ] VaultPgAdapter configured (not hardcoded credentials)
- [ ] Local docker-compose postgres configured
- [ ] Initial migration created successfully

## References
- `.claude/skills/backend-developer/server-scaffolding/SKILL.md`
- `.claude/skills/backend-developer/database-migration/SKILL.md`
- `.claude/skills/backend-developer/per-service-infra-setup/SKILL.md`
