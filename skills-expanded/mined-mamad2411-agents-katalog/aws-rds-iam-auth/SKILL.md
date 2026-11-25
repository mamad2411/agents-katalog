---
name: aws-rds-iam-auth
description: >
  Amazon RDS/Aurora IAM database authentication for owned databases: enabling IAM
  auth, creating DB users with AWSAuthenticationPlugin / rds_iam, generating auth
  tokens, IAM policies, and TLS requirements. Use when replacing static DB passwords
  for apps — not for unauthorized access to databases you do not own.
---

# AWS RDS IAM Auth

## Scope And Authorization

- **In scope:** RDS/Aurora instances/clusters you operate under authorization.
- **Out of scope:** Generating tokens against third-party databases; password spraying.
- IAM auth tokens are short-lived but powerful — protect signer credentials and require TLS.
- Not all engines/versions support IAM auth equally — verify engine eligibility.
- Pair with `aws-rds-proxy` (proxy supports IAM), `aws-rds-public-access`, `code-quality-standards`.

## When To Use

- Enabling IAM DB authentication on RDS/Aurora.
- Mapping IAM roles/users to database users.
- App integration with auth token generators (SDK `generate_db_auth_token`).
- Reducing long-lived DB passwords for human break-glass (still prefer SSO patterns).
- Debugging `Access denied` / token expiry / missing `rds-db:connect`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Connection pooling | `aws-rds-proxy` |
| Public accessibility hardening | `aws-rds-public-access` |
| Secrets Manager password rotation | `aws-parameter-store-vs-secrets` |
| Aurora Global | `aws-aurora-global-db` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Detail |
| --- | --- |
| Cluster/instance flag | IAM authentication enabled |
| DB user | MySQL: `AWSAuthenticationPlugin`; PostgreSQL: `GRANT rds_iam` |
| IAM action | `rds-db:connect` on `dbuser` ARN |
| Token | ~15 minutes validity; reconnect must refresh |
| TLS | Required for IAM auth connections |

## Resource ARN Form (connect)

```text
arn:aws:rds-db:REGION:ACCOUNT:dbuser:DB_RESOURCE_ID/DB_USER_NAME
```

Get resource ID from `DbiResourceId` / cluster resource id fields.

## Workflow

### 1. Confirm scope and success criteria

1. Record engine, version, resource IDs, app roles, whether Proxy is used.
2. Success: app connects with token only; password auth disabled for that user if desired; TLS enforced; IAM policy scoped to specific dbuser ARN.
3. Fallback break-glass SQL user stored in Secrets Manager.

### 2. Inventory

```bash
aws rds describe-db-instances --query "DBInstances[].{Id:DBInstanceIdentifier,IAM:IAMDatabaseAuthenticationEnabled,Public:PubliclyAccessible}"
aws rds describe-db-clusters --query "DBClusters[].{Id:DBClusterIdentifier,IAM:IAMDatabaseAuthenticationEnabled}"
aws rds describe-db-instances --db-instance-identifier "$ID" --query "DBInstances[].DbiResourceId"
```

1. List app connection methods today (password, proxy, IAM).
2. Confirm SSL/TLS parameter group settings.

### 3. Baseline

1. Capture current DB users and grants (authorized DBA session).
2. Measure connection rate for token refresh design.
3. Export IAM policies that will need `rds-db:connect`.

### 4. Enable and wire users

```bash
aws rds modify-db-instance --db-instance-identifier "$ID" \
  --enable-iam-database-authentication --apply-immediately
# or modify-db-cluster for Aurora
```

**MySQL user sketch:**

```sql
CREATE USER 'app_iam'@'%' IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';
GRANT SELECT, INSERT, UPDATE ON appdb.* TO 'app_iam'@'%';
FLUSH PRIVILEGES;
```

**PostgreSQL sketch:**

```sql
CREATE USER app_iam;
GRANT rds_iam TO app_iam;
GRANT CONNECT ON DATABASE appdb TO app_iam;
-- table grants...
```

**IAM policy:**

```json
{
  "Effect": "Allow",
  "Action": "rds-db:connect",
  "Resource": "arn:aws:rds-db:REGION:ACCT:dbuser:db-XXXXXXXXXXXXXXXXXXX/app_iam"
}
```

**App token (CLI example):**

```bash
TOKEN=$(aws rds generate-db-auth-token \
  --hostname "$HOST" --port 3306 --region "$REGION" --username app_iam)
# Connect with TLS and password=TOKEN
```

1. Use SDK token generator in connection pool on-demand (refresh before expiry).
2. With RDS Proxy: enable IAM on proxy target; clients may auth to proxy with IAM.
3. Do not log tokens.

### 5. Verify with evidence

```bash
# Connect with token succeeds
# Connect with wrong/expired token fails
# Role without rds-db:connect fails
```

1. Confirm `PubliclyAccessible=false` still holds.
2. Rotate away static password for app user if policy requires.
3. Load test: token refresh under pool churn.

### 6. Observe and harden

1. Alert on auth failures spikes.
2. Audit DB users still using native passwords for apps.
3. Scope `rds-db:connect` per function/role, not wildcard all dbusers.

### 7. Hand off

1. Document resource IDs and db user mapping.
2. Sample connection code for each language used.
3. Break-glass password user procedure.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tokens | short-lived, refreshed | cached 24h illegally |
| IAM | specific dbuser ARN | `dbuser:*/*` |
| TLS | required | plaintext |
| Users | least SQL grants | SUPER/admin IAM user |
| Logs | no tokens | print auth token |
| Network | private SG | public + IAM “enough” |

## Output Checklist

- [ ] Engine support and resource IDs recorded
- [ ] IAM auth enabled on instance/cluster
- [ ] DB users created with IAM plugin/role
- [ ] IAM `rds-db:connect` scoped
- [ ] TLS enforced client-side and server
- [ ] Token refresh logic verified
- [ ] Deny tests for wrong roles/users
- [ ] Break-glass documented
- [ ] Proxy interaction clarified if used
- [ ] `code-quality-standards` on client code

## Rules

- Owned databases only.
- Always use TLS with IAM auth.
- Scope connect ARNs tightly; least SQL privileges.
- Never log authentication tokens.
- Focus on IAM DB auth; proxy and public access in companion skills.
