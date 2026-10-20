---
name: observability-otel
category: observability
description: "OpenTelemetry Patterns — Spring Boot, Go를 위한 OpenTelemetry 설정 및 Collector 구성 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# OpenTelemetry Patterns

Spring Boot, Go를 위한 OpenTelemetry 설정 및 Collector 구성

## Quick Reference

```
OTel 설정
    │
    ├─ Spring Boot ────> spring-boot-starter-opentelemetry
    │
    ├─ Go ─────────────> go.opentelemetry.io/otel
    │
    └─ Collector ──────> Tempo(traces) + Loki(logs) + Prometheus(metrics)
```

---

## Spring Boot 설정

### 의존성

```groovy
// Spring Boot 4 (예정)
implementation 'org.springframework.boot:spring-boot-starter-opentelemetry'

// Spring Boot 3 — OTel Spring Boot Starter + Instrumentation BOM
implementation platform('io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom:2.25.0')
implementation 'io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter'

// HikariCP 수동 계측 (auto-instrumentation 미포함 시)
implementation 'io.opentelemetry.instrumentation:opentelemetry-hikaricp-3.0'
```

### 설정

```yaml
spring:
  application:
    name: order-service

otel:
  exporter:
    otlp:
      endpoint: http://otel-collector:4317
  resource:
    attributes:
      service.name: order-service
      service.version: 1.0.0
      deployment.environment: production

logging:
  pattern:
    console: "%d [%X{traceId}/%X{spanId}] %-5level %logger{36} - %msg%n"
```

### 자동 계측 (150+ 라이브러리)

- Spring MVC/WebFlux
- JDBC, JPA, Hibernate
- Kafka, RabbitMQ
- RestTemplate, WebClient
- Redis, MongoDB

---

## Go 설정

### 의존성

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
    "go.opentelemetry.io/otel/sdk/trace"
    "go.opentelemetry.io/otel/sdk/resource"
    semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
)
```

### 초기화

```go
func initTracer(ctx context.Context) (*trace.TracerProvider, error) {
    exporter, err := otlptracehttp.New(ctx,
        otlptracehttp.WithEndpoint("otel-collector:4318"),
        otlptracehttp.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    res := resource.NewWithAttributes(
        semconv.SchemaURL,
        semconv.ServiceName("order-service"),
        semconv.ServiceVersion("1.0.0"),
        semconv.DeploymentEnvironment("production"),
    )

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithResource(res),
        trace.WithSampler(trace.TraceIDRatioBased(0.1)), // 10% 샘플링
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}
```

### HTTP 미들웨어 (Gin)

```go
import "go.opentelemetry.io/contrib/instrumentation/github.com/gin-gonic/gin/otelgin"

r := gin.New()
r.Use(otelgin.Middleware("order-service"))
```

### 커스텀 Span

```go
func ProcessOrder(ctx context.Context, orderID string) error {
    tracer := otel.Tracer("order-service")
    ctx, span := tracer.Start(ctx, "ProcessOrder")
    defer span.End()

    span.SetAttributes(
        attribute.String("order.id", orderID),
        attribute.Int("order.items", 5),
    )

    // 중첩 span
    ctx, childSpan := tracer.Start(ctx, "ValidateStock")
    err := validateStock(ctx, orderID)
    childSpan.End()

    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return err
    }

    return nil
}
```

---

## Collector 설정

### Docker Compose (Grafana LGTM Stack)

```yaml
version: '3.8'
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.115.0  # 2024.12 기준
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP

  tempo:
    image: grafana/tempo:latest
    # 트레이스 저장

  loki:
    image: grafana/loki:latest
    # 로그 저장

  prometheus:
    image: prom/prometheus:latest
    # 메트릭 저장

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```

### Collector Config

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
  prometheus:
    endpoint: 0.0.0.0:8889

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/tempo]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [loki]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

---

## 샘플링 전략

| 환경 | 샘플링 비율 | 이유 |
|------|------------|------|
| 개발 | 100% | 전체 디버깅 |
| 스테이징 | 50% | 중간 수준 |
| 프로덕션 | 10-20% | 비용 최적화 |

```go
// 부모 기반 + 비율
trace.WithSampler(
    trace.ParentBased(trace.TraceIDRatioBased(0.1)),
)
```

---

## Collector 버전 관리

```yaml
# 권장: 특정 버전 명시 (latest 지양)
otel-collector:
  image: otel/opentelemetry-collector-contrib:0.115.0

