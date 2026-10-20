---
name: kubernetes-cluster-post-provision-conformance-validation
description: >
  Guides validating a freshly provisioned Kubernetes cluster before
  declaring it production-ready — running CNCF conformance tests via
  Sonobuoy (quick mode first, then `certified-conformance`), and
  layering targeted smoke tests (Service DNS resolution, cross-node pod
  connectivity, PVC provisioning) that conformance alone doesn't cover.
  Use when a user asks to "run conformance tests on a new cluster,"
  "validate a cluster with Sonobuoy," "is this cluster production
  ready," "smoke test a cluster after standing it up," "certify a
  cluster as CNCF conformant," or "re-validate a cluster after a CNI/
  Kubernetes upgrade."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: kubernetes-platform
  maturity: stable
---

# Kubernetes Cluster Post-Provision Conformance Validation

## Purpose

A cluster reporting `kubectl get nodes` all `Ready` is not the same
claim as "this cluster behaves like Kubernetes is supposed to." Whether
a cluster was bootstrapped with kubeadm/Cluster API, provisioned as a
managed EKS/AKS/GKE cluster, or stood up as K3s, subtle
misconfiguration — a CNI that doesn't fully implement the Service/DNS
data path, a storage class that silently doesn't provision, a
NetworkPolicy engine that accepts but doesn't enforce — can pass every
surface-level check and still fail real workloads days later. **Sonobuoy**
running the official **CNCF conformance test suite** is the standard,
vendor-neutral way to validate a cluster actually implements the
Kubernetes API and core behaviors correctly, and a small set of targeted
smoke tests closes gaps conformance doesn't cover (storage
provisioning, ingress paths, cross-node connectivity under your
specific CNI/network topology). This skill covers running both as a
required gate between "cluster provisioned" and "cluster declared
production-ready" — not the provisioning itself, covered in
[kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md),
[managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md),
and
[lightweight-kubernetes-k3s](../lightweight-kubernetes-k3s/SKILL.md).

## When to use

- Immediately after any cluster is provisioned — kubeadm/CAPI, managed
  (EKS/AKS/GKE), or K3s — and before it is handed to teams to deploy
  production workloads onto.
- Re-validating a cluster after a Kubernetes version upgrade, a CNI
  swap or migration, or a node pool/instance-type change that could
  affect scheduling or networking behavior.
- Formally certifying that a custom or vendor Kubernetes distribution
  meets CNCF's conformance requirements.
- Building a "cluster factory" pipeline where every newly provisioned
  cluster must pass an automated gate before being registered as
  available for use.
- Investigating a vague "something's off with this cluster" report
  where no specific workload-level bug has been pinned down yet.

## Prerequisites & environment

- Cluster-admin `kubectl` access to the target cluster (Sonobuoy creates
  a dedicated namespace, RBAC, and many test pods/resources across the
  cluster — it needs broad permissions, not a scoped service account).
- The `sonobuoy` CLI, version-matched to the target Kubernetes version's
  supported range (check Sonobuoy's own compatibility matrix — running
  a conformance image built for a much newer/older Kubernetes minor
  version against your cluster produces false failures unrelated to the
  cluster itself).
- Real spare capacity on the cluster: the full conformance suite
  schedules many e2e test pods across multiple namespaces and expects
  to actually run workloads, not just query the API — running it
  against a cluster already packed to its scheduling limit produces
  `Pending`-pod failures that reflect capacity, not conformance.
- Outbound access (or an air-gapped image mirror) to pull the Sonobuoy
  worker and conformance test images — these are not the workload
  images your applications use, and a network-restricted cluster needs
  them mirrored internally first.
- A maintenance window or non-production cluster for the **full**
  `certified-conformance` mode: it can take 1–2+ hours, creates and
  tears down many namespaces/resources, and is not intended to run
  silently alongside live production traffic on a shared cluster.

## Step-by-step guidance

1. **Run the quick smoke mode first** — a small, fast subset (a handful
   of minutes) that catches gross cluster misconfiguration before
   committing to the full run:
   ```bash
   sonobuoy run --mode quick --wait
   sonobuoy status
   ```

2. **Retrieve and inspect quick-mode results** before proceeding:
   ```bash
   results=$(sonobuoy retrieve)
   sonobuoy results "$results"
   ```
   A quick-mode failure means something fundamental is broken (API
   server reachability, basic pod scheduling, DNS) — fix that before
   spending an hour on the full suite.

