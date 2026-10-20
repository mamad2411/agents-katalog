---
name: "tdsk-database"
description: "Knowledge base for the database ORM & migrations repo"
tags: ["drizzle", "postgresql", "orm", "migrations", "database", "neon", "quotas", "subscriptions", "agents", "domains", "invitations", "sandboxes", "skills", "schedules"]
---
# Database Repo Skill

## Overview

- **ORM layer** for Threaded Stack using **Drizzle ORM** + **PostgreSQL (Neon.com)**
- 30 Drizzle-managed tables + 2 external (Neon Auth `users`, Caddy `certificates`), 9 junction tables
- 22 service classes with CRUD, domain model conversion, and polymorphic "Exclusive Arc" relationships
- **pgvector** enabled for the `memories` semantic store (`vector(1536)` embedding column)
- Database singleton via `pg.Pool`; all services auto-initialized on first `database()` call
- **Path Alias:** `@TDB/*`

## Directory Structure

```
repos/database/
├── configs/               # db.config.ts, drizzle.config.ts, vitest.config.ts, aliases.ts, biome.json
├── drizzle/               # Generated migrations (meta/ + *.sql)
├── scripts/               # seed.ts, purge.ts, script.ts, addToProcess.ts, addProviderSecretFk.ts
├── src/
│   ├── index.ts           # Main export (types + database)
│   ├── database.ts        # Database singleton factory + disconnectDatabase
│   ├── constants/         # DefDBProto constant
│   ├── schemas/           # 31 Drizzle table schemas (29 managed + junction tables)
│   ├── seeds/             # ids.seed.ts, fullorg.ts
│   ├── services/          # 21 service classes + base + tests
│   ├── types/             # db.types.ts, schema.types.ts, helper.types.ts, service.types.ts
│   └── utils/             # crypto.ts, logger.ts, database/, error/, schema/
├── index.ts               # Root re-export
├── package.json
└── tsconfig.json
```

## Key Files

| File | Purpose |
|------|---------|
| `src/database.ts` | Singleton database factory with Pool management + `disconnectDatabase()` |
| `src/schemas/schemas.ts` | Barrel for 25 Drizzle-managed tables (excludes users, certificates) |
| `src/schemas/index.ts` | Full barrel: schemas.ts + users + certificates |
| `src/services/base.ts` | `Base<TTable, S, I, M>` class with CRUD, `model()`, `with()` |
| `src/services/index.ts` | 21 named service exports |
| `src/types/schema.types.ts` | TDB*Select/Insert types via `$inferSelect`/`$inferInsert` |
| `src/types/db.types.ts` | TDatabase (NodePgDatabase + services), TDBConfig, TDBServices |
| `src/utils/crypto.ts` | `encryptSecret()` using domain's HKDF + AES-256-GCM |
| `configs/db.config.ts` | Connection config from env vars |

## Schema Overview

### Table Reference

**25 Drizzle-managed tables** + **2 external** (read-only):

