---
name: logging-loki
category: observability
description: "Loki Log Analysis Guide — Grafana Loki + LogQL을 활용한 로그 검색/분석 가이드 (보안팀/개발팀용) Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Loki Log Analysis Guide

Grafana Loki + LogQL을 활용한 로그 검색/분석 가이드 (보안팀/개발팀용)

## Quick Reference (선택 기준)
```
Loki vs ELK 선택
    ├─ Loki ────────> 비용 효율, Grafana 통합, 메트릭 연계
    │                 메타데이터만 인덱싱 (저장 70% 절감)
    │
    └─ ELK ─────────> 전체 텍스트 검색, 복잡한 집계
                      장기 보관 + 컴플라이언스 감사
```

### Loki 장점/제한
| 장점 | 제한 |
|------|------|
| 저장 비용 70% 절감 | 전체 텍스트 인덱싱 없음 |
| Prometheus 라벨 연계 | 고카디널리티 비효율 |
| 설정 간단 | 복잡한 조인 불가 |

---

## Native OTLP vs LokiExporter (필수 이해)

**권장 방식은 Native OTLP** (권장 방식). LokiExporter는 deprecated이므로 사용 금지.

| 항목 | LokiExporter (deprecated) | Native OTLP (현재) |
|------|--------------------------|---------------------|
| 로그 레벨 필터 | `\| level="error"` | `\| detected_level="ERROR"` |
| 서비스 필터 | `{job="dev/auth"}` | `{service_name="auth"}` |
| 속성 접근 | JSON blob → `\| json` 파싱 필요 | Structured Metadata → 직접 접근 |
| 속성 예시 | `\| json \| severity="INFO"` | `\| severity_text="INFO"` |

### `detected_level` 규칙 (대문자)

```logql
# ✅ Native OTLP — 대문자 (OTel severityText 기준)
{service_name=~"$svc"} | detected_level="ERROR"
{service_name=~"$svc"} | detected_level=~"ERROR|WARN"

# ❌ LokiExporter 방식 (사용 금지)
{job="example-server"} | level="error"
```

- `detected_level`은 Loki가 severity를 자동 감지하여 structured metadata에 저장
- **반드시 대문자** (`ERROR`, `WARN`, `INFO`, `DEBUG`) — OTel severityText 기준
- 소문자 `level="error"`는 구 LokiExporter 방식이므로 절대 사용하지 않는다

### Structured Metadata 설정

OTLP attribute를 Loki stream label로 승격하는 방법은 **2가지**:

#### 방법 1: `distributor.otlp_config` (권장, 안정적)

```yaml
# loki-values.yaml
loki:
  structuredConfig:
    distributor:
      otlp_config:
        default_resource_attributes_as_index_labels:
          # 기본 17개를 완전히 대체 (리스트 전체 교체)
          - service.name          # → service_name
          - service.namespace     # → service_namespace
          - deployment.environment.name
          - k8s.namespace.name
          - k8s.deployment.name
          - log_type              # ← 커스텀 attribute 추가
```

**CRITICAL**: 이 설정은 기본 리스트를 **완전히 대체**한다. 유지할 기본 attribute를 모두 명시해야 함.

#### 방법 2: `limits_config.otlp_config` (known bug 있음)

```yaml
loki:
  structuredConfig:
    limits_config:
      allow_structured_metadata: true
      otlp_config:
        resource_attributes:
          ignore_defaults: false
          attributes_config:
            - action: index_label
              attributes:
                - log_type
            - action: structured_metadata
              attributes:
                - host.name
            - action: drop
              regex: "internal\\..*"
        log_attributes:
          - action: structured_metadata
            attributes:
              - user.id
              - trace_id
```

