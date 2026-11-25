---
name: scoutsuite
description: >
  Build, extend, and operate ScoutSuite — a multi-cloud security auditing tool by NCC Group.
  Use when performing cloud security assessments against AWS, Azure, GCP, Alibaba Cloud, or OCI.
  Use when the user asks about cloud misconfigurations, CIS benchmark checks, IAM analysis,
  or generating HTML security reports. Covers installation, provider authentication, scanning,
  rule engine, custom rules, findings triage, CI/CD integration, and cloud assessment workflow.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/nccgroup/ScoutSuite
  stars: '6.8k'
---

# scoutsuite Agent Skill

## When to Use This Skill

Use this skill when:
- Running a cloud security assessment against AWS, Azure, GCP, OCI, or Alibaba Cloud
- The user wants to enumerate misconfigurations, over-permissive IAM, or public exposure
- Generating an HTML or JSON security report for a cloud environment
- Writing or customizing ScoutSuite rules for specific compliance requirements
- Integrating cloud scanning into a CI/CD security gate
- Triaging ScoutSuite findings (danger/warning/info) and building remediation plans

## What ScoutSuite Does

ScoutSuite is a multi-cloud security auditing tool that collects configuration data from cloud provider APIs and evaluates it against a built-in rule engine. It produces an interactive HTML report categorizing findings into danger, warning, and informational levels across all major services. Unlike Prowler or CloudSploit, ScoutSuite maintains its own offline graph of all collected resources, enabling cross-service correlation without repeated API calls.

## Installation

```bash
# Recommended: virtualenv
python3 -m venv scoutsuite-env
source scoutsuite-env/bin/activate

# Install from PyPI
pip install scoutsuite

# Or install from source (latest)
git clone https://github.com/nccgroup/ScoutSuite.git
cd ScoutSuite
pip install -r requirements.txt
pip install .

# Verify
scout --version
```

### Cloud Provider SDK Dependencies

```bash
# AWS
pip install boto3

# Azure
pip install msrestazure azure-mgmt-*  # pulled automatically with scoutsuite

# GCP
pip install google-auth google-cloud-*  # pulled automatically

# All providers in one shot (already included via requirements.txt)
pip install scoutsuite[all]
```

## Supported Providers

| Provider    | Flag         | Notes                                     |
|-------------|--------------|-------------------------------------------|
| AWS         | `aws`        | IAM, EC2, S3, RDS, Lambda, CloudTrail, etc. |
| Azure       | `azure`      | Subscriptions, AAD, Storage, VMs, NSGs    |
| GCP         | `gcp`        | Projects, GCS, GCE, IAM, Cloud SQL        |
| Alibaba     | `aliyun`     | ECS, OSS, RAM, RDS                        |
| OCI         | `oci`        | Compute, Object Storage, IAM, VCN         |

## Authentication Methods

### AWS Authentication

```bash
# Named profile (recommended)
scout aws --profile prod-readonly

# Environment variables
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
scout aws

# Assume a role
scout aws --profile base-profile --role-arn arn:aws:iam::123456789:role/AuditRole

# MFA-protected
scout aws --profile mfa-profile --mfa-serial arn:aws:iam::123456789:mfa/user --mfa-code 123456

# All regions (default is all enabled regions)
scout aws --profile prod --all-regions

# Specific regions only
scout aws --profile prod --regions us-east-1 us-west-2
```

**Minimum AWS IAM permissions for read-only scan:**
Attach `SecurityAudit` managed policy plus `ReadOnlyAccess` for full coverage. For a minimal custom policy, ScoutSuite needs `Get*`, `List*`, `Describe*` across all services being scanned.

### Azure Authentication

```bash
# Interactive browser login (default)
scout azure --cli

# Service principal
scout azure --service-principal \
  --tenant-id <tenant-id> \
  --subscription-id <sub-id> \
  --client-id <app-id> \
  --client-secret <secret>

# Managed identity (from Azure VM)
scout azure --msi

# Specific subscription
scout azure --cli --subscription-id <sub-id>
```

### GCP Authentication

