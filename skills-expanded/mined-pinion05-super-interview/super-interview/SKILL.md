---
name: super-interview
description: "OMX의 실행 전 명확화 discipline과 Superpowers brainstorming, deep-interview의 장점을 합쳐 Discovery → Design → 승인 가능한 spec으로 수렴시키는 통합 skill."
version: 1.0.0
author: pinion05
license: MIT
metadata:
  tags: [requirements, clarification, design, specification, brownfield, readiness, ambiguity, discovery, planning]
  related_skills: [writing-plans]
  argument_hint: "[--quick|--standard|--deep] [--show-scores] [--autoresearch] [--threshold 0.20] <topic or change request>"
  outputs: [docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md]
  optional_outputs: [readiness-report.json, discovery-state.json]
  inspired_by: [omx, brainstorming, deep-interview]
---

# super-interview

구현 전에 요구사항을 명확화하고, 필요한 수준만큼 탐색한 뒤, 승인 가능한 설계 spec으로 정리하는 통합 skill.

핵심은 단순하다.
- OMX처럼 성급히 구현하지 않고 먼저 의도와 경계를 명확히 한다.
- Superpowers의 `brainstorming`처럼 discovery 뒤에 design gate와 canonical spec으로 수렴한다.
- `deep-interview`처럼 ambiguity를 체계적으로 줄이고 readiness를 판단한다.

즉, 이 스킬은 discovery와 design을 하나의 흐름으로 묶되, 둘을 섞지 않는다.
항상 먼저 ambiguity를 줄이고, 충분히 명확해졌을 때만 설계로 넘어간다.

<HARD-GATE>
사용자에게 검토 가능한 설계를 제시하고 승인을 받기 전까지는:
- 구현 스킬을 호출하지 않는다.
- 코드를 작성하지 않는다.
- 스캐폴딩이나 실행 가능한 구현 행동을 하지 않는다.
</HARD-GATE>

이 게이트는 작은 요청에도 적용되지만, 작은 요청은 discovery와 design을 아주 짧게 압축할 수 있다.

## 기본 철학

1. 항상 discovery는 하되, 깊이는 적응적으로 조절한다.
- simple task라서 discovery를 생략하지 않는다.
- 이미 확인 가능한 사실을 먼저 확인한 뒤, 필요한 최소 질문만 던진다.

2. 질문 단계와 설계 단계를 섞지 않는다.
- discovery 중에는 ambiguity를 줄인다.
- readiness에 도달하기 전에는 설계를 밀어붙이지 않는다.
- readiness 이후에만 옵션 비교와 설계 합성을 시작한다.

3. canonical artifact는 하나를 기본값으로 유지한다.
- 기본 산출물은 design spec 한 파일이다.
- deep mode에서만 readiness/state를 추가 산출물로 남긴다.
- transcript, assumptions, key entities는 가능하면 spec appendix에 넣는다.

4. 구현 전 handoff는 하나로 고정한다.
- spec 승인 전에는 구현으로 가지 않는다.
- 승인 후 다음 planning 단계는 `writing-plans` 하나만 사용한다.

## 언제 쓰는가

### `--quick`
- 이미 요청이 구체적이거나 작은 변경인 경우
- 질문 수를 최소화해야 하는 경우
- 내부적으로만 readiness를 판단하고 점수/ontology는 생략 가능

### `--standard`
- 기본 모드
- 대부분의 기능 추가, 변경, brownfield 확장
- weakest dimension 중심 discovery 진행

### `--deep`
- 고비용/고복잡도 변경
- ambiguity scoring
- ontology extraction / stability tracking
- readiness gating
- state persistence
- challenge modes

추천 상황:
- 시스템 경계가 복잡한 brownfield 변경
- 여러 하위 시스템이 얽힌 설계
- multi-agent handoff가 필요한 경우
- 사용자가 “추정하지 말고 명확히 하자”를 강하게 요구한 경우

## 핵심 운영 원칙

