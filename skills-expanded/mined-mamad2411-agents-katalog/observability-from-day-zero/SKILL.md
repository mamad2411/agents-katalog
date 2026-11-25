---
name: observability-from-day-zero
category: observability
description: 관찰성을 사후 조립하지 않고 코드 작성 첫 줄부터 trace/metric/log 3-pillar를 설계하는 ODD(Observability-Driven Development) 체크리스트. TraceID 누락, label cardinality 폭발, signal silo 방지.
---

# Observability from Day Zero (M6: 관찰성 사후 조립)

관찰성을 "릴리스 후 모니터링 팀이 추가" 하면 항상 **TraceID 누락**, **label cardinality 폭발**, **signal 간 correlation 부재** 등 사후 보강 비용이 폭증한다. ODD (Observability-Driven Development) = 코드 첫 줄부터 관찰성을 설계한다.

> Claude mental model 오류: "메트릭은 나중에 추가하면 된다" → trace context propagation 은 boundary 수정이 필요해 retrofit 비용이 매우 크다. label 명명도 일관성 없이 추가되면 cardinality 폭발로 Mimir/Prometheus 가 OOM.

---

## 3-Pillar + Correlation

```
┌─────────────────────────────────────────────────┐
│ Traces (request 흐름)                            │
│   - trace_id, span_id, parent_span_id            │
│   - W3C Trace Context propagation                │
│   ↓ correlation key: trace_id                   │
│ Logs (event detail)                              │
│   - structured (JSON / key=value)                │
│   - trace_id 필드 포함 → trace ↔ log jump        │
│   ↓ correlation key: trace_id + labels          │
│ Metrics (집계)                                   │
│   - exemplars 로 trace_id 첨부                   │
│   - label cardinality < 100 / metric            │
└─────────────────────────────────────────────────┘
```

**핵심**: 세 신호가 **같은 trace_id 와 같은 resource attributes** 를 공유해야 cross-signal 분석 가능.

---

## Day Zero 설계 결정 (코드 작성 전)

### 1. Tracing context propagation

- **W3C Trace Context** 헤더 (`traceparent`, `tracestate`) — Cloud-neutral 표준
- 모든 boundary (HTTP / gRPC / Kafka / DB) 에서 propagation 강제
- OTel SDK / agent 사용 시 자동 처리 — 단, 비표준 transport (e.g., 자체 RPC) 는 수동 inject

### 2. Resource attributes (cross-signal join key)

```yaml
# OTel Resource — 세 신호 모두에 자동 첨부
service.name: user-service           # 필수
service.namespace: goti              # 환경 분리
service.version: 1.2.3               # 배포 버전
deployment.environment: prod         # dev/staging/prod
k8s.namespace.name: goti             # K8s context
k8s.pod.name: ${HOSTNAME}
```

→ Grafana 에서 `service.name=user-service` 로 metric ↔ trace ↔ log 동시 필터 가능.

### 3. Label 명명 컨벤션 (cardinality 폭탄 방지)

```
✅ 허용 (low cardinality)
- http_method (GET/POST/PUT/DELETE — 7종)
- http_status_class (2xx/4xx/5xx — 3종)
- endpoint (라우트 패턴 /users/:id — 수십 종)
- env (dev/staging/prod — 3종)

❌ 금지 (high cardinality)
- user_id (수백만 개)
- request_id / trace_id (label 아닌 exemplar 로)
- raw_url (path parameter 그대로 — /users/12345 별 series 생성)
- error_message (자유 문자열)
```

규칙:
- **per-metric label 수 < 10**
- **per-label cardinality < 100**
- **trace_id 는 exemplar 로** (label 아님)

### 4. SLI 를 코드와 같이 설계

API endpoint 만들 때 동시에:
- **Availability SLI**: 5xx / total 의 ratio
- **Latency SLI**: p95 / p99 histogram
- **Quality SLI**: business 정확성 (예: 결제 성공률)

이 셋을 PR 머지 전 만든다. 사후 보강이 가장 비싸다.

