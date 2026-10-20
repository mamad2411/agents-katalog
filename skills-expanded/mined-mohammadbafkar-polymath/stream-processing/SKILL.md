---
name: stream-processing
description: Design stream processing — windowing (tumbling/sliding/session), watermarks for late data, stateful operators, exactly-once, stream-stream/table joins, and CEP.
---

# stream-processing

> Streaming computation is batch computation where the data never stops and time is ambiguous. Decide event-time vs processing-time and your lateness policy first; everything else is detail.

## When to use

- Computing aggregations, joins, or pattern detection over an unbounded stream (Flink/Kafka Streams/Spark Structured Streaming).
- Results are wrong because of late/out-of-order events or unbounded state.
- A workflow invokes `polymath-streaming:stream-processing`.

Not this when: you are designing the topics/partitions/delivery the job consumes — that is `polymath-streaming:streaming-design`. For scheduled batch transforms, `polymath-streaming:data-pipeline`.

## Inputs

- The computation (aggregate, join, detect), the event-time field, and tolerance for late data.
- State size expectations and correctness/latency trade-off.

## Procedure

1. **Event-time vs processing-time**: use *event-time* (when it happened) for correctness; processing-time only when you genuinely don't care about ordering. State which.
2. **Windowing** by the question: *tumbling* (fixed, non-overlapping — "per minute"), *sliding* (overlapping — moving averages), *session* (activity gaps — user sessions). Name the window type and size.
3. **Watermarks + lateness**: set a watermark (how long to wait for late events) and an allowed-lateness policy; decide what happens to events past it (drop, side-output, or late-update). This is the accuracy↔latency dial — make it explicit.
4. **State management**: bound state (TTL/retention) so it doesn't grow forever; choose keyed state; plan checkpointing and the state backend. Unbounded keyed state is the classic OOM.
5. **Delivery/consistency**: for exactly-once results, use the framework's checkpoint + transactional sink; otherwise document at-least-once and make sinks idempotent.
6. **Joins**: stream-stream joins need a time bound (windowed) or state explodes; stream-table (enrichment) joins need a versioned/temporal lookup. State the join type and its bound.
7. **CEP / pattern detection** where required: define the pattern, the time window, and the partition key it's evaluated within.
8. **Reprocessing**: plan how to replay from the log to recompute after a logic change (versioned state / parallel run).

## Output

- A one-page design: event-time decision, window type+size, watermark + lateness policy, bounded-state + checkpoint plan, delivery semantics, join types with time bounds, and the reprocessing path.

## Quality bar

- Event-time vs processing-time is stated, with a watermark + explicit late-data policy.
- All keyed state is bounded (TTL/retention); checkpointing is defined.
- Stream-stream joins are time-bounded; sinks are idempotent or exactly-once.
- There is a documented replay/reprocessing path for logic changes.
