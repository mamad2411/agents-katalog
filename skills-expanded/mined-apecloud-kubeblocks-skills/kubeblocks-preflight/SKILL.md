---
name: kubeblocks-preflight
version: "0.1.0"
description: Check whether a Kubernetes environment is ready for first-time KubeBlocks database rollout, then emit an environment profile / recommendation bundle for downstream engine-entry skills. Use this before provisioning MySQL, PostgreSQL, Redis, MongoDB, Kafka, or any other database when rollout readiness is still unknown.
---

# KubeBlocks Preflight

Run this skill **after KubeBlocks is installed but before first-time database provisioning**.

Its job is not only to inspect the cluster. It must also produce a stable **environment profile / recommendation bundle** that downstream engine-entry skills can use directly.

## When To Use

Use this skill when any of the following is true:

- The user is provisioning the first database in a cluster.
- Storage behavior is unknown.
- The cluster spans multiple availability zones.
- Monitoring expectations are unclear.
- The user asks "can I deploy PG/MySQL/Redis here?" before creating the cluster.

Do **not** skip this step for high-frequency engines such as MySQL or PostgreSQL when rollout readiness is still unknown.

## Workflow

```text
- [ ] Step 1: Confirm cluster access and namespace assumptions
- [ ] Step 2: Inspect storage and topology risks
- [ ] Step 3: Inspect addon and snapshot prerequisites
- [ ] Step 4: Inspect monitoring baseline
- [ ] Step 5: Emit the recommendation bundle
```

## Step 1: Confirm Cluster Access

```bash
kubectl config current-context
kubectl get nodes -o wide
kubectl get ns
```

Capture:

- cluster type if known (ACK / EKS / GKE / on-prem / local)
- number of nodes
- node zone / topology labels
- target namespace if already chosen

## Step 2: Inspect Storage And Topology Risks

This is the most important gate for real deployments.

```bash
kubectl get storageclass
kubectl get storageclass -o yaml
kubectl get nodes -L topology.kubernetes.io/zone,failure-domain.beta.kubernetes.io/zone
```

Check and record:

- whether a default `StorageClass` exists
- candidate `storageClassName`
- `volumeBindingMode`
- whether the class is topology-aware
- whether multi-AZ scheduling plus `Immediate` binding can create `PV node affinity` risk
- whether `allowVolumeExpansion` is enabled

If the cluster is multi-AZ and the selected class binds volumes immediately to a single zone, mark that as a rollout risk and recommend a topology-aware class with `WaitForFirstConsumer`.

## Step 3: Inspect Addon And Snapshot Prerequisites

```bash
helm list -n kb-system
kubectl get volumesnapshotclass 2>/dev/null || true
kubectl api-resources | grep -i snapshot || true
```

Check and record:

- whether the required addon is already installed
- whether CSI snapshot capability exists if snapshot-based workflows matter
- whether any cluster policy or quota is likely to block rollout

## Step 4: Inspect Monitoring Baseline

```bash
kubectl get pods -A | grep -E 'prometheus|grafana' || true
kubectl get servicemonitor,podmonitor -A 2>/dev/null || true
```

Decide which observability path is appropriate:

- `existing-stack`: Prometheus / Grafana already exists and only integration is needed
- `bootstrap-stack`: no usable monitoring base exists yet

Also note if exporter presence is enough for now (`metrics-ready`) or if the user expects dashboards / alerting.

## Step 5: Emit The Recommendation Bundle

The output of this skill must be structured enough for downstream skills to consume directly.

Use the schema in [references/recommendation-bundle.md](references/recommendation-bundle.md).

At minimum, produce:

- storage recommendation
- topology / scheduling risk summary
- recommended engine-entry path
- forbidden generic paths
- demo vs production sizing default
- observability route

### Example

```yaml
environmentProfile:
  clusterType: ack
  multiAZ: true
  targetNamespace: demo
recommendations:
  storage:
    storageClassName: alicloud-disk-topology-alltype
    volumeBindingMode: WaitForFirstConsumer
    topologyAwareRequired: true
  engineEntry:
    recommendedSkill: kubeblocks-addon-postgresql
    forbiddenGenericPaths:
      - kubeblocks-create-cluster
  sizing:
    defaultTier: demo
  observability:
    recommendedSkill: kubeblocks-observability-existing-stack
    readinessTarget: scrape-ready
risks:
  - multi-AZ cluster + immediate-binding storage can strand PVCs in the wrong zone
```

## Exit Criteria

Preflight is complete only when:

- a candidate `storageClassName` is selected
- topology risk is explicitly judged
- the next engine-entry skill is named
- the observability path is named
- demo vs production sizing guidance is stated

If you cannot answer those five items, preflight is incomplete.
