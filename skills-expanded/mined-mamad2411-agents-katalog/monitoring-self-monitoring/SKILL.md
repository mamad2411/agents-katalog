---
name: monitoring-self-monitoring
category: observability
description: "Observability Stack Self-Monitoring — Who watches the watchmen? — 모니터링 스택 자체의 건강 상태를 감시하는 전략과 패턴 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Observability Stack Self-Monitoring

Who watches the watchmen? — 모니터링 스택 자체의 건강 상태를 감시하는 전략과 패턴

## Quick Reference (증상 → 컴포넌트 매핑)

| 증상 | 의심 컴포넌트 | 확인 메트릭 |
|------|-------------|-----------|
| 메트릭 누락/지연 | Prometheus, OTel Collector | `up`, `scrape_duration_seconds` |
| 대시보드 빈 패널 | Grafana, Datasource 연결 | `grafana_datasource_request_duration_seconds` |
| 로그 지연/누락 | Loki, OTel Collector | `loki_distributor_bytes_received_total` |
| 트레이스 불완전 | Tempo, OTel Collector | `tempo_ingester_traces_created_total` |
| 알림 미발송 | Alertmanager, 채널 설정 | `alertmanager_notifications_failed_total` |
| 카디널리티 폭발 | Prometheus TSDB | `prometheus_tsdb_head_series` |
| OOM/재시작 반복 | 모든 컴포넌트 | `kube_pod_container_status_restarts_total` |
| 디스크 부족 | Prometheus, Loki, Tempo | `kubelet_volume_stats_available_bytes` |

**관련 스킬**: `/monitoring-metrics`, `/monitoring-troubleshoot`, `/kube-prometheus-stack`, `/alerting-discord`

---

## CRITICAL: 독립 알림 채널 (Independent Alert Channel)

모니터링 스택의 알림을 **자기 자신(같은 AlertManager)** 을 통해 보내면,
스택 장애 시 알림도 함께 죽는다. 이것이 self-monitoring의 핵심 함정이다.

### 원칙

- MUST 모니터링 스택 자체의 알림은 **별도 채널**로 발송
- NEVER 감시 대상인 AlertManager를 통해 자기 자신의 장애를 알림
- PREFER 외부 watchdog 서비스 활용

### 권장 구성

```
모니터링 스택 알림 경로:
  Watchdog Alert → 외부 서비스 (Healthchecks.io, Dead Man's Snitch)
                 → 외부 서비스가 heartbeat 미수신 감지
                 → PagerDuty / SMS / 별도 Slack Webhook

일반 비즈니스 알림 경로:
  PrometheusRule → AlertManager → Discord / Slack / PagerDuty
```

### 외부 Watchdog 서비스 추천

| 서비스 | 무료 티어 | 특징 |
|--------|----------|------|
| Healthchecks.io | 20개 체크 | cron 모니터링, 심플 |
| Dead Man's Snitch | 1개 체크 | PagerDuty 네이티브 통합 |
| Cronitor | 5개 모니터 | 다양한 알림 채널 |
| UptimeRobot | 50개 모니터 | HTTP 엔드포인트 모니터링 |

---

## Prometheus Self-Monitoring

### 핵심 메트릭

```yaml
# TSDB 건강 상태
prometheus_tsdb_head_series                    # 현재 active time series 수
prometheus_tsdb_head_chunks                    # 메모리 내 chunk 수
prometheus_tsdb_compaction_failed_total         # compaction 실패 (디스크 문제 의심)
prometheus_tsdb_wal_corruptions_total           # WAL 손상 감지
prometheus_tsdb_out_of_order_samples_total      # 순서 역전 샘플 (clock skew)
prometheus_tsdb_head_max_time                   # 최신 샘플 시각 (ingestion 지연 감지)

# 스크레이프 건강
prometheus_target_scrape_pool_exceeded_target_limit  # target 수 초과
prometheus_sd_discovered_targets                     # 서비스 디스커버리 결과
up                                                   # target 접근 가능 여부
scrape_duration_seconds                              # 스크레이프 소요 시간

# 리소스
process_resident_memory_bytes                  # RSS 메모리
prometheus_tsdb_storage_blocks_bytes           # 디스크 사용량
```

