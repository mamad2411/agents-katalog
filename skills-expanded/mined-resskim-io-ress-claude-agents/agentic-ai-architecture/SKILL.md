---
name: agentic-ai-architecture
category: architecture
description: "Agentic AI Architecture 가이드 — AI Agent 시스템 설계, MCP/A2A 프로토콜, Multi-Agent 오케스트레이션, Spring AI/Go 구현 패턴 Use when working with architecture 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Agentic AI Architecture 가이드

AI Agent 시스템 설계, MCP/A2A 프로토콜, Multi-Agent 오케스트레이션, Spring AI/Go 구현 패턴

## Quick Reference (결정 트리)

```
AI 시스템 아키텍처 선택?
├── 단순 LLM 호출 (Q&A, 요약) ──────────> RAG + Prompt Engineering
├── 외부 시스템 연동 필요 ──────────────> Single Agent + Tool Use (MCP)
├── 복잡한 단일 워크플로우 ─────────────> Single Agent + Chain Pattern
├── 다중 전문가 협업 필요 ──────────────> Multi-Agent Orchestration
│   ├── 중앙 제어 필요 ────────────────> Orchestrator-Worker
│   ├── 순차 파이프라인 ───────────────> Chain Pattern
│   ├── 품질 검증 루프 ────────────────> Evaluator-Optimizer
│   └── 독립 병렬 처리 ────────────────> Parallel + Aggregator
└── 크로스 조직 Agent 통신 ─────────────> A2A (Agent2Agent) Protocol

Agent 상태 관리?
├── 단발성 요청 (stateless) ────────────> Function Calling
├── 대화 컨텍스트 유지 ────────────────> Session Memory (Redis/DB)
├── 장기 실행 워크플로우 ──────────────> Checkpoint + Resume (Temporal)
└── 멀티턴 협업 ───────────────────────> Shared State Store
```

---

## CRITICAL: 핵심 프로토콜 비교

### MCP vs A2A

```
┌─────────────────────────────────────────────────────────┐
│                    Agentic AI Stack                      │
│                                                         │
│  ┌─────────┐  A2A Protocol  ┌─────────┐               │
│  │ Agent A │<──────────────>│ Agent B │  Agent 간 통신  │
│  └────┬────┘                └────┬────┘               │
│       │ MCP                      │ MCP                 │
│  ┌────┴────┐                ┌────┴────┐               │
│  │ Tools   │                │ Tools   │  도구/데이터    │
│  │ & Data  │                │ & Data  │  접근          │
│  └─────────┘                └─────────┘               │
└─────────────────────────────────────────────────────────┘
```

| 항목 | MCP (Model Context Protocol) | A2A (Agent2Agent Protocol) |
|------|------------------------------|---------------------------|
| **목적** | Agent ↔ Tool/데이터 연결 | Agent ↔ Agent 통신 |
| **주체** | Anthropic 주도 | Google 주도 |
| **통신 방식** | JSON-RPC 2.0 (stdio/SSE/HTTP) | HTTP + JSON-RPC / SSE |
| **핵심 개념** | Tool, Resource, Prompt | AgentCard, Task, Artifact |
| **발견 메커니즘** | MCP Server manifest | /.well-known/agent.json |
| **상태 관리** | Stateless (Tool 호출) | Stateful (Task lifecycle) |
| **보안** | OAuth 2.1 (2025 spec) | Enterprise Auth + RBAC |
| **적합 시나리오** | DB 조회, API 호출, 파일 접근 | 주문→결제→배송 Agent 협업 |

---

## CRITICAL: Agent 아키텍처 패턴

### 1. Orchestrator-Worker 패턴

```
                    ┌──────────────────┐
                    │   Orchestrator   │
                    │    (중앙 제어)     │
                    └──┬─────┬──────┬──┘
                       │     │      │
              ┌────────┘     │      └────────┐
              v              v               v
        ┌──────────┐  ┌──────────┐   ┌──────────┐
        │ Worker A │  │ Worker B │   │ Worker C │
        │ (재고확인) │  │ (결제처리) │   │ (배송예약) │
        └──────────┘  └──────────┘   └──────────┘
```

