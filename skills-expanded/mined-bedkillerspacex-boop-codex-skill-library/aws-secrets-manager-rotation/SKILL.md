---
name: aws-secrets-manager-rotation
description: >
  AWS Secrets Manager automatic and immediate rotation for owned accounts: rotation
  Lambda steps, AWSCURRENT/AWSPENDING/AWSPREVIOUS labels, single- vs multi-user
  strategies, hosted RDS/Redshift/DocumentDB rotation, and post-leak cutover. Use when
  enabling or fixing Secrets Manager rotation, staging-label stuck rotations, custom
  rotation functions, or dual-credential cutover — not for third-party account abuse or
  generic git/.env secret scanning alone.
---

# AWS Secrets Manager Rotation

## Scope And Authorization

- **In scope:** Secrets and databases in AWS accounts you own or are authorized to operate.
- **Out of scope:** Rotating or reading secrets in accounts without authorization; using rotation to maintain unauthorized access.
- Rotation can lock applications out — use change windows, dual-credential strategies, and rollbacks.
- Never log secret plaintext; redact ARNs in public tickets if policy requires.
- Pair rotation Lambda code with `aws-secretsmanager-rotation-lambda` and `code-quality-standards`.

## When To Use

- Enabling automatic rotation on DB credentials, API keys, or service passwords in Secrets Manager.
- Immediate rotation after suspected leak or offboarding.
- Debugging stuck rotations (`AWSPENDING` never finishes), failed Lambda steps, or apps pinned to stale passwords.
- Choosing single-user vs alternating-user rotation for RDS-compatible engines.
- Hosted rotation templates vs custom multi-service secrets.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Implementing rotation Lambda step handlers | `aws-secretsmanager-rotation-lambda` |
| Org-wide secrets inventory / git scanning | `secrets-management-hygiene` |
| KMS key policy design alone | KMS-focused skill / account hardening |
| S3 bucket hardening | `aws-s3-bucket-hardening` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Staging labels | `AWSCURRENT` (active), `AWSPENDING` (candidate), `AWSPREVIOUS` (prior) |
| Rotation steps | `createSecret` → `setSecret` → `testSecret` → `finishSecret` |
| Single-user | Change password on one DB user; brief overlap risk |
| Multi-user | Alternate two users; safer for continuous traffic |
| Immediate rotation | `rotate-secret` with optional `RotationLambdaARN` |
| Tooling | AWS CLI Secrets Manager, Lambda, RDS, CloudWatch Logs, CloudTrail |

## Workflow

### 1. Confirm scope and success criteria

1. Record secret ARN, consumers (apps, Lambdas, ECS tasks), DB/engine, RTO for failed rotation.
2. Success: rotation succeeds end-to-end; apps fetch `AWSCURRENT` without downtime; old label retired.
3. Define abort: disable rotation schedule, keep last known good password procedure.

### 2. Inventory secrets and consumers

```bash
aws sts get-caller-identity
aws secretsmanager list-secrets --query "SecretList[].{Name:Name,ARN:ARN,Rotation:RotationEnabled}"
SECRET_ARN=arn:aws:secretsmanager:region:acct:secret:prod/db-app
aws secretsmanager describe-secret --secret-id "$SECRET_ARN"
aws secretsmanager get-secret-value --secret-id "$SECRET_ARN" --query "VersionIdsToStages"  # no SecretString in logs
```

1. Map who reads the secret (IAM `GetSecretValue`, VPC endpoints, caching SDKs).
2. Confirm rotation Lambda ARN, schedule (`rotation-rules`), and success/failure metrics.
3. Check KMS key grants for Secrets Manager + Lambda role.

### 3. Baseline

1. Note current version IDs and stage labels (do not print secret values into tickets).
2. Snapshot DB user list / grants for multi-user rotation.
3. Confirm app refresh behavior: TTL cache, restart required, Secrets Manager agent/sidecar.

### 4. Enable or repair rotation

**Hosted RDS rotation (high level):**

```bash
aws secretsmanager rotate-secret \
  --secret-id "$SECRET_ARN" \
  --rotation-lambda-arn "$ROTATION_LAMBDA_ARN" \
  --rotation-rules AutomaticallyAfterDays=30,Duration="3h"

# Immediate one-shot
aws secretsmanager rotate-secret --secret-id "$SECRET_ARN"
```

