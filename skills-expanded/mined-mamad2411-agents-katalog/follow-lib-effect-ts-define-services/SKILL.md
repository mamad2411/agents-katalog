---
name: follow-lib-effect-ts-define-services
description: Effect services + Layer DI — Effect.Service, Context.Tag, Layer composition, scoped deps
argument-hint: "[scope]"
related:
  - follow-lib-effect-ts
  - run-typecheck
  - resolve-errors
---

## Goal

Write services + dependency injection correctly with `Effect.Service` / `Context.Tag` + `Layer`

## Scope

service definition, layer composition, dependency graph — installation lives in `setup-effect`; v3 API (v4 RC → `Context.Service` instead, see `migrate-to-effect`)

## Execute

### 1. Define Service

> Goal: a service with its default layer

```ts
import { Effect } from "effect"

class TodoRepo extends Effect.Service<TodoRepo>()("TodoRepo", {
  effect: Effect.gen(function* () {
    const db = yield* Database
    return {
      findAll: () => db.query("SELECT * FROM todos"),
      create: (t: Todo) => db.insert(t),
    }
  }),
  dependencies: [Database.Default],   // declared deps
}) {}
```

- `Effect.Service` (v3.9+) = Tag + Layer in one — default layer `TodoRepo.Default`
- Manual control → `Context.Tag`/`Context.GenericTag` + `Layer.succeed`/`Layer.effect`/`Layer.scoped`

### 2. Compose Layers

> Goal: the graph of dependencies

```ts
const AppLayer = Layer.mergeAll(Database.Default, HttpLive)
  .pipe(Layer.provideMerge(ConfigLayer))
// or TodoRepo.Default — deps already bound from `dependencies`
```

- `Layer.mergeAll` (parallel), `Layer.provide`/`provideMerge` (pass a dep through), `Layer.scoped` (acquire/release)
- `Layer.succeed` = pure impl; `Layer.effect` = effectful init; `Layer.scoped` = needs cleanup

### 3. Consume In Effects

```ts
const program = Effect.gen(function* () {
  const repo = yield* TodoRepo          // yield* the service tag for its requirements
  return yield* repo.findAll()
})
Effect.runPromise(program.pipe(Effect.provide(TodoRepo.Default)))
```

- The `R` channel = requirements — provide them fully at the boundary only
- Access pattern variants: `Effect.serviceFunctions`, `Effect.serviceMembers` for the fn style

### 4. Test Substitution

- `Layer.mock(TodoRepo)` (v3.17+) with a partial impl, or `Layer.succeed(TodoRepo, fakeImpl)` — see `test-effect`

## Rules

- Every external dep (db, http, clock, config) = a service — never import a singleton directly
- The `dependencies` array must be complete — never stack provides afterward
- `Layer.scoped` for resources that must be released (connections, file handles)
- Requirements flow through types only — no hidden globals

## Expected Outcome

- Services written with `Effect.Service` + a clear Layer graph
- Tests can substitute impls via Layers — without touching business code
