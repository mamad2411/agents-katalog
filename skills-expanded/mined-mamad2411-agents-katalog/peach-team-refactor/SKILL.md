---
name: peach-team-refactor
model: opus
description: |
  기존 PeachSolution 모듈을 test-data 패턴으로 리팩토링하는 팀 오케스트레이터 스킬.
  "팀 리팩토링", "레거시 코드 정리", "test-data 패턴으로 변환" 키워드로 트리거.
  layer=backend|frontend|all 지원, 독립 QA로 확증 편향 방지.
---

# Peach Agent Team Refactor

## Overview

PeachSolution 레거시 모듈을 `test-data` 패턴으로 변환하는 리팩토링 전용 팀 스킬입니다.

기존 `team-refactor`를 대체하며, backend/frontend 역할 정의와 QA 절차를 이 문서 안에 포함합니다.

## Inputs

```bash
/peach-agent-team-refactor [모듈명] layer=backend|frontend|all [옵션]

# 옵션
# model=sonnet|opus|haiku  (서브에이전트 모델 override, 기본값: sonnet)
# file=Y|N
# ui=crud|two-depth|select-list
# tdd=Y|N
```

## Preconditions

- 리팩토링 대상 모듈이 존재해야 합니다.
- Backend 리팩토링 시 DB 스키마가 존재해야 합니다.
- 기능 변경이 아니라 구조 정리만 수행합니다.

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

layer와 모듈명이 모두 지정되어야 다음 단계로 진행합니다.
누락된 경우 **반드시** 개발자에게 질문합니다.

**layer 미지정 시:**
```
layer를 선택해주세요:
1. backend — Backend만 리팩토링
2. frontend — Frontend만 리팩토링
3. all — 전체 리팩토링
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
# 레거시 모듈 존재 확인
ls api/src/modules/[모듈명]/
ls front/src/modules/[모듈명]/

# DAO 라이브러리 감지 (중요!)
head -5 api/src/modules/test-data/dao/test-data.dao.ts
# from 'bunqldb' → 재할당 방식 (sql`${query} AND ...`)
# from 'sql-template-strings' → append 방식 (.append(SQL`AND ...`))

# Controller 프레임워크 감지
head -3 api/src/modules/test-data/controller/test-data.controller.ts
# routing-controllers → Koa / elysia / createElysia → Elysia

# DB 스키마 확인
ls api/db/schema/
```

### 1.5. 레거시 코드 분석 (Analyze)

오케스트레이터가 레거시 모듈의 현재 상태를 분석하고, 서브에이전트 프롬프트에 컨텍스트로 주입합니다.

```bash
# 레거시 코드 구조 파악
ls -la api/src/modules/[모듈명]/
ls -la front/src/modules/[모듈명]/

# 주요 파일 읽기
cat api/src/modules/[모듈명]/**/*.ts
cat front/src/modules/[모듈명]/**/*.{vue,ts}
```

**분석 항목**:
1. 구조 gap: test-data 대비 파일 분리 상태, 네이밍 불일치
2. 로직 gap: test-data에 없는 비즈니스 로직 식별
3. 보존 목록: 기능으로서 반드시 유지해야 할 로직 목록화
4. 적응 결정: Must Follow → 강제 변환 / May Adapt → 보존할 로직과 변환 방식

**분석 결과를 서브에이전트에게 전달**:
- 각 에이전트 생성 시 프롬프트에 "레거시 분석 결과: [gap 목록], 보존 로직: [목록]"을 포함

### 2. 팀 구성 다이어그램

**layer=all**
```
refactor-backend ──→ backend-qa        (병렬)
         │
         └──→ refactor-frontend ──→ frontend-qa
```

**layer=backend**
```
refactor-backend ──→ backend-qa
```

**layer=frontend**
```
refactor-frontend ──→ frontend-qa
```

### 3. 팀 생성

