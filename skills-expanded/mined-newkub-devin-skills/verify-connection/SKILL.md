---
name: follow-service-aws-sdk-verify-connection
description: Confirm after setup/config that the AWS SDK really connects — credentials valid, region correct, permissions sufficient
related:
  - follow-service-aws-sdk
---

## Goal

Confirm after setup/config that the AWS SDK really connects — credentials valid, region correct, permissions sufficient

## Scope

- Used when `/follow-service-aws-sdk` dispatches to `verify`/`verify-connection`
- Read-only: check only — do not change credentials

## Execute

### 1. Check Credentials Loaded

> Goal: credentials exist and load via the right chain

1. Check `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` or the credentials chain (profile, SSO, IAM role)
2. Check `AWS_REGION` is set and matches what the config expects

### 2. Smoke Test API Call

> Goal: a real call responds

1. `aws sts get-caller-identity` — must return Account/Arn
2. If the SDK is used in code → a minimal read call (e.g. `sts.getCallerIdentity()` via the SDK)
3. If service-specific → a read-only call of that service (e.g. `s3.listBuckets()`, `dynamodb.listTables()`)

### 3. Report

> Goal: Summarize connection status

1. Use `/report` columns: `No.`, `Check`, `Result`, `Evidence`
2. Verdict: `connected` / `auth-failed` / `wrong-region` / `missing-permission`

## Rules

- Use read-only calls only — never calls that change state
- Do not print secret values — show only Account/Arn/Region
- Auth failure → recommend `/follow-secret-manager` — do not fix it yourself

## Expected Outcome

- Connection verdict with Account/Region evidence
