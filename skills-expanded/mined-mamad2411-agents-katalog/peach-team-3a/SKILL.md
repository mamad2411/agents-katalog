---
name: peach-team-3a
model: opus
description: |
  3-에이전트(Architect→Builder→Reviewer) 루프로 단일 기능을 설계·구현·검증하는 팀 스킬.
  "3a로 만들어줘", "3에이전트", "설계-구현-검토", "team-3a" 키워드로 트리거.
  peach-team보다 가벼운 단일 기능·소규모 수정에 적합.
---

# Peach Team 3A

## Overview

**Architect → Builder → Reviewer → Architect** 루프로 단일 기능을 완성하는 3-에이전트 팀 스킬입니다.

| 에이전트 | 역할 | 핵심 원칙 |
|---------|------|----------|
| **Architect** | 설계 계획 수립 + 최종 결정권 | BRIEF를 SendMessage로 전달 → Reviewer 판정 수용/거부 |
| **Builder** | BRIEF 기반 코드 구현 | 범위 밖 터치 금지, 완료 후 파일 수정 금지, 자기 검토 + 검증 증거 제출 |
| **Reviewer** | 독립 검증 + 3단계 판정 | qa-gate + 코드 리뷰 통합, 읽기전용, worktree 격리, CONDITIONAL 남용 금지 |

### peach-team과의 차이

| | peach-team | peach-team-3a |
|--|-----------|--------------|
| 에이전트 수 | 최대 5개 | 3개 고정 |
| 적합 케이스 | 대규모 fullstack | 단일 기능, 소규모 수정 |
| 판정 방식 | 통과/실패 2단계 | APPROVED / CONDITIONAL / REJECTED 3단계 |
| 애매한 경우 | 무조건 재작업 | Architect가 최종 판단 |

## Inputs

```bash
/peach-team-3a [작업 설명]

# 옵션
# model=sonnet|opus|haiku  (서브에이전트 모델 override, 기본값: sonnet)
# layer=backend|frontend|fullstack  (구현 범위, 미지정 시 Architect가 판단)
```

## Orchestration

### 0. 입력 검증

#### 에이전트 팀 기능 활성화 확인

```bash
cat ~/.claude/settings.json | grep -i "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"
```

설정이 없거나 `"1"`이 아니면 **즉시 중단**하고 안내를 출력합니다:

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

---

작업 설명이 누락된 경우 질문합니다:

```
어떤 기능을 구현할까요? (예: "공지사항 목록 API 추가", "회원 상태 필드 수정")
```

**model 옵션:**
- 미지정: 기본값 sonnet으로 서브에이전트 실행
- 지정 시: 모든 서브에이전트를 해당 모델로 override
- 허용 값: sonnet, opus, haiku

### 1. 환경 확인

```bash
# 프로젝트 구조 파악
ls api/src/modules/ 2>/dev/null
ls front/src/modules/ 2>/dev/null

# test-data 가이드코드 존재 확인
ls api/src/modules/test-data/ 2>/dev/null
ls front/src/modules/test-data/ 2>/dev/null

# DAO 라이브러리 감지
head -5 api/src/modules/test-data/dao/test-data.dao.ts 2>/dev/null
# from 'bunqldb' → 재할당 방식
# from 'sql-template-strings' → append 방식

# Controller 프레임워크 감지
head -3 api/src/modules/test-data/controller/test-data.controller.ts 2>/dev/null

# _common 구성 감지
ls api/src/modules/_common/ 2>/dev/null
ls api/src/modules/_common/constants/ 2>/dev/null

# 스킬 references 경로 감지
SKILL_BASE=$(dirname "$(find ~/.claude ~/.agents -path "*/peach-gen-backend/references" -type d 2>/dev/null | head -1)" 2>/dev/null)
```

### 2. 팀 구성 다이어그램

