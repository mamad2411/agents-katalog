---
name: observability-otel-migration
category: observability
description: "OTel Migration Patterns — Grafana Agent → Alloy, Zipkin → OTLP, Semantic Conventions 마이그레이션 전략 및 Declarative Configuration 1.0.0 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# OTel Migration Patterns

Grafana Agent → Alloy, Zipkin → OTLP, Semantic Conventions 마이그레이션 전략 및 Declarative Configuration 1.0.0

## Quick Reference (마이그레이션 결정 트리)

```
무엇을 마이그레이션해야 하는가?
    │
    ├─ 텔레메트리 수집기 ─────────────────────────────────────────────┐
    │       │                                                        │
    │       ├─ Grafana Agent (Static/Flow) ──> Alloy 마이그레이션     │
    │       │   (EOL: 2025-10, Alloy가 후속)                         │
    │       │                                                        │
    │       └─ OTel Collector (유지) ────────> 설정 최적화만          │
    │                                                                │
    ├─ 트레이싱 프로토콜 ────────────────────────────────────────────┐│
    │       │                                                       ││
    │       ├─ Zipkin ──────────────────────> OTLP 전환              ││
    │       │   (deprecated 2025-12, 제거 2026-12)                   ││
    │       │                                                       ││
    │       └─ Jaeger Thrift ──────────────> OTLP 전환              ││
    │           (deprecated, gRPC native 지원)                      ││
    │                                                               ││
    ├─ Semantic Conventions ────────────────────────────────────────┐││
    │       │                                                      │││
    │       ├─ http.method → http.request.method                   │││
    │       ├─ db.statement → db.query.text                        │││
    │       └─ GenAI semconv (experimental)                        │││
    │                                                              │││
    └─ Collector 설정 방식 ────────────────────────────────────────┐│││
            │                                                     ││││
            ├─ YAML pipeline 설정 ──────> 유지 가능               ││││
            └─ Declarative Config 1.0.0 ──> 신규 도입 검토        ││││
```

---

## Grafana Agent → Alloy 마이그레이션

### EOL 타임라인

| 날짜 | 이벤트 |
|------|--------|
| 2024-04 | Alloy 1.0 GA 릴리스 |
| 2024-09 | Grafana Agent 신규 기능 동결 |
| 2025-04 | Grafana Agent 보안 패치만 제공 |
| 2025-10 | Grafana Agent EOL — 모든 지원 종료 |

### River 문법 vs YAML 비교

Alloy는 **River 문법**만 지원한다. 기존 YAML 설정은 변환 필수.

```yaml
# Grafana Agent (YAML) — 더 이상 사용하지 않음
metrics:
  configs:
    - name: default
      remote_write:
        - url: http://mimir:9009/api/v1/push
      scrape_configs:
        - job_name: app
          static_configs:
            - targets: ['localhost:8080']
```

```hcl
// Alloy (River) — 마이그레이션 후
prometheus.scrape "app" {
  targets    = [{"__address__" = "localhost:8080"}]
  forward_to = [prometheus.remote_write.default.receiver]
}

prometheus.remote_write "default" {
  endpoint {
    url = "http://mimir:9009/api/v1/push"
  }
}
```

### 핵심 컴포넌트 매핑

| Grafana Agent (YAML) | Alloy (River) | 비고 |
|----------------------|---------------|------|
| `metrics.remote_write` | `prometheus.remote_write` | 동일 기능 |
| `metrics.scrape_configs` | `prometheus.scrape` | 컴포넌트 분리 |
| `logs.configs` | `loki.source.*` + `loki.write` | 수집/전송 분리 |
| `traces.configs` | `otelcol.receiver.*` + `otelcol.exporter.*` | OTel 파이프라인 |
| `integrations.node_exporter` | `prometheus.exporter.unix` | 이름 변경 |
| `integrations.process_exporter` | `prometheus.exporter.process` | 이름 변경 |
| `server.log_level` | `logging { level = "info" }` | 전역 설정 |

### 자동 변환 도구

