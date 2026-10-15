---
name: peach-skill-feedback
description: |
  피치 스킬 사용 중 발견된 문제점/노하우를 구조화하여 docs/스킬피드백/에 문서화하는 범용 스킬.
  "스킬 개선", "피드백 정리", "문제점 기록", "스킬 리뷰", "개선사항", "스킬 피드백" 키워드로 트리거.
  모든 피치 스킬에 범용 적용 가능. 다른 AI 에이전트가 문서를 읽고 스킬을 개선할 수 있도록 구성.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# peach-skill-feedback — 스킬 개선 피드백 문서화

> ⛔ **이 스킬의 책임 범위: 문서 생성까지**
>
> - **할 것**: 피드백 문서(`docs/스킬피드백/TODO-*.md`) 생성
> - **하지 말 것**: 대상 스킬의 SKILL.md 수정, references/ 파일 변경, 코드 수정
>
> 문서를 생성하고 사용자에게 경로를 알려주면 이 스킬의 역할은 끝난다.
> 실제 스킬 반영은 **다른 세션의 다른 AI 에이전트**가 문서를 읽고 수행한다.

피치 스킬을 사용하면서 발견한 **문제점, 우회 방법, 노하우, 개선 방향**을 구조화하여
`docs/스킬피드백/`에 날짜별 한글 파일로 저장한다.

다른 AI 에이전트가 이 문서를 읽고 **바로 스킬 업데이트 작업을 시작**할 수 있도록
문제 분석 + 검증 시나리오 + 구체적 변경 제안까지 포함한다.

## 이 스킬의 위치 (워크플로우)

```
피치 스킬 사용 → 문제 발견 →
  /peach-skill-feedback (이 스킬) → docs/스킬피드백/ 문서 생성 →
  다른 에이전트가 문서를 읽고 → skills/{대상스킬}/ 업데이트
```

---

## 0단계: 환경 감지

피치 하네스 원본 폴더를 자동 감지한다.

```bash
# OS별 자동 감지
if [ -d "D:/peachSolution2/peach-harness" ]; then
  HARNESS_ROOT="D:/peachSolution2/peach-harness"
elif [ -d "$HOME/source/peachSolution2/peach-harness" ]; then
  HARNESS_ROOT="$HOME/source/peachSolution2/peach-harness"
else
  echo "❌ 피치 하네스 폴더를 찾을 수 없습니다"
  echo "   Windows: D:\\peachSolution2\\peach-harness"
  echo "   macOS:   ~/source/peachSolution2/peach-harness"
  # 사용자에게 경로 확인
fi

FEEDBACK_DIR="$HARNESS_ROOT/docs/스킬피드백"
SKILLS_DIR="$HARNESS_ROOT/skills"

# 피드백 폴더 생성 (최초 1회)
mkdir -p "$FEEDBACK_DIR"
```

> **규칙**: 피드백 문서는 반드시 피치 하네스 **원본 폴더**에 저장한다.
> 플러그인 캐시(`~/.claude/plugins/cache/`)에 저장하면 npm 업데이트 시 삭제된다.

---

## 1단계: 대상 스킬 식별

### 자동 감지

현재 대화 맥락에서 사용된 피치 스킬을 파악한다:
- `/peach-e2e-browse` → 대상: `peach-e2e-browse`
- `/peach-gen-backend` → 대상: `peach-gen-backend`
- 복수 스킬이면 가장 문제가 많았던 스킬을 주 대상으로

### 수동 지정

사용자가 직접 지정하는 경우:
```
/peach-skill-feedback peach-e2e-browse
```

### 대상 스킬 문서 읽기

```bash
# SKILL.md 읽기
cat "$SKILLS_DIR/{대상스킬}/SKILL.md"

# references/ 목록 확인
ls "$SKILLS_DIR/{대상스킬}/references/" 2>/dev/null
```

---

## 2단계: 문제/해결 패턴 수집

현재 대화에서 아래 4가지를 추출한다:

### 2-1. 발견된 문제

| 수집 항목 | 예시 |
|----------|------|
| 시도했지만 실패한 것 | Flutter에서 eval click()이 안 먹힘 |
| 스킬 문서에 없던 상황 | accessibility 재활성화 필요 |
| 토큰 낭비가 발생한 지점 | screenshot + Read 3회 = 수천 토큰 |
| 예상과 다르게 동작한 것 | VPN 메뉴 클릭 → 다른 페이지로 튕김 |

