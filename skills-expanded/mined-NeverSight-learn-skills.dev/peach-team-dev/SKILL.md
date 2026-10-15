---
name: peach-team-dev
model: opus
description: |
  PeachSolution 신규 모듈 풀스택 개발을 조율하는 통합 팀 스킬.
  Spec과 ui-proto 기반 표준 모드 + Spec만 모드 + 자연어 prompt 모드를 지원.
  "팀으로 만들어줘", "풀스택 개발", "팀 개발", "백엔드+UI 전체 생성",
  "버그 수정해줘", "이 화면에 X 추가해줘", "API와 화면 같이 만들어줘",
  "백엔드만 만들어줘", "API만 만들어줘", "UI만 추가" 키워드로 트리거.
  mode=backend(API+Store) | ui(UI만) | fullstack(전체) 지원하며,
  mode/proto 없이 자연어 입력만으로도 즉흥적 버그 수정·기능 추가 가능.
  peach-team을 흡수 통합한 스킬로, 신규 기능부터 즉흥적 변경까지 모두 처리한다.
---

# Peach Team Dev

PeachSolution 풀스택 개발을 조율하는 통합 오케스트레이터.

## Overview

신규 기능 개발부터 즉흥적 버그 수정까지 한 스킬에서 처리한다. 기존 `peach-team`을 흡수 통합하면서 다음 기능을 추가했다.

- **검증 기준의 외부화** — ui-proto + Spec을 본 개발의 검증 기준으로 삼는다
- **proto 자동 복사** — ui-proto 저장소의 `_spec.md`를 본 프로젝트로 자동 이전
- **prompt 모드** — Spec/proto 없이 자연어 입력만으로도 즉흥적 작업 가능

> 의사결정 근거: `docs/05-스킬재구성-2026-04-27.md` 참조.
> 표준 워크플로우: `docs/03-워크플로우.md` 참조.

## 입력 모드 3가지

| 모드 | 입력 | 검증 기준 | 적합 케이스 |
|------|------|---------|-----------|
| **표준** | mode + proto 경로 | ui-proto 화면 + Spec | 신규 기능 (재구성 핵심 경로) |
| **Spec만** | mode (proto 생략) | `docs/spec/...` Spec | 백엔드만, UI 없는 변경 |
| **prompt** | 자연어 입력 | prompt 텍스트 | 버그 수정, 즉흥적 변경, 핫픽스 |

prompt 모드는 검증 기준이 약하므로 **결과를 직접 확인해야 한다**. 변경 규모가 크면 Spec 작성을 자동 권고한다.

## Modes

| mode | 용도 | 포함 역할 |
| --- | --- | --- |
| `backend` | 기존 UI에 API + Store 연결 | backend-dev, backend-qa, store-dev, frontend-qa |
| `ui` | Store 기반 UI만 구현 | ui-dev, frontend-qa |
| `fullstack` | DB 스키마 기반 전체 생성 | backend-dev, backend-qa, store-dev, ui-dev, frontend-qa |

## Preconditions

### 표준 모드 (proto 인자 사용)

- ui-proto 저장소의 태스크 폴더가 존재하고 `_spec.md`를 포함해야 한다.
- 본 프로젝트는 `docs/spec/{년}/{월}/` 폴더 구조를 가져야 한다 (없으면 자동 생성).

### Spec만 모드

- DB 스키마가 필요한 모드(`backend`, `fullstack`)에서는 `api/db/schema/[도메인]/[테이블].sql`이 존재해야 한다.
- `ui` 모드에서는 `front/src/modules/[모듈명]/store/[모듈명].store.ts`가 존재해야 한다.
- Store가 없으면 먼저 `peach-gen-store`, UI가 없으면 `peach-gen-ui`를 기준으로 생성한다.
- 기존 기능 수정 맥락에서 실행하는 경우 `docs/기능별설명/{카테고리명}/{기능명}/`가 있으면 개요 → 로직 → 명세 → TDD 순으로 먼저 읽고 컨텍스트를 주입한다.

