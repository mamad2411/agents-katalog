---
name: kubeblocks-engine-pulsar
version: "0.2.0"
description: Primary create-time entry for Pulsar on KubeBlocks. Use when the user wants to provision Pulsar and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown.
---

# Pulsar Engine Entry

Use this as the primary create-time entry for Pulsar. Tier-1 Pulsar never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising monitoring readiness.
- Keep Pulsar as a broker-plus-storage platform path, not as a generic streaming placeholder.

## Topology Selection

- Default topology: `basic`
- `basic`: default path with brokers, bookies, and ZooKeeper, suitable for most first deployments.
- `enhanced`: use when the rollout explicitly needs proxy and bookies-recovery components.
- `external-zookeeper`: use only when the platform already has a trusted ZooKeeper service reference and the user explicitly wants to reuse it.
- If the user cannot justify extra components or external coordination, stay on `basic`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence surfaces Pulsar `2.11.2` and `3.0.2`.
- If the user asks for "latest", stay on an addon-backed supported line rather than a raw upstream tag.

## Preflight Interpretation

- `storage_class`: required before apply because brokers and bookies persist to PVC-backed storage.
- `volume_binding_mode`: confirm storage placement before multi-component rollout.
- `addon_readiness`: Pulsar addon must be installed first.
- `dependency_clusters`: if the plan reuses an external ZooKeeper path, validate those service references before apply.

## Sizing Profiles

- `demo`: `basic` with small broker and bookie footprints for evaluation.
- `production`: `basic` or `enhanced` with explicit storage, monitoring, and component-count decisions made up front.
- Treat bookie count and broker count as real durability and throughput decisions, not just cosmetic replica numbers.

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
- Set `clusterDef: pulsar` for every Pulsar create path in this wave.
- `basic`: render the addon topology as `topology: pulsar-basic-cluster`, keep `name: broker`, `name: bookies`, and `name: zookeeper`, and size broker/bookie storage directly.
- `enhanced`: render the addon topology as `topology: pulsar-enhanced-cluster`, keep the `basic` components, and add `name: proxy` plus `name: bookies-recovery`.
- `external-zookeeper`: keep `clusterDef: pulsar`, use external service references for ZooKeeper, and do not leave both a local `name: zookeeper` quorum and an external ZooKeeper contract in the same manifest.
- Validate with `kubectl apply --dry-run=server -f <pulsar-cluster.yaml>`.
- Apply with `kubectl apply -f <pulsar-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `nodeport-or-loadbalancer`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: verify broker or proxy service readiness and use Pulsar admin or client tooling before handoff.
- If the rollout uses proxy, validate clients through the proxy path, not only broker-local connectivity.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-reconfigure`, and `kubeblocks-observability-router`.
- Treat credential and TLS work as engine-specific validation rather than assuming [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) or [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) are default Pulsar paths.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); Pulsar recovery should stay on troubleshoot or engine-specific repair workflows instead.
- Route broken service references, broker startup failures, or bookie issues to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route Pulsar create through `kubeblocks-engine-generic`, `kubeblocks-family-streaming`, `kubeblocks-engine-kafka`, or `kubeblocks-engine-rabbitmq`.
- If the request is really Kafka-style log streaming or queue-style RabbitMQ semantics, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Current addon evidence: `examples/pulsar/cluster-basic.yaml`, `examples/pulsar/cluster-enhanced.yaml`, `examples/pulsar/cluster-service-refer.yaml`.
