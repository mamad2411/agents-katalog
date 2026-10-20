---
name: observability-otel-optimization
category: observability
description: "OpenTelemetry 비용 최적화 가이드 — Kafka 버퍼 아키텍처, 데이터 볼륨 절감, Collector 모니터링 & 알림 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# OpenTelemetry 비용 최적화 가이드

Kafka 버퍼 아키텍처, 데이터 볼륨 절감, Collector 모니터링 & 알림

---

## Kafka 버퍼 아키텍처

### 초대규모 트래픽용

```yaml
# Kafka exporter/receiver 설정
config:
  exporters:
    kafka:
      brokers:
        - kafka-0.kafka:9092
        - kafka-1.kafka:9092
        - kafka-2.kafka:9092
      topic: otel-traces
      encoding: otlp_proto
      producer:
        max_message_bytes: 10000000
        compression: zstd
        required_acks: 1  # 성능 우선
        flush_max_messages: 1000

  receivers:
    kafka:
      brokers:
        - kafka-0.kafka:9092
        - kafka-1.kafka:9092
        - kafka-2.kafka:9092
      topic: otel-traces
      encoding: otlp_proto
      group_id: otel-backend-consumer
      initial_offset: latest
```

### Kafka 토픽 설정 (CLI)

```bash
# 토픽 생성 (파티션 수 = Gateway 인스턴스 수의 배수)
kafka-topics.sh --create \
  --topic otel-traces \
  --partitions 30 \
  --replication-factor 3 \
  --config retention.ms=3600000 \
  --config compression.type=zstd \
  --config max.message.bytes=10485760
```

### Strimzi KafkaTopic CRD (Kubernetes 환경)

CLI 대신 Strimzi KafkaTopic CRD로 GitOps 관리.

```yaml
# observability.traces.v1
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: observability.traces.v1
  namespace: kafka
  labels:
    strimzi.io/cluster: goti-kafka
spec:
  partitions: 6            # Back Collector replicas 이하
  replicas: 3
  config:
    retention.ms: "3600000"          # 1시간 버퍼
    retention.bytes: "5368709120"    # 5GB/partition
    cleanup.policy: delete
    compression.type: zstd           # traces: 구조 복잡, zstd가 효율적
    max.message.bytes: "2097152"     # 2MB
    segment.bytes: "536870912"       # 512MB
    min.insync.replicas: "2"
---
# observability.logs.v1
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: observability.logs.v1
  namespace: kafka
  labels:
    strimzi.io/cluster: goti-kafka
spec:
  partitions: 12           # logs는 traces보다 고볼륨
  replicas: 3
  config:
    retention.ms: "7200000"          # 2시간 (Loki 장애 대비 여유)
    retention.bytes: "10737418240"   # 10GB/partition
    cleanup.policy: delete
    compression.type: lz4            # logs: 고처리량, lz4가 CPU 효율적
    max.message.bytes: "1048576"     # 1MB
    segment.bytes: "536870912"
    min.insync.replicas: "2"
```

#### 파티션 수 가이드

| 신호 | 권장 파티션 | 근거 |
|------|-----------|------|
| traces | 6 | Back Collector replica 수 이하 (idle 방지) |
| logs | 12 | 볼륨 높음, 병렬 소비 필요 |
| metrics | 불필요 | Mimir 직접 전송 (Kafka 미경유) |

**핵심**: partitions >= Back Collector replicas. 초과하면 일부 pod idle.

#### 압축 선택 기준

| | zstd | lz4 |
|---|---|---|
| 압축률 | **30-40% 더 작음** | 보통 |
| CPU (압축) | 높음 | **낮음** |
| CPU (해제) | 보통 | **매우 낮음** |
| 적합 | **traces** (복잡 구조) | **logs** (고처리량) |

#### Strimzi KafkaUser (prod SCRAM-SHA-512)

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaUser
metadata:
  name: otel-collector
  namespace: kafka
  labels:
    strimzi.io/cluster: goti-kafka
spec:
  authentication:
    type: scram-sha-512
  authorization:
    type: simple
    acls:
      - resource:
          type: topic
          name: observability.
          patternType: prefix    # observability.* 전체
        operations: [Write, Describe]
        host: "*"
      - resource:
          type: cluster
          name: kafka-cluster
          patternType: literal
        operations: [IdempotentWrite]
        host: "*"
---
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaUser
metadata:
  name: otel-backend-consumer
  namespace: kafka
  labels:
    strimzi.io/cluster: goti-kafka
spec:
  authentication:
    type: scram-sha-512
  authorization:
    type: simple
    acls:
      - resource:
          type: topic
          name: observability.
          patternType: prefix
        operations: [Read, Describe]
        host: "*"
      - resource:
          type: group
          name: otel-backend-
          patternType: prefix
        operations: [Read]
        host: "*"
