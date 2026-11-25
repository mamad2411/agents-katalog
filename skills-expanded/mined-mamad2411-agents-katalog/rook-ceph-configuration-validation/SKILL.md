---
name: rook-ceph-configuration-validation
description: >
  Validates a Rook-managed Ceph cluster's actual health before relying on
  it for production persistent storage — reading `ceph status`/`ceph
  health detail`, checking OSD placement against intended failure
  domains, placement group (PG) state, and CephCluster/CephBlockPool
  CRD status conditions. Use when a user asks to "check if my Ceph
  cluster is healthy," "validate Rook-Ceph before going to production,"
  "why is my CephCluster stuck HEALTH_WARN," "check OSD placement/CRUSH
  map," or "diagnose stuck/degraded placement groups."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Rook-Ceph Configuration Validation

## Purpose

A `CephCluster` CRD can report `Ready` in Kubernetes terms — the
operator reconciled it, all expected pods are `Running` — while the
underlying Ceph cluster itself is in `HEALTH_WARN` or even `HEALTH_ERR`,
because Kubernetes-level pod health and Ceph's own internal
consensus/data-placement health are two different signals that don't
automatically agree. Trusting Rook-Ceph for production workloads without
directly checking Ceph's own health output is the single most common
way teams discover a storage problem only when an application already
depends on it and something breaks. This skill covers the validation
workflow — `ceph status`, OSD placement/CRUSH, and PG state — that
should run before a newly deployed cluster is trusted, and periodically
after. It assumes the cluster was deployed per
[rook-ceph-storage-operations](../rook-ceph-storage-operations/SKILL.md)
and focuses purely on verifying its health, not on configuring it.

## When to use

- Before pointing any production workload's StorageClass at a newly
  deployed Rook-Ceph cluster.
- A `CephCluster` shows `HEALTH_WARN`/`HEALTH_ERR` and the specific
  cause isn't obvious from the Kubernetes-level CRD status alone.
- Confirming OSDs are actually spread across the intended failure
  domains (hosts, racks) rather than accidentally concentrated in ways
  that defeat the configured replication.
- Investigating placement groups stuck `degraded`, `undersized`,
  `stale`, or `inactive` after a node failure, device replacement, or
  capacity expansion.
- Periodic (e.g. weekly, or pre-change) health verification as part of
  an operational runbook, not only during incidents.
- Validating a Ceph cluster's health *before* a planned disruptive
  operation (node drain, Kubernetes upgrade, device replacement) to
  confirm the cluster can tolerate it.

## Prerequisites & environment

- A Rook-Ceph cluster already deployed per
  [rook-ceph-storage-operations](../rook-ceph-storage-operations/SKILL.md),
  with the `rook-ceph-tools` deployment running (`kubectl -n rook-ceph
  get pods -l app=rook-ceph-tools`) — most of the checks below assume a
  shell into this pod (`kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- bash`).
- `kubectl` read access to the `rook-ceph` namespace and the
  cluster-scoped `CephCluster`/`CephBlockPool`/`CephFilesystem`/
  `CephObjectStore` CRDs.
- Familiarity with the CRUSH map concept (Ceph's data-placement
  algorithm, which assigns placement groups to OSDs according to a
  configured failure-domain hierarchy) — this skill checks CRUSH/OSD
  placement against intent but does not re-explain CRUSH from first
  principles.
- Ideally, the Ceph dashboard enabled
  (`CephCluster.spec.dashboard.enabled: true`) for a visual
  cross-check alongside the CLI checks below.

## Step-by-step guidance

1. **Start from `ceph status`, not the Kubernetes CRD's `Ready`
   field** — they measure different things:
   ```bash
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph status
   ```
   Read the `health:` line first (`HEALTH_OK`/`HEALTH_WARN`/
   `HEALTH_ERR`), then `mon`/`mgr`/`osd` counts (`3 up, 3 in` for a
   healthy 3-OSD cluster — `up` means the daemon is responsive, `in`
   means it's included in data placement; an OSD that's `up` but not
   `in`, or vice versa, is a specific, distinct problem), then `pgs:`
   for placement group state summary.

2. **Get the specific reason behind any non-`HEALTH_OK` state** —
   `ceph status`'s health line is a summary; the detail is elsewhere:
   ```bash
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph health detail
   ```
   This surfaces the actual warning/error codes (e.g.
   `PG_DEGRADED`, `OSD_DOWN`, `MON_DISK_LOW`,
   `POOL_NEAR_FULL`) rather than a generic "warning" — treat this
   output, not the one-line summary, as the starting point for any
   investigation.

3. **Cross-check the Kubernetes-level CRD status against the Ceph-level
   status** — they should agree, but confirm rather than assume:
   ```bash
   kubectl -n rook-ceph get cephcluster rook-ceph -o jsonpath='{.status.phase}{"\n"}{.status.ceph.health}{"\n"}{.status.ceph.details}'
   kubectl -n rook-ceph get pods -o wide | grep -E 'osd|mon|mgr'
   ```
   A `CephCluster` reporting Kubernetes-level `Ready`/`Progressing` with
   an inconsistent or stale `.status.ceph.health` field usually means
   the operator's own reconciliation loop is behind — check the
   operator's own logs
   (`kubectl -n rook-ceph logs -l app=rook-ceph-operator --tail=200`)
   rather than trusting a CRD status that hasn't updated recently.