### 2-2. 해결된 방법

| 수집 항목 | 예시 |
|----------|------|
| 성공한 우회 방법 | dart.js에서 API method 추출 → fetch 직접 호출 |
| 효율적이었던 패턴 | eval "body.innerText.substring(0,200)" |
| 새로 발견한 명령/기능 | highlight, record, find 명령 |

### 2-3. 기존 스킬과의 차이

대상 스킬의 SKILL.md + references/를 읽고, 현재 대화에서 발견된 것 중 **기존 문서에 없는 항목**을 식별한다.

### 2-4. 심각도 분류

| 심각도 | 기준 | 예시 |
|--------|------|------|
| **높음** | 스킬이 안내하는 방법으로는 작업 불가 | Flutter accessibility 활성화 방법 누락 |
| **중간** | 토큰 대량 낭비 또는 시행착오 유발 | screenshot + Read 대신 eval 사용 안내 부족 |
| **낮음** | 편의 기능 누락 | highlight, record 명령 미문서화 |

---

## 3단계: 기존 스킬 문서와 비교 분석

```bash
# SKILL.md에서 의사결정 트리 확인
grep -n "결정\|판단\|분기\|├─\|└─" "$SKILLS_DIR/{대상스킬}/SKILL.md"

# 핵심 규칙 확인
grep -n "규칙\|금지\|필수\|주의" "$SKILLS_DIR/{대상스킬}/SKILL.md"

# references/ 문서 목록
ls "$SKILLS_DIR/{대상스킬}/references/"
```

비교 결과를 아래 형태로 정리:

```
| # | 발견된 문제 | 현재 SKILL.md에 있는가 | 위치 (행 번호) |
|---|-----------|:---:|-----|
| 1 | Flutter accessibility 활성화 | X (없음) | — |
| 2 | eval click isTrusted 차이 | X (없음) | — |
| 3 | 세션 끊김 복구 | X (없음) | — |
```

---

## 4단계: 산출물 생성

### 파일명 규칙

미반영(처리 대기) 파일은 `TODO-` 접두어를 붙인다. 반영 완료 시 `TODO-`를 제거한다.

```
# 생성 시 (미반영)
docs/스킬피드백/TODO-YYYY-MM-DD-{스킬명}-피드백.md

# 반영 완료 후
docs/스킬피드백/YYYY-MM-DD-{스킬명}-피드백.md
```

예시:
```
# 대기 중
docs/스킬피드백/TODO-2026-04-15-peach-gen-backend-피드백.md

# 반영 완료
docs/스킬피드백/2026-04-12-peach-e2e-browse-피드백.md
```

> 폴더를 `ls`로 볼 때 `TODO-` 파일만 눈에 띄어 할 일을 즉시 파악할 수 있다.
> 대부분의 파일은 반영 완료(접두어 없음)이므로 폴더가 깔끔하게 유지된다.

### 문서 구조 (필수 섹션)

