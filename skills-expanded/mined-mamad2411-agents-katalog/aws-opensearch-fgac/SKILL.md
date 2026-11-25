---
name: aws-opensearch-fgac
description: >
  Amazon OpenSearch Service fine-grained access control (FGAC) for owned domains:
  master user, internal users/roles, FGAC vs resource policies/IAM, mapped backend
  roles, and dashboard access. Use when securing multi-tenant search domains —
  not for attacking OpenSearch domains outside authorization.
---

# AWS OpenSearch FGAC

## Scope And Authorization

- **In scope:** OpenSearch Service domains you own or administer under authorization.
- **Out of scope:** Brute-forcing or probing third-party OpenSearch endpoints.
- FGAC misconfig often leaves dashboards world-readable or master passwords weak — treat as high risk.
- Prefer VPC domains; if public, enforce FGAC + strict resource policies + SSO.
- Pair with `aws-iam-least-privilege` and secrets hygiene for master users.

## When To Use

- Enabling fine-grained access control on a domain.
- Mapping IAM roles to OpenSearch roles.
- Creating index-level permissions for teams.
- Migrating from IAM-only access to FGAC.
- Fixing 403 after FGAC enablement.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General IAM | `aws-iam-least-privilege` |
| Network isolation only | VPC skills |
| Elasticsearch legacy specifics | still similar; verify API differences |
| Secrets rotation | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Layer | Controls |
| --- | --- |
| Network | VPC SG / public endpoint decision |
| Domain resource policy | IAM principals allowed at HTTP layer |
| FGAC | Internal users, roles, role mappings, index perms |
| Master user | IAM ARN or internal user for bootstrap admin |
| Dashboards | Auth via SAML/Cognito/internal users |

## Access Stack

```text
Client → (TLS) → Resource policy / IAM auth → FGAC role mapping → index/doc permissions
```

Both outer IAM/resource policy **and** FGAC must allow the action.

## Workflow

### 1. Confirm scope and success criteria

1. Record domain ARN/endpoint, engine version, VPC vs public, tenants, Dashboards needs.
2. Success: least-privilege roles per team; master user in Secrets Manager; anonymous denied; apps use least roles.
3. Maintenance window if enabling FGAC on existing domain.

### 2. Inventory

```bash
aws opensearch describe-domain --domain-name "$DOMAIN"
aws opensearch describe-domain-config --domain-name "$DOMAIN"
# AdvancedSecurityOptions / FGAC flags in config
```

1. Current access policies (JSON).
2. Whether `AdvancedSecurityOptions.Enabled` is true.
3. List app clients and human admin paths.

### 3. Baseline

1. Export domain access policy and security options.
2. Snapshot index list and critical templates.
3. Test admin and app queries for baseline 200s.

### 4. Enable and configure FGAC

1. Enable advanced security / FGAC with master user:
   - Prefer **IAM ARN master** for ops via SigV4, or internal master stored in Secrets Manager.
2. Create OpenSearch roles: `team-a-read`, `team-a-write`, `dashboards-ro`.
3. Index patterns: `logs-team-a-*` with CRUD as needed; deny others.
4. Role mappings: map `arn:aws:iam::ACCT:role/team-a` → `team-a-write`.
5. Domain resource policy: allow those IAM roles (and deny unneeded accounts).
6. Dashboards: SAML/Cognito preferred over sharing master password.
7. Disable anonymous access; remove wide `Principal":"*"` unless public search product with read-only FGAC carefully designed.

**Least privilege examples (conceptual security plugin roles)**

- Cluster perms: minimal `cluster_composite_ops_ro` for readers.
- Index perms: `read` / `write` / `create_index` only where required.
- Tenant isolation for Dashboards objects.

### 5. Verify with evidence

```bash
# SigV4 signed request as app role — expect allowed on own indices
# As other team role — expect 403
curl -sS -u "master:****" "https://$ENDPOINT/_plugins/_security/api/roles"  # if internal user admin
```

1. Public unauthenticated GET → deny.
2. Master credentials not in git; rotation tested.
3. Dashboards login path uses SSO groups mapped to roles.

### 6. Observe and harden

1. Audit security plugin change logs / CloudTrail domain updates.
2. Alert on access policy changes to `Principal:*`.
3. Periodic review of role mappings for stale IAM roles.

### 7. Hand off

1. Role/mapping catalog and index naming convention.
2. Break-glass master recovery procedure.
3. App client signing libraries documented.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Master | IAM master or vaulted password | shared master in Slack |
| Mapping | IAM role → limited FGAC role | all map to all_access |
| Network | VPC + FGAC | public + no FGAC |
| Policy | explicit principals | `Principal":"*"` Action es:* |
| Indices | pattern per tenant | every role on `*` |
| Humans | SAML groups | everyone uses master |

## Output Checklist

- [ ] Domain network and FGAC status recorded
- [ ] Master user strategy secured
- [ ] Resource policy tightened
- [ ] FGAC roles and index patterns created
- [ ] IAM role mappings verified
- [ ] 403/200 evidence for allow/deny
- [ ] Dashboards auth configured
- [ ] Alerts on policy changes
- [ ] Break-glass documented
- [ ] `code-quality-standards` for automation

## Rules

- Owned domains only.
- FGAC + resource policy + network defense in depth.
- Never share master user for applications.
- Prefer SSO for humans; IAM roles for apps.
- Focus on FGAC; broader IAM design in companion skill.