### 카디널리티 폭발 감지

카디널리티 폭발은 Prometheus OOM의 가장 흔한 원인이다.

```promql
# 시계열 수 급증 감지 (1시간 기준 20% 이상 증가)
delta(prometheus_tsdb_head_series[1h]) / prometheus_tsdb_head_series > 0.2

# 상위 카디널리티 메트릭 확인 (Prometheus /api/v1/status/tsdb 엔드포인트)
# curl -s localhost:9090/api/v1/status/tsdb | jq '.data.seriesCountByMetricName[:10]'

# label 값 폭발 확인
count by (__name__) ({__name__=~".+"}) > 10000
```

### WAL 손상 감지

```promql
# WAL 손상 발생 시 즉시 알림
increase(prometheus_tsdb_wal_corruptions_total[5m]) > 0
```

### Alert Rules (PrometheusRule)

```yaml
groups:
  - name: prometheus-self-monitoring
    rules:
      - alert: PrometheusHighCardinalitySeries
        expr: prometheus_tsdb_head_series > 2000000
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Prometheus 시계열 수 200만 초과"
          description: "현재 {{ $value }} 시계열. 카디널리티 폭발 여부 확인 필요."

      - alert: PrometheusCompactionFailed
        expr: increase(prometheus_tsdb_compaction_failed_total[1h]) > 0
        labels:
          severity: critical
        annotations:
          summary: "TSDB compaction 실패"
          description: "디스크 공간/권한 문제 가능성. WAL 크기 확인 필요."

      - alert: PrometheusWALCorrupted
        expr: increase(prometheus_tsdb_wal_corruptions_total[5m]) > 0
        labels:
          severity: critical
        annotations:
          summary: "Prometheus WAL 손상 감지"

      - alert: PrometheusTargetDown
        expr: up == 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "스크레이프 타겟 다운: {{ $labels.job }}"
```

---

## OTel Collector Self-Monitoring

### 데이터 유실 공식 (핵심)

```
데이터 유실 = receiver_accepted - exporter_sent
```

이 차이가 지속적으로 증가하면 Collector 내부에서 데이터가 손실되고 있다.

```promql
# Span 유실 감지
otelcol_receiver_accepted_spans - otelcol_exporter_sent_spans > 100

# Metric 유실 감지
otelcol_receiver_accepted_metric_points - otelcol_exporter_sent_metric_points > 100

# Log 유실 감지
otelcol_receiver_accepted_log_records - otelcol_exporter_sent_log_records > 100
```

### Queue 용량 모니터링

```promql
# Queue 사용률 (80% 이상이면 위험)
otelcol_exporter_queue_size / otelcol_exporter_queue_capacity > 0.8

# 내보내기 실패
rate(otelcol_exporter_send_failed_spans[5m]) > 0
rate(otelcol_exporter_send_failed_metric_points[5m]) > 0
```

### 거부된 데이터

```promql
# Receiver 거부 (형식 오류, rate limit 등)
rate(otelcol_receiver_refused_spans[5m]) > 0

# Processor에서 드롭
rate(otelcol_processor_dropped_spans[5m]) > 0
```

> 상세 최적화 전략은 `/observability-otel-optimization` 참조. 여기서는 self-monitoring 관점만 다룬다.

---

## Grafana Health

### 핵심 메트릭

```promql
# API 응답 시간 (대시보드 검색)
grafana_api_dashboard_search_duration_seconds

# Datasource 쿼리 시간
grafana_datasource_request_duration_seconds_sum
  / grafana_datasource_request_duration_seconds_count

# 로그인 실패
grafana_api_login_oauth_count{result="error"}

# 활성 사용자 수 (라이선스 초과 감지)
grafana_stat_active_users
```

