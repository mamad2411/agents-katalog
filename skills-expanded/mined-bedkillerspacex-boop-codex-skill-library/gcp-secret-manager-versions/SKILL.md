---
name: gcp-secret-manager-versions
description: >
  Google Cloud Secret Manager versioning: add versions, enable/disable, destroy,
  aliases (latest, custom), IAM on secrets vs versions, rotation patterns, and
  audit logging. Use for owned GCP projects when implementing secret rotation or
  reviewing version lifecycle — never dump live secret payloads into tickets or git.
---

# GCP Secret Manager Versions

## Scope And Authorization

- **In scope:** Owned/authorized projects managing application and infrastructure secrets.
- **Out of scope:** Reading or exfiltrating secrets outside authorization; brute-forcing
  secret names on third-party projects.
- Secret **payloads** are highly sensitive — prefer metadata operations in reviews.
- Production rotation needs dual control or automated pipelines with break-glass.
- Pair app integration code with `code-quality-standards` and org-wide process with
  `secrets-management-hygiene`.

## When To Use

- Creating secrets and managing multiple versions (rotate without downtime).
- Pinning workloads to version aliases (`latest`, `stable`, `previous`).
- Disabling compromised versions and destroying old material on schedule.
- Granting `secretAccessor` with conditions limited to secret name prefixes.
- Auditing who accessed which version (Data Access logs).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org-wide secrets program / inventory | `secrets-management-hygiene` |
| Baseline IAM / SA keys | `gcp-iam-basics` |
| IAM CEL on secret resources | `gcp-iam-conditions` |
| WIF for CI access to secrets | `gcp-workload-identity-federation` |
| VPC-SC around Secret Manager API | `gcp-vpc-sc-basics` |
| HashiCorp Vault / other KMS products | product-specific skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Secret | Named container with metadata and IAM |
| Version | Immutable payload revision (`1`, `2`, …) with state ENABLED/DISABLED/DESTROYED |
| Alias | Named pointer to a version id (`latest` is automatic; custom aliases supported) |
| Replication | Automatic multi-region or user-managed locations |
| CMEK | Customer-managed encryption keys for secret payloads |
| Rotation | Add new version → flip alias / deploy → disable old → destroy after grace |

### Access model

- `roles/secretmanager.admin` — manage secrets (too broad for apps).
- `roles/secretmanager.secretAccessor` — access payload (apps/CI).
- `roles/secretmanager.viewer` — metadata only.
- Prefer resource-level IAM on `projects/.../secrets/NAME` not project-wide accessor.
- Version destroy is irreversible after destruction completes — plan grace periods.

## Workflow

### 1. Confirm scope

1. Record project, secret names (classification), consumers, rotation SLA, authorization.
2. Success: zero long-lived secrets in git; consumers pin alias; old versions destroyed
   after N days; access logs enabled.

### 2. Inventory secrets and versions

```bash
gcloud services enable secretmanager.googleapis.com --project=PROJECT_ID

gcloud secrets list --project=PROJECT_ID --format=json > secrets.json

gcloud secrets versions list SECRET_ID --project=PROJECT_ID
gcloud secrets describe SECRET_ID --project=PROJECT_ID

# IAM on a single secret
gcloud secrets get-iam-policy SECRET_ID --project=PROJECT_ID
```

Do **not** run `versions access` unless required; if you must, avoid writing payload to disk
unencrypted and never commit it.

### 3. Create secret and first version

```bash
# Create empty secret with automatic replication
gcloud secrets create SECRET_ID \
  --project=PROJECT_ID \
  --replication-policy=automatic

# Add version from file (preferred over shell history)
gcloud secrets versions add SECRET_ID \
  --project=PROJECT_ID \
  --data-file=./secret-value.txt

# Or from stdin (careful with shell history)
printf '%s' "$SECRET_VALUE" | gcloud secrets versions add SECRET_ID \
  --project=PROJECT_ID --data-file=-
```

### 4. Aliases and consumer contract

```bash
# Point custom alias "stable" at version 3
gcloud secrets aliases update SECRET_ID \
  --project=PROJECT_ID \
  --update-aliases=stable=3

# Apps should fetch:
# projects/PROJECT_ID/secrets/SECRET_ID/versions/latest
# or .../versions/stable
```

| Consumer pattern | Guidance |
| --- | --- |
| Always `latest` | Simple; ensure deploy restarts on rotation |
| Pin version number | Reproducible; manual bump on rotate |
| Alias `stable` / `canary` | Blue/green rotation of secret material |
| Mount at startup only | Need rolling restart after rotate |

### 5. Rotate safely

1. Generate new material out-of-band (IdP, DB password change, API key mint).
2. `versions add` new payload → note version id.
3. Update external system if secret must match remote (DB user password).
4. Move alias `stable` → new version **or** roll fleet reading `latest`.
5. Verify app health.
6. `versions disable` previous version after soak.
7. `versions destroy` after retention/legal hold window.

```bash
gcloud secrets versions disable VERSION_ID --secret=SECRET_ID --project=PROJECT_ID
gcloud secrets versions destroy VERSION_ID --secret=SECRET_ID --project=PROJECT_ID
# Confirm prompts; destroy is permanent
```

### 6. IAM least privilege

```bash
gcloud secrets add-iam-policy-binding SECRET_ID \
  --project=PROJECT_ID \
  --member="serviceAccount:app@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

Use IAM Conditions (`gcp-iam-conditions`) to limit accessor to secret name prefixes when
granting at project level is unavoidable.

### 7. Verify and audit

```bash
# Metadata check
gcloud secrets versions list SECRET_ID --project=PROJECT_ID

# Access with impersonation (authorized test)
gcloud secrets versions access latest \
  --secret=SECRET_ID --project=PROJECT_ID \
  --impersonate-service-account=app@PROJECT_ID.iam.gserviceaccount.com \
  > /dev/null   # discard payload; success = IAM works

# Ensure Data Access audit logs enabled for Secret Manager
```

Monitoring:

- Alert on `DestroySecretVersion`, `SetIamPolicy` on secrets, burst `AccessSecretVersion`.
- SCC findings for public / overbroad secret IAM.

## Rotation matrix

| Secret type | Notes |
| --- | --- |
| API keys | Mint new key first; dual-run if provider allows |
| DB passwords | Transactional user alter + version add; connection pool recycle |
| TLS material | Prefer Certificate Manager / short-lived mTLS over raw PEMs in SM |
| Third-party webhooks | Update remote console before disabling old version |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Storage | Secret Manager + CMEK optional | Secrets in git / images |
| IAM | Per-secret accessor SA | Project `secretAccessor` for all humans |
| Rotation | Version add + alias flip + destroy | Overwrite tribal knowledge only |
| Access | Metadata in tickets | Paste secret values in Jira |
| Aliases | `stable` with soak | Disable old before apps restart |

## Output Checklist

- [ ] Project, secret inventory, classification recorded
- [ ] Version list and states documented
- [ ] Consumers and alias/version pin strategy defined
- [ ] IAM bindings least-privilege verified
- [ ] Rotation runbook tested in non-prod
- [ ] Old versions disabled/destroyed per policy
- [ ] Audit logs for AccessSecretVersion enabled
- [ ] Alerts on IAM/destroy events
- [ ] No secret payloads in git/tickets/chat
- [ ] `code-quality-standards` applied to integration code

## Rules

- Authorized projects only; minimize payload exposure.
- Prefer aliases + versions over “edit the one secret string in place.”
- Destroy schedules must respect legal hold / incident forensics.
- Never commit `versions access` output.
- Focus on Secret Manager version lifecycle; org process → `secrets-management-hygiene`.
