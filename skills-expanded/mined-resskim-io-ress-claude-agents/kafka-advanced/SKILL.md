---
name: kafka-advanced
category: messaging
description: "Kafka 고급 Producer/Consumer 가이드 — Transactional API, Exactly-Once, KIP-848 리밸런싱, Offset 전략, Inbox 패턴 Use when working with messaging 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Kafka 고급 Producer/Consumer 가이드

Transactional API, Exactly-Once, KIP-848 리밸런싱, Offset 전략, Inbox 패턴

## Quick Reference (결정 트리)

```
메시지 전달 보장 수준?
    │
    ├─ At-Most-Once ────> auto.commit=true (메시지 유실 허용)
    │
    ├─ At-Least-Once ──> 수동 커밋 + Idempotent Consumer (표준)
    │
    └─ Exactly-Once ───> Transactional API (Kafka-to-Kafka)
            │            + Inbox 패턴 (Kafka-to-DB)
            │
            ├─ Kafka → Kafka ─> sendOffsetsToTransaction()
            └─ Kafka → DB ────> Inbox 테이블 (DB unique constraint)

Consumer 리밸런싱 전략?
    │
    ├─ Kafka 3.x ──> CooperativeStickyAssignor (점진적)
    └─ Kafka 4.x ──> KIP-848 Server-Side (차세대, 최소 지연)
```

---

## CRITICAL: Transactional API (Exactly-Once)

### 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│  Exactly-Once Semantics (EOS)                                │
│                                                              │
│  Idempotent Producer (단일 파티션 내 중복 방지)               │
│    └─ PID + Sequence Number → 브로커가 중복 감지             │
│                                                              │
│  Transactional Producer (다중 파티션/토픽 원자적 쓰기)        │
│    └─ transactional.id → 트랜잭션 코디네이터가 관리          │
│    └─ Consumer offset도 같은 트랜잭션에 포함 가능            │
│                                                              │
│  Transactional Consumer (커밋된 메시지만 읽기)               │
│    └─ isolation.level=read_committed                         │
└─────────────────────────────────────────────────────────────┘
```

### Producer Transactional API

```java
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG,
    "order-processor-" + instanceId);  // 인스턴스별 고유
// transactional.id 설정 시 idempotence 자동 활성화

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();  // 트랜잭션 초기화 (앱 시작 시 1회)

try {
    producer.beginTransaction();

    // 여러 토픽/파티션에 원자적 쓰기
    producer.send(new ProducerRecord<>("orders", orderId, orderJson));
    producer.send(new ProducerRecord<>("audit-log", orderId, auditJson));

    // Consumer offset도 같은 트랜잭션에 포함 (Kafka-to-Kafka EOS)
    producer.sendOffsetsToTransaction(
        currentOffsets, consumerGroupMetadata);

    producer.commitTransaction();
} catch (ProducerFencedException | OutOfOrderSequenceException e) {
    // 복구 불가 - 새 인스턴스가 같은 transactional.id로 시작됨
    producer.close();
} catch (KafkaException e) {
    // 복구 가능 - 트랜잭션 중단 후 재시도
    producer.abortTransaction();
}
```

### Consumer read_committed

```java
// Transactional Consumer 설정
props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
// → 커밋된 트랜잭션의 메시지만 읽음
// → abort된 트랜잭션의 메시지는 자동 필터링
// → 트랜잭션 진행 중인 메시지는 대기
```

### CRITICAL: transactional.id 설계

```
transactional.id는 인스턴스별 고유해야 함:
  - "order-processor-0", "order-processor-1", ...
  - 파티션 샤드 ID에서 파생 권장

같은 transactional.id로 새 Producer 시작 시:
  → 이전 Producer가 "fenced" (ProducerFencedException)
  → 진행 중 트랜잭션 자동 abort
  → 좀비 프로세스 방지 메커니즘

주의: transactional.id가 모든 인스턴스에서 같으면
     → 인스턴스 간 서로 fencing → 정상 동작 불가
```

### Spring Kafka 트랜잭션

```yaml
spring:
  kafka:
    producer:
      transaction-id-prefix: "order-tx-"  # 자동으로 suffix 추가
      acks: all
    consumer:
      isolation-level: read_committed
      enable-auto-commit: false
      properties:
        max.poll.records: 100
```

```java
@Service
@RequiredArgsConstructor
public class OrderProcessor {
    private final KafkaTemplate<String, String> kafkaTemplate;

    // @Transactional로 Kafka 트랜잭션 자동 관리
    @Transactional
    public void processOrder(String orderId, String orderJson) {
        kafkaTemplate.send("processed-orders", orderId, orderJson);
        kafkaTemplate.send("notifications", orderId, notificationJson);
        // 메서드 종료 시 자동 commit, 예외 시 자동 abort
    }

