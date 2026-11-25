---
name: follow-service-run-on-setup-run-on
description: Install the RunsOn stack on AWS (CloudFormation/Terraform), register the GitHub App, and enable self-hosted runners for the repo — first-time setup
related:
  - follow-service-run-on
---

## Goal

Install the RunsOn stack on AWS (CloudFormation/Terraform), register the GitHub App, and enable self-hosted runners for the repo — first-time setup

## Scope

- Covers the AWS stack, GitHub App registration, and org settings
- Does not include creating an AWS account, purchasing a license, or automatic commit/push
- Runner label/workflow config → `workflows/config-run-on/SKILL.md`

## Execute

### 1. Check Prerequisites

> Goal: context and permissions ready before deploying the stack

1. Check `aws --version` and AWS credentials have permission to create a CloudFormation stack
2. Confirm the GitHub organization/account and the RunsOn license key with the user
3. Pick an AWS region such as `us-east-1`
4. If context is missing → stop and run `/ask-me`

### 2. Deploy AWS Stack

> Goal: RunsOn infrastructure running on AWS

1. Use the CloudFormation quick-create URL from https://runs-on.com/installation/ — always check the latest template before use
2. Fill in parameters: GitHub org, `LicenseKey`, email for cost alerts
3. If it fails with `Unable to assume the service linked role` → run `aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com`
4. Wait for stack status `CREATE_COMPLETE`, then save the `RunsOnEntryPoint` output URL
5. Store `LicenseKey` via `/follow-secret-manager` — never commit it

### 3. Register GitHub App

> Goal: repo connected to RunsOn

1. Open the `RunsOnEntryPoint` URL and press `Register app` to create a private GitHub App
2. Select the repositories the app may access
3. Open org settings → Actions to enable repository-level self-hosted runners

### 4. Validate

> Goal: the runner really works

1. Create a test workflow or trigger `workflow_dispatch` with a `runs-on:` label
2. Check GitHub Actions logs that it runs on a `runs-on` runner and the EC2 instance launches/terminates correctly
3. If it fails → run `/deep-validate` then `/ask-me`

## Rules

- Ask the user before deploying the stack — it is an infrastructure change with cost
- Install in a dedicated AWS sub-account for isolation
- Never hardcode `LicenseKey` in any file
- Use official docs https://runs-on.com as the primary source

## Expected Outcome

- RunsOn stack `CREATE_COMPLETE` and GitHub App registered
- The test workflow runs successfully on a self-hosted runner
- Ready for `workflows/config-run-on/SKILL.md`
