---
name: web-pipeline
description: 웹사이트 개발 파이프라인 오케스트레이터. 디자인 → 프론트엔드(JS/jQuery) → 백엔드(Spring Boot) → QA 4단계를 web-designer/web-frontend/web-backend/web-qa 에이전트로 자동 위임한다. Track 시스템(.claude/tracks/{track_id}/)을 산출물 저장소로 사용하며 metadata.json의 current_phase를 갱신하여 /track-status와 호환된다. "웹사이트 만들어줘", "랜딩페이지", "관리자 페이지", "신규 화면 + API", "회원가입 페이지", "/web-pipeline" 같은 요청에 트리거된다. "재실행", "다시 만들어", "업데이트", "수정해줘", "이전 결과 보완" 등 후속 작업 키워드에도 트리거된다. 단일 화면만 수정하는 작은 요청에도 사용 가능 (Phase 부분 실행).
---

# Web Pipeline — 웹사이트 개발 4단계 오케스트레이터

웹사이트 개발 작업(디자인/프론트/백/QA가 모두 또는 일부 포함)을 4단계 파이프라인으로 자동 수행하는 오케스트레이터 스킬.

## 언제 사용하는가

- 신규 화면 + API 함께 개발이 필요할 때
- Figma 또는 텍스트 요구사항에서 시작하는 웹사이트 작업
- 기존 화면/API의 부분 수정 (Phase 일부만 재실행)
- 사용자가 명시적으로 `/web-pipeline` 호출

기존 `/work-plan` + `/work-plan-start`는 일반 작업용. 이 스킬은 웹사이트 도메인 전용 라우터.

## Phase 0: 컨텍스트 확인 + Track 결정

### 0-1. Track 디렉토리 결정

CLAUDE.md의 "DOC_DIR 결정 규칙"을 그대로 따른다:

1. `.claude/tracks/index.md` 읽기
2. 분기:
   - **Active Track 0개**: 신규 Track 생성 (`T{YYYY-MM-DD}-{단어요약}` 형식)
   - **Active Track 1개**: 자동 선택
   - **Active Track 2개+**: AskUserQuestion으로 선택 요청
3. 사용자가 `$ARGUMENTS`로 직접 경로 지정 시 위 규칙 건너뜀

### 0-2. 실행 모드 판별

선택된 Track 디렉토리에서:

| 조건 | 모드 | 동작 |
|------|------|------|
| 빈 디렉토리 (또는 신규) | **initial** | Phase 1부터 순차 실행 |
| `4_PLAN.html` 존재 + 사용자가 부분 수정 요청 | **partial-rerun** | 영향 Phase만 재호출 |
| `4_PLAN.html` 존재 + 새 요구사항 입력 | **append** | 기존 Phase 보존, 새 항목만 추가 |

### 0-3. metadata.json 초기화/갱신

```json
{
  "track_id": "T2026-05-11-signup",
  "description": "회원가입 페이지 + API",
  "domain": "web-pipeline",
  "current_phase": 0,
  "total_phases": 4,
  "phases": [
    {"id": 1, "name": "design",   "agent": "web-designer", "status": "pending"},
    {"id": 2, "name": "frontend", "agent": "web-frontend", "status": "pending"},
    {"id": 3, "name": "backend",  "agent": "web-backend",  "status": "pending"},
    {"id": 4, "name": "qa",       "agent": "web-qa",       "status": "pending"}
  ],
  "created_at": "2026-05-11T...",
  "updated_at": "2026-05-11T..."
}
```

신규 Track이면 `.claude/tracks/index.md`에 한 줄 추가.

## Phase 1: 디자인 (web-designer)

**실행 모드:** 서브 에이전트

```
Agent(
  subagent_type="general-purpose",
  description="디자인 명세 + 와이어프레임 생성",
  prompt=(
    "당신은 web-designer 에이전트다. ~/.claude/agents/web-designer.md를 먼저 읽고 역할/원칙을 숙지하라.\n\n"
    "track_dir: {track_dir}\n"
    "requirement: {원본 요구사항}\n"
    "mode: {initial|partial-rerun}\n\n"
    "design-spec-generate 스킬을 사용하여 1_REQ-SNAPSHOT.html, 2_WORK-SPEC.html, 3_FEATURE-CHECKLIST.html, 5_ARCHITECTURE.html, 6_SPEC.html을 작성하라. 각 문서는 html-doc 스킬 규칙에 따라 자체 완결 HTML로 생성하고, html-doc 시각화 가이드에 따라 인라인 SVG 다이어그램 1개 이상 포함한다."
  ),
  model="opus"
)
```

완료 시:
- metadata.json의 phase 1 status = "done"
- current_phase = 2

## Phase 2: 프론트엔드 (web-frontend)

**실행 모드:** 서브 에이전트

Phase 1 완료 후 6_SPEC.html의 화면 목록을 추출하여 `target_pages` 전달.

```
Agent(
  subagent_type="general-purpose",
  description="JS/jQuery 화면 구현",
  prompt=(
    "당신은 web-frontend 에이전트다. ~/.claude/agents/web-frontend.md를 먼저 읽어라.\n\n"
    "track_dir: {track_dir}\n"
    "target_pages: {6_SPEC.html에서 추출한 화면 ID 목록}\n"
    "mode: {mode}\n\n"
    "frontend-jquery-build 스킬을 사용하여 HTML/CSS/JS를 구현하고, 6_SPEC.html의 'API 계약' 섹션을 확정 상태로 갱신하라."
  ),
  model="opus"
)
```

