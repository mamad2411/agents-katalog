---
name: kubernetes-node-maintenance-and-troubleshooting
description: >
  Guides safely taking a Kubernetes node out of service for
  maintenance — `kubectl cordon`/`kubectl drain` with
  PodDisruptionBudget awareness so eviction doesn't cause an outage —
  and diagnosing a node stuck `NotReady` (kubelet, container runtime,
  network, and disk-pressure causes) before `kubectl uncordon`. Use when
  a user asks to "drain a node for maintenance," "why is my node
  NotReady," "safely patch/reboot a Kubernetes node," "a node drain is
  stuck/hanging," "uncordon a node," or "PodDisruptionBudget is blocking
  my drain."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Kubernetes Node Maintenance and Troubleshooting

## Purpose

Taking a node out of service — for an OS patch, a hardware swap, a
kubelet upgrade, or decommissioning — is routine, but doing it wrong is
one of the most common self-inflicted causes of a Kubernetes outage: a
`drain` evicts every non-DaemonSet pod on the node, and if the workload
running there doesn't have enough replicas elsewhere (and no
`PodDisruptionBudget` to make that constraint explicit), the eviction
itself becomes the incident. Separately, a node that goes `NotReady`
unexpectedly needs its own diagnosis — kubelet/runtime/network/disk
causes each look similar from `kubectl get nodes` but require different
fixes. This skill covers the safe cordon/drain/uncordon sequence with
`PodDisruptionBudget` awareness, and diagnosing an unexpectedly
`NotReady` node.

## When to use

- Planned maintenance on a node (OS patching, hardware replacement,
  kubelet/container-runtime upgrade, decommissioning) that requires
  safely moving its workloads off first.
- A node shows `NotReady` in `kubectl get nodes` and needs root-cause
  diagnosis before deciding whether to wait, intervene, or replace it.
- A `kubectl drain` is hanging or timing out and it's unclear whether
  that's expected (a `PodDisruptionBudget` correctly blocking it) or a
  different problem.
- Bringing a node back into service with `kubectl uncordon` after
  maintenance completes.
- Draining nodes one at a time as part of a `kubeadm upgrade` — see
  [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md)
  for the upgrade sequence this fits into.

## Prerequisites & environment

- `kubectl` access with permission to cordon/drain/uncordon nodes and to
  evict pods across the namespaces scheduled on that node (`nodes/drain`
  and `pods/eviction` RBAC verbs, in addition to general node read
  access).
- Awareness of every `PodDisruptionBudget` (PDB) covering workloads on
  the target node — a drain that respects PDBs (the default,
  eviction-based behavior) will block rather than violate one, which is
  correct behavior, not a bug to work around.
- SSH or console access to the node itself for OS-level diagnosis when
  it's `NotReady` (kubelet logs, disk usage, container runtime status)
  — `kubectl` alone often can't explain *why* a node stopped reporting
  Ready.
- Understanding that `kubectl drain` does not evict DaemonSet-managed
  pods by default (`--ignore-daemonsets` is required and expected for
  any node running DaemonSets, which is nearly every real cluster) and
  does not delete `emptyDir`-backed pod data by default either
  (`--delete-emptydir-data` is required to proceed past pods using
  local ephemeral storage).

## Step-by-step guidance

1. **Diagnose a `NotReady` node before doing anything else**, if that's
   why you're here rather than planned maintenance:
   ```bash
   kubectl describe node <node>
   ```
   Check the `Conditions` block: `Ready=False`/`Unknown`,
   `MemoryPressure`, `DiskPressure`, `PIDPressure` each point to a
   different cause. `Ready=Unknown` typically means the node stopped
   reporting to the API server at all (network partition, kubelet
   crashed) rather than reporting an explicit failure.

