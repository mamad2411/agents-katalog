---
name: follow-lib-effect-ts-use-platform
description: Effect Platform — FileSystem, Path, HttpServer/Client, Command, Terminal per runtime
argument-hint: "[package]"
related:
  - follow-lib-effect-ts
  - run-test
  - resolve-errors
---

## Goal

Use `@effect/platform-*` abstractions — FileSystem, Path, HttpServer/HttpClient, Command, Socket, Terminal — runtime-agnostically

## Scope

platform services (v3: `@effect/platform`, `platform-node`, `platform-bun`, `platform-browser`, `platform-node-shared`) — API-consistent services that are testable via Layer swap

## Execute

### 1. Install Per Runtime

```bash
bun i @effect/platform @effect/platform-bun      # Bun
# @effect/platform-node (Node), @effect/platform-browser (browser)
```

- Every service is a Tag — provide with the runtime layer: `BunContext.layer`, `NodeContext.layer`

### 2. Core Services

```ts
import { FileSystem, Path, Command, Terminal } from "@effect/platform"

const program = Effect.gen(function* () {
  const fs = yield* FileSystem.FileSystem
  const path = yield* Path.Path
  yield* fs.writeFileString(path.join(dir, "out.txt"), data)
  const term = yield* Terminal.Terminal
  yield* term.display("done\n")
})
```

### 3. HttpServer And HttpClient

```ts
// server: HttpServer.router + HttpServer.server.serve()
const HttpLive = HttpRouter.Default.pipe(Layer.provide(BunHttpServer.layer({ port: 3000 })))
// client: HttpClient.HttpClient — request/execute, Schema decode response
```

- `HttpClient` — request building, retries, `schemaBodyJson`/`schemaNoBody` decode integration
- `HttpServer` — router groups, middleware, multipart, websockets (support differs per runtime)

### 4. Command And Interop

- `Command.make("bun", "x", "tsc")` — spawn processes effectfully, stdout capture
- `Socket` — tcp/ws clients; `KeyValueStore` — KV abstraction (redis/fs/memory)

### 5. Testability

- Platform services are mockable via Layer — `FileSystem` has `FileSystem.layerNoop`/test impls
- Don't import `fs`/`path` directly inside Effect code — always go through platform services

## Rules

- Install the platform package **matching the runtime** — `platform-node` ≠ `platform-bun` context layers
- All IO (fs/http/process) goes through platform services — substitute with Layers in tests
- Reuse the `HttpClient` instance — don't call `fetch` directly when inside the effect world
- Check the runtime support matrix — some services (Terminal, Socket) don't exist on some platforms

## Expected Outcome

- IO fully via platform services, runtime layer provided at the boundary
- Testable through Layer swap — no mocking module imports
