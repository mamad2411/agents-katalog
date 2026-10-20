---
name: msa-event-driven
category: msa
description: "이벤트 드리븐 아키텍처 가이드 — 서비스 간 비동기 통신, 이벤트 스키마 설계, 발행/수신 패턴, Kubernetes 통합 Use when working with msa 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# 이벤트 드리븐 아키텍처 가이드

서비스 간 비동기 통신, 이벤트 스키마 설계, 발행/수신 패턴, Kubernetes 통합

## Quick Reference (결정 트리)

```
동기 vs 비동기?
    |
    +-- 즉각 응답 필요 ---------> REST/gRPC (동기)
    +-- 작업 완료 대기 불필요 ---> 이벤트 발행 (비동기)
    +-- 다수 서비스 알림 필요 ---> Pub/Sub 이벤트 (비동기)
    +-- 장시간 작업 -----------> 비동기 + 상태 폴링

메시징 모델 선택?
    |
    +-- 1:N 브로드캐스트 -------> Pub/Sub (Fan-out)
    +-- 순서 보장 + 리플레이 ---> Event Streaming (Kafka)
    +-- 1:1 작업 분배 ----------> Message Queue (RabbitMQ)
    +-- HTTP 이벤트 수신 -------> Webhook + 재시도

이벤트 발행 신뢰성?
    |
    +-- DB + 이벤트 원자성 -----> Transactional Outbox
    +-- DB 변경 실시간 캡처 ----> CDC (Debezium)
    +-- 단순 Fire-and-Forget ---> 직접 발행 (유실 허용)
```

---

## CRITICAL: 메시징 패턴 비교

### 통신 모델 비교

| 항목 | Pub/Sub | Point-to-Point | Event Streaming |
|------|---------|----------------|-----------------|
| 토폴로지 | 1:N (Fan-out) | 1:1 | 1:N (Consumer Group) |
| 메시지 보존 | 소비 후 삭제 | 소비 후 삭제 | 보존 기간 설정 가능 |
| 리플레이 | 불가 | 불가 | 가능 (offset 조정) |
| 순서 보장 | 미보장 | 보장 | 파티션 내 보장 |
| 사용 예 | 알림, 이벤트 전파 | 작업 큐, 태스크 분배 | 로그, 스트림 처리 |

### 브로커 비교

| 항목 | Kafka | RabbitMQ | NATS JetStream |
|------|-------|----------|----------------|
| 처리량 | 매우 높음 (수백만 msg/s) | 중간 (수만 msg/s) | 높음 |
| 지연시간 | ms 단위 | sub-ms 가능 | sub-ms |
| 메시지 보존 | 디스크 영구 보존 | 소비 후 삭제 기본 | 설정 가능 |
| 순서 보장 | 파티션 내 보장 | 큐 내 보장 | 스트림 내 보장 |
| Consumer Group | 네이티브 지원 | 플러그인 필요 | 네이티브 지원 |
| K8s 운영 | Strimzi Operator | RabbitMQ Operator | Helm Chart |
| 추천 사용 | 이벤트 소싱, CDC, 로그 | 작업 큐, RPC | 경량 메시징, IoT |

---

## 이벤트 스키마 설계

### CloudEvents 표준

CNCF 졸업 프로젝트로, 이벤트 데이터의 표준 포맷을 정의한다.

```json
{
  "specversion": "1.0",
  "id": "evt-20260205-001",
  "source": "/order-service",
  "type": "com.example.order.created",
  "subject": "order-12345",
  "time": "2026-02-05T10:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "order-12345",
    "customerId": "cust-789",
    "totalAmount": 59000
  }
}
```

### Avro vs Protobuf vs JSON Schema

| 항목 | Avro | Protobuf | JSON Schema |
|------|------|----------|-------------|
| 성능 | 높음 | 최고 (Avro 대비 ~5% 빠름) | 낮음 |
| 스키마 진화 | 우수 (forward/backward) | 우수 (tag 기반) | 기본적 |
| 코드 생성 | 선택 사항 | 필수 (.proto) | 불필요 |
| 가독성 | 낮음 (바이너리) | 낮음 (바이너리) | 높음 (텍스트) |
| 추천 용도 | Kafka 내부 통신, Data Lake | gRPC 연동, 최대 성능 | 외부 API, 파트너 연동 |