4. **Verify OSD placement matches the intended failure domain**, not
   just that OSD count matches expectation:
   ```bash
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph osd tree
   ```
   Confirm each `host` bucket in the tree output actually corresponds
   to a distinct physical/VM node, and that no single host holds a
   disproportionate share of OSDs relative to others — an OSD tree
   where two "hosts" turn out to be VMs on the same hypervisor, or a
   node with 3 OSDs versus others with 1, means the configured
   `failureDomain: host` replication isn't buying the durability its
   configuration implies.

5. **Confirm the CRUSH map's rule set matches the pool's declared
   `failureDomain`**:
   ```bash
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph osd crush rule dump
   kubectl -n rook-ceph get cephblockpool replicapool -o jsonpath='{.spec.failureDomain}'
   ```
   A pool declared with `failureDomain: host` in its CRD but whose
   actual CRUSH rule steps by `osd` (not `host`) indicates the CRD spec
   and the live CRUSH rule have drifted — re-apply the `CephBlockPool`
   CRD, and if it doesn't reconcile the CRUSH rule automatically, treat
   this as an operator-level bug requiring the Rook operator log for
   root cause rather than silently leaving mismatched durability in
   place.

6. **Check placement group (PG) state for anything other than
   `active+clean`**:
   ```bash
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph pg stat
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph pg dump_stuck
   ```
   `active+clean` is the fully healthy state. `degraded` means fewer
   replicas than configured currently exist (usually mid-recovery after
   an OSD loss — expected temporarily, concerning if it persists);
   `undersized` means not enough OSDs exist to satisfy the pool's
   replica count at all (a structural problem, not transient);
   `stale`/`inactive` PGs mean the primary OSD for that PG isn't
   responding — I/O to that data is blocked, which is more urgent than
   `degraded`.

