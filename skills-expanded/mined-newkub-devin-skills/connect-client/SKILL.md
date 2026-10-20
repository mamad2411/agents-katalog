---
name: follow-lib-orpc-connect-client
description: oRPC client — createRouterClient, RPCLink, fetch config, TanStack Query integration
argument-hint: "[transport]"
related:
  - follow-lib-orpc
  - follow-lib-tanstack-ecosystem
  - run-test
  - resolve-errors
---

## Goal

Set up the oRPC client — `createRouterClient`, link transports (RPC/OpenAPI), headers/context, TanStack Query hooks

## Scope

client-side — `@orpc/client` (`createORPCClient`/`createRouterClient`), `RPCLink`/`OpenAPILink`, `client` helpers, `@orpc/tanstack-query` (orpc-query utils); server impl → `define-procedures`

## Execute

### 1. Create Client

```ts
import { createORPCClient } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'
import type { ContractRouterClient } from '@orpc/contract'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  headers: async () => ({ Authorization: `Bearer ${getToken()}` }),
})
export const client: ContractRouterClient<typeof contract> = createORPCClient(link)
```

- `RPCLink` — compact RPC protocol (POST, batching-friendly)
- `OpenAPILink` — REST-style calls (requires `.route()` metadata in the contract)
- `headers` async fn — auth tokens per request; `fetch` override for custom transport

### 2. Call Procedures

```ts
const user = await client.getUser({ id })
// typed errors: try/catch → ORPCError with .code matching contract errors
```

- Client methods mirror router paths — `client.users.list(...)`, `client.admin.users.create(...)`
- `safe()` variant (v1+): `const [err, data] = await client.getUser.safe(input)` — no throw

### 3. TanStack Query Integration

```ts
import { createORPCReactQueryUtils } from '@orpc/tanstack-query'  // or the latest orpc helper

const orpc = createORPCReactQueryUtils(client)
useQuery(orpc.getUser.queryOptions({ input: { id } }))
useMutation(orpc.createUser.mutationOptions())
```

- `@orpc/tanstack-query` — `queryOptions`/`mutationOptions`/`infiniteOptions` per proc
- `queryKey` deterministic from the procedure path + input — `client.key()`/`orpc.key()` invalidation
- React/Vue/Solid variants available (`@orpc/react-query`, `@orpc/vue-query`, `@orpc/solid-query` legacy paths — check the latest docs)

### 4. Server-Side Client

- `createRouterClient(router)` — call the router in-process (SSR/tests/edge) without an HTTP hop

## Rules

- Client type comes from the contract: `ContractRouterClient<typeof contract>` — never `any`
- Auth headers go through the `headers` async fn — never bake the token at create time
- TanStack Query = the canonical reactive layer — don't manually wrap client calls in state
- `RPCLink` default; `OpenAPILink` when you need REST-compat/debuggable URLs

## Expected Outcome

- Client typed E2E, auth header flow correct
- TanStack Query options generated for every proc
