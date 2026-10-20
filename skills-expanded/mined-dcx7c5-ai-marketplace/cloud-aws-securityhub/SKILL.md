---
name: cloud-aws-securityhub
description: "Cloud Aws Securityhub."
domain: cybersecurity
---

|
| Security Standard | Pre-packaged set of controls mapped to compliance frameworks such as CIS, PCI-DSS, NIST 800-53, and AWS best practices |
| Security Control | Individual automated check that evaluates a specific AWS resource configuration against a security requirement |
| ASFF | AWS Security Finding Format, a standardized JSON schema for normalizing findings from all integrated security products |
| Compliance Score | Percentage of controls in a passing state within a given security standard, calculated per account and aggregated at the organization level |
| Finding Aggregator | Cross-region mechanism that consolidates findings from all enabled regions into a single administrator region |
| Custom Action | User-defined action that can be triggered from the Security Hub console to invoke EventBridge rules for manual or automated response |

## Tools & Systems

- **AWS Security Hub CSPM**: Core platform for automated security posture checks and finding aggregation
- **AWS Config**: Underlying configuration recorder that Security Hub relies on for resource evaluation
- **Amazon EventBridge**: Event routing service for connecting Security Hub findings to automated remediation workflows
- **AWS Systems Manager**: Automation documents that Security Hub can invoke for remediation of common misconfigurations
- **AWS Audit Manager**: Generates audit-ready reports using Security Hub findings as evidence

## Common Scenarios

### Scenario: Failed CIS Controls Across 50 Accounts

**Context**: An enterprise enables CIS AWS Foundations Benchmark v5.0 and discovers 340 failed controls across 50 accounts, primarily in IAM password policy, CloudTrail configuration, and VPC flow log enablement.

**Approach**:
1. Export all FAILED findings grouped by control ID to identify the most prevalent issues
2. Prioritize Critical and High severity controls that affect the most accounts
3. Create Systems Manager Automation documents for the top 10 recurring failures
4. Deploy automated remediation via EventBridge for controls like S3.1 (block public access) and CloudTrail.1 (enable multi-region trail)
5. Schedule weekly compliance score reviews and track improvement over a 90-day remediation window

**Pitfalls**: Enabling automated remediation for all controls at once can break production workloads that legitimately require public S3 access or specific network configurations. Always test remediation in a staging account first.

## Output Format

```
AWS Security Hub Compliance Report
====================================
Organization: acme-corp
Administrator Account: 111122223333
Report Date: 2025-02-23
Standards Enabled: CIS v5.0, AWS FSBP v1.0, PCI DSS v3.2.1

COMPLIANCE SCORES:
  CIS AWS Foundations Benchmark v5.0: 78%
  AWS Foundational Security Best Practices: 85%
  PCI DSS v3.2.1: 72%

TOP FAILED CONTROLS (by account count):
  [S3.1]   Block public access settings enabled      - 23/50 accounts FAILED
  [CT.1]   CloudTrail multi-region enabled            - 12/50 accounts FAILED
  [IAM.4]  Root account has no access keys            -  3/50 accounts FAILED
  [EC2.19] Security groups restrict unrestricted ports- 31/50 accounts FAILED
  [RDS.3]  RDS encryption at rest enabled             - 18/50 accounts FAILED

FINDING SUMMARY:
  Total Active Findings: 1,247
  Critical: 34 | High: 189 | Medium: 567 | Low: 457
  Auto-Remediated This Month: 89
  Suppressed: 23
```
