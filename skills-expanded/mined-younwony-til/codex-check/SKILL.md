---
name: codex-check
description: Codex CLI 크로스 체크 표준 워크플로우 스킬. codex-reviewer 에이전트가 사용한다. Bash CLI(codex exec, codex review) 호출을 표준화한다. work-plan/self-review/review-pr/team-review 등이 이 스킬로 위임하여 일관된 호출 정책(timeout 240s, CODEX_FAIL 처리, 재시도, 로그 보존)을 적용한다. "codex 호출", "Codex 크로스 체크", "AI 검증" 같은 작업 또는 다른 스킬의 위임 호출로 트리거된다.
---

# Codex Check — Codex CLI 호출 표준

외부 AI 크로스 체크 시 Codex CLI를 호출하는 표준 워크플로우.

## 핵심 정책

| 항목 | 규칙 |
|------|------|
| 사용 가능 | `codex exec -`, `codex review --base ...`, `codex "..." --model ...` (모두 Bash 도구) |
| Bash timeout | **`timeout: 240000ms` (4분) 필수 명시** |
| 실패 처리 | `2>&1 \|\| echo "CODEX_FAIL"` 패턴 |

## 언제 사용하는가

- 다른 스킬(work-plan, self-review, review-pr, team-review 등)에서 Codex 검증이 필요할 때
- 사용자가 명시적으로 "Codex로 크로스 체크" 요청

## 위임 호출 패턴 (호출자가 따라야 할 패턴)

```
Agent(
  subagent_type="general-purpose",
  description="Codex 크로스 체크",
  prompt=(
    "당신은 codex-reviewer 에이전트다. ~/.claude/agents/codex-reviewer.md를 먼저 읽어라.\n\n"
    "다음 입력으로 codex-check 스킬을 실행하라:\n"
    "mode: exec  (또는 review)\n"
    "purpose: work-plan-cross-check\n"
    "log_dir: {Track의 _workspace/ai-cross-check/codex/}\n\n"
    "prompt_text:\n---\n"
    "{프롬프트 본문}\n"
    "---\n\n"
    "결과 JSON을 마지막 메시지로 반환하라."
  ),
  model="opus"
)
```

호출자는 반환 JSON을 파싱하여 `status` 확인 후 `response` 사용.

## 표준 호출 절차 (codex-reviewer 에이전트가 수행)

### Step 1: 환경 검증

```bash
command -v codex >/dev/null 2>&1 && echo "CODEX_OK" || echo "CODEX_NOT_INSTALLED"
```

미설치 시 즉시 fail 반환.

### Step 2: 로그 준비

```bash
LOG_DIR="${log_dir:-_workspace/ai-cross-check/codex}"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
PROMPT_FILE="$LOG_DIR/${purpose}-${TIMESTAMP}-prompt.txt"
RESPONSE_FILE="$LOG_DIR/${purpose}-${TIMESTAMP}-response.txt"
```

### Step 3: 호출 모드 분기

**Mode A — exec (일반 프롬프트, 권장):**

ai-harness-monitor의 `ask-codex.sh` wrapper를 통해 호출. wrapper가 dashboard용 로그(`~/.claude/skills/ai-harness-monitor/log/$TEAM/codex-{TS}.log`)와 symlink(`latest-codex.log`)를 자동 생성하므로, `dashboard.sh codex` 패널에 호출 카드가 라이브로 표시된다.

Bash 도구 호출, `timeout: 240000ms`:
```bash
printf '%s' "$PROMPT_TEXT" > "$PROMPT_FILE"
~/.claude/skills/ai-harness-monitor/scripts/ask-codex.sh "$(cat "$PROMPT_FILE")" \
  2>&1 | tee "$RESPONSE_FILE" || echo "CODEX_FAIL" >> "$RESPONSE_FILE"
```

**Mode B — review (브랜치/PR 리뷰, dashboard 미표시):**

`ask-codex.sh`는 `codex review --base`를 지원하지 않으므로 직접 CLI 호출. 이 경우 dashboard에 카드가 뜨지 않는다. 가능하면 Mode A 패턴(diff를 프롬프트에 embed)으로 호출해서 dashboard에 띄우는 것을 권장한다.

