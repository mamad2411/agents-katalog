---
name: msa-cqrs-eventsourcing
category: msa
description: "CQRS & Event Sourcing 가이드 — Command/Query 분리와 이벤트 기반 상태 관리로 확장 가능한 마이크로서비스를 구축하는 실전 가이드 Use when working with msa 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# CQRS & Event Sourcing 가이드

Command/Query 분리와 이벤트 기반 상태 관리로 확장 가능한 마이크로서비스를 구축하는 실전 가이드

## Quick Reference (결정 트리)

```
데이터 처리 패턴 선택?
    ├─ 읽기/쓰기 비율 유사, 단순 도메인 ──────> 전통 CRUD
    ├─ 읽기 >> 쓰기, 복잡한 조회 요구 ────────> CQRS만 (ES 없이)
    │   └─ 별도 Read Model + Write Model
    └─ 감사 추적/시간 여행/리플레이 필요 ─────> CQRS + Event Sourcing
        └─ Event Store + Projection + Snapshot

Event Store 선택?
    ├─ 높은 처리량, 스트리밍 중심 ────> Kafka (+ 외부 Snapshot Store)
    ├─ 순수 이벤트 저장소 ───────────> EventStoreDB
    └─ 프레임워크 통합 ──────────────> Axon Server
```

---

## CRITICAL: CQRS vs Traditional 비교

| 항목 | 전통 CRUD | CQRS만 | CQRS + Event Sourcing |
|------|-----------|--------|----------------------|
| **데이터 모델** | 단일 모델 | 읽기/쓰기 분리 | 이벤트 로그 + Projection |
| **확장성** | 수직 스케일링 | 읽기/쓰기 독립 스케일링 | 읽기/쓰기 독립 + 리플레이 |
| **일관성** | Strong | Eventual 가능 | Eventual Consistency |
| **감사 추적** | 별도 구현 | 별도 구현 | 자동 (이벤트 = 이력) |
| **복잡도** | 낮음 | 중간 | 높음 |
| **적합 대상** | 단순 도메인 | 읽기 집중, 복잡 조회 | 금융/결제/규제 도메인 |

---

## CQRS 패턴

### 아키텍처 다이어그램

```
              ┌──────────────────────────────┐
              │         API Gateway          │
              └──────┬───────────┬───────────┘
                     │           │
          ┌──────────▼───┐  ┌───▼────────────┐
          │ Command Side │  │  Query Side     │
          │ (Write)      │  │  (Read)         │
          │ ┌──────────┐ │  │ ┌────────────┐ │
          │ │ Command  │ │  │ │Query       │ │
          │ │ Handler  │ │  │ │Handler     │ │
          │ └────┬─────┘ │  │ └─────┬──────┘ │
          │ ┌────▼─────┐ │  │ ┌─────▼──────┐ │
          │ │Write DB  │ │  │ │Read DB     │ │
          │ └────┬─────┘ │  │ └────────────┘ │
          └──────┼───────┘  └───────▲────────┘
                 │     Event Bus    │
            ┌────▼──────────────────┴────┐
            │  Kafka (이벤트 → Projection)│
            └────────────────────────────┘
```

### Command Handler (Spring Boot)

```java
public record CreateOrderCommand(
    String orderId, String customerId,
    List<OrderLineItem> items, BigDecimal totalAmount
) {}

@Service
@RequiredArgsConstructor
public class OrderCommandHandler {
    private final OrderRepository orderRepository;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public String handle(CreateOrderCommand cmd) {
        if (cmd.items() == null || cmd.items().isEmpty())
            throw new InvalidOrderException("주문 항목이 비어있습니다");

        Order order = Order.create(cmd.orderId(), cmd.customerId(),
            cmd.items(), cmd.totalAmount());
        orderRepository.save(order);

        // 도메인 이벤트 발행
        eventPublisher.publishEvent(new OrderCreatedEvent(
            order.getId(), order.getCustomerId(),
            order.getTotalAmount(), Instant.now()));
        return order.getId();
    }
}
```

### Query Handler (Spring Boot)

```java
public record OrderSummaryView(
    String orderId, String customerName,
    BigDecimal totalAmount, String status, LocalDateTime createdAt
) {}

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class OrderQueryHandler {
    private final OrderReadRepository readRepository;

    public OrderSummaryView findOrder(String orderId) {
        return readRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));
    }

    public Page<OrderSummaryView> findByCustomer(String customerId, Pageable pageable) {
        return readRepository.findByCustomerId(customerId, pageable);
    }
}
```

---

## Event Sourcing

### 이벤트 스키마 설계

