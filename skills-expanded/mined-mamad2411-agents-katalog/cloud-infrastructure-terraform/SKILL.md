---
name: cloud-infrastructure-terraform
description: "Cloud Infrastructure Terraform."
domain: cybersecurity
---

|
| Infrastructure as Code | Practice of managing cloud infrastructure through declarative configuration files (Terraform, CloudFormation) rather than manual console operations |
| Policy as Code | Expressing security and compliance policies as executable code (Rego, Python) that can be automatically evaluated against infrastructure definitions |
| Shift Left Security | Moving security checks earlier in the development lifecycle by scanning IaC before deployment rather than auditing after provisioning |
| Terraform Plan | Preview of changes Terraform will make, which can be exported as JSON for security scanning before applying changes |
| Checkov | Open-source static analysis tool for IaC supporting Terraform, CloudFormation, Kubernetes, and Docker with 1000+ built-in policies |
| OPA/Rego | Open Policy Agent and its policy language Rego for defining custom security rules that evaluate against structured data inputs |

## Tools & Systems

- **Checkov**: Comprehensive IaC scanner with 1000+ policies for Terraform, CloudFormation, Kubernetes, ARM, and Dockerfile
- **tfsec**: Terraform-specific static analysis tool with detailed remediation guidance and SARIF output
- **Terrascan**: Multi-IaC scanner supporting compliance frameworks (CIS, NIST, SOC 2) with policy-as-code
- **OPA/Conftest**: Custom policy engine for defining organization-specific security rules using Rego language
- **Bridgecrew**: Commercial platform built on Checkov providing drift detection and supply chain security

## Common Scenarios

### Scenario: Adding Security Gates to an Existing Terraform CI/CD Pipeline

**Context**: A DevOps team deploys infrastructure via Terraform in GitHub Actions but has no security scanning. Recent audit findings show multiple S3 buckets without encryption and security groups allowing SSH from the internet.

**Approach**:
1. Add Checkov as the first security gate in the GitHub Actions workflow
2. Run `checkov -d ./terraform/` to establish the current baseline of findings
3. Triage existing findings: fix CRITICAL issues, create tickets for HIGH, suppress accepted risks
4. Add tfsec as a secondary scanner for Terraform-specific checks
5. Write custom OPA policies for organization standards (required tags, naming conventions)
6. Configure the pipeline to block PRs with CRITICAL or HIGH findings
7. Generate SARIF reports for GitHub Security tab integration

**Pitfalls**: Adding security scanning to an existing project will initially produce hundreds of findings. Implement gradually by starting with CRITICAL-only blocking, then expanding to HIGH. Use inline suppression comments (`#checkov:skip=CKV_AWS_18:Public bucket for static website`) for intentional exceptions with documented justification.

## Output Format

```
Terraform Security Audit Report
==================================
Repository: acme-corp/infrastructure
Branch: main
Scan Date: 2026-02-23
Tools: Checkov 3.x, tfsec 1.x, OPA custom policies

SCAN RESULTS:
  Checkov checks passed:    187
  Checkov checks failed:     34
  tfsec checks passed:      156
  tfsec checks failed:       28
  OPA custom policies:       12 passed, 3 failed

CRITICAL FINDINGS:
[TF-001] S3 Bucket Without Encryption
  File: modules/storage/main.tf:24
  Resource: aws_s3_bucket.data_lake
  Check: CKV_AWS_19
  Fix: Add server_side_encryption_configuration block

[TF-002] Security Group Allows SSH from 0.0.0.0/0
  File: modules/network/security.tf:45
  Resource: aws_security_group_rule.ssh_access
  Check: CKV_AWS_24
  Fix: Restrict cidr_blocks to bastion subnet

[TF-003] IAM Policy with Wildcard Actions
  File: modules/iam/policies.tf:12
  Resource: aws_iam_policy.developer_policy
  Check: CKV_AWS_1
  Fix: Scope actions to specific services required

SUMMARY BY SEVERITY:
  Critical:  6 findings
  High:     14 findings
  Medium:   28 findings
  Low:      18 findings
  Info:     12 findings
```
