---
name: kubeblocks-engine-rabbitmq
version: "0.2.0"
description: Primary create-time entry for RabbitMQ on KubeBlocks. Use when the user wants to provision RabbitMQ and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-rabbitmq skill remains only as a compatibility shim.
---

# RabbitMQ Engine Entry

Use this as the primary create-time entry for RabbitMQ. Tier-1 RabbitMQ never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising scrape readiness.
- Keep the legacy [kubeblocks-addon-rabbitmq](../kubeblocks-addon-rabbitmq/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `cluster`
- `cluster`: the only supported Tier-1 create shape in the current truth; scale the replica count instead of inventing a separate single-node path.
- Keep quorum-queue semantics in mind and favor odd replica counts when the cluster is meant to survive member failure.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence surfaces RabbitMQ `3.8` through `3.13`, with the shipped examples anchored on addon-backed defaults.
- If the user asks for "latest", stay on a supported addon line instead of a raw upstream tag.

## Preflight Interpretation

- `storage_class`: required before apply because RabbitMQ queue data persists on PVCs.
- `volume_binding_mode`: confirm placement behavior before multi-member rollout.
- `addon_readiness`: RabbitMQ addon must be installed first.
- `observability_mode`: RabbitMQ has exporter and scrape evidence, so choose existing-stack vs bootstrap before rollout.

## Sizing Profiles

- `demo`: a small `cluster` for AMQP validation or developer testing.
- `production`: `cluster` with odd replica counts, persistent storage, and clear exposure requirements for AMQP and management UI.
- Do not present an even-sized production cluster as the safe default for quorum queues.

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
- Keep one `name: rabbitmq` component, use `componentDef: rabbitmq`, and set `serviceVersion`, `replicas: 3`, `resources`, and `volumeClaimTemplates` on that component.
- Validate with `kubectl apply --dry-run=server -f <rabbitmq-cluster.yaml>`.
- Apply with `kubectl apply -f <rabbitmq-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `exposed service`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: port-forward the management service and check cluster status before handing the endpoint to application teams.
- If the user needs AMQP access, validate both the broker path and the management/UI path.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-reconfigure`, and `kubeblocks-observability-router`.
- Treat credential and TLS work as engine-specific validation rather than assuming [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) or [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) are default RabbitMQ paths.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); RabbitMQ recovery should stay on cluster repair or troubleshoot paths.
- Route unhealthy quorum behavior, peer discovery failures, or management-plane issues to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route RabbitMQ create through `kubeblocks-engine-generic`, `kubeblocks-family-streaming`, `kubeblocks-addon-rabbitmq`, `kubeblocks-engine-kafka`, or `kubeblocks-engine-pulsar`.
- If the request is really log-streaming Kafka or Pulsar semantics, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/rabbitmq/cluster.yaml`.
- There is no separate legacy reference file for this engine in the current repository snapshot.
