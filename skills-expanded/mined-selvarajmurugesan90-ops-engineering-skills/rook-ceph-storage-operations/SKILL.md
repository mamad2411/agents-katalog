---
name: rook-ceph-storage-operations
description: >
  Deploys and operates Rook as the Kubernetes operator managing a Ceph
  storage cluster in-cluster — the `CephCluster` CRD, OSD device
  discovery/placement, and exposing block (RBD), shared filesystem
  (CephFS), and object (RGW/S3-compatible) storage as Kubernetes
  StorageClasses. Use when a user asks to "install Rook-Ceph," "set up a
  CephCluster on Kubernetes," "create a Ceph block/object/filesystem
  StorageClass," "add OSD devices to a Rook cluster," or "provide
  persistent storage for stateful workloads without a cloud provider's
  managed disk service."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Rook-Ceph Storage Operations

## Purpose

Rook is a Kubernetes operator that turns raw block devices attached to
cluster nodes into a fully-managed Ceph cluster, then exposes that
cluster's storage back to Kubernetes as ordinary StorageClasses — giving
on-prem or bare-metal clusters the same self-service, dynamically
provisioned persistent storage that cloud providers offer natively via
EBS/Persistent Disk/managed disks. This matters operationally because
Ceph itself is a complex, stateful distributed system (OSDs, monitors,
managers, placement groups, CRUSH maps); Rook's value is collapsing that
operational surface into a handful of Kubernetes CRDs (`CephCluster`,
`CephBlockPool`, `CephFilesystem`, `CephObjectStore`) that are
declarative and GitOps-friendly, at the cost of still needing to
understand what Ceph is doing underneath when something goes wrong. This
skill covers deploying and configuring Rook-managed Ceph for production
use; validating that the resulting cluster is actually healthy before
depending on it is
[rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md)'s
job, and comparing this approach against the simpler
[longhorn-storage-configuration](../longhorn-storage-configuration/SKILL.md)
alternative is covered there.

## When to use

- Standing up persistent, dynamically-provisioned storage on a
  bare-metal or on-prem Kubernetes cluster with no cloud block-storage
  service available.
- Deciding OSD device placement and count per node for a new
  `CephCluster`.
- Creating block (RBD), shared-filesystem (CephFS), or S3-compatible
  object (RGW) storage classes for different workload storage needs
  within the same underlying Ceph cluster.
- Scaling Ceph capacity by adding nodes/devices to an existing
  Rook-managed cluster.
- Deciding replication (replica count) or erasure-coding policy for a
  storage pool based on the durability/capacity tradeoff a workload
  needs.
- Migrating workloads that need `ReadWriteMany` volumes (shared
  filesystem) onto CephFS-backed storage.

## Prerequisites & environment

- Kubernetes ≥ 1.26 and Rook ≥ v1.14 (check the Rook/Ceph/Kubernetes
  compatibility matrix in Rook's release notes before upgrading either
  component independently — Rook version compatibility with a given
  Ceph release is not automatic).
- Raw, unformatted block devices (or free disk space in an existing
  volume group, or explicit directories, though raw devices are
  strongly preferred) available on at least 3 nodes for meaningful
  replication — Ceph's placement-group/CRUSH design assumes failure
  domains, and fewer than 3 nodes fundamentally limits durability
  options.
- Sufficient dedicated CPU/RAM per node running OSDs — each OSD
  process needs headroom (roughly 1-2 vCPU and 2-4GiB RAM as a rough
  starting point per OSD, scaling with device size and I/O load); do
  not co-locate OSDs on nodes already tightly resource-constrained by
  workload pods.
- The Rook Ceph Helm chart or raw operator manifests, plus `kubectl`/
  Helm access with permission to create cluster-scoped CRDs and
  privileged DaemonSets (Rook's OSD pods require host-level device
  access).
- A decision on storage strategy already made relative to
  [longhorn-storage-configuration](../longhorn-storage-configuration/SKILL.md)
  — Rook-Ceph is the right choice when object storage (S3-compatible
  RGW) or CephFS shared filesystems are needed alongside block storage;
  Longhorn is simpler when only replicated block storage is required.

## Step-by-step guidance

1. **Install the Rook operator** (Helm, the recommended path):
   ```bash
   helm repo add rook-release https://charts.rook.io/release
   helm install --create-namespace --namespace rook-ceph rook-ceph rook-release/rook-ceph --version v1.14.9
   ```
   Confirm the operator pod is `Running` before proceeding —
   `kubectl -n rook-ceph get pods -l app=rook-ceph-operator`.