```bash
codex review --base "$BASE_BRANCH" 2>&1 | tee "$RESPONSE_FILE" || echo "CODEX_FAIL" >> "$RESPONSE_FILE"
```

**Mode C — 모델 명시 (dashboard 미표시):**

wrapper가 `--model` 옵션을 노출하지 않으므로 직접 CLI 호출.

```bash
cat "$PROMPT_FILE" | codex --model "$MODEL" exec - 2>&1 | tee "$RESPONSE_FILE" || echo "CODEX_FAIL" >> "$RESPONSE_FILE"
```

**주의:**
- `ask-codex.sh`는 내부적으로 `codex exec --skip-git-repo-check "$PROMPT"` (argv 방식)로 호출. 큰 프롬프트는 ARG_MAX(~2MB) 제한 있음. /self-review의 1000줄 diff 가드(~50KB) 안에서는 안전.
- wrapper는 기본 모드(reviewer role + trust boundary 자동 적용). skill이 보내는 프롬프트는 self-contained이므로 충돌 없음 (20260511-153737 세션 검증).
- **금지**: 메인 세션에서 `codex exec -` 직접 호출 — dashboard 카드 안 뜸. Mode A 사용.

### Step 4: 결과 분류

| 신호 | reason | 재시도 |
|------|--------|--------|
| 정상 응답 | - | - |
| `CODEX_FAIL` 검출 + ECONNRESET | `network` | 5초 후 1회 |
| `CODEX_FAIL` 검출 + 429 | `rate_limit` | 30초 후 1회 |
| `CODEX_FAIL` 검출 + 5xx | `model_error` | 1회 |
| Bash timeout (4분 초과) | `timeout` | **X** (즉시 fail) |
| `CODEX_FAIL` + 401/403 | `auth` | X |
| `CODEX_FAIL` + 400 / schema | `input_error` | X |
| 빈 응답 | `empty_response` | X |
| `CODEX_NOT_INSTALLED` | `not_installed` | X |

### Step 5: JSON 반환

```json
{
  "status": "ok",
  "response": "<codex 응답 전문>",
  "log_path": "<RESPONSE_FILE 경로>",
  "duration_seconds": 120
}
```

또는

```json
{
  "status": "fail",
  "reason": "timeout",
  "log_path": "<RESPONSE_FILE 경로>"
}
```

## 호출자 권장 처리

```
result_json = call codex-check
if result_json.status == "ok":
    use result_json.response
else:
    log result_json.reason
    proceed without Codex cross-check (Claude 단독)
    optional: 결과 보고서에 "Codex cross-check skipped: {reason}" 명시
```

## Plugin 분기가 호출자에 남아 있어도

`self-review.md`, `review-pr.md`, `team-review.md`, `work-plan.md`, `work-plan/SKILL.md`에 "Plugin 우선, CLI fallback" 패턴이 남아 있더라도, 이 스킬은 **Plugin 분기를 무시하고 CLI fallback 단계로 직행**한다 (CLAUDE.md 정책).

## 로그 관리

- 자동 삭제 X. 사용자/정리 스킬 책임.
- 추천 위치:
  - Track 컨텍스트: `.claude/tracks/{track_id}/_workspace/ai-cross-check/codex/`
  - 비Track: `_workspace/ai-cross-check/codex/`

## 테스트 시나리오

### 정상 (exec)
- 입력: 짧은 코드 리뷰 프롬프트, mode=exec
- 기대: status=ok, response 비어있지 않음

### 정상 (review)
- 입력: mode=review, base_branch=main
- 기대: status=ok, git diff 기반 리뷰 응답

### 환경 폴백
- 입력: codex 미설치
- 기대: status=fail, reason=not_installed

### Timeout
- 입력: 매우 큰 프롬프트
- 기대: 4분 후 자동 종료, status=fail, reason=timeout

## 완료 체크리스트

- [ ] 환경 검증
- [ ] 로그 파일 2개 저장
- [ ] Bash timeout 240000ms 명시
- [ ] Plugin Skill(`/codex:*`) 호출 0건
- [ ] 결과 JSON 반환
