---
name: managing-aws-codedeploy
description: |
  Use when working with Aws Codedeploy — aWS CodeDeploy application and
  deployment management. Covers applications, deployment groups, deployment
  history, deployment configurations, instance health, target revisions, and
  rollback settings. Use when inspecting deployments, debugging failed
  deployments, reviewing deployment strategies, or auditing deployment group
  configurations.
connection_type: aws
preload: false
---

# AWS CodeDeploy Management Skill

Analyze and manage AWS CodeDeploy applications, deployment groups, and deployment history.

## MANDATORY: Discovery-First Pattern

**Always list applications before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== CodeDeploy Applications ==="
aws deploy list-applications --output text --query 'applications[]'

echo ""
echo "=== Application Details ==="
for app in $(aws deploy list-applications --output text --query 'applications[]'); do
  aws deploy get-application --application-name "$app" --output text \
    --query 'application.[applicationName,computePlatform,createTime]' &
done
wait

echo ""
echo "=== Deployment Groups ==="
for app in $(aws deploy list-applications --output text --query 'applications[]'); do
  for dg in $(aws deploy list-deployment-groups --application-name "$app" --output text --query 'deploymentGroups[]'); do
    aws deploy get-deployment-group --application-name "$app" --deployment-group-name "$dg" --output text \
      --query "deploymentGroupInfo.[\"$app\",deploymentGroupName,deploymentConfigName,computePlatform]" &
  done
done
wait

echo ""
echo "=== Deployment Configurations ==="
aws deploy list-deployment-configs --output text --query 'deploymentConfigsList[]'
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== Recent Deployments ==="
for app in $(aws deploy list-applications --output text --query 'applications[]'); do
  deploy_ids=$(aws deploy list-deployments --application-name "$app" --max-items 5 --output text --query 'deployments[]')
  if [ -n "$deploy_ids" ]; then
    for dep_id in $deploy_ids; do
      aws deploy get-deployment --deployment-id "$dep_id" --output text \
        --query "deploymentInfo.[deploymentId,applicationName,deploymentGroupName,status,createTime]" &
    done
  fi
done
wait | head -25

echo ""
echo "=== Failed Deployments ==="
for app in $(aws deploy list-applications --output text --query 'applications[]'); do
  failed=$(aws deploy list-deployments --application-name "$app" \
    --include-only-statuses Failed --max-items 3 --output text --query 'deployments[]')
  for dep_id in $failed; do
    aws deploy get-deployment --deployment-id "$dep_id" --output text \
      --query "deploymentInfo.[deploymentId,applicationName,status,errorInformation.code,errorInformation.message]" &
  done
done
wait | head -15

echo ""
echo "=== Deployment Group Health ==="
for app in $(aws deploy list-applications --output text --query 'applications[]'); do
  for dg in $(aws deploy list-deployment-groups --application-name "$app" --output text --query 'deploymentGroups[]'); do
    aws deploy get-deployment-group --application-name "$app" --deployment-group-name "$dg" --output text \
      --query "deploymentGroupInfo.[applicationName,deploymentGroupName,lastSuccessfulDeployment.deploymentId,lastSuccessfulDeployment.status,lastSuccessfulDeployment.createTime]" &
  done
done
wait
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: AppName, DeploymentGroup, DeploymentId, Status
- Aggregate deployment counts by status for busy applications
- Never dump full revision details -- show deployment metadata only

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Deployment status values**: Created, Queued, InProgress, Baking, Succeeded, Failed, Stopped, Ready
- **Compute platforms**: Server (EC2/On-prem), Lambda, ECS -- each has different deployment group config
- **Deployment configs**: CodeDeployDefault.OneAtATime, HalfAtATime, AllAtOnce, and custom configs
- **Rollback config**: Check `autoRollbackConfiguration` -- can trigger on DEPLOYMENT_FAILURE or DEPLOYMENT_STOP_ON_ALARM
- **Blue/Green vs In-Place**: Check `deploymentStyle` -- Blue/Green requires load balancer config
- **Target revision**: Verify `targetRevision` in deployment group points to correct S3/GitHub location
- **Instance health**: For EC2, check `instanceSummary` with deployment ID for per-instance status
