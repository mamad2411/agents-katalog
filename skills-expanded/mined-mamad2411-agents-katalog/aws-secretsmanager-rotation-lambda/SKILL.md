---
name: aws-secretsmanager-rotation-lambda
description: >
  Implement and harden AWS Secrets Manager rotation Lambdas for owned accounts: the
  four-step handler (createSecret, setSecret, testSecret, finishSecret), staging labels,
  IAM/VPC/KMS wiring, retries, and safe logging. Use when writing or debugging custom
  rotation functions or adapting AWS sample templates — not for org-wide secrets
  policy alone or generic Lambda performance tuning.
---

# AWS Secrets Manager Rotation Lambda

## Scope And Authorization

- **In scope:** Rotation functions and secrets in AWS accounts you own or are authorized to change.
- **Out of scope:** Deploying rotation against third-party secrets; logging or exfiltrating secret material.
- Broken handlers can lock out production databases — develop in nonprod with disposable credentials.
- Pair with `aws-secrets-manager-rotation` for enablement/ops; use `code-quality-standards` for code.

## When To Use

- Authoring a custom rotation Lambda for non-template secret types (API keys, multi-host, dual systems).
- Adapting AWS-provided RDS/Redshift/DocumentDB rotation code.
- Debugging step failures, timeout, VPC DNS, or incorrect label transitions.
- Hardening rotation code: least privilege, no plaintext logs, idempotent steps.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Enabling schedules / operational rotation runbook | `aws-secrets-manager-rotation` |
| Org secrets hygiene / scanning | `secrets-management-hygiene` |
| Generic Lambda isolation patterns | Azure/AWS compute skills as applicable |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Step | Responsibility |
| --- | --- |
| `createSecret` | Generate new secret value; put as `AWSPENDING` (do not promote yet) |
| `setSecret` | Apply pending credentials to the service (e.g. `ALTER USER`) |
| `testSecret` | Verify pending credentials work (connect, call API) |
| `finishSecret` | Move `AWSCURRENT` to pending version; demote previous |
| Trigger | Event includes `SecretId`, `Token` (version id), `Step` |
| Tooling | Python/Node rotation templates, AWS Lambda, VPC ENI, Secrets Manager API |

## Workflow

### 1. Confirm scope and success criteria

1. Secret type, engine/API, multi-user vs single-user, runtime language, VPC requirements.
2. Success: each step idempotent; full rotation in nonprod; no secret values in CloudWatch Logs.
3. Rollback: previous version still labeled `AWSPREVIOUS` until confirmed stable.

### 2. Inventory existing function and permissions

```bash
aws lambda get-function --function-name "$ROTATION_FN"
aws lambda get-policy --function-name "$ROTATION_FN"
aws iam get-role-policy --role-name "$ROTATION_ROLE" --policy-name inline-or-list-attached
aws secretsmanager describe-secret --secret-id "$SECRET_ARN"
```

1. Confirm resource-based policy allows `secretsmanager.amazonaws.com` to invoke the function.
2. Confirm Lambda can reach Secrets Manager (interface endpoint or NAT) and the target system.
3. Review environment variables — no hardcoded master passwords.

### 3. Baseline

1. Capture current handler code hash / image digest.
2. Sample CloudWatch log groups for accidental secret logging (redact findings).
3. Document expected JSON schema of the secret string (keys like `username`, `password`, `host`, `engine`).

### 4. Implement or fix the handler

**Skeleton (Python-style logic):**

```python
def lambda_handler(event, context):
    arn = event["SecretId"]
    token = event["Token"]
    step = event["Step"]
    if step == "createSecret":
        create_secret(arn, token)
    elif step == "setSecret":
        set_secret(arn, token)
    elif step == "testSecret":
        test_secret(arn, token)
    elif step == "finishSecret":
        finish_secret(arn, token)
    else:
        raise ValueError(f"Invalid step {step}")
```

**Step rules:**

1. **createSecret:** If `AWSPENDING` for `token` already exists, return success (idempotent). Else generate password with required complexity; `put_secret_value` with `ClientRequestToken=token`, `VersionStages=["AWSPENDING"]`.
2. **setSecret:** Read pending; apply to backend using master or current admin secret; do not promote labels.
3. **testSecret:** Authenticate with pending only; raise on failure so rotation aborts.
4. **finishSecret:** `update_secret_version_stage` to move `AWSCURRENT` to `token`; ensure previous version gets `AWSPREVIOUS`.