```bash
# grafana-agent convert 명령으로 자동 변환
# Static mode config → Alloy River 문법
grafana-agent convert --source-format=static \
  --output=config.alloy \
  agent-config.yaml

# Flow mode config → Alloy River 문법
grafana-agent convert --source-format=flow \
  --output=config.alloy \
  agent-flow.river

# 변환 결과 검증 (dry-run)
alloy run config.alloy --stability.level=generally-available
```

### Helm 마이그레이션

```yaml
# values.yaml (Alloy Helm chart)
alloy:
  configMap:
    content: |
      // OTel 수신
      otelcol.receiver.otlp "default" {
        grpc { endpoint = "0.0.0.0:4317" }
        http { endpoint = "0.0.0.0:4318" }
        output {
          traces  = [otelcol.exporter.otlp.tempo.input]
          metrics = [otelcol.exporter.prometheus.mimir.input]
          logs    = [otelcol.exporter.loki.default.input]
        }
      }

      // Tempo로 트레이스 전송
      otelcol.exporter.otlp "tempo" {
        client { endpoint = "tempo:4317" }
      }

  replicas: 2
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
```

### 마이그레이션 검증 체크리스트

- [ ] `grafana-agent convert`로 설정 변환 완료
- [ ] Alloy dry-run 실행 시 에러 없음
- [ ] 메트릭 수집: Prometheus `up` 메트릭으로 타겟 스크래핑 확인
- [ ] 로그 수집: Loki에서 기존과 동일한 라벨로 로그 조회 가능
- [ ] 트레이스: Tempo에서 신규 트레이스 수신 확인
- [ ] Grafana 대시보드: 기존 대시보드 쿼리 정상 동작
- [ ] 알림 규칙: 기존 alerting rule 정상 동작
- [ ] 리소스 사용량: Agent 대비 CPU/Memory 비교

---

## Zipkin → OTLP 마이그레이션

### 타임라인

| 날짜 | 이벤트 |
|------|--------|
| 2025-06 | OTel Collector에서 Zipkin receiver deprecated 경고 시작 |
| 2025-12 | Zipkin receiver 공식 deprecated |
| 2026-12 | Zipkin receiver 제거 예정 |

### Collector 설정 변경

```yaml
# BEFORE: Zipkin receiver 사용
receivers:
  zipkin:
    endpoint: 0.0.0.0:9411

# AFTER: OTLP receiver로 전환
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

# 전환 기간 중 병행 운영 (점진적 마이그레이션)
receivers:
  zipkin:
    endpoint: 0.0.0.0:9411    # 레거시 클라이언트용 (임시)
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
```

### 클라이언트 SDK 변경

**Java (Spring Boot)**

```groovy
// BEFORE: Zipkin exporter
implementation 'io.zipkin.reporter2:zipkin-sender-okhttp3'

// AFTER: OTel OTLP exporter
implementation platform('io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom:2.25.0')
implementation 'io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter'
```

```yaml
# application.yml — OTLP 설정
otel:
  exporter:
    otlp:
      endpoint: http://otel-collector:4317
      protocol: grpc
```

**Go**

```go
// BEFORE: Zipkin exporter
import "go.opentelemetry.io/otel/exporters/zipkin"
exporter, _ := zipkin.New("http://collector:9411/api/v2/spans")

// AFTER: OTLP gRPC exporter
import "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
exporter, _ := otlptracegrpc.New(ctx,
    otlptracegrpc.WithEndpoint("otel-collector:4317"),
    otlptracegrpc.WithInsecure(),
)
```

---

## Semantic Conventions 마이그레이션

### OTEL_SEMCONV_STABILITY_OPT_IN 상세

OTel SDK/에이전트가 사용하는 attribute 이름을 제어하는 환경변수.

```bash
# 단계별 마이그레이션 전략
# 1단계: 구버전 + 신버전 동시 emit (안전한 전환 시작)
OTEL_SEMCONV_STABILITY_OPT_IN=http/dup

# 2단계: 대시보드/알림을 신규 attribute로 전환 완료 후
OTEL_SEMCONV_STABILITY_OPT_IN=http

# 3단계: 모든 semconv stable 전환 (여러 도메인)
OTEL_SEMCONV_STABILITY_OPT_IN=http,database
```

