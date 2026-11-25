---
name: aws-iam-least-privilege
description: Narrows AWS IAM policies to the actions and resources a workload really uses, based on code and access logs, with every change explained.
---

# AWS IAM least privilege

Reduce permissions to what is used, and prove it before removing anything.

## Steps

1. List the policies in scope: inline, managed and trust policies in IaC files (Terraform, CloudFormation, CDK) or exported JSON.
2. Establish usage from three sources: the AWS SDK calls in the code (`grep` for client and command names), CloudTrail or `aws iam generate-service-last-accessed-details`, and IAM Access Analyzer findings if present.
3. Rewrite each statement:
   - replace `Action: "*"` and `service:*` with the named actions in use
   - replace `Resource: "*"` with specific ARNs, using prefixes like `arn:aws:s3:::my-bucket/uploads/*` where names are dynamic
   - add `Condition` keys that pin region, `aws:PrincipalOrgID`, VPC endpoint, or tag where they fit
   - split read and write into separate statements
4. Check trust policies: a specific principal, an `ExternalId` for cross-account roles, no `Principal: "*"` without conditions.
5. Validate with `aws accessanalyzer validate-policy` and, where possible, `aws iam simulate-principal-policy` for the calls the code makes.

## Rules

- Never remove a permission you cannot show is unused. Put it under "unconfirmed".
- Never apply policy changes to a live account; edit the files and let the user deploy.
- Keep `iam:PassRole` and `sts:AssumeRole` scoped to exact role ARNs.

## Report

Per policy: before and after actions, resources narrowed, evidence used, and the unconfirmed list.
