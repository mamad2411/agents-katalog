---
name: gemini-check
description: Gemini CLI 크로스 체크 표준 워크플로우 스킬. gemini-reviewer 에이전트가 사용한다. work-plan/self-review/review-pr/team-review 등 외부 AI 검증이 필요한 모든 스킬은 이 스킬로 위임하여 Gemini CLI 호출을 표준화한다. timeout 240s, 환경 검증, 에러 분류, 재시도 정책, 호출 로그 보존을 일관 적용한다. "gemini 호출", "Gemini 크로스 체크", "AI 검증" 같은 작업 또는 다른 스킬의 위임 호출로 트리거된다.
---

# Gemini Check — Gemini CLI 호출 표준

외부 AI 크로스 체크 시 Gemini CLI를 호출하는 표준 워크플로우. 정책을 한 곳에 집중하여 호출자 스킬의 코드 중복을 제거한다.

## 언제 사용하는가

- 다른 스킬(work-plan, self-review, review-pr, team-review 등)에서 Gemini 검증이 필요할 때
- 사용자가 명시적으로 "Gemini로 크로스 체크" 요청
- 단독 호출은 거의 없음. 주로 위임 호출.

## 위임 호출 패턴 (호출자가 따라야 할 패턴)

호출자 스킬은 직접 `gemini -p` Bash 호출을 작성하지 않고, 다음 패턴으로 위임한다:

```
Agent(
  subagent_type="general-purpose",
  description="Gemini 크로스 체크",
  prompt=(
    "당신은 gemini-reviewer 에이전트다. ~/.claude/agents/gemini-reviewer.md를 먼저 읽어라.\n\n"
    "다음 입력으로 gemini-check 스킬을 실행하라:\n"
    "purpose: work-plan-cross-check\n"
    "log_dir: {Track의 _workspace/ai-cross-check/gemini/}\n\n"
    "prompt_text:\n---\n"
    "{...프롬프트 텍스트 전문...}\n"
    "---\n\n"
    "결과 JSON을 마지막 메시지로 반환하라."
  ),
  model="opus"
)
```

호출자는 반환 JSON을 파싱하여 `status` 확인 후 `response` 사용.

## 표준 호출 절차 (gemini-reviewer 에이전트가 수행)

### Step 1: 환경 검증

```bash
command -v gemini >/dev/null 2>&1 && echo "GEMINI_OK" || echo "GEMINI_NOT_INSTALLED"
```

미설치 시 즉시 fail 반환:
```json
{"status": "fail", "reason": "not_installed"}
```

### Step 2: 로그 디렉토리 준비

```bash
LOG_DIR="${log_dir:-_workspace/ai-cross-check/gemini}"
mkdir -p "$LOG_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
PROMPT_FILE="$LOG_DIR/${purpose}-${TIMESTAMP}-prompt.txt"
RESPONSE_FILE="$LOG_DIR/${purpose}-${TIMESTAMP}-response.txt"
STDERR_FILE="$LOG_DIR/${purpose}-${TIMESTAMP}-stderr.txt"
```

### Step 3: 호출 실행 (Bash, timeout 240000ms 필수)

**ai-harness-monitor의 `ask-gemini.sh` wrapper를 통해 호출**한다. wrapper가 dashboard용 로그(`~/.claude/skills/ai-harness-monitor/log/$TEAM/gemini-{TS}.log`)와 symlink(`latest-gemini.log`)를 자동 생성하므로, `dashboard.sh gemini` 패널에 호출 카드가 라이브로 표시된다.

화면에 **요청 + 응답 페어**를 함께 표시하고, stdout(응답)과 stderr(Warning/info)를 별도 파일로 분리한다.

```bash
# 프롬프트 저장
printf '%s' "$PROMPT_TEXT" > "$PROMPT_FILE"

# 화면에 요청 페어 표시
echo "[gemini-check] purpose=${purpose} timestamp=${TIMESTAMP}"
echo "[gemini-check] >>> 요청"
cat "$PROMPT_FILE"
echo ""
echo "[gemini-check] <<< 응답"

# ask-gemini.sh wrapper 호출 — dashboard 카드 자동 생성
# stdout(응답)은 RESPONSE_FILE + 화면(tee), stderr(Warning/info)는 STDERR_FILE로 격리
START=$(date +%s)
~/.claude/skills/ai-harness-monitor/scripts/ask-gemini.sh "$(cat "$PROMPT_FILE")" \
  2> "$STDERR_FILE" | tee "$RESPONSE_FILE"
EXIT_CODE=${PIPESTATUS[0]}
END=$(date +%s)
DURATION=$((END - START))

echo ""
echo "[gemini-check] duration=${DURATION}s exit_code=${EXIT_CODE}"

if [ $EXIT_CODE -ne 0 ]; then
  echo "GEMINI_FAIL" >> "$RESPONSE_FILE"
fi
```