### prompt 모드

- 사전 조건 없음. 자연어 입력만 있으면 동작.
- 단, 변경 규모 추정 후 대규모로 판단되면 Spec 작성 권고가 자동으로 뜬다.

## Inputs

```bash
# 표준 모드 (Spec + ui-proto 기반)
/peach-team-dev [모듈명] mode=backend|ui|fullstack proto=<경로> [옵션]

# Spec만 모드 (proto 생략)
/peach-team-dev [모듈명] mode=backend|ui|fullstack [옵션]

# prompt 모드 (mode/proto 생략, 자연어 입력)
/peach-team-dev "버그/개선 사항 자연어 설명" [force=Y] [옵션]

# 공통 옵션
# model=sonnet|opus|haiku  (서브에이전트 모델 override, 기본값: sonnet)
# figma=[URL]
# ui=crud|page|two-depth|infinite-scroll|select-list
# file=Y
# excel=Y
# storeTdd=Y
```

| 인자 | 역할 |
|------|------|
| `[모듈명]` | 표준/Spec만 모드에서 권장. prompt 모드에서는 AI가 후보 제안 후 사용자 확정 |
| `mode` | 표준/Spec만 모드에서 필수 |
| `proto` | 선택. ui-proto 저장소의 태스크 폴더 절대 경로 |
| `prompt` | 위치 인자. 자연어 작업 설명 (mode/proto 없을 때) |
| `force` | 선택. prompt 모드에서 큰 변경에도 Spec 권고 무시하고 강제 진행 (`force=Y`) |
| `model` | 선택. 서브에이전트 모델 override |

## proto 인자 자동 처리

`proto=<경로>`가 주어지면 다음 절차를 자동 실행한다. 상세는 `references/proto-sync.md` 참조.

1. **proto 경로 검증** — 폴더 존재, `_spec.md` 존재
2. **메타 추출** — `_task-meta.ts`에서 `planner`, `date`, `title` 읽기
3. **Spec 자동 복사** — `_spec.md` → `docs/spec/{년}/{월}/{planner}-{YYMMDD}-{title}.md`
4. **충돌 감지** — 본 프로젝트에 같은 파일이 이미 있으면 사용자에게 (a) 덮어쓰기 / (b) 유지 / (c) diff 보기 선택
5. **컨텍스트 주입** — 복사된 Spec과 ui-proto 화면 폴더를 검증 기준으로 서브에이전트 프롬프트에 주입

## prompt 모드 동작

mode/proto 없이 자연어 입력이 주어지면 다음 절차로 동작한다. 상세는 `references/prompt-mode.md` 참조.

1. **입력 분석**
   - 작업 규모 추정 (단일 파일 vs 다중 파일, 신규 vs 수정)
   - 영향 범위 추정 (백엔드/UI/풀스택)
   - 모듈 후보 식별 (파일 경로, 도메인 키워드 기반)
   - 기존 기능 수정이면 `peach-doc-feature` 권고 여부 판단

2. **모듈명 확정 (사용자 확인)**
   - prompt 분석 결과로 모듈 후보 1~3개를 제안한다
   - 사용자가 선택 또는 직접 입력
   - 단일 후보가 명확하면 자동 채택 안내 후 진행

3. **분기**
   - **소규모** (단일 파일, 명확한 패턴): 즉시 단독 모드 실행
   - **중규모** (여러 파일, 단일 모듈): 팀 모드 실행, Spec 자동 생성 제안 (선택)
   - **대규모** (모듈 추가, 다중 모듈): Spec 권고 안내 → 사용자가 (a) `/peach-gen-spec` 작성 후 재진입 / (b) `force=Y`로 강제 진행 선택

4. **실행**
   - prompt를 임시 컨텍스트로 주입
   - 단독/팀 모드에 따라 서브에이전트 분배
   - 랄프루프 5회 (prompt 모드는 검증 기준이 약하므로 10회 비권장)

## 검증 우선순위 규칙

ui-proto는 본질적으로 Mock이라 100% 구현되지 않을 수 있다. 다음 우선순위를 적용한다.

