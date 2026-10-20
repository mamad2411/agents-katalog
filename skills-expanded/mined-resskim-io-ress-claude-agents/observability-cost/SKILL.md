---
name: observability-cost
category: observability
description: "Observability Cost Management — Metrics, Traces, Logs, Profiles 스택 전반의 비용 최적화 전략과 실행 가이드 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Observability Cost Management

Metrics, Traces, Logs, Profiles 스택 전반의 비용 최적화 전략과 실행 가이드

---

## Quick Reference (비용 드라이버 결정 트리)

```
비용이 급증한 신호 유형?
    ├─ Metrics ──────> 카디널리티 확인 (고유 시계열 수)
    │   ├─ label 폭발 (user_id, request_id) → relabel_configs로 드롭
    │   ├─ 미사용 메트릭 → keep 화이트리스트
    │   └─ 히스토그램 버킷 과다 → Native Histogram 전환
    │
    ├─ Traces ───────> 스팬 볼륨 확인 (spans/sec)
    │   ├─ 100% 샘플링 → tail-based sampling 적용
    │   ├─ 대용량 속성 (SQL body, HTTP body) → 속성 필터링
    │   └─ health check 스팬 → 수집 제외
    │
    ├─ Logs ─────────> 수집량 확인 (GB/day)
    │   ├─ DEBUG 레벨 과다 → 프로덕션 INFO 이상만
    │   ├─ 중복 로그 → rate limiting
    │   └─ label 카디널리티 → 인덱스 라벨 최소화
    │
    └─ Profiles ─────> 수집 빈도 확인 (samples/sec)
        ├─ 상시 수집 → on-demand 또는 주기적 수집
        └─ SDK 오버헤드 → eBPF 전환 검토
```

---

## CRITICAL: 4대 비용 드라이버

### 월간 비용 공식

```
월간_비용 = 수집_속도(GB/day) × 30일 × 저장소_단가($/GB) + 쿼리_비용
```

| 신호 유형 | 주요 비용 드라이버 | 측정 지표 | 위험 임계값 |
|----------|-------------------|----------|------------|
| Metrics | 카디널리티 (고유 시계열 수) | `prometheus_tsdb_head_series` | > 5M series |
| Traces | 스팬 볼륨 (spans/sec) | `otelcol_receiver_accepted_spans` | > 100K spans/sec |
| Logs | 수집량 (GB/day) | `loki_distributor_bytes_received_total` | > 100 GB/day |
| Profiles | 수집 빈도 (samples/sec) | `pyroscope_ingester_ingested_sample_count` | > 10K samples/sec |

### 비용 비중 (일반적인 분포)

```
Logs     ████████████████████  50-60%  ← 가장 큰 비용
Metrics  ████████              20-25%
Traces   ██████                15-20%
Profiles ██                     5-10%
```

> 로그가 전체 비용의 절반 이상을 차지하는 경우가 대부분이므로, 로그 최적화부터 시작하라.

---

## Metrics 비용 최적화

### 카디널리티 분석 쿼리

```promql
# 시계열 수 상위 20개 메트릭
topk(20, count by (__name__) ({__name__=~".+"}))

# 시계열 수 상위 10개 job
topk(10, count by (job) ({__name__=~".+"}))

# TSDB 상태 확인 (Prometheus API)
# GET /api/v1/status/tsdb
# → seriesCountByMetricName, labelValueCountByLabelName 확인
```

### Recording Rules로 쿼리 비용 절감

대시보드에서 반복 실행되는 고비용 쿼리는 recording rule로 사전 집계한다.

```yaml
groups:
  - name: cost-optimized-recordings
    interval: 30s
    rules:
      # 원본: histogram_quantile(0.99, sum(rate(http_server_requests_seconds_bucket[5m])) by (le, service))
      # → 매번 모든 bucket을 계산하는 대신 사전 집계
      - record: service:http_request_duration_seconds:p99
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_server_requests_seconds_bucket[5m])) by (le, service)
          )

      # 에러율 사전 집계 (여러 대시보드에서 재사용)
      - record: service:http_error_rate:5m
        expr: |
          sum(rate(http_server_requests_seconds_count{http_response_status_code=~"5.."}[5m])) by (service)
          /
          (sum(rate(http_server_requests_seconds_count[5m])) by (service) > 0)
```