# 업그레이드 가이드: https://github.com/open-telemetry/opentelemetry-collector/releases
# Breaking changes 확인 후 업그레이드
```

| 버전 | 주요 변경 |
|------|----------|
| 0.115+ | Zipkin exporter deprecated |
| 0.100+ | Log body 구조 변경 |

- **Grafana Agent EOL**: Alloy로 전환 필수. 마이그레이션 가이드: `/observability-otel-migration`

### Semantic Conventions 변경 추적

**CRITICAL**: OTel semantic conventions 버전에 따라 메트릭 이름이 변경됨. 업그레이드 전 changelog 필수 확인.

| 영역 | 레거시 | Stable | 전환 방법 |
|------|--------|--------|----------|
| DB 메트릭 | `db.client.connections.create_time` (ms) | `db.client.connection.create_time` (seconds) | `OTEL_SEMCONV_STABILITY_OPT_IN=database` |
| HikariCP | `_milliseconds` suffix | `_seconds` suffix | 위와 동일 |
| HTTP 메트릭 | `http.server.duration` | `http.server.request.duration` | `OTEL_SEMCONV_STABILITY_OPT_IN=http` |

```bash
# 환경변수로 stable conventions 전환
OTEL_SEMCONV_STABILITY_OPT_IN=database,http
```

### Stable HTTP Semantic Conventions (v1.23.0+)

OTel Java Agent 2.x는 **stable conventions** 기본 사용. 구버전(v1.20 이전) 속성명과 다름.

| 구버전 (unstable) | 현재 (stable) | 비고 |
|-------------------|--------------|------|
| `http.method` | `http.request.method` | |
| `http.status_code` | `http.response.status_code` | |
| `http.url` | `url.full` | client span |
| `http.target` | `url.path` + `url.query` | |
| `net.peer.name` | `server.address` | |
| `net.peer.port` | `server.port` | |
| `net.host.name` | `server.address` | |

**전환 환경변수**: `OTEL_SEMCONV_STABILITY_OPT_IN=http` (stable만) / `http/dup` (양쪽 동시)

### HikariCP 메트릭 레거시 suffix

| 상태 | 메트릭명 | 단위 |
|------|---------|------|
| 레거시 (현재) | `db_client_connections_create_time_milliseconds` | ms suffix |
| Stable (향후) | `db_client_connection_create_time_seconds` | seconds suffix |

- `OTEL_SEMCONV_STABILITY_OPT_IN=database` 설정 시 stable 메트릭으로 전환
- 전환 시 Grafana 대시보드 쿼리도 함께 변경 필요

### Resource Attributes → Prometheus 매핑 요약

```
┌─────────────────────────────────────────────┐
│ OTel Resource Attributes                     │
│   service.name = "example-server"              │
│   service.namespace = "myapp"                │
│   service.instance.id = "host1:8080"        │
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│ Prometheus Labels                            │
│   job = "myapp/example-server"                  │
│   instance = "host1:8080"                   │
└─────────────────────────────────────────────┘
```

- `service.namespace` 설정 시 `job` 레이블이 `namespace/name` 형식으로 변경됨
- 대시보드/alert rules에서 `job` 레이블 쿼리 시 이 형식 고려 필수
- Spring Boot `http.route` → OTel 기본 설정에서 자동 매핑 안 됨 (별도 설정 필요)

### OTel → Prometheus 메트릭명 변환 규칙

`.` → `_` 변환, 단위 suffix 자동 추가.

| OTel 메트릭 | Prometheus 메트릭 | 비고 |
|------------|------------------|------|
| `http.server.request.duration` (s) | `http_server_request_duration_seconds` | histogram |
| `jvm.memory.used` (By) | `jvm_memory_used_bytes` | |
| `jvm.gc.duration` (s) | `jvm_gc_duration_seconds` | histogram |
| `jvm.cpu.recent_utilization` (1) | `jvm_cpu_recent_utilization_ratio` | unitless → `_ratio` |
| `jvm.thread.count` ({threads}) | `jvm_thread_count` | |
| `db.client.connections.usage` ({conn}) | `db_client_connections_usage` | |
| `db.client.connections.wait_time` (ms) | `db_client_connections_wait_time_milliseconds` | 레거시 suffix |

### Span Attribute vs Resource Attribute 구분

TraceQL, Loki, Grafana에서 attribute를 참조할 때 scope를 구분해야 한다.

| Scope | 설명 | 예시 |
|-------|------|------|
| `resource` | 서비스 수준 (불변) | `resource.service.name`, `resource.deployment.environment.name` |
| `span` | 요청 수준 (매 요청마다 다름) | `span.http.route`, `span.db.system`, `span.http.response.status_code` |
| `intrinsic` | 내장 속성 (prefix 불필요) | `duration`, `status`, `kind`, `name` |

- Tempo TraceQL에서 `resource.service.name="example-server"` (scope prefix 필수)
- span attribute에 `resource.` prefix를 붙이면 결과 없음 (반대도 동일)
- intrinsic은 prefix 없이 사용: `duration > 500ms`, `status = error`

---

## Tempo v2 Scoped Tag API

Tempo v2 API (`/api/v2/search/tag/{name}/values`)는 **scoped tag name만 허용**한다.

```
GET /api/v2/search/tag/service.name/values          → 400 ❌ (unscoped)
GET /api/v2/search/tag/resource.service.name/values  → 200 ✅ (scoped)
```

유효한 scope: `resource`, `span`, `intrinsic`, `event`, `link`, `instrumentation`

- Grafana Tempo datasource의 `tags[].key`에도 scoped name 사용 필수
- Grafana 공식 문서 기본값(`service.name`)은 Tempo v2에서 400 에러 발생

---

## Alloy (Grafana Agent) 주의사항

### River 문법 (HCL-like)

Alloy는 표준 OTel Collector의 YAML config가 아닌 **River** 문법 사용. 호환 안 됨.

```river
// ✅ Alloy River 문법
otelcol.receiver.otlp "default" {
  grpc { endpoint = "0.0.0.0:4317" }
  http { endpoint = "0.0.0.0:4318" }
  output { metrics = [otelcol.processor.batch.default.input] }
}

