---
name: longhorn-storage-configuration
description: >
  Deploys and configures Longhorn as cloud-native distributed block
  storage for Kubernetes — StorageClass replica count, data locality,
  volume snapshot/backup targets, and node/disk scheduling — as a
  simpler alternative to Rook-Ceph when only replicated block storage
  (no object store, no shared filesystem) is needed. Use when a user
  asks to "install Longhorn," "set up replicated block storage on
  Kubernetes," "configure Longhorn volume snapshots/backups," "choose
  between Longhorn and Rook-Ceph," or "recover a Longhorn volume after a
  node failure."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Longhorn Storage Configuration

## Purpose

Longhorn is a Kubernetes-native distributed block storage system that
replicates each volume across multiple nodes at the storage layer
itself — no external Ceph cluster, no separate storage appliance —
making it markedly simpler to operate than
[rook-ceph-storage-operations](../rook-ceph-storage-operations/SKILL.md)
when a workload's only requirement is durable, replicated `ReadWriteOnce`
block storage. The tradeoff for that simplicity is scope: Longhorn does
not provide S3-compatible object storage or a POSIX shared filesystem
the way Ceph's RGW/CephFS do, and its per-volume replication model
(each volume's replicas live on distinct nodes, not on a cluster-wide
placement-group/CRUSH abstraction) is architecturally different from
Ceph's. This skill covers installing Longhorn, configuring replica
count/data locality/scheduling, and setting up snapshot/backup targets;
choosing between Longhorn and Rook-Ceph in the first place is covered in
the Best practices section below and in
[rook-ceph-storage-operations](../rook-ceph-storage-operations/SKILL.md)'s
Purpose section.

## When to use

- Providing dynamically-provisioned, replicated block storage on a
  bare-metal or on-prem cluster where object storage and shared
  filesystems aren't required.
- Choosing between Longhorn and Rook-Ceph for a new cluster's storage
  layer.
- Configuring a StorageClass's replica count or data-locality setting to
  balance durability against I/O latency for a specific workload.
- Setting up scheduled snapshots and off-cluster backups (to S3 or NFS)
  for Longhorn volumes.
- Recovering a volume after the node it was scheduled on fails, or
  rebuilding a degraded replica.
- Migrating stateful workloads that need only RWO block storage off a
  more operationally heavy Rook-Ceph deployment.

## Prerequisites & environment

- Kubernetes ≥ 1.25 and Longhorn ≥ v1.6 (check Longhorn's own release
  compatibility matrix — Longhorn moves its supported Kubernetes range
  forward fairly aggressively).
- `open-iscsi` (or the distro equivalent) installed and the `iscsid`
  service running on every node that will host Longhorn volumes —
  Longhorn's data path depends on iSCSI, and a missing/stopped `iscsid`
  is the most common install-time blocker.
- At least 3 nodes with free disk space for meaningful replication (the
  same failure-domain reasoning as etcd/Ceph: 3 replicas need at least
  3 independent nodes to actually protect against a single node
  failure).
- The Longhorn Helm chart or the official manifest, plus `kubectl`/Helm
  access with permission to create the `longhorn-system` namespace and
  its privileged DaemonSets (Longhorn's engine/replica processes need
  host-level block device and iSCSI access).
- A decided backup target (S3-compatible object storage or NFS) before
  going to production — Longhorn's built-in replication protects
  against node failure, but not against an accidentally deleted volume
  or a cluster-wide disaster, which only an off-cluster backup target
  covers.

## Step-by-step guidance