| Table (variable) | Key Fields | Notes |
|---|---|---|
| `organizations` (`orgs`) | name, description, config (jsonb `TOrgConfig`), ownerId (FK users) | Relations: owner, users (via roles), quotas, assets, agents, secrets, projects, providers, invitations |
| `users` (Neon Auth, schema `neon_auth`) | name, email, image, role, banned, emailVerified | External, not in Drizzle migrations |
| `roles` | name, type, userId, orgId, projectId | `orgId XOR projectId` arc; unique on `(userId, orgId)` and `(userId, projectId)` |
| `invitations` | email, userId, roleType, orgId, invitedBy, token (unique), status (pending/accepted/expired/revoked), expiresAt | Indexes: orgId, email, status; 3 user relations via `relationName` |
| `agents` | name, description, orgId, systemPrompt, model, maxTokens, tools (jsonb), envVars (jsonb), environment (jsonb), active | Relations: org, secrets, threads, projects/providers/skills via junctions |
| `skills` | name, description, instructions, triggerKeywords (jsonb), tools (jsonb), alwaysActive, orgId | Org-scoped AI skill definitions linked to agents via agentSkills |
| `schedules` | agentId, orgId, cronExpression, prompt, enabled, lastRunAt, nextRunAt, threadId, createThread, maxConsecutiveErrors, consecutiveErrors | Indexes: orgId, agentId, `(enabled, nextRunAt)` |
| `threads` | name, meta, public, parentThreadId (self-ref), branchMessageId, providerId, agentId, orgId, projectId, userId, sandboxId, ptyBuffer (bytea) | Supports branching via parentThreadId + branchMessageId |
| `messages` | meta (jsonb), type, content (jsonb), orgId, projectId, threadId | |
| `projects` | meta, gitUrl, name, description, branch (default 'main'), orgId | Unique: `(orgId, name)` |
| `endpoints` | name, headers (jsonb), options (jsonb), path, public, method, type, projectId | Unique: `(projectId, path, method)` |
| `functions` | name, description, content, branch, defaultArgs (jsonb), dependencies (jsonb), inputSchema (jsonb), language, endpointId, projectId | Indexes: projectId, endpointId |
| `providers` | name, type (EProvider), brand (TProviderBrand), options/headers/bodyParams (jsonb), secretId, orgId | Org-scoped only (not an exclusive arc) |
| `secrets` | name, description, hashKey, encryptedValue, orgId, projectId, providerId, agentId | 4-way arc + combo (see Exclusive Arc); AES-256-GCM encryption |
| `apiKeys` (`api_keys`) | name, expiresAt, lastUsedAt, scopes (text default 'read'), active, rateLimit, keyHash (unique), keyPrefix, orgId, projectId, userId | CHECK: allows both NULL, orgId XOR projectId |
| `assets` | url, meta (jsonb), content (jsonb), name, type, providerId (not in arc), orgId, userId, threadId, projectId, messageId | 5-way strict arc: exactly one of orgId/projectId/userId/threadId/messageId |
| `domains` | domain (unique), verifiedAt, sslExpiresAt, sslPrivateKey, sslCertificate, verified, sslEnabled, orgId, projectId | 2-way arc: orgId XOR projectId; unique: `(orgId, domain)` |
| `quotas` | orgId, period, projects, compute, threads, messages, endpoints, secrets (all integer counters) | Unique: `(orgId, period)` |
| `subscriptions` | userId (unique), tier (default 'free'), status, stripeCustomerId, stripeSubscriptionId, stripePriceId, currentPeriodStart/End, cancelAtPeriodEnd, seats | One subscription per user |
| `sandboxes` | name, orgId, userId, config (jsonb `TKubeSandboxConfig`), builtIn | Custom nanoid with lowercase alphabet for SSH compatibility; indexes: orgId, `(orgId, userId)` |
| `invoices` | userId, stripeInvoiceId (unique), amount, currency, status, invoiceUrl, period | Stripe invoice tracking |
| `memories` | orgId, agentId, kind (fact/insight/reflection/compaction/roadmap), text, importance (1-10), embedding (`vector(1536)`, nullable), lastAccessedAt | pgvector semantic memory store; org+agent-scoped; roadmap persisted as a singleton `roadmap`-kind row |
| `certificates` (`caddy_certmagic_objects`) | Composite PK `(parent, name)`, isFile, value (bytea), modified | External: Caddy certmagic storage plugin |

### Junction Tables

| Table | Links | Key Fields | Notes |
|---|---|---|---|
| `agentProjects` | agents <-> projects | agentId, projectId, alias, model, maxTokens, systemPrompt, tools, functionIds, envVars, environment, enabled | Per-project overrides: NULL inherits from agent, non-null overrides |
| `agentFunctions` | agents <-> functions | agentId, functionId | Simple many-to-many |
| `agentProviders` | agents <-> providers | agentId, providerId, priority (default 0) | Index: `(agentId, priority)` |
| `agentSkills` | agents <-> skills | agentId, skillId | Unique: `(agentId, skillId)` |
| `sandboxProjects` | sandboxes <-> projects | sandboxId, projectId, alias, enabled, config (jsonb `Partial<TKubeSandboxConfig>`) | Per-project config deep-merged (project wins) |
| `sandboxProviders` | sandboxes <-> providers | sandboxId, providerId, model, priority (default 0) | onDelete restrict for providerId |
| `sandboxSkills` | sandboxes <-> skills | sandboxId, skillId, projectId? | Optional projectId scope, conditional unique indexes |
| `projectProviders` | projects <-> providers (git) | projectId, providerId, priority | Git providers first-class; unique (projectId, providerId) |
| `sandboxProjectProviders` | sandboxes <-> projects <-> providers | sandboxId, projectId, providerId, branch? | 3-way junction for per-project git provider assignment |

## Architecture

The database repo uses a 3-layer architecture: **Consumer repos** (backend, proxy) import the `database()` singleton which provides 21 auto-initialized services. Each **service** extends `Base<TTable, S, I, M>` with CRUD + domain model conversion. Services operate on **Drizzle schemas** (27 table definitions + relations) backed by PostgreSQL via Neon.com.

The `database()` factory is a singleton that creates a `pg.Pool`, initializes a Drizzle instance, and attaches all 21 services. Call `disconnectDatabase()` to close the pool and reset. Consumers access services via `db.services.<name>`.