2. **Check kubelet and runtime health directly on the node** — the API
   server's view is downstream of both:
   ```bash
   # on the node itself
   systemctl status kubelet
   journalctl -u kubelet -n 200 --no-pager
   systemctl status containerd    # or the configured CRI runtime
   df -h                          # DiskPressure candidate
   ```
   Common causes: kubelet or the container runtime crashed/stopped, the
   node's disk filled up (triggering `DiskPressure` and image/container
   garbage collection, or blocking new pod starts entirely), or a
   network issue prevents the node reaching the API server (unrelated
   to the CNI's pod-to-pod data path — see
   [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
   for that separate failure class).

3. **Before draining for planned maintenance, check what's actually
   running there and which PDBs apply**:
   ```bash
   kubectl get pods -A -o wide --field-selector spec.nodeName=<node>
   kubectl get pdb -A
   ```
   For any workload on the node with a `PodDisruptionBudget`, compare
   its `minAvailable`/`maxUnavailable` against its current replica
   count and health — a PDB that leaves zero disruption budget with the
   node's pods included means an eviction-respecting drain will
   correctly refuse to proceed until that changes.

4. **Cordon the node** to stop new pods from being scheduled onto it
   (existing pods are untouched by cordon alone):
   ```bash
   kubectl cordon <node>
   ```

5. **Drain the node**, letting `kubectl drain` respect
   PodDisruptionBudgets by default:
   ```bash
   kubectl drain <node> \
     --ignore-daemonsets \
     --delete-emptydir-data \
     --timeout=300s
   ```
   `kubectl drain` cordons the node automatically as part of this
   command if not already cordoned — running `cordon` first (step 4) is
   still good practice for visibility, but not strictly required before
   `drain`.

6. **If the drain hangs or times out, diagnose before forcing
   anything**:
   ```bash
   kubectl get pdb -A -o wide
   kubectl describe pdb <pdb-name> -n <namespace>
   ```
   A drain blocked by a PDB is the mechanism working as intended — it
   is protecting the workload's own stated availability requirement.
   The correct response is to address *that* constraint (temporarily
   scale up replicas so eviction no longer violates `minAvailable`,
   coordinate a maintenance window with the owning team, or wait for
   capacity elsewhere), not to bypass the protection.

7. **Perform the actual maintenance** (OS patch, reboot, hardware swap,
   kubelet/runtime upgrade) once the node has no non-DaemonSet pods
   remaining.

8. **Uncordon the node** to make it schedulable again:
   ```bash
   kubectl uncordon <node>
   ```
   This only marks the node schedulable for *future* pods — it does not
   move any already-rescheduled workloads back. That's expected
   behavior: the scheduler will naturally place new/rescheduled pods on
   the node going forward based on normal scheduling, not as an
   automatic rebalancing action triggered by uncordon itself.

9. **Verify the node and its workloads are healthy** before considering
   the maintenance complete:
   ```bash
   kubectl get nodes
   kubectl get pods -A -o wide --field-selector spec.nodeName=<node>
   ```
   Confirm the node reports `Ready`, and that any workload scaled up
   temporarily to satisfy a PDB during the drain (step 6) is scaled back
   down once maintenance across the fleet is complete.

10. **For multi-node maintenance, proceed one node at a time**, verifying
    cluster and workload health between each — draining several nodes
    simultaneously multiplies the chance of exhausting a PDB's
    disruption budget across more of a workload's replicas at once than
    intended.

## Best practices

- Define a `PodDisruptionBudget` for every workload that has an actual
  availability requirement *before* a maintenance window needs one, not
  reactively when a drain unexpectedly hangs — a workload with no PDB
  at all can be evicted down to zero replicas by a drain with no warning
  whatsoever, which is a worse outcome than a drain that pauses to ask.
- Drain one node at a time in any multi-node maintenance operation, and
  confirm workload health before moving to the next — parallel draining
  compounds risk exactly when a PDB's protection matters most.
- Reserve `--force` only for pods that are genuinely unmanaged (no
  controller) or stuck because their node is already gone/unreachable —
  not as a default response to a slow or blocked drain.
- Give `kubectl drain` a `--grace-period` (or trust the pod's own
  configured `terminationGracePeriodSeconds`) long enough for the
  workload to actually shut down cleanly — a long-running request or
  connection-draining load balancer needs more than the default grace
  period to avoid cutting off in-flight work.
- Monitor node `Conditions` (`MemoryPressure`, `DiskPressure`,
  `Ready`) proactively via node-exporter/kube-state-metrics alerting,
  not only when someone happens to notice a node in a bad state during
  `kubectl get nodes`.
- Treat a node that goes `NotReady` repeatedly (not just once) as a
  signal to investigate the underlying hardware/OS/network rather than
  uncordoning and moving on each time it recovers — a flapping node is a
  reliability risk even between episodes.

## Common pitfalls

- **Symptom:** `kubectl drain` hangs indefinitely or times out.
  **Fix:** Check `kubectl get pdb -A` for a `PodDisruptionBudget`
  covering pods on that node whose `minAvailable`/`maxUnavailable`
  the eviction would violate. This is the drain correctly refusing to
  cause an outage — address the underlying capacity constraint
  (temporarily scale up, coordinate with the owning team, or wait)
  rather than reaching for `--force --grace-period=0` as the first
  response, which bypasses the protection instead of resolving what it
  was protecting against.

- **Symptom:** A node is drained for routine maintenance and a service
  with only one or two replicas — and no `PodDisruptionBudget` at all —
  goes fully unavailable during the drain.
  **Fix:** With no PDB, eviction-respecting drain has nothing to check
  against and will happily evict every replica if they're all scheduled
  on (or migrate through) the node being drained. Define a PDB for every
  workload with a real availability requirement ahead of any
  maintenance window, and check `kubectl get pods -o wide
  --field-selector spec.nodeName=<node>` plus `kubectl get pdb -A`
  together before draining, not just PDB existence in isolation.

- **Symptom:** Pods stuck `Terminating` are cleared with
  `kubectl delete pod --force --grace-period=0` to unblock a drain.
  **Fix:**
  > **Warning:** this skips graceful shutdown entirely — no
  pre-stop hook runs, no clean connection drain, no confirmation the
  process actually stopped on the node. For a stateful workload this can
  leave on-disk state inconsistent or a volume attached to a pod that no
  longer logically exists (check `kubectl get volumeattachments`
  afterward). It "masks" a stuck termination instead of diagnosing why
  the pod won't terminate cleanly (frequently a hung process or a
  container runtime issue on the node itself) — reserve this for pods
  whose node is confirmed gone/unreachable, not as a default unblock
  tactic.