- Orchestrator가 태스크를 분해하고 Worker에 분배
- 각 Worker는 독립적 전문 Agent (MCP Tool 보유)
- 결과 통합 및 오류 처리를 Orchestrator가 담당

### 2. Chain (순차 파이프라인)

```
[입력] → Agent A → Agent B → Agent C → [출력]
         (분석)     (생성)     (검증)
```

### 3. Evaluator-Optimizer (생성 + 검증 루프)

```
[입력] → Generator Agent ──→ Evaluator Agent ──→ [통과] → [출력]
              ^                    │
              └────── [재생성] ─────┘
                    (max 3 iterations)
```

### 4. Parallel (병렬 실행 + 결과 통합)

```
         ┌→ Agent A (시장 분석) ──┐
[입력] ──┼→ Agent B (경쟁사 분석) ─┼→ Aggregator → [출력]
         └→ Agent C (재무 분석) ──┘
```

### 패턴 선택 비교

| 패턴 | 복잡도 | 지연시간 | 적합 사례 |
|------|--------|---------|-----------|
| Orchestrator-Worker | 높음 | 중간 | 주문 처리, 멀티스텝 워크플로우 |
| Chain | 낮음 | 높음 (순차) | 문서 분석 → 요약 → 번역 |
| Evaluator-Optimizer | 중간 | 높음 (반복) | 코드 생성 + 리뷰, 콘텐츠 검수 |
| Parallel | 중간 | 낮음 (병렬) | 다차원 분석, 보고서 생성 |

---

## CRITICAL: Spring AI 구현

### A2A Server 설정

```java
// Agent 역할 정의 (AgentCard)
@Configuration
public class A2AConfig {

    @Bean
    public AgentCard agentCard() {
        return AgentCard.builder()
            .name("order-agent")
            .description("주문 처리 전문 Agent")
            .url("https://order-agent.internal:8080")
            .capabilities(new AgentCapabilities(
                List.of("order-processing", "inventory-check"),
                true,  // streaming 지원
                true   // pushNotifications 지원
            ))
            .authentication(AuthType.BEARER)
            .build();
    }

    // A2A Task 처리 엔드포인트
    @Bean
    public TaskHandler taskHandler(OrderOrchestrator orchestrator) {
        return TaskHandler.builder()
            .onTask("process-order", orchestrator::processOrder)
            .onTask("check-status", orchestrator::checkStatus)
            .build();
    }
}
```

### MCP Tool 등록

```java
@McpTool
public class OrderTools {

    @Tool("get-order-status")
    @Description("주문 상태 조회")
    public OrderStatus getOrderStatus(
            @Param("orderId") String orderId) {
        return orderRepository.findStatusById(orderId);
    }

    @Tool("create-order")
    @Description("신규 주문 생성")
    public OrderResult createOrder(
            @Param("items") List<OrderItem> items,
            @Param("customerId") String customerId) {
        // 입력 검증 Guardrail
        validateOrderItems(items);
        return orderService.create(items, customerId);
    }
}
```

### Multi-Agent Orchestrator (Orchestrator-Worker)