```

Strimzi가 자동으로 Secret 생성 (`otel-collector`, `otel-backend-consumer`). OTel Collector pod에서 환경변수로 주입.

#### NetworkPolicy (monitoring → kafka)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-monitoring-to-kafka
  namespace: kafka
spec:
  podSelector:
    matchLabels:
      strimzi.io/cluster: goti-kafka
  policyTypes: [Ingress]
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: monitoring
      ports:
        - port: 9092    # dev plaintext
          protocol: TCP
        - port: 9093    # prod TLS+SASL
          protocol: TCP
```

---

## 비용 최적화

### 데이터 볼륨 절감

```yaml
processors:
  # 1. 속성 필터링
  attributes:
    actions:
      # 큰 속성 제거
      - key: http.request.body
        action: delete
      - key: http.response.body
        action: delete
      # SQL 쿼리 잘라내기
      - key: db.statement
        action: truncate
        truncate:
          limit: 500

  # 2. 스팬 필터링
  filter:
    traces:
      span:
        # 내부 통신 제외
        - 'attributes["http.url"] contains "internal"'
        # 짧은 스팬 제외
        - 'duration < 1ms'

  # 3. 메트릭 집계
  metricstransform:
    transforms:
      - include: http.server.request.duration
        action: aggregate
        aggregation_type: histogram
        # 상세 라벨 제거
        label_set: [service.name, http.method, http.status_code]
```

### 비용 대비 가치

```
트래픽: 100K RPS 가정

샘플링 없음 (100%):
  - 일일 트레이스: ~8.6B spans
  - 저장 비용: ~$10,000/월 (Tempo Cloud 기준)

5% 샘플링:
  - 일일 트레이스: ~430M spans
  - 저장 비용: ~$500/월
  - 절감: 95%

Tail-based (에러/지연 100%, 나머지 5%):
  - 일일 트레이스: ~500M spans
  - 중요 이벤트 100% 보존
  - 저장 비용: ~$600/월
  - 가치: 높음 (문제 분석 가능)
```

---

## 모니터링 및 알림

### Collector 자체 메트릭

```yaml
# Collector 메트릭 활성화
service:
  telemetry:
    metrics:
      address: 0.0.0.0:8888
      level: detailed
    logs:
      level: info

# ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: otel-collector
  namespace: observability
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: otel-collector
  endpoints:
    - port: metrics
      interval: 30s
```

### 주요 알림 규칙

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: otel-collector-alerts
spec:
  groups:
    - name: otel-collector
      rules:
        # 큐 포화
        - alert: OTelCollectorQueueFull
          expr: |
            otelcol_exporter_queue_size / otelcol_exporter_queue_capacity > 0.8
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "OTel Collector queue is filling up"

        # 드롭된 데이터
        - alert: OTelCollectorDataDropped
          expr: |
            rate(otelcol_processor_dropped_spans[5m]) > 0
          for: 2m
          labels:
            severity: critical
          annotations:
            summary: "OTel Collector is dropping spans"

        # 메모리 압박
        - alert: OTelCollectorHighMemory
          expr: |
            container_memory_usage_bytes{container="otel-collector"}
            / container_spec_memory_limit_bytes > 0.85
          for: 5m
          labels:
            severity: warning

        # Export 실패
        - alert: OTelCollectorExportFailure
          expr: |
            rate(otelcol_exporter_send_failed_spans[5m]) > 0
          for: 5m
          labels:
            severity: critical
```

---

---

## Alloy Known Issues

### `loki.attribute.labels` 미작동 (v1.8.x)

Alloy v1.8.x에서 `loki.attribute.labels` 설정이 동작하지 않는 known issue.
GitHub: #2064, #3216

**대체: `loki.process` 파이프라인**

```alloy
// ❌ 미작동 (v1.8.x)
otelcol.exporter.loki "default" {
  forward_to = [loki.write.default.receiver]
  // loki.attribute.labels = ["service_name", "severity"]  ← 무시됨
}

// ✅ 대체 (레거시): loki.process 파이프라인
loki.process "add_labels" {
  forward_to = [loki.write.default.receiver]

  stage.json {
    expressions = {
      service_name = "resources.service\\.name",
      severity     = "severity",
    }
  }

  stage.labels {
    values = {
      service_name = "",
      severity     = "",
    }
  }
}
```

### Loki Native OTLP Endpoint (권장 대안, 2026-03-13+)

`loki.process` 파이프라인 대신 Loki native OTLP endpoint 사용을 권장한다.
Alloy의 `otelcol.exporter.otlphttp`로 Loki의 `/otlp` 엔드포인트에 직접 전송하고,
Loki values의 `otlp_config`에서 `index_label`로 라벨 승격을 처리한다.

**Alloy 설정:**
```alloy
// loki.process 불필요 — Loki가 OTLP 네이티브로 처리
otelcol.exporter.otlphttp "loki" {
  client {
    endpoint = "http://loki:3100/otlp"
  }
}
```

**Loki values 설정:**
```yaml
loki:
  structuredConfig:
    limits_config:
      allow_structured_metadata: true
      otlp_config:
        resource_attributes:
          ignore_defaults: true
          attributes_config:
            - action: index_label
              attributes:
                - service.name       # → service_name label
                - service.namespace  # → service_namespace label
