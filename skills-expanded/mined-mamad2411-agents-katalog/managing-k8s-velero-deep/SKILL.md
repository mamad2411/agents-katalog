---
name: managing-k8s-velero-deep
description: |
  Use when working with K8S Velero Deep — velero deep-dive management for
  Kubernetes backup and disaster recovery. Covers backup schedules, backup
  status, restore operations, backup storage locations, volume snapshot
  locations, backup item actions, and plugin health. Use when auditing backup
  coverage, debugging backup failures, reviewing restore operations, or
  validating disaster recovery configurations.
connection_type: k8s
preload: false
---

# Velero Deep-Dive Skill

Deep analysis of Velero backups, schedules, restores, and disaster recovery configurations.

## MANDATORY: Discovery-First Pattern

**Always check Velero installation and storage locations before inspecting backups.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Velero Deployment ==="
kubectl get deployment velero -n velero -o custom-columns='NAME:.metadata.name,READY:.status.readyReplicas,IMAGE:.spec.template.spec.containers[0].image' 2>/dev/null

echo ""
echo "=== Velero Pods ==="
kubectl get pods -n velero -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,RESTARTS:.status.containerStatuses[0].restartCount' 2>/dev/null

echo ""
echo "=== Backup Storage Locations ==="
kubectl get backupstoragelocations -n velero -o custom-columns='NAME:.metadata.name,PROVIDER:.spec.provider,BUCKET:.spec.objectStorage.bucket,PHASE:.status.phase,LAST_VALIDATED:.status.lastValidationTime' 2>/dev/null

echo ""
echo "=== Volume Snapshot Locations ==="
kubectl get volumesnapshotlocations -n velero -o custom-columns='NAME:.metadata.name,PROVIDER:.spec.provider' 2>/dev/null

echo ""
echo "=== Backup Schedules ==="
kubectl get schedules -n velero -o custom-columns='NAME:.metadata.name,SCHEDULE:.spec.schedule,LAST_BACKUP:.status.lastBackup,PHASE:.status.phase' 2>/dev/null

echo ""
echo "=== Installed Plugins ==="
kubectl get deployment velero -n velero -o jsonpath='{range .spec.template.spec.initContainers[*]}{.image}{"\n"}{end}' 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Recent Backups ==="
kubectl get backups -n velero --sort-by=.metadata.creationTimestamp -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,STARTED:.status.startTimestamp,COMPLETED:.status.completionTimestamp,EXPIRY:.status.expiration,ITEMS:.status.progress.totalItems' 2>/dev/null | tail -15

echo ""
echo "=== Failed Backups ==="
kubectl get backups -n velero -o json 2>/dev/null | jq -r '
  .items[] |
  select(.status.phase == "Failed" or .status.phase == "PartiallyFailed") |
  "\(.metadata.name)\t\(.status.phase)\t\(.status.failureReason // "see logs")"
' | head -10

echo ""
echo "=== Restore Operations ==="
kubectl get restores -n velero -o custom-columns='NAME:.metadata.name,BACKUP:.spec.backupName,STATUS:.status.phase,STARTED:.status.startTimestamp,COMPLETED:.status.completionTimestamp' 2>/dev/null | head -10

echo ""
echo "=== Backup Details (latest per schedule) ==="
for schedule in $(kubectl get schedules -n velero -o jsonpath='{.items[*].metadata.name}' 2>/dev/null); do
  kubectl get backups -n velero -l velero.io/schedule-name="$schedule" --sort-by=.metadata.creationTimestamp -o custom-columns='SCHEDULE:.metadata.labels.velero\.io/schedule-name,NAME:.metadata.name,STATUS:.status.phase,ITEMS:.status.progress.totalItems' 2>/dev/null | tail -2
done

echo ""
echo "=== Delete Backup Requests ==="
kubectl get deletebackuprequests -n velero -o custom-columns='NAME:.metadata.name,BACKUP:.spec.backupName,STATUS:.status.phase' 2>/dev/null | head -5

echo ""
echo "=== PV Backup Info ==="
kubectl get podvolumebackups -n velero -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,VOLUME:.spec.volume,NODE:.spec.node' 2>/dev/null | head -10

echo ""
echo "=== Velero Logs (errors) ==="
kubectl logs deployment/velero -n velero --tail=20 2>/dev/null | grep -i "error\|fail\|warn" | head -10
```

## Output Format

- Target ≤50 lines per output
- Use `-o custom-columns` for CRD listings
- Show backup success/failure rates as aggregated summary
- List latest backup per schedule for quick health check
- Never dump full backup specs -- show status and item counts only

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

- **BSL validation**: BackupStorageLocation must be Available -- Unavailable BSL blocks all backups
- **Plugin compatibility**: Velero plugins must match Velero version -- mismatched versions cause crashes
- **PV snapshots vs file-copy**: Volume snapshots are provider-specific; Restic/Kopia handles file-level backup
- **Namespace exclusion**: Default excludes `velero` namespace -- check `--exclude-namespaces` in schedules
- **TTL**: Backups have TTL (default 30 days) -- expired backups are automatically deleted
- **Partial failures**: PartiallyFailed means some items failed -- check backup logs with `velero backup logs`
- **Restore hooks**: Pre/post restore hooks can fail silently -- check restore logs for hook errors
- **CSI snapshots**: CSI snapshot support requires VolumeSnapshotClass and CSI plugin -- verify CSI driver compatibility
