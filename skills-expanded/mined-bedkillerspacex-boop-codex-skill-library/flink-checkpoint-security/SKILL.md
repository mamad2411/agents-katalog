---
name: flink-checkpoint-security
description: >
  Secure Apache Flink checkpoint storage and access: filesystem/object-store permissions,
  encryption, retention, state backend choices (RocksDB/heap), and prevention of checkpoint
  tampering or data leakage. Use when hardening owned Flink clusters and jobs that persist
  state containing sensitive stream data.
---

# Flink Checkpoint Security

## Scope And Authorization

- **In scope:** Flink clusters, state backends, and checkpoint directories/buckets you operate.
- **Out of scope:** reading other tenants’ checkpoints or attacking shared cloud accounts without auth.
- Checkpoints may contain **plaintext stream state** (PII, tokens)—treat as sensitive data stores.
- Redact paths that embed customer ids if required; never paste secrets from state dumps.
- Pair config changes with `code-quality-standards`.

## When To Use

- Configuring `state.checkpoints.dir`, `state.savepoints.dir`, and high-availability storage.
- Reviewing who can read/write checkpoint object prefixes.
- Enabling encryption-at-rest and tight IAM for Flink TaskManagers/JobManagers.
- Incidents involving state leakage or unauthorized job restore.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Savepoint upgrade/ops procedures | `flink-savepoints-ops` |
| CDC source connectors | `flink-cdc-connectors` |
| General secrets hygiene | `secrets-management-hygiene` |
| Cloud firewall only | `firewall-rule-review` / `gcp-firewall-rules` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Artifact | Sensitivity |
| --- | --- |
| Checkpoint | Periodic consistent state; often auto-retained |
| Savepoint | Operator-triggered; portable across upgrades |
| HA metadata | Job graph / pointers in DFS/ZooKeeper/K8s |
| RocksDB local dir | Disk of TaskManager—ephemeral but sensitive |

| Control | Guidance |
| --- | --- |
| IAM/ACL | Job identity write; limited read for restore; no public ACL |
| Encryption | Bucket SSE-KMS; consider state encryption features per version |
| Network | Private storage endpoints |
| Retention | Bound history; purge abandoned job dirs |
| Isolation | Per-env and per-tenant prefixes |

## Workflow

### 1. Confirm scope and success criteria

1. Flink version, state backend, checkpoint storage URI, multi-tenancy model.
2. Success: anonymous access denied; cross-job prefix isolation; encryption on; only operators restore.
3. Data classification of typical state contents.

### 2. Inventory configuration

```bash
# Search configs (owned repos/clusters)
rg -n "state.backend|checkpoints.dir|savepoints.dir|high-availability" -g '*.{yaml,yml,properties,conf}'
```

```properties
# Example flink-conf style
state.backend: rocksdb
state.checkpoints.dir: s3://flink-state-prod/checkpoints/
state.savepoints.dir: s3://flink-state-prod/savepoints/
# Ensure credentials via instance role / IRSA / workload identity — not keys in conf files
```

1. List cloud IAM policies on the bucket/prefix.
2. Note local `state.backend.rocksdb.localdir` mount security.

### 3. Baseline access tests (authorized)

```bash
# Anonymous or wrong-role list/get should fail
aws s3 ls s3://flink-state-prod/checkpoints/   # expect AccessDenied without role
```

1. Confirm old job directories not world-readable.
2. Check completed checkpoint side-output logs for secret echoes.

### 4. Apply hardening

1. **Dedicated bucket/prefix** per environment; deny `s3:ListBucket` broadly when possible.
2. TaskManager/JobManager service accounts: `Put/Get/Delete` only on assigned prefix.
3. Enable **default encryption** with KMS; restrict `kms:Decrypt` to Flink roles and break-glass.
4. Disable public access blocks off? Ensure block public access **on**.
5. Separate checkpoint vs savepoint prefixes if ops roles differ.
6. Avoid storing checkpoints on shared NFS with world bits `0777`.
7. Scrub job names/paths that embed secrets; do not put passwords in operator UI free text that lands in state.
8. Consider incremental checkpoints disk growth—retention policies to limit exposure window.

### 5. Verify with evidence

| Check | Evidence |
| --- | --- |
| Public access | Blocked |
| Cross-role read | Denied |
| Job recovery | Succeeds with correct role |
| KMS | Encryption config shown on objects |

```bash
# After deploy: successful checkpoint in UI; storage objects encrypted
```

### 6. Observe and harden

1. Metrics: checkpoint duration, failure rate, state size (sudden growth may leak data volume).
2. Alert on IAM policy changes to state bucket.
3. Periodic cleanup of orphaned checkpoint directories after job teardown.

### 7. Hand off

1. Document URI layout, roles, KMS keys, retention.
2. Link savepoint ops for upgrade procedures.
3. Apply `code-quality-standards` for IaC.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Storage ACL | Private + job role | Public-read “for debug” |
| Secrets | Workload identity | Access keys in flink-conf |
| Paths | Env-separated prefixes | Single open bucket all jobs |
| Encryption | SSE-KMS | None on sensitive state |
| Local disk | Restricted mounts | World-readable RocksDB dirs |
| Retention | Bounded | Infinite checkpoint history |

## Output Checklist

- [ ] Checkpoint/savepoint/HA URIs inventoried
- [ ] IAM/ACL least privilege evidenced
- [ ] Encryption enabled and tested
- [ ] Cross-tenant isolation reviewed
- [ ] Local RocksDB path permissions reviewed
- [ ] Retention/cleanup policy set
- [ ] Monitoring for checkpoint failures and IAM drift
- [ ] `code-quality-standards` applied

## Rules

- Owned clusters only; treat checkpoints as sensitive datastores.
- Recovery convenience must not equal public state.
- Coordinate with `flink-savepoints-ops` for operational restore steps.
- Never commit cloud keys into Flink config maps.