```

**장점:**
- `loki.process` JSON 파싱 불필요 → 성능 향상, 설정 단순화
- OTel structured metadata 직접 활용 → attribute 손실 없음
- `loki.attribute.labels` known issue 완전 회피

---

## HikariCP OTel 메트릭

### 레거시 `_milliseconds` suffix 주의

OTel Java agent의 HikariCP 계측은 레거시 semantic conventions 사용 시 `_milliseconds` suffix를 생성.

```
# 레거시 (기본)
db_client_connections_create_time_milliseconds_bucket
db_client_connections_create_time_milliseconds_sum

# Stable (opt-in 후)
db_client_connection_create_time_seconds_bucket
db_client_connection_create_time_seconds_sum
```

**대시보드 작성 시:**
- 레거시 사용 중이면 `_milliseconds_bucket` + 단위 변환 (`/ 1000`)
- Stable 전환: `OTEL_SEMCONV_STABILITY_OPT_IN=database` 환경변수

### BeanPostProcessor 빈 초기화 순서

OTel auto-configuration과 HikariCP DataSource 빈 초기화 순서 충돌은 **발견이 늦는** 대표적 문제.
앱은 정상 기동되지만 메트릭만 수집되지 않아, 대시보드 구축 시점에 발견된다.

#### 증상 식별

WARN 로그에서 다음 메시지가 출력되면 BPP 초기화 순서 문제:

```
Bean 'openTelemetry' of type [...] is not eligible for getting processed by all BeanPostProcessors
```

- 앱 기동 OK, 기능 정상 → 메트릭만 누락
- `db_client_connections_usage` 등 HikariCP 메트릭이 Prometheus에 없음

#### 3가지 핵심 문제와 해결

| 문제 | 원인 | 해결 |
|------|------|------|
| non-static `@Bean` | Configuration 클래스 인스턴스화 시 의존 빈 조기 초기화 | **`static`** 팩토리 메서드 |
| 직접 `OpenTelemetry` 주입 | BPP 생성 시점에 OTel 빈 강제 초기화 | **`ObjectProvider<OpenTelemetry>`** 지연 로딩 |
| `postProcessAfterInitialization` | OTel auto-config이 After 단계에서 DataSource를 프록시 래핑 → `instanceof HikariDataSource` 실패 | **`postProcessBeforeInitialization`** |

#### 검증된 패턴 (Spring Boot 3 + OTel)

```java
@Bean
static BeanPostProcessor hikariMetricsPostProcessor(
    ObjectProvider<OpenTelemetry> openTelemetryProvider) {
    return new BeanPostProcessor() {
        @Override
        public Object postProcessBeforeInitialization(Object bean, String beanName) {
            if (bean instanceof HikariDataSource ds) {
                OpenTelemetry otel = openTelemetryProvider.getIfAvailable();
                if (otel != null) {
                    HikariTelemetry telemetry = HikariTelemetry.create(otel);
                    ds.setMetricsTrackerFactory(telemetry.createMetricsTrackerFactory());
                }
            }
            return bean;
        }
    };
}
```

**3가지가 모두 필요한 이유:**
- `static` 없으면 → Configuration 클래스의 다른 빈이 먼저 초기화됨
- `ObjectProvider` 없으면 → BPP 등록 시 OTel 빈이 강제 생성되어 다른 BPP를 놓침
- `Before` 대신 `After` 쓰면 → OTel auto-config의 DataSource 프록시가 원본을 감싸서 타입 체크 실패

#### 검증 방법

Prometheus에서 다음 메트릭이 수집되는지 확인:
```promql
db_client_connections_usage{state="used"}
db_client_connections_max
db_client_connections_create_time_milliseconds_bucket
```

#### Anti-patterns

- ❌ BPP에서 `OpenTelemetry` 직접 주입 (non-static + eager initialization)
- ❌ `postProcessAfterInitialization`에서 DataSource 타입 체크 (프록시 래핑 후 instanceof 실패)
- ❌ `@DependsOn("openTelemetry")` 로 순서 강제 시도 (BPP 생명주기와 무관)

---

## Sources

- [OTel Collector Scaling](https://opentelemetry.io/docs/collector/scaling/)
- [Tail-based Sampling](https://opentelemetry.io/docs/collector/configuration/#tail-sampling-processor)
- [OTel Collector Helm Chart](https://github.com/open-telemetry/opentelemetry-helm-charts)
- [Grafana Tempo Scaling](https://grafana.com/docs/tempo/latest/operations/scaling/)

## 참조 스킬

- `/observability-otel-scale` - 대규모 트래픽 OTel 아키텍처, 샘플링 전략
- `/observability-otel` - OTel 기본 설정
- `/monitoring-grafana` - Grafana 모니터링
- `/finops` - FinOps 기초
