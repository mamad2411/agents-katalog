---
name: velero-backup-and-restore
description: >
  Guides using Velero to back up and restore Kubernetes cluster state and
  persistent volumes — Backup/Restore/Schedule custom resources, volume
  snapshot integration via CSI snapshots or the restic/kopia file-system
  backup path, and cross-cluster or cross-account migration. Use when a
  user asks to "back up a Kubernetes namespace/cluster", "restore a
  namespace after accidental deletion", "schedule recurring cluster
  backups", "migrate workloads to a new cluster or AWS account", "back up
  persistent volumes with Velero", or "recover from a botched
  deployment/upgrade."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Velero Backup and Restore

## Purpose

Kubernetes has no built-in way to snapshot "everything a namespace or
cluster needs to exist" — object manifests, RBAC, CRDs, and the
persistent volume data behind stateful workloads are each backed up (if
at all) through different mechanisms. Velero unifies this: it snapshots
Kubernetes API objects to object storage (S3, Azure Blob, GCS, or
S3-compatible on-prem storage) and coordinates persistent volume data
capture either through the cloud provider's native CSI volume snapshot
API or through Velero's file-system backup path (restic, or its
successor kopia) for volumes without CSI snapshot support — then restores
both together, on the same cluster or a completely different one. That
makes Velero the tool of choice for three distinct but related jobs:
routine scheduled backup/restore of cluster state, disaster recovery of
a specific namespace or the whole cluster, and cross-cluster/cross-account
migration (e.g. moving a namespace from a dev cluster to a new AWS
account, or between Kubernetes distributions). This skill is Velero-
specific; for the broader RTO/RPO-driven DR pattern selection and backup
immutability strategy that Velero backups should fit into, see the
general disaster-recovery skill referenced below.

## When to use

- Setting up scheduled, recurring backups of a namespace or entire
  cluster's Kubernetes objects and persistent volumes.
- Recovering from an accidental `kubectl delete namespace`, a botched
  Helm upgrade/rollback, or a corrupted CRD/webhook that took down a
  workload.
- Migrating workloads between clusters (dev → staging, on-prem →
  cloud, or old cluster → new cluster during an EKS/AKS/GKE version
  upgrade) or between cloud accounts/subscriptions/projects.
- Testing whether existing backups actually restore, as part of DR
  runbook validation.
- Deciding between CSI volume snapshots and Velero's file-system
  backup (restic/kopia) path for a given storage class.
- Excluding specific namespaces/resources (e.g. `kube-system`,
  cert-manager-issued Secrets that shouldn't be duplicated) from backup
  scope.

## Prerequisites & environment

- Velero CLI and server (commonly Velero 1.14.x/1.15.x at the time of
  writing) installed into the cluster, matched to a compatible
  Kubernetes version — check the Velero compatibility matrix before
  upgrading either independently.
- Object storage backend already provisioned: an S3 bucket (or
  S3-compatible, e.g. MinIO on-prem) with a dedicated IAM
  role/policy scoped only to that bucket, an Azure Blob Storage
  container with a scoped service principal, or a GCS bucket with a
  scoped service account — never reuse a broad admin credential for the
  Velero storage backend.
- For volume data capture, decide per storage class:
  - **CSI volume snapshots** (preferred where supported): requires the
    `VolumeSnapshotClass` for the CSI driver in use (EBS CSI, Azure
    Disk CSI, PD CSI) and Velero's `velero-plugin-for-csi` installed.
  - **File-system backup (restic/kopia)**: works for any volume type
    (including hostPath-backed or non-CSI storage) but is slower and
    reads data at the file level; enabled via
    `--use-node-agent`/`--uploader-type=kopia` (kopia is the default
    uploader path from Velero 1.10+, replacing restic).
- Velero's own credentials (the object-storage IAM
  role/service-principal/service-account key) stored as a Kubernetes
  `Secret`, never inline in the `BackupStorageLocation`.
- Cluster-admin access to install Velero's CRDs
  (`Backup`, `Restore`, `Schedule`, `BackupStorageLocation`,
  `VolumeSnapshotLocation`) and its server Deployment/DaemonSet
  (node-agent for file-system backup runs as a DaemonSet).

## Step-by-step guidance

1. **Install Velero pointed at object storage**, scoped credentials
   only:
   ```bash
   velero install \
     --provider aws \
     --plugins velero/velero-plugin-for-aws:v1.10.0,velero/velero-plugin-for-csi:v0.7.1 \
     --bucket <VELERO_BACKUP_BUCKET> \
     --backup-location-config region=us-east-1 \
     --snapshot-location-config region=us-east-1 \
     --secret-file ./credentials-velero \
     --use-node-agent \
     --uploader-type=kopia
   ```
   `credentials-velero` contains only the scoped IAM access key for the
   backup bucket/role — reference it via a file path passed to
   `--secret-file`, never paste the key into a manifest or command
   history.

