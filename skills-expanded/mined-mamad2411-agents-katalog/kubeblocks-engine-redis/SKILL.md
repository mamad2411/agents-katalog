---
name: kubeblocks-engine-redis
version: "0.2.0"
description: Primary create-time entry for Redis on KubeBlocks. Use when the user wants to provision Redis and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-redis skill remains only as a compatibility shim.
---

# Redis Engine Entry

Use this as the primary create-time entry for Redis. Tier-1 Redis never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising scrape or alert readiness.
- Keep the legacy [kubeblocks-addon-redis](../kubeblocks-addon-redis/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `replication`
- `standalone`: only for dev/test or throwaway cache workloads where HA is unnecessary.
- `replication`: default choice for most durable Redis rollouts because Sentinel-backed failover is already part of the path.
- `sharding`: choose only when the keyspace or write load has outgrown a single shard and the client path can speak Redis Cluster.
- If the user only needs a cache and has no explicit horizontal-scale requirement, stay on `replication`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current preserved evidence centers on Redis `7.2.4`, with `7.0.6` still available as an older supported line.
- For `sharding`, keep the `serviceVersion` aligned across shard template and sentinel or access components.

## Preflight Interpretation

- `storage_class`: required before apply because Redis persistence still lands on PVC-backed storage.
- `volume_binding_mode`: confirm zone behavior before choosing replicated or sharded layouts that span nodes.
- `addon_readiness`: Redis addon must be installed first.
- `observability_mode`: Redis has exporter, scrape, and alert examples, so pick existing-stack vs bootstrap before rollout.

## Sizing Profiles

- `demo`: `standalone` or small `replication` with modest CPU, memory, and PVCs.
- `production`: `replication` or `sharding` with explicit failover expectations, anti-affinity, and capacity headroom for rebalancing.
- For `sharding`, treat shard count as a capacity decision, not a cosmetic topology toggle.

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
- Set `clusterDef: redis` for every dedicated Redis path in this wave.
- `standalone`: set `topology: standalone`, keep a single `name: redis` component, and place `serviceVersion`, `resources`, and `volumeClaimTemplates` on that component.
- `replication`: set `topology: replication`, keep `name: redis` and `name: redis-sentinel`, and size replicas plus PVCs on the storage-bearing Redis component.
- `sharding`: declare `shardings:` instead of a single component, use template `name: redis`, set `componentDef: redis-cluster-7`, and put `serviceVersion`, `replicas`, `resources`, and `volumeClaimTemplates` on the shard template.
- Validate with `kubectl apply --dry-run=server -f <redis-cluster.yaml>`.
- Apply with `kubectl apply -f <redis-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `exposed service`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: `redis-cli -h <service> -p 6379 -a <password> PING`.
- For `sharding`, validate with `redis-cli -c` and a cluster command such as `CLUSTER INFO` before handoff.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-reconfigure`, `kubeblocks-op-backup`, and `kubeblocks-observability-router`.
- Password and Secret handling can route to [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md).
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); `rebuild_instance` is not the Redis recovery path in the current ops truth.
- Treat [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) as an engine-specific validation task, not an automatic follow-up promise for every Redis rollout.
- If failover, sharding state, or exposure behavior is unclear, route to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route Redis create through `kubeblocks-engine-generic` or `kubeblocks-addon-redis`.
- Do not collapse Redis into a generic cache path when the user is really asking for replication or cluster sharding semantics.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Preserved detail remains in [legacy reference](../kubeblocks-addon-redis/references/reference.md).
- Current addon evidence: `examples/redis/cluster-standalone.yaml`, `examples/redis/cluster.yaml`, `examples/redis/cluster-sharding.yaml`, `examples/redis/cluster-twemproxy.yaml`.
