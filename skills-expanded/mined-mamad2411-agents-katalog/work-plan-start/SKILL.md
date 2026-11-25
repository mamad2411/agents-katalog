---
name: work-plan-start
description: WORK-SPEC.html 작업 명세서를 기반으로 단계별 실제 구현을 수행한다. Solo/Standard/Coordinator 모드 자동 선택. 내부에서 tdd, diagnose, test-generator atomic skill/agent를 조합 호출하는 wrapper. "/work-plan-start", "작업 시작", "WORK-SPEC 실행", "명세서 기반 작업", "계획대로 구현", "스펙 실행" 요청 트리거.
---

# Work Plan Start (Atomic Wrapper)

`2_WORK-SPEC.html`를 입력으로 단계별 구현을 진행하고 `4_PLAN.html` / `5_ARCHITECTURE.html` / `6_SPEC.html`를 산출한다.

본 skill은 **wrapper**다. 실제 작업은 atomic skill/agent들이 수행한다 — ADR 0002 (Track as Skill Container) 참조:

- 각 Phase 내부: `tdd` 패턴 (test-coverage-check skill 또는 test-generator agent)
- 에러 시: `debugger` agent (5-phase diagnose loop)
- 리팩터링 시: `code-refactor` agent
- 아키텍처 의문: `/improve-codebase-architecture` skill 호출

외부 호출 인터페이스(`/work-plan-start`)는 그대로 유지된다.

> 구버전: `deprecated/work-plan-start-legacy/`. 호출 비권장.

## 사전 조건 (Hard Dependency)

**Requires**: 현재 Active Track의 `*_WORK-SPEC.html` 존재. 없으면 `/work-plan` 먼저.

## 모드 자동 선택

WORK-SPEC.html의 예상 변경 파일 수에 따라:

| 예상 변경 파일 | 모드 | Main 역할 |
|---------------|------|----------|
| 1~2개 | **Solo** | Main 단독 처리. 에이전트 오버헤드 불필요 |
| 3~4개 | **Standard** | Main이 조율 + 구현 + 문서화 |
| 5개+ | **Coordinator** | Main은 순수 조율자. 구현을 워커에 위임 |

## 절차

### Step 1 — 사전 확인

- Active Track의 `2_WORK-SPEC.html` 존재 확인 → 없으면 사용자에게 안내 후 종료
- `3_FEATURE-CHECKLIST.html` 존재 확인 (없어도 진행 가능, 단 경고)
- `metadata.json`의 `current_phase` 확인 → 재개 가능 여부 판단
- `.claude/CONTEXT.md` 읽기 → 도메인 어휘 인지

### Step 2 — Phase 계획

WORK-SPEC.html를 파싱하여 Phase 목록 추출. 보통 4~6개. 각 Phase는:

- 제목 + 변경 인터페이스 (AGENT-BRIEF 양식)
- 의존성 (이전 Phase 산출물 사용 여부)
- 검증 방법 (테스트 명령, 동작 확인)

`4_PLAN.html`을 작성한다. **`work-plan-start/references/plan-template.html`을 skeleton으로 사용**한다 — `2_WORK-SPEC.html`(workspec-template) / `1_REQ-SNAPSHOT.html` / `3_FEATURE-CHECKLIST.html`와 동일한 카드 디자인 시스템을 공유하여 Track 문서 묶음의 시각 일관성을 유지한다.

구성: 헤더 + 통계 카드(총/완료 Phase·현재 Phase·진행률) + **Phase 타임라인 SVG** + 구성 방향(해당 시) + Phase 진행률 표 + Phase 상세(`details`).

- **인라인 SVG 다이어그램 1개 이상 필수** — Phase 타임라인(완료/진행/대기 상태별 색상 구분) 권장. 색상은 템플릿 CSS 변수(`--ok`/`--accent`/`--border` 등)로 라이트·다크 대응.
- Phase·작업 상태는 배지로 표기하고 진행에 따라 갱신: `badge-ok`(완료) / `badge-info`(진행) / `badge-warn`(대기) / `badge-err`(차단).
- `4_PLAN.html`이 Phase 진행 상태의 SSOT다 — `metadata.json`의 `current_phase`와 동기화한다.

### Step 3 — Phase별 실행

각 Phase를 순차 실행 (Phase 간 의존성 보존):

#### Solo 모드
Main이 직접 코드 작성. 매 Phase마다:
1. 변경 인터페이스에 맞춰 코드 작성
2. test 작성 (test-coverage-check skill 또는 직접)
3. 검증 (테스트 실행)
4. `4_PLAN.html` 상태 갱신 (in_progress → completed)

