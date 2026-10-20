---
name: druid-realtime-ingest
description: >
  Operate Apache Druid realtime/streaming ingest safely on owned clusters: supervisors,
  Kafka/Kinesis indexing, schema/rollup, authenticity of input, authn on Overlord/Router,
  and lag/failure runbooks. Use when Druid supervisor, kafka ingestion, realtime tasks,
  IoConfig/tuningConfig, or securing Druid ingest paths — not for attacking open Druid UIs.
---

# Druid Realtime Ingest

## Scope And Authorization

- **In scope:** Druid clusters, Kafka/Kinesis topics, and schemas you operate.
- **Out of scope:** Probing third-party Druid consoles; injecting events into foreign topics.
- Prefer staging supervisors before production parallel loads.
- Redact credentials in supervisor specs and tickets.
- Pair with Kafka security skills, `observability-metrics-tracing`, and `code-quality-standards`.

## When To Use

- Standing up or hardening Kafka/Kinesis → Druid streaming ingest.
- Fixing supervisor lag, task failures, or schema explode.
- Ensuring Overlord/Coordinator/Router are not open anonymous.
- Designing rollup/timestamp strategies for realtime datasources.
- Incident: bad events poison segments.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Batch Hadoop/MiddleManager deep ops | broader Druid ops docs |
| Kafka ACL design detail | Kafka security skills |
| General observability | `observability-metrics-tracing` |
| DynamoDB (different store) | dynamodb skills |
| Code quality baseline | `code-quality-standards` |

## Architecture (streaming)

```text
Producers → Kafka/Kinesis → Druid Supervisor → Indexing tasks →
  Incremental segments → Hand off / queryable datasource
```

| Component | Role |
| --- | --- |
| Supervisor | Manages task lifecycle for a topic |
| ioConfig | Input topic, consumer props, input format |
| tuningConfig | Task counts, partitions, windows |
| dataSchema | timestamp, dimensions, metrics, transform |
| Overlord | Task management API |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster version, topic SLAs, query latency needs, security mode (Druid auth).
2. Success: lag under SLO; exactly-once/at-least-once expectations documented; auth enabled; bad-data quarantine plan.
3. Owners for schema changes.

### 2. Inventory current ingest

```bash
# Authorized admin APIs (examples; secure them!)
curl -sS https://overlord.example/druid/indexer/v1/supervisor?full | head
# Check task failures in Overlord UI/API
```

1. List supervisors, datasources, retention.
2. Note if Router/Overlord exposed without auth.

### 3. Secure the control and data plane

1. Enable Druid authentication/authorization; TLS everywhere.
2. Kafka: SASL/SSL; least-privilege consumer group; ACLs on topics.
3. Network: Overlord not public internet.
4. Secrets for Kafka passwords via env/secret mounts—not committed supervisor JSON in git with passwords.

### 4. Author supervisor spec (illustrative)

```json
{
  "type": "kafka",
  "dataSchema": {
    "dataSource": "events",
    "timestampSpec": { "column": "ts", "format": "iso" },
    "dimensionsSpec": { "dimensions": ["userId", "eventType"] },
    "metricsSpec": [{ "type": "count", "name": "count" }],
    "granularitySpec": {
      "type": "uniform",
      "segmentGranularity": "HOUR",
      "queryGranularity": "MINUTE",
      "rollup": true
    }
  },
  "ioConfig": {
    "topic": "app.events",
    "inputFormat": { "type": "json" },
    "consumerProperties": {
      "bootstrap.servers": "kafka:9092"
    },
    "taskCount": 2,
    "replicas": 1
  },
  "tuningConfig": {
    "type": "kafka",
    "maxRowsInMemory": 100000
  }
}
```

1. Validate JSON/events sample against schema; reject huge dimension cardinality surprises.
2. Use transforms/filters to drop poison fields early.
3. Pin task image/version with cluster.

### 5. Rollup, time, and late data

1. Choose `segmentGranularity` vs query needs and late-arrival windows.
2. Document timezone and timestamp field trust (client clock skew).
3. High cardinality dimensions destroy performance—prefer IDs + lookups.

### 6. Operate lag and failures

| Symptom | Actions |
| --- | --- |
| Growing lag | Scale taskCount; check Kafka; pause producers; tune maxRows |
| Task crash loops | Parse errors; OOM; check MiddleManager logs |
| Schema explosion | Block new dims; fix producers |
| Duplicate events | Understand at-least-once; idempotent metrics design |

```bash
# Kafka lag (owned cluster tooling)
# kafka-consumer-groups --describe --group druid-...
```

1. Alerts: supervisor unhealthy, lag, failed tasks, disk on MiddleManagers.
2. Runbook: pause supervisor → fix → resume; avoid dual supervisors fighting.

### 7. Verify and hand off

1. Query datasource for recent time intervals; compare counts to Kafka approx.
2. Chaos: kill task; ensure supervisor restores.
3. Document schema registry process and who can POST supervisors.
4. Apply `code-quality-standards` to any producer code.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | TLS + Druid auth + Kafka ACL | Open Overlord :8888 |
| Schema | Bounded dims | Unlimited free-text dims |
| Secrets | Mounted/env | Password in git JSON |
| Lag | Alert + scale | Discover days later |
| Time | Clear ts policy | Mixed epochs/timezones silent |
| Deploy | Staging first | Prod-only experiment |

## Output Checklist

- [ ] Supervisors and topics inventoried
- [ ] Control plane authenticated and networked safely
- [ ] Kafka ACLs/TLS configured
- [ ] Schema/rollup/time policy documented
- [ ] Lag and task failure alerts live
- [ ] Poison event handling defined
- [ ] Staging validation of supervisor done
- [ ] Runbook for pause/resume/scale
- [ ] Secrets not in git
- [ ] Residual risk noted

## Rules

- Druid ingest APIs are powerful—authenticate and authorize.
- Control cardinality and timestamps deliberately.
- Streaming is usually at-least-once—design metrics accordingly.
- Owned clusters only.
- Focus on realtime/streaming ingest safety and ops.
