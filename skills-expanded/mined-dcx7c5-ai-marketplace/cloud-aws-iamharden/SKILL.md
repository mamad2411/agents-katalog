---
name: cloud-aws-iamharden
description: "Cloud Aws Iamharden."
domain: cybersecurity
---

|
| Least Privilege | Granting only the minimum permissions required for an identity to perform its function |
| Permission Boundary | An advanced IAM feature that sets the maximum permissions an entity can have, regardless of attached policies |
| IAM Access Analyzer | AWS service that uses automated reasoning to identify resources shared externally and generate least-privilege policies from CloudTrail activity |
| Service Control Policy (SCP) | Organization-level policy that sets permission guardrails across all accounts in an AWS Organization |
| Assume Role | STS operation that returns temporary security credentials for cross-account or service-to-service access |
| Credential Report | AWS-generated CSV listing all IAM users, their access keys, MFA status, and last activity timestamps |
| Policy Condition | Constraints in IAM policies that restrict when and how permissions apply, such as MFA requirements or IP ranges |
| Identity Federation | Allowing external identity providers to grant temporary AWS access without creating IAM users |

## Tools & Systems

- **AWS IAM Access Analyzer**: Generates least-privilege policies from CloudTrail activity and identifies resources shared with external entities
- **AWS Config**: Continuously evaluates IAM configuration compliance against managed and custom rules
- **AWS Security Hub**: Aggregates IAM security findings from Access Analyzer, Config, and third-party tools into a unified dashboard
- **IAM Policy Simulator**: Tests the effects of IAM policies before deployment by simulating API calls against policy evaluation logic
- **Prowler**: Open-source AWS security assessment tool that runs over 300 checks including IAM best practices and CIS benchmark controls

## Common Scenarios

### Scenario: Developer Role Over-Provisioned with AdministratorAccess

**Context**: A startup attached the AWS-managed AdministratorAccess policy to all developer roles for speed during early development. A security audit reveals 15 roles with full account access while developers only use S3, Lambda, and DynamoDB.

**Approach**:
1. Enable IAM Access Analyzer and generate policy recommendations based on 90 days of CloudTrail data for each role
2. Create scoped policies allowing only the specific S3 buckets, Lambda functions, and DynamoDB tables each team accesses
3. Attach a permission boundary denying IAM, Organizations, and billing actions
4. Deploy the new policies in a parallel role with CloudTrail monitoring before replacing the original
5. Remove AdministratorAccess and rotate all access keys

**Pitfalls**: Replacing policies without a parallel testing period causes service disruptions. Forgetting to scope Lambda:InvokeFunction to specific function ARNs leaves lateral movement paths open.

### Scenario: Rotating Compromised Access Keys Across Multiple Services

**Context**: An access key is found in a public GitHub repository. The key belongs to an IAM user with S3 and EC2 permissions across three AWS accounts.

**Approach**:
1. Immediately deactivate the compromised key using `aws iam update-access-key --status Inactive`
2. Review CloudTrail logs for all API calls made with the compromised key in the past 30 days
3. Create a new access key for the user and update all dependent services and CI/CD pipelines
4. Delete the compromised key after confirming all services use the new credentials
5. Migrate the workload to use IAM roles with STS temporary credentials to prevent future key exposure

**Pitfalls**: Deleting the key before deactivating it prevents forensic analysis of which services relied on it. Failing to check all three accounts for unauthorized activity leaves potential backdoors undetected.

## Output Format

```
IAM Security Assessment Report
==============================
Account ID: 123456789012
Assessment Date: 2025-02-23
Analyzer: IAM Access Analyzer + Prowler v4.3

CRITICAL FINDINGS:
[C-001] Root account has active access keys
  - Resource: arn:aws:iam::123456789012:root
  - Remediation: Delete root access keys, enable MFA on root
  - CIS Benchmark: 1.4 (Ensure no root account access key exists)

[C-002] IAM user 'deploy-bot' has AdministratorAccess with no MFA
  - Resource: arn:aws:iam::123456789012:user/deploy-bot
  - Last Activity: 2025-02-20
  - Remediation: Replace with IAM role, enforce MFA condition

HIGH FINDINGS:
[H-001] 3 IAM policies use wildcard Resource "*" with sensitive actions
  - Policies: DevPolicy, CIPolicy, LegacyAdminPolicy
  - Remediation: Scope resources to specific ARNs using Access Analyzer

[H-002] 7 access keys older than 90 days detected
  - Users: svc-backup, svc-monitoring, dev-alice, dev-bob, ...
  - Remediation: Rotate keys, migrate to role-based access

SUMMARY:
  Total Findings: 14
  Critical: 2 | High: 4 | Medium: 5 | Low: 3
  Compliance Score: 62% (CIS AWS Foundations Benchmark v3.0)
```