### Datasource Health Check

```yaml
# Grafana provisioning에서 healthcheck 설정
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    healthCheckEnabled: true     # 주기적 health check 활성화

  - name: Loki
    type: loki
    url: http://loki:3100
    healthCheckEnabled: true

  - name: Tempo
    type: tempo
    url: http://tempo:3200
    healthCheckEnabled: true
```

### Grafana 알림

```promql
# Datasource 연결 실패
grafana_datasource_request_total{status="error"} > 0

# 대시보드 로딩 느림 (5초 이상)
grafana_api_dashboard_search_duration_seconds > 5
```

---

## Loki Health

### 핵심 메트릭

```promql
# Ingestion 속도
rate(loki_distributor_bytes_received_total[5m])

# 활성 스트림 수 (카디널리티 지표)
loki_ingester_streams_created_total

# 요청 지연
histogram_quantile(0.99,
  sum(rate(loki_request_duration_seconds_bucket[5m])) by (le, route)
)

# Rate limit 도달
rate(loki_discarded_samples_total[5m]) > 0

# Ingester 메모리 사용
loki_ingester_memory_chunks
```

### Alert Rules

```yaml
- alert: LokiIngestionRateLimited
  expr: rate(loki_discarded_samples_total[5m]) > 0
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Loki ingestion rate limit 도달. 로그 유실 발생 중."

- alert: LokiHighLatency
  expr: |
    histogram_quantile(0.99,
      sum(rate(loki_request_duration_seconds_bucket{route=~"loki_api_v1_push"}[5m])) by (le)
    ) > 5
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Loki push API p99 지연 5초 초과"
```

---

## Tempo Health

### 핵심 메트릭

```promql
# Trace ingestion 속도
rate(tempo_distributor_spans_received_total[5m])

# Ingester 활성 트레이스
tempo_ingester_traces_created_total

# Compactor 블록 수 (정상 compaction 확인)
tempo_compactor_blocks_total

# 쿼리 지연
histogram_quantile(0.99,
  sum(rate(tempo_query_frontend_queries_duration_seconds_bucket[5m])) by (le)
)

# Ingester 플러시 실패
rate(tempo_ingester_failed_flushes_total[5m]) > 0
```

### Trace 완전성 확인

```promql
# 수신 span 대비 저장 성공률
1 - (
  rate(tempo_discarded_spans_total[5m])
  / rate(tempo_distributor_spans_received_total[5m])
) < 0.99  # 99% 미만이면 알림
```

### Alert Rules

```yaml
- alert: TempoIngesterFlushFailed
  expr: rate(tempo_ingester_failed_flushes_total[5m]) > 0
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Tempo ingester 플러시 실패. 트레이스 데이터 유실 위험."

- alert: TempoCompactorUnhealthy
  expr: tempo_compactor_blocks_total == 0
  for: 30m
  labels:
    severity: warning
  annotations:
    summary: "Tempo compactor가 30분간 블록을 생성하지 않음"
```

---

## Alertmanager Self-Monitoring

### 핵심 메트릭

```promql
# 알림 발송 실패
alertmanager_notifications_failed_total

# 알림 발송 성공률
rate(alertmanager_notifications_total{status="success"}[5m])
  / rate(alertmanager_notifications_total[5m])

# 클러스터 동기화 (HA 구성 시)
alertmanager_cluster_members                   # 클러스터 멤버 수
alertmanager_cluster_messages_invalid_total     # 잘못된 클러스터 메시지

# Silence 활성 개수 (과도한 silence는 알림 누락 위험)
alertmanager_silences_active
```

### Alert Rules

