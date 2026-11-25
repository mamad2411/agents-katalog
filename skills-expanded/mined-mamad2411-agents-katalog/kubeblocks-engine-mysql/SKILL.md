---
name: kubeblocks-engine-mysql
version: "0.2.0"
description: Primary create-time entry for MySQL on KubeBlocks. Use when the user wants to provision MySQL and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-mysql skill remains only as a compatibility shim.
---

# MySQL Engine Entry

Use this as the primary create-time entry for MySQL. Tier-1 MySQL never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising anything beyond metrics collection.
- Keep the legacy [kubeblocks-addon-mysql](../kubeblocks-addon-mysql/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `semisync`
- `semisync`: safest default for a normal HA MySQL rollout; use when the user wants primary-secondary semantics without extra routing layers.
- `mgr`: use when the platform explicitly wants native MySQL Group Replication and can afford three MySQL members from day one.
- `orchestrator`: use only when external Orchestrator-managed failover is part of the platform contract.
- `proxysql`: treat this as a frontend routing layer, not a reason to change the storage or HA shape by itself.
- If the user cannot clearly justify `mgr`, `orchestrator`, or `proxysql`, stay on `semisync`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Preserved example evidence centers on the MySQL `8.0` line, with `serviceVersion: 8.0.35` in the current example set.
- If the user only says "latest", choose the newest stable line already surfaced by addon examples or docs instead of inventing an image tag.

## Preflight Interpretation

- `storage_class`: required before apply because MySQL data PVCs are not safe to leave implicit in a production rollout.
- `volume_binding_mode`: if storage binds late and the cluster spans zones, confirm placement risk before choosing a multi-member HA path.
- `addon_readiness`: MySQL addon must already be installed; do not debug create failures before checking addon readiness.
- `observability_mode`: MySQL has exporter, scrape, and alert examples, so decide existing-stack vs bootstrap before rollout.

## Sizing Profiles

- `demo`: 1-2 MySQL members, modest CPU and memory, and 20Gi-class PVCs for evaluation or CI.
- `production`: dedicated storage, anti-affinity or spread policies from preflight, monitoring on day 1, and replicas sized for failover headroom.
- For `mgr`, production should start at three MySQL members; do not present a one- or two-member `mgr` shape as normal.

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
- `semisync`: keep a single `name: mysql` component, use `componentDef: mysql-8.0`, and set `serviceVersion`, `replicas`, `resources`, and `volumeClaimTemplates` directly on that component.
- `mgr`: keep a single `name: mysql` component, switch to `componentDef: mysql-mgr-8.0`, and keep `replicas: 3` as the minimum safe starting point.
- `orchestrator`: keep a single `name: mysql` component, use `componentDef: mysql-orc-8.0`, and add `serviceRefs:` that point at the external Orchestrator service before apply.
- `proxysql`: set `clusterDef: mysql`, set `topology: semisync-proxysql`, keep the storage-bearing `name: mysql` component, and add a second `name: proxysql` component for routing.
- Validate with `kubectl apply --dry-run=server -f <mysql-cluster.yaml>`.
- Apply with `kubectl apply -f <mysql-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `exposed service`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default MySQL path: use the root Secret and validate with `mysql -h <service> -P 3306 -u root -p`.
- If `proxysql` is part of the chosen route, validate through the ProxySQL listener before handing the endpoint to application teams.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-reconfigure`, `kubeblocks-op-backup`, and `kubeblocks-observability-router`.
- Access and connection hardening should route to [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) and [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md).
- Failed secondaries should route to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md) instead of improvised pod deletion.
- If phase, role, or storage state is unclear, stop and route to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route MySQL create through `kubeblocks-engine-generic`, `kubeblocks-family-sql`, `kubeblocks-addon-mysql`, `kubeblocks-engine-mariadb`, or `kubeblocks-engine-tidb`.
- If the request is really MariaDB or TiDB semantics, switch engines before applying anything.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Preserved detail remains in [legacy reference](../kubeblocks-addon-mysql/references/reference.md).
- Current addon evidence: `examples/mysql/cluster.yaml`, `examples/mysql/cluster-mgr.yaml`, `examples/mysql/cluster-orc.yaml`, `examples/mysql/cluster-proxysql.yaml`.