2. **Define the `CephCluster`**, specifying node/device selection
   explicitly rather than letting Rook opportunistically claim every
   unformatted device it finds cluster-wide:
   ```yaml
   apiVersion: ceph.rook.io/v1
   kind: CephCluster
   metadata:
     name: rook-ceph
     namespace: rook-ceph
   spec:
     cephVersion:
       image: quay.io/ceph/ceph:v18.2.4
     dataDirHostPath: /var/lib/rook
     mon:
       count: 3
       allowMultiplePerNode: false
     mgr:
       count: 2
     dashboard:
       enabled: true
       ssl: true
     storage:
       useAllNodes: false
       useAllDevices: false
       nodes:
         - name: "worker-1"
           devices: [{ name: "sdb" }]
         - name: "worker-2"
           devices: [{ name: "sdb" }]
         - name: "worker-3"
           devices: [{ name: "sdb" }]
     resources:
       osd: { requests: { cpu: "1", memory: "4Gi" }, limits: { memory: "4Gi" } }
       mon: { requests: { cpu: "500m", memory: "1Gi" } }
   ```
   `mon.count: 3` (odd, for quorum, same principle as
   [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md))
   is the minimum for production; explicit `storage.nodes`/`devices`
   avoids Rook accidentally wiping a device that happens to look
   unformatted but is actually in use.

3. **Wait for the cluster to reach `HEALTH_OK`** before creating any
   pools or StorageClasses on top of it:
   ```bash
   kubectl -n rook-ceph get cephcluster rook-ceph -o jsonpath='{.status.ceph.health}'
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph status
   ```
   (The `rook-ceph-tools` deployment, deployed separately, provides a
   `ceph`/`rbd`/`radosgw-admin` CLI shell inside the cluster — see
   [rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md)
   for the full health-check workflow.)

4. **Create a block pool and StorageClass** for RWO block storage
   (the most common case — databases, most stateful workloads):
   ```yaml
   apiVersion: ceph.rook.io/v1
   kind: CephBlockPool
   metadata:
     name: replicapool
     namespace: rook-ceph
   spec:
     failureDomain: host
     replicated:
       size: 3
   ---
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: rook-ceph-block
   provisioner: rook-ceph.rbd.csi.ceph.com
   parameters:
     clusterID: rook-ceph
     pool: replicapool
     imageFormat: "2"
     imageFeatures: layering
     csi.storage.k8s.io/fstype: ext4
     csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
     csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
     csi.storage.k8s.io/node-stage-secret-name: rook-csi-rbd-node
     csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
   reclaimPolicy: Delete
   allowVolumeExpansion: true
   ```
   `failureDomain: host` ensures the 3 replicas land on 3 different
   nodes, not 3 devices on the same node — set to `osd` only on
   single-node test clusters where host-level failure domains are
   meaningless.

5. **Create a CephFS shared filesystem** when a workload needs
   `ReadWriteMany` (multiple pods, same volume, e.g. a shared media
   library or CI cache):
   ```yaml
   apiVersion: ceph.rook.io/v1
   kind: CephFilesystem
   metadata:
     name: shared-fs
     namespace: rook-ceph
   spec:
     metadataPool: { replicated: { size: 3 } }
     dataPools:
       - { name: data0, replicated: { size: 3 } }
     metadataServer: { activeCount: 1, activeStandby: true }
   ---
   apiVersion: storage.k8s.io/v1
   kind: StorageClass
   metadata:
     name: rook-cephfs
   provisioner: rook-ceph.cephfs.csi.ceph.com
   parameters:
     clusterID: rook-ceph
     fsName: shared-fs
     pool: shared-fs-data0
     csi.storage.k8s.io/provisioner-secret-name: rook-csi-cephfs-provisioner
     csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
     csi.storage.k8s.io/node-stage-secret-name: rook-csi-cephfs-node
     csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
   reclaimPolicy: Delete
   ```

6. **Create an object store (S3-compatible RGW)** when workloads need
   an object API rather than a mounted filesystem/block device:
   ```yaml
   apiVersion: ceph.rook.io/v1
   kind: CephObjectStore
   metadata:
     name: object-store
     namespace: rook-ceph
   spec:
     metadataPool: { replicated: { size: 3 } }
     dataPool: { erasureCoded: { dataChunks: 2, codingChunks: 1 } }
     preservePoolsOnDelete: false
     gateway:
       port: 80
       instances: 2
   ```
   Expose it to clients with a `CephObjectStoreUser` (issues S3
   access/secret key pairs stored as a Kubernetes Secret Rook
   generates — never hand-write these keys into a manifest):
   ```yaml
   apiVersion: ceph.rook.io/v1
   kind: CephObjectStoreUser
   metadata:
     name: app-user
     namespace: rook-ceph
   spec:
     store: object-store
     displayName: "app-user"
   ```

