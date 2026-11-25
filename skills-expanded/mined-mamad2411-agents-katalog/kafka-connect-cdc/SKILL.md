---
name: kafka-connect-cdc
category: messaging
description: "Kafka Connect & CDC (Debezium) 가이드 — Source/Sink Connector, Debezium CDC, Outbox Event Router, Schema Registry 심화, Strimzi 운영 Use when working with messaging 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Kafka Connect & CDC (Debezium) 가이드

Source/Sink Connector, Debezium CDC, Outbox Event Router, Schema Registry 심화, Strimzi 운영

## Quick Reference (결정 트리)

```
데이터 통합 방식?
    │
    ├─ DB → Kafka ──────────> Source Connector
    │       │
    │       ├─ Outbox 패턴 ──> Debezium + EventRouter SMT
    │       ├─ 전체 테이블 ──> Debezium (WAL/Binlog CDC)
    │       └─ JDBC 폴링 ───> JDBC Source Connector (비권장)
    │
    ├─ Kafka → DB/ES/S3 ──> Sink Connector
    │       │
    │       ├─ RDBMS ────────> JDBC Sink Connector
    │       ├─ Elasticsearch ─> ES Sink Connector
    │       └─ S3/GCS ───────> S3 Sink Connector
    │
    └─ 스키마 관리 ──────────> Schema Registry
            │
            ├─ Kafka 내부 ───> Avro + BACKWARD (기본)
            ├─ gRPC 연동 ───> Protobuf + BACKWARD_TRANSITIVE
            └─ 외부 API ────> JSON Schema + FULL
```

---

## CRITICAL: Kafka Connect 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│  Kafka Connect Cluster                                       │
│                                                              │
│  ┌──────────────────┐    ┌──────────────────┐              │
│  │  Worker 1         │    │  Worker 2         │              │
│  │  ┌─────────────┐ │    │  ┌─────────────┐ │              │
│  │  │ Task 0 (src)│ │    │  │ Task 1 (src)│ │              │
│  │  └──────┬──────┘ │    │  └──────┬──────┘ │              │
│  │         │        │    │         │        │              │
│  │  ┌─────────────┐ │    │  ┌─────────────┐ │              │
│  │  │ Task 0 (snk)│ │    │  │ Task 1 (snk)│ │              │
│  │  └──────┬──────┘ │    │  └──────┬──────┘ │              │
│  └─────────┼────────┘    └─────────┼────────┘              │
│            │                       │                         │
│            ▼                       ▼                         │
│  ┌──────────────────────────────────────────┐               │
│  │            Kafka Cluster                  │               │
│  │  ┌─────────┐ ┌──────────┐ ┌───────────┐ │               │
│  │  │ offsets │ │ config   │ │ status    │ │               │
│  │  │ topic   │ │ topic    │ │ topic     │ │               │
│  │  └─────────┘ └──────────┘ └───────────┘ │               │
│  └──────────────────────────────────────────┘               │
│                                                              │
│  Connector = 논리적 작업 정의 (DB → Kafka)                   │
│  Task = 실제 데이터 복사 단위 (병렬화)                       │
│  Worker = Task를 실행하는 JVM 프로세스                       │
│  SMT = Single Message Transform (메시지 변환)                │
└─────────────────────────────────────────────────────────────┘
```

---

## Debezium CDC Source Connector

### PostgreSQL Outbox Connector (권장)

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnector
metadata:
  name: pg-outbox-connector
  labels:
    strimzi.io/cluster: kafka-connect
spec:
  class: io.debezium.connector.postgresql.PostgresConnector
  tasksMax: 1
  config:
    # DB 연결
    database.hostname: postgres
    database.port: "5432"
    database.user: debezium
    database.password: "${secrets:db-cred:password}"
    database.dbname: orderdb
    topic.prefix: cdc

    # WAL 설정
    plugin.name: pgoutput           # PostgreSQL 10+ 기본
    slot.name: debezium_outbox
    publication.name: outbox_pub

    # Outbox 전용 테이블만 캡처
    table.include.list: public.outbox_events

    # Outbox Event Router SMT
    transforms: outbox
    transforms.outbox.type: io.debezium.transforms.outbox.EventRouter
    transforms.outbox.table.field.event.id: id
    transforms.outbox.table.field.event.key: aggregate_id
    transforms.outbox.table.field.event.type: event_type
    transforms.outbox.table.field.event.payload: payload
    transforms.outbox.table.fields.additional.placement: "version:header"
    transforms.outbox.route.topic.replacement: "${routedByValue}.events"
    # aggregate_type 값이 토픽명 → Order → order.events

    # Outbox 테이블 자동 정리 (DELETE 전파)
    transforms.outbox.table.expand.json.payload: true

    # 스키마 히스토리
    schema.history.internal.kafka.topic: schema-changes
    schema.history.internal.kafka.bootstrap.servers: kafka:9092

    # Heartbeat (WAL 슬롯 유지)
    heartbeat.interval.ms: 10000

    # 에러 처리
    errors.tolerance: none          # all = 에러 무시 (비권장)
    errors.deadletterqueue.topic.name: dlq.cdc
    errors.deadletterqueue.context.headers.enable: true
```

