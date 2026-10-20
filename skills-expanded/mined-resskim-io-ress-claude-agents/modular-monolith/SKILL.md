---
name: modular-monolith
category: architecture
description: "Modular Monolith Architecture — 단일 배포 단위 내에서 모듈 경계를 강제하여 확장성과 단순성의 균형을 달성하는 아키텍처 패턴 Use when working with architecture 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Modular Monolith Architecture

단일 배포 단위 내에서 모듈 경계를 강제하여 확장성과 단순성의 균형을 달성하는 아키텍처 패턴

## Quick Reference (결정 트리)

```
아키텍처 선택?
    │
    ├─ 팀 1~5명, 도메인 단순 ──────────> Monolith
    ├─ 팀 5~15명, 도메인 중간 복잡도 ──> Modular Monolith (권장)
    │    ├─ Module = Bounded Context
    │    ├─ Event Bus로 모듈 간 통신
    │    └─ 추후 서비스 추출 가능
    └─ 팀 15명+, 독립 배포/스케일링 필요 ──> Microservices

모듈 추출 시점?
    ├─ 팀이 2개 이상으로 성장 ─────────> 서비스 추출
    ├─ 독립 스케일링 필요 (10x 트래픽) ──> 서비스 분리
    ├─ 배포 독립성 필요 ─────────────> 서비스 분리
    └─ 기술 스택 다변화 필요 ──────────> 서비스 분리
```

---

## CRITICAL: 왜 Modular Monolith인가?

```
실제 산업 데이터:
  - 42% of organizations consolidating microservices back (2024)
  - 비용 절감: 3.75x ~ 6x (인프라, 운영, 개발)
  - 개발 생산성 향상: 30~50%

MSA의 숨겨진 비용:
  ├─ 인프라: 서비스당 컨테이너/DB, Service Mesh, API Gateway
  ├─ 운영: 분산 트랜잭션, 장애 추적, 데이터 일관성
  ├─ 개발: 분산 테스트, Contract Testing, 네트워크 디버깅
  └─ 조직: 팀 간 조율 오버헤드
```

| 항목 | Modular Monolith | Microservices |
|------|------------------|---------------|
| **배포** | 단일 아티팩트 | 서비스별 독립 배포 |
| **통신** | In-Process (메서드/이벤트) | Network (HTTP/gRPC/Kafka) |
| **트랜잭션** | ACID (단일 DB) | Saga, Eventual Consistency |
| **디버깅** | 단일 프로세스 (IDE) | 분산 추적 필수 |
| **인프라** | 단순 (앱 서버 + DB) | 복잡 (K8s, Mesh) |
| **팀 규모** | 5~15명 최적 | 15명+ 최적 |
| **장애 격리** | 전체 장애 | 서비스별 격리 |

---

## CRITICAL: 모듈 설계 원칙

```
┌────────────────────────────────────────────────────┐
│       Modular Monolith (Single Deployment)         │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐      │
│ │Order Module│ │Payment Mod │ │Inventory   │      │
│ │ Domain     │ │ Domain     │ │ Domain     │      │
│ │ Service    │ │ Service    │ │ Service    │      │
│ │ Repository │ │ Repository │ │ Repository │      │
│ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘      │
│       └── Internal Event Bus (ApplicationEvent) ─┘ │
│ ┌─────────────────────────────────────────────┐    │
│ │ Single Database (Schema per Module)         │    │
│ └─────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────┘
```

### Public API vs Internal

```
com.example.order/
├── api/                          # PUBLIC: 다른 모듈에서 사용
│   ├── OrderService.java         # 인터페이스
│   ├── dto/CreateOrderRequest.java
│   └── event/OrderCreatedEvent.java
└── internal/                     # PRIVATE: 모듈 내부만
    ├── domain/Order.java
    ├── service/OrderServiceImpl.java
    └── repository/OrderRepository.java
```

### Database per Module

```sql
CREATE SCHEMA order_schema;
CREATE SCHEMA payment_schema;
-- 모듈 간 참조는 ID만 (Foreign Key 금지)
CREATE TABLE order_schema.orders (
  id UUID PRIMARY KEY,
  customer_id UUID NOT NULL,  -- FK 없음
  status VARCHAR(20)
);
```

---

## Spring Modulith 구현

```java
// === Public API ===
package com.example.order;
public interface OrderService {
    OrderResult createOrder(CreateOrderRequest request);
}
public record OrderCreatedEvent(String orderId, String customerId,
                                BigDecimal totalAmount, Instant createdAt) {}

// === Internal 구현 ===
package com.example.order.internal;

@Service
@RequiredArgsConstructor
class OrderServiceImpl implements OrderService {
    private final OrderRepository orderRepository;
    private final ApplicationEventPublisher events;

    @Transactional
    @Override
    public OrderResult createOrder(CreateOrderRequest request) {
        Order order = Order.create(request.customerId(), request.items());
        orderRepository.save(order);
        events.publishEvent(new OrderCreatedEvent(
            order.getId(), order.getCustomerId(),
            order.getTotalAmount().amount(), Instant.now()));
        return OrderResult.from(order);
    }
}

// === Payment: Event 수신 ===
package com.example.payment.internal;

@Component
class PaymentEventListener {
    @ApplicationModuleListener
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void onOrderCreated(OrderCreatedEvent event) {
        paymentService.createPayment(event.orderId(), event.totalAmount());
    }
}
// Spring Modulith가 event_publication 테이블로 Outbox 패턴 자동 처리
```

