---
name: t3-monorepo-patterns
description: T3 Turbo monorepo patterns for pnpm workspaces, Turborepo task configuration, package extraction, and cross-package type sharing. Use when structuring monorepo packages, configuring Turbo tasks, or managing workspace dependencies.
user-invocable: false
allowed-tools: Read, Glob, Grep
---


# T3 Turbo Monorepo Patterns

## Structure Reference

```
apps/
  web/          — Next.js app (user-facing)
  dashboard/    — Next.js admin
  scripts/      — domain scripts: seeders, backfills, mocks, ops (see § Scripts Package) —
                  a top-level consumer app, NOT a package; nothing may depend on it back
packages/
  db/           — Drizzle schema + client
  api/          — tRPC router
  ui/           — Shared React components
  auth/         — Better Auth config
  validators/   — Zod schemas
  logger/       — pino + OpenTelemetry mixin (see § Logger Package)
  contracts/    — schema-only wire-format types (optional — see § Contracts Boundary)
tooling/
  eslint/
  typescript/
```

### Logger Package

`packages/logger` is a pure leaf (depends only on `pino` and `@opentelemetry/api`) that wires
pino's `mixin()` to inject the active OTel trace/span IDs into every log line, giving Sentry-to-log
joins for free. T3 projects that ship to production SHOULD include it. Full shape, the tRPC
middleware wiring, and the `console.log`-in-scripts exception: `references/logger-package.md`.

Package manager: pnpm workspaces. Build system: Turborepo. TypeScript project references.

---

## 1. Package Extraction Decisions

Extract to `packages/` ONLY when 2+ apps consume the code.

| Signal | Action |
|--------|--------|
| 2+ apps import the same module | Extract to `packages/` |
| 1 consumer for >3 months | Inline back into the app |
| >200 lines with clear public API | Ready to extract |
| Single utility function | Never extract — inline it |

Single-consumer code belongs in the app. Premature extraction creates a package that only one app
uses, requiring cross-package PRs for every change.

---

## 2. Turbo Task Dependency Graph

```jsonc
// turbo.json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"],        // dependencies built first
      "outputs": [".next/**", "dist/**"]
    },
    "typecheck": {
      "dependsOn": [],                // NO ^build — use project references instead
      "outputs": []
    },
    "test": {
      "dependsOn": [],                // independent, runs in parallel
      "outputs": ["coverage/**"]
    },
    "db:generate": {
      "cache": false                  // always re-run, never cached
    },
    "db:migrate": {
      "cache": false                  // never cached — side effects
    }
  }
}
```

Key rules:
- `typecheck` must NOT depend on `^build` in dev — it becomes a full build chain. Use
  `composite: true` and TypeScript project references instead.
- `db:generate` and `db:migrate` always set `"cache": false` — they have side effects.
- `outputs` drives what Turborepo caches. Omitting outputs = nothing cached for that task.

### Turbopack Build & Dev Caches (Next.js apps)

Turbopack (default bundler since Next.js 16) maintains its own persistent caches, independent of
Turborepo's task cache above:

- **Build cache** — `experimental: { turbopackFileSystemCacheForBuild: true }` in `next.config.ts`
  lets `next build` reuse previously-compiled work from disk. The mechanism is CI persisting the
  generated `.next` directory between runs — the same directory `outputs: [".next/**"]` above
  already restores on a Turborepo cache hit.
  **Open question, not a documented recipe:** whether the Turbopack filesystem cache lives inside
  `.next` such that a Turborepo `outputs` restore preserves it, or whether it needs a separate CI
  cache step (e.g. keyed on `.next/cache`), is not established. Do not invent an answer — verify
  against the installed Next.js version before relying on either shape.
- **Dev memory eviction** is on by default in current Next.js releases and requires the dev
  filesystem cache to also be enabled (both are on by default). Don't disable the dev filesystem
  cache without expecting dev-server memory growth to come back.
