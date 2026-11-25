---
name: kafka-integration
description: "Connect applications to Apache Kafka 4.x (KRaft), Confluent Cloud/Platform or AWS MSK — client configuration with kafkajs or Confluent clients, SASL/SCRAM, mTLS, PLAIN, OAUTHBEARER and MSK IAM auth, Schema Registry, Kafka Connect, ksqlDB, ACLs and RBAC, using the standard Kafka CLI tools and REST APIs. Use when wiring an app to a Kafka cluster, configuring client security, or managing topics, consumer groups, schemas, connectors or access control."
keywords: [kafka, streaming, event-driven, schema-registry, kafka-connect, ksqldb, confluent, msk, pubsub, messaging, kraft, docker]
---

# Apache Kafka Integration

Practical guidance for connecting applications to a Kafka cluster and administering the pieces around it —
whichever distribution is in play. Pair with `kafka-event-driven-architecture` for design patterns
(event modelling, Streams, delivery semantics).

> **There is no bundled CLI.** Earlier versions of this skill documented an `npm run kafka …` wrapper; that
> tool does not exist in this hub. Everything below uses the **standard Kafka CLI tools** (`bin/kafka-*.sh`,
> or `/opt/kafka/bin/` inside the `apache/kafka` image), the **Confluent CLI**, the documented **REST APIs**
> (Schema Registry, Connect, ksqlDB), or **client code** (kafkajs / `@confluentinc/kafka-javascript`, the
> Java client, `confluent-kafka-python`).

## Kafka 4.x baseline (current as of 2026)

- **KRaft only.** Apache Kafka 4.0 removed ZooKeeper; Confluent Platform 8.x is KRaft-only as well. Never
  generate `zookeeper.connect`, `--zookeeper` flags or a ZooKeeper service. A 3.x ZooKeeper cluster must be
  migrated to KRaft (on 3.9) before upgrading to 4.x.
- All admin CLIs take `--bootstrap-server` (plus `--command-config client.properties` for a secured cluster).
- Brokers/Connect/tools need Java 17+; Java clients and Streams need Java 11+. 4.x brokers reject clients
  older than 2.1.
- The new consumer rebalance protocol (KIP-848, `group.protocol=consumer`) is GA — use it where the client supports it.

## Deployment types

| Deployment | Auth options | Extras | Notes |
|---|---|---|---|
| Apache Kafka 4.x (self-hosted) | SASL/PLAIN, SASL/SCRAM, mTLS, OAUTHBEARER, Kerberos | core only | KRaft controllers + brokers |
| Confluent Platform 8.x | SASL/SCRAM, mTLS, LDAP, OAuth, RBAC | Schema Registry, Connect, ksqlDB, Control Center | KRaft-only |
| Confluent Cloud | API key (SASL/PLAIN over TLS), OAuth | fully managed SR / Connect / ksqlDB / Flink | managed |
| AWS MSK | IAM, SASL/SCRAM, mTLS | AWS integration | new clusters run KRaft; older ones may still be ZooKeeper-based and managed by AWS |
| Azure Event Hubs (Kafka endpoint) | SASL/PLAIN with connection string, OAuth (Entra ID) | Kafka protocol compatibility | not every Kafka API is supported |

## Local development cluster

```bash
# Official Apache Kafka image — single-node KRaft broker+controller. Pin a current 4.x tag.
docker run -d --name kafka -p 9092:9092 apache/kafka:4.1.0

# Or from the tarball (https://kafka.apache.org/downloads):
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t "$KAFKA_CLUSTER_ID" -c config/server.properties
bin/kafka-server-start.sh config/server.properties
```

On Windows, the tarball ships `bin\windows\*.bat` equivalents; Docker or WSL is the smoother path.
For a local Schema Registry / Connect / ksqlDB stack, use Confluent's `cp-all-in-one` Compose files for
the current Confluent Platform release (the KRaft variant).

## Client configuration

