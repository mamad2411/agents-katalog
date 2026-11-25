---
name: effect-stream
description: Build effectful pull-based streaming pipelines with Effect Stream — creation, transformation, consumption, NDJSON/SchemaBinary encoding, concurrency, resource safety. Use when working with values produced over time, paginated APIs, event listeners, or streaming I/O.
---

You are an Effect TypeScript expert specializing in pull-based streaming with `Stream`, `Sink`, and `Channel`.

## Effect Source Reference

Baseline: **effect@4.1.0 stable**. Inspect the paths below with
`git show effect@4.1.0:<path>`; main may contain later APIs.

The Effect v4 source is available at `~/.local/share/opencode/repos/github.com/Effect-TS/effect@main/`.
Browse and read files there directly to look up APIs, types, and implementations.

Reference this for:

- Stream constructors and combinators (`packages/effect/src/Stream.ts`)
- Creating streams from various sources (`ai-docs/src/02_stream/10_creating-streams.ts`)
- Consuming and transforming streams (`ai-docs/src/02_stream/20_consuming-streams.ts`)
- Encoding/decoding with NDJSON and SchemaBinary (`packages/effect/src/encoding/`)

## Core Model

A `Stream<A, E, R>` is a program that can emit many `A` values, fail with `E`, and require `R`. Streams are **pull-based with backpressure** and emit chunks internally to amortize effect evaluation. They support monadic composition and error handling similar to `Effect`, adapted for multiple values.

Use a stream when values are naturally many-valued and ordered over time. For one effect repeated only for its side effects, prefer `Effect.repeat` with `Schedule`; see the effect-scheduling skill.

```ts
import { Effect, Schedule, Schema, Sink, Stream } from 'effect';
import { Ndjson, SchemaBinary } from 'effect/encoding';
```

For Node.js readable streams:

```ts
import { NodeStream } from '@effect/platform-node';
```

---

## 1. Creating Streams

Source chooser:

- Values/tests: `Stream.make` or `Stream.fromIterable`.
- Callback boundary consumed by one worker: private `Queue` + `Stream.fromQueue`.
- Broadcast events: private `PubSub` + `Stream.fromPubSub`.
- Current value plus changes: `SubscriptionRef`.
- Schedule outputs/ticks: `Stream.fromSchedule`.
- Paginated pull API: `Stream.paginate`.
- Effect that first reads services/config: `Stream.unwrap`.
- Async iterable/platform source: `Stream.fromAsyncIterable` when no native Effect source exists.

### From values and iterables

```ts
// Fixed values
const s1 = Stream.make(1, 2, 3);

// From any iterable
const s2 = Stream.fromIterable([1, 2, 3, 4, 5]);

// Integer range (inclusive on both ends)
const s3 = Stream.range(1, 100);

// Infinite stream via pure iteration
const s4 = Stream.iterate(1, (n) => n * 2); // 1, 2, 4, 8, ...

// Single value from an effect
const s5 = Stream.fromEffect(Effect.succeed(42));

// Empty stream
const s6 = Stream.empty;
```

### From effects (polling / repeating)

```ts
// Poll an effect on a schedule — useful for metrics, health checks, cache refresh
const samples = Stream.fromEffectSchedule(
	Effect.succeed(3),
	Schedule.spaced('30 seconds')
).pipe(Stream.take(10));

// Repeat an effect forever (no schedule delay)
const forever = Stream.fromEffectRepeat(Effect.succeed('tick'));
```

`Stream.repeat(source, schedule)` and `Stream.forever(source)` repeat the whole
source, closing each completed run's scope before starting the next one. Keep
per-run acquisitions inside the source so they release between iterations;
resources that must span repetitions belong to an outer owning scope.

### Paginated APIs

`Stream.paginate` drives cursor-based pagination. Return the current page and `Option.some(nextCursor)` or `Option.none()` to stop.

```ts
import * as Option from 'effect/Option';

const fetchAllPages = Stream.paginate(
	0, // initial cursor
	Effect.fn(function* (page) {
		yield* Effect.sleep('50 millis'); // simulate network
		const results = Array.from(
			{ length: 100 },
			(_, i) => `Job ${i + 1 + page * 100}`
		);
		const nextPage = page < 10 ? Option.some(page + 1) : Option.none();
		return [results, nextPage] as const;
	})
);
```

