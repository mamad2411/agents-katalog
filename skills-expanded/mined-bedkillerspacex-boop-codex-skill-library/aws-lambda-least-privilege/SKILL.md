---
name: aws-lambda-least-privilege
description: >
  Least-privilege IAM for owned AWS Lambda functions: execution role design,
  resource-scoped permissions, environment/secrets access, invokers, and VPC
  execution roles. Use when locking down Lambda roles or reviewing over-privileged
  policies — not for escalating privileges in foreign accounts.
---

# AWS Lambda Least Privilege

## Scope And Authorization

- **In scope:** Lambda functions and their execution/invoke roles in authorized accounts.
- **Out of scope:** Modifying roles in accounts without permission.
- Execution roles are frequently over-permissioned (`*` on S3/DynamoDB) — prioritize review.
- Separate execution role (runtime) from invoker permissions (who can call the function).
- Pair with `aws-iam-least-privilege`, `aws-lambda-event-source-mapping`, `code-quality-standards`.

## When To Use

- Creating a new function role from scratch.
- Removing AdministratorAccess / PowerUser from Lambda roles.
- Scoping Secrets Manager, SSM, KMS, SQS, DynamoDB permissions to specific ARNs.
- Configuring resource-based policy for allowed invokers (API GW, S3, Account).
- VPC Lambdas needing ENI permissions (modern AWS managed or explicit).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Event source mapping tuning | `aws-lambda-event-source-mapping` |
| SnapStart | `aws-lambda-snapstart` |
| General IAM simulation | `aws-iam-policy-simulator` |
| KMS key policies | `aws-kms-key-policy-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Permission class | Examples |
| --- | --- |
| Logging | `logs:CreateLogStream`, `PutLogEvents` on function log group |
| Data plane | specific table/queue/bucket ARNs |
| Secrets | `GetSecretValue` on one secret ARN + KMS decrypt |
| Network | VPC access managed policy or ENI actions as required |
| Invoke | resource policy / `lambda:InvokeFunction` for callers |

## Baseline Execution Role Skeleton

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Logs",
      "Effect": "Allow",
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:REGION:ACCT:log-group:/aws/lambda/order-fn:*"
    },
    {
      "Sid": "DDB",
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:UpdateItem"],
      "Resource": "arn:aws:dynamodb:REGION:ACCT:table/orders"
    },
    {
      "Sid": "Secret",
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue"],
      "Resource": "arn:aws:secretsmanager:REGION:ACCT:secret:order-db-*"
    }
  ]
}
```

Add KMS decrypt only for the CMK protecting that secret.

## Workflow

### 1. Confirm scope and success criteria

1. Record function name, triggers, data stores, secrets, VPC needs.
2. Success: function works; role has no `Resource:*` for data services; invokers listed; Access Analyzer unused trimmable later.
3. Inventory environment variables for secret leakage (move to Secrets Manager).

### 2. Inventory current role and invokers

```bash
aws lambda get-function --function-name "$FN" --query 'Configuration.{Role:Role,Env:Environment,Vpc:VpcConfig}'
ROLE=...
aws iam list-attached-role-policies --role-name "$ROLE"
aws iam list-role-policies --role-name "$ROLE"
aws lambda get-policy --function-name "$FN" 2>/dev/null || echo "no resource policy"
```

1. Expand managed policies attached.
2. List triggers (EventBridge, SQS ESM, API GW) for required invoke permissions.
3. CloudTrail: actions the function actually called.

### 3. Baseline

1. Export role policies and resource policy.
2. Canary invocations for each trigger path.
3. Note cold start / VPC ENI considerations separately from IAM.

### 4. Apply least privilege

1. Replace shared mega-roles with **per-function** or per-domain roles.
2. Scope every data action to ARNs; include indexes (`table/orders/index/*`) if needed.
3. Secrets: single secret ARN prefix; no `secretsmanager:*`.
4. SQS ESM: `sqs:ReceiveMessage`, `DeleteMessage`, `GetQueueAttributes` on that queue; DLQ send if used.
5. Kinesis: `kinesis:GetRecords`, `GetShardIterator`, `DescribeStream`, `ListShards` on stream ARN.
6. Remove `iam:PassRole` unless function truly creates resources needing it (high risk).
7. Resource-based policy: only API GW source ARN / account principals required.

```bash
aws lambda add-permission \
  --function-name "$FN" \
  --statement-id apigw \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:REGION:ACCT:API/*/*/*"
```

8. Do not put AWS keys in env vars; role credentials only.

### 5. Verify with evidence

```bash
aws iam simulate-principal-policy --policy-source-arn "$ROLE_ARN" \
  --action-names dynamodb:Scan --resource-arns arn:aws:dynamodb:REGION:ACCT:table/other
# expect implicitDeny
aws lambda invoke --function-name "$FN" --payload '{}' out.json
```

1. Integration tests all triggers.
2. Confirm secret access works; other secrets denied.
3. Unused analyzer after 90 days for further trim.

### 6. Observe and harden

1. CloudWatch metric filters / GuardDuty for suspicious API calls from role.
2. Alert on policy attachments of `AdministratorAccess` to Lambda roles.
3. CI: policy linter (deny `*` resources on data plane).

### 7. Hand off

1. Role-per-function IaC module.
2. Document required permissions next to function code.
3. Link ESM and KMS skills for related configs.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Roles | one function one role | all Lambdas share admin role |
| Resources | explicit ARNs | `*` on S3/DDB |
| Secrets | GetSecretValue scoped | secrets in env plaintext |
| Invoke | source-arn conditions | public invoke permission |
| PassRole | avoided | wildcard PassRole |
| Logging | function log group only | `logs:*` on `*` |

## Output Checklist

- [ ] Function triggers and data access mapped
- [ ] Execution role policies inventoried
- [ ] Scoped permissions applied and tested
- [ ] Resource-based invoker policy tightened
- [ ] Secrets/KMS permissions minimal
- [ ] Negative tests for other resources
- [ ] No admin managed policies attached
- [ ] CI/lint considerations noted
- [ ] `aws-lambda-event-source-mapping` aligned if used
- [ ] `code-quality-standards` on IaC

## Rules

- Owned functions only.
- Execution role ≠ invoker permission; design both.
- Never use admin policies on Lambda “to unblock.”
- Scope secrets and data plane ARNs tightly.
- Focus on Lambda IAM; ESM tuning and SnapStart elsewhere.