7. **Check capacity headroom before it becomes an outage**:
   ```bash
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph df
   kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph osd df
   ```
   `ceph df`'s `%USED` per pool and `ceph osd df`'s per-OSD `%USE`
   matter separately: overall cluster capacity can look fine in
   aggregate while one specific OSD is nearly full (Ceph's CRUSH
   placement isn't perfectly uniform), and a single near-full OSD can
   trigger `OSD_NEARFULL`/`OSD_FULL` warnings and eventually block
   writes to the pools mapped onto it well before the cluster-wide
   number looks alarming.

8. **Validate CSI provisioning actually works end-to-end**, not just
   that Ceph itself is healthy — a healthy Ceph cluster with a broken
   CSI driver still fails every PVC:
   ```bash
   kubectl apply -f - <<'EOF'
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata: { name: rook-validation-test, namespace: default }
   spec:
     accessModes: [ReadWriteOnce]
     storageClassName: rook-ceph-block
     resources: { requests: { storage: 1Gi } }
   EOF
   kubectl get pvc rook-validation-test -w   # confirm it reaches Bound
   kubectl delete pvc rook-validation-test
   ```
   Run this as a smoke test after any Rook/Ceph upgrade or CRUSH/pool
   change, not only at initial install.

## Best practices

- Treat `ceph status`/`ceph health detail` as the source of truth for
  storage health, and the Kubernetes CRD status as a secondary,
  sometimes-lagging signal — never certify a cluster healthy from
  `kubectl get cephcluster` output alone.
- Run the OSD-placement and CRUSH-rule checks (steps 4-5) after *every*
  capacity change (node/device addition or removal), not just at
  initial deployment — a rebalance can shift which hosts hold which
  data, and it's worth confirming the failure-domain intent still
  holds afterward.
- Alert on `ceph health detail`'s specific warning codes
  (`OSD_NEARFULL`, `PG_DEGRADED`, `MON_DISK_LOW`) via the Ceph
  mgr Prometheus exporter rather than only checking manually during
  incidents — see
  [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md).
- Include the end-to-end PVC provisioning smoke test (step 8) in CI/CD
  or a post-upgrade runbook — a cluster can be `HEALTH_OK` at the Ceph
  layer while the CSI driver itself is broken (a stale secret, a
  version mismatch after an upgrade).
- Don't treat `HEALTH_WARN` as automatically low-priority — read
  `health detail` first; some warnings (`MON_DISK_LOW`,
  `OSD_NEARFULL`) are early signals of an imminent `HEALTH_ERR` if
  ignored, not cosmetic noise.
- Validate against the pool's *declared* failure domain, not an assumed
  one — a pool created with a default/forgotten `failureDomain` setting
  can silently end up providing less durability than a team believes it
  has.

## Common pitfalls

- **Symptom:** `kubectl get cephcluster` shows `phase: Ready`, but an
  application backed by Rook storage experiences I/O errors or extreme
  latency.
  **Fix:** The CRD's Kubernetes-level `Ready` reflects operator
  reconciliation, not Ceph's internal health — always cross-check
  `ceph status`/`ceph health detail` directly; a cluster can be
  `HEALTH_ERR` (e.g. PGs `inactive`) while the CRD itself still reports
  `Ready` because the operator successfully reconciled the *desired
  spec*, which is a different question from whether Ceph is currently
  serving I/O correctly.

- **Symptom:** `ceph osd tree` shows the expected number of OSDs and
  hosts, but two of the three "hosts" turn out to be VMs colocated on
  the same physical hypervisor.
  **Fix:** `failureDomain: host` only protects against failures Ceph's
  CRUSH map can see as separate — if the underlying infrastructure puts
  two "host" failure domains on the same physical machine or the same
  power/network path, a single physical failure can take out multiple
  replicas simultaneously. Confirm actual physical/availability-zone
  independence of each node Ceph considers a separate host, not just
  that Kubernetes lists them as separate `Node` objects.

- **Symptom:** PGs are stuck `undersized` and `degraded` indefinitely,
  well beyond any reasonable recovery window.
  **Fix:** Distinguish transient (`degraded` shrinking over time, OSDs
  actively backfilling) from structural (`undersized` not decreasing
  because there simply aren't enough OSDs/hosts to satisfy the pool's
  replica count). `ceph osd df` and `ceph osd tree` show whether enough
  healthy OSDs across enough distinct failure domains actually exist;
  if not, either add capacity or reduce the pool's replica requirement
  deliberately — waiting longer does not resolve a structural
  under-provisioning problem.

- **Symptom:** `ceph df` shows the cluster only 60% full overall, but
  writes to a specific pool start failing with a "near full" or
  "full" error.
  **Fix:** Check `ceph osd df` per-OSD, not just cluster-aggregate
  capacity — CRUSH placement is not perfectly uniform, and one OSD can
  hit its full-ratio threshold while overall cluster capacity looks
  comfortable. Rebalance (`ceph osd reweight-by-utilization`) or add
  capacity to the specific overloaded OSDs/hosts rather than concluding
  the cluster overall has room to spare.

- **Symptom:** Someone runs `ceph osd out <osd-id>` or deletes a
  `CephBlockPool` directly to "clean up" during a validation exercise,
  and production PVCs backed by that pool/OSD start failing.
  **Fix:** These are destructive, production-impacting actions, not
  read-only validation steps — validation should be limited to `status`/
  `health detail`/`df`/`tree`/`dump_stuck` read commands (and the
  disposable smoke-test PVC in step 8, immediately cleaned up). Never
  run `ceph osd out`, `ceph osd rm`, or pool/filesystem deletion as part
  of a health-check exercise against a cluster serving real workloads.

## Worked example

**Scenario:** Before migrating a production PostgreSQL StatefulSet onto
an existing Rook-Ceph cluster that's been running for a few weeks,
confirm it's genuinely healthy end-to-end.

```bash
kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph status
```
```
  cluster:
    health: HEALTH_WARN
            1 pools nearfull

  services:
    mon: 3 daemons, quorum a,b,c
    mgr: a(active), standbys: b
    osd: 3 osds: 3 up, 3 in

  data:
    pools:   3 pools, 96 pgs
    objects: 128.4k objects, 480 GiB
    usage:   1.4 TiB used, 600 GiB / 2.0 TiB avail
    pgs:     96 active+clean
```

`HEALTH_WARN` with `1 pools nearfull` — not `HEALTH_OK`, so this
requires investigation before proceeding, not a shrug.

```bash
kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph health detail
```
```
HEALTH_WARN 1 pools nearfull
POOL_NEARFULL 1 pools nearfull
    pool 'replicapool' is nearfull
```
```bash
kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph osd df
```
Shows `osd.1` at 87% used versus `osd.0`/`osd.2` around 55% — an
uneven distribution, not a genuine capacity shortfall.

Remediate with a reweight (a routine operational action, not
destructive) rather than immediately adding hardware:
```bash
kubectl -n rook-ceph exec deploy/rook-ceph-tools -- ceph osd reweight-by-utilization
```
Re-run `ceph status` after rebalancing completes — `health: HEALTH_OK`
— then run the end-to-end PVC smoke test (step 8) to confirm CSI
provisioning works, before greenlighting the PostgreSQL migration.

## Cross-references

- [rook-ceph-storage-operations](../rook-ceph-storage-operations/SKILL.md) — deploying and configuring the CephCluster/pools this skill validates.
- [longhorn-storage-configuration](../longhorn-storage-configuration/SKILL.md) — the equivalent validation concerns (replica placement, capacity) for the simpler Longhorn alternative.
- [etcd-backup-restore-and-cluster-health](../etcd-backup-restore-and-cluster-health/SKILL.md) — analogous quorum/health-monitoring discipline applied to etcd rather than Ceph.
- [prometheus-and-grafana-monitoring-stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md) — continuous alerting on the Ceph health signals checked manually here.
- [cloud-resource-post-provisioning-validation-and-drift-detection](../../../cloud/skills/cloud-resource-post-provisioning-validation-and-drift-detection/SKILL.md) — the broader post-provisioning validation discipline this skill applies specifically to Rook-Ceph.
