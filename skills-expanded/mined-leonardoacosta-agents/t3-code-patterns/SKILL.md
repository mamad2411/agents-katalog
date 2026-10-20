---
name: t3-code-patterns
description: >
  Project-specific code patterns for T3 Turbo monorepo development. Use when
  writing or reviewing code in any T3 fleet repo (acme, storefront,
  operations, backoffice, portal, legacy) and you touch: DB imports / raw SQL,
  the Drizzle schema or a migration, placement of a one-off script,
  null-narrowing a query result, deciding which package owns a type
  (db→entities, api→DTOs, app→UI), a Stripe SDK call, a Terraform file, an
  ESLint rule/whitelist decorator, Better Auth rate-limit policy, or when
  creating a new service / router / script and you need the search-first
  placement rules. Triggers on: T3 Turbo, drizzle migration, db:push (never),
  POSTGRES_URL, snake_case column, ctx.db.query, RouterOutputs, DomainError,
  tenantProtectedProcedure, ROUTER_DB_ALLOWLIST, packages/db, packages/api,
  @theme-exception, better-auth, rate limit, VERCEL_ENV. Do NOT use for Bun +
  Effect repositories; that stack is paradigm-divergent.
user-invocable: false
disable-model-invocation: false
category: Framework
level: framework
engineer: ui-engineer
gate: "pnpm tsc --noEmit"
bundles:
  - skill: drizzle
    category: DB
  - skill: vercel
    category: Deploy
  - skill: trpc-patterns
    category: API
  - skill: react-dev
    category: UI
  - skill: t3-testing-patterns
    category: E2E
allowed-tools: Read, Glob, Grep, Bash
---


<!-- discovery detail (moved out of frontmatter description for length): raw SQL means
     camelCase→snake_case columns and POSTGRES_URL not DATABASE_URL; migrations means
     drizzle-kit generate, NEVER db:push; Better Auth rate-limit policy means
     deployment-aware preview protection and isolated E2E capacity. -->
# T3 Code Patterns

> Project-specific code patterns for T3 Turbo monorepo development.
> For core rules: `rules/CORE.md` | For deploy: `deploy-and-env` skill

## E2E Testing

Canonical manual E2E uses exact root key `test:e2e` and deployed HTTPS non-production mode only.
Local `test:e2e:local` and CI modes are loopback-only. A private capability binds mode, operation,
query/fragment-free URL, target, deployment, run, database, and service identities. Collection
requires explicit `--list`/no-test-body operation and exposes exact Chromium only, without setup or
web-server dependency graphs. Reject every other pairing; missing, mismatched, insecure,
non-loopback HTTP, or production input fails before collection.

Load `t3-testing-patterns/references/e2e-command-target-lifecycle.md` for commands and target
classes, and `t3-testing-patterns/references/e2e-topology-evidence.md` for workers, shards, reports,
and flake classification.

## Database

### Import Pattern

```typescript
import { db } from "@{workspace}/db/client";  // ✅
ctx.db.query  // ❌ Causes TS recursion
```

### Raw SQL Column Names

Drizzle uses camelCase in TypeScript but generates **snake_case** columns in Postgres. When writing
raw SQL (psql, migrations, ad-hoc queries), ALWAYS use snake_case.

**Rule:** `eventId` → `event_id`, `eventSeriesId` → `event_series_id`, `createdAt` → `created_at`,
etc. When unsure, check the schema: `grep 'text("\|varchar("' packages/db/src/schemas/`. Full
before/after SQL example: `references/database.md` § Raw SQL Column Names.

### Raw SQL Connection

The DB connection env var is `POSTGRES_URL`, NOT `DATABASE_URL`. Using `DATABASE_URL` silently
resolves to empty, causing psql to attempt a local socket connection and fail. All T3 projects use
`POSTGRES_URL` (Neon convention, set in `.env`).

```bash
# ✅ Correct — load .env (--overload so repo .env beats shell/~/.env) and use POSTGRES_URL
dotenvx run --overload --quiet -f .env -- bash -c 'psql "$POSTGRES_URL" -c "SELECT 1"'
```

