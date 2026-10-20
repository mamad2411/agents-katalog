---
name: aws-ecs-exec-security
description: >
  Amazon ECS Exec security for owned accounts: enabling Execute Command, SSM session
  permissions, task role vs exec auditing, logging to CloudWatch/S3, and least-privilege
  access for break-glass debugging. Use when reviewing who can ecs:ExecuteCommand —
  not for unauthorized shell access to third-party tasks.
---

# AWS ECS Exec Security

## Scope And Authorization

- **In scope:** ECS clusters/services/tasks you operate under authorization.
- **Out of scope:** Exec into tasks in accounts/systems without permission.
- ECS Exec is interactive shell-equivalent access — treat like production SSH.
- Prefer temporary elevation (SSO permission sets, JIT) over standing exec rights.
- Pair with `aws-ecs-task-security` for task definition hardening.

## When To Use

- Enabling ECS Exec for Fargate/EC2 launch types safely.
- Restricting `ecs:ExecuteCommand` and `ssm:StartSession` related permissions.
- Configuring exec session logging and KMS encryption.
- Auditing who used exec (CloudTrail + Session Manager logs).
- Disabling exec on prod services that should never allow shells.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Task roles, secrets, privileged containers | `aws-ecs-task-security` |
| EKS pod exec / kubectl | Kubernetes skills |
| SSM Session Manager fleet-wide | SSM skill |
| General IAM least privilege | `aws-iam-least-privilege` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Guidance |
| --- | --- |
| Task definition | `enableExecuteCommand` at service/task |
| Agent | SSM agent managed on Fargate when exec enabled |
| IAM user/role | `ecs:ExecuteCommand`, `ecs:DescribeTasks`, plus SSM messaging perms as documented |
| Task role | Often needs `ssmmessages:*` for exec channel |
| Logging | CloudWatch/S3 logging of session; optional KMS |
| Cluster setting | `executeCommandConfiguration` logging |

## Permission Sketch

| Principal | Needs |
| --- | --- |
| Human/break-glass role | `ecs:ExecuteCommand` on specific cluster/service ARNs; `ecs:DescribeTasks`; SSM start session related actions per AWS docs |
| Task role | `ssmmessages:CreateControlChannel`, `CreateDataChannel`, `OpenControlChannel`, `OpenDataChannel` |
| Execution role | image/logs secrets — not exec login itself |

## Workflow

### 1. Confirm scope and success criteria

1. Record clusters, services, environments, who needs exec and why.
2. Success: exec denied by default on prod; allowed JIT on staging; sessions logged; CloudTrail shows actor.
3. Define max session duration and approval process.

### 2. Inventory exec posture

```bash
aws ecs list-clusters
aws ecs describe-clusters --clusters "$CLUSTER" --include CONFIGURATIONS
aws ecs describe-services --cluster "$CLUSTER" --services "$SVC" \
  --query "services[].enableExecuteCommand"
aws ecs list-tasks --cluster "$CLUSTER" --service-name "$SVC"
# IAM
aws iam list-entities-for-policy --policy-arn "$POLICY_WITH_EXECUTE" 2>/dev/null || true
```

1. Find services with `enableExecuteCommand=true`.
2. Search org for `ecs:ExecuteCommand` in policies (Access Analyzer / IAM).
3. Check whether logging configuration is set on cluster.

### 3. Baseline

1. Export task definitions and service JSON.
2. List last 30 days CloudTrail `ExecuteCommand` events (if any).
3. Confirm log destination bucket/KMS policies.

### 4. Harden configuration

**Cluster execute command logging:**

```bash
aws ecs update-cluster \
  --cluster "$CLUSTER" \
  --configuration '{
    "executeCommandConfiguration": {
      "logging": "OVERRIDE",
      "logConfiguration": {
        "cloudWatchLogGroupName": "/ecs/exec",
        "cloudWatchEncryptionEnabled": true,
        "s3Bucket": "ecs-exec-logs-prod",
        "s3EncryptionEnabled": true,
        "s3KeyPrefix": "exec/"
      }
    }
  }'
```

**Service enable only where needed:**

```bash
aws ecs update-service --cluster "$CLUSTER" --service "$SVC" \
  --enable-execute-command \
  --force-new-deployment
# Disable:
aws ecs update-service --cluster "$CLUSTER" --service "$SVC" \
  --no-enable-execute-command --force-new-deployment
```

**IAM least privilege (human):**

```json
{
  "Effect": "Allow",
  "Action": ["ecs:ExecuteCommand", "ecs:DescribeTasks"],
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "ecs:cluster": "arn:aws:ecs:REGION:ACCT:cluster/staging"
    }
  }
}
```

Refine resource ARNs as supported; prefer permission boundaries and SSO session tags.

1. Separate staging vs prod permission sets.
2. Require MFA for exec roles.
3. Task role: only ssmmessages permissions required for exec — not AdministratorAccess.
4. Containers: read-only root FS still recommended; exec does not justify privileged=true.

### 5. Verify with evidence

```bash
aws ecs execute-command --cluster "$CLUSTER" --task "$TASK" \
  --container app --interactive --command "/bin/sh"
# Expect deny without role; allow with break-glass
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=ExecuteCommand
```

1. Confirm session logs appear in CloudWatch/S3.
2. Confirm prod service with exec disabled rejects ExecuteCommand.
3. Test that unprivileged IAM user cannot exec.

### 6. Observe and harden

1. Alert on any ExecuteCommand in production accounts.
2. Periodic access review of exec-capable roles.
3. Prefer short-lived ECS Exec over baking SSH keys into images.

### 7. Hand off

1. Runbook: request access → SSO role → exec → ticket ID in session notes.
2. Document logging bucket retention and who can read session logs (also sensitive!).
3. Link task security skill for broader hardening.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | exec off in prod | exec on all services |
| Identity | JIT SSO + MFA | shared long-lived keys with exec |
| Logging | CW+S3 encrypted | no session logs |
| IAM | cluster-conditioned | `ecs:*` on `*` |
| Response | alerts on prod exec | silent shells |
| Container | still non-root, minimal | privileged for “debugging ease” |

## Output Checklist

- [ ] Clusters/services needing exec inventoried
- [ ] enableExecuteCommand justified per service
- [ ] Cluster logging configuration set
- [ ] Human IAM least privilege + MFA/JIT
- [ ] Task role ssmmessages minimal
- [ ] Allow/deny tests evidenced
- [ ] CloudTrail/session log review path
- [ ] Prod alerts configured
- [ ] `aws-ecs-task-security` cross-check done

## Rules

- Authorized break-glass only; exec is production access.
- Log all sessions; restrict who can read logs.
- Prefer disable-by-default on production.
- Never trade container isolation for easier debugging without ticket.
- Focus on Exec access control; broader task definition hardening in `aws-ecs-task-security`.
