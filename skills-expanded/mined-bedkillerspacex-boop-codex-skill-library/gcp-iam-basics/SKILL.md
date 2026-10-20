---
name: gcp-iam-basics
description: >
  GCP IAM principles for authorized assessment and hardening: least privilege,
  policy inheritance (org → folder → project), principal types, basic vs predefined
  vs custom roles, service accounts, user-managed key hygiene, and common privilege-
  escalation footguns. Use when reviewing org-owned projects or written engagements —
  not unauthorized enumeration of third-party GCP organizations.
---

# GCP IAM Basics

## Scope And Authorization

- **In scope:** GCP organizations, folders, and projects you own; labs; written
  authorized assessments.
- **Out of scope:** Unsolicited enumeration of third-party orgs, credential stuffing,
  or abusing compromised service-account keys.
- Prefer read-only inventory (`get-iam-policy`, IAM Recommender) before binding changes.
- Production role changes need a change window, owner, and rollback plan.
- Redact SA emails with elevated roles, key IDs, and customer project IDs from tickets
  when sharing outside the trust boundary.
- Pair implementation changes with `code-quality-standards`.

## When To Use

- Establishing or reviewing baseline IAM on a GCP project/org.
- Replacing broad `roles/owner` / `roles/editor` with predefined or custom roles.
- Auditing service accounts, key usage, and domain-wide delegation risk.
- Explaining IAM inheritance and effective policy to engineers or auditors.
- Preparing for deeper work: conditions, WIF, VPC-SC, or SCC findings.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| CEL condition expressions on bindings | `gcp-iam-conditions` |
| Workload Identity Federation (no keys) | `gcp-workload-identity-federation` |
| Org Policy constraints (deny public, restrict locations) | `gcp-org-policies` |
| VPC Service Controls perimeters | `gcp-vpc-sc-basics` |
| Secret Manager versions / rotation | `gcp-secret-manager-versions` |
| SCC finding triage | `gcp-scc-findings` |
| Public GCS / allUsers bindings | `gcp-storage-public-access` |
| AWS IAM / Azure RBAC | cloud-specific IAM skills |
| Implementation quality baseline | `code-quality-standards` |

## Concepts

| Concept | Notes |
| --- | --- |
| Resource hierarchy | Organization → Folder → Project → resource; policies inherit down |
| Binding | `{role, members[], condition?}` on a resource policy |
| Principals | `user:`, `serviceAccount:`, `group:`, `domain:`, `principalSet://` (WIF) |
| Basic roles | `roles/owner`, `roles/editor`, `roles/viewer` — avoid for day-to-day |
| Predefined roles | Curated (`roles/storage.objectViewer`, `roles/pubsub.subscriber`, …) |
| Custom roles | Project/org-level; only permissions you list; version carefully |
| Deny policies | IAM deny (separate from allow) can block even Owner in some cases |
| SA user vs SA itself | `iam.serviceAccountUser` lets a principal *act as* the SA |

### Inheritance and effective access

1. Effective allow set ≈ union of bindings from resource up the hierarchy (plus
   Google-managed and system policies).
2. A project-level Viewer plus a folder-level Editor still has Editor on that project.
3. Always inspect **effective** policy when diagnosing surprise access — do not only
   look at the project binding you just edited.

### Privilege-escalation footguns (authorized review)

| Pattern | Why it matters |
| --- | --- |
| `roles/iam.serviceAccountUser` + powerful SA | Impersonate SA → SA permissions |
| `roles/iam.serviceAccountTokenCreator` | Mint tokens / sign as SA |
| `roles/iam.serviceAccountKeyAdmin` | Create long-lived keys |
| `roles/resourcemanager.projectIamAdmin` | Grant self any role on project |
| `roles/owner` / primitive Editor | Full mutation surface |
| SA keys in repos / CI secrets | Static credentials, hard to rotate |
| Domain-wide delegation (Workspace) | SA can impersonate users |

## Workflow

### 1. Confirm scope

1. Record org ID, folder IDs, project IDs, environment, authorization, and blast radius.
2. Success criteria examples: no primitive Owner on humans in prod; no user-managed SA
   keys; each workload has a dedicated SA with predefined roles only.
3. Identify break-glass (`roles/owner` group with MFA + approval) before removing access.

### 2. Inventory policies and principals

```bash
# Auth context
gcloud auth list
gcloud config get-value project

# Project IAM policy (JSON for review)
gcloud projects get-iam-policy PROJECT_ID --format=json > project-iam.json

# Org / folder (needs resourcemanager permissions)
gcloud organizations get-iam-policy ORG_ID --format=json > org-iam.json
gcloud resource-manager folders get-iam-policy FOLDER_ID --format=json > folder-iam.json

# Service accounts and user-managed keys
gcloud iam service-accounts list --project=PROJECT_ID
gcloud iam service-accounts keys list \
  --iam-account=SA_EMAIL --project=PROJECT_ID

# Who can act as a given SA
gcloud iam service-accounts get-iam-policy SA_EMAIL --project=PROJECT_ID
```

