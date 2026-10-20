---
name: kafka-msa-patterns
category: architecture
description: "Kafka MSA 실전 패턴 — MSA에서 Kafka를 올바르게 사용하기 위한 실전 패턴. Idempotency, DLQ, Retry, Outbox, Schema Evolution. Use when cross-service event 일관성 / 트레이드오프 cascade 분석이 필요할 때."
effort: max
deprecated: false
---

# Kafka MSA 실전 패턴

MSA에서 Kafka를 올바르게 사용하기 위한 실전 패턴. Idempotency, DLQ, Retry, Outbox, Schema Evolution 등.

## Quick Reference

```
메시지 처리 보장?
    │
    ├─ 중복 처리 방지 ────> Idempotent Consumer (deduplication table)
    ├─ 처리 실패 격리 ────> Dead Letter Queue (DLQ)
    ├─ 일시적 오류 대응 ──> Retry + Exponential Backoff
    ├─ DB-Kafka 원자성 ──> Transactional Outbox Pattern
    └─ Kafka 내부 보장 ──> Idempotent Producer + Transactions

이벤트 설계?
    │
    ├─ 표준 이벤트 구조 ──> Event Envelope (CloudEvents 호환)
    ├─ 스키마 변경 안전 ──> Protobuf + reserved 필드 + 호환성 테스트
    └─ 분산 트랜잭션 ────> Saga (3~4단계: Choreography, 5+: Orchestration)

운영?
    │
    ├─ 지연 감지 ─────────> Consumer Lag Monitoring (Prometheus)
    └─ 파티션 균형 ───────> Partition Key 카디널리티 + hot partition 방지
```

---

## 1. Idempotent Consumer

동일 메시지를 여러 번 수신해도 **한 번만 처리**하는 패턴. Kafka는 at-least-once가 기본이므로 application 레벨 중복 방지 필수.

### Deduplication Table

```sql
CREATE TABLE processed_events (
    event_id       UUID PRIMARY KEY,
    topic          VARCHAR(249) NOT NULL,
    consumer_group VARCHAR(100) NOT NULL,
    processed_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_processed_events_time ON processed_events (processed_at);
-- 30일 이후 TTL 정리
```

### Go 구현 (Sarama)

```go
func (c *IdempotentConsumer) ConsumeClaim(
    session sarama.ConsumerGroupSession,
    claim sarama.ConsumerGroupClaim,
) error {
    for msg := range claim.Messages() {
        var envelope kafka.EventEnvelope
        if err := json.Unmarshal(msg.Value, &envelope); err != nil {
            session.MarkMessage(msg, "") // 파싱 불가 → skip
            continue
        }

        // 비즈니스 로직 + 중복 기록을 같은 DB 트랜잭션으로
        tx, _ := c.db.BeginTx(ctx, nil)

        var exists bool
        tx.QueryRowContext(ctx,
            "SELECT EXISTS(SELECT 1 FROM processed_events WHERE event_id = $1)",
            envelope.EventID,
        ).Scan(&exists)

        if exists {
            tx.Rollback()
            session.MarkMessage(msg, "") // 이미 처리됨
            continue
        }

        if err := c.processEvent(ctx, tx, &envelope); err != nil {
            tx.Rollback()
            continue // retry 대기
        }

        tx.ExecContext(ctx,
            "INSERT INTO processed_events (event_id, topic, consumer_group) VALUES ($1, $2, $3)",
            envelope.EventID, msg.Topic, c.groupID,
        )
        tx.Commit()
        session.MarkMessage(msg, "")
    }
    return nil
}
```

### Anti-pattern

| 잘못된 방법 | 올바른 방법 |
|------------|-----------|
| offset만 믿고 중복 체크 안 함 | event_id 기반 deduplication |
| 메모리 map으로만 추적 | DB에 영구 기록 |
| 비즈니스 + dedup 별도 트랜잭션 | 같은 DB 트랜잭션으로 원자성 보장 |

---

## 2. Dead Letter Queue (DLQ)

반복 실패하는 메시지를 **격리**하여 Consumer 블록을 방지. 격리된 메시지는 나중에 재처리.

### Go 구현: Retry + DLQ