| 검증 항목 | 1차 기준 | 2차 기준 |
|----------|---------|---------|
| 화면 레이아웃, 컴포넌트 배치 | ui-proto 화면 | (없으면 Spec) |
| 사용자 인터랙션 흐름 | ui-proto 화면 | Spec |
| 비즈니스 규칙 (검증, 권한, 분기) | Spec | (없으면 검증 불가 → 보고) |
| 데이터 정확성 (API 응답값) | Spec | (없으면 검증 불가 → 보고) |
| 에러/예외 처리 | Spec | - |

**핵심 원칙**: ui-proto가 있으면 ui-proto, 없거나 모호하면 Spec, 둘 다 모호하면 보고.

## Orchestration

### 0. 입력 검증

#### 에이전트 팀 기능 활성화 확인

```bash
cat ~/.claude/settings.json | grep -i "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"
```

설정이 없거나 `"1"`이 아니면 **즉시 중단**하고 다음 안내를 출력한다:

```
⚠️  에이전트 팀 기능이 비활성화되어 있습니다.

~/.claude/settings.json에 아래 내용을 추가한 후 Claude Code를 재시작하세요:

{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}

설정 가이드: https://github.com/peachSolution/peach-harness/blob/main/docs/06-에이전트팀-설정.md
```

#### 입력 모드 분기

다음 순서로 입력 형태를 판별한다.

```
1. 위치 인자가 자연어 문장이고 mode/proto 없음 → prompt 모드 진입
   → references/prompt-mode.md 절차 수행
2. mode 지정 + proto 인자 있음 → 표준 모드
   → references/proto-sync.md로 Spec 복사 후 진행
3. mode 지정 + proto 없음 → Spec만 모드
   → docs/spec/... 의 기존 Spec 사용
4. 모두 누락 → 사용자에게 모드 선택 안내
```

**mode 미지정 시 (Spec만 모드 진입 시도):**
```
mode를 선택해주세요:
1. backend — 기존 UI에 API + Store 연결
2. ui — Store 기반 UI만 구현
3. fullstack — DB 스키마 기반 전체 생성
```

**모듈명 미지정 시:**
- 표준/Spec만 모드: 직접 입력 요청
- prompt 모드: 위 "prompt 모드 동작 §2"에 따라 후보 제안 후 확정

**model 옵션:**
- 미지정: 기본값 sonnet으로 모든 서브에이전트 실행
- 지정 시: 모든 서브에이전트를 해당 모델로 override
- 허용 값: sonnet, opus, haiku

### 1. 환경 확인

```bash
# 스키마 / 타입 / 가이드 코드 확인
ls api/db/schema/
head -5 api/src/modules/test-data/dao/test-data.dao.ts
head -3 api/src/modules/test-data/controller/test-data.controller.ts
ls front/src/modules/test-data/

# DAO 라이브러리 감지
# from 'bunqldb' → 재할당 방식
# from 'sql-template-strings' → append 방식

# modules 분리 구조 감지
ls -d api/src/modules*/
ls -d front/src/modules*/

# _common 구성 감지
ls api/src/modules/_common/
ls api/src/modules/_common/constants/ 2>/dev/null

# 스킬 references 경로 감지
SKILL_BASE=$(dirname "$(find ~/.claude ~/.agents -path "*/peach-gen-backend/references" -type d 2>/dev/null | head -1)" 2>/dev/null)
```

### 1.5. 도메인 분석 (Analyze)

오케스트레이터가 대상 도메인의 스키마(또는 prompt 입력)를 읽고, test-data 대비 차이점을 파악한 뒤 서브에이전트 프롬프트에 컨텍스트로 주입한다.

```bash
# 표준/Spec만 모드: 대상 스키마 읽기
cat api/db/schema/[도메인]/[테이블].sql

# 표준 모드 추가: ui-proto 화면 폴더 분석
ls <proto경로>/
cat <proto경로>/_spec.md
```

