# AGENTS.md

Guidance for AI agents and contributors working in the Naucto Backend. This is a **working
guide, not a rigid rulebook** — the config files are the source of truth for enforced rules;
this file documents the intent, conventions, and gotchas that tooling can't capture.

> Compatible with Claude Code (via `CLAUDE.md` → `@AGENTS.md`) and OpenCode (native `AGENTS.md`).

## Overview

Naucto Backend is a **NestJS 11 + Prisma 7 + TypeScript** REST/WebSocket API for a
collaborative, multiplayer game editor. It uses PostgreSQL (via the Prisma `pg` adapter), JWT
auth (`passport-jwt`) with encrypted refresh-token cookies and Google/GitHub/Microsoft OAuth,
S3-compatible object storage for game and asset content, handed to the browser from
`EDGE_ENDPOINT`, and a `ws` + Yjs (CRDT) server for real-time multiplayer editing. The HTTP API is
documented with `@nestjs/swagger`, and its OpenAPI spec is the **contract the Frontend's generated
client consumes**. The dev server runs on `http://localhost:3000`; the frontend runs on
`http://localhost:3001`. The typed client is published as `@naucto/api-client` on GitHub Packages
from `client/` (see `client/README.md`).

## How to work in this repo

1. **Explore and reuse before writing.** Look for existing services, guards, DTOs, decorators,
   and common helpers first. A feature is a NestJS module — study an existing one end-to-end
   (`src/routes/project/`) and match its shape.
2. **The config files are the rule authority** — don't rely on memory for style rules:
   - `eslint.config.mjs` — lint rules (import order, explicit return types, the env-access ban,
     naming, …), not formatting.
   - `tsconfig.json` — (very) strict TypeScript settings.
   - `.prettierrc` — owns formatting (`npm run format`); `eslint.config.mjs` extends
     `eslint-config-prettier`, so the two never disagree.
   - `package.json` — available scripts and dependencies.
