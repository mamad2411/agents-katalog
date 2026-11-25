---
name: cloud-aws-lambda-aws
description: "Cloud Aws Lambda Aws."
domain: cybersecurity
---

|
| Execution Role | IAM role assumed by Lambda during function execution that defines all AWS API actions the function can perform |
| Least Privilege | Security principle of granting only the minimum permissions required for a function to perform its intended operations |
| Permission Boundary | IAM policy that sets the maximum permissions an execution role can have, even if identity policies grant broader access |
| IAM Access Analyzer | AWS service that generates least-privilege policies based on actual CloudTrail usage and validates policies for security issues |
| Resource-Scoped Policy | IAM policy that specifies exact resource ARNs rather than wildcards, limiting access to only the specific resources needed |
| Confused Deputy Prevention | Adding `aws:SourceAccount` or `aws:SourceArn` conditions to trust policies to prevent cross-account role assumption attacks |

## Tools & Systems

- **IAM Access Analyzer**: Generates least-privilege policies from CloudTrail data and validates policy security
- **IAM Policy Simulator**: Tests effective permissions for a role against specific API actions before deployment
- **CloudTrail**: Audit log of all API calls used to determine actual function permission usage
- **Prowler**: Security tool with Lambda-specific checks for role permissions and configuration
- **Checkov**: Infrastructure-as-code scanner that validates Lambda IAM policies in CloudFormation/Terraform

## Common Scenarios

### Scenario: Reducing a Lambda Function from AdministratorAccess to Least Privilege

**Context**: A security audit finds 12 Lambda functions using a shared execution role with `AdministratorAccess`. The team needs to scope each function to minimum required permissions without breaking production.

**Approach**:
1. Enable CloudTrail data events for Lambda to capture actual API usage per function
2. Wait 30 days to collect a representative sample of API calls
3. Use IAM Access Analyzer policy generation for each function's role usage
4. Create individual scoped policies for each function based on actual API usage
5. Apply permission boundaries to cap maximum permissions
6. Deploy scoped roles to staging and run integration tests
7. Roll out to production with canary deployment and rollback plan
8. Validate with IAM Policy Simulator before removing the old broad role

**Pitfalls**: Some Lambda functions may have infrequent code paths that only trigger monthly (batch jobs, error handlers). A 30-day observation window may miss rare API calls. Review the function code alongside CloudTrail data to identify all potential API calls. Use Access Analyzer's policy validation rather than relying solely on generated policies.

## Output Format

```
Lambda Execution Role Security Report
========================================
Account: 123456789012
Review Date: 2026-02-23
Functions Audited: 34

ROLE PERMISSION SUMMARY:
  Functions with AdministratorAccess:    3 (CRITICAL)
  Functions with PowerUserAccess:        5 (HIGH)
  Functions with wildcard actions:      12 (MEDIUM)
  Functions with scoped policies:       14 (OK)

REMEDIATION PROGRESS:
  [x] payment-processor: Scoped to DynamoDB + S3 + KMS (3 actions)
  [x] order-notification: Scoped to SNS + SES (2 actions)
  [ ] data-pipeline: Generating policy from 30-day CloudTrail data
  [ ] image-resizer: Awaiting staging validation

PERMISSION BOUNDARY STATUS:
  Functions with boundary applied:  14 / 34
  Functions without boundary:       20 / 34

POLICY VALIDATION RESULTS:
  Policies with security warnings:   4
  Policies with errors:              0
  Policies with suggestions:        12
```