**분석 항목**:
1. 스키마 비교: test-data 대비 필드 수, 타입 복잡도, 관계성
2. 비즈니스 로직 판단: 단순 CRUD vs 상태 전이/계산 필드/조건부 검증
3. 적응 결정: Must Follow → 그대로 / May Adapt → 도메인 맞춤 항목 식별
4. (표준 모드) ui-proto 화면 흐름과 Spec의 비즈니스 규칙 매핑

**분석 결과를 서브에이전트에게 전달**:
- 각 에이전트 생성 시 프롬프트에 "이 도메인의 특성: [분석 결과]"를 포함
- 모듈 생성 경로: `api/src/[감지된 modules 경로]/[모듈명]/`
- front 대응 경로: `front/src/[감지된 modules 경로]/[모듈명]/`
- _common 상수 목록: `[감지된 상수 파일 목록]` (존재 시 하드코딩 금지 지시)
- file 옵션 추론: 스키마에 파일 관련 요구가 보이면 `file=Y` 제안
- (표준 모드) 검증 기준 컨텍스트: ui-proto 화면 + Spec 부합 검증 지시
- references 경로 (역할별 분리 주입):
  - backend-dev: `${SKILL_BASE}/peach-gen-backend/references/`
  - store-dev: `${SKILL_BASE}/peach-gen-store/references/`
  - ui-dev: `${SKILL_BASE}/peach-gen-ui/references/`

5. **구조 제안 (May Suggest)**:
   도메인 분석 결과 가이드코드(test-data)와 다른 구조가 더 적합하다고 판단되면:
   - 제안 내용과 이유를 사용자에게 먼저 제시
   - 사용자 확인 후 서브에이전트 프롬프트에 반영

   **제안 가능 범위:**
   - service 파일 분리 (예: 상태전이 전용 service)
   - DAO 구성 변경 (예: 복합 조회용 DAO 분리)
   - 트랜잭션 서비스 필요 여부
   - 모듈 내부 하위 디렉토리 (예: step1/step2 단계별 분리)

   **제안 불가 (Must Follow):**
   - 모듈 경계, 네이밍, 타입 원칙 등

### 2. 팀 구성 다이어그램

**mode=backend**
```
backend-dev ──→ backend-qa
       │
       └──→ store-dev ──→ frontend-qa
```

**mode=ui**
```
ui-dev ──→ frontend-qa
```

**mode=fullstack**
```
backend-dev ──→ backend-qa
       │
       └──→ store-dev ──→ ui-dev ──→ frontend-qa
```

**prompt 모드 (소규모, 단독)**
```
단일 dev-agent (영향 범위에 따라 backend-dev / ui-dev / store-dev 중 1개)
       │
       └──→ 해당 qa-agent (랄프루프 5회)
```

### 3. 팀 생성 및 작업 등록

표준/Spec만 모드 (기존과 동일):

```
TeamCreate: team_name="[모듈명]-[mode]-team"

# mode=backend 작업 등록
TaskCreate:
1. "Backend API 개발" (owner: backend-dev)
2. "Backend QA 검증" (blockedBy: Task1, owner: backend-qa)
3. "Frontend Store 개발" (blockedBy: Task1, owner: store-dev)
4. "Frontend QA 검증" (blockedBy: Task3, owner: frontend-qa)

# mode=ui 작업 등록
TaskCreate:
1. "UI 컴포넌트 생성" (owner: ui-dev)
2. "Frontend QA 검증" (blockedBy: Task1, owner: frontend-qa)

# mode=fullstack 작업 등록
TaskCreate:
1. "Backend API 개발" (owner: backend-dev)
2. "Backend QA 검증" (blockedBy: Task1, owner: backend-qa)
3. "Frontend Store 개발" (blockedBy: Task1, owner: store-dev)
4. "Frontend UI 개발" (blockedBy: Task3, owner: ui-dev)
5. "Frontend QA 검증" (blockedBy: Task4, owner: frontend-qa)
```

prompt 모드 소규모는 팀 생성 생략하고 단일 에이전트에 직접 작업 위임. 중/대규모는 표준 모드와 동일한 팀 구성.

