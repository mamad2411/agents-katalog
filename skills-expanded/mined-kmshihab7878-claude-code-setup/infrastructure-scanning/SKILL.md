---
name: infrastructure-scanning
description: Security scanning for Docker images, Terraform, K8s manifests, and Python deps using Trivy, Checkov, and Semgrep on AWS infrastructure
triggers:
  - infrastructure scan
  - security scan
  - trivy
  - checkov
  - vulnerability scan
  - iac security
---

# Infrastructure Scanning

Comprehensive security scanning for containerized Python services on AWS. Combines Trivy (vulnerabilities), Checkov (IaC misconfigurations), and Semgrep (code patterns).

## Quick Commands

```bash
# Full infrastructure scan
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL .

# Docker image scan
trivy image --severity HIGH,CRITICAL coremind-fresh:latest

# Terraform scan
trivy config terraform/ --severity HIGH,CRITICAL
checkov -d terraform/ --framework terraform --check HIGH

# Kubernetes manifests
trivy config k8s/ --severity HIGH,CRITICAL
checkov -d k8s/ --framework kubernetes

# Python dependency audit
trivy fs --scanners vuln --severity HIGH,CRITICAL requirements.txt
pip-audit --strict --desc
```

## Trivy Configuration

```yaml
# .trivy.yaml
severity:
  - HIGH
  - CRITICAL
scanners:
  - vuln
  - secret
  - misconfig
ignorefile: .trivyignore
cache-dir: /tmp/trivy-cache
```

## Checkov Configuration

```yaml
# .checkov.yaml
framework:
  - terraform
  - kubernetes
  - dockerfile
soft-fail: false
skip-check:
  - CKV_AWS_18  # S3 access logging (dev environments)
  - CKV_AWS_145 # RDS encryption (handled separately)
```

## CI Integration

```yaml
# In GitHub Actions
- name: Trivy vulnerability scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: fs
    severity: HIGH,CRITICAL
    exit-code: 1

- name: Checkov IaC scan
  uses: bridgecrewio/checkov-action@master
  with:
    directory: terraform/
    soft_fail: false
```

## AWS-Specific Checks

Priority checks for AWS infrastructure:
- S3 bucket policies (public access, encryption)
- IAM policies (overly permissive, wildcard actions)
- Security groups (open ports, 0.0.0.0/0)
- RDS (encryption at rest, public accessibility)
- EKS (public endpoint, logging, secrets encryption)
- Lambda (VPC config, IAM role scope)

## Remediation Workflow

1. Run scan: `just security` or `trivy fs .`
2. Review findings grouped by severity
3. Fix CRITICAL first, then HIGH
4. Re-scan to verify fixes
5. Add false positives to `.trivyignore` with justification comment
6. Commit fixes with `fix(security): remediate [CVE-ID]`