```
TeamCreate: team_name="[모듈명]-refactor-team"

# layer=all
TaskCreate:
1. "Backend 리팩토링" (owner: refactor-backend)
2. "Backend QA 검증" (blockedBy: Task1, owner: backend-qa)
3. "Frontend 리팩토링" (blockedBy: Task1, owner: refactor-frontend)
4. "Frontend QA 검증" (blockedBy: Task3, owner: frontend-qa)

# layer=backend
TaskCreate:
1. "Backend 리팩토링" (owner: refactor-backend)
2. "Backend QA 검증" (blockedBy: Task1, owner: backend-qa)

# layer=frontend
TaskCreate:
1. "Frontend 리팩토링" (owner: refactor-frontend)
2. "Frontend QA 검증" (blockedBy: Task1, owner: frontend-qa)
```

## 역할별 지시

각 역할의 전체 정의(페르소나, Bounded Autonomy, 워크플로우)는 `references/`에 있습니다.
서브에이전트 생성 시 해당 파일의 전체 내용을 프롬프트에 포함합니다.
`model=` 옵션이 지정된 경우, 각 에이전트 호출 시 model 파라미터로 전달하여 frontmatter 기본값을 override합니다.

| 역할 | 참조 파일 | 핵심 스킬 |
|------|----------|----------|
| refactor-backend | references/refactor-backend-agent.md | peach-refactor-backend |
| backend-qa | references/backend-qa-agent.md | 검증 전용 (읽기전용, worktree) |
| refactor-frontend | references/refactor-frontend-agent.md | peach-refactor-frontend |
| frontend-qa | references/frontend-qa-agent.md | 검증 전용 (읽기전용, worktree) |

#### refactor-backend
- `peach-refactor-backend` 기준으로 type/dao/service/controller/test를 정리합니다.
- **DAO 라이브러리 분기**:
  - `bunqldb` 감지 시: 재할당 방식 (`sql\`${query} AND field = ${val}\``)
  - `sql-template-strings` 감지 시: append 방식 (`.append(SQL\`AND field = ${val}\``)
- 기존 기능은 유지하고 구조만 개선합니다.
- 4단계 리팩토링 순서: Type → DAO → Service/Controller → TDD
- 완료 기준: `bun test`, `bun run lint:fixed`, `bun run build`
- 상세: `references/refactor-backend-agent.md` 참조

#### backend-qa
- 리팩토링 후 구조, 패턴, 테스트, 빌드를 검증합니다.
- `test-data` 패턴 준수 여부를 확인합니다.
- **QA 체크리스트 (7항목)**:
  1. `type/`, `dao/`, `service/`, `controller/`, `test/` 구조 존재
  2. Service static 메서드 규칙 준수
  3. FK 제약조건 없음
  4. `bun test` 통과
  5. `bun run lint:fixed` 통과
  6. `bun run build` 성공
  7. 기능 100% 보존 확인
- 상세: `references/backend-qa-agent.md` 참조

#### refactor-frontend
- `peach-refactor-frontend` 기준으로 type/store/pages/modals를 정리합니다.
- URL watch 패턴, Composition API, Pinia Option API를 강제합니다.
- 3단계 리팩토링 순서: Type & Store → Pages → Modals
- 완료 기준: `bunx vue-tsc --noEmit`, `bun run lint:fix`, `bun run build`
- 상세: `references/refactor-frontend-agent.md` 참조

#### frontend-qa
- 파일 구조, watch 패턴, UI 패턴, 빌드 결과를 검증합니다.
- 금지된 UI 패턴과 타입 규칙 위반 여부를 확인합니다.
- **QA 체크리스트 (8항목)**:
  1. 파일 구조 (pages/, modals/, store/, type/) 존재
  2. Composition API (`<script setup>`) 패턴 준수
  3. Pinia Option API Store 패턴 준수
  4. URL watch 패턴 적용 여부
  5. `listAction`, `resetAction`, `listMovePage` 함수 존재
  6. `bunx vue-tsc --noEmit` 통과
  7. `bun run lint:fix` 통과
  8. `bun run build` 성공 + AI Slop 제거 확인
- 상세: `references/frontend-qa-agent.md` 참조

## QA 판정 처리 (3단계)

