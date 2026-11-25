---
name: aws-lambda-configuration-validation
description: >
  Validates an AWS Lambda function's configuration — reserved/provisioned
  concurrency budget, VPC networking config, environment variables, IAM
  execution role scope, and failure handling — before it deploys, catching
  problems that only otherwise surface as production throttling or an
  incident. Use when the user asks to "validate a Lambda function before
  deploy," "check Lambda reserved concurrency," "review a Lambda IAM role,"
  "why is my Lambda throttling," or "add a pre-deploy check for Lambda
  config."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# AWS Lambda Configuration Validation

## Purpose

Lambda configuration mistakes rarely fail at deploy time — `aws lambda
update-function-configuration` almost always succeeds even when the
resulting configuration is unsafe. A reserved concurrency value that
starves the rest of the account, a VPC subnet with too few free IPs, a
plaintext secret in an environment variable, or an execution role widened
"to make it work" all pass a normal deploy and only surface later as
throttling, an incident, or a security finding. This skill is the pre-deploy
gate that catches those problems before they reach production, complementing
[aws-lambda-packaging-and-configuration](../aws-lambda-packaging-and-configuration/SKILL.md),
which covers how to build the configuration in the first place.

## When to use

- Before promoting a Lambda deploy (via CI/CD, SAM, CDK, Terraform, or
  CloudFormation) to a production stage.
- Reviewing an infrastructure-as-code diff that changes a Lambda
  function's memory, timeout, concurrency, VPC config, or IAM role.
- Diagnosing functions across an account suddenly throttling with
  `TooManyRequestsException` after a new function was deployed.
- Adding VPC configuration to a previously VPC-less function.
- Auditing existing functions for plaintext secrets in environment
  variables or overly broad execution roles.

## Prerequisites & environment

- AWS CLI v2 with `lambda:GetFunctionConfiguration`,
  `lambda:GetAccountSettings`, `lambda:ListFunctions`, and
  `iam:GetRolePolicy`/`iam:ListAttachedRolePolicies` read permissions.
- `jq` for parsing CLI JSON output in shell-based checks.
- If validating IaC before it's applied: `cfn-lint`, `checkov`, or `tflint`
  (whichever matches the IaC tool in use) as a first-pass schema/policy
  check, with this skill's checks layered on top for Lambda-specific
  semantics those generic tools don't cover.

## Step-by-step guidance

1. **Check reserved concurrency against the account's shared concurrency
   pool before setting or raising it.** Every AWS account has an
   account-level concurrency limit per region, shared across all functions;
   reserved concurrency configured on one function is carved out of that
   shared pool and is unavailable to every other function, including ones
   with no reserved concurrency configured at all:
   ```bash
   aws lambda get-account-settings --query 'AccountLimit'
   aws lambda list-functions \
     --query "Functions[?ReservedConcurrentExecutions!=null].[FunctionName,ReservedConcurrentExecutions]" \
     --output table
   ```
   Sum existing reserved concurrency, add the new/changed value, and
   confirm meaningful headroom remains for functions with no reservation —
   if the sum approaches the account limit, request a quota increase
   (via Service Quotas) before deploying, don't just proceed.

2. **Validate VPC configuration, if present, before it ships.** Confirm
   subnets span multiple Availability Zones (a single-AZ Lambda VPC config
   is a resilience gap), that each subnet has enough free IP addresses to
   absorb burst concurrency, and that the security group's egress rules
   actually allow the destinations the function calls (including AWS
   service endpoints, if reached over the internet or via VPC endpoints):
   ```bash
   aws lambda get-function-configuration --function-name my-fn --query 'VpcConfig'
   aws ec2 describe-subnets --subnet-ids <SUBNET_ID> --query 'Subnets[0].AvailableIpAddressCount'
   ```
   If the function only calls AWS APIs (not resources inside the VPC),
   confirm it actually needs VPC attachment at all — removing unnecessary
   VPC config is usually the simpler and safer fix.

3. **Validate environment variables**: total size must stay under the 4 KB
   combined limit, no plaintext secrets should be present, and every
   variable the code reads at runtime should have a value set for the
   target stage:
   ```bash
   aws lambda get-function-configuration --function-name my-fn --query 'Environment.Variables'
   ```
   A secret-shaped value (API key, connection string with a password) here
   is a finding — it should be replaced with a reference resolved at
   runtime via Secrets Manager or SSM Parameter Store (SecureString),
   not stored as plaintext configuration.

4. **Validate the execution role's policy is scoped to specific resource
   ARNs**, not wildcards:
   ```bash
   aws iam list-attached-role-policies --role-name my-fn-execution-role
   aws iam get-role-policy --role-name my-fn-execution-role --policy-name my-fn-inline-policy
   ```
   Flag any statement with `"Resource": "*"` paired with a mutating action
   (`s3:*`, `dynamodb:*`, `iam:*`) as a required fix, not a warning to
   note and move past.

5. **Validate failure handling is configured for asynchronous invocations**
   (S3 event notifications, SNS, EventBridge targets) — a function with no
   Dead Letter Queue or on-failure destination silently drops events that
   exhaust their retry attempts:
   ```bash
   aws lambda get-function-event-invoke-config --function-name my-fn \
     --query '{DLQ: DestinationConfig.OnFailure, MaxRetry: MaximumRetryAttempts}'
   ```

