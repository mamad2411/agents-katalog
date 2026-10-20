---
name: observability-alloy-to-otel
category: observability
description: "Alloy → OTel Collector 마이그레이션 가이드 — Grafana Alloy에서 표준 OTel Collector로 전환하기 위한 컴포넌트 매핑, 설정 변환, 영향 분석 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Alloy → OTel Collector 마이그레이션 가이드

Grafana Alloy에서 표준 OTel Collector로 전환하기 위한 컴포넌트 매핑, 설정 변환, 영향 분석

## Quick Reference (마이그레이션 결정 트리)

```
Alloy → OTel Collector 전환 시
    │
    ├─ otelcol.* 블록 ──────────> YAML 1:1 변환 (직접 매핑)
    │
    ├─ loki.process / loki.write ─> Loki OTLP native endpoint로 대체
    │                               otlphttp exporter → /otlp
    │
    ├─ prometheus.remote_write ───> prometheusremotewrite exporter
    │                               또는 otlphttp → Mimir /otlp
    │
    └─ Alloy 전용 기능 ──────────> 대안 필요
        ├─ UI (12345) ──────────> 없음 (Grafana 대시보드로 대체)
        ├─ 클러스터링 ──────────> 외부 LB + HPA
        └─ pyroscope.* ─────────> Pyroscope Java Agent 직접 연동
```

---

## 자동 변환 도구

**Alloy → OTel 변환 도구는 존재하지 않는다.** 반대 방향만 공식 지원.

| 도구 | 방향 | 비고 |
|------|------|------|
| `alloy convert --source-format=otelcol` | OTel → Alloy | 공식 |
| Alloy → OTel | **없음** | 수동 변환 필수 |

---

## 컴포넌트 매핑 (핵심)

### 1:1 매핑 가능 (otelcol.* 블록)

| Alloy (River) | OTel Collector (YAML) | 비고 |
|---|---|---|
| `otelcol.receiver.otlp` | `receivers.otlp` | 포트/프로토콜 동일 |
| `otelcol.processor.batch` | `processors.batch` | timeout, send_batch_size 동일 |
| `otelcol.processor.memory_limiter` | `processors.memory_limiter` | limit_mib, spike_limit_mib 동일 |
| `otelcol.processor.attributes` | `processors.attributes` | action 매핑 동일 |
| `otelcol.processor.transform` | `processors.transform` | OTTL 문법 동일 |
| `otelcol.processor.tail_sampling` | `processors.tail_sampling` | 정책 구조 동일 |
| `otelcol.processor.filter` | `processors.filter` | OTTL 조건 동일 |
| `otelcol.processor.k8sattributes` | `processors.k8sattributes` | 메타데이터 추출 동일 |
| `otelcol.exporter.otlp` | `exporters.otlp` | gRPC endpoint 동일 |
| `otelcol.exporter.otlphttp` | `exporters.otlphttp` | HTTP endpoint 동일 |
| `otelcol.exporter.kafka` | `exporters.kafka` | contrib 필요 |
| `otelcol.receiver.kafka` | `receivers.kafka` | contrib 필요 |
| `otelcol.connector.spanmetrics` | `connectors.spanmetrics` | contrib 필요 |

### 대체 필요 (Alloy 전용)

| Alloy 전용 | OTel Collector 대안 | 핵심 차이 |
|---|---|---|
| `loki.process` + `loki.write` | `exporters.otlphttp` → Loki `/otlp` | Loki 서버 측 `otlp_config`로 라벨 승격 |
| `prometheus.remote_write` | `exporters.prometheusremotewrite` | 거의 동일 |
| `prometheus.scrape` | ServiceMonitor + Prometheus/Mimir | Collector가 직접 scrape 안 함 |
| `prometheus.operator.servicemonitor` | Prometheus Operator CRD 직접 사용 | Alloy가 아닌 Prometheus/Mimir가 scrape |
| `loki.source.kubernetes_events` | `receivers.k8sobjects` (contrib) | K8s events 수집 |
| `mimir.rules.kubernetes` | mimirtool 또는 Mimir ruler API | PrometheusRule CRD sync |
| `pyroscope.*` | Pyroscope Java Agent (javaagent) | Collector 경유 없이 직접 전송 |
| `discovery.kubernetes` | Helm preset `kubernetesAttributes` | K8s 메타데이터 자동 주입 |

