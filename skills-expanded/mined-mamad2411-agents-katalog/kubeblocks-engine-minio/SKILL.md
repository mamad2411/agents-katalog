---
name: kubeblocks-engine-minio
version: "0.2.0"
description: Primary create-time entry for MinIO on KubeBlocks. Use when the user wants to provision MinIO and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown.
---

# MinIO Engine Entry

Use this as the primary create-time entry for MinIO. Tier-1 MinIO never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising monitoring readiness.
- Keep MinIO as object storage, not as a generic bucket service detached from storage and placement constraints.

## Topology Selection

- Default topology: `distributed`
- `distributed`: the only supported Tier-1 create shape in the current truth; adjust replica count for dev/test vs production instead of inventing a different topology.
- For dev/test, the examples tolerate 2 replicas; for production, start at 4 or another even, erasure-coding-safe replica count.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence centers on MinIO `2024-06-29T01-20-47Z`.
- If the user asks for "latest", stay on an addon-backed supported line rather than a raw upstream tag.

## Preflight Interpretation

- `storage_class`: required before apply because MinIO is storage-backed and highly sensitive to PVC behavior.
- `volume_binding_mode`: confirm placement and anti-affinity behavior before a multi-member distributed rollout.
- `addon_readiness`: MinIO addon must be installed first.
- MinIO currently has no exporter evidence in the observability truth, so do not promise scrape-ready observability by default.

## Sizing Profiles

- `demo`: a small `distributed` cluster with 2 replicas for evaluation.
- `production`: `distributed` with 4 or more even replicas, anti-affinity from preflight, and storage sized for object growth.
- Treat replica count as an erasure-coding and durability decision, not just horizontal scale.

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
- Keep one `name: minio` component, use `componentDef: minio`, and set `replicas: 2` only for dev/test; for production distributed quorum start at an even count of `4` or more.
- Keep optional bucket bootstrap in env `MINIO_BUCKETS` instead of inventing a second create path.
- Validate with `kubectl apply --dry-run=server -f <minio-cluster.yaml>`.
- Apply with `kubectl apply -f <minio-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: port-forward the console or API endpoint and confirm login or bucket access.
- If the user predefines `MINIO_BUCKETS`, validate that initialization succeeds before handoff.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, and `kubeblocks-observability-router`.
- Password and Secret handling can route to [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) when system accounts were customized.
- Treat [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) as engine-specific validation work rather than a default promise.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); MinIO recovery should stay on troubleshoot, scale, or restore paths instead.
- Route placement, console, or S3 endpoint failures to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route MinIO create through `kubeblocks-engine-generic`.
- If the user really wants a database engine instead of object storage, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/minio/cluster.yaml`.
