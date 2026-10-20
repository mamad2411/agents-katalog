---
description: >
  Scan Infrastructure as Code files for security misconfigurations and compliance violations.
  Supports Terraform, CloudFormation, Kubernetes manifests, Dockerfiles, Helm charts, Ansible,
  and ARM templates. Runs automated scanning (Checkov, trivy, tfsec), performs manual review
  for logic-level misconfigs, and generates a formal IaC Security Report with CIS benchmark
  mapping and framework traceability. Use this skill whenever the user asks to scan infrastructure
  code, review Terraform for security, check Kubernetes manifests, audit Dockerfiles, validate
  cloud configurations, or assess IaC compliance. Also trigger on: 'IaC scan', 'Terraform
  security', 'K8s security', 'Docker security', 'cloud misconfiguration', 'CIS benchmark',
  'infrastructure audit', 'Checkov', 'tfsec', or any request to find security issues
  in infrastructure definitions — even 'is my Terraform secure' or 'review my deployment config'.
---

# IaC Security Scanner

You are acting as a Cloud Security Engineer reviewing Infrastructure as Code for security
misconfigurations and compliance violations.

Before generating, read:
→ `references/report-template.md` — report structure
→ `references/check-catalog.md` — high-value manual checks by IaC type

---

## Step 1 — Detect IaC Type & Collect Context

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
DATE=$(date +%Y%m%d)
REPORT_DIR="$REPO_ROOT/security-review"
mkdir -p "$REPORT_DIR"
AUTHOR_NAME=$(git config user.name 2>/dev/null || echo "N/A")
AUTHOR_EMAIL=$(git config user.email 2>/dev/null || echo "N/A")
REPO_NAME=$(basename "$REPO_ROOT")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "N/A")
COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "N/A")
```

These variables populate the report Header Metadata (Author, Repository, Branch, Commit).

Scan for IaC files:

| Indicator | IaC Type | Scanner priority |
|---|---|---|
| `*.tf`, `*.tfvars`, `.terraform.lock.hcl` | Terraform | Checkov → trivy → tfsec (legacy) |
| `*.yaml`/`*.json` with `AWSTemplateFormatVersion` | CloudFormation | Checkov → cfn-lint |
| `*.yaml` with `apiVersion`/`kind` | Kubernetes | Checkov → trivy → kubesec |
| `Dockerfile*` | Docker | Checkov → trivy → hadolint |
| `Chart.yaml`, `templates/` | Helm | Checkov (with `--framework helm`) |
| `*.yml` with `tasks:`/`hosts:` | Ansible | Checkov (with `--framework ansible`) |
| `*.bicep`, `*.json` with `$schema.*deploymentTemplate` | ARM/Bicep | Checkov |
| `docker-compose*.yml` | Docker Compose | Checkov → manual |

```bash
echo "=== IaC file detection ==="
IAC_FILES=$(find "$REPO_ROOT" -maxdepth 4 \
  \( -name "*.tf" -o -name "Dockerfile*" -o -name "*.yaml" -o -name "*.yml" \
     -o -name "*.bicep" -o -name "Chart.yaml" \) \
  -not -path "*/.terraform/*" -not -path "*/node_modules/*")
echo "$IAC_FILES" | head -50

if [ -z "$IAC_FILES" ]; then
  echo "No IaC files detected under $REPO_ROOT. Nothing to scan."
  echo "Provide a path containing Terraform/CloudFormation/Kubernetes/Docker/Helm/Ansible/ARM files."
  exit 0
fi
```

If `$IAC_FILES` is empty the run stops above with guidance.

---

## Step 2 — Run Automated Scans

### 2a. Primary: Checkov (preferred — covers all IaC types)

```bash
if command -v checkov &>/dev/null; then
  CHECKOV_JSON="$REPORT_DIR/checkov-results-${DATE}.json"

  checkov -d "$REPO_ROOT" \
    --output json \
    --compact \
    --quiet \
    > "$CHECKOV_JSON" 2>/dev/null

  echo "Checkov results: $CHECKOV_JSON"
else
  echo "Checkov not found. Install: pip install checkov"
  CHECKOV_JSON=""
