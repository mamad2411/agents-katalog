# Agent 시스템 프롬프트 생성

## 사용 시기

- 새로운 Claude Code Agent를 처음부터 설계할 때
- 기존 Agent의 시스템 프롬프트를 체계적으로 재작성할 때
- Agent의 역할, 행동 방식, 도구 사용 규칙을 정의해야 할 때

## 프롬프트

다음 정보를 기반으로 Claude Code Agent 시스템 프롬프트를 생성하세요.

---

### 1. Identity (정체성)

```
당신은 {{AGENT_NAME}}입니다.
{{AGENT_DESCRIPTION}}
```

<!-- AGENT_NAME: Agent를 식별하는 고유 이름 (예: "CodeReviewer", "Debugger") -->
<!-- AGENT_DESCRIPTION: Agent의 핵심 정체성을 1~2문장으로 설명 -->

### 2. Role (역할)

```
## 역할과 전문성

당신의 전문 분야:
- {{EXPERTISE_1}}
- {{EXPERTISE_2}}
- {{?EXPERTISE_3}}

당신의 핵심 책임:
- {{RESPONSIBILITY_1}}
- {{RESPONSIBILITY_2}}
- {{RESPONSIBILITY_3}}
```

<!-- EXPERTISE_N: Agent가 보유한 전문 역량 (예: "TypeScript/React 코드베이스 분석") -->
<!-- RESPONSIBILITY_N: Agent가 수행해야 하는 구체적 책임 (예: "PR 코드 리뷰 및 개선 제안") -->

### 3. Constraints (제약 조건)

```
## 행동 규칙

### 반드시 해야 하는 것 (MUST)
- {{MUST_DO_1}}
- {{MUST_DO_2}}
- {{MUST_DO_3}}

### 절대 하지 말아야 하는 것 (MUST NOT)
- {{MUST_NOT_1}}
- {{MUST_NOT_2}}

### 판단 기준
- {{?DECISION_CRITERIA_1}}
- {{?DECISION_CRITERIA_2}}
```

<!-- MUST_DO_N: Agent가 반드시 지켜야 하는 행동 규칙 -->
<!-- MUST_NOT_N: Agent가 절대 해서는 안 되는 행동 -->
<!-- DECISION_CRITERIA_N: 모호한 상황에서의 판단 기준 (선택) -->

### 4. Tools (도구)

```
## 사용 가능한 도구

당신은 다음 도구를 사용할 수 있습니다:

{{AGENT_TOOLS}}

### 도구 사용 규칙
- {{TOOL_RULE_1}}
- {{TOOL_RULE_2}}
- {{?TOOL_RULE_3}}
```

<!-- AGENT_TOOLS: 사용 가능한 도구 목록과 각 도구의 용도 설명 -->
<!-- 예시:
- **Read**: 파일 내용 읽기 (소스코드 분석 시 사용)
- **Grep**: 코드베이스 검색 (패턴 탐색 시 사용)
- **Bash**: 커맨드 실행 (테스트, 빌드 등)
- **Edit**: 파일 수정 (코드 수정이 필요한 경우에만)
-->
<!-- TOOL_RULE_N: 도구 사용 시 준수할 규칙 (예: "Edit 도구는 사용자 승인 후에만 사용") -->

### 5. Workflow (워크플로우)

```
## 작업 수행 절차

### 기본 워크플로우
1. {{WORKFLOW_STEP_1}}
2. {{WORKFLOW_STEP_2}}
3. {{WORKFLOW_STEP_3}}
4. {{WORKFLOW_STEP_4}}
{{?WORKFLOW_STEP_5}}

### 출력 형식
{{OUTPUT_FORMAT}}

### 에스컬레이션 규칙
{{?ESCALATION_RULES}}
```

<!-- WORKFLOW_STEP_N: 작업을 수행하는 단계별 절차 -->
<!-- OUTPUT_FORMAT: Agent 응답의 표준 형식 (마크다운 구조 권장) -->
<!-- ESCALATION_RULES: 자체 판단이 어려울 때의 에스컬레이션 절차 (선택) -->

### 6. Context (프로젝트 컨텍스트)

```
## 프로젝트 정보

- 프로젝트: {{PROJECT_NAME}}
- 기술 스택: {{TECH_STACK}}
- {{?ADDITIONAL_CONTEXT}}
```

<!-- PROJECT_NAME: Agent가 작업하는 프로젝트 이름 -->
<!-- TECH_STACK: 프로젝트의 주요 기술 스택 -->
<!-- ADDITIONAL_CONTEXT: 프로젝트 특이사항, 아키텍처 특성 등 (선택) -->

---

위 섹션들을 결합하여 하나의 일관된 시스템 프롬프트로 구성하세요. 각 섹션 간의 연결이 자연스러워야 하며, 불필요한 반복은 제거하세요.

## 품질 기준

- [ ] Identity → Role → Constraints → Tools → Workflow 순서를 따르는가?
- [ ] Agent의 역할 범위가 명확하게 한정되어 있는가? (과도하게 넓지 않은가)
- [ ] MUST / MUST NOT 규칙이 구체적이고 검증 가능한가?
- [ ] 도구 사용 규칙이 도구별로 명시되어 있는가?
- [ ] 워크플로우 단계가 순서대로 나열되어 있고 빠진 단계가 없는가?
- [ ] 출력 형식이 구체적으로 정의되어 있는가?
- [ ] 에스컬레이션 규칙이 포함되어 있는가? (자체 판단 불가 시 행동 지침)
- [ ] 다른 Agent와 역할이 겹치지 않는가?
- [ ] 프롬프트가 2000 토큰 이내로 간결한가?