```go
const maxRetries = 3

func (h *DLQHandler) HandleWithRetry(
    ctx context.Context,
    msg *sarama.ConsumerMessage,
    process func(context.Context, *sarama.ConsumerMessage) error,
) error {
    retryCount := getRetryCount(msg) // x-retry-count 헤더에서 읽기

    if err := process(ctx, msg); err != nil {
        if isTransientError(err) && retryCount < maxRetries {
            return h.sendToRetry(ctx, msg, retryCount+1, err)
        }
        return h.sendToDLQ(ctx, msg, err, retryCount)
    }
    return nil
}

func (h *DLQHandler) sendToDLQ(
    ctx context.Context,
    original *sarama.ConsumerMessage,
    processErr error,
    retryCount int,
) error {
    dlqTopic := fmt.Sprintf("eodini.dlq.%s", original.Topic)

    _, _, err := h.producer.SendMessage(&sarama.ProducerMessage{
        Topic: dlqTopic,
        Key:   sarama.ByteEncoder(original.Key),
        Value: sarama.ByteEncoder(original.Value),
        Headers: []sarama.RecordHeader{
            {Key: []byte("x-original-topic"), Value: []byte(original.Topic)},
            {Key: []byte("x-error-message"), Value: []byte(processErr.Error())},
            {Key: []byte("x-retry-count"), Value: []byte(strconv.Itoa(retryCount))},
            {Key: []byte("x-failed-at"), Value: []byte(time.Now().Format(time.RFC3339))},
            {Key: []byte("x-consumer-group"), Value: []byte(h.consumerGroup)},
        },
    })
    return err
}

func getRetryCount(msg *sarama.ConsumerMessage) int {
    for _, h := range msg.Headers {
        if string(h.Key) == "x-retry-count" {
            count, _ := strconv.Atoi(string(h.Value))
            return count
        }
    }
    return 0
}
```

### Error 분류

```go
func isTransientError(err error) bool {
    // 재시도 가능한 일시적 오류
    var netErr net.Error
    if errors.As(err, &netErr) && netErr.Timeout() {
        return true
    }
    // DB 연결 실패, FCM 일시 장애 등
    return errors.Is(err, sql.ErrConnDone) ||
           errors.Is(err, context.DeadlineExceeded)
}
// permanent error (잘못된 데이터, 비즈니스 규칙 위반)는 즉시 DLQ
```

### DLQ 토픽 규칙

| 원본 토픽 | DLQ 토픽 | Retention |
|-----------|----------|-----------|
| `eodini.vehicle.boarding` | `eodini.dlq.eodini.vehicle.boarding` | 무제한 |
| `eodini.chat.events` | `eodini.dlq.eodini.chat.events` | 무제한 |

---

## 3. Retry with Exponential Backoff

일시적 오류 시 **점진적으로 대기 시간을 늘려** 재시도. 즉시 재시도는 장애를 악화시킴.

### Backoff 계산

```go
func calculateBackoff(retryCount int, baseDelay, maxDelay time.Duration) time.Duration {
    delay := baseDelay * time.Duration(1<<uint(retryCount)) // 2^retryCount
    if delay > maxDelay {
        delay = maxDelay
    }
    // jitter: 0~25% (thundering herd 방지)
    jitter := time.Duration(rand.Int63n(int64(delay) / 4))
    return delay + jitter
}

// 예: baseDelay=1s, maxDelay=30s
// retry 0: 1s + jitter
// retry 1: 2s + jitter
// retry 2: 4s + jitter
// retry 3: DLQ로 전송
```

### Retry Topic Consumer

```go
func (h *RetryConsumer) ConsumeClaim(
    session sarama.ConsumerGroupSession,
    claim sarama.ConsumerGroupClaim,
) error {
    for msg := range claim.Messages() {
        retryAt := getRetryAt(msg) // x-retry-at 헤더
        if time.Now().Before(retryAt) {
            time.Sleep(time.Until(retryAt))
        }

        retryCount := getRetryCount(msg)
        if err := h.process(ctx, msg); err != nil {
            if retryCount >= maxRetries {
                h.dlqHandler.sendToDLQ(ctx, msg, err, retryCount)
            } else {
                h.sendToRetry(ctx, msg, retryCount+1, err)
            }
        }
        session.MarkMessage(msg, "")
    }
    return nil
}
```

