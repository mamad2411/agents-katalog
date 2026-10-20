---
name: kubeblocks-engine-qdrant
version: "0.2.0"
description: Primary create-time entry for Qdrant on KubeBlocks. Use when the user wants to provision Qdrant and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-qdrant skill remains only as a compatibility shim.
---

# Qdrant Engine Entry

Use this as the primary create-time entry for Qdrant. Tier-1 Qdrant never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising scrape readiness.
- Keep the legacy [kubeblocks-addon-qdrant](../kubeblocks-addon-qdrant/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `cluster`
- `cluster`: the only supported Tier-1 create shape in the current truth; use it even for small environments by reducing replica count instead of inventing a separate single-node route.
- If the user only wants a local demo, keep the cluster tiny, but do not leave the matrix-backed `cluster` shape.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence surfaces Qdrant `1.5`, `1.7`, `1.8`, and `1.10`, with create examples anchored on the shipped addon defaults.
- If the user asks for "latest", stay on an addon-backed supported line rather than a raw upstream tag.

## Preflight Interpretation

- `storage_class`: required before apply because Qdrant data lives on PVCs.
- `volume_binding_mode`: confirm placement behavior before multi-replica cluster rollout.
- `addon_readiness`: Qdrant addon must be installed first.
- Qdrant is `scrape-ready` in the current observability truth; do not promise dashboards or alerts by default.

## Sizing Profiles

- `demo`: a small `cluster` with minimal replicas and modest PVC sizing.
- `production`: `cluster` with explicit capacity headroom for data redistribution during scale or member replacement.
- Keep replica counts odd when possible to reduce Raft coordination risk.

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
- Set `clusterDef: qdrant` and `topology: cluster`.
- Keep one `name: qdrant` component and set `serviceVersion`, `replicas: 3`, `resources`, and `volumeClaimTemplates` directly on that component.
- Validate with `kubectl apply --dry-run=server -f <qdrant-cluster.yaml>`.
- Apply with `kubectl apply -f <qdrant-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `exposed service`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: port-forward the API endpoint and check the Qdrant HTTP API before handoff.
- If externally exposed, verify the public endpoint and collection API path before application use.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-backup`, and `kubeblocks-observability-router`.
- Treat credential and TLS work as engine-specific validation rather than assuming [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) or [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) are default Qdrant paths.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); Qdrant recovery should stay on backup, restore, or troubleshoot paths instead.
- Route unhealthy members, rebalance issues, or API failures to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route Qdrant create through `kubeblocks-engine-generic`, `kubeblocks-family-vector`, `kubeblocks-addon-qdrant`, or `kubeblocks-engine-milvus`.
- If the request is really Milvus-style dependency-backed vector search, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/qdrant/cluster.yaml`.
- There is no separate legacy reference file for this engine in the current repository snapshot.
