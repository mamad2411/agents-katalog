---
name: follow-service-aws-sdk-setup-aws-sdk
description: Install AWS SDK v3 (modular packages) and prepare credentials so the client can call AWS services — first-time setup
related:
  - follow-service-aws-sdk
---

## Goal

Install AWS SDK v3 (modular packages) and prepare credentials so the client can call AWS services — first-time setup

## Scope

- Install `@aws-sdk/client-<service>` only for services used — `aws-sdk` v2 is deprecated
- Configure credentials via env/IAM role
- If already set up → verify only; region/endpoint config → `workflows/config-aws-sdk/SKILL.md`

## Execute

### 1. Check Prerequisites

> Goal: Confirm the project is ready and not yet set up

1. Check `package.json` for existing `@aws-sdk/client-*` — if present → install only what's missing
2. Check env/secrets for `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, or `AWS_PROFILE`
3. If credentials are missing → store them via `/follow-secret-manager` or use an IAM role (production)

### 2. Install SDK

> Goal: Install only the modular clients actually used

1. Run `bun add @aws-sdk/client-s3` (or the needed service such as `@aws-sdk/client-dynamodb`, `@aws-sdk/client-lambda`)
2. Confirm the import works, e.g. `import { S3Client } from '@aws-sdk/client-s3'`
3. Use TypeScript for type safety

### 3. Configure Credentials

> Goal: correct credential chain

1. development → env vars `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` or `aws configure` + `AWS_PROFILE`
2. production → IAM role/instance profile — never put static keys
3. Never hardcode credentials in code — the SDK resolves them from the default chain automatically

### 4. Create Client And Smoke Check

> Goal: the client really works

1. Create a client such as `new S3Client({ region })` — read region from env/config
2. Run a smoke check with a read-only call such as `client.send(new ListBucketsCommand({}))`
3. If the local AWS CLI is ready → check identity with `aws sts get-caller-identity`

### 5. Verify

> Goal: the SDK actually works

1. Do `/run-verify` for lint, typecheck
2. If verify fails → do `/resolve-errors` max 3 rounds, then stop and report
3. Success → do `/suggest-next-action`

## Rules

- Use AWS SDK v3 only — never add `aws-sdk` v2
- Install only the clients actually used (modular)
- Use `/follow-best-practice` and `/learn-from-web` when unsure about the API — see official docs https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/

## Expected Outcome

- `@aws-sdk/client-*` installed only for services used
- Credentials live in env/IAM role, never in code
- Smoke check passes — ready for `workflows/config-aws-sdk/SKILL.md`