### 4. 역할별 지시

각 역할의 전체 정의(페르소나, Bounded Autonomy, 워크플로우)는 `references/`에 있다.
서브에이전트 생성 시 해당 파일의 전체 내용을 프롬프트에 포함한다.
`model=` 옵션이 지정된 경우, 각 에이전트 호출 시 model 파라미터로 전달하여 frontmatter 기본값을 override한다.

| 역할 | 참조 파일 | 핵심 패턴 |
|------|----------|----------|
| backend-dev | references/backend-dev-agent.md | test-data 가이드 코드 |
| backend-qa | references/backend-qa-agent.md | 검증 전용 (읽기전용, worktree) |
| store-dev | references/store-dev-agent.md | test-data 가이드 코드 |
| ui-dev | references/ui-dev-agent.md | test-data 가이드 코드 + 디자인 시스템 |
| frontend-qa | references/frontend-qa-agent.md | 검증 전용 (읽기전용, worktree) |

> 위 페르소나 정의는 **gen-* 스킬과 동일한 가이드 코드 패턴**을 가리킨다.
> 진짜 SoT는 대상 프로젝트의 `test-data/` 폴더이며, gen-* 스킬과 team-dev는
> 같은 패턴을 두 가지 호출 방식(단독/팀 컨텍스트)으로 사용한다.

#### backend-dev
- test-data 가이드 코드를 기준으로 API 코드를 생성한다.
- Koa/Elysia 모드를 감지한다.
- DAO 라이브러리(bunqldb/sql-template-strings)를 감지한다.
- 완료 기준: `bun test`, `bun run lint:fixed`, `bun run build` 통과
- 산출물: API 파일 목록, 엔드포인트 스펙, 테스트 결과
- 상세: `references/backend-dev-agent.md` 참조

#### backend-qa
**QA 체크리스트 (7항목)**:
1. `type/`, `dao/`, `service/`, `controller/`, `test/` 파일 구조 존재
2. Service static 메서드 규칙 준수
3. FK 제약조건 없음
4. `bun test` 통과
5. `bun run lint:fixed` 통과
6. `bun run build` 성공
7. API 엔드포인트 스펙 일치 (Spec 기반)
- 상세: `references/backend-qa-agent.md` 참조

#### store-dev
- test-data 가이드 코드를 기준으로 Pinia Store를 생성한다.
- Backend 타입과 인터페이스를 맞춘다.
- 완료 기준: `bunx vue-tsc --noEmit`
- 상세: `references/store-dev-agent.md` 참조

#### ui-dev
- test-data 가이드 코드 + (필요 시) 디자인 시스템을 사용한다.
- `figma=[URL]`가 있으면 FigmaRemote MCP를 로드하여 디자인을 분석한다.
- **표준 모드에서 proto 인자가 있으면 ui-proto 화면 폴더를 우선 참조**한다.
- UI 패턴(`ui=`)이 없으면 사용자에게 확인한다.
- 대상 프로젝트에 `_common/components/`가 존재하면 래퍼 컴포넌트를 우선 사용한다.
- 완료 기준: `bunx vue-tsc --noEmit`, `bun run lint:fix`, `bun run build`
- 상세: `references/ui-dev-agent.md` 참조

#### frontend-qa
**QA 체크리스트 (8항목 + 검증 우선순위 규칙)**:
1. 파일 구조 (pages/, modals/, store/, type/) 존재
2. Composition API (`<script setup>`) 패턴 준수
3. Pinia Option API Store 패턴 준수
4. `listAction`, `resetAction`, `listMovePage` 함수 구현
5. URL watch 패턴 적용 (`route → listParams`, `route → getList`)
6. `bunx vue-tsc --noEmit` 통과
7. `bun run lint:fix` 통과
8. `bun run build` 성공 + AI Slop 디자인 패턴 없음
9. **(proto 인자 있을 때)** ui-proto 화면 흐름과 일치, Spec 비즈니스 규칙 부합
- 상세: `references/frontend-qa-agent.md` 참조