### From async iterables

```ts
class IterError extends Schema.TaggedError<IterError>()('IterError', {
	cause: Schema.Defect()
}) {}

async function* generate() {
	yield 'a';
	yield 'b';
	yield 'c';
}

const letters = Stream.fromAsyncIterable(
	generate(),
	(cause) => new IterError({ cause })
);
```

### From DOM events

```ts
// Direct event listener binding
const clicks = Stream.fromEventListener<PointerEvent>(button, 'click');
```

### From callback-based APIs

`Stream.callback` gives you a `Queue` to push values into. Use `Effect.acquireRelease` inside to register/unregister listeners with guaranteed cleanup.

Registration runs before the first downstream pull, so callback sources can
prepare immediately without waiting for demand. This does not remove the need
for an explicit readiness handshake when another fiber must publish only after
registration has finished.

```ts
const callbackStream = Stream.callback<PointerEvent>(
	Effect.fn(function* (queue) {
		function onEvent(event: PointerEvent) {
			Queue.offerUnsafe(queue, event);
		}
		yield* Effect.acquireRelease(
			Effect.sync(() => button.addEventListener('click', onEvent)),
			() =>
				Effect.sync(() => button.removeEventListener('click', onEvent))
		);
	})
);
```

Options: `{ bufferSize?: number, strategy?: "sliding" | "dropping" | "suspend" }`

### Queue completion and terminal batches

For a queue-backed source, `Queue.end` stops new offers but lets buffered values
drain before `Cause.Done`; `Queue.fail` likewise drains before its error.
`Queue.takeN` / `takeBetween` can return a final batch smaller than their requested
minimum once closing begins. An open queue with a partial batch stays suspended
until its batching threshold is reached; it does not busy-loop on each offer.
Do not interpret a short terminal batch as malformed input.

<!-- typecheck -->
```ts
import { Cause, Effect, Queue } from 'effect';

const program = Effect.gen(function* () {
	const queue = yield* Queue.bounded<number, Cause.Done>(8);
	yield* Queue.offerAll(queue, [1, 2]);
	yield* Queue.end(queue);
	const finalBatch = yield* Queue.takeN(queue, 5); // [1, 2]
	const terminal = yield* Effect.exit(Queue.take(queue)); // Done
	return { finalBatch, terminal };
});
```

Interrupted pending `offer` / `offerAll` producers withdraw their unaccepted
values even during closing, allowing the queue to finish. `Queue.shutdown`
discards buffered messages immediately; `shutdownUnsafe` is the synchronous
callback equivalent. Both return `false` if already completed or shut down.
They preserve an existing closing cause; an open queue shuts down by interruption.

### From ReadableStream (DOM/Web)

Reader locks are released on every exit. With `releaseLockOnEnd` enabled, the
reader is released rather than canceled; otherwise rejected reader cancellation
is surfaced as a defect, not silently ignored.

<!-- typecheck -->
```ts
import { Stream } from 'effect';
import * as Schema from 'effect/Schema';

class ReadError extends Schema.TaggedError<ReadError>()('ReadError', {
	cause: Schema.Unknown
}) {}

// Select this branch only after the boundary has established a body exists.
const fromWebBody = (body: ReadableStream<Uint8Array>) =>
	Stream.fromReadableStream({
		evaluate: () => body,
		onError: (cause) => new ReadError({ cause }),
		releaseLockOnEnd: false // default; true releases lock instead of canceling
	});
```

### From Node.js readable streams

<!-- typecheck -->
```ts
import { NodeStream } from '@effect/platform-node';
import { Readable } from 'node:stream';
import * as Schema from 'effect/Schema';

class NodeErr extends Schema.TaggedError<NodeErr>()('NodeErr', {
	cause: Schema.Defect()
}) {}

const nodeStream = NodeStream.fromReadable({
	evaluate: () => Readable.from(['Hello', ' ', 'world']),
	onError: (cause) => new NodeErr({ cause }),
	closeOnDone: true // true by default
});
```

