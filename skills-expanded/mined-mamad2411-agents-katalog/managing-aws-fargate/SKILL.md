---
name: managing-aws-fargate
description: |
  Use when working with Aws Fargate — aWS Fargate task and service analysis
  covering ECS cluster inventory, Fargate task status, CPU and memory
  utilization, task definition review, networking configuration, service
  auto-scaling policies, and container health checks. Use for Fargate-specific
  workload optimization.
connection_type: aws
preload: false
---

# AWS Fargate Management

Analyze AWS Fargate tasks, services, and resource utilization across ECS clusters.

## Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== ECS Clusters ==="
aws ecs list-clusters --output text --query 'clusterArns[]' \
  | tr '\t' '\n' | while read ARN; do
  aws ecs describe-clusters --clusters "$ARN" \
    --query 'clusters[].[clusterName,status,registeredContainerInstancesCount,runningTasksCount,pendingTasksCount]' \
    --output text
done | column -t

echo ""
echo "=== Fargate Services ==="
for CLUSTER in $(aws ecs list-clusters --output text --query 'clusterArns[]' | tr '\t' '\n'); do
  CLUSTER_NAME=$(echo "$CLUSTER" | rev | cut -d'/' -f1 | rev)
  aws ecs list-services --cluster "$CLUSTER" --launch-type FARGATE --output text --query 'serviceArns[]' \
    | tr '\t' '\n' | while read SVC; do
    aws ecs describe-services --cluster "$CLUSTER" --services "$SVC" \
      --query "services[].[serviceName,status,desiredCount,runningCount,launchType,platformVersion]" \
      --output text
  done
done | column -t | head -20

echo ""
echo "=== Running Fargate Tasks ==="
for CLUSTER in $(aws ecs list-clusters --output text --query 'clusterArns[]' | tr '\t' '\n'); do
  CLUSTER_NAME=$(echo "$CLUSTER" | rev | cut -d'/' -f1 | rev)
  for TASK in $(aws ecs list-tasks --cluster "$CLUSTER" --launch-type FARGATE --output text --query 'taskArns[]' | tr '\t' '\n'); do
    aws ecs describe-tasks --cluster "$CLUSTER" --tasks "$TASK" \
      --query "tasks[].[taskDefinitionArn | split('/') | last, lastStatus, cpu, memory, group, connectivity]" \
      --output text &
  done
done
wait
echo "" | column -t | head -20

echo ""
echo "=== Task Definitions (Fargate-compatible) ==="
aws ecs list-task-definitions --status ACTIVE --output text --query 'taskDefinitionArns[]' \
  | tr '\t' '\n' | tail -10 | while read TD; do
  aws ecs describe-task-definition --task-definition "$TD" \
    --query 'taskDefinition.[family,revision,cpu,memory,networkMode,requiresCompatibilities[0]]' \
    --output text
done | column -t
```

## Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")

echo "=== CPU & Memory Utilization per Service ==="
for CLUSTER in $(aws ecs list-clusters --output text --query 'clusterArns[]' | tr '\t' '\n'); do
  CLUSTER_NAME=$(echo "$CLUSTER" | rev | cut -d'/' -f1 | rev)
  for SVC in $(aws ecs list-services --cluster "$CLUSTER" --launch-type FARGATE --output text --query 'serviceArns[]' | tr '\t' '\n'); do
    SVC_NAME=$(echo "$SVC" | rev | cut -d'/' -f1 | rev)
    {
      CPU=$(aws cloudwatch get-metric-statistics --namespace AWS/ECS --metric-name CPUUtilization \
        --dimensions Name=ClusterName,Value="$CLUSTER_NAME" Name=ServiceName,Value="$SVC_NAME" \
        --start-time "$START" --end-time "$END" --period 604800 --statistics Average Maximum \
        --output text --query 'Datapoints[0].[Average,Maximum]')
      MEM=$(aws cloudwatch get-metric-statistics --namespace AWS/ECS --metric-name MemoryUtilization \
        --dimensions Name=ClusterName,Value="$CLUSTER_NAME" Name=ServiceName,Value="$SVC_NAME" \
        --start-time "$START" --end-time "$END" --period 604800 --statistics Average Maximum \
        --output text --query 'Datapoints[0].[Average,Maximum]')
      printf "%s/%s\tCPU:%s\tMEM:%s\n" "$CLUSTER_NAME" "$SVC_NAME" "$CPU" "$MEM"
    } &
  done
done
wait

echo ""
echo "=== Auto Scaling Policies ==="
for CLUSTER in $(aws ecs list-clusters --output text --query 'clusterArns[]' | tr '\t' '\n'); do
  CLUSTER_NAME=$(echo "$CLUSTER" | rev | cut -d'/' -f1 | rev)
  for SVC in $(aws ecs list-services --cluster "$CLUSTER" --launch-type FARGATE --output text --query 'serviceArns[]' | tr '\t' '\n'); do
    SVC_NAME=$(echo "$SVC" | rev | cut -d'/' -f1 | rev)
    aws application-autoscaling describe-scaling-policies \
      --service-namespace ecs \
      --resource-id "service/${CLUSTER_NAME}/${SVC_NAME}" \
      --query 'ScalingPolicies[].[ResourceId,PolicyName,PolicyType]' \
      --output text 2>/dev/null
  done
done | column -t

echo ""
echo "=== Container Health Checks ==="
for CLUSTER in $(aws ecs list-clusters --output text --query 'clusterArns[]' | tr '\t' '\n'); do
  for TASK in $(aws ecs list-tasks --cluster "$CLUSTER" --launch-type FARGATE --output text --query 'taskArns[]' | tr '\t' '\n' | head -10); do
    aws ecs describe-tasks --cluster "$CLUSTER" --tasks "$TASK" \
      --query 'tasks[].containers[].[name,lastStatus,healthStatus]' --output text 2>/dev/null
  done
done | column -t
```

## Output Format

```
AWS FARGATE ANALYSIS
=====================
Cluster/Service        Tasks  CPU-Avg  CPU-Max  Mem-Avg  Mem-Max  Scaling
─────────────────────────────────────────────────────────────────────────
prod/web-api           3      25.4%    78.2%    45.1%    62.3%    target-tracking
prod/worker            2      65.2%    92.1%    78.0%    85.4%    step-scaling
staging/web-api        1      5.1%     12.0%    20.5%    25.0%    none

Clusters: 2 | Services: 5 | Tasks: 8 running
Platform: 1.4.0 | Health: 8/8 containers HEALTHY
```

## Safety Rules

- **Read-only**: Only use `list-*`, `describe-*`, and CloudWatch queries
- **Never stop tasks**, update services, or modify scaling without confirmation
- **Parallel execution**: Use background jobs for multi-service metric queries
- **Costs**: Large clusters with many services may incur CloudWatch API costs

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