7. **Scale capacity by adding nodes/devices to `CephCluster.spec.storage.nodes`**
   rather than replacing the whole cluster — Rook detects the change,
   provisions new OSDs, and Ceph's CRUSH algorithm rebalances data
   across the expanded device set automatically. Expect a rebalancing
   period with elevated I/O; schedule large expansions during
   lower-traffic windows.

8. **Set explicit resource requests/limits on `mon`, `mgr`, and `osd`
   pods** in `CephCluster.spec.resources` — an OSD pod OOM-killed under
   default (unbounded) limits during a rebalance is a common
   destabilizing event that's easy to prevent with sane requests.

## Best practices

- Use raw block devices for OSDs, not files/loopback devices or
  directories on an existing filesystem — file-based OSDs have
  materially worse performance and are only appropriate for
  throwaway test clusters.
- Keep `mon.count` at 3 (or 5 for larger clusters) and spread monitors
  across failure domains (`allowMultiplePerNode: false`) — losing mon
  quorum is Ceph's equivalent of etcd losing quorum: the whole cluster
  stops serving I/O, not just the affected component.
- Choose `failureDomain: host` (not `osd`) for replicated pools in any
  multi-node cluster, so a single node failure can't take out multiple
  replicas of the same object.
- Prefer replication (`replicated.size: 3`) for latency-sensitive block
  workloads and erasure coding for large, less latency-sensitive object
  data — erasure coding is more storage-efficient but has higher
  recovery/rebuild cost per failure.
- Enable the Ceph dashboard (`spec.dashboard.enabled: true`) and wire
  its metrics into
  [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  rather than relying only on `ceph status` run ad hoc during
  incidents.
- Deploy the `rook-ceph-tools` pod in every environment running Ceph —
  it's the primary interface for the health checks in
  [rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md)
  and for any manual `ceph`/`rbd` diagnostic command.
- Never let `reclaimPolicy: Delete` surprise someone on a StorageClass
  backing genuinely important data — set `Retain` for pools where an
  accidental PVC deletion should not also delete the underlying Ceph
  image/data.

## Common pitfalls

- **Symptom:** `CephCluster` never reaches `HEALTH_OK`; OSD pods are
  stuck `Pending` or `CrashLoopBackOff`.
  **Fix:** Usually a device selection problem — check
  `kubectl -n rook-ceph logs -l app=rook-ceph-operator` for "no
  available devices," which means the specified device already has a
  filesystem/partition table Rook won't overwrite by default (by
  design, to avoid destroying data). Wipe the device explicitly and
  intentionally (`sgdisk --zap-all /dev/sdb` on the target node, only
  after confirming it holds no needed data) before retrying, rather
  than changing device selectors to "make the error go away."

- **Symptom:** PVCs using a Rook StorageClass stay `Pending` indefinitely
  with no clear error in `kubectl describe pvc`.
  **Fix:** Check the CSI provisioner pods
  (`kubectl -n rook-ceph get pods -l app=csi-rbdplugin-provisioner`) for
  crash-looping or a missing/misnamed
  `csi.storage.k8s.io/provisioner-secret-name` in the StorageClass —
  the CSI secrets are auto-generated by Rook per pool/filesystem and
  must match exactly, and a typo here fails silently at the CSI layer
  rather than producing an obvious StorageClass-level error.

- **Symptom:** Deleting a `CephBlockPool` or `CephFilesystem` also
  deletes all the data in it with no confirmation prompt.
  **Fix:** This is a destructive action — Rook honors
  `preservePoolsOnDelete` (object stores) and `spec.deletionPolicy` on
  `CephCluster`/pool CRDs in more recent Rook versions. Set them
  explicitly (`preservePoolsOnDelete: true`, or a deletion policy of
  `retain`) on any pool holding real data, and always confirm no PVCs
  still reference a pool before deleting it — treat pool/filesystem
  deletion with the same caution as `terraform destroy` in
  [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md).