```bash
# Application Default Credentials (gcloud auth application-default login)
scout gcp --user-account --project-id my-project

# Service account key file
scout gcp --service-account --key-file /path/to/sa-key.json --project-id my-project

# All projects accessible to the account
scout gcp --user-account --all-projects

# Specific folder
scout gcp --user-account --folder-id 123456789
```

### OCI Authentication

```bash
# Uses ~/.oci/config automatically
scout oci --tenancy-id ocid1.tenancy.oc1..xxx

# Specific profile from config
scout oci --profile AUDIT
```

## Core Scanning Workflow

```bash
# Basic AWS scan — outputs to ./scoutsuite-report/
scout aws --profile prod

# Specify output directory
scout aws --profile prod --report-dir /tmp/scout-prod-$(date +%Y%m%d)

# Run only specific services
scout aws --profile prod --services ec2 iam s3 rds

# Skip specific services
scout aws --profile prod --exceptions-file exceptions.json

# Force overwrite existing report
scout aws --profile prod --force

# Parallelism (default 10 threads)
scout aws --profile prod --max-workers 20

# Full multi-cloud example
scout gcp --service-account --key-file sa.json --project-id myproject --report-dir ./gcp-audit
```

## Understanding Findings

### Severity Levels

| Level   | Color  | Meaning                                             |
|---------|--------|-----------------------------------------------------|
| danger  | Red    | Critical misconfiguration — direct security risk    |
| warning | Orange | Elevated risk — deviates from best practice         |
| info    | Blue   | Informational — no immediate risk, useful context   |

### Navigating the HTML Report

1. Open `scoutsuite-report/scoutsuite_results_aws-<profile>.html` in a browser
2. Left sidebar: services (IAM, EC2, S3, RDS, Lambda, CloudTrail, KMS…)
3. Click a service → see rule violations with counts
4. Click a rule → see all affected resources with raw JSON evidence
5. Filter by severity using the top toggles
6. Export finding data via the JSON file: `scoutsuite-report/scoutsuite_results_aws-<profile>.js`

### Programmatic Access to Results

```python
import json, re

# Strip the JS wrapper to get raw JSON
with open('scoutsuite-report/scoutsuite_results_aws-prod.js') as f:
    raw = f.read()
data = json.loads(re.sub(r'^scoutsuite_results\s*=\s*', '', raw).rstrip(';'))

# Enumerate danger-level findings
for svc, svc_data in data['services'].items():
    for rule_id, rule in svc_data.get('findings', {}).items():
        if rule.get('level') == 'danger' and rule.get('flagged_items', 0) > 0:
            print(f"[DANGER] {svc}/{rule_id}: {rule['flagged_items']} items")
```

## Rule Engine

### Rule File Structure

Rules live in `ScoutSuite/providers/<provider>/rules/ruleset-default.json` and individual JSON files under `rules/findings/`.

```json
{
  "description": "Root account used recently",
  "rationale": "Root account usage indicates shared credentials or privilege abuse.",
  "remediation": "Disable root access keys; enable MFA.",
  "compliance": [{"name": "CIS AWS", "version": "1.4", "reference": "1.7"}],
  "references": ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-account.html"],
  "dashboard_name": "Root account used recently",
  "display_path": "iam.root.LastUsedDate",
  "path": "iam.root.LastUsedDate",
  "conditions": ["and", ["iam.root.LastUsedDate", "withinlastdays", "1"]],
  "id": "root-account-used-recently",
  "level": "danger"
}
```

### Custom Rule Creation

```bash
# Create a custom ruleset directory
mkdir -p ~/.scoutsuite/rules/findings

# Write a custom rule: detect S3 buckets without versioning
cat > ~/.scoutsuite/rules/findings/s3-versioning-disabled.json << 'EOF'
{
  "description": "S3 bucket versioning disabled",
  "rationale": "Versioning protects against accidental deletion and ransomware.",
  "remediation": "Enable versioning on all S3 buckets.",
  "path": "s3.buckets.id",
  "conditions": ["and",
    ["s3.buckets.id.Versioning", "notEqual", "Enabled"]
  ],
  "id": "s3-versioning-disabled",
  "level": "warning"
}
EOF

# Use custom ruleset
scout aws --profile prod --ruleset ~/.scoutsuite/rules/ruleset-custom.json
```

