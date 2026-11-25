---
name: peach-agent-team
model: opus
description: |
  PeachSolution 신규 모듈 전체 개발을 조율하는 팀 오케스트레이터 스킬.
  "팀으로 만들어줘", "풀스택 개발", "백엔드+UI 전체 생성" 키워드로 트리거.
  mode=backend(API+Store), mode=ui(UI만), mode=fullstack(전체) 지원.
---

# Peach Agent Team

## Overview

PeachSolution 아키텍처에서 신규 기능 개발을 조율하는 통합 팀 스킬입니다.

기존 `team-backend`, `team-ui`, `team-fullstack`를 하나로 통합하며, 역할별 페르소나와 체크리스트를 이 문서 안에 포함합니다.

## Modes

| mode | 용도 | 포함 역할 |
| --- | --- | --- |
| `backend` | 기존 UI에 API + Store 연결 | backend-dev, backend-qa, store-dev, frontend-qa |
| `ui` | Store 기반 UI만 구현 | ui-dev, frontend-qa |
| `fullstack` | DB 스키마 기반 전체 생성 | backend-dev, backend-qa, store-dev, ui-dev, frontend-qa |

## Preconditions

- DB 스키마가 필요한 모드(`backend`, `fullstack`)에서는 `api/db/schema/[도메인]/[테이블].sql`이 존재해야 합니다.
- `ui` 모드에서는 `front/src/modules/[모듈명]/store/[모듈명].store.ts`가 존재해야 합니다.
- Store가 없으면 먼저 `peach-gen-store`, UI가 없으면 `peach-gen-ui`를 기준으로 생성합니다.
- 기존 기능 수정 맥락에서 실행하는 경우 `docs/기능별설명/{카테고리명}/{기능명}/`가 있으면 개요 → 로직 → 명세 → TDD 순으로 먼저 읽고 컨텍스트를 주입합니다.

## Inputs

```bash
/peach-agent-team [모듈명] mode=backend|ui|fullstack [옵션]

# 공통 옵션
# model=sonnet|opus|haiku  (서브에이전트 모델 override, 기본값: sonnet)
# figma=[URL]
# ui=crud|page|two-depth|infinite-scroll|select-list
# file=Y
# excel=Y
# storeTdd=Y
```

## Orchestration

### 0. 입력 검증

#### 에이전트 팀 기능 활성화 확인

아래 명령으로 `~/.claude/settings.json`에 에이전트 팀 플래그가 설정되어 있는지 확인합니다:

```bash
cat ~/.claude/settings.json | grep -i "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"
```

설정이 없거나 `"1"`이 아니면 **즉시 중단**하고 다음 안내를 출력합니다:

```
⚠️  에이전트 팀 기능이 비활성화되어 있습니다.

~/.claude/settings.json에 아래 내용을 추가한 후 Claude Code를 재시작하세요:

{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}

설정 가이드: https://github.com/peachSolution/peach-harness/blob/main/docs/06-에이전트팀-설정.md
공식 문서: https://code.claude.com/docs/ko/agent-teams
```

---

mode와 모듈명이 모두 지정되어야 다음 단계로 진행합니다.
누락된 경우 **반드시** 개발자에게 질문합니다.

**mode 미지정 시:**
```
mode를 선택해주세요:
1. backend — 기존 UI에 API + Store 연결
2. ui — Store 기반 UI만 구현
3. fullstack — DB 스키마 기반 전체 생성
```

**모듈명 미지정 시:**
```
모듈명을 입력해주세요 (예: notice-board, product-manage):
```

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
```

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

### 3. 팀 생성 및 작업 등록

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

### 4. 역할별 지시

각 역할의 전체 정의(페르소나, Bounded Autonomy, 워크플로우)는 `references/`에 있습니다.
서브에이전트 생성 시 해당 파일의 전체 내용을 프롬프트에 포함합니다.
`model=` 옵션이 지정된 경우, 각 에이전트 호출 시 model 파라미터로 전달하여 frontmatter 기본값을 override합니다.

| 역할 | 참조 파일 | 핵심 스킬 |
|------|----------|----------|
| backend-dev | references/backend-dev-agent.md | peach-gen-backend |
| backend-qa | references/backend-qa-agent.md | 검증 전용 (읽기전용, worktree) |
| store-dev | references/store-dev-agent.md | peach-gen-store |
| ui-dev | references/ui-dev-agent.md | peach-gen-ui + peach-gen-design |
| frontend-qa | references/frontend-qa-agent.md | 검증 전용 (읽기전용, worktree) |

#### backend-dev
- `peach-gen-backend` 기준으로 API 코드를 생성합니다.
- Koa/Elysia 모드를 감지합니다.
- DAO 라이브러리(bunqldb/sql-template-strings)를 감지합니다.
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
7. API 엔드포인트 스펙 일치
- 상세: `references/backend-qa-agent.md` 참조

#### store-dev
- `peach-gen-store` 기준으로 Pinia Store를 생성합니다.
- Backend 타입과 인터페이스를 맞춥니다.
- 완료 기준: `bunx vue-tsc --noEmit`
- 상세: `references/store-dev-agent.md` 참조

#### ui-dev
- `peach-gen-ui`, 필요 시 `peach-gen-design`을 사용합니다.
- `figma=[URL]`가 있으면 FigmaRemote MCP를 로드하여 디자인을 분석합니다.
- UI 패턴(`ui=`)이 없으면 사용자에게 확인합니다.
- 대상 프로젝트에 `_common/components/`가 존재하면 래퍼 컴포넌트를 우선 사용합니다.
- 완료 기준: `bunx vue-tsc --noEmit`, `bun run lint:fix`, `bun run build`
- 상세: `references/ui-dev-agent.md` 참조

#### frontend-qa
**QA 체크리스트 (8항목)**:
1. 파일 구조 (pages/, modals/, store/, type/) 존재
2. Composition API (`<script setup>`) 패턴 준수
3. Pinia Option API Store 패턴 준수
4. `listAction`, `resetAction`, `listMovePage` 함수 구현
5. URL watch 패턴 적용 (`route → listParams`, `route → getList`)
6. `bunx vue-tsc --noEmit` 통과
7. `bun run lint:fix` 통과
8. `bun run build` 성공 + AI Slop 디자인 패턴 없음
- 상세: `references/frontend-qa-agent.md` 참조

## Ralph Loop (반복 검증 메커니즘)

QA 실패 시 단순 재시도가 아니라 **Ralph Loop**(Vercel Labs) 패턴으로 구조화된 피드백을 주입한다.

### 에스컬레이션 단계

| 반복 횟수 | 단계 | 행동 |
|----------|------|------|
| 1~3회 | 자율 수정 | QA 피드백만으로 코드 수정 |
| 4~7회 | 가이드 재참조 | test-data 기준골격 전체 재읽기 후 수정 |
| 8~10회 | 최소 수정 | Must Follow 항목만 집중, 나머지 보류 |
| 11+ | 중단 | 사용자 에스컬레이션 |

### 적용 방식

- Backend QA 실패 → backend-dev 수정 → backend-qa 재검증 (SendMessage)
- Store 문제 → store-dev 수정 → frontend-qa 재검증
- UI 문제 → ui-dev 수정 → frontend-qa 재검증

### 에스컬레이션 보고

```
## Ralph Loop 에스컬레이션
- 모듈: [모듈명]
- 반복: N/10회
- 단계: [현재 단계]
- 미해결: [위반 항목]
- 권장: [수동 개입 사항]
```

## Completion

모든 QA 통과 후:

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

### mode=backend

```
✅ Backend + Store 연결 팀 개발 완료

