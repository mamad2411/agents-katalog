---
name: follow-lib-orpc-define-contracts
description: oRPC contract-first design — contract builder, input/output schemas, error maps, router contracts
argument-hint: "[scope]"
related:
  - follow-lib-orpc
  - follow-lib-zod
  - run-typecheck
  - resolve-errors
---

## Goal

Design oRPC contracts — contract-first API definition with schemas + error maps that generate server impl + client types

## Scope

contract layer — `@orpc/contract` (`oc` builder), input/output validation contracts, error specs, router contract composition; implementation → `define-procedures`

## Execute

### 1. Contract Builder

```ts
import { oc } from '@orpc/contract'
import { z } from 'zod'

export const contract = oc.router({
  getUser: oc
    .input(z.object({ id: z.uuid() }))
    .output(UserSchema)
    .errors({ NOT_FOUND: { status: 404, data: z.object({ id: z.string() }) } })
    .route({ method: 'GET', path: '/users/{id}' }),
  createUser: oc.input(CreateUserSchema).output(UserSchema).route({ method: 'POST', path: '/users' }),
})
```

- `oc` = contract builder — `oc.input().output().errors().route().meta()`
- `.route({ method, path })` — OpenAPI-compatible routing metadata
- Contract = standalone — not bound to the server impl; shared FE/BE through the same object

### 2. Contract Router Organization

- `contracts/` dir per domain — compose `oc.router({ domain: domainContract })`
- Contract package shareable (npm/workspace pkg) — client imports types without depending on server code
- `InferContractRouterInputs`/`InferContractRouterOutputs` — derive types from the contract

### 3. Error Maps

- `.errors({ KEY: { status, data: Schema } })` — typed declared errors per procedure
- Common error keys shared base contract: `oc.errors({ UNAUTHORIZED: {...} })` → spread per proc

### 4. Contract-First Workflow

1. Define contract → review API surface (types, errors, routes)
2. `implement(contract)` on the server → `createRouterClient(contract)` on the client
3. Schema changes → contract update → type errors surface mismatches (compile-time safety)

## Rules

- Contracts = API source of truth — design/review here before implementing
- Add `.errors()` to every proc with expected failures — typed errors on the client
- `.route()` metadata must be OpenAPI-valid (method + path template) — the OpenAPI export stays usable
- Schemas in contracts are Standard Schema (zod/valibot/arktype can be mixed across procs)

## Expected Outcome

- Contract router typed E2E — input/output/errors declared
- FE/BE share the contract — compile-time drift detection