### Outbox 테이블 스키마

```sql
CREATE TABLE outbox_events (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(255) NOT NULL,   -- 예: "Order"
    aggregate_id   VARCHAR(255) NOT NULL,   -- 예: 주문 ID
    event_type     VARCHAR(255) NOT NULL,   -- 예: "OrderCreated"
    payload        JSONB NOT NULL,          -- 이벤트 데이터
    version        INT DEFAULT 1,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

-- PostgreSQL Publication (pgoutput 플러그인용)
CREATE PUBLICATION outbox_pub FOR TABLE outbox_events;
```

### MySQL CDC Connector

```yaml
spec:
  class: io.debezium.connector.mysql.MySqlConnector
  config:
    database.hostname: mysql
    database.port: "3306"
    database.user: debezium
    database.password: "${secrets:db-cred:password}"
    database.server.id: "1"         # MySQL 서버 ID (고유)
    database.include.list: orderdb
    table.include.list: orderdb.outbox_events
    # Binlog 설정
    include.schema.changes: false
    # 나머지 SMT 설정 동일
```

---

## Sink Connector

### Elasticsearch Sink (CQRS Read Model)

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnector
metadata:
  name: es-order-sink
  labels:
    strimzi.io/cluster: kafka-connect
spec:
  class: io.confluent.connect.elasticsearch.ElasticsearchSinkConnector
  tasksMax: 3
  config:
    connection.url: http://elasticsearch:9200
    topics: order.events
    key.ignore: false
    schema.ignore: true
    behavior.on.null.values: delete     # tombstone → ES 문서 삭제

    # Debezium 이벤트에서 payload 추출
    transforms: unwrap
    transforms.unwrap.type: >
      io.debezium.transforms.ExtractNewRecordState
    transforms.unwrap.drop.tombstones: true

    # 배치 설정
    batch.size: 200
    max.buffered.records: 500
    flush.timeout.ms: 10000
```

### JDBC Sink (DB 동기화)

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnector
metadata:
  name: jdbc-order-sink
spec:
  class: io.confluent.connect.jdbc.JdbcSinkConnector
  tasksMax: 2
  config:
    connection.url: "jdbc:postgresql://read-db:5432/orderdb"
    connection.user: writer
    connection.password: "${secrets:db-cred:password}"
    topics: order.events

    # Upsert 모드 (INSERT or UPDATE)
    insert.mode: upsert
    pk.mode: record_key
    pk.fields: id

    # 테이블 자동 생성
    auto.create: true
    auto.evolve: true           # 스키마 변경 시 ALTER TABLE
```

### S3 Sink (Data Lake)

```yaml
spec:
  class: io.confluent.connect.s3.S3SinkConnector
  config:
    s3.bucket.name: data-lake-bucket
    s3.region: ap-northeast-2
    topics.dir: raw/kafka
    flush.size: 1000            # 1000 레코드마다 파일 생성
    rotate.interval.ms: 600000  # 10분마다 파일 로테이션
    format.class: io.confluent.connect.s3.format.parquet.ParquetFormat
    storage.class: io.confluent.connect.s3.storage.S3Storage
    partitioner.class: >
      io.confluent.connect.storage.partitioner.TimeBasedPartitioner
    path.format: "'year'=YYYY/'month'=MM/'day'=dd/'hour'=HH"
    locale: ko_KR
    timezone: Asia/Seoul
```

