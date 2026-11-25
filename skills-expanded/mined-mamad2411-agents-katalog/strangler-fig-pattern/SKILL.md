---
name: strangler-fig-pattern
category: architecture
description: "Strangler Fig Pattern — 레거시 시스템을 점진적으로 현대화하는 안전한 마이그레이션 전략 Use when working with architecture 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Strangler Fig Pattern
레거시 시스템을 점진적으로 현대화하는 안전한 마이그레이션 전략

## Quick Reference: 레거시 현대화 전략 결정 트리

```
레거시 시스템 현대화 필요?
│
├─ 비즈니스 중단 가능? (다운타임 수용)
│  └─ YES → Big Bang Rewrite (비추천, 실패율 70%+)
│
├─ 레거시와 신규의 공존 기간 최소화?
│  ├─ 기능이 명확히 분리됨 → Strangler Fig Pattern
│  └─ 기능 간 의존성 높음 → Branch by Abstraction
│
├─ 레거시 유지하며 신규 추가?
│  └─ YES → Anti-Corruption Layer + Bridge Pattern
│
└─ 데이터 마이그레이션이 복잡?
   ├─ YES → Event-Driven CDC + Strangler Fig
   └─ NO → Proxy 기반 Strangler Fig
```

## CRITICAL: Strangler Fig Pattern 핵심 개념

### Martin Fowler의 열대 무화과나무 비유

```
숙주 나무 둘레를 감싸며 성장 → 점진적으로 숙주를 대체 → 최종적으로 숙주 사라짐
= Facade/Proxy로 레거시 감싸기 → 기능 단위로 새 서비스 전환 → 레거시 완전 제거
```

### Big Bang Rewrite vs Strangler Fig

| 항목 | Big Bang Rewrite | Strangler Fig |
|------|------------------|---------------|
| **전환 방식** | 전체 한 번에 교체 | 기능 단위 점진 전환 |
| **리스크** | 매우 높음 (실패율 70%+) | 낮음 (롤백 가능) |
| **다운타임** | 필수 (Cut-over 시점) | 제로 (동시 운영) |
| **비용** | 초기 투자 거대 | 점진적 투자 |
| **검증** | 전환 후 발견 | 단계별 검증 가능 |
| **롤백** | 거의 불가능 | 라우팅 변경으로 즉시 |

### 핵심 원칙

```
1. 점진성: 한 번에 하나의 기능만 전환
2. 공존성: 레거시와 신규가 동시 운영
3. 투명성: 사용자는 전환 인지 못함
4. 가역성: 문제 시 즉시 레거시로 롤백
5. 검증성: 각 단계에서 신규 시스템 검증
6. 완결성: 전환 완료 후 레거시 완전 제거
```

## CRITICAL: 구현 4단계

### Phase 1: Facade/Proxy 설치

```
Before: Client → Legacy System
After:  Client → [API Gateway/Proxy] → Legacy System
```

```yaml
# kong.yml
services:
  - name: legacy-service
    url: http://legacy-app:8080
    routes:
      - name: legacy-route
        paths: [/api]
  - name: new-service
    url: http://new-app:8080
    routes: []  # 아직 트래픽 없음
```

### Phase 2: 기능 단위로 새 서비스 구현

```
우선순위: 1. 비즈니스 가치 높은 기능 → 2. 기술 부채 심각 → 3. 의존성 낮은 독립 기능
예시: 1차 상품 조회 (Read-Only) → 2차 주문 생성 (Write) → 3차 결제 처리 (Critical)
```

### Phase 3: 트래픽 점진적 전환

```yaml
# Phase 3-1: Dark Launch (Shadow Traffic - 응답 무시, 비교만)
# Phase 3-2: Canary Release
routes:
  - name: product-read
    paths: ["/api/products"]
    plugins:
      - name: canary
        config:
          percentage: 10  # 10% → 50% → 100% 점진 전환
          upstream_fallback: true
```

### Phase 4: 레거시 제거

```
체크리스트:
  ✓ 신규 시스템 트래픽 100% 도달, 최소 2주간 안정 운영
  ✓ 레거시 DB 읽기 트래픽 0%, 데이터 동기화 완료
  ✓ 레거시 코드 아카이빙, 모니터링 대시보드 정리
```

