---
name: cloud-devsecops-iacscan
description: "Cloud Devsecops Iacscan."
domain: cybersecurity
---

|
| IaC Scanning | Automated analysis of infrastructure code templates to detect security misconfigurations before deployment |
| Policy as Code | Security policies defined as executable code that can be version-controlled, tested, and enforced automatically |
| CKV Check ID | Checkov's unique identifier for each security check (e.g., CKV_AWS_18 for S3 public access) |
| Terraform Plan Scanning | Scanning the resolved Terraform plan JSON which includes computed values and module expansions |
| Graph-based Scanning | Checkov's ability to analyze relationships between resources, not just individual resource configs |
| Drift Detection | Identifying differences between IaC definitions and actual deployed infrastructure state |
| Custom Policy | Organization-specific security checks authored in Python or YAML to enforce internal standards |

## Tools & Systems

- **Checkov**: Open-source IaC scanner by Bridgecrew with 2500+ built-in policies covering major cloud providers
- **tfsec**: Terraform-focused static analysis tool by Aqua Security with deep HCL understanding
- **KICS**: Open-source IaC scanner by Checkmarx supporting 15+ IaC frameworks
- **Terrascan**: IaC scanner with OPA Rego policy support for custom policy authoring
- **Snyk IaC**: Commercial IaC scanner integrated with the Snyk platform

## Common Scenarios

### Scenario: Preventing Public S3 Buckets in Terraform

**Context**: A development team repeatedly creates S3 buckets without proper access controls. A recent incident exposed customer data through a public bucket.

**Approach**:
1. Enable Checkov in the CI/CD pipeline for all Terraform changes
2. Enforce CKV_AWS_18 (no public read ACL), CKV_AWS_19 (encryption), CKV_AWS_20 (no public access block disabled)
3. Create a custom policy requiring the `aws_s3_bucket_public_access_block` resource for every S3 bucket
4. Set `soft_fail: false` to block PR merges when S3 security checks fail
5. Provide Terraform modules with security defaults that teams can reuse

**Pitfalls**: Scanning only `.tf` files misses dynamically computed values. Use Terraform plan scanning for higher accuracy. Checkov's resource-relationship checks (CKV2 prefix) require graph analysis mode.

## Output Format

```
IaC Security Scan Report
==========================
Framework: Terraform
Directory: terraform/
Scan Date: 2026-02-23

Checkov Results:
  Passed: 187
  Failed: 12
  Skipped: 3
  Unknown: 0

FAILED CHECKS:
  CKV_AWS_18  [HIGH]   S3 Bucket has public read ACL
              Resource: aws_s3_bucket.data_lake
              File:     terraform/storage.tf:15-28

  CKV_AWS_24  [HIGH]   CloudWatch log group not encrypted
              Resource: aws_cloudwatch_log_group.app
              File:     terraform/monitoring.tf:3-8

  CKV_AWS_79  [MEDIUM] Instance metadata service v1 enabled
              Resource: aws_instance.web
              File:     terraform/compute.tf:12-30

QUALITY GATE: FAILED (2 HIGH severity findings)
```