### 모듈 의존성 검증

```java
class ModuleStructureTest {
    ApplicationModules modules = ApplicationModules.of(OrderApplication.class);

    @Test
    void verifiesModularStructure() {
        modules.verify(); // Cyclic dependency, internal 노출 탐지
    }
    @Test
    void createModuleDocumentation() throws Exception {
        new Documenter(modules).writeDocumentation(); // C4 다이어그램 자동 생성
    }
}

@ApplicationModuleTest
class OrderModuleIntegrationTest {
    @Test
    void shouldPublishEvent(Scenario scenario) {
        scenario.publish(new CreateOrderCommand("customer-1", items))
            .andWaitForEventOfType(OrderCreatedEvent.class)
            .matching(e -> e.customerId().equals("customer-1"));
    }
}
```

---

## Go 구현 (internal 패키지)

```
internal/
├── order/
│   ├── api.go          # Public interface
│   ├── service.go      # Implementation
│   └── events.go
├── payment/
│   └── listener.go
└── shared/eventbus/
    └── eventbus.go
```

```go
// internal/order/api.go — Public API
type Service interface {
    CreateOrder(ctx context.Context, req CreateOrderRequest) (*OrderResult, error)
}
type OrderCreatedEvent struct {
    OrderID, CustomerID string
    TotalAmount         float64
}

// internal/order/service.go
func (s *service) CreateOrder(ctx context.Context, req CreateOrderRequest) (*OrderResult, error) {
    order := &Order{ID: uuid.New().String(), CustomerID: req.CustomerID, Status: "PENDING"}
    if err := s.repo.Save(ctx, order); err != nil {
        return nil, err
    }
    s.eventBus.Publish(ctx, OrderCreatedEvent{
        OrderID: order.ID, CustomerID: order.CustomerID,
        TotalAmount: order.CalculateTotal(),
    })
    return &OrderResult{OrderID: order.ID, Status: order.Status}, nil
}

// internal/shared/eventbus/eventbus.go
type EventBus interface {
    Publish(ctx context.Context, event interface{})
    Subscribe(eventType reflect.Type, handler EventHandler)
}
type inMemoryEventBus struct {
    mu       sync.RWMutex
    handlers map[reflect.Type][]EventHandler
}
func (eb *inMemoryEventBus) Publish(ctx context.Context, event interface{}) {
    eb.mu.RLock()
    handlers := eb.handlers[reflect.TypeOf(event)]
    eb.mu.RUnlock()
    for _, h := range handlers { go h(ctx, event) }
}
```

---

## 모듈 → 서비스 추출 전략

```
✅ 추출 시점:
  ├─ 팀 분리: 모듈 담당 팀이 2개+
  ├─ 독립 스케일링: 특정 모듈 10x 트래픽
  ├─ 배포 독립성: 주기 불일치
  └─ 장애 격리 필요

❌ 너무 이른 추출:
  ├─ "MSA가 트렌드라서"
  ├─ 모듈 경계 불명확
  └─ 인프라/운영 역량 부족

Strangler Fig 추출 단계:
  1. API Gateway 도입 → 모든 트래픽 라우팅
  2. 모듈을 독립 서비스로 구현
  3. 트래픽 점진 전환 (1% → 10% → 50% → 100%)
  4. Debezium CDC로 데이터 분리 → 레거시 스키마 제거
```

### Shopify 사례

```
2004~2016: Rails Monolith → 2017~2019: MSA (수백 개 서비스)
2020~현재: Modular Monolith + Selective MSA
결과: 개발 속도 30%↑, 인프라 비용 40%↓, 장애 복구 60%↓
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 모듈 간 직접 DB 접근 | 강결합, 추출 불가 | Public API/Event로만 통신 |
| Circular Dependency | 순환 의존 | Event 기반 의존성 역전 |
| God Module | 모든 로직 집중 | Bounded Context 재분리 |
| internal 직접 노출 | 경계 무의미 | api 패키지 인터페이스 |
| FK 제약 사용 | 모듈 간 결합 | 스키마 분리 + ID 참조 |
| 너무 이른 서비스 추출 | 복잡도 폭증 | 팀 성장 시점까지 대기 |
| 모듈 테스트 없음 | 위반 감지 불가 | ApplicationModules.verify() |

---

## 체크리스트

### 설계
- [ ] Bounded Context 기반 모듈 경계 식별
- [ ] Public API / Internal 분리
- [ ] 모듈 간 통신 Event 기반 설계
- [ ] Database per Module (스키마 분리)

### 구현
- [ ] Spring Modulith 또는 Go internal 패키지
- [ ] @ApplicationModuleListener Event 수신
- [ ] Transactional Event Publication (Outbox)

### 검증
- [ ] ApplicationModules.verify() 자동 검증
- [ ] @ApplicationModuleTest 모듈 테스트
- [ ] Circular Dependency 없음 확인

### 진화
- [ ] Strangler Fig 추출 전략 수립
- [ ] CDC 기반 데이터 동기화 준비
- [ ] 추출 시점 기준 정의

**관련 스킬**: `/msa-ddd`, `/msa-saga`, `/msa-event-driven`, `/msa-cqrs-eventsourcing`, `/strangler-fig-pattern`