```java
@Service
public class OrderOrchestrator {
    private final ChatClient chatClient;
    private final A2AClient a2aClient;

    public OrderResult processOrder(OrderRequest request) {
        // Step 1: 재고 확인 Agent 호출 (A2A)
        Task inventoryTask = a2aClient
            .sendTask("inventory-agent", new TaskRequest(
                "check-availability",
                Map.of("items", request.getItems())
            ));

        if (!inventoryTask.isSuccess()) {
            return OrderResult.failed("재고 부족: " + inventoryTask.getError());
        }

        // Step 2: 결제 처리 Agent 호출 (A2A)
        Task paymentTask = a2aClient
            .sendTask("payment-agent", new TaskRequest(
                "process-payment",
                Map.of("amount", request.getTotalAmount(),
                       "method", request.getPaymentMethod())
            ));

        if (!paymentTask.isSuccess()) {
            // 보상: 재고 예약 해제
            a2aClient.sendTask("inventory-agent",
                new TaskRequest("release-reservation",
                    Map.of("reservationId", inventoryTask.getArtifact("reservationId"))));
            return OrderResult.failed("결제 실패");
        }

        // Step 3: 배송 Agent 호출
        Task shippingTask = a2aClient
            .sendTask("shipping-agent", new TaskRequest(
                "schedule-delivery",
                Map.of("orderId", request.getOrderId(),
                       "address", request.getShippingAddress())
            ));

        return OrderResult.success(inventoryTask, paymentTask, shippingTask);
    }
}
```

### Guardrails 구현 (Spring AI)

```java
@Component
public class AgentGuardrails {

    // Input Guardrail: 프롬프트 인젝션 방지
    @Bean
    public InputGuardrail promptInjectionGuard() {
        return input -> {
            if (containsInjectionPattern(input.text())) {
                return GuardrailResult.block("프롬프트 인젝션 감지");
            }
            return GuardrailResult.pass();
        };
    }

    // Output Guardrail: 민감정보 마스킹
    @Bean
    public OutputGuardrail piiMaskingGuard() {
        return output -> {
            String masked = maskPII(output.text());  // 주민번호, 카드번호 등
            return GuardrailResult.pass(masked);
        };
    }

    // Token Budget 제한
    @Bean
    public TokenBudgetAdvisor tokenBudget() {
        return TokenBudgetAdvisor.builder()
            .maxTokensPerRequest(4096)
            .maxTokensPerSession(50_000)
            .onExceed(BudgetAction.REJECT_WITH_SUMMARY)
            .build();
    }
}
```

---

## Go 구현

### MCP Server

```go
package main

import "github.com/mark3labs/mcp-go/server"

type OrderMCPServer struct {
    srv *server.MCPServer
}

func NewOrderMCPServer() *OrderMCPServer {
    s := server.NewMCPServer("order-mcp", "1.0.0")

    // Tool 등록
    s.AddTool(mcp.NewTool("get-order-status",
        mcp.WithDescription("주문 상태 조회"),
        mcp.WithString("orderId", mcp.Required()),
    ), handleGetOrderStatus)

    s.AddTool(mcp.NewTool("create-order",
        mcp.WithDescription("신규 주문 생성"),
        mcp.WithObject("items", mcp.Required()),
    ), handleCreateOrder)

    return &OrderMCPServer{srv: s}
}

func handleGetOrderStatus(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
    orderId := req.Params.Arguments["orderId"].(string)
    status, err := orderRepo.GetStatus(ctx, orderId)
    if err != nil {
        return mcp.NewToolResultError(err.Error()), nil
    }
    return mcp.NewToolResultText(status.String()), nil
}
```

### A2A Agent

```go
type AgentCard struct {
    Name         string   `json:"name"`
    Description  string   `json:"description"`
    URL          string   `json:"url"`
    Capabilities []string `json:"capabilities"`
}

type Agent struct {
    card     AgentCard
    executor TaskExecutor
    tools    *OrderMCPServer
}

// Multi-Agent Orchestrator
func (a *Agent) Orchestrate(ctx context.Context, req OrderRequest) (*OrderResult, error) {
    g, gCtx := errgroup.WithContext(ctx)

    var inventoryResult, paymentResult *TaskResult

    // 병렬 실행 가능한 태스크
    g.Go(func() error {
        var err error
        inventoryResult, err = a.callAgent(gCtx, "inventory-agent", "check", req.Items)
        return err
    })

    if err := g.Wait(); err != nil {
        return nil, fmt.Errorf("inventory check failed: %w", err)
    }

    // 순차 실행: 결제 → 배송
    paymentResult, err := a.callAgent(ctx, "payment-agent", "process", req.Payment)
    if err != nil {
        a.callAgent(ctx, "inventory-agent", "rollback", inventoryResult.ReservationID)
        return nil, fmt.Errorf("payment failed: %w", err)
    }

    return &OrderResult{
        Inventory: inventoryResult,
        Payment:   paymentResult,
    }, nil
}
```