### Schema Registry 활용

```yaml
# application.yml - Confluent Schema Registry 연동
spring:
  kafka:
    properties:
      schema.registry.url: http://schema-registry:8081
      auto.register.schemas: true
    producer:
      value-serializer: io.confluent.kafka.serializers.KafkaAvroSerializer
    consumer:
      value-deserializer: io.confluent.kafka.serializers.KafkaAvroDeserializer
      properties:
        specific.avro.reader: true
```

### 이벤트 버저닝 전략

```
스키마 진화 규칙 (BACKWARD 호환):
  1. 새 필드 추가 시 반드시 default 값 지정
  2. 기존 필드 삭제 금지 (deprecated 마킹 후 유예기간)
  3. 필드 타입 변경 금지
  4. 필드명 변경 금지 (새 필드 추가 + 기존 deprecated)
  5. Protobuf: tag 번호 절대 재사용 금지

Upcaster 패턴:
  - v1 이벤트를 v2 포맷으로 변환하는 변환기
  - Consumer 측에서 버전별 변환 로직 적용
  - Schema Registry의 호환성 검증과 병행 사용
```

---

## 이벤트 발행 패턴

### CRITICAL: Transactional Outbox 패턴

DB 트랜잭션과 이벤트 발행의 원자성을 보장하는 핵심 패턴이다.

```
문제: DB 커밋 성공 + 이벤트 발행 실패 = 데이터 불일치
해결: 이벤트를 같은 DB에 outbox 테이블로 저장 후 별도 릴레이가 발행

[Service] --@Transactional--> [orders 테이블] + [outbox 테이블]
                                                      |
                                              [Polling/CDC Relay]
                                                      |
                                                  [Kafka Topic]
```

```java
// Outbox 엔티티
@Entity
@Table(name = "outbox_events")
public class OutboxEvent {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;
    @Column(nullable = false)
    private String aggregateType;  // 예: "Order"
    @Column(nullable = false)
    private String aggregateId;    // 예: 주문 ID
    @Column(nullable = false)
    private String eventType;      // 예: "OrderCreated"
    @Column(columnDefinition = "TEXT", nullable = false)
    private String payload;        // JSON 직렬화된 이벤트 데이터
    @Column(nullable = false)
    private boolean published = false;
    @Column(nullable = false)
    private Instant createdAt = Instant.now();
    // getter/setter 생략
}

// 주문 서비스 - 비즈니스 로직과 Outbox를 하나의 트랜잭션으로 처리
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final OutboxEventRepository outboxRepository;
    private final ObjectMapper objectMapper;

    @Transactional
    public Order createOrder(CreateOrderCommand cmd) {
        // 1. 비즈니스 로직 수행
        Order order = Order.create(cmd);
        orderRepository.save(order);
        // 2. 같은 트랜잭션에서 Outbox 이벤트 저장
        OutboxEvent event = new OutboxEvent();
        event.setAggregateType("Order");
        event.setAggregateId(order.getId());
        event.setEventType("OrderCreated");
        event.setPayload(objectMapper.writeValueAsString(
            new OrderCreatedEvent(order.getId(), order.getCustomerId(), order.getTotalAmount())
        ));
        outboxRepository.save(event);
        return order;
    }
}

// Outbox 릴레이 - 주기적으로 미발행 이벤트를 Kafka로 전송
@Component
@RequiredArgsConstructor
public class OutboxRelay {
    private final OutboxEventRepository outboxRepository;
    private final KafkaTemplate<String, String> kafkaTemplate;

    @Scheduled(fixedDelay = 1000)  // 1초마다 폴링
    @Transactional
    public void publishPendingEvents() {
        List<OutboxEvent> events = outboxRepository
            .findByPublishedFalseOrderByCreatedAtAsc();
        for (OutboxEvent event : events) {
            kafkaTemplate.send(
                event.getAggregateType().toLowerCase() + "-events",
                event.getAggregateId(),
                event.getPayload()
            );
            event.setPublished(true);
        }
    }
}
```

### CDC (Change Data Capture) with Debezium

