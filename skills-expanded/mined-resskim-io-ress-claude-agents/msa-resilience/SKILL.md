---
name: msa-resilience
category: msa
description: "MSA 복원력 패턴 가이드 — Resilience4j 기반 Circuit Breaker, Bulkhead, Retry, Timeout, Fallback 패턴의 실전 구현과 조합 전략 Use when working with msa 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# MSA 복원력 패턴 가이드

Resilience4j 기반 Circuit Breaker, Bulkhead, Retry, Timeout, Fallback 패턴의 실전 구현과 조합 전략

## Quick Reference (결정 트리)

```
장애 유형별 패턴 선택
    ├─ 일시적 네트워크 오류 ──────────> Retry (Exponential Backoff + Jitter)
    ├─ 다운스트림 장기 장애 ──────────> Circuit Breaker + Fallback
    ├─ 느린 서비스 자원 고갈 ─────────> Bulkhead (Thread Pool 격리)
    ├─ 응답 지연 연쇄 장애 ──────────> Timeout (TimeLimiter)
    ├─ 장애 시 사용자 경험 유지 ──────> Fallback (캐시/기본값/대체)
    └─ 복합 장애 (실무 대부분) ───────> 패턴 조합 (조합 섹션 참조)

패턴 선택 기준
    ├─ "재시도하면 되나?" ── Yes ──> Retry
    ├─ "차단해야 하나?" ── Yes ──> Circuit Breaker
    ├─ "격리해야 하나?" ── Yes ──> Bulkhead
    └─ "시간 제한 필요?" ── Yes ──> Timeout + Fallback
```

---

## CRITICAL: 복원력 패턴 비교

| 패턴 | 목적 | 적용 범위 | 복잡도 | 주요 설정 |
|------|------|----------|-------|----------|
| Circuit Breaker | 장애 서비스 호출 차단 | 서비스 간 통신 | 중 | failureRateThreshold, waitDuration |
| Bulkhead | 자원 격리, 연쇄 장애 방지 | 스레드/커넥션 풀 | 중 | maxConcurrentCalls, maxWaitDuration |
| Retry | 일시적 실패 자동 재시도 | 개별 요청 | 낮음 | maxAttempts, waitDuration, backoff |
| Timeout | 응답 대기 시간 제한 | 개별 요청 | 낮음 | timeoutDuration |
| Fallback | 장애 시 대체 응답 | 비즈니스 로직 | 낮음 | fallbackMethod |
| Rate Limiter | 초과 요청 제한 | API 엔드포인트 | 낮음 | limitForPeriod |

---

## Circuit Breaker

### 상태 다이어그램

```
  ┌─ 성공 ──┐          실패율 초과
  │         ▼             │
  │   ┌──────────┐   ┌──────────┐
  └───│  CLOSED  │──►│   OPEN   │──── 실패 시 복귀
      └──────────┘   └──────────┘         ▲
           ▲              │ waitDuration  │
           └── 성공률 충족 ─┤               │
                    ┌──────────┐          │
                    │ HALF_OPEN│──────────┘
                    └──────────┘
```

- CLOSED: 정상, 요청 통과, 실패율 모니터링 / OPEN: 차단, Fail Fast / HALF_OPEN: 복구 확인

### Resilience4j 구현

```java
@Service
@Slf4j
public class OrderService {
    private final PaymentClient paymentClient;
    @CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
    public PaymentResponse processPayment(PaymentRequest request) {
        return paymentClient.charge(request);
    }
    private PaymentResponse paymentFallback(PaymentRequest request, Throwable t) {
        log.warn("결제 서비스 장애 - Fallback: {}", t.getMessage());
        return PaymentResponse.pending(request.getOrderId(), "결제 처리 지연 중");
    }
}
```

```yaml
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        registerHealthIndicator: true       # Actuator 헬스 체크
        slidingWindowType: COUNT_BASED      # 카운트 기반 윈도우
        slidingWindowSize: 10               # 최근 10개 요청 기준
        minimumNumberOfCalls: 5             # 최소 5개 후 판단
        failureRateThreshold: 50            # 50% 초과 시 OPEN
        waitDurationInOpenState: 30s        # OPEN 후 30초 대기
        permittedNumberOfCallsInHalfOpenState: 3
        slowCallRateThreshold: 80           # 느린 호출 80% 시 OPEN
        slowCallDurationThreshold: 3s
        recordExceptions:
          - java.io.IOException
          - java.util.concurrent.TimeoutException
          - org.springframework.web.client.HttpServerErrorException
        ignoreExceptions:
          - com.example.BusinessException
```

