---
name: ecr-image-scanning
description: >
  Enable and operate Amazon ECR image vulnerability scanning for owned AWS
  accounts: basic vs enhanced (Inspector) scan, scan-on-push, registry and
  repository filters, finding triage, and CI/deploy gates on CRITICAL/HIGH.
  Use when ECR scanOnPush, Inspector enhanced scanning, describe-image-scan-findings,
  or blocking deploys on CVEs — not for abusing third-party registries.
---

# ECR Image Scanning

## Scope And Authorization

- **In scope:** AWS accounts and ECR repositories you own or are contracted to secure.
- **Out of scope:** Pulling/scanning images from registries you do not control as an attack.
- Scanning findings may include package versions—share carefully outside the security team.
- Prefer non-prod repos first when changing scan configuration blast radius.
- Pair deploy gates with `code-quality-standards` and container base-image hygiene.

## When To Use

- Turning on scan-on-push or continuous enhanced scanning for ECR.
- Choosing **basic** (Clair-based, on push) vs **enhanced** (Amazon Inspector) scanning.
- Defining registry-level filters (scan all vs include/exclude prefixes).
- Triaging CRITICAL/HIGH CVEs, suppressions with expiry, and CI fail policies.
- Auditing whether production digests were scanned before deploy.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic SBOM / supply chain program | SBOM skill in catalog |
| Kubernetes admission (Kyverno/OPA image checks) | policy admission skills |
| Dockerfile authoring with Earthly | `earthly-ci-basics` |
| Secrets in images | `secrets-management-hygiene` |
| Host OS patching outside containers | OS hardening skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Basic scan | Per-image on push; good starter; limited frequency features |
| Enhanced | Inspector continuous + better CVE intelligence; account config |
| Gates | Fail deploy on CRITICAL (and HIGH where feasible) for prod |
| Triage | Fix base image / rebuild > endless suppressions |
| Identity | Least-privilege IAM for `ecr:DescribeImageScanFindings` |
| Evidence | Store scan status in CI logs and change tickets |

## Workflow

### 1. Confirm scope and success criteria

1. Account IDs, regions, and repo name prefixes for prod vs non-prod.
2. Policy: which severities block merge/deploy; exception owner + max age.
3. Success: every prod digest has a successful scan; blockers enforced in pipeline.

### 2. Inventory scanning configuration

```bash
aws ecr get-registry-scanning-configuration --region "$AWS_REGION"
aws ecr describe-repositories --region "$AWS_REGION" \
  --query 'repositories[].{name:repositoryName,scan:imageScanningConfiguration}'
```

1. Note basic vs enhanced at registry level.
2. List repos with `scanOnPush` false.
3. Check Inspector whether enhanced is active in the account/region.

### 3. Baseline findings

```bash
REPO=my-app
IMAGE_TAG=sha-abc123
aws ecr describe-image-scan-findings --repository-name "$REPO" \
  --image-id imageTag=$IMAGE_TAG --region "$AWS_REGION" \
  --query 'imageScanFindings.findingSeverityCounts'
```

1. Sample top CRITICAL/HIGH package names for common bases (openssl, glibc, etc.).
2. Record false-positive patterns already accepted (with tickets).

### 4. Enable and tune scanning

```bash
# Repository scan on push (basic path)
aws ecr put-image-scanning-configuration --repository-name "$REPO" \
  --image-scanning-configuration scanOnPush=true --region "$AWS_REGION"

# Registry-level example: enhanced scanning for all repos (adjust to org policy)
aws ecr put-registry-scanning-configuration --region "$AWS_REGION" \
  --scan-type ENHANCED \
  --rules '[{"scanFrequency":"SCAN_ON_PUSH","repositoryFilters":[{"filter":"*","filterType":"WILDCARD"}]}]'
```

1. Prefer enhanced for production accounts when Inspector cost is approved.
2. Use filters if only `prod/*` must be continuous-scanned.
3. Ensure CI waits for scan completion before reading findings (basic scans are async after push).

### 5. CI / deploy gate

```bash
# Poll until COMPLETE (basic scan)
for i in $(seq 1 30); do
  STATUS=$(aws ecr describe-image-scan-findings --repository-name "$REPO" \
    --image-id imageDigest=$DIGEST --region "$AWS_REGION" \
    --query 'imageScanStatus.status' --output text)
  [ "$STATUS" = "COMPLETE" ] && break
  sleep 10
done
CRITICAL=$(aws ecr describe-image-scan-findings --repository-name "$REPO" \
  --image-id imageDigest=$DIGEST --region "$AWS_REGION" \
  --query 'imageScanFindings.findingSeverityCounts.CRITICAL' --output text)
if [ "${CRITICAL:-0}" != "0" ] && [ "${CRITICAL:-None}" != "None" ]; then
  echo "Blocking: CRITICAL findings present"; exit 1
fi
```

1. Gate on **digest**, not mutable `:latest`.
2. Allow listed exceptions via ticket id env var only with expiry date in the ticket.
3. Notify image owners (CODEOWNERS / repo tags) on new CRITICAL.

### 6. Triage workflow

1. Prefer upgrading base image or application dependency over infinite ignore lists.
2. Confirm fix available; if not, document residual risk and compensating controls.
3. Rebuild and re-scan; attach before/after severity counts to the change.

### 7. Hand off

1. Runbook: how to read findings in console vs CLI; who owns base images.
2. Periodic job: report unscanned prod digests still running in ECS/EKS.
3. IAM review: scanners and CI roles least privilege.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tags | Deploy by digest after scan | Deploy `:latest` never scanned |
| Policy | CRITICAL blocks prod | Scan enabled, results ignored |
| Exceptions | Ticket + expiry + owner | Permanent global suppress |
| Scope | Owned account repos | Scanning random public images as “recon” |
| Fix | Rebuild base | Hope runtime “is fine” |

## Output Checklist

- [ ] Registry/repo scan configuration recorded
- [ ] Basic vs enhanced decision documented
- [ ] scanOnPush or continuous rules applied for prod prefixes
- [ ] CI gate on digest with severity thresholds
- [ ] Sample findings triaged with owners
- [ ] Exception process with expiry
- [ ] IAM least privilege for scan APIs
- [ ] Residual risk and review date noted

## Rules

- Owned AWS accounts only.
- Scans are not a substitute for minimal base images and rapid rebuilds.
- Do not disable scanning “temporarily” without expiry.
- Keep credentials out of scan logs.
- Focus on ECR scanning; broader supply chain routes to SBOM/admission skills.
