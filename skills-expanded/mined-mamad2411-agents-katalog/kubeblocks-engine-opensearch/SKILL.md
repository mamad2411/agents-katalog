---
name: kubeblocks-engine-opensearch
version: "0.2.0"
description: Primary create-time entry for OpenSearch on KubeBlocks. Use when the user wants to provision OpenSearch and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown.
---

# OpenSearch Engine Entry

Use this as the primary create-time entry for OpenSearch. Tier-1 OpenSearch never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising monitoring readiness.
- Do not collapse OpenSearch back into Elasticsearch or a generic search family once the engine is known.

## Topology Selection

- Default topology: `cluster`
- `cluster`: the only supported Tier-1 create shape in the current truth; the shipped example includes the search core plus dashboard component.
- If the user only wants a small proof-of-concept, shrink replica counts inside `cluster` instead of inventing a second topology.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence centers on OpenSearch `2.7.0`.
- If the user asks for "latest", stay on an addon-backed supported line rather than a raw upstream tag.

## Preflight Interpretation

- `storage_class`: required before apply because the search core persists on PVC-backed storage.
- `volume_binding_mode`: confirm placement before a multi-replica rollout.
- `addon_readiness`: OpenSearch addon must be installed first.
- OpenSearch currently has no exporter evidence in the observability truth, so do not promise scrape-ready observability by default.

## Sizing Profiles

- `demo`: a small `cluster` for evaluation.
- `production`: `cluster` with persistent storage, enough memory for search workloads, and an explicit dashboard/access plan.
- Treat dashboard exposure as part of the rollout plan, not as an afterthought.

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
- Keep `name: opensearch` as the core storage-bearing component, use `componentDef: opensearch-core`, and set `serviceVersion`, `replicas: 3`, `resources`, and `volumeClaimTemplates` there.
- Add `name: dashboard` with `componentDef: opensearch-dashboard` only when the rollout really includes the UI path.
- Validate with `kubectl apply --dry-run=server -f <opensearch-cluster.yaml>`.
- Apply with `kubectl apply -f <opensearch-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `exposed service`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: port-forward the service and check `/_cluster/health`.
- If the dashboard is part of the rollout, validate both the API endpoint and the dashboard path before handoff.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-expose`, and `kubeblocks-observability-router`.
- Treat credential and TLS work as engine-specific validation rather than assuming [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) or [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) are default OpenSearch paths.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); OpenSearch recovery should stay on troubleshoot or restore-style paths.
- Route unhealthy search cluster or dashboard failures to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route OpenSearch create through `kubeblocks-engine-generic`, `kubeblocks-family-search`, or `kubeblocks-engine-elasticsearch`.
- If the request is really Elasticsearch compatibility work, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/opensearch/cluster.yaml`.
