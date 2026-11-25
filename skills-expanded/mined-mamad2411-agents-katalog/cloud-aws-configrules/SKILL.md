---
name: cloud-aws-configrules
description: "Cloud Aws Configrules."
domain: cybersecurity
---

|
| AWS Config Rule | A compliance check that evaluates whether AWS resource configurations meet specified requirements, either continuously or on a schedule |
| Managed Rule | AWS-provided pre-built Config rule with standardized logic for common compliance checks like encryption and public access |
| Custom Rule | Organization-specific Config rule backed by a Lambda function that evaluates custom compliance logic |
| Remediation Action | SSM Automation document or Lambda function triggered to automatically fix non-compliant resources |
| Configuration Aggregator | AWS Config feature that collects compliance data from multiple accounts and regions into a centralized view |
| Conformance Pack | Collection of Config rules and remediation actions packaged as a deployable unit for specific compliance frameworks |

## Tools & Systems

- **AWS Config**: Continuous configuration recording and compliance evaluation service for AWS resources
- **SSM Automation**: AWS Systems Manager documents for executing automated remediation actions on non-compliant resources
- **Config Conformance Packs**: Pre-built rule collections for CIS, PCI DSS, NIST 800-53, and HIPAA compliance
- **CloudFormation StackSets**: Multi-account deployment mechanism for Config rules across AWS Organizations
- **Config Aggregator**: Cross-account and cross-region compliance data consolidation

## Common Scenarios

### Scenario: Deploying CIS Compliance Monitoring Across 30 AWS Accounts

**Context**: A financial services company needs to demonstrate continuous CIS AWS Foundations Benchmark compliance across all 30 production accounts for their annual SOC 2 audit.

**Approach**:
1. Enable AWS Config recording in all accounts via CloudFormation StackSets
2. Deploy the CIS conformance pack to all accounts using StackSets
3. Set up a Config aggregator in the security account for organization-wide visibility
4. Configure auto-remediation for safe-to-fix rules (public S3, unencrypted volumes)
5. Create EventBridge rules to alert on new NON_COMPLIANT evaluations
6. Build a weekly compliance report aggregating scores across all accounts
7. Store Config snapshots in S3 with lifecycle policies for audit retention

**Pitfalls**: Config recording incurs costs per configuration item recorded. In accounts with many resources, costs can be significant. Use targeted recording groups to focus on compliance-relevant resource types rather than recording all resources. Auto-remediation of network rules (security groups) can disrupt applications if the rule was intentionally permissive.

## Output Format

```
AWS Config Compliance Report
===============================
Organization: Acme Financial (30 accounts)
Framework: CIS AWS Foundations 1.4
Report Date: 2026-02-23
Config Rules Active: 48

COMPLIANCE SUMMARY:
  Overall Compliance: 87%
  Compliant Resources:     4,234
  Non-Compliant Resources:   612
  Not Applicable:            189

TOP NON-COMPLIANT RULES:
  encrypted-volumes:              89 resources (14 accounts)
  vpc-flow-logs-enabled:          67 resources (12 accounts)
  mfa-enabled-for-iam-console:    45 resources (8 accounts)
  s3-bucket-ssl-requests-only:    34 resources (6 accounts)
  restricted-ssh:                 28 resources (5 accounts)

AUTO-REMEDIATION (Last 30 Days):
  Public S3 buckets remediated:    12
  Security groups restricted:       8
  EBS default encryption enabled:   6
  Total auto-remediated:           26
  Failed remediation attempts:      3

ACCOUNT COMPLIANCE RANKING:
  1. prod-core (account-001):     96% compliant
  2. prod-data (account-002):     94% compliant
  ...
  30. dev-sandbox (account-030):  68% compliant
```