1. **Verify prerequisites cluster-wide before installing**:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.6.2/deploy/prerequisite/longhorn-iscsi-installation.yaml
   kubectl -n longhorn-system get pods -l app=longhorn-iscsi-installation
   ```
   Confirm every node's iSCSI installation pod completes successfully
   before proceeding — installing Longhorn itself on top of a node
   missing `open-iscsi` produces engine pods stuck `CrashLoopBackOff`
   with an unhelpful error.

2. **Install Longhorn** via Helm:
   ```bash
   helm repo add longhorn https://charts.longhorn.io
   helm install longhorn longhorn/longhorn --namespace longhorn-system --create-namespace --version 1.6.2
   kubectl -n longhorn-system get pods   # wait for all Running
   ```

3. **Define a StorageClass with an explicit replica count and data
   locality**, rather than accepting the chart's default for every
   workload uniformly:
   ```yaml
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: longhorn-replicated
   provisioner: driver.longhorn.io
   allowVolumeExpansion: true
   reclaimPolicy: Retain
   parameters:
     numberOfReplicas: "3"
     staleReplicaTimeout: "30"
     dataLocality: "best-effort"
     fromBackup: ""
   ```
   `dataLocality: best-effort` schedules one replica on the same node
   as the workload when possible (lower read latency) without making it
   a hard requirement; `strict-local` forces it (fastest, but the
   volume becomes unschedulable if that specific node is unavailable) —
   choose based on whether latency or scheduling flexibility matters
   more for the workload.

4. **Scope node/disk scheduling explicitly** for heterogeneous
   clusters (e.g. only some nodes have fast local NVMe) via node
   tags and the Longhorn UI/CRDs, rather than letting every volume
   schedule onto every node uniformly:
   ```yaml
   apiVersion: longhorn.io/v1beta2
   kind: Node
   metadata:
     name: worker-1
     namespace: longhorn-system
   spec:
     disks:
       nvme-disk:
         path: /var/lib/longhorn-nvme
         allowScheduling: true
         tags: ["fast"]
   ```
   Pair with a StorageClass parameter `diskSelector: "fast"` so
   latency-sensitive volumes land only on tagged fast-disk nodes.

5. **Configure a backup target** (S3-compatible or NFS) before any
   volume is considered production-ready — Longhorn's replication
   protects against a node failure, not against cluster-wide loss or an
   accidental volume deletion:
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: longhorn-backup-s3-secret
     namespace: longhorn-system
   type: Opaque
   stringData:
     AWS_ACCESS_KEY_ID: "${LONGHORN_BACKUP_ACCESS_KEY_ID}"
     AWS_SECRET_ACCESS_KEY: "${LONGHORN_BACKUP_SECRET_ACCESS_KEY}"
   ```
   ```bash
   kubectl -n longhorn-system patch settings.longhorn.io backup-target \
     --type=merge -p '{"value":"s3://longhorn-backups-<ACCOUNT_ID>@us-east-1/"}'
   kubectl -n longhorn-system patch settings.longhorn.io backup-target-credential-secret \
     --type=merge -p '{"value":"longhorn-backup-s3-secret"}'
   ```
   Never place the access key/secret directly in a StorageClass or
   ConfigMap — always reference a Kubernetes Secret, and source the
   Secret's values from your actual secrets manager rather than
   hardcoding them, per
   [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md).

6. **Schedule recurring snapshots and backups** via a `RecurringJob`
   rather than relying on manual, ad hoc backup runs:
   ```yaml
   apiVersion: longhorn.io/v1beta2
   kind: RecurringJob
   metadata:
     name: daily-backup
     namespace: longhorn-system
   spec:
     cron: "0 2 * * *"
     task: "backup"
     groups: ["default"]
     retain: 7
     concurrency: 2
   ```
   Attach the `RecurringJob` to volumes via the
   `recurring-job.longhorn.io/source: enabled` label/group mechanism on
   the PVC, or a StorageClass-level default group, so new volumes are
   covered automatically rather than needing to be manually opted in
   one at a time.

7. **Recover a volume after a node failure** by confirming the volume's
   remaining healthy replicas and letting Longhorn's manager reschedule
   the workload/rebuild automatically, verifying rather than assuming:
   ```bash
   kubectl -n longhorn-system get volumes.longhorn.io <volume-name> -o jsonpath='{.status.robustness}'
   kubectl -n longhorn-system get replicas.longhorn.io -l longhornvolume=<volume-name>
   ```
   `robustness: degraded` (one or more replicas down but the volume
   still serving I/O from remaining healthy replicas) is recoverable
   automatically once the failed node returns or Longhorn schedules a
   replacement replica elsewhere; `robustness: faulted` (no healthy
   replica remains) requires restoring from the most recent backup —
   see step 8.