For bounded collection of a Node readable, use `NodeStream.toString`, `NodeStream.toArrayBuffer`, or `NodeStream.toUint8Array` with `maxBytes`. The limit is inclusive: `maxBytes: 0` permits an empty stream but fails through `onError` as soon as any byte is received, and the consumer destroys the readable on interruption or failure.

```ts
const text = NodeStream.toString(() => readable, {
	maxBytes: 0,
	onError: (cause) => new NodeErr({ cause })
});
```

### Advanced constructors

```ts
// Unwrap: create a stream from an effect that returns a stream
const unwrapped = Stream.unwrap(Effect.succeed(Stream.make(1, 2, 3)));

// From a Channel directly
const fromChan = Stream.fromChannel(myChannel);
```

---

## 2. Transforming Streams

Choose `map` for pure work, `mapEffect` for effectful work, and bounded `mapEffect(..., { concurrency })` for parallel work. Add `unordered: true` only when output order is irrelevant. Use `flatMap` for zero/many outputs, `filter`/`filterEffect` for selection, and `mapAccum`/`mapAccumEffect` for stateful transforms.

### Pure transforms

```ts
// Per-element mapping (receives element and index)
stream.pipe(Stream.map((value, index) => value * 2));

// Filter elements
stream.pipe(Stream.filter((x) => x > 10));

// Windowing
stream.pipe(Stream.take(5)); // first 5 elements
stream.pipe(Stream.drop(3)); // skip first 3
stream.pipe(Stream.takeWhile((x) => x < 100));
```

### Effectful transforms

```ts
// mapEffect with concurrency control
stream.pipe(
	Stream.mapEffect((order) => enrichOrder(order), { concurrency: 4 })
);
```

A synchronous throw from a concurrent mapping callback is reported as a defect
inside its worker fiber; it does not become a typed mapping error. Lift expected
throwable operations with `Effect.try` / `tryPromise` at their boundary.

### FlatMap

Transform each element into a stream and flatten. Supports concurrency.

```ts
Stream.make('US', 'CA', 'NZ').pipe(
	Stream.flatMap(
		(country) =>
			Stream.range(1, 50).pipe(
				Stream.map((i) => ({ id: `${country}_${i}`, country }))
			),
		{ concurrency: 2 }
	)
);
```

### Accumulation

```ts
// Running accumulator — emits initial state plus each accumulated state
// Output: [0, 1, 3, 6]
Stream.make(1, 2, 3).pipe(Stream.scan(() => 0, (acc, n) => acc + n));

// Effectful variant
Stream.make(1, 2, 3).pipe(
	Stream.scanEffect(() => 0, (acc, n) => Effect.succeed(acc + n))
);
```

`scan` emits its seed even when the source is empty. The seed thunk runs once
per stream execution, not once per emitted chunk.

### Grouping and batching

```ts
// Group into fixed-size chunks
stream.pipe(Stream.grouped(100));

// Group by size OR time window (whichever comes first)
stream.pipe(Stream.groupedWithin(100, '1 second'));
```

`groupedWithin` starts its duration when the group's first element arrives;
an idle stream does not wake just to emit an empty group. `aggregateWithin`
steps its schedule at most once per aggregation, with the previous output as
input. Idle time between aggregations is hidden from the schedule; prefer
`Schedule.spaced` for a flush timer. Schedule completion emits the current
aggregation and sink leftovers, then stops without further upstream pulls.

### Rate control

```ts
// Debounce — emit only the latest element after a pause
stream.pipe(Stream.debounce('300 millis'));

// Throttle — control throughput
stream.pipe(
	Stream.throttle({
		cost: () => 1,
		units: 10,
		duration: '1 second',
		strategy: 'shape' // "shape" delays, "enforce" drops
	})
);

// Timeout — end stream if no element produced within duration
stream.pipe(Stream.timeout('5 seconds'));

// Timeout with fallback — switch to another stream on timeout
stream.pipe(
	Stream.timeoutOrElse({
		duration: '5 seconds',
		orElse: () => Stream.make(fallbackValue)
	})
);
```

Both `timeout` and `timeoutOrElse` are dual functions. `timeout` is implemented as `timeoutOrElse` with `Stream.empty` as the fallback. Non-finite durations return the stream unchanged; zero duration immediately switches to `orElse`.