2. **Confirm the `BackupStorageLocation` is `Available`** before
   trusting any backup:
   ```bash
   velero backup-location get
   ```

3. **Take an on-demand backup of a namespace**, including PV data via
   CSI snapshots where the storage class supports it:
   ```bash
   velero backup create payments-ns-backup \
     --include-namespaces payments \
     --snapshot-volumes=true \
     --ttl 720h0m0s
   ```
   For volumes without CSI snapshot support, add
   `--default-volumes-to-fs-backup=true` to fall back to the
   kopia/restic file-system path for that backup.

4. **Exclude resources that shouldn't be duplicated or restored
   verbatim** — cluster-scoped resources, webhook configurations, or
   Secrets managed by an external system (e.g. cert-manager-issued TLS
   certs, or Secrets synced by External Secrets Operator that will
   regenerate on restore anyway):
   ```bash
   velero backup create payments-ns-backup \
     --include-namespaces payments \
     --exclude-resources secrets.certmanager.k8s.io \
     --snapshot-volumes=true
   ```

5. **Schedule recurring backups** with a `Schedule` custom resource
   instead of a cron job wrapping the CLI, so Velero manages retention
   (TTL) and backup naming consistently:
   ```yaml
   apiVersion: velero.io/v1
   kind: Schedule
   metadata:
     name: payments-ns-daily
     namespace: velero
   spec:
     schedule: "0 3 * * *"          # 03:00 daily, standard cron syntax
     template:
       includedNamespaces:
         - payments
       snapshotVolumes: true
       ttl: 720h0m0s                # 30-day retention
   ```

6. **Restore into the same or a different cluster.** Restoring while
   the original namespace/resources still exist will, by default,
   **skip** objects that already exist rather than overwrite them —
   but always verify this before running against a live cluster (see
   warning below):
   ```bash
   velero restore create payments-ns-restore \
     --from-backup payments-ns-backup \
     --include-namespaces payments
   ```
   To restore into a **different** namespace or cluster (migration use
   case), remap the namespace and target a cluster with its own
   `BackupStorageLocation` pointed at the same bucket:
   ```bash
   velero restore create payments-ns-restore-staging \
     --from-backup payments-ns-backup \
     --namespace-mappings payments:payments-staging
   ```

7. **⚠️ Warning — restore can overwrite live resources.** If a
   `Restore` targets a namespace where some objects still exist and
   have since been modified, Velero's default policy is to leave
   pre-existing objects alone (report them as skipped) for most
   resource types, but this is **not uniform across every resource
   kind and Velero version**, and `--existing-resource-policy=update`
   explicitly enables overwriting. **Never run a restore with
   `--existing-resource-policy=update` against a live, currently-serving
   namespace without first confirming in a dry run / staging restore
   what will change** — a restore that overwrites a live Deployment,
   ConfigMap, or Secret with stale backup content can cause an
   immediate outage or silently roll back a recent, intentional change.
   Prefer restoring into a new/renamed namespace first to inspect
   the result, then cut traffic over deliberately.

8. **Validate restores periodically**, not just on paper: restore the
   most recent scheduled backup into a scratch namespace or scratch
   cluster on a recurring basis and run a smoke test (pod readiness,
   a basic application health check) to confirm backups are actually
   restorable, not just "completed" per `velero backup describe`.

9. **For cross-account/cross-cluster migration**, set up a second
   `BackupStorageLocation` in the destination cluster pointed at the
   *same* bucket (with cross-account bucket policy/IAM trust configured
   if the destination is a different AWS account), then run the restore
   there — this is the same mechanism as disaster recovery, just
   targeting a different cluster deliberately rather than reactively.

## Best practices

- **Scope Velero's storage credentials narrowly** (one bucket, one
  IAM role/service principal) — Velero's credential is effectively a
  master key to every namespace's backed-up data; a broad credential
  turns a Velero compromise into a full-cluster data exposure.
- **Prefer CSI volume snapshots over file-system backup where
  supported** — CSI snapshots are faster, consistent at the block level,
  and don't require running a DaemonSet with node-level filesystem
  access; reserve kopia/restic file-system backup for storage classes
  without CSI snapshot support.
- **Set backup TTL deliberately per retention requirement**, not the
  default — a 30-day default TTL may not match a compliance-driven
  retention requirement for some workloads.
- **Exclude regenerable/externally-managed resources from backup
  scope** (cert-manager certificates, External Secrets Operator-synced
  Secrets, webhook-managed resources) so restores don't fight with the
  system that regenerates them.