Outbox 테이블의 변경을 Debezium이 자동 캡처하여 Kafka로 전달한다.
폴링 방식 대비 실시간성이 높고, 애플리케이션 코드 변경 없이 적용 가능하다.

```
[DB outbox 테이블] --WAL/Binlog--> [Debezium Connector] --> [Kafka Topic]
```

```yaml
# Strimzi KafkaConnector - Debezium PostgreSQL Outbox Connector
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaConnector
metadata:
  name: outbox-connector
  labels:
    strimzi.io/cluster: kafka-connect-cluster
spec:
  class: io.debezium.connector.postgresql.PostgresConnector
  tasksMax: 1
  config:
    database.hostname: postgres-service
    database.port: "5432"
    database.user: "${secrets:db-credentials:username}"
    database.password: "${secrets:db-credentials:password}"
    database.dbname: orderdb
    # Outbox 전용 SMT (Single Message Transform)
    transforms: outbox
    transforms.outbox.type: io.debezium.transforms.outbox.EventRouter
    transforms.outbox.table.field.event.id: id
    transforms.outbox.table.field.event.key: aggregate_id
    transforms.outbox.table.field.event.type: event_type
    transforms.outbox.table.field.event.payload: payload
    transforms.outbox.route.topic.replacement: "${routedByValue}-events"
    schema.history.internal.kafka.topic: schema-changes
    schema.history.internal.kafka.bootstrap.servers: kafka-cluster:9092
```

---

## 이벤트 수신 패턴

### CRITICAL: Idempotent Consumer 패턴

Kafka는 at-least-once 전달을 보장하므로 중복 메시지가 발생할 수 있다.
Consumer는 반드시 멱등성을 보장해야 한다.

```java
// 처리 완료 이벤트 추적 테이블
@Entity
@Table(name = "processed_events")
public class ProcessedEvent {
    @Id
    private String eventId;  // 이벤트 고유 ID
    @Column(nullable = false)
    private Instant processedAt;
}

// Idempotent Consumer 구현
@Component
@RequiredArgsConstructor
public class OrderEventConsumer {
    private final ProcessedEventRepository processedEventRepo;
    private final OrderFulfillmentService fulfillmentService;

    @KafkaListener(topics = "order-events", groupId = "fulfillment-group")
    @Transactional
    public void consume(
            @Header(KafkaHeaders.RECEIVED_KEY) String key,
            @Payload String payload,
            @Header("eventId") String eventId) {
        // 1. 중복 체크 - 이미 처리된 이벤트인지 확인
        if (processedEventRepo.existsById(eventId)) {
            log.info("중복 이벤트 무시: eventId={}", eventId);
            return;
        }
        // 2. 비즈니스 로직 처리
        OrderCreatedEvent event = objectMapper.readValue(payload, OrderCreatedEvent.class);
        fulfillmentService.startFulfillment(event);
        // 3. 처리 완료 기록 (같은 트랜잭션)
        processedEventRepo.save(new ProcessedEvent(eventId, Instant.now()));
    }
}
```

> DB 기반 중복 체크가 가장 안전하다. 캐시(Redis, Caffeine)는 TTL 만료 후
> 중복 처리 위험이 있으므로, 부작용이 큰 작업에는 DB 기반을 사용한다.

### Dead Letter Queue (DLQ)

처리 실패한 메시지를 별도 토픽에 보관하여 데이터 유실을 방지한다.

```java
// Spring Kafka - Non-Blocking Retry + DLT 설정
@Component
public class PaymentEventConsumer {
    // 최대 4회 시도, 지수 백오프 (1s, 2s, 4s), 실패 시 DLT로 이동
    @RetryableTopic(
        attempts = "4",
        backoff = @Backoff(delay = 1000, multiplier = 2),
        topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE,
        dltStrategy = DltStrategy.FAIL_ON_ERROR
    )
    @KafkaListener(topics = "payment-events", groupId = "payment-group")
    public void consume(PaymentEvent event) {
        paymentProcessor.process(event);  // 실패 시 자동 재시도
    }

    @DltHandler  // 모든 재시도 소진 후 호출
    public void handleDlt(PaymentEvent event,
            @Header(KafkaHeaders.EXCEPTION_MESSAGE) String error) {
        log.error("DLT 도착: event={}, error={}", event.getPaymentId(), error);
        alertService.notifyDltArrival("payment-events", event, error);
    }
}
```