- **Symptom:** A single-node or 2-node test cluster's `CephCluster`
  reports `HEALTH_WARN` with placement groups stuck `undersized` or
  `degraded` indefinitely.
  **Fix:** A `replicated.size: 3` pool structurally cannot achieve full
  health with fewer than 3 failure domains (nodes, if
  `failureDomain: host`) — either add nodes, or explicitly set a lower
  replica size (`size: 1` or `2`) understanding the reduced durability,
  for non-production clusters; don't leave production pools configured
  for more replicas than the cluster topology can satisfy.

- **Symptom:** OSD pods get OOM-killed repeatedly during a large data
  rebalance after adding capacity.
  **Fix:** Default/unset resource limits on `osd` pods let a rebalance's
  memory spike exceed available node memory. Set explicit
  `resources.osd.limits.memory` with real headroom (Ceph's own sizing
  guidance scales roughly with OSD count and device size), and consider
  throttling recovery (`osd_recovery_max_active`,
  `osd_max_backfills` in the Ceph config overrides) to spread the
  rebalance's resource impact over a longer window instead of pursuing
  the fastest possible convergence.

## Worked example

**Scenario:** Stand up Rook-Ceph across 3 worker nodes each with one
free 500GiB block device, then provide both block storage for a
PostgreSQL StatefulSet and a shared CephFS volume for a CI artifact
cache.

```bash
helm repo add rook-release https://charts.rook.io/release
helm install --create-namespace --namespace rook-ceph rook-ceph rook-release/rook-ceph --version v1.14.9
```

```yaml
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata: { name: rook-ceph, namespace: rook-ceph }
spec:
  cephVersion: { image: quay.io/ceph/ceph:v18.2.4 }
  dataDirHostPath: /var/lib/rook
  mon: { count: 3 }
  mgr: { count: 2 }
  dashboard: { enabled: true, ssl: true }
  storage:
    useAllNodes: false
    useAllDevices: false
    nodes:
      - { name: "worker-1", devices: [{ name: "sdb" }] }
      - { name: "worker-2", devices: [{ name: "sdb" }] }
      - { name: "worker-3", devices: [{ name: "sdb" }] }
```

```bash
kubectl -n rook-ceph get cephcluster rook-ceph -o jsonpath='{.status.ceph.health}'
# HEALTH_OK
```

```yaml
apiVersion: ceph.rook.io/v1
kind: CephBlockPool
metadata: { name: replicapool, namespace: rook-ceph }
spec: { failureDomain: host, replicated: { size: 3 } }
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata: { name: rook-ceph-block }
provisioner: rook-ceph.rbd.csi.ceph.com
parameters:
  clusterID: rook-ceph
  pool: replicapool
  imageFormat: "2"
  imageFeatures: layering
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-rbd-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
reclaimPolicy: Retain
allowVolumeExpansion: true
```

`postgres-pvc.yaml` (excerpt): `storageClassName: rook-ceph-block`,
`accessModes: [ReadWriteOnce]`. `reclaimPolicy: Retain` is deliberately
chosen here (not the earlier example's `Delete`) since this pool backs
a production database — an accidental PVC deletion won't also delete
the underlying Ceph RBD image.

CephFS for the CI cache, mounted `ReadWriteMany` by multiple concurrent
CI runner pods:
```yaml
apiVersion: ceph.rook.io/v1
kind: CephFilesystem
metadata: { name: ci-cache-fs, namespace: rook-ceph }
spec:
  metadataPool: { replicated: { size: 3 } }
  dataPools: [{ name: data0, replicated: { size: 3 } }]
  metadataServer: { activeCount: 1, activeStandby: true }
```

## Cross-references

- [rook-ceph-configuration-validation](../rook-ceph-configuration-validation/SKILL.md) — validating `ceph status`/OSD placement/PG health before trusting this cluster for production.
- [longhorn-storage-configuration](../longhorn-storage-configuration/SKILL.md) — a simpler block-storage-only alternative when object storage and CephFS aren't required.
- [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md) — the same quorum/failure-domain reasoning applied to etcd rather than Ceph monitors.
- [cloud-native-storage-strategy](../../../cloud/skills/cloud-native-storage-strategy/SKILL.md) — broader decision framework for choosing in-cluster storage (Rook/Longhorn) vs. cloud-managed storage.
- [velero-backup-and-restore](../../../observability-and-platform-extras/skills/velero-backup-and-restore/SKILL.md) — backing up PVC data (including Rook-backed volumes) at the application/workload level.
- [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md) — scraping the Ceph dashboard/mgr Prometheus exporter for ongoing capacity and health monitoring.