```java
// 기본 도메인 이벤트 인터페이스
public interface DomainEvent {
    String getAggregateId();
    Instant getOccurredAt();
    int getVersion();        // 스키마 버전 관리
    String getEventType();   // 이벤트 타입 식별자
}

// 주문 도메인 이벤트 (비즈니스 의미를 담는 이벤트명 사용)
public record OrderCreatedEvent(
    String orderId, String customerId,
    BigDecimal totalAmount, List<OrderLineItem> items, Instant occurredAt
) implements DomainEvent {
    public String getAggregateId() { return orderId; }
    public int getVersion() { return 1; }
    public String getEventType() { return "ORDER_CREATED"; }
}
```

### Event Store 엔티티

```java
@Entity
@Table(name = "event_store", indexes = {
    @Index(name = "idx_aggregate", columnList = "aggregateId, sequenceNumber")
})
public class EventEntry {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String aggregateId;
    private String aggregateType;
    private long sequenceNumber;     // Aggregate 내 이벤트 순서
    private String eventType;
    private String payload;          // JSON 직렬화
    private Instant createdAt;
    private int schemaVersion;       // 스키마 진화 관리
    private String metadata;         // correlationId 등
}

@Repository
public interface EventStoreRepository extends JpaRepository<EventEntry, Long> {
    List<EventEntry> findByAggregateIdOrderBySequenceNumberAsc(String aggregateId);
    List<EventEntry> findByAggregateIdAndSequenceNumberGreaterThan(
        String aggregateId, long snapshotSequence);
}
```

### Kafka를 Event Store로 활용

```java
@Service
@RequiredArgsConstructor
public class KafkaEventPublisher {
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final ObjectMapper objectMapper;

    public void publish(DomainEvent event) {
        String payload = objectMapper.writeValueAsString(event);
        // aggregateId를 Key로 → 같은 Aggregate 이벤트는 같은 파티션 (순서 보장)
        var record = new ProducerRecord<>("order-events",
            event.getAggregateId(), payload);
        record.headers()
            .add("eventType", event.getEventType().getBytes())
            .add("schemaVersion", String.valueOf(event.getVersion()).getBytes());
        kafkaTemplate.send(record);
    }
}

// Kafka Producer 필수 설정
// acks=all (모든 ISR 확인), enable.idempotence=true (중복 방지), retries=3
```

### Snapshot 전략

```java
@Entity
@Table(name = "aggregate_snapshots")
public class AggregateSnapshot {
    @Id private String aggregateId;
    private long lastSequenceNumber;  // 스냅샷 시점 이벤트 시퀀스
    private String snapshotData;      // JSON 직렬화된 Aggregate 상태
    private int schemaVersion;        // 스냅샷 스키마 버전 (진화 관리)
    private Instant createdAt;
}

@Service
@RequiredArgsConstructor
public class OrderAggregateLoader {
    private final EventStoreRepository eventStore;
    private final SnapshotRepository snapshotRepo;
    private static final int SNAPSHOT_THRESHOLD = 100; // 메트릭 기반 조정

    public Order load(String orderId) {
        var snapshot = snapshotRepo.findById(orderId);
        Order order;
        List<EventEntry> events;
        if (snapshot.isPresent()) {
            // 스냅샷 복원 후 이후 이벤트만 리플레이
            order = deserializeSnapshot(snapshot.get());
            events = eventStore.findByAggregateIdAndSequenceNumberGreaterThan(
                orderId, snapshot.get().getLastSequenceNumber());
        } else {
            order = new Order();
            events = eventStore.findByAggregateIdOrderBySequenceNumberAsc(orderId);
        }
        events.forEach(e -> order.apply(deserializeEvent(e)));
        // 임계값 초과 시 새 스냅샷 생성
        if (events.size() > SNAPSHOT_THRESHOLD) saveSnapshot(order);
        return order;
    }
}
```

**Snapshot 핵심 원칙**: 조기 최적화 금지. Aggregate 복원 시간 메트릭을 먼저 수집하고, 95th percentile이 SLO를 초과할 때 도입. 스냅샷 스키마 버전이 불일치하면 폐기 후 전체 리플레이.

---

## Eventual Consistency

### 일관성 모델 비교

| 특성 | Strong Consistency | Eventual Consistency |
|------|-------------------|---------------------|
| **모델** | ACID | BASE (Basically Available, Soft state) |
| **지연** | 높음 (동기 대기) | 낮음 (비동기 처리) |
| **가용성** | 일관성 우선 | 가용성 우선, 일시적 불일치 허용 |
| **사용 사례** | 은행 이체, 재고 차감 | 조회 화면, 추천, 알림 |

### Projection (Materialized View) 구현

