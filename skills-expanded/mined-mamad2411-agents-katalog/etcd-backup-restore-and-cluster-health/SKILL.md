---
name: etcd-backup-restore-and-cluster-health
description: >
  Guides taking and verifying etcd snapshots (`etcdctl snapshot save`),
  restoring a Kubernetes cluster's control-plane state from a snapshot,
  and monitoring etcd cluster health — quorum, member status, disk fsync/
  backend commit latency, and DB size — on self-managed clusters
  (kubeadm, Cluster API, K3s with its default embedded etcd, on-prem). Use
  when a user asks to "back up etcd," "take an etcd snapshot," "restore
  etcd from a snapshot," "check etcd cluster health/quorum," "size disks
  for etcd," "diagnose slow etcd/high fsync latency," or "recover a
  Kubernetes cluster after losing the control plane."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# etcd Backup, Restore, and Cluster Health

## Purpose

Every Kubernetes distribution — kubeadm, Cluster API, K3s, OpenShift,
even the managed control planes of EKS/AKS/GKE under the hood — stores
all cluster state (every object, every Secret, every CRD instance) in
etcd, a single Raft-consensus key-value store. Nothing else in the
platform is more foundational or less forgiving of neglect: etcd has no
built-in application-level backup, quorum loss takes the entire API
server down (not just etcd), and a bad restore silently rolls back
*everything* in the cluster to the snapshot's point in time, live
Secrets and CRDs included. This skill covers the operational discipline
managed-Kubernetes users get for free but self-managed cluster operators
must build themselves: taking and verifying snapshots, restoring
correctly, and watching the handful of etcd-specific health signals
(quorum, disk fsync latency, DB size) that predict an outage before it
happens. It does not cover provisioning the cluster itself — see
[kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md)
— nor application-level backup of workload data, which is
[velero-backup-and-restore](../../../observability-and-platform-extras/skills/velero-backup-and-restore/SKILL.md)'s
job.

## When to use

- Standing up scheduled etcd snapshots for a self-managed cluster that
  currently has no backup story beyond "the cloud disk snapshot."
- Restoring a cluster's control plane after losing a majority of etcd
  members, corrupting the data directory, or needing to roll the whole
  cluster back to a known-good point in time.