- **`turbopackLocalPostcssConfig`** (experimental) resolves the nearest `postcss.config.*` to each
  CSS file instead of only the project root — relevant once a monorepo has per-package PostCSS
  transforms instead of one shared root config.

---

## 3. TypeScript Project References

Each package uses two tsconfig files:

- `tsconfig.json` — for development (used by editors and `tsc --noEmit`)
- `tsconfig.build.json` — for declaration output (`composite: true`, emits `.d.ts`)

**Root tsconfig paths** resolve during development. **Package-level `references`** drive
incremental compilation. Both must be consistent.

### Adding a new package — checklist

1. Create `packages/newpkg/package.json` with `"name": "@workspace/newpkg"` and `"exports"` field.
2. Add `"@workspace/newpkg": ["../../packages/newpkg/src"]` to root `tsconfig.json` → `paths`.
3. Add `{ "path": "../../packages/newpkg" }` to consuming package's `tsconfig.json` → `references`.
4. Run `pnpm add @workspace/newpkg --filter @workspace/consuming-app` to register the dep.
5. Verify: `pnpm turbo run typecheck` from monorepo root passes.

If `Cannot find module '@workspace/newpkg'` appears, all four steps above are required — missing
any one causes the error.

---

## 4. pnpm Workspace Gotchas

```bash
# ALWAYS filter — never add to root
pnpm add zod --filter @workspace/validators

# Internal deps use workspace:* protocol
# package.json: "dependencies": { "@workspace/db": "workspace:*" }

# Create via worktree-standard, then install before any build.
# Use its returned WORKTREE path; keep the coordinator in its original directory.
CREATED=$(python3 "$HOME/.agents/skills/worktree-standard/scripts/worktree.py" create \
  --repo "$REPO" --client "$CLIENT" --task my-task --session "$SESSION_ID" \
  --base origin/base-branch) && \
WORKTREE=$(printf '%s' "$CREATED" | python3 -c 'import json,sys; print(json.load(sys.stdin)["path"])') && \
( cd "$WORKTREE" && pnpm install --frozen-lockfile )

# Scope a command to one package
pnpm --filter @workspace/web dev

# Run across all packages
pnpm -r typecheck
```

Skipping `pnpm install --frozen-lockfile` after `git worktree add` causes `turbo: command not
found` and `Cannot find module` errors — workspace symlinks are not set up until install runs.

---

## 4b. `with-env` Scripts Must Use `dotenvx run --overload`

T3 monorepo `with-env` scripts (`apps/*/package.json`, `packages/db/package.json`) load the root
`.env` for local tooling (dev server, `drizzle-kit generate`, seeds, `db:migrate`). They MUST pass the
`--overload` flag so the project `.env` wins over any stray global `~/.env` or exported shell
var:

```jsonc
"with-env": "dotenvx run --overload --quiet -f ../../.env --"
// seeds/migrations inherit it — never re-load .env inline:
"seed:foo": "pnpm with-env tsx src/seed-foo.ts"
```

Flag notes: `--overload` is mandatory (parity with the old dotenv-cli `-o` — repo `.env` beats
shell/`~/.env`); `--quiet` suppresses the stdout startup banner; the file flag is `-f` (not `-e`),
and multiple `-f a -f b` are last-wins. A `with-env` invocation WITHOUT `--overload` is an
anti-pattern.

Without `--overload`, a pre-set shell var (e.g. a machine-global `POSTGRES_URL=...localhost...`) shadows
the project value and **every tool silently hits the wrong DB** — dev server renders no data,
`drizzle-kit generate`/`db:migrate`/seeds target the wrong database. Verify in a shell that has the stray var set:

```bash
pnpm with-env node -e 'console.log(new URL(process.env.POSTGRES_URL).host)'  # must NOT be localhost
```

> **DB policy:** schema changes are migration-based only — `drizzle-kit generate` → commit the
> migration → deploy applies `db:migrate`. NEVER `db:push` (state-based live-diff; collides with
> `db:migrate` replay → drift). See `t3-code-patterns` § Migrations.

