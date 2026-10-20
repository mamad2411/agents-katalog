---
name: kubeblocks
version: "0.3.0"
description: Route database work on Kubernetes to the right KubeBlocks skill. Use this as the top-level entrypoint when the user needs a database, database operations, or database observability on Kubernetes. The root skill only decides the next hop; detailed workflows live in the leaf skills.
compatibility:
  required_tools:
    - kubectl
    - helm
  optional_tools:
    - npx
  notes: Requires Kubernetes access for install, preflight, provisioning, and operations. For local development, create a cluster first.
---

# KubeBlocks Router

This root skill is **router only**. It should decide the next step, not become a second README and not restate every leaf workflow.

Use:

- [AGENTS.md](AGENTS.md) for the cold-start agent operating model
- [README.md](README.md) for repository layout, truth layers, installation, and validation

## Route Order

Always route in this order:

1. **No Kubernetes cluster yet**
   Route to [create-local-k8s-cluster](skills/kubeblocks-create-local-k8s-cluster/SKILL.md).

2. **Kubernetes exists, but KubeBlocks is not installed**
   Route to [install-kubeblocks](skills/kubeblocks-install/SKILL.md).

3. **First-time provisioning, or environment readiness is unknown**
   Route to [kubeblocks-preflight](skills/kubeblocks-preflight/SKILL.md) before any engine-specific provisioning.

4. **Provision a database after preflight**
   - MySQL → [engine-mysql](skills/kubeblocks-engine-mysql/SKILL.md)
   - PostgreSQL → [engine-postgresql](skills/kubeblocks-engine-postgresql/SKILL.md)
   - Redis → [engine-redis](skills/kubeblocks-engine-redis/SKILL.md)
   - MongoDB → [engine-mongodb](skills/kubeblocks-engine-mongodb/SKILL.md)
   - Kafka → [engine-kafka](skills/kubeblocks-engine-kafka/SKILL.md)
   - Elasticsearch → [engine-elasticsearch](skills/kubeblocks-engine-elasticsearch/SKILL.md)
   - Milvus → [engine-milvus](skills/kubeblocks-engine-milvus/SKILL.md)
   - Qdrant → [engine-qdrant](skills/kubeblocks-engine-qdrant/SKILL.md)
   - RabbitMQ → [engine-rabbitmq](skills/kubeblocks-engine-rabbitmq/SKILL.md)
   - ClickHouse → [engine-clickhouse](skills/kubeblocks-engine-clickhouse/SKILL.md)
   - MariaDB → [engine-mariadb](skills/kubeblocks-engine-mariadb/SKILL.md)
   - MinIO → [engine-minio](skills/kubeblocks-engine-minio/SKILL.md)
   - OpenSearch → [engine-opensearch](skills/kubeblocks-engine-opensearch/SKILL.md)
   - Pulsar → [engine-pulsar](skills/kubeblocks-engine-pulsar/SKILL.md)
   - TiDB → [engine-tidb](skills/kubeblocks-engine-tidb/SKILL.md)
   - Other engines without dedicated entry skills → [engine-generic](skills/kubeblocks-engine-generic/SKILL.md)

5. **Operate an existing cluster**
   Route to the matching capability layer:
   - lifecycle → [op-lifecycle](skills/kubeblocks-op-lifecycle/SKILL.md)
   - horizontal scale → [op-horizontal-scale](skills/kubeblocks-op-horizontal-scale/SKILL.md)
   - vertical scale → [op-vertical-scale](skills/kubeblocks-op-vertical-scale/SKILL.md)
   - volume expansion → [op-volume-expansion](skills/kubeblocks-op-volume-expansion/SKILL.md)
   - parameters → [op-reconfigure](skills/kubeblocks-op-reconfigure/SKILL.md)
   - backup → [op-backup](skills/kubeblocks-op-backup/SKILL.md)
   - restore → [op-restore](skills/kubeblocks-op-restore/SKILL.md)
   - expose → [op-expose](skills/kubeblocks-op-expose/SKILL.md)
   - switchover → [op-switchover](skills/kubeblocks-op-switchover/SKILL.md)
   - engine upgrade → [op-upgrade](skills/kubeblocks-op-upgrade/SKILL.md)
   - account / password management → [manage-accounts](skills/kubeblocks-manage-accounts/SKILL.md)
   - TLS / mTLS → [configure-tls](skills/kubeblocks-configure-tls/SKILL.md)
   - safe deletion → [delete-cluster](skills/kubeblocks-delete-cluster/SKILL.md)

6. **Observability**
   - Broad observability ask → [observability-router](skills/kubeblocks-observability-router/SKILL.md)
   - Existing Prometheus/Grafana stack → [observability-existing-stack](skills/kubeblocks-observability-existing-stack/SKILL.md)
   - No monitoring base yet → [observability-bootstrap-stack](skills/kubeblocks-observability-bootstrap-stack/SKILL.md)
   - If the user only says “set up monitoring”, use the shim [setup-monitoring](skills/kubeblocks-setup-monitoring/SKILL.md), which routes to the right observability branch.

7. **Troubleshooting**
   Route to [troubleshoot](skills/kubeblocks-troubleshoot/SKILL.md) from any stage when state is unknown, capability is unclear, or observed behavior is broken.
   For replica recovery or HA repair after troubleshooting, also consider [rebuild-replica](skills/kubeblocks-rebuild-replica/SKILL.md).

## Hard Routing Rules

- Do **not** route the Tier-1 engine set to [engine-generic](skills/kubeblocks-engine-generic/SKILL.md) or to any family/taxonomy-only explanation layer.
- Do **not** provision a first-time database without going through [kubeblocks-preflight](skills/kubeblocks-preflight/SKILL.md) when environment readiness is unknown.
- Do **not** send agents back to raw addon examples as the primary create-time path once a dedicated Tier-1 engine entry exists.
- Do **not** require `kubeblocks-addons` or KubeBlocks core repo checkouts as runtime prerequisites. The runtime path must work from this repo plus official public docs.
- Do **not** equate “metrics exist” with “monitoring is delivered”. Observability must declare whether it is only `metrics-ready`, `scrape-ready`, `dashboard-ready`, or `alerting-ready`.
- Do **not** recommend legacy `kubeblocks-addon-*`, `kubeblocks-create-cluster`, or old Day-2 names as the primary path when the corresponding `kubeblocks-engine-*`, `kubeblocks-engine-generic`, or `kubeblocks-op-*` entry exists.

## Recommendation Bundle Contract

[kubeblocks-preflight](skills/kubeblocks-preflight/SKILL.md) should produce an environment profile / recommendation bundle that downstream engine-entry skills can consume. At minimum it must answer:

- Recommended `storageClassName`
- Whether topology-aware / `WaitForFirstConsumer` storage is required
- Which engine entry skill to use
- Which generic paths are forbidden
- Demo vs production sizing guidance
- Whether observability should go to `existing-stack` or `bootstrap-stack`

## Common Misroutes To Prevent

- **ACK multi-AZ + PostgreSQL/MySQL**:
  Route to `preflight` first. Do not jump directly from install to addon provisioning.
- **Existing Prometheus/Grafana**:
  Route to `observability-existing-stack`, not full monitoring bootstrap.
- **Unknown or low-frequency engines**:
  Only then use [engine-generic](skills/kubeblocks-engine-generic/SKILL.md) as the `other-addons` fallback.