```
Architect
   │
   │ SendMessage: BRIEF 전달
   ▼
Builder ──────────────────────────────────┐
   │                                       │ REJECTED → Ralph Loop
   │ SendMessage: 구현 완료 + 자기 검토     │
   ▼                                       │
Reviewer (worktree 격리)                  │
   │                                       │
   ├── APPROVED ──→ SendMessage → Architect│
   ├── CONDITIONAL → SendMessage → Architect│
   └── REJECTED ──→ SendMessage → Builder ─┘
```

### 3. 팀 생성 및 작업 등록

```
TeamCreate: team_name="3a-[작업축약명]-team"

TaskCreate:
1. "설계 계획 수립" (owner: architect)
2. "코드 구현" (blockedBy: Task1, owner: builder)
3. "검증 및 판정" (blockedBy: Task2, owner: reviewer)
```

### 4. 역할별 지시

각 역할의 전체 정의는 `references/`에 있습니다.
서브에이전트 생성 시 해당 파일의 전체 내용을 프롬프트에 포함합니다.
`model=` 옵션이 지정된 경우, model 파라미터로 전달하여 frontmatter 기본값을 override합니다.

| 역할 | 참조 파일 | 실행 환경 |
|------|----------|----------|
| architect | references/architect-agent.md | 일반 |
| builder | references/builder-agent.md | 일반 |
| reviewer | references/reviewer-agent.md | worktree 격리 |

#### Architect 지시 포인트

오케스트레이터가 Architect 에이전트 생성 시 프롬프트에 포함할 컨텍스트:

- 작업 설명: `[사용자 입력 그대로]`
- 환경 정보: DAO 라이브러리, Controller 프레임워크, modules 경로, _common 상수 목록
- 가이드코드 위치: `api/src/modules/test-data/`, `front/src/modules/test-data/`
- references 경로: `${SKILL_BASE}/peach-gen-backend/references/`, `${SKILL_BASE}/peach-gen-ui/references/`
- 상세: `references/architect-agent.md` 참조

#### Builder 지시 포인트

Architect가 BRIEF를 SendMessage로 전달한 후 Builder를 스핀업합니다.
오케스트레이터는 Builder 에이전트 생성 시 아래를 포함합니다:

- Architect의 BRIEF 내용 (SendMessage로 수신한 전체 텍스트)
- 환경 정보: Architect 지시와 동일
- 상세: `references/builder-agent.md` 참조

#### Reviewer 지시 포인트

Builder가 구현 완료를 SendMessage로 보고한 후 Reviewer를 스핀업합니다.
오케스트레이터는 Reviewer 에이전트 생성 시 아래를 포함합니다:

- Builder의 구현 보고 내용 (구현 파일 목록 + 자기 검토 결과)
- Architect의 BRIEF 내용 (판정 기준)
- 상세: `references/reviewer-agent.md` 참조

### 5. Reviewer 판정 처리

Reviewer가 판정 결과를 SendMessage로 오케스트레이터에게 보고하면, 오케스트레이터가 처리합니다.

#### ✅ APPROVED

```
Reviewer → SendMessage → 오케스트레이터: "APPROVED" + 검증 결과
오케스트레이터 → SendMessage → Architect: 완료 보고
오케스트레이터 → /peach-qa-gate 자동 실행 (최종 증거 수집)
오케스트레이터 → 팀 정리
```

#### ⚠️ CONDITIONAL

```
Reviewer → SendMessage → 오케스트레이터: "CONDITIONAL" + 조건 내용
오케스트레이터 → SendMessage → Architect: 조건 전달 + 판단 요청
Architect → SendMessage → 오케스트레이터:
    "조건 수용" → 오케스트레이터 → SendMessage → Builder: 수정 지시 → Reviewer 재검증
    "조건 무시" → 판단 근거 기록 후 APPROVED로 처리
```

규칙:
- CONDITIONAL은 Ralph Loop가 아닙니다. Architect 판단 전까지 완료 처리 금지입니다.
- Reviewer는 **조건 항목 + 왜 REJECTED가 아닌지 이유**를 함께 보고해야 합니다.
- Architect가 "무시"를 선택한 경우 오케스트레이터는 근거를 최종 완료 보고에 포함합니다.

#### ❌ REJECTED — Ralph Loop 작동

