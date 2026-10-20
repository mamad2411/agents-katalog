---
name: athena-jsm
description: Implement, integrate, inspect, debug, document, test, or release `@xylex-group/athena` from `packages/athena-js/**`. Use for client construction and service routing; fluent table queries, mutations, RPC, raw requests, AST/debug traces, results and errors; auth clients, server bootstrap, sessions, admin/email helpers, OAuth2 and social providers; React hooks, Next client/server adapters, cookies and session bridges; storage, chat, organization, billing, utilities, exports, package subpaths, compatibility, docs, examples, tests, and release surfaces. Billing includes the published `@xylex-group/athena/billing` subpath, `billingSdkManifest`, `billingLiveHttpRoutes`, and `v3-client` billing namespace wiring. For Cloudflare D1/R2 edge adapter, createClient({ db: { d1 }, storage: { r2 } }), createCloudflareClient, createAthenaRuntime, hybrid billing, D1 SQL compiler, or ADR 0015–0020, prefer `$athena-js-cloudflare-edge-adapter`. Use `$athena-billing` when the task is primarily about Athena billing routes, webhook ingestion, canonical billing tables, grants, or provider adapters. Use `$athena-js-generator` for generator pipeline/config/output work and `$athena-js-typed-schema-registry` for table DSL and schema type-system work. Use when the user runs /athena-jsm.
---

# Athena JS

Work from the current `packages/athena-js` checkout. Do not infer the public API from internal files or remembered versions.

## Establish the contract

1. Read `package.json` for version, scripts, conditional exports, subpaths, peers, and publish files.
2. Read `tsup.config.ts` to distinguish built entrypoints from published package subpaths.
3. Read the matching public barrel listed in [references/export-map.md](references/export-map.md).
4. Read the relevant docs from `docs/index.md`, `docs/api-reference.md`, and `docs/complete-method-reference.md`.
5. Read the implementation family in [references/implementation-map.md](references/implementation-map.md).
6. Read [references/framework-surface.md](references/framework-surface.md) when the task touches `@xylex-group/athena/react`, `@xylex-group/athena/next/*`, `@xylex-group/athena/cookies`, `@xylex-group/athena/utils`, or app-host session bridge behavior.
7. Read the closest focused tests and examples before changing behavior.

When artifacts disagree:

- Treat `package.json` as authoritative for consumer imports.
- Treat the selected entrypoint barrel as authoritative for exported symbols.
- Treat concrete source as authoritative for runtime behavior.
- Bring docs, tests, examples, export maps, and build entries back into sync when changing a public contract.
- Never recommend deep `src` or `dist` imports that the manifest does not publish.

Use [references/runtime-surface.md](references/runtime-surface.md) for client/query/auth invariants and validation routing.

## Route the task

### Client, routing, and request context

Start at `src/v3-client.ts` / `src/client.ts`. Preserve canonical unified-root construction, direct service overrides, immutable `withContext`, and request header/auth propagation across DB, auth, chat, storage, and billing. Use `client.request(...)` for unwrapped routes instead of adding consumer fetch wrappers.

**Cloudflare edge / D1 / R2:** drop-in backends are `createClient({ db: { d1 }, storage: { r2 } })`. Do not invent a second client core. For transport, SQL compiler, hybrid billing, capabilities, runtime façades, and ADRs 0015–0020, load `$athena-js-cloudflare-edge-adapter` and edit `src/cloudflare/**` + `materializeEdgeBindings` in `v3-client.ts`.

### Queries, mutations, RPC, and results

Trace builder state, AST construction, gateway payload serialization, transport, and normalized result/error handling together. Preserve deferred thenable execution and single-request memoization. Keep model-aware overloads additive and derive consumer types from generated Athena models when available.

### Auth, OAuth, providers, and admin

Start with `src/auth/client.ts`, then the exact binding/type or OAuth/provider module. Preserve route compatibility, token body/authentication requirements, awaited fetch hooks, redirect rejection, PKCE/JWKS verification, provider-specific profile contracts, session forwarding, admin limits, and React Email template metadata. Patch the named provider seam instead of broad auth rewrites.

### React, Next, cookies, and session bridges

Keep React runtime state framework-light and browser-safe. Trace providers, query client, hooks, session-bound clients, Next client/server adapters, bridge payload/handlers/cookies, request-scoped headers, auth route helpers, auth URL helpers, and cookie wipe helpers together. Preserve React singleton compatibility and server/client boundaries.

When the task is adapter-specific:

