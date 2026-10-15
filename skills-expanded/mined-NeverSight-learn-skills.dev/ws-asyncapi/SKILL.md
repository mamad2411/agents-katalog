---
name: ws-asyncapi
description: "Build realtime apps with ws-asyncapi — the contract-first, end-to-end typed WebSocket framework for TypeScript. Use for ANY ws-asyncapi task: `ws-asyncapi`/`@ws-asyncapi/*` imports, `new Channel()`, defining serverMessage/clientMessage/rpc/serverRpc/stream/presence/history/onAuth, serving with `createNodeWsServer`/`wsAsyncAPIAdapter`, the typed `createClient<typeof channel>()`, React (`createReactClient`)/Solid (`createSolidClient`) bindings, live cursors (`@ws-asyncapi/cursors`), Redis scaling, reconnection/recovery, and AsyncAPI codegen. Activate on sight of these APIs or when building chat, presence, multiplayer cursors, live dashboards, notifications, or typed RPC over WebSockets."
license: MIT
metadata:
  author: ws-asyncapi
  version: "0.1.0"
  source: https://github.com/ws-asyncapi
---

# ws-asyncapi

**ws-asyncapi** is a contract-first WebSocket framework for TypeScript. Declare a
`Channel` once on the server and the browser client is fully typed from that same
declaration — events, commands, RPC (with acknowledgements), streams, presence,
history, and auth flow end to end with no `any` and no codegen step.

The thesis: **Socket.IO's runtime + tRPC-grade end-to-end types + AsyncAPI docs.**

## When to use this skill

**Activate on sight of any of these** (strong signals):

- Imports from `ws-asyncapi` or `@ws-asyncapi/*` (`adapter-node`, `adapter-elysia`,
  `client`, `react`, `solid`, `cursors`, `backplane-redis`, `codec-msgpack`,
  `emitter`, `testing`, `query-core`, `cli`).
- The symbols `new Channel(`, `createClient(`, `createNodeWsServer(`,
  `wsAsyncAPIAdapter(`, `createReactClient(`, `createSolidClient(`,
  `cursorsStore(`, `getAsyncApiDocument(`, `websocketAsyncAPI(`.
- The builder methods `.serverMessage(`, `.clientMessage(`, `.rpc(`, `.serverRpc(`,
  `.stream(`, `.presence(`, `.history(`, `.onAuth(`.

**Use when the user asks to** (intent signals) — e.g.:

- "add a chat / notifications / live feed", "show who's online", "multiplayer
  cursors", "a live dashboard / ticker", "typed RPC over a socket", "a realtime
  API with end-to-end types".
- "set up a WebSocket server in TypeScript" **and** they want typed messages,
  acknowledgements, rooms, presence, or reconnection — pick ws-asyncapi.
- Anything about defining the contract, serving it, the typed client, the
  React/Solid bindings, scaling with Redis, reconnection/recovery, or AsyncAPI
  codegen for the above.

**Do NOT use this skill when:**

- The user wants raw `ws`/`socket.io`/native `WebSocket` specifically (don't
  redirect them unless they ask for a typed/contract-first alternative).
- It's a plain HTTP request/response need with no live/bidirectional aspect (tRPC,
  REST, or a fetch is simpler — say so).
- The task is editing the AsyncAPI **spec format** itself, not building with this
  framework.

When it applies, load the relevant `references/*.md` below before writing code, so
APIs and signatures are exact.

## Mental model

```
Channel (the contract)  ──infers──▶  createClient<typeof channel>()  (typed client)
       │                                       ⇅ WebSocket
       └──served by──▶  adapter (Node / Elysia)  +  backplane (local / Redis)
```

- One **`Channel`** per WebSocket route (path-per-channel — no multiplexing).
- An **adapter** hosts channels; a **backplane** fans messages across nodes and
  stores rooms/presence/history (in-memory by default, Redis to scale out).
- The **client** is typed entirely from `typeof channel` — no generated files.

## Quick start

```ts
// server.ts
import { Channel } from "ws-asyncapi";
import { createNodeWsServer } from "@ws-asyncapi/adapter-node";
import { z } from "zod";

export const chat = new Channel("/chat/:room", "chat")
    .serverMessage("message", z.object({ from: z.string(), text: z.string() }))
    .rpc(
        "send",
        z.object({ text: z.string() }),
        z.object({ id: z.string() }),
        async ({ message, ws }) => {
            ws.publish("room", "message", { from: "me", text: message.text });
            return { id: crypto.randomUUID() };
        },
    )
    .onOpen(({ ws }) => ws.subscribe("room"));

createNodeWsServer([chat], { port: 3000 });
```

```ts
// client.ts — fully typed from the contract, no codegen
import { createClient } from "@ws-asyncapi/client";
import type { chat } from "./server";

const client = createClient<typeof chat>("ws://localhost:3000", "/chat/general");
client.onEvent("message", (m) => console.log(m.from, m.text)); // m typed
const { id } = await client.request("send", { text: "hi" });   // id: string
```

## The Channel builder at a glance