## QA 판정 처리 (3단계)

QA 에이전트(backend-qa, frontend-qa)는 **APPROVED / CONDITIONAL / REJECTED** 3단계로 판정한다.
오케스트레이터가 Architect 역할을 수행하여 판정을 처리한다.

### ✅ APPROVED

```
QA → SendMessage → 오케스트레이터: "APPROVED" + 검증 결과
오케스트레이터 → /peach-qa-gate 자동 실행
→ 완료
```

### ⚠️ CONDITIONAL

```
QA → SendMessage → 오케스트레이터: "CONDITIONAL" + 조건 내용 + 왜 REJECTED가 아닌지 근거
오케스트레이터 판단:
    "조건 수용" → dev 에이전트에 수정 지시 → QA 재검증
    "조건 무시" → 판단 근거 기록 후 APPROVED로 처리
```

규칙:
- CONDITIONAL은 Ralph Loop가 아니다. 오케스트레이터 판단 전까지 완료 처리 금지.
- QA는 **조건 항목 최소 1개 + 왜 REJECTED가 아닌지 근거**를 함께 보고해야 한다.
- 오케스트레이터가 "무시"를 선택한 경우 근거를 최종 완료 보고에 포함한다.

### ❌ REJECTED → Ralph Loop 작동

REJECTED 시 단순 재시도가 아닌 **Ralph Loop**(Vercel Labs) 패턴으로 구조화된 피드백을 주입한다.

#### 에스컬레이션 단계

| 반복 횟수 | 단계 | 행동 |
|----------|------|------|
| 1~3회 | 자율 수정 | QA 피드백만으로 코드 수정 |
| 4회 | 가이드 재참조 | test-data 기준골격 전체 재읽기 후 수정 |
| 5~7회 | Codex 진단 | `codex:codex-rescue`로 실패 원인 독립 진단 + 가이드 재참조 |
| 8~10회 | 최소 수정 | Must Follow 항목만 집중, 나머지 보류 |
| 11+ | 중단 | 사용자 에스컬레이션 |

#### prompt 모드 랄프루프 상한

prompt 모드는 검증 기준이 약하므로 **5회를 상한**으로 둔다. 5회 초과 시 사용자에게 Spec 작성을 권고하고 중단한다.

#### Codex 투입 조건 (5~7회)

- `CODEX_AVAILABLE=true` 시에만 투입 (settings.json에서 `"codex@openai-codex": true` 감지)
- `CODEX_AVAILABLE=false`: Codex 없이 기존 Ralph Loop 계속 (가이드 재참조)
- Codex 무응답/타임아웃: 60초 대기 → 응답 없으면 스킵, 기존 피드백으로 진행
- Codex 진단 결과 부실: 오케스트레이터가 무시하고 기존 피드백으로 진행

#### 적용 방식

- Backend QA REJECTED → backend-dev 수정 → backend-qa 재검증 (SendMessage)
- Store 문제 → store-dev 수정 → frontend-qa 재검증
- UI 문제 → ui-dev 수정 → frontend-qa 재검증

#### 에스컬레이션 보고

```
## Ralph Loop 에스컬레이션
- 모듈: [모듈명]
- 모드: [표준 / Spec만 / prompt]
- 반복: N/10회 (prompt 모드는 N/5회)
- 단계: [현재 단계]
- 미해결: [위반 항목]
- 권장: [수동 개입 사항]
```

## Completion

모든 QA APPROVED 후:

### 1. 증거 수집
오케스트레이터가 `/peach-qa-gate`를 자동 실행 → 증거 보고서 생성
- 판정이 ❌이면 해당 항목 수정 후 재실행
- 판정이 ✅이면 다음 단계 진행

### 2. 팀 정리
```
SendMessage(shutdown_request) → 모든 팀원에게
TeamDelete → 팀 정리
```

## 완료 보고 형식

### 표준 모드 (proto 사용, mode=fullstack)

