---
name: msa-observability
category: msa
description: "MSA 분산 추적 & 관측성 가이드 — Distributed Tracing, Correlation ID, Service Topology, Trace Context, Baggage Propagation Use when working with msa 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# MSA 분산 추적 & 관측성 가이드

Distributed Tracing, Correlation ID, Service Topology, Trace Context, Baggage Propagation

## Quick Reference (결정 트리)

```
관측성 도구 선택?
    |
    +-- Grafana 스택 사용 중 ---------> Grafana Tempo (S3/GCS 백엔드)
    |       +-- 메트릭 연동 ----------> Exemplar (Prometheus -> Tempo)
    |       +-- 토폴로지 맵 ----------> Service Graph (metrics-generator)
    |
    +-- 독립 실행 + 실시간 디버깅 ----> Jaeger v2 (OTel 네이티브)
    |       +-- K8s 운영 -------------> Jaeger Operator
    |       +-- 스토리지 -------------> Elasticsearch / Cassandra
    |
    +-- 경량 / 학습 목적 -------------> Zipkin
    +-- 하이브리드 ------------------> Jaeger(실시간) + Tempo(장기 저장)

샘플링 전략?
    |
    +-- 비용 우선 -------------------> Head-based (SDK, 10-50%)
    +-- 에러/지연 분석 우선 ---------> Tail-based (Collector)
    +-- 균형 -----------------------> Head(기본) + Tail(에러/고지연 보존)
    +-- 동적 제어 ------------------> Remote Sampling (Jaeger)

Context 전파 방식?
    |
    +-- HTTP 동기 호출 --------------> W3C Trace Context (자동)
    +-- gRPC -----------------------> Metadata 기반 자동 전파
    +-- Kafka / 메시지 큐 -----------> Header에 traceparent 주입
    +-- 비동기 (@Async) ------------> ContextExecutorService 래핑
```

---

## CRITICAL: 분산 추적 도구 비교

| 항목 | Jaeger v2 | Grafana Tempo | Zipkin |
|------|-----------|---------------|--------|
| **라이선스** | Apache 2.0 (CNCF Graduated) | AGPLv3 | Apache 2.0 |
| **스토리지** | ES, Cassandra, Kafka | S3, GCS, Azure Blob | ES, Cassandra, MySQL |
| **비용 (대규모)** | 높음 (인덱스 DB 필요) | 낮음 (Object Storage) | 중간 |
| **OTel 지원** | 네이티브 (v2 코어) | 네이티브 (OTLP 수신) | 호환 (Collector 경유) |
| **K8s 배포** | Jaeger Operator | Helm Chart | Helm Chart |
| **UI** | 내장 Jaeger UI | Grafana 통합 | 내장 Zipkin UI |
| **쿼리** | 빠름 (인덱스 기반) | TraceQL (ID 기반) | 보통 |
| **Service Graph** | 의존성 DAG | metrics-generator | 의존성 그래프 |
| **Exemplar** | 제한적 | Prometheus 네이티브 | 미지원 |
| **적합 대상** | 실시간 디버깅, 독립 운영 | Grafana 생태계, 비용 최적화 | 경량, PoC |

> Jaeger v2 (2024.11): OTel Collector를 코어로 재작성. v1은 2026.01 deprecated.

---

## Trace Context 전파 (CRITICAL)

### W3C Trace Context 표준

```
# traceparent: 버전-트레이스ID-부모스팬ID-플래그
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
             ^^                                                    ^^
          version=00                                          flags=01(sampled)
             |------- trace-id (32 hex) ---------|-- parent-id (16 hex) --|

# tracestate: 벤더별 확장 데이터 (최대 32개 키-값)
tracestate: vendor1=opaque-value,vendor2=another-value
```

- `traceparent` 파싱 실패 시 `tracestate`도 무시
- `tracestate` 파싱 실패는 `traceparent`에 영향 없음
- PII를 traceparent/tracestate에 포함 금지

### Spring Boot 자동 전파 (Micrometer Tracing)

```yaml
# application.yml - Spring Boot 3.x / 4.x
management:
  tracing:
    sampling:
      probability: 1.0               # 개발: 1.0, 운영: 0.1~0.5
    propagation:
      type: w3c                       # W3C Trace Context (기본값)
      produce: w3c                    # 발신 헤더 형식
      consume: w3c, b3                # 수신 헤더 형식 (다중 가능)
```

