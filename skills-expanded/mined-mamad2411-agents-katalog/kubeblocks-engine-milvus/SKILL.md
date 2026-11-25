---
name: kubeblocks-engine-milvus
version: "0.2.0"
description: Primary create-time entry for Milvus on KubeBlocks. Use when the user wants to provision Milvus and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-milvus skill remains only as a compatibility shim.
---

# Milvus Engine Entry

Use this as the primary create-time entry for Milvus. Tier-1 Milvus never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising scrape readiness.
- Keep the legacy [kubeblocks-addon-milvus](../kubeblocks-addon-milvus/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `cluster`
- `standalone`: use only for evaluation, demos, or very small vector workloads.
- `cluster`: default production path because Milvus usually depends on separate metadata, log, and object-storage services.
- If the user is doing real retrieval or vector search work, stay on `cluster`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Use the addon-backed Milvus line from current examples and keep dependency services aligned with the same shipped addon generation.
- Do not guess a version from generic Milvus release notes when the addon examples already define a safe line.

## Preflight Interpretation

- `storage_class`: required before apply because Milvus data and dependency services persist to PVCs.
- `volume_binding_mode`: confirm storage placement before cluster rollout.
- `addon_readiness`: Milvus addon must be installed first.
- `dependency_clusters`: the cluster path depends on metadata, log, and object storage references; do not skip dependency validation.

## Sizing Profiles

- `demo`: `standalone` or a very small dependency-backed `cluster` for SDK validation.
- `production`: `cluster` with explicit etcd, MinIO, and Pulsar dependency posture plus observability from day 1.
- Treat Milvus dependency capacity as part of the create decision, not as an afterthought.

## Minimal Create Path

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: <cluster>
  namespace: <ns>
spec:
  terminationPolicy: Delete
```

- Do not leave this skill to read raw addon examples before drafting the manifest.
- Set `clusterDef: milvus` for every Milvus create path in this wave.
- `standalone`: set `topology: standalone`, keep a single `name: milvus` component, and set `serviceVersion`, `resources`, and `volumeClaimTemplates` on that component.
- `cluster`: set `topology: cluster`, let the topology materialize `name: proxy`, `name: mixcoord`, `name: datanode`, `name: indexnode`, and `name: querynode`, and only continue after dependency clusters are already resolved in preflight.
- Validate with `kubectl apply --dry-run=server -f <milvus-cluster.yaml>`.
- Apply with `kubectl apply -f <milvus-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: port-forward the Milvus endpoint and confirm SDK or health access on the gRPC/data path.
- For `cluster`, verify dependency clusters are reachable before handing the endpoint to application teams.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, and `kubeblocks-observability-router`.
- Treat credential and TLS work as engine-specific validation rather than assuming [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) or [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) are default Milvus paths.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); Milvus recovery should stay on troubleshoot, restore, or dependency repair.
- Route dependency, component, or service-reference failures to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route Milvus create through `kubeblocks-engine-generic`, `kubeblocks-family-vector`, `kubeblocks-addon-milvus`, or `kubeblocks-engine-qdrant`.
- If the request is actually a lightweight vector store with Qdrant semantics, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/milvus/cluster-standalone.yaml`, `examples/milvus/cluster.yaml`.
- There is no separate legacy reference file for this engine in the current repository snapshot.