### Indexing and neighbors

```ts
stream.pipe(Stream.zipWithIndex); // [A, number]
stream.pipe(Stream.zipWithNext); // [A, Option<A>]
stream.pipe(Stream.zipWithPrevious); // [Option<A>, A]
stream.pipe(Stream.zipWithPreviousAndNext); // [Option<A>, A, Option<A>]
```

---

## 3. Consuming Streams

All `run*` methods return `Effect` values — the stream is only pulled when the effect is executed.

Use `runForEach` for side-effecting consumers, `runDrain` when values are irrelevant, and `runFold` for bounded aggregation. Reserve `runCollect` for tests and known-finite, memory-bounded streams; never collect an unbounded production event stream. In tests, prefer `take(n)` + `runCollect`.

For stream tests, use `fromIterable` for finite fixtures, `empty` for no events, and a test-owned `Queue` plus `fromQueue` when the test must drive events interactively. Coordinate with `Deferred`, `Queue`, `Latch`, or `TestClock`, never real sleeps.

```ts
// Collect all elements into an array
const all = Stream.runCollect(stream);
// Effect<Array<A>, E, R>

// Run for side effects, ignore output
const drained = Stream.runDrain(stream);
// Effect<void, E, R>

// Execute effectful consumer per element
stream.pipe(Stream.runForEach((item) => Effect.log(`Got: ${item}`)));
// Effect<void, E, R>

// Fold to a single value (initial is a LazyArg — a thunk)
stream.pipe(
	Stream.runFold(
		() => 0,
		(acc, n) => acc + n
	)
);
// Effect<number, E, R>

// First / last element as Option
Stream.runHead(stream); // Effect<Option<A>, E, R>
Stream.runLast(stream); // Effect<Option<A>, E, R>

// Count / Sum helpers
Stream.runCount(stream); // Effect<number, E, R>
Stream.runSum(stream); // Effect<number, E, R> (stream must be Stream<number>)

// Consume with a Sink
stream.pipe(
	Stream.map((order) => order.totalCents),
	Stream.run(Sink.sum)
);
```

---

## 4. Encoding & Decoding (NDJSON / SchemaBinary)

Use `Stream.pipeThroughChannel` with codec channels from `effect/encoding`.

```ts
import { Ndjson, SchemaBinary } from 'effect/encoding';
```

### Schema-derived binary frames

<!-- typecheck -->
```ts
import { Stream } from 'effect';
import * as Schema from 'effect/Schema';
import { SchemaBinary } from 'effect/encoding';

class Reading extends Schema.Class<Reading>('Reading')({
	id: Schema.String,
	value: Schema.Number
}) {}

const roundTrip = Stream.make(new Reading({ id: 'sensor-1', value: 21 })).pipe(
	Stream.pipeThroughChannel(SchemaBinary.encode(Reading)()),
	Stream.pipeThroughChannel(SchemaBinary.decode(Reading, { maxFrameSize: 1024 })()),
	Stream.runCollect
);
```

`encode(schema)()` and `decode(schema)()` are channel factories; use them with
`Stream.pipeThroughChannel`. Input chunks can split or concatenate frames.
The decoder retains completed values before a later failure and fails with
`Schema.SchemaError` on an incomplete final frame. Decoding/encoding services
from schema transformations remain in the channel requirements. `maxFrameSize`
limits decoding only. Keep paired schemas/options compatible, and copy any
arena-backed encoded bytes that must survive later writes. For synchronous
framing/dictionaries use `SchemaBinary.encoder` and `parser`; `duplex` adapts a
bidirectional channel. See `effect-schema-composition` for codec layout,
fingerprints, and ownership. Use `RpcSerialization.layerSchemaBinary` for RPC.

### Text decoding (split multi-byte characters)

To turn a byte stream into text, use `Stream.decodeText` (or `Channel.decodeText`) rather than hand-rolling `new TextDecoder().decode(chunk)` per chunk. These helpers decode with streaming enabled, so multi-byte UTF-8 characters split across `Uint8Array` chunk boundaries are reassembled correctly; per-chunk `TextDecoder` calls would corrupt characters that straddle a boundary.

