---
name: gcp-cloud-sql-iam-auth
description: >
  Connect applications to Cloud SQL using IAM database authentication and the Cloud SQL
  Auth Proxy / connectors: instance IAM, DB users, token refresh, private IP, and secret
  elimination. Use when hardening owned GCP apps to drop long-lived DB passwords where
  IAM auth is supported.
---

# GCP Cloud SQL IAM Auth

## Scope And Authorization

- **In scope:** Cloud SQL instances and apps in projects you own.
- **Out of scope:** attacking or connecting to unauthorized instances.
- Prefer private IP + proxy; restrict public IP.
- Redact connection names and tokens from logs.
- Pair with `secrets-management-hygiene` and `code-quality-standards`.

## When To Use

- Replacing static MySQL/Postgres passwords with **IAM DB users**.
- Running **Cloud SQL Auth Proxy** or language connectors with ADC.
- GKE/Cloud Run/GCE workloads needing short-lived DB credentials.
- Auditing lingering password users.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cloud Run Jobs batch | `gcp-cloud-run-jobs` |
| VPC firewall rules | `gcp-firewall-rules` |
| General secrets program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Instance flag | IAM authentication enabled |
| IAM policy | `cloudsql.instanceUser` / client roles as required |
| DB user | IAM user type matching SA email / Google user |
| Auth Proxy / Connector | Exchanges ADC for ephemeral DB auth |
| Private path | Private IP + VPC; optional PSC patterns |

## Workflow

### 1. Confirm scope and success criteria

1. Engine (Postgres/MySQL), instance connection name, consumers (Run/GKE/GCE).
2. Success: app connects without password secret; password users removed or minimized; public IP optional off; SSL/proxy enforced.
3. Break-glass SQL user with stored secret in vault only if required.

### 2. Inventory

```bash
gcloud sql instances describe INSTANCE --project=PROJECT
gcloud sql users list --instance=INSTANCE
# App configs for DATABASE_URL passwords
rg -n "DATABASE_URL|CLOUDSQL|5432|3306" -g '*.{env,yml,yaml,tf,py,go}'
```

1. Note existing password users and who knows them.
2. Network: public IP? authorized networks?

### 3. Enable IAM auth and create users

```bash
# Enable IAM authentication (engine-specific flags — verify docs)
# gcloud sql instances patch INSTANCE --database-flags=cloudsql.iam_authentication=on

# Create IAM service account user (Postgres example pattern)
# gcloud sql users create SA_EMAIL --instance=INSTANCE --type=cloud_iam_service_account
```

1. Grant GCP IAM roles for client: e.g. `roles/cloudsql.client` plus instance user binding as required.
2. Map each app runtime SA to a DB IAM user.
3. Least privilege grants inside DB (`GRANT SELECT...`).

### 4. Connect via proxy/connector

```bash
# Local/dev proxy
cloud-sql-proxy PROJECT:REGION:INSTANCE --port=5432
# App uses localhost with IAM auth plugin / connector library — no password
```

```python
# Conceptual: use Cloud SQL Python Connector with IAM
# from google.cloud.sql.connector import Connector
# conn = connector.connect(instance, "pg8000", user=SA_EMAIL, db="app", enable_iam_auth=True)
```

1. On Cloud Run/GKE: prefer built-in connectors/sidecar patterns with workload identity.
2. Do not bake JSON keys; use ADC/workload identity federation.
3. Enforce private IP; disable public if possible.

### 5. Verify with evidence

| Check | Expect |
| --- | --- |
| Connect as app SA | Success |
| Connect without IAM token | Fail |
| Old password user | Removed or vaulted break-glass only |
| Public network | Restricted/none |

```bash
# From owned runtime with ADC
# psql "host=127.0.0.1 dbname=app user=SA_EMAIL"  # via proxy IAM
```

### 6. Observe and harden

1. Log failed auth attempts; alert anomalies.
2. Rotate/disable unused SQL password users.
3. Keep proxy/connector libraries updated.
4. SSL mode require where applicable.

### 7. Hand off

1. Connection runbook per app; SA→DB user map.
2. Break-glass procedure with dual control.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Creds | IAM auth + ADC | Password in env forever |
| Network | Private IP | 0.0.0.0/0 authorized network |
| SA | One per app | Shared god SA |
| Keys | Workload identity | Downloaded JSON key in pod |
| Users | Minimal IAM users | Dozens of personal password users |
| Evidence | Denied unauth connect | “Proxy runs” only |

## Output Checklist

- [ ] Instance IAM auth enabled
- [ ] IAM DB users created for app SAs
- [ ] GCP IAM bindings least privilege
- [ ] Proxy/connector integrated
- [ ] Password secrets removed from app config
- [ ] Private networking posture reviewed
- [ ] Break-glass documented
- [ ] Auth failure monitoring
- [ ] `code-quality-standards` applied

## Rules

- Owned instances only.
- IAM auth still needs DB-level GRANTs—do not grant superuser casually.
- Prefer private connectivity and short-lived credentials.
- Verify engine-specific user naming rules (Postgres vs MySQL differ).