- Diagnosing an API server that's slow or returning `etcdserver: request
  timed out` / `context deadline exceeded` errors that trace back to
  etcd rather than the API server itself.
- Sizing disks (IOPS, latency) for a new etcd deployment, or explaining
  why an existing etcd cluster on shared/network storage is unstable.
- Checking whether an etcd cluster currently has quorum and can tolerate
  losing another member before doing risky maintenance (node
  reboot, upgrade, certificate rotation).
- Investigating etcd DB size approaching its quota (`mvcc: database
  space exceeded`) or alarm-triggered read-only mode.

## Prerequisites & environment

- `etcdctl` matching the target etcd server version (etcd ≥ 3.5
  recommended; check `etcdctl version` against `etcd --version` on a
  member — a client/server major-version mismatch can silently fail or
  misparse output). Set `ETCDCTL_API=3` explicitly; v2 API defaults on
  older installs and produces different (incompatible) output/commands.
- TLS client certificates for etcd's peer/client API (kubeadm places
  these at `/etc/kubernetes/pki/etcd/{ca,server,peer,healthcheck-client}.{crt,key}`
  by default) — etcdctl needs `--cacert`, `--cert`, `--key` for any
  authenticated cluster.
- Root/sudo access on control-plane nodes to read the etcd data
  directory (`/var/lib/etcd` by default) and to stop/start the etcd
  static pod or systemd unit during a restore.
- Know your topology: **stacked etcd** (etcd runs as a static pod
  colocated with each control-plane node, the kubeadm default) vs.
  **external etcd** (a dedicated etcd cluster the API servers point to)
  — the restore mechanics below differ slightly in which service you
  stop/start.
- On managed Kubernetes (EKS/AKS/GKE), etcd is entirely provider-managed
  and **this skill does not apply** — there is no customer-accessible
  etcdctl endpoint; see
  [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md)
  for what is and isn't under your control there.

## Step-by-step guidance

1. **Take a snapshot on a schedule, not just before risky changes**:
   ```bash
   ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot-$(date +%Y%m%d%H%M%S).db \
     --endpoints=https://127.0.0.1:2379 \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
     --key=/etc/kubernetes/pki/etcd/healthcheck-client.key
   ```
   Snapshot against `127.0.0.1` (the local member), not a load-balanced
   endpoint — `snapshot save` streams the entire DB file over that
   connection, and pointing it at a VIP/LB risks the connection landing
   on a different member mid-stream on retry.

2. **Verify every snapshot immediately after taking it** — a corrupt or
   truncated snapshot file is worse than no backup, because it creates
   false confidence:
   ```bash
   ETCDCTL_API=3 etcdctl snapshot status /backup/etcd-snapshot-20260728120000.db -w table
   ```
   Confirm the reported `hash`, `revision`, and `total keys` look
   sane (non-zero, roughly matching expected cluster size) — a
   `0`-key or errored snapshot means the backup silently failed and
   needs immediate investigation, not a shrug.

3. **Ship snapshots off the node they were taken on**, to object storage
   or a separate host, on the same schedule as the snapshot itself —
   a snapshot sitting only on the control-plane node's local disk is
   lost in exactly the scenario (node/disk failure) it's meant to
   protect against:
   ```bash
   aws s3 cp /backup/etcd-snapshot-20260728120000.db \
     s3://<BACKUP_BUCKET>/etcd/$(hostname)/etcd-snapshot-20260728120000.db
   ```
   Retain enough history (e.g. hourly for 24h, daily for 30 days) to
   cover both "restore to five minutes ago" and "restore to before a
   slow-burning corruption was introduced last week" — see
   [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md)
   for RPO/retention design that applies here too.

4. **Automate snapshotting with a CronJob or systemd timer** rather than
   a person remembering to run it manually:
   ```yaml
   apiVersion: batch/v1
   kind: CronJob
   metadata:
     name: etcd-snapshot
     namespace: kube-system
   spec:
     schedule: "0 * * * *"
     jobTemplate:
       spec:
         template:
           spec:
             hostNetwork: true
             nodeSelector: { node-role.kubernetes.io/control-plane: "" }
             tolerations:
               - key: node-role.kubernetes.io/control-plane
                 effect: NoSchedule
             containers:
               - name: etcd-snapshot
                 image: registry.k8s.io/etcd:3.5.15-0
                 command: ["/bin/sh", "-c"]
                 args:
                   - >
                     etcdctl snapshot save /backup/etcd-$(date +%Y%m%d%H%M%S).db
                     --endpoints=https://127.0.0.1:2379
                     --cacert=/etc/kubernetes/pki/etcd/ca.crt
                     --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt
                     --key=/etc/kubernetes/pki/etcd/healthcheck-client.key
                 volumeMounts:
                   - { name: etcd-certs, mountPath: /etc/kubernetes/pki/etcd, readOnly: true }
                   - { name: backup, mountPath: /backup }
             restartPolicy: OnFailure
             volumes:
               - { name: etcd-certs, hostPath: { path: /etc/kubernetes/pki/etcd } }
               - { name: backup, hostPath: { path: /backup } }
   ```
   Follow the CronJob with a step (a sidecar container, or a separate
   scheduled job) that uploads the file off-node per step 3.

5. **Restore from a snapshot — a full control-plane recovery procedure,
   not a single command.**
   > **Warning:** Restoring etcd overwrites the *entire* cluster's
   > current state with the snapshot's point-in-time contents — every
   > object created, Secret rotated, or CRD instance reconciled after
   > the snapshot was taken is lost. Only restore when quorum is
   > genuinely unrecoverable (see step 7) or a deliberate rollback to a
   > known-good state is the intended outcome, and confirm this is
   > understood by whoever is asking for the restore before running it.
   ```bash
   # 1. Stop the kubelet and the etcd static pod/container on every control-plane node
   systemctl stop kubelet
   crictl ps -a | grep etcd   # find and stop the etcd container, or move
   mv /etc/kubernetes/manifests/etcd.yaml /tmp/etcd.yaml.bak

   # 2. Restore the snapshot into a fresh data directory (per member, with that member's own name/peer URLs)
   ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd-snapshot-20260728120000.db \
     --name=control-plane-1 \
     --initial-cluster="control-plane-1=https://10.0.1.10:2380,control-plane-2=https://10.0.1.11:2380,control-plane-3=https://10.0.1.12:2380" \
     --initial-cluster-token=etcd-cluster-restored \
     --initial-advertise-peer-urls=https://10.0.1.10:2380 \
     --data-dir=/var/lib/etcd-restored

   # 3. Point etcd's manifest at the restored data directory, then bring it back
   sed -i 's#/var/lib/etcd#/var/lib/etcd-restored#' /tmp/etcd.yaml.bak
   mv /tmp/etcd.yaml.bak /etc/kubernetes/manifests/etcd.yaml
   systemctl start kubelet
   ```
   Every member must restore with the **same snapshot file**, its own
   correct `--name`, and an identical `--initial-cluster` list —
   restoring members from different snapshots, or with mismatched
   cluster membership strings, produces a cluster that never reaches
   quorum.

6. **Verify the restored cluster before declaring it recovered**:
   ```bash
   ETCDCTL_API=3 etcdctl endpoint health --cluster -w table \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=... --key=...
   kubectl get nodes
   kubectl get pods -A | grep -v Running
   ```
   Confirm all expected members report healthy, the API server is
   reachable again, and workload state (deployments, pods) matches
   expectations for the snapshot's point in time — do not assume
   `etcdctl endpoint health` returning green means the whole cluster is
   fully recovered without also checking the API server and workloads.

7. **Monitor quorum and member health continuously, not just during
   incidents.** A cluster of `2n+1` members tolerates `n` failures —
   check current member count and status before any planned disruptive
   maintenance:
   ```bash
   ETCDCTL_API=3 etcdctl member list -w table \
     --endpoints=https://127.0.0.1:2379 --cacert=... --cert=... --key=...
   ETCDCTL_API=3 etcdctl endpoint status --cluster -w table \
     --endpoints=https://127.0.0.1:2379,https://127.0.0.1:2380 --cacert=... --cert=... --key=...
   ```
   A 3-member cluster already missing one member has **zero** further
   tolerance — losing a second member loses quorum and takes the whole
   API server down, not just etcd; treat "currently at N-1 members" as
   an active incident, not a background fact.

8. **Watch disk fsync/backend-commit latency and DB size as the two
   leading indicators of etcd degradation**, via the `etcd` metrics
   endpoint scraped by
   [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md):
   ```promql
   histogram_quantile(0.99, rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m]))
   histogram_quantile(0.99, rate(etcd_disk_backend_commit_duration_seconds_bucket[5m]))
   etcd_mvcc_db_total_size_in_bytes / etcd_server_quota_backend_bytes
   ```
   p99 `wal_fsync_duration_seconds` sustained above ~10ms is the
   classic "etcd is on the wrong disk" signal (network storage, a
   shared/throttled volume) long before it manifests as API server
   timeouts; `db_total_size_in_bytes` approaching `quota_backend_bytes`
   (default 2GiB) predicts the cluster going read-only
   (`mvcc: database space exceeded`) before it happens.

## Best practices

- Provision etcd on **local NVMe/SSD**, never network-attached or
  shared storage — etcd's Raft commit path requires every write to be
  fsync'd to disk before acknowledging, and network storage latency
  variance directly becomes API server latency variance cluster-wide.
- Run etcd with an odd member count (3 or 5) for real fault tolerance;
  an even count (e.g. 2 or 4) doesn't improve tolerance over one member
  fewer and only adds split-vote risk.
- Automate snapshot scheduling and off-node shipping together — a
  snapshot schedule with no verified successful upload is a false sense
  of security.
- Set a compaction and defragmentation schedule
  (`etcdctl compact`, `etcdctl defrag`) rather than letting the DB grow
  unbounded between restarts — high churn workloads (frequent
  Job/Pod creation, verbose CRDs) can approach the default 2GiB quota
  surprisingly fast.
- Practice a full restore in a non-production environment on a real
  schedule (quarterly, or after any etcd/Kubernetes version bump) —
  a restore procedure that's never been executed outside a document is
  unverified, not ready.
- Alert on quorum headroom (members healthy vs. members expected), not
  only on "etcd is down" — a 3-member cluster at 2 healthy members is
  already one failure away from an outage and should page, not wait for
  full quorum loss.

## Common pitfalls

- **Symptom:** `etcdctl snapshot restore` succeeds with no errors, but
  the restored cluster never reaches quorum and the API server stays
  down.
  **Fix:** Check that every member restored with an identical
  `--initial-cluster` membership string and each member's own correct
  `--name`/`--initial-advertise-peer-urls` — a copy-pasted `--name`
  across members, or a peer URL that doesn't match what's in
  `--initial-cluster`, produces members that can't agree on cluster
  identity even though each restore individually reported success.

- **Symptom:** The API server intermittently returns `etcdserver:
  request timed out`, and etcd itself reports `Healthy` on
  `endpoint health`.
  **Fix:** `endpoint health` checks liveness, not latency — pull p99
  `etcd_disk_wal_fsync_duration_seconds` and
  `etcd_disk_backend_commit_duration_seconds` from metrics; sustained
  latency above single-digit milliseconds almost always traces to disk
  I/O contention (etcd on the same volume as other high-I/O workloads,
  or on network-attached storage), not an etcd bug.

- **Symptom:** The cluster suddenly goes read-only and every write
  returns `mvcc: database space exceeded`.
  **Fix:** The DB hit its backend quota (`etcd_server_quota_backend_bytes`,
  default ~2GiB). Compact old revisions and defragment to reclaim
  space (`etcdctl compact <revision>` then `etcdctl defrag`), then raise
  the quota (`--quota-backend-bytes`) if the workload's legitimate churn
  warrants it — don't raise the quota reflexively without also
  compacting, since an unbounded, never-compacted history caused the
  problem in the first place.

- **Symptom:** A snapshot is taken and stored, but months later when a
  restore is actually needed, `etcdctl snapshot restore` fails or
  produces a cluster missing expected data.
  **Fix:** The snapshot was never verified at capture time (`etcdctl
  snapshot status`) and/or was taken with a client/server API version
  mismatch. Always run `snapshot status` right after `snapshot save`
  and treat a snapshot as unverified — and therefore not a real backup
  — until that check passes.

- **Symptom:** A well-intentioned engineer runs `etcdctl snapshot
  restore` directly against a live, healthy cluster "just to test it,"
  and the cluster's current state is unexpectedly wiped.
  **Fix:** This is a destructive action masquerading as a read-only
  test — `snapshot restore` writes a *new* data directory, but pointing
  a running etcd's manifest at it (or restoring in place) discards all
  state since the snapshot. Always test restores against an isolated
  scratch cluster/VM, never against a live control plane, and require
  explicit confirmation of the target before any restore command runs
  against a real cluster's data directory.

## Worked example

**Scenario:** A 3-node stacked-etcd kubeadm cluster's `control-plane-2`
node suffered a disk failure, corrupting its etcd data directory. The
other two members are healthy, so quorum (2 of 3) is intact, but the
team wants both to replace the failed member and confirm they could
fully recover from a snapshot if quorum had been lost.

1. Confirm current quorum before touching anything:
   ```bash
   ETCDCTL_API3=3 etcdctl member list -w table --endpoints=https://127.0.0.1:2379 \
     --cacert=/etc/kubernetes/pki/etcd/ca.crt \
     --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
     --key=/etc/kubernetes/pki/etcd/healthcheck-client.key
   ```
   Two members healthy, one unreachable — quorum intact but at zero
   further tolerance, so this is treated as urgent, not routine.

2. Remove the failed member and re-add it fresh (member replacement,
   not a snapshot restore, since quorum never fully broke):
   ```bash
   ETCDCTL_API=3 etcdctl member remove <failed-member-id> --endpoints=https://127.0.0.1:2379 --cacert=... --cert=... --key=...
   # wipe /var/lib/etcd on control-plane-2, then:
   ETCDCTL_API=3 etcdctl member add control-plane-2 \
     --peer-urls=https://10.0.1.11:2380 --endpoints=https://127.0.0.1:2379 --cacert=... --cert=... --key=...
   # restart kubelet/etcd static pod on control-plane-2 with the returned ETCD_INITIAL_CLUSTER env
   ```

3. Separately, in a scratch VM, verify the most recent off-node
   snapshot actually restores cleanly (the practice-restore discipline
   from Best practices):
   ```bash
   ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd-snapshot-20260728110000.db \
     --name=scratch-restore-test \
     --initial-cluster="scratch-restore-test=https://127.0.0.1:2380" \
     --initial-advertise-peer-urls=https://127.0.0.1:2380 \
     --data-dir=/tmp/etcd-restore-test
   ETCDCTL_API=3 etcdctl snapshot status /backup/etcd-snapshot-20260728110000.db -w table
   ```
   The restore completes and `snapshot status` reports a non-zero key
   count matching expectations — confirming the backup chain (snapshot
   → upload → restore) genuinely works, discovered during a drill
   rather than during a real quorum-loss incident.

## Cross-references

- [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md) — where the etcd topology (stacked vs. external) is decided at cluster bring-up time.
- [kubernetes-node-maintenance-and-troubleshooting](../kubernetes-node-maintenance-and-troubleshooting/SKILL.md) — broader control-plane node maintenance this skill's disk/quorum checks feed into before disruptive operations.
- [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md) — RPO/RTO and retention design principles that apply to etcd snapshot scheduling too.
- [velero-backup-and-restore](../../../observability-and-platform-extras/skills/velero-backup-and-restore/SKILL.md) — application/workload-level backup (PVs, namespaced objects); complementary to, not a substitute for, etcd's cluster-wide state backup.
- [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md) — scraping and alerting on the etcd fsync-latency and DB-size metrics referenced above.
- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) — why this skill's procedures don't apply to managed control planes, where etcd is fully provider-operated.