---

## Schema Registry 심화

### 호환성 모드

| 모드 | 허용 변경 | Consumer/Producer 배포 순서 |
|------|----------|---------------------------|
| **BACKWARD** (기본) | 필드 삭제, default 필드 추가 | Consumer 먼저 |
| **FORWARD** | 필드 추가, default 필드 삭제 | Producer 먼저 |
| **FULL** | default 필드 추가/삭제만 | 순서 무관 (가장 안전) |
| **BACKWARD_TRANSITIVE** | 모든 이전 버전과 BACKWARD | Protobuf 권장 |
| **NONE** | 모든 변경 허용 | 개발 환경만 |

### 토픽별 호환성 설정

```bash
# 전역 기본값 설정
curl -X PUT http://schema-registry:8081/config \
  -H "Content-Type: application/json" \
  -d '{"compatibility": "FULL"}'

# 토픽별 오버라이드
curl -X PUT http://schema-registry:8081/config/orders-value \
  -H "Content-Type: application/json" \
  -d '{"compatibility": "BACKWARD_TRANSITIVE"}'

# 호환성 검증 (CI/CD에서 사용)
curl -X POST http://schema-registry:8081/compatibility/subjects/orders-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{...}"}'
```

### Avro 스키마 진화 규칙

```
FULL 호환 규칙:
  ✅ default 값이 있는 필드 추가
  ✅ default 값이 있는 필드 삭제
  ❌ 필드 타입 변경 (int → long은 promotion 허용)
  ❌ 필드명 변경 (aliases로 우회)
  ❌ required 필드 추가

Protobuf 규칙:
  ✅ 새 tag 번호로 필드 추가
  ✅ reserved로 필드 삭제
  ❌ tag 번호 재사용 (절대 금지)
  ❌ 기존 필드를 oneof로 이동
```

### CI/CD 스키마 검증

```yaml
# GitHub Actions - 스키마 호환성 체크
- name: Schema Compatibility Check
  run: |
    for schema_file in schemas/*.avsc; do
      subject=$(basename "$schema_file" .avsc)-value
      result=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "http://schema-registry:8081/compatibility/subjects/$subject/versions/latest" \
        -H "Content-Type: application/vnd.schemaregistry.v1+json" \
        -d "{\"schema\": $(cat "$schema_file" | jq -Rs .)}")
      if [ "$result" != "200" ]; then
        echo "INCOMPATIBLE: $subject"
        exit 1
      fi
    done
```

---

## Strimzi Kafka Connect on K8s

### KafkaConnect 리소스

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnect
metadata:
  name: kafka-connect
  annotations:
    strimzi.io/use-connector-resources: "true"  # KafkaConnector CRD 활성화
spec:
  version: 3.7.0
  replicas: 3
  bootstrapServers: kafka-cluster:9092
  config:
    group.id: connect-cluster
    offset.storage.topic: connect-offsets
    config.storage.topic: connect-configs
    status.storage.topic: connect-status
    offset.storage.replication.factor: 3
    config.storage.replication.factor: 3
    status.storage.replication.factor: 3
    key.converter: org.apache.kafka.connect.json.JsonConverter
    value.converter: org.apache.kafka.connect.json.JsonConverter
    key.converter.schemas.enable: false
    value.converter.schemas.enable: false
  resources:
    requests: { cpu: 500m, memory: 1Gi }
    limits: { cpu: 2, memory: 4Gi }
  build:
    # 커넥터 플러그인 빌드 (Strimzi가 이미지 자동 생성)
    output:
      type: docker
      image: registry.example.com/kafka-connect:latest
    plugins:
    - name: debezium-postgres
      artifacts:
      - type: maven
        group: io.debezium
        artifact: debezium-connector-postgres
        version: 2.5.0.Final
    - name: confluent-elasticsearch
      artifacts:
      - type: maven
        group: io.confluent
        artifact: kafka-connect-elasticsearch
        version: 14.1.0