**Known Bug**: `limits_config.otlp_config`의 `index_label` action이 일부 환경에서 동작하지 않음 (GitHub #13440, #15927). **distributor 방식을 우선 사용**.

#### attribute 타입별 승격 가능 여부

| Attribute 타입 | index_label | structured_metadata | drop |
|---|---|---|---|
| resource_attributes | **가능** | 가능 | 가능 |
| scope_attributes | 불가 | 가능 | 가능 |
| log_attributes | **불가** | 가능 | 가능 |

**CRITICAL**: `log_type`을 index_label로 쓰려면 **반드시 resource attribute**로 설정해야 한다. OTel SDK에서 log attribute로 넣으면 승격 불가.

#### Naming 변환 규칙

OTLP attribute의 `.`은 Loki에서 `_`로 자동 변환:
- `service.name` → `service_name`
- `deployment.environment.name` → `deployment_environment_name`
- `log_type` → `log_type` (점 없으면 그대로)

#### log_type을 resource attribute로 설정하는 방법

**Spring Boot application.yml:**
```yaml
otel:
  resource:
    attributes:
      log_type: app   # 기본값
```

**또는 OTel Collector attributes processor:**
```yaml
processors:
  attributes/log_type:
    actions:
      - key: log_type
        value: app
        action: upsert
```

### Structured Metadata 제한

| 항목 | 기본값 | 설정키 |
|------|--------|--------|
| 최대 크기 | 64KB/entry | `max_structured_metadata_size` |
| 최대 항목 수 | 128/entry | `max_structured_metadata_entries_count` |
| 스키마 요구 | v13 + TSDB | 미충족 시 OTLP 거부 |

### 보존 정책과 index_label

`log_type`이 index_label로 승격되면 보존 정책 selector에서 사용 가능:

```yaml
limits_config:
  retention_period: 744h  # 기본 30일
  retention_stream:
    - selector: '{log_type="payment"}'
      priority: 3
      period: 43800h  # 5년 (전자금융거래법 22조)
    - selector: '{log_type="audit"}'
      priority: 2
      period: 17520h  # 2년 (개인정보보호법)
    - selector: '{log_type="app"}'
      priority: 1
      period: 168h    # 7일
```

### Mixed Workload 주의 (OTLP + Push API 동시 사용)

OTLP와 `/loki/api/v1/push`를 동시에 사용하면 distributor 경합 발생 가능 (#19392):
- 메모리 스파이크 (512MiB+)
- goroutine 블로킹
- append 실패

**대응**: `rate_store.max_request_parallelism`을 600 이상으로 설정하거나, **OTLP 단일 경로**로 통일.

### `service_name` 필터 패턴

```logql
# ✅ service_name은 namespace 없는 순수 서비스명 (OTel service.name)
{service_name=~"$svc", service_name=~".+"}

# service_name=~".+" 는 빈 값 제외 (safety guard)
# Grafana 변수 $svc가 비어있을 때 전체 로그를 가져오는 것 방지
```

### Loki Schema v13 + TSDB

```yaml
# boltdb-shipper는 deprecated → tsdb 사용
schemaConfig:
  configs:
    - from: "2024-01-01"
      store: tsdb          # ✅ boltdb-shipper는 deprecated
      object_store: filesystem
      schema: v13          # 최신 schema
```

- `v13`은 TSDB store 필수
- `boltdb-shipper` → `tsdb` 마이그레이션: `from` 날짜를 새로 추가하여 전환

---

## 역할별 LogQL 쿼리

### 개발팀용 쿼리

**에러 추적**
```logql
# 내 서비스 에러 로그
{namespace="production", app="order-service"} |= "error"

# 특정 trace_id로 전체 흐름 추적
{namespace="production"} | json | trace_id="abc123def456"

# 최근 5분간 에러 + 스택트레이스
{app="payment-service"} |= "Exception" | json | line_format "{{.timestamp}} {{.message}}\n{{.stacktrace}}"
```

**성능 분석**
```logql
# 느린 요청 (1초 이상)
{app="api-gateway"} | json | duration_ms > 1000

# 엔드포인트별 평균 응답시간
avg_over_time({app="api-gateway"} | json | unwrap duration_ms [5m]) by (endpoint)

# P95 응답시간
quantile_over_time(0.95, {app="api-gateway"} | json | unwrap duration_ms [5m])
```

### 보안팀용 쿼리

**인증/접근 분석**
```logql
# 로그인 실패 시도
{job="security"} |= "login_failed" | json
  | line_format "IP={{.ip}} USER={{.username}} TIME={{.timestamp}}"

# 동일 IP 다중 실패 (brute force 의심)
sum by (ip) (count_over_time({job="security"} |= "login_failed" | json [5m])) > 5

# 비정상 시간대 접근 (야간 02-06시)
{job="security"} |= "login_success" | json
  | __timestamp__ >= 02:00 and __timestamp__ <= 06:00
```

**봇/매크로 탐지**
```logql
# 봇 탐지 이벤트
{app="bot-detector"} | json | is_bot="true"
  | line_format "{{.timestamp}} IP={{.client_ip}} SIGNAL={{.detection_signals}}"

# 고신뢰도 봇 (confidence > 0.9)
{app="bot-detector"} | json | is_bot="true" | confidence > 0.9

# IP별 봇 탐지 횟수
sum by (client_ip) (count_over_time({app="bot-detector"} | json | is_bot="true" [1h]))
```

**결제/민감정보 접근**
```logql
# 결제 로그 조회
{log_type="payment"} | json
  | line_format "{{.timestamp}} TXN={{.transaction_id}} AMT={{.amount}} STATUS={{.status}}"

# 개인정보 접근 로그
{log_type="personal_info_access"} | json
  | line_format "{{.timestamp}} USER={{.accessor}} TARGET={{.data_subject}} ACTION={{.action}}"

# 대량 조회 탐지 (10건 이상/분)
sum by (accessor) (count_over_time({log_type="personal_info_access"} | json [1m])) > 10
```

---

## LogQL 문법 심화

### 파서 (Parser)
```logql
# JSON 파싱
{app="api"} | json

# 정규식 파싱
{app="nginx"} | regexp `(?P<ip>\d+\.\d+\.\d+\.\d+) - (?P<user>\S+)`

# Pattern 파싱 (간단한 구조)
{app="nginx"} | pattern `<ip> - <user> [<_>] "<method> <path> <_>" <status>`

# 라인 포맷 (출력 형식 지정)
{app="api"} | json | line_format "{{.level}} [{{.trace_id}}] {{.message}}"
```

### 필터 연산자
```logql
# 포함 (대소문자 구분)
{app="api"} |= "error"

# 포함 (대소문자 무시)
{app="api"} |~ "(?i)error"

# 미포함
{app="api"} != "health"

# 정규식 매칭
{app="api"} |~ "status=[45][0-9]{2}"

# 체이닝 (AND 조건)
{app="api"} |= "error" != "timeout" |~ "user_id=\\d+"
```

### 메트릭 쿼리
```logql
# 분당 에러 수
count_over_time({app="api"} |= "error" [1m])

# 에러율 (%)
sum(rate({app="api"} |= "error" [5m]))
  / sum(rate({app="api"} [5m])) * 100

# 레이블별 집계
sum by (status_code) (count_over_time({app="api"} | json [5m]))

# Top 10 에러 엔드포인트
topk(10, sum by (endpoint) (count_over_time({app="api"} |= "error" | json [1h])))
```

---

## 대시보드 구성

### 개발팀 대시보드
```
┌──────────────┬──────────────┬──────────────┐
│ Error Count  │ Error Rate % │ Slow Requests│
│  (실시간)    │   (5분)      │   (>1초)     │
├──────────────┴──────────────┴──────────────┤
│           Error Logs (실시간 스트림)         │
├──────────────────────────────────────────────┤
│           Endpoint별 에러 분포               │
└──────────────────────────────────────────────┘
```

**패널 쿼리**
```logql
# Error Count
sum(count_over_time({app=~"$app"} |= "error" [1m]))

# Slow Requests
count_over_time({app=~"$app"} | json | duration_ms > 1000 [5m])
```

### 보안팀 대시보드
```
┌──────────────┬──────────────┬──────────────┐
│ Bot Detected │ Login Failed │ PII Access   │
│   (1시간)    │   (1시간)    │   (1시간)    │
├──────────────┴──────────────┴──────────────┤
│        국가별/IP별 봇 탐지 히트맵            │
├────────────────────┬─────────────────────────┤
│  보안 이벤트 로그  │  의심 IP Top 10        │
└────────────────────┴─────────────────────────┘
```

---

## 알림 설정 (Grafana Alerting)

### 에러율 알림
```yaml
# 에러율 5% 초과 시
- alert: HighErrorRate
  expr: |
    sum(rate({app="order-service"} |= "error" [5m]))
    / sum(rate({app="order-service"} [5m])) * 100 > 5
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "High error rate: {{ $value }}%"
```

### 봇 공격 알림
```yaml
# 분당 봇 100건 초과
- alert: BotAttackDetected
  expr: |
    sum(count_over_time({app="bot-detector"} | json | is_bot="true" [1m])) > 100
  for: 1m
  labels:
    severity: warning
  annotations:
    summary: "Bot attack: {{ $value }} detections/min"
```

### 개인정보 대량 접근 알림
```yaml
# 단일 사용자 10건/분 초과 접근
- alert: SuspiciousPIIAccess
  expr: |
    max by (accessor) (
      sum(count_over_time({log_type="personal_info_access"} | json [1m])) by (accessor)
    ) > 10
  for: 1m
  labels:
    severity: high
```

---

## 고급 패턴

### Trace-Log 연계
```logql
# 1. 느린 trace 찾기 (Tempo에서)
# 2. trace_id로 전체 로그 조회
{namespace="production"} | json | trace_id="<TRACE_ID>"
  | line_format "{{.service}} {{.timestamp}} {{.message}}"
```

### 시계열 분석
```logql
# 시간별 트렌드
sum(count_over_time({app="api"} |= "error" [1h])) by (hour)

# 이전 기간 대비 (offset 사용)
count_over_time({app="api"} |= "error" [1h])
  / count_over_time({app="api"} |= "error" [1h] offset 1d) * 100 - 100
```

---

## 성능 최적화

### 쿼리 최적화
```
✅ 좋은 쿼리
───────────
{app="order-service", env="production"} |= "error"
→ 라벨로 먼저 필터, 그 후 텍스트 필터

❌ 나쁜 쿼리
───────────
{} |= "order-service" |= "error"
→ 모든 로그 스캔 후 필터 (매우 느림)
```

### 고카디널리티 주의
```
❌ 피해야 할 라벨
───────────────
- user_id (무한 증가)
- request_id (무한 증가)
- ip_address (높은 카디널리티)

✅ 사용해야 할 라벨
─────────────────
- app, service, namespace
- env (dev/staging/prod)
- detected_level (ERROR/WARN/INFO) — Native OTLP 기준
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 빈 라벨 셀렉터 `{}` | 전체 스캔 | 라벨 먼저 지정 |
| 고카디널리티 라벨 | 인덱스 폭발 | 로그 본문에 포함 |
| 긴 시간 범위 | 타임아웃 | 시간 범위 축소 |
| 복잡한 정규식 | CPU 부하 | 단순 필터 우선 |

---

## 체크리스트

### 개발팀
- [ ] 에러 추적 쿼리 숙지
- [ ] trace_id 연계 검색
- [ ] 성능 분석 쿼리

### 보안팀
- [ ] 로그인/접근 분석 쿼리
- [ ] 봇 탐지 대시보드
- [ ] 개인정보 접근 모니터링
- [ ] 알림 규칙 설정

**관련 skill**: `/monitoring-logs`, `/logging-security`, `/logging-elk`

---

## 참고 자료
- [LogQL 공식 문서](https://grafana.com/docs/loki/latest/query/)
- [LogQL 쿼리 예제](https://grafana.com/docs/loki/latest/query/query_examples/)
- [Loki vs ELK 비교](https://signoz.io/blog/loki-vs-elasticsearch/)