8. **Restore a volume from a backup** when no healthy replica survives
   (all replicas were on failed/lost nodes, or a volume was accidentally
   deleted):
   > **Warning:** Restoring creates a new volume from the backup's
   > point-in-time state; any writes to the original volume after that
   > backup was taken are not recoverable this way. Confirm the backup's
   > timestamp against the actual data-loss window before restoring, and
   > restore into a new PVC name rather than overwriting anything that
   > might still hold newer (even if degraded/inaccessible) data.
   ```bash
   kubectl -n longhorn-system get backups.longhorn.io -l longhornvolume=<volume-name>
   ```
   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: restored-volume
     namespace: payments
   spec:
     accessModes: [ReadWriteOnce]
     storageClassName: longhorn-replicated
     resources: { requests: { storage: 20Gi } }
     dataSource:
       name: <volumesnapshot-name>
       kind: VolumeSnapshot
       apiGroup: snapshot.storage.k8s.io
   ```

## Best practices

- Choose Longhorn over Rook-Ceph when the requirement is purely
  replicated RWO block storage and operational simplicity matters more
  than the broader Ceph feature set (object storage, CephFS, erasure
  coding) — don't default to the heavier system when the lighter one
  fully covers the need.
- Set `numberOfReplicas: 3` (not the frequent default of 2) for
  anything production-facing — 2 replicas means losing one node already
  puts the volume at zero further tolerance, mirroring the etcd/Ceph
  quorum principle.
- Configure and *test* a backup target before considering any
  Longhorn-backed volume production-ready — replication alone does not
  protect against cluster-wide disaster, accidental deletion, or
  corruption that replicates to every replica identically.
- Use `dataLocality: best-effort`, not `disabled`, as the default for
  latency-sensitive workloads unless node-affinity flexibility is more
  important than read latency for that specific volume.
- Tag disks/nodes explicitly (`diskSelector`/`nodeSelector`) in any
  cluster with heterogeneous storage hardware, rather than letting
  Longhorn schedule replicas onto slow disks for a latency-sensitive
  workload by chance.
- Monitor Longhorn's own health via its Prometheus metrics
  (`longhorn_volume_robustness`, `longhorn_node_storage_usage_bytes`)
  through
  [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  rather than only checking the Longhorn UI reactively.

## Common pitfalls

- **Symptom:** Longhorn engine/replica pods are stuck
  `CrashLoopBackOff` immediately after install.
  **Fix:** Almost always a missing or stopped `iscsid` on one or more
  nodes — re-run the iSCSI prerequisite installation
  (`longhorn-iscsi-installation.yaml`) and confirm
  `systemctl status iscsid` is active on every node, not just the ones
  that appeared to install correctly initially.

- **Symptom:** A volume shows `robustness: degraded` for a long time
  after a node recovers from a brief outage, never returning to
  `healthy`.
  **Fix:** Check `kubectl -n longhorn-system get replicas.longhorn.io`
  for a replica stuck in a rebuilding or error state — a prolonged
  rebuild can be blocked by insufficient free disk space on the target
  node for the replacement replica, or a stale replica timeout setting
  too short/long for the actual rebuild time; check available disk
  space on candidate nodes before assuming the volume itself is broken.

- **Symptom:** A volume with `numberOfReplicas: 2` becomes `faulted`
  (no healthy replica) after a single node failure.
  **Fix:** Two replicas provide no tolerance once one is lost if the
  remaining replica's node also has any issue during the rebuild
  window — this is the expected (if painful) consequence of
  under-replicating a production volume. Restore from backup (step 8)
  for the immediate recovery, and change the StorageClass default to
  `numberOfReplicas: 3` going forward for anything at this criticality.

- **Symptom:** Backups appear to run successfully on schedule, but a
  test restore produces a volume that's missing recent data or fails to
  mount.
  **Fix:** This usually means the backup target's credentials or
  network path degraded silently (backups "succeeding" against a
  misconfigured/unreachable target can still report success in some
  failure modes, or point at the wrong bucket/path after a
  reconfiguration) — periodically perform an actual test restore (not
  just checking the "backup completed" status), the same discipline as
  the practice-restore guidance in
  [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md).

- **Symptom:** Someone deletes a PVC to "free up space" during
  cleanup, and the underlying Longhorn volume (and its replicas) is
  immediately and irreversibly deleted along with any data not yet
  backed up.
  **Fix:** This is a destructive action — set `reclaimPolicy: Retain`
  on any StorageClass backing data that matters, so a PVC deletion
  leaves the underlying volume/`PersistentVolume` intact for manual
  review rather than triggering immediate deletion, and confirm a
  recent backup exists before ever deleting a volume outright.

## Worked example

**Scenario:** Provide replicated block storage for a Redis cluster on a
5-node bare-metal cluster, with daily backups to S3, and validate
recovery after simulating a node failure.

```bash
kubectl apply -f https://raw.githubusercontent.com/longhorn/longhorn/v1.6.2/deploy/prerequisite/longhorn-iscsi-installation.yaml
helm repo add longhorn https://charts.longhorn.io
helm install longhorn longhorn/longhorn --namespace longhorn-system --create-namespace --version 1.6.2
```

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: { name: longhorn-redis }
provisioner: driver.longhorn.io
reclaimPolicy: Retain
allowVolumeExpansion: true
parameters:
  numberOfReplicas: "3"
  dataLocality: "best-effort"
```