```
Reviewer → SendMessage → 오케스트레이터: "REJECTED" + 수정 필요 항목
오케스트레이터 → Ralph Loop 단계 판단
오케스트레이터 → SendMessage → Builder: 피드백 + 수정 지시
Builder 수정 완료 → SendMessage → 오케스트레이터 → Reviewer 재검증
```

## Ralph Loop (반복 검증 메커니즘)

REJECTED 시 단순 재시도가 아닌 **구조화된 피드백 주입**으로 반복합니다.

### 에스컬레이션 단계

| 반복 횟수 | 단계 | 행동 |
|----------|------|------|
| 1~3회 | 자율 수정 | Reviewer 피드백만으로 Builder 수정 |
| 4회 | 가이드 재참조 | test-data 기준골격 전체 재읽기 후 수정 |
| 5~7회 | Codex 진단 | `codex:codex-rescue`로 실패 원인 독립 진단 + 가이드 재참조 |
| 8~10회 | 최소 수정 | Must Follow 항목만 집중, 나머지 보류 |
| 11+ | 중단 | 사용자 에스컬레이션 |

#### Codex 투입 조건 (5~7회 또는 REJECTED 2회 연속)

- `CODEX_AVAILABLE=true` 시에만 투입 (settings.json에서 `"codex@openai-codex": true` 감지)
- **REJECTED 2회 연속 시**: Ralph Loop 5회 대기 없이 즉시 `codex:codex-rescue` 투입 (3A는 소규모 루프 특성상 조기 탈출 유도)
- `CODEX_AVAILABLE=false`: Codex 없이 기존 Ralph Loop 계속 (가이드 재참조)
- Codex 무응답/타임아웃: 60초 대기 → 응답 없으면 스킵, 기존 피드백으로 진행
- Codex 진단 결과 부실: 오케스트레이터가 무시하고 기존 피드백으로 진행

### 에스컬레이션 보고

```
## Ralph Loop 에스컬레이션
- 작업: [작업 설명]
- 반복: N/10회
- 단계: [현재 단계]
- 미해결: [위반 항목]
- 권장: [수동 개입 사항]
```

## 에이전트 간 통신 구조

peach-team 계열과 동일하게 **SendMessage + TaskUpdate**로 통신합니다.

```
Architect → 오케스트레이터 (SendMessage): BRIEF 내용
오케스트레이터 → Builder 프롬프트에 BRIEF 포함하여 스핀업
Builder → 오케스트레이터 (SendMessage): 구현 완료 + 자기 검토 + 파일 목록
오케스트레이터 → Reviewer 프롬프트에 BRIEF + 구현 보고 포함하여 스핀업
Reviewer → 오케스트레이터 (SendMessage): 판정 + 검증 결과
```

각 단계 완료 시 **TaskUpdate**로 상태를 갱신합니다:
- Task #1 (설계): Architect 완료 → `completed`
- Task #2 (구현): Builder 완료 → `completed`
- Task #3 (검증): Reviewer APPROVED → `completed` / REJECTED → Builder 재작업

## Completion

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
✅ 3A 팀 작업 완료

작업: [작업 설명]
반복: [총 Reviewer 검증 횟수]회

결과:
✅ Architect: BRIEF 수립 완료
✅ Builder: 구현 완료
✅ Reviewer: APPROVED (또는 CONDITIONAL → Architect 수용)
✅ qa-gate: 증거 보고서 생성 + 완료 가능 판정

생성/수정된 파일:
[파일 목록]

다음 단계:
[실행 방법 안내]
```

## Examples

```bash
# 단일 API 추가
/peach-team-3a 공지사항 목록 조회 API 추가

# 기존 기능 수정
/peach-team-3a 회원 상태 필드에 '정지' 값 추가 layer=backend

# UI 컴포넌트 수정
/peach-team-3a 상품 목록 페이지에 엑셀 다운로드 버튼 추가 layer=frontend

# opus 모델로 실행
/peach-team-3a 결제 상태 전이 로직 구현 model=opus
```