    // executeInTransaction으로 명시적 관리
    public void processWithExplicit(String orderId, String data) {
        kafkaTemplate.executeInTransaction(ops -> {
            ops.send("topic-a", orderId, data);
            ops.send("topic-b", orderId, data);
            return true;
        });
    }
}
```

---

## Offset 관리 전략

### 전략 비교

| 전략 | 방식 | 장점 | 단점 |
|------|------|------|------|
| **배치 커밋** | poll() 후 전체 커밋 | 단순, 성능 좋음 | 실패 시 배치 전체 재처리 |
| **레코드별 커밋** | 레코드마다 커밋 | 정밀한 복구 | 커밋 오버헤드 큼 |
| **비동기 + 동기 혼합** | 루프: async, shutdown: sync | 성능 + 안정성 | 구현 복잡 |
| **트랜잭션 커밋** | sendOffsetsToTransaction | Exactly-once | Kafka-to-Kafka만 |

### 비동기 + 동기 혼합 (Best Practice)

```java
try {
    while (running) {
        ConsumerRecords<String, String> records =
            consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);
        }
        // 일반 루프: 비동기 커밋 (높은 처리량)
        consumer.commitAsync((offsets, exception) -> {
            if (exception != null) {
                log.warn("Async commit failed: {}", offsets, exception);
            }
        });
    }
} finally {
    try {
        // Shutdown: 동기 커밋 (마지막 offset 보장)
        consumer.commitSync();
    } finally {
        consumer.close();
    }
}
```

### 특정 파티션 offset 커밋

```java
// 파티션별 정밀 offset 관리
Map<TopicPartition, OffsetAndMetadata> currentOffsets = new HashMap<>();
int count = 0;

for (ConsumerRecord<String, String> record : records) {
    processRecord(record);
    currentOffsets.put(
        new TopicPartition(record.topic(), record.partition()),
        new OffsetAndMetadata(record.offset() + 1)  // +1: 다음 읽을 위치
    );
    if (++count % 100 == 0) {
        consumer.commitAsync(currentOffsets, null);  // 100건마다 커밋
    }
}
```

---

## KIP-848: 차세대 Consumer 리밸런싱

### 기존 vs KIP-848

```
기존 (Client-Side Rebalance):
  Consumer 1  ──┐
  Consumer 2  ──┼─ JoinGroup ──> GroupCoordinator ──> SyncGroup ──> 할당
  Consumer 3  ──┘
  ※ 전체 Consumer가 참여해야 완료 (느린 Consumer가 병목)

KIP-848 (Server-Side Rebalance, Kafka 4.0):
  Consumer 1  ──> Heartbeat(구독 정보) ──> GroupCoordinator
  Consumer 2  ──> Heartbeat(구독 정보) ──>   (서버가 직접 할당)
  Consumer 3  ──> Heartbeat(구독 정보) ──>   (개별 통보)
  ※ 각 Consumer가 독립적으로 할당 수신 (최대 20배 빠름)
```

### 리밸런싱 전략 비교

| 전략 | 방식 | 리밸런싱 시간 | 적합 시나리오 |
|------|------|-------------|-------------|
| **Eager (Range/RoundRobin)** | 전체 해제 → 재할당 | 수십 초 | 레거시 |
| **CooperativeStickyAssignor** | 이동 파티션만 해제 | 수 초 | Kafka 2.4~3.x |
| **KIP-848 Server-Side** | 서버가 직접 관리 | 밀리초~초 | Kafka 4.0+ |

### CooperativeStickyAssignor 설정

```yaml
spring:
  kafka:
    consumer:
      properties:
        partition.assignment.strategy: >
          org.apache.kafka.clients.consumer.CooperativeStickyAssignor
        # Cooperative 모드에서는 리밸런싱 중에도
        # 이동하지 않는 파티션의 처리가 계속됨
```

### KIP-848 활성화 (Kafka 4.0+)

```yaml
# 브로커 설정
group.coordinator.rebalance.protocols=consumer,classic
# Consumer 설정
group.protocol=consumer  # 새 프로토콜 사용
```

---

## Inbox 패턴 (Idempotent Consumer 심화)

### DB 기반 Inbox

```sql
-- Inbox 테이블 (processed_messages)
CREATE TABLE inbox (
    message_id   UUID PRIMARY KEY,
    handler_type VARCHAR(255) NOT NULL,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(message_id, handler_type)
);

-- TTL 정리 (30일 이후 삭제)
CREATE INDEX idx_inbox_processed_at ON inbox(processed_at);
-- 스케줄러: DELETE FROM inbox WHERE processed_at < NOW() - INTERVAL '30 days'
```

### Outbox + Inbox 조합 (Gold Standard)

```
┌──────────────────────────────────────────────────────┐
│  End-to-End Exactly-Once (Application Level)          │
│                                                       │
│  Producer (Service A):                                │
│  ┌─────────────────────────────────────────────┐     │
│  │ @Transactional                               │     │
│  │   1. 비즈니스 로직 (orders 테이블)           │     │
│  │   2. Outbox 이벤트 저장 (outbox 테이블)      │     │
│  └─────────────────────────────────────────────┘     │
│              ↓ (Polling Relay / CDC)                  │
│          [Kafka Topic]                                │
│              ↓                                        │
│  Consumer (Service B):                                │
│  ┌─────────────────────────────────────────────┐     │
│  │ @Transactional                               │     │
│  │   1. Inbox 중복 체크 (inbox 테이블)          │     │
│  │   2. 비즈니스 로직 (shipments 테이블)        │     │
│  │   3. Inbox 처리 기록 (inbox 테이블)          │     │
│  └─────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────┘
```

```java
@Component
@RequiredArgsConstructor
public class ShipmentEventHandler {
    private final InboxRepository inboxRepo;
    private final ShipmentService shipmentService;

