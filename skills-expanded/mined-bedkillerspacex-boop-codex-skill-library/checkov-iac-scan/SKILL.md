---
name: checkov-iac-scan
description: >
  Checkov IaC scanning for owned Terraform/CloudFormation/Kubernetes/Helm/serverless
  code: install, CI gates, policy packs, suppressions with justification, and fix
  loops. Use when checkov CLI, bridgecrew policies, CKV_ IDs, or IaC misconfig CI —
  pair with `terraform-security-basics` for Terraform hardening depth.
---

# Checkov Iac Scan

## Scope And Authorization

- **In scope:** Infrastructure-as-code repositories you own or are authorized to scan.
- **Out of scope:** Scanning third-party private infra without permission.
- Suppressions are security decisions — require owners and review dates.
- Pair with `terraform-security-basics`, cloud hardening skills, `code-quality-standards`.

## When To Use

- Adding SAST-for-IaC to CI (Terraform, CFN, K8s manifests, Helm, ARM/Bicep as supported).
- Triaging `CKV_*` / `CKV2_*` findings.
- Enforcing org custom policies / soft-fail baselines.
- Pre-merge prevention of public S3, open SG, privileged pods, etc.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Terraform design hardening narrative | `terraform-security-basics` |
| Runtime cloud posture only | CSPM skills |
| Secrets in git general | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Item | Notes |
| --- | --- |
| Checkov | Static policy engine for IaC |
| CKV IDs | Built-in policy identifiers |
| Frameworks | terraform, cloudformation, kubernetes, helm, serverless, … |
| Suppress | inline comments or skip files — justify |
| CI | Fail on severity / specific policy sets |
| Custom policies | Python/YAML policy as code for org rules |

## Workflow

### 1. Confirm scope and success criteria

1. IaC roots, frameworks, CI system, severity gate policy.
2. Success: checkov in CI; critical findings fixed; suppressions tracked; developers know how to run locally.
3. Align with cloud baselines (CIS-ish).

### 2. Install and baseline

```bash
pip install checkov==3.*   # pin exact in CI
# or docker
docker run --rm -v "$PWD":/tf bridgecrew/checkov -d /tf
checkov --version
checkov -d . --framework terraform
checkov -d . -o json | head
```

1. Record counts by severity/framework.
2. Identify noisy policies that need config not blind skip.

### 3. Configure project

**.checkov.yaml sketch:**

```yaml
compact: true
framework:
  - terraform
  - kubernetes
directory:
  - .
skip-check:
  # - CKV_AWS_X  # prefer not; use metadata suppressions with reason
soft-fail: false
```

```bash
# Useful flags
checkov -d infra/ --quiet --compact
checkov -d . --check CKV_AWS_18,CKV_AWS_21
checkov -d . --skip-path vendor/
checkov -d . --repo-id org/repo --directory .
```

1. Exclude generated dirs carefully (still scan templates that matter).
2. For Terraform plan scanning, use supported plan JSON workflow when desired.

### 4. Triage findings

| Severity | Action |
| --- | --- |
| Critical/High | Block merge; fix or exception with security approval |
| Medium | Sprint fix / risk accept expiry |
| Low | Backlog / tune |

**Common fix directions:**

| Finding theme | Fix |
| --- | --- |
| Public storage | Block public ACLs/policies |
| Open 0.0.0.0/0 admin ports | Restrict CIDRs / SSM |
| Unencrypted resources | Enable CMK/SSE |
| Privileged K8s | drop caps, non-root |
| IAM * | Least privilege |

1. Prefer code fix over skip.
2. Inline skip format (example) must include reason:

```hcl
resource "aws_s3_bucket" "b" {
  # checkov:skip=CKV_AWS_XX: ticket-123 temporary for static site pending CloudFront 2026-10-01
  bucket = "example"
}
```

### 5. CI integration

```yaml
# GitHub Actions sketch
- uses: actions/checkout@v4
- run: pip install checkov==3.2.0
- run: checkov -d . --framework terraform --soft-fail-on LOW
```

1. Start soft-fail on legacy code with baseline, then ratchet.
2. Upload SARIF if using code scanning UI.
3. Cache pip; pin checkov version.

### 6. Custom policies (optional)

1. Encode org “must tag Owner” / “deny public LB” as custom checks.
2. Version policy pack in same or central repo.
3. Test policies against positive/negative fixtures.

### 7. Verify and hand off

```bash
checkov -d . --framework terraform
terraform validate
# Ensure skips have tickets
rg -n "checkov:skip" -g '*.tf'
```

1. Document how to run checkov in CONTRIBUTING.
2. Quarterly review of skips expired.
3. Apply `code-quality-standards` to modules when fixing.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Gate | CI fail on High | Optional local only |
| Skip | Reason + ticket + date | Mass skip-check list |
| Scope | All prod modules | Only toy examples scanned |
| Version | Pinned checkov | Latest floating surprises |
| Fix | Encrypt + least priv | Disable policy pack |
| Plan | Scan templates + plan | Trust manual console |

## Output Checklist

- [ ] Frameworks/roots identified
- [ ] Checkov pinned and baselined
- [ ] Config file committed
- [ ] High findings fixed or approved exceptions
- [ ] CI gate active
- [ ] Suppressions justified with expiry
- [ ] Dev docs for local run
- [ ] Custom policies considered
- [ ] Related terraform hardening applied
- [ ] `code-quality-standards` on fixes

## Rules

- Fix root misconfig; suppressions are temporary and owned.
- Pin tool versions for reproducible gates.
- Authorized repos only.
- Checkov is static — still need runtime posture and reviews.
- Terraform narrative hardening → `terraform-security-basics`.