## CRITICAL: API Gateway 라우팅 전략

### URL 패턴 기반 (NGINX)

```nginx
upstream legacy { server legacy-app:8080; }
upstream new_service { server new-app:8080; }

server {
    listen 80;
    location /api/products { proxy_pass http://new_service; }  # 전환 완료
    location /api/orders   { proxy_pass http://new_service; }  # 전환 완료
    location /              { proxy_pass http://legacy; }       # 나머지 레거시
}
```

### Header 기반 카나리 (Istio)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: product-service-vs
spec:
  hosts: [product.example.com]
  http:
    - match:
        - headers: { x-version: { exact: "v2" } }
      route:
        - destination: { host: new-product-service, subset: v2 }
    - route:
        - destination: { host: new-product-service, subset: v2 }
          weight: 20
        - destination: { host: legacy-product-service, subset: v1 }
          weight: 80
```

### Weighted Routing (점진적 비율 전환)

```
Week 1: legacy 95%, new 5%   (초기 검증)
Week 2: legacy 80%, new 20%  (확대)
Week 3: legacy 50%, new 50%  (동등)
Week 4: legacy 20%, new 80%  (대부분 전환)
Week 5: legacy 0%,  new 100% (완전 전환)
```

## CRITICAL: 데이터 동기화 전략

### 1. Kafka CDC (Debezium) - 추천

```yaml
# Debezium Connector for MySQL
name: legacy-product-connector
config:
  connector.class: io.debezium.connector.mysql.MySqlConnector
  database.hostname: legacy-db
  database.server.name: legacy
  table.include.list: legacy_db.products,legacy_db.orders
```

```java
// New Service CDC Consumer
@KafkaListener(topics = "cdc.products", groupId = "new-product-service")
public void handleProductChange(@Payload DebeziumChangeEvent<Product> event) {
    switch (event.getOperation()) {
        case CREATE, UPDATE -> productRepository.save(event.getAfter());
        case DELETE -> productRepository.deleteById(event.getBefore().getId());
    }
}
```

### 2. Outbox Pattern (Dual Write 안전 버전)

```java
@Transactional
public void createOrderWithOutbox(Order order) {
    legacyOrderRepo.save(order);
    outboxRepo.save(OutboxEvent.builder()
        .aggregateType("Order").aggregateId(order.getId())
        .eventType("OrderCreated").payload(toJson(order)).build());
    // CDC가 outbox 테이블 모니터링 → 신규 DB로 전파
}
```

### 3. Event-Driven 동기화

```java
// Legacy에서 이벤트 발행
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void onOrderCreated(OrderCreatedEvent event) {
    kafka.send("order-events", new OrderEvent(event.getOrder()));
}
```

## Spring Boot 구현

### Feature Toggle + Proxy

```java
@RestController @RequestMapping("/api")
public class LegacyProxyController {
    private final RestTemplate legacyClient;
    private final FeatureToggleService featureToggle;

    @GetMapping("/products/{id}")
    public ResponseEntity<Product> getProduct(@PathVariable Long id) {
        if (featureToggle.isEnabled("new-product-service", id))
            return newProductService.getProduct(id);
        return legacyClient.getForEntity("http://legacy:8080/api/products/" + id, Product.class);
    }
}

