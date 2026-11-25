---
name: athena-js
description: >
  Runtime and package guide for `@xylex-group/athena` from packages/athena-js.
  Covers createClient construction and service routing (db/auth/chat/storage/billing),
  fluent queries/mutations/RPC/raw SQL, request context and headers, results/errors,
  auth client and admin/email helpers, React hooks, Next client/server façades,
  cookies and session bridges, organization helpers, billing subpath, utils/env/contracts,
  storage parity, browser-safe exports, CLI binary, docs tracks, tests, and release surfaces.
  Use when implementing or debugging Athena JS client call sites, subpath imports,
  export-map drift, session forwarding, query builders, or packages/athena-js/** changes.
  For Cloudflare D1/R2 edge, createCloudflareClient, createAthenaRuntime,
  createAthenaFromWorkerEnv, hybrid billing, D1 SQL compiler, or ADR 0015–0020, prefer
  $athena-js-cloudflare-edge-adapter. For generator config/output/CI, use $athena-js-generator.
  For table DSL, registries, fromModel, and model forms, use $athena-js-typed-schema-registry.
  For v2→v3 migration and removed constructors, use $athena-js-v3-migration.
  For Athena billing domain routes/webhooks outside the JS package, use $athena-billing.
  Use when the user runs /athena-js.
---

# Athena JS (`@xylex-group/athena`)

Package root in this monorepo: `packages/athena-js`.

Published name: **`@xylex-group/athena`**. Current package version is whatever
`packages/athena-js/package.json` reports (do not hardcode from this skill).

Work from the live checkout. Do not invent public APIs from memory, deep
`src/**` paths, or `dist/**` internals.

## Establish the contract

1. Read `packages/athena-js/package.json` for version, scripts, conditional
   exports, `typesVersions`, peers, bin, and publish files.
2. Read `packages/athena-js/tsup.config.ts` to separate **built entrypoints**
   from **published package subpaths**.
3. Read the matching public barrel in [references/export-map.md](references/export-map.md).
4. Read docs from `docs/index.md` (track map), then the seam-specific page
   (`getting-started.md`, `api-reference.md`, `complete-method-reference.md`,
   auth/storage/Next/cloudflare docs).
5. Read ownership in [references/implementation-map.md](references/implementation-map.md).
6. For React / Next / cookies / utils, read
   [references/framework-surface.md](references/framework-surface.md).
7. For client/query/auth/storage/billing invariants, read
   [references/runtime-surface.md](references/runtime-surface.md).
8. Open the closest `test/*.test.ts` (and examples under `examples/` /
   `test-sdk/`) before changing behavior.

When artifacts disagree:

| Authority | Wins for |
| --- | --- |
| `package.json` exports / `typesVersions` | consumer import paths |
| Selected entrypoint barrel (`src/index.ts`, `src/browser.ts`, …) | exported symbols |
| Concrete source implementation | runtime behavior |
| Focused tests | regression proof of the seam |
| Docs | onboarding and examples only — resync when the public contract changes |

Never recommend deep `src/*` or `dist/*` imports the export map does not publish.

Context7 library ID: `/xylex-group/athena-js`.

## Route the task

### Client construction, routing, context

- Materializer: `createClient(config)` in `src/v3-client.ts` (sole primitive;
  ADRs 0001 / 0014).
- Internal fluent core: `src/client.ts`.
- Stable namespaces on every client: `.db`, `.auth`, `.chat`, `.storage`,
  `.billing`, plus root shortcuts `.from` / `.rpc` / `.query` / `.request` /
  `.withContext` / `.capabilities`.
- Unified root `url` derives `/db`, `/auth`, `/chat`, `/chat/ws`, `/storage`.
  Explicit `db` / `auth` / `chat` / `storage` / `billing` objects override.
- Missing service routes still expose the namespace and fail on use with
  `AthenaConfigurationError` / `ATHENA_SERVICE_NOT_CONFIGURED`.
- Env alias catalogs: `src/env/index.ts` and `@xylex-group/athena/env`
  (`ATHENA_ENV_URL_KEYS`, `ATHENA_ENV_API_KEY_KEYS`, …). Pass `env` explicitly
  when alias resolution is wanted; do not invent new key lists in consumers.
- Edge drop-in (same constructor): `createClient({ db: { d1 }, storage: { r2 } })`.
  Detailed edge work → `$athena-js-cloudflare-edge-adapter`.

### Queries, mutations, RPC, results

Trace builder state → AST (`src/query-ast.ts`) → gateway payload
(`src/gateway/**`) → transport → normalized `{ data, error, count }`.

Preserve deferred thenable chains, single-execution memoization, model-aware
overloads, UUID-aware filters, and delete guards. Prefer direct result
destructuring and published helpers (`unwrap*`, `requireSuccess`,
`requireAffected`, `normalizeAthenaError`, `withRetry`) over app-local wrappers.
Use top-level `retryReads` (not an `experimental` bag).

### Auth, OAuth, admin, email

- Prefer `createClient(...).auth` over standalone wrappers; keep
  `createAuthClient` only where compatibility already exists.
- Bindings and routes: `src/auth/client.ts`, types in `src/auth/types.ts`.
- Server bootstrap: `src/auth/server.ts`.
- OAuth2 / JWKS / PKCE: `src/auth/oauth2/**`.
- Social providers: `src/auth/social-providers/**` and published
  `@xylex-group/athena/social-providers`.
- Admin limits and React Email: `src/auth/limits.ts`, `src/auth/react-email.ts`.
- Framework-agnostic admin helpers: `@xylex-group/athena/admin`.
- Org membership helpers: `@xylex-group/athena/organization`.
- Session / cookie / URL helpers live in utils, cookies, and Next barrels — do
  not re-copy magic numbers or cookie prefixes into apps.

### React, Next, cookies, session bridge

Keep adapters thin over `createClient`. Apps own singleton lifetime; do not
cache request-bound server clients.

| Subpath | Role |
| --- | --- |
| `@xylex-group/athena/react` | Athena-native query client, hooks, model-form helpers |
| `@xylex-group/athena/next/client` | `createAthenaBrowserClient`, bridge client helpers |
| `@xylex-group/athena/next/server` | `createAthenaServerClient`, bridge handlers, server context |
| `@xylex-group/athena/cookies` | Portable cookie parse/session store primitives |
| `@xylex-group/athena/utils` | Auth URL/routes/cookies, headers, origin, coercions, SQL literals |

Details: [references/framework-surface.md](references/framework-surface.md).

### Storage, chat, billing

Treat **module + live route JSON + client wiring + docs + parity tests** as one
contract:

- Storage: `src/storage/module.ts`, `storageLiveHttpRoutes`,
  `docs/storage/index.md`, `test/storage-*.test.ts`.
- Chat: `src/chat/**`.
- Billing: `src/billing/**`, published `./billing` subpath,
  `billingSdkManifest` / `billingLiveHttpRoutes`, `test/billing-*.test.ts`.
  Domain/server billing work outside this package → `$athena-billing`.

### Exports, browser safety, CLI, release

- Root package has a **conditional browser export** that maps `.` to
  `dist/browser.*` in browser conditions; explicit `./browser` is the same
  browser-safe surface.
- Node-only generator / Postgres introspection APIs throw explicit
  browser-unsupported errors on the browser entry (stubs in `src/browser.ts`).
- CLI binary: `bin/athena-js.js` → built `cli/index`; not a published consumer
  subpath unless `package.json.exports` says so.
- Changing a public entrypoint requires updating **exports + typesVersions +
  tsup entry + barrel + tests + docs** together.

### Generator / schema registry / migration / edge

| Concern | Skill |
| --- | --- |
| D1/R2, hybrid, capabilities, ADR 0015–0020 | `$athena-js-cloudflare-edge-adapter` |
| `athena-js generate`, config, CI, models layout | `$athena-js-generator` |
| table DSL, registries, model forms | `$athena-js-typed-schema-registry` |
| Removed v2 constructors / migration | `$athena-js-v3-migration` |
| Server billing routes / Mollie / grants | `$athena-billing` |
| Full monorepo implement playbook (overlap) | `$athena-jsm` |

Stay on this skill when those changes also touch root/browser exports, runtime
overloads, package build output, or cross-domain docs.

## Core rules

- Prefer additive changes unless removal is explicitly requested.
- One client type: `AthenaClient<TModels>`. One materializer: `createClient`.
- Next and Cloudflare helpers are **thin façades**, not a second core
  (ADRs 0014, 0016, 0019).
- No general-purpose `experimental` bag on the runtime client. Storage and
  billing are stable namespaces without enable flags. Generator may still use
  its own `experimental` config flags.
- Preserve unified-root routing, per-service overrides, and env alias catalogs.
- Preserve cookie + session-token and bearer + Athena-bearer header mirroring.
- Preserve `X-Athena-Client` / `X-Athena-Key` conventions.
- Keep gateway/auth/storage/chat/billing errors structured; normalize unknown
  throws only at boundaries.
- Derive consumer row/payload types from generated `athena/models/*` when
  present; do not clone contracts in the app.
- Reuse exported admin limits and package utils instead of app-local copies.
- Do not pass D1/R2 bindings into browser bundles.
- Keep generated method docs in sync via `pnpm docs:methods` when callables change.
- Site dual-publish: package docs sync into `apps/docs` via
  `pnpm docs:site:sync` / `docs:site:check` (see `docs/site-publish.md`).

## Docs track map (package-local)

Start at `packages/athena-js/docs/index.md`:

| Track | Topics |
| --- | --- |
| A Runtime | getting-started, api-reference, cloudflare-edge-local, headers, findMany AST, storage, contracts |
| B Next | next-js, ADR 0014, session bridge / forwarding |
| C Auth | auth/*.mdx, auth-client-bindings, cookies, routes, org membership, react-email |
| D Types | typed-schema-registry, type-surface-manifest, type-safety-playbook |
| E Generator | generator-quickstart/config/cicd, CLI reference |
| F Utils | utils-and-helpers |
| G Maintainers | ADRs 0001–0021, client-internal-architecture, site-publish |

ADRs live under `docs/adr/`. Edge cluster: 0015–0020. Contracts: 0021.

## Validation

Run the **narrowest** focused proof first, then widen:

| Seam | Gate |
| --- | --- |
| Client / builders / AST | matching `test/v3-client.test.ts`, `query-*.test.ts`, … |
| Auth / OAuth / providers | `test/auth-*.test.ts`, `oauth2-*.test.ts`, `social-providers.test.ts` |
| React | `test/react-*.test.ts` |
| Next / bridge / cookies | `test/next-*.test.ts`, `session-bridge.test.ts`, `cookies.test.ts` |
| Storage | `test/storage-*.test.ts` |
| Billing | `test/billing-client.test.ts`, `test/billing-contract-spine.test.ts` |
| Cloudflare | `test/cloudflare-*.test.ts` |
| Browser / exports | `test/browser-entry.test.ts`, type-compatibility checks |
| Types / public API | `pnpm typecheck` |
| Callable docs | `pnpm docs:methods` |
| Package completion | `pnpm check:all` (`lint` + `typecheck` + `test` + `build`) |

From package dir:

```bash
cd packages/athena-js
pnpm typecheck
pnpm test
pnpm build
pnpm check:all
```

Do not treat a green broad suite as a substitute for the focused regression that
proves the changed seam.

## Consumer repo rules

- Import only published subpaths from [references/export-map.md](references/export-map.md).
- Prefer object-form `createClient({ url, key, client, ... })`.
- Prefer Next façades in Next apps; prefer Worker façades / drop-in bindings in Workers.
- Keep generator output (`athena/models`, registries) as the type source of truth.
- If the bug is in the SDK, fix `packages/athena-js`; do not paper over it with
  a consumer wrapper unless explicitly temporary.
---

## Related skills

- `$athena-jsm` — deeper monorepo implement/inspect playbook for the same package
- `$athena-js-cloudflare-edge-adapter` — D1/R2 edge execution
- `$athena-js-generator` — schema generator / CLI generate
- `$athena-js-typed-schema-registry` — table DSL and registries
- `$athena-js-v3-migration` — breaking migration from v2
- `$athena-billing` — server-side billing domain
- `$athena-auth-emails` / `$athena-auth-runtime-contracts` — auth-service depth
- `$athena-storage` — server storage routes / S3 catalog
