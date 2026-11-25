---
name: gcp-artifact-registry-cleanup
description: >
  Configure Google Artifact Registry cleanup policies: delete untagged images, retain
  minimum versions, package format specifics (Docker/Maven/npm/Python), dry-run validation,
  and IAM least privilege. Use when controlling storage cost and attack surface from stale
  images on owned GCP projects—not for deleting other orgs’ artifacts.
---

# GCP Artifact Registry Cleanup

## Scope And Authorization

- **In scope:** Artifact Registry repositories in GCP projects you own or administer.
- **Out of scope:** deleting artifacts in projects without authorization.
- Prefer dry-run / audit before destructive cleanup in production.
- Redact registry credentials; use ADC/workload identity.
- Pair IaC with `code-quality-standards`.

## When To Use

- Storage growth from untagged Docker layers and old package versions.
- Enforcing **cleanup policies** (conditional delete rules) on AR repos.
- Aligning retention with release cadence and rollback needs.
- Reducing stale vulnerable images lingering pullable.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Binary Authorization deploy policy | `gcp-binary-authorization` |
| Flux image automation | `flux-image-automation` |
| General secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| Cleanup policy | Rules evaluated to delete versions matching conditions |
| Untagged | Docker images without tags—often safe delete candidates |
| Keep minimum | Retain last N versions even if old |
| Formats | Docker, Maven, npm, Python, apt, etc.—conditions differ |
| IAM | `artifactregistry.*` permissions for policy admin vs reader |

## Example policy patterns

| Goal | Rule idea |
| --- | --- |
| Drop untagged Docker | delete when untagged older than 7d |
| Cap versions | keep last 30; delete older |
| Protect release tags | condition excludes `v*` or `release` tags if supported by rule design |
| Dev repo aggressive | shorter TTLs than prod |

## Workflow

### 1. Confirm scope and success criteria

1. Projects, repos, formats, current size/cost, rollback window.
2. Success: policy applied; dry-run expected deletions reviewed; prod protected tags retained.
3. Owners for emergency undelete (note: deletes may be permanent—confirm GCP undelete limits).

### 2. Inventory

```bash
gcloud artifacts repositories list --project=PROJECT
gcloud artifacts repositories describe REPO --location=REGION --project=PROJECT
# Docker size signals
gcloud artifacts docker images list LOCATION-docker.pkg.dev/PROJECT/REPO --include-tags
```

1. Identify untagged sprawl and ancient tags.
2. Map which CI still needs old tags.

### 3. Design retention

1. Prod: longer keep count; never delete last known good without process.
2. Dev/ephemeral: aggressive untagged + short TTL.
3. Document tag conventions (`sha-*`, `v1.2.3`, `latest` policy).

### 4. Apply cleanup policies

```bash
# Export / edit policy YAML per current gcloud flags
gcloud artifacts repositories list-cleanup-policies REPO \
  --location=REGION --project=PROJECT

# Apply from file (illustrative — verify flags for your gcloud version)
# gcloud artifacts repositories set-cleanup-policies REPO \
#   --location=REGION --project=PROJECT --policy=cleanup-policy.json
```

```json
{
  "cleanupPolicies": {
    "delete-untagged": {
      "id": "delete-untagged",
      "action": {"type": "DELETE"},
      "condition": {
        "tagState": "UNTAGGED",
        "olderThan": "7d"
      }
    },
    "keep-minimum": {
      "id": "keep-minimum",
      "action": {"type": "KEEP"},
      "mostRecentVersions": {"keepCount": 20}
    }
  }
}
```

1. Start with **dry-run** if available for your policy type/version.
2. Encode policy in Terraform/Pulumi for reviewable changes.
3. Restrict who can modify cleanup policies (break-glass).

### 5. Verify with evidence

| Check | Evidence |
| --- | --- |
| Policy present | describe/list shows rules |
| Untagged count trend | decreases after schedule |
| Protected versions | still pullable |
| CI | still pulls needed tags |

```bash
gcloud artifacts docker images list LOCATION-docker.pkg.dev/PROJECT/REPO --include-tags | head
```

### 6. Observe and harden

1. Billing/storage metrics per repo.
2. Alert on sudden mass delete anomalies if monitoring available.
3. Quarterly review of keepCount vs incident rollback needs.

### 7. Hand off

1. Policy JSON/YAML in Git with owners.
2. Tag naming standard doc.
3. Link Binary Authorization for deploy-time trust.
4. Apply `code-quality-standards` for IaC.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Dry-run + staged | Delete all >1d including prod tags |
| Prod | keepCount + tagged retention | Only untagged rule forgotten, tags forever |
| IaC | Reviewed policy | ClickOps silent change |
| Tags | Immutable semver | Overwrite `latest` as only reference |
| Access | Limited policy admins | All developers can set delete-all |
| Evidence | Size before/after | “We enabled cleanup” |

## Output Checklist

- [ ] Repos/formats inventoried
- [ ] Retention requirements documented
- [ ] Cleanup policy defined and applied
- [ ] Dry-run or staged validation done
- [ ] Protected versions verified pullable
- [ ] IaC ownership set
- [ ] Cost/size monitoring
- [ ] `code-quality-standards` applied

## Rules

- Owned projects only; destructive ops need review.
- Prefer keep rules that preserve rollback windows.
- Cleanup is not a substitute for vulnerability scanning or Binary Authorization.
- Verify exact gcloud/Terraform schema for your API version.
