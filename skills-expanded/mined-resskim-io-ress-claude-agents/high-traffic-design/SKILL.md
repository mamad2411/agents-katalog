---
name: high-traffic-design
category: msa
description: "대규모 트래픽 설계 가이드 — Backpressure, Rate Limiting, CDN Edge, Connection Pooling, Queue Load Leveling, Request Batching 패턴 기반 대규모 트래픽 아키텍처 가이드 Use when working with msa 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# 대규모 트래픽 설계 가이드

Backpressure, Rate Limiting, CDN Edge, Connection Pooling, Queue Load Leveling, Request Batching 패턴 기반 대규모 트래픽 아키텍처 가이드

## Quick Reference (결정 트리)

```
트래픽 규모별 전략
    ├─ ~1K/s ──────> 단일 인스턴스 + CDN + DB 인덱스
    ├─ ~10K/s ─────> HPA + Redis 캐시 + Connection Pool 튜닝
    ├─ ~100K/s ────> KEDA + Kafka 버퍼 + Rate Limiting + Read Replica
    └─ ~1M/s ──────> Edge Computing + Sharding + CQRS + Backpressure

병목 유형별 해결
    ├─ CPU bound ──────> HPA (CPU 기반), Pod Scale-Out
    ├─ I/O bound ──────> Connection Pooling, Async/Non-blocking
    ├─ DB bound ───────> Read Replica, Sharding, 캐싱
    ├─ Network bound ──> CDN, Edge Function, gRPC
    └─ Queue lag ──────> KEDA (lag 기반), Consumer 병렬화
```

---

## CRITICAL: 트래픽 규모별 아키텍처

| 항목 | 1K/s | 10K/s | 100K/s | 1M/s |
|------|------|-------|--------|------|
| **인프라** | 단일 서버+LB | HPA+멀티Pod | KEDA+Karpenter | Multi-Region+Edge |
| **캐싱** | Local Cache | Redis Cluster | Redis+CDN | Edge Cache+L1/L2 |
| **DB** | Single RDS | Read Replica | Sharding+CQRS | 분산DB (Vitess) |
| **메시징** | 동기 호출 | SQS/RabbitMQ | Kafka 파티션 | Kafka Multi-cluster |
| **Rate Limit** | 불필요 | 앱 Bucket4j | GW+Redis 분산 | Edge+Multi-layer |

---

## Backpressure 패턴

생산자가 소비자보다 빠르게 데이터를 생성할 때 속도 불일치를 제어하는 메커니즘.

| 전략 | 동작 | 적합한 상황 |
|------|------|-------------|
| **Drop** | 초과 요청 버림 | 실시간 스트리밍 (유실 허용) |
| **Buffer** | 큐에 임시 저장 | 일시적 스파이크 |
| **Throttle** | 생산 속도 제한 | API Gateway |
| **큐 깊이 기반** | 큐 크기로 스케일링 | Kafka Consumer, SQS Worker |

### Spring WebFlux Backpressure

```java
@Service
public class BackpressureService {
    public Flux<Event> processWithBackpressure(Flux<Event> source) {
        return source
            .onBackpressureBuffer(1024,           // 버퍼 최대 1024개
                dropped -> log.warn("버퍼 초과 drop: {}", dropped.getId()),
                BufferOverflowStrategy.DROP_LATEST)
            .publishOn(Schedulers.boundedElastic())
            .flatMap(this::processEvent, 16);     // 동시 처리 16개 제한
    }
    public Flux<Metric> realtimeMetrics(Flux<Metric> source) {
        return source
            .onBackpressureDrop(m -> log.debug("메트릭 drop: {}", m.getName()))
            .sample(Duration.ofMillis(100));       // 100ms 샘플링
    }
}
```

### Kafka Consumer Backpressure

```java
@Bean
public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerFactory(
        ConsumerFactory<String, String> cf) {
    var factory = new ConcurrentKafkaListenerContainerFactory<String, String>();
    factory.setConsumerFactory(cf);
    factory.setConcurrency(3);                                      // Consumer 수 제한
    factory.getContainerProperties().setIdleBetweenPolls(1000L);    // poll 간격
    factory.getContainerProperties().setAckMode(AckMode.MANUAL_IMMEDIATE);
    return factory;
}
```