### relabel_configs로 불필요한 메트릭/라벨 제거

```yaml
# scrape_configs 내부 — 수집 단계에서 제거
scrape_configs:
  - job_name: app
    relabel_configs:
      # 특정 엔드포인트의 고카디널리티 라벨 제거
      - source_labels: [__name__]
        regex: "go_gc_.*"
        action: drop

    metric_relabel_configs:
      # 화이트리스트 방식 — 필요한 메트릭만 유지
      - source_labels: [__name__]
        regex: "(http_server_requests_seconds_.+|process_cpu_seconds_total|jvm_memory_.+)"
        action: keep

      # 고카디널리티 라벨 제거
      - regex: "instance|pod"
        action: labeldrop

      # unbounded 라벨 값 제거 (user_id, trace_id 등)
      - source_labels: [user_id]
        target_label: user_id
        replacement: ""
```

### 수집 시점 집계 (Aggregation at Collection)

```yaml
# OTel Collector — 수집 시점에서 집계하여 카디널리티 감소
processors:
  metricstransform:
    transforms:
      # pod 라벨을 제거하고 service 단위로 집계
      - include: http_server_requests_seconds_bucket
        action: update
        operations:
          - action: aggregate_labels
            label_set: [service, http_request_method, http_response_status_code, le]
            aggregation_type: sum
```

---

## Traces 비용 최적화

> 샘플링 전략 상세는 `/observability-otel-optimization` 참조.
> 여기서는 비용 관점의 핵심 전략만 다룬다.

### Retention 티어링 (Hot/Warm/Cold)

| 티어 | 보존 기간 | 저장소 | 용도 |
|------|----------|--------|------|
| Hot | 1-3일 | SSD (Tempo local) | 실시간 디버깅, 최근 트레이스 조회 |
| Warm | 7-14일 | S3 Standard | 이슈 분석, 트렌드 확인 |
| Cold | 30-90일 | S3 Glacier / IA | 컴플라이언스, 감사 |

```yaml
# Tempo compactor 설정 — retention 티어링
compactor:
  compaction:
    block_retention: 72h          # Hot: 로컬 72시간
  ring:
    kvstore:
      store: memberlist

storage:
  trace:
    backend: s3
    s3:
      bucket: traces-warm
    blocklist_poll: 5m
    # Cold 티어는 S3 Lifecycle Policy로 관리
    # S3 → Glacier 전환: 14일 후 자동
```

### 스팬 속성 필터링

```yaml
# OTel Collector — 대용량 속성 제거/truncate
processors:
  attributes:
    actions:
      - key: http.request.body
        action: delete
      - key: http.response.body
        action: delete
      - key: db.statement
        action: truncate
        truncate:
          limit: 500            # SQL 쿼리 500자로 제한
      - key: exception.stacktrace
        action: truncate
        truncate:
          limit: 2000

  # Health check, readiness probe 스팬 제외
  filter:
    traces:
      span:
        - 'attributes["http.route"] == "/healthz"'
        - 'attributes["http.route"] == "/readyz"'
        - 'attributes["http.route"] == "/livez"'
        - 'attributes["http.user_agent"] matches "kube-probe/.*"'
```

### 비용 절감 효과 예시

```
Before: 100% 샘플링, 모든 속성 포함 → 50GB/day
After:
  - tail-based sampling (에러/느린 요청만 100%) → -70%
  - 속성 필터링 (body, stacktrace 제거)       → -15%
  - health check 제외                         → -5%
  결과: 50GB → 5GB/day (90% 절감)
```

---

## Logs 비용 최적화

### 로그 레벨 최적화

```yaml
# 프로덕션 환경 — INFO 이상만 수집
# application.yml (Spring Boot)
logging:
  level:
    root: INFO
    com.myapp: INFO
    org.hibernate.SQL: WARN       # SQL 로그 비활성화
    org.springframework: WARN

# OTel Collector — 로그 필터링
processors:
  filter:
    logs:
      log_record:
        - 'severity_number < SEVERITY_NUMBER_INFO'  # DEBUG, TRACE 제거
```

