---
name: gcp-iam-conditions
description: >
  GCP IAM Conditions (CEL) on role bindings: time windows, resource attributes,
  request attributes, and principal tags for least privilege beyond static roles.
  Use on owned GCP projects/orgs when tightening access with conditional bindings —
  not as a substitute for basic IAM review or unauthorized access testing.
---

# GCP IAM Conditions

## Scope And Authorization

- **In scope:** Owned or authorized GCP resources where you may add/update IAM
  bindings with conditions.
- **Out of scope:** Crafting conditions to evade detection on systems you do not own;
  bypassing customer security controls without engagement authorization.
- Validate conditions in non-prod first; a bad CEL expression can lock operators out
  or fail open relative to intent (always test both allow and deny paths).
- Redact principal emails and resource names containing customer data from notes.
- Pair IaC changes with `code-quality-standards`.

## When To Use

- Time-bound access (contractor, break-glass, maintenance window).
- Restrict a role to specific resource names, types, or tags (e.g. only one bucket).
- Limit high-risk APIs by IP / VPC attributes where supported.
- Express “role only if request matches X” without inventing many custom roles.
- Hardening after `gcp-iam-basics` shows roles that are still too broad in scope.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Baseline IAM, roles, SA keys | `gcp-iam-basics` |
| Org-wide guardrails (constraint list) | `gcp-org-policies` |
| Network/data exfil perimeter | `gcp-vpc-sc-basics` |
| WIF / external identity | `gcp-workload-identity-federation` |
| Secret version access patterns | `gcp-secret-manager-versions` |
| ABAC design in application code | `golang-abac-design` or app ABAC skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Piece | Description |
| --- | --- |
| Conditional binding | Same as IAM binding + `condition: { title, description, expression }` |
| CEL | Common Expression Language; must evaluate to bool |
| Resource attributes | e.g. `resource.name`, `resource.type`, `resource.service` |
| Request attributes | e.g. `request.time`, limited network attributes depending on product |
| Principal attributes | Tags / access levels in supported setups |
| Title / description | Required operational metadata — not optional fluff |

### What conditions are (and are not)

- **Are:** Fine-grained **when** a role applies for that binding.
- **Are not:** A full policy language replacing deny policies, Org Policy, or VPC-SC.
- Multiple bindings for the same role/member are OR’d for allow; conditions on each
  binding apply only to that binding.
- Not every permission respects every attribute — verify with Policy Troubleshooter
  and product docs for the API you care about.

### Common CEL patterns

```cel
// Time window (UTC)
request.time < timestamp("2026-12-31T23:59:59Z")

// Business hours example (illustrative — verify timezone handling)
request.time.getHours("America/Los_Angeles") >= 9 &&
request.time.getHours("America/Los_Angeles") < 17

// Resource name prefix (GCS bucket)
resource.type == "storage.googleapis.com/Bucket" &&
resource.name.startsWith("projects/_/buckets/app-dev-")

// Specific secret
resource.name == "projects/PROJECT_NUMBER/secrets/billing-api-key"
```

## Workflow

### 1. Confirm intent and supported attributes

1. Record principal, role, resource scope (org/folder/project/resource), and why a
   static role is insufficient.
2. Check product support: which attributes work for the target API (Storage, Secret
   Manager, Compute, etc.).
3. Define measurable success: access works only when condition true; 403 otherwise.
4. Plan break-glass unconditional binding (highly restricted group) before tightening.

### 2. Inventory existing conditional bindings

```bash
gcloud projects get-iam-policy PROJECT_ID --format=json > iam-before.json

# Filter bindings that already have conditions (jq example)
# jq '.bindings[] | select(.condition != null)' iam-before.json
```

Note titles, expiry timestamps, and owners for every condition found.

### 3. Design the condition

1. Write **title** (short, unique) and **description** (ticket URL, owner, expiry).
2. Prefer **deny by omission**: grant narrow role + condition rather than broad role
   with a weak condition.
