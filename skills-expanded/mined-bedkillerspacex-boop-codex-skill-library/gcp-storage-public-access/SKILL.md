---
name: gcp-storage-public-access
description: >
  Authorized assessment and hardening of Google Cloud Storage public exposure:
  allUsers / allAuthenticatedUsers IAM, uniform bucket-level access (UBLA),
  public access prevention (PAP), legacy ACLs vs IAM, signed URLs as alternative,
  and org-policy guardrails. Use for org-owned buckets or written engagements —
  not unauthorized enumeration of third-party GCS buckets.
---

# GCP Storage Public Access

## Scope And Authorization

- **In scope:** GCS buckets in projects you own or are authorized to assess.
- **Out of scope:** Scanning or accessing third-party public buckets without permission;
  using public object data for harm.
- Prefer read-only inventory first; remediations can break static websites or CDN origins.
- Redact object names that reveal customer data when reporting.
- Pair with `gcp-org-policies` for preventative controls and `gcp-scc-findings` for detection.

## When To Use

- Hunting `allUsers` / `allAuthenticatedUsers` on buckets or objects.
- Enabling Uniform Bucket-Level Access and Public Access Prevention.
- Migrating public static sites to Cloud CDN + backend bucket with controlled exposure
  or authenticated alternatives.
- Responding to SCC `PUBLIC_BUCKET_*` findings.
- Replacing public ACLs with short-lived Signed URLs / Signed Policy Documents.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org Policy enforce PAP / UBLA | `gcp-org-policies` |
| SCC finding triage workflow | `gcp-scc-findings` |
| Baseline project IAM | `gcp-iam-basics` |
| VPC-SC data exfil perimeter | `gcp-vpc-sc-basics` |
| Generic cloud public storage (S3) | AWS-specific skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| Control | Role |
| --- | --- |
| Legacy object ACLs | Per-object ALL_USERS readers — easy to leak |
| Bucket IAM | `allUsers` + `roles/storage.objectViewer` = public list/read depending on role |
| Uniform Bucket-Level Access | Disables ACLs; IAM only |
| Public Access Prevention | `enforced` blocks public principals even if IAM tries |
| Soft PAP / inherited | Project/org settings may influence |
| Signed URL | Time-bound access without making bucket public |
| Website config | `mainPageSuffix` often coexists with intentional public design |

### Public principals

| Member | Meaning |
| --- | --- |
| `allUsers` | Anyone on the Internet |
| `allAuthenticatedUsers` | Any Google account — still broadly public for most threat models |

## Workflow

### 1. Confirm scope

1. List projects/folders in scope; authorization letter for multi-project orgs.
2. Success: no unintentional public buckets; intentional public buckets documented,
   PAP exceptions justified; org policy prevents regression.

### 2. Inventory buckets and public bindings

```bash
gcloud storage buckets list --project=PROJECT_ID --format=json > buckets.json

# Per bucket IAM
gcloud storage buckets get-iam-policy gs://BUCKET --format=json

# Describe PAP / UBLA / website
gcloud storage buckets describe gs://BUCKET --format=json
```

Search exports for:

- `allUsers`, `allAuthenticatedUsers`
- `publicAccessPrevention` not `enforced`
- `uniformBucketLevelAccess` disabled
- Legacy ACL usage indicators

SCC / Asset Inventory:

```bash
# If SCC available — filter public bucket categories
gcloud scc findings list organizations/ORG_ID \
  --filter='state="ACTIVE" AND category:"PUBLIC_BUCKET"'
```

### 3. Classify each public bucket

| Class | Action |
| --- | --- |
| Accidental data | Remove public principals immediately; rotate any exposed secrets |
| Intentional static site | Prefer CDN, dedicated project, no sensitive prefixes; document |
| Partner sharing | Replace with signed URLs or authenticated service accounts |
| Unknown | Treat as incident until owner claims |

### 4. Remediate

**Remove public IAM:**

```bash
gcloud storage buckets remove-iam-policy-binding gs://BUCKET \
  --member=allUsers \
  --role=roles/storage.objectViewer

gcloud storage buckets remove-iam-policy-binding gs://BUCKET \
  --member=allAuthenticatedUsers \
  --role=roles/storage.objectViewer
```

**Enable UBLA and PAP:**

```bash
gcloud storage buckets update gs://BUCKET --uniform-bucket-level-access

gcloud storage buckets update gs://BUCKET \
  --public-access-prevention=enforced
```

**Object-level legacy ACLs** (if UBLA off): use `gcloud storage objects describe` and
strip public ACLs before enabling UBLA (UBLA requires ACL cleanup).

**Prefer signed URLs for temporary share:**

```bash
gcloud storage sign-url gs://BUCKET/object.bin \
  --duration=15m \
  --private-key-file=KEY.json
# Prefer service account + short duration; avoid long-lived signing keys
```

### 5. Org-level prevention

```text
# Via gcp-org-policies skill:
# constraints/storage.publicAccessPrevention
# constraints/storage.uniformBucketLevelAccess
```

Apply at folder/org after project cleanup so deploys cannot re-open public access.

### 6. Verify

| Check | Expect |
| --- | --- |
| Anonymous HTTP GET to object URL | 403 for private buckets |
| IAM policy JSON | No allUsers / allAuthenticatedUsers |
| `publicAccessPrevention` | `enforced` |
| SCC finding | INACTIVE / resolved |
| Legitimate app access | SA still works |

```bash
# Unauthenticated probe from authorized assessment host only
curl -sI "https://storage.googleapis.com/BUCKET/OBJECT"
# Expect 403

gcloud storage buckets describe gs://BUCKET \
  --format="yaml(iamConfiguration)"
```

### 7. Hand off

- Inventory of remaining intentional public buckets with owners.
- CI policy checks (Terraform plan deny public members).
- Alert on `SetIamPolicy` adding `allUsers`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Sharing | Signed URL 15m | Public objectAdmin |
| Static web | Dedicated public bucket + no secrets | Mix public assets and backups |
| Prevention | PAP enforced + org policy | Rely only on “we told engineers” |
| ACLs | UBLA on | Fine-grained public object ACLs |
| Response | Remove public + scan for leaked secrets | Only mute SCC finding |

## Output Checklist

- [ ] Scope/authorization recorded
- [ ] All buckets inventoried; public principals listed
- [ ] Each public bucket classified (accidental/intentional)
- [ ] Public bindings removed or exception documented
- [ ] UBLA + PAP enforced where required
- [ ] Anonymous access test 403 evidenced
- [ ] Org policy preventative control planned/applied
- [ ] SCC findings resolved
- [ ] Intentional public assets documented with owner
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- No unauthorized bucket enumeration on the public Internet for third parties.
- Assume leaked objects may contain secrets — rotate if exposure confirmed.
- Prefer PAP enforced as default for sensitive projects.
- Evidence over screenshots alone: policy JSON + curl status.
- Focus on GCS public access; org policy and SCC are sibling workflows.
