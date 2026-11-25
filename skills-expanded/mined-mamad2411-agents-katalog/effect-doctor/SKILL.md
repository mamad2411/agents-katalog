---
name: effect-doctor
description: Diagnose and improve Effect-TS code against canonical patterns. Use whenever the user is writing, reviewing, refactoring, or debugging code that imports from `effect`, `@effect/*`, or a project built on Effect (like effectctx). Covers Layer composition, Service/Context.Tag, error channels with Data.TaggedError, Scope and resource management, Stream/Queue/PubSub, Schema decoding at boundaries, fiber management, tracing with withSpan, and the anti-patterns that experienced Effect users keep flagging (missing `yield*`, unbounded concurrency, providing Layers twice, accessor R-leakage, etc.). Trigger on phrases like "review my Effect code", "is this idiomatic Effect", "audit the Layer composition", "why is this fiber not interrupting", "what's the right error type here", "convert this Promise code to Effect", or any task that involves writing non-trivial Effect-TS code where idiom matters.
---

# effect-doctor

You are diagnosing or writing Effect-TS code. The goal is idiomatic Effect — the way the core team and production adopters actually structure things — not "TypeScript with Effect sprinkled on top."

## How to use this skill

Two modes:

1. **Writing new Effect code** — use the patterns below as the default vocabulary. Reach for `references/anti-patterns.md` when you catch yourself drifting.
2. **Auditing existing Effect code** — walk the checklist in `references/audit-checklist.md` against the diff or files in scope. Flag findings with concrete file:line references. Don't rewrite anything until the user has seen the findings.

When in doubt about which canonical primitive applies, consult `references/primitives.md` — it has the decision tables (Layer.effect vs scoped vs scopedDiscard; fail vs die; fork vs forkScoped vs forkDaemon; Stream vs Queue vs PubSub).

## The load-bearing rules

These are the rules that, when broken, produce the bugs experienced Effect users see over and over. Internalize them; everything else is style.

### Layers

- **`Layer.scoped` whenever construction uses `acquireRelease` or `addFinalizer`.** Otherwise `Layer.effect`. `Layer.scopedDiscard` is for environment mutations with no service surface (installing a `FiberRef` patch, registering a long-lived finalizer, swapping `Clock`/`ConfigProvider`).
- **Provide each Layer exactly once, at the entry boundary.** Providing the same Layer in two places gives two instances. Use `ManagedRuntime.make(layer)` to hand a runtime to non-Effect hosts.
- **Many small Layers, composed at the top.** Avoid god-layers. The `@effect/platform` split (abstract / shared / runtime-specific) is the reference shape.
- **Tag identifier convention**: `"@scope/pkg/ServiceName"`. Stable across HMR and bundlers.

### Services

- `Effect.Service` class form is the modern default. `Context.Tag` is still first-class.
- **Default to `accessors: false` on public library APIs.** `accessors: true` propagates the service's own `R` into every caller, which looks like dependency leakage in inferred types. Use plain functions that take the service via `Effect.gen` internally when shipping a library.
- Ship both the service class and a default `Live` Layer. Real test implementations beat mocks.

### Errors

- **`Data.TaggedError("Foo")<{...}>`** is the primary tool. Use it for the error channel of every public function.
- **`Schema.TaggedError`** when errors cross a wire (workers, RPC, SSE, persisted event log). Plain `Data.TaggedError` doesn't serialize.
- **`Effect.fail` vs `Effect.die`**: `fail` for things callers should handle (typed in `E`). `die` for invariant violations. Defects don't appear in `E`; only `catchAllCause` / `sandbox` sees them.
- **Keep `E` precise and small at boundaries.** If internals have many error types, catch and re-tag into 2-4 documented public errors.

### Resource management

- Inside services, prefer `Effect.acquireRelease` for local acquire/release pairs. Use `Effect.addFinalizer` for cross-cutting cleanup tied to the surrounding scope.
- Finalizers run in **reverse order** and receive an `Exit`, so they can branch on success/failure/interrupt.
- Per-request work inside a long-running runtime: wrap the unit in `Effect.scoped` so resources don't accumulate on the parent scope.

### Streams, Queues, PubSub

- Single result: `Effect`. Zero-or-more values over time: `Stream`.
- `Queue` is single-consumer with back-pressure. `PubSub` is multi-consumer broadcast (use `Stream.fromPubSub(hub)` per subscriber). For an event log with multiple subscribers (UI, persistence, eval), `PubSub` is the right primitive.
- Choose the back-pressure strategy explicitly: `bounded`, `dropping`, `sliding`, `unbounded`. The default isn't always what you want.

