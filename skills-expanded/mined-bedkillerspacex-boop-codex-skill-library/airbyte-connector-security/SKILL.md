---
name: airbyte-connector-security
description: >
  Airbyte connector and platform trust for owned ELT: connector image supply chain,
  credential storage, network egress, custom connector review, destination least privilege,
  and secret hygiene. Use when hardening Airbyte OSS/Cloud workspaces you operate or
  reviewing custom source/destination connectors — not for abusing others’ Airbyte tenants.
---

# Airbyte Connector Security

## Scope And Authorization

- **In scope:** Airbyte deployments, workspaces, and connectors your organization owns.
- **Out of scope:** Accessing customer tenants without authorization; probing vendor SaaS outside contract.
- Prefer staging workspace for connector experiments; production credential changes need change control.
- Redact connection configs, API keys, and warehouse credentials from tickets.
- Pair custom connector code with `code-quality-standards`.

## When To Use

- Onboarding a new source/destination connector (marketplace or custom).
- Reviewing custom Docker connectors for unsafe code or overbroad auth.
- Hardening Airbyte secrets, RBAC, and egress.
- Incident review after credential leak via sync logs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Airflow DAG security | `airflow-dag-security` |
| Generic secrets program | `secrets-management-hygiene` |
| Warehouse IAM deep dive | cloud data-platform skills |
| Container image signing | `acr-content-trust` / image signing skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Surface | Risk |
| --- | --- |
| Source connectors | Read overly broad data; store long-lived tokens |
| Destination connectors | Overprivileged write (delete tables); inject SQL |
| Custom connector code | SSRF, path traversal, pickle, arbitrary commands |
| Platform | UI RBAC, secret store, log redaction, admin API |
| Network | Connector pods egress to Internet; SSRF to metadata IP |
| Images | Unpinned/malicious connector images |

## Workflow

### 1. Confirm scope and success criteria

1. Record Airbyte edition (OSS/Cloud), version, workspace, sources/destinations list.
2. Success: credentials in secret backend; connectors pinned/trusted; least-privilege dest roles; logs free of secrets; custom connectors reviewed.
3. Data classes flowing through syncs.

### 2. Inventory connections and identities

```bash
# OSS examples — adapt to your install
# UI: Settings → Sources / Destinations / Connections
# API (authorized):
curl -sS -H "Authorization: Bearer $TOKEN" "$AIRBYTE/api/v1/sources/list"
curl -sS -H "Authorization: Bearer $TOKEN" "$AIRBYTE/api/v1/destinations/list"
```

1. List who can create sources (can exfil via new destination).
2. Note where credentials live (DB vs secret manager integration).

### 3. Credential and RBAC hygiene

| Control | Target |
| --- | --- |
| Secret storage | External secret manager when available; no git |
| RBAC | Least workspace roles; separate prod/dev |
| Token lifetime | Short-lived OAuth where connector supports |
| Rotation | Documented per source system |
| Logs | Disable debug that prints Authorization headers |

1. Rotate any credential ever pasted into chat/tickets.
2. Prefer destination service accounts that can write only target schemas.

### 4. Review connector trust

**Marketplace / official images:**

1. Pin versions; record digest if self-hosting.
2. Read connector changelog before upgrade.
3. Limit which connectors operators may enable.

**Custom connectors:**

```bash
# Review repo
rg -n "subprocess|eval|pickle|requests\.(get|post)|socket|yaml.load" connectors/
# Build and scan image
docker build -t airbyte/source-custom:test .
trivy image airbyte/source-custom:test
```

| Check | Pass criteria |
| --- | --- |
| Network | Explicit allowlist hosts; timeouts |
| Paths | No arbitrary file read on platform host |
| Config schema | Secrets marked; not logged |
| Deps | Pinned; scanned |
| Spec | Least scopes documented for OAuth |

### 5. Destination least privilege (examples)

| Destination | Guidance |
| --- | --- |
| Snowflake/BigQuery/Redshift | Write to dedicated schema; no ACCOUNTADMIN |
| S3/GCS | Prefix-limited IAM; no `s3:*` on `*` |
| Warehouse raw layer | Separate from marts serving PII consumers |

### 6. Network and runtime isolation

1. Run connector workloads with restricted egress (proxy allowlist) when architecture allows.
2. Block cloud metadata IP from connector network namespace if SSRF-prone patterns exist.
3. Resource limits on sync jobs to reduce noisy-neighbor / fork bombs.

### 7. Verify and hand off

```bash
# Sync test in staging with synthetic data
# Confirm destination only has expected tables
# Grep logs for "Bearer", "password", "private_key"
rg -i "bearer|password|private_key|BEGIN " /var/log/airbyte/ 2>/dev/null || true
```

1. Document approved connectors list and review SLA for custom ones.
2. Alert on new destination creation in prod workspace (audit log).
3. Incident runbook: revoke source tokens, disable connection, rotate dest keys.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Credentials | Secret manager + rotation | Long-lived PAT in YAML git |
| Custom code | Reviewed + scanned image | Random GitHub fork unchecked |
| Dest IAM | Schema-scoped writer | Full warehouse admin |
| Logs | Redacted | Full request dumps |
| Workspace | Prod locked down | Everyone is admin |

## Output Checklist

- [ ] Edition/version/workspaces inventoried
- [ ] Sources/destinations and credential locations listed
- [ ] RBAC least privilege applied
- [ ] Connector allowlist / version pins
- [ ] Custom connectors reviewed and scanned
- [ ] Destination IAM scoped
- [ ] Egress/isolation considered
- [ ] Log redaction verified
- [ ] Audit alerts for sensitive config changes
- [ ] `code-quality-standards` on custom code

## Rules

- Owned Airbyte only; protect tenant boundaries.
- Treat connectors as code execution with data access — review accordingly.
- Never commit source/destination secrets.
- Prefer least privilege over “sync everything as admin.”
- Route warehouse-specific hardening to platform skills when needed.
