---
name: cloud-aws-hubcompliance
description: "Cloud Aws Hubcompliance."
domain: cybersecurity
---

|
| Security Hub | AWS service that aggregates security findings from AWS services and third-party tools, evaluates compliance against standards, and provides a unified security dashboard |
| Security Standard | A predefined set of security controls (CIS, PCI DSS, NIST 800-53) that Security Hub evaluates against your AWS configuration |
| Security Control | An individual check within a standard that evaluates a specific AWS resource configuration, such as whether S3 buckets block public access |
| Finding | A security issue detected by Security Hub or an integrated service, formatted in AWS Security Finding Format (ASFF) |
| Insight | A custom or managed grouping of findings by a specific attribute, providing aggregated views for security analysis |
| ASFF | AWS Security Finding Format, the standardized JSON schema used by all Security Hub integrations for consistent finding representation |

## Tools & Systems

- **AWS Security Hub**: Central aggregation and compliance evaluation platform for security findings across AWS accounts
- **AWS Config**: Configuration recording service required by Security Hub for evaluating resource compliance
- **Amazon EventBridge**: Event bus for routing Security Hub findings to Lambda, SNS, or external remediation systems
- **AWS Lambda**: Serverless compute for automated remediation functions triggered by Security Hub findings
- **Prowler**: Open-source tool that can send findings to Security Hub via ASFF integration

## Common Scenarios

### Scenario: Rolling Out Security Hub Across a 50-Account Organization

**Context**: A security team needs to enable Security Hub with CIS and FSBP standards across all accounts in an AWS Organization, with centralized finding aggregation and automated alerting.

**Approach**:
1. Enable Security Hub in the management account and designate a security account as delegated admin
2. Configure auto-enable for all existing and new member accounts via `update-organization-configuration`
3. Create a cross-region finding aggregator to consolidate findings from all regions into the admin account
4. Enable CIS AWS Foundations 1.4 and AWS FSBP standards across all accounts
5. Create EventBridge rules to route CRITICAL findings to PagerDuty and all findings to Splunk
6. Build custom insights for the top organizational risks: public resources, missing encryption, unused credentials
7. Schedule weekly compliance reports to stakeholders using Lambda and SES

**Pitfalls**: Security Hub requires AWS Config to be enabled in every account and region. Failing to enable Config will result in controls showing as "No data" rather than PASSED or FAILED. Member accounts with Config disabled will silently produce incomplete compliance scores.

## Output Format

```
AWS Security Hub Compliance Report
=====================================
Organization: acme-corp (50 accounts)
Region: us-east-1 (aggregated from all regions)
Report Date: 2026-02-23
Standards Enabled: CIS 1.4, FSBP v1.0, PCI DSS 3.2.1

COMPLIANCE SCORES:
  CIS AWS Foundations 1.4:     78% (142/182 controls passing)
  AWS FSBP v1.0.0:             85% (198/233 controls passing)
  PCI DSS 3.2.1:               72% (89/124 controls passing)

CRITICAL FINDINGS: 23
HIGH FINDINGS: 87
MEDIUM FINDINGS: 245
LOW FINDINGS: 412

TOP FAILING CONTROLS:
  [IAM.6]  MFA not enabled for root account           12 accounts
  [S3.2]   S3 Block Public Access not enabled          8 accounts
  [EC2.19] Security groups allow unrestricted access   15 accounts
  [RDS.3]  RDS encryption at rest not enabled          6 accounts

AUTO-REMEDIATION ACTIONS (Last 30 Days):
  S3 Block Public Access enabled:    14
  Security Group rules restricted:    8
  CloudTrail logging re-enabled:      3
  Total auto-remediated findings:    25
```
