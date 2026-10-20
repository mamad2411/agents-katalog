---
name: kubeblocks-engine-mongodb
version: "0.2.0"
description: Primary create-time entry for MongoDB on KubeBlocks. Use when the user wants to provision MongoDB and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-mongodb skill remains only as a compatibility shim.
---

# MongoDB Engine Entry

Use this as the primary create-time entry for MongoDB. Tier-1 MongoDB never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising any monitoring ceiling.
- Keep the legacy [kubeblocks-addon-mongodb](../kubeblocks-addon-mongodb/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `replicaset`
- `replicaset`: default path for normal HA MongoDB workloads.
- `sharding`: advanced path for large datasets or explicit horizontal partitioning; use only when the user really wants shard routers, config servers, and shard ReplicaSets.
- If the user only asks for "MongoDB" and does not justify distributed partitioning, stay on `replicaset`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence surfaces supported lines across MongoDB `4.0`, `5.0`, `6.0`, and `7.0`.
- When the user asks for sharding, keep all shard and routing components on the same addon-backed service line.

## Preflight Interpretation

- `storage_class`: required before apply because all ReplicaSet and shard members rely on PVC-backed storage.
- `volume_binding_mode`: confirm zone and binding behavior before multi-member HA rollout.
- `addon_readiness`: MongoDB addon must be installed first.
- MongoDB does not currently have the same observability ceiling as MySQL or PostgreSQL in the shipped truth, so do not oversell monitoring readiness during create.

## Sizing Profiles

- `demo`: small `replicaset` for application development or operator validation.
- `production`: `replicaset` or `sharding` with explicit anti-affinity, volume sizing, and backup posture from day 1.
- Treat `sharding` as an advanced scale path, not a default recommendation.

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
- Set `clusterDef: mongodb` for every MongoDB create path in this wave.
- `replicaset`: set `topology: replicaset`, keep a single `name: mongodb` component, and place `serviceVersion`, `replicas`, `resources`, and `volumeClaimTemplates` on that component.
- `sharding`: set `topology: sharding`, let the topology manage router, config, and shard roles, and do not collapse that path back into one `name: mongodb` component after the engine is identified.
- Validate with `kubectl apply --dry-run=server -f <mongodb-cluster.yaml>`.
- Apply with `kubectl apply -f <mongodb-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `exposed service`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: `mongosh mongodb://<service>:27017`.
- For `sharding`, validate through the `mongos` entrypoint, not by talking directly to a shard pod.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-backup`, and `kubeblocks-observability-router`.
- Password and Secret handling can route to [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md).
- Treat [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) as engine-specific validation work rather than a universal post-create promise.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); MongoDB recovery should stay on troubleshooting, switchover, or restore paths instead.
- Route unknown role, election, or exposure failures to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route MongoDB create through `kubeblocks-engine-generic` or `kubeblocks-addon-mongodb`.
- Do not collapse MongoDB sharding into a generic document-store path after the engine has already been identified.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Preserved detail remains in [legacy reference](../kubeblocks-addon-mongodb/references/reference.md).
- Current addon evidence: `examples/mongodb/cluster.yaml` for ReplicaSet, plus preserved sharding detail in the legacy reference.
