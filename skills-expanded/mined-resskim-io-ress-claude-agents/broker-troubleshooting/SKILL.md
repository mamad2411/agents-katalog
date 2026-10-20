---
name: broker-troubleshooting
category: messaging
description: "메시지 브로커 장애 진단 — Kafka consumer lag·partition rebalancing·ISR shrink, RabbitMQ queue depth·unacked 누적·quorum leader election·memory alarm, NATS JetStream slow consumer. 증상별 진단 명령과 대응. Use when consumer lag 이 쌓이거나 queue 가 밀리거나 rebalance 가 반복될 때."
effort: xhigh
deprecated: false
---

# 메시지 브로커 트러블슈팅

증상 → 진단 명령 → 대응. 브로커별 구현 패턴은 [`kafka-patterns`](../kafka-patterns/SKILL.md) / [`rabbitmq`](../rabbitmq/SKILL.md) / [`nats-messaging`](../nats-messaging/SKILL.md),
DLQ·Outbox·Idempotent Consumer 같은 설계 패턴은 [`msa-event-driven`](../msa-event-driven/SKILL.md) / [`msa-resilience`](../msa-resilience/SKILL.md) 참조.

## Broker Comparison Matrix

| 기준 | Kafka | RabbitMQ | NATS JetStream | Redis Streams |
|------|-------|----------|----------------|--------------|
| 처리량 | ~2M msg/s | ~50K msg/s | ~500K msg/s | ~1M msg/s |
| 지연 시간 | 2~10ms | 1~5ms | <1ms | <1ms |
| 메시지 순서 | 파티션 내 보장 | 큐 내 보장 | Stream 내 보장 | Stream 내 보장 |
| 내구성 | 디스크 (복제) | 디스크 (미러링) | 디스크 (R=3) | AOF/RDB |
| 프로토콜 | Binary (TCP) | AMQP 0.9.1 | NATS Protocol | RESP |
| Consumer 모델 | Pull (Long poll) | Push + Pull | Push + Pull | Pull (XREAD) |
| 재처리 | Offset reset | Nack + Requeue | AckPolicy | XPENDING |
| K8s Operator | Strimzi | RabbitMQ Operator | NATS Operator | Redis Operator |
| 적합 용도 | 이벤트 스트리밍, 로그 | 작업 큐, RPC | IoT, 경량 메시징 | 캐시+스트림 통합 |

### 선택 기준

```
어떤 메시지 브로커를 선택할까?
    │
    ├─ 대용량 이벤트 스트리밍 ──> Kafka
    │  (로그 수집, CDC, 이벤트 소싱)
    │
    ├─ 작업 큐 + 복잡한 라우팅 ──> RabbitMQ
    │  (비동기 작업, 이메일 발송, 백그라운드 처리)
    │
    ├─ 초저지연 + 경량 ──────────> NATS
    │  (IoT, 마이크로서비스 내부 통신, Request-Reply)
    │
    └─ 이미 Redis 사용 중 ───────> Redis Streams
       (간단한 이벤트 파이프라인, 실시간 피드)
```

---

## Kafka Troubleshooting

### Consumer Lag 진단

```bash
# Consumer group lag 확인
kubectl exec -n kafka deploy/kafka-client -- \
  kafka-consumer-groups.sh --bootstrap-server kafka-cluster-kafka-bootstrap:9092 \
  --describe --group order-consumer-group

# 출력 해석:
# TOPIC     PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
# orders    0          1000            1500            500  ← LAG 확인
# orders    1          2000            2000            0    ← 정상

# Consumer group 상태 (Stable/Rebalancing/Dead)
kubectl exec -n kafka deploy/kafka-client -- \
  kafka-consumer-groups.sh --bootstrap-server kafka-cluster-kafka-bootstrap:9092 \
  --describe --group order-consumer-group --state

# 파티션별 메시지 유입 속도 (Offset 증가율)
kubectl exec -n kafka deploy/kafka-client -- \
  kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list kafka-cluster-kafka-bootstrap:9092 \
  --topic orders --time -1
```