---

## 안전장치 (Guardrails) 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                    Agent Pipeline                         │
│                                                          │
│  [User Input]                                            │
│       │                                                  │
│       v                                                  │
│  ┌─────────────────┐                                    │
│  │ Input Guardrail │ ← 프롬프트 인젝션, 유해 콘텐츠 차단  │
│  └────────┬────────┘                                    │
│           v                                              │
│  ┌─────────────────┐     ┌──────────────┐              │
│  │   LLM Agent     │────>│  Tool Call   │ ← RBAC 권한   │
│  └────────┬────────┘     └──────────────┘              │
│           v                                              │
│  ┌─────────────────┐                                    │
│  │ Output Guardrail│ ← PII 마스킹, 환각 검증            │
│  └────────┬────────┘                                    │
│           v                                              │
│  ┌─────────────────┐                                    │
│  │ Human-in-Loop   │ ← 고위험 작업 승인 (금액 > 100만원) │
│  └────────┬────────┘                                    │
│           v                                              │
│      [Response]                                          │
└──────────────────────────────────────────────────────────┘
```

### 핵심 안전장치 항목

| 카테고리 | 기법 | 설명 |
|---------|------|------|
| Input | Prompt Injection 탐지 | 악의적 프롬프트 패턴 필터링 |
| Input | Schema Validation | 입력 파라미터 타입/범위 검증 |
| Execution | RBAC + 최소 권한 | Agent별 Tool 접근 권한 제한 |
| Execution | Rate Limiting | Agent별 분당 호출 수 제한 |
| Execution | Token Budget | 요청/세션별 토큰 상한 설정 |
| Execution | Max Iterations | 무한 루프 방지 (기본 10회) |
| Execution | Timeout | Agent 실행 시간 제한 (기본 120s) |
| Output | PII Masking | 개인정보 자동 마스킹 |
| Output | Hallucination Check | Tool 결과와 응답 교차 검증 |
| Audit | 감사 로그 | 모든 Agent 행동 로깅 |
| Cost | 비용 대시보드 | 토큰 사용량 + 비용 실시간 추적 |

---

## 기업 도입 현황 (Gartner/Deloitte 2025-2026)

- Gartner 예측: **2028년까지 기업 소프트웨어 33%에 Agentic AI 내장** (2024년 1% 미만)
- Deloitte 조사: 기업의 25%가 Agentic AI 파일럿 진행 중, **14%만 프로덕션 배포 준비 완료**
- 주요 장벽: 보안/거버넌스 (47%), 비용 예측 어려움 (35%), 기존 시스템 통합 (31%)

### 성숙도 모델

```
Level 1: Chatbot       → 단순 Q&A, RAG 기반 정보 검색
Level 2: Tool-Using    → LLM + 외부 API/DB 연동 (MCP)
Level 3: Single Agent  → 자율적 계획 수립 + 실행 + 검증
Level 4: Multi-Agent   → 전문 Agent 간 협업 오케스트레이션
Level 5: Autonomous    → 크로스 조직 Agent 네트워크 (A2A)
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Agent에 과도한 권한 부여 | 의도치 않은 데이터 수정/삭제 | RBAC + 최소 권한 원칙, Tool별 권한 분리 |
| 무한 루프 (Agent 자기 호출) | 리소스 고갈, 비용 폭발 | Max iterations (10) + timeout (120s) |
| LLM 비용 무제한 허용 | 월 수천만원 비용 발생 | Token budget + 응답 캐싱 + 모델 티어링 |
| 모든 작업에 Agent 적용 | 불필요한 복잡성, 높은 지연 | 결정적 로직은 기존 코드, AI는 판단 영역만 |
| Agent 출력 무검증 사용 | 환각(Hallucination) 전파 | Output Guardrail + 사실 검증 체인 |
| 동기식 Agent 체인 | 높은 지연, 장애 전파 | 비동기 + 이벤트 기반 + 타임아웃 |
| 상태 공유 없는 멀티 Agent | 중복 작업, 일관성 깨짐 | Shared State Store (Redis) + 체크포인트 |
| 관측성 부재 | 디버깅 불가, 장애 원인 미상 | OTel 추적 + Agent별 메트릭 + 비용 대시보드 |

