---
name: kubeblocks-engine-postgresql
version: "0.2.0"
description: Primary create-time entry for PostgreSQL on KubeBlocks. Use when the user wants to provision PostgreSQL and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-postgresql skill remains only as a compatibility shim.
---

# PostgreSQL Engine Entry

Use this as the primary create-time entry for PostgreSQL. Tier-1 PostgreSQL never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising scrape, dashboard, or alert readiness.
- Keep the legacy [kubeblocks-addon-postgresql](../kubeblocks-addon-postgresql/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `replication`
- `replication`: the normal Patroni-style HA path and the default choice for nearly every PostgreSQL rollout.
- `replication-with-etcd`: use only when the platform explicitly requires an external etcd-backed DCS shape instead of the default addon path.
- If the user does not know why they need `replication-with-etcd`, stay on `replication`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence surfaces supported lines across PostgreSQL `12`, `14`, `15`, `16`, and `17`, with stable examples anchored on the shipped defaults.
- If the user asks for "latest", stay within addon-backed supported lines rather than inventing a raw image tag.

## Preflight Interpretation

- `storage_class`: required before apply because PostgreSQL WAL and data PVCs should not rely on implicit defaults in production.
- `volume_binding_mode`: if the storage class binds late, confirm zone placement before choosing multi-replica HA.
- `addon_readiness`: PostgreSQL addon must be installed before rollout.
- `observability_mode`: PostgreSQL has exporter, scrape, and alert examples, so choose existing-stack vs bootstrap before create.

## Sizing Profiles

- `demo`: a compact `replication` shape with small PVCs and minimal resources for evaluation.
- `production`: dedicated storage, anti-affinity or spread constraints from preflight, and observability enabled from day 1.
- Treat `replication-with-etcd` as an advanced platform shape, not the default recommendation.

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
- Set `clusterDef: postgresql` for every PostgreSQL create path in this wave.
- `replication`: set `topology: replication`, keep a single `name: postgresql` component, and put `serviceVersion`, `replicas`, `resources`, and `volumeClaimTemplates` on that component.
- `replication-with-etcd`: still render `clusterDef: postgresql` with `topology: replication`, then inject env `ETCD3_HOST` and leave the Kubernetes DCS env unset so Patroni points at external etcd instead of the in-cluster default.
- Validate with `kubectl apply --dry-run=server -f <postgresql-cluster.yaml>`.
- Apply with `kubectl apply -f <postgresql-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `exposed service`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default SQL validation: `psql -h <service> -p 5432 -U postgres`.
- Validate replication readiness before handoff if the user explicitly asked for HA or failover.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-reconfigure`, `kubeblocks-op-backup`, and `kubeblocks-observability-router`.
- Access and connection hardening should route to [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) and [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md).
- Failed secondaries should route to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md) rather than direct pod deletion.
- If the rollout is blocked by a non-Running phase or unresolved storage/platform issue, route to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route PostgreSQL create through `kubeblocks-engine-generic`, `kubeblocks-family-sql`, `kubeblocks-addon-postgresql`, or `kubeblocks-engine-tidb`.
- Do not force PostgreSQL through MySQL- or TiDB-like semantics.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Preserved detail remains in [legacy reference](../kubeblocks-addon-postgresql/references/reference.md).
- Current addon evidence: `examples/postgresql/cluster.yaml`, `examples/postgresql/cluster-with-etcd.yaml`.