Two-level schema barrel: `schemas/schemas.ts` exports 25 Drizzle-managed tables (used for migrations), `schemas/index.ts` adds the 2 external read-only tables.

## Services (22 total)

### Base Service Class

`Base<TTable, S, I, M>` provides generic CRUD (`create`, `get`, `by`, `list`, `update`, `upsert`, `delete`) that returns `{ data, error }` -- never throws. Subclasses override `model()` for domain model conversion and `with()` for default relation loading. The `list()` method supports `{ where, limit, offset, orderBy, with }` options.

### Service Reference

| Service | Schema | Model | Notable Methods |
|---|---|---|---|
| `org` | `orgs` | `Organization` | base CRUD |
| `role` | `roles` | `Role` | getOrgRole, getProjectRole, getUserRoles, getOrgMembers, getOrgOwner, isOrgMember, updateOrgRole, removeFromOrg, getUserOrgs, getUserProjects |
| `user` | `users` | `User` | byEmail, getByIds |
| `asset` | `assets` | `Asset` | listByThread, listByMessage |
| `quota` | `quotas` | `Quota` | getUsage, findByOrgAndPeriod, increment (atomic SQL), decrement (atomic, floor 0), initializePeriod |
| `agent` | `agents` | `Agent` | Auto-loads relations via with(); junction management (add/remove project/function/provider); setProviders; sanitizes secrets by default |
| `apiKey` | `apiKeys` | -- | base CRUD |
| `secret` | `secrets` | -- | base CRUD |
| `thread` | `threads` | `Thread` | listByAgent, listByUser, getWithMessages, branchThread (transaction: copies thread + messages to branchpoint) |
| `project` | `projects` | -- | base CRUD |
| `message` | `messages` | `Message` | listByThread, createBatch, listRecentByAgent |
| `endpoint` | `endpoints` | -- | base CRUD |
| `function` | `functions` | `Function` | Auto-loads agents, listByAgent, setAgents, addAgent, removeAgent |
| `provider` | `providers` | -- | base CRUD |
| `domain` | `domains` | `Domain` | find (cert check), validate, verified, enableSSL, disableSSL, owner |
| `invitation` | `invitations` | `Invitation` | getByToken, getByEmailAndOrg, getPendingByOrg, getAllByOrg, accept, revoke, markExpired, isValid |
| `subscription` | `subscriptions` | `Subscription` | findByUser, findByStripeId, upsertByUser |
| `sandbox` | `sandboxes` | `Sandbox` | listByOrg, addProject, removeProject, upsertProjectConfig, getProjectConfig, addProvider, removeProvider, setProviders (atomic replace, transactional) |
| `skill` | `skills` | `Skill` | addAgent (onConflictDoNothing), listForAgent, removeAgent |
| `schedule` | `schedules` | `Schedule` | listDue (enabled + nextRunAt <= now), markRun (resets errors), incrementErrors (auto-disables at max) |
| `invoice` | `invoices` | `Invoice` | findByUserId, upsertByStripeId |
| `memory` | `memories` | `Memory` | searchScored (scored retrieval: recency `0.995^hours` x importance x relevance, where relevance = cosine when embeddings present, else `ts_rank` lexical, else 1), getRoadmap, upsertRoadmap |

**Agent service** is the most complex (~578 lines). Auto-loads secrets, projects, functions, providers, and skills. Sorts providers by priority. `create`/`update`/`upsert` handle junction tables automatically. Pass `opts.sanitize = false` to skip secret sanitization.

**Sandbox service** auto-loads projects (via sandboxProjects), providers (via sandboxProviders), and skills (via sandboxSkills). The `model()` method maps junction data to `SandboxModel` with `projects`, `projectConfigs`, `providerLinks`, and `skillLinks` arrays. Additional methods: `addSkill`, `removeSkill`, `listSkillsForSandbox`.

**Quota service** uses atomic SQL: `increment` does `INSERT ... ON CONFLICT DO UPDATE` with `column + amount`; `decrement` uses `GREATEST(column - amount, 0)`.

**Invitation service** status flow: `pending` -> `accepted` | `expired` | `revoked`. Methods `accept`/`revoke` validate `status=pending` first. `markExpired()` bulk-updates past-expiration pending invites.

## Exclusive Arc Pattern

Polymorphic relationships ensuring a record belongs to exactly ONE parent entity, enforced via CHECK constraints.