Inventory checklist:

- [ ] Humans with Owner/Editor on prod projects
- [ ] Groups vs individual user bindings
- [ ] SAs with admin-class roles
- [ ] User-managed key counts and ages
- [ ] Cross-project SA usage / impersonation chains
- [ ] External identities (`allUsers`, `allAuthenticatedUsers`, partner domains)

### 3. Baseline recommendations

```bash
# IAM Recommender: unused role insights (API / Console / gcloud recommender)
gcloud recommender insights list \
  --project=PROJECT_ID \
  --location=global \
  --insight-type=google.iam.policy.Insight \
  --format=json
```

Capture before/after: binding count, primitive role count, open key count.

### 4. Apply least-privilege changes

1. Prefer **groups** in Cloud Identity / Workspace over direct `user:` bindings.
2. Replace `roles/editor` with service-specific predefined roles (e.g.
   `roles/run.developer`, `roles/container.developer`).
3. One SA per workload; grant only roles that workload needs.
4. Prefer Workload Identity / WIF over SA keys (`gcp-workload-identity-federation`).
5. Disable and delete unused user-managed keys; set org policy to constrain key creation
   where possible (`gcp-org-policies`).
6. Use custom roles only when predefined roles are too wide; document permission list
   and version.

```bash
# Add a binding (example — project-scoped)
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="group:app-readers@example.com" \
  --role="roles/storage.objectViewer"

# Remove a primitive role
gcloud projects remove-iam-policy-binding PROJECT_ID \
  --member="user:alice@example.com" \
  --role="roles/editor"

# Create custom role from YAML permissions list
gcloud iam roles create appDataReader \
  --project=PROJECT_ID \
  --file=custom-role-app-data-reader.yaml
```

### 5. Verify with evidence

```bash
# Policy diff after change
gcloud projects get-iam-policy PROJECT_ID --format=json > project-iam-after.json
# diff project-iam.json project-iam-after.json  (redact members if needed)

# Test as a principal (authorized; use test user or impersonation)
gcloud storage ls gs://BUCKET --impersonate-service-account=SA_EMAIL

# Policy Troubleshooter (Console or API): principal + permission + resource
# Confirms whether access is granted and which binding applied
```

1. Confirm intended principals can still perform required actions.
2. Confirm removed principals are denied (403) on sensitive APIs.
3. Re-run recommender / SCC IAM findings after stabilization.

### 6. Observe and harden

- Enable Data Access audit logs for IAM-sensitive services where required by policy.
- Alert on: `SetIamPolicy`, `CreateServiceAccountKey`, `google.iam.admin.v1.CreateServiceAccountKey`.
- Periodic access reviews: unused roles, stale group membership, orphaned SAs.
- Document exceptions with owner + expiry (e.g. temporary Owner for migration).

### 7. Hand off

1. Store policy exports in a controlled location (not a public bucket).
2. Update runbooks: who owns IAM for each project, break-glass procedure.
3. Link follow-ups: conditions, org policies, WIF migration.

## Role selection cheat sheet

| Workload need | Prefer | Avoid |
| --- | --- | --- |
| Read GCS objects | `roles/storage.objectViewer` | `roles/storage.admin` |
| Pub/Sub consume | `roles/pubsub.subscriber` | `roles/pubsub.admin` |
| GKE deploy only | `roles/container.developer` | `roles/container.admin` |
| View only | `roles/viewer` or service viewers | `roles/editor` |
| CI deploy | Dedicated SA + WIF + minimal deploy roles | Shared Owner user keys |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Human access | Groups + predefined roles | Individual Owner on every project |
| Workloads | One SA, no keys, WI/WIF | Shared SA + JSON key in repo |
| Inheritance | Review org/folder before project-only fix | Only patch project binding |
| Escalation | No SA User on powerful SAs for broad groups | Developers all get `serviceAccountUser` on prod compute SA |
| Keys | Zero user-managed keys | Keys never rotated |
| Verification | Troubleshooter + deny test | “Should work” after console click |

## Output Checklist

- [ ] Scope, project/org IDs, authorization recorded
- [ ] IAM policies exported (org/folder/project as applicable)
- [ ] Primitive Owner/Editor usage documented and reduced where agreed
- [ ] Service accounts inventoried; key hygiene status recorded
- [ ] Impersonation / SA User chains reviewed
- [ ] Least-privilege bindings applied or findings filed
- [ ] Verification: intended allow + unintended deny evidenced
- [ ] Audit logging / alerting for IAM mutations considered
- [ ] Exceptions have owner + expiry
- [ ] Neighbors routed (conditions, WIF, org policy, SCC) when needed
- [ ] `code-quality-standards` applied if IaC/code shipped

## Rules

- Authorized orgs/projects only; evidence over assumption.
- Prefer groups, predefined roles, and short-lived credentials over keys.
- Never commit SA JSON keys; never paste live keys into chat or tickets.
- Do not grant `roles/owner` “temporarily” without ticket, MFA, and expiry.
- Keep focus on baseline GCP IAM; route specialized controls to sibling skills.