6. **Wire these checks into CI as a gate**, not a manual step someone
   remembers to run. A minimal shell gate:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   FN=my-fn
   ACCOUNT_LIMIT=$(aws lambda get-account-settings --query 'AccountLimit.ConcurrentExecutions' --output text)
   RESERVED_SUM=$(aws lambda list-functions \
     --query "sum(Functions[?ReservedConcurrentExecutions!=null].ReservedConcurrentExecutions)" --output text)
   if [ "$RESERVED_SUM" -gt "$((ACCOUNT_LIMIT * 80 / 100))" ]; then
     echo "FAIL: reserved concurrency sum ($RESERVED_SUM) exceeds 80% of account limit ($ACCOUNT_LIMIT)"
     exit 1
   fi
   ROLE_POLICY=$(aws lambda get-function-configuration --function-name "$FN" --query 'Role' --output text)
   echo "Checked $FN against role $ROLE_POLICY — see IAM checks above for manual/checkov follow-up."
   ```

## Best practices

- Run these checks as a required CI gate on every IaC change that touches
  a Lambda resource, not just before a first deploy — configuration drift
  (someone hand-editing via console) is exactly what this catches later.
- Alert on reserved concurrency utilization at the account level
  (CloudWatch metric `ConcurrentExecutions` vs. account limit), not just
  at validation time — the shared pool can be consumed gradually as more
  functions are added over time.
- Prefer removing VPC attachment over widening subnet IP capacity when a
  function doesn't actually need private-network access — the simplest
  fix to a VPC-related throttling problem is often "don't attach a VPC at
  all."
- Bake secret-in-env-var detection into the same pipeline stage as generic
  secret scanning, so it's caught by the same mechanism regardless of
  which config surface (source code vs. Lambda console) introduced it.
- Re-validate after any manual console change — a change made outside the
  pipeline bypasses every check in this list until the next validation
  run catches it.

## Common pitfalls

- **Symptom:** Unrelated functions across the account start throttling
  with `TooManyRequestsException` shortly after a new function was
  deployed with a large reserved concurrency setting.
  **Fix:** The new function's reserved concurrency was carved out of the
  account's shared pool without checking remaining headroom; reduce it,
  request an account concurrency quota increase, or use provisioned
  concurrency scoped to a specific alias instead if the goal was
  cold-start mitigation, not concurrency isolation.

- **Symptom:** Adding VPC configuration to a function causes slow scale-up
  or ENI-related throttling under burst traffic.
  **Fix:** Verify subnet free-IP capacity across all AZs the function's
  VPC config references, and prefer VPC endpoints over NAT gateway routing
  for AWS service calls to reduce contention — or remove VPC attachment
  entirely if the function doesn't reach private resources.

- **Symptom:** A deploy pipeline reports success, but production traffic
  keeps hitting the previous version's behavior.
  **Fix:** Configuration was updated on `$LATEST` but a pinned alias
  (`prod`) still points at an older version; validate the alias's target
  version and its resolved configuration, not just `$LATEST`, after every
  deploy.

- **Symptom:** `aws lambda get-function-configuration` shows a
  recognizable secret value (API key, DB password) directly in
  `Environment.Variables`.
  **Fix:** Treat this as a real security finding — move it to Secrets
  Manager or SSM Parameter Store `SecureString` and have the function
  resolve it at runtime, then rotate the exposed secret.

- **Symptom:** An async-invoked function's failures never show up
  anywhere — no alert, no retry record — until a downstream team notices
  missing data.
  **Fix:** Configure a Dead Letter Queue or `on-failure` destination on
  the event invoke config, and alarm on messages landing there; validate
  this is set on every async-triggered function before deploy, not after
  the first silent data loss.

## Worked example

**Scenario:** A CI pipeline is about to deploy a change that adds
`ReservedConcurrentExecutions: 200` to a new order-processing function in
an account whose total concurrency limit is 1,000, and where five other
functions already reserve a combined 700.

Validation run:
```bash
$ aws lambda get-account-settings --query 'AccountLimit.ConcurrentExecutions' --output text
1000
$ aws lambda list-functions \
    --query "sum(Functions[?ReservedConcurrentExecutions!=null].ReservedConcurrentExecutions)" --output text
700
```
Adding `200` more brings the reserved total to `900` against a `1000`
limit, leaving only `100` unreserved for every other function in the
account, including ones with no reservation configured — below the 80%
soft threshold used as a gate in step 6's script, this deploy is flagged
to fail CI. The fix applied: request an account concurrency quota
increase via Service Quotas before this deploy proceeds, and separately
confirm with the order-processing team whether `200` is actually needed
or whether a lower reservation (sized to expected peak throughput) is
sufficient. The pipeline is re-run only after the quota increase is
approved and the reserved value is confirmed against real traffic
projections, not a round number picked without data.

## Cross-references

- [aws-lambda-packaging-and-configuration](../aws-lambda-packaging-and-configuration/SKILL.md) — how the memory, timeout, VPC, and IAM configuration validated here is built in the first place.
- [dapr-configuration-validation](../dapr-configuration-validation/SKILL.md) — the same pre-deploy validation discipline applied to Dapr component configs in a polyglot microservices context.
- [knative-configuration-validation](../knative-configuration-validation/SKILL.md) — the equivalent pre-deploy validation pattern for Knative Service/Revision configuration on Kubernetes.