1. 한 번에 질문 하나
- 서로 다른 결정을 한 번에 묶어 묻지 않는다.

2. 가장 큰 병목 모호성을 먼저
- 사소한 디테일보다 rework를 크게 만드는 ambiguity를 우선 줄인다.

3. 이미 확인 가능한 사실은 다시 묻지 않음
- 코드, 설정, 문서, 리서치로 알 수 있는 것은 먼저 확인한다.
- 사용자에게는 사실이 아니라 결정을 묻는다.

4. fact와 decision을 분리
- “지금 무엇이 존재하는가?”와 “그것을 유지할 것인가?”를 구분한다.

5. 질문은 assumption-exposing이어야 함
- feature checklist를 읽는 식으로 질문하지 않는다.
- intent, tradeoff, boundary, success criteria를 드러내는 질문을 우선한다.

6. 충분히 명확해지면 질문을 멈춤
- endless interview를 하지 않는다.
- scope, constraints, outputs, success criteria, non-goals, context가 충분하면 design으로 넘어간다.

7. 범위가 너무 크면 먼저 분해
- 하나의 spec으로 다루기 어려우면 subproject로 나눈다.
- 각 단위는 별도의 spec → plan → implementation cycle을 가진다.
- 이 스킬은 먼저 첫 번째 단위만 다룬다.

8. YAGNI를 기본값으로 둠
- 모호하거나 욕심나는 확장은 뒤로 미룬다.
- 가장 단순하지만 가치 있는 버전을 우선한다.

## 전체 흐름

### 1. Context Scan
먼저 현재 프로젝트 상태를 확인한다.
- 관련 파일, 문서, 최근 변경, 기존 패턴 확인
- brownfield라면 구조와 경계를 fact로 정리
- 필요하면 외부 리서치로 최신 사실 수집

### 2. Scope Check
요청의 크기와 구조를 판단한다.
- 여러 독립 하위 시스템이 섞여 있으면 먼저 분해
- 하나의 spec으로 처리 가능한지 판단
- 너무 크면 subproject 목록과 권장 순서를 제시하고 첫 번째 단위만 진행

### 3. Visual Companion 제안 (선택)
앞으로 다룰 내용이 시각적으로 설명될 때 더 잘 이해될 것 같다면, companion을 독립 메시지로 제안한다.
- mockup
- wireframe
- layout 비교
- architecture diagram
- 시각 디자인 비교

텍스트 질문과 섞지 않는다.
사용자가 거절하면 텍스트만으로 계속 진행한다.

### 4. Discovery Loop
현재 가장 큰 ambiguity axis를 줄이는 질문 하나를 던진다.
- 한 메시지에 질문 하나만
- 가능하면 객관식 또는 좁은 질문 선호
- weakest dimension을 우선 공략
- 한 세부사항만 너무 오래 파지 않도록 breadth control 유지

주요 축:
- Goal
- Constraints
- Outputs
- Success Criteria
- Non-Goals
- Context (brownfield)

### 5. Readiness Check
다음이 충분히 명확하면 discovery를 종료한다.
- scope
- constraints
- outputs
- verification / success criteria
- non-goals
- brownfield context (해당 시)

Greenfield:
`ambiguity = 1 - (goal × 0.40 + constraints × 0.30 + criteria × 0.30)`

Brownfield:
`ambiguity = 1 - (goal × 0.35 + constraints × 0.25 + criteria × 0.25 + context × 0.15)`

기본 threshold:
`ambiguity <= 0.20`

점수는 절대 판정기가 아니라 readiness를 설명하기 위한 보조 도구다.
기본 출력에는 강제하지 않고, `--show-scores` 또는 `--deep`에서 compact하게 보여줄 수 있다.

### 6. Approach Exploration
이제 2~3가지 접근법을 제안한다.
- trade-off를 함께 설명
- 추천안을 먼저 제시하고 이유 설명
- 사용자가 선택하거나 수정 의견을 줄 수 있게 함