### Istio Outlier Detection vs 앱 레벨

| 구분 | Resilience4j (앱) | Istio (인프라) |
|------|-------------------|---------------|
| 위치 | 애플리케이션 코드 내부 | Envoy Sidecar Proxy |
| 제어 | 메서드 단위 세밀 제어 | 서비스/호스트 단위 |
| Fallback | 비즈니스 로직 Fallback | 다른 인스턴스 라우팅만 |
| 언어 | Java 전용 | Polyglot |
| 권장 | 비즈니스 로직 보호 | 인프라 장애 격리 |

---

## Bulkhead

### Thread Pool vs Semaphore

```
Semaphore (기본)              Thread Pool
├ 호출 스레드에서 실행          ├ 별도 스레드 풀에서 실행
├ 동시 호출 수만 제한           ├ 스레드 풀 + 큐 크기 제한
└ 오버헤드 적음, 동기 적합      └ 완전 격리, 비동기 적합
```

### Resilience4j Bulkhead 구현

```java
@Service
@Slf4j
public class ProductService {
    @Bulkhead(name = "inventoryService", fallbackMethod = "inventoryFallback")
    public InventoryResponse checkInventory(String productId) {
        return inventoryClient.getStock(productId);
    }
    @Bulkhead(name = "reviewService", type = Bulkhead.Type.THREADPOOL,
              fallbackMethod = "reviewFallback")
    public CompletableFuture<ReviewResponse> getReviews(String productId) {
        return CompletableFuture.supplyAsync(() -> reviewClient.getReviews(productId));
    }
    private InventoryResponse inventoryFallback(String productId, Throwable t) {
        return InventoryResponse.unknown(productId);
    }
    private CompletableFuture<ReviewResponse> reviewFallback(String productId, Throwable t) {
        return CompletableFuture.completedFuture(ReviewResponse.empty());
    }
}
```

```yaml
resilience4j:
  bulkhead:
    instances:
      inventoryService:
        maxConcurrentCalls: 20       # 최대 동시 호출
        maxWaitDuration: 500ms       # 초과 시 BulkheadFullException
      reviewService:
        maxConcurrentCalls: 10       # 비핵심은 더 적게
  thread-pool-bulkhead:
    instances:
      reviewService:
        maxThreadPoolSize: 10
        coreThreadPoolSize: 5
        queueCapacity: 20
```

---

## Retry

### Exponential Backoff + Jitter

```
시도1 → 실패 → 500ms(+jitter) → 시도2 → 실패 → 1s(+jitter) → 시도3 → 성공/Fallback
Jitter: Thundering Herd(동시 재시도 폭주) 방지 필수
```

### Resilience4j Retry 구현

```java
@Service
@Slf4j
public class NotificationService {
    @Retry(name = "emailService", fallbackMethod = "emailFallback")
    public void sendEmail(EmailRequest request) {
        emailClient.send(request);
    }
    private void emailFallback(EmailRequest request, Throwable t) {
        log.error("이메일 최종 실패 - DLQ 저장: {}", t.getMessage());
        deadLetterQueue.enqueue(request);
    }
}
```

```yaml
resilience4j:
  retry:
    instances:
      emailService:
        maxAttempts: 3
        waitDuration: 500ms
        enableExponentialBackoff: true
        exponentialBackoffMultiplier: 2     # 500ms → 1s → 2s
        enableRandomizedWait: true         # Jitter 활성화
        randomizedWaitFactor: 0.5
        retryExceptions:
          - java.io.IOException
          - java.net.SocketTimeoutException
          - org.springframework.web.client.HttpServerErrorException
        ignoreExceptions:
          - com.example.InvalidRequestException
          - com.example.DuplicateOrderException
```

### 재시도 가능/불가능 예외

| Retryable | Non-Retryable |
|-----------|---------------|
| IOException, SocketTimeout | IllegalArgumentException |
| 503 Service Unavailable | 400/401/403/404 |
| 429 Too Many Requests | 409 Conflict, 422 Validation |

### Idempotency 보장 (CRITICAL)

```
Retry 시 반드시 멱등성 보장 필요
  방법1: Idempotency Key → POST /payments (Header: Idempotency-Key: uuid)
  방법2: 자연 멱등 연산  → PUT /orders/123, DELETE /items/456
  방법3: DB 유니크 제약  → INSERT ... ON CONFLICT DO NOTHING
```

---

## Timeout

### 연쇄 타임아웃 방지