자동 전파 클라이언트 (auto-configured Builder 사용 시):
- `RestClient.Builder`, `RestTemplateBuilder` -> HTTP
- `WebClient.Builder` -> WebFlux 리액티브
- `KafkaTemplate` -> Kafka 메시지 헤더
- gRPC -> Metadata 기반 전파

### 수동 전파: 비동기 (@Async, CompletableFuture)

```java
import io.micrometer.context.ContextExecutorService;
import io.micrometer.context.ContextSnapshot;

@Configuration
public class AsyncTracingConfig implements AsyncConfigurer {
    @Autowired private ThreadPoolTaskExecutor taskExecutor;

    @Override
    public Executor getAsyncExecutor() {
        // Executor 래핑 -> Trace Context가 자식 스레드로 전파
        return ContextExecutorService.wrap(
            taskExecutor.getThreadPoolExecutor(),
            ContextSnapshot::captureAll
        );
    }
}

// CompletableFuture 직접 사용 시
Executor wrapped = ContextExecutorService.wrap(
    ForkJoinPool.commonPool(), ContextSnapshot::captureAll
);
CompletableFuture.supplyAsync(() -> orderService.process(orderId), wrapped);
```

핵심: 수동 생성한 RestTemplate/WebClient는 전파 안 됨 -> 반드시 Builder 사용

---

## Correlation ID

### Request ID vs Trace ID vs Span ID

| ID 유형 | 범위 | 생성 위치 | 용도 |
|---------|------|-----------|------|
| **Request ID** | Gateway -> 클라이언트 | Gateway/LB | 사용자 문의 추적 |
| **Trace ID** | 전체 분산 요청 | 첫 서비스 (SDK) | 서비스 간 추적 |
| **Span ID** | 단일 작업 단위 | 각 서비스 | 개별 작업 측정 |

### MDC + Correlation ID Filter (Java)

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class CorrelationIdFilter extends OncePerRequestFilter {
    private static final String HEADER = "X-Correlation-ID";

    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String cid = request.getHeader(HEADER);
        if (cid == null || cid.isBlank()) cid = UUID.randomUUID().toString();

        MDC.put("correlationId", cid);          // 로그에 자동 출력
        response.setHeader(HEADER, cid);
        try { chain.doFilter(request, response); }
        finally { MDC.remove("correlationId"); }
    }
}
```

```xml
<!-- logback-spring.xml: Correlation ID + Trace ID 포함 -->
<pattern>
  %d{ISO8601} [%thread] [cid=%X{correlationId}] [tid=%X{traceId}/%X{spanId}] %-5level %logger{36} - %msg%n
</pattern>
```

---

## Baggage Propagation

Baggage는 Trace Context와 함께 서비스 간 전파되는 Key-Value 데이터이다.
Span Attribute와 달리 **모든 하위 서비스로 자동 전달**된다.

사용 사례: `tenant-id`(멀티테넌트), `user-id`(사용자 추적), `region`(리전), `feature-flag`(A/B 테스트)

### Spring Boot 설정

```yaml
management:
  tracing:
    baggage:
      remote-fields:            # HTTP 헤더로 전파할 필드
        - tenant-id
        - user-id
        - region
      correlation:
        fields:                 # MDC에 추가 -> 로그에 포함
          - tenant-id
          - user-id
```

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final Tracer tracer;

    public Order createOrder(OrderRequest req) {
        // Baggage 설정 -> 이후 모든 하위 호출에 자동 전파
        try (var scope = tracer.createBaggageInScope("tenant-id", req.getTenantId())) {
            return processOrder(req);  // 하위 서비스 호출 시 HTTP 헤더로 자동 전파
        }
    }
}
```

주의사항:
- Baggage 크기 최소화 (총 8KB 이하 권장)
- 민감 정보(비밀번호, 토큰) 절대 포함 금지
- Span Attribute에 자동 추가 안 됨 (명시적 등록 필요)
- B3 전파에서는 Baggage 자동 전파 안 됨 -> W3C 권장

---

## Span Attributes & Events

### Span 이름 규칙

```
좋은 예:  GET /api/orders/{id}       # HTTP 메서드 + 경로 패턴
         OrderService.createOrder    # 클래스.메서드
         SELECT orders               # DB 작업 + 테이블
나쁜 예: GET /api/orders/12345       # 파라미터 포함 (카디널리티 폭발)
         handleRequest               # 너무 일반적
```