---

## 체크리스트

### 설계 단계
- [ ] 각 Agent의 역할과 책임 범위를 명확히 정의했는가?
- [ ] Agent 아키텍처 패턴을 결정했는가? (Orchestrator/Chain/Parallel)
- [ ] MCP Tool 목록과 각 Tool의 입출력 스키마를 정의했는가?
- [ ] Agent 간 통신 프로토콜을 결정했는가? (내부: 직접 호출 / 외부: A2A)
- [ ] 실패 시 보상 로직과 Fallback 전략을 설계했는가?
- [ ] Human-in-the-loop 대상 작업을 식별했는가?

### 구현 단계
- [ ] Input/Output Guardrail을 적용했는가?
- [ ] Token Budget과 Rate Limiting을 설정했는가?
- [ ] Max Iterations와 Timeout을 설정했는가?
- [ ] Agent 상태 관리 방식을 구현했는가? (Stateful: 체크포인트)
- [ ] 멱등성(Idempotency)을 보장하는가?
- [ ] 에러 처리와 보상 트랜잭션을 구현했는가?

### 운영 단계
- [ ] Agent 행동에 대한 감사 로그를 수집하는가?
- [ ] 토큰 사용량/비용 모니터링 대시보드를 구축했는가?
- [ ] Agent 응답 품질 메트릭을 추적하는가? (정확도, 환각 비율)
- [ ] 장애 시 Agent 자동 복구(Circuit Breaker)를 적용했는가?
- [ ] A/B 테스트로 Agent 성능을 지속 개선하는가?

### 보안 단계
- [ ] Agent별 RBAC 권한을 최소 권한 원칙으로 설정했는가?
- [ ] Prompt Injection 방어 레이어를 적용했는가?
- [ ] PII/민감정보 마스킹을 Output Guardrail에 포함했는가?
- [ ] Agent가 접근하는 Tool/API의 인증/인가를 검증했는가?
- [ ] 모델 업데이트 시 회귀 테스트를 수행하는가?

---

## 참조 스킬

- `/msa-event-driven` - 이벤트 드리븐 아키텍처 (Agent 비동기 통신 기반)
- `/msa-saga` - Saga 패턴 (Agent 오케스트레이션과 보상 트랜잭션)
- `/dx-ai-agents` - AI Agent 개발 가이드라인 (프롬프트, 메모리)
- `/dx-ai-agents-orchestration` - Agent 오케스트레이션 패턴 상세
- `/msa-resilience` - 서킷브레이커, Retry, Bulkhead (Agent 안정성)
- `/observability-otel` - OpenTelemetry 기반 Agent 추적

## 참고 레퍼런스

- [Google A2A Protocol](https://github.com/google/A2A) -- Agent2Agent 공식 스펙
- [MCP Specification](https://modelcontextprotocol.io/) -- Model Context Protocol 공식 문서
- [Spring AI MCP](https://docs.spring.io/spring-ai/reference/api/mcp.html) -- Spring AI MCP 통합
- [Anthropic Agent Patterns](https://www.anthropic.com/engineering/building-effective-agents) -- 효과적인 Agent 설계
- [Gartner Agentic AI](https://www.gartner.com/en/topics/agentic-ai) -- 2026 기업 AI 트렌드
- [Deloitte Agentic AI Report](https://www2.deloitte.com/us/en/pages/consulting/articles/agentic-ai.html) -- 기업 도입 현황