```
[Client 10s] → [API GW 8s] → [Order 5s] → [Payment 3s]
핵심: 상위 Timeout > 하위 Timeout (Fallback 처리 시간 확보)
```

### Resilience4j TimeLimiter 구현

```java
@Service
public class SearchService {
    @TimeLimiter(name = "searchService", fallbackMethod = "searchFallback")
    @CircuitBreaker(name = "searchService")
    public CompletableFuture<SearchResult> search(String query) {
        return CompletableFuture.supplyAsync(() -> searchClient.search(query));
    }
    private CompletableFuture<SearchResult> searchFallback(String query, Throwable t) {
        return CompletableFuture.completedFuture(cachedSearchResult(query));
    }
}
```

```yaml
resilience4j:
  timelimiter:
    instances:
      searchService:
        timeoutDuration: 3s
        cancelRunningFuture: true
      paymentService:
        timeoutDuration: 5s          # 결제는 여유 있게
```

---

## Fallback

### 전략 유형

| 전략 | 설명 | 예시 |
|------|------|------|
| 캐시 Fallback | 마지막 성공 응답 반환 | 상품 정보, 설정값 |
| 기본값 Fallback | 정적 기본값 반환 | 인기 상품 목록 |
| 대체 서비스 | 백업 서비스 호출 | 다른 리전/provider |
| 기능 축소 | 핵심 기능만 제공 | 상세 없이 목록만 |
| 빈 응답 | 빈 결과 반환 | 리뷰 0건 |

### 단계별 Fallback 구현

```java
@Service
@Slf4j
public class RecommendationService {
    private final RedisTemplate<String, List<Product>> cache;
    @CircuitBreaker(name = "recommendService", fallbackMethod = "recommendFallback")
    public List<Product> getRecommendations(String userId) {
        List<Product> result = recommendClient.getPersonalized(userId);
        cache.opsForValue().set("recommend:" + userId, result, Duration.ofHours(1));
        return result;
    }
    // 단계별: 캐시 → 인기 상품 → 빈 목록
    private List<Product> recommendFallback(String userId, Throwable t) {
        List<Product> cached = cache.opsForValue().get("recommend:" + userId);
        if (cached != null && !cached.isEmpty()) return cached;
        List<Product> popular = cache.opsForValue().get("recommend:popular");
        return (popular != null) ? popular : Collections.emptyList();
    }
}
```

---

## 패턴 조합 (CRITICAL)

### Resilience4j Aspect 적용 순서

```
요청 → Retry → CircuitBreaker → RateLimiter → TimeLimiter → Bulkhead → 실제 호출
(바깥)                                                         (안쪽)
```

### 어노테이션 조합 예시

```java
@Service
@Slf4j
public class PaymentGatewayService {
    @Retry(name = "paymentGw", fallbackMethod = "paymentFallback")
    @CircuitBreaker(name = "paymentGw")
    @TimeLimiter(name = "paymentGw")
    @Bulkhead(name = "paymentGw", type = Bulkhead.Type.THREADPOOL)
    public CompletableFuture<PaymentResult> processPayment(PaymentRequest req) {
        return CompletableFuture.supplyAsync(() -> paymentClient.charge(req));
    }
    private CompletableFuture<PaymentResult> paymentFallback(PaymentRequest req, Throwable t) {
        compensationService.scheduleRetry(req);
        return CompletableFuture.completedFuture(PaymentResult.deferred(req.getOrderId()));
    }
}
```

### 통합 application.yml

```yaml
resilience4j:
  retry:
    retryAspectOrder: 4                    # 높은 값 = 바깥쪽
    instances:
      paymentGw:
        maxAttempts: 2
        waitDuration: 1s
        enableExponentialBackoff: true
        exponentialBackoffMultiplier: 2
        retryExceptions:
          - java.io.IOException
          - java.util.concurrent.TimeoutException
  circuitbreaker:
    circuitBreakerAspectOrder: 3
    instances:
      paymentGw:
        registerHealthIndicator: true
        slidingWindowSize: 10
        failureRateThreshold: 50
        waitDurationInOpenState: 30s
        permittedNumberOfCallsInHalfOpenState: 3
        slowCallDurationThreshold: 4s
  timelimiter:
    timeLimiterAspectOrder: 2
    instances:
      paymentGw:
        timeoutDuration: 5s
        cancelRunningFuture: true
  thread-pool-bulkhead:
    bulkheadAspectOrder: 1
    instances:
      paymentGw:
        maxThreadPoolSize: 10
        coreThreadPoolSize: 5
        queueCapacity: 15

management:
  endpoints:
    web:
      exposure:
        include: health,metrics,circuitbreakers,retries,bulkheads
  health:
    circuitbreakers:
      enabled: true
```