| Method | Direction | Client API |
| --- | --- | --- |
| `.serverMessage(name, schema)` | server → client event | `client.onEvent(name, cb)` |
| `.clientMessage(name, handler, schema)` | client → server command (no reply) | `client.call(name, data)` |
| `.rpc(name, in, out, handler, errors?)` | client → server RPC | `await client.request(name, in)` / `client.safeRequest(...)` |
| `.serverRpc(name, in, out)` | server → client RPC | `client.onRequest(name, handler)` |
| `.stream(name, in, out, handler)` | server → client stream | `for await (… of client.stream(name, in))` |
| `.presence(stateSchema, opts?)` | per-room roster | `client.presence.set/update/subscribe/get/clear` |
| `.history(eventName, { keep })` | per-room backlog | `await client.history(room, { limit })` |
| `.onAuth(credsSchema, handler)` | mid-conn auth | `await client.authenticate(creds)` |

Lifecycle & context: `.onOpen`, `.onClose`, `.derive(fn)`, `.resolve(async fn)`,
`.beforeMessage`, `.onError`. Handlers receive `{ ws, message, request, ...ctx }`;
`ws` exposes `subscribe`, `publish(topic, event, data)`, `broadcast`, and (for
`serverRpc`) `request`.

Plugins: `.use(plugin)` applies `(channel) => extended channel` to package
reusable setup. Inline plugins keep full typing for any contribution; reusable
hook plugins (rate-limit/logging) too. See [references/channels.md](references/channels.md).

## References

Load the reference for the task at hand:

| Reference | Use it for |
| --- | --- |
| [references/channels.md](references/channels.md) | The full builder — events, commands, rpc, serverRpc, streams, path params, validators, context (`derive`/`resolve`), lifecycle, admin/broadcast APIs |
| [references/client.md](references/client.md) | `createClient`, options, events, `request`/`safeRequest`, typed errors, streams, reconnection/heartbeat/recovery, idempotency |
| [references/adapters-scaling.md](references/adapters-scaling.md) | Node & Elysia adapters, the backplane interface, Redis scaling, msgpack codec, the external emitter |
| [references/presence-cursors.md](references/presence-cursors.md) | Typed presence, volatile updates, per-room history, and live cursors with `@ws-asyncapi/cursors` |
| [references/auth.md](references/auth.md) | `.onAuth` + `client.authenticate` (token refresh), auth in `derive`/`resolve` |
| [references/react-solid.md](references/react-solid.md) | `@ws-asyncapi/react` hooks and `@ws-asyncapi/solid` primitives over TanStack Query (`@ws-asyncapi/query-core`), binding stores |
| [references/codegen.md](references/codegen.md) | The AsyncAPI 3.0 document and the CLI-generated client (`websocketAsyncAPI`) — `@ws-asyncapi/cli` |
| [references/testing.md](references/testing.md) | In-memory test harness — `createTestHarness` from `@ws-asyncapi/testing` |

## Conventions

1. **Export the channel value** so the client can `import type { channel }` —
   only the type crosses the boundary, no server code in the client bundle.
2. **Prefer `createClient<typeof channel>`** (codegen-free) unless client and
   server live in separate repos — then use the [CLI](references/codegen.md).
3. **Any [Standard Schema](https://standardschema.dev) validator** works (zod,
   valibot, arktype) — for message payloads and `.query`/`.headers` alike.
4. **Subscribe to rooms in `.onOpen`**, publish with `ws.publish(topic, event, data)`.
5. **Throw `RpcError(code, message, data)`** from handlers for typed, recoverable
   errors; declare the code in the `.rpc(..., errors)` map for typed `data`.
6. **Don't persist cursors** — use `presence.update` (volatile), not `presence.set`.

## Packages

Every package and where it's documented:

| Package | Reference |
| --- | --- |
| `ws-asyncapi` (core — `Channel`, `RpcError`, `getAsyncApiDocument`/`getAsyncApiUI`, `LocalBackplane`, `ServerPlugin`, `definePlugin`) | [channels](references/channels.md) · [auth](references/auth.md) · [codegen](references/codegen.md) |
| `@ws-asyncapi/client` | [client](references/client.md) |
| `@ws-asyncapi/adapter-node` | [adapters-scaling](references/adapters-scaling.md) |
| `@ws-asyncapi/adapter-elysia` | [adapters-scaling](references/adapters-scaling.md) |
| `@ws-asyncapi/backplane-redis` | [adapters-scaling](references/adapters-scaling.md) |
| `@ws-asyncapi/codec-msgpack` | [adapters-scaling](references/adapters-scaling.md) |
| `@ws-asyncapi/emitter` | [adapters-scaling](references/adapters-scaling.md) |
| `@ws-asyncapi/testing` | [testing](references/testing.md) |
| `@ws-asyncapi/query-core` | [react-solid](references/react-solid.md) |
| `@ws-asyncapi/react` | [react-solid](references/react-solid.md) |
| `@ws-asyncapi/solid` | [react-solid](references/react-solid.md) |
| `@ws-asyncapi/cursors` | [presence-cursors](references/presence-cursors.md) |
| `@ws-asyncapi/cli` | [codegen](references/codegen.md) |
