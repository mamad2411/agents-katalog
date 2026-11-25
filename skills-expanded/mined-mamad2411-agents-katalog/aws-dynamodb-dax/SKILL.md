---
name: aws-dynamodb-dax
description: >
  Amazon DynamoDB Accelerator (DAX) for owned accounts: cluster VPC design, IAM,
  consistency caveats (eventual cache), encryption, parameter groups, and when not
  to use DAX. Use when adding or reviewing microsecond caching in front of DynamoDB —
  not for unauthorized access to others’ DAX clusters.
---

# AWS DynamoDB DAX

## Scope And Authorization

- **In scope:** DAX clusters and DynamoDB tables in AWS accounts you own or operate with authorization.
- **Out of scope:** Connecting to third-party DAX endpoints; data exfiltration.
- DAX is an in-memory cache — treat node security groups and IAM as sensitive as the data classification of cached items.
- Prefer private subnets only; no public DAX.
- Pair app client changes with `code-quality-standards`.

## When To Use

- Read-heavy workloads needing microsecond latency beyond DynamoDB eventually consistent reads.
- Evaluating DAX vs application cache (Redis/ElastiCache) vs DynamoDB DAX specifics.
- Configuring IAM policies for DAX access (`dax:*` vs DynamoDB API).
- Understanding strongly consistent reads and write-through behavior.
- Troubleshooting cache stampede, stale reads, or cluster failover.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| DynamoDB table design/keys | DynamoDB modeling skill |
| ElastiCache Serverless | `aws-elasticache-serverless` |
| General IAM least privilege | `aws-iam-least-privilege` |
| App concurrency patterns | `async-concurrency-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Guidance |
| --- | --- |
| API compatibility | DAX supports subset of DynamoDB API (GetItem, BatchGetItem, Query, Scan, writes write-through) |
| Consistency | Cached reads may be stale; strongly consistent reads may bypass or special-case — verify current client behavior |
| Auth | Cluster IAM + VPC; clients use DAX client library not plain HTTP DynamoDB endpoint |
| Encryption | At-rest encryption options; in-transit TLS for clients |
| Scaling | Node types/counts; multi-AZ replicas for HA |

## When DAX Helps / Hurts

| Helps | Hurts / avoid |
| --- | --- |
| Hot key reads | Rarely read tables (extra cost/complexity) |
| Microsecond cache hits | Need always strongly consistent reads for every request |
| Same-VPC microservices | Cross-Region reads (DAX is Regional) |
| DynamoDB-specific API reuse | Generic Redis data structures needed |

## Workflow

### 1. Confirm scope and success criteria

1. Record table(s), Region, RCU patterns, item sensitivity, client languages.
2. Success: p99 read latency improved; error rate stable; SG/IAM least privilege; failover test OK.
3. Define freshness SLO (max acceptable staleness).

### 2. Inventory

```bash
aws dax describe-clusters
aws dax describe-parameters --parameter-group-name default.dax.1
aws dynamodb describe-table --table-name "$TABLE"
```

1. Note subnet group, SG, IAM roles used by app.
2. Measure current DynamoDB consumed read capacity and latency.

### 3. Baseline

1. Capture p50/p99 GetItem/Query latency without DAX.
2. Document items that must never be stale (balances, locks) — may bypass DAX.
3. Confirm client SDK supports DAX for your language version.

### 4. Deploy and integrate

**Cluster (conceptual):**

```bash
aws dax create-cluster \
  --cluster-name app-dax \
  --node-type dax.r5.large \
  --replication-factor 3 \
  --iam-role-arn arn:aws:iam::ACCT:role/DAXServiceRole \
  --subnet-group-name dax-subnets \
  --security-group-ids sg-... \
  --sse-specification Enabled=true
```

**Security**

1. SG: ingress only from app SGs on DAX port (9111 TLS / 8111 plaintext — prefer TLS).
2. IAM: app role needs DAX API permissions; cluster role needs DynamoDB access to target tables only.
3. Avoid `dynamodb:*` on all resources for cluster role.

**Application**

1. Use DAX client endpoint cluster discovery URL.
2. Route only eligible operations through DAX; dual-path for strong consistency needs.
3. Writes go through DAX write-through so cache updates — understand failure modes.
4. Timeouts/retries: tune for cluster maintenance events.

### 5. Verify with evidence

```bash
aws dax describe-clusters --cluster-names app-dax
# App integration tests: read path hits DAX; item update visible per freshness expectations
# Chaos: reboot node → client recovers via cluster endpoints
```

1. Load test hot keys; watch DAX CloudWatch `ItemCacheHits` / `Misses` / `CPU`.
2. Confirm no public network exposure (`aws ec2 describe-network-interfaces` for cluster).
3. Authz: role without DAX perms fails closed.

### 6. Observe and harden

1. Alarms: CPU, cache memory, error counts, eviction rates.
2. Patch/maintenance windows understood; multi-node for HA.
3. Periodic review: is DAX still needed vs DynamoDB performance improvements?

### 7. Hand off

1. Document which APIs/tables use DAX; bypass list for strong consistency.
2. Runbook for scale-out and client endpoint changes.
3. Cost comparison dashboard vs provisioned RCU alone.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Network | private subnets + tight SG | open 0.0.0.0/0 to DAX |
| IAM | table-scoped DynamoDB for cluster role | `*` on DynamoDB |
| Consistency | explicit bypass for critical reads | assume cache always fresh |
| Client | supported DAX SDK | generic HTTP to DAX port |
| HA | multi-node AZ spread | single node prod |
| Scope | hot-key read heavy | caching everything by default |

## Output Checklist

- [ ] Tables, Region, freshness SLO recorded
- [ ] Decision: DAX vs alternatives documented
- [ ] Cluster encryption, subnets, SG hardened
- [ ] IAM least privilege for app + cluster roles
- [ ] Client integration and bypass paths tested
- [ ] Latency/hit-rate evidence from load test
- [ ] Alarms configured
- [ ] Ops runbook handed off
- [ ] `code-quality-standards` applied to client code

## Rules

- Owned clusters only; DAX holds sensitive cached data.
- Prefer TLS and private networking.
- Do not ignore consistency requirements when introducing cache.
- Scope IAM to required tables/operations.
- Focus on DAX caveats; DynamoDB data modeling and Redis elsewhere.
