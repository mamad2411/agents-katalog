---
name: managing-alibaba-cloud
description: |
  Use when working with Alibaba Cloud — alibaba Cloud infrastructure management
  via the aliyun CLI. Covers ECS instances, RDS databases, VPCs, SLB load
  balancers, OSS storage, and billing. Use when managing Alibaba Cloud resources
  or checking infrastructure health.
connection_type: alibaba-cloud
preload: false
---

# Managing Alibaba Cloud

Manage Alibaba Cloud infrastructure using the `aliyun` CLI.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Account Info ==="
aliyun sts GetCallerIdentity 2>/dev/null | jq '{AccountId, Arn, UserId}'

echo ""
echo "=== ECS Instances ==="
aliyun ecs DescribeInstances --PageSize 50 2>/dev/null | jq -r '.Instances.Instance[] | "\(.InstanceId)\t\(.InstanceName)\t\(.RegionId)\t\(.InstanceType)\t\(.Status)\t\(.VpcAttributes.PrivateIpAddress.IpAddress[0] // "N/A")"' | head -30

echo ""
echo "=== RDS Instances ==="
aliyun rds DescribeDBInstances --PageSize 50 2>/dev/null | jq -r '.Items.DBInstance[] | "\(.DBInstanceId)\t\(.DBInstanceDescription)\t\(.Engine)\t\(.EngineVersion)\t\(.DBInstanceStatus)\t\(.DBInstanceClass)"' | head -20

echo ""
echo "=== VPCs ==="
aliyun vpc DescribeVpcs --PageSize 50 2>/dev/null | jq -r '.Vpcs.Vpc[] | "\(.VpcId)\t\(.VpcName)\t\(.RegionId)\t\(.CidrBlock)\t\(.Status)"' | head -10

echo ""
echo "=== SLB Load Balancers ==="
aliyun slb DescribeLoadBalancers --PageSize 50 2>/dev/null | jq -r '.LoadBalancers.LoadBalancer[] | "\(.LoadBalancerId)\t\(.LoadBalancerName)\t\(.Address)\t\(.LoadBalancerStatus)"' | head -10

echo ""
echo "=== OSS Buckets ==="
aliyun oss ls 2>/dev/null | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

INSTANCE_ID="${1:?ECS Instance ID required}"

echo "=== Instance Details ==="
aliyun ecs DescribeInstanceAttribute --InstanceId "$INSTANCE_ID" 2>/dev/null | jq '{
    InstanceId, InstanceName, Status, InstanceType,
    Cpu, Memory, RegionId, ZoneId,
    CreationTime, ExpiredTime,
    InternetMaxBandwidthIn, InternetMaxBandwidthOut
}'

echo ""
echo "=== Instance Monitoring (CPU, Network) ==="
aliyun cms DescribeMetricLast --Namespace acs_ecs_dashboard --MetricName CPUUtilization \
    --Dimensions "[{\"instanceId\":\"$INSTANCE_ID\"}]" 2>/dev/null | jq -r '.Datapoints | fromjson | .[] | "\(.timestamp)\tCPU: \(.Average)%"' | tail -10

echo ""
echo "=== Disks ==="
aliyun ecs DescribeDisks --InstanceId "$INSTANCE_ID" --PageSize 50 2>/dev/null | jq -r '.Disks.Disk[] | "\(.DiskId)\t\(.DiskName)\t\(.Size)GB\t\(.Category)\t\(.Status)"' | head -10

echo ""
echo "=== Security Groups ==="
aliyun ecs DescribeInstanceAttribute --InstanceId "$INSTANCE_ID" 2>/dev/null | jq -r '.SecurityGroupIds.SecurityGroupId[]' | while read sg; do
    aliyun ecs DescribeSecurityGroupAttribute --SecurityGroupId "$sg" 2>/dev/null | jq -r '.Permissions.Permission[] | "\(.IpProtocol)\t\(.PortRange)\t\(.SourceCidrIp)\t\(.Policy)\t\(.Direction)"' | head -10
done
```

## Output Format

```
INSTANCE_ID          NAME     REGION        TYPE            STATUS
i-abc123def456       web-01   cn-hangzhou   ecs.c6.large    Running
i-abc123ghi789       db-01    cn-hangzhou   ecs.r6.xlarge   Running
```

## Safety Rules
- Use read-only commands: `Describe*`, `List*`, `Get*`
- Never run `Delete*`, `Stop*`, `Release*` without explicit user confirmation
- Use jq for structured output parsing
- Limit output with `| head -N` to stay under 50 lines

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