3. **Clean up between runs** — Sonobuoy's namespace/resources persist
   until explicitly removed, and a stale run can interfere with the
   next:
   ```bash
   sonobuoy delete --all --wait
   ```

4. **Run the full CNCF conformance suite** once quick mode passes:
   ```bash
   sonobuoy run --mode certified-conformance --wait
   sonobuoy status
   ```
   `--wait` blocks until the run completes rather than requiring manual
   polling; for CI use, poll `sonobuoy status --json` on an interval
   instead of a long foreground wait.

5. **Retrieve and evaluate full results**:
   ```bash
   results=$(sonobuoy retrieve)
   sonobuoy results "$results" --mode=report
   ```
   A conformant cluster shows zero failed tests in the conformance
   subset; investigate any failure by extracting that test's detail
   from the results tarball rather than treating a partial pass as
   good enough.

6. **Clean up conformance resources**:
   ```bash
   sonobuoy delete --all --wait
   ```

7. **Layer targeted smoke tests conformance doesn't fully cover.**
   Service DNS resolution and cross-node pod connectivity, both
   dependent on the cluster's specific CNI and CoreDNS configuration:
   ```bash
   kubectl create namespace smoke-test
   kubectl run dns-check -n smoke-test --image=busybox:1.36 --restart=Never --rm -it -- \
     nslookup kubernetes.default.svc.cluster.local
   ```
   See
   [kubernetes-service-connectivity-troubleshooting](../kubernetes-service-connectivity-troubleshooting/SKILL.md)
   for the full diagnostic sequence if this fails, and
   [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md)
   for cross-node connectivity checks specific to the installed CNI.