| 값 | 동작 | 용도 |
|----|------|------|
| (미설정) | 구버전 attribute만 emit | 기본값, 하위 호환 |
| `http/dup` | 구버전 + 신버전 **동시** emit | 전환 기간 — 대시보드 마이그레이션용 |
| `http` | 신버전 attribute만 emit | 전환 완료 후 |
| `database/dup` | DB 관련 구버전 + 신버전 동시 emit | DB semconv 전환 기간 |
| `database` | DB 신버전만 emit | DB 전환 완료 |

### HTTP Semantic Conventions 마이그레이션

```
단계별 전환 (http/dup → http):

1. OTEL_SEMCONV_STABILITY_OPT_IN=http/dup 설정
   → http.method + http.request.method 둘 다 emit

2. Grafana 대시보드 / PromQL 쿼리 업데이트
   - http.method        → http.request.method
   - http.status_code   → http.response.status_code
   - http.url           → url.full
   - http.target        → url.path + url.query
   - net.host.name      → server.address
   - net.host.port      → server.port
   - http.scheme        → url.scheme

3. Alerting rule 업데이트
   - recording rule의 label 매핑 확인
   - PrometheusRule에서 구버전 label 참조 제거

4. OTEL_SEMCONV_STABILITY_OPT_IN=http 로 전환
   → 구버전 attribute 제거, 카디널리티 절반으로 감소
```

### DB Semantic Conventions 마이그레이션

```
구버전 → 신버전 매핑:

db.system              → db.system.name
db.statement           → db.query.text
db.operation           → db.operation.name
db.name                → db.namespace
db.connection_string   → (제거, 보안 위험)
net.peer.name          → server.address
net.peer.port          → server.port
```

### GenAI Semantic Conventions (실험적)

```
상태: Experimental (2026-03 기준)
안정화 예정: 미정 — 프로덕션 사용 시 breaking change 주의

주요 attribute:
  gen_ai.system           = "openai" | "anthropic" | ...
  gen_ai.request.model    = "gpt-5" | "claude-opus-4-7" | ...
  gen_ai.usage.input_tokens
  gen_ai.usage.output_tokens
  gen_ai.response.finish_reasons

권장: 실험적 semconv는 내부 시스템에만 적용, 외부 의존 대시보드에는 미적용
```

---

## OTel Declarative Configuration 1.0.0

### 전체 YAML 예시

```yaml
# otel-config.yaml — Declarative Configuration
file_format: "0.4"

# SDK 전역 설정
sdk:
  disabled: false
  resource:
    attributes:
      service.name: order-service
      service.version: 1.2.0
      deployment.environment: production

  # 트레이스 설정
  tracer_provider:
    processors:
      - batch:
          schedule_delay: 5000
          max_queue_size: 2048
          max_export_batch_size: 512
    exporters:
      - otlp:
          protocol: grpc
          endpoint: http://otel-collector:4317
          timeout: 10000
    sampler:
      parent_based:
        root:
          trace_id_ratio_based:
            ratio: 0.1

  # 메트릭 설정
  meter_provider:
    readers:
      - periodic:
          interval: 30000
          exporters:
            - otlp:
                protocol: grpc
                endpoint: http://otel-collector:4317

  # 로그 설정
  logger_provider:
    processors:
      - batch:
          schedule_delay: 5000
    exporters:
      - otlp:
          protocol: grpc
          endpoint: http://otel-collector:4317
```

### 환경별 오버라이드 패턴

```yaml
# otel-config-dev.yaml — 개발 환경 오버라이드
file_format: "0.4"

sdk:
  resource:
    attributes:
      deployment.environment: development
  tracer_provider:
    sampler:
      parent_based:
        root:
          always_on: {}   # 개발 환경은 100% 샘플링
```

