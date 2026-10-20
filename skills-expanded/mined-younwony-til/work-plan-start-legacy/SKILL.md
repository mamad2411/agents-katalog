---
name: work-plan-start
effort: max
description: |
  WORK-SPEC.html 작업 명세서를 기반으로 단계별 실제 구현을 수행합니다. 코드 작성, 테스트, 문서화, git add까지 한 번에 처리하는 풀 파이프라인입니다.
  "/work-plan-start", "작업 시작", "WORK-SPEC 실행", "명세서 기반 작업", "계획대로 구현", "스펙 실행", "work plan 실행" 요청에 트리거됩니다.
  복잡한 작업(파일 3개+)은 팀 에이전트 워크플로우(Explore, Plan, test-generator, code-refactor)를 자동 디스패치하여 병렬 처리합니다.
  반드시 `/work-plan` 스킬로 WORK-SPEC.html를 먼저 생성한 후 사용하세요.
---

# Work Plan Start

WORK-SPEC.html 명세서를 읽고, 설계대로 구현 → 테스트 → 문서화 → git add를 수행한다.

## 왜 이 스킬인가?

- **명세서 기반 실행**: WORK-SPEC.html의 설계를 그대로 구현하므로 임의 변경이 없음
- **팀 에이전트 병렬화**: 복잡한 작업은 Explore/Plan/test-generator/code-refactor를 자동 디스패치
- **품질 체크 내장**: CLAUDE.md 규칙 체크리스트를 구현 중 자동 적용

---

## 실행 방법

```
/work-plan-start                        # {DOC_DIR}/1_WORK-SPEC.html 자동 탐색
/work-plan-start path/to/1_WORK-SPEC.html # 지정 경로의 WORK-SPEC 사용
```

---

## 작업 절차

### 0. WORK-SPEC.html 검증

글로벌 CLAUDE.md의 **DOC_DIR 결정 규칙**에 따라 `{DOC_DIR}`을 결정한 후, `{DOC_DIR}/*_WORK-SPEC.html`를 패턴 매칭으로 찾는다.
`$ARGUMENTS`로 경로가 직접 지정된 경우 해당 경로를 사용한다. (레거시 경로 `WORK-SPEC.html`도 폴백 탐색)

**검증 항목:**
- 파일 존재 여부
- 필수 섹션: "요구사항 요약", "작업 단계 (Phase)"
- Phase 목록이 비어있지 않은지

검증 실패 시 → `/work-plan`을 먼저 실행하도록 안내한다.

### 1. TaskCreate로 작업 목록 생성

WORK-SPEC.html의 "작업 단계 (Phase)" 섹션을 파싱하여 **TaskCreate**로 작업 목록을 만든다.

**규칙:**
- Phase별 그룹화 — 각 Phase가 상위 작업, 하위 항목이 세부 작업
- `addBlockedBy`로 Phase 간 순서 의존성 설정
- 모든 작업에 현재 진행형 `activeForm` 포함

```
예시:
- Task #1: [Phase 1] Entity 클래스 생성 (activeForm: "Entity 클래스 생성 중")
- Task #2: [Phase 1] Service 로직 구현 (activeForm: "Service 로직 구현 중", blockedBy: [#1])
- Task #3: [Phase 2] 단위 테스트 작성 (activeForm: "단위 테스트 작성 중", blockedBy: [#2])
- Task #4: [Phase 3] 문서화 (activeForm: "문서 작성 중", blockedBy: [#3])
- Task #5: [Phase 4] git add + 완료 보고 (activeForm: "마무리 작업 중", blockedBy: [#4])
```

### 1.5. 실행 모드 판단

WORK-SPEC.html의 파일 변경 목록을 기반으로 실행 모드를 결정한다.

| 예상 변경 파일 수 | 모드 | 설명 |
|------------------|------|------|
| 1~2개 | **Solo** | Main 단독 처리. 에이전트 오버헤드 불필요 |
| 3~4개 | **Standard** | 현재 팀 워크플로우. Main이 구현 + 조율 |
| 5개+ | **Coordinator** | Main은 순수 조율자. 구현을 워커에 위임 |

모드 선택 후 안내:
```
실행 모드: {Solo / Standard / Coordinator}
사유: {변경 예상 파일 N개}
워커 수: {Coordinator 시 워커 에이전트 수}
```

#### Standard 모드 (3~4파일)

```
Phase 1: 탐색 + 설계 (병렬, foreground — 결과가 Phase 2 입력)
├─ [Explore]  코드베이스 구조 파악, 영향 범위 분석
└─ [Plan]     구현 전략 설계, 파일별 변경 계획

Phase 2: 구현 + 테스트 (병렬)
├─ [Main]            핵심 코드 수정 (Phase 1 결과 기반)
└─ [test-generator]  테스트 자동 생성 (background)

Phase 3: 검증 + 문서화 (병렬)
├─ [code-refactor]   코드 품질 리뷰 (background)
└─ [Main]            ARCHITECTURE.html, SPEC.md 작성
```

#### Coordinator 모드 (5파일+)

Main은 **지시 + 검증 + 취합만** 수행하고, 구현은 워커 에이전트에 위임한다.