// ❌ 표준 OTel Collector YAML → Alloy에서 동작 안 함
```

### loki.attribute.labels 미작동 (known issue)

```
# ❌ Alloy에서 미작동
loki.attribute.labels = ["service.name"]

# ✅ 대안: Loki native OTLP endpoint 사용
# otelcol.exporter.otlphttp "loki" → Loki의 /otlp endpoint
# Loki values의 otlp_config.index_label로 레이블 승격
```

- 해결: `otelcol.exporter.otlphttp "loki"` + Loki native OTLP endpoint (`/otlp`)
- Loki `otlp_config.resource_attributes.attributes_config` → `action: index_label`로 승격

---

## Declarative Configuration (1.0.0 Stable, 2026)

SDK 설정을 코드 대신 YAML 파일로 관리. 환경별 설정 분리에 유용.

```bash
# 환경변수로 설정 파일 지정
OTEL_EXPERIMENTAL_CONFIG_FILE=/etc/otel/sdk-config.yaml
```

```yaml
# sdk-config.yaml (file_format: "0.4")
file_format: "0.4"
resource:
  attributes:
    service.name: order-service
tracer_provider:
  processors:
    - batch:
        exporter:
          otlp:
            endpoint: http://collector:4317
            protocol: grpc
```

- 코드 변경 없이 환경별 샘플링/엔드포인트 전환 가능
- 상세 마이그레이션 가이드: `/observability-otel-migration`

## Zipkin Exporter Deprecation (2025-12)

Zipkin exporter가 OTel Collector에서 deprecated. 2026-12 제거 예정.
- 기존 Zipkin → OTLP exporter로 전환 필요
- Tempo는 Zipkin/OTLP 모두 수신 가능하므로 exporter만 변경
- 마이그레이션 가이드: `/observability-otel-migration`

## Profiling Signal (OTLP v1.3.0)

OTel에 네 번째 신호로 **Profiling** 추가. Pyroscope와 OTLP로 통합.
- Alloy `pyroscope.ebpf` + `pyroscope.java` 컴포넌트로 수집
- Span Profiles로 trace↔profile 연결
- 상세 가이드: `/observability-pyroscope`

---

## 버전 레퍼런스 (2026-03 기준)

| 컴포넌트 | 버전 | 비고 |
|----------|------|------|
| OTel Java SDK | 1.60.1 | 월별 릴리즈 |
| OTel Instrumentation BOM | 2.25.0 | stable / alpha 분리 |
| OTel Spring Boot Starter | 2.25.0 | Spring Boot 3.1+ |
| OTel HikariCP (`opentelemetry-hikaricp-3.0`) | 2.15.0-alpha | 패키지 `v3_0` 이동, API 유효 |
| Spring Boot 4 (예정) | - | 내장 `spring-boot-starter-opentelemetry` |

- **Instrumentation BOM**을 사용하면 OTel SDK 버전도 자동 정렬됨 (BOM이 SDK BOM을 포함)
- `-alpha` artifact는 API가 변경될 수 있으므로 버전 고정 필수

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| OTel resource 설정 후 Prometheus 레이블 검증 생략 | 대시보드/alert 쿼리 실패 | `up` 메트릭으로 `job`, `instance` 레이블 확인 |
| Semantic conventions 버전 무시하고 메트릭 이름 가정 | 메트릭 조회 실패 | changelog 확인 후 메트릭 이름 사용 |
| `service.namespace` 설정이 `job` 레이블에 미치는 영향 무시 | `job` 쿼리 실패 | `job="namespace/name"` 형식 인지 |
| OTel SDK 버전과 Spring Boot BOM 충돌 미확인 | 빌드 실패, 런타임 오류 | `dependency-management` 플러그인과 OTel BOM 우선순위 확인 |
| `latest` 태그로 Collector 배포 | 예기치 않은 breaking change | 특정 버전 명시 |
| OTel instrumentation BOM 없이 개별 버전 관리 | artifact 간 버전 불일치, 런타임 오류 | `opentelemetry-instrumentation-bom` platform 사용 |
| `-alpha` artifact를 버전 고정 없이 사용 | breaking change로 빌드/런타임 실패 | BOM 또는 명시적 버전 고정 |

---

## 체크리스트

### SDK 설정
- [ ] OTel SDK 의존성 추가
- [ ] 서비스 리소스 속성 설정
- [ ] 샘플링 비율 설정
- [ ] Prometheus 레이블 매핑 검증 (`up` 메트릭 확인)

### Collector
- [ ] Collector 배포 (버전 명시)
- [ ] 파이프라인 구성 (traces/logs/metrics)
- [ ] 백엔드 연결 (Tempo/Loki/Prometheus)

### Semantic Conventions
- [ ] 사용 중인 OTel SDK/agent 버전의 semconv 확인
- [ ] 레거시 → stable 전환 필요 여부 검토
- [ ] 대시보드/alert 쿼리가 실제 메트릭 이름과 일치하는지 확인

### 모니터링
- [ ] Grafana 대시보드 구성
- [ ] 알림 규칙 설정

**관련 skill**: `/monitoring-grafana`, `/monitoring-metrics`, `/monitoring-logs`