**Lag 원인 분석 트리:**
```
Consumer Lag 증가?
    │
    ├─ Consumer 처리 속도 저하
    │   ├─ 하류 서비스 응답 시간 증가 (DB, API)
    │   ├─ Consumer CPU/Memory 부족
    │   └─ 직렬화/역직렬화 병목
    │
    ├─ Consumer 수 부족
    │   ├─ 파티션 수 > Consumer 수 → 스케일 아웃
    │   └─ Consumer 수 > 파티션 수 → 유휴 Consumer 발생
    │
    └─ Producer 유입량 급증
        ├─ 배치 작업/마이그레이션
        └─ 트래픽 급증 (이벤트, 캠페인)
```

### Partition Rebalancing 문제

```bash
# Consumer 재시작 빈도 확인
kubectl get events -n production --field-selector reason=Killing | \
  grep consumer | tail -10

# Consumer 설정 확인 (Strimzi KafkaConnect/App 로그)
kubectl logs -n production deploy/order-consumer --tail=50 | \
  grep -i "rebalance\|revoked\|assigned"
```

**Rebalancing 빈번 발생 시 점검:**

| 설정 | 기본값 | 권장값 | 설명 |
|------|-------|-------|------|
| `session.timeout.ms` | 45000 | 30000~60000 | heartbeat 실패 감지 시간 |
| `heartbeat.interval.ms` | 3000 | session.timeout의 1/3 | heartbeat 전송 간격 |
| `max.poll.interval.ms` | 300000 | 처리 시간의 2~3배 | poll 간 최대 허용 시간 |
| `max.poll.records` | 500 | 처리 능력에 맞게 조정 | poll당 최대 레코드 수 |

### ISR (In-Sync Replica) Shrink

```bash
# ISR 상태 확인
kubectl exec -n kafka deploy/kafka-client -- \
  kafka-topics.sh --bootstrap-server kafka-cluster-kafka-bootstrap:9092 \
  --describe --under-replicated-partitions

# Broker 상태 확인
kubectl exec -n kafka deploy/kafka-client -- \
  kafka-broker-api-versions.sh --bootstrap-server kafka-cluster-kafka-bootstrap:9092

# Strimzi Kafka 리소스 상태
kubectl get kafka -n kafka -o jsonpath='{.items[0].status.conditions}'
```

### Strimzi / K8s 디버깅

```bash
# Strimzi Operator 로그
kubectl logs -n kafka deploy/strimzi-cluster-operator --tail=100 | \
  grep -i "error\|warn\|reconcil"

# Kafka Pod 상태
kubectl get pods -n kafka -l strimzi.io/kind=Kafka -o wide

# PVC 사용량 (디스크 부족 확인)
kubectl exec -n kafka kafka-cluster-kafka-0 -- df -h /var/lib/kafka/data
```

---

## RabbitMQ Troubleshooting

### Queue Depth 급증

```bash
# RabbitMQ 큐 상태 조회
kubectl exec -n rabbitmq deploy/rabbitmq -- \
  rabbitmqctl list_queues name messages consumers message_bytes

# 특정 큐 상세 정보
kubectl exec -n rabbitmq deploy/rabbitmq -- \
  rabbitmqctl list_queues name messages_ready messages_unacknowledged \
  consumers memory --formatter json

# 큐별 메시지 유입/유출 속도 (Management API)
kubectl exec -n rabbitmq deploy/rabbitmq -- \
  rabbitmqadmin list queues name messages message_stats.publish_details.rate \
  message_stats.deliver_get_details.rate
```

### Unacked Messages 증가

```
원인:
  - Consumer가 메시지를 받았지만 ack하지 않음
  - Consumer 처리 시간 > Consumer timeout
  - Consumer 코드에서 ack 누락 (버그)

조사:
  1. Consumer 프로세스 상태 확인
  2. Consumer 처리 시간 메트릭 확인
  3. Consumer prefetch_count 설정 검토
  4. 에러 로그에서 처리 실패 확인

해결:
  - prefetch_count 조정 (1~10, 처리 속도에 맞게)
  - Consumer timeout 증가
  - nack + requeue 또는 DLQ로 실패 메시지 처리
```

```bash
# Connection별 unacked 확인
kubectl exec -n rabbitmq deploy/rabbitmq -- \
  rabbitmqctl list_consumers queue_name channel_pid ack_required \
  prefetch_count --formatter json
```

