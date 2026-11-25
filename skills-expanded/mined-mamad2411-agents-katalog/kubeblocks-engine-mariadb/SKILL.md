---
name: kubeblocks-engine-mariadb
version: "0.2.0"
description: Primary create-time entry for MariaDB on KubeBlocks. Use when the user wants to provision MariaDB and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown.
---

# MariaDB Engine Entry

Use this as the primary create-time entry for MariaDB. Tier-1 MariaDB never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising anything above the currently documented ceiling.
- Do not treat MariaDB as a drop-in MySQL route just because the SQL surface looks similar.

## Topology Selection

- Default topology: `standalone`
- `standalone`: the only supported Tier-1 create shape in the current addon evidence; replication is not yet a safe default path.
- If the user asks for MariaDB HA semantics, stop and explain that the current rollout truth does not promote a replicated MariaDB path yet.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence centers on MariaDB `10.6.15`.
- If the user asks for "latest", stay on an addon-backed supported line rather than inventing an upstream tag.

## Preflight Interpretation

- `storage_class`: required before apply because MariaDB data still lands on PVC-backed storage.
- `volume_binding_mode`: confirm storage placement before promising future growth or strict node policies.
- `addon_readiness`: MariaDB addon must be installed first.
- MariaDB currently has no exporter evidence in the observability truth, so do not promise scrape-ready observability by default.

## Sizing Profiles

- `demo`: a single MariaDB instance with modest CPU, memory, and storage.
- `production`: still `standalone` in the current truth, but with larger PVCs, backups, and a clear external recovery story.
- Do not present MariaDB as a Tier-1 HA default until the addon evidence changes.

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
- Keep one `name: mariadb` component, use `componentDef: mariadb`, and set `serviceVersion`, `replicas: 1`, `resources`, and `volumeClaimTemplates` on that component.
- Validate with `kubectl apply --dry-run=server -f <mariadb-cluster.yaml>`.
- Apply with `kubectl apply -f <mariadb-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: `mysql -h <service> -P 3306 -u root -p`.
- Keep create-time validation simple and do not promise a hidden replication layout.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-vertical-scale`, `kubeblocks-op-volume-expansion`, and `kubeblocks-observability-router`.
- Password handling can route to [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md).
- Treat [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) as engine-specific validation work.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); that recovery flow is not part of the current MariaDB truth.
- Route uncertain failure or unsupported HA requests to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route MariaDB create through `kubeblocks-engine-generic`, `kubeblocks-family-sql`, or `kubeblocks-engine-mysql`.
- If the user really wants MySQL HA topologies, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/mariadb/cluster.yaml`.