### Ruleset Configuration

```json
{
  "name": "Custom Ruleset",
  "about": "Org-specific security rules",
  "rules": {
    "s3-versioning-disabled": {"enabled": true, "level": "danger"},
    "root-account-no-mfa": {"enabled": true, "level": "danger"},
    "ec2-security-group-open-to-all": {"enabled": true, "level": "danger"},
    "cloudtrail-not-enabled": {"enabled": false}
  }
}
```

## Filtering and Exceptions

```bash
# Exclude specific resources from findings (not from collection)
# exceptions.json:
{
  "ec2": {
    "security_groups": ["sg-xxxxxx", "sg-yyyyyy"]
  },
  "s3": {
    "buckets": ["my-public-website-bucket"]
  }
}

scout aws --profile prod --exceptions-file exceptions.json
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Cloud Security Scan
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6AM
  workflow_dispatch:

jobs:
  scoutsuite:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/ScoutSuiteAuditRole
          aws-region: us-east-1

      - name: Install ScoutSuite
        run: pip install scoutsuite

      - name: Run ScoutSuite
        run: scout aws --report-dir ./report --force

      - name: Check for danger findings
        run: |
          python3 - << 'EOF'
          import json, re, sys
          with open('./report/scoutsuite_results_aws-default.js') as f:
              data = json.loads(re.sub(r'^scoutsuite_results\s*=\s*', '', f.read()).rstrip(';'))
          dangers = sum(
              rule.get('flagged_items', 0)
              for svc in data['services'].values()
              for rule in svc.get('findings', {}).values()
              if rule.get('level') == 'danger'
          )
          print(f"Danger findings: {dangers}")
          sys.exit(1 if dangers > 0 else 0)
          EOF

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: scoutsuite-report
          path: ./report/
```

## Common Workflows

### External Cloud Pentest Assessment

```bash
# 1. Auth check
aws sts get-caller-identity --profile client-audit

# 2. Full scan with timestamped output
REPORT_DIR="./scoutsuite-$(date +%Y%m%d)"
scout aws --profile client-audit --report-dir "$REPORT_DIR" --all-regions

# 3. Extract critical findings for report
python3 extract_dangers.py "$REPORT_DIR"/scoutsuite_results_aws-*.js

# 4. Manually verify top findings in console or CLI
aws iam get-account-password-policy --profile client-audit
aws s3api get-bucket-acl --bucket <bucket-name> --profile client-audit

# 5. Screenshot key report sections for deliverable
```

### Assumed Role / Cross-Account Scan

```bash
# Assume audit role in target account
aws sts assume-role \
  --role-arn arn:aws:iam::TARGET_ACCOUNT:role/AuditRole \
  --role-session-name scoutsuite-session \
  --profile source-account \
  | jq -r '.Credentials | "export AWS_ACCESS_KEY_ID=\(.AccessKeyId)\nexport AWS_SECRET_ACCESS_KEY=\(.SecretAccessKey)\nexport AWS_SESSION_TOKEN=\(.SessionToken)"' \
  > assume_role.sh
source assume_role.sh
scout aws --report-dir ./target-account-audit
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `NoCredentialsError` | Check `~/.aws/credentials` or env vars; verify `aws sts get-caller-identity` |
| Rate limiting / throttling | Add `--max-workers 5`; scan fewer services with `--services` |
| `AccessDenied` for specific service | Add missing `List*`/`Describe*` permissions or skip service |
| HTML report blank in browser | Serve via `python3 -m http.server 8080` — browser security blocks local JS |
| `ModuleNotFoundError` | Activate virtualenv; run `pip install scoutsuite` again |
| Azure auth loop | Use `az login` first, then `scout azure --cli` |
| GCP `permission denied` | Ensure SA has `Security Reviewer` + `Viewer` roles at project/org level |
| Stale results | Delete report dir and rerun with `--force` |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Azure AD Conditional Access Policies Most Companies Get Wrong](https://redhound.us/azure-ad-conditional-access)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