```yaml
- alert: AlertmanagerNotificationFailing
  expr: rate(alertmanager_notifications_failed_total[5m]) > 0
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "AlertManager 알림 발송 실패 (integration: {{ $labels.integration }})"

- alert: AlertmanagerClusterMembersMismatch
  expr: alertmanager_cluster_members != 2  # HA 구성 시 예상 멤버 수
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "AlertManager 클러스터 멤버 불일치"
```

---

## DeadManSwitch 패턴

항상 firing 상태인 Watchdog 알림을 외부 서비스로 전송하여,
알림 파이프라인 전체가 살아있는지 확인하는 패턴이다.

### kube-prometheus-stack 내장 Watchdog

kube-prometheus-stack은 기본으로 `Watchdog` 알림을 포함한다.
이 알림은 **항상 firing** 상태이며, firing이 멈추면 파이프라인이 죽은 것이다.

```yaml
# kube-prometheus-stack values.yaml
alertmanager:
  config:
    route:
      routes:
        # Watchdog 알림을 별도 receiver로 라우팅
        - matchers:
            - alertname = "Watchdog"
          receiver: deadmansswitch
          repeat_interval: 1m    # 1분마다 외부 서비스에 heartbeat

    receivers:
      - name: deadmansswitch
        webhook_configs:
          # Healthchecks.io 연동
          - url: "https://hc-ping.com/<YOUR_CHECK_UUID>"
            send_resolved: false

          # Dead Man's Snitch 연동
          # - url: "https://nosnch.in/<YOUR_SNITCH_TOKEN>"
          #   send_resolved: false
```

### 동작 원리

```
정상:
  Watchdog 알림 (항상 firing) → AlertManager → 1분마다 외부 서비스 ping
  외부 서비스: "heartbeat 수신 중, 정상"

장애:
  Prometheus 다운 OR AlertManager 다운 → ping 중단
  외부 서비스: "heartbeat 미수신 감지" → PagerDuty / SMS 발송
```

### Healthchecks.io 설정 예시

1. Healthchecks.io에서 체크 생성 (Period: 1분, Grace: 5분)
2. 생성된 ping URL을 AlertManager webhook에 설정
3. Healthchecks.io에서 알림 채널 설정 (PagerDuty, Slack, Email)
4. **Grace period = 5분** — 일시적 네트워크 지연을 허용

---

## Dashboard Template (통합 스택 건강 대시보드)

### 권장 패널 구성

```
Row 1: 개요 (Overview)
  ├─ [Stat] 모니터링 스택 컴포넌트 UP/DOWN 상태
  ├─ [Stat] 총 active time series 수
  ├─ [Stat] 로그 ingestion rate (bytes/sec)
  └─ [Stat] 트레이스 ingestion rate (spans/sec)

Row 2: Prometheus
  ├─ [TimeSeries] prometheus_tsdb_head_series (시계열 수 추이)
  ├─ [TimeSeries] scrape_duration_seconds (스크레이프 지연)
  └─ [Gauge] TSDB 디스크 사용률

Row 3: OTel Collector
  ├─ [TimeSeries] receiver_accepted vs exporter_sent (데이터 유실 갭)
  ├─ [Gauge] exporter queue 사용률
  └─ [TimeSeries] send_failed rate

Row 4: Loki + Tempo
  ├─ [TimeSeries] Loki ingestion rate + discarded rate
  ├─ [TimeSeries] Tempo spans received + failed flushes
  └─ [TimeSeries] 양쪽 p99 쿼리 지연

Row 5: AlertManager
  ├─ [TimeSeries] notifications total (success vs failed)
  ├─ [Stat] active silences 수
  └─ [Stat] Watchdog heartbeat 최종 전송 시각
```

### 변수 (Template Variables)

```
$datasource = prometheus (uid: prometheus)
$namespace  = 모니터링 스택 네임스페이스 (기본: monitoring)
$interval   = 1m / 5m / 15m
```

> 대시보드 JSON 관리는 `grafana/dashboards/` SSOT 원칙을 따른다.
> 상세 Grafana 운영은 `/monitoring-grafana` 참조.
