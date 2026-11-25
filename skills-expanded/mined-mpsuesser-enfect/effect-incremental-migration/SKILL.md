---
name: effect-incremental-migration
description: Incrementally migrate existing async/Promise-based modules to Effect services while preserving backward compatibility. Use this skill when effectifying an existing module, replacing async facades with Effect services, or maintaining dual async/Effect APIs during migration.
---

# Incremental Migration Skill

This skill provides a step-by-step template for converting existing async/Promise-based modules to Effect services. Preserve backward compatibility only where you still have non-Effect callers. The main goal is to move Effect callers onto `yield* SomeService.Service` early so dependency edges become explicit in the code and in the layer graph.

## Effect Source Reference

The Effect v4 source is available at `~/.local/share/opencode/repos/github.com/Effect-TS/effect@main/`.
Baseline: **effect@4.1.0 stable**. Use `git show effect@4.1.0:<path>`;
keep historical Before examples as migration input, not current guidance.

Reference this for:

- Context source: `packages/effect/src/Context.ts`
- Layer source: `packages/effect/src/Layer.ts`
- ManagedRuntime source: `packages/effect/src/ManagedRuntime.ts`
- Migration guide: `MIGRATION.md`
- Effect source: `packages/effect/src/`

## The 8-Step Migration Template

### Step 1: Define the Service Interface

Extract a named `Interface` type with Effect-returning methods. Preserve the
caller's successful values, but make every possible failure explicit in `E`.
Keep an established service layout; otherwise use file-local exports and an
ES-module namespace projection, not a TypeScript namespace.

```typescript
import type { Effect } from 'effect';

export interface Interface {
	readonly get: (id: string) => Effect.Effect<Item, MyModuleError>;
	readonly list: Effect.Effect<ReadonlyArray<Item>, MyModuleError>;
}
```

### Step 2: Declare the Service Class

Empty class body — no `make:`, no `static readonly layer`. The interface and
service class live in the same ES module.

```typescript
import { Context } from 'effect';
import type { Effect } from 'effect';

export interface Interface {
	readonly get: (id: string) => Effect.Effect<Item, MyModuleError>;
	readonly list: Effect.Effect<ReadonlyArray<Item>, MyModuleError>;
}

export class Service extends Context.Service<Service, Interface>()('@app/MyModule') {}
```

### Step 3: Build the Raw Layer

Construct the service inside `Layer.effect`, capturing dependencies via `yield*`. Use `Effect.fn` for traced methods.

```typescript
import { Effect, Layer, Context } from 'effect';

// Interface and Service as above; dependency failures must match MyModuleError
// or be translated into it at this boundary.
export const layer = Layer.effect(
	Service,
	Effect.gen(function* () {
		const config = yield* Config.Service;
		const db = yield* Database.Service;

		const get = Effect.fn('MyModule.get')(function* (id: string) {
			const cfg = yield* config.get();
			return yield* db.findById(cfg.table, id);
		});
		const list = Effect.gen(function* () {
			const cfg = yield* config.get();
			return yield* db.listAll(cfg.table);
		});
		return Service.of({ get, list });
	})
);
```

The layer's type exposes unsatisfied requirements (`Config.Service | Database.Service`). This is intentional — the raw layer declares its true dependency graph.

### Step 4: Build the Wired Default Layer

Compose the wired `defaultLayer` directly in the normal case. Use `Layer.suspend(() => ...)` only if module evaluation order or a real circular import requires deferral.

```typescript
import { Layer } from 'effect';

export const defaultLayer = layer.pipe(
	Layer.provide(Config.defaultLayer),
	Layer.provide(Database.defaultLayer)
);
export * as MyModule from './my-module.js';
```

If the module really needs deferred composition:

```typescript
export const defaultLayer = Layer.suspend(() =>
	layer.pipe(Layer.provide(Config.defaultLayer))
);
```

### Step 5: Create the Runtime Bridge

A shared `memoMap` ensures layers are deduplicated across all per-service runtimes. Define the bridge utility once and reuse it across migrated modules.

<!-- typecheck -->
```typescript
import { Layer, ManagedRuntime } from 'effect';
import type { Effect, Context } from 'effect';

const memoMap = Layer.makeMemoMapUnsafe();

export function makeRuntime<I, S, E>(
	service: Context.Service<I, S>,
	layer: Layer.Layer<I, E>
) {
	const runtime = ManagedRuntime.make(layer, { memoMap });
	return {
		runPromise: <A, Err>(fn: (svc: S) => Effect.Effect<A, Err, I>) =>
			runtime.runPromise(service.use(fn)),
		runSync: <A, Err>(fn: (svc: S) => Effect.Effect<A, Err, I>) =>
			runtime.runSync(service.use(fn)),
		dispose: () => runtime.dispose()
	};
}
```

