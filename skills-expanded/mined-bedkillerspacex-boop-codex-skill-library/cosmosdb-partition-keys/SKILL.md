---
name: cosmosdb-partition-keys
description: >
  Design and review Azure Cosmos DB partition keys for owned accounts: choose
  high-cardinality keys, avoid hot partitions, plan cross-partition queries,
  hierarchical partition keys, and RU cost. Use when modeling containers,
  fixing 429 hotspots, or migrating partition strategies on Azure subscriptions
  you control.
---

# Cosmos DB Partition Keys

## Scope And Authorization

- **In scope:** Cosmos DB accounts, databases, and containers in Azure subscriptions you own or administer.
- **Out of scope:** Accessing or load-testing third-party Cosmos accounts without authorization.
- Prefer non-prod for synthetic load and partition key experiments; production changes need change windows (partition key is immutable per container).
- Redact connection strings, keys, and AAD tokens from notes.
- Pair application code changes with `code-quality-standards`.

## When To Use

- Designing a new container’s partition key path(s).
- Diagnosing hot partitions, high 429s, or skewed RU consumption.
- Planning hierarchical partition keys (HPK) vs single key.
- Reviewing cross-partition query costs and fan-out.
- Estimating whether synthetic keys or tenantId+entityId composites are needed.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General Azure identity / RBAC | Azure managed identity / IAM skills |
| SQL relational indexing | database skills for SQL Server/Postgres |
| Global distribution / multi-region failover only | Cosmos multi-region runbooks |
| App-tier retry/backoff | `retry-backoff-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Partitioning essentials

| Concept | Guidance |
| --- | --- |
| Partition key | Immutable logical partition routing value (or HPK hierarchy) |
| Logical partition | All items sharing same PK value; practical size limits apply |
| Physical partitions | Managed by Cosmos; split as data/RU grow |
| Hot partition | One PK absorbs disproportionate RU or traffic |
| Cross-partition query | Fans out; higher RU and latency |
| Lookup by id | Efficient only with **id + partition key** |

Good PK properties: high cardinality, even access distribution, aligns with most common query filters, stable (not frequently changing attributes).

## Workflow

### 1. Confirm scope and success criteria

1. Record account, consistency level, multi-region, and workload (OLTP read/write ratios).
2. Success metrics: p99 latency, 429 rate, RU/s per physical partition balance, major queries are single-partition.
3. Inventory top access patterns (by frequency and criticality).

### 2. Inventory current model

```bash
# Azure CLI examples (owned subscription)
az cosmosdb show -g RG -n ACCOUNT -o table
az cosmosdb sql container show -g RG -n ACCOUNT -d DB -c CONTAINER \
  --query "{pk:resource.partitionKey, indexing:resource.indexingPolicy}" -o json
```

From app/SDK: note `PartitionKey` usage on point reads vs queries without PK.

### 3. Map access patterns to candidate keys

| Pattern | Candidate PK ideas | Avoid |
| --- | --- | --- |
| Multi-tenant SaaS | `/tenantId` or `/tenantId`+`/userId` HPK | Single `"shared"` value |
| IoT per device | `/deviceId` | `/status` (few values) |
| User profile | `/userId` | `/country` alone |
| Time-series append | `/deviceId` or `/deviceId`+time bucket (design carefully) | PK = day for all devices (hot day) |
| Global catalog small | Consider single partition if tiny + known limits | Giant cross-partition scans as default |

Write a table: query → filter fields → expected QPS → single-partition? Y/N.

### 4. Design rules of thumb

1. Prefer filtering **equality on PK** for hot paths.
2. Avoid low-cardinality keys (`boolean`, small enums) as sole PK.
3. Avoid monotonically increasing PK that concentrates writes (unless intentional with careful design).
4. Item size × count per logical partition must stay within service limits; plan for growth.
5. Hierarchical partition keys: use when you need finer fan-out while still querying at a parent prefix (e.g. tenant then user).
6. **Changing PK requires new container + data migration** — design for the long term.

### 5. Application patterns

```csharp
// Point read: id + partition key
var response = await container.ReadItemAsync<Order>(
    id: orderId,
    partitionKey: new PartitionKey(tenantId));

// Query within one partition
var q = new QueryDefinition(
    "SELECT * FROM c WHERE c.tenantId = @t AND c.status = @s")
    .WithParameter("@t", tenantId)
    .WithParameter("@s", "Open");
// Ensure SDK request options set PartitionKey when possible
```

```python
# python SDK sketch
container.read_item(item=order_id, partition_key=tenant_id)
```

### 6. Verify distribution and cost

```bash
# Portal/Metrics: Normalized RU Consumption, throttled requests by partition
# Diagnostic logs: partition key ranges under load
```

Load test in non-prod:

1. Synthetic traffic matching production key distribution (not uniform if real traffic is skewed).
2. Watch per-partition RU; identify top PK values.
3. Measure RU for representative cross-partition queries; add composite indexes if needed.

### 7. Migration if redesign required

1. Create new container with new PK/HPK.
2. Bulk move (bulk executor / Spark / change feed) with dual-write or blue-green cutover.
3. Validate item counts and checksum samples.
4. Switch reads; decommission old container after soak.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| PK choice | tenantId+high-card entity | `type = "order"` for all orders |
| Reads | ReadItem with PK | Query all partitions for one id |
| Growth | Plan logical partition size | Unbounded list under one user PK without paging design |
| Hot keys | Split popular tenants with synthetic suffix | Ignore 429 on one PK range |
| Change | New container + migration | Expect in-place PK alter |

## Output Checklist

- [ ] Workload and top queries documented
- [ ] Candidate PK/HPK evaluated for cardinality and evenness
- [ ] Hot-path operations are single-partition
- [ ] Logical partition size growth estimated
- [ ] Cross-partition queries justified and indexed
- [ ] Metrics/429 review done (existing) or load test planned (new)
- [ ] SDK samples use PK on point ops
- [ ] Migration plan if changing PK
- [ ] Secrets redacted; RBAC preferred over account keys in apps
- [ ] Residual skew risks accepted or mitigated

## Rules

- Treat partition key as a one-way door per container.
- Prefer identity (AAD/managed identity) over account keys in applications.
- Authorized Azure scopes only.
- Focus on **partition key design and hot-partition operations**; not general Azure governance.