Keep connection settings in environment variables (never hardcode secrets; see the hub's credential rules):

```bash
KAFKA_BROKERS=broker1:9092,broker2:9092
KAFKA_CLIENT_ID=my-service
KAFKA_SASL_MECHANISM=SCRAM-SHA-512     # PLAIN | SCRAM-SHA-256 | SCRAM-SHA-512 | OAUTHBEARER
KAFKA_SASL_USERNAME=${...}             # from the secret store
KAFKA_SASL_PASSWORD=${...}
SCHEMA_REGISTRY_URL=https://sr.example.com
```

### Node.js

KafkaJS is no longer actively maintained. For new work prefer **`@confluentinc/kafka-javascript`** (librdkafka-based,
ships a KafkaJS-compatible API under `.KafkaJS`); existing KafkaJS code ports with minimal changes.

```js
// kafkajs-style API (works with kafkajs, and with @confluentinc/kafka-javascript's KafkaJS namespace
// after its config differences are applied — check that package's migration guide)
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: process.env.KAFKA_CLIENT_ID,
  brokers: process.env.KAFKA_BROKERS.split(','),
  ssl: true,
  sasl: {
    mechanism: process.env.KAFKA_SASL_MECHANISM.toLowerCase(), // 'plain' | 'scram-sha-256' | 'scram-sha-512'
    username: process.env.KAFKA_SASL_USERNAME,
    password: process.env.KAFKA_SASL_PASSWORD,
  },
});

const producer = kafka.producer({ idempotent: true });
await producer.connect();
await producer.send({
  topic: 'user-events',
  messages: [{ key: 'user-123', value: JSON.stringify({ action: 'login' }) }],
});

const consumer = kafka.consumer({ groupId: 'user-events-processor' });
await consumer.connect();
await consumer.subscribe({ topic: 'user-events', fromBeginning: true });
await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    // idempotent handler — a message can be redelivered after a rebalance
  },
});
```

Schema Registry from Node: `@kafkajs/confluent-schema-registry` (encode/decode Avro, Protobuf, JSON Schema) or the
Schema Registry client bundled with Confluent's JavaScript packages.

### Java / Spring and Python

- Java: `org.apache.kafka:kafka-clients` (or Spring for Apache Kafka) — `security.protocol`, `sasl.mechanism`,
  `sasl.jaas.config` properties; see `kafka-event-driven-architecture` for full examples.
- Python: `confluent-kafka` — same librdkafka property names (`bootstrap.servers`, `security.protocol`, `sasl.*`).

## Authentication recipes (client properties)

| Method | Key properties |
|---|---|
| SASL/PLAIN (always with TLS) | `security.protocol=SASL_SSL`, `sasl.mechanism=PLAIN`, JAAS `PlainLoginModule` |
| SASL/SCRAM | `security.protocol=SASL_SSL`, `sasl.mechanism=SCRAM-SHA-512` (or 256), JAAS `ScramLoginModule` |
| mTLS | `security.protocol=SSL`, truststore/keystore (Java) or `ssl.ca.location`/`ssl.certificate.location`/`ssl.key.location` (librdkafka) |
| OAUTHBEARER (Confluent Cloud, OIDC) | `sasl.mechanism=OAUTHBEARER`, token endpoint URL, client id/secret from the secret store |
| AWS MSK IAM | Java: `aws-msk-iam-auth` (`AWS_MSK_IAM` or OAUTHBEARER with its callback handler); other languages: AWS's MSK IAM SASL signer library producing OAUTHBEARER tokens |
| Confluent Cloud API key | SASL/PLAIN over TLS — API key as username, secret as password |

A secured cluster's admin CLI uses the same properties in a file:

```properties
# client.properties — values injected from the environment / secret store, never committed
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-512
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="..." password="...";
```

## Administration with the standard tools

```bash
B="--bootstrap-server localhost:9092"  # add --command-config client.properties when secured

# Topics
bin/kafka-topics.sh $B --create --topic user-events --partitions 6 --replication-factor 3 \
  --config retention.ms=604800000 --config min.insync.replicas=2
bin/kafka-topics.sh $B --list
bin/kafka-topics.sh $B --describe --topic user-events
bin/kafka-configs.sh $B --alter --entity-type topics --entity-name user-events --add-config retention.ms=172800000
bin/kafka-topics.sh $B --delete --topic user-events

# Quick produce / consume
bin/kafka-console-producer.sh $B --topic user-events --property parse.key=true --property key.separator=:
bin/kafka-console-consumer.sh $B --topic user-events --group debug-reader --from-beginning

# Consumer groups: list, lag, reset (group must be inactive to reset)
bin/kafka-consumer-groups.sh $B --list
bin/kafka-consumer-groups.sh $B --describe --group user-events-processor     # LAG column
bin/kafka-consumer-groups.sh $B --group user-events-processor --topic user-events \
  --reset-offsets --to-earliest --execute     # or --to-latest | --to-offset N | --to-datetime 2026-02-01T00:00:00.000
bin/kafka-consumer-groups.sh $B --delete --group user-events-processor

# ACLs
bin/kafka-acls.sh $B --add --allow-principal User:alice --operation Read --topic user-events
bin/kafka-acls.sh $B --add --allow-principal User:alice --operation Read --group user-events-processor
bin/kafka-acls.sh $B --add --allow-principal User:admin --operation All --topic prod- --resource-pattern-type prefixed
bin/kafka-acls.sh $B --list --topic user-events
bin/kafka-acls.sh $B --remove --allow-principal User:alice --operation Read --topic user-events

# Cluster
bin/kafka-metadata-quorum.sh $B describe --status       # KRaft controller quorum health
bin/kafka-broker-api-versions.sh $B                     # reachable brokers
bin/kafka-configs.sh $B --describe --entity-type brokers --entity-name 1
```

**Confluent Cloud / Platform** equivalents live in the Confluent CLI (`confluent kafka topic …`,
`confluent kafka acl …`). **RBAC** (Confluent only):

```bash
confluent iam rbac role-binding create --principal User:alice --role DeveloperRead \
  --resource Topic:user-events --kafka-cluster <cluster-id>
confluent iam rbac role-binding list --principal User:alice --kafka-cluster <cluster-id>
```

Common roles: `SystemAdmin`, `ClusterAdmin`, `SecurityAdmin`, `UserAdmin`, `Operator`, `ResourceOwner`,
`DeveloperManage`, `DeveloperRead`, `DeveloperWrite`.

## Schema Registry (REST)

```bash
SR=$SCHEMA_REGISTRY_URL   # add -u "$SR_KEY:$SR_SECRET" for Confluent Cloud
curl -s -X POST -H 'Content-Type: application/vnd.schemaregistry.v1+json' \
  --data "{\"schemaType\":\"AVRO\",\"schema\":$(jq -Rs . < schemas/user.avsc)}" $SR/subjects/user-value/versions
curl -s $SR/subjects                                   # list subjects
curl -s $SR/subjects/user-value/versions/latest        # get
curl -s -X POST -H 'Content-Type: application/vnd.schemaregistry.v1+json' \
  --data "{\"schemaType\":\"AVRO\",\"schema\":$(jq -Rs . < schemas/user-v2.avsc)}" \
  $SR/compatibility/subjects/user-value/versions/latest   # compatibility check
curl -s -X PUT -H 'Content-Type: application/vnd.schemaregistry.v1+json' \
  --data '{"compatibility":"BACKWARD_TRANSITIVE"}' $SR/config/user-value
curl -s -X DELETE $SR/subjects/user-value/versions/1     # soft delete; add ?permanent=true after a soft delete for hard delete
```

`schemaType` is `AVRO` (default), `PROTOBUF` or `JSON`.

## Kafka Connect (REST)

```bash
C=$KAFKA_CONNECT_URL   # e.g. http://localhost:8083
curl -s $C/connectors
curl -s -X POST -H 'Content-Type: application/json' --data @connectors/postgres-source.json $C/connectors
curl -s $C/connectors/postgres-source/status
curl -s -X PUT -H 'Content-Type: application/json' --data @connectors/postgres-source-config.json $C/connectors/postgres-source/config
curl -s -X POST "$C/connectors/postgres-source/restart?includeTasks=true"
curl -s -X PUT $C/connectors/postgres-source/pause ; curl -s -X PUT $C/connectors/postgres-source/resume
curl -s -X DELETE $C/connectors/postgres-source
curl -s $C/connector-plugins
```

Example Debezium source (Debezium 2.x+ uses `topic.prefix`; credentials come from a config provider, not a literal):

```json
{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.port": "5432",
    "database.user": "${env:PG_USER}",
    "database.password": "${env:PG_PASSWORD}",
    "database.dbname": "mydb",
    "topic.prefix": "dbserver1",
    "table.include.list": "public.users,public.orders"
  }
}
```

(`${env:...}` requires `config.providers=env` with `EnvVarConfigProvider` on the Connect worker.)

## ksqlDB (REST or CLI)

```bash
curl -s -X POST $KSQLDB_URL/ksql -H 'Content-Type: application/vnd.ksql.v1+json' --data '{
  "ksql": "CREATE STREAM user_events (userId INT, action VARCHAR, ts BIGINT) WITH (KAFKA_TOPIC='\''user-events'\'', VALUE_FORMAT='\''JSON'\'', PARTITIONS=3);",
  "streamsProperties": {}
}'
# Push queries: POST /query-stream; list: "SHOW STREAMS;" / "SHOW TABLES;"; drop: "DROP STREAM user_events DELETE TOPIC;"
```

On Confluent Cloud, Flink SQL is the primary stream-processing option; ksqlDB remains for existing workloads.

## Producer and consumer essentials

- **Idempotence / EOS:** `enable.idempotence=true` (default in modern Java clients), `acks=all`; transactions
  (`transactional.id`) for atomic multi-topic writes; consumers use `isolation.level=read_committed`.
- **Compression:** `compression.type=zstd` or `lz4` for throughput; `snappy`/`gzip` also supported.
- **Batching:** tune `linger.ms` and `batch.size` together.
- **Keys drive partitioning** — same key, same partition, ordered. Don't change partition counts on keyed topics casually.
- **Parallelism** is bounded by partition count; scale consumers up to it, not past it.
- **Every external call gets timeout, retry (transient only), breaker, fallback and observability** — see
  `RULES.md → ## resilient-integration`. Dead-letter topics are the usual consumer fallback.

## Troubleshooting

| Symptom | Check |
|---|---|
| Cannot connect | `kafka-broker-api-versions.sh $B`; advertised listeners match what the client resolves; `openssl s_client -connect broker:9093` for TLS |
| SASL auth failed | mechanism matches the broker listener; credentials; Confluent Cloud key scoped to the right cluster |
| Topic not found | `kafka-topics.sh --list`; create explicitly — prefer `auto.create.topics.enable=false` in production |
| Consumer lag growing | `kafka-consumer-groups.sh --describe`; add consumers up to partition count; profile the handler; check rebalances |
| Schema rejected | compatibility check endpoint above; subject compatibility level |

## Resources

- [Apache Kafka documentation](https://kafka.apache.org/documentation/) · [KRaft operations](https://kafka.apache.org/documentation/#kraft)
- [Confluent documentation](https://docs.confluent.io/)
- [KafkaJS documentation](https://kafka.js.org/)
- [Schema Registry API](https://docs.confluent.io/platform/current/schema-registry/develop/api.html)
- [Kafka Connect REST API](https://docs.confluent.io/platform/current/connect/references/restapi.html)
- [ksqlDB documentation](https://docs.ksqldb.io/)
