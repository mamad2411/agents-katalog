---
name: observability-genai
category: observability
description: "GenAI Observability — OTel GenAI Semantic Conventions, LLM 호출 Tracing, Token Usage Metrics, Quality Metrics, Grafana 대시보드 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# GenAI Observability

OTel GenAI Semantic Conventions, LLM 호출 Tracing, Token Usage Metrics, Quality Metrics, Grafana 대시보드

## Quick Reference (결정 트리)

```
GenAI 관측 대상?
    │
    ├─ LLM API 호출 추적 ─────> OTel GenAI Spans (gen_ai.*)
    │       │
    │       ├─ 지연시간/에러율 ──> gen_ai.client.operation.duration
    │       ├─ 토큰 사용량 ─────> gen_ai.client.token.usage
    │       └─ 비용 추적 ───────> token metrics → FinOps 환산
    │
    ├─ RAG 파이프라인 ────────> 검색→컨텍스트→LLM 전체 trace
    │       │
    │       ├─ 검색 품질 ───────> retrieval relevance score
    │       └─ 응답 품질 ───────> groundedness, faithfulness
    │
    ├─ Agent 워크플로우 ──────> gen_ai.agent.* spans
    │       │
    │       ├─ 도구 호출 추적 ──> gen_ai.tool.* attributes
    │       └─ 루프 감지 ───────> iteration count monitoring
    │
    └─ 품질 & 안전 ───────────> Guardrail metrics
            │
            ├─ Hallucination ──> 자동 감지 지표
            └─ PII 노출 ───────> 필터링 이벤트 추적

계측 방식?
    │
    ├─ Spring AI ───────────> Advisor에서 OTel span 생성
    ├─ Go ──────────────────> middleware로 LLM 호출 계측
    ├─ Python (LangChain) ─> OpenLLMetry 자동 계측
    └─ 벤더 네이티브 ───────> Datadog/Grafana GenAI 통합
```

---

## OTel GenAI Semantic Conventions

### 핵심 Attribute Namespace

```
gen_ai.*                         ← 최상위 namespace
├── gen_ai.system               = "anthropic" | "openai" | "ollama"
├── gen_ai.request.model        = "claude-opus-4-7"
├── gen_ai.request.temperature  = 0.7
├── gen_ai.request.max_tokens   = 4096
├── gen_ai.response.model       = "claude-opus-4-7"
├── gen_ai.response.finish_reason = "stop" | "max_tokens" | "tool_use"
├── gen_ai.usage.input_tokens   = 1523
├── gen_ai.usage.output_tokens  = 847
└── gen_ai.operation.name       = "chat" | "embeddings"
```

### Agent Spans (Agentic 워크플로우)

```
gen_ai.agent.*
├── gen_ai.agent.name           = "code-reviewer"
├── gen_ai.agent.description    = "코드 리뷰 에이전트"
└── gen_ai.tool.*
    ├── gen_ai.tool.name        = "search_code"
    ├── gen_ai.tool.description = "코드 검색 도구"
    └── gen_ai.tool.call.id     = "call_abc123"
```

### Span 구조 (LLM 호출)

```
[HTTP Request Span]
  └── [gen_ai chat Span]          ← gen_ai.operation.name = "chat"
        ├── gen_ai.system = "anthropic"
        ├── gen_ai.request.model = "claude-opus-4-7"
        ├── gen_ai.usage.input_tokens = 1523
        ├── gen_ai.usage.output_tokens = 847
        │
        ├── [Event: gen_ai.user.message]     ← 프롬프트 (opt-in)
        ├── [Event: gen_ai.assistant.message] ← 응답 (opt-in)
        │
        └── [gen_ai tool_call Span]   ← Function calling 시
              ├── gen_ai.tool.name = "search_code"
              └── gen_ai.tool.call.id = "call_abc123"
```

---

## LLM 호출 Tracing 구현

### Spring AI + OTel

```java
@Component
public class GenAITracingAdvisor implements CallAroundAdvisor {

    private final Tracer tracer;

    @Override
    public AdvisedResponse aroundCall(AdvisedRequest request,
            CallAroundAdvisorChain chain) {

        Span span = tracer.spanBuilder("gen_ai chat")
            .setAttribute("gen_ai.system", "anthropic")
            .setAttribute("gen_ai.request.model", getModel(request))
            .setAttribute("gen_ai.request.temperature", getTemperature(request))
            .setAttribute("gen_ai.operation.name", "chat")
            .startSpan();

        try (Scope scope = span.makeCurrent()) {
            AdvisedResponse response = chain.nextAroundCall(request);

            // 응답 메타데이터
            var usage = response.response().getMetadata().getUsage();
            span.setAttribute("gen_ai.usage.input_tokens",
                usage.getPromptTokens());
            span.setAttribute("gen_ai.usage.output_tokens",
                usage.getCompletionTokens());
            span.setAttribute("gen_ai.response.finish_reason",
                getFinishReason(response));

            return response;
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR);
            throw e;
        } finally {
            span.end();
        }
    }
}
```