- `@xylex-group/athena/next/client`: browser facade, bridge client helpers, auth route helpers, auth URL helpers, cookie wipe helpers.
- `@xylex-group/athena/next/server`: request-scoped server facade, request-context resolvers, session bridge handlers/path helpers, cookie detection.
- `@xylex-group/athena/react`: query client/provider, `useQuery`, `useMutation`, `useSession`, `useAthenaSessionClient`, storage hooks, model-form helpers.
- `@xylex-group/athena/cookies`: portable cookie parsing, session token lookup, session stores, request-cookie mutation.
- `@xylex-group/athena/utils`: auth URLs/routes/cookies, request/origin/header helpers, coercion helpers, SQL literal helpers, dynamic-server guards.

Use [references/framework-surface.md](references/framework-surface.md) before editing those surfaces.

### Storage, chat, organization, or utilities

Treat module types, manifest methods, client namespace binding, docs, and route-parity tests as one contract. Reuse shared auth URL, route, cookie, origin, header, coercion, SQL literal, and environment utilities rather than duplicating them.

### Billing SDK subpath and namespace

Start with `src/billing/index.ts`, `src/billing/module.ts`, `src/v3-client.ts`, and the matching `test/billing-*.test.ts` coverage. Keep the published `./billing` subpath, root/browser re-exports, `billingSdkManifest`, `billingLiveHttpRoutes`, and the Rust live inventory synchronized. Preserve static-admin-key headers, `connectionId` query conventions, provider webhook raw-body handling, `jwt_secret` debug query support, and explicit envelope/error parsing. If the change is mainly about Athena billing domain behavior outside the JS package, use `$athena-billing` too.

### Exports, browser safety, and release

Update manifest exports, `typesVersions`, `tsup` entries, source barrels, browser stubs or exclusions, tests, and docs together. A built CLI entry is not automatically a published package subpath. Keep Node-only introspection/generator behavior out of browser bundles while preserving compatible exported types and explicit unsupported-runtime failures.

## Ownership boundaries

- Use `$athena-js-cloudflare-edge-adapter` for D1/R2 edge transport, hybrid routing, capabilities, SQL compiler, and `@xylex-group/athena/cloudflare` façades.
- Use `$athena-js-generator` for generator config discovery, providers, filtering, naming, renderer output, CLI generate flows, CI/CD, and `athena/models` layouts.
- Use `$athena-js-typed-schema-registry` for `table`, column builders, `defineModel`, registries, typed clients, model targets, model forms, and compile-time schema inference.
- Keep this skill involved when those changes also alter root/browser exports, runtime client overloads, package build output, or cross-domain docs.

## Core rules

- Keep changes additive unless removal is explicitly requested.
- Preserve the root conditional browser export and explicit `/browser` behavior.
- Prefer `createClient(...).auth` over new standalone auth wrappers while maintaining `createAuthClient` compatibility.
- Treat `createAthenaBrowserClient(...)` and `createAthenaServerClient(...)` as published thin facades over `createClient(...)`, not as a second client core.
- Treat `createCloudflareClient` / `createAthenaRuntime` / `createAthenaFromWorkerEnv` as thin façades over `createClient({ db: { d1 }, storage: { r2 }, ... })` (ADR 0016 / 0019).
- Preserve direct service overrides and legacy URL aliases.
- Preserve request-scoped user, organization, bearer, session-token, cookie, and no-cache propagation.
- Do not invent new app-local aliases for published Next helpers when the package already exports them.
- Keep `@xylex-group/athena/react`, `@xylex-group/athena/next/*`, `@xylex-group/athena/cookies`, and `@xylex-group/athena/utils` aligned with the generated method docs and package barrels.
- Keep gateway/auth/storage/chat errors structured and normalize unknown thrown values only at boundaries.
- Await async auth fetch hooks before downstream consumers inspect mutated state.
- Respect provider-specific token authentication; do not force a universal OAuth body shape.
- Reuse exported auth/admin limits instead of copying numbers into consumers.
- Keep session bridge constants, payload extraction, browser POST/DELETE helpers, route handlers, path filters, and cookie name variants synchronized.
- Keep React hook return contracts, provider/query-client exports, and session-derived scoped-client behavior additive and browser-safe.
- Keep storage/chat manifests, namespace implementations, docs, and parity tests synchronized.
- Keep billing manifests, JS live-route mirrors, browser/root exports, and contract-spine tests synchronized.
- Keep generated method docs and public docs synchronized with callable runtime methods.

## Validation

Run the narrowest focused Node test from `test/*.test.ts`, then `pnpm typecheck` for type/public changes. Use `pnpm build` for entrypoints and declarations, browser-entry tests for browser safety, route-parity tests for service namespaces, `test/billing-client.test.ts` plus `test/billing-contract-spine.test.ts` for billing surfaces, Next/React/cookie tests for adapters and helpers, and `pnpm check:all` for package-facing completion. Run `pnpm docs:methods` when callable method documentation changes.

Do not use broad checks as a substitute for the focused regression that proves the changed seam.
