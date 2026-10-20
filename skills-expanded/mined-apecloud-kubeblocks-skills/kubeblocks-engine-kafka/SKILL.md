---
name: kubeblocks-engine-kafka
version: "0.2.0"
description: Primary create-time entry for Kafka on KubeBlocks. Use when the user wants to provision Kafka and needs the correct topology, version, storage, sizing, connection, and next-hop guidance. Run kubeblocks-preflight first when environment readiness is unknown. The legacy kubeblocks-addon-kafka skill remains only as a compatibility shim.
---

# Kafka Engine Entry

Use this as the primary create-time entry for Kafka. Tier-1 Kafka never falls back to `kubeblocks-engine-generic`.

## Cold-Start Contract

- Run [kubeblocks-preflight](../kubeblocks-preflight/SKILL.md) whenever the environment is not already profiled.
- Treat [engine-create-matrix](../../references/coverage/engine-create-matrix.yaml) as the create-time truth for topology, version strategy, sizing, validation, next hops, and forbidden routes.
- Use [observability-capability-matrix](../../references/coverage/observability-capability-matrix.yaml) before promising scrape or alert readiness.
- Keep the legacy [kubeblocks-addon-kafka](../kubeblocks-addon-kafka/SKILL.md) path as preserved detail only, not as the primary cold-start route.

## Topology Selection

- Default topology: `combined`
- `combined`: default KRaft path when controller and broker can live in the same pod set and operational simplicity matters most.
- `separated`: use when the platform explicitly wants controller and broker failure domains or scale boundaries to diverge.
- Keep controller quorum odd after scale events; if the user cannot justify a separated layout, stay on `combined`.

## ServiceVersion / Version Strategy

- Strategy: use the stable addon default from current examples unless the user explicitly pins a serviceVersion
- Current addon evidence includes Kafka `3.3.2` and a preserved `2.8.2` line for external ZooKeeper cases.
- If the user asks for authentication, note that the shipped examples tie SASL/SCRAM guidance to the preserved `2.x` path rather than making it a default create promise.

## Preflight Interpretation

- `storage_class`: required before apply because brokers and controllers persist state to PVCs.
- `volume_binding_mode`: confirm storage binding before multi-member KRaft rollout.
- `addon_readiness`: Kafka addon must be installed first.
- `observability_mode`: Kafka has exporter and scrape examples; decide existing-stack vs bootstrap before rollout.

## Sizing Profiles

- `demo`: small `combined` footprint for evaluation or local integration tests.
- `production`: explicit controller quorum, broker sizing based on retention and throughput, and monitoring wired in from day 1.
- For `separated`, do not undersize controllers just because they are isolated from brokers.

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
- Set `clusterDef: kafka` for every Kafka create path in this wave.
- `combined`: render the addon topology as `topology: combined_monitor`, keep `name: kafka-combine` plus `name: kafka-exporter`, and preserve both `data` and `metadata` PVCs on the combined component.
- `separated`: render the addon topology as `topology: separated_monitor`, keep `name: kafka-broker`, `name: kafka-controller`, and `name: kafka-exporter`, and size broker plus controller PVCs independently.
- Validate with `kubectl apply --dry-run=server -f <kafka-cluster.yaml>`.
- Apply with `kubectl apply -f <kafka-cluster.yaml>`.
- Watch `kubectl get cluster <name> -n <ns> -w` until the phase is `Running`.

## Connection and Validation

- Supported connection methods: `in-cluster service`, `port-forward`, `nodeport-or-loadbalancer`
- First validation step: `kubectl get cluster <name> -n <ns>` and wait for `Running`.
- Default validation: get the bootstrap service and use `kafka-topics.sh --bootstrap-server <host>:<port> --list`.
- If the platform exposes Kafka externally, validate the advertised listener path before application handoff.

## Next Hops

- Day-2 operations currently route to `kubeblocks-op-lifecycle`, `kubeblocks-op-horizontal-scale`, `kubeblocks-op-reconfigure`, and `kubeblocks-observability-router`.
- Do not treat [kubeblocks-manage-accounts](../kubeblocks-manage-accounts/SKILL.md) as a guaranteed Kafka account path; the current ops truth marks account handling as `unknown`.
- Treat [kubeblocks-configure-tls](../kubeblocks-configure-tls/SKILL.md) as engine-specific design work rather than an automatic follow-up promise.
- Do not send this path to [kubeblocks-rebuild-replica](../kubeblocks-rebuild-replica/SKILL.md); Kafka recovery should stay on troubleshooting, restart, or engine-specific repair workflows instead.
- Route broken listener, broker, or controller state to [kubeblocks-troubleshoot](../kubeblocks-troubleshoot/SKILL.md).

## Forbidden Routes

- Never route Kafka create through `kubeblocks-engine-generic`, `kubeblocks-family-streaming`, `kubeblocks-addon-kafka`, `kubeblocks-engine-pulsar`, or `kubeblocks-engine-rabbitmq`.
- If the request is really queue-style RabbitMQ or bookie-backed Pulsar semantics, switch engines before apply.

## Evidence Anchors

- Use the evidence anchors below only as optional secondary evidence and parity checks after the manifest is already drafted here. A cold-start runtime should not need these files, but a stronger agent may inspect them when available.
- Preserved detail remains in [legacy reference](../kubeblocks-addon-kafka/references/reference.md).
- Current addon evidence: `examples/kafka/cluster-combined.yaml`, `examples/kafka/cluster-separated.yaml`.