---

## 설정 변환 예시

### Alloy config.alloy → OTel Collector YAML

**Before (Alloy):**
```alloy
otelcol.receiver.otlp "default" {
  grpc { endpoint = "0.0.0.0:4317" }
  http { endpoint = "0.0.0.0:4318" }
  output {
    metrics = [otelcol.processor.memory_limiter.default.input]
    logs    = [otelcol.processor.memory_limiter.default.input]
    traces  = [otelcol.processor.memory_limiter.default.input]
  }
}

otelcol.processor.memory_limiter "default" {
  check_interval = "1s"
  limit           = "384MiB"
  spike_limit     = "128MiB"
  output {
    metrics = [otelcol.processor.attributes.default.input]
    logs    = [otelcol.processor.attributes.default.input]
    traces  = [otelcol.processor.attributes.default.input]
  }
}

otelcol.processor.attributes "default" {
  action {
    key    = "deployment.environment"
    value  = "dev"
    action = "upsert"
  }
  action {
    key    = "service.namespace"
    value  = "goti"
    action = "upsert"
  }
  output {
    metrics = [otelcol.processor.batch.default.input]
    logs    = [otelcol.processor.batch.default.input]
    traces  = [otelcol.processor.batch.default.input]
  }
}
```

**After (OTel Collector):**
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  memory_limiter:
    check_interval: 1s
    limit_mib: 384
    spike_limit_mib: 128

  attributes:
    actions:
      - key: deployment.environment
        value: dev
        action: upsert
      - key: service.namespace
        value: goti
        action: upsert

  batch:
    timeout: 5s
    send_batch_size: 1024

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, attributes, batch]
      exporters: [...]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, attributes, batch]
      exporters: [...]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, attributes, batch]
      exporters: [...]
```

### log_type 라벨 처리 — 핵심 변환

**Before (Alloy loki.process):**
```alloy
loki.process "default" {
  forward_to = [loki.write.default.receiver]
  stage.json {
    expressions = { log_type_raw = "attributes.log_type" }
  }
  stage.labels {
    values = { log_type = "log_type_raw" }
  }
}
```

**After (OTel Collector + Loki OTLP native):**
```yaml
# OTel Collector — loki.process 불필요
exporters:
  otlphttp/loki:
    endpoint: http://loki:3100/otlp

# Loki values — 서버 측에서 라벨 승격
loki:
  structuredConfig:
    distributor:
      otlp_config:
        default_resource_attributes_as_index_labels:
          - service.name
          - service.namespace
          - deployment.environment.name
          - log_type          # ← 커스텀 attribute 추가
```

**CRITICAL**: `log_type`은 반드시 **resource attribute**으로 설정해야 한다. log attribute나 scope attribute는 index_label로 승격 불가.

Spring Boot에서 resource attribute로 설정:
```yaml
otel:
  resource:
    attributes:
      log_type: app  # 기본값 — 코드에서 동적 변경 시 LogRecord에 넣지 말고 resource에 넣어야 함
```

또는 OTel Collector의 attributes processor로 주입:
```yaml
processors:
  attributes/log_type:
    actions:
      - key: log_type
        value: app
        action: upsert
```

---

## 메트릭 호환성

### otelcol_* 메트릭 — 대부분 호환

Alloy의 `otelcol.*` 컴포넌트와 OTel Collector는 **동일한 내부 메트릭 이름**을 사용:

| 메트릭 | Alloy | OTel Collector | 호환 |
|--------|-------|----------------|------|
| `otelcol_receiver_accepted_spans_total` | ✅ | ✅ | 동일 |
| `otelcol_processor_refused_metric_points_total` | ✅ | ✅ | 동일 |
| `otelcol_exporter_sent_log_records_total` | ✅ | ✅ | 동일 |
| `otelcol_exporter_queue_size` | ✅ | ✅ | 동일 |
| `alloy_config_last_load_successful` | ✅ | ❌ | Alloy 전용 |

**대시보드 영향:**
- `otelcol_*` 메트릭 사용 패널: **그대로 동작**
- `alloy_*` 메트릭 사용 패널: **교체 필요** → `otelcol_process_*` 등으로 대체

### 알림 규칙 리네이밍

```yaml
# Before (Alloy 이름)
- alert: AlloyExporterFailed
  expr: rate(otelcol_exporter_send_failed_spans[5m]) > 0