| Table | Arc Columns | Style |
|---|---|---|
| `secrets` | orgId, projectId, providerId, agentId | 4-way + combo (orgId+providerId allowed together) |
| `assets` | orgId, projectId, userId, threadId, messageId | 5-way strict (exactly one, using `::int` cast sum = 1) |
| `roles` | orgId, projectId | 2-way strict (exactly one) |
| `domains` | orgId, projectId | 2-way strict (exactly one) |

Tables NOT using exclusive arc: `providers` (org-scoped only), `apiKeys` (CHECK allows both NULL or orgId XOR projectId), `agents` (org-scoped only, providers via junction).

## Key Patterns

- **Base schema**: All tables use `base` fields (uuid PK `id`, `createdAt`, `updatedAt` timestamps) from `src/utils/schema/base.ts`.
- **Service inheritance**: Minimal services extend `Base` with constructor + `model()` override. Complex services additionally override `with()`, `get()`, `list()`, and add junction management methods.
- **Type inference**: `schema.types.ts` uses `$inferSelect`/`$inferInsert` with a `TInferDates` wrapper that makes date fields accept `string | Date`. Special types like `TDBApiKeySelect` extend this for additional date fields.
- **Schema barrel**: Two-level separation -- `schemas.ts` (25 Drizzle-managed, used for migrations) vs `index.ts` (full export including 2 external tables).
- **Cascade deletion**: `onDelete: 'cascade'` for hard deletes, `'set null'` for soft unlinks, `'restrict'` to prevent parent deletion.

## Commands

```bash
pnpm push                # Push schema to DB (INTERACTIVE -- requires manual confirmation)
pnpm generate            # Generate migration files from schema changes
pnpm migrate             # Apply pending migrations
pnpm introspect          # Introspect existing DB schema
pnpm studio              # Launch Drizzle Studio (visual DB browser)
pnpm check               # Check migration consistency
pnpm drop                # Drop a migration
pnpm export              # Export schema as SQL
pnpm dup                 # drizzle-kit up (update migration format)
pnpm dk <command>        # Direct drizzle-kit access
pnpm seed                # Run database seeder
pnpm purge               # Purge database data
pnpm script              # Run utility scripts with aliases
pnpm types               # TypeScript type checking (tsc --noEmit)
pnpm fleet:off           # Stand the autonomous agent fleet DOWN (see below)
pnpm fleet:on            # Bring the fleet back UP
pnpm fleet:status        # Print current fleet state (read-only)
```

> **Note**: `pnpm push` runs `drizzle-kit push` which is interactive. Claude cannot run this automatically.
> **drizzle-kit push limitation**: Cannot modify existing CHECK constraints -- must drop+recreate via manual SQL.

### Fleet Toggle (`scripts/toggleFleet.ts`)

Stands the autonomous AI agent fleet **down or up** in one command, without touching the platform (backend/proxy/caddy/egress/admin/threads keep serving). Preferred entry point is the CLI wrapper `tdsk fleet on | off | status`; the underlying implementation is this script (`pnpm fleet:on | fleet:off | fleet:status`, or `tsx scripts/toggleFleet.ts --on|--off|--status`).

- **What it flips** (prod only): the 6 always-on residents (CEO/CMO/CTO-lead/3 engineers — clears/sets each body sandbox's `config.resident` flag + deletes/lets-boot the pods), the 5 steward/CTO-board schedules (`enabled` flag), and 2 GitHub workflows (`system-monitor`, `update-behind-prs`).
- **Self-contained**: reads the prod DB URL from the `tdsk-db-cfg` k8s secret (context `tdsk`, ns `tdsk-production`) via kubectl — no credential export. Pure `pg` + `node:child_process`.
- **Deploy caveat**: "off" is live DB/workflow state, NOT a seed change. A full `tdsk release` / merge-to-main deploy re-runs the reconcile (`reconcileResidentActivations` + `reconcileSchedules`) and turns the fleet back **on**. Re-run `fleet:off` after any deploy while the fleet should stay down.

## Environment Variables

Required in `deploy/values.*.yml`:

| Variable | Purpose |
|----------|---------|
| `TDSK_DB_URL` | Full connection URL (preferred) |
| `TDSK_DB_NAME` | Database name |
| `TDSK_DB_USER` / `TDSK_DB_PASS` | Credentials |
| `TDSK_DB_PROTO` | Protocol (postgres/postgresql) |
| `TDSK_DB_DIALECT` / `TDSK_DB_TYPE` | Drizzle dialect |
| `TDSK_DB_LOG_LEVEL` / `TDSK_DB_LOG_LABEL` | Optional logging |

## Integration Points

Main exports from `@tdsk/database` (`src/index.ts`): all TypeScript types + `database()` / `disconnectDatabase()`. Schemas and services are NOT directly exported -- they are accessed via the `database()` singleton's `.services` property.