- **Symptom:** A node goes `NotReady` after a transient network blip,
  and workloads on it are evicted and rescheduled elsewhere even though
  the node recovers shortly after.
  **Fix:** The default `pod-eviction-timeout` (5 minutes) passed before
  the node reported healthy again, so the control plane started
  evicting its pods as if the node were permanently gone. For workloads
  that shouldn't churn on a brief blip, add an explicit, bounded
  toleration for `node.kubernetes.io/not-ready`/`node.kubernetes.io/
  unreachable` — but don't disable eviction entirely, since that risks
  two copies of a stateful workload's pod running simultaneously if the
  node is truly gone (a split-brain risk, not just an inconvenience).

- **Symptom:** `kubectl uncordon` is run, but expected workloads don't
  come back to the node.
  **Fix:** This is expected — `uncordon` only makes the node eligible
  for future scheduling decisions, it does not proactively move
  already-rescheduled pods back. If rebalancing onto the node is
  actually desired, that requires a separate action (e.g. scaling the
  workload, or deleting a pod elsewhere to let the scheduler place a
  new one), not an assumption that uncordon itself triggers it.

- **Symptom:** `kubectl delete node <node>` is run directly to remove a
  problem node, without draining it first.
  **Fix:** This immediately removes the node object from the API
  without evicting or rescheduling its pods first —
  > **Warning:** this is a destructive shortcut that can leave workloads
  orphaned or delayed in rescheduling compared to a normal
  cordon-then-drain-then-remove sequence; drain the node first whenever
  it's still reachable, and reserve direct deletion for nodes truly
  gone from the infrastructure layer already.

## Worked example

**Scenario:** `node-3` needs a kernel patch requiring a reboot.
`payments-api` runs on it with a `PodDisruptionBudget` of
`minAvailable: 2` but only 2 total replicas cluster-wide.

```bash
kubectl get pods -n payments -o wide --field-selector spec.nodeName=node-3
# payments-api-7d9f6-abc12   1/1   Running   node-3

kubectl get pdb -n payments
# NAME               MIN AVAILABLE   MAX UNAVAILABLE   ALLOWED DISRUPTIONS
# payments-api-pdb    2               N/A               0
```

`ALLOWED DISRUPTIONS: 0` means draining `node-3` right now would
violate the PDB — evicting this pod would drop `payments-api` below its
required 2 available replicas.

```bash
kubectl scale deployment payments-api -n payments --replicas=3
kubectl get pdb payments-api-pdb -n payments
# ALLOWED DISRUPTIONS: 1
```

```bash
kubectl cordon node-3
kubectl drain node-3 --ignore-daemonsets --delete-emptydir-data --timeout=300s
# node/node-3 drained
```

The drain now succeeds because the temporary third replica gives the
PDB one disruption to allow. After the kernel patch and reboot:

```bash
kubectl uncordon node-3
kubectl get nodes
# node-3   Ready

kubectl scale deployment payments-api -n payments --replicas=2
```

The service stayed at or above its required 2 available replicas
throughout the entire maintenance window, and the temporary scale-up was
reverted once the node was back in service — no outage, no bypassed
PDB.

## Cross-references

- [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md) — the node-by-node drain/upgrade sequence this skill's drain steps fit into during a `kubeadm upgrade`.
- [pod-crashloop-and-oom-troubleshooting](../pod-crashloop-and-oom-troubleshooting/SKILL.md) — diagnosing an individual pod's health issue, as distinct from the node-level pressure/readiness issues covered here.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — diagnosing a node-to-node networking cause of `NotReady` that isn't kubelet/runtime/disk related.
- [chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md) — deliberately testing node-loss resilience under controlled conditions, rather than discovering a missing PDB during a real maintenance window.
- [kubernetes-cluster-post-provision-conformance-validation](../kubernetes-cluster-post-provision-conformance-validation/SKILL.md) — re-validating a node pool after maintenance that changed node images/kernels at scale.