3. Prefer resource.name / type filters over complex time math when possible.
4. Avoid conditions that always evaluate true (e.g. empty checks that pass).
5. For temporary access, put an absolute `request.time < timestamp(...)` upper bound.

### 4. Apply the conditional binding

```bash
# Temporary Storage admin-ish access scoped by time
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:contractor@example.com" \
  --role="roles/storage.objectAdmin" \
  --condition='expression=request.time < timestamp("2026-08-01T00:00:00Z"),title=temp-gcs-aug,description=Ticket-1234 expires 2026-08-01'

# Resource-restricted Secret Accessor (expression may need product-specific form)
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:app@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" \
  --condition='expression=resource.name.startsWith("projects/PROJECT_NUMBER/secrets/app-"),title=app-secrets-only,description=Only app- prefix secrets'
```

Terraform sketch:

```hcl
resource "google_project_iam_member" "temp_reader" {
  project = var.project_id
  role    = "roles/viewer"
  member  = "group:auditors@example.com"

  condition {
    title       = "audit-window-q3"
    description = "Ticket-999; remove after 2026-09-30"
    expression  = "request.time < timestamp(\"2026-10-01T00:00:00Z\")"
  }
}
```

### 5. Verify allow and deny paths

```bash
# After change, re-export policy
gcloud projects get-iam-policy PROJECT_ID --format=json > iam-after.json

# Policy Troubleshooter (Console) or API:
# principal + permission + resource + request context (time)
```

Test matrix:

| Case | Expect |
| --- | --- |
| Condition true, correct resource | Allow |
| Condition true, wrong resource | Deny (if resource-scoped) |
| Condition false (expired time) | Deny |
| Same principal, unconditional other binding | May still allow — remove conflicts |

1. Do not rely only on CEL syntax acceptance; runtime authorization is the proof.
2. Check for **duplicate bindings** without conditions that override your intent.
3. Document residual access from parent folders/org.

### 6. Lifecycle and hygiene

- Calendar or ticket expiry matching `request.time` bounds; remove dead bindings.
- Alert on `SetIamPolicy` that add conditions with long or missing expiry.
- Prefer IAM Conditions + groups; avoid one-off user conditions that never expire.
- Revisit when migrating to WIF principal sets (condition principal attributes differ).

### 7. Hand off

1. Export final policy; store redacted evidence of allow/deny tests.
2. List every conditional binding with owner and review date.
3. Link `gcp-iam-basics` for remaining primitive roles; org policy for hard guardrails.

## Condition design table

| Goal | Prefer | Avoid |
| --- | --- | --- |
| Temp access | Absolute timestamp upper bound | Open-ended “business hours only” forever |
| One bucket | resource.name equality / prefix | Project-wide `objectAdmin` unconditional |
| Break-glass | Short TTL + monitored group | Standing Owner + weak condition |
| Multi-resource | Tags / consistent naming | Copy-pasted near-duplicate expressions |
| Complexity | Small CEL, documented | Nested expressions no one can review |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Metadata | Title + ticket in description | Empty title, mystery expression |
| Testing | True and false cases evidenced | “gcloud accepted the flag” |
| Overlap | Search for unconditional same role | Ignore parent org bindings |
| Expiry | Date in CEL + calendar | Condition lives years past need |
| Scope | After basics least privilege | Conditions bolted onto Owner |

## Output Checklist

- [ ] Authorization and project/resource scope recorded
- [ ] Supported attributes validated for target APIs
- [ ] Pre-change IAM export stored
- [ ] Condition title, description, expression, owner, expiry documented
- [ ] Binding applied via gcloud/Terraform with review
- [ ] Allow path tested when condition true
- [ ] Deny path tested when condition false / wrong resource
- [ ] Conflicting unconditional bindings checked
- [ ] Cleanup ticket for expiry
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Authorized projects only; never use conditions to hide persistent over-privilege.
- CEL must be reviewed like code; prefer simple expressions.
- Conditions complement, not replace, Org Policy and VPC-SC.
- No live secrets in expressions, tickets, or chat.
- Keep skill focus on IAM Conditions; route baseline IAM and org guardrails elsewhere.