#### Standard 모드
1. 코드 작성 (Main, foreground)
2. test-generator agent 디스패치 (background, 테스트 자동 생성)
3. 검증 통합 (Main이 결과 받아 정리)

#### Coordinator 모드
1. Main이 워커 분배 (구현 영역별로 sub-agent 디스패치)
2. 병렬 실행
3. Main이 결과 통합 + 검증

### Step 4 — 에러 처리 (`debugger` agent 5-phase)

테스트 실패 / 빌드 에러 / 런타임 에러 발생 시 `debugger` agent 디스패치:

- Phase 1: 재현 loop 구축 (failing test / curl / CLI 등)
- Phase 2: 재현 확인
- Phase 3: 가설 3~5개 ranked + 사용자 승인
- Phase 4: 계측 (한 번에 한 변수)
- Phase 5: fix + 회귀 테스트

`Loop 옵션 10단계`는 글로벌 debugger agent의 SKILL.md 참조.

### Step 5 — 아키텍처 의문 시

Phase 중 "이 모듈 모양이 잘못된 거 같다" 신호 (shallow module, untestable, leaky abstraction) → `/improve-codebase-architecture` skill 호출.

deepening opportunity가 발견되면 사용자에게 surface:
- 즉시 처리: 현재 Phase에 통합
- 후속 처리: WORK-SPEC.html "Out of Scope"에 추가 + 새 Track 후보

### Step 6 — 산출물 생성

구현 완료 시:

산출 HTML 문서는 자체 완결 HTML로 작성하며, **Track 문서 묶음과 동일한 카드 디자인 시스템**(`work-plan/references/workspec-template.html` 기준 — `:root` CSS 변수, `.card`/`.badge`/`.callout`/`figure` 컴포넌트)을 공유한다. `1_REQ-SNAPSHOT`~`6_SPEC` 전체가 시각적으로 일관되어야 한다.

- `5_ARCHITECTURE.html` — 시스템 아키텍처, 데이터 흐름. 산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 시스템 구조를 인라인 SVG 다이어그램으로 1개 이상 포함한다 (권장: 시스템·모듈 구조도).
- `6_SPEC.html` — 기능 명세, 사용자 인터페이스, 핵심 로직. 산출 HTML 문서에는 html-doc 스킬의 시각화 가이드에 따라 데이터 흐름을 인라인 SVG 다이어그램으로 1개 이상 포함한다 (권장: 처리 흐름도).
- `4_PLAN.html` — 모든 Phase 상태 completed로 갱신

### Step 7 — 검증

- [ ] 모든 Phase의 검증 통과
- [ ] Java 프로젝트면 test-coverage-check skill 실행
- [ ] CONTEXT.md / ADR 갱신 필요 시 surface
- [ ] `5_ARCHITECTURE.html` / `6_SPEC.html` / `4_PLAN.html`에 인라인 SVG 다이어그램 1개 이상 포함 확인
- [ ] git add (TIL 한정, `.claude/` 예외)

검증 후 사용자에게 다음 단계 안내: "`/self-review`로 자체 코드 리뷰 진행, 또는 `/qa-scenario`로 QA 시나리오 생성."

## Atomic Skill 직접 호출

Track 외부 즉흥 구현이라면 atomic skill을 직접 호출:

- 테스트만 추가 → `test-coverage-check` skill 또는 `test-generator` agent 단독
- 한 버그만 디버깅 → `debugger` agent 단독
- 한 모듈만 deep화 → `/improve-codebase-architecture` 단독

## Atomic 호출 흐름 (간단 예)

```
WORK-SPEC.html (Phase 3개)
   ↓
[Phase 1 — 도메인 모델]
   ├─ Main: 코드 작성
   ├─ test-generator agent: 단위 테스트 (background)
   └─ 검증: ./gradlew test
[Phase 2 — API 레이어]
   ├─ Main: Controller/Service
   ├─ test-generator agent
   └─ 검증
[Phase 3 — UI]
   ├─ Main: 프론트엔드
   ├─ Phase 도중 에러 발생 → debugger agent (5-phase)
   └─ 검증
   ↓
5_ARCHITECTURE.html + 6_SPEC.html 생성 (인라인 SVG 다이어그램 필수 포함)
4_PLAN.html 완료 상태 갱신
```

## 관련

- `/work-plan` — 본 skill의 입력 (WORK-SPEC.html) 생성
- `debugger` agent — Phase 내 에러 시 호출
- `test-generator`, `code-refactor`, `test-coverage-check` — 보조 atomic
- `/improve-codebase-architecture` — 아키텍처 의문 시
- ADR 0002 — Track-as-Skill-Container
