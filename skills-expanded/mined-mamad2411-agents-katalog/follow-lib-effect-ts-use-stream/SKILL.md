---
name: follow-lib-effect-ts-use-stream
description: Effect Stream — pull-based streams, sinks, channels, resource-safe processing, backpressure
argument-hint: "[scope]"
related:
  - follow-lib-effect-ts
  - run-test
  - resolve-errors
---

## Goal

Use `Stream` for lazy/pull-based data processing — from collection/IO sources, transform, sink, resource-safe

## Scope

`Stream<A, E, R>` — streaming sources/transforms/sinks; backpressure built-in; unlike `Effect` (one-shot) it emits many values lazily

## Execute

### 1. Create Streams

```ts
import { Stream } from "effect"

Stream.make(1, 2, 3)                  // values
Stream.fromIterable(list)             // collections
Stream.fromEffect(fetch())            // single effect
Stream.paginate(seed, fn)             // paginated APIs
Stream.fromReadableStream(() => rs, onError)  // Web streams interop
```

### 2. Transform

- `Stream.map`, `filter`, `mapEffect` (effectful element-wise), `filterMap`
- `Stream.mapConcat` (flatMap), `Stream.zip`, `merge`, `concat`
- `Stream.grouped`/`rechunk` — batch elements; `Stream.throttle`, `debounce`
- `Stream.take`/`takeWhile`/`drop`/`runHead` — bounded consumption

### 3. Consume With Sinks

```ts
Stream.runCollect(stream)             // Chunk<A>
Stream.runForEach(stream, fn)         // effectful per element
Stream.runDrain(stream)               // discard results, run effects
stream.pipe(Stream.toReadableStream)  // back to Web streams
```

- `Sink.fold`, `Sink.collectAll`, `Sink.forEach` — composable consumers
- `Channel` = a lower-level pull/push primitive for custom stream transforms

### 4. Resource Safety

- `Stream.unwrapScoped` / `Stream.acquireRelease` — resource per element/stream
- `Stream.run` inside `Effect.scoped` — release guaranteed
- Error handling: `Stream.catchAll`, `catchTag`, `retry(Schedule)`

## Rules

- Stream is pull-based lazy — it doesn't run until consumed (unlike eager `Effect.all`)
- Effectful per-element ops use `mapEffect`/`runForEach` — not collect-then-forEach
- Bounded memory: use `grouped`/`buffer` capacity options — unbounded buffer = OOM
- Streams holding resources (sockets, files) must use acquireRelease/scoped

## Expected Outcome

- Streaming pipelines lazy + backpressured + resource-safe
- Interop with Web streams/iterables in the right direction