### Schema

- **Decode at the boundary, encode at the boundary, internal code uses the decoded type.** This is the load-bearing rule. Don't pass `Schema.encodedSchema` shapes through business logic.
- Round-trip invariant: `encode . decode === id`. If a schema breaks this, it's a bug in the schema.
- For libraries, export schemas (not just inferred types) so consumers can derive validators, OpenAPI, AI tool definitions.

### Fibers and shutdown

- Default to `Effect.fork` (child dies with parent). `Effect.forkScoped` when the work outlives the originating effect but not the runtime. `Effect.forkDaemon` is a foot-gun: no supervision, must be interrupted manually.
- Graceful shutdown: OS signal handlers interrupt the root fiber. Cascades through children automatically.

### Tracing

- `Effect.withSpan(name, options)` per unit of work. `Effect.annotateCurrentSpan` for attributes. Spans nest via Effect context with no manual propagation.
- For AI/agent code, mirror `@effect/ai`'s span attribute naming (`gen_ai.system`, `gen_ai.request.model`, tool name) so traces compose with theirs.
- `@effect/opentelemetry` is the canonical wiring.

### Idiom and tree-shaking

- `import * as Effect from "effect/Effect"` (namespace imports tree-shake; method-style breaks it).
- `Effect.gen` for control flow with branching and conditionals. `.pipe` for linear data transformation. Switching from a long `.andThen` chain to `gen` is almost always an improvement in readability.
- Always pass `{ concurrency }` to `Effect.all` and `forEach`. Unbounded parallelism is rarely what you want; use `Semaphore` for rate limiting.

## The anti-patterns

These show up over and over in production Effect code. If you spot one during an audit, flag it.

1. **Missing `yield*`** inside `Effect.gen`. Silent failure: you get an `Effect<...>` value back, not its result. Single most common bug.
2. **`throw` instead of `Effect.fail`** with a tagged error.
3. **Unbounded `Effect.all` / `Effect.forEach`** with no concurrency limit.
4. **Providing the same Layer in multiple places** instead of once at entry.
5. **`Effect.runSync` where `runFork` / `runPromise` is correct.** `runSync` only works when the effect is genuinely synchronous and has no async or scoped dependencies; otherwise it throws at runtime.
6. **Methods over namespace functions** (breaks tree-shaking).
7. **Long `.andThen` / `.flatMap` chains** that should be `Effect.gen`.
8. **`accessors: true` on library services**, leaking `R` into every consumer.
9. **`forkDaemon` for things that should be `forkScoped`**, leaving orphaned fibers on shutdown.
10. **`Data.TaggedError` across a wire** — use `Schema.TaggedError` for anything serialized.
11. **Decoding inside business logic** instead of at the boundary; or worse, passing encoded types around.

## Audit workflow

When the user asks for an audit, or you're reviewing Effect code:

1. **Identify the scope.** Which files? The diff, or the whole package? Be explicit.
2. **Walk `references/audit-checklist.md`** in order. Don't skip sections.
3. **Collect findings with file:line references.** Severity tags: `[bug]` (will misbehave), `[idiom]` (works but not canonical), `[smell]` (worth a second look).
4. **Report before fixing.** Show the findings, let the user choose what to apply. Resist the urge to rewrite half the codebase.
5. **When applying fixes, prefer the smallest change that resolves the finding.** Don't bundle unrelated cleanups.

## Sources of truth

When something is contested, prefer in order:

1. The Effect source in `node_modules/effect/src` (JSDoc and types are canonical)
2. The official docs at https://effect.website/docs/
3. The `@effect/ai`, `@effect/platform`, `@effect/sql` source as reference implementations
4. Effect Days talks and the team's public posts
5. Community blogs (dtech.vision, EffectPatterns)

Community guidance (e.g. "avoid `accessors: true` on public APIs") is strong default-true but not in official docs. Say so when citing it; don't present it as canonical.

## When you're not sure

Effect 4.x is in flight (Michael Arnaldi, Effect Days 2025). The Service/Layer model is stable; perf and codegen ergonomics are evolving. If you're about to recommend a deep refactor based on a pattern, check whether the user is on Effect 3.x or 4.x first (look at `package.json`), and skim the relevant section of `node_modules/effect` to confirm the API still matches what you remember.

If you genuinely don't know whether something is idiomatic, say so. The Effect community is small and opinionated; confident-sounding wrong advice is worse than "I'd check the source."
