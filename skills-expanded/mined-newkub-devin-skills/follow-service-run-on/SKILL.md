---
name: follow-service-run-on
description: Install, configure, and validate self-hosted GitHub Actions runners on AWS with RunsOn
argument-hint: "[scope]"
related:
  - ask-me
  - deep-validate
  - git-commit
---

## Goal

Install and configure self-hosted GitHub Actions runners on AWS with RunsOn — from the AWS stack, IAM, GitHub App, `.github/runs-on.yml` through validation

## Scope

Used for:
- Installing the RunsOn stack on AWS with CloudFormation or Terraform
- Configuring IAM, VPC, GitHub App
- Creating/editing `.github/runs-on.yml` and `.github/workflows/*.yml`
- Validating that runners really work
Not included: creating an AWS account, purchasing a license, or automatic commit/push

## Execute

### Workflows

| Topic  | Workflow |
|--------|----------|
| Setup  | `workflows/setup-run-on/SKILL.md` — AWS stack, GitHub App registration |
| Config | `workflows/config-run-on/SKILL.md` — `runs-on.yml` runner definitions, workflow labels |
| Verify | `workflows/verify-connection/SKILL.md` — stack healthy, runners register, labels match |

Read `workflows/<name>/SKILL.md` per topic and follow the flow there — do not execute from this table directly

### 1. Prepare Context

> Goal: Check context and permissions before installing

1. Check `aws --version` and AWS credentials with permission to create a CloudFormation stack
2. Confirm the GitHub organization/personal account and the RunsOn license key
3. Pick an AWS region such as `us-east-1`, `us-west-2`, `eu-west-1`
4. If context is not ready → stop and `/ask-me`

### 2. Deploy RunsOn Stack

> Goal: Install the AWS infrastructure for RunsOn

Note: template version `v3.3.1` is a pinned snapshot — check the latest template at `https://runs-on.com/installation/` before use (verified 2026-09-12)

1. Use the CloudFormation quick-create URL:
   `https://<region>.console.aws.amazon.com/cloudformation/home?region=<region>#/stacks/quickcreate?templateUrl=https://runs-on.s3.eu-west-1.amazonaws.com/cloudformation/template-v3.3.1.yaml&stackName=runs-on`
2. Fill in the main parameters: GitHub org, `LicenseKey`, email for cost alerts, `Environment` (optional)
3. If the stack fails with `Unable to assume the service linked role`, run:
   `aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com`
4. Wait for stack status `CREATE_COMPLETE`, then save the `RunsOnEntryPoint` output URL
5. If Terraform is wanted: use module `runs-on/runs-on/aws//flex` version `v3.3.1`

### 3. Register GitHub App And Repository

> Goal: Connect the GitHub repo with RunsOn

1. Open the `RunsOnEntryPoint` URL and press `Register app` to create a private GitHub App
2. Select the repositories the app may access
3. Open `https://github.com/organizations/<org>/settings/actions` to enable repository-level self-hosted runners
4. For warm pools or shared runner definitions, create `.github-private/.github/runs-on.yml` in the org (optional)

### 4. Configure Runners

> Goal: Configure custom runners and workflow labels

1. Create/edit `.github/runs-on.yml` in the repository (Flex) for custom runner definitions:
   ```yaml
   runners:
     gpu-type1:
       family: ["g4dn", "g5"]
       image: ubuntu24-gpu-x64
       cpu: [4, 16]
       spot: price-capacity-optimized
       extras: ["s3-cache"]
   ```
2. Edit `.github/workflows/<file>.yml` to use `runs-on` labels:
   ```yaml
   jobs:
     build:
       runs-on: runs-on=${{ github.run_id }}/runner=gpu-type1
   ```
3. If `.github/runs-on.yml` is not used, specify labels directly in the `runs-on:` value:
   - `runs-on=${{ github.run_id }}` to prevent the runner from being claimed
   - `runner=2cpu-linux-x64` or `cpu=`, `ram=`, `family=`, `image=`, `volume=`, `spot=`, `extras=`
4. For Fleet, use `runs-on: runs-on/fleet=<fleet-name>/env=<env>`

### 5. Validate Deployment

> Goal: Confirm the runner works

1. Push a commit or trigger `workflow_dispatch`
2. Check GitHub Actions logs that the job runs on a `runs-on` runner
3. Watch the AWS EC2 console / CloudWatch logs that the instance launches and terminates correctly
4. Confirm the email for the SNS cost/alert subscription
5. If the workflow fails, run `/deep-validate` then `/ask-me`

## Rules

### 1. AWS And IAM

- Install RunsOn in a dedicated AWS sub-account for isolation
- CloudFormation automatically creates IAM roles with limited permissions for the service
- Never hardcode `LicenseKey` in skill files or source code

### 2. GitHub Actions Integration

- Always use `runs-on=${{ github.run_id }}` as the routing key
- Use `runner=<name>` when `.github/runs-on.yml` exists
- Use backticks for `commands`, `paths`, and runner labels

### 3. Configuration Files

- `.github/runs-on.yml` is for custom runners in Flex
- `.github-private/.github/runs-on.yml` is for warm pools and org-wide runner definitions
- Edit `.github/workflows/*.yml` with `edit` or `write` as appropriate

### 4. Safety

- Ask the user before deploying the stack or changing important repos
- No automatic commit/push — the user runs it or uses `git-commit` as desired
- If data or permissions are missing → stop and report


## Expected Outcome

- RunsOn stack running on AWS and GitHub App registered
- `.github/runs-on.yml` and workflows correct for the chosen Flex/Fleet mode
- The workflow runs successfully on a self-hosted runner on EC2
- Validation logs show the instance launches per the specified labels
