---
name: gcp-assured-workloads
description: >
  Plan and operate Google Cloud Assured Workloads for regulated controls: compliance
  regimes, folder-level enforcement, data residency, personnel access controls, and
  monitoring gaps. Use when designing owned GCP environments that must meet Assured
  Workloads regimes—not as a guarantee of full legal compliance without counsel.
---

# GCP Assured Workloads

## Scope And Authorization

- **In scope:** GCP organizations/folders/projects you administer with authorization.
- **Out of scope:** modifying another customer’s Assured Workloads or claiming legal certification without authority.
- Assured Workloads supports compliance **controls**—legal sign-off remains with compliance teams.
- Redact org IDs and sensitive control exceptions from public docs.
- Pair with `code-quality-standards` for automation.

## When To Use

- Creating **Assured Workloads** folders for regimes (e.g. FedRAMP, IL, EU regions—availability depends on Google offerings).
- Understanding what AW enforces vs what you must still configure (VPC, IAM, logging).
- Reviewing data location, support access, and key management constraints.
- Migrating projects into assured folders carefully.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| VPC firewall hygiene | `gcp-firewall-rules` |
| BigQuery row access | `gcp-bigquery-row-access` |
| Binary Authorization | `gcp-binary-authorization` |
| Secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Topic | Guidance |
| --- | --- |
| Folder boundary | AW typically applies at folder; projects inherit constraints |
| Regime selection | Choose correct compliance program at creation—hard to “swap” casually |
| Org policies | Additional constraints beyond baseline GCP |
| Data residency | Region restrictions for resources |
| Access transparency / support | Understand personnel access features per regime |
| Shared responsibility | You still secure apps, IAM least privilege, logging sinks |

## Workflow

### 1. Confirm scope and success criteria

1. Compliance target, data classification, regions, existing org structure.
2. Success: AW folder created with correct regime; projects inside pass control checks; residual gaps listed for owners.
3. Engage compliance/legal stakeholders early.

### 2. Inventory org landscape

```bash
gcloud organizations list
gcloud resource-manager folders list --organization=ORG_ID
gcloud assured workloads list --location=global --organization=ORG_ID 2>/dev/null || true
```

1. Map existing projects that must move vs greenfield.
2. Note services not available under chosen regime/region.

### 3. Design folder and networking

1. Separate AW folders per regime if required.
2. Plan Shared VPC host projects under constraints.
3. KMS key locations aligned with residency.
4. Logging sinks to compliant storage destinations.

### 4. Create and enroll (high level)

```bash
# Exact flags depend on regime and current gcloud surface — verify docs
# gcloud assured workloads create ... --compliance-regime=... --billing-account=...
```

1. Create via console/gcloud/Terraform with change control.
2. Create child projects **inside** the AW folder—not outside then hope.
3. Apply baseline IaC: IAM, firewall, SCC, logging.

### 5. Validate controls

| Check | Method |
| --- | --- |
| Resource region | Attempt create outside allowed region → denied |
| Org policy | `gcloud org-policies describe` on folder |
| Services | Unsupported API fails predictably |
| Access logs | Access Transparency configured if applicable |
| CMEK | Keys in allowed locations |

### 6. Operate ongoing

1. Monitor policy violations via Policy Controller / Org Policy / SCC as used.
2. Change management for exceptions with expiry.
3. Vendor shared responsibility matrix reviewed annually.
4. Do not disable AW controls to “unblock” prod without compliance approval.

### 7. Hand off

1. Architecture diagram folder→projects→regions.
2. Gap list: app-level controls still required.
3. Runbook for project creation in AW.
4. Apply `code-quality-standards` for IaC modules.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Placement | Projects born in AW folder | Uncontrolled projects then migrate panic |
| Regime | Chosen with compliance | Random regime “sounds secure” |
| Expectation | Shared responsibility clear | “AW means fully compliant app” |
| Exceptions | Ticketed + expiry | Silent org policy weaken |
| Regions | Enforced + monitored | Multi-region free-for-all |
| Evidence | Denied create proofs | Checkbox only |

## Output Checklist

- [ ] Compliance regime and stakeholders documented
- [ ] AW folder/workload inventory
- [ ] Project placement strategy
- [ ] Region/service constraints validated
- [ ] IAM/logging/KMS baseline under folder
- [ ] Residual gaps assigned
- [ ] Exception process defined
- [ ] IaC quality standards applied

## Rules

- Owned org only; not legal advice—pair with compliance officers.
- Assured Workloads ≠ automatic application security.
- Prefer greenfield under AW over risky retrofits without plan.
- Keep secrets and customer data handling policies explicit.