### KEDA Kafka Lag 기반 스케일링

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-consumer-scaler
spec:
  scaleTargetRef:
    name: order-consumer
  minReplicaCount: 2
  maxReplicaCount: 50
  cooldownPeriod: 60
  pollingInterval: 10
  triggers:
    - type: kafka
      metadata:
        bootstrapServers: kafka-cluster:9092
        consumerGroup: order-consumer-group
        topic: orders
        lagThreshold: "100"
        activationLagThreshold: "10"
```

---

## Rate Limiting 심화

### 알고리즘 비교

| 알고리즘 | Burst | 정밀도 | 적합한 상황 |
|----------|-------|--------|-------------|
| **Fixed Window** | 경계 문제 | 낮음 | 단순 요청 수 제한 |
| **Sliding Window** | 양호 | 높음 | 공정 분배 필요 |
| **Leaky Bucket** | 평활화 | 보통 | 일정 처리율 보장 |
| **Token Bucket** | 허용 | 높음 | API Rate Limiting (범용) |

### Spring Boot + Bucket4j + Redis

```java
// 의존성: bucket4j-redis, redisson-spring-boot-starter
@Configuration
public class RateLimitConfig {
    @Bean
    public RedissonBasedProxyManager<String> proxyManager(RedissonClient redisson) {
        return RedissonBasedProxyManager.builderFor(redisson).build();
    }
    public BucketConfiguration defaultBucketConfig() {
        return BucketConfiguration.builder()
            .addLimit(Bandwidth.builder()
                .capacity(120)                                // 최대 토큰
                .refillGreedy(100, Duration.ofMinutes(1))     // 분당 100 리필
                .build())
            .build();
    }
}

@Component
public class RateLimitFilter extends OncePerRequestFilter {
    private final RedissonBasedProxyManager<String> proxyManager;
    private final RateLimitConfig config;
    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain) throws Exception {
        String key = resolveKey(request);
        Bucket bucket = proxyManager.builder()
            .build(key, () -> config.defaultBucketConfig());
        ConsumptionProbe probe = bucket.tryConsumeAndReturnRemaining(1);
        if (probe.isConsumed()) {
            response.setHeader("X-Rate-Limit-Remaining",
                String.valueOf(probe.getRemainingTokens()));
            chain.doFilter(request, response);
        } else {
            response.setStatus(429);
            response.setHeader("Retry-After",
                String.valueOf(probe.getNanosToWaitForRefill() / 1_000_000_000));
        }
    }
    private String resolveKey(HttpServletRequest req) {
        String apiKey = req.getHeader("X-API-Key");
        return apiKey != null ? "api:" + apiKey : "ip:" + req.getRemoteAddr();
    }
}
```

### Gateway vs 앱 레벨

| 구분 | Gateway 레벨 | 앱 레벨 |
|------|-------------|---------|
| **장점** | 전체 트래픽 일괄 제어, DDoS 방어 | 비즈니스 로직별 세밀한 제어 |
| **단점** | 세밀한 룰 어려움 | 분산 상태 관리 필요 (Redis) |
| **적용** | 글로벌 Rate Limit, IP 차단 | 사용자별/API별 차등 제한 |

---

## CDN & Edge Computing

### CDN 캐싱 전략

| 컨텐츠 유형 | TTL | 무효화 방식 |
|------------|-----|-----------|
| 정적 (JS/CSS/이미지) | 1년 (hash 버저닝) | 파일명 해시 변경 |
| API 응답 (읽기 전용) | 30s~5min | Purge API |
| 동적 (개인화) | 캐시 안함 | Edge Function |
| 미디어 (동영상) | 1주 | Version path |

### Cache-Control 헤더

```
Cache-Control: public, max-age=31536000, immutable           # 정적 자산 (해시 포함)
Cache-Control: public, max-age=30, stale-while-revalidate=60 # API (stale 허용)
Cache-Control: private, no-store, no-cache                   # 개인화
CDN-Cache-Control: public, max-age=300                       # CDN 전용 캐시
```

### Edge Function (Cloudflare Workers)

```javascript
// Edge A/B 테스트 + 캐시 분기
export default {
  async fetch(request) {
    const group = request.headers.get('cookie')?.includes('variant=b') ? 'b' : 'a';
    const origin = group === 'b'
      ? 'https://canary.example.com' : 'https://stable.example.com';
    const resp = await fetch(origin + new URL(request.url).pathname, {
      headers: request.headers, cf: { cacheTtl: 300, cacheEverything: true }
    });
    const modified = new Response(resp.body, resp);
    modified.headers.set('Vary', 'Cookie');
    return modified;
  }
};
```

---

## Connection Pooling

### HikariCP (Spring Boot)

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20        # 공식: (core*2)+spindles = (8*2)+1=17 -> 20
      minimum-idle: 5
      connection-timeout: 30000    # 대기 30초
      idle-timeout: 600000         # 유휴 10분
      max-lifetime: 1740000        # 수명 29분 (DB timeout보다 짧게)
      leak-detection-threshold: 60000
```

