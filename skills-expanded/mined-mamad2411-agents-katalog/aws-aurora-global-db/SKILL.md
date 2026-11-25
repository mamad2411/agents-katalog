---
name: aws-aurora-global-db
description: >
  Amazon Aurora Global Database for owned AWS accounts: primary/secondary clusters,
  managed RPO/RTO, write forwarding, headless secondaries, failover/switchover, and
  cross-Region networking/IAM considerations. Use when designing or operating multi-Region
  Aurora — not for unauthorized access to databases you do not own.
---

# AWS Aurora Global Database

## Scope And Authorization

- **In scope:** Aurora clusters (MySQL/PostgreSQL-compatible) in accounts you own or operate under authorization.
- **Out of scope:** Connecting to or failing over third-party databases without authority.
- Global failover changes write Region — require change control and application readiness.
- Protect master credentials via Secrets Manager; prefer IAM DB auth where applicable (`aws-rds-iam-auth`).
- Pair parameter/IaC changes with `code-quality-standards`.

## When To Use

- Multi-Region read scaling and DR for Aurora.
- Planning planned switchover vs unplanned failover.
- Enabling write forwarding (MySQL) patterns carefully.
- Monitoring replication lag (AuroraGlobalDBReplicationLag).
- Removing secondary or promoting clusters during region exit.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Single-Region Aurora/RDS hardening | RDS public access / proxy skills |
| RDS Proxy connection pooling | `aws-rds-proxy` |
| IAM DB authentication | `aws-rds-iam-auth` |
| App retry/backoff | `retry-backoff-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Global database | One primary cluster (writer) + up to multiple secondary Regions |
| Storage replication | Aurora storage-based, typically sub-second lag target (workload dependent) |
| Secondary cluster | Reader endpoints; optional promotion |
| Write forwarding | Secondary can forward writes to primary (MySQL feature set; verify engine) |
| Switchover | Planned, managed role reverse with sync |
| Failover | Promote secondary when primary Region impaired |

## Topology Sketch

```text
Region A (primary): writer + readers  ──storage replication──► Region B secondary readers
                                         └──────────────────► Region C secondary readers
App: write → primary endpoint; read → local reader or custom endpoint
```

## Workflow

### 1. Confirm scope and success criteria

1. Record engine (MySQL/PostgreSQL), versions, Regions, RPO/RTO objectives, app multi-Region readiness.
2. Success: secondary lag within SLO; readers serve local traffic; failover runbook tested in DR drill; secrets/endpoints updated automatically (Route53/app config).
3. Note cross-account if any (usually same account multi-Region).

### 2. Inventory global databases

```bash
aws rds describe-global-clusters
aws rds describe-db-clusters --query "DBClusters[?Engine!=null].[DBClusterIdentifier,Engine,EngineVersion,AvailabilityZones]" --output table
GDB=my-global
aws rds describe-global-clusters --global-cluster-identifier "$GDB"
```

1. Identify primary member vs secondaries.
2. List custom endpoints and app connection strings.
3. Check backup retention and encryption (KMS CMK per Region considerations).

### 3. Baseline

1. Capture CloudWatch: `AuroraGlobalDBReplicationLag`, `CPUUtilization`, commit latency.
2. Document current parameter groups and major versions (secondaries must be compatible).
3. Export connection bootstrap config (writer vs reader hostnames).

### 4. Build or modify global DB

**Add secondary (conceptual CLI):**

```bash
# Primary cluster already exists and is eligible
aws rds create-global-cluster \
  --global-cluster-identifier "$GDB" \
  --source-db-cluster-identifier "arn:aws:rds:us-east-1:ACCT:cluster:primary-cluster"

aws rds create-db-cluster \
  --db-cluster-identifier secondary-eu \
  --engine aurora-postgresql \
  --global-cluster-identifier "$GDB" \
  --region eu-west-1 \
  --engine-version "$VERSION" \
  --kms-key-id "arn:aws:kms:eu-west-1:ACCT:key/..."
# then create instances in secondary cluster
```

**Operational controls**

1. Encryption: plan KMS keys in each Region; replication requires proper key policy grants.
2. Networking: apps in secondary Region use local VPC connectivity; Security Groups least privilege.
3. Parameter groups: keep compatible settings; test `max_connections` and timeouts.
4. Write forwarding (if used): understand latency and conflict semantics; many apps prefer writing only to primary endpoint intentionally.
5. Headless secondary (storage only) patterns for DR cost optimization when supported by your design — validate current AWS guidance.

**Planned switchover**

1. Stop writes / drain app; use managed switchover API when available for engine.
2. Update DNS/config to new writer endpoint.
3. Verify lag zero-ish and app health in new primary Region.

**Unplanned failover**

1. Promote secondary per runbook; accept potential small data loss if primary unrecoverable (understand RPO).
2. Rebuild former primary as new secondary later.
3. Rotate secrets if compromise suspected during incident.

### 5. Verify with evidence

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name AuroraGlobalDBReplicationLag \
  --dimensions Name=DBClusterIdentifier,Value=secondary-eu \
  --start-time "$(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" \
  --end-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --period 60 --statistics Maximum
# Read from secondary reader endpoint; write only to primary
```

1. DR game day: timed failover/switchover with app validation.
2. Confirm automated backups and PITR expectations per cluster.
3. Connectivity from each Region’s app tier only as intended.

### 6. Observe and harden

1. Alarms: lag > threshold, secondary instance failures, storage encryption issues.
2. Block public accessibility on all cluster instances (`aws-rds-public-access`).
3. Regular version upgrade plan across all members.

### 7. Hand off

1. Runbook: endpoints, promotion steps, DNS, owner contacts, RPO/RTO.
2. App guidance: never guess writer Region; use config/service discovery.
3. Cost review: secondaries are full clusters — right-size readers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Writes | primary writer endpoint | apps writing to random readers |
| DR | tested switchover/failover | untested “we have a secondary” |
| Lag | alarms + SLO | ignore lag until users complain |
| Keys | per-Region CMK policies correct | broken key policy blocks secondary |
| Public | private subnets only | public + weak SG |
| Versions | coordinated upgrades | mixed incompatible members |

## Output Checklist

- [ ] Engine, versions, Regions, RPO/RTO recorded
- [ ] Global cluster members inventoried
- [ ] Encryption/KMS and networking validated
- [ ] App write/read endpoint strategy documented
- [ ] Lag metrics and alarms configured
- [ ] Switchover/failover drill evidenced
- [ ] Public access disabled; SG least privilege
- [ ] Secrets/IAM auth approach documented
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Owned databases only; failover is a production event.
- Test DR — topology alone is not resilience.
- Keep secondaries encrypted and private.
- Align application retries with `retry-backoff-patterns`.
- Focus on Global Database operations; proxy/IAM auth/public access in neighbor skills.
