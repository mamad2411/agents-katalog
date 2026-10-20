---
name: aws-rds-proxy
description: >
  Amazon RDS Proxy for owned databases: pooling, IAM/Secrets Manager auth, target
  groups, connection borrow timeouts, pin-session behaviors, and failover benefits.
  Use when scaling app connections to RDS/Aurora safely — not for unauthorized
  proxying to databases you do not own.
---

# AWS RDS Proxy

## Scope And Authorization

- **In scope:** RDS Proxy endpoints and target databases in accounts you operate under authorization.
- **Out of scope:** Pointing proxies at third-party databases without permission.
- Proxy holds DB credentials (Secrets Manager) and may use IAM — protect roles tightly.
- Prefer private subnets; security groups least privilege.
- Pair with `aws-rds-iam-auth`, `aws-rds-public-access`, `code-quality-standards`.

## When To Use

- Exhaustion of DB `max_connections` from Lambda/containers.
- Smoother Aurora failover for connection handling.
- Centralizing credentials via Secrets Manager with optional IAM auth to proxy.
- Multiplexing many app connections to fewer DB connections.
- Debugging `Timeout waiting for connection from pool` / pinned sessions.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| IAM DB auth details | `aws-rds-iam-auth` |
| Public access off | `aws-rds-public-access` |
| Aurora Global multi-Region | `aws-aurora-global-db` |
| App pool tuning only | still here + app code standards |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Proxy | Managed pooler in front of RDS/Aurora |
| Target group | Points at instance/cluster |
| Secrets | DB user credentials in Secrets Manager |
| IAM auth | Clients authenticate to proxy with IAM tokens |
| Pinning | Some session features force 1:1 client-DB connection (reduces pooling benefit) |
| Endpoints | Reader vs default endpoints for Aurora |

## When Pooling Helps

| Helps | Less helpful |
| --- | --- |
| Many short-lived clients (Lambda) | Few long-lived already-pooled app servers well-tuned |
| Connection storms | Features forcing pin (temp tables, session vars, advisory locks heavy) |
| Faster failover absorb | Cross-Region (proxy is Regional) |

## Workflow

### 1. Confirm scope and success criteria

1. Record engine, cluster/instance, client types, connection peak, IAM vs password.
2. Success: DB threads/connections stable under load; app errors drop; failover RTO improved; SG private.
3. Identify session features that cause pinning.

### 2. Inventory

```bash
aws rds describe-db-proxies
aws rds describe-db-proxy-targets --db-proxy-name "$PROXY"
aws rds describe-db-proxy-target-group --db-proxy-name "$PROXY" --target-group-name default
aws secretsmanager list-secrets --query "SecretList[?contains(Name, 'db')].Name"
```

1. Current `max_connections` and app pool sizes.
2. Whether clients use TLS.

### 3. Baseline

1. CloudWatch DBConnections peak; Lambda concurrent → estimated connections.
2. Failover last duration if known.
3. Secret ARNs for each DB user the proxy will use.

### 4. Deploy proxy

```bash
aws rds create-db-proxy \
  --db-proxy-name app-proxy \
  --engine-family MYSQL \
  --auth '[{"AuthScheme":"SECRETS","SecretArn":"arn:aws:secretsmanager:...","IAMAuth":"REQUIRED"}]' \
  --role-arn arn:aws:iam::ACCT:role/rds-proxy-role \
  --vpc-subnet-ids subnet-a subnet-b \
  --vpc-security-group-ids sg-proxy \
  --require-tls

aws rds register-db-proxy-targets \
  --db-proxy-name app-proxy \
  --db-cluster-identifiers my-aurora
```

**IAM role for proxy:** read secrets + KMS decrypt + connect to DB network.

**Client config**

1. Host = proxy endpoint (not direct DB) for pooled apps.
2. If IAMAuth REQUIRED: generate RDS auth token against **proxy** endpoint with DB username matching secret/mapped user.
3. TLS required.
4. Tune `MaxConnectionsPercent`, `MaxIdleConnectionsPercent`, `ConnectionBorrowTimeout`.

**Avoid pinning when possible**

1. Reduce session-level state; prefer transaction-scoped work.
2. Monitor `DatabaseConnectionsCurrentlySessionPinned` metric.

### 5. Verify with evidence

```bash
aws rds describe-db-proxies --db-proxy-name app-proxy
# Load test Lambda concurrency; DB Connections should rise sub-linearly vs clients
# Kill writer on Aurora test env; clients recover via proxy
```

1. Unauthorized IAM principal cannot connect.
2. Direct public access still disabled on DB.
3. Secret rotation: proxy picks up new secret versions per AWS behavior — test.

### 6. Observe and harden

1. Alarms: `ClientConnections`, `DatabaseConnections`, borrow timeouts, pinned connections.
2. Capacity: proxy scales — still watch DB limits.
3. Review secrets and proxy role quarterly.

### 7. Hand off

1. Endpoint, auth mode, secret ARNs, SG diagram.
2. App guidance: pool sizes smaller when using proxy.
3. Runbook for failover and secret rotation.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | IAM to proxy + secrets to DB | shared long-lived password in all Lambdas |
| TLS | required | optional |
| Network | private SG chain app→proxy→db | public proxy |
| Pinning | minimize session state | heavy session features ignoring metric |
| Pools | app pool reduced | app pool max + proxy + DB max all huge |
| Targets | Aurora cluster targets | wrong instance after topology change |

## Output Checklist

- [ ] Engine/targets/clients recorded
- [ ] Proxy created with TLS and private subnets
- [ ] Secrets + proxy role least privilege
- [ ] IAM auth mode decided and tested
- [ ] Borrow/pool settings tuned
- [ ] Load and failover evidence captured
- [ ] Pinning metrics reviewed
- [ ] Alarms configured
- [ ] App connection strings updated
- [ ] `aws-rds-iam-auth` / public access checked

## Rules

- Owned DBs only.
- Keep proxy and DB private; require TLS.
- Design for pinning and rotation.
- Do not treat proxy as substitute for least-privilege SQL users.
- Focus on RDS Proxy; deep IAM token and public access skills complement this.