Full right-vs-wrong command pair: `references/database.md` § Raw SQL Connection.

### Schema Path

The Drizzle schema directory varies by project. Do NOT guess — check first:

```bash
# Find the actual schema directory
ls packages/db/src/schema/ 2>/dev/null || ls packages/db/src/schemas/ 2>/dev/null
```

| Project | Schema Path |
|---------|-------------|
| acme, legacy | `packages/db/src/schemas/` (plural dir) |
| operations | `packages/db/src/schema.ts` (single flat file) |
| backoffice | `packages/db/src/*-schema.ts` (multiple flat files in src/) |
| storefront, portal | `packages/db/src/schema/` (singular dir) |
| cl, cw, co | `packages/db/src/schemas/` (plural dir) |

**Always verify** before assuming — run `ls packages/db/src/` to confirm structure.

### Migrations

> PreToolUse hook blocks creating new `.sql` files in `drizzle/` — enforced automatically.

**Migration-based schema changes ONLY. NEVER `db:push` / `drizzle-kit push`.** Edit `schema.ts` →
`db:generate` (writes a reviewed, ordered `.sql` migration) → **commit the migration** → the
**deploy** applies it via `db:migrate` (the deploy is the single writer to any live/shared DB).
Engineers never apply schema directly to a live DB during a task. To test a migration locally, run
`db:migrate` against a throwaway/local DB — never `db:push` against shared/prod.

| Action | Command |
|--------|---------|
| Schema change | Edit Drizzle schema → `pnpm drizzle-kit generate` → commit `.sql` |
| Apply (deploy / local test) | `pnpm db:migrate` (ordered file replay) |
| Data / custom DDL | `pnpm drizzle-kit generate --custom --name=<name>` → write SQL into empty file |