### Gradle 의존성

```groovy
implementation 'io.github.resilience4j:resilience4j-spring-boot3:2.2.0'
implementation 'org.springframework.boot:spring-boot-starter-aop'
implementation 'org.springframework.boot:spring-boot-starter-actuator'
implementation 'io.micrometer:micrometer-registry-prometheus'
```

---

## Kubernetes + Istio 연동

### 이중 보호 전략

```
┌──────────────────────────────────────────────────┐
│ Istio (인프라): Outlier Detection + Connection Pool │
│   → 비정상 인스턴스 자동 제거, 언어 무관 일괄 적용    │
├──────────────────────────────────────────────────┤
│ Resilience4j (앱): Circuit Breaker + Fallback      │
│   → 비즈니스 로직 보호, 메서드 단위 세밀 제어         │
└──────────────────────────────────────────────────┘
```

### Istio DestinationRule

```yaml
apiVersion: networking.istio.io/v1
kind: DestinationRule
metadata:
  name: payment-service-resilience
  namespace: production
spec:
  host: payment-service.production.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp: { maxConnections: 100 }
      http: { http2MaxRequests: 1000, maxRequestsPerConnection: 10 }
    outlierDetection:
      consecutive5xxErrors: 5        # 5회 연속 시 제거
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 30         # 최대 30%만 제거
```

### Prometheus 모니터링

```promql
resilience4j_circuitbreaker_state{application="order-service"}           # CB 상태
rate(resilience4j_circuitbreaker_failure_rate[5m])                       # 실패율
resilience4j_bulkhead_available_concurrent_calls{application="order-service"}  # Bulkhead
increase(resilience4j_retry_calls_total[5m])                            # Retry 횟수
envoy_cluster_outlier_detection_ejections_active{cluster_name="payment-service"} # Istio
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 모든 예외에 Retry | 4xx도 재시도, 불필요한 부하 | retryExceptions로 대상 한정 |
| Retry 횟수 과다 (5+) | 느린 실패, 부하 가중 | maxAttempts 2~3 + CB |
| Jitter 없는 Retry | Thundering Herd | enableRandomizedWait: true |
| 전 서비스 동일 Timeout | 연쇄 타임아웃 | 상위 > 하위 원칙 |
| Bulkhead 없이 CB만 | 스레드 전체 고갈 | Bulkhead + CB 병행 |
| Fallback에서 외부 호출 | 이중 장애 | 캐시/기본값 로컬 처리 |
| CB 미모니터링 | OPEN 장기 방치 | Actuator + Alert |
| Retry 멱등성 미보장 | 중복 결제/주문 | Idempotency Key |
| slidingWindow 과소 | 오작동 | minimumNumberOfCalls 설정 |
| Thread Pool 과다 생성 | 리소스 낭비 | 중요도별 차등 배분 |

---

## 체크리스트

### 설계
- [ ] 서비스 간 의존성 맵 작성, 장애 유형 분류
- [ ] 패턴 선택 및 조합 전략 결정
- [ ] Timeout 체인 계산 (상위 > 하위), Fallback 전략 정의

### 구현
- [ ] Resilience4j 의존성 추가 (starter-aop 포함)
- [ ] application.yml 인스턴스별 설정
- [ ] Retry 예외 목록 정의, 멱등성 보장 구현
- [ ] Fallback 시그니처 확인 (동일 파라미터 + Throwable), Aspect 순서 설정

### 테스트
- [ ] CB 상태 전환, Bulkhead 제한, Retry Backoff, Timeout Fallback 동작 확인
- [ ] Chaos Engineering (Chaos Monkey / Litmus)

### 운영
- [ ] Actuator + Prometheus + Grafana Dashboard
- [ ] Alert 설정 (CB OPEN, Bulkhead 포화)
- [ ] Istio DestinationRule 적용, 프로덕션 Threshold 튜닝

---

## 참조 스킬

- `/istio-core` - Istio Service Mesh 핵심 개념 및 모드 선택
- `/k8s-traffic-istio` - Kubernetes Istio 트래픽 관리
- `/spring-cache` - Redis 캐싱 전략 (Fallback 캐시 구현 시 참조)
- `/observability` - 모니터링 및 관찰 가능성
- `/monitoring-metrics` - Prometheus/Grafana 메트릭 설정