    @KafkaListener(topics = "order-events", groupId = "shipment-group")
    @Transactional
    public void handle(
            @Header("ce_id") String messageId,    // CloudEvents ID
            @Payload OrderCreatedEvent event) {

        // 1. Inbox 중복 체크
        if (inboxRepo.existsByMessageIdAndHandlerType(
                messageId, "ShipmentCreation")) {
            log.info("Duplicate ignored: {}", messageId);
            return;
        }

        // 2. 비즈니스 로직
        shipmentService.createShipment(event);

        // 3. Inbox 기록 (같은 DB 트랜잭션)
        inboxRepo.save(new InboxEntry(
            messageId, "ShipmentCreation", Instant.now()));
    }
}
```

---

## 고급 Producer 튜닝

### 처리량 vs 지연시간

| 설정 | 처리량 우선 | 지연시간 우선 | Kafka 4.0 기본값 |
|------|-----------|-------------|-----------------|
| `batch.size` | 65536~131072 | 16384 | 16384 |
| `linger.ms` | 50~100 | 0~5 | 5 |
| `compression.type` | zstd | lz4 | none |
| `buffer.memory` | 64~128MB | 32MB | 32MB |
| `max.in.flight.requests` | 5 | 5 | 5 |

### Custom Partitioner

```java
public class TenantPartitioner implements Partitioner {
    @Override
    public int partition(String topic, Object key, byte[] keyBytes,
                         Object value, byte[] valueBytes, Cluster cluster) {
        String tenantId = extractTenantId((String) key);
        int numPartitions = cluster.partitionCountForTopic(topic);
        // 같은 tenant → 같은 파티션 (순서 보장)
        return Math.abs(tenantId.hashCode()) % numPartitions;
    }
}

// 설정
props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG,
    TenantPartitioner.class.getName());
```

### CRITICAL: Kafka 4.0 주요 변경사항

```
1. linger.ms 기본값: 0 → 5 (배치 효율 향상)
2. KRaft 전용 (ZooKeeper 완전 제거)
3. KIP-848 Consumer 프로토콜 (서버 사이드 리밸런싱)
4. enable.idempotence 기본 true (3.0부터)
5. acks=all 기본 (3.0부터)
```

---

## 디버깅

```bash
# Consumer Group 상태 확인
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group order-group

# 트랜잭션 상태 확인
kafka-transactions.sh --bootstrap-server localhost:9092 \
  describe --transactional-id order-processor-0

# Hanging 트랜잭션 abort
kafka-transactions.sh --bootstrap-server localhost:9092 \
  abort --transactional-id order-processor-0

# Consumer Lag 확인
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group order-group --members --verbose

# Offset 리셋 (주의!)
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group order-group --topic orders --reset-offsets \
  --to-earliest --execute
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| transactional.id 공유 | 인스턴스 간 fencing | 인스턴스별 고유 ID |
| commitSync 과다 사용 | 처리량 저하 | async + shutdown sync 혼합 |
| auto.commit=true + EOS | 중복 처리 | 반드시 수동 커밋 |
| Inbox TTL 미설정 | 테이블 무한 증가 | 30일 TTL 정리 스케줄러 |
| Eager Assignor 유지 | 긴 리밸런싱 | CooperativeSticky 전환 |
| max.poll.records 과다 | 리밸런싱 트리거 | 처리시간 × records < poll.interval |

---

## 체크리스트

### Exactly-Once
- [ ] transactional.id 인스턴스별 고유 설정
- [ ] Consumer isolation.level=read_committed
- [ ] sendOffsetsToTransaction 사용 (Kafka-to-Kafka)
- [ ] Inbox 패턴 적용 (Kafka-to-DB)

### Consumer 튜닝
- [ ] CooperativeStickyAssignor 설정
- [ ] max.poll.records × 처리시간 < max.poll.interval.ms
- [ ] commitAsync + shutdown commitSync 패턴
- [ ] Graceful shutdown 구현

### Producer 튜닝
- [ ] acks=all, idempotence=true 확인
- [ ] batch.size/linger.ms 워크로드에 맞게 조정
- [ ] compression.type 설정 (zstd 권장)
- [ ] Custom Partitioner 검토 (순서 보장 필요 시)

**관련 skill**: `/kafka`, `/kafka-patterns`, `/msa-event-driven`, `/msa-cqrs-eventsourcing`
