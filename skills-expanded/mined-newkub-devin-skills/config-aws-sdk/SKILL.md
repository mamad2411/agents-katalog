---
name: follow-service-aws-sdk-config-aws-sdk
description: Set/edit AWS SDK configuration — region, credentials chain, endpoint overrides, and client options — merging with the existing config
related:
  - follow-service-aws-sdk
---

## Goal

Set/edit AWS SDK configuration — region, credentials chain, endpoint overrides, and client options — merging with the existing config

## Scope

- Covers env keys, client options, and local endpoints (e.g. LocalStack)
- If not yet installed/credentials missing → do `workflows/setup-aws-sdk/SKILL.md` first

## Execute

### 1. Read Current Config

> Goal: Know the current config before editing

1. Read the current client construction, env keys (`AWS_REGION`, `AWS_PROFILE`, `AWS_ENDPOINT_URL*`), and `~/.aws/config` if relevant
2. Do `/deep-review-codebase` domain `review-config` if env must be compared with code
3. If no client is found → do `workflows/setup-aws-sdk/SKILL.md` first

### 2. Configure Region

> Goal: region correct and consistent

1. Use the `AWS_REGION` env var as the primary source — client option `{ region }` only when an override is needed
2. Confirm the region matches the real resources (S3 bucket region, DynamoDB table region)

### 3. Configure Credentials Chain

> Goal: the SDK resolves credentials in the right order

1. Use the default provider chain: env vars → shared config/`AWS_PROFILE` → IAM role
2. For assume role → use `@aws-sdk/credential-providers` (`fromTemporaryCredentials`) per the official docs
3. All secrets through `/follow-secret-manager` — never hardcode

### 4. Configure Endpoints And Options

> Goal: endpoint overrides correctly scoped

1. For local dev (LocalStack) → set `endpoint` in client options or the `AWS_ENDPOINT_URL` env var in dev only
2. Add only options actually used, such as `maxAttempts` and `requestHandler` timeouts
3. Guard endpoint overrides with `NODE_ENV` — never point at a local endpoint in production

### 5. Verify

> Goal: config works against real AWS or the local endpoint

1. Run a smoke call such as `ListBucketsCommand` or `DescribeTableCommand`
2. Do `/run-verify` for lint, typecheck
3. If broken → revert the key just changed, then report the diff

## Rules

- Edit only the necessary keys/options — never overwrite the whole config
- Production uses IAM roles — never static credentials
- Endpoint overrides must be scoped per environment
- Use `/follow-best-practice` for retry/timeout patterns

## Expected Outcome

- Region/credentials chain correct per environment
- Endpoint overrides work in dev without affecting production
- Smoke call succeeds — lint, typecheck pass