```bash
# 환경변수로 설정 파일 지정
OTEL_CONFIG_FILE=otel-config.yaml
# 오버라이드 (환경별 추가 설정)
OTEL_CONFIG_FILE=otel-config.yaml,otel-config-dev.yaml
```

### 환경변수 vs Declarative Configuration 비교

| 항목 | 환경변수 방식 | Declarative Config |
|------|-------------|-------------------|
| 설정 범위 | 제한적 (주요 옵션만) | 전체 SDK 설정 가능 |
| 타입 안전성 | 문자열만 | YAML 스키마 검증 가능 |
| 환경별 관리 | `.env` 파일 분리 | YAML 파일 오버라이드 |
| 코드 변경 | 불필요 | 불필요 |
| 복잡한 설정 | 불가 (sampler 체인 등) | 완전 지원 |
| 기존 호환성 | 모든 SDK 지원 | SDK별 지원 확인 필요 |
| GitOps 친화성 | 보통 | 높음 (YAML 파일 버전 관리) |

> **권장**: 신규 프로젝트는 Declarative Configuration 채택 검토.
> 기존 프로젝트는 환경변수 방식 유지하면서 점진적 전환.

---

## 안티패턴

| 안티패턴 | 결과 | 올바른 접근 |
|---------|------|-----------|
| Grafana Agent EOL 이후 계속 사용 | 보안 패치 미제공, 취약점 노출 | Alloy로 마이그레이션 |
| Alloy에서 YAML 문법 사용 시도 | 파싱 에러, 기동 실패 | River 문법만 사용, `convert` 도구 활용 |
| Zipkin/Jaeger receiver를 신규 구축에 채택 | deprecated 프로토콜 의존 | 신규는 반드시 OTLP 사용 |
| `http/dup` 상태로 장기간 운영 | attribute 카디널리티 2배, 스토리지/비용 증가 | 전환 기간은 최대 2-4주로 제한 |
| semconv 전환 없이 SDK만 업그레이드 | 대시보드/알림 쿼리 깨짐 | SDK 업그레이드 전 attribute 매핑 확인 |
| GenAI semconv를 외부 대시보드에 적용 | breaking change 시 장애 | experimental은 내부 시스템에만 |
| Declarative Config와 환경변수 혼용 | 우선순위 충돌, 예측 불가 동작 | 하나의 방식으로 통일 |
| `convert` 도구 결과를 검증 없이 배포 | 미지원 기능 누락, 런타임 에러 | 반드시 dry-run 후 배포 |

---

## 체크리스트

### Grafana Agent → Alloy
- [ ] 현재 Agent 버전 및 설정 방식(Static/Flow) 확인
- [ ] `grafana-agent convert`로 설정 변환
- [ ] Alloy dry-run 검증
- [ ] 스테이징 환경 배포 및 데이터 수집 확인
- [ ] Grafana 대시보드 정상 동작 확인
- [ ] 프로덕션 롤아웃 (카나리 → 전체)

### Zipkin → OTLP
- [ ] 클라이언트 SDK를 OTel OTLP exporter로 교체
- [ ] Collector에 OTLP receiver 추가
- [ ] 병행 운영 기간 설정 (Zipkin + OTLP 동시 수신)
- [ ] 모든 서비스 전환 완료 후 Zipkin receiver 제거

### Semantic Conventions
- [ ] 현재 사용 중인 SDK 버전의 semconv 확인
- [ ] `OTEL_SEMCONV_STABILITY_OPT_IN=http/dup` 설정
- [ ] 대시보드/알림 쿼리를 신규 attribute로 업데이트
- [ ] `OTEL_SEMCONV_STABILITY_OPT_IN=http`로 전환
- [ ] 구버전 attribute가 더 이상 emit 되지 않음을 확인

### Declarative Configuration
- [ ] SDK 버전이 Declarative Config를 지원하는지 확인
- [ ] `otel-config.yaml` 작성 및 스키마 검증
- [ ] 환경별 오버라이드 파일 구성
- [ ] 기존 환경변수와 충돌 없는지 확인

**관련 skill**: `/observability-otel`, `/observability-otel-scale`, `/observability-otel-optimization`