### 5. Log 구조화 의무

```java
// ❌ 자유 문자열
log.info("User 12345 logged in from 1.2.3.4 at 2026-05-12T10:00");

// ✅ 구조화 + trace_id 포함
MDC.put("trace_id", currentTraceId());
log.info("user login",
  kv("user_id", userId),
  kv("source_ip", sourceIp),
  kv("auth_method", authMethod));
```

OTel Logs Bridge 사용 시 자동으로 trace_id 첨부.

---

## ❌ 사후 보강 안티패턴 5종

### 1. trace_id 없는 log

→ Tempo trace 에서 "이 span 의 application log" 점프 불가. retrofit 시 모든 logger 패턴 수정 필요.

### 2. metric 에 user_id 라벨

```
http_requests_total{user_id="u_12345", endpoint="/api/x"}
```

→ user 100만 명 × endpoint 50 = 5천만 series. Mimir OOM.

### 3. Service name 명명 일관성 부재

- 어떤 곳은 `user-service`, 어떤 곳은 `user_service`, 또 어떤 곳은 `goti-user`
- 대시보드 query 가 매번 `OR` 조건으로 양쪽 다 처리해야 함
- **표준**: OTel `service.name` semantic convention 의 형식 (`<namespace>/<service.name>` Prometheus 매핑 주의)

### 4. Sampling 정책 사후 추가

처음부터 모든 trace 수집 → cost 폭증 → 100:1 sampling 적용 → critical path 가 sampled out
→ Day 0 에 **tail-based sampling** 또는 **error+slow priority** 정책 설계

### 5. Dashboard / Alert 가 코드와 분리

→ 코드 변경 시 dashboard 가 깨짐 (label rename 등) → 자동 검출 안 됨
→ dashboard / alert 도 같은 PR 에서 갱신 (monorepo 또는 cross-link 의무)

---

## 자가 검증 체크리스트

새 서비스 / endpoint 추가 시 **PR 머지 전**:

- [ ] OTel resource attributes (`service.name`, `service.version`, `deployment.environment`) 설정?
- [ ] HTTP / gRPC / Kafka / DB boundary 에서 trace context propagation 확인?
- [ ] Log 가 structured (JSON / key=value) 이고 `trace_id` 필드 포함?
- [ ] 새 metric 의 label 이 **low cardinality** (< 100 unique values) 인가?
- [ ] user_id / request_id / raw_url 등 high cardinality 값이 **label 아닌 exemplar** 인가?
- [ ] SLI (availability / latency / quality) 가 정의되었는가?
- [ ] Dashboard / Alert 가 **같은 PR** 에서 갱신되었는가?
- [ ] Sampling 정책이 명시되었는가? (head / tail / probabilistic)

---

## 외부 근거

- [Observability-Driven Development — Honeycomb](https://www.honeycomb.io/blog/observability-driven-development)
- [Authors' Cut — Making the Move to ODD — Honeycomb](https://www.honeycomb.io/blog/authors-cut-observability-driven-development)
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [Prometheus naming conventions](https://prometheus.io/docs/practices/naming/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)

---

## 연계 skill

- [`observability/observability-otel.md`](../observability-otel/SKILL.md) — OTel SDK 상세
- [`observability/monitoring-prometheus-operator.md`](../monitoring-prometheus-operator/SKILL.md) — Prometheus operator
- [`architecture/config-explicit-defaults.md`](../config-explicit-defaults/SKILL.md) — OTel exporter default 변경 추적

---

## 의외의 발견 (Honeycomb 분석)

- Honeycomb 본인이 "ODD" 명칭에 미묘하게 부정적 — "관찰성은 TDD 같은 process 가 아니라 mindset" 강조
- 그러나 **"코드 작성 전 관찰성 설계"** 라는 개념 자체는 SRE / DevOps 커뮤니티 광범위 합의
- 가장 실효성 있는 1줄 규칙: **"PR template 에 SLI 정의 + dashboard 링크 필드 강제"**