```java
@Component
@RequiredArgsConstructor
public class OrderProjection {
    private final OrderReadModelRepository readModelRepo;

    @KafkaListener(topics = "order-events", groupId = "order-projection")
    public void on(ConsumerRecord<String, String> record) {
        String eventType = new String(
            record.headers().lastHeader("eventType").value());
        switch (eventType) {
            case "ORDER_CREATED" -> {
                var event = deserialize(record.value(), OrderCreatedEvent.class);
                readModelRepo.save(OrderReadModel.builder()
                    .orderId(event.orderId()).customerId(event.customerId())
                    .totalAmount(event.totalAmount()).status("CREATED")
                    .createdAt(event.occurredAt()).build());
            }
            case "ORDER_CONFIRMED" -> {
                var event = deserialize(record.value(), OrderConfirmedEvent.class);
                readModelRepo.updateStatus(event.orderId(), "CONFIRMED");
            }
        }
    }
}
```

### Idempotency 보장

```java
@Component
@RequiredArgsConstructor
public class IdempotentEventHandler {
    private final ProcessedEventRepository processedEventRepo;

    // eventId 기반 중복 방지 (DB Unique 제약조건 활용)
    public boolean tryProcess(String eventId, Runnable handler) {
        try {
            processedEventRepo.save(new ProcessedEvent(eventId, Instant.now()));
            handler.run();
            return true;
        } catch (DataIntegrityViolationException e) {
            log.info("중복 이벤트 무시: {}", eventId);
            return false; // 이미 처리된 이벤트
        }
    }
}

@Entity @Table(name = "processed_events")
public class ProcessedEvent {
    @Id private String eventId;
    private Instant processedAt;
}
```

**충돌 해결 전략**: UI 낙관적 업데이트(Command 성공 시 즉시 반영), Read Model 폴링/SSE로 최종 상태 동기화, Last-Writer-Wins 또는 도메인 로직 기반 머지.

---

## Axon Framework (선택적 도구)

```groovy
// build.gradle - Axon 4.9+ / Spring Boot 3.x
dependencies {
    implementation 'org.axonframework:axon-spring-boot-starter:4.9.2'
    testImplementation 'org.axonframework:axon-test:4.9.2'
}
// Axon Server: docker run -d --name axonserver -p 8024:8024 -p 8124:8124 axoniq/axonserver
```

```java
@Aggregate
public class OrderAggregate {
    @AggregateIdentifier private String orderId;
    private OrderStatus status;
    private BigDecimal totalAmount;
    protected OrderAggregate() {}

    @CommandHandler  // 주문 생성 커맨드
    public OrderAggregate(CreateOrderCommand cmd) {
        if (cmd.totalAmount().compareTo(BigDecimal.ZERO) <= 0)
            throw new IllegalArgumentException("주문 금액은 0보다 커야 합니다");
        AggregateLifecycle.apply(new OrderCreatedEvent(
            cmd.orderId(), cmd.customerId(), cmd.totalAmount(), Instant.now()));
    }

    @CommandHandler  // 주문 확인 커맨드
    public void handle(ConfirmOrderCommand cmd) {
        if (this.status != OrderStatus.CREATED)
            throw new IllegalStateException("CREATED 상태에서만 확인 가능");
        AggregateLifecycle.apply(new OrderConfirmedEvent(
            this.orderId, cmd.confirmedBy(), Instant.now()));
    }

    @EventSourcingHandler  // 이벤트로부터 상태 복원
    public void on(OrderCreatedEvent e) {
        this.orderId = e.orderId();
        this.totalAmount = e.totalAmount();
        this.status = OrderStatus.CREATED;
    }

    @EventSourcingHandler
    public void on(OrderConfirmedEvent e) { this.status = OrderStatus.CONFIRMED; }
}

@Component
@RequiredArgsConstructor
public class OrderQueryProjection {
    private final OrderViewRepository repository;

    @EventHandler  // Read Model 갱신
    public void on(OrderCreatedEvent e) {
        repository.save(new OrderView(e.orderId(), e.customerId(),
            e.totalAmount(), "CREATED"));
    }

    @QueryHandler  // 조회 처리
    public OrderView handle(FindOrderQuery q) {
        return repository.findById(q.orderId())
            .orElseThrow(() -> new OrderNotFoundException(q.orderId()));
    }
}
```

---

## Kubernetes 배포

### Kafka Event Store (Strimzi) - 핵심 설정

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata: { name: event-store-kafka, namespace: cqrs-system }
spec:
  kafka:
    replicas: 3
    config:
      log.retention.hours: -1          # 이벤트 영구 보관 (Event Store 필수)
      log.retention.bytes: -1
      min.insync.replicas: 2
      auto.create.topics.enable: false
    storage: { type: persistent-claim, size: 100Gi, class: gp3 }
  zookeeper:
    replicas: 3
    storage: { type: persistent-claim, size: 20Gi }
