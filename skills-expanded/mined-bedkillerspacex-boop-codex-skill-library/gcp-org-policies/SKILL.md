---
name: gcp-org-policies
description: >
  GCP Organization Policy Service: constraints, policy hierarchy (org/folder/project),
  boolean and list constraints, dry-run/preview, and common hardening policies
  (public IP, SA keys, resource locations, domain restricted sharing). Use for owned
  GCP organizations with Org Policy Admin authority — not to weaken customer orgs.
---

# GCP Organization Policies

## Scope And Authorization

- **In scope:** Owned GCP orgs/folders/projects; authorized hardening engagements.
- **Out of scope:** Changing org policies on organizations you do not administer;
  using policy gaps to attack third parties.
- Org policies are **guardrails**: misconfiguration can block all SA key creation,
  all public IPs, or all resource creation in a region — use dry-run / pilot folders.
- Require change management for production org roots; document exceptions with expiry.
- Redact org IDs and exception principals appropriately when exporting configs.
- Pair IaC with `code-quality-standards`.

## When To Use

- Establishing security baselines at org or folder level.
- Enforcing “no user-managed SA keys”, “no public GCS”, “resource location allowlist”.
- Restricting sharing to corporate domains (`iam.allowedPolicyMemberDomains`).
- Rolling out constraints gradually with tags / conditional policies where supported.
- Responding to audit findings about missing org-level preventative controls.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Per-binding least privilege / CEL | `gcp-iam-conditions` / `gcp-iam-basics` |
| VPC Service Controls data perimeter | `gcp-vpc-sc-basics` |
| Public bucket investigation | `gcp-storage-public-access` |
| SCC finding workflow | `gcp-scc-findings` |
| WIF setup | `gcp-workload-identity-federation` |
| Binary Authorization / image signing | container supply-chain skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Constraint | Named control (e.g. `constraints/iam.disableServiceAccountKeyCreation`) |
| Policy | Constraint + rules at org, folder, or project |
| Inheritance | Child inherits parent unless replaced/merged per constraint rules |
| Boolean constraint | Enforce / not enforce |
| List constraint | Allow / deny values (services, regions, identities, …) |
| Dry-run / preview | Evaluate violations without enforcing (where supported) |
| Exception | Project/folder excluded or alternate rule with owner + expiry |

### Hierarchy behavior

1. Policies attach at organization, folder, or project.
2. Effective policy for a project merges inheritance per constraint semantics
   (some constraints are mergeable list; some replace).
3. Prefer **folder-level** pilots before org root enforcement.
4. Project-level exceptions should be rare and time-bounded.

## High-value constraints (starter set)

| Constraint | Purpose |
| --- | --- |
| `iam.disableServiceAccountKeyCreation` | Block new user-managed SA keys |
| `iam.disableServiceAccountKeyUpload` | Block uploading external keys |
| `iam.automaticIamGrantsForDefaultServiceAccounts` | Stop default broad grants |
| `iam.allowedPolicyMemberDomains` | Domain-restricted sharing |
| `storage.publicAccessPrevention` | Prevent public GCS access |
| `storage.uniformBucketLevelAccess` | Force UBLA |
| `compute.vmExternalIpAccess` | Limit external IPs on VMs |
| `compute.requireOsLogin` | OS Login requirement |
| `gcp.resourceLocations` | Data residency / region allowlist |
| `sql.restrictPublicIp` | No public Cloud SQL IPs |
| `run.allowedIngress` | Cloud Run ingress controls |

Always confirm exact constraint IDs and parameters in current Google docs before apply.

## Workflow

### 1. Confirm scope and success criteria

1. Record org ID, pilot folder, production folders, authorization, and rollback owner.
2. Success examples: zero new SA keys org-wide; no `allUsers` on GCS; only `us-*`
   locations for regulated folder.
3. Inventory workloads that **will break** (legacy keys, multi-region buckets, public
   demos) before enforce.

### 2. Inventory current policies