```bash
kubectl -n longhorn-system patch settings.longhorn.io backup-target \
  --type=merge -p '{"value":"s3://longhorn-backups-example@us-east-1/"}'
kubectl -n longhorn-system patch settings.longhorn.io backup-target-credential-secret \
  --type=merge -p '{"value":"longhorn-backup-s3-secret"}'
```

```yaml
apiVersion: longhorn.io/v1beta2
kind: RecurringJob
metadata: { name: redis-daily-backup, namespace: longhorn-system }
spec: { cron: "30 1 * * *", task: "backup", groups: ["redis"], retain: 14 }
```

Redis's PVCs are labeled into the `redis` recurring-job group so the
nightly backup covers them automatically. To validate recovery, a
worker node is cordoned and powered off deliberately in a staging
cluster:
```bash
kubectl -n longhorn-system get volumes.longhorn.io -l longhornvolume=redis-data-0 -o jsonpath='{.status.robustness}'
# degraded
```
Within Longhorn's configured replica-rebuild window, a new replica is
scheduled on a healthy node and `robustness` returns to `healthy`
automatically — confirming the 3-replica configuration tolerates a
single node loss without needing to fall back to a backup restore at
all, which is the intended outcome for this failure class.

## Cross-references

- [rook-ceph-storage-operations](../rook-ceph-storage-operations/SKILL.md) — the heavier alternative when object storage or CephFS is also required, not just replicated block storage.
- [rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md) — analogous production-readiness health-check discipline, adapted here to Longhorn's `robustness`/replica model.
- [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md) — the same replica-count/quorum reasoning applied to etcd.
- [cloud-native-storage-strategy](../../../cloud/skills/cloud-native-storage-strategy/SKILL.md) — broader framework for choosing between in-cluster storage systems and cloud-managed storage.
- [secrets-management](../../../devsecops/skills/secrets-management/SKILL.md) — how the backup-target credentials referenced above should actually be sourced and rotated.
- [velero-backup-and-restore](../../../observability-and-platform-extras/skills/velero-backup-and-restore/SKILL.md) — namespace/application-level backup that can complement (not replace) Longhorn's volume-level backup target.