# After (이름만 변경, expr 동일)
- alert: OTelCollectorExporterFailed
  expr: rate(otelcol_exporter_send_failed_spans[5m]) > 0
```

---

## Alloy에서 잃는 것 vs 얻는 것

### 잃는 것

| 기능 | 영향 | 대안 |
|------|------|------|
| Web UI (12345) | 파이프라인 시각화 불가 | Grafana 대시보드 + `otelcol_*` 메트릭 |
| 내장 클러스터링 | DaemonSet 간 자동 타겟 분배 불가 | HPA + 외부 LB |
| `prometheus.operator.servicemonitor` | Collector가 직접 K8s 메트릭 scrape 불가 | Prometheus/Mimir가 직접 scrape |
| `mimir.rules.kubernetes` | PrometheusRule CRD 자동 sync 불가 | mimirtool 또는 Mimir ruler API |
| River 조건문 | 동적 파이프라인 불가 | Helm values + envsubst |

### 얻는 것

| 기능 | 이점 |
|------|------|
| 표준 YAML 설정 | 커뮤니티 자료 풍부, 팀 학습 비용 낮음 |
| contrib 생태계 | kafkaexporter/receiver 등 공식 지원 |
| 커스텀 빌드 (ocb) | 필요한 컴포넌트만 포함한 경량 바이너리 |
| OTel Operator | CRD 기반 auto-instrumentation, sidecar injection |
| 벤더 중립 | Grafana 스택 외 백엔드로 전환 용이 |

---

## 마이그레이션 체크리스트

### 설정 변환
- [ ] `otelcol.*` 블록 → YAML 변환 완료
- [ ] `loki.process` → Loki OTLP native 전환 (distributor otlp_config)
- [ ] `prometheus.remote_write` → `prometheusremotewrite` exporter 전환
- [ ] Tail sampling 정책 변환 확인
- [ ] PII 마스킹 (transform processor) 변환 확인

### 대시보드/알림
- [ ] `alloy_*` 메트릭 사용 패널 교체
- [ ] `otelcol_*` 메트릭 패널 동작 확인
- [ ] 알림 규칙 이름 리네이밍 (Alloy* → OTelCollector*)
- [ ] LogQL 쿼리가 `log_type` 라벨로 정상 동작하는지 확인
- [ ] Loki 보존 정책 selector 동작 확인

### K8s 메트릭 수집
- [ ] ServiceMonitor/PodMonitor가 Prometheus/Mimir에서 직접 scrape 되는지 확인
- [ ] Node Exporter, Kube-State-Metrics 수집 경로 확인
- [ ] Kubernetes Events 수집 (`k8sobjects` receiver 또는 별도 설정)

### 인프라
- [ ] Alloy Helm chart 제거
- [ ] OTel Collector Helm chart 설치
- [ ] NetworkPolicy 업데이트 (monitoring → kafka, monitoring → backends)
- [ ] Prometheus scrape config에서 Alloy 타겟 제거, Collector 타겟 추가

---

## Anti-Patterns

| 안티패턴 | 결과 | 올바른 접근 |
|---------|------|-----------|
| `log_type`을 log attribute로 설정 | Loki index_label 승격 불가 | **resource attribute**로 설정 |
| Alloy의 `loki.process`를 OTel Collector의 `lokiexporter`로 대체 | deprecated exporter 사용 | `otlphttp` → Loki `/otlp` 사용 |
| otelcol_* 메트릭이 동일하다고 가정하고 label 카디널리티 미확인 | 알림 오발 | label 차이 확인 후 threshold 조정 |
| ServiceMonitor scraping을 Collector에서 하려고 시도 | 복잡한 설정, 비효율 | Prometheus/Mimir가 직접 scrape |
| Alloy 제거와 OTel Collector 설치를 동시에 진행 | 텔레메트리 유실 | 병행 운영 후 전환 |

---

## 참조 스킬

- `/observability-otel` — OTel Collector 기본 설정
- `/observability-otel-optimization` — Kafka 버퍼, 비용 최적화
- `/observability-otel-scale` — 대규모 트래픽 스케일링
- `/observability-otel-collector-helm` — Helm chart 환경별 패턴
- `/logging-loki` — Loki OTLP native 상세 설정
- `/observability-mimir-monolithic` — Mimir 싱글바이너리 설정
