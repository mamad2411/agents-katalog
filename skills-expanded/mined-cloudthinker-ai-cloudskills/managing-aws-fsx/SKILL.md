---
name: managing-aws-fsx
description: |
  Use when working with Aws Fsx — aWS FSx file system management and health
  analysis. Covers FSx for Lustre, Windows File Server, NetApp ONTAP, and
  OpenZFS file systems, volumes, backups, data repository associations, and
  storage capacity metrics. Use when inspecting FSx file systems, debugging
  performance issues, reviewing backup configurations, or analyzing storage
  utilization.
connection_type: aws
preload: false
---

# AWS FSx Management Skill

Analyze and manage AWS FSx file systems across all types (Lustre, Windows, ONTAP, OpenZFS).

## MANDATORY: Discovery-First Pattern

**Always list file systems before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash
export AWS_PAGER=""

echo "=== FSx File Systems ==="
aws fsx describe-file-systems --output text \
  --query 'FileSystems[].[FileSystemId,FileSystemType,Lifecycle,StorageCapacity,StorageType,DNSName]' | head -20

echo ""
echo "=== FSx Volumes ==="
aws fsx describe-volumes --output text \
  --query 'Volumes[].[VolumeId,Name,VolumeType,Lifecycle,FileSystemId]' 2>/dev/null | head -20

echo ""
echo "=== Storage Virtual Machines (ONTAP) ==="
aws fsx describe-storage-virtual-machines --output text \
  --query 'StorageVirtualMachines[].[StorageVirtualMachineId,Name,Lifecycle,FileSystemId]' 2>/dev/null | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
export AWS_PAGER=""

END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")
START_TIME=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")

echo "=== File System Details ==="
for fs_id in $(aws fsx describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  aws fsx describe-file-systems --file-system-ids "$fs_id" --output text \
    --query 'FileSystems[].[FileSystemId,FileSystemType,StorageCapacity,Lifecycle,SubnetIds[0],VpcId]' &
done
wait

echo ""
echo "=== FSx Backups ==="
aws fsx describe-backups --output text \
  --query 'Backups[].[BackupId,FileSystemId,Type,Lifecycle,CreationTime]' | head -15

echo ""
echo "=== Data Repository Associations (Lustre) ==="
aws fsx describe-data-repository-associations --output text \
  --query 'Associations[].[AssociationId,FileSystemId,Lifecycle,DataRepositoryPath,FileSystemPath]' 2>/dev/null | head -10

echo ""
echo "=== Data Repository Tasks ==="
aws fsx describe-data-repository-tasks --output text \
  --query 'DataRepositoryTasks[:5].[TaskId,FileSystemId,Lifecycle,Type,StartTime]' 2>/dev/null

echo ""
echo "=== Storage Metrics ==="
for fs_id in $(aws fsx describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  {
    free_storage=$(aws cloudwatch get-metric-statistics --namespace AWS/FSx --metric-name FreeStorageCapacity \
      --dimensions Name=FileSystemId,Value="$fs_id" \
      --start-time "$START_TIME" --end-time "$END_TIME" --period 604800 --statistics Average \
      --output text --query 'Datapoints[0].Average')
    printf "%s\tFreeStorage:%s\n" "$fs_id" "${free_storage:-N/A}"
  } &
done
wait

echo ""
echo "=== File System Tags ==="
for fs_id in $(aws fsx describe-file-systems --output text --query 'FileSystems[].FileSystemId'); do
  aws fsx describe-file-systems --file-system-ids "$fs_id" --output text \
    --query "FileSystems[].Tags[?Key!='aws:cloudformation:stack-id'].[\"$fs_id\",Key,Value]" 2>/dev/null &
done
wait | head -15
```

## Output Format

- Target ≤50 lines per output
- Use `--output text --query` for all commands
- Tab-delimited fields: FileSystemId, Type, StorageCapacity, Lifecycle
- Convert storage values to GB/TB with awk when appropriate
- Never dump full file system configurations -- extract key fields only

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

- **File system types**: LUSTRE, WINDOWS, ONTAP, OPENZFS -- each has different APIs and metrics
- **Lifecycle states**: AVAILABLE, CREATING, FAILED, DELETING, MISCONFIGURED, UPDATING -- only AVAILABLE is healthy
- **ONTAP volumes**: ONTAP uses SVMs and volumes -- query volumes separately from file systems
- **Lustre S3 integration**: Data repository associations link Lustre to S3 -- check association lifecycle
- **Storage capacity**: FSx for Windows and ONTAP support storage capacity scaling -- check `AdministrativeActions`
- **Backup types**: AUTOMATIC (scheduled), USER_INITIATED, AWS_BACKUP -- check retention policies
- **Throughput capacity**: Separate from storage -- can be scaled independently on Windows and ONTAP
- **Multi-AZ**: Windows File Server supports Multi-AZ -- check `DeploymentType` (SINGLE_AZ vs MULTI_AZ)