```
🎉 풀스택 개발 완료! (표준 모드)

모듈: [모듈명]
mode: fullstack
proto: [proto 경로]
Spec 사본: docs/spec/{년}/{월}/{planner}-{YYMMDD}-{title}.md

결과:
✅ Spec 자동 복사 완료
✅ backend-dev: API 생성 완료
✅ backend-qa: TDD X개 통과
✅ store-dev: Store 생성 완료
✅ ui-dev: UI 컴포넌트 생성 완료 (ui-proto 흐름 일치)
✅ frontend-qa: vue-tsc + lint + build 통과 + 검증 우선순위 규칙 부합

검증 우선순위 부합 결과:
- 화면 흐름: ui-proto 일치
- 비즈니스 규칙: Spec 부합
- (검증 불가 항목 있으면 보고)

생성된 파일:
[기존 형식 유지]

다음 단계:
→ /peach-team-e2e proto=[proto 경로] (E2E 검증)
```

### Spec만 모드 (기존 형식 유지)

기존 `peach-team`의 mode=backend / mode=ui / mode=fullstack 완료 보고 형식 그대로.

### prompt 모드

```
✅ 즉흥적 작업 완료 (prompt 모드)

입력: "[원본 prompt 텍스트]"
판정 규모: [소/중/대]
영향 범위: [backend / ui / fullstack]
선택 모듈: [확정된 모듈명]

결과:
✅ [실행한 dev 에이전트]: [작업 요약]
✅ [실행한 qa 에이전트]: [검증 결과]

변경 파일:
[변경된 파일 목록]

검증 한계:
- prompt 모드는 검증 기준이 약합니다. 결과를 직접 확인해주세요.
- (대규모였고 force=Y로 진행한 경우) Spec 사후 작성을 권장합니다.

다음 단계 (선택):
→ /peach-gen-spec (사후 Spec 작성)
→ /peach-team-e2e (E2E 검증)
```

## Examples

```bash
# === 표준 모드 (proto 사용) ===

# 풀스택 일괄
/peach-team-dev product-manage mode=fullstack proto=/Users/nettem/source/peachSolution2/peach-ui-proto-backoffice/src/modules-task/2604/260427-nettem-goods

# 백엔드 먼저
/peach-team-dev product-manage mode=backend

# UI 이어서 (proto 화면 기반)
/peach-team-dev product-manage mode=ui proto=/Users/.../260427-nettem-goods

# === Spec만 모드 (기존 패턴) ===

# 기존 UI에 API + Store 연결
/peach-team-dev notice-board mode=backend

# UI만 구현
/peach-team-dev member-list mode=ui ui=two-depth figma=https://figma.com/file/xxx

# 전체 풀스택 생성 (DB 스키마 기반)
/peach-team-dev product-manage mode=fullstack ui=page file=Y

# opus 모델로 서브에이전트 실행
/peach-team-dev product-manage mode=fullstack model=opus ui=page

# === prompt 모드 (자연어 입력) ===

# 즉흥적 버그 수정
/peach-team-dev "list.vue 검색 후 페이지네이션 클릭 시 검색어 초기화되는 문제 수정"

# 작은 기능 추가
/peach-team-dev "게시판 상세 화면에 인쇄 버튼 추가하고 인쇄 페이지도 만들어줘"

# 큰 변경 강제 진행 (Spec 권고 무시)
/peach-team-dev "주문 모듈에 환불 기능 전체 추가" force=Y
```

## 관련 스킬

- `peach-gen-spec` — Spec 단독 생성 (Tier 2)
- `peach-gen-ui-proto` — ui-proto 화면 단독 생성 (Tier 2)
- `peach-gen-backend`, `peach-gen-store`, `peach-gen-ui`, `peach-gen-db` — 단계별 단독 호출 (Tier 2)
- `peach-team-e2e` — E2E 검증 (다음 단계)
- `peach-team-3a` — 작은 단일 기능 (Architect→Builder→Reviewer 3-에이전트)
- `peach-doc-feature` — 기존 기능 As-Is 분석 (수정 작업 전)
