---
name: follow-lib-elysia-validate-requests
description: Elysia validation — TypeBox t.*, body/query/params/headers/response schemas, Standard Schema, type inference
argument-hint: "[scope]"
related:
  - follow-lib-elysia
  - follow-lib-zod
  - run-typecheck
  - resolve-errors
---

## Goal

Validate requests/responses in Elysia — TypeBox `t.*` schemas per field (body/query/params/headers/cookie), response schemas, Standard Schema interop

## Scope

request/response validation — `t.Object`/`t.String`/... schema keys per handler+group+global; Standard Schema (Zod/Valibot/ArkType/Effect) can replace TypeBox; error handling → `use-lifecycle` onError

## Execute

### 1. Per-Route Schemas

```ts
import { Elysia, t } from 'elysia'

app.post('/users', ({ body }) => body, {
  body: t.Object({
    name: t.String({ minLength: 1 }),
    age: t.Optional(t.Integer({ minimum: 0 })),
    email: t.String({ format: 'email' }),
  }),
  query: t.Object({ verbose: t.Optional(t.BooleanString()) }),
  params: t.Object({ id: t.Numeric() }),          // auto-coerce string→number
  headers: t.Object({ authorization: t.String() }),
  response: { 200: UserSchema, 422: ErrorSchema }, // per-status response validation
})
```

- Schema keys: `body`, `query`, `params`, `headers`, `cookie`, `response`
- Coercion built-ins: `t.Numeric()`, `t.BooleanString()`, `t.File()`/`t.Files()` (uploads)
- Validated values **replace** raw — handler sees typed+coerced data

### 2. TypeBox Essentials

- `t.Object`, `t.String({ format })`, `t.Number`, `t.Integer`, `t.Boolean`, `t.Array(t.X)`, `t.Union`, `t.Literal`, `t.Record`, `t.Optional`, `t.Nullable`, `t.Partial`, `t.Pick`, `t.Omit`, `t.Ref`/`t.Model` shared
- `t.File({ type: 'image', maxSize: '5m' })` — upload validation
- Custom formats: `t.String({ format: 'email'|'uuid'|'date-time'|... })`

### 3. Shared Models

```ts
app.model({ user: t.Object({...}), error: t.Object({ message: t.String() }) })
app.post('/', h, { body: 'user', response: { 422: 'error' } })   // string ref → shared model
```

- `.model({ name: schema })` — app-level shared schemas, ref by string keys
- Reuse across routes/groups — single source

### 4. Standard Schema Interop

```ts
import { z } from 'zod'
app.post('/', h, { body: z.object({ name: z.string() }) })  // Zod/Valibot/ArkType work directly
```

- Elysia supports Standard Schema validators — Zod/Valibot/ArkType/Effect Schema drop-in
- TypeBox preferred — JIT-compiled fastest + Elysia-native inference; Standard Schema when schemas are shared with other libs

### 5. Inference

- `t` schemas → typed `body`/`params`/`query`/`headers` in the handler automatically
- Response schema → client type inference via Eden (`use-eden`)

## Rules

- Validate at schema keys — never manual `if (!body.x)` guards in the handler
- `t.Numeric`/`BooleanString` coercion — not string parsing in the handler
- `response` schema on every route the Eden client uses — inference + contract check
- Standard Schema lib = consistent across the app — don't mix TypeBox+Zod per route without reason

## Expected Outcome

- Requests validated+coerced at every boundary — handlers use typed data directly
- Shared models reused, Eden inference gets response types
