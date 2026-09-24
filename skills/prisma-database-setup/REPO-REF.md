# Repo Referensi: prisma/skills

Repo: https://github.com/prisma/skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/prisma_skills
API: curl "localhost:27126/repos/readme?name=prisma_skills"
Dibuat: 2026-09-16

## Cuplikan README
# prisma/skills

Source: https://github.com/prisma/skills
Fetched: 2026-09-16

## README
# Prisma Skills

A collection of skills for AI coding agents working with Prisma ORM. Skills are packaged instructions that extend agent capabilities for database development.

Skills follow the [Agent Skills](https://agentskills.io/) format and are compatible with `npx skills add`.

## Available Skills

### prisma-cli

Complete reference for current Prisma ORM CLI commands. For Prisma Compute app deployment, use `prisma-compute`.

**Use when:**
- Running Prisma ORM/database commands
- Setting up new projects (`prisma init`)
- Managing migrations and database schema
- Generating Prisma Client

**Commands covered:**
- `init`, `generate`, `dev` (local Prisma Postgres)
- `migrate dev`, `migrate deploy`, `migrate reset`
- `db push`, `db pull`, `db seed`, `db execute`
- `studio`, `mcp`

---

### prisma-upgrade-v7

Step-by-step migration guide from Prisma v6 to v7, covering all breaking changes.

**Use when:**
- Upgrading existing projects to Prisma 7
- Troubleshooting v7 compatibility issues
- Understanding what changed in v7

**Topics covered:**
- ESM-first module configuration plus CommonJS fallback
- Driver adapter requirements
- New `prisma.config.ts` file
- Manual environment variable loading
- Generated client entrypoints (`client`, `browser`, `models`, `enums`)
- `Prisma.validator` to `satisfies` migration
- Removed features (middleware, metrics, CLI flags)
- Special handling for Accelerate users

---

### prisma-mongodb-upgrade

Decision and migration guide for MongoDB projects on Prisma v6, which have no path to Prisma 7.

**Use when:**
- A MongoDB project asks about upgrading Prisma versions
- Evaluating a move from Prisma v6 to Prisma Next
- Preventing an impossible "upgrade MongoDB to v7" plan

**Topics covered:**
- The version landscape (v6 terminal for MongoDB; v7 has no connector; Prisma Next is the successor path)
- Stay-on-v6 vs migrate-now decision table with no-go signals
- Schema/contract, client API, and migrations mapping between v6 and Prisma Next
- No-data-moves cutover verification checklist

---

### prisma-client-api

Comprehensive Prisma Client API reference.

**Use when:**
- Writing Prisma Client queries
- Understanding query options (select, include, where)
- Working with transactions
- Using raw SQL queries

**Topics covered:**
- PrismaClient constructor and configuration
- CRUD operations (findMany, create, update, delete)
- Query options (se