### Go + OTel

```go
func TraceLLMCall(ctx context.Context, tracer trace.Tracer,
    model string, fn func(context.Context) (*LLMResponse, error)) (*LLMResponse, error) {

    ctx, span := tracer.Start(ctx, "gen_ai chat",
        trace.WithAttributes(
            attribute.String("gen_ai.system", "anthropic"),
            attribute.String("gen_ai.request.model", model),
            attribute.String("gen_ai.operation.name", "chat"),
        ))
    defer span.End()

    resp, err := fn(ctx)
    if err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return nil, err
    }

    span.SetAttributes(
        attribute.Int("gen_ai.usage.input_tokens", resp.Usage.InputTokens),
        attribute.Int("gen_ai.usage.output_tokens", resp.Usage.OutputTokens),
        attribute.String("gen_ai.response.finish_reason", resp.FinishReason),
    )
    return resp, nil
}
```

---

## Token Usage Metrics

### OTel Metrics 정의

```yaml
# OTel Collector — GenAI metrics 수집
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  batch:
    timeout: 5s

  # 토큰 → 비용 변환 (FinOps 연동)
  transform/cost:
    metric_statements:
      - context: datapoint
        statements:
          - set(attributes["estimated_cost_usd"],
              Double(attributes["gen_ai.usage.input_tokens"]) * 0.000003 +
              Double(attributes["gen_ai.usage.output_tokens"]) * 0.000015)

exporters:
  prometheus:
    namespace: genai
    resource_to_telemetry_conversion:
      enabled: true
```

### Grafana 대시보드 쿼리

```promql
# 1. 모델별 토큰 사용량 (input/output)
sum(rate(genai_gen_ai_client_token_usage_total[5m]))
  by (gen_ai_request_model, gen_ai_token_type)

# 2. LLM 호출 지연시간 (p95)
histogram_quantile(0.95,
  sum(rate(genai_gen_ai_client_operation_duration_seconds_bucket[5m]))
    by (le, gen_ai_request_model)
)

# 3. 에러율 (모델별)
sum(rate(genai_gen_ai_client_operation_duration_seconds_count{
  status_code="ERROR"
}[5m])) by (gen_ai_request_model)
/
sum(rate(genai_gen_ai_client_operation_duration_seconds_count[5m]))
  by (gen_ai_request_model)

# 4. 일별 예상 비용
sum(increase(genai_estimated_cost_usd_total[1d]))
  by (gen_ai_request_model)

# 5. Agent 루프 감지 (반복 횟수 이상)
sum(rate(genai_gen_ai_agent_iterations_total[5m]))
  by (gen_ai_agent_name) > 5
```

---

## RAG 파이프라인 Tracing

```
[User Query Span]
  ├── [Embedding Span]                ← 쿼리 임베딩
  │     └── gen_ai.operation.name = "embeddings"
  │
  ├── [Vector Search Span]            ← 유사 문서 검색
  │     ├── db.system = "pgvector"
  │     ├── db.operation = "similarity_search"
  │     └── retrieval.top_k = 5
  │
  ├── [Context Assembly Span]         ← 컨텍스트 조립
  │     └── retrieval.documents_count = 3
  │
  └── [LLM Generation Span]          ← 최종 응답 생성
        ├── gen_ai.usage.input_tokens = 3200
        └── gen_ai.usage.output_tokens = 500
```

---

## Quality & Safety Metrics

### 수집 지표

| 지표 | 설명 | 수집 방법 |
|------|------|---------|
| `gen_ai.response.latency` | 응답 지연시간 | OTel span duration |
| `gen_ai.token.usage` | 토큰 사용량 | API 응답 메타데이터 |
| `gen_ai.error.rate` | 에러 비율 | span status |
| `gen_ai.guardrail.triggered` | 가드레일 트리거 횟수 | 커스텀 counter |
| `gen_ai.response.groundedness` | 응답 근거성 점수 | 자동 평가기 |
| `gen_ai.pii.detected` | PII 감지 횟수 | 필터 이벤트 |
| `gen_ai.cache.hit_rate` | 프롬프트 캐시 적중률 | API 응답 |