```ts
byteStream.pipe(Stream.decodeText, Stream.runForEach(handleText));
```

### NDJSON — string variants

```ts
// Decode: raw NDJSON string → parsed JSON objects
rawStream.pipe(
	Stream.pipeThroughChannel(Ndjson.decodeString()),
	Stream.runCollect
);

// Decode with schema validation
rawStream.pipe(
	Stream.pipeThroughChannel(Ndjson.decodeSchemaString(MySchema)()),
	Stream.runCollect
);

// Encode: objects → NDJSON strings
objectStream.pipe(
	Stream.pipeThroughChannel(Ndjson.encodeString()),
	Stream.runCollect
);

// Encode through schema (applies transforms like date formatting)
typedStream.pipe(
	Stream.pipeThroughChannel(Ndjson.encodeSchemaString(MySchema)()),
	Stream.runCollect
);
```

### NDJSON — binary variants (Uint8Array)

For TCP sockets, file descriptors, etc.

```ts
binaryStream.pipe(Stream.pipeThroughChannel(Ndjson.decode())); // Uint8Array → objects
objectStream.pipe(Stream.pipeThroughChannel(Ndjson.encode())); // objects → Uint8Array
```

### NDJSON options

```ts
// Ignore blank lines instead of raising NdjsonError
Stream.pipeThroughChannel(Ndjson.decodeString({ ignoreEmptyLines: true }));
```

Use SchemaBinary for a schema-derived binary contract and NDJSON for JSON
interoperability. Both peers must agree on the wire format and schema.

### Realistic pipeline: decode → transform → re-encode

```ts
const pipeline = rawNdjsonStream.pipe(
	Stream.pipeThroughChannel(Ndjson.decodeSchemaString(LogEntry)()),
	Stream.filter((entry) => entry.level === 'error'),
	Stream.pipeThroughChannel(Ndjson.encodeSchemaString(LogEntry)()),
	Stream.runCollect
);
```

### Handling encoding errors

`Ndjson.NdjsonError` has a `kind` field: `"Pack"` (encoding) or `"Unpack"` (decoding).

```ts
rawStream.pipe(
	Stream.pipeThroughChannel(Ndjson.decodeString()),
	Stream.catchTag('NdjsonError', (err) =>
		Stream.succeed({ recovered: true, kind: err.kind })
	),
	Stream.runCollect
);
```

---

## 5. Error Handling

### catchTag / catchTags

Recover from specific tagged errors, producing a fallback stream.

```ts
stream.pipe(
	Stream.catchTag('NetworkError', (err) => Stream.succeed(fallbackValue))
);
```

### retry

Retry a failing stream with a schedule. The stream restarts from the beginning on each retry.

```ts
stream.pipe(Stream.retry(Schedule.recurs(3)));

// With exponential backoff
stream.pipe(Stream.retry(Schedule.exponential('100 millis')));
```

Schedules can be effectful and fail. `Stream.retry` includes the schedule's error in the resulting stream error channel; `Effect.schedule` and `Effect.scheduleFrom` likewise union schedule errors into their error channels. Recover or map that error explicitly rather than assuming only the repeated operation can fail. For sequential schedule composition, use `Schedule.concat` / `Schedule.concatResult`; the former `andThen` names were removed.

`Stream.retry` resets its schedule after the first successfully emitted element.
Retries use constant call stack even for synchronous failures. As with Effect
typed recovery, a cause containing a defect bypasses retry/catches and promotes
all typed errors to defects, preserving reason order and interrupts. Typed error
plus interruption without a defect can recover/retry; pure interruption cannot.
`Stream.mapError` instead maps every typed error in place without promotion.

### Execution-plan attempt events

`Stream.withExecutionPlan` accepts an `onEvent` observer for attempt-level logs and metrics:

```ts
const planned = stream.pipe(
	Stream.withExecutionPlan(plan, {
		onEvent: (event) => Effect.log('execution plan event', event)
	})
);
```

Events are `AttemptStart`, `AttemptSuccess`, or `AttemptFailure`. Every start has one terminal event, failures carry the full `Cause`, and `attempt` is cumulative while `stepAttempt` is 1-based within a step. The observer must have a `never` error channel; an observer defect is isolated from the attempt outcome and does not leave events unpaired. If a downstream consumer intentionally stops pulling early, the truncated attempt is reported as successful.

