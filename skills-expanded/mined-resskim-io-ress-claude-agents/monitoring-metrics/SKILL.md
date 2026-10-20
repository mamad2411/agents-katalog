---
name: monitoring-metrics
category: observability
description: "Metrics Monitoring Patterns — Prometheus 스케일링, Thanos, VictoriaMetrics 설정 가이드 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Metrics Monitoring Patterns

Prometheus 스케일링, Thanos, VictoriaMetrics 설정 가이드

## Quick Reference (결정 트리)
```
클러스터 수?
    ├─ 1-5개 ────> Prometheus Federation (단순)
    ├─ 5-50개 ───> Thanos (S3 저장, 쿼리 통합)
    └─ 50+개 ────> VictoriaMetrics (고성능, 비용 효율)

일일 데이터 포인트?
    ├─ < 10M ────> 단일 Prometheus
    ├─ 10M-100M ─> Thanos
    └─ > 100M ───> VictoriaMetrics Cluster
```

---

## CRITICAL: 스케일링 솔루션 비교

| 항목 | Federation | Thanos | VictoriaMetrics |
|------|------------|--------|-----------------|
| 복잡도 | 낮음 | 중간 | 중간 |
| 장기 저장 | 제한적 | S3/GCS | 로컬/S3 |
| 쿼리 성능 | 단일 | 분산 | 고성능 |
| HA | 별도 구성 | 내장 | 내장 |
| 권장 규모 | 소규모 | 중-대 | 모든 규모 |

```
비용 우선 + 대규모 ────> VictoriaMetrics
AWS/GCP 네이티브 ─────> Thanos + S3/GCS
단순함 우선 ──────────> Prometheus Federation
```

---

## Thanos 설정

### 아키텍처
```
┌────────────┐    ┌────────────┐
│Prometheus  │    │Prometheus  │
│ + Sidecar  │    │ + Sidecar  │
└─────┬──────┘    └─────┬──────┘
      └────────┬────────┘
               ▼
        ┌────────────┐
        │  Thanos    │◄── Grafana
        │  Query     │
        └─────┬──────┘
              ▼
     ┌────────────────┐
     │ Store/Compact  │──> S3
     └────────────────┘
```

### Helm 배포
```yaml
thanos:
  query:
    enabled: true
    replicaCount: 2
    stores:
      - dnssrv+_grpc._tcp.prometheus-operated.monitoring.svc
  storegateway:
    enabled: true
    persistence:
      size: 8Gi
  compactor:
    enabled: true
    retentionResolutionRaw: 30d
    retentionResolution5m: 90d
    retentionResolution1h: 1y
  objstoreConfig: |-
    type: S3
    config:
      bucket: thanos-metrics
      region: ap-northeast-2
```

### Prometheus Sidecar
```yaml
prometheus:
  prometheusSpec:
    thanos:
      objectStorageConfig:
        name: thanos-objstore-secret
        key: objstore.yml
    externalLabels:
      cluster: production
```

---

## VictoriaMetrics 설정

### 클러스터 아키텍처
```
              ┌──────────┐
              │vmselect  │◄── Grafana
              └────┬─────┘
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│vmstorage│  │vmstorage│  │vmstorage│
└─────────┘  └─────────┘  └─────────┘
     ▲             ▲             ▲
     └─────────────┼─────────────┘
              ┌────┴─────┐
              │vminsert  │◄── Prometheus/OTel
              └──────────┘
```

### Helm 배포
```yaml
victoria-metrics-cluster:
  vmselect:
    replicaCount: 2
  vminsert:
    replicaCount: 2
    extraArgs:
      replicationFactor: 2
  vmstorage:
    replicaCount: 3
    persistentVolume:
      size: 50Gi
      storageClass: gp3
    retentionPeriod: 6  # 6개월
    extraArgs:
      dedup.minScrapeInterval: 15s
      downsampling.period: 30d:5m,90d:1h  # 비용 최적화
```

---

## OTel → Prometheus 메트릭

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  batch:
    timeout: 10s
  transform:
    metric_statements:
      - context: datapoint
        statements:
          - set(attributes["exported_job"], attributes["job"])

exporters:
  prometheusremotewrite:
    endpoint: http://vminsert:8480/insert/0/prometheus/api/v1/write

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors: [batch, transform]
      exporters: [prometheusremotewrite]