### 알림 규칙

```yaml
# PrometheusRule
groups:
  - name: genai-alerts
    rules:
      - alert: GenAIHighErrorRate
        expr: |
          sum(rate(genai_gen_ai_client_operation_duration_seconds_count{
            status_code="ERROR"}[5m]))
          / sum(rate(genai_gen_ai_client_operation_duration_seconds_count[5m]))
          > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "GenAI 에러율 5% 초과"

      - alert: GenAICostSpike
        expr: |
          sum(increase(genai_estimated_cost_usd_total[1h]))
          > 1.5 * sum(increase(genai_estimated_cost_usd_total[1h] offset 1d))
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "GenAI 비용 전일 대비 150% 초과"

      - alert: GenAIAgentLoop
        expr: |
          sum(rate(genai_gen_ai_agent_iterations_total[5m]))
            by (gen_ai_agent_name) > 8
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Agent {{ $labels.gen_ai_agent_name }} 루프 감지"
```

---

## 도구 에코시스템

| 도구 | 역할 | OTel 지원 |
|------|------|----------|
| **OpenLLMetry** | OTel 기반 LLM 관측 라이브러리 | 네이티브 |
| OpenLLMetry Hub | LLM gateway + OTel spans 중앙화 | 네이티브 |
| OpenLLMetry MCP | 프로덕션 telemetry → 개발 도구 | 네이티브 |
| Datadog LLM Obs | 엔터프라이즈 LLM 관측 | v1.37+ |
| Grafana | 대시보드/알림 | Prometheus exporter |
| Langfuse | 오픈소스 LLM 관측 | OTel export 지원 |

### 민감정보 필터링

```yaml
# OTel Collector — 프롬프트/응답 내 PII 마스킹
processors:
  redaction:
    # gen_ai.content.prompt, gen_ai.content.completion 이벤트 필터링
    allow_all_keys: false
    blocked_values:
      - "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z]{2,}\\b"  # 이메일
      - "\\b\\d{3}-\\d{2}-\\d{4}\\b"                             # SSN
      - "\\b\\d{13,16}\\b"                                       # 카드번호
    summary: debug
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 프롬프트/응답 무조건 로깅 | PII 노출, 스토리지 폭증 | opt-in + PII 마스킹 |
| 토큰 메트릭만 수집 | 품질/안전 사각지대 | guardrail + quality metrics |
| 벤더 전용 관측 도구 | 락인, 비교 불가 | OTel GenAI conventions |
| Agent 루프 모니터링 없음 | 비용 폭증 미감지 | iteration count 알림 |
| 비용 메트릭 분리 운영 | FinOps 연동 불가 | OTel → cost 변환 파이프라인 |

---

## 체크리스트

### 계측
- [ ] OTel GenAI semantic conventions 적용
- [ ] LLM 호출 span 생성 (input/output tokens)
- [ ] RAG 파이프라인 전체 trace
- [ ] Agent 워크플로우 span (iterations 포함)

### 메트릭 & 대시보드
- [ ] 토큰 사용량 대시보드 (모델별, 워크플로우별)
- [ ] LLM 지연시간/에러율 패널
- [ ] 비용 추정 대시보드 (FinOps 연동)
- [ ] Agent 루프 감지 알림

### 보안
- [ ] PII 마스킹 파이프라인
- [ ] 프롬프트/응답 로깅 opt-in 정책
- [ ] 감사 로그 보존 정책

---

## 참조 스킬

- `observability-otel.md` — OTel 기본 설정, Collector 구성
- `observability-otel-scale.md` — 대규모 트래픽 OTel 스케일링
- `observability-cost.md` — 관측성 스택 비용 관리
- `finops-ai.md` — AI FinOps, Token Economics
- `agentic-coding.md` — Agentic Coding 패턴, Agent 루프 방지
- `spring-ai.md` — Spring AI Advisor 기반 계측

---

## Sources

- [OTel GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [OTel GenAI Agent Spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)
- [OTel Standardizes LLM Tracing](https://earezki.com/ai-news/2026-03-21-opentelemetry-just-standardized-llm-tracing-heres-what-it-actually-looks-like-in-code/)
- [Datadog OTel GenAI Support](https://www.datadoghq.com/blog/llm-otel-semantic-convention/)
- [OpenLLMetry](https://horovits.medium.com/opentelemetry-for-genai-and-the-openllmetry-project-81b9cea6a771)
