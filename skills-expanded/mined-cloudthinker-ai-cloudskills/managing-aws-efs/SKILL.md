---
name: managing-aws-efs
description: |
  Use when working with Aws Efs — aWS EFS file system management and performance
  analysis. Covers file system inventory, mount targets, access points,
  throughput modes, lifecycle policies, replication configurations, and storage
  metrics. Use when inspecting EFS file systems, debugging mount issues,
  reviewing performance settings, or optimizing storage costs.
connection_type: aws
preload: false
---

# AWS EFS Management Skill

Analyze and manage AWS EFS file systems, mount targets, and performance configurations.

## MANDATORY: Discovery-First Pattern

**Always list file systems before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== EFS File Systems ==="
aws efs describe-file-systems --output text \
  --query 'FileSystems[].[FileSystemId,Name,LifeCycleState,PerformanceMode,ThroughputMode,SizeInBytes.Value]'

echo ""
echo "=== Mount Targets ==="
for fs_id in $(aws efs describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  aws efs describe-mount-targets --file-system-id "$fs_id" --output text \
    --query "MountTargets[].[FileSystemId,MountTargetId,SubnetId,LifeCycleState,IpAddress]" &
done
wait

echo ""
echo "=== Access Points ==="
for fs_id in $(aws efs describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  aws efs describe-access-points --file-system-id "$fs_id" --output text \
    --query "AccessPoints[].[FileSystemId,AccessPointId,Name,LifeCycleState,RootDirectory.Path]" &
done
wait
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
START_TIME=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")

echo "=== Storage & Throughput Metrics ==="
for fs_id in $(aws efs describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  {
    total_io=$(aws cloudwatch get-metric-statistics --namespace AWS/EFS --metric-name TotalIOBytes \
      --dimensions Name=FileSystemId,Value="$fs_id" \
      --start-time "$START_TIME" --end-time "$END_TIME" --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    client_conns=$(aws cloudwatch get-metric-statistics --namespace AWS/EFS --metric-name ClientConnections \
      --dimensions Name=FileSystemId,Value="$fs_id" \
      --start-time "$START_TIME" --end-time "$END_TIME" --period 604800 --statistics Maximum \
      --output text --query 'Datapoints[0].Maximum')
    burst_balance=$(aws cloudwatch get-metric-statistics --namespace AWS/EFS --metric-name BurstCreditBalance \
      --dimensions Name=FileSystemId,Value="$fs_id" \
      --start-time "$START_TIME" --end-time "$END_TIME" --period 604800 --statistics Minimum \
      --output text --query 'Datapoints[0].Minimum')
    printf "%s\tTotalIO:%s\tMaxConns:%s\tMinBurstCredits:%s\n" "$fs_id" "${total_io:-0}" "${client_conns:-0}" "${burst_balance:-N/A}"
  } &
done
wait

echo ""
echo "=== Lifecycle Policies ==="
for fs_id in $(aws efs describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  aws efs describe-lifecycle-configuration --file-system-id "$fs_id" --output text \
    --query "LifecyclePolicies[].[\"$fs_id\",TransitionToIA,TransitionToPrimaryStorageClass]" 2>/dev/null &
done
wait

echo ""
echo "=== Replication Configurations ==="
for fs_id in $(aws efs describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  aws efs describe-replication-configurations --file-system-id "$fs_id" --output text \
    --query "Replications[].[SourceFileSystemId,Destinations[0].FileSystemId,Destinations[0].Region,Destinations[0].Status]" 2>/dev/null &
done
wait

echo ""
echo "=== Mount Target Security Groups ==="
for fs_id in $(aws efs describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  for mt_id in $(aws efs describe-mount-targets --file-system-id "$fs_id" --output text --query 'MountTargets[].MountTargetId'); do
    aws efs describe-mount-target-security-groups --mount-target-id "$mt_id" --output text \
      --query "SecurityGroups" 2>/dev/null | awk -v mt="$mt_id" '{print mt"\t"$0}' &
  done
done
wait

echo ""
echo "=== File System Policy ==="
for fs_id in $(aws efs describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  aws efs describe-file-system-policy --file-system-id "$fs_id" --output text \
    --query "'$fs_id has policy'" 2>/dev/null || echo "$fs_id no_policy" &
done
wait
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: FileSystemId, Name, PerformanceMode, Metric
- Convert SizeInBytes to human-readable format with awk
- Never dump full file system policies -- indicate presence only

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

- **Performance modes**: generalPurpose (default, lower latency) vs maxIO (higher throughput, higher latency) -- cannot be changed after creation
- **Throughput modes**: bursting (credits-based), provisioned (fixed), elastic (auto-scaling) -- check BurstCreditBalance for bursting
- **Burst credit depletion**: Bursting mode file systems can exhaust credits -- monitor BurstCreditBalance metric
- **Storage classes**: Standard and Infrequent Access (IA) -- lifecycle policies move files between classes
- **Mount target per AZ**: One mount target per AZ per file system -- ensure coverage for all AZs with EC2 instances
- **NFS port 2049**: Security groups on mount targets must allow TCP 2049 inbound
- **Encryption**: Encryption at rest is set at creation and cannot be changed -- check `Encrypted` field
