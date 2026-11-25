---
name: aws-eventbridge-archive
description: >
  Amazon EventBridge event archives and replay for owned event buses: archive
  filters, retention, replay windows, IAM, and safe replay into prod vs isolated
  buses. Use when implementing auditability or reprocessing of events — not for
  replaying events into systems you do not own.
---

# AWS EventBridge Archive

## Scope And Authorization

- **In scope:** EventBridge buses, archives, and replays in AWS accounts you operate under authorization.
- **Out of scope:** Injecting or replaying events against third-party buses/applications.
- Replays can duplicate side effects (charges, emails, shipments) — always assess idempotency first.
- Archives may store sensitive payloads — encrypt, restrict IAM, set retention.
- Pair consumer idempotency with `code-quality-standards` and `retry-backoff-patterns`.

## When To Use

- Creating archives on custom or partner buses for compliance/debug.
- Replaying a time window after consumer downtime or bug fix.
- Filtering archives by event pattern to reduce storage.
- Isolating replay to a staging bus before production.
- Reviewing IAM for `events:StartReplay` / archive read.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Schema registry / EventBridge schemas | schema skill |
| General async API docs | `asyncapi-specs-basics` |
| Lambda event sources | `aws-lambda-event-source-mapping` |
| App idempotency patterns | messaging/reliability skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Archive | Stored copy of events from a source bus matching optional pattern |
| Retention | Days to keep events in archive |
| Replay | Re-inject events into a bus for a time range |
| Event pattern | Same filtering language as rules |
| Side effects | Consumers must be idempotent or feature-flagged during replay |

## Safe Replay Decision Tree

```text
Are consumers idempotent?
  no → fix consumers or replay to isolated bus/dev rules only
  yes → can you filter to only failed event types?
          yes → filtered archive/replay
          no → full window with rate awareness
```

## Workflow

### 1. Confirm scope and success criteria

1. Record bus name, event types, consumers, data class, retention needs.
2. Success: archive capturing expected events; replay restores processing without double business harm; IAM limited.
3. Identify owners who approve production replays.

### 2. Inventory buses and archives

```bash
aws events list-event-buses
aws events list-archives
aws events describe-archive --archive-name "$ARCHIVE"
aws events list-replays
aws events list-rules --event-bus-name "$BUS"
```

1. Map rules/targets per event type.
2. Note whether archive pattern excludes high-volume noisy events intentionally.

### 3. Baseline

1. Sample event JSON (redact PII) for pattern writing.
2. Measure daily event volume for cost/retention sizing.
3. Document consumer idempotency keys (e.g., event.id).

### 4. Create archive and plan replay

```bash
aws events create-archive \
  --archive-name orders-archive \
  --event-source-arn arn:aws:events:REGION:ACCT:event-bus/orders \
  --retention-days 90 \
  --event-pattern '{"source":["app.orders"],"detail-type":["OrderCreated","OrderPaid"]}'
```

**Replay (prefer non-prod targets first):**

```bash
aws events start-replay \
  --replay-name orders-fix-2026-07-01 \
  --event-source-arn arn:aws:events:REGION:ACCT:archive/orders-archive \
  --event-start-time 2026-07-01T00:00:00Z \
  --event-end-time 2026-07-01T06:00:00Z \
  --destination '{"Arn":"arn:aws:events:REGION:ACCT:event-bus/orders-replay"}'
```

**Patterns for safety**

1. Create a **replay bus** with rules only to fixed consumers under feature flag.
2. Or disable non-idempotent targets before replaying to prod bus.
3. Use smallest time window and event pattern possible.
4. KMS CMK for archives when org requires; restrict `events:DescribeArchive` / start replay.

**IAM**

- Operators: `events:StartReplay`, `ListReplays`, `CancelReplay` on specific ARNs.
- Deny broad replay in prod accounts for general developers via SCP/permission boundaries if needed.

### 5. Verify with evidence

```bash
aws events describe-archive --archive-name orders-archive
aws events describe-replay --replay-name orders-fix-2026-07-01
# Consumer metrics: processed count, duplicate skips, error rate
```

1. Inject test event → appears in archive (allow for delay).
2. Replay window → expected consumer invocations; no unexpected targets.
3. Confirm archive encryption and access logs/CloudTrail for StartReplay.

### 6. Observe and harden

1. Alarm on failed replays; dashboard for archive size/cost.
2. Alert Security on StartReplay in production.
3. Periodic review: retention still justified; patterns still correct after schema changes.

### 7. Hand off

1. Runbook: who approves, steps to disable side effects, replay command, validation.
2. Document event `id` idempotency requirements for all new consumers.
3. Link schema/AsyncAPI docs for event types archived.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Replay target | isolated bus or idempotent consumers | blind prod replay to email/charge systems |
| Window | minimal filtered range | entire year “just in case” |
| IAM | break-glass operators | all engineers StartReplay |
| Payload | retention + encryption | infinite keep of PII |
| Prep | consumer dual-write flags | hope duplicates are fine |
| Audit | CloudTrail + ticket | ad-hoc CLI without record |

## Output Checklist

- [ ] Bus, event types, consumers, authorization recorded
- [ ] Idempotency assessment done
- [ ] Archive pattern + retention set
- [ ] IAM for archive/replay least privilege
- [ ] Replay dry-run to isolated path evidenced
- [ ] Production replay approval path defined
- [ ] CloudTrail/alerts for StartReplay
- [ ] Cost/retention reviewed
- [ ] `code-quality-standards` applied to consumer fixes

## Rules

- Owned buses only; replays create real side effects.
- Never replay into production without idempotency or mitigations.
- Minimize window and event types.
- Treat archives as sensitive data stores.
- Focus on archive/replay; broader event design in AsyncAPI/schema skills.
