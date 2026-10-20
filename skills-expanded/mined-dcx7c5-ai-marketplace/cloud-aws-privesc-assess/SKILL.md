---
name: cloud-aws-privesc-assess
description: "Cloud Aws Privesc Assess."
domain: cybersecurity
---

|
| IAM Privilege Escalation | Exploiting overly permissive IAM policies to gain higher-level access than originally granted to a principal |
| Permission Boundary | IAM policy that sets the maximum permissions a principal can have, regardless of identity-based policies attached to it |
| iam:PassRole | IAM action allowing a principal to pass an IAM role to an AWS service, enabling the service to act with that role's permissions |
| Confused Deputy | Attack where an attacker tricks a trusted service into performing actions on their behalf using cross-account role assumption without external ID validation |
| Service Control Policy | AWS Organizations policy that sets maximum permissions for member accounts, providing guardrails against privilege escalation |
| Principal Mapper | Open-source tool that models IAM principals and their escalation paths as a directed graph for analysis |

## Tools & Systems

- **Pacu**: AWS exploitation framework with 21+ privilege escalation modules for automated detection and exploitation
- **Principal Mapper**: Graph-based IAM analysis tool that maps escalation paths between principals
- **CloudFox**: AWS enumeration tool focused on identifying attack paths from an attacker's perspective
- **IAM Policy Simulator**: AWS-native tool for testing effective permissions against specific API actions
- **AWS Access Analyzer**: Service that identifies resource policies granting external access and validates IAM policy changes

## Common Scenarios

### Scenario: Developer Role with iam:CreatePolicyVersion Leads to Admin Access

**Context**: During an authorized assessment, a tester discovers that a developer role has the `iam:CreatePolicyVersion` permission, which allows creating a new version of any customer-managed policy with arbitrary permissions.

**Approach**:
1. Enumerate policies attached to the developer role using `iam__enum_permissions` in Pacu
2. Identify that the role can call `iam:CreatePolicyVersion` on its own attached policy
3. Create a new policy version with `"Action": "*", "Resource": "*", "Effect": "Allow"`
4. Set the new version as the default policy version
5. Verify admin access by calling `iam:ListUsers`, `s3:ListBuckets`, etc.
6. Document the escalation chain and recommend removing `iam:CreatePolicyVersion` and implementing permission boundaries

**Pitfalls**: AWS limits managed policies to 5 versions. If all 5 exist, you must delete a version before creating a new one. Always record the original default version to restore it during cleanup. Permission boundaries prevent this escalation if properly configured, so verify boundary policies before declaring a finding.

## Output Format

```
AWS Privilege Escalation Assessment Report
=============================================
Account: 123456789012 (Production)
Assessment Date: 2026-02-23
Starting Principal: arn:aws:iam::123456789012:user/test-user
Starting Permissions: S3 read-only, Lambda invoke, EC2 describe
Authorization: Signed by CISO, engagement #PT-2026-014

ESCALATION PATHS DISCOVERED: 4

[PRIVESC-001] iam:CreatePolicyVersion -> Admin
  Severity: CRITICAL
  Starting Permission: iam:CreatePolicyVersion on policy/dev-policy
  Escalation: Created policy version 6 with Action:* Resource:*
  Time to Exploit: < 2 minutes
  Remediation: Remove iam:CreatePolicyVersion, apply permission boundary

[PRIVESC-002] iam:PassRole + lambda:CreateFunction -> LambdaAdminRole
  Severity: CRITICAL
  Starting Permission: iam:PassRole, lambda:CreateFunction
  Escalation: Created Lambda function with AdminRole, invoked to get admin credentials
  Time to Exploit: < 5 minutes
  Remediation: Restrict iam:PassRole to specific role ARNs with condition key

[PRIVESC-003] sts:AssumeRole -> Cross-Account Admin
  Severity: HIGH
  Starting Permission: sts:AssumeRole on arn:aws:iam::987654321098:role/SharedRole
  Escalation: Role trust policy allows any principal in source account
  Remediation: Add sts:ExternalId condition and restrict Principal to specific roles

TOTAL ESCALATION PATHS: 4 (2 Critical, 1 High, 1 Medium)
PERMISSION BOUNDARIES IN PLACE: 0 / 47 IAM principals
SCP GUARDRAILS BLOCKING ESCALATION: 0 / 3 tested vectors
```