```markdown
---
status: pending            # pending → completed
target_skill: peach-{name}
severity: 높음 N / 중간 N / 낮음 N
completed_at:              # 반영 완료 시 날짜 기입
applied_by:                # 반영 완료 시 에이전트명 기입
---

# {스킬명} 피드백 — YYYY-MM-DD

> **대상 스킬**: peach-{name}
> **작성 근거**: [어떤 작업을 하다가 발견했는지 한 줄]
> **심각도 요약**: 높음 N건 / 중간 N건 / 낮음 N건

---

## 1. 발견된 문제

| # | 문제 | 심각도 | 현재 스킬에 있는가 | SKILL.md 행 |
|---|------|:---:|:---:|-----|

## 2. 해결 방법 / 우회 전략

(문제 번호별 대응. 실제 실행한 명령 + 결과 포함)

### 문제 #1: {제목}
**원인**: ...
**해결**: ...
```bash
# 실제 실행한 명령
```

## 3. 스킬 업데이트 제안

### 3-1. SKILL.md 변경
(구체적 행 범위 + 추가/수정할 내용을 마크다운으로 제시)

### 3-2. references/ 추가/수정
(새 레퍼런스 파일명 + 핵심 내용 요약)

### 3-3. agent-browser-명령어.md 등 기존 레퍼런스 보완
(추가할 명령어/패턴)

## 4. 검증 시나리오

(다른 AI 에이전트가 이 문서만으로 재현할 수 있는 단계별 명령)

### 시나리오 {번호}: {제목}
**목적**: ...
**전제**: ...
```bash
# 단계 1: ...
# 단계 2: ...
```
**기대 결과**: ...
**통과 기준**: ...

## 5. 다음 에이전트를 위한 작업 지시

이 문서를 읽은 AI 에이전트는 아래 순서로 작업한다:

1. 피치 하네스 원본 폴더 확인
   - Windows: `D:\peachSolution2\peach-harness\`
   - macOS: `~/source/peachSolution2/peach-harness/`

2. 대상 스킬 현재 상태 확인
   `cat skills/{대상스킬}/SKILL.md`

3. 이 문서의 "3. 스킬 업데이트 제안"을 순서대로 반영
   - SKILL.md 수정
   - references/ 파일 추가/수정

4. 검증 시나리오(4장) 실행하여 변경 사항 확인

5. 변경 완료 후:
   - frontmatter의 `status`를 `completed`로 변경, `completed_at`과 `applied_by` 기입
   - 파일명에서 `TODO-` 접두어 제거 (`git mv`로 rename)
   - 하단에 반영 기록 추가:
   ```markdown
   ## 반영 기록
   - [날짜] {에이전트}: SKILL.md 행 XX~YY 수정, references/XX.md 추가
   ```
```

---

## 5단계: 저장 및 안내

### 저장

```bash
# 피드백 문서 저장 (TODO- 접두어 포함)
FEEDBACK_FILE="$FEEDBACK_DIR/TODO-YYYY-MM-DD-{스킬명}-피드백.md"
# Write tool로 저장
```

### 사용자 안내

```
📄 피드백 문서 생성 완료

경로: docs/스킬피드백/YYYY-MM-DD-{스킬명}-피드백.md
문제: N건 (높음 X / 중간 Y / 낮음 Z)
검증 시나리오: N개

다음 에이전트가 이 문서를 읽고 스킬을 업데이트할 수 있습니다.
반영하려면: /peach-skill-feedback 문서를 참고하여 skills/{대상스킬}/ 수정
```

### ⛔ 이 스킬의 작업은 여기서 끝난다

문서를 저장하고 사용자에게 경로를 안내한 뒤 **더 이상 어떤 파일도 수정하지 않는다**.
스킬 반영(SKILL.md 수정, references/ 추가)은 이 문서를 읽은 다른 AI 에이전트가 수행한다.

---

## 핵심 규칙

1. **피치 하네스 원본 폴더에만 저장** — 캐시 폴더 금지
2. **파일명은 한글 + 날짜** — `YYYY-MM-DD-{스킬명}-피드백.md`
3. **실제 명령 포함** — 추상적 설명 금지, 실행 가능한 명령어로
4. **검증 시나리오 필수** — 다른 에이전트가 재현할 수 있어야 함
5. **다음 에이전트 작업 지시 필수** — 문서를 읽고 바로 작업 가능해야 함
6. **기존 문서 비교 필수** — SKILL.md 행 번호까지 명시
7. **스킬 파일 절대 수정 금지** — SKILL.md, references/, 기타 스킬 파일을 직접 Edit/Write 금지.
   문서(TODO-*.md)를 생성하고 사용자에게 보고하면 이 스킬의 작업은 완료된다.
   스킬 반영은 반드시 다른 세션의 에이전트가 피드백 문서를 읽고 수행한다.
8. **작업 종료 기준** — `docs/스킬피드백/TODO-*.md` 파일을 Write tool로 저장한 순간 작업 완료.
   그 이후 어떠한 파일도 수정하지 않는다.

---

## 사용 예시

```bash
# e2e-browse 스킬 사용 후 문제 발견
/peach-skill-feedback peach-e2e-browse

# gen-backend 스킬 피드백
/peach-skill-feedback peach-gen-backend

# 스킬명 생략 시 대화 맥락에서 자동 감지
/peach-skill-feedback
```
