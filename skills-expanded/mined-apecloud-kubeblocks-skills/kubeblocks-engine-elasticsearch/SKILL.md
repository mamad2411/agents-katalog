---
name: kubeblocks-engine-elasticsearch
version: "0.2.0"
description: Primary create-time entry for Elasticsearch on KubeBlocks. Use when the user wants to provision Elasticsearch and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-elasticsearch skill remains only as a compatibility shim.
---

# Elasticsearch Engine Entry

Use this as the primary create-time entry for Elasticsearch. Tier-1 Elasticsearch never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising anything above scrape readiness.
- Keep the legacy [kubeblocks-addon-elasticsearch](../kubeblocks-addon-elasticsearch/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `multi-node`
- `single-node`: dev/test only, or when the user explicitly accepts no HA and limited scale.
- `multi-node`: default production path with separated master and data roles.
- If the user asks for search or log analytics without any special constraint, stay on `multi-node`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence centers on Elasticsearch `8.8.2`, with preserved `7.8.1` examples still present for older compatibility.
- If the user asks for Kibana, keep it on the same supported line as the Elasticsearch data plane.

## Preflight Interpretation

- `storage_class`: required before apply because master and data components both rely on PVC-backed storage.
- `volume_binding_mode`: confirm zone behavior before multi-node data placement.
- `addon_readiness`: Elasticsearch addon must be installed first.
- Elasticsearch is only `scrape-ready` in the current observability truth, so do not promise dashboards or alert bundles by default.

## Sizing Profiles

- `demo`: `single-node` or a very small `multi-node` footprint for evaluation.
- `production`: `multi-node`, dedicated data PVCs, explicit spread or anti-affinity, and enough memory for JVM heap planning.
- Do not recommend `single-node` for anything that needs availability or shard movement.

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
- `single-node`: keep one `name: mdit` component, use `componentDef: elasticsearch-8`, and set `serviceVersion`, `replicas: 1`, `resources`, and `volumeClaimTemplates` directly on that component.
- `multi-node`: split the manifest into `name: master` and `name: data`, use `componentDef: elasticsearch-master-8` and `componentDef: elasticsearch-data-8`, and size master/data replicas independently.
- Validate with `kubectl apply --dry-run=server -f <elasticsearch-cluster.yaml>`.
- Apply with `kubectl apply -f <elasticsearch-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `exposed service`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: `curl -X GET http://<service>:9200/_cluster/health?pretty`.
- If the service is exposed externally, validate the public endpoint and role layout before handoff.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-expose`, and `kubeblocks-observability-router`.
- Treat credential and TLS work as engine-specific validation work rather than assuming [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) or [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) are default Elasticsearch paths.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); that recovery flow is not the Elasticsearch path in the current truth.
- Route non-green cluster health, shard allocation issues, or exposure failures to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route Elasticsearch create through `kubeblocks-engine-generic`, `kubeblocks-family-search`, `kubeblocks-addon-elasticsearch`, or `kubeblocks-engine-opensearch`.
- If the user really wants OpenSearch semantics or dashboard defaults, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/elasticsearch/cluster-multi-node.yaml`, `examples/elasticsearch/cluster-single-node.yaml`, `examples/elasticsearch/cluster-with-kibana.yaml`.
- There is no separate legacy reference file for this engine in the current repository snapshot.
