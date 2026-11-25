---
name: csharp-channels-pipelines
description: >
  Design in-process producer/consumer pipelines with System.Threading.Channels
  in owned .NET apps: bounded vs unbounded channels, single/multiple readers,
  backpressure, Completion, and graceful shutdown. Use when replacing ad-hoc
  BlockingCollection queues, building async stages, or controlling concurrency
  without full external message brokers.
---

# C# Channels Pipelines

## Scope And Authorization

- **In scope:** .NET codebases you maintain using `System.Threading.Channels`.
- **Out of scope:** Operating cloud message buses (Kafka/SQS) as the primary design — hand off when durability/cross-process is required.
- Prefer load tests for bounded capacity choices that can block producers under traffic.
- Pair with `code-quality-standards` and `csharp-style-conventions`.

## When To Use

- Async pipelines inside a process (ingest → transform → write).
- Applying backpressure with `BoundedChannelOptions`.
- Fan-out/fan-in with multiple workers reading one channel.
- Clean shutdown: complete writer, drain readers, cancel via `CancellationToken`.
- Migrating from `BlockingCollection` or unbounded `Queue` + lock.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cross-service durable messaging | broker/queue skills |
| ASP.NET Minimal API security | `csharp-minimal-apis-security` |
| Generic math | `csharp-generic-math` |
| Language style only | `csharp-style-conventions` |
| Implementation quality baseline | `code-quality-standards` |

## Channel types

| API | Characteristics |
| --- | --- |
| `Channel.CreateUnbounded<T>()` | No capacity limit — risk memory growth |
| `Channel.CreateBounded<T>(n)` | Backpressure when full |
| `SingleReader` / `SingleWriter` | Optimizations when true |
| `FullMode` | Wait, DropWrite, DropOldest, DropNewest |
| `ChannelReader.Completion` | Signals end of stream |

## Workflow

### 1. Confirm scope and success criteria

1. Stages, expected rates, max acceptable queue latency, durability needs (none for pure in-memory).
2. Success: no unbounded memory under spike; shutdown drains or cancels cleanly; metrics for depth/drops.

### 2. Choose bounded policy

```csharp
var options = new BoundedChannelOptions(capacity: 256)
{
    SingleReader = false,
    SingleWriter = true,
    FullMode = BoundedChannelFullMode.Wait, // backpressure
};
var channel = Channel.CreateBounded<WorkItem>(options);
```

| FullMode | When |
| --- | --- |
| `Wait` | Must not lose items; producers should slow down |
| `DropOldest` | Prefer fresh data (telemetry) |
| `DropWrite` | Prefer shedding new load |
| `DropNewest` | Rare; know the semantics |

### 3. Producer / consumer pattern

```csharp
public sealed class Pipeline
{
    private readonly Channel<WorkItem> _channel =
        Channel.CreateBounded<WorkItem>(new BoundedChannelOptions(1024)
        {
            SingleReader = false,
            SingleWriter = false,
            FullMode = BoundedChannelFullMode.Wait,
        });

    public async Task ProduceAsync(WorkItem item, CancellationToken ct)
        => await _channel.Writer.WriteAsync(item, ct);

    public async Task RunWorkersAsync(int workers, CancellationToken ct)
    {
        var tasks = Enumerable.Range(0, workers)
            .Select(_ => Task.Run(() => ConsumeAsync(ct), ct));
        await Task.WhenAll(tasks);
    }

    private async Task ConsumeAsync(CancellationToken ct)
    {
        await foreach (var item in _channel.Reader.ReadAllAsync(ct))
        {
            await ProcessAsync(item, ct);
        }
    }

    public void Complete() => _channel.Writer.TryComplete();
}
```

### 4. Multi-stage pipelines

```text
Channel A (bounded) → transform workers → Channel B (bounded) → I/O workers
```

1. Each stage has its own capacity matching cost (CPU stage smaller buffer than cheap parse).
2. Propagate completion: when stage N finishes writing, `TryComplete` its writer so stage N+1 exits `ReadAllAsync`.
3. Propagate errors: decide whether to complete with exception (`TryComplete(ex)`) and fail the host.

### 5. Shutdown

1. Stop accepting external input.
2. `Writer.TryComplete()`.
3. Await consumer tasks with linked `CancellationToken` for forced abort after deadline.
4. Do not abandon in-flight work without defining at-least-once side effects policy.

### 6. Observe

```csharp
// Periodic metric: channel.Reader.Count (approx) if available for type;
// track write wait time, process duration, drop counts for Drop* modes
```

### 7. Verify

```bash
dotnet test
# Load test: ensure memory plateaus with bounded Wait/Drop policy
```

Unit test: producer blocked when full (Wait); drops increment when DropWrite; consumers drain after complete.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Capacity | Bounded + measured | Unbounded “temporary” in prod |
| Shutdown | Complete + drain | Fire-and-forget host exit |
| Errors | Defined poison handling | Swallow exceptions in workers |
| Concurrency | Worker count tied to I/O/CPU | Thousands of readers default |
| Broker need | Upgrade to queue when multi-host | Channels across machines via hacks |

## Output Checklist

- [ ] Pipeline stages diagrammed
- [ ] Bounded options and FullMode chosen
- [ ] SingleReader/Writer flags accurate
- [ ] Completion and cancellation path implemented
- [ ] Error/poison policy defined
- [ ] Metrics for depth/latency/drops
- [ ] Tests for backpressure and shutdown
- [ ] Confirmed in-process scope (no durability illusion)
- [ ] `code-quality-standards` applied
- [ ] Residual risk documented

## Rules

- Channels are not a distributed bus — no multi-instance durability.
- Prefer backpressure over silent unbounded queues.
- Focus on **System.Threading.Channels pipelines** in C#.
