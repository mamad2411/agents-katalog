---
name: kubeblocks-engine-tidb
version: "0.2.0"
description: Primary create-time entry for TiDB on KubeBlocks. Use when the user wants to provision TiDB and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown.
---

# TiDB Engine Entry

Use this as the primary create-time entry for TiDB. Tier-1 TiDB never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising scrape readiness.
- Do not reduce TiDB to a generic SQL path or a MySQL/PostgreSQL substitute once the engine is known.

## Topology Selection

- Default topology: `standard`
- `standard`: the only supported Tier-1 create shape in the current truth; it already includes the PD, TiKV, and TiDB components required for a real cluster.
- If the user asks about TiFlash or other analytical extensions, treat that as a future expansion, not as the default create path in this wave.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence surfaces TiDB `8.4.0`, `7.5.2`, `7.1.5`, and `6.5.10`.
- If the user asks for "latest", stay on an addon-backed supported line rather than a raw upstream tag.

## Preflight Interpretation

- `storage_class`: required before apply because PD and TiKV components both rely on PVC-backed storage.
- `volume_binding_mode`: confirm placement before multi-component rollout, especially for TiKV data.
- `addon_readiness`: TiDB addon must be installed first.
- `observability_mode`: TiDB has scrape evidence, so choose existing-stack vs bootstrap before rollout.

## Sizing Profiles

- `demo`: a compact `standard` cluster with reduced TiKV and TiDB capacity for evaluation.
- `production`: `standard` with storage sized for TiKV, quorum-aware PD sizing, and explicit observability from day 1.
- Treat TiKV storage as the dominant capacity constraint in create-time planning.

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
- Set `clusterDef: tidb` for every TiDB create path in this wave.
- The agent-facing `standard` path maps to addon `topology: cluster`.
- Keep `name: tidb-pd`, `name: tikv`, and `name: tidb` on the same `serviceVersion`, with PVC-backed storage on the PD and TiKV components before apply.
- Validate with `kubectl apply --dry-run=server -f <tidb-cluster.yaml>`.
- Apply with `kubectl apply -f <tidb-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: connect through the SQL entrypoint with the MySQL protocol, typically `mysql -h <service> -P 4000 -u root -p`.
- Validate PD and TiKV readiness before handing the SQL endpoint to application teams.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-vertical-scale`, `kubeblocks-op-volume-expansion`, and `kubeblocks-observability-router`.
- Treat credential and TLS work as engine-specific validation rather than assuming [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) or [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) are default TiDB paths.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); TiDB recovery should stay on troubleshoot or engine-specific repair flows instead.
- Route PD, TiKV, or SQL-plane failures to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route TiDB create through `kubeblocks-engine-generic`, `kubeblocks-family-sql`, `kubeblocks-engine-mysql`, or `kubeblocks-engine-postgresql`.
- If the user really wants MySQL or PostgreSQL semantics, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/tidb/cluster.yaml`.