3. **Run the feedback loop before finishing:** `npm run lint`, `npm run typecheck`, `npm run build`,
   and `npm run test`. CI (`.github/workflows/ci.yml`) runs lint (check-only), typecheck, build and
   Jest against a real Postgres on every push/PR to `main` and must pass. A husky pre-commit hook
   runs `eslint --fix` on staged files and `commit-msg` enforces the `[PART] [TYPE] Message` format.
   `.github/workflows/docker.yml` builds the production image on PRs and publishes it to
   `ghcr.io/naucto/backend:{main,sha-<sha>,<tag>}` on `main` / `v*` tags (consumed by the
   Frontend's full e2e run).
4. **Ask the user when a decision is non-obvious** — especially architectural ones (new
   dependencies, schema/migration changes, cross-cutting structure). Prefer asking over assuming.
5. **Never hand-edit generated code** — `swagger.json`, `client/src` + `client/dist` (all three
   gitignored), and `prisma/migrations/` are generated (see Gotchas).

## Commands

| Command                                                                             | Purpose                                                                                                                          |
| ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `npm run start:dev`                                                                 | Start Nest in watch mode on `localhost:3000`                                                                                     |
| `npm run build`                                                                     | Compile with `nest build` (strict `tsc`)                                                                                         |
| `npm run start:prod`                                                                | Run the compiled server (`node dist/main`)                                                                                       |
| `npm run lint`                                                                      | ESLint over `src/`, `test/`, `prisma/`, `tool/` and the root config files — **note: runs with `--fix` (mutates files)**          |
| `npm run lint:check`                                                                | ESLint, check-only (what CI runs)                                                                                                |
| `npm run typecheck`                                                                 | `tsc --noEmit` over the same files as `lint:check` (`tsconfig.eslint.json`)                                                      |
| `npm run format`                                                                    | Prettier-format `src/` and `test/`                                                                                               |
| `npm run test`                                                                      | Unit tests (Jest, co-located `*.spec.ts`)                                                                                        |
| `npm run test:cov`                                                                  | Unit tests with coverage                                                                                                         |
| `npm run generate:swagger`                                                          | Boot the app and emit `swagger.json` from the Swagger decorators                                                                 |
| `npm run generate:client`                                                           | Generate the typed API client sources into `client/src`                                                                          |
| `npm run client:build`                                                              | Emit `swagger.json`, then generate + compile `@naucto/api-client` into `client/dist` (what the publish workflow runs)            |
| `npx prisma migrate dev --name <desc>`                                              | Create + apply a dev migration from the schema                                                                                   |
| `npx prisma generate`                                                               | Regenerate the Prisma client                                                                                                     |
| `npm run seed:dev`                                                                  | Seed a local database with people, friendships, pending requests and shared game sessions (refuses non-local hosts)              |
| `npm run seed:analytics`                                                            | Fill a local database with 60 days of synthetic analytics and finalize it, so the admin panel has data (refuses non-local hosts) |
| `npm run analytics:acceptance`                                                      | Run the analytics acceptance scenarios against a scratch copy of the local database, over two connections; by hand, never in CI  |
| `npm run repair:release-view-keys`                                                  | Delete the release view keys once derived from readers' addresses (one-off)                                                      |
| `docker compose -f docker-compose.yml -f docker-compose.dev.yml up --watch backend` | Dev stack: Postgres, MinIO, and the API with hot reload                                                                          |
| `./dev.sh`                                                                          | The line above with a `build` first — the shorthand, and the usual way in                                                        |

**The dev container and a host build share `dist/`.** The repo is bind-mounted into the container,
which runs `nest start --watch` as root, so `dist/` on the host ends up root-owned and a subsequent
`npm run build` fails with `EACCES ... unlink dist/...`. Stop the backend service before building or
testing on the host (`docker compose ... stop backend`). Mounting a volume over `dist/` does not
help: `nest build` removes the whole directory first and cannot remove a mountpoint.

The dev stack includes **MinIO** (`:9000`, console `:9001`), because release content is fetched by
the _browser_ straight from `EDGE_ENDPOINT` — point that at a bucket the browser cannot reach and
`/play/:id` renders a black screen with "Failed to fetch". `docker-compose.dev.yml` creates the
bucket named by `S3_BUCKET_NAME` and makes it anonymously readable; set the five `S3_*` values and
`EDGE_ENDPOINT` as `.env.example` shows and a published game plays on localhost.

`config/webrtc.json` is gitignored and **required**: no WebRTC offer can be built without it.
Create it with `cp config/webrtc.example.json config/webrtc.json`.

## Architecture map

| Path                                         | Purpose                                                                                                                                                                                                                             |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/main.ts`                                | Bootstrap: Express adapter, global `ValidationPipe`, CORS, `cookie-parser`, Swagger, request logging                                                                                                                                |
| `src/app.module.ts`                          | Root module wiring every feature module                                                                                                                                                                                             |
| `src/auth/`                                  | JWT auth, passport strategy, access control (`access/`: global guard, `@Public()`/`@RequiresAuth()`/`@RequiresRole()`, roles), project ownership guards, OAuth providers (Google/GitHub/Microsoft), refresh-token crypto            |
| `src/routes/<feature>/`                      | One folder per HTTP feature: `*.controller.ts`, `*.service.ts`, `*.module.ts`, `*.error.ts`, `dto/`, co-located `*.spec.ts` (`recommendations` = featured release / game of the week, admin-only writes via `@RequiresRole(ADMIN)`) |
| `src/webrtc/`                                | `ws` + Yjs real-time multiplayer server (`server/`); `WebRTCService` allocates one port per server and advertises its public URL (see _WebSocket servers_ below)                                                                    |
| `src/routes/analytics/`                      | Usage analytics: ingest from browsers, business facts, multiplayer accounting, minute presence sampling, finalization into rollups, account history projection, purge, and the admin and user read APIs (see _Analytics_ below)     |
| `src/routes/admin/`                          | The admin console's own sign-in and admin accounts: who holds the role, promoting and revoking (see _Admin console_ below)                                                                                                          |
| `src/tasks/`                                 | Scheduled jobs (`@nestjs/schedule` cron)                                                                                                                                                                                            |
| `src/prisma/`                                | `PrismaService` + module                                                                                                                                                                                                            |
| `src/common/`                                | Cross-feature DTOs + decorators (pagination, signed-CDN, `@AtLeastOne`)                                                                                                                                                             |
| `src/util/`                                  | Framework-agnostic helpers                                                                                                                                                                                                          |
| `src/swagger.ts`, `tool/generate-swagger.ts` | OpenAPI document build + emit                                                                                                                                                                                                       |
| `prisma/`                                    | `schema.prisma` + split `models/*.prisma` + `migrations/`                                                                                                                                                                           |
| `client/`                                    | `@naucto/api-client` package: `package.json`/`tsconfig.json`/`README.md` committed, `src/`+`dist/` **generated** (gitignored)                                                                                                       |
| `config/`                                    | Runtime config read from the working directory: feature flags (`features.json`), ICE servers (`webrtc.json`, gitignored)                                                                                                            |
| `test/`                                      | Specs for the code that lives outside `src/`                                                                                                                                                                                        |

**Module pattern:** every feature is a NestJS `@Module` declaring `controllers`, `providers`,
`imports`, `exports`. Keep **controllers thin** — HTTP + Swagger decorators + guards only; put
business logic in `@Injectable()` services; reach the database **only** through `PrismaService`.

**DTOs + validation:** request/response shapes are classes in `dto/`, decorated with
`class-validator` (`@IsString`, `@IsOptional`, …) and `@ApiProperty`. The global `ValidationPipe`
(`whitelist: true, forbidNonWhitelisted: true, transform: true`) **strips unknown fields and
rejects unexpected ones** — so every accepted field needs a validator decorator, or it is dropped.

**Access control — deny by default.** One global guard (`src/auth/access/access.guard.ts`,
registered as `APP_GUARD`) decides every route from the access its handler, or failing that its
controller, declares with exactly one of three decorators (`src/auth/access/access.decorators.ts`):

- `@Public()` — anyone; a valid bearer token still sets `req.user`, a missing or bad one leaves it
  `null` and never refuses.
- `@RequiresAuth()` — any signed-in user (401 otherwise).
- `@RequiresRole(MODERATOR)` / `@RequiresRole(ADMIN)` — a signed-in user holding that role or one
  ranked above it (403 otherwise). Roles are a hierarchy, `MODERATOR` < `ADMIN`: an admin is also a
  moderator. The constants live in `src/auth/access/roles.ts` and equal the role rows the
  migrations seed.

A route that declares nothing is treated as `@RequiresRole(ADMIN)`, and `access-coverage.spec.ts`
fails on it anyway: every route states who may call it. Handler metadata overrides the
controller's, so a `@RequiresAuth()` controller can open single routes with `@Public()`. The
decorators carry the Swagger security annotations — don't add `@ApiBearerAuth` by hand.
Ownership checks stay per route: `@UseGuards(ProjectCollaboratorGuard)` /
`@UseGuards(ProjectCreatorGuard)` run after the global guard, so `req.user` is set. Reuse these —
don't re-implement.

**WebSocket servers:** three `WebRTCServer`s run next to the HTTP API, each on its own port
(sequential from `BACKEND_WEBRTC_PORT_BASE`, default 10000) and with a stable public name
(`WEBRTC_SERVER_NAMES`): `collab` (Yjs collaboration, `WorkSessionService`), `game` (multiplayer
game table, `MultiplayerService`), `user` (per-user notifications, `NotificationsService`).
Clients never guess the address — they fetch an offer whose signaling URL comes from
`WebRTCService.buildSignalingUrl`:

- **Local dev** (`BACKEND_WEBRTC_PUBLIC_URL_TEMPLATE` unset): `ws://{BACKEND_WEBRTC_HOSTNAME}:{port}`
  (`wss://` when the hostname isn't `localhost`), so the compose files publish the port range.
- **Production**: set `BACKEND_WEBRTC_PUBLIC_URL_TEMPLATE=wss://{name}.ws.beta.naucto.net` and map one
  domain per server in Production-Environment/Willy (`collab.ws.beta.naucto.net → backend:10000`,
  `game.ws… → :10001`, `user.ws… → :10002`; Willy issues the certificates). `{port}` is also
  substituted if a template needs it. Adding a server = adding a name to `WEBRTC_SERVER_NAMES`,
  defaulting it in the server's options class, and mapping one more domain.

**Errors:** from services, prefer Nest's built-in `HttpException` subclasses
(`NotFoundException`, `ForbiddenException`, `BadRequestException`, …) — they map to status codes
automatically. Domain errors are small classes in `*.error.ts`; translate them to HTTP responses
at the controller boundary (see `project.controller.ts` catching `S3ObjectNotFoundException`).

**Analytics** (`src/routes/analytics/`), behind the `analytics` flag of `config/features.json`:

- `analytics-metrics.ts` is the single source of every KPI: who it counts, how its values combine,
  when a period of it becomes final, and its version. Change a definition by bumping its version;
  values of different versions are never combined, and final periods are never recomputed.
- Browsers that consented report under a visitor and a session cookie the frontend sets; the API
  never reads them. Tabs that declined send identifier-free pings, tallied per minute. Ingest
  routes take JSON sent as text/plain without credentials and never read an account; linking a
  browser to an account is the one authenticated call.
- Business facts (signups, projects, release transitions) are written in the transaction of the
  operation they record, keyed per transition, never by an account id. Multiplayer is accounted
  from the game room server through `SyncedGameTableObserver`.
- Identities are coordinated by transaction-scoped advisory locks (`identity-locks.ts`), always
  taken in the order purge gate, account, visitors. Any new writer that can reach an account's
  analytics must take them; erasure relies on it.
- Every day is a UTC day. Raw data is kept 90 days and purged only once every period built from
  it is final and every linked account's history has it; rollups and account histories stay.

**Admin console** (`src/routes/admin/`), for the separate Admin-Panel app:

- `admin/auth/*` signs an admin in with a password and an account holding the admin role. It
  answers an access token and sets the httpOnly `naucto_admin_session` cookie that renews it for
  eight hours; that cookie is signed with a key of its own, so it never verifies as a bearer token.
- Wrong passwords per address are limited in memory (`attempt-limiter.ts`), which holds while the
  backend runs as one instance.
- An admin cannot change their own role, and the last admin cannot be demoted.

## Conventions (not all enforced by tooling — follow these)

These complement the lint/TS rules (which you should read from the config files, not restate).

**Imports** — relative paths (`./x`, `../auth/auth.service`); the project has no path aliases.
`@prisma/client`, `@nestjs/*`, `@aws-sdk/*`, `@tygra/*` are npm packages. No file extensions.
Ordering is `simple-import-sort`'s, applied by `npm run lint`.

**Naming** — no one-letter names (`id-length`) beyond indexes `i`/`j`/`k`, coordinates `x`/`y`,
a comparator's `a`/`b`, an ignored `_` and the `Y` namespace of Yjs: `error`, not `e`;
`project`, not `p`.

**Formatting** — Prettier owns it (`npm run format`), with the same `.prettierrc` as the
Frontend; ESLint only adds `curly: all`, so every `if`/`for` body is a braced block. Use the
`private` keyword, never `#private` fields.

**TypeScript** — the config is **very strict** (`strict` plus `noUncheckedIndexedAccess`,
`exactOptionalPropertyTypes`, `noUnusedLocals`/`noUnusedParameters`, `noImplicitOverride`,
`noPropertyAccessFromIndexSignature`, …). Practical consequences:

- Mark overrides with `override` (e.g. a guard's `canActivate`).
- Indexed access can be `undefined` — narrow it; don't assume.
- No unused locals/params. `any` is discouraged (typescript-eslint warns) — prefer real types
  or `unknown`. **Don't loosen `tsconfig.json` to silence an error.**

**Return types** — explicit function return types are **required** (`explicit-function-return-type`),
including `Promise<T>` and `void`.

**Configuration** — read environment variables with `getEnv(key)` (throws when unset) or
`getOptionalEnv(key, fallback)` from `src/config/env.ts`; the key is typed and the value comes back
parsed (numbers, flags). A new variable is declared in that registry and in `.env.example`. Specs set
values with `withEnv({...})` from `test/env.ts`, restored after each test.

**Logging** — use Nest's `Logger` (`private readonly logger = new Logger(MyClass.name)`).
`console.*` trips `no-console` (warn) — avoid it in app code (`prisma/` seeds and `tool/` scripts
are exempted in `eslint.config.mjs`).

**Files & folders**

- **Folder names are `kebab-case`** (`work-session/`, `project-comment/`).
- Files follow Nest's dot-suffix convention: `project.controller.ts`, `create-project.dto.ts`,
  `project.service.spec.ts`, `project.error.ts`. Classes are `PascalCase`.
- Keep one clear responsibility per file; split as features grow.

**TODO / FIXME** — reference a Jira ticket: `// TODO(NCTO-123): …`.

**Testing** — unit tests are co-located `*.spec.ts` using `@nestjs/testing`
(`Test.createTestingModule`) with mocked providers (`useValue`). Add or extend specs for new
services, controllers, and business logic. Specs for code outside `src/` go in `test/`.

**Database / Prisma** — edit the schema in `prisma/models/*.prisma`, then create a migration
with `npx prisma migrate dev --name <desc>` and run `npx prisma generate`. **Never hand-edit
files under `prisma/migrations/`.** Access the DB only via `PrismaService`.

**Commits / branches** — see `CONTRIBUTING.md` (branch = Jira key; commit = `[PART] [TYPE] Message`).

## Security

See `SECURITY.md` for the disclosure policy. Rules for agents and contributors:

- **No secrets in code or git.** All config comes from env (`.env`, gitignored) read via
  `getEnv` / `getOptionalEnv`. Never commit `.env`, `*.pem` (CloudFront keys), or real keys/tokens — even in
  tests or fixtures. `.env.example` documents the variable names; the only values it carries are
  the local MinIO defaults.
- **Validate all input.** Every controller input is a DTO with `class-validator` decorators and
  the global `ValidationPipe` rejects unknown fields — don't bypass it with an untyped `@Body()`
  or by disabling `whitelist`/`forbidNonWhitelisted`.
- **Auth/secrets handling.** Access tokens are JWT bearer tokens (`passport-jwt`); refresh tokens
  are encrypted (AES-256-GCM, `auth/refresh-cookie.crypto.ts`) and delivered as httpOnly cookies;
  passwords are hashed with `bcryptjs`. Don't log tokens/passwords, never return password hashes
  (use response DTOs / Prisma `select`), and keep routes behind access control — `@Public()` must be a
  deliberate choice.
- **Database.** Use Prisma's query builder (parameterized). Avoid `$queryRawUnsafe` or
  string-interpolated SQL.
- **CORS** is locked to `FRONTEND_URL` with credentials — don't widen it to `*`.
- **File uploads** go through `ParseFilePipeBuilder` (size/type validators). Keep limits and
  allowed types when adding upload endpoints.
- **Never disable a security-related lint rule or type check** to silence a warning — fix the
  underlying issue or ask.

## Gotchas

- **`swagger.json`, `client/src` and `client/dist` are generated and gitignored — never hand-edit
  them.** `npm run generate:swagger` boots the app to read the `@nestjs/swagger` decorators;
  `npm run client:build` runs it, then `@hey-api/openapi-ts` + `tsc`, and builds
  the client that `.github/workflows/api-client.yml` publishes to GitHub Packages (tags
  `api-client/vX.Y.Z` → `latest`, `main` → `next`, PRs → `pr-N`). Bump `client/package.json`
  `version` when the contract changes. The API contract is defined by controllers + DTOs + Swagger
  decorators; the frontend consumes `@naucto/api-client`. **Annotate new/changed endpoints**
  (`@ApiTags`, `@ApiOperation`, `@ApiResponse`, typed DTOs) or the generated client will be wrong.
- Swagger generation runs with a **stubbed env** (`tool/generate-swagger.ts`) so it works without
  real secrets. If generation breaks after adding a module that reads new env at construction
  time, add a stub there.
- The Prisma schema is **split** across `prisma/schema.prisma` + `prisma/models/*.prisma`. Edit
  the model files; let Prisma generate the migrations.
- `npm run lint` runs ESLint with `--fix` (it **modifies files**); the pre-commit hook only lints
  staged files — still run typecheck / build / test yourself before pushing.
- Country lookups read an IP-to-country database in MMDB format from `GEOIP_DB_PATH`. Mount it;
  never bake it into the image or commit it. DB-IP Lite (CC BY 4.0) needs the credit the privacy
  page gives. Without the file, every country is unknown.
- The text/plain body parser of the analytics routes is mounted under its own function name: Nest
  skips its own JSON parser when a middleware named `jsonParser` is already mounted, which a bare
  `express.json()` is, and every JSON body then arrives empty.

## Known incoherencies (being addressed in later phases — don't "fix" ad-hoc)

These are tracked cleanups; avoid partial migrations that make them worse.

- **Data model:** `prisma/models/user.prisma` carries a `// FIXME` to rename the
  `workSession`/`hostingSession` relations to `joined*`/`hosting*` after a merge.