**주의:**
- Bash 도구 `timeout: 240000ms` 인자 명시는 필수.
- `ask-gemini.sh`는 내부적으로 `gemini -p "$PROMPT"` (argv 방식)로 호출하므로 큰 프롬프트는 ARG_MAX(보통 ~2MB) 제한이 있다. /self-review의 1000줄 diff 가드(~50KB) 안에서는 안전.
- wrapper는 기본 모드(researcher role + trust boundary 자동 적용)로 호출한다. skill이 보내는 프롬프트는 이미 self-contained이므로 충돌 없음 (20260511-153737 세션 검증).
- **금지**: `gemini -p ...` / `cat | gemini` 직접 호출 — dashboard 카드 안 뜸.

### Step 4: 결과 분류

| 신호 | reason | 재시도 |
|------|--------|--------|
| 정상 응답 + 비어있지 않음 | - | - |
| Bash timeout (4분 초과) | `timeout` | X |
| stderr "ECONNRESET / network" | `network` | 5초 후 1회 재시도 |
| HTTP 429 / rate limit | `rate_limit` | 30초 후 1회 재시도 |
| HTTP 5xx | `model_error` | 1회 재시도 |
| HTTP 401/403 | `auth` | X (사용자 안내) |
| HTTP 400 / schema | `input_error` | X (프롬프트 축소 후 호출자가 재호출) |
| 빈 응답 | `empty_response` | X |
| GEMINI_NOT_INSTALLED | `not_installed` | X |

### Step 5: 결과 JSON 반환

```json
{
  "status": "ok",
  "response": "<gemini 응답 전문>",
  "log_path": "<RESPONSE_FILE 경로>",
  "duration_seconds": 45
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
result_json = call gemini-check
if result_json.status == "ok":
    use result_json.response
else:
    log result_json.reason
    proceed without Gemini cross-check (Claude 단독)
    optional: 결과 보고서에 "Gemini cross-check skipped: {reason}" 명시
```

## 비호출 케이스

다음 상황에서는 gemini-check를 호출하지 않는다 (불필요한 비용):
- 단순 정보 조회 (파일 읽기, grep 등)
- 사용자가 명시적으로 "AI 크로스 체크 없이"를 요청
- 직전 5분 이내 동일 프롬프트로 호출한 적 있음 (캐시 활용 — 호출자 책임)

## 로그 관리

- 로그는 자동 삭제하지 않음. 사용자 또는 별도 정리 스킬이 담당.
- 추천 위치:
  - Track 컨텍스트: `.claude/tracks/{track_id}/_workspace/ai-cross-check/gemini/`
  - 비Track 컨텍스트: `_workspace/ai-cross-check/gemini/` (cwd 기준)
- 로그 파일명: `{purpose}-{timestamp}-{prompt|response|stderr}.txt` (3종)
  - `prompt`: 입력 본문
  - `response`: Gemini stdout (응답 본문만)
  - `stderr`: Gemini stderr (Warning/info — 디버깅 및 에러 분류용)

## 테스트 시나리오

### 정상
- 입력: 짧은 코드 리뷰 프롬프트
- 기대: status=ok, response 본문 비어있지 않음, log 파일 2개 생성

### 환경 폴백
- 입력: gemini 미설치 환경
- 기대: status=fail, reason=not_installed, 호출자가 Claude 단독 진행

### Timeout
- 입력: 매우 큰 프롬프트
- 기대: 4분 후 자동 종료, status=fail, reason=timeout, 호출자가 Claude 단독 진행

## 완료 체크리스트

- [ ] 환경 검증 수행
- [ ] 로그 파일 2개(prompt, response) 저장
- [ ] Bash timeout 240000ms 명시
- [ ] 결과 JSON 반환 (status 필드 필수)