```
Phase 1: Research (병렬, foreground — 결과 대기)
├─ [Explore]  코드베이스 구조 + 영향 범위
└─ [Plan]     구현 전략 + 워커 분배 계획 (어떤 워커가 어떤 파일을 담당할지)

Phase 2: Synthesis (Main 단독)
Main이 Phase 1 결과를 종합하여 워커별 구현 스펙 작성
- 워커 A: "이 파일들을 이렇게 수정하라" (구체적 지시)
- 워커 B: "이 파일들을 이렇게 수정하라"

Phase 3: Implementation (병렬)
├─ [impl-worker A]   파일 그룹 1 구현 (isolation: "worktree")
├─ [impl-worker B]   파일 그룹 2 구현 (isolation: "worktree")
└─ [test-generator]  테스트 자동 생성 (background)

Phase 4: Verification (병렬)
├─ Main              워커 결과 검증 + 충돌 해결
├─ [code-refactor]   코드 품질 리뷰 (background)
└─ Main              문서화 (ARCHITECTURE.html, SPEC.md)

Phase 5: Finalize
Main: git add + 완료 보고
```

#### Coordinator 워커 분배 규칙

- 하나의 파일을 2개 워커가 동시에 수정하지 않음
- 워커당 최대 5파일 (초과 시 워커 추가)
- 파일 간 의존성이 있으면 워커 실행 순서 지정 (blockedBy)
- 워커 프롬프트에 포함: WORK-SPEC 관련 섹션 + 구현 스펙 + 기존 코드 패턴 요약
- 워커는 `general-purpose` Agent를 `isolation: "worktree"`로 디스패치 (별도 에이전트 정의 불필요)

#### 공통 디스패치 규칙

- Phase 순서는 반드시 순차 실행 (Phase 간 의존성)
- 각 Phase 내 에이전트는 최대한 병렬
- 에이전트 실패 시 Withhold-then-Recover 패턴 적용 (CLAUDE.md 참조)
- **Explore 에이전트는 `model: "haiku"`로 디스패치** (읽기 전용 탐색이므로 비용 절감)

팀 워크플로우 적용 시 아래 2~4단계는 워크플로우 내에서 자동 수행된다.

### 2. 핵심 구현

WORK-SPEC.html 설계에 따라 코드를 구현한다.

**Java 프로젝트인 경우**: `references/java-checklist.md`를 Read 도구로 읽어서 체크리스트를 적용하라.

### 3. 테스트

#### 단위 테스트
- WORK-SPEC.html의 "테스트 전략 > 단위 테스트" 기반
- 우선순위 P1부터, 핵심 비즈니스 로직 중심

#### 통합 테스트
- WORK-SPEC.html의 "테스트 전략 > 통합 테스트" 기반
- API 엔드포인트 + 데이터 흐름 검증 (Spring Boot API인 경우)

#### 실패 시 재시도

| 시도 | 행동 |
|------|------|
| 1차 실패 | 에러 분석 → 코드 수정 → 재실행 |
| 2차 실패 | 다른 접근 방식으로 수정 → 재실행 |
| 3차 실패 | AskUserQuestion으로 진행 방향 질문 |

3차 실패 시 메시지:
```
테스트 실패가 3회 반복되었습니다.

실패 테스트: {테스트명}
에러: {에러 내용}
시도한 수정: {수정 내역}

어떻게 진행할까요?
1. 테스트 스킵 후 계속 진행
2. 테스트 수정 방향 직접 지정
3. 작업 중단
```

### 4. 문서화

CLAUDE.md 규칙에 따라 생성한다.

- **ARCHITECTURE.html**: 시스템 아키텍처, 데이터 흐름, 핵심 로직(다이어그램), 파일 구조, 이슈 번호
- **SPEC.md**: 기능 설명, 사용자 인터페이스, 데이터 흐름(다이어그램), 핵심 로직, 이슈 번호

다이어그램은 `mermaid-diagram` 스킬을 우선 사용한다 (플로우차트, 시퀀스, ER 등). 픽셀 단위 제어가 필요하면 `svg-diagram` 스킬을 사용한다. Mermaid CLI 미설치 시 ASCII 폴백.

**TIL 문서 프로젝트**: 문서 자체가 결과물이므로 이 단계를 건너뛴다.

### 5. 마무리

```bash
git add {변경된 파일들}
git status
```

commit은 수행하지 않는다 (사용자 요청 시에만).

완료 보고 템플릿은 `references/completion-report.md`를 Read 도구로 읽어서 형식을 따르라.

---

## 프로젝트 유형별 Phase 조정

### TIL 문서 프로젝트

| Phase | 내용 |
|-------|------|
| 1 | 마크다운 문서 작성 (템플릿 준수) |
| 2 | 링크 검증, README 업데이트 |
| 3 | git add + 완료 보고 |

### 알고리즘 프로젝트

| Phase | 내용 |
|-------|------|
| 1 | 알고리즘 구현 |
| 2 | 테스트 케이스 작성 및 실행 |
| 3 | 시간/공간 복잡도 분석 문서화 |
| 4 | git add + 완료 보고 |

### Spring Boot API 프로젝트

| Phase | 내용 |
|-------|------|
| 1 | Entity, DTO, Repository, Service, Controller 구현 |
| 2 | 단위 테스트 + 통합 테스트 |
| 3 | ARCHITECTURE.html + SPEC.md 작성 |
| 4 | git add + 완료 보고 |

---

## 주의사항

- **WORK-SPEC.html 우선**: 명시된 설계를 따른다. 임의 변경 금지.
- **단계별 진행**: TaskCreate 작업을 순서대로 진행하며, 완료 시 TaskUpdate로 상태 갱신.
- **실패 시 보고**: 설계가 불가능하면 AskUserQuestion으로 대안 제시.
- **commit 금지**: git add까지만 수행.
- **기존 패턴 존중**: 프로젝트의 기존 코드 스타일과 패턴을 따른다.
