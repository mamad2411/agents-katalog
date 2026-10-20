---
name: gcp-scc-findings
description: >
  Google Cloud Security Command Center (SCC) findings: list/filter, severity triage,
  mute rules, continuous exports, asset context, and remediation tracking for owned
  GCP orgs. Use when operating SCC Standard/Premium/Enterprise findings pipelines —
  not for unauthorized scanning of third-party organizations.
---

# GCP Security Command Center Findings

## Scope And Authorization

- **In scope:** SCC on organizations/projects you own or are authorized to operate.
- **Out of scope:** Using SCC APIs against orgs without permission; exploiting findings
  on systems outside engagement scope.
- Findings often include resource names, IPs, and misconfig details — treat as sensitive.
- Prefer least-privilege SCC roles (`securitycenter.findingsViewer`, etc.) for analysts.
- Pair remediations with domain skills (`gcp-iam-basics`, `gcp-storage-public-access`, …)
  and `code-quality-standards` for code/IaC fixes.

## When To Use

- Standing up or improving findings triage workflow (SOC / cloud security).
- Querying active findings by category, severity, state, or resource.
- Creating mute rules for accepted risk or false positives with expiry.
- Exporting findings to BigQuery / Pub/Sub / SIEM for correlation.
- Measuring remediation SLAs (time-to-mute, time-to-inactive).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Fixing IAM primitives / SA keys | `gcp-iam-basics` |
| Public bucket hardening | `gcp-storage-public-access` |
| Org Policy preventative controls | `gcp-org-policies` |
| VPC-SC design | `gcp-vpc-sc-basics` |
| Container image CVE pipeline | `gcr-vulnerability-scanning` |
| Generic vulnerability mgmt process | broader vuln-mgmt skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Finding | Security signal: category, severity, state, resource name, source |
| Source | Detector (Security Health Analytics, Event Threat Detection, Web Security Scanner, custom modules, …) |
| State | ACTIVE / INACTIVE (lifecycle as resource fixed or finding closed) |
| Mute | Hides finding from default views; mute state vs finding state |
| Asset | SCC inventory of GCP resources for context |
| Continuous export | Stream findings to Pub/Sub or snapshot to BigQuery |
| Security Health Analytics (SHA) | Misconfiguration detectors (public bucket, open firewall, …) |
| Event Threat Detection (ETD) | Log-based threat detections (Premium+) |

Tier features differ (Standard vs Premium vs Enterprise). Confirm which detectors are
enabled for your org before promising coverage.

## Workflow

### 1. Confirm scope and access

1. Record organization ID, SCC tier, responsible team, authorization.
2. Verify API enablement: `securitycenter.googleapis.com`.
3. Success criteria: critical ACTIVE findings owned within SLA; mute rules reviewed
   quarterly; export to SIEM healthy.

```bash
gcloud auth list
gcloud services enable securitycenter.googleapis.com --project=PROJECT_ID
```

### 2. Inventory sources and findings volume

```bash
# List findings under org (filter examples; adjust parent)
# Parent formats: organizations/ORG_ID , folders/FOLDER_ID , projects/PROJECT_ID

gcloud scc findings list organizations/ORG_ID \
  --filter='state="ACTIVE" AND severity="CRITICAL"' \
  --format=json > findings-critical-active.json

gcloud scc findings list organizations/ORG_ID \
  --filter='state="ACTIVE" AND category="PUBLIC_BUCKET_ACL"' \
  --limit=50
```

Triage dimensions:

| Dimension | Questions |
| --- | --- |
| Severity | CRITICAL/HIGH first |
| Category | Known high-impact (public data, keys, open admin ports) |
| Resource | Prod vs sandbox; data classification |
| Age | New burst vs long-standing debt |
| Source | SHA misconfig vs ETD threat (different response playbooks) |

### 3. Enrich with asset and IAM context