```
메시지 흐름:
[payment-events] --> 실패 --> [payment-events-retry-0] (1초 후)
                    --> 실패 --> [payment-events-retry-1] (2초 후)
                      --> 실패 --> [payment-events-retry-2] (4초 후)
                        --> 실패 --> [payment-events-dlt]

재처리 전략: 1) 자동 스케줄러 재처리  2) 관리자 수동 승인 후 재처리
           3) Parking Lot 패턴 (재처리 3회 실패 시 별도 토픽으로 격리)
```

### Consumer Group 전략

```yaml
# application.yml - Consumer Group 설정
spring:
  kafka:
    consumer:
      group-id: order-fulfillment-group
      properties:
        # CooperativeStickyAssignor: 점진적 리밸런싱 (추천)
        # 리밸런싱 시 기존 할당 유지, Stop-the-World 방지
        partition.assignment.strategy: org.apache.kafka.clients.consumer.CooperativeStickyAssignor
      max-poll-records: 500           # 한 번에 가져올 최대 레코드 수
      max-poll-interval-ms: 300000    # 최대 처리 시간 (5분)
      session-timeout-ms: 45000      # 세션 타임아웃
      heartbeat-interval-ms: 15000   # 하트비트 간격
      auto-offset-reset: earliest    # 신규 그룹 시작 위치
      enable-auto-commit: false      # 수동 커밋 권장
    listener:
      ack-mode: MANUAL_IMMEDIATE     # 수동 커밋 모드
      concurrency: 3                 # Consumer 스레드 수
```

---

## Kubernetes 통합

### KEDA 이벤트 기반 스케일링

KEDA(CNCF 졸업 프로젝트)는 외부 이벤트 소스 기반으로 Pod를 자동 스케일링한다.
유휴 시 0으로 축소 가능하여 비용을 절감한다. 59개 이상의 이벤트 소스를 지원한다.

```yaml
# Kafka Consumer Lag 기반 ScaledObject
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-consumer-scaler
  namespace: order-service
spec:
  scaleTargetRef:
    name: order-consumer        # 스케일링 대상 Deployment
  pollingInterval: 15           # 메트릭 폴링 간격 (초)
  cooldownPeriod: 60            # 스케일 다운 대기 시간 (초)
  minReplicaCount: 0            # 최소 레플리카 (0 = scale-to-zero)
  maxReplicaCount: 20           # 최대 레플리카
  triggers:
    - type: kafka
      metadata:
        bootstrapServers: kafka-cluster:9092
        consumerGroup: order-fulfillment-group
        topic: order-events
        lagThreshold: "50"      # 파티션당 lag 50 이상이면 스케일 업
        activationLagThreshold: "5"  # lag 5 이상이면 0에서 1로 활성화
        offsetResetPolicy: earliest
---
# SQS/RabbitMQ 트리거도 동일한 구조로 적용 가능
# triggers[].type: aws-sqs-queue, rabbitmq, prometheus, cron 등
# 각 트리거별 metadata에 큐 URL, threshold 등 설정
```

### Knative Eventing (간략)

