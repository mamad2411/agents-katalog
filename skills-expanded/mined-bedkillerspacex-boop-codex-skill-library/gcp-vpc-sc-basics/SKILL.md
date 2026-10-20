---
name: gcp-vpc-sc-basics
description: >
  VPC Service Controls (VPC-SC) basics for owned GCP orgs: service perimeters,
  restricted services, access levels (Access Context Manager), ingress/egress
  policies, dry-run mode, and common break-glass patterns. Use to reduce data
  exfiltration risk from Google APIs — not as a substitute for IAM or firewall rules.
---

# GCP VPC Service Controls Basics

## Scope And Authorization

- **In scope:** Organizations where you administer Access Context Manager / VPC-SC.
- **Out of scope:** Weakening perimeters on customer orgs; using perimeter gaps to exfiltrate.
- Perimeter misconfig can **deny all API access** to Storage, BigQuery, etc. — always
  dry-run and pilot projects first.
- Production enforce requires change window, rollback plan, and on-call.
- Pair with `gcp-iam-basics` and `gcp-org-policies`; VPC-SC is defense-in-depth.

## When To Use

- Protecting sensitive projects (PII, finance) from data exfil via Google APIs.
- Bridging on-prem / partner access with Access Levels (IP, device, identity).
- Moving from dry-run to enforced perimeters after violation cleanup.
- Designing ingress (who can enter) and egress (which external projects/APIs allowed).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| VPC firewall / network segmentation only | network VPC skills |
| IAM least privilege | `gcp-iam-basics` |
| Org Policy constraints | `gcp-org-policies` |
| Public GCS hardening | `gcp-storage-public-access` |
| WIF for CI identity | `gcp-workload-identity-federation` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Service perimeter | Boundary around projects + restricted Google services |
| Restricted services | APIs protected (e.g. `storage.googleapis.com`, `bigquery.googleapis.com`) |
| Access level | ACM condition (IP, members, device policy) required for access from outside |
| Ingress policy | Who/what may call into perimeter resources |
| Egress policy | Whether data/API calls may leave to exterior projects/services |
| Dry-run | Log violations without blocking |
| Bridge | Links perimeters for controlled sharing |
| VPC-SC ≠ VPC firewall | Works at Google API identity/context layer, not only packet filter |

### Threat model (simplified)

Attacker with stolen user/SA credentials **or** compromised VM tries to copy BigQuery/
GCS data to a personal project or public Internet using Google APIs. Perimeter +
egress policies block or raise violations even when IAM would allow the API method.

## Workflow

### 1. Confirm scope and success criteria

1. Record org ID, pilot projects, sensitive data stores, admin identities, authorization.
2. Success: dry-run clean for pilot; enforce without breaking CI; exfil to free trial
   project denied in test.
3. Map required **cross-project** flows (ETL, shared KMS, logging sinks) before lock-down.

### 2. Inventory Access Context Manager assets

```bash
# Access policies (org)
gcloud access-context-manager policies list --organization=ORG_ID

# Access levels
gcloud access-context-manager levels list --policy=POLICY_ID

# Perimeters
gcloud access-context-manager perimeters list --policy=POLICY_ID
gcloud access-context-manager perimeters describe PERIMETER \
  --policy=POLICY_ID --format=json
```

### 3. Design perimeter

1. **Projects in perimeter:** all projects that hold sensitive data + their runtimes.
2. **Restricted services:** start with high-value APIs (Storage, BQ, Secret Manager,
   Spanner, Pub/Sub, …) — expand deliberately.
3. **Access levels:** corp IP ranges / identity groups for admin break-glass.
4. **Ingress:** allow only required identities/VPC sources/APIs.
5. **Egress:** deny by default where possible; allowlist partner projects and needed
   external services explicitly.

Document expected violation classes (legacy personal gcloud from home IP, etc.).

### 4. Implement dry-run first

```bash
# Example: create perimeter in dry-run (prefer YAML files in git)
# gcloud access-context-manager perimeters create PERIMETER \
#   --title="sensitive-data-dryrun" \
#   --resources=projects/PROJECT_NUMBER \
#   --restricted-services=storage.googleapis.com,bigquery.googleapis.com \
#   --policy=POLICY_ID \
#   --perimeter-type=regular
#
# Enable dry-run config / use update with dry-run spec per current gcloud docs
```

Use **dry-run perimeter config** so traffic is logged, not blocked. Collect 1–2 weeks
of violations in large orgs.

### 5. Remediate violations then enforce

Common violation fixes:

| Violation | Fix |
| --- | --- |
| User from home IP using gcloud | VPN / BeyondCorp / access level update |
| CI outside perimeter | Move runner project inside or ingress from WIF identity |
| Cross-project sink | Egress to logging project or move sink project inside |
| SaaS integration | Documented egress to vendor; prefer PSC patterns |

```bash
# Update perimeter to enforced after dry-run clean
# gcloud access-context-manager perimeters update PERIMETER \
#   --policy=POLICY_ID \
#   --set-spec-from-dry-run  # if using dual dry-run/enforce workflow
```

### 6. Verify

| Test | Expect (enforced) |
| --- | --- |
| SA inside perimeter → GCS in perimeter | Allow (with IAM) |
| SA inside → copy to project outside without egress | Deny / violation |
| User matching access level from allowed IP | Allow admin paths |
| Random Internet identity with stolen key | Blocked by perimeter even if IAM still attached |

```bash
# Attempt authorized exfil test in lab project only
# gcloud storage cp gs://IN_PERIMETER/file gs://OUTSIDE_BUCKET/
# Expect VPC-SC error
```

Enable audit logs for Access Context Manager / perimeter denials; pipe to SIEM.

### 7. Operate

- Change management for every perimeter membership edit.
- Alert on perimeter updates and spike in dry-run/enforce violations.
- Quarterly review of access levels (stale CIDRs, contractors).
- Coordinate with `gcp-storage-public-access` — public buckets still matter; VPC-SC
  does not make public Internet ACLs safe.

## Ingress / egress cheat sheet

| Direction | Prefer |
| --- | --- |
| Human admin | Access level + MFA identity group |
| GKE/GCE workload | Same perimeter project; private Google access |
| CI (GitHub) | WIF + ingress identity from pool; limit to deploy APIs |
| Shared services project | Same perimeter or explicit egress + bridge |
| Break-glass | Temporary access level widen with ticket/expiry |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Dry-run weeks → enforce | Enforce Friday on all prod |
| Egress | Explicit allowlist | Open egress “so ETL works” |
| Membership | All data + compute together | Data in perimeter, ETL outside unmanaged |
| Break-glass | Timed access level | Disable perimeter permanently |
| Testing | Lab exfil attempt documented | Assume IAM alone enough |

## Output Checklist

- [ ] Org policy ID, perimeter design, authorization recorded
- [ ] Sensitive projects and restricted services listed
- [ ] Access levels defined and reviewed
- [ ] Dry-run enabled; violations triaged to near-zero
- [ ] Ingress/egress policies documented
- [ ] Enforce cutover with rollback plan
- [ ] Exfil denial test evidenced in lab
- [ ] Monitoring/alerts on violations and perimeter changes
- [ ] Related IAM/org-policy/storage work linked
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Only on orgs you administer with authorization.
- Dry-run before enforce; never “test in prod” without pilots.
- VPC-SC complements IAM — keep least privilege.
- Document every egress exception with owner + review date.
- Focus on VPC-SC basics; deep network firewall design is out of scope.