```

### OTel → Prometheus 레이블 매핑 스펙

**출처**: [opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/)

| OTel Resource Attribute | Prometheus Label | 규칙 |
|------------------------|-----------------|------|
| `service.name` | `job` | 기본 매핑 |
| `service.namespace` + `service.name` | `job` = `<namespace>/<service.name>` | namespace 있을 때 |
| `service.instance.id` | `instance` | 인스턴스 식별 |

**Attribute → Label 변환 규칙:**
- `.` → `_` (예: `http.method` → `http_method`)
- 특수문자 → `_` (영숫자, `_` 외 모든 문자)
- 숫자로 시작 시 `_` 접두어 추가

```
# 예: service.namespace=myapp, service.name=example-server
# → Prometheus job="myapp/example-server"

# ❌ Anti-pattern: service_name 레이블로 대시보드/rules 작성
sum by (service_name) (rate(http_requests_total[5m]))

# ✅ Correct: job 레이블 사용
sum by (job) (rate(http_requests_total[5m]))
```

### OTel 기본 히스토그램 버킷

OTel SDK 기본 explicit bucket boundaries (초 단위):
```
[0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
```

**주의**: `le="2.0"` 버킷 없음 → Apdex 계산 시 `le="2.5"` 사용

```promql
# Apdex (T=0.5s, OTel 버킷 기준)
(
  sum(rate(http_server_request_duration_seconds_bucket{le="0.5"}[5m]))
  + sum(rate(http_server_request_duration_seconds_bucket{le="2.5"}[5m]))
) / 2
/ sum(rate(http_server_request_duration_seconds_count[5m]))
```

커스텀 버킷이 필요하면 OTel SDK에서 View로 설정:
```yaml
# application.yml (Spring Boot OTel)
otel:
  metrics:
    views:
      - instrument_name: http.server.request.duration
        histogram:
          bucket_boundaries: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 2.5, 5.0, 10.0]
```

### Recording Rule 패턴

```yaml
# ❌ BAD: label 불일치 시 or vector(0)이 실패할 수 있음
- record: job:http_requests:error_rate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
    / sum(rate(http_requests_total[5m])) by (job)
    or vector(0)

# ✅ GOOD: on() 으로 label matching 무시 → universal fallback
- record: job:http_requests:error_rate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
    / sum(rate(http_requests_total[5m])) by (job)
    or on() vector(0)
```

**`or vector(0)` vs `or on() vector(0)` 차이:**
- `or vector(0)`: `or`는 label set이 동일한 시계열끼리 매칭. 좌변이 `{job="svc-a"}`이면 `vector(0)`은 label이 `{}`이므로 매칭 실패 → fallback 미적용
- `or on() vector(0)`: `on()`은 label matching을 명시적으로 빈 집합으로 제한 → label 불일치를 무시하고 universal fallback 적용
- **MSA 필수**: 서비스가 여러 개면 `by (job)` 결과에 여러 label set 존재 → `on()` 없이는 fallback이 특정 시계열에만 적용되거나 전혀 적용 안 됨
- 단일 서비스(모놀리식)에서는 양쪽 모두 동작하지만, MSA 전환 대비 **항상 `on()` 사용**

### histogram_quantile — `by (le)` 필수

```promql
# ✅ by (le) 필수 — histogram_quantile은 le 레이블이 있어야 버킷 경계를 인식
histogram_quantile(0.99, sum(rate(http_server_request_duration_seconds_bucket[5m])) by (le))

# ✅ 추가 label로 분리할 때도 le 반드시 포함
histogram_quantile(0.99, sum(rate(http_server_request_duration_seconds_bucket[5m])) by (le, job))

# ❌ by (le) 누락 → 결과 NaN (가장 흔한 실수)
histogram_quantile(0.99, sum(rate(http_server_request_duration_seconds_bucket[5m])))

# ❌ by에 le 없이 다른 label만 → NaN
histogram_quantile(0.99, sum(rate(http_server_request_duration_seconds_bucket[5m])) by (job))
```

### 나눗셈 0 보호 패턴

```promql
# ✅ 방법 1: > 0 필터 (분모가 0이면 시계열 자체를 제거 → NaN 대신 no data)
sum(rate(errors_total[5m])) / (sum(rate(requests_total[5m])) > 0)

# ✅ 방법 2: clamp_min (분모를 최소값으로 고정 → 0 대신 아주 작은 값)
sum(rate(errors_total[5m])) / clamp_min(sum(rate(requests_total[5m])), 0.001)

