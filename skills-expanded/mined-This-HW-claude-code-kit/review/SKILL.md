---
name: review
description: Run a full code review on current changes or specified files. Runs ruff lint, review-code agent, and security scan in sequence.
model: opus
effort: high
---

# 코드 리뷰 실행

**즉시 실행하세요. 설명하지 말고 바로 실행합니다.**

## 파이프라인 구조

```
┌──────────────┐   ┌──────────────┐   ┌───────────────┐
│ 리뷰 대상    │ → │ review-code  │ → │ security-scan │
│ 파악 (Main)  │   │ (opus)       │   │ (sonnet)      │
└──────────────┘   └──────────────┘   └───────────────┘
```

---

## 0단계: 정적 분석 (Python 파일 포함 시)

**리뷰 대상에 `.py` 파일이 포함되어 있으면 ruff check를 먼저 실행합니다.**

```bash
# 특정 파일 지정 시
ruff check [대상 파일 또는 디렉토리]

# git diff 대상 시 (변경된 .py 파일 추출 후)
git diff HEAD --name-only | grep '\.py$' | xargs ruff check 2>/dev/null
```

**결과 처리:**

- ruff check 출력이 있으면: 리뷰 컨텍스트에 포함하여 review-code 에이전트에 전달
- ruff check 통과 시: "정적 분석: 통과" 메시지만 출력
- ruff가 설치되지 않은 경우: "스킵됨 (ruff 미설치)" 메시지 출력

**형식:**

```
## 0단계: 정적 분석 (ruff)
- 대상: [파일 목록 또는 "없음 (Python 파일 없음)"]
- 결과: [통과 | N건 발견]
- 발견된 이슈: [있을 때만 출력]
```

---

## 0.5단계: 복잡도 flag — 하이브리드 (advisory 전용, Python 파일 포함 시)

**결정론 flag → LLM 판단** 2단 하이브리드입니다. 복잡도 수치는 **리젝 사유가 아니라
리뷰 초점 신호**입니다.

```bash
# mccabe 복잡도 flag (ruff 내장, 기본 임계 10)
ruff check --select C901 [0단계와 동일한 대상 파일]
```

**결과 처리:**

- flag된 함수가 있으면: 목록을 review-code 에이전트 컨텍스트에 다음 지시와 함께 전달 —
  > 아래 함수들은 복잡도 임계를 넘었다(결정론 flag). **줄수·복잡도 수치 자체를 리젝
  > 사유로 삼지 말고**, 다음 관점으로만 분리 타당성을 판단하라: ① 모듈/함수 경계가
  > 단일 책임인가 ② IN/OUT 계약(인자·반환·부수효과)이 명확히 분리 가능한가
  > ③ 분리 시 계약이 단순해지는가(아니면 그대로가 응집적인가). 응집적이면 flag를
  > 기각하고 그 근거를 명시하라.
- flag 없으면: "복잡도: 통과" 한 줄만.
- **절대 blocking 아님**: 이 단계는 어떤 경우에도 리뷰를 실패시키지 않는다
  (전역 lint(E,F)·stop-validator와 무관 — advisory 전용).
- ruff 미설치: "스킵됨 (ruff 미설치)" — fail-open.

**형식:**

```
## 0.5단계: 복잡도 flag (advisory)
- flag: [없음 | 함수 N건 (파일:라인, 복잡도)]
- 처리: [review-code 판단 위임 | 통과]
```

---

## 1단계: 리뷰 대상 파악

$ARGUMENTS가 있으면:

- 해당 파일/디렉토리를 읽어서 리뷰

$ARGUMENTS가 없으면:

- `git diff HEAD`로 변경사항 확인
- 변경사항이 없으면 `git diff HEAD~1`로 마지막 커밋 확인

---

## 1.5단계: 자동 범위 판단 (Auto-Scope)

**변경 파일을 분석하여 리뷰 범위를 자동으로 결정합니다.**

### 수동 오버라이드 확인

$ARGUMENTS에 `--quick`이 포함되어 있으면:

- scope = 'quick' (사용자 명시 오버라이드)
- security_scan_needed = false
- "수동으로 quick 모드가 지정되었습니다" 메시지 출력
- 1.5단계 나머지 스킵하고 2단계로 진행

### 자동 범위 판단

변경 파일 목록을 분석하여 scope를 자동 결정:

#### 보안 관련 파일 감지

다음 경로 패턴에 매칭되는 파일이 **1개라도 있으면**:

- `**/auth/**`, `**/security/**`, `**/payment/**`
- `**/middleware/**`, `**/*secret*`, `**/*token*`
- `hooks/*.py`, `**/config.py`

→ **scope = 'adversarial', security_scan_needed = true**

#### Trivial 파일 판정

다음 파일 유형이 **전체의 80% 이상**이면:

- `*.md`, `*.txt`, `docs/**`
- `*.json`, `*.yml`, `*.yaml` (예외: `settings.json`, `project.yaml`)

→ **scope = 'quick', security_scan_needed = false**

#### 기본 (일반 코드)

위 두 조건에 해당하지 않으면:

- `src/**`, `agents/**`, `skills/**`, `scripts/**`