### orElseIfEmpty / orElseSucceed

```ts
// Provide a default stream if the source emits nothing
stream.pipe(Stream.orElseIfEmpty(() => Stream.make(defaultValue)));

// Provide a single fallback value when the source fails
stream.pipe(Stream.orElseSucceed((error) => defaultValue));
```

---

## 6. Concurrency & Merging

### Buffer policy

Prefer natural backpressure. Add `Stream.buffer` only to deliberately decouple producer and consumer: `"suspend"` backpressures when full, `"dropping"` drops new values, and `"sliding"` drops old values to retain the latest. Avoid `capacity: "unbounded"` unless growth is bounded elsewhere and documented.

`Stream.partition` returns `[passes, fails]` and accepts `{ capacity }` (default
16). Consume both sides concurrently to avoid blocking a full partition.

Ending a partition or `groupBy` consumer early releases its queue rather than
leaving producers blocked on a consumer that will never drain it. Active slow
consumers can still exert backpressure.
`Stream.mapBoth` takes `onElement` / `onError`. `catchTags` rejects unknown tag
keys; `catchDefect` handles defects separately from typed failures/interruption.
`tapDefect`, `tapErrorTag`, and `unwrapReason` provide targeted observation/recovery.
Use `Channel.runDrain` to consume channel output and return its completion value.

### merge

Interleave elements from two streams concurrently in arrival order.

```ts
Stream.merge(streamA, streamB);
Stream.merge(streamA, streamB, { haltStrategy: 'left' }); // stop when left ends
// HaltStrategy: "left" | "right" | "both" | "either"
```

### mergeAll

Merge many streams concurrently. The streams are passed as a single **iterable**, followed by the options.

```ts
Stream.mergeAll([streamA, streamB, streamC], {
	concurrency: 4
});
```

### interleave

Deterministically alternate elements from two streams (round-robin).

```ts
Stream.interleave(left, right);

// Custom interleave pattern via boolean decider stream
Stream.interleaveWith(left, right, Stream.make(true, false, false, true));
```

### mergeResult

Tag values from two streams: left as `Result.succeed`, right as `Result.fail`.

```ts
Stream.mergeResult(left, right); // Stream<Result<LeftA, RightA>>
```

### mergeEffect

Run a background effect concurrently with a stream; keep the stream's elements.

```ts
stream.pipe(Stream.mergeEffect(Effect.log('background task')));
```

### zipWith

Pair elements from two streams positionally.

```ts
Stream.zipWith(numbersStream, labelsStream, (n, label) => `${label}: ${n}`);
```

### broadcast

PubSub-backed multicast: the source is consumed once and fanned out to every subscriber. Returns a scoped effect, and the **producer starts immediately** — it does not wait for subscribers to attach.

```ts
Effect.scoped(
	Effect.gen(function* () {
		const shared = yield* stream.pipe(
			Stream.broadcast({ capacity: 16, replay: 3 })
		);
		// Each consumer subscribes independently. Because the producer starts
		// immediately, a late subscriber only sees values still held in `replay`.
		const fiberA = yield* Stream.runCollect(shared).pipe(Effect.forkChild);
		const fiberB = yield* Stream.runCollect(shared).pipe(Effect.forkChild);
		// ...
	})
);
```

Options: `{ capacity: number | "unbounded", strategy?: "sliding" | "dropping" | "suspend", replay?: number }`

Because the producer starts immediately, subscribers that attach after the source has already emitted will miss earlier values unless `replay` is configured (and `replay` only retains the most recent N values — it is not a full log). For a **fixed, known set of consumers**, prefer `broadcastN`: it subscribes all downstream streams before starting the source, so none of them miss values.

Completion and failure are retained separately from ordinary values:
`broadcast`, `broadcastN`, `share`, and `toPubSubTake` end their underlying PubSub
with the source's terminal exit. Current and late subscribers observe that exit
after buffered/replayed values, even if a dropping buffer was full. This does
not replay earlier data. For `toPubSubTake`, consume with `Stream.fromPubSubTake`
so the terminal `Take` is interpreted as completion/failure.

