---
name: use-neemata
description: 'Answer questions about the Neemata framework and help build RPC-based applications with bidirectional streaming, dependency injection, and multi-runtime support. Use when developers: (1) Ask about Neemata APIs like n.procedure, n.router, n.rootRouter, n.app, n.server, n.guard, n.guardFactory, n.middleware, n.factory, (2) Want to build RPC servers, streaming endpoints, background jobs, or type-safe clients, (3) Have questions about dependency injection scopes, transports (WS/HTTP), contracts, blobs, typed guards, or the protocol layer, (4) Use the nmtjs package or @nmtjs/* packages including @nmtjs/client, @nmtjs/ws-client, and @nmtjs/http-client. Triggers on: "neemata", "nmtjs", "@nmtjs/client", "StaticClient", "RuntimeClient", "WsTransportClient", "HttpTransportClient", "n.procedure", "n.router", "n.rootRouter", "n.app", "n.server", "createProcedure", "RPC framework", "ProtocolBlob", "t.object", "c.procedure", "n.guard", "n.guardFactory", "typed guard", "n.middleware", "n.factory", "defineApplication", "defineServer", "defineConfig".'
---

## Prerequisites

Before working with a Neemata project, check whether the relevant public
packages are installed:

- Server / application definitions: `node_modules/nmtjs`
- Client runtime: `node_modules/@nmtjs/client`

For server-side code, prefer the `nmtjs` umbrella package. Do not install most
internal `@nmtjs/*` packages directly for application/router/DI usage. Server
transport packages (`@nmtjs/ws-transport`, `@nmtjs/http-transport`) remain
separate dependencies for application definitions:

```bash
pnpm add nmtjs @nmtjs/ws-transport @nmtjs/http-transport
```

For client-side usage, install:

```bash
pnpm add @nmtjs/client @nmtjs/ws-client @nmtjs/json-format
# or
pnpm add @nmtjs/client @nmtjs/http-client @nmtjs/json-format
```

## Finding Documentation

Search source code in `node_modules/nmtjs/`:

- **Public API**: `grep -r "query" node_modules/nmtjs/src/`
- **Client API**: `grep -r "query" node_modules/@nmtjs/client/src/`
- **Client transports**: `grep -r "query" node_modules/@nmtjs/ws-client/ node_modules/@nmtjs/http-client/`
- **Core DI**: `grep -r "query" node_modules/@nmtjs/core/src/`
- **Contract types**: `grep -r "query" node_modules/@nmtjs/contract/src/`
- **Type system**: `grep -r "query" node_modules/@nmtjs/type/src/`
- **Protocol**: `grep -r "query" node_modules/@nmtjs/protocol/src/`

## Key Concepts

### Import Convention

Server-side Neemata APIs should import from `nmtjs`:

```ts
import { n, t, c, Scope, ErrorCode, ProtocolBlob, ConnectionType } from 'nmtjs'
```

- `n` — Namespace with all builder functions (`n.procedure`, `n.router`, `n.app`, `n.server`, etc.)
- `t` — Type system (wraps zod/mini with encode/decode, e.g., `t.string()`, `t.object()`, `t.date()`)
- `c` — Contract definitions (`c.procedure()`, `c.router()`, `c.event()`, `c.blob()`)
- `Scope` — DI scopes: `Global`, `Connection`, `Call`, `Transient`

### Architecture

Neemata uses a layered architecture:

1. **Config** (`neemata.config.ts`) — defines applications and server entry point via `defineConfig()`
2. **Server** (`n.server()`) — orchestrates workers, proxy, store, metrics
3. **Application** (`n.app()`) — defines transports, router, guards, middleware for one app
4. **Router** (`n.rootRouter()` / `n.router()`) — groups procedures
5. **Procedure** (`n.procedure()`) — individual RPC endpoint with input/output types and handler
6. **Client** (`StaticClient` / `RuntimeClient`) — type-safe RPC calls via `@nmtjs/client`

### Dependency Injection Scopes

- `Scope.Global` — Singleton, lives for entire app lifetime
- `Scope.Connection` — Per WebSocket/HTTP connection, disposed on disconnect
- `Scope.Call` — Per RPC call, disposed after handler completes
- `Scope.Transient` — New instance on every injection

Containers form a hierarchy: `Global → Connection → Call`. A scope can only depend on same-or-higher scopes.

### Streaming

Two streaming mechanisms:

- **RPC Streams** — Procedure returns `AsyncIterable`, set `stream: true`. Client consumes via `client.stream.*`
- **Blob Streams** — Binary data via `ProtocolBlob.from()` (client) and `createBlob` injectable (server). Use `c.blob()` in contracts

## When Typecheck Fails

1. Check the relevant reference for correct usage:
  - [RPC](references/rpc.md), [Injectables](references/injectables.md),
  - [Server Setup](references/server-setup.md), [Client](references/client-usage.md)
2. Check [API Quick Reference](references/api-reference.md) for correct signatures
3. Search `node_modules/nmtjs/src/` for current type definitions
4. Verify you're importing from the correct public package:
   - server/application code → `nmtjs`
   - client runtime code → `@nmtjs/client`, `@nmtjs/ws-client`, `@nmtjs/http-client`

## Project Structure

A typical Neemata project follows this structure:

```
project/
  neemata.config.ts              # defineConfig — app entries + server path
  src/
    index.ts                     # n.server({...}) — server configuration
    applications/
      main/
        index.ts                 # n.app({...}) — application definition
        router.ts                # n.rootRouter([routerA, routerB] as const) — route tree
        procedures/
          example.ts             # n.procedure({...}) — RPC handlers
        guards/
        middleware/
        injectables/
```

## References

- [API Quick Reference](references/api-reference.md) — Function signatures and options for `n.*`, `t.*`, `c.*` APIs
- [Type System](references/type-system.md) — `t.*` encode/decode modes, inference, and Standard Schema (JSON Schema) support
- [RPC](references/rpc.md) — Procedures, routers, streaming, blobs, contracts, guards, middleware, filters, error handling
- [Injectables](references/injectables.md) — DI scopes, injectable builders (value/lazy/factory), built-in `n.inject.*`
- [Server Setup](references/server-setup.md) — `n.app()`, `n.server()`, `defineConfig()`, project structure
- [Client Usage](references/client-usage.md) — `StaticClient` setup, RPC calls, streams, blobs, abort
- [Jobs](references/jobs.md) — Background jobs, steps, job manager, retry/backoff, progress, job router