```bash
# Describe a finding by name (full resource name from list)
gcloud scc findings list organizations/ORG_ID \
  --filter='name:"FINDING_ID"' --format=json

# Cross-check resource
gcloud storage buckets describe gs://BUCKET --format=json
gcloud projects get-iam-policy PROJECT_ID --format=json
```

Map finding → owner via:

- Resource labels (`owner`, `team`, `env`)
- Project folder hierarchy
- CMDBs / asset inventory exports

### 4. Remediate or risk-accept

1. **Remediate** using the specialist skill for the category (IAM, storage, firewall…).
2. Re-scan / wait for detector refresh; confirm finding becomes INACTIVE or disappears.
3. **Risk accept**: mute with justification, ticket, expiry — never silent forever mute.

```bash
# Mute config example (prefer Console/YAML IaC for complex rules)
# gcloud scc muteconfigs create ... --filter='...'
```

Mute rule hygiene:

- Filter as narrow as possible (project + category + resource prefix).
- Title includes ticket ID and expiry date.
- Quarterly review job deletes expired mutes.

### 5. Continuous export and alerting

```bash
# Continuous export to Pub/Sub (illustrative)
gcloud scc exports create EXPORT_ID \
  --organization=ORG_ID \
  --pubsub-topic=projects/PROJECT_ID/topics/scc-findings \
  --filter='severity="CRITICAL" OR severity="HIGH"'
```

Pipeline checklist:

- [ ] Pub/Sub topic + subscriber (SIEM / Cloud Function)
- [ ] Deduplicate by finding name
- [ ] Page on CRITICAL ACTIVE for prod folders
- [ ] BigQuery dataset for trend reporting (open vs closed over time)

### 6. Metrics and SLAs

| Metric | Intent |
| --- | --- |
| Open CRITICAL count | Backlog health |
| Median time-to-remediate | Response quality |
| Mute rate by category | Detector noise vs real risk |
| Recurrence rate | Fix durability |
| Export lag | Pipeline health |

Dashboard in Cloud Monitoring / Looker / SIEM; review weekly for cloud sec ops.

### 7. Hand off

1. Document top categories and standard playbooks (link sibling skills).
2. Assign default owners per folder/project label scheme.
3. Schedule mute-rule and false-positive reviews.
4. Align preventative controls (org policies) so findings do not recur.

## Category → remediation routing (examples)

| Finding theme | Route |
| --- | --- |
| Public bucket / object ACL | `gcp-storage-public-access` |
| SA user-managed keys | `gcp-iam-basics` + org policy |
| Overbroad IAM | `gcp-iam-basics` / conditions |
| Public SQL / open firewall | network hardening + org policies |
| K8s / image CVEs | `gcr-vulnerability-scanning` + cluster skills |
| VPC-SC violations | `gcp-vpc-sc-basics` |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Triage | Severity + asset criticality | Only sort by arrival time |
| Mute | Narrow filter + expiry + ticket | Mute `severity!=""` forever |
| Export | Filtered continuous export | Manual CSV once a year |
| Fix | Finding INACTIVE + preventative policy | Ticket closed while still ACTIVE |
| Access | Least-privilege SCC roles | All engineers org Admin |

## Output Checklist

- [ ] Org/project scope, SCC tier, authorization recorded
- [ ] ACTIVE CRITICAL/HIGH inventory exported
- [ ] Owners mapped for top findings
- [ ] Remediations applied or risk accepted with mute expiry
- [ ] Verification that fixed findings left ACTIVE state
- [ ] Continuous export / alerting configured
- [ ] SLA metrics defined
- [ ] Playbooks linked to sibling skills
- [ ] Secrets/resource identifiers redacted in external reports
- [ ] `code-quality-standards` applied if automation code shipped

## Rules

- Authorized SCC parents only.
- Findings are sensitive security data — minimize distribution.
- Prefer fix + prevent (org policy) over permanent mute.
- Evidence: finding name, resource, before/after state, ticket.
- This skill is triage/ops for SCC findings; deep remediations live in domain skills.