→ **scope = 'adversarial', security_scan_needed = false**

### 판정 결과 출력

```
🔍 Auto-Scope 판정 결과:
- 변경 파일: [N]개
- 보안 관련: [N]개
- Trivial: [N]개
- **Scope: [adversarial | quick]**
- Security Scan: [필요 | 불필요]
```

---

## 1.7단계: 사용자 의견 처리 원칙 (조건부)

<!-- Pattern from: superpowers/receiving-code-review -->
**트리거**: $ARGUMENTS에 파일 경로·옵션(`--quick` 등)이 아닌 **자연어 문장이 포함된 경우**에만 실행.

예시:
- `/review src/auth.py 보안이 걱정돼` → **실행** (자연어 의견 포함)
- `/review src/auth.py` → 실행 안 함 (경로만)
- `/review --quick` → 실행 안 함 (옵션만)

### 처리 절차

```
1. Restate  — 의견을 기술적으로 재술 (오해 없게)
2. Verify   — Read/Grep 도구만으로 해당 코드를 직접 확인 (이 단계에서는 읽기 전용 — Bash 실행 없이)
3. Evaluate — 기술적 타당성 판단
4. Respond  — 동의 or 근거 있는 반박을 review-code 프롬프트에 반영
```

### 금지

- "맞습니다!" / "좋은 지적이에요!" (검증 없는 동의)
- Verify 없이 의견을 바로 리뷰 방향에 반영

### 처리 예시

```
의견: "이 함수는 성능 문제가 있을 것 같아"
Verify: [Read로 함수 확인 → 중첩 루프 발견]
Evaluate: 타당함 — O(n²) 확인됨
→ review-code 프롬프트에 포함: "사용자 지적 — 성능 이슈 가능성, 검증됨"

의견: "이 부분은 타입 체크가 없어"
Verify: [Grep으로 상위 검증 로직 확인 → strict mode 확인]
Evaluate: 상위에서 처리됨 — 중복 불필요
→ review-code 프롬프트에 반영 안 함. 사용자에게 이유 명시.
```

---

## 2단계: 코드 리뷰 실행

> **`review-code`에는 Bash가 없다** (`tools: Read/Glob/Grep`, `disallowedTools`에 Bash).
> 따라서 프롬프트에 "`git diff`로 확인하라"고 **위임하면 안 된다** — 에이전트가 실행하지
> 못하고 빈 리뷰를 반환한다(2026-08-23 실측). 1단계에서 **main이 diff를 뽑아 프롬프트에
> 인라인으로 붙이거나**, diff가 크면 **읽을 파일 경로 목록**을 명시해서 넘겨라.
> (`security-scan`은 Bash가 있으므로 이 제약이 없다 — 두 에이전트를 같은 방식으로
> 호출하지 말 것.)
>
> 또한 **에이전트의 마지막 메시지가 곧 반환값**이다. "리포트 형식 그대로, 서두 없이,
> 마지막 메시지로 출력하라"를 프롬프트에 명시하지 않으면 진행 상황 서술이 반환될 수 있다.


```
Task tool 사용:
subagent_type: review-code
model: opus
prompt: |
  다음 코드를 리뷰해주세요:
  [1단계에서 확인한 코드/diff]

  **정적 분석 결과 (0단계):**
  [0단계 ruff check 결과 - 있으면 포함, 없으면 "정적 분석 통과" 또는 "Python 파일 없음"]

  **Auto-Scope 설정:**
  - scope: [1.5단계에서 결정된 scope]
  - security_scan_needed: [1.5단계 결과]

  scope가 'quick'이면:
  - CRITICAL, HIGH 등급만 스캔
  - MEDIUM, LOW는 필터링
  - 예상 시간: 1-2분

  scope가 'adversarial'이면:
  - 4개 페르소나 전체 공격
  - 모든 등급 보고
  - 예상 시간: 3-5분

  리뷰 형식:
  ## 전체 평가: [A/B/C/D/F]
  ## Scope Used: [adversarial | quick]

  ## Critical (즉시 수정 필요)
  ## Warning (권장 수정)
  ## Suggestion (개선 제안)

  ## 권장 조치
```

---

## 3단계: 보안 검토 (조건부)

**1.5단계에서 security_scan_needed = true인 경우에만 실행**

코드에 보안 관련 파일이 포함되면 security-scan을 실행:

```
Task tool 사용:
subagent_type: security-scan
model: sonnet
prompt: |
  다음 코드의 보안 취약점을 검사해주세요:
  [대상 코드]

  검사 항목:
  - OWASP Top 10 취약점
  - 인증/인가 로직
  - 입력 검증
  - SQL 인젝션
  - XSS
```

**security_scan_needed = false인 경우**:

- 이 단계를 스킵하고 4단계로 진행

---

## 4단계: 결과 요약

리뷰 결과를 사용자에게 요약 보고

### 리뷰 결과

| 항목       | 결과        |
| ---------- | ----------- |
| 전체 평가  | [A/B/C/D/F] |
| Critical   | [N개]       |
| Warning    | [N개]       |
| Suggestion | [N개]       |
| 보안 이슈  | [N개]       |

### 수정 필요 사항

[Critical/Warning 항목 목록]