# ❌ 보호 없이 나눗셈 → 트래픽 없는 서비스에서 NaN/Inf 발생
sum(rate(errors_total[5m])) / sum(rate(requests_total[5m]))
```

**선택 기준:**
- `> 0`: 데이터 없는 서비스는 대시보드에서 완전히 사라짐 (recording rule 추천)
- `clamp_min`: 데이터 없는 서비스도 0으로 표시됨 (대시보드 패널 추천)

### OTel 메트릭 Suffix 규칙

OTel SDK가 Prometheus exporter/remote write로 내보낼 때 자동 변환되는 suffix 규칙.

| OTel 타입 | 단위 | Prometheus Suffix | 예시 |
|-----------|------|------------------|------|
| Counter | - | `_total` | `http_server_active_requests` → `http_server_active_requests_total` |
| Histogram | s (seconds) | `_seconds_bucket`, `_seconds_sum`, `_seconds_count` | `http.server.request.duration` → `http_server_request_duration_seconds_bucket` |
| Histogram | ms | `_milliseconds_bucket`, `_milliseconds_sum`, `_milliseconds_count` | 레거시 HikariCP 계측 |
| Gauge | By (bytes) | `_bytes` | `jvm.memory.used` → `jvm_memory_used_bytes` |
| Gauge | 1 (unitless) | `_ratio` | `jvm.cpu.recent_utilization` → `jvm_cpu_recent_utilization_ratio` |
| Gauge | {threads} | 단위 제거 | `jvm.thread.count` → `jvm_thread_count` |

**메트릭명 변환 규칙:**
- `.` → `_` (OTel `http.server.request.duration` → Prometheus `http_server_request_duration_seconds`)
- 단위가 메트릭명에 이미 포함되면 중복 추가 안 함
- `{custom}` 중괄호 단위는 제거됨

**레거시 Java agent 주의:**
- HikariCP 등 일부 계측: `_milliseconds` suffix (opt-in 전 레거시)
- Stable conventions 전환: `OTEL_SEMCONV_STABILITY_OPT_IN=database` 환경변수 설정
- 전환 후: `db.client.connection.create_time` (seconds 단위, `_seconds` suffix)

---

## Cardinality 관리

### CRITICAL: High Cardinality 방지
```
❌ BAD
http_requests_total{user_id="123", request_id="abc"}

✅ GOOD
http_requests_total{method="GET", status="200", path="/api/orders"}
```

### 레이블 가이드
| 레이블 | 권장 | 이유 |
|--------|------|------|
| user_id | ❌ | 무한 증가 |
| request_id | ❌ | 무한 증가 |
| status_code | ✅ | ~10개 값 |
| method | ✅ | ~5개 값 |

### Prometheus Relabeling
```yaml
metric_relabel_configs:
  - source_labels: [__name__]
    regex: 'go_.*'
    action: drop
  - source_labels: [path]
    regex: '/api/v1/users/[0-9]+'
    target_label: path
    replacement: '/api/v1/users/:id'
```

### 카디널리티 모니터링
```promql
# 상위 10개 high cardinality 메트릭
topk(10, count by (__name__) ({__name__=~".+"}))

# 레이블별 고유 값 수
count(count by (endpoint) (http_requests_total))
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| user_id 레이블 | 카디널리티 폭발 | 로그로 이동 |
| 100% 데이터 보관 | 스토리지 비용 | 다운샘플링 |
| 단일 Prometheus | SPOF | HA/Thanos |
| 모든 메트릭 수집 | 비용, 성능 | 필요한 것만 |
| 짧은 scrape interval | 부하 증가 | 15-30초 |

---

## 2026 트렌드: 통합 데이터베이스 스택

```
기존: Prometheus(메트릭) + Loki(로그) + Tempo(트레이스) 별도 운영
트렌드: 단일 스토리지 기반 통합

옵션:
├─ ClickHouse 기반 ──> Signoz, Qryn (오픈소스)
├─ Grafana Cloud ────> Managed LGTM Stack
└─ VictoriaMetrics ──> Logs/Traces 지원 확대 중
```

**장점**: 운영 복잡도 감소, 쿼리 언어 통일, 비용 절감

---

## 체크리스트

### 스케일링
- [ ] 규모에 맞는 솔루션 선택
- [ ] HA 구성 (2+ 레플리카)
- [ ] 장기 저장소 설정

### Cardinality
- [ ] 레이블 가이드라인 수립
- [ ] 모니터링 쿼리 설정
- [ ] Relabeling 설정

### 성능
- [ ] scrape interval 15-30s
- [ ] 다운샘플링 설정

**관련 skill**: `/observability`, `/observability-otel`, `/monitoring-grafana`