### broadcastN

Fixed-fanout multicast produces a tuple of `n` streams; the source starts only **after all `n` downstream streams have been subscribed**, so every consumer sees the full sequence without needing `replay`. If a downstream stream is interrupted, it unsubscribes and no longer contributes backpressure.

```ts
Effect.scoped(
	Effect.gen(function* () {
		const [left, right] = yield* Stream.make(1, 2, 3).pipe(
			Stream.broadcastN({ n: 2, capacity: 8 })
		);

		const [leftValues, rightValues] = yield* Effect.all(
			[Stream.runCollect(left), Stream.runCollect(right)],
			{ concurrency: 'unbounded' }
		);
		// leftValues and rightValues each === [1, 2, 3]
	})
);
```

Options: `{ n: number, capacity: number | "unbounded", strategy?: "sliding" | "dropping" | "suspend", replay?: number }`

### share

Like broadcast but subscribes lazily when the first consumer starts, keeps upstream alive while consumers exist.

```ts
const shared = yield* stream.pipe(Stream.share({ capacity: 16 }));
```

---

## 7. Resource Safety

### Long-lived service consumers

Expose `Stream` values from service interfaces while keeping producer `Queue`, `PubSub`, and mutable state private. Own long-lived consumers in a layer and ordinarily run them with `stream.pipe(Stream.runForEach(handle), Effect.forkScoped)` so layer shutdown interrupts the consumer.

`forkScoped` provides lifetime supervision, not failure recovery or restart supervision. A failed child fiber does not automatically fail its parent or restart itself. If consumer failure must stop the application, restart with policy, or be reported, explicitly join/monitor the fiber or install a supervisor at the owning runtime boundary. Preserve interruption as shutdown; do not blanket-catch causes and turn interruption into a retry loop.

### scoped

Run a stream that requires `Scope` in a managed scope, ensuring finalizers run when the stream completes.

```ts
const safeStream = Stream.scoped(
	Stream.fromEffect(
		Effect.acquireRelease(
			Effect.log('acquire').pipe(Effect.as('resource')),
			() => Effect.log('release')
		)
	)
);
// Stream<string, never, never> — Scope is eliminated
```

`Stream.scoped` provides its managed scope to **pull effects**, including effects created by `Stream.fromEffect` and sequential `Stream.mapEffect`. `Effect.acquireRelease` finalizers inside those pulls run when the stream completes.

### unwrap

Create a stream from an effect that produces a stream. The outer effect runs once; the inner stream is then consumed.

```ts
const stream = Stream.unwrap(
	Effect.gen(function* () {
		const config = yield* loadConfig;
		return Stream.fromIterable(config.items);
	})
);
```

### callback with acquireRelease

The `Stream.callback` constructor accepts a scoped effect, so you can register and unregister resources:

```ts
Stream.callback<Event>(
	Effect.fn(function* (queue) {
		yield* Effect.acquireRelease(
			Effect.sync(() =>
				emitter.on('data', (e) => Queue.offerUnsafe(queue, e))
			),
			() => Effect.sync(() => emitter.removeAllListeners('data'))
		);
	})
);
```

---

## 8. Piping Through Channels

`Stream.pipeThroughChannel` connects a stream to a `Channel` for encode/decode, compression, framing, etc.

```ts
// pipeThroughChannel: upstream errors flow into the channel
stream.pipe(Stream.pipeThroughChannel(myChannel));

// pipeThroughChannelOrFail: upstream errors preserved alongside channel errors
stream.pipe(Stream.pipeThroughChannelOrFail(myChannel));
```

---

## Key Patterns

### Pagination → transform → consume

```ts
const pipeline = Stream.paginate(0, fetchPage).pipe(
	Stream.mapEffect(enrichItem, { concurrency: 8 }),
	Stream.filter((item) => item.isValid),
	Stream.grouped(50),
	Stream.runForEach((batch) => writeBatch(batch))
);
```

### Event stream → debounce → side effect

```ts
const autosave = Stream.fromEventListener(input, 'input').pipe(
	Stream.debounce('500 millis'),
	Stream.mapEffect((e) => saveDocument(e.target.value)),
	Stream.runDrain
);
```