### Quorum Queue Leader Election

```bash
# Quorum queue 리더 분포
kubectl exec -n rabbitmq deploy/rabbitmq -- \
  rabbitmq-queues quorum_status <queue-name>

# 클러스터 노드 상태
kubectl exec -n rabbitmq deploy/rabbitmq -- \
  rabbitmqctl cluster_status --formatter json

# Memory alarm 확인
kubectl exec -n rabbitmq deploy/rabbitmq -- \
  rabbitmqctl status | grep -A5 "memory\|alarms"
```

### Memory Alarm 대응

```
Memory alarm 발생 시:
  1. 큰 큐 식별: list_queues 명령으로 message_bytes 확인
  2. Lazy queue로 전환 (메모리 → 디스크)
  3. Consumer 스케일 아웃으로 큐 소진
  4. TTL 설정으로 오래된 메시지 자동 삭제
  5. vm_memory_high_watermark 조정 (기본 0.4)
```

---

## NATS Troubleshooting

### JetStream Consumer Issues

```bash
# JetStream 스트림 상태
kubectl exec -n nats deploy/nats-box -- \
  nats stream info ORDERS -s nats://nats:4222

# Consumer 정보
kubectl exec -n nats deploy/nats-box -- \
  nats consumer info ORDERS order-processor -s nats://nats:4222

# Pending 메시지 확인
kubectl exec -n nats deploy/nats-box -- \
  nats consumer report ORDERS -s nats://nats:4222
```

### Slow Consumer 대응

```
증상:
  - "slow consumer detected" 로그
  - 메시지 드롭 발생
  - Consumer 연결 끊김

해결:
  - JetStream 사용 (Core NATS의 slow consumer 문제 해결)
  - AckPolicy: Explicit (자동 ack 비활성화)
  - MaxAckPending 조정 (Consumer 처리 능력에 맞게)
  - DeliverPolicy: New (과거 메시지 건너뛰기)
```

---

## Performance Tuning Checklist

### Kafka

```
Producer:
  □ batch.size: 16384~65536 (배치 크기 증가로 처리량 향상)
  □ linger.ms: 5~50 (배치 수집 대기 시간)
  □ compression.type: lz4 또는 zstd
  □ acks: -1 (durability) 또는 1 (throughput)
  □ buffer.memory: 충분한 크기 (기본 32MB)

Consumer:
  □ fetch.min.bytes: 1~1024 (서버 측 배치)
  □ max.poll.records: 처리 능력에 맞게 조정
  □ auto.offset.reset: earliest 또는 latest (용도에 따라)
  □ enable.auto.commit: false (수동 커밋 권장)

Broker:
  □ num.partitions: Consumer 수의 배수
  □ replication.factor: 3 (프로덕션)
  □ min.insync.replicas: 2
  □ log.retention.hours: 비즈니스 요구사항에 따라
```

### RabbitMQ

```
  □ prefetch_count: Consumer 처리 속도에 맞게 (1~100)
  □ Quorum Queue 사용 (Classic Mirrored Queue 대신)
  □ Lazy Queue 모드 (메모리 압박 시)
  □ Publisher Confirms 활성화
  □ Consumer ack 모드: manual
  □ 메시지 TTL 설정 (무한 큐 방지)
  □ Queue length limit (x-max-length)
```

---

## 참조 스킬

- [`kafka-patterns`](../kafka-patterns/SKILL.md) — Producer/Consumer 패턴, KEDA 오토스케일링
- [`kafka-k8s-operations`](../kafka-k8s-operations/SKILL.md) — Strimzi 운영, JMX→Prometheus
- [`rabbitmq`](../rabbitmq/SKILL.md) — Publisher Confirms, DLX, Cluster Operator
- [`nats-messaging`](../nats-messaging/SKILL.md) — JetStream, Consumer 패턴
- [`msa-event-driven`](../msa-event-driven/SKILL.md) — Outbox / 이벤트 스키마
- [`msa-resilience`](../msa-resilience/SKILL.md) — Retry / Circuit Breaker / Timeout
- [`msa-saga`](../msa-saga/SKILL.md) — Idempotent Consumer, DLQ + 보상
