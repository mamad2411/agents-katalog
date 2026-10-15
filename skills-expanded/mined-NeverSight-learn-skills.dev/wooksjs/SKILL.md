---
name: wooksjs
description: >-
  Use this skill when working with the wooksjs monorepo or any @wooksjs package.
  Covers @wooksjs/event-core (EventContext, key/cached/cachedBy slots, defineWook
  composables, defineEventKind, AsyncLocalStorage propagation, useRouteParams,
  useEventId, useLogger), @wooksjs/event-http (createHttpApp, HTTP routing,
  useRequest, useHeaders, useCookies, useUrlParams, useAuthorization, useAccept,
  useResponse, HttpResponse, HttpError, prepareTestHttpContext),
  @wooksjs/event-cli (createCliApp, command routing, useCliOptions, useCliOption,
  useCliHelp, useAutoHelp), @wooksjs/event-ws (WooksWs, onMessage, onConnect,
  onDisconnect, useWsConnection, useWsMessage, useWsRooms, useWsServer,
  WsRoomManager, WsBroadcastTransport, WsError), @wooksjs/event-wf (createWfApp,
  workflow steps and flows, useWfState, pause/resume, conditions, loops, string
  handlers, StepRetriableError, outlets), @wooksjs/ws-client (createWsClient,
  WsClient, send, call, subscribe, on, reconnection, RPC, push listeners,
  WsClientError).
---

# wooksjs

Typed composable framework for Node.js. Every piece of request/event data is accessed through composable functions — no `req`/`res` parameters, no middleware chains. Context is propagated via `AsyncLocalStorage`, so composables work transparently across async boundaries.

Adapters: HTTP, CLI, WebSocket, Workflows. Plus a standalone WebSocket client.

## Architecture

### Composable pattern

All public API is accessed through composable functions created with `defineWook(factory)`. Each composable is cached per event context — call it multiple times, get the same result:

```ts
import { defineWook } from '@wooksjs/event-core'

export const useFoo = defineWook((ctx) => ({
  bar: () => ctx.get(someSlot),
}))
```

### Slot system

Typed context slots avoid stringly-typed lookups:

- `key<T>(name)` — writable slot
- `cached<T>(fn)` — lazy-computed, cached per context
- `cachedBy<K,V>(fn)` — lazy-computed, keyed by first argument
- `slot<T>()` — schema marker for `defineEventKind`

### EventContext + AsyncLocalStorage

Every event gets an `EventContext` — a typed slot container propagated via `AsyncLocalStorage`. Composables call `current()` to get it without parameter passing. Supports parent context chains for nested events (e.g. HTTP request spawning a workflow).

### Dependency chain

```
event-core  <-  wooks  <-  adapters (event-http, event-cli, event-ws, event-wf)
                                 ^
                                 |--- utilities (http-body, http-static, http-proxy)

ws-client (standalone, no event-core dependency)
```

## How to use this skill

Read the reference file that matches the task. Do not load all files — only what is needed.

| Domain            | File                                              | Load when...                                                     |
| ----------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| Routing           | [router.md](references/router.md)                 | Route patterns, params, wildcards, regex, path builders, config  |
| Context engine    | [event-core.md](references/event-core.md)         | Working with slots, composables, EventContext, custom adapters   |
| HTTP core/routing | [event-http.md](references/event-http.md)         | Creating HTTP apps, routing, server lifecycle, security headers  |
| HTTP request      | [http-request.md](references/http-request.md)     | Reading headers, cookies, query params, body, authorization      |
| HTTP response     | [http-response.md](references/http-response.md)   | Status, headers, cookies, cache, errors, streaming, testing      |
| CLI apps          | [event-cli.md](references/event-cli.md)           | Building CLI tools, command routing, options, help system         |
| WebSocket server  | [event-ws.md](references/event-ws.md)             | WS server, rooms, broadcasting, message routing, wire protocol   |
| Workflow core     | [event-wf.md](references/event-wf.md)             | Steps, flows, schema syntax, pause/resume, useWfState            |
| Workflow outlets  | [wf-outlets.md](references/wf-outlets.md)         | HTTP/email delivery, state strategies, tokens, trigger handler   |
| Workflow advanced | [wf-advanced.md](references/wf-advanced.md)       | Parent context, spies, error handling, testing                   |
| WS client         | [ws-client.md](references/ws-client.md)           | Browser/Node WS client, RPC, subscriptions, reconnection        |

## Quick reference

### @wooksjs/event-core

```ts
import {
  // primitives
  key, cached, cachedBy, slot, defineEventKind, defineWook,
  // context
  EventContext, run, current, tryGetCurrent, createEventContext,
  // composables
  useRouteParams, useEventId, useLogger,
  // standard keys
  routeParamsKey, eventTypeKey,
  // observability
  ContextInjector, getContextInjector, replaceContextInjector, resetContextInjector,
} from '@wooksjs/event-core'
```

