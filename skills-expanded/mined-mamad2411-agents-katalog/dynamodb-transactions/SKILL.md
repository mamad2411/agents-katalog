---
name: dynamodb-transactions
description: >
  Use DynamoDB TransactWriteItems/TransactGetItems correctly: limits, idempotency,
  conditions, isolation semantics, cancellation reasons, and when to avoid transactions
  on owned tables. Use when DynamoDB transactions, TransactWriteItems, transactional
  condition checks, all-or-nothing multi-item updates, or payment-like flows on DynamoDB.
---

# DynamoDB Transactions

## Scope And Authorization

- **In scope:** DynamoDB tables and apps in AWS accounts you operate.
- **Out of scope:** Abusing transactional APIs on foreign accounts; load testing without budget approval.
- Prefer staging verification of conflict rates and latency.
- Redact primary keys that encode customer IDs in public docs.
- Pair with `dynamodb-gsi-design`, idempotency/retry skills, and `code-quality-standards`.

## When To Use

- Multi-item all-or-nothing updates (ledger line + balance).
- Condition checks that must hold across items atomically.
- Preventing double-spend style races with condition expressions.
- Reviewing failures: `TransactionCanceledException` reasons.
- Deciding transactions vs single-item conditional writes vs saga.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| GSI/access pattern design | `dynamodb-gsi-design` |
| Distributed locks in Redis | `distributed-lock-redis-safety` |
| SQL ACID RDBMS | relational transaction skills |
| Retry/backoff | `retry-backoff-patterns` |
| Code quality baseline | `code-quality-standards` |

## Semantics (practical)

| API | Purpose |
| --- | --- |
| `TransactWriteItems` | Atomic write set: Put/Update/Delete/ConditionCheck |
| `TransactGetItems` | Atomic read set (stronger read consistency story for the set) |

| Limit (know current AWS docs) | Typical constraint |
| --- | --- |
| Items per transaction | Low tens (e.g. 100—confirm current) |
| Total size | Bounded MB total payload |
| Same item | Cannot touch same item twice in one transaction |
| Cross-table | Allowed within region/account limits |
| Isolation | Serializable-style for the transaction; know conflicts |

**Idempotency:** Use `ClientRequestToken` on TransactWrite for safe retries.

## Workflow

### 1. Confirm scope and success criteria

1. Business invariant (e.g. balance never negative; unique reservation).
2. Success: races fail cleanly; retries safe; latency/cost acceptable; monitoring on cancellations.
3. Alternative designs considered (single-item aggregate root).

### 2. Prefer simpler options first

| Pattern | When enough |
| --- | --- |
| Single-item conditional update | All state fits one item |
| Optimistic version attribute | Low contention single item |
| Saga + idempotency | Long workflows, external side effects |
| Transaction | True multi-item atomic invariant |

1. Side effects (email, Stripe) **cannot** be in DynamoDB transaction—use outbox pattern.

### 3. Model the transaction

```python
# boto3 sketch
client.transact_write_items(
    ClientRequestToken=idempotency_key,
    TransactItems=[
        {
            "ConditionCheck": {
                "TableName": "accounts",
                "Key": {"pk": {"S": user_id}},
                "ConditionExpression": "balance >= :amt",
                "ExpressionAttributeValues": {":amt": {"N": str(amount)}},
            }
        },
        {
            "Update": {
                "TableName": "accounts",
                "Key": {"pk": {"S": user_id}},
                "UpdateExpression": "SET balance = balance - :amt",
                "ExpressionAttributeValues": {":amt": {"N": str(amount)}},
            }
        },
        {
            "Put": {
                "TableName": "ledger",
                "Item": {
                    "pk": {"S": user_id},
                    "sk": {"S": f"tx#{tx_id}"},
                    "amount": {"N": str(amount)},
                },
                "ConditionExpression": "attribute_not_exists(sk)",
            }
        },
    ],
)
```

1. Encode uniqueness with condition `attribute_not_exists` on ledger key.
2. Include only items required for the invariant.

### 4. Handle cancellation and conflicts

```text
TransactionCanceledException
  → inspect CancellationReasons[] per item
  → ConditionalCheckFailed vs ValidationError vs Throughput
```

1. Map reasons to user errors vs retryable.
2. Retry only with same `ClientRequestToken` when appropriate; change token only for new business op.
3. High conflict: redesign keys to reduce contention or serialize via single item.

### 5. Cost, latency, limits

1. Transactions cost more than single writes—budget.
2. Avoid huge items in transactional sets.
3. Do not use transactions as distributed lock across unrelated domains.
4. Confirm current AWS item count/size limits before design freeze.

### 6. Consistency with GSIs and streams

1. GSI updates remain eventually consistent with base—design reads accordingly (`dynamodb-gsi-design`).
2. Streams: transactional writes still produce stream records—consumers must be idempotent.
3. Do not assume global secondary reads see transactional result instantly.

### 7. Verify and hand off

1. Concurrency tests: parallel transact on same keys → one wins, invariant holds.
2. Chaos: retry with same client token → no double ledger.
3. Metrics: cancel rate, latency p99, throttles.
4. Document invariants and token strategy.
5. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Small multi-item invariant | 50 unrelated updates in one tx |
| Idempotency | ClientRequestToken | Blind retry new token every time |
| Side effects | Outbox after commit | Email inside “transaction” hope |
| Contention | Low-conflict keys | Hot balance item without plan |
| Errors | Parse cancellation reasons | Generic 500 always |
| Design | Prefer single-item when possible | Transactions everywhere |

## Output Checklist

- [ ] Invariant and item set documented
- [ ] Limits checked against current AWS docs
- [ ] ClientRequestToken strategy defined
- [ ] ConditionExpressions cover business rules
- [ ] Cancellation handling implemented
- [ ] Concurrency tests pass
- [ ] Retry policy correct
- [ ] Streams/GSI consistency understood
- [ ] Cost/latency acceptable
- [ ] Runbooks for conflict spikes

## Rules

- Transactions are not sagas for external systems.
- Always plan idempotency tokens for TransactWrite.
- Minimize items and contention.
- Owned accounts only; watch cost.
- Focus on DynamoDB transactional API correctness and ops.