- **Store backups in a different account/subscription/project than the
  cluster being backed up**, mirroring the general DR principle that a
  backup sharing a trust boundary with its source doesn't protect
  against an account-level compromise or accidental account deletion.
- **Validate restores on a schedule**, not only when a real incident
  forces the first real test — a `Completed` backup status only means
  the backup job ran, not that the data restores cleanly.
- **Restore into a new/scratch namespace first for migration or
  recovery scenarios**, verify the result, then cut traffic over —
  restoring directly on top of a live namespace risks the overwrite
  behavior flagged above.
- **Pin Velero server, CLI, and plugin versions together** and check
  the compatibility matrix before any upgrade — Velero's CRDs and
  plugin API can change between minor versions.

## Common pitfalls

- **Symptom:** A restore into a namespace that already has live,
  running workloads causes those workloads to revert to stale
  configuration or briefly go unready.
  **Fix:** The restore ran with `--existing-resource-policy=update`
  (or against a resource type where Velero's default behavior updates
  rather than skips) against a live namespace. Restore into a
  scratch/renamed namespace first, diff the result against what's
  currently live, and only promote deliberately — see the warning in
  step 7.

- **Symptom:** `velero backup describe` shows `Completed`, but
  restoring that backup later fails to bring back persistent volume
  data, or the restored PVs are empty.
  **Fix:** `--snapshot-volumes` was left at its default (or
  `--default-volumes-to-fs-backup` wasn't set) for a storage class
  without CSI snapshot support, so PV data was silently skipped.
  Confirm the storage class's CSI driver actually supports
  `VolumeSnapshotClass`, or explicitly enable file-system backup for
  volumes that don't.

- **Symptom:** Backups are taking increasingly long, and the node-agent
  DaemonSet pods show high CPU/memory usage.
  **Fix:** File-system backup (kopia/restic) is being used for volumes
  that do support CSI snapshots, doing much more expensive file-level
  reads than necessary. Move eligible storage classes to CSI volume
  snapshots and reserve file-system backup only for volumes that
  genuinely require it.

- **Symptom:** A scheduled `Schedule` backup silently stops running, and
  nobody notices until a restore is needed and the most recent backup
  is weeks old.
  **Fix:** No monitoring/alerting was wired to Velero's backup status
  (e.g. via the `velero_backup_last_successful_timestamp` metric
  scraped by Prometheus). Add an alerting rule against that metric — see
  [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
  — so a stalled schedule pages someone within hours, not weeks.

- **Symptom:** Cross-account migration restore fails with an access-
  denied error reading the backup from object storage.
  **Fix:** The destination cluster's `BackupStorageLocation` credential
  doesn't have cross-account read access to the source bucket (missing
  bucket policy / IAM trust relationship). Grant the destination
  account's Velero role explicit read access to the shared bucket (or
  copy the backup data to a bucket the destination account can already
  reach) before attempting the restore.

## Worked example

**Scenario:** An engineer runs `kubectl delete namespace payments`
against the wrong cluster context, deleting the `payments` namespace and
everything in it, including a PostgreSQL StatefulSet's persistent
volumes. A daily Velero `Schedule` backup exists.

1. Confirm the most recent backup and inspect it before restoring
   anything:
   ```bash
   velero backup get
   velero backup describe payments-ns-daily-20260728030000 --details
   ```
2. **Do not restore directly into a namespace named `payments`** if
   anything else in the cluster might already reference that name in a
   half-recreated state — restore first into a scratch namespace to
   verify integrity:
   ```bash
   velero restore create payments-recovery-check \
     --from-backup payments-ns-daily-20260728030000 \
     --namespace-mappings payments:payments-recovery-check
   ```
3. Confirm the PostgreSQL StatefulSet comes up healthy and data looks
   intact in the scratch namespace (connect and spot-check row counts
   against what's expected).
4. Once verified, restore into the real `payments` namespace (which no
   longer exists, so there's no live-overwrite risk in this specific
   case):
   ```bash
   velero restore create payments-ns-restore \
     --from-backup payments-ns-daily-20260728030000 \
     --include-namespaces payments
   ```
5. Confirm all Deployments/StatefulSets report `Ready` and persistent
   volumes are bound with data intact; clean up the scratch
   `payments-recovery-check` namespace once satisfied.
6. Follow up: add a validating admission policy or RBAC restriction
   limiting who can delete namespaces in this cluster, and add a
   Prometheus alert on `velero_backup_last_successful_timestamp` so a
   future failed/stalled schedule is caught immediately rather than
   discovered during the next incident.

## Cross-references

- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)
- [kubernetes-network-policy-zero-trust](../kubernetes-network-policy-zero-trust/SKILL.md)
- [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md)