---

## 4. Transactional Outbox Pattern

DB 변경과 이벤트 발행을 **하나의 DB 트랜잭션으로 원자적 보장**. Dual-write 문제 해결.

### Outbox Table

```sql
CREATE TABLE outbox (
    id          BIGSERIAL PRIMARY KEY,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    kafka_topic VARCHAR(249) NOT NULL,
    kafka_key   VARCHAR(100) NOT NULL,
    kafka_value BYTEA NOT NULL,
    published   BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_outbox_unpublished ON outbox (id) WHERE published = FALSE;
```

### Go 구현: 비즈니스 로직 + Outbox 기록

```go
func (s *VehicleService) Board(ctx context.Context, cmd BoardCmd) error {
    tx, _ := s.db.BeginTx(ctx, nil)
    defer tx.Rollback()

    // 1. 비즈니스 데이터 저장
    event, err := s.boardingRepo.CreateEvent(ctx, tx, cmd)
    if err != nil {
        return err
    }

    // 2. 이벤트를 outbox에 기록 (같은 트랜잭션)
    envelope := kafka.NewEnvelope("boarding.boarded", event.VehicleID, payload)
    value, _ := json.Marshal(envelope)

    _, err = tx.ExecContext(ctx,
        "INSERT INTO outbox (kafka_topic, kafka_key, kafka_value) VALUES ($1, $2, $3)",
        "eodini.vehicle.boarding", event.VehicleID, value,
    )
    if err != nil {
        return err
    }

    return tx.Commit() // DB 저장 + 이벤트 기록이 원자적
}
```

### Go 구현: Outbox Publisher (Polling)

```go
func (p *OutboxPublisher) Run(ctx context.Context) error {
    ticker := time.NewTicker(100 * time.Millisecond)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return nil
        case <-ticker.C:
            p.publishBatch(ctx)
        }
    }
}

func (p *OutboxPublisher) publishBatch(ctx context.Context) error {
    tx, _ := p.db.BeginTx(ctx, nil)
    defer tx.Rollback()

    // FOR UPDATE SKIP LOCKED: 분산 환경 경합 방지
    rows, _ := tx.QueryContext(ctx, `
        SELECT id, kafka_topic, kafka_key, kafka_value
        FROM outbox WHERE published = FALSE
        ORDER BY id ASC LIMIT 100
        FOR UPDATE SKIP LOCKED
    `)
    defer rows.Close()

    var ids []int64
    for rows.Next() {
        var id int64
        var topic, key string
        var value []byte
        rows.Scan(&id, &topic, &key, &value)

        _, _, err := p.producer.SendMessage(&sarama.ProducerMessage{
            Topic: topic,
            Key:   sarama.StringEncoder(key),
            Value: sarama.ByteEncoder(value),
        })
        if err != nil {
            return err // 실패 시 트랜잭션 롤백 → 다음 batch에서 재시도
        }
        ids = append(ids, id)
    }

    if len(ids) > 0 {
        tx.ExecContext(ctx,
            "UPDATE outbox SET published = TRUE, published_at = NOW() WHERE id = ANY($1)",
            pq.Array(ids),
        )
    }
    return tx.Commit()
}
```

### 현재 eodini vs Outbox 비교

| 현재 (Direct Publish) | Outbox Pattern |
|----------------------|----------------|
| DB 저장 성공 + Kafka 실패 = 이벤트 유실 | DB 트랜잭션으로 원자성 보장 |
| Kafka 장애 시 요청 지연 | DB만 가용하면 요청 성공 |
| 발행 실패를 무시(best-effort) | 미발행 레코드 자동 재시도 |

---

## 5. Schema Evolution (Protobuf)

서비스 독립 배포 시 **이벤트 스키마 변경이 기존 consumer를 깨뜨리지 않아야** 함.

### Backward Compatibility 규칙

| 변경 | 안전? | 규칙 |
|------|-------|------|
| 새 optional 필드 추가 | YES | 기존 consumer는 무시 |
| 기존 필드 삭제 | 조건부 | `reserved` 필수 |
| 필드 번호 변경 | **NO** | 절대 금지 |
| 필드 타입 변경 | **NO** | 새 필드 번호로 추가 |

