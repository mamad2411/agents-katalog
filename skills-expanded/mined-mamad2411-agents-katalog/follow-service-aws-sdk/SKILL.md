---
name: follow-service-aws-sdk
description: Use the AWS SDK per best practices for connecting to AWS cloud services
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - follow-service-cloudflare
  - follow-secret-manager
  - follow-best-practice
  - learn
  - setup-cicd

---

## Goal

Use the AWS SDK per best practices for connecting to AWS cloud services

## Scope

Use for developing applications that need to interact with AWS services such as S3, Lambda, DynamoDB, and others

## Execute

### Workflows

| Topic  | Workflow |
|--------|----------|
| Setup  | `workflows/setup-aws-sdk/SKILL.md` — SDK v3 modular install, credentials |
| Config | `workflows/config-aws-sdk/SKILL.md` — region, credentials chain, endpoint config |
| Verify | `workflows/verify-connection/SKILL.md` — smoke test credentials/connectivity |

Read `workflows/<name>/SKILL.md` per topic and follow the flow there — do not execute from this table directly

### 1. Install And Configure

> Goal: Install the AWS SDK and configure credentials

Latest: `@aws-sdk/client-s3@3.1139.0` (verified 2026-09-24) — use AWS SDK v3 (modular) only; `aws-sdk` v2 is deprecated

1. Install the SDK with `bun add @aws-sdk/client-s3` for the needed service
2. Configure credentials with IAM roles for production or environment variables for development
3. Create a client instance with `new S3Client({ region: 'us-east-1' })`
4. Use TypeScript for type safety and autocomplete

### 2. Make API Calls

> Goal: Call AWS services with the command pattern

1. Make API calls with the command pattern such as `await client.send(new PutObjectCommand(...))`
2. Handle errors with try-catch and use built-in retry logic
3. Use streaming for large files
4. Use pagination helpers for large datasets

## Rules

### 1. Installation

- Use `bun add` or `bun add -D` instead of `bun install`
- Install only the clients you need (modular v3)

### 2. Security

- Use IAM roles for production
- Use environment variables for development
- Never hardcode credentials in code

### 3. Error Handling

- Handle AWS SDK errors properly
- Implement retry logic with built-in retries
- Log errors for debugging

### 4. Type Safety

- Use TypeScript for type safety
- Use streaming for large files
- Use pagination helpers for large datasets

- Use /follow-create-sdk if needed
- Use /follow-service-cloudflare if needed
- Use /follow-secret-manager if needed
- Use /follow-best-practice if needed
- Use /learn-from-web if needed
- Use /setup-cicd if needed


## Expected Outcome

- Reliable integration with AWS services
- Code that follows best practices
- Robust error handling
- Appropriate security