8. **Smoke test storage provisioning** if the cluster is expected to
   support persistent workloads:
   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata: { name: smoke-pvc, namespace: smoke-test }
   spec:
     accessModes: ["ReadWriteOnce"]
     resources: { requests: { storage: 1Gi } }
   ```
   ```bash
   kubectl apply -f smoke-pvc.yaml
   kubectl get pvc smoke-pvc -n smoke-test -w   # expect Bound, not stuck Pending
   ```

9. **Smoke test the ingress path** end-to-end if an Ingress controller
   is part of the platform baseline (see
   [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md)):
   deploy a trivial echo service, expose it via Ingress, and `curl` it
   from outside the cluster rather than only confirming the Ingress
   object was accepted by the API server.

10. **Tear down all smoke-test resources** and record a pass/fail
    verdict against a defined checklist (conformance clean + DNS +
    cross-node connectivity + storage + ingress, as applicable to the
    cluster's intended use) before marking the cluster available —
    treat the checklist itself as the gate, not an informal "looks
    fine":
    ```bash
    kubectl delete namespace smoke-test
    ```

## Best practices

- Always run `--mode quick` before `--mode certified-conformance` — it
  costs minutes, not hours, and catches the same category of gross
  misconfiguration far cheaper.
- Run the full conformance suite in a maintenance window or against a
  cluster with no production traffic yet — it consumes real capacity
  across many namespaces and is not designed to run invisibly alongside
  live workloads.
- Automate this as a required stage in whatever pipeline provisions
  clusters (a "cluster factory" pattern) rather than a manual step
  someone remembers to run — an optional gate reliably gets skipped
  under deadline pressure.
- Store conformance/smoke-test results as pipeline artifacts tied to the
  cluster's identity and provisioning commit, so "is this cluster
  validated, and against what config" is answerable later without
  re-running the suite.
- Re-run the full validation after any change that could plausibly
  affect conformance or networking behavior — a Kubernetes minor
  version upgrade, a CNI swap, a container runtime change, or a new node
  pool with a different instance type/kernel — not only at initial
  cluster creation.
- Version-match the Sonobuoy CLI and conformance image to the target
  Kubernetes version explicitly; don't assume "latest" is always
  compatible, especially for clusters intentionally running an older
  supported minor version.

## Common pitfalls

- **Symptom:** `sonobuoy run` appears to hang indefinitely at "running."
  **Fix:** Check the Sonobuoy namespace's pod status directly
  (`kubectl get pods -n sonobuoy`) rather than only watching
  `sonobuoy status` — a common cause is insufficient cluster capacity
  (test pods stuck `Pending`) or no outbound access to pull the
  conformance test images, neither of which is a conformance failure of
  the cluster itself.

- **Symptom:** Conformance fails specific storage-related tests on a
  cluster that intentionally has no default `StorageClass`/CSI driver
  installed yet.
  **Fix:** This reflects the cluster's current state, not a defect —
  decide and document whether storage is in scope for this cluster's
  intended workloads before treating a storage-test failure as
  blocking; install and configure the intended CSI driver first if it
  is in scope, then re-run.

- **Symptom:** Test pods for the full `certified-conformance` run stay
  `Pending` across most namespaces.
  **Fix:** The cluster doesn't have enough spare scheduling capacity for
  the suite's real resource requests — this is a capacity problem, not
  a cluster-behavior conformance problem. Add capacity or run
  conformance before onboarding production workloads onto the cluster,
  not after it's already packed.

- **Symptom:** A cluster gets declared "production ready" and handed
  off to teams the same day it's provisioned, with no conformance or
  smoke test run at all — and a CNI-level NetworkPolicy or DNS bug
  surfaces days later once real traffic patterns exercise it.
  **Fix:** Treat this validation as a required gate before handoff, not
  an optional nice-to-have — the whole point is catching exactly this
  class of issue before it becomes a production incident instead of a
  pre-launch checklist item.

- **Symptom:** Conformance passes cleanly, but a specific application
  still fails to reach another Service by DNS name once deployed.
  **Fix:** Conformance validates the Kubernetes API/behavior contract in
  general, not your specific CNI's cross-node data path or a
  NetworkPolicy interaction with DNS egress — run the targeted smoke
  tests (step 7) in addition, and if DNS specifically fails, see
  [kubernetes-service-connectivity-troubleshooting](../kubernetes-service-connectivity-troubleshooting/SKILL.md).

## Worked example

**Scenario:** A 3-node HA kubeadm cluster (see
[kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md))
was just bootstrapped with Calico. Validate it before handing it to
application teams.

```bash
sonobuoy run --mode quick --wait
results=$(sonobuoy retrieve)
sonobuoy results "$results"
# Plugin: e2e
# Status: passed
# Total: 1, Passed: 1, Failed: 0, Skipped: 0
sonobuoy delete --all --wait
```

```bash
sonobuoy run --mode certified-conformance --wait
results=$(sonobuoy retrieve)
sonobuoy results "$results" --mode=report
# Total: 350+, Passed: 350+, Failed: 0, Skipped: <n>
sonobuoy delete --all --wait
```

```bash
kubectl create namespace smoke-test
kubectl run dns-check -n smoke-test --image=busybox:1.36 --restart=Never --rm -it -- \
  nslookup kubernetes.default.svc.cluster.local
# Server:    10.96.0.10
# Address:   10.96.0.10:53
# Name:      kubernetes.default.svc.cluster.local
# Address:   10.96.0.1

kubectl apply -f smoke-pvc.yaml
kubectl get pvc smoke-pvc -n smoke-test
# NAME        STATUS   VOLUME    CAPACITY   ACCESS MODES
# smoke-pvc   Bound    pvc-...   1Gi        RWO

kubectl delete namespace smoke-test
```

With conformance clean, DNS resolving correctly, and PVC provisioning
succeeding, the cluster is recorded as validated (conformance report +
smoke-test log attached to the provisioning ticket) and marked
available for application teams to deploy onto.

## Cross-references

- [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md) — the self-managed provisioning path this validation gate most commonly follows.
- [managed-kubernetes-eks-aks-gke](../managed-kubernetes-eks-aks-gke/SKILL.md) and [lightweight-kubernetes-k3s](../lightweight-kubernetes-k3s/SKILL.md) — the managed and lightweight provisioning paths that also warrant this validation before handoff.
- [cni-networking-calico-flannel](../cni-networking-calico-flannel/SKILL.md) — diagnosing cross-node connectivity or NetworkPolicy-enforcement smoke-test failures at the CNI layer.
- [kubernetes-service-connectivity-troubleshooting](../kubernetes-service-connectivity-troubleshooting/SKILL.md) — the deeper diagnostic path if a DNS or Service smoke test fails.
- [ingress-nginx-configuration](../ingress-nginx-configuration/SKILL.md) — installing the Ingress controller exercised by the ingress-path smoke test.
