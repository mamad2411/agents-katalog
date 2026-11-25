---
name: specgen-node-cli-web
model: claude-opus-4-8
effort: high
description: >
  Generate a detailed specification document for building a self-hosted Node.js web
  application distributed as a global npm CLI — installed via `npm install -g <app-name>`,
  started via `<app-name> start`, and accessed at `http://IP:PORT`. Single-process,
  local-first architecture: one Node 22 process serves both the REST API (Hono 4) and an
  embedded pre-built React 19 + Vite 6 SPA styled with Tailwind CSS v4 and vendored
  shadcn/ui. Data lives in per-user SQLite (better-sqlite3 + Drizzle ORM with shipped
  migrations, auto-migrated on start). Authentication is hand-rolled scrypt sessions with
  a first-run auto-generated admin, forced password change, and admin-managed users — no
  OAuth, no JWT, no email flows. CLI parsing via commander 12, bundling via tsup 8,
  monorepo via pnpm workspaces, Biome lint/format, Vitest + Playwright tests, mandatory
  built-binary smoke test. Standardized input: application name (mandatory), version
  (mandatory), module (optional).
  Use this skill whenever the user asks to create a spec, specification, blueprint, or
  technical design document for a self-hosted web app installed as a global CLI, a
  "local-first web tool", an "npm-installable web dashboard", a "CLI that serves a web
  UI", or a single-binary-style Node web application with an embedded frontend. Also
  trigger when the user says things like "spec out a self-hosted Node web app",
  "design an npm global CLI with a web interface", "write a spec for a local web tool
  installed with npm -g", or any request describing a web application that end users
  install on their own machine and open at an IP:PORT. Even if the user only mentions a
  subset (e.g., "Hono + SQLite app started from the terminal" or "CLI-launched
  dashboard"), this skill likely applies — ask and confirm.
---

# Self-Hosted Node.js CLI Web Application Specification Generator

This skill generates a comprehensive specification document (Markdown) that serves as a
blueprint for building a lightweight Node.js web application that is **installed via
`npm install -g <app-name>`**, started via **`<app-name> start`**, and accessed at
**`http://IP:PORT`**. The spec is intended to be followed by a developer or coding agent
to produce a fully functional, publishable package.

The specification does NOT generate code. It produces a detailed, opinionated technical
document describing every layer of the application — from the pnpm workspace layout to
the publish pipeline to the forced-password-change middleware — so that implementation
becomes a mechanical exercise.

**Architecture model (non-negotiable):** Single-process, local-first. One Node process
serves both the REST API and the embedded pre-built web UI. All state lives on the user's
machine. There is no hosted backend. The web app is compiled to static assets at publish
time; end users never run a build.

## Technology Stack

### Core Stack (Always Included)

These are the fixed versions the spec targets. Do not deviate unless the user explicitly
requests different versions.

| Layer | Technology | Version Constraint |
|---|---|---|
| Runtime | Node.js | 22 LTS (`engines.node: ">=22"`) |
| Package manager (dev) | pnpm workspaces | `>=9` |
| Language | TypeScript | `^5.6`, strict mode mandatory |
| CLI framework | commander | `^12` |
| Web framework | Hono (`@hono/node-server`) | `^4` |
| Frontend | React + Vite (built SPA, embedded) | React `^19`, Vite `^6` |
| Styling | Tailwind CSS | `^4` |
| Components | shadcn/ui (vendored) | latest |
| Validation | Zod | `^3` |
| ORM | Drizzle ORM + drizzle-kit | `^0.36` / `^0.28` |
| Database | SQLite via better-sqlite3 | `^11` |
| Auth | Hand-rolled sessions — `node:crypto` only | n/a |
| CLI/package build | tsup | `^8` |
| Lint + format | Biome | `^1.9` |
| Tests | Vitest + Playwright | `^2` / `^1.48` |
| Terminal output | picocolors | `^1` |

> **Why Hono:** framework-agnostic single-process embedding, ~14 kB core, first-class
> TypeScript inference, and `serve-static` for shipping the built SPA from inside the
> installed package.

### Explicitly Excluded

The generated spec must NOT include any of the following — where the coding agent's
general habits conflict with this list, this list wins:

- **Next.js** — cannot be packaged as a global binary
- **Express** — Hono supersedes it
- **Better Auth or any auth framework** — no self-serve signup exists in this model
- **Any database server** (PostgreSQL, MySQL, MongoDB, Redis, ...)
- **Docker** — distribution is npm; daemonization is the OS's job
- **Email flows, self-serve registration, OAuth/social login, JWTs** — see auth rules
- **CORS middleware** — the UI is same-origin by construction

### Optional Integration Versions

Include in the version table only when the corresponding integration is selected
(see Determining Optional Components).

| Component | Version | When Selected |
|---|---|---|
| @tanstack/react-table | 8.x | DataGrid = yes |
| recharts | 2.x | Charts = yes |
| react-day-picker + date-fns | 9.x / 4.x | DatePickers = yes |
| @tiptap/react + @tiptap/starter-kit | 2.x | RichText = yes |
| env-paths | 3.x | Optional helper for the data directory (may resolve manually instead) |

New runtime dependencies beyond these require explicit human approval — the published
tarball SHOULD stay under 5 MB excluding `better-sqlite3`.

## Monorepo Structure (development)

The spec targets this fixed pnpm workspace layout. Package responsibilities are strict:

```
project-root/
├── pnpm-workspace.yaml
├── CLAUDE.md
├── biome.json
├── packages/
│   ├── core/                       # shared: Zod schemas, types, constants
│   │   └── src/
│   │       ├── schemas/            # one file per domain (user.ts, session.ts, ...)
│   │       └── index.ts
│   ├── server/                     # Hono app + Drizzle + auth
│   │   ├── drizzle/                # generated SQL migrations (committed, shipped)
│   │   ├── src/
│   │   │   ├── app.ts              # Hono app factory (routes + middleware)
│   │   │   ├── db/
│   │   │   │   ├── schema.ts
│   │   │   │   ├── index.ts        # connection factory (takes data dir path)
│   │   │   │   └── bootstrap.ts    # first-run: migrate + create default admin
│   │   │   ├── auth/               # sessions, password hashing, middleware
│   │   │   ├── features/<name>/    # routes.ts, service.ts, schema.ts, __tests__/
│   │   │   └── lib/                # logger, env/config
│   │   └── vitest.config.ts
│   ├── web/                        # React SPA (Vite)
│   │   ├── src/
│   │   │   ├── routes/             # login, force-change-password, users, settings, <modules>
│   │   │   ├── components/ui/      # shadcn vendored
│   │   │   └── lib/api.ts          # typed fetch client (hono/client RPC)
│   │   └── vite.config.ts
│   └── cli/                        # THE published package
│       ├── package.json            # name: <app-name>, bin, files: ["dist","static","drizzle"]
│       ├── src/
│       │   ├── index.ts            # #!/usr/bin/env node — commander program
│       │   └── commands/           # start.ts, status.ts, reset-admin.ts, <extra commands>
│       └── tsup.config.ts
└── e2e/                            # Playwright against a started instance
```

**Publish pipeline (the critical mechanic):** `packages/cli` is the only published
artifact. Its build step (1) tsup-bundles the CLI + server into `dist/` with
`better-sqlite3` marked external — it is a native module and must remain a real
dependency, (2) runs `vite build` in `packages/web` and copies the output to
`cli/static/`, (3) copies `server/drizzle/` migrations into the package. The published
package is therefore self-contained: bundle + static UI + migrations.

Structural rules: feature-folder colocation, no barrel files, <300 lines/file, Zod at
every boundary, `any` forbidden, types via `z.infer<>`.

## When the Skill Triggers

Generate the spec when the user provides an **application name** and **version** that
corresponds to one of the custom applications defined in `CLAUDE.md`. The skill reads all
required inputs from the project's context files — no interactive Q&A is needed for the
core inputs.

The user invokes this skill by specifying the target application and version, for example:
- `/specgen-node-cli-web my_tool v1.0.0`
- `/specgen-node-cli-web my_tool v1.0.0 module:Inventory`
- `/specgen-node-cli-web "My Tool" v1.0.0`

The skill then locates the matching context folder and reads all input files automatically.

## Version Gate

Before starting any work, resolve the application folder first (see Input Resolution below), then check `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. If `<app_folder>/CHANGELOG.md` does not exist, skip this check (first-ever execution for this application).
2. If `<app_folder>/CHANGELOG.md` exists, scan all `## vX.Y.Z` headings and determine the **highest version** using semantic versioning comparison.
3. Compare the requested version against the highest version:
   - If requested version **>=** highest version: proceed normally.
   - If requested version **<** highest version: **STOP immediately**. Print: `"Version {requested} is lower than the current application version {highest} recorded in <app_folder>/CHANGELOG.md. Execution rejected."` Do NOT proceed with any work.

## Input Resolution

This skill uses standardized input resolution. Provide:

| Argument | Required | Example | Description |
|----------|----------|---------|-------------|
| `<application>` | Yes | `my_tool` | Application name to locate the context folder |
| `<version>` | Yes | `v1.0.0` | Version to scope processing |
| `module:<name>` | No | `module:Inventory` | Limit generation to a single module |

### Application Folder Resolution

The application name is matched against root-level application folders:
1. Strip any leading `<number>_` prefix from folder names (e.g., `1_my_tool` → `my_tool`)
2. Match case-insensitively against the provided application name
3. Accept snake_case, kebab-case, or title-case input (all match the same folder)
4. If no match found, list available applications and stop

### Auto-Resolved Paths

| File | Resolved Path |
|------|---------------|
| PRD.md | `<app_folder>/context/PRD.md` |
| Module Models | `<app_folder>/context/model/` |
| HTML Mockups | `<app_folder>/context/mockup/` |
| Output (specification) | `<app_folder>/context/specification/` |

### Version Filtering

When a version is provided, only include user stories, NFRs, and constraints from versions
<= the provided version. For example, if `v1.0.4` is specified:
- Include items tagged `[v1.0.0]` through `[v1.0.4]`
- Exclude items tagged `[v1.0.5]` or later
- Version comparison uses semantic versioning order

### Module Filtering

When `module:<name>` is provided:
- Only generate the `SPEC.md` for that specific module
- Other existing module spec files remain untouched
- `SPECIFICATION.md` (root) gets a partial update — only that module's entry in the TOC
  is added or updated; all other TOC entries are preserved as-is
- The mandatory `user-management/SPEC.md` is regenerated only when the filtered module
  IS the user management module

## Gathering Input

The specification is driven by **six input sources** read from the project's context
files. The skill does NOT ask the user for auth, ports, or optional component choices —
it **determines** these automatically from the context.

### Input 1: Application Name (from CLAUDE.md)

From CLAUDE.md (already loaded in context), locate the target application under the
**Custom Applications** section. Extract:

- **Application name**: The section heading (e.g., "Home Inventory", "Team Board")
- **Application description**: The description paragraph below the heading
- **Dependencies**: The "Depends on" list — a self-hosted local-first app normally has
  none; any external service dependency becomes an optional HTTP integration in the spec

The application name is used to derive:
- **Package name / binary name**: kebab-case (e.g., `home-inventory`) — the npm package
  name, the `bin` entry, AND the per-platform data directory name
- **App title**: Title-case, used in the SPA `<title>` and topbar
- **Env var prefix**: SCREAMING_SNAKE of the binary name is NOT used — the CLI env vars
  are always `APP_PORT`, `APP_HOST`, `APP_DATA_DIR`

### Input 2: User Stories (from PRD.md)

Read `<app_folder>/context/PRD.md`. This file contains all user stories organized by
module. Extract:

- **System modules**: Modules under `# System Module` (e.g., Authentication, User
  Management). These map onto the mandatory auth/user-management blueprint — merge their
  IDs into its traceability rather than generating a competing design.
- **Business modules**: Modules under `# Business Module`. Each becomes a server feature
  folder (`server/src/features/<module>/`), a set of SPA routes, and a `<module>/SPEC.md`.
- **CLI-facing stories**: Stories describing terminal interactions (e.g., "start the app
  from my terminal", "reset the admin password offline") map to CLI commands.

**Important:** Items with strikethrough (`~~text~~`) are deprecated — do NOT include them
as active requirements. List them in the "Removed / Replaced" subsection of the
traceability table. Track the `[v1.0.x]` version tag for each item and carry it through
to the generated specification's traceability section.

### Input 3: Non-Functional Requirements (from PRD.md)

Each module's `### Non Functional Requirement` section informs:

- Pagination, filtering, and list-size decisions (Hono query params + SPA table setup)
- Validation rules (character limits, formats) → Zod schemas in `core/`
- Performance constraints (response budgets, LAN access expectations)
- Security posture beyond the mandatory auth baseline

### Input 4: Constraints (from PRD.md)

Each module's `### Constraint` section defines hard boundaries:

- Status enum values → Drizzle `text({ enum })` columns + shared Zod enums
- Business rules → service-layer invariants with tests
- Access control (e.g., "only ADMIN can ...") → route guard configuration

### Input 5: Module Model (from model/ folder)

Read `<app_folder>/context/model/MODEL.md` first as the index, then the individual module
model files (e.g., `model/inventory/model.md` + `schemas.json`). The module model maps to:

- Drizzle table definitions in `server/src/db/schema.ts` (field-for-field, not placeholder)
- Zod schemas in `core/src/schemas/<domain>.ts`
- Service method signatures and route request/response DTOs
- Generated SQL migrations shipped in `server/drizzle/`

This skill expects **relational models** (`modelgen-relational`) since the datastore is
SQLite. If only a NoSQL model exists, flatten document structures into relational tables
and note the mapping decisions in the spec.

### Input 6: HTML Mockup Screens (from mockup/ folder)

Read `<app_folder>/context/mockup/MOCKUP.html` first as the index, then the HTML files
organized by role in subfolders. The mockups map to:

- React page components in `web/src/routes/` (one per screen)
- shadcn/ui component selections (Table vs Cards, Dialog vs Sheet, etc.)
- Navigation structure and per-role menu items
- Tailwind v4 design tokens (colors, font, radius extracted from mockup CSS)

**Role folders inform access control, NOT URL paths.** `mockup/admin/users.html` means
the route requires the `admin` role — the URL is `/users`, never `/admin/users`. If no
mockups exist for the mandatory auth screens (login, force-change-password, users,
settings), spec them from the auth blueprint anyway — they are not optional.

## PRD.md Extended Sections

Before determining optional components, check PRD.md for the following extended sections:

### Architecture Principle Extraction

If PRD.md contains an `# Architecture Principle` section, extract patterns that affect
decisions — but remember this skill's architecture model is fixed. Principles like
"container based deployment" or "microservices" CONFLICT with the single-process
local-first model; surface the conflict to the user instead of silently complying.
Compatible principles (e.g., "offline-first", "no external services") are cited in the
spec's overview.

### Design System Extraction

If PRD.md contains a `# Design System` section with a file reference, resolve and read
it, then map design tokens into the Tailwind v4 CSS-first theme (`@theme` block in the
SPA's global CSS) and shadcn/ui CSS variables. If absent, derive tokens from the mockup
CSS (existing behavior).

### High Level Process Flow Extraction

If PRD.md contains a `# High Level Process Flow` section, flows inform service-method
sequencing, status enums surfaced in list filters, and the Playwright E2E scenario order.
If absent, derive flow from user stories only.

## Determining Optional Components

The mandatory baseline (CLI contract, data directory, bootstrap, auth and user lifecycle)
is never optional. Beyond it, the skill determines optional components by analyzing
PRD.md NFRs, constraints, and mockups:

| Content Pattern | Component Selection |
|---|---|
| NFRs mention "sortable columns", "bulk select", "export CSV", grids | DataGrid = yes (TanStack Table, shadcn Data Table) |
| NFRs mention "chart", "graph", "statistics", "dashboard metrics" | Charts = yes (Recharts) |
| NFRs mention "date picker", "date range", "calendar" | DatePickers = yes (react-day-picker) |
| User stories mention "rich text", "WYSIWYG", "formatted content" | RichText = yes (Tiptap) |
| User stories mention uploading files/images | FileStorage = yes (files under `<data-dir>/files/`, streamed by a Hono route — never inside the install dir) |
| NFRs mention periodic/background work ("every hour", "auto-prune", "scheduled") | InProcessJobs = yes (`setInterval` in the server process; no external queue, no daemon) |
| CLAUDE.md dependencies or NFRs reference an external REST API | HttpIntegration = yes (native `fetch`, config-driven base URL in `config.json`) |
| PRD.md defines CLI commands beyond start/status/reset-admin | ExtraCommands = yes (list them) |

### Summary of Determination

After analyzing all inputs, produce a determination summary before generating the spec.
Present it to the user for confirmation:

```
Mandatory baseline: CLI (start/status/reset-admin) + data dir + bootstrap + scrypt session auth
Optional Component Determination:
- DataGrid:        yes (from PRD.md → NFR mentions sortable item list with bulk delete)
- Charts:          no
- DatePickers:     yes (from PRD.md → purchase date field)
- RichText:        no
- FileStorage:     yes (from PRD.md → item photo upload)
- InProcessJobs:   no
- HttpIntegration: no
- ExtraCommands:   yes (`export` — from PRD.md → offline backup story)
```

If the user disagrees with any determination, allow them to override before proceeding.

## Generating the Specification

Once inputs are gathered and optional components are determined, generate the
specification as a **multi-file output split by module**. Read the spec template at
`references/spec-template.md` for the exact structure and content of each section — it is
the authoritative guide. Read the pattern references when generating the corresponding
sections:

| Reference | Read when generating |
|---|---|
| `references/spec-template.md` | Always — the authoritative section-by-section template |
| `references/cli-packaging-patterns.md` | CLI contract, tsup config, publish pipeline, npm distribution sections |
| `references/server-patterns.md` | Hono composition, data directory, config, DB factory, logger sections |
| `references/auth-patterns.md` | Bootstrap, sessions, password hashing, user lifecycle sections |
| `references/testing-patterns.md` | Testing strategy, smoke test, and Playwright E2E sections |

The specification is split into two categories:

1. **Root `SPECIFICATION.md`** — TOC, monorepo + workspace config, CLI contract, data
   directory, database layer, server composition, first-run bootstrap, authentication,
   SPA shell, testing strategy, and packaging/distribution.
2. **Per-module `<module-name>/SPEC.md`** — Each module gets its own folder with a
   self-contained blueprint spanning server feature (routes + service + schema) and SPA
   feature (pages + components + typed client usage).

Additionally, generate the **mandatory `user-management/SPEC.md`** covering the auth and
user lifecycle screens (login, forced change, users list, settings) even when PRD.md has
no explicit module for it. When PRD.md DOES define an auth/user module, merge its story
IDs into this file's traceability — the security invariants in `references/auth-patterns.md`
still win over any conflicting PRD phrasing, and conflicts must be flagged to the user.

**Important:** The generated spec must use **real application data** from the context
files, not generic placeholders:

- **Modules** use actual module names from PRD.md and MODEL.md
- **Drizzle tables and TypeScript types** match the model files field-for-field
- **Routes and services** map to actual user stories
- **Pages** map to actual mockup screens; URL paths are module-based, not role-prefixed
- **Zod schemas** enforce the actual PRD constraints
- **Version tags** on every user story ID, NFR ID, constraint ID, and mockup screen in
  traceability tables (e.g., `USHI00003 [v1.0.2]`); **ALL traceability sub-tables MUST
  include the `| Version |` column**
- **Removed / Replaced** subsection lists deprecated items with the removing version,
  replacement ID (if any), and reason

### Output Structure

```
<app_folder>/context/specification/
├── SPECIFICATION.md              ← Root: TOC + shared infrastructure (CLI, data dir, DB, server, auth, packaging)
├── user-management/
│   └── SPEC.md                   ← MANDATORY: auth + user lifecycle blueprint
├── <module-1>/
│   └── SPEC.md                   ← Business module blueprint (server feature + SPA feature)
├── <module-2>/
│   └── SPEC.md
└── ...                           ← One folder per business module from PRD.md
```

**Sample code is mandatory.** Every component described in any spec file must include a
complete, self-explanatory code sample. The code must be continuous (no `// ...` gaps)
and usable as a direct reference by a coding agent.

## Changelog Append

After all specification files are successfully generated, append an entry to `CHANGELOG.md` in the application folder (`<app_folder>/CHANGELOG.md`):

1. Read `<app_folder>/CHANGELOG.md`. If it does not exist, create it with:
   ```markdown
   # Changelog

   - This file tracks all skill executions by version for this application.
   - The highest version recorded here is the current application version.
   - Skills MUST NOT execute for a version lower than the highest version in this file.

   ---
   ```
2. Search for a `## {version}` heading matching the current version.
3. If the section **exists**: append a new row to its table.
4. If the section **does not exist**: insert a new section after the `---` below the context header and before any existing `## vX.Y.Z` section (newest-first ordering), with a new table header and the first row.
5. Row format: `| {YYYY-MM-DD} | {application_name} | specgen-node-cli-web | {module or "All"} | Generated self-hosted Node.js CLI web application technical specification |`
6. **Never modify or delete existing rows.**

## Constraints (Non-Negotiable)

These constraints apply to every code sample in the generated spec. Where the coding
agent's habits conflict with them, these constraints win.

### Structure & Types

**TypeScript strict mode everywhere.** `"strict": true` in every package. No `any` —
use `unknown` with Zod narrowing. Types derive from schemas via `z.infer<>`.

**Zod at every boundary.** CLI flags, `config.json`, every API request body/query, and
every external input are parsed with a Zod schema before use. Shared schemas live in
`packages/core` and are consumed by both server routes and SPA forms.

**Feature-folder colocation, no barrel files, <300 lines per file.** Each server feature
is `features/<name>/{routes.ts, service.ts, schema.ts, __tests__/}`. No `index.ts`
re-export barrels.

**Thin CLI handlers.** Command handlers parse flags with commander, validate with Zod,
and delegate to `server`/`core` functions. No business logic in `packages/cli`.

### Process & Distribution

**Foreground process only.** `start` runs in the foreground; Ctrl-C stops it with a
graceful shutdown that closes the SQLite handle. NEVER implement forking/daemon logic —
daemonization belongs to `systemd`/`pm2`.

**Fail loud on a taken port.** Print a clear message naming the flag to change it
(`--port`); never auto-increment silently.

**Option resolution order** for every `start` option: CLI flag → environment variable
(`APP_PORT`, `APP_HOST`, `APP_DATA_DIR`) → `config.json` → default (port `3000`, host
`0.0.0.0` for LAN access).

**The install directory is read-only at runtime.** Global npm installs may not be
writable — never write anything next to the installed code. All state (DB, config, files,
logs) lives in the per-platform data directory, created `0700` on first run.

**`better-sqlite3` stays external.** It is a native module: a real runtime `dependency`
of the published package, never bundled by tsup, never a devDependency. Everything else
is bundled into `dist/` — end users must not need pnpm or the workspace.

**Migrations auto-run on every `start`** before the server binds, against the shipped
`drizzle/` folder. Idempotent; no user-facing migrate command.

### Server & Security

**One Hono app serves everything.** `/api/*` routes first, then `serveStatic` for the SPA
build, with an SPA fallback rewriting unknown non-API GETs to `index.html`. Middleware
order: request-id → logger → session resolution → route guards → routes.

**No CORS, security headers on.** `hono/secure-headers` on all responses. The UI is
same-origin by construction — never add permissive CORS.

**Typed API contract via `hono/client`.** Export the route tree's type from `server`;
`web` consumes a fully typed RPC client. No OpenAPI codegen step.

**Auth is hand-rolled scrypt sessions — nothing else.** scrypt via `node:crypto`
(N=2^15, r=8, p=1, 32-byte key, 16-byte salt, `timingSafeEqual` verify). Opaque session
tokens: raw token client-side in an `httpOnly` `SameSite=Lax` cookie, only the SHA-256
hash server-side; sliding expiry, 30-day absolute cap. NEVER implement email flows,
self-serve registration, OAuth/social login, JWTs, or password recovery other than
`reset-admin` (CLI) and admin-reset (UI).

**Forced password change is server-enforced.** While `must_change_password` is true,
every API route except login, change-password, and logout returns
`403 PASSWORD_CHANGE_REQUIRED` from middleware. The SPA redirect is convenience, not the
control.

**Server-side invariants with tests:** cannot delete the last remaining admin; changing a
password revokes all other sessions; login is rate-limited in-memory (10 attempts / 15
min per username+IP); the plaintext bootstrap password is printed once and never written
to any file or log.

**No module-level DB singletons.** The connection factory takes the resolved data-dir
path as an argument (so tests inject `:memory:`) and always sets the mandatory pragmas:
WAL mode, `foreign_keys = ON`, `busy_timeout = 5000`.

### Verification

**`pnpm verify` must pass before any task is complete** — `check` (tsc + Biome), `test`
(Vitest with real migrations on `:memory:`, never a mocked DB), `build`, and the
**mandatory smoke stage** that executes the *built* CLI: random port, temp `--data-dir`,
HTTP 200 on `/` and the health endpoint, login with the printed admin credentials, clean
shutdown. Shebang, bundling, native-module, and asset-path failures only surface
post-build — testing source alone is insufficient.

## Principles Embedded in the Spec

- Local-first: the user's machine is the source of truth; filesystem access is the root
  of trust (hence `reset-admin` instead of email recovery)
- One printed status block on successful start: local URL, network URL (detected LAN IP),
  data directory, version — structured logs after that
- The `package.json` version field equals the version argument from skill invocation;
  `--version` prints it and the SPA footer renders it
- Password policy is NIST 800-63B posture: minimum 10 characters, reject
  username-as-password, no composition-class rules
- `Secure` cookie flag only when the request arrived over HTTPS — local HTTP on a LAN
  must still work; TLS termination is a reverse-proxy concern (documented, not built)
- Definition of Done per task: structure per the monorepo layout, thin CLI handlers, Zod
  boundaries, shipped migrations, auth invariants tested, `pnpm verify` green including
  the built-binary smoke test, `CLAUDE.md` and `--help` updated when commands change