### 커스텀 Attribute + Event (Java)

```java
Span span = tracer.currentSpan();
if (span != null) {
    span.tag("payment.method", req.getMethod().name());     // Attribute
    span.tag("payment.amount", String.valueOf(req.getAmount()));
    span.event("payment.validation.started");                // Event

    try {
        PaymentResult result = gateway.charge(req);
        span.event("payment.completed");
        span.tag("payment.transaction_id", result.getTxId());
    } catch (PaymentException e) {
        span.error(e);                                       // 에러 기록
        span.tag("payment.error_code", e.getCode());
        throw e;
    }
}
```

### OpenTelemetry Semantic Conventions (주요)

| Attribute | 설명 | 예시 |
|-----------|------|------|
| `http.request.method` | HTTP 메서드 | `GET`, `POST` |
| `http.response.status_code` | 상태 코드 | `200`, `500` |
| `db.system` | DB 종류 | `postgresql`, `redis` |
| `db.operation.name` | 쿼리 타입 | `SELECT`, `INSERT` |
| `messaging.system` | 메시징 | `kafka`, `rabbitmq` |
| `messaging.destination.name` | 토픽/큐 | `order-events` |

---

## Service Topology & Dependency Map

### 자동 토폴로지 생성 (Grafana Tempo)

```yaml
# Tempo 설정 - metrics_generator 활성화
metrics_generator:
  processor:
    service_graphs:
      enabled: true
      dimensions: [http.method, http.status_code]
      peer_attributes: [peer.service, db.system, db.name]
    span_metrics:
      enabled: true
      dimensions: [http.method, http.route, http.status_code]
  storage:
    path: /var/tempo/wal
    remote_write:
      - url: http://prometheus:9090/api/v1/write
```

생성 메트릭:
- `traces_service_graph_request_total` -> 서비스 간 요청 수
- `traces_service_graph_request_failed_total` -> 실패 요청 수
- `traces_service_graph_request_server_seconds` -> 서버 응답 시간
- `traces_spanmetrics_calls_total` -> Span별 호출 수
- `traces_spanmetrics_latency_bucket` -> Span 지연 히스토그램

Grafana 설정: Tempo Data Source -> Service Graph 활성화 -> Prometheus 연결 -> Explore에서 시각화

---

## Exemplar (메트릭 -> 트레이스 연결)

Exemplar는 집계된 메트릭에서 **특정 트레이스로 드릴다운**할 수 있는 참조 데이터이다.
Grafana 차트의 녹색 다이아몬드 클릭 -> 해당 Trace 이동.

### Spring Boot + Prometheus 설정

```yaml
# application.yml
management:
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true   # 히스토그램 활성화 (Exemplar 필수)
      minimum-expected-value:
        http.server.requests: 1ms
      maximum-expected-value:
        http.server.requests: 10s
```

```yaml
# Prometheus scrape - OpenMetrics 형식 필수
scrape_configs:
  - job_name: 'spring-boot-app'
    metrics_path: '/actuator/prometheus'
    scrape_protocols: [OpenMetricsText1.0.0]
    static_configs:
      - targets: ['app:8080']
```

Grafana 설정: Prometheus Data Source -> Exemplars -> Internal link -> Tempo 선택, Label: `traceID`

---

## Kubernetes 배포

### Grafana Tempo (Helm)

```yaml
# tempo-values.yaml - Monolithic 모드 (소~중규모)
tempo:
  storage:
    trace:
      backend: s3
      s3:
        bucket: my-tempo-traces
        endpoint: s3.ap-northeast-2.amazonaws.com
        region: ap-northeast-2
        # IRSA 사용 시 access_key/secret_key 생략 가능
  retention: 720h                     # 30일 보존
  metricsGenerator:
    enabled: true
    remoteWriteUrl: http://prometheus:9090/api/v1/write
```

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install tempo grafana/tempo \
  --namespace observability --create-namespace \
  --values tempo-values.yaml
```

### OTel Collector -> Tempo 파이프라인

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc: { endpoint: "0.0.0.0:4317" }
      http: { endpoint: "0.0.0.0:4318" }

processors:
  batch: { timeout: 5s, send_batch_size: 1024 }
  tail_sampling:                      # 에러/고지연 100% 보존
    decision_wait: 10s
    policies:
      - name: error-policy
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: latency-policy
        type: latency
        latency: { threshold_ms: 2000 }
      - name: probabilistic-policy
        type: probabilistic
        probabilistic: { sampling_percentage: 10 }

exporters:
  otlp/tempo:
    endpoint: tempo:4317
    tls: { insecure: true }

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling]
      exporters: [otlp/tempo]
```

