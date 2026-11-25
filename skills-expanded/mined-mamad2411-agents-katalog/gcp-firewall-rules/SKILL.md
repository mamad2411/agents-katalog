---
name: gcp-firewall-rules
description: >
  Review and harden Google Cloud VPC firewall rules for owned projects: 0.0.0.0/0 ingress,
  priority/order, target tags vs service accounts, hierarchical firewall policies, and
  shadow/redundant rules. Use when assessing GCP VPC allow/deny posture, open admin ports,
  over-broad CIDRs, or effective policy after org/folder policies—not for scanning or
  abusing third-party GCP networks.
---

# GCP Firewall Rules

## Scope And Authorization

- **In scope:** VPC firewall rules and hierarchical policies in GCP orgs/projects you administer.
- **Out of scope:** probing or attacking third-party GCP projects/networks.
- Prefer read-only inventory first; changes via change windows and IaC.
- Pair with general `firewall-rule-review` methodology and `code-quality-standards`.

## When To Use

- Auditing **`gcloud compute firewall-rules`** and hierarchical firewall policies.
- Finding SSH/RDP/DB open to `0.0.0.0/0`.
- Migrating from target tags to service account targeting.
- Understanding priority (lower number = higher precedence) and implied rules.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic multi-platform FW review | `firewall-rule-review` |
| GKE Autopilot constraints | `gcp-gke-autopilot-limits` |
| Cloud SQL auth | `gcp-cloud-sql-iam-auth` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | GCP behavior |
| --- | --- |
| Priority | 0–65535; lower wins |
| Direction | INGRESS / EGRESS |
| Targets | all instances, tags, or service accounts |
| Source | ranges, tags, service accounts (ingress) |
| Hierarchical policy | Org/folder policies evaluated with project rules |
| Implied rules | Default allow egress / deny ingress (project VPC) — confirm current model |

## High-risk patterns

| Pattern | Risk |
| --- | --- |
| `0.0.0.0/0` → tcp:22/3389 | Internet admin |
| `0.0.0.0/0` → tcp:5432/3306/27017 | Exposed data stores |
| Wide ranges + high priority allow | Shadows tighter denies |
| Tags applied inconsistently | Rules miss intended VMs |
| Egress fully open on sensitive tier | Exfil / pivot |

## Workflow

### 1. Confirm scope and success criteria

1. Projects, VPC networks, hierarchical policy folders, change freeze.
2. Success: inventory export; critical findings ticketed; over-broad rules fixed; effective access matches architecture.
3. Risk rubric agreed (world-SSH = critical).

### 2. Inventory project rules

```bash
gcloud compute firewall-rules list --project=PROJECT --format=json > fw-PROJECT.json
gcloud compute firewall-rules list --project=PROJECT \
  --filter='direction=INGRESS AND allowed[].ports:22'
# Hierarchical (org)
# gcloud compute firewall-policies list --organization=ORG
```

1. Map target tags → instances:
```bash
gcloud compute instances list --project=PROJECT --format='csv(name,tags.items[])'
```
2. Map service accounts used as targets.

### 3. Analyze

```text
For each INGRESS allow:
  - sourceRanges includes 0.0.0.0/0 or huge cloud NAT ranges unintentionally?
  - ports: specific vs 0-65535
  - targetTags empty? (applies broadly)
  - priority vs conflicting deny
  - disabled=true leftovers
```

1. Compare to intended tiers: lb → web → app → data.
2. Check GKE-related rules for over-broad node access.
3. Review egress allows that duplicate defaults or open sensitive destinations only.

### 4. Remediate

```bash
# Example tighten SSH to IAP-only ranges / corp CIDR — prefer IAP tunnel
# gcloud compute firewall-rules update allow-ssh --source-ranges=35.235.240.0/20 ...
```

1. Prefer **Identity-Aware Proxy** for admin SSH over public 22.
2. Prefer service account targets over sprawling tags when stable.
3. Encode rules in Terraform; PR review required.
4. Remove unused rules; rename for clarity (`allow-iap-ssh-ops`).

### 5. Verify with evidence

| Test | Expect |
| --- | --- |
| External SSH without IAP | Timed out / denied |
| Health checks from GCP ranges | Still succeed |
| Hierarchical deny | Effective as designed |

1. Use VPC Flow Logs samples if needed (authorized).
2. Avoid aggressive port scans; prefer config proofs.

### 6. Observe and harden

1. Enable Firewall Rules Logging selectively on risky rules.
2. Alert on new `0.0.0.0/0` admin port rules via policy-as-code checks.
3. Quarterly review of hierarchical policies.

### 7. Hand off

1. Findings table with rule names, priorities, evidence.
2. Target diagram tags/SAs.
3. Apply `code-quality-standards` for IaC.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Admin access | IAP / private | `0.0.0.0/0:22` |
| Targets | SA or precise tags | Empty targets on allow-all |
| Priority | Documented | Random 1000 everywhere |
| IaC | Reviewed Terraform | Console click drift |
| Evidence | Rule JSON snippet | “VPC is locked” vibe |
| Scope | Owned projects | Internet-wide GCP probe |

## Output Checklist

- [ ] Project/org scope recorded
- [ ] Firewall JSON inventory saved
- [ ] Hierarchical policies considered
- [ ] World-open and wide ports flagged
- [ ] Tag/SA target map complete
- [ ] Remediations applied or ticketed
- [ ] Verification of intended access
- [ ] Logging/drift detection planned
- [ ] `code-quality-standards` applied

## Rules

- Authorized GCP resources only.
- Prefer least privilege source ranges and IAP for admin.
- Evidence includes rule names and priorities.
- Use `firewall-rule-review` for cross-platform methodology depth; keep this skill GCP-specific.