완료 시:
- metadata.json의 phase 2 status = "done"
- current_phase = 3

## Phase 3: 백엔드 (web-backend)

**실행 모드:** 서브 에이전트 (백그라운드 test-generator 디스패치는 web-backend가 자체 수행)

```
Agent(
  subagent_type="general-purpose",
  description="Spring Boot API 구현",
  prompt=(
    "당신은 web-backend 에이전트다. ~/.claude/agents/web-backend.md를 먼저 읽어라.\n\n"
    "track_dir: {track_dir}\n"
    "target_endpoints: {6_SPEC.html '확정된 API 계약'에서 추출한 엔드포인트 목록}\n"
    "mode: {mode}\n\n"
    "spring-api-build 스킬로 Controller/Service/Repository/DTO를 구현하라.\n"
    "구현 진행 중 일정 분량 도달 시 test-generator 에이전트를 백그라운드 디스패치하라.\n"
    "구현 종료 직전 test-coverage-check 스킬을 호출하라."
  ),
  model="opus"
)
```

완료 시:
- metadata.json의 phase 3 status = "done"
- current_phase = 4

## Phase 4: QA (web-qa)

**실행 모드:** 서브 에이전트

```
Agent(
  subagent_type="general-purpose",
  description="경계면 정합성 + 브라우저 QA",
  prompt=(
    "당신은 web-qa 에이전트다. ~/.claude/agents/web-qa.md를 먼저 읽어라.\n\n"
    "track_dir: {track_dir}\n"
    "scope: full\n"
    "target_features: {3_FEATURE-CHECKLIST.html의 항목 ID 목록}\n\n"
    "web-qa-integration 스킬로 FE↔BE 경계면 교차 비교를 먼저 수행하고,\n"
    "qa-scenario 스킬로 8_QA-SCENARIOS.html을 작성한 뒤,\n"
    "browser-debug 스킬로 실제 페이지 동작을 검증하라.\n"
    "결과를 9_QA-REPORT.html에 기록하라. html-doc 스킬 규칙에 따라 자체 완결 HTML로 생성하고, html-doc 시각화 가이드에 따라 인라인 SVG 다이어그램 1개 이상 포함한다."
  ),
  model="opus"
)
```

완료 시:
- metadata.json의 phase 4 status = "done"
- current_phase = 4 (완료)

QA에서 [Critical] 이슈가 발견되면 영향 Phase를 partial-rerun 모드로 재호출하고 완료까지 반복.

## 데이터 전달 프로토콜

- **파일 기반** (Track 디렉토리): 모든 Phase가 동일한 Track 문서를 SSOT로 공유
- **메시지 기반**: 에이전트 간 직접 협상이 필요할 때 SendMessage (예: web-frontend ↔ web-backend의 API 계약 협상)
- **태스크 기반**: TaskCreate로 Phase별 작업 상태 가시화

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| 에이전트 1회 실패 | 동일 prompt로 1회 재호출 |
| 에이전트 2회 실패 | 에러 메시지를 분석하여 prompt 수정 후 재시도 |
| 에이전트 3회 실패 | 메인이 직접 수행 또는 사용자 보고 |
| 환경 미충족 (Figma/Browser MCP) | 폴백 모드로 자동 전환 (텍스트 기반, 코드 검증) + 사용자 알림 |
| FE↔BE 계약 미합의 | 사용자에게 결정 요청 (5분 이내 응답 없으면 FE 선언이 우선) |

## 완료 후 정리

1. `4_PLAN.html`에 Phase별 시작/완료 시각 + 산출 파일 목록 정리
2. `0_INDEX.html` 자동 생성/갱신 (문서 2개 이상이면)
3. 변경된 파일 git add (단, `.claude/` 하위는 제외 — CLAUDE.md 룰)
4. 사용자에게 진행 결과 요약 + `/track-status {track_id}` 안내

## 테스트 시나리오

### 정상 흐름
사용자 입력: "회원가입 페이지랑 API 만들어줘"
1. Phase 0: 신규 Track `T2026-05-11-signup` 생성
2. Phase 1: web-designer가 회원가입 폼 와이어프레임 + 필드 명세 + API 초안 작성
3. Phase 2: web-frontend가 signup.html + signup.js (jQuery) 구현, API 계약 확정
4. Phase 3: web-backend가 SignupController/Service/Repository + 테스트 생성
5. Phase 4: web-qa가 BDD 시나리오 + 브라우저 검증 + 경계면 비교 → 9_QA-REPORT.html
6. 모든 Phase status = "done", 사용자에게 완료 보고

### 에러 흐름 (계약 불일치)
1. Phase 4에서 web-qa가 FE의 `userId` 호출과 BE 응답의 `id` 필드 불일치 발견
2. 9_QA-REPORT.html에 [Boundary-Mismatch] 마커로 기록
3. 오케스트레이터가 web-frontend와 web-backend 양쪽에 SendMessage로 합의 요청
4. 합의된 필드명으로 양쪽 코드 수정 + 6_SPEC.html 갱신
5. Phase 4 boundary-only 재실행으로 확인

## 후속 작업 (재실행) 트리거

이 스킬은 다음 표현에도 반응한다:
- "회원가입 페이지 다시", "API 응답 수정", "디자인만 다시"
- "이전 작업 이어서", "방금 만든 거 보완", "QA 다시 돌려"
- "Phase 2부터 다시"

Phase 0의 모드 판별 로직에서 자동으로 `partial-rerun`으로 분기.
