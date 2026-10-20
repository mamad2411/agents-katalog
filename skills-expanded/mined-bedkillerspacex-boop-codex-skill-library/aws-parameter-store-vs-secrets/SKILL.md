---
name: aws-parameter-store-vs-secrets
description: >
  Choose and operate AWS Systems Manager Parameter Store vs Secrets Manager for
  owned accounts: secret types, rotation, pricing, IAM, KMS, hierarchical
  parameters, and migration patterns. Use when designing config/secret storage —
  not for exfiltrating parameters from accounts you do not own.
---

# AWS Parameter Store vs Secrets

## Scope And Authorization

- **In scope:** SSM Parameter Store and Secrets Manager in authorized AWS accounts.
- **Out of scope:** Reading secrets from foreign accounts; disabling rotation to weaken security without approval.
- Never commit secret values to git; redact console screenshots.
- Prefer IAM roles to fetch at runtime over baking into images.
- Pair with `aws-kms-key-policy-basics`, `secrets-management-hygiene`, `code-quality-standards`.

## When To Use

- Deciding where to put DB passwords, API keys, feature flags, or config.
- Enabling automatic rotation for database credentials.
- Designing parameter hierarchies (`/app/prod/db/url`).
- Migrating plaintext env vars to managed stores.
- Reviewing IAM `GetParameter` / `GetSecretValue` scope.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| KMS CMK policies | `aws-kms-key-policy-basics` |
| ECS secret injection | `aws-ecs-task-security` |
| Lambda secret access IAM | `aws-lambda-least-privilege` |
| Org-wide secrets program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus — Comparison

| Dimension | Parameter Store | Secrets Manager |
| --- | --- | --- |
| Best for | Config, feature flags, non-rotating or infrequently rotated data; SecureString for secrets | Secrets needing managed rotation, cross-service integration |
| Types | String, StringList, SecureString | Binary/string secrets; JSON key-value common |
| Rotation | DIY Lambda/cron | Native rotation Lambdas for many DBs/services |
| Throughput | Standard vs advanced parameters | Higher intended for secrets retrieval patterns |
| Cost model | Often cheaper for config; advanced params priced | Per secret per month + API |
| Versioning | Parameter versions/labels (history) | Secret versions/stages (AWSCURRENT/AWSPENDING) |
| Cross-account | Resource policies possible | Resource policies common for sharing |

## Decision Guide

```text
Need automatic rotation / DB integration? → Secrets Manager
Pure config / hierarchical app settings? → Parameter Store
Occasional secret without rotation? → SecureString param OR Secrets Manager (org standard)
Cross-account share of a credential? → Often Secrets Manager policy
```

Many orgs: **config in SSM**, **credentials in Secrets Manager**.

## Workflow

### 1. Confirm scope and success criteria

1. Record apps, secret types, rotation requirements, consumers (ECS/Lambda/EKS).
2. Success: no plaintext secrets in git/task defs; IAM scoped; rotation tested if required; KMS CMK used for prod.
3. Inventory existing secrets locations (env, SSM, SM, third-party vaults).

### 2. Inventory

```bash
aws ssm describe-parameters --max-results 50
aws ssm get-parameters-by-path --path /app --recursive --query "Parameters[].Name"
aws secretsmanager list-secrets
```

1. Find `SecureString` vs plaintext String misuse for passwords.
2. List secrets without rotation where rotation is required by policy.
3. Check resource policies for external principals.

### 3. Baseline

1. Export names (not values) and owners tags.
2. Capture IAM roles that currently read them.
3. Note KMS keys used.

### 4. Implement storage correctly

**Parameter Store SecureString:**

```bash
aws ssm put-parameter \
  --name /app/prod/log_level \
  --type String \
  --value INFO \
  --overwrite

aws ssm put-parameter \
  --name /app/prod/api_token \
  --type SecureString \
  --key-id alias/ssm-prod \
  --value "$TOKEN" \
  --overwrite
```

**Secrets Manager + rotation (conceptual):**

```bash
aws secretsmanager create-secret \
  --name app/prod/db \
  --kms-key-id alias/secrets-prod \
  --secret-string '{"username":"app","password":"..."}'

aws secretsmanager rotate-secret \
  --secret-id app/prod/db \
  --rotation-lambda-arn arn:aws:lambda:REGION:ACCT:function:rotate-db \
  --rotation-rules AutomaticallyAfterDays=30
```

**IAM least privilege**

```json
{
  "Effect": "Allow",
  "Action": ["secretsmanager:GetSecretValue"],
  "Resource": "arn:aws:secretsmanager:REGION:ACCT:secret:app/prod/db-*"
}
```

```json
{
  "Effect": "Allow",
  "Action": ["ssm:GetParameter", "ssm:GetParametersByPath"],
  "Resource": "arn:aws:ssm:REGION:ACCT:parameter/app/prod/*"
}
```

Add `kms:Decrypt` for the specific CMK.

**App patterns**

1. Fetch at startup or with cache + TTL; handle rotation (refresh on auth failure).
2. ECS/Lambda: inject via native secrets, not plaintext env in IaC.
3. Hierarchy: `/<app>/<env>/<name>`.

### 5. Verify with evidence

```bash
aws ssm get-parameter --name /app/prod/api_token --with-decryption --query 'Parameter.Value' # redacted in tickets
aws secretsmanager get-secret-value --secret-id app/prod/db --query 'SecretString' # do not log
# Unauthorized role expect AccessDenied
```

1. Rotation dry-run in non-prod: password changes; app reconnects.
2. Confirm CloudTrail shows GetSecretValue from expected roles only.
3. Scan git history for leaked values; rotate if found.

### 6. Observe and harden

1. Alerts on secret policy changes and mass GetSecretValue anomalies.
2. Disable unused secrets; expire temporary parameters.
3. Prefer advanced tier only when needed (size/throughput/policies).

### 7. Hand off

1. Decision record: which store for which class of data.
2. Naming and tagging standard.
3. Rotation ownership for each secret class.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Passwords | Secrets Manager + rotation | plaintext SSM String or git |
| Config | SSM hierarchy | secrets manager sprawl for flags |
| IAM | ARN-scoped gets | `GetParameters*` on `*` |
| KMS | CMK per env/app | default key with open policy |
| Caching | TTL + refresh on fail | never refresh after rotate |
| Sharing | resource policies explicit | open to organization unintentionally |

## Output Checklist

- [ ] Data classes mapped to SSM vs SM
- [ ] Inventory of parameters/secrets complete
- [ ] Secure types and KMS applied
- [ ] IAM scoped to paths/ARNs
- [ ] Rotation tested where required
- [ ] Apps use managed injection/fetch
- [ ] No plaintext in git/task defs
- [ ] Monitoring on access/policy changes
- [ ] Naming standard documented
- [ ] `code-quality-standards` applied

## Rules

- Owned accounts only; never dump secret values into tickets.
- Prefer rotation for credentials; SSM for config.
- Scope IAM and KMS tightly.
- Design for rotation-safe clients.
- Focus on store selection/ops; deeper KMS and ECS injection in neighbors.
