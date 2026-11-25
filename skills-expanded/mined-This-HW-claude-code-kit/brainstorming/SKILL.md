---
name: brainstorming
description: Design and spec before any planning or code. MUST USE before new features, creative work, or any implementation. Explores requirements, proposes approaches, gets design approval, then chains to plan-task.
---

# Brainstorming

설계 승인 없이 plan-task를 invoke하거나 코드를 작성하면 안 됩니다.

<HARD-GATE>
plan-task 호출, 코드 작성, 파일 생성 — 어떤 구현 행동도 사용자가 설계를 승인하기 전까지 금지입니다. 작업이 단순해 보여도 예외 없음.
</HARD-GATE>

## 체크리스트

진입 즉시 ToolSearch("select:TaskCreate,TaskUpdate,TaskList")로 Task 도구를 로드한 후,

> **Task 도구가 없으면 멈추지 말고 대체 경로로 간다** — `ToolSearch`가 Task 계열을
> 반환하지 않는 호스트/세션이 있다(F-038). 그때는 `./scripts/checklist.sh` 기반
> durable checklist로 추적한다. 규율 SSOT: `skills/plan-task/references/task-tools-fallback.md`.
아래 항목 각각에 대해 TaskCreate를 실행하세요.

**Task 네이밍 규약:** `[Brainstorm] {항목명}` (plan-task의 `[Planning]` Task와 구분)
**완료 마킹 규약 [건너뛰기 금지]:** 각 항목을 마치면 **즉시** `TaskUpdate(status="completed")`,
마지막 항목(plan-task invoke)은 **invoke 직전에** 마킹 (규율 SSOT:
`rules/definition-of-done.md#task-마감-규율`).
**work_id metadata:** brainstorming 단계에서는 Work ID가 없으므로 `{"phase": "brainstorming"}`만 사용

1. 프로젝트 컨텍스트 파악 (파일, 최근 커밋, docs)
2. 명확화 질문 (한 번에 하나씩)
3. 2-3가지 접근법 + 추천
4. 설계 제시 및 사용자 승인
5. 스펙 문서 작성 (`docs/specs/YYYY-MM-DD-{topic}.md`)
6. 스펙 자가 검토 (플레이스홀더, 모순, 모호성)
7. 사용자 스펙 검토 대기
8. `plan-task` invoke

## 프로세스

### 1단계: 컨텍스트 파악

- 관련 파일, README, 최근 커밋 확인
- 규모 판단: 복수의 독립 서브시스템이면 분해 먼저 제안

### 2단계: 명확화 질문

- 한 번에 하나의 질문만
- 목적, 제약, 성공 기준에 집중
- 가능하면 객관식 선택지 제공

### 3단계: 접근법 제안

- 2-3가지 접근법과 트레이드오프
- 추천안과 이유를 먼저 제시

### 4단계: 설계 제시

- 각 섹션을 순서대로 제시하고 승인 확인
- 아키텍처, 컴포넌트, 데이터 흐름, 에러 처리, 테스트 전략 포함
- 수정 요청 시 해당 섹션 재작성

### 5단계: 스펙 문서 작성

**저장 경로:** `docs/specs/YYYY-MM-DD-{topic}.md`
(`docs/works/` 있으면 해당 Work와 연결)

스펙 문서 구조:
```markdown
# {Topic} 설계

**Goal:** [한 문장]
**Architecture:** [2-3 문장]

## 요구사항
## 접근 방식
## 컴포넌트 구조
## 데이터 흐름
## 에러 처리
## 테스트 전략
## 범위 외
```

### 6단계: 자가 검토

1. **플레이스홀더 스캔:** TBD, TODO, 미완성 섹션 → 즉시 수정
2. **일관성:** 섹션 간 모순 없는지 확인
3. **범위:** 단일 plan으로 구현 가능한가?
4. **모호성:** 두 가지로 해석 가능한 요구사항 → 명확화

### 7단계: 사용자 검토 대기

> 세션 경계 주의: 이 단계에서 세션이 끝나면 대기 태스크가 다음 세션에 잔존한다 —
> 정상이다. 재개 판단 기준은 `docs/specs/`의 스펙 파일 (rules/task-resume.md 참고).

```
스펙을 `{path}`에 저장했습니다. 검토 후 수정 사항이 있으면 말씀해 주세요.
승인되면 plan-task로 넘어갑니다.
```

수정 요청 시 → 수정 후 자가 검토 재실행
승인 시 → 8단계

### 8단계: plan-task invoke

```
설계 승인 완료. plan-task를 시작합니다.
```

`plan-task` 스킬을 invoke합니다. (Skill 도구 사용)