```
# 풀 사이즈 계산: connections = (core_count * 2) + effective_spindle_count
# 4코어 SSD: 9  |  8코어 SSD: 17  |  16코어 HDD*4: 36
# 과도한 커넥션 -> DB 컨텍스트 스위칭 증가 -> 오히려 처리량 감소
```

### Redis / HTTP Client Pool

```yaml
spring:
  data:
    redis:
      lettuce:
        pool: { max-active: 32, max-idle: 16, min-idle: 4, max-wait: 2000ms }
```

```java
@Bean
public RestClient restClient() {
    var cm = PoolingHttpClientConnectionManagerBuilder.create()
        .setMaxConnTotal(200).setMaxConnPerRoute(50)
        .setDefaultConnectionConfig(ConnectionConfig.custom()
            .setConnectTimeout(Timeout.ofSeconds(3))
            .setSocketTimeout(Timeout.ofSeconds(10)).build())
        .build();
    return RestClient.builder()
        .requestFactory(new HttpComponentsClientHttpRequestFactory(
            HttpClients.custom().setConnectionManager(cm)
                .evictIdleConnections(TimeValue.ofMinutes(5)).build()))
        .build();
}
```

---

## Queue-based Load Leveling

트래픽 스파이크를 큐가 흡수, Consumer가 일정 속도 처리. Producer/Consumer 독립 스케일링.

### SQS 버퍼 + KEDA 우선순위 스케일링

```java
@Service
public class OrderBufferService {
    private final SqsTemplate sqsTemplate;
    public OrderResponse submitOrder(OrderRequest request) {
        String msgId = sqsTemplate.send(to -> to
            .queue("order-processing-queue").payload(request)
            .header("priority", request.isPremium() ? "high" : "normal")
        ).messageId();
        return new OrderResponse(msgId, "ACCEPTED");
    }
    @SqsListener(value = "order-processing-queue",
                 maxConcurrentMessages = "10", maxMessagesPerPoll = "5")
    public void processOrder(@Payload OrderRequest request) {
        orderService.process(request);
    }
}
```

```yaml
# 우선순위별 큐 분리 + KEDA 차등 스케일링
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: high-priority-consumer
spec:
  scaleTargetRef: { name: order-consumer-high }
  minReplicaCount: 3
  maxReplicaCount: 100
  triggers:
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.ap-northeast-2.amazonaws.com/123/orders-high
        queueLength: "5"           # 메시지 5개당 Pod 1개
---
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: low-priority-consumer
spec:
  scaleTargetRef: { name: order-consumer-low }
  minReplicaCount: 0
  maxReplicaCount: 20
  triggers:
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.ap-northeast-2.amazonaws.com/123/orders-low
        queueLength: "50"          # 메시지 50개당 Pod 1개
```

---

## Request Batching & Coalescing

### DataLoader 패턴 (N+1 방지)

개별 요청을 모아 1개의 IN 쿼리로 실행. N개 SELECT 대신 배치 처리.

```java
@Controller
public class PostController {
    @SchemaMapping(typeName = "Post", field = "author")
    public CompletableFuture<User> author(Post post, DataLoader<Long, User> loader) {
        return loader.load(post.getAuthorId());
    }
    @Bean
    public BatchLoaderRegistration<Long, User> authorLoader(UserRepository repo) {
        return reg -> reg.forTypePair(Long.class, User.class)
            .registerMappedBatchLoader((ids, env) -> {
                Map<Long, User> map = repo.findAllById(ids).stream()
                    .collect(Collectors.toMap(User::getId, Function.identity()));
                return Mono.just(map);
            });
    }
}
```

### 배치 API