**Strategy checklist:**

1. Prefer **multi-user** for production databases when the engine supports it.
2. Ensure Lambda is in the same VPC/subnets/security groups as the DB when required.
3. Lambda role: `secretsmanager:GetSecretValue`, `PutSecretValue`, `UpdateSecretVersionStage`, DB network access, KMS decrypt/encrypt.
4. Resource policy on secret: allow rotation Lambda; deny broad `Principal: "*"` without conditions.
5. For custom secrets (API tokens): implement all four steps; never set `AWSCURRENT` before `testSecret` succeeds.

**Unstick pending label (careful, authorized break-glass):**

```bash
# Inspect versions/stages first
aws secretsmanager list-secret-version-ids --secret-id "$SECRET_ARN"
# Only after root-causing Lambda failures — follow AWS recovery guidance for your case
# Typical recovery: finish or abandon pending after ensuring DB password state is known
```

### 5. Verify with evidence

```bash
aws secretsmanager describe-secret --secret-id "$SECRET_ARN"
# Confirm RotationEnabled, LastRotatedDate, next rotation
aws lambda get-function --function-name "$ROTATION_LAMBDA"
aws logs filter-log-events --log-group-name "/aws/lambda/$ROTATION_LAMBDA" --limit 20
# App health: connection pool metrics, auth success rate — not secret dumps
```

1. Force a test rotation in nonprod; validate read path for `AWSCURRENT`.
2. Confirm `AWSPENDING` is cleared after success; `AWSPREVIOUS` retained for rollback window.
3. After leak response: rotate, invalidate caches, rotate dependent secrets, review CloudTrail `GetSecretValue`.

### 6. Observe and harden

1. Alarms: rotation Lambda errors, duration, secret age > threshold, pending version older than N hours.
2. CloudTrail: `RotationSucceeded` / failures; unusual `GetSecretValue` principals.
3. Disable long-lived static copies of the password in Parameter Store, SSM, CI variables, AMIs.

### 7. Hand off

1. Runbook: disable schedule, manual rotate, recover stuck pending, who owns DB users.
2. Document consumer refresh SLAs (cache TTL ≤ rotation period).
3. Cross-link Lambda implementation skill for custom code changes.

## Rotation Strategy Matrix

| Strategy | Best for | Watch-outs |
| --- | --- | --- |
| Single-user | Simple apps, low concurrency | Dropped connections during setSecret |
| Multi-user | Prod RDS-style engines | Both users must stay permission-equal |
| Immediate | Incident response | App cache may still hold old secret |
| Custom Lambda | Non-DB or multi-target secrets | Must implement all four steps correctly |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Labels | Promote CURRENT only after testSecret | Mark CURRENT before DB accepts password |
| Consumers | SDK fetch on interval / restart hooks | Password baked into task definition env |
| Lambda net | Same VPC + SG to DB + Secrets Manager endpoint | Public Lambda cannot reach private RDS |
| Logging | Step success/failure without secret body | `print(secret)` in rotation code |
| After leak | Rotate + audit GetSecretValue + revoke clones | Only rotate and hope |

## Output Checklist

- [ ] Secret ARN, consumers, DB/engine, authorization recorded
- [ ] Baseline version stages noted without leaking values
- [ ] Rotation Lambda + IAM + network path validated
- [ ] Strategy (single/multi/custom) chosen and documented
- [ ] Successful rotation evidenced (describe-secret + app health)
- [ ] Stuck-pending recovery procedure documented if relevant
- [ ] Alarms for rotation failure and secret age configured
- [ ] Duplicate secret copies eliminated or ticketed
- [ ] `code-quality-standards` applied to automation/Lambda code

## Rules

- Authorized accounts only; never dump secrets into chat, git, or tickets.
- Prefer multi-user rotation for critical databases.
- Do not disable rotation permanently without risk acceptance and expiry.
- Treat rotation Lambda as production critical path — test in nonprod first.
- Route Lambda step coding details to `aws-secretsmanager-rotation-lambda`.