```
Knative 선택 기준:
  - HTTP/gRPC 요청 기반 스케일링 --> Knative Serving
  - 큐/스트림 백로그 기반 스케일링 --> KEDA
  - 두 가지 혼합 --> Knative(API) + KEDA(Worker) 조합

주의: 하나의 Deployment에 KEDA와 Knative를 동시 적용하지 않는다.

Knative Eventing 구성 요소:
  - Broker: 이벤트 수신 및 라우팅
  - Trigger: 필터 조건에 따른 구독
  - Source: 외부 이벤트 소스 연동 (Kafka, GitHub, etc.)
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 모든 것을 이벤트로 | 불필요한 복잡성, 디버깅 난이도 증가 | 동기 호출이 적합한 경우 REST/gRPC 유지 |
| 이벤트에 내부 스키마 노출 | 서비스 간 강결합 (DB 스키마 공유와 동일) | Public Event와 Internal Model 분리 |
| 순서 보장 과도 의존 | 스케일링 제한, 파티션 병목 | Saga로 순서 무관하게 설계 |
| 이벤트 과다 발행 (Chatty) | 메시지 폭증, 네트워크 과부하 | 도메인 이벤트 단위로 집약 |
| Outbox 미사용 직접 발행 | DB 커밋-이벤트 발행 불일치 | Transactional Outbox 또는 CDC 적용 |
| 멱등성 미구현 | 중복 처리로 데이터 오염 | Idempotent Consumer 패턴 필수 적용 |
| DLQ 미설정 | 실패 메시지 유실, 원인 파악 불가 | DLQ + 알림 + 재처리 파이프라인 구축 |
| Fat Event (과대 페이로드) | 브로커 부하, 네트워크 비용 증가 | 이벤트에 ID만, 상세 데이터는 API 조회 |
| Consumer에서 Producer 직접 호출 | 순환 의존, 무한 루프 위험 | Saga/Choreography로 이벤트 체인 관리 |
| 단일 토픽에 모든 이벤트 | 스케일링 불가, 필터링 부하 | 도메인별 토픽 분리 |

---

## 체크리스트

### 설계 단계
- [ ] 동기/비동기 통신 경계를 명확히 정의했는가?
- [ ] 이벤트 스키마에 CloudEvents 표준을 적용했는가?
- [ ] Schema Registry를 통한 스키마 버저닝을 구성했는가?
- [ ] 스키마 호환성 레벨(BACKWARD/FORWARD/FULL)을 결정했는가?
- [ ] 도메인별 토픽 분리 전략을 수립했는가?

### 발행 단계
- [ ] Transactional Outbox 또는 CDC로 발행 원자성을 보장하는가?
- [ ] 이벤트에 고유 ID (eventId)가 포함되어 있는가?
- [ ] Producer의 idempotence=true, acks=all 설정을 확인했는가?
- [ ] 이벤트 페이로드 크기가 적정한가? (1MB 미만 권장)

### 수신 단계
- [ ] Idempotent Consumer로 중복 처리를 방지하는가?
- [ ] DLQ(Dead Letter Queue)를 설정하고 알림을 연동했는가?
- [ ] Consumer Group의 파티션 할당 전략을 검토했는가?
- [ ] CooperativeStickyAssignor로 리밸런싱 영향을 최소화했는가?
- [ ] enable.auto.commit=false로 수동 커밋을 사용하는가?

### 운영 단계
- [ ] KEDA ScaledObject로 Consumer 자동 스케일링을 구성했는가?
- [ ] Consumer Lag 모니터링 및 알림을 설정했는가?
- [ ] DLQ 메시지 재처리 절차를 문서화했는가?
- [ ] 이벤트 흐름에 분산 추적(Distributed Tracing)을 적용했는가?

---

## 참조 스킬

- `/kafka` - Kafka 클러스터, Strimzi Operator, 핵심 개념
- `/kafka-patterns` - Producer/Consumer 구현, KEDA 오토스케일링
- `/msa-saga` - Saga 패턴 (Choreography/Orchestration)
- `/msa-cqrs-eventsourcing` - CQRS, Event Sourcing 패턴
- `/observability-otel` - OpenTelemetry 분산 추적
- `/nats-messaging` - NATS JetStream 기반 이벤트 드리븐
- `/rabbitmq` - RabbitMQ Exchange, Quorum Queue

## 참고 레퍼런스

### Go
- [go-food-delivery-microservices](https://github.com/mehdihadeli/go-food-delivery-microservices) -- DDD + CQRS + Event Sourcing + RabbitMQ
- [shop-golang-microservices](https://github.com/meysamhadeli/shop-golang-microservices) -- Vertical Slice + Event-Driven

### Java/Spring
- [spring-food-delivery-microservices](https://github.com/mehdihadeli/spring-food-delivery-microservices) -- DDD + CQRS + Event-Driven
- [spring-kafka-microservices](https://github.com/ZaTribune/spring-kafka-microservices) -- Kafka 기반 E-commerce Event-Driven
- [ecommerce-microservices](https://github.com/hoangtien2k3/ecommerce-microservices) -- Spring Cloud + Kafka + WebFlux Reactive