### @wooksjs/event-http

```ts
import { createHttpApp } from '@wooksjs/event-http'

const app = createHttpApp()

// Route registration
app.get('/path', handler)      // also: post, put, patch, delete, head, options, all
app.on('GET', '/path', handler) // generic method

// Composables
import {
  useRequest, useResponse, useHeaders, useCookies,
  useUrlParams, useAuthorization, useAccept,
  useRouteParams, useLogger,
} from '@wooksjs/event-http'

// Errors & testing
import { HttpError, prepareTestHttpContext } from '@wooksjs/event-http'
```

**Auto-status inference:**

| Method | Body   | Status |
| ------ | ------ | ------ |
| GET    | truthy | 200    |
| POST   | truthy | 201    |
| PUT    | truthy | 201    |
| PATCH  | truthy | 202    |
| DELETE | truthy | 202    |
| Any    | void   | 204    |

### @wooksjs/event-cli

```ts
import { createCliApp } from '@wooksjs/event-cli'

const app = createCliApp()
app.cli('command/:param', handler)
app.run()

import {
  useCliOptions, useCliOption, useCliHelp, useAutoHelp, useCommandLookupHelp,
  useRouteParams, useLogger,
} from '@wooksjs/event-cli'
```

### @wooksjs/event-ws

```ts
import { createWsApp } from '@wooksjs/event-ws'

const ws = createWsApp(http)             // integrated with HTTP
const ws = createWsApp()                 // standalone

ws.onMessage('message', '/chat/:room', handler)
ws.onConnect(handler)
ws.onDisconnect(handler)

import {
  useWsConnection, useWsMessage, useWsRooms, useWsServer, currentConnection,
  useRouteParams, useLogger,
} from '@wooksjs/event-ws'

// Testing
import { prepareTestWsConnectionContext, prepareTestWsMessageContext } from '@wooksjs/event-ws'
```

**Wire protocol — 3 message types:**

```ts
// Client -> Server
interface WsClientMessage { event: string; path: string; data?: unknown; id?: string | number }

// Server -> Client (reply to RPC)
interface WsReplyMessage { id: string | number; data?: unknown; error?: { code: number; message: string } }

// Server -> Client (push)
interface WsPushMessage { event: string; path: string; params?: Record<string, string>; data?: unknown }
```

### @wooksjs/event-wf

```ts
import { createWfApp } from '@wooksjs/event-wf'

const app = createWfApp<MyContext>()

app.step('step-id', { handler: (ctx) => { /* ... */ } })
app.flow('flow-id', ['step-a', 'step-b', { id: 'step-c', condition: 'ready' }])

const result = await app.start('flow-id', initialContext)

import { useWfState, useRouteParams, useLogger, StepRetriableError } from '@wooksjs/event-wf'
```

### @wooksjs/ws-client

```ts
import { createWsClient } from '@wooksjs/ws-client'

const client = createWsClient('ws://localhost:3000', { reconnect: { enabled: true } })

client.send('chat', '/room/general', { text: 'hello' })             // fire-and-forget
const reply = await client.call('rpc', '/api/users', { id: 1 })     // RPC with correlation
const unsub = await client.subscribe('/notifications')              // RPC + auto-resubscribe on reconnect
const unreg = client.on('push', '/chat/*', (ev) => { /* ... */ })   // push listener (suffix wildcard only)
```

## Cross-cutting patterns

### Adapter integration (HTTP + WebSocket)

```ts
const http = createHttpApp()
const ws = createWsApp(http)

ws.onMessage('message', '/chat/:room', handler)
http.get('/api/health', () => 'ok')

http.listen(3000)  // serves both HTTP and WS
```

### Parent context chains

Child contexts traverse the parent chain for slot lookups, enabling composables to work transparently across boundaries:

```ts
// HTTP -> Workflow: pass the HTTP context directly; WF creates a child linked to it.
const result = await wfApp.start('flow-id', ctx, {
  eventContext: current()   // workflow composables can read HTTP slots via parent chain
})

// HTTP -> WebSocket: connection context parents from HTTP upgrade
```

### Shared router

Adapter factories accept `(opts?, wooks?)`. Pass another adapter or a `Wooks` as the second arg to share routing:

```ts
const http = createHttpApp()
const cli = createCliApp({}, http)       // shares http's router
const wf  = createWfApp<Ctx>({}, http)   // shares http's router
const ws  = createWsApp(http)            // first arg detects adapter vs opts
```

### Performance: resolve context once

When calling multiple composables in one handler, resolve context once and pass it:

```ts
app.get('/path', () => {
  const ctx = current()
  const { url, method } = useRequest(ctx)
  const logger = useLogger(ctx)
  const response = useResponse(ctx)
})
```