### Protobuf 진화 예시

```protobuf
// v1
message StudentBoarded {
  string vehicle_id = 1;
  string student_id = 2;
  string student_name = 3;
  int64 boarded_at = 9;
}

// v2: 필드 추가 (backward compatible)
message StudentBoarded {
  string vehicle_id = 1;
  string student_id = 2;
  string student_name = 3;
  int64 boarded_at = 9;
  string boarding_method = 10;  // Phase 2: "manual", "qr", "nfc"
  double boarding_lat = 11;     // 탑승 위치
}

// v3: 필드 삭제 (reserved 사용)
message StudentBoarded {
  string vehicle_id = 1;
  string student_id = 2;
  reserved 3;                   // student_name 제거 (PII)
  reserved "student_name";
  int64 boarded_at = 9;
  string boarding_method = 10;
}
```

### 호환성 테스트

```go
func TestV1MessageReadableByV2(t *testing.T) {
    v1 := &pb_v1.StudentBoarded{VehicleId: "v1", StudentId: "s1"}
    data, _ := proto.Marshal(v1)

    v2 := &pb_v2.StudentBoarded{}
    err := proto.Unmarshal(data, v2)

    assert.NoError(t, err)
    assert.Equal(t, "v1", v2.VehicleId)
    assert.Equal(t, "", v2.BoardingMethod) // 새 필드: zero value
}
```

---

## 6. Partition Key 전략

동일 Key = 동일 파티션 = **순서 보장**. 잘못된 Key는 hot partition을 유발.

### eodini 토픽별 Key 분석

| 토픽 | Key | 순서 보장 단위 | 주의 |
|------|-----|---------------|------|
| `eodini.vehicle.boarding` | `vehicle_id` | 차량별 탑승 순서 | OK (차량 수 >> 파티션 수) |
| `eodini.tracking.location` | `vehicle_id` | 차량별 GPS 순서 | 10초 간격 → 편중 가능 |
| `eodini.chat.events` | `room_id` | 채팅방별 메시지 순서 | OK |
| `eodini.user.events` | `user_id` | 사용자별 이벤트 순서 | OK (높은 카디널리티) |

### Key 선택 의사결정

```
순서 보장 필요?
  ├─ NO  → null key (round-robin 최대 분산)
  └─ YES → Key 카디널리티 > 파티션 수 × 10?
           ├─ YES → 그대로 사용
           └─ NO  → composite key (vehicle_id + route_id)
```

---

## 7. Consumer Lag Monitoring

Consumer Lag = `Latest Offset - Committed Offset`. **가장 중요한 Kafka 건강 지표**.

### Prometheus 메트릭

```go
var (
    kafkaConsumerLag = promauto.NewGaugeVec(prometheus.GaugeOpts{
        Name: "kafka_consumer_group_lag",
        Help: "Consumer lag by topic and partition",
    }, []string{"consumer_group", "topic", "partition"})

    kafkaMessagesProcessed = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "kafka_messages_processed_total",
        Help: "Processed messages count",
    }, []string{"consumer_group", "topic", "status"}) // success, error, dlq

    kafkaProcessingDuration = promauto.NewHistogramVec(prometheus.HistogramOpts{
        Name:    "kafka_message_processing_duration_seconds",
        Buckets: prometheus.DefBuckets,
    }, []string{"consumer_group", "topic"})
)

// ConsumeClaim 내부에서 업데이트
lag := claim.HighWaterMarkOffset() - msg.Offset
kafkaConsumerLag.WithLabelValues(group, msg.Topic, partition).Set(float64(lag))
```

### Grafana 알림 규칙

```yaml
- alert: KafkaConsumerLagHigh
  expr: kafka_consumer_group_lag > 10000
  for: 5m
  labels: { severity: warning }

- alert: KafkaConsumerLagIncreasing
  expr: deriv(kafka_consumer_group_lag[5m]) > 100
  for: 10m
  labels: { severity: warning }

- alert: KafkaDLQAccumulation
  expr: kafka_dlq_messages_total > 100
  for: 5m
  labels: { severity: critical }
```