모듈: [모듈명]
mode: backend

결과:
✅ backend-dev: API 생성 완료
✅ backend-qa: TDD X개 통과
✅ store-dev: Store 생성 완료
✅ frontend-qa: vue-tsc + lint + build 통과
✅ qa-gate: 증거 보고서 생성 + 완료 가능 판정

생성된 파일:
Backend:
├── api/src/modules/[모듈명]/type/
├── api/src/modules/[모듈명]/dao/
├── api/src/modules/[모듈명]/service/
├── api/src/modules/[모듈명]/controller/
└── api/src/modules/[모듈명]/test/

Frontend:
├── front/src/modules/[모듈명]/type/[모듈명].type.ts
└── front/src/modules/[모듈명]/store/[모듈명].store.ts

다음 단계:
→ bun start (Backend 실행)
→ bun run dev (Frontend 실행)
→ 브라우저에서 /[모듈명]/list 접속
```

### mode=ui

```
✅ UI Only 팀 개발 완료

모듈: [모듈명]
mode: ui
패턴: [ui=패턴]
피그마: [URL 또는 없음]

결과:
✅ ui-dev: UI 컴포넌트 생성 완료
✅ frontend-qa: vue-tsc + lint + build 통과

생성된 파일:
├── front/src/modules/[모듈명]/pages/list.vue
├── front/src/modules/[모듈명]/pages/list-search.vue
├── front/src/modules/[모듈명]/pages/list-table.vue
├── front/src/modules/[모듈명]/modals/insert.modal.vue
├── front/src/modules/[모듈명]/modals/update.modal.vue
├── front/src/modules/[모듈명]/modals/detail.modal.vue
├── front/src/modules/[모듈명]/_[모듈명].routes.ts
└── front/src/modules/[모듈명]/_[모듈명].validator.ts

다음 단계:
→ bun run dev (Frontend 실행)
→ 브라우저에서 /[모듈명]/list 접속
```

### mode=fullstack

```
🎉 풀스택 개발 완료!

모듈: [모듈명]
mode: fullstack

결과:
✅ backend-dev: API 생성 완료
✅ backend-qa: TDD X개 통과
✅ store-dev: Store 생성 완료
✅ ui-dev: UI 컴포넌트 생성 완료
✅ frontend-qa: vue-tsc + lint + build 통과

생성된 파일:
Backend:
├── api/src/modules/[모듈명]/type/
├── api/src/modules/[모듈명]/dao/
├── api/src/modules/[모듈명]/service/
├── api/src/modules/[모듈명]/controller/
└── api/src/modules/[모듈명]/test/

Frontend:
├── front/src/modules/[모듈명]/type/
├── front/src/modules/[모듈명]/store/
├── front/src/modules/[모듈명]/pages/
├── front/src/modules/[모듈명]/modals/
├── front/src/modules/[모듈명]/_[모듈명].routes.ts
└── front/src/modules/[모듈명]/_[모듈명].validator.ts

다음 단계:
→ bun start (Backend 실행)
→ bun run dev (Frontend 실행)
→ 브라우저에서 /[모듈명]/list 접속
```

## Examples

```bash
# 기존 UI에 API + Store 연결
/peach-agent-team notice-board mode=backend

# UI만 구현
/peach-agent-team member-list mode=ui ui=two-depth figma=https://figma.com/file/xxx

# 전체 풀스택 생성
/peach-agent-team product-manage mode=fullstack ui=page file=Y

# opus 모델로 서브에이전트 실행
/peach-agent-team product-manage mode=fullstack model=opus ui=page
```