Then at the non-Effect boundary, create the bridge from the service and its default layer:

```typescript
const { runPromise, dispose } = makeRuntime(MyModule.Service, MyModule.defaultLayer);
```

`ManagedRuntime.make` builds the layer lazily on first use, so no separate lazy
runtime variable is needed. The host owns the bridge: stop admitting work and
await `dispose()` on shutdown. Disposal interrupts managed fibers and waits for
their cleanup before releasing layer resources. A shared memo map deduplicates
acquisition, but does not remove each runtime's disposal obligation.

Reuse identical layer objects: 4.1.0 memoizes composed layers too. Runtime layer
build failures are cached; retry acquisition inside the layer or dispose and
create another runtime. External concurrent disposal calls join cleanup, but
runtime-owned fibers/finalizers do not wait on their own disposal.

> **Memo-map nuance:** Keep the bridge `memoMap` shared (the root `Layer.makeMemoMapUnsafe()` above) so every per-service runtime reuses the same layer allocations. Do not `Layer.forkMemoMap` it unless a specific child runtime intentionally needs isolated allocations — a forked memo map can read the parent's existing allocations but builds new ones in isolation, which defeats the deduplication this bridge exists to provide.

### Step 6: Keep Boundary Facades Only When Still Needed

If non-Effect callers still exist, wrap each service method in a thin `async` function that delegates to `runPromise`. Do not keep facades as the primary API once Effect callers can `yield*` the service directly.

```typescript
// Boundary facade module, separate from the service module.
export async function get(id: string): Promise<Item> {
	return runPromise((svc) => svc.get(id));
}

export async function list(): Promise<ReadonlyArray<Item>> {
	return runPromise((svc) => svc.list);
}
```

These facades are boundary shims. Do not add new internal Effect callers that go through them.

### Step 7: Update Effect Callers Immediately

As soon as the service exists, replace `Effect.promise(() => facade())` calls in Effect code with direct service yields:

```typescript
// Before: calling through async facade
const item = yield* Effect.promise(() => MyModule.get(id));

// After: yielding the service directly
const myModule = yield* MyModule.Service;
const item = yield* myModule.get(id);
```

When replacing `Effect.promise(() => facade())` with direct service yields, errors that previously flowed as defects become typed channel errors. Update any `catchDefect` handlers to `catch` or `catchTag`.

This is the real migration milestone: the dependency graph becomes visible at the call site, and reviewers no longer need to remember which helper hides which runtime requirements.

**Common migration transformation — `Promise.all` fan-out to `Effect.forEach`:**

When migrating callers that use `Promise.all(items.map(async (x) => ...))`, replace with `Effect.forEach`:

```typescript
// Before: wrapped Promise.all fan-out
const results =
	yield*
	Effect.promise(() =>
		Promise.all(items.map(async (item) => processItem(item)))
	);

// After: Effect.forEach with explicit concurrency
const results =
	yield*
	Effect.forEach(items, (item) => processItem(item), {
		concurrency: 'unbounded'
	});
```

This transformation eliminates the `Effect.promise` wrapper entirely and gives explicit control over concurrency.

### Step 8: Prune Dead Facades Aggressively

Once Effect callers have been updated to yield the service directly, the async facade functions from Step 6 become dead code. Remove them in a dedicated cleanup commit:

1. Search for callers of each facade function (grep for the function name across the codebase)
2. Verify no remaining callers exist outside of Effect service code
3. Delete the facade functions and the runtime bridge (`runPromise`)
4. If the runtime bridge was the last consumer of `defaultLayer`, the `makeRuntime` call can also be removed

**Prune in a separate commit.** Facade pruning is a pure deletion — it should be reviewable independently from the migration work that preceded it. This makes it easy to verify that no callers were missed.

## Complete Before/After Example

### Before: Plain Async Module