---

## 8. Idempotent Producer + Transactions

### Producer 설정

```go
config := sarama.NewConfig()
config.Producer.Idempotent = true           // PID + Sequence로 중복 방지
config.Producer.RequiredAcks = sarama.WaitForAll
config.Producer.Return.Successes = true
config.Net.MaxOpenRequests = 1              // 순서 보장

// Transactional Producer (Consume-Transform-Produce)
config.Producer.Transaction.ID = "notification-service-0"
config.Producer.Transaction.Retry.Max = 3
```

### Exactly-Once 범위

| 범위 | 보장 | 방법 |
|------|------|------|
| 단일 파티션 중복 방지 | YES | Idempotent Producer |
| 멀티 파티션 원자 쓰기 | YES | Transactional Producer |
| Kafka→Kafka EOS | YES | Consume-Transform-Produce + Txn |
| Kafka→DB EOS | **NO** | Idempotent Consumer 필요 |

---

## 9. Saga Pattern (Choreography)

eodini의 탑승 → 알림 → 채팅 흐름은 Choreography 방식 적합 (3~4단계).

### 이벤트 흐름

```
Vehicle Service
    Board()
    ├── Save DB
    └── Publish "StudentBoarded"
            │
            ├──► Notification Service
            │    ├── FindParent → Save Notification → FCM Push
            │    └── Publish "NotificationSent" (선택)
            │
            └──► Chat Service
                 ├── FindRoom → Save SystemMessage → SSE Broadcast
                 └── (끝)

보상 (탑승 취소 시):
Vehicle Service
    CancelBoarding()
    ├── Update DB
    └── Publish "BoardingCancelled"
            │
            ├──► Notification → "탑승 취소" 알림
            └──► Chat → "탑승 취소" 시스템 메시지
```

### 5단계 이상 (Phase 2 결제)이면 Orchestration 고려

```go
type SagaStep struct {
    Name       string
    Execute    func(ctx context.Context) error
    Compensate func(ctx context.Context) error
}

// 실패 시 역순으로 보상 트랜잭션 실행
```

---

## eodini 프로젝트 적용 우선순위

| 우선순위 | 패턴 | 이유 |
|---------|------|------|
| **P0** | Idempotent Consumer | 탑승 알림 중복 방지 (학부모 신뢰) |
| **P0** | DLQ | 실패 메시지 무한루프 방지 |
| **P0** | Retry + Backoff | FCM/gRPC transient error 대응 |
| **P1** | Transactional Outbox | Vehicle Service의 DB-Kafka 원자성 |
| **P1** | Consumer Lag Monitoring | LGTM Stack 통합 |
| **P2** | Schema Evolution | Phase 2/3 스키마 변경 시 |
| **P2** | Partition Key 최적화 | 차량 수 증가 시 |
| **P3** | Saga (보상 트랜잭션) | Phase 2 결제 기능 |

---

## 체크리스트

### Producer
- [ ] `acks=all`, `Idempotent=true`
- [ ] AggregateID를 Partition Key로 사용
- [ ] Transactional Outbox 또는 best-effort publish

### Consumer
- [ ] event_id 기반 deduplication (processed_events table)
- [ ] 비즈니스 로직 + dedup을 같은 DB 트랜잭션으로
- [ ] maxRetries 초과 시 DLQ 전송
- [ ] transient vs permanent error 분류

### DLQ
- [ ] `eodini.dlq.{원본_topic}` 네이밍
- [ ] 원본 이벤트 + 에러 메타데이터 포함
- [ ] DLQ 크기 모니터링 + 알림
- [ ] DLQ 재처리 워커

### Monitoring
- [ ] `kafka_consumer_group_lag` Gauge
- [ ] `kafka_messages_processed_total` Counter (success/error/dlq)
- [ ] `kafka_message_processing_duration_seconds` Histogram
- [ ] Grafana 대시보드 + 알림 규칙

### Schema
- [ ] Protobuf 필드 번호 변경/재사용 금지
- [ ] 삭제된 필드는 `reserved` 사용
- [ ] v1↔v2 호환성 테스트 작성