> **OVERRIDE 2026-07-06:** the project adopts `@dotenvx/dotenvx` as loader canon; the prior
> stay-on-dotenv-cli verdict is reversed. See openspec change `adopt-dotenvx-and-t3-env-canon`.

A running dev server caches the bad connection — restart it after fixing.

## 4c. Scripts Package (`@{ws}/scripts`)

Domain scripts (seeders, backfills, mocks, ops actions) live in a dedicated `apps/scripts`
workspace app — NOT co-located in `packages/db/src/scripts/` (the pre-2026-07-06 pattern,
now the migration source) and NOT at root `<repo>/scripts/` (reserved for pure infra with zero
workspace imports). Full placement doctrine: `t3-code-patterns` § Script Placement.

**Why `apps/`, not `packages/`** (2026-07-14 revision): `scripts` may depend on ANY other
package (db, api, inventory, ...) but nothing may ever depend on `scripts` back — that's what an
`apps/*` entry means in this fleet (a top-level consumer, same as `apps/nextjs` or `apps/ios`),
and enforcing it structurally prevents a class of turbo dependency cycle. A file that another
package's code needs to `import` (not just run as a script) does NOT belong in `apps/scripts` —
it belongs in whichever package already legitimately owns that concern, even if it started life
looking like a one-off script.

```
apps/scripts/
  package.json      # name @{ws}/scripts; deps: @{ws}/db, @{ws}/api (as needed), tsx; with-env sibling
  tsconfig.json     # extends the repo tsconfig base
  README.md         # inventory table: name -> purpose -> env needs
  src/<name>.ts     # one file per script; shared helpers in src/lib/
```

- **Root surface** — each script gets a root `package.json` delegation key:
  `"scripts:<name>": "pnpm --filter @{ws}/scripts <name> --"`, invoked as `pnpm scripts:<name>`.
- **Env** — the package's own `with-env` sibling (`dotenvx run --overload --quiet -f ../../.env --`,
  § 4b). `apps/scripts` sits at the same depth as `packages/db`, so `../../.env` is unchanged.
- **Turbo** — a script gets a turbo task ONLY if another task depends on it or its output is
  cacheable (e.g. a `seed:e2e` chain that e2e depends on: `@{ws}/scripts#seed:e2e`). One-shot
  ops actions get a root key but no turbo entry.
- **Audit** — `scripts/bin/fleet-scripts-audit --json` reports a repo's script placement classes,
  root-key coverage, and turbo awareness. Starter skeleton:
  `skills/t3-code-patterns/templates/scripts-app/`.

## 5. Common Monorepo Mistakes

| Mistake | Correct Pattern |
|---------|-----------------|
| `import from '../../packages/db/src/schema'` | `import from '@workspace/db'` |
| `pnpm install` inside `packages/db/` | `pnpm install` from monorepo root only |
| Missing `"exports"` in `package.json` | Always define `exports` — types won't resolve without it |
| `db` imports from `api`, `api` imports from `db` | Circular — restructure; `db` is always a leaf |
| `import { db } from '@workspace/db/client'` via deep path | Use the exports map; add subpath export if needed |

---

## Thinking Patterns (frame before restructuring)

The tables above give you signals and mechanics; these are the judgment calls that decide which
row applies.

1. **When do I actually extract a package?** The extraction table's "2+ apps import the same
   module" row is the trigger, not the whole cost-benefit. Extracting before a second consumer
   exists creates a package with no reuse payback — every future change to that code now needs a
   cross-package understanding (exports map, tsconfig references, workspace filter) that a
   same-app move would not have required. Ask "does a second app need this today," not "could a
   second app need this eventually" — the second question is YAGNI dressed as foresight.