### 구조화 로깅으로 효율적 쿼리

```
# BAD: 비구조화 → 전체 텍스트 검색 필요 (느리고 비쌈)
2024-01-15 10:30:00 ERROR Payment failed for user 12345, amount 50000

# GOOD: 구조화 → 인덱스 라벨로 빠른 필터링
{"level":"ERROR","msg":"payment failed","userId":"12345","amount":50000}
```

### Loki 라벨 카디널리티 관리

```yaml
# Loki — 인덱스 라벨은 최소한으로 (5개 이하 권장)
# 낮은 카디널리티 라벨만 인덱스로 사용
limits_config:
  max_label_names_per_series: 15
  max_label_value_length: 2048

# GOOD: 인덱스 라벨 = namespace, service_name, detected_level
# BAD:  인덱스 라벨에 user_id, trace_id, request_id 포함 (카디널리티 폭발)
```

### 스트림별 Retention 정책

```yaml
# Loki — 중요도별 보존 기간 차등 적용
limits_config:
  retention_period: 168h          # 기본 7일

  retention_stream:
    - selector: '{detected_level="ERROR"}'
      priority: 1
      period: 720h                # 에러 로그: 30일
    - selector: '{detected_level="DEBUG"}'
      priority: 2
      period: 24h                 # 디버그 로그: 1일 (수집된 경우)
    - selector: '{namespace="kube-system"}'
      priority: 3
      period: 72h                 # 시스템 로그: 3일
```

---

## Profiles 비용 최적화

### 수집 빈도 튜닝

| 시나리오 | 수집 빈도 | CPU 오버헤드 | 용도 |
|----------|----------|-------------|------|
| 상시 프로파일링 | 10초 간격 | 2-5% | 프로덕션 상시 모니터링 |
| 주기적 프로파일링 | 60초 간격 | < 1% | 비용 절감, 트렌드 분석 |
| On-demand | 수동 트리거 | 0% (비활동 시) | 이슈 발생 시만 |

```yaml
# Pyroscope — 수집 빈도 조정
pyroscope:
  scrape_configs:
    - job_name: app
      scrape_interval: 60s        # 기본 10s → 60s로 변경 (비용 6배 절감)
      enabled_profiles:
        - cpu                     # 필요한 프로파일 타입만 활성화
        - memory
        # - goroutine            # 불필요 시 비활성화
        # - mutex
```

### eBPF vs SDK 오버헤드 비교

| 항목 | eBPF (Parca/Pyroscope) | SDK (pprof/async-profiler) |
|------|----------------------|---------------------------|
| CPU 오버헤드 | < 1% | 2-5% |
| 메모리 오버헤드 | 최소 | 중간 |
| 코드 변경 | 불필요 | 라이브러리 추가 필요 |
| 프로파일 정밀도 | 커널 수준 | 애플리케이션 수준 |
| 권장 환경 | 프로덕션 상시 | 개발/스테이징 정밀 분석 |

### Retention 및 Compaction

```yaml
# Pyroscope — 저장 설정
storage:
  backend: s3
  s3:
    bucket: profiles-storage
compactor:
  compaction_interval: 1h
  retention_period: 168h          # 7일 (프로파일은 짧게 유지)
  block_retention: 48h            # 로컬 블록 2일
```

---

## Cloud Provider 비용 비교

| 항목 | Grafana Cloud | Datadog | New Relic | Self-hosted |
|------|-------------|---------|-----------|-------------|
| **Metrics** | $8/1K series/월 | $5/host/월 + custom | 무료 (한도 내) | 인프라 비용만 |
| **Traces** | $0.5/GB | $1.70/GB indexed span | $0.30/GB | 인프라 비용만 |
| **Logs** | $0.50/GB | $0.10/GB ingested + $1.70/M indexed | $0.30/GB | 인프라 비용만 |
| **Free Tier** | 10K series, 50GB traces, 50GB logs | 14일 체험 | 100GB/월 | - |
| **장점** | OSS 호환, 유연한 retention | APM 통합 우수 | 관대한 무료 티어 | 완전 제어 |
| **단점** | 대규모 시 비용 급증 | lock-in, 비용 예측 어려움 | 쿼리 성능 이슈 | 운영 부담 |