```

---

## Log Compaction (상태 토픽)

### 설정

```bash
# Compacted Topic 생성
kafka-topics.sh --create \
  --topic user-profiles \
  --partitions 12 \
  --replication-factor 3 \
  --config cleanup.policy=compact \
  --config min.compaction.lag.ms=3600000 \
  --config delete.retention.ms=86400000 \
  --config segment.bytes=268435456 \
  --config min.cleanable.dirty.ratio=0.5
```

### 사용 시나리오

| 토픽 유형 | cleanup.policy | 용도 |
|----------|---------------|------|
| 이벤트 로그 | `delete` | 주문 이벤트, 로그 |
| 상태 저장 | `compact` | 사용자 프로필, 설정 |
| 이벤트 + 상태 | `compact,delete` | Kafka Streams changelog |
| Event Store | `delete` + retention=-1 | CQRS Event Sourcing |

### CRITICAL: Compaction 동작

```
Compaction 전:
  key=A → v1, key=B → v1, key=A → v2, key=B → v2, key=A → v3

Compaction 후:
  key=B → v2, key=A → v3  (각 key의 최신 값만 유지)

Tombstone (삭제):
  key=A → null  → compaction 후 delete.retention.ms 이후 제거

주의: min.compaction.lag.ms 이내의 메시지는 compaction 대상 아님
     → Consumer가 최신 메시지를 놓치지 않도록 보호
```

---

## 디버깅

```bash
# Connector 상태 확인
kubectl get kafkaconnector -n kafka

# Connector 상세 상태
kubectl describe kafkaconnector pg-outbox-connector -n kafka

# Connect REST API
curl http://kafka-connect:8083/connectors
curl http://kafka-connect:8083/connectors/pg-outbox-connector/status

# Connector 재시작
curl -X POST http://kafka-connect:8083/connectors/pg-outbox-connector/restart

# Task 재시작
curl -X POST http://kafka-connect:8083/connectors/pg-outbox-connector/tasks/0/restart

# WAL 슬롯 상태 확인 (PostgreSQL)
SELECT * FROM pg_replication_slots WHERE slot_name = 'debezium_outbox';

# WAL 크기 확인
SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)
FROM pg_replication_slots WHERE slot_name = 'debezium_outbox';
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| JDBC 폴링으로 CDC | 높은 DB 부하, 지연 | Debezium WAL/Binlog 사용 |
| tasksMax 과다 | 커넥터 리소스 낭비 | Source: 1, Sink: 파티션 수 |
| WAL 슬롯 미관리 | 디스크 가득 참 | heartbeat + 모니터링 |
| Schema 호환성 NONE | 프로덕션 장애 | FULL 또는 BACKWARD |
| errors.tolerance=all | 에러 무시 | none + DLQ 설정 |
| Compaction 미이해 | 데이터 유실 착각 | 최신 상태만 유지됨을 이해 |

---

## 체크리스트

### Debezium CDC
- [ ] WAL/Binlog 활성화 확인
- [ ] Replication Slot 모니터링
- [ ] Outbox Event Router SMT 설정
- [ ] heartbeat.interval.ms 설정
- [ ] DLQ 토픽 설정 (errors.deadletterqueue)

### Sink Connector
- [ ] Upsert 모드 설정 (insert.mode)
- [ ] 배치 크기 최적화 (batch.size)
- [ ] 에러 처리 전략 설정
- [ ] 스키마 진화 대응 (auto.evolve)

### Schema Registry
- [ ] 프로덕션: FULL 또는 BACKWARD 호환성
- [ ] CI/CD 스키마 호환성 검증
- [ ] 토픽별 호환성 오버라이드 검토
- [ ] Avro/Protobuf 규칙 팀 공유

### Strimzi Connect
- [ ] KafkaConnect CRD 배포
- [ ] 커넥터 플러그인 빌드 설정
- [ ] replicas >= 2 (HA)
- [ ] 리소스 requests/limits 설정

**관련 skill**: `/kafka`, `/kafka-patterns`, `/kafka-advanced`, `/msa-event-driven`, `/msa-cqrs-eventsourcing`
