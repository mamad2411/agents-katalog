---
name: athena-js-v3-migration
description: Migrate applications, packages, examples, or tests from Athena JS 2.16.x to Athena JS 3.0.1. Use when a task mentions removed constructors such as `createClient(url, key, options)`, `AthenaClient.builder()`, `AthenaClient.fromEnvironment()`, `createTypedClient(...)`, `createAuthClient(...)`, legacy types like `AthenaSdkClient*` or `TypedAthenaClient`, old flags like `experimental` or `typecheckColumns`, or Next adapter and request-scoped client confusion involving `createAthenaBrowserClient(...)`, `createAthenaServerClient(...)`, `resolveAthenaServerContext(...)`, `useAthenaSessionClient(...)`, session bridge / session forwarding, or guessed aliases like `createServerAthenaClient` and `createBrowserClient`. Use when the user runs /athena-js-v3-migration.
---

# Athena JS V2 To V3 Migration

## Overview

Use this skill to convert Athena JS v2 construction, config, env, context, and
typing seams onto the v3 unified `createClient({ ... })` contract, including the
3.0.1 Next adapter surface. Keep the migration centered on the real
construction boundary first, then clean up request scope, removed types, and
validation.

Read [references/migration-guide.md](references/migration-guide.md) immediately
for the concrete symbol mapping, code examples, search commands, and validation
checklist.

Read [references/next-adapters.md](references/next-adapters.md) when the task
primarily involves Next.js App Router, browser/server adapter callsites,
request-scoped client construction, session bridge / session forwarding,
`resolveAthenaServerContext(...)`, `resolveNextRequestContext(...)`, or
`useAthenaSessionClient(...)`.

## Workflow

1. Inventory every Athena client construction seam before editing.
2. Replace all removed v2 constructors with `createClient({ ... })`.
3. Convert env and service configuration onto the explicit v3 contract.
4. Replace legacy client types and request-scoped wrapper patterns.
5. Normalize Next adapter imports and request/session boundaries onto the published 3.0.1 subpaths.
6. Run the narrowest focused validation that proves the migrated seam.

## Migration Order

1. Find construction callsites and client annotations first.
2. Migrate the shared app-owned env resolution seam next.
3. Decide whether a given Next callsite should use root `createClient(...)` + `withContext(...)` or the published `@xylex-group/athena/next/*` facades.
4. Move server request code to `withContext(...)` or `createAthenaServerClient(...)` instead of rebuilding or caching request-bound clients.
5. Remove deleted flags, builder states, and capability-specific types only after the construction seam is stable.
6. Keep generator-specific or typed-schema-registry-specific follow-ups routed to the existing Athena JS generator or typed-registry skills when that becomes the primary task.

## Rules

- Treat `createClient({ ... })` as the single runtime-neutral constructor.
- Treat `createAthenaBrowserClient(...)` and `createAthenaServerClient(...)` as thin published facades over `createClient(...)`, not as removed APIs and not as a second client core.
- For Workers/D1/R2, migrate onto drop-in backends `createClient({ db: { d1 }, storage: { r2 } })` (not a parallel product API). Thin helpers: `createCloudflareClient` / `createAthenaRuntime`. Details: `$athena-js-cloudflare-edge-adapter` and ADRs 0015–0020.
- Do not invent aliases such as `createServerAthenaClient` or `createBrowserClient`; use the published names from `@xylex-group/athena/next/client` and `@xylex-group/athena/next/server`.
- Do not assume Athena JS 3 reads global `process.env`; pass `env` explicitly when env-backed resolution is intended.
- Keep browser config limited to intentionally public variables.
- Prefer one immutable app-level client per key/config set and derive request-scoped views with `withContext(...)`.
- Do not cache the result of `createAthenaServerClient(...)` across requests.
- Replace legacy client identities with `AthenaClient<TModels>`.
- Preserve raw `client.request(...)` usage for uncovered routes instead of inventing wrapper fetches.
- When the app also uses Athena Auth packages, prefer exact coordinated pins during the migration.

## Validation

- Start with the focused search set in [references/migration-guide.md](references/migration-guide.md).
- Validate the exact migrated seam first: focused tests, typecheck, then the package or app build if needed.
- Do not trust a broad repo failure if the targeted migration seam already passes and the remaining errors are unrelated baseline issues.
