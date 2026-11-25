---
name: aws-deploy
description: Deploy containers to ECS on Fargate with ECR, IAM task roles, CloudWatch and X-Ray observability, and cost basics. Use when the user is containerizing a service for AWS or debugging an ECS deployment.
---

# Deploying Containers on AWS (ECS + Fargate)

## ECR: registry first

```bash
aws ecr create-repository --repository-name myapp \
  --image-scanning-configuration scanOnPush=true
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker build --platform linux/arm64 -t myapp .
docker tag myapp ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/myapp:git-SHA
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/myapp:git-SHA
```

Tag with immutable git SHAs, never deploy `:latest`. Set repo tag
immutability on, add a lifecycle policy to expire untagged images.

## ECS on Fargate

Pieces: cluster (namespace) -> task definition (image, cpu/mem, roles,
logging) -> service (desired count, load balancer, deployment config).

- **Task role** vs **execution role**: the task role is what your app code
  assumes (S3, DynamoDB access); the execution role is what ECS itself uses
  to pull from ECR and write logs. Confusing them is the top IAM bug.
- Fargate cpu/memory come in fixed pairs (e.g. 0.25 vCPU/512 MB up to
  16 vCPU/120 GB); ARM64 (`runtimePlatform`) is about 20% cheaper.
- Inject config via environment; inject secrets via `secrets` referencing
  Secrets Manager or SSM Parameter Store ARNs (execution role needs read).
- Health checks: ALB target group health check drives rollout success; set
  a real `/healthz` and a `healthCheckGracePeriodSeconds` covering startup.
- Enable circuit breaker with rollback on every service:
  `deploymentConfiguration: { deploymentCircuitBreaker: { enable: true,
  rollback: true } }`. Without it, a bad image loops forever "IN_PROGRESS".

Ship it (CDK does all of this in ~20 lines with
`aws-ecs-patterns.ApplicationLoadBalancedFargateService`):

```bash
aws ecs update-service --cluster prod --service myapp \
  --force-new-deployment            # redeploy same task def
aws ecs describe-services --cluster prod --services myapp \
  --query 'services[0].events[:10]' # first place to look when stuck
aws ecs execute-command --cluster prod --task TASK_ID \
  --container app --interactive --command "/bin/sh"   # needs enableExecuteCommand
```

Stuck rollout triage order: service events -> stopped task
`stoppedReason` -> container exit code -> target group health.
`CannotPullContainerError` means execution role, VPC endpoints/NAT, or a
bad tag.

## Observability

- `awslogs` log driver to CloudWatch Logs; structured JSON lines so Logs
  Insights can query them. Set retention explicitly (default is forever,
  which is billable forever).
- Container Insights on the cluster for cpu/mem/task metrics; alarm on
  `RunningTaskCount` versus desired and on ALB 5xx + target response time.
- Tracing: X-Ray via ADOT (AWS Distro for OpenTelemetry) sidecar or SDK;
  newer CloudWatch Application Signals gives service maps and SLOs on top
  of OTel with less setup. Instrument the ALB request ID through your logs
  at minimum.

## Cost basics

- Fargate bills per vCPU-second and GB-second while tasks run: right-size
  from Container Insights p95, not from launch-day guesses.
- Biggest quiet costs: NAT gateway data processing (use VPC endpoints for
  ECR/S3/Logs), over-provisioned task sizes, log retention, idle ALBs.
- Fargate Spot for interruptible workers (capacity provider weight mix);
  Compute Savings Plans once usage is steady.
- One ALB with host/path rules can front many services; do not create one
  per service by default.

Current Fargate pricing and region support: check live via the
`aws-knowledge` MCP server rather than trusting remembered numbers.
