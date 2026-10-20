---
name: follow-lib-effect-ts-use-schema
description: Effect Schema — decode/encode, transforms, branded types, TaggedError schemas, JSON Schema
argument-hint: "[scope]"
related:
  - follow-lib-effect-ts
  - run-typecheck
  - run-test
  - resolve-errors
---

## Goal

Use `Schema` (built-in `effect` since v3) fully — decode/encode, transforms, branded, filters, struct composition, TaggedError schemas

## Scope

runtime validation + type derivation — external data boundaries (API, env, DB rows); standalone `@effect/schema` is deprecated — use `Schema` from `effect` only

## Execute

### 1. Define Schemas

```ts
import { Schema } from "effect"

class Todo extends Schema.Class<Todo>("Todo")({
  id: Schema.UUID,
  title: Schema.NonEmptyString,
  done: Schema.Boolean,
  dueAt: Schema.optional(Schema.DateFromString),
}) {}
```

- `Schema.Class` = runtime schema + class instance + nominal typing in one
- Composition: `Schema.Struct`, `Schema.Union`, `Schema.Literal`, `Schema.Array`, `Schema.optional`, `Schema.NullOr`

### 2. Decode/Encode

```ts
Schema.decodeUnknownSync(Todo)(raw)         // throws — boundaries you can trust
Schema.decodeUnknown(Todo)(raw)             // Effect — ParseError in the E channel
Schema.encode(Todo)(todo)                   // domain → wire format
```

- `decode` = input→domain, `encode` = domain→output — transforms flow both ways
- `Schema.is(Todo)` type guard; `Schema.validate` variants as needed

### 3. Transforms And Refinements

- `Schema.transform`/`transformOrFail` — string→Date, csv→array, etc.
- `Schema.filter` / built-ins: `NonEmptyString`, `MinLength`, `Int`, `UUID`, `greaterThan`
- `Schema.brand` nominal typing (`UserId`, `Email`) — prevents primitive mixups
- `Schema.partial`/`pick`/`omit`/`required` — derive variants

### 4. Patterns

1. **Tagged errors as schemas**: `Schema.TaggedError` — serialize errors across RPC/HTTP
2. **Config/env validation**: decode env into a typed config at boot
3. **Message/payload schemas**: RPC, queue payloads — validate in both directions
4. **Arbitrary** (testing): `Arbitrary.make(Todo)` for fast-check random data

## Rules

- Validate only at the boundary — inside the domain the types already hold, don't re-validate
- `Schema.Class` for domain entities — `Schema.Struct` for plain payloads
- Inspect ParseError with `ParseResult`/`TreeFormatter` — don't swallow the message
- Never `as T` casts on external data — always decode

## Expected Outcome

- Schemas typed + runtime-validated at every boundary
- Transforms/branded/TaggedError used at the right spots