```java
@PostMapping("/api/batch")
public BatchResponse executeBatch(@RequestBody @Valid BatchRequest req) {
    if (req.getOperations().size() > 50)
        throw new BatchLimitExceededException("최대 50개");
    return new BatchResponse(req.getOperations().stream().map(op -> {
        try { return OperationResult.success(op.getId(),
                  dispatcher.dispatch(op.getMethod(), op.getParams()));
        } catch (Exception e) {
            return OperationResult.failure(op.getId(), e.getMessage()); }
    }).toList());
}
```

---

## Kubernetes 대규모 트래픽

### HPA + KEDA + Karpenter 조합

```
스케일업: 요청 증가 -> KEDA 감지 -> HPA Pod 증가
  -> Pod Pending -> Karpenter 노드 프로비저닝 (<60초) -> 스케줄링 완료
스케일다운: 트래픽 감소 -> KEDA cooldown -> HPA stabilization (300초)
  -> Pod 축소 -> Karpenter consolidation -> 노드 축소
```

### Pod Topology Spread + Anti-Affinity

```yaml
spec:
  replicas: 6
  template:
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector: { matchLabels: { app: api-server } }
        - maxSkew: 2
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: ScheduleAnyway
          labelSelector: { matchLabels: { app: api-server } }
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector: { matchLabels: { app: api-server } }
                topologyKey: kubernetes.io/hostname
```

### In-Place Pod Vertical Scaling (K8s 1.33+ Beta, 1.35 GA)

```yaml
spec:
  containers:
    - name: app
      resources:
        requests: { cpu: "500m", memory: "512Mi" }
        limits: { cpu: "2", memory: "2Gi" }
      resizePolicy:
        - resourceName: cpu
          restartPolicy: NotRequired       # CPU: 재시작 없이 변경
        - resourceName: memory
          restartPolicy: RestartContainer   # Memory: 재시작 필요
```

```bash
kubectl patch pod api-server --subresource=resize --patch \
  '{"spec":{"containers":[{"name":"app","resources":{"requests":{"cpu":"1"}}}]}}'
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Unbounded Queue | OOM Kill | 큐 크기 제한 + Drop 전략 |
| 커넥션 풀 과다 | DB 컨텍스트 스위칭 증가 | `(core*2)+1` 공식 기반 |
| CDN 미적용 정적 서빙 | Origin 부하 집중 | CDN + immutable 캐시 |
| 동기 호출 체이닝 | Latency 누적, 장애 전파 | Queue 비동기 + Circuit Breaker |
| 단일 Rate Limit | 내부 서비스 과부하 | Multi-layer (Edge+GW+App) |
| Retry without Backoff | Thundering Herd | Exponential Backoff + Jitter |
| 개별 DB 쿼리 반복 | N+1, 커넥션 고갈 | DataLoader 배치 + 캐싱 |
| Auto-scaling만 의존 | 스케일 지연 장애 | Predictive Scaling + Warm Pool |
| Cache Stampede 미방지 | TTL 만료 시 Origin 폭주 | stale-while-revalidate + Lock |

---

## 체크리스트

### 설계
- [ ] 예상 RPS 산정 및 규모별 아키텍처 선택
- [ ] 병목 식별 (CPU/I-O/DB/Network), Backpressure 전략 결정
- [ ] Rate Limiting 알고리즘 및 적용 레이어 결정

### 구현
- [ ] Connection Pool 사이즈 공식 기반 산정 (HikariCP, Redis, HTTP)
- [ ] CDN + Cache-Control 헤더 전략, Queue Load Leveling (SQS/Kafka)
- [ ] DataLoader 패턴으로 N+1 제거

### 인프라
- [ ] HPA + KEDA + Karpenter 오토스케일링 파이프라인
- [ ] Pod Topology Spread + PDB + graceful shutdown

### 운영
- [ ] Rate Limit 메트릭 (429 비율), Queue lag 대시보드
- [ ] Connection Pool 사용률 알림, Load Test 한계치 검증

---

## 참조 스킬

- `/k8s-autoscaling` - HPA, VPA, KEDA, Karpenter 상세
- `/msa-resilience` - Circuit Breaker, Retry, Bulkhead
- `/msa-event-driven` - 이벤트 기반 아키텍처, Saga
- `/database-sharding` - DB 샤딩 전략
- `/kafka-patterns` - Kafka Producer/Consumer 심화
- `/load-testing` - k6, Gatling 부하 테스트
- `/observability-otel` - OpenTelemetry 분산 추적
