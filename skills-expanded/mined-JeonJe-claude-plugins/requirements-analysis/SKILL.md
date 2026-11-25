---
name: requirements-analysis
description: "PRD 분석해줘, 요구사항 분석해줘, 요구사항 정리해줘, 요구사항 명확히 해줘 요청 시 사용. PRD → 실행 가능한 요구사항 정제 + Plan Seed 생성. 구현은 하지 않음. 이미 요구사항이 확정된 경우나 단일 파일 수정은 제외."
---

# Requirements Analysis (PRD + Plan-Ready)

PRD/요청을 분석해 모호함을 제거하고, Claude가 바로 계획을 세울 수 있는 **Requirements Analysis Packet**을 만든다.
이 단계에서는 코드 구현을 하지 않는다 — 분석 결과의 신뢰가 후속 plan/구현 품질을 결정한다.

## Use Cases

| Input | Action | Output |
|-------|--------|--------|
| "PRD 분석해줘" + PRD 텍스트/파일 | PRD 요약 → scope 분해 → gap 탐지 → 수용기준 → Plan Seed | Requirements Analysis Packet 8 섹션 (요구사항 매트릭스 + Decision + Plan Seed) |
| "요구사항 명확히" + 모호한 기능 요청 | 갭 식별 → 옵션 2-3개 + 권장안 | Decision 목록 + 사용자 확인 후 packet 갱신 |
| "Plan Seed 생성" + 확정 PRD | acceptance criteria + constraints + risks 정리 | 계획 단계 입력용 텍스트 블록 |

## Goal

- PRD를 구현 가능한 단위로 분해
- 누락된 의사결정을 드러내고 질문으로 확정
- 작업계획 품질이 높아지도록 입력 품질을 고정

## Quality Bar

1. 요구사항은 검증 가능한 문장(pass/fail)이어야 한다.
2. 사실(Fact)과 가정(Assumption)을 분리한다.
3. 범위(In/Out)를 분명히 나눈다.
4. 핵심 리스크와 대응을 우선순위로 제시한다.
5. 다음 단계(계획)에서 바로 쓸 수 있는 패킷으로 끝낸다.

## Workflow

0. **(조건부) 환경 제약사항 조사** — 외부 평가자가 있거나 시간이 제한된 작업(코딩 테스트, 해커톤, 클라이언트 데모)일 때만. 착수 전에 작업 환경의 제약을 조사해 packet의 제약·우선순위로 주입한다:
   - **형식**: 제한 시간, 필수/선택 과제 분리 여부와 개수, 제출 후 구술 질문(내 산출물 설명) 유무
   - **도구 정책**: AI 도구 허용 범위, 평소 쓰던 개인 하네스·설정·플러그인 반입 가능 여부 (가능하면 반입이 곧 준비)
   - **평가 신호**: 주최측 기술 블로그의 채점 파이프라인/평가 철학 글, 이전 회차 응시 후기, 회사 스택 — "무엇을 채점하나"(코드 완성도만인가, 문제 정의·프롬프트·검증 과정까지인가)를 추정
   - **과정 기록형 평가 도구**(전용 IDE/평가 솔루션에서 프롬프트·반복 과정 자체가 기록·채점되는 형식)가 확인되면: AI 협업 기록은 제출용으로 나중에 정리하는 게 아니라 **작업 중 실시간으로 남는 것** — 프롬프트 하나하나가 채점 대상이라는 전제로 작업한다
   - 조사 결과 → §4 Constraints에 "환경 제약"으로, 필수/선택 구조 → 계획 단계의 Cutline에 매핑
1. **PRD 요약**: 문제/목표/대상 사용자/성공지표를 1-2문장으로 재정의
2. **요구사항 분해**: 기능/비기능/제약(기술, 일정, 정책) 분리
   - **(조건부) 기능 What tree**: 기능 3개 초과 또는 In/Out 경계 모호 시, 요청 목표 → 하위기능 → leaf로 분해하는 What tree 1장을 먼저 그린다. 각 leaf가 §3 Requirement Matrix의 한 행 — 분해 완전성("빠짐없이 덮었나")을 강제. 기능이 단순·명백하면 생략하고 바로 매트릭스로.
3. **갭 탐지**: 누락 결정사항과 모호한 표현 식별
   - **(조건부) 퀘스천맵**: 빠진 관점 발굴이 목적일 때, 중심 "이 PRD에서 무엇을 물어야 하나"에서 scope / behavior / data / constraints / edge / 실패모드로 방사한다. 미응답으로 남은 가지(갭)가 §5 Decision 항목으로 승격. (대화형 명확화가 이미 진행 중이면 생략 — 정적 분석용일 때만)
4. **의사결정 제안**: 각 갭마다 옵션 2-3개 + 트레이드오프 + 권장안
5. **수용기준 작성**: Given/When/Then 또는 측정 가능한 pass/fail 기준으로 명시 — 비검증 가능한 문장은 후속 단계에서 해석 차이 유발
6. **계획 입력 패킷 생성**: 아래 고정 포맷으로 출력
7. 본 단계에서 코드 구현 금지 — 패킷 신뢰가 후속 plan/구현 품질을 결정

> 사고 도구 역할 분리: **What tree = 분해 완전성**(step2, 빠짐없이 덮었나) / **퀘스천맵 = 갭 발굴**(step3, 무엇을 못 물었나). 둘 다 조건부 — 단순하면 생략.

## Output Format (Fixed)

### 1) PRD Snapshot
- Problem:
- Target User:
- Business Goal:
- Success Metric:

### 2) Scope Definition
- In-Scope:
- Out-of-Scope:

### 3) Requirement Matrix

**(조건부) 기능 What tree** — 기능 3개 초과 또는 In/Out 모호 시, 아래 표 위에 1장(코드블록). leaf = 표의 행.

```
<요청 목표 전체>
├ <하위기능1>
│  ├ <leaf = 요구사항 행>
│  └ <leaf>
├ <하위기능2>
└ ...
```

| ID | Requirement | Type(F/NF) | Priority | Why it matters | Verification |
|----|-------------|------------|----------|----------------|--------------|

### 4) Constraints
- Technical:
- Policy/Compliance:
- Timeline/Resource:

### 5) Gaps & Decisions

> (조건부) step3 퀘스천맵의 미응답 가지 = 여기 Decision 항목으로 승격.

- [ ] Decision: ...
  - Options: A / B / C
  - Trade-off:
  - Recommended:

### 6) Acceptance Criteria (Testable)
1. Given ... When ... Then ...
2. Given ... When ... Then ...

### 7) Risk Register
| Risk | Impact | Likelihood | Mitigation | Trigger |
|------|--------|------------|------------|---------|

### 8) Plan Seed (계획 단계 입력)
```text
[OBJECTIVE]
...

[IN-SCOPE]
...

[OUT-OF-SCOPE]
...

[MUST-HAVE ACCEPTANCE CRITERIA]
...

[CONSTRAINTS]
...

[OPEN DECISIONS]
...

[TOP RISKS]
...
```

## Completion Criteria

- 수용기준이 Given/When/Then 또는 측정 가능한 pass/fail 형태로 작성됨
- 모호한 요구사항이 Decision 항목으로 분리됨
- 계획 단계(`plan-quick`)에 바로 넘길 수 있는 Plan Seed 포함
- 본 단계에서 코드 구현이 발생하지 않음

## Next Step

- 의사결정이 남아 있으면 먼저 확정
- 확정 후 `plan-quick`으로 작업계획 수립