> 가격은 2025년 기준이며 변동 가능. 실제 견적은 각 벤더에 확인하라.
> Self-hosted는 인프라 비용 + 엔지니어 운영 시간을 함께 계산해야 한다.

---

## Cost Monitoring 대시보드

### 수집량 추적 PromQL 쿼리

```promql
# 메트릭 — 시계열 수 추이
prometheus_tsdb_head_series

# 메트릭 — 일일 샘플 수집량
increase(prometheus_tsdb_head_samples_appended_total[24h])

# 트레이스 — 일일 수집 스팬 수
increase(otelcol_receiver_accepted_spans[24h])

# 로그 — 일일 수집량 (bytes)
sum(increase(loki_distributor_bytes_received_total[24h]))

# 프로파일 — 일일 수집 샘플 수
increase(pyroscope_ingester_ingested_sample_count[24h])
```

### 일간/주간 트렌드 패널 설정

```promql
# 일간 메트릭 카디널리티 증가율 (7일 비교)
prometheus_tsdb_head_series / prometheus_tsdb_head_series offset 7d - 1

# 일간 로그 수집량 (GB 단위)
sum(increase(loki_distributor_bytes_received_total[24h])) / 1024 / 1024 / 1024

# 주간 스팬 수집량 추이
sum(increase(otelcol_receiver_accepted_spans[7d]))
```

### 팀별 비용 귀속 (Recording Rules)

```yaml
groups:
  - name: cost-attribution
    interval: 60s
    rules:
      # 팀별 로그 수집량 (namespace → team 매핑)
      - record: team:log_bytes_received:rate1h
        expr: |
          sum(rate(loki_distributor_bytes_received_total[1h])) by (tenant)
        labels:
          __cost_center__: observability

      # 팀별 시계열 수
      - record: team:active_series:count
        expr: |
          count by (job) ({__name__=~".+"})

      # 팀별 스팬 수집률
      - record: team:spans_received:rate1h
        expr: |
          sum(rate(otelcol_receiver_accepted_spans[1h])) by (service_name)
```

---

## Cost Reduction Playbook

### Quick Wins (즉시 적용, 20-40% 절감)

- [ ] 프로덕션 로그 레벨을 INFO 이상으로 제한
- [ ] health check, readiness/liveness probe 스팬 수집 제외
- [ ] `http.request.body`, `http.response.body` 속성 제거
- [ ] 미사용 메트릭 식별 및 `metric_relabel_configs`로 드롭
- [ ] `db.statement` 속성을 500자로 truncate
- [ ] Loki 인덱스 라벨에서 고카디널리티 라벨 제거

### Medium-term (1-4주, 추가 30-50% 절감)

- [ ] Tail-based sampling 도입 (에러/느린 요청만 100% 수집)
- [ ] Recording rules로 고빈도 대시보드 쿼리 사전 집계
- [ ] Retention 티어링 적용 (Hot/Warm/Cold)
- [ ] 스트림별 로그 retention 차등 적용
- [ ] 프로파일 수집 빈도를 60초로 조정
- [ ] 팀별 비용 귀속 대시보드 구축

### Long-term (1-3개월, 아키텍처 변경)

- [ ] OTel Collector Gateway 패턴으로 중앙 집중 필터링
- [ ] Kafka 버퍼 아키텍처로 피크 부하 평탄화
- [ ] Native Histogram 전환으로 히스토그램 카디널리티 90% 감소
- [ ] Self-hosted → Managed 또는 Managed → Self-hosted 비용 비교 분석
- [ ] eBPF 기반 프로파일링으로 SDK 오버헤드 제거
- [ ] Exemplar 기반 trace 연결로 trace 전체 저장 대신 선택적 저장

---

## 관련 스킬

- `/observability-otel-optimization` — OTel Collector 샘플링, Kafka 버퍼 상세
- `/monitoring-metrics` — Prometheus 스케일링, Thanos, VictoriaMetrics
- `/sre-finops` — 클라우드 인프라 전체 비용 최적화
- `/logging-loki` — Loki 설정 및 LogQL 상세
