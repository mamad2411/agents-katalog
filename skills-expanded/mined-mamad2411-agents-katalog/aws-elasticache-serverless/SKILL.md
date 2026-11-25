---
name: aws-elasticache-serverless
description: >
  Amazon ElastiCache Serverless (Redis/Memcached-compatible) for owned accounts:
  VPC endpoints, encryption, IAM/RBAC auth, network exposure, sizing/ECUs, and app
  connection patterns. Use when deploying or reviewing serverless caches — not for
  unauthorized access to third-party cache endpoints.
---

# AWS ElastiCache Serverless

## Scope And Authorization

- **In scope:** ElastiCache Serverless caches in AWS accounts you own or operate under authorization.
- **Out of scope:** Connecting to or flushing caches outside authorization.
- Caches often hold sessions and PII-derived data — encrypt and isolate network paths.
- Prefer private VPC access only; never open to 0.0.0.0/0.
- Pair app client code with `code-quality-standards` and `caching-strategies`.

## When To Use

- Choosing ElastiCache Serverless vs node-based replication groups.
- Enabling transit/at-rest encryption and AUTH/IAM authentication.
- Configuring subnets, security groups, and user groups (Redis ACL).
- Planning capacity (ECPU/storage) and cost alarms.
- Migrating clients to TLS endpoints and new auth flows.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| DynamoDB DAX | `aws-dynamodb-dax` |
| Application cache pattern design | `caching-strategies` |
| Redis security misconfig generically | `redis-security-misconfig` |
| Secrets rotation for app passwords | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Guidance |
| --- | --- |
| Engine | Redis OSS-compatible / Valkey / Memcached options per current AWS offering |
| Auth | Redis AUTH token, RBAC users, or IAM auth where supported |
| Encryption | Transit TLS + at-rest |
| Network | VPC, SG, private subnets; no public access |
| Ops | Serverless scaling; still monitor throttling and connections |

## Serverless vs Node-based

| Prefer serverless when | Prefer node-based when |
| --- | --- |
| Variable traffic, less capacity planning | Fine-grained node type control / specific features |
| Faster provisioning | Reserved instance cost patterns, advanced configs |
| Simpler HA story from service | Need specific cluster-mode topology control |

Validate feature parity (modules, version commands, limits) before migration.

## Workflow

### 1. Confirm scope and success criteria

1. Record engine, Region, data class, client languages, multi-AZ needs.
2. Success: TLS required; auth required; SG only from app; encryption on; chaos reconnect works.
3. Define max memory/data eviction expectations.

### 2. Inventory

```bash
aws elasticache describe-serverless-caches
aws elasticache describe-users
aws elasticache describe-user-groups
aws ec2 describe-security-groups --group-ids sg-cache
```

1. List existing node-based clusters that might be consolidated.
2. Note whether AUTH tokens live in Secrets Manager.

### 3. Baseline

1. Capture hit rate, latency, connection counts from current cache if migrating.
2. Document key naming and TTL policies (`caching-strategies`).
3. Export current SG and subnet groups.

### 4. Deploy hardened serverless cache

```bash
aws elasticache create-serverless-cache \
  --serverless-cache-name app-redis \
  --engine redis \
  --major-engine-version "7" \
  --security-group-ids sg-cache \
  --subnet-ids subnet-a subnet-b \
  --snapshot-retention-limit 7 \
  --daily-snapshot-time "03:00"
# Enable encryption/auth per CLI/API parameters available for your engine version
```

**Security controls**

1. SG ingress: app SG only on Redis port (6379) / Memcached (11211).
2. Transit encryption: clients use `rediss://` and proper TLS.
3. AUTH/RBAC: least-privilege users (no `FLUSHALL` for app users).
4. Store tokens in Secrets Manager; rotate with dual-user strategies when possible.
5. Disable dangerous commands via user ACL (~@all -@dangerous or explicit allowlists).

**Application**

1. Connection pool sizes bounded; timeouts set.
2. Handle MOVE/ASK/reconnects; serverless endpoints may differ from classic config endpoints — use documented endpoint.
3. Do not cache security decisions without TTL and invalidation plan.

### 5. Verify with evidence

```bash
aws elasticache describe-serverless-caches --serverless-cache-name app-redis
# From bastion/app: TLS connect with auth succeeds; without auth fails
# redis-cli --tls -h $ENDPOINT -p 6379 -a $TOKEN PING
```

1. Port from Internet: should not connect.
2. Wrong password/user denied.
3. Load test for throttling (ECPU) and set alarms.

### 6. Observe and harden

1. CloudWatch: ECPU, bytes, connections, throttles, auth errors.
2. Alert on SG changes and auth failures spikes.
3. Periodic ACL review; remove unused users.

### 7. Hand off

1. Endpoint, auth method, secret ARN, SG diagram.
2. Runbook for rotation and client config.
3. Cost budget alarms.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Network | private + app SG | 0.0.0.0/0 open |
| Auth | RBAC/IAM + secrets manager | no AUTH on prod |
| TLS | required | plaintext redis:// |
| ACL | app user without flush/admin | default user full access |
| Clients | pools + timeouts | unbounded connections |
| Data | TTLs for sessions | eternal PII keys |

## Output Checklist

- [ ] Engine/Region/data class recorded
- [ ] Serverless vs node decision documented
- [ ] Encryption + auth enabled
- [ ] SG/subnet isolation verified
- [ ] Secrets storage and rotation path set
- [ ] Client TLS/auth evidence captured
- [ ] Throttle/connection alarms set
- [ ] ACL least privilege reviewed
- [ ] `code-quality-standards` / caching strategy applied

## Rules

- Owned caches only; treat contents as sensitive.
- Always encrypt in transit for production.
- Never expose cache ports publicly.
- App users must not have admin/destructive commands.
- Focus on ElastiCache Serverless; DAX and generic Redis host hardening in neighbors.