**Blocked:** `db:push` / `drizzle-kit push` (state-based live-diff — mutates the DB without writing
a migration journal and collides with the deploy's replay). Also blocked: hand-creating `.sql`
files, TypeScript migration scripts, reconcile scripts for schema changes. Output dir:
`packages/db/drizzle/`. Enforced by `templates/pre-commit-block-db-push.sh`. Deploy-side replay
detail + the a prior migration incident incident: `references/database.md` § Migrations. See also `deploy-and-env`
§ Migration-on-Deploy for the `IGNORE_DB_SYNC_ERRORS` foot-gun.

## Script Placement

Domain scripts (seeders, backfills, mocks, ops actions) MUST live in a dedicated
`apps/scripts` workspace app (`@{ws}/scripts`) that declares its workspace deps,
surfaced from the repo root as `pnpm scripts:[name]`. Root `<repo>/scripts/` is reserved for
pure infra/ops with ZERO workspace internals.

> **Canon reversal (2026-07-06 — "Centralize").** This REPLACES the former co-location
> tree (DB scripts in `packages/db/src/scripts/`, api scripts in `packages/api/src/scripts/`).
> Co-location existed for ownership locality; centralization wins on discoverability (one
> `pnpm scripts:*` surface), uniform env wiring, and turbo awareness. A workspace app with
> declared `@{ws}/db` / `@{ws}/api` deps has none of the pnpm-hoisting problem that still bans
> workspace-importing *root* scripts. Per-repo migration is agent work
> (`standardize-fleet-scripts-package`); audit a repo's state with
> `scripts/bin/fleet-scripts-audit --json`.
>
> **Second reversal (2026-07-14 — "apps/, not packages/").** `apps/scripts` moved out of
> `packages/` entirely, discovered while migrating acme: a package genuinely needing to `import`
> from a script (not just run it) creates a turbo dependency cycle the moment `scripts` also
> depends on that package's own workspace — e.g. `@{ws}/api` importing `@{ws}/scripts` while
> `@{ws}/scripts` already depends on `@{ws}/api`. `apps/*` in this fleet means "top-level
> consumer, nothing depends on it back" (same as `apps/nextjs`, `apps/ios`) — the exact
> constraint `scripts` needs. A file another package's *code* needs to import does not belong in
> `apps/scripts` even if it started life looking like a script; it belongs in whichever package
> already legitimately owns that concern.

### Decision Tree

| Script needs… | Place at |
|---|---|
| ANY workspace import — `@{ws}/db`, `@{ws}/api`, services, drizzle (seeder / backfill / mock / ops action) | `apps/scripts/src/<name>.ts` |
| Pure infra — cron diagnostic, config parse, lint tooling — NO workspace imports | `<repo>/scripts/<name>.ts` (legitimate root case, unchanged) |
| e2e suite infrastructure (fixtures, storage-state seeders) | `packages/e2e/scripts/` — suite infra, not a domain script (`t3-testing-patterns` § E2E Lint Gates) |
| drizzle migration output | `packages/db/drizzle/` — generated, not a script |
| Another package's *code* (not just its build/test tooling) needs to `import` this file | **NOT** `apps/scripts` — a `packages/*` app can never depend back on an `apps/*` entry without a turbo cycle. Place it in whichever package already owns the concern (e.g. a pure predicate over `@{ws}/inventory` types belongs in `@{ws}/inventory`, not scripts) |
| Doesn't fit AND isn't pure infra | **Defer** — ask; do NOT default to root `scripts/` |

### Package Shape

```
apps/scripts/
  package.json      # name @{ws}/scripts; deps: @{ws}/db, @{ws}/api (as needed), tsx; with-env sibling
  tsconfig.json     # extends the repo tsconfig base
  README.md         # inventory table: name -> purpose -> env needs
  src/
    <name>.ts       # one file per script; shared helpers in src/lib/
```

- **package.json keys** — one per script: `"<name>": "pnpm with-env tsx src/<name>.ts"`, with a
  `with-env` (and a `with-test-env` / `:local`) sibling in the dotenvx form below.
- **Root delegation** — root `package.json` gains `"scripts:<name>": "pnpm --filter @{ws}/scripts <name> --"`.
- **Starter template** — `skills/t3-code-patterns/templates/scripts-app/` (copy, substitute
  `{ws}`, `pnpm install`).

### Turbo Integration — selective

Every script gets a root `scripts:<name>` key. A script gets a **turbo task only if another
task depends on it OR its output is cacheable** (e.g. acme's `seed:e2e` chain that e2e depends
on). Blanket turbo registration for one-shot ops actions is config noise.

### Env Loader / With-Env

The canonical with-env invocation is `dotenvx run --overload --quiet -f <path> --`
(`@dotenvx/dotenvx` pinned at `^1.34.0`, acme's reference):

| Flag | Why |
|---|---|
| `--overload` | **Mandatory** — repo `.env` MUST beat already-exported shell vars / a sourced `~/.env` (parity with the old dotenv-cli `-o`; preserves the storefront-za5z wrong-DB protection). A `dotenvx run` WITHOUT `--overload` is an anti-pattern. |
| `--quiet` | Suppresses the dotenvx stdout banner |
| `-f <path>` (not `-e`) | dotenvx's file flag; multi-file is last-wins (`-f base.env -f local.env`) |

New env vars enter via a t3-env `env.ts` schema (see § Env Validation) — never a bare
`process.env.X` read. Full flag-by-flag rationale: `references/script-placement.md`.

### Anti-Patterns

| Pattern | Why It Breaks |
|---|---|
| Root `scripts/*.ts` importing `@{ws}/db` schemas | pnpm doesn't hoist workspace internals; tsx resolution fails — move into `apps/scripts` |
| NEW domain script in `packages/db/src/scripts/` or `packages/api/src/scripts/` | The OLD co-location pattern — now the migration source, not a destination for new work |
| `dotenvx run` WITHOUT `--overload` | Reintroduces the storefront-za5z wrong-DB class |
| Bare `process.env.X` read for a new env var | Must enter via `env.ts` schema — see § Env Validation |

Full anti-pattern table (`createRequire()` hack, hand-loaded `dotenv.config()`, env-var invention):
`references/script-placement.md` § Anti-Patterns.

### Canonical Example

`apps/scripts/src/mock-app.ts` — a `@{ws}/db`-importing seeder wired as
`"mock-app": "pnpm with-env tsx src/mock-app.ts"` in `@{ws}/scripts`, delegated from root as
`"scripts:mock-app": "pnpm --filter @{ws}/scripts mock-app --"`, invoked as `pnpm scripts:mock-app`.
Before creating a new script, check `apps/scripts/src/` + its README inventory —
extension usually beats creation. Full walkthrough: `references/script-placement.md`
§ Canonical Example.

### Defer Trigger

If the new script doesn't fit `apps/scripts` AND isn't pure infra, DEFER. Do NOT fall back to
root `scripts/` as a default — ask whether to extend an existing surface or create a new package.

Cross-ref: `extend-before-create` § 11. Scripts (the decision-tree entry point).

## Env Validation (@t3-oss/env)

Env loading (`dotenvx run --overload`, see § Env Loader / With-Env) and env **validation** are two
layers. `dotenvx` puts values on `process.env`; `@t3-oss/env` validates + types them through a Zod
schema so a missing/malformed var fails loudly instead of surfacing as `undefined` deep in a handler.

### `createEnv` schema

`createEnv` from `@t3-oss/env-nextjs` (Next apps) declares a `server` block, a `client` block, and
a `runtimeEnv` map. Client keys MUST be `NEXT_PUBLIC_`-prefixed — the validator rejects any
`client` entry that isn't (they'd never reach the browser bundle otherwise). Full schema example:
`references/env-validation.md` § `createEnv` schema.

### Placement

| Where | env.ts |
|---|---|
| Next app | `apps/nextjs/src/env.ts` |
| Non-Next package that reads env directly (`packages/auth`, `packages/api`) | per-package `src/env.ts` |

A package that reads env directly ships its own `env.ts` — do NOT reach across into the app's
schema.

### Build-time enforcement (next.config)

Import `./src/env.ts` at the top of `next.config` so validation runs during `next build` — a
missing or malformed env var **fails the build** instead of the running app. Code:
`references/env-validation.md` § Build-time enforcement.

### Non-Next packages: `@t3-oss/env-core`

Non-Next packages use `createEnv` from `@t3-oss/env-core` (no `NEXT_PUBLIC_`/`client` split —
`server`/`runtimeEnv` only). Same schema-as-source-of-truth contract.

### CI / `skipValidation` caveat

Build-time validation means CI must supply a satisfying env. Either the checked-in `.env.example`
satisfies every schema, OR CI sets `SKIP_ENV_VALIDATION=1` / passes `skipValidation` to `createEnv`
so a build without secrets doesn't fail on schema. Keep `.env.example` in sync with the schemas.

### Rule

New env vars enter via the `env.ts` schema — add the key to `server`/`client` + `runtimeEnv`, then
read `env.X`. A bare `process.env.X` read for a new var is the anti-pattern (untyped, unvalidated,
invisible to the schema).

**Enforcement:** the `no-process-env` ESLint rule (see § ESLint Rules catalog +
`templates/eslint-rules/no-process-env.cjs`) bans direct `process.env.X` outside the `env.ts` /
`next.config` boundary, with a per-repo `{ allow: [...] }` allowlist for legitimate raw reads.
Install it AFTER a repo's read-migration wave so CI enforces the end state
(`remediate-env-validation-gap`, 2026-07).

**Status (2026-07-15): dotenvx encryption live fleet-wide — api-app, storefront, operations, backoffice, acme** — `.env`
is dotenvx-encrypted ciphertext, committed and PR-reviewable; `.env.keys` (the decryption
private key) stays gitignored and local-only; `DOTENV_PRIVATE_KEY` is set per-repo in
Vercel (Production + Preview). acme also had 7 stale one-off `.env*` snapshots deleted
(never-wired-in `vercel env pull` dumps from an April-May debugging window); only its
primary `.env` was encrypted, matching every other repo's protocol — `.env.test`/
`.env.local`/`.env.vercel-production` were deliberately left gitignored/untouched rather
than encrypting every "live" file, a narrower scope call. This is the pilot-plus-rollout
half of `remediate-env-validation-gap`; the read-migration half (moving raw `process.env.X`
reads into `env.ts`) landed earlier per-repo per this section's enforcement note above.

### Residual risk: `$(command)` substitution in `.env`

`dotenvx` executes `$(command)` shell substitution in **unquoted or double-quoted** `.env` values,
with **no off-switch** — an accepted, documented residual risk, not solved. Mitigations
(single-quote literal `$(` values; the encrypted-`.env` end-state makes every change
PR-reviewable): full detail in `references/env-validation.md` § Residual risk.

## Better Auth Rate Limiting

Select Better Auth rate-limit policy from validated deployment identity, not `NODE_ENV` alone.
Keep the limiter enabled with an explicit abuse-resistant policy on every reachable preview/dev
deployment and preserve strict production policy. Authenticated isolated E2E may receive short-
lived run/persona/route-scoped capacity or bypass derived server-side from the non-production runner
capability; never globally disable preview protection or weaken production.

When preview/dev sign-ins flake or return 429, read
[`references/better-auth-rate-limiting.md`](references/better-auth-rate-limiting.md) for the
environment distinction, config placement, security boundary, and E2E concurrency triage.

## Null Narrowing

Query results that could be null/undefined MUST have an early-return guard before property access.
No exceptions for "it should always exist."

```typescript
// ✅ Correct
const application = await db.query.application.findFirst({ ... });
if (!application) return null;  // Guard first
application.status;  // Safe access

// ❌ Wrong — 'application' is possibly null
const application = await db.query.application.findFirst({ ... });
application.status;  // TS18047 error
```

## Type Ownership

| Package          | Owns                  |
| ---------------- | --------------------- |
| `packages/db`    | Entity types, enums   |
| `packages/api`   | DTOs via RouterOutputs |
| `apps/*/types/`  | UI-only types         |

## Stripe API Types

When calling Stripe SDK methods, ALWAYS check the type definition before adding properties.
Create-only fields (e.g., `customer`) are NOT valid on update calls:

```typescript
// ✅ Check type first
type Params = Stripe.InvoiceUpdateParams;  // Hover or cmd+click to see valid fields

// ❌ Wrong — 'customer' only exists on InvoiceCreateParams, not Update
stripe.invoices.update(id, { customer: "cus_..." });  // TypeScript error
```

## Terraform Path

Per-project Terraform files MUST live in `packages/infra/`, NOT `infrastructure/terraform/`.

```
packages/infra/
  environments/{dev,prod}/   → Per-environment root modules (.tf, .tfvars)
  modules/                   → Project-local modules (optional)
```

Shared modules: `../shared-modules/` (referenced via git source or relative path).
A PreToolUse hook blocks writes to `infrastructure/terraform/`.

## ESLint Agent Guidance

> Automated checks: `tooling/eslint/`. Below: patterns ESLint **cannot** catch.

| Package | Blocked Pattern | Use Instead |
|---------|-----------------|-------------|
| nextjs | Local `Button.tsx` | `@{workspace}/ui` Button |
| nextjs | `<div onClick cursor-pointer>` | `<Button>` from `@{workspace}/ui` |
| nextjs | `<div rounded shadow>` | `<Card>` from `@{workspace}/ui` |
| nextjs | `style={{}}` | Tailwind classes |
| nextjs | `bg-red-600` | `bg-destructive` (theme token) |
| nextjs | `text-gray-500` | `text-muted-foreground` |
| nextjs | Multiple exports | One component per file |
| nextjs | Inline `<Dialog>` | `*Dialog.tsx` file |
| expo | hardcoded px | responsive values |
| e2e | `.class-name` | `[data-testid]` |

If a real case needs an exception to one of these, the sanctioned route is a whitelist decorator
(below) with an inline justification — not silently writing the blocked pattern anyway.

## ESLint Whitelist Decorators

A decorator is a **documented exception**, not a bypass. Each one requires an inline comment
naming the justification, and a reviewer MUST reject an undocumented or unconvincing one exactly
like any other lint failure — this mirrors the `debt:` marker contract (`rules/CORE.md`): a
shortcut is allowed only when it is auditable, never merely spelled correctly.

| Decorator | Purpose | Justified when | Abuse signal — reject on review |
|-----------|---------|-----------------|----------------------------------|
| `@theme-exception` | Allow arbitrary Tailwind colors | One-off color with no theme-token equivalent (e.g. a partner-brand swatch) | Avoiding the correct existing token (`bg-destructive`, `text-muted-foreground`) |
| `@ui-exception` | Allow inline primitives | A one-time prototype layout with no reusable shape | Recurring markup that should become a shared `@{workspace}/ui` component |
| `@state-exception` | Allow state pattern violation | A non-query state (e.g. a local UI toggle) the loading/error/empty triad doesn't apply to | Skipping loading/error/empty states on a real data-fetching call |
| `@multi-component` | Allow multiple exports | A tightly-coupled parent+subcomponent pair with no reuse outside the pair | Bundling unrelated components together to dodge file-splitting |
| `@wait-exception` | Allow `waitForTimeout` in E2E with justification | A genuine non-deterministic wait (animation settle, third-party widget load) with no better selector | Papering over a flaky selector instead of fixing it with a proper `waitFor` |
| `@isolation-strategy` | Document E2E parallel test isolation approach | A test that legitimately needs process-level isolation (e.g. a shared external resource) | Default answer for any flaky parallel test without diagnosing the real race |
| `@icon-exception` | Allow direct lucide-react import (rare, justify in comment) | An icon genuinely absent from `@{workspace}/ui`'s icon set | Convenience shortcut when the icon already exists in the project's icon package |

**Rule:** `// @theme-exception: partner logo swatch, no theme token exists` is a justified use;
`// @theme-exception` alone, or one that restates the decorator name without a reason, is not.

## Custom ESLint Rules

Twelve ESLint rules ship as copy-ready templates in `templates/eslint-rules/`. Per `feedback_skills_over_npm_packages.md`, these are vendored per-repo (NOT a published npm package) — each project owns its copy and can customize without coordinating a fleet release.

### Catalog

| Rule | Origin | What it catches |
|---|---|---|
| `no-inferSelect-in-service-exports` | acme | `$inferSelect` leaking into RouterOutputs |
| `no-any-in-services` | acme | `any` type in service files |
| `no-this-bang-in-services` | acme | `this!.x` non-null assertions in service methods |
| `max-fn-lines-services` | acme | Service functions exceeding 60 LOC |
| `no-bare-identifier-in-sql-template` | acme | Raw SQL identifier interpolation (injection risk) |
| `no-nested-template-in-sql` | acme | Nested template strings inside `sql\`...\`` |
| `no-role-level-literals` | acme | Hardcoded `"platform-owner"` role strings |
| `require-output-schema` | acme | tRPC procedures missing `.output(...)` |
| `no-ctx-db-query` | **2026-05-17 audit** | `ctx.db.query.*` chains (TS recursion) |
| `no-double-cast` | **2026-05-17 audit** | `as unknown as T` boundary tunneling |
| `procedure-name-matches-middleware` | **2026-05-17 audit** | `adminProcedure` missing actual role check (portal bypass) |
| `no-vi-mock-db` | **2026-05-17 audit** | `vi.mock("@{ws}/db")` outside integration tests |
| `no-process-env` | **2026-07 env-gap** | Direct `process.env.X` outside `env.ts`/`next.config` (bypasses createEnv) |

### Adoption

```bash
# Per-repo, from inside the target repo
cp -r $T3_CODE_PATTERNS_SKILL_DIR/templates/eslint-rules/* tooling/eslint/rules/
# Then wire into eslint.config — see templates/eslint-rules/install.md
```

Full README + AST patterns + fix recipes: `templates/eslint-rules/README.md`.

### Audit-driven rules cite their source

The 4 new rules each cite the 2026-05-17 fleet audit finding that drove them. Future agent-authored procedure work in any T3 fleet repo with these rules wired in will fail-loud at lint time on the documented anti-patterns rather than slipping through code review.

## Domain Errors

Codified from the 2026-05-17 fleet audit. Reference impl: `acme/packages/api/src/infra/monitoring/errors/domain-error.ts` + `acme/packages/api/src/trpc-config.ts:113-184`.

T3 projects ship business errors via a `DomainError` class + `DomainErrors` factory namespace, NOT via bare `throw new TRPCError(...)` scattered through router/service code. The error formatter at the tRPC route handler surfaces structured fields to the client:

| Field | Purpose |
|---|---|
| `userMessage` | UI-safe message rendered to users without sanitization |
| `retryable` | Drives "Try again" button affordance |
| `expected` | Sentry/Linear noise gate — 4xx user-facing errors skip alerting |
| `field` | Form-field name for validation errors |
| `httpStatus` | Maps to HTTP status (single dictionary, not scattered `code:` strings) |

**Rule:** Forbid bare `throw new TRPCError(...)` in service files (`packages/api/src/services/**`). Router files MAY keep direct `TRPCError` for auth gates and tenant-context guards. No ESLint rule ships for this yet — enforce in review until a `no-bare-trpcerror-in-services` rule is added to `templates/eslint-rules/`.

**Why:** Without the contract, every throw site re-invents the user-message / retryable / Sentry-routing decision. With it, one factory call (`DomainErrors.notFound("booking", id)`) gives clients consistent shape and engineers consistent observability.

## Tenant-Scoped Procedures

Codified from acme's pattern. Reference impl: `acme/packages/api/src/trpc-procedures.ts:152-168` + `acme/packages/api/src/middleware/permission.ts`.

Projects with a tenant column (`eventSeriesId`, `eventId`, `campaignId`, `orgId`) MUST define tiered procedure builders:

```typescript
export const tenantProtectedProcedure = protectedProcedure.use(requireTenantContext("event"));
export const tenantSeriesProtectedProcedure = protectedProcedure.use(requireTenantContext("series"));
```

The middleware resolves tenant context once, throws `BAD_REQUEST` on missing context, and narrows `ctx.eventId` / `ctx.eventSeriesId` to non-null for downstream resolvers.

**Rule:** Routers MUST NOT manually re-check `if (!ctx.eventId)` — that's middleware's job. **Procedure name MUST match its actual authorization check.** `adminProcedure` that doesn't check admin role is a critical auth-naming bug (audit caught this in portal). ESLint rule: `procedure-name-matches-middleware` (shipped — `templates/eslint-rules/procedure-name-matches-middleware.cjs`).

**Why:** 1,996 references to `eventSeriesId` in acme's router — without tiered procedures, each one would need defensive guards. The middleware ladder eliminates the boilerplate AND prevents the "I forgot to check tenant" class of bug.

## Data Scoping ESLint Allowlist

Codified from operations's pattern. Reference impl: `operations/tooling/eslint/api.ts:25-90,110-129`.

Tenant-bearing projects SHOULD ship a per-router import allowlist that blocks new router files from importing `@{ws}/db/client` unless explicitly added to `ROUTER_DB_ALLOWLIST` with reviewer sign-off confirming all queries inside `tenantProtectedProcedure` handlers include the tenant `WHERE` clause.

```typescript
// Excerpt from operations/tooling/eslint/api.ts shape:
const ROUTER_DB_ALLOWLIST = new Set([
  "campaign-crud", "character-crud", /* reviewer-approved routers */
]);
// New router files NOT in the set fail lint when they import @{ws}/db/client
```

**Why:** Cross-tenant data leaks are the #1 multi-tenant SaaS catastrophe. ESLint cannot read SQL semantics, but it CAN force a human gate at the obvious moment (new router file added). Defense-in-depth with the runtime tenant-procedure middleware above.

## Metadata/SEO

Next.js App Router `generateMetadata` conventions for title/description/canonical/OG tags,
Twitter Card, JSON-LD, robots, and favicons.

**Agreement rule (MUST):** title, description, canonical URL, and `og:url` MUST all agree with
each other and with the actual served URL. The most common regression is a stale canonical/OG
URL left pointing at the old path after a route rename.

**Verify social cards against a REAL deployed/preview URL, never `localhost`** — social crawlers
(Slack, Twitter/X, iMessage, Facebook) cannot reach `localhost`; a locally-previewed OG image is
not verified.

Key placement rules (full detail + code in the reference below):

| Rule | Gotcha |
|---|---|
| `metadataBase` | Set once, root layout only — a child layout/page resetting it silently overrides the resolution base for its whole subtree |
| Nested layout merge | `openGraph`/`twitter` objects replace the parent wholesale (no deep-merge) — a page overriding `openGraph.title` must repeat `openGraph.images` or loses the parent's OG image |
| Static vs dynamic | Use the static `Metadata` object when nothing depends on params/fetch; reach for async `generateMetadata` only when content is derived from a (cached) data fetch |
| Robots | Site-wide policy in `app/robots.ts`; per-route `metadata.robots` only for a page that must diverge |

Full priority×impact table, per-field coverage checklist, and code samples:
`references/metadata-seo.md`.

React post-change regression check: `npx react-doctor@latest --verbose --scope changed`
(score must not regress). Full contract + flags: `references/react-doctor.md`.

## Reference Files

Deep-dive code examples and rationale live in `references/` — this body keeps the rule an agent
needs at write-time. Available references: `references/database.md`,
`references/script-placement.md`, `references/env-validation.md`, `references/react-doctor.md`,
and `references/better-auth-rate-limiting.md`.

## Related Skills

- `drizzle-best-practices` — Drizzle ORM schema design, migration safety, query gotchas
- `trpc-patterns` — tRPC queryOptions/mutationOptions pattern, type inference, middleware
- `state-handling` — Loading → Error → Empty → Data state pattern for React components
- `database-schema-designer-ext` — Extended database schema design guidance
- `extend-before-create` § 11. Scripts — search-first decision tree for new scripts
- `t3-testing-patterns/references/e2e-fixtures-personas-ownership.md` — mutation safety,
  personas, and provider adapters
- `t3-testing-patterns/references/e2e-topology-evidence.md` — worker benchmarks and
  capacity-vs-test-timing flake triage

## LSP Usage (demoted from rules/CORE.md, 2026-07-25)

> vtsls/TypeScript-specific — a stack concern, not a universal rule. Demoted by
> `prune-core-stale-and-rescope-narrow`; `rules/CORE.md` keeps a one-line pointer.

## LSP Usage

The `LSP` tool (provided by `vtsls@claude-code-lsps`) gives type-aware code navigation that
grep cannot. Reach for LSP first when:

| Goal | LSP invocation | Why over grep |
| --- | --- | --- |
| Find every caller of a function | `LSP({ operation: "findReferences", filePath, line, character })` | Resolves symbol references precisely; grep matches comments + strings |
| Scan file structure (functions, classes, exports) | `LSP({ operation: "documentSymbol", filePath })` | Returns typed symbol tree; grep would need fragile regex |
| Trace who calls X | `LSP({ operation: "callHierarchy", filePath, line, character })` | Walks the call graph through reassignments + alias renames |
| Find a symbol across the workspace | `LSP({ operation: "workspaceSymbol", query })` | Type-aware fuzzy search; grep flattens to text matches |
| Get hover-info / inferred type at point | `LSP({ operation: "hover", filePath, line, character })` | Authoritative type from the language server, not heuristics |

When LSP IS NOT the right tool:
- File contents you've never seen → `Read` first (LSP doesn't read; it traverses).
- Markdown / docs / config files → grep is fine (LSP is for source code).
- Regex-style pattern matches across the whole repo → grep wins.

**Failure mode**: If LSP returns empty/errors for a file that exists, the language server may not
be initialized for that file's project root. Fall back to grep + `Read`, and note the gap in
the response so the LSP install/config can be inspected.