### Decode NDJSON file → filter → re-encode

```ts
const filterErrors = fileStream.pipe(
	Stream.pipeThroughChannel(Ndjson.decodeSchemaString(LogEntry)()),
	Stream.filter((entry) => entry.level === 'error'),
	Stream.pipeThroughChannel(Ndjson.encodeSchemaString(LogEntry)()),
	Stream.runCollect
);
```

### Retry with backoff

```ts
const resilient = unreliableStream.pipe(
	Stream.retry(
		Schedule.exponential('100 millis').pipe(Schedule.upTo({ times: 5 }))
	),
	Stream.runCollect
);
```

`Schedule.upTo({ times: n })` bounds an unbounded schedule to `n` recurrences. To log full retry metadata without changing the schedule's behavior, add `Schedule.tap`, whose callback receives `{ attempt, input, output, duration, elapsed }`:

```ts
const monitored = Schedule.exponential('100 millis').pipe(
	Schedule.upTo({ times: 5 }),
	Schedule.tap((meta) =>
		Effect.log(
			`attempt ${meta.attempt}, next delay ${meta.duration}, elapsed ${meta.elapsed}`
		)
	)
);
```

### Completion, failures, and bounded pulls

`Stream.groupBy` / `groupByKey` end their groups when upstream ends or fails.
`grouped` / `rechunk` emit buffered elements before an upstream failure.
Upstream failures in `run`, `peel`, `aggregate`, and `aggregateWithin` bypass
`Sink.mapError`, `catch`, `catchCause`, and `orElse`; `Sink.onExit` observes them
as interruption. Recover upstream failures on the stream itself.

For Node stream/socket adapters, `chunkSize` now bounds chunks per pull (default
4096), not byte size. `NodeStream` uses `readSize` for byte read requests;
`chunkSize: Infinity` opts out of the per-pull bound. The unstable
`effect/encoding/Csv` module offers streaming CSV parsing/writing over text or
UTF-8 bytes, with schema adapters through `Schema.toCodecStringTree`.

## Common Mistakes

### Release-specific lifecycle edges

- `switchMap` finalizes the replaced inner stream even if replacement happens
  before that inner starts pulling.
- Unordered `mapEffect` with `concurrency: Infinity` (or a limit larger than the
  input) still awaits all results; it must not complete after an early subset.
- Shaping `throttle` uses monotonic time and retains token debt across chunks;
  wall-clock changes are not a reason to implement a second limiter.
- `decodeText` flushes the decoder at end, including incomplete trailing input;
  byte chunks need not align with characters.
- `toReadableStreamWith(stream, context, { signal })` can interrupt production
  even when the reader stops pulling. Abort closes the Web stream; demand gates
  upstream pulls, not just enqueueing already-pulled chunks. Cancel/abort ownership
  remains necessary when a consumer abandons the stream.

<!-- typecheck -->
```ts
import { Context, Stream } from 'effect';

const controller = new AbortController();
const readable = Stream.toReadableStreamWith(
	Stream.make(1, 2, 3),
	Context.empty(),
	{ signal: controller.signal }
);
controller.abort(); // stops production even without another reader pull
```

1. **Forgetting `runFold` initial is a thunk** — `Stream.runFold(() => 0, f)` not `Stream.runFold(0, f)`
2. **Using `Stream.acquireRelease` when it doesn't exist** — use `Stream.scoped` + `Effect.acquireRelease` or `Stream.callback` with `Effect.acquireRelease` instead
3. **Not specifying `onError` for `fromAsyncIterable` / `fromReadableStream`** — these require an error mapper
4. **Assuming `retry` resumes** — `Stream.retry` restarts the entire stream from the beginning on each retry
5. **Ignoring `haltStrategy` on `merge`** — default is `"both"` (wait for both to end); use `"either"` to stop as soon as one ends
6. **Assuming `forkScoped` supervises failures** — it scopes lifetime only. Explicitly monitor/restart/report long-lived consumers according to the owning service policy.
7. **Collecting open streams** — use `runForEach`/`runDrain` in production and `take(n)` + `runCollect` for finite tests.