### 7. Design Review
충분히 이해했다고 판단되면 설계를 제시한다.
다룰 항목:
- architecture
- components / boundaries
- data flow
- error handling / rollback / recovery
- testing / acceptance verification

큰 작업은 섹션별 승인,
작은 작업은 condensed design approval 하나로 처리할 수 있다.

설계 중 모순이 드러나면 discovery loop로 되돌아간다.

### 8. Spec Write
검증된 설계를 canonical spec 파일로 저장한다.

기본 경로:
`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`

이 파일은 아래 역할을 동시에 수행한다.
- clarified spec
- design doc
- implementation handoff의 기준 문서

### 9. Spec Self-Review
spec 작성 직후 바로 다듬는다.
- placeholder / TODO / TBD 제거
- section 간 내적 일관성 검사
- 단일 implementation plan으로 다룰 수 있는 범위인지 검사
- 다의적 문장을 하나의 해석으로 좁히기

### 10. Optional Commit
작업 공간이 git 저장소이고 문서 변경을 커밋하는 흐름이 자연스러울 때만 spec을 커밋한다.
커밋은 초안 직후가 아니라 self-review 이후에 한다.

### 11. User Review Gate
사용자가 spec을 검토하도록 요청한다.

예:
> 스펙을 `<path>`에 작성했습니다. 구현 계획으로 넘어가기 전에, 변경하고 싶은 점이 있는지 검토해 주세요.

변경 요청이 있으면 반영하고 이 게이트를 반복한다.
사용자가 승인할 때까지 다음 단계로 넘어가지 않는다.

### 12. Handoff
사용자가 spec을 승인한 뒤에만 `writing-plans` skill을 호출한다.
이 다음 단계에서만 구현 스킬이나 코드 작업이 가능하다.

## 질문 라우팅 규칙

### PATH A — 자동 확인 가능한 사실
manifest, config, repo 구조, docs로 명확한 사실은 직접 확인한다.
예:
- 언어 / 프레임워크 / 런타임 버전
- 패키지 매니저
- CI/CD 도구
- 기존 폴더 구조

### PATH B — 해석이 필요한 사실
코드상 근거는 있지만 확정이 어려우면 확인 질문으로 바꾼다.
예:
- “src/auth/jwt.py 기준으로 JWT 인증 경계로 보이는데, 이 이해가 맞나요?”

### PATH C — 사용자 판단이 필요한 결정
반드시 사용자에게 묻는다.
- 목표와 우선순위
- acceptance criteria
- 비즈니스 규칙
- non-goals
- trade-off

### PATH D — fact + decision 혼합
관련 사실을 먼저 짚고, 그 사실을 유지/변경할지 묻는다.
예:
- “orders/에 saga 패턴이 보이는데, payment도 같은 복구 전략을 따라야 하나요?”

### PATH E — 외부 리서치
서드파티 API, 가격 정책, 버전 호환성, 보안 권고, 업계 표준처럼 로컬 컨텍스트 밖의 사실은 먼저 조사한다.
그 fact를 제시한 다음, 채택 여부를 사용자에게 묻는다.

## 브라운필드 운영 원칙

- 기존 구조를 먼저 이해하고 그 위에서 질문한다.
- 관련 없는 리팩터링은 제안하지 않는다.
- 현재 작업과 직접 관련된 구조적 문제만 설계에 포함한다.
- 기존 패턴, 경계, 복구 전략, 테스트 방식이 있으면 먼저 재사용을 검토한다.

좋은 질문 예시:
- “기존 JWT 인증 경계를 그대로 따르게 할까요?”
- “현재 saga 복구 전략을 payment에도 재사용할까요?”

나쁜 질문 예시:
- “인증 방식이 뭐예요?”
- “데이터베이스 뭐 써요?”

## Depth Features

### Quick
- discovery를 짧게 압축
- 점수/ontology 출력 생략 가능
- 작은 수정이나 이미 상세한 요청에 적합

### Standard
- weakest dimension 중심 탐색
- brownfield routing 적극 사용
- 필요하면 간단한 ambiguity 요약

