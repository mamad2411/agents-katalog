---
name: athena-client-instantiation-migration
description: Migrate Athena client construction off local createClient wrappers onto the published browser/server/auth/query adapter surfaces, and document the blast radius for server, client, auth, and query seams. Use when the user asks about athena client instantiation migration, needs to implement or review athena client instantiation migration code, or runs related commands.
---

# Athena Client Instantiation Migration

Use this skill when a task mentions `createClient(...)`, `createAthenaBrowserClient(...)`, `createAthenaServerClient(...)`, `resolveAthenaServerContext(...)`, `createAthenaAuthClient(...)`, `createAthenaServerAuthClient(...)`, `createAthenaAuthProxyHandlers(...)`, `createAthenaQueryClient(...)`, Athena `select`/`findMany` reads, raw `query(...)` calls, RPC calls, or auth methods, especially when the goal is to collapse local wrappers into the published Athena adapter split.

## Workflow

1. Inventory all Athena-backed seams first.
2. Separate real instantiations and query/auth callsites from consumers like `useSession(...)`.
3. Group work into four tracks:
   - `[server]` request-scoped server clients
   - `[client]` browser-only clients
   - `[auth]` direct auth-origin bridging and session persistence
   - `[query]` query-provider setup, reads, RPC, and hydration boundaries
4. Prefer the published adapter over repo-local `createClient(...)` wrappers when the newer surface already covers the use case.
4b. On Cloudflare Workers, prefer drop-in `createClient({ db: { d1 }, storage: { r2 } })` (or thin `@xylex-group/athena/cloudflare` façades) over app-local D1 clients. See `$athena-js-cloudflare-edge-adapter`.
5. Add short `TODO.. <LINEAR-ID>` comments above the exact function or singleton that should be migrated.
6. Write a markdown report that lists:
   - the published constructor surface
   - the repo-local callsites
   - the query/auth callsites by side and intent
   - the highest-value migration order
   - the blast-radius risks

## Heuristics

- Treat wrapper functions that only forward options as cleanup candidates.
- Keep server-only auth and session assembly on the server.
- Keep browser clients free of request-scoped server plumbing.
- Keep query client creation at the provider boundary unless the wrapper adds real behavior.
- Classify each query callsite before editing it: safe builder, hard query, RPC, raw query, or auth method.

## Validation

- Verify the installed package docs before claiming a constructor exists.
- Run the narrowest useful tests around auth, query, and server session seams.
- If a migration affects auth round-trips, cover the exact callback or bridge path rather than relying on generic login tests.