```bash
# List available constraints (org policy API)
gcloud org-policies list --organization=ORG_ID

# Describe effective / set policy for a constraint
gcloud org-policies describe CONSTRAINT_ID --organization=ORG_ID
gcloud org-policies describe CONSTRAINT_ID --folder=FOLDER_ID
gcloud org-policies describe CONSTRAINT_ID --project=PROJECT_ID

# Export for review
gcloud org-policies list --organization=ORG_ID --format=json > org-policies.json
```

Also inventory:

- Custom constraints (org policy custom constraints) if used
- Tags used for conditional org policies
- Existing project exceptions

### 3. Baseline with dry-run / simulate

1. Use **dry-run** mode or audit-only observation where the constraint supports it.
2. Collect would-be violations: projects creating keys, public buckets, wrong regions.
3. Share violation list with app owners; plan migrations (WIF, private SQL, etc.).

```bash
# Example: set policy from file (prefer dry-run fields when available in policy YAML)
# gcloud org-policies set-policy policy.yaml --organization=ORG_ID
```

### 4. Apply policies (pilot → expand)

Example boolean enforce (illustrative YAML shape — verify live schema):

```yaml
# disable-sa-key-creation.yaml
name: organizations/ORG_ID/policies/iam.disableServiceAccountKeyCreation
spec:
  rules:
    - enforce: true
```

```bash
gcloud org-policies set-policy disable-sa-key-creation.yaml

# Domain restricted sharing (list constraint — values are customer IDs / directory customer)
# Use current docs for allowed values format (directory customer ID, not always domain string)
```

List constraint pattern (resource locations):

```bash
# Prefer managed YAML in git; example command form varies by gcloud version
gcloud org-policies set-policy resource-locations.yaml
```

Rollout sequence:

1. Dev folder enforce.
2. Fix breakages; document exceptions.
3. Staging folder.
4. Prod folders / org root.
5. Remove temporary exceptions on schedule.

### 5. Verify enforcement

```bash
# Expect failure when constraint active
gcloud iam service-accounts keys create /tmp/key.json \
  --iam-account=SA_EMAIL --project=PROJECT_ID
# Should error with org policy violation

# Public access / location checks via product APIs after storage constraints
gcloud storage buckets describe gs://BUCKET --format=json
```

Evidence pack:

- Policy YAML + apply timestamp
- Failed mutation attempts showing deny
- Legitimate workflows still succeeding
- Exception list with owners

### 6. Exception management

| Exception type | Control |
| --- | --- |
| Project excluded from constraint | Ticket, owner, expiry, compensating control |
| Alternate allowlist value | Justify each value |
| Break-glass disable | Time-boxed, dual control, audit alert |

Never leave org-root `enforce: false` “for debugging” without a calendar end date.

### 7. Observe and hand off

- Alert on org policy changes (`SetPolicy` / SetOrgPolicy audit logs).
- SCC / Config Connector drift detection if used.
- Document how to request exceptions; link WIF and storage hardening runbooks.
- Review constraints quarterly against new Google constraint catalog.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Folder pilot + dry-run | Org-root big bang Friday |
| Exceptions | Expiry + owner + ticket | Permanent silent exclude |
| SA keys | Block create + migrate to WIF | Block keys but leave existing keys forever |
| Locations | Allowlist matched to apps | Deny list that surprises DR region |
| Sharing | Domain restricted + group IAM | Broad `allAuthenticatedUsers` exceptions |

## Output Checklist

- [ ] Org/folder scope and authorization recorded
- [ ] Current policies inventoried
- [ ] Violation / impact analysis completed for pilot set
- [ ] Dry-run or pilot enforce done before org-wide
- [ ] Target constraints applied as YAML/IaC
- [ ] Negative tests prove enforcement
- [ ] Positive tests prove critical apps still work
- [ ] Exceptions documented with expiry
- [ ] Audit alerting on policy mutation enabled
- [ ] Related IAM/WIF/storage follow-ups filed
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Only on orgs you administer or are authorized to harden.
- Prefer preventative org policies + detective SCC — not either alone.
- Never weaken public-access or key-creation constraints without compensating control.
- Keep originals of policy YAML in version control; review like code.
- Focus this skill on Organization Policy; route IAM bindings and VPC-SC separately.
