---
name: azure-servicebus-sessions
description: >
  Azure Service Bus message sessions for owned namespaces: session-enabled queues/
  subscriptions, session affinity, ordered processing per SessionId, idle timeouts,
  and processor patterns. Use when requiring per-entity ordering or stateful session
  handlers — not for unauthorized access to third-party namespaces.
---

# Azure Service Bus Sessions

## Scope And Authorization

- **In scope:** Service Bus namespaces, queues, and subscriptions you own or operate.
- **Out of scope:** Reading/dead-lettering messages in foreign namespaces without authorization.
- Session processors hold locks — bugs can stall an entire SessionId partition of work.
- Pair general backpressure with `backpressure-patterns`; SNS FIFO analog `aws-sns-fifo-ordering`.

## When To Use

- Strict ordering per user/order/device (`SessionId`).
- Stateful processing where consecutive messages share handler state.
- Migrating from non-session queues after ordering bugs.
- Tuning session idle timeout and prefetch for throughput.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Event Hubs Capture archives | `azure-eventhubs-capture` |
| General backpressure | `backpressure-patterns` |
| AWS SQS fair queues | `aws-sqs-fair-queues` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Requires session | Queue/subscription flag; all messages need SessionId |
| Session lock | Receiver exclusively processes one session at a time |
| Order | In-order delivery within a session |
| Cross-session | No global order across SessionIds |
| Dead-letter | Poison messages can block progress if not handled |
| Tooling | `az servicebus`, Azure.Messaging.ServiceBus SDK, Portal metrics |

## Workflow

### 1. Confirm scope and success criteria

1. Entity names, ordering key → SessionId strategy, concurrency, authorization.
2. Success: messages for same SessionId processed in order; different sessions parallel.
3. Accept throughput trade-off vs non-session queues.

### 2. Inventory entities

```bash
az account show
az servicebus namespace show -g "$RG" -n "$NS"
az servicebus queue show -g "$RG" --namespace-name "$NS" -n "$Q" --query "{sessions:requiresSession,dupe:requiresDuplicateDetection,ttl:defaultMessageTimeToLive}"
az servicebus topic subscription show -g "$RG" --namespace-name "$NS" --topic-name "$T" -n "$SUB" --query requiresSession
```

1. Note duplicate detection, partitioning, auto-forward.
2. List consumer apps and max concurrent sessions.
3. Check MI/RBAC vs SAS policies (prefer AAD).

### 3. Baseline

1. Define SessionId = business key (e.g. `orderId`), never random per message if order needed.
2. Measure message rates per key for hot sessions.
3. DLQ depth and abandonment patterns.

### 4. Enable sessions and implement processors

```bash
# Queues must be created with --enable-session true (cannot flip arbitrarily on all SKUs/paths)
az servicebus queue create -g "$RG" --namespace-name "$NS" -n "orders-session" \
  --enable-session true \
  --enable-duplicate-detection true \
  --max-delivery-count 10
```

**SDK pattern (conceptual):**

```csharp
await using var client = new ServiceBusClient(ns, new DefaultAzureCredential());
var processor = client.CreateSessionProcessor("orders-session", new ServiceBusSessionProcessorOptions
{
    MaxConcurrentSessions = 16,
    AutoCompleteMessages = false,
    SessionIdleTimeout = TimeSpan.FromSeconds(30)
});
processor.ProcessMessageAsync += async args =>
{
    // process in order within args.Message.SessionId
    await args.CompleteMessageAsync(args.Message);
};
processor.ProcessErrorAsync += _ => Task.CompletedTask;
await processor.StartProcessingAsync();
```

1. Send path must set `Message.SessionId`.
2. Use session state sparingly (`GetSessionState`/`SetSessionState`) — size limits apply.
3. Prefer completing explicitly; handle poison → dead letter without infinite retry.
4. Scale out with `MaxConcurrentSessions`, not multiple competing receivers on same session.
5. Network: private endpoint; RBAC `Azure Service Bus Data Owner/Receiver/Sender` least privilege.

### 5. Verify with evidence

```bash
# Send ordered messages with same SessionId; observe handler order in logs
# Parallel sessions make progress concurrently
az servicebus queue show -g "$RG" --namespace-name "$NS" -n "orders-session" --query countDetails
```

1. Publish 1..N sequence for one session; assert processing order.
2. Inject poison message; confirm session recovers after DLQ.
3. Auth: app MI can receive; random user cannot.

### 6. Observe and harden

1. Metrics: active sessions, server errors, DLQ length, user errors.
2. Alerts on DLQ growth and abandoned message spikes.
3. Hot SessionId keys → shard (`customerId:shard`) only if order can be relaxed within customer.

### 7. Hand off

1. SessionId convention doc for all producers.
2. Consumer options (`MaxConcurrentSessions`, idle timeout) standards.
3. Runbook for stuck sessions / DLQ replay preserving order.

## Design Choices

| Choice | Guidance |
| --- | --- |
| SessionId | Stable business key |
| Concurrent sessions | Match CPU / downstream limits |
| Idle timeout | Balance sticky state vs throughput |
| Duplicate detection | Useful with at-least-once senders |
| Sessions vs partitioning | Different features; don’t confuse |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| IDs | `orderId` session | New GUID each message (no order benefit) |
| Poison | DLQ + alert | Retry forever blocking session |
| Auth | MI + data roles | Namespace listen SAS in mobile app |
| Scale | Many sessions concurrent | Single global session id |
| State | Small session state | Megabytes in session state |

## Output Checklist

- [ ] Session-enabled entity configured
- [ ] SessionId strategy documented
- [ ] Processor options tuned
- [ ] Ordered processing test passed
- [ ] Concurrent multi-session test passed
- [ ] DLQ/poison handling verified
- [ ] RBAC/network hardened
- [ ] Metrics/alerts set
- [ ] `code-quality-standards` applied to producers/consumers

## Rules

- Authorized namespaces only.
- Ordering is per SessionId only.
- Always set SessionId on session entities.
- Prefer AAD/MI over SAS keys.
- Don’t log full message bodies with PII.