### Deep
필요할 때만 활성화한다.
- ambiguity scoring
- ontology extraction / stability tracking
- readiness gating
- state persistence

#### Ontology Tracking
용어와 개념 구조가 자꾸 흔들릴 때만 사용한다.
- stable entities
- changed entities
- new entities
- removed entities
- stability ratio

#### Challenge Modes
Round 4+: Contrarian Mode
- 핵심 가정을 일부러 흔들어 본다.
- “반대로 해도 정말 안 되는 이유가 있나요?”

Round 6+: Simplifier Mode
- 뒤로 미뤄도 되는 것을 걷어낸다.
- “가장 단순하지만 여전히 가치 있는 버전은 무엇인가요?”

Round 8+: Ontologist Mode
- 핵심 엔티티와 관계를 정리한다.
- “지금 말하는 workflow, planner, inbox 중 핵심 엔티티는 무엇인가요?”

## Output Strategy

### Required
- `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`

### Optional
- `readiness-report.json`
- `discovery-state.json`

추가 파일은 다음 경우에만 만든다.
- deep mode이고 resume이 필요할 때
- handoff automation이 상태 파일을 요구할 때
- 사용자가 점수/상태 산출물을 명시적으로 원할 때

기본값은 단일 canonical spec 파일 하나다.
가능하면 discovery transcript, assumptions, key entities는 별도 파일 대신 spec appendix에 포함한다.

## 권장 spec 구조

```md
# Design Spec: {title}

## Metadata
- Mode: quick | standard | deep
- Type: greenfield | brownfield
- Status: DRAFT | APPROVED
- Final Ambiguity: {optional}

## Goal
...

## Scope
...

## Constraints
...

## Non-Goals
...

## Success Criteria
- [ ] ...

## Existing Context
...

## Options Considered
1. ...
2. ...
3. ...

## Recommended Design
### Architecture
...
### Components / Boundaries
...
### Data Flow
...
### Error Handling
...
### Testing / Verification
...

## Assumptions Resolved
| Assumption | Resolution |
|------------|------------|
| ... | ... |

## Key Entities (optional)
| Entity | Type | Fields | Relationships |
|--------|------|--------|---------------|
| ... | ... | ... | ... |

## Appendix: Discovery Notes (optional)
...
```

## 좋은 패턴

- fact를 먼저 확인하고 decision을 묻는다.
- 질문은 좁고 선명하며, 한 번에 하나다.
- 설계는 approval 가능한 단위로 제시한다.
- spec은 하나의 canonical artifact로 유지한다.
- ambiguity가 충분히 줄어든 뒤에만 설계 합성으로 넘어간다.

## 나쁜 패턴

- 구현이 금지된 단계에서 코드나 스캐폴딩을 시작한다.
- 이미 확인 가능한 사실을 사용자에게 다시 묻는다.
- breadth control 없이 한 세부사항만 오래 파고든다.
- clarified-spec, design doc, notes, transcript를 모두 별도 필수 파일로 만들어 관리 부담을 키운다.
- ambiguity가 높은데도 implementation plan으로 성급히 넘어간다.

## 종료 조건

다음 중 하나면 discovery/design 단계는 종료된다.
- 사용자 승인된 spec이 작성되었고 다음 단계가 `writing-plans`인 경우
- 사용자가 이 정도면 충분하다고 판단했고, 남은 risk를 명시한 compact spec을 남긴 경우
- 범위가 너무 커서 subproject decomposition 결과를 남기고 첫 번째 단위만 진행한 경우
- 사용자가 stop / cancel / abort를 명시한 경우

## 호환성 메모

- 이 스킬은 기존 `brainstorming`의 설계 게이트를 유지한다.
- `deep-interview`의 ambiguity reduction / readiness 판단을 흡수한다.
- OMX 스타일의 실행 전 명확화 discipline을 반영한다.
- 승인 후 다음 단계는 `writing-plans` 하나로 고정한다.
- 복잡한 로직은 한 곳에만 두어야 drift가 줄어든다.
