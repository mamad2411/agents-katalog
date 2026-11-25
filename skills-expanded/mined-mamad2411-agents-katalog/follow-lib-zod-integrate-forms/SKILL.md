---
name: follow-lib-zod-integrate-forms
description: Zod integration — Standard Schema, react-hook-form/tanstack-form, JSON Schema/OpenAPI, env/config patterns
argument-hint: "[integration]"
related:
  - follow-lib-zod
  - follow-lib-tanstack-ecosystem
  - run-test
  - resolve-errors
---

## Goal

Integrate Zod into the ecosystem — Standard Schema interop, form libs (RHF/TanStack Form), JSON Schema export, OpenAPI, validation libs interop

## Scope

interop — `StandardSchemaV1` interface (zod is an implementer), resolver patterns, `z.toJSONSchema` (v4), ecosystem tool compat

## Execute

### 1. Standard Schema

```ts
// Zod v3.24+ / v4 implement Standard Schema — every lib accepting StandardSchemaV1 works directly
import type { StandardSchemaV1 } from '@standard-schema/spec'

// works with TanStack Form, tRPC, oRPC, Hono validator, Nitro, Arkaic... (auto-detect)
```

- Zod schemas satisfy the Standard Schema contract — use them with any supporting lib, no adapter needed

### 2. Form Libraries

```tsx
// react-hook-form
import { zodResolver } from '@hookform/resolvers/zod'
useForm({ resolver: zodResolver(FormSchema) })

// TanStack Form (v1) — Standard Schema directly
<form.Field validators={{ onChange: FieldSchema }} />
```

- `@hookform/resolvers` — `zodResolver`; TanStack Form → via Standard Schema directly
- Server + client shared schema — validate both sides with the same schema

### 3. JSON Schema Export (v4)

```ts
import { z } from 'zod'
const jsonSchema = z.toJSONSchema(UserSchema)   // v4 native
// v3: zod-to-json-schema package
```

- `z.toJSONSchema` — export schemas → OpenAPI/JSON Schema docs, code-gen, form builders
- Limitation: transforms/some refinements aren't representable — check the output

### 4. OpenAPI And Docs

- `zod-to-openapi`/`@asteasolutions/zod-to-openapi` — OpenAPI spec from schemas (v3); v4 → `z.toJSONSchema` + OpenAPI tooling
- oRPC/tRPC — schemas are the procedure input/output contract directly
- `zod-openapi` ecosystem — check v4 support before adopting

### 5. Env/Config (application)

- Env schema → `z.toJSONSchema` → generated `.env.example` docs
- Config schemas shared FE/BE — the same contract for both runtime and docs

## Rules

- Standard Schema is the canonical interop — prefer directly supporting libs before an adapter
- `z.toJSONSchema` is v4-native — v3 uses the `zod-to-json-schema` package
- Shared schemas FE/BE — one contract, validate both sides
- Transforms don't serialize into JSON Schema — split input/output schemas when docs are needed

## Expected Outcome

- Zod wired into forms/OpenAPI/Standard Schema completely
- Schema = a single contract for runtime validation + docs + types