QA 에이전트(backend-qa, frontend-qa)는 **APPROVED / CONDITIONAL / REJECTED** 3단계로 판정합니다.
오케스트레이터가 Architect 역할을 수행하여 판정을 처리합니다.

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
- CONDITIONAL은 Ralph Loop가 아닙니다. 오케스트레이터 판단 전까지 완료 처리 금지.
- QA는 **조건 항목 최소 1개 + 왜 REJECTED가 아닌지 근거**를 함께 보고해야 합니다.
- 오케스트레이터가 "무시"를 선택한 경우 근거를 최종 완료 보고에 포함합니다.

### ❌ REJECTED → Ralph Loop 작동

REJECTED 시 **Ralph Loop**(Vercel Labs) 패턴으로 구조화된 피드백을 주입합니다.

#### 에스컬레이션 단계

| 반복 횟수 | 단계 | 행동 |
|----------|------|------|
| 1~3회 | 자율 수정 | QA 피드백만으로 코드 수정 |
| 4회 | 가이드 재참조 | test-data 기준골격 전체 재읽기 후 수정 |
| 5~7회 | Codex 진단 | `codex:codex-rescue`로 실패 원인 독립 진단 + 가이드 재참조 |
| 8~10회 | 최소 수정 | Must Follow 항목만 집중, 나머지 보류 |
| 11+ | 중단 | 사용자 에스컬레이션 |

#### Codex 투입 조건 (5~7회)

- `CODEX_AVAILABLE=true` 시에만 투입 (settings.json에서 `"codex@openai-codex": true` 감지)
- `CODEX_AVAILABLE=false`: Codex 없이 기존 Ralph Loop 계속 (가이드 재참조)
- Codex 무응답/타임아웃: 60초 대기 → 응답 없으면 스킵, 기존 피드백으로 진행
- Codex 진단 결과 부실: 오케스트레이터가 무시하고 기존 피드백으로 진행

#### 적용 방식

- Backend QA REJECTED → refactor-backend 수정 → backend-qa 재검증 (SendMessage)
- Frontend QA REJECTED → refactor-frontend 수정 → frontend-qa 재검증

#### 에스컬레이션 보고

```
## Ralph Loop 에스컬레이션
- 모듈: [모듈명]
- 반복: N/10회
- 단계: [현재 단계]
- 미해결: [위반 항목]
- 권장: [수동 개입 사항]
```

## Completion

기능 100% 보존과 QA APPROVED가 모두 확인되어야 완료입니다.

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

```
✅ 리팩토링 팀 작업 완료

모듈: [모듈명]
layer: [all|backend|frontend]

결과:
✅ refactor-backend: Backend 리팩토링 완료
✅ backend-qa: TDD X개 통과
✅ refactor-frontend: Frontend 리팩토링 완료
✅ frontend-qa: vue-tsc + lint + build 통과
✅ qa-gate: 증거 보고서 생성 + 완료 가능 판정

리팩토링된 파일:
Backend:
├── api/src/modules/[모듈명]/type/
├── api/src/modules/[모듈명]/dao/
├── api/src/modules/[모듈명]/service/
├── api/src/modules/[모듈명]/controller/
└── api/src/modules/[모듈명]/test/

Frontend:
├── front/src/modules/[모듈명]/type/[모듈명].type.ts
├── front/src/modules/[모듈명]/store/[모듈명].store.ts
├── front/src/modules/[모듈명]/pages/
└── front/src/modules/[모듈명]/modals/

변경 요약:
- [레거시 패턴 → 신규 패턴 목록]
- [제거된 AI Slop 항목]
- [개선된 구조 설명]
```

## Examples

```bash
# 전체 리팩토링
/peach-agent-team-refactor notice-board layer=all

# Backend만 리팩토링
/peach-agent-team-refactor product-manage layer=backend tdd=Y

# Frontend만 리팩토링
/peach-agent-team-refactor member-data layer=frontend ui=two-depth

# opus 모델로 전체 리팩토링
/peach-agent-team-refactor notice-board layer=all model=opus
```