2. **What does the one-runtime-dependency invariant buy me?** `packages/contracts`' "exactly one
   of `zod`/`effect`, zero internal workspace deps" rule (§ Contracts Boundary) isn't arbitrary
   purism — it's the mechanism that stops a client bundle from transitively pulling Drizzle or
   Better Auth through a "convenience" re-export. When deciding where a new type belongs, the test
   is: would adding this pull a second runtime dependency into contracts' `package.json`? If yes,
   it belongs downstream, not in the narrow-waist package.
3. **Narrow-waist reasoning: which side of the boundary owns this?** `db` is always a leaf (§5)
   and `contracts` is schema-only — both are narrow-waist packages: many things depend on them,
   they depend on almost nothing. Before adding an import, check which way the dependency arrow
   points. Importing `api` from `db`, or `drizzle-orm` from `contracts`, isn't a shortcut — it
   widens the waist, and every future consumer inherits the coupling.

---

## NEVER

- NEVER run `turbo run build` from inside a package directory — always from monorepo root.
- NEVER import across packages via relative paths (`../../packages/db`) — use `@workspace/` alias.
- NEVER create a package for a single utility function — inline it.
- NEVER add a dependency to the root `package.json` unless it is a tooling-level dep (e.g., turbo, typescript). App and package deps go in their own `package.json`.
- NEVER skip `pnpm install --frozen-lockfile` after `git worktree add` — workspace symlinks aren't
  wired up until install runs, and skipping it surfaces as `turbo: command not found` and
  `Cannot find module` errors that look like a broken monorepo, not a missing install step.
- NEVER omit `--overload` on a `with-env` invocation. A production incident demonstrated that a
  pre-set shell/global var (e.g. a machine-wide `POSTGRES_URL=...localhost...`) silently shadows
  the project's real `.env` value, and every tool — dev server, `drizzle-kit generate`,
  `db:migrate`, seeds — quietly targets the wrong database with no error thrown.
- NEVER let `apps/scripts` become an import target for another package's *code*. The 2026-07-14
  reversal that moved scripts out of `packages/` into `apps/` exists specifically because a
  package importing from `scripts` while `scripts` already depends on that same package (e.g.
  `@{ws}/api` ↔ `@{ws}/scripts`) creates a live turbo dependency cycle — this was discovered
  mid-migration, not designed in from the start.
- NEVER add a new domain script under `packages/db/src/scripts/` or `packages/api/src/scripts/`.
  That co-location tree is the pre-2026-07-06 pattern — it is now exclusively a migration
  *source*, never a valid destination for new work.
- NEVER let `packages/contracts` grow a second runtime dependency or an internal workspace import.
  A contracts package that imports `drizzle-orm` schemas as a "convenience re-export" reproduces
  the exact coupling the schema-only boundary exists to prevent — it pulls Drizzle (or Better
  Auth, or Effect Layers) transitively into every client bundle that depends on contracts.
- NEVER extract code to `packages/` before a second app actually consumes it. Ask "does a second
  app need this today," not "could it eventually" — premature extraction creates a package with no
  reuse payback, and every future change now needs cross-package machinery (exports map, tsconfig
  references, workspace filter) a same-app move would never have required.
- NEVER wire a blanket turbo task onto a one-shot ops script. Turbo registration is selective —
  a script earns a task only when another task depends on it or its output is cacheable (a
  `seed:e2e` chain, which e2e genuinely depends on, is the one earning example) — anything else
  is pure config noise with no cache payoff.

---

## Contracts Boundary (Schema-Only `packages/contracts`)

A **schema-only contracts package** is the narrow-waist between server and client: it declares
wire-format types (Zod or Effect Schema) and nothing else — no runtime logic, no DB clients, no
business code. `package.json` MUST list exactly ONE runtime dependency (`zod` or `effect`), zero
internal workspace deps — the discipline that keeps client bundles from transitively pulling
Drizzle/Better Auth/Effect Layers. Full invariant test, retrofit recipe, and the "fancy re-export"
anti-pattern (a contracts package that imports `drizzle-orm` schemas — same coupling, more files):
`references/contracts-boundary.md`.
