---
name: clickhouse-access-control
description: >
  Harden ClickHouse access: SQL users/roles, grants, row policies, quotas, settings
  profiles, network restrictions, and query log privacy. Use on owned ClickHouse
  clusters (self-hosted or cloud) when implementing least privilege or auditing
  default open access — not for attacking exposed CH instances without authorization.
---

# ClickHouse Access Control

## Scope And Authorization

- **In scope:** ClickHouse deployments you own or are authorized to administer.
- **Out of scope:** credential stuffing against third-party CH; exfiltrating data outside engagement scope.
- Prefer changes on staging replica/cluster first; avoid locking out the only admin.
- Redact passwords, cloud access keys, and query snippets with PII from tickets.
- Pair SQL/config with `code-quality-standards` and `secrets-management-hygiene`.

## When To Use

- Replacing default/`default` empty password or shared superuser.
- Introducing **RBAC**: roles, grants, row-level security, quotas.
- Restricting network listen / `users.xml` host patterns / cloud IP allowlists.
- Reducing sensitive data in `system.query_log`.
- Tokens: ClickHouse, RBAC, GRANT, ROW POLICY, QUOTA, settings profile, users.xml.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Dictionaries / external sources | `clickhouse-dictionaries` |
| Materialized view ops | `clickhouse-materialized-views-ops` |
| ReplicatedMergeTree replication | `clickhouse-replicated-merge-tree` |
| Generic secrets program | `secrets-management-hygiene` |
| App SQL injection into CH | `sqli-sql-injection` |

## Access Control Surface

| Layer | Controls |
| --- | --- |
| Network | Bind address, reverse proxy TLS, IP allowlists, private link |
| Authn | Password, LDAP, Kerberos, SSL certs (per deployment) |
| Authz | Databases/tables/columns grants; `GRANT`/`REVOKE` |
| Row policy | `CREATE ROW POLICY` filters per user/role |
| Quota | Queries, errors, result rows, execution time, read bytes |
| Settings profile | readonly, max_memory, allow_ddl |
| Audit | query_log, session_log, access management SQL |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster topology, version (`SELECT version()`), admin break-glass user, change window.
2. Success: least-privilege roles work for apps/analysts; unauthorized access denied; admin recovery documented.
3. Never apply broad REVOKE without a second admin session open.

### 2. Inventory current access

```sql
SELECT version();
SHOW USERS;
SHOW ROLES;
SHOW SETTINGS PROFILES;
SHOW QUOTAS;
SHOW ROW POLICIES;
SELECT * FROM system.grants LIMIT 100;
SELECT * FROM system.role_grants;
```

Also review `users.xml` / config.d and cloud IAM integration if used.

### 3. Baseline risks

1. Empty or weak passwords; users with `GRANT ALL ON *.*`.
2. `0.0.0.0` listen without network policy.
3. Apps using superuser for SELECT-only workloads.
4. query_log retaining full query text with secrets/PII.

### 4. Apply least privilege

**Roles and users (SQL-driven access control):**

```sql
CREATE ROLE IF NOT EXISTS analyst_ro;
GRANT SELECT ON analytics.* TO analyst_ro;

CREATE ROLE IF NOT EXISTS ingest_rw;
GRANT INSERT ON analytics.events TO ingest_rw;
-- avoid broad CREATE/DROP for app roles

CREATE USER IF NOT EXISTS app_ingest
  IDENTIFIED WITH sha256_password BY 'REDACTED_USE_VAULT'
  HOST IP '10.0.0.0/8'
  DEFAULT ROLE ingest_rw;

CREATE USER IF NOT EXISTS human_analyst
  IDENTIFIED WITH sha256_password BY 'REDACTED'
  HOST ANY
  DEFAULT ROLE analyst_ro;

CREATE SETTINGS PROFILE IF NOT EXISTS ro_safe SETTINGS readonly = 1, max_execution_time = 60;
ALTER USER human_analyst SETTINGS PROFILE ro_safe;

CREATE QUOTA IF NOT EXISTS analyst_quota
  KEYED BY user_name
  FOR INTERVAL 1 hour MAX queries = 1000, result_rows = 100000000
  TO analyst_ro;
```

**Row policy example:**

```sql
CREATE ROW POLICY IF NOT EXISTS tenant_isolation ON analytics.events
  FOR SELECT USING tenant_id = currentUser()  -- or map via dict / session setting
  TO analyst_ro;
-- Prefer explicit session settings / mapped attributes over abusing currentUser() if tenants ≠ users
```

**Network / config notes:**

1. Disable anonymous access; force auth on native and HTTP interfaces.
2. Separate interfaces for public HTTP query if required; prefer private network.
3. Store passwords in vault; rotate with dual-control.

### 5. Verify with evidence

```sql
-- as app_ingest
SHOW GRANTS;
SELECT * FROM analytics.events LIMIT 1;   -- expect OK if granted
DROP TABLE analytics.events;              -- expect DENIED

-- as human_analyst
INSERT INTO analytics.events VALUES (...); -- expect DENIED
```

```bash
# From unauthorized IP: connection refused / auth fail
clickhouse-client -h ch.example --user app_ingest --password ...
```

1. Prove deny for DDL/DML outside role.
2. Prove row policy filters rows (two tenants).
3. Confirm quota trips under controlled load.

### 6. Observe and harden

1. Monitor authentication failures and grant changes.
2. Configure query_log retention and scrubbing; avoid logging secrets in SQL literals (use parameters).
3. Quarterly access review: unused users, overprivileged roles.

### 7. Hand off

1. Document role matrix (persona → role → grants).
2. Break-glass admin procedure offline + monitored.
3. Link dictionary/MV/replication skills for non-IAM ops.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| App auth | Dedicated role, host IP limited | Shared `default` superuser |
| Analysts | readonly profile + quota | Unlimited result sets |
| Row security | Policy + tests per tenant | Only app-layer filters |
| Logs | Redaction / short retention | Forever full SQL with PII |
| Changes | Second admin session open | Single session revoke-all |

## Output Checklist

- [ ] Version/topology/admin recovery recorded
- [ ] Users/roles/grants inventory captured
- [ ] Network restrictions reviewed
- [ ] Least-privilege roles applied and tested (allow + deny)
- [ ] Quotas and readonly profiles on human access
- [ ] Row policies tested if multi-tenant
- [ ] query_log privacy reviewed
- [ ] Passwords in vault; no secrets in git
- [ ] Residual overprivileged accounts listed with plan

## Rules

- Authorized clusters only.
- Evidence of GRANT/DENY over assumptions.
- Never leave production with empty default password.
- Focus on ClickHouse **access control**; MV/replication/dictionaries are separate skills.