### 샘플링 전략: Head vs Tail

| 항목 | Head-based | Tail-based |
|------|-----------|------------|
| **결정 시점** | 요청 시작 시 (SDK) | 트레이스 완료 후 (Collector) |
| **설정 난이도** | 환경 변수 한 줄 | Collector 프로세서 설정 |
| **리소스** | 낮음 | 높음 (상태 유지 필요) |
| **정확도** | 무작위 (에러 유실 가능) | 높음 (조건부 보존) |
| **스케일링** | 불필요 | 2-tier Collector 필요 |

K8s 2-tier 구조 (Tail Sampling 스케일링):
```
DaemonSet Collector ──(load_balancing_exporter)──> Deployment Collector
 (각 노드)             trace_id 기반 라우팅          (tail_sampling 처리)
                                                         |
                                                         v
                                                    Tempo / Jaeger
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 수동 RestTemplate 생성 | Trace Context 전파 안 됨 | auto-configured Builder 사용 |
| Span 이름에 파라미터 포함 | 카디널리티 폭발 | 경로 패턴 사용 (`/orders/{id}`) |
| 모든 트레이스 100% 수집 | 스토리지 비용 폭증 | 샘플링 전략 적용 (10-50%) |
| Baggage에 민감 정보 저장 | 보안 취약점 (헤더 노출) | 민감 데이터는 별도 채널 전달 |
| 비동기 Executor 미래핑 | Trace 끊김 (orphan span) | ContextExecutorService 래핑 |
| Correlation ID 없는 로그 | 로그-트레이스 연결 불가 | MDC에 traceId/correlationId 등록 |
| Exemplar 미설정 | 메트릭->트레이스 드릴다운 불가 | 히스토그램 + OpenMetrics 활성화 |
| Tail Sampling 단일 Collector | 샘플링 부정확 | load_balancing_exporter 2-tier |
| Service Graph 미활성화 | 서비스 의존성 파악 불가 | metrics-generator 활성화 |
| 벤더 종속 전파 형식 | 멀티벤더 호환 불가 | W3C Trace Context 표준 사용 |

---

## 체크리스트

### 계측 (Instrumentation)
- [ ] OpenTelemetry SDK / Spring Boot Starter 설치
- [ ] W3C Trace Context 전파 설정 확인
- [ ] auto-configured Builder로 HTTP 클라이언트 생성
- [ ] 비동기 Executor에 ContextExecutorService 래핑
- [ ] Kafka 메시지에 Trace Context 전파 확인
- [ ] 의미 있는 Span 이름 + Semantic Conventions 적용
- [ ] Baggage 필드 설정 (tenant-id 등)
- [ ] MDC에 traceId, spanId, correlationId 등록

### 배포 (Deployment)
- [ ] Tempo 또는 Jaeger 백엔드 배포
- [ ] OTel Collector 파이프라인 구성
- [ ] 샘플링 전략 설정 (Head + Tail 하이브리드 권장)
- [ ] Prometheus Exemplar 수집 (OpenMetrics 형식)
- [ ] Grafana에서 Tempo + Service Graph 연결
- [ ] S3/GCS 스토리지 백엔드 구성

### 운영 (Operation)
- [ ] 샘플링 비율 모니터링 및 동적 조정
- [ ] Trace 보존 기간 설정 (비용 vs 분석)
- [ ] Service Graph로 토폴로지 정기 검토
- [ ] 메트릭 -> Exemplar -> 트레이스 드릴다운 검증
- [ ] Tail Sampling Collector 리소스 모니터링
- [ ] 에러 트레이스 알림 설정 (Grafana Alert)

---

## 참조 스킬
- `/observability-otel` - OpenTelemetry SDK 설정 (Spring Boot, Go)
- `/observability-otel-scale` - 대규모 트래픽 OTel Collector 스케일링
- `/monitoring-metrics` - Prometheus 메트릭 수집 및 PromQL
- `/monitoring-grafana` - Grafana 대시보드 구성
- `/kafka-patterns` - Kafka 메시징 패턴
