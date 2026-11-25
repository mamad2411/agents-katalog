---
name: kubeblocks-engine-clickhouse
version: "0.2.0"
description: Primary create-time entry for ClickHouse on KubeBlocks. Use when the user wants to provision ClickHouse and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown.
---

# ClickHouse Engine Entry

Use this as the primary create-time entry for ClickHouse. Tier-1 ClickHouse never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising scrape readiness.
- Use addon examples as evidence, not as a reason to invent a different create path.

## Topology Selection

- Default topology: `cluster`
- `standalone`: use for local analytics evaluation or one-node testing only.
- `cluster`: default production path; this includes ClickHouse server shards plus ClickHouse Keeper coordination.
- If the user needs distributed analytics or failover, stay on `cluster`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence surfaces ClickHouse `22`, `24`, and `25`, with example-driven defaults anchored on shipped addon lines.
- If the user asks for "latest", stay on an addon-backed supported line instead of a raw upstream tag.

## Preflight Interpretation

- `storage_class`: required before apply because server and keeper data persist to PVCs.
- `volume_binding_mode`: confirm storage placement before distributed rollout.
- `addon_readiness`: ClickHouse addon must be installed first.
- `observability_mode`: ClickHouse has scrape examples; choose existing-stack vs bootstrap before rollout.

## Sizing Profiles

- `demo`: `standalone` or a very small `cluster` for query validation.
- `production`: `cluster` with keeper, shard sizing, and storage sized for analytical retention and merge pressure.
- Treat shard count and replica count as data-distribution decisions, not just replica cosmetics.

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
- Set `clusterDef: clickhouse` for every ClickHouse create path in this wave.
- `standalone`: set `topology: standalone` and keep the data plane as a single ClickHouse service path without `shardings:`.
- `cluster`: set `topology: cluster`, keep `name: ch-keeper` under `componentSpecs`, and put the actual ClickHouse data plane under `shardings:` with template `name: clickhouse`.
- Validate with `kubectl apply --dry-run=server -f <clickhouse-cluster.yaml>`.
- Apply with `kubectl apply -f <clickhouse-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `nodeport-or-loadbalancer`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: connect with `clickhouse-client --host <endpoint> --port 9000 --user admin --password`.
- If TLS is enabled, validate the secure client path before handing the endpoint to users.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-backup`, and `kubeblocks-observability-router`.
- Password and Secret handling can route to [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) when the create path used system accounts.
- Treat [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) as engine-specific validation work, not a universal default.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); ClickHouse recovery should stay on backup, restore, or troubleshoot paths.
- Route keeper, shard, or exposure failures to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route ClickHouse create through `kubeblocks-engine-generic` or `kubeblocks-family-ts-analytics`.
- If the request is really GreptimeDB or another analytics engine, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/clickhouse/cluster-standalone.yaml`, `examples/clickhouse/cluster.yaml`, `examples/clickhouse/cluster-with-nodeport.yaml`.