// Canary: userId 기반 점진적 활성화
@Service
public class FeatureToggleService {
    public boolean isEnabled(String feature, Long userId) {
        if (featureManager.isActive(MyFeatures.valueOf(feature.toUpperCase()))) {
            int percentage = configClient.getInteger("canary." + feature + ".percentage", 0);
            return (userId % 100) < percentage;
        }
        return false;
    }
}
```

### Shadow Traffic 검증

```java
@Service
public class ShadowTrafficService {
    @Async
    public void compareLegacyAndNew(Long productId) {
        var legacyFuture = CompletableFuture.supplyAsync(() -> legacyService.getProduct(productId));
        var newFuture = CompletableFuture.supplyAsync(() -> newService.getProduct(productId));

        CompletableFuture.allOf(legacyFuture, newFuture).thenAccept(v -> {
            boolean match = Objects.equals(legacyFuture.join(), newFuture.join());
            metrics.counter("shadow.comparison", "match", String.valueOf(match)).increment();
            if (!match) log.warn("Mismatch for product {}", productId);
        });
    }
}
```

### Rollback (Circuit Breaker)

```java
@Bean
public CircuitBreaker newServiceCircuitBreaker() {
    var config = CircuitBreakerConfig.custom()
        .failureRateThreshold(10).waitDurationInOpenState(Duration.ofMinutes(1))
        .slidingWindowSize(100).build();
    CircuitBreaker cb = CircuitBreaker.of("new-service", config);
    cb.getEventPublisher().onStateTransition(event -> {
        if (event.getStateTransition() == CLOSED_TO_OPEN) {
            log.error("Circuit opened! Rolling back to legacy");
            featureToggleService.disable("NEW_PRODUCT_SERVICE");
        }
    });
    return cb;
}
```

## 모니터링 & 검증

### SLO 기반 전환 판단

```yaml
slos:
  product-service-migration:
    objectives:
      - name: availability
        target: 99.9
        condition: "신규 서비스 에러율 < 0.1%"
      - name: latency
        target: 95
        percentile: p95
        threshold_ms: 200
      - name: consistency
        target: 99.99
        condition: "Shadow traffic 일치율 > 99.99%"
    rollout_gates:
      - percentage: 10
        requires: [availability, latency]
      - percentage: 50
        requires: [availability, latency, consistency]
      - percentage: 100
        requires: [availability, latency, consistency]
        duration: 14d
```

### 필수 모니터링 항목

```
✓ Shadow traffic 비교 결과 (일치율)
✓ 에러율 비교 (legacy vs new)
✓ 레이턴시 비교 (legacy vs new, p95)
✓ 데이터 동기화 지연
✓ Circuit breaker 상태
✓ 트래픽 분배 비율
```

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 영원한 공존 (기한 없음) | 이중 운영 비용, 기술 부채 누적 | 전환 로드맵 6-12개월, 데드라인 설정 |
| Facade 없이 직접 전환 | 롤백 불가, 단계적 검증 불가 | API Gateway를 통한 라우팅 |
| 데이터 정합성 무시 | 신규 DB에 데이터 없음 → 에러 | Fallback: new → legacy 순서 조회 |
| 너무 큰 단위로 전환 | 리스크 집중, 검증 어려움 | 기능 단위 2주 단위 전환 |
| 모니터링 부재 | 문제 감지 지연 | Shadow traffic + SLO 기반 게이트 |

## 체크리스트

### Phase 0: 계획
- [ ] 레거시 시스템 의존성 맵 작성
- [ ] 전환 우선순위 결정 (비즈니스 가치 x 기술 복잡도)
- [ ] 데이터 마이그레이션 전략 수립 (CDC/Event/Outbox)
- [ ] 롤백 시나리오 정의

### Phase 1: Facade 구축
- [ ] API Gateway 설치 (Kong/NGINX/Istio)
- [ ] 모든 트래픽을 Gateway로 라우팅
- [ ] 모니터링 대시보드 및 Circuit breaker 설정

### Phase 2: 신규 서비스 개발
- [ ] 첫 번째 기능 선정 (낮은 리스크, Read-Only 우선)
- [ ] 신규 서비스 구현 + 테스트
- [ ] 데이터 동기화 설정 (CDC/Event)
- [ ] Shadow traffic 설정

### Phase 3: 점진적 전환
- [ ] Dark launch → Shadow traffic 검증
- [ ] 결과 일치율 99.99% 이상 확인
- [ ] Canary 릴리스 (1% → 10% → 50% → 100%)
- [ ] 각 단계별 SLO 충족 확인
- [ ] 최소 2주간 100% 트래픽 안정 운영

### Phase 4: 레거시 제거
- [ ] 레거시 코드 아카이빙 + DB 백업
- [ ] 라우팅 규칙 단순화
- [ ] 회고 미팅 (교훈 정리)

**관련 스킬**: `/msa-event-driven`, `/kafka-connect-cdc`, `/deployment-strategies`, `/msa-resilience`, `/msa-api-gateway`