**IAM minimum (illustrative):**

```json
{
  "Effect": "Allow",
  "Action": [
    "secretsmanager:GetSecretValue",
    "secretsmanager:PutSecretValue",
    "secretsmanager:UpdateSecretVersionStage",
    "secretsmanager:DescribeSecret"
  ],
  "Resource": "arn:aws:secretsmanager:region:acct:secret:prod/db-*"
}
```

Plus `kms:Decrypt` / `kms:Encrypt` on the secret’s CMK; VPC ENI actions if in VPC; DB network via security groups (not IAM).

**Publish and grant invoke:**

```bash
aws lambda update-function-code --function-name "$ROTATION_FN" --zip-file fileb://rotation.zip
aws lambda add-permission --function-name "$ROTATION_FN" \
  --principal secretsmanager.amazonaws.com \
  --action lambda:InvokeFunction \
  --statement-id AllowSecretsManager \
  --source-arn "$SECRET_ARN"
aws secretsmanager update-secret --secret-id "$SECRET_ARN"  # ensure rotation config points here
aws secretsmanager rotate-secret --secret-id "$SECRET_ARN" \
  --rotation-lambda-arn "$ROTATION_FN_ARN" \
  --rotation-rules AutomaticallyAfterDays=30
```

### 5. Verify with evidence

```bash
aws secretsmanager rotate-secret --secret-id "$SECRET_ARN"
aws logs tail "/aws/lambda/$ROTATION_FN" --since 30m --format short
aws secretsmanager list-secret-version-ids --secret-id "$SECRET_ARN"
# Confirm stages: AWSCURRENT on new version; AWSPENDING absent after success
```

1. Unit-test each step with mocked Secrets Manager where possible.
2. Integration test against nonprod DB/API.
3. Grep logs for password patterns; fix any leak before prod.

### 6. Observe and harden

1. Alarms on Lambda errors, throttles, duration near timeout (VPC cold start + DB).
2. Set reserved concurrency thoughtfully so rotation is not starved.
3. Dependency pin + SAST on rotation package; no debug `print` of secret dicts.

### 7. Hand off

1. Document secret JSON schema, multi-user username fields, and master secret ARN.
2. Runbook for partial failures (setSecret succeeded but testSecret failed).
3. Link ops skill for schedules, consumer refresh, and incident rotation.

## Common Failure Modes

| Symptom | Likely cause | Fix direction |
| --- | --- | --- |
| createSecret timeout | No SM VPC endpoint / NAT | Network path to Secrets Manager |
| setSecret fails auth | Wrong master secret / grants | Fix admin user privileges |
| testSecret fails | Password policy / host SSL | Align generation with engine rules |
| finishSecret never runs | Earlier step exception | Fix error; clear pending carefully |
| Apps fail after success | Client cache | Shorten TTL; restart consumers |
| AccessDenied on PutSecretValue | Missing IAM or replica region | Align role and multi-region secret |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Idempotency | Safe re-invoke per step | Duplicate users every retry |
| Logging | Step name + version id only | Full secret JSON in logs |
| Labels | finishSecret last after tests | Manual CURRENT flip in createSecret |
| Privileges | Resource-scoped secret ARNs | `secretsmanager:*` on `*` |
| Templates | Start from AWS samples, then harden | Unknown third-party zip from chat |

## Output Checklist

- [ ] Four steps implemented and idempotent
- [ ] IAM, KMS, VPC, and resource policy validated
- [ ] Secrets Manager invoke permission present
- [ ] Nonprod full rotation succeeded with correct labels
- [ ] CloudWatch shows no secret plaintext
- [ ] Timeouts and alarms set
- [ ] Secret JSON schema documented for consumers
- [ ] Ops handoff to `aws-secrets-manager-rotation`
- [ ] `code-quality-standards` applied to handler code

## Rules

- Never log or return secret values from the handler.
- Do not promote `AWSCURRENT` before a successful `testSecret`.
- Keep rotation Lambdas out of shared “debug” roles.
- Authorized environments only; dispose of test credentials.
- Prefer multi-user rotation logic when the service supports it.