fi
```

### 2b. Supplementary scanners (if available)

Run the best supplementary scanner for the detected IaC type:

```bash
# Docker/K8s/Terraform/IaC — trivy config mode (preferred for Terraform misconfig)
if command -v trivy &>/dev/null; then
  trivy config "$REPO_ROOT" --format json > "$REPORT_DIR/trivy-config-${DATE}.json" 2>/dev/null
fi

# Terraform — tfsec (legacy fallback only).
# NOTE: tfsec is deprecated; Aqua Security merged it into Trivy (2023). Prefer `trivy config`
# above for Terraform misconfig scanning. Run tfsec only if trivy is unavailable.
if find "$REPO_ROOT" -maxdepth 3 -name '*.tf' -print -quit | grep -q . \
   && ! command -v trivy &>/dev/null && command -v tfsec &>/dev/null; then
  tfsec "$REPO_ROOT" --format json > "$REPORT_DIR/tfsec-results-${DATE}.json" 2>/dev/null
fi

# CloudFormation — cfn-lint
if find "$REPO_ROOT" -maxdepth 4 \( -name '*.yaml' -o -name '*.yml' -o -name '*.json' \) \
     -print -quit | grep -q . && command -v cfn-lint &>/dev/null; then
  cfn-lint "$REPO_ROOT" --format json > "$REPORT_DIR/cfn-lint-${DATE}.json" 2>/dev/null
fi

# Kubernetes — kubesec (per manifest)
if command -v kubesec &>/dev/null; then
  : > "$REPORT_DIR/kubesec-${DATE}.json"   # truncate so same-day re-runs are idempotent
  find "$REPO_ROOT" -maxdepth 4 \( -name '*.yaml' -o -name '*.yml' \) \
       -not -path "*/.terraform/*" -not -path "*/node_modules/*" -print0 2>/dev/null \
    | while IFS= read -r -d '' MANIFEST; do
        kubesec scan "$MANIFEST" >> "$REPORT_DIR/kubesec-${DATE}.json" 2>/dev/null
      done
fi

# Helm — checkov with the helm framework
if find "$REPO_ROOT" -maxdepth 4 -name 'Chart.yaml' -print -quit | grep -q . \
   && command -v checkov &>/dev/null; then
  checkov -d "$REPO_ROOT" --framework helm --output json --compact --quiet \
    > "$REPORT_DIR/checkov-helm-${DATE}.json" 2>/dev/null
fi

# Ansible — checkov with the ansible framework
if find "$REPO_ROOT" -maxdepth 4 \( -name '*.yml' -o -name '*.yaml' \) -print -quit | grep -q . \
   && command -v checkov &>/dev/null; then
  checkov -d "$REPO_ROOT" --framework ansible --output json --compact --quiet \
    > "$REPORT_DIR/checkov-ansible-${DATE}.json" 2>/dev/null
fi

# Dockerfile — hadolint (scan every detected Dockerfile, not only repo-root)
if command -v hadolint &>/dev/null; then
  : > "$REPORT_DIR/hadolint-${DATE}.json"   # truncate so same-day re-runs are idempotent
  find "$REPO_ROOT" -maxdepth 4 -name 'Dockerfile*' \
       -not -path "*/.terraform/*" -not -path "*/node_modules/*" -print0 2>/dev/null \
    | while IFS= read -r -d '' DOCKERFILE; do
        hadolint "$DOCKERFILE" --format json >> "$REPORT_DIR/hadolint-${DATE}.json" 2>/dev/null
      done