```typescript
import { loadConfig } from './config';

export namespace Items {
	let cachedConfig: Config | undefined;

	async function getConfig(): Promise<Config> {
		return (cachedConfig ??= await loadConfig());
	}

	export async function get(id: string): Promise<Item> {
		const cfg = await getConfig();
		const res = await fetch(`${cfg.apiUrl}/items/${id}`);
		if (!res.ok) throw new Error(`Item ${id} not found`);
		return res.json();
	}

	export async function list(): Promise<ReadonlyArray<Item>> {
		const cfg = await getConfig();
		const res = await fetch(`${cfg.apiUrl}/items`);
		return res.json();
	}
}
```

### After: Effect Service with Backward-Compatible Facades

The service module below is self-contained. Its raw layer exposes the HTTP
transport requirement; the composition root supplies the release-matched Bun
transport. HTTP modules are `@stability unstable` in 4.1.0.

<!-- typecheck -->
```typescript
import { Context, Effect, Layer } from 'effect';
import * as Schema from 'effect/Schema';
import { HttpClient, HttpClientRequest, HttpClientResponse } from 'effect/http';

class Item extends Schema.Class<Item>('Item')({
	id: Schema.String,
	name: Schema.String
}) {}

class ItemsError extends Schema.TaggedError<ItemsError>()('ItemsError', {
	operation: Schema.String,
	cause: Schema.Unknown
}) {}

export interface Interface {
	readonly get: (id: string) => Effect.Effect<Item, ItemsError>;
	readonly list: Effect.Effect<ReadonlyArray<Item>, ItemsError>;
}

export class Service extends Context.Service<Service, Interface>()('@app/Items') {}

export const layer = Layer.effect(Service, Effect.gen(function* () {
	const client = (yield* HttpClient.HttpClient).pipe(
		HttpClient.mapRequest(HttpClientRequest.prependUrl('https://api.example.com')),
		HttpClient.filterStatusOk
	);
	const get = Effect.fn('Items.get')(function* (id: string) {
		return yield* client.get(`/items/${encodeURIComponent(id)}`).pipe(
			Effect.flatMap(HttpClientResponse.schemaBodyJson(Item)),
			Effect.mapError((cause) => new ItemsError({ operation: 'get', cause }))
		);
	});
	const list = client.get('/items').pipe(
		Effect.flatMap(HttpClientResponse.schemaBodyJson(Schema.Array(Item))),
		Effect.mapError((cause) => new ItemsError({ operation: 'list', cause }))
	);
	return Service.of({ get, list });
}));
// At the owning module boundary: export * as Items from './items.js';
```

```typescript
// items-async.ts — only while Promise callers remain
import { ManagedRuntime, Layer } from 'effect';
import { BunHttpClient } from '@effect/platform-bun';
import { Items } from './items.js';

const defaultLayer = Items.layer.pipe(Layer.provide(BunHttpClient.layer));
const runtime = ManagedRuntime.make(defaultLayer);
export const get = (id: string) => runtime.runPromise(Items.Service.use((svc) => svc.get(id)));
export const list = () => runtime.runPromise(Items.Service.use((svc) => svc.list));
export const dispose = () => runtime.dispose(); // host awaits this at shutdown
```

The adapter checks status before decoding, preserves transport/decode errors in
`ItemsError`, and lets the HTTP transport propagate cancellation. For a legacy SDK
that still returns promises, use `Effect.tryPromise({ try: (signal) => ..., catch })`.
Declare `signal` as an ordinary parameter: signal creation is arity-sensitive
(`promise`/`tryPromise`: at least one parameter; `callback`: at least two).
Default/rest parameters do not count toward that arity.

## Migration Checklist

- [ ] Interface type extracted with Effect-returning methods
- [ ] Service class declared with `Context.Service`
- [ ] Layer built with `Layer.effect` capturing dependencies via `yield*`
- [ ] Effect callers migrate to `yield* SomeService.Service` as early as possible
- [ ] Default layer composes directly unless deferred evaluation is truly required
- [ ] Runtime bridge created with shared `memoMap`
- [ ] Async facades kept only for remaining non-Effect boundaries
- [ ] Callers in Effect.gen blocks updated to yield service directly
- [ ] `Promise.all(items.map(...))` patterns replaced with `Effect.forEach`
- [ ] Former `catchDefect` handlers updated to `catch`/`catchTag` for now-typed errors
- [ ] Dead facade functions pruned in a separate commit once all callers migrated

## Related Skills

- `effect-service-implementation` — service declaration patterns and capability design
- `effect-layer-design` — layer composition, merging, and dependency management
- `effect-managed-runtime` — ManagedRuntime lifecycle and `memoMap` usage
- `effect-error-handling` — typed errors, `catchTag`, and error channel design