```

### Read/Write 서비스 분리 배포 전략

| 서비스 | replicas | CPU/Memory | DB | 특성 |
|--------|----------|------------|-----|------|
| **Command (Write)** | 2 | 500m~1 / 512Mi~1Gi | write-db (PostgreSQL) | 쓰기 최적화, Kafka 연동 |
| **Query (Read)** | 4+ | 250m~500m / 256Mi~512Mi | read-db (비정규화) | 읽기 최적화, HPA 대상 |
| **Projection** | 1~12 | KEDA 자동 | read-db 갱신 | Consumer Lag 기반 스케일 |

### Projection KEDA 오토스케일링

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata: { name: order-projection-scaler }
spec:
  scaleTargetRef: { name: order-projection-service }
  pollingInterval: 15
  cooldownPeriod: 60
  minReplicaCount: 1
  maxReplicaCount: 12              # Kafka 파티션 수 이하
  triggers:
    - type: kafka
      metadata:
        bootstrapServers: event-store-kafka-bootstrap:9092
        consumerGroup: order-projection
        topic: order-events
        lagThreshold: "500"
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| **단순 도메인에 CQRS+ES 적용** | 불필요한 복잡도 증가 | CRUD 사용, 필요한 Bounded Context에만 적용 |
| **CRUD 스타일 이벤트** | `UserUpdatedEvent` 무의미 | 도메인 기반: `OrderShippedEvent` |
| **시스템 전체에 CQRS** | 복잡도 폭증 | DDD Bounded Context별 선택적 적용 |
| **Snapshot 미설계** | 복원 시간 급증 | 메트릭 기반 임계값, 주기적 스냅샷 |
| **스키마 버전 미관리** | 역직렬화 실패 | Schema Registry + Upcaster 패턴 |
| **Idempotency 미구현** | 중복 이벤트 → 데이터 오류 | eventId 기반 중복 체크 |
| **이벤트 스트림 공유** | 서비스 간 강결합 | 독립 스트림 + Anti-Corruption Layer |
| **Eventual Consistency 무시** | 오래된 데이터 노출 | UI 낙관적 업데이트 + 폴링/SSE |
| **자체 프레임워크 구축** | 버그, 재개발 비용 | Axon 등 검증된 프레임워크 사용 |
| **이벤트에 민감 정보** | GDPR 삭제 불가 | Crypto Shredding (키 삭제) |

---

## 체크리스트

### 설계 단계
- [ ] CQRS 적용 범위 결정 (전체 vs Bounded Context)
- [ ] CQRS만 vs CQRS+ES 결정 (도메인 복잡도 기준)
- [ ] 이벤트 스키마 설계 및 버전 관리 전략
- [ ] Aggregate 경계 및 이벤트 스트림 식별
- [ ] 일관성 요구사항 분석 (Strong vs Eventual)

### 구현 단계
- [ ] Command Handler / Query Handler 분리
- [ ] Event Store (DB 또는 Kafka) 구성
- [ ] Projection (Read Model 동기화) 구현
- [ ] Idempotent Consumer (eventId 기반)
- [ ] Snapshot 전략 (메트릭 기반 임계값)
- [ ] 직렬화 포맷 결정 (JSON/Avro/Protobuf)

### 배포 및 운영
- [ ] Command/Query 서비스 독립 배포
- [ ] Kafka retention 정책 (ES용: 무기한)
- [ ] Projection KEDA 오토스케일링
- [ ] Consumer Lag 모니터링 및 알림
- [ ] Aggregate 복원 시간 메트릭 수집
- [ ] 이벤트 리플레이 테스트 (장애 복구)
- [ ] Schema Registry 운영

## 참조 스킬

- `/kafka-patterns` - Kafka Producer/Consumer 패턴, KEDA 오토스케일링
- `/kafka` - Kafka 기본 개념, Strimzi 클러스터 운영
- `/spring-data` - Spring Data JPA, Repository 패턴
- `/k8s-helm` - Kubernetes Helm 배포
- `/deployment-strategies` - 배포 전략 (Blue-Green, Canary)

## 참고 레퍼런스

### Go
- [go-food-delivery-microservices](https://github.com/mehdihadeli/go-food-delivery-microservices) -- CQRS + Event Sourcing + RabbitMQ + gRPC

### Java/Spring
- [event-sourcing-microservices-example](https://github.com/kbastani/event-sourcing-microservices-example) -- Event Sourcing + K8s + Helm 배포
- [ddd-cqrs-4-java-example](https://github.com/fuinorg/ddd-cqrs-4-java-example) -- Quarkus + Spring Boot + EventStore
- [booking-microservices-java-spring-boot](https://github.com/meysamhadeli/booking-microservices-java-spring-boot) -- CQRS + DDD + gRPC + MongoDB
- [product-microservice-cqrs](https://github.com/SuperMohit/product-microservice-cqrs) -- Hexagonal + CQRS + Netflix OSS
