---
name: aws-ecs-task-security
description: >
  Harden Amazon ECS task definitions and services for owned AWS accounts: task role
  vs execution role split, Secrets Manager/SSM injection, public tasks and
  assignPublicIp, security groups, Fargate vs EC2 launch type, and privileged
  containers. Use when reviewing ECS task IAM, plaintext env secrets, open service
  security groups, privileged/SYS_ADMIN Linux parameters, or public Fargate tasks —
  not for abusing third-party AWS accounts.
---

# AWS ECS Task Security

## Scope And Authorization

- **In scope:** ECS task definitions, services, and related IAM/SG in accounts you own or assess with authorization.
- **Out of scope:** Modifying or attacking ECS in third-party accounts.
- Task roles grant AWS API power to application code — least privilege is mandatory.
- Prefer Fargate where it reduces host management burden unless EC2 is required.
- Pair with `aws-ecs-exec-security` for shell access; `aws-lambda-least-privilege` patterns analogous for IAM.

## When To Use

- Reviewing taskRoleArn vs executionRoleArn responsibilities.
- Replacing plaintext secrets in environment variables with Secrets Manager/SSM.
- Closing `assignPublicIp=ENABLED` exposure and wide security groups.
- Removing privileged containers, host network, or dangerous Linux capabilities.
- Hardening logging, read-only root filesystem, and non-root users.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ECS Exec / SSM sessions | `aws-ecs-exec-security` |
| ECR image IAM | artifact/ECR skills |
| Network firewall design broadly | networking skills |
| K8s Pod Security | EKS skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Role | Purpose |
| --- | --- |
| Execution role | Pull images (ECR), write logs, fetch secrets for injection at start |
| Task role | Runtime AWS API calls from app code |
| Never | Merge both into one admin role “for simplicity” |

| Risk control | Target |
| --- | --- |
| Secrets | `secrets` / `secretsManager` ARNs — not plain `environment` |
| Network | Private subnets; SG least ports; public IP only if required |
| Linux params | `privileged=false`; drop caps; no host PID/network unless justified |
| User | non-root `user` in container definition |
| Filesystem | `readonlyRootFilesystem=true` when app allows |

## Workflow

### 1. Confirm scope and success criteria

1. Record clusters, services, launch type, data class, public exposure needs.
2. Success: secrets not in task JSON plaintext; roles split and scoped; SG minimal; no privileged; public IP justified or removed.
3. List AWS APIs the app truly needs (S3 prefix, SQS queue, etc.).

### 2. Inventory task definitions

```bash
aws ecs list-services --cluster "$CLUSTER"
aws ecs describe-services --cluster "$CLUSTER" --services "$SVC"
TD_ARN=$(aws ecs describe-services --cluster "$CLUSTER" --services "$SVC" --query 'services[0].taskDefinition' --output text)
aws ecs describe-task-definition --task-definition "$TD_ARN"
```

1. Flag `environment` entries that look like passwords/keys.
2. Note `privileged`, `linuxParameters.capabilities`, `networkMode`, `pidMode`.
3. Check `networkConfiguration.assignPublicIp` and SG rules.

### 3. Baseline

1. Export current task definition JSON to Git (redact secrets if any — rotate if found).
2. Capture IAM policies for both roles.
3. Snapshot SG ingress rules.

### 4. Apply hardening

**Split roles**

```json
{
  "executionRoleArn": "arn:aws:iam::ACCT:role/ecsTaskExecution",
  "taskRoleArn": "arn:aws:iam::ACCT:role/ecsAppTask"
}
```

- Execution: `ecr:GetAuthorizationToken`, pull, `logs:CreateLogStream`, `logs:PutLogEvents`, `secretsmanager:GetSecretValue` / `ssm:GetParameters` for **referenced** secrets only.
- Task: only runtime permissions (e.g., `s3:GetObject` on one prefix).

**Secret injection**

```json
"secrets": [
  {
    "name": "DB_PASSWORD",
    "valueFrom": "arn:aws:secretsmanager:REGION:ACCT:secret:app/db-xxxxxx"
  }
]
```

**Network**

```bash
# Prefer DISABLED public IP for private services behind ALB
aws ecs update-service --cluster "$CLUSTER" --service "$SVC" \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-private],securityGroups=[sg-app],assignPublicIp=DISABLED}"
```

**Container security options**

```json
{
  "user": "1000:1000",
  "privileged": false,
  "readonlyRootFilesystem": true,
  "linuxParameters": {
    "capabilities": { "drop": ["ALL"], "add": ["NET_BIND_SERVICE"] }
  }
}
```

1. Front with ALB/NLB security groups; app SG only allows LB SG on container port.
2. Avoid `host` network mode on multi-tenant hosts.
3. Pin image digests; scan images in CI.
4. FireLens/awslogs: no secrets in log drivers.

### 5. Verify with evidence

```bash
aws ecs describe-task-definition --task-definition "$TD" \
  --query 'taskDefinition.containerDefinitions[].{env:environment,secrets:secrets,priv:privileged,user:user}'
aws ec2 describe-security-groups --group-ids sg-app
# Runtime: task can reach only required AWS APIs (deny test)
```

1. Confirm secret values not visible in `describe-task-definition` plaintext env.
2. Port scan / SG review: no 0.0.0.0/0 on app ports unless intentional public service.
3. App smoke test after dropping capabilities.

### 6. Observe and harden

1. CloudTrail for role usage; Access Analyzer unused permissions.
2. GuardDuty ECS runtime findings if enabled.
3. Redeploy pipeline blocks privileged=true and plaintext secret patterns.

### 7. Hand off

1. Task definition module in IaC with secure defaults.
2. Checklist for new services (roles, secrets, SG, public IP).
3. Cross-link Exec skill for debugging without weakening task policy to admin.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Roles | split execution/task | single AdministratorAccess |
| Secrets | Secrets Manager ARN inject | `PASSWORD=...` in env |
| Network | private + LB | public IP + 0.0.0.0/0:443 to world if not needed |
| Privileged | false | true for convenience |
| User | non-root | root default ignored |
| Images | digests + scan | `:latest` always |

## Output Checklist

- [ ] Services/task defs inventoried
- [ ] Execution vs task roles split and scoped
- [ ] Secrets migrated off plaintext env
- [ ] Public IP/SG posture justified/hardened
- [ ] Privileged/caps/host modes reviewed
- [ ] Non-root / read-only applied where possible
- [ ] Verification evidence captured
- [ ] CI policy checks considered
- [ ] `aws-ecs-exec-security` reviewed if exec used
- [ ] `code-quality-standards` on IaC

## Rules

- Owned accounts only.
- Least privilege task roles; never share execution role as app identity.
- Secrets from managers, not git/task JSON plaintext.
- Public networking is an explicit product decision with owners.
- Focus on task/service hardening; Exec access is a separate control plane.