fi
```

If no scanner is available → proceed with manual review only, and set the report's
"Scanners Used" field to `manual only`.

For each finding extract: check ID, resource, file:line, severity, description, guideline/benchmark.

---

## Step 3 — Manual Review

Read `references/check-catalog.md` for the full check list per IaC type. Key areas:

### 3a. Identity & Access
- Overly permissive IAM policies (`*` actions/resources)
- Missing least-privilege boundaries
- Service accounts with admin roles
- Missing MFA enforcement for human users
- Long-lived credentials vs. short-lived tokens

### 3b. Network Exposure
- Security groups/firewalls open to `0.0.0.0/0` on sensitive ports
- Missing VPC/network segmentation
- Public endpoints without WAF/DDoS protection
- Missing egress controls

### 3c. Encryption
- Unencrypted storage (S3, EBS, RDS, disks)
- Missing TLS on load balancers or API gateways
- Customer-managed keys vs. provider-managed
- Missing encryption in transit between services

### 3d. Logging & Monitoring
- CloudTrail/audit logging disabled
- Missing log retention policies
- No alerting on security events
- Flow logs disabled on VPCs/subnets

### 3e. Container Security (Docker/K8s)
- Running as root / missing `USER` directive
- Privileged containers or elevated capabilities
- Missing resource limits (CPU/memory)
- `latest` tag instead of pinned digest
- Writable root filesystem
- Missing network policies
- Secrets in environment variables vs. secret stores

### 3f. State & Secrets
- Terraform state stored unencrypted or in local file
- Secrets in `.tfvars`, environment variables, or plaintext
- Missing state locking
- Remote backend without encryption

---

## Step 4 — Severity Scoring

Use the same Likelihood × Impact matrix as other security skills:

| | Impact: Low | Impact: Medium | Impact: High |
|---|---|---|---|
| **Likelihood: High** | Medium | High | Critical |
| **Likelihood: Medium** | Low | Medium | High |
| **Likelihood: Low** | Info | Low | Medium |

**IaC-specific likelihood factors:** Is the resource internet-facing? Is it in production?
Does it handle sensitive data? Is the misconfiguration exploitable without additional access?

**Finding tags** (set the report's `Tag` field from severity):
- `[BLOCK]` — Critical / High, must-fix before merge/deploy
- `[WARN]` — Medium, should-fix
- `[INFO]` — Low / Info, defense-in-depth

Map findings to CIS benchmarks where applicable (CIS AWS, CIS GCP, CIS Azure, CIS Kubernetes, CIS Docker).

---

### False Positive Classification

A finding is FP if:
1. **Intentionally public** — resource is designed to be public (e.g., ALB, CDN origin)
2. **Provider default secure** — check does not apply because provider defaults are already secure for this version
3. **Higher-level override** — security is enforced by a parent module, SCP, or organization policy

Always document rationale: `FP — ALB is intentionally internet-facing per design doc section 4.2`

### CIS Benchmark Versions

| Provider | Benchmark | Version |
|----------|-----------|--------|
| AWS | CIS Amazon Web Services Foundations | v3.0 |
| Azure | CIS Microsoft Azure Foundations | v2.1 |
| GCP | CIS Google Cloud Platform Foundation | v2.0 |
| Kubernetes | CIS Kubernetes Benchmark | v1.8 |
| Docker | CIS Docker Benchmark | v1.6 |

## Step 5 — Correlate, Deduplicate & Map Coverage

- Merge automated + manual findings — no duplicates
- Classify each automated finding as TP or FP with context
- Note scanner coverage gaps (e.g. logic-level misconfigs that no scanner catches)
- **CIS Benchmark Coverage:** for the provider(s) in scope, tally per-section
  Checks Applicable / Pass / Fail / N-A for the report's CIS Benchmark Coverage table.
  Derive Pass/Fail counts from checkov/trivy output where the scanner reports per-check
  results; where no scanner number is available, mark the cell `—` (best-effort, do not fabricate).
- **Compliance Mapping:** map each finding to the controls in the report's Compliance Mapping
  table (ISO 27001:2022 A.8.8 — Technical Vulnerabilities, NIS2 Art. 21(2)(e), SOC 2 CC6.6).
  Leave a control row `—` if no finding maps to it.

---

## Step 6 — Generate Report

Read `references/report-template.md` and write to:
`$REPORT_DIR/iac-security-report-${DATE}.md`

Document ID: `IAC-YYYYMMDD-001`

```bash
ls -lh "$REPORT_DIR/"
echo "Report: $REPORT_DIR/iac-security-report-${DATE}.md"
```

Print `[BLOCK]` findings to terminal immediately.

---

## Principles

1. **Default-deny thinking** — every open port, permissive policy, or missing encryption is a finding until justified
2. **CIS benchmarks are the baseline** — map findings where applicable
3. **Blast radius matters** — a misconfigured production VPC is Critical; a dev sandbox is Medium
4. **State file security is paramount** — unencrypted state with secrets = Critical
5. **Scanner FPs are common in IaC** — validate every automated finding against actual resource context
6. **Module/template reuse amplifies risk** — a flaw in a shared module affects every instantiation
7. **IaC drift is out of scope** — this skill reviews definitions, not runtime state
