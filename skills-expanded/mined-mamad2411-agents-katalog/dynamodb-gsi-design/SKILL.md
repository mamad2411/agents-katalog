---
name: dynamodb-gsi-design
description: >
  Design DynamoDB Global Secondary Indexes: key selection, projection types, sparse indexes,
  fan-out writes, RCU/WCU costing, consistency, and hot partition avoidance on owned tables.
  Use when DynamoDB GSI, secondary index design, projection KEYS_ONLY/INCLUDE/ALL, sparse GSI,
  or access-pattern modeling for single-table/multi-table AWS designs.
---

# DynamoDB GSI Design

## Scope And Authorization

- **In scope:** AWS accounts and DynamoDB tables you operate.
- **Out of scope:** Load testing someone else’s tables; cost attacks.
- Prefer design in staging; GSI creation/backfill has cost and throttling implications.
- Redact production key values in tickets.
- Pair with `dynamodb-transactions`, AWS IAM least privilege, and `code-quality-standards`.

## When To Use

- New access patterns cannot be served by table PK/SK.
- Query by attributes that are not the primary key.
- Designing single-table design indexes.
- Cost review of `ProjectionType: ALL` GSIs.
- Fixing scans that should be queries via GSI.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| DynamoDB transactions / TransactWrite | `dynamodb-transactions` |
| Generic data modeling theory only | broader DynamoDB design guides |
| RDS/SQL indexes | SQL performance skills |
| Caching | `caching-strategies` |
| Code quality baseline | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| GSI | Alternate partition (and optional sort) key; eventually consistent by default |
| Projection | Which attributes copied to index: `KEYS_ONLY`, `INCLUDE`, `ALL` |
| Sparse GSI | Only items with the index key attribute present appear |
| Fan-out | Each item write may write to each GSI → WCU cost |
| Hot key | Uneven partition key traffic |

**Rule:** Model **access patterns first**, then keys—not attributes first.

## Workflow

### 1. Confirm scope and success criteria

1. List access patterns: “Get X by Y”, “List Z for user sorted by time”.
2. Success: all patterns are Query (not Scan); cost model accepted; no hot partitions by design.
3. Latency/consistency needs (GSI eventual).

### 2. Inventory table and patterns

```bash
# AWS CLI owned account
aws dynamodb describe-table --table-name MyTable --query 'Table.[KeySchema,GlobalSecondaryIndexes]'
```

1. Current GSIs, projections, and provisioned/on-demand mode.
2. Metrics: throttles, scanned vs returned items.

### 3. Choose index keys

| Pattern | Index idea |
| --- | --- |
| By status + time | GSI PK=`status`, SK=`createdAt` |
| By email unique | GSI PK=`email` (careful uniqueness is app-level) |
| Tenant isolation | PK includes `tenantId#...` |
| Sparse “open jobs” | Attribute `openJobId` only when open |

1. High-cardinality partition keys; avoid single status value as only PK without sharding if huge.
2. Sort keys for ranges (`begins_with`, between).

### 4. Projection strategy

| Projection | Pros | Cons |
| --- | --- | --- |
| KEYS_ONLY | Cheapest storage/write | Need GetItem for attrs |
| INCLUDE | Balance | Must list attrs; evolve carefully |
| ALL | Query returns full item | Highest write cost/storage |

1. Prefer KEYS_ONLY/INCLUDE unless every query needs full item and cost OK.
2. Changing projections often requires new GSI.

### 5. Cost and throttling

1. Writes: item size on **each** index projection counts toward WCUs.
2. On-demand still bills usage—bad GSI multiplies cost.
3. Backfill when adding GSI consumes capacity—schedule.
4. Watch `ThrottledRequests` on index.

### 6. Application patterns

```python
# boto3 sketch — Query GSI
resp = table.query(
    IndexName="gsi_status_created",
    KeyConditionExpression=Key("status").eq("OPEN") & Key("createdAt").between(a, b),
    ScanIndexForward=False,
    Limit=50,
)
```

1. Never Scan if Query possible.
2. Paginate with `ExclusiveStartKey`.
3. Sparse index: remove attribute to delete from GSI.

### 7. Verify and hand off

1. Load test access patterns; confirm no hot partition (CloudWatch `SuccessfulRequestLatency`, partition metrics tools).
2. Document each GSI → access pattern mapping.
3. IAM: least privilege on indexes.
4. Apply `code-quality-standards` to data access layer.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Design | Access patterns → keys | GSI per column “just in case” |
| Projection | KEYS_ONLY + Get | ALL on huge items by default |
| PK | High cardinality | One hot status partition |
| Read | Query + page | Table Scan in API |
| Sparse | Optional attrs | Index every item needlessly |
| Change | New GSI planned | Assume free alter |

## Output Checklist

- [ ] Access patterns listed and mapped
- [ ] GSI keys chosen with cardinality in mind
- [ ] Projection type justified
- [ ] Sparse indexes used where fit
- [ ] Write amplification cost estimated
- [ ] Queries implemented (no unjustified scans)
- [ ] Pagination correct
- [ ] Metrics/throttles reviewed
- [ ] IAM least privilege
- [ ] Docs for future patterns

## Rules

- GSIs cost write amplification—design deliberately.
- Eventual consistency on GSI unless using specific newer features—know your API.
- Prefer Query over Scan.
- Owned AWS accounts only.
- Transactions neighbor skill for multi-item atomicity.
