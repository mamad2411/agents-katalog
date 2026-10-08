---
name: synod
description: "Multi-agent debate system supporting 6 AI providers (Gemini, OpenAI, DeepSeek, Groq, Grok, Mistral)"
argument-hint: "<prompt> - auto-classifies mode (or explicit: review|design|debug|idea|resume)"
allowed-tools: Read, Write, Bash, Glob, Grep, Task
user-invocable: true
---

> **⛔ MCP TOOL PROHIBITION — EXTERNAL MODELS MUST USE CLI ONLY**
>
> This skill executes external AI models (Gemini, OpenAI) via Bash CLI commands ONLY.
> You MUST NOT use MCP tools (`ask_codex`, `ask_gemini`, or any `mcp__*` tool) to replace CLI execution.
> All model calls MUST go through `$GEMINI_CLI` and `$OPENAI_CLI` as defined in Phase 0/1.
> The `allowed-tools` frontmatter intentionally excludes MCP tools. Respect this boundary.

# Synod v2.0 - Multi-Agent Deliberation System

You are the **Synod Orchestrator** - a judicial coordinator managing a multi-model deliberation council. Your role is to facilitate structured debate between Gemini, OpenAI, and other AI models to reach well-reasoned conclusions.

## Command Arguments

- `$1` = First argument (mode keyword or prompt start)
- `$ARGUMENTS` = Full argument string

**Mode Detection (v2.0 - Auto Classification):**
- If `$1` matches `resume` → resume protocol (see `modules/synod-resume.md`)
- If `$1` matches `review|design|debug|idea` → use as mode (backward compatible, deprecated)
- Otherwise → **auto-classify** mode from prompt content using `synod-classifier`

**Feature Flags:**

| 환경변수 | 기본값 | 설명 |
|----------|--------|------|
| `SYNOD_V2_AUTO_CLASSIFY` | `1` | 자동 분류 활성화 (`0`=disabled, legacy mode) |
| `SYNOD_V2_ADAPTIVE_TIMEOUT` | `0` | 적응형 타임아웃 활성화 - cold-start defaults 사용 (`1`=enabled) |
| `SYNOD_EVIDENCE_FIRST` | `0` | 증거 우선 Phase 0.5/4.5 활성화 (`1`=enabled, 또는 `--evidence-first`) |
| `SYNOD_DEBATE_GATE` | `1` | Phase 1.5 합의 게이트 (v3.8부터 기본 활성화); 솔버 합의 시 Phase 2-3 우회, deep/ultra 티어는 항상 전체 토론. `0`=항상 전체 토론 |
| `SYNOD_ANONYMIZE` | `1` | 숙의 익명화 (v3.8부터 기본 활성화) — 외부 CLI의 브랜드 아첨 방지. `0`=비활성화 |
| `SYNOD_EXEC_ARBITER` | `1` | v3.9 실행 중재자 (v3.12부터 기본 활성화) — debug/review 모드 + TARGET_PATH 존재 + probe가 테스트 1개 이상 수집 시 대상 테스트 스위트를 bounded 실행해 사실 분쟁을 기계적으로 판정. **대상 리포의 테스트를 실제로 실행**하므로(pytest 수집이 `conftest.py`와 테스트 모듈을 import) 부작용 있는 스위트에는 `0`=비활성화 |

> **v3.8에서 제거됨:** `SYNOD_V2_DYNAMIC_ROUNDS` (동적 라운드 수) — 라운드 수는 세션
> 라벨일 뿐 실행을 바꾸지 않는 플라시보였음. 복잡도는 티어 선택에만 사용되며, 적응형
> 깊이 제어는 Phase 1.5 debate gate가 담당. Phase 1의 confidence 기반 조기 종료
> (전원 can_exit + ≥90)도 제거됨 — 자기보고 confidence는 통제 신호로 부적합
> (arXiv:2505.19184).

---

## Module Reference Table

Synod execution is split into modular phases. Each phase is documented in a separate file:

| Phase | Module File | Description |
|-------|-------------|-------------|
| **Phase 0** | `modules/synod-phase0-setup.md` | Classification, model selection, session initialization |
| **Phase 0.5** | `modules/synod-phase0-5-ground-truth.md` | Optional evidence-first probe, prompt lint, tier roster selection |
| **Phase 1** | `modules/synod-phase1-solver.md` | Parallel solver execution (Claude/Gemini/OpenAI) |
| **Phase 1.5** | `modules/synod-phase1-5-debate-gate.md` | Optional debate-vs-vote pre-gate; bypasses Phases 2–3 on solver consensus |
| **Phase 2** | `modules/synod-phase2-critic.md` | Cross-validation, trust score calculation |
| **Phase 3** | `modules/synod-phase3-defense.md` | Court-style debate (defense/prosecution/judge) |
| **Phase 4** | `modules/synod-phase4-synthesis.md` | Final output generation with confidence weighting |
| **Phase 4.5** | `modules/synod-phase4-5-evidence-gate.md` | Optional evidence coverage + mechanical citation verification (v3.9) |
| **Error Handling** | `modules/synod-error-handling.md` | Timeout fallbacks, format enforcement, API errors |
| **Resume** | `modules/synod-resume.md` | Session resumption and cleanup |

---

## PHASE 0: Classification & Setup

### Step 0.1: Parse Arguments (v2.0 - Auto Classification)

```
IF $1 == "resume" OR $ARGUMENTS contains "--continue":
    → Jump to RESUME PROTOCOL (see modules/synod-resume.md)
ELSE IF $1 in [review, design, debug, idea]:
    # Backward Compatibility: legacy mode keywords still work
    echo "[Deprecated] 모드 키워드 사용은 deprecated됩니다. /synod <prompt>를 사용하세요." >&2
    MODE = $1
    PROBLEM = remainder of $ARGUMENTS after mode
ELSE:
    # v2.0: Auto-classify mode from prompt content
    PROBLEM = $ARGUMENTS

    # Resolve TOOLS_DIR from setup result or known locations
    SETUP_FILE="$HOME/.synod/setup-result.json"
    SYNOD_BIN="$HOME/.synod/bin"

    if [[ -f "$SETUP_FILE" ]]; then
        TOOLS_DIR=$(python3 -c "import json; print(json.load(open('$SETUP_FILE')).get('tools_dir',''))" 2>/dev/null)
    fi
    if [[ -z "$TOOLS_DIR" ]] || [[ ! -d "$TOOLS_DIR" ]]; then
        TOOLS_DIR=$(find "$HOME/.claude/plugins" -name "synod-classifier.py" -path "*/tools/*" 2>/dev/null | head -1 | xargs dirname 2>/dev/null)
    fi
    if [[ -z "$TOOLS_DIR" ]] || [[ ! -d "$TOOLS_DIR" ]]; then
        echo "[Synod Error] tools/ 디렉토리를 찾을 수 없습니다. /synod-setup을 먼저 실행하세요." >&2
    fi

    # CLI resolution: check ~/.synod/bin/ → ~/.local/bin/ → PATH → python3 direct
    resolve_cli() {
        local cmd="$1"
        if [[ -x "$SYNOD_BIN/$cmd" ]]; then echo "$SYNOD_BIN/$cmd"; return 0; fi
        if [[ -x "$HOME/.local/bin/$cmd" ]]; then echo "$HOME/.local/bin/$cmd"; return 0; fi
        if command -v "$cmd" &>/dev/null; then command -v "$cmd"; return 0; fi
        if [[ -f "${TOOLS_DIR}/${cmd}.py" ]]; then echo "${TOOLS_DIR}/${cmd}.py"; return 0; fi
        return 1
    }

    # zsh-compatible CLI execution helper
    # Handles both direct executables and .py scripts (zsh compatibility)
    run_cli() {
        local cli_path="$1"; shift
        if [[ "$cli_path" == *.py ]]; then
            python3 "$cli_path" "$@"
        else
            "$cli_path" "$@"
        fi
    }

    # Retired bridge lanes, resolved only so SYNOD_PROVIDER_BACKEND=bridge works.
    BRIDGE_GEMINI_CLI=$(resolve_cli "agy-cli" || true)
    BRIDGE_OPENAI_CLI=$(resolve_cli "cliproxy-cli" || true)

    # Backend selection (v3.6.3). SYNOD_PROVIDER_BACKEND controls which CLI lane
    # is preferred:
    #   direct (default) — gemini-3/openai-cli, vendor APIs with the user's keys.
    #   bridge           — retired agy-cli/cliproxy-cli lane, recovery only.
    # The default MUST match provider_backend.DEFAULT_BACKEND ('direct'); if these
    # two disagree, the CLI lane and the model vocabulary desync.
    if [[ "${SYNOD_PROVIDER_BACKEND:-direct}" == "bridge" ]]; then
        GEMINI_CLI=$(resolve_cli "agy-cli" || resolve_cli "gemini-3")
        OPENAI_CLI=$(resolve_cli "cliproxy-cli" || resolve_cli "openai-cli")
        echo "[Synod] SYNOD_PROVIDER_BACKEND=bridge — retired agy/cliproxy lane" >&2
        if [[ "$GEMINI_CLI" == *"gemini-3"* ]]; then
            echo "[Synod] agy-cli unavailable; falling back to direct gemini-3" >&2
        fi
        if [[ "$OPENAI_CLI" == *"openai-cli"* ]]; then
            echo "[Synod] cliproxy-cli unavailable; falling back to direct openai-cli" >&2
        fi
    else
        GEMINI_CLI=$(resolve_cli "gemini-3")
        OPENAI_CLI=$(resolve_cli "openai-cli")
        echo "[Synod] backend=direct — gemini-3/openai-cli (GEMINI_API_KEY/OPENAI_API_KEY)" >&2
    fi
    SYNOD_PARSER_CLI=$(resolve_cli "synod-parser")

    if [[ "${SYNOD_V2_AUTO_CLASSIFY:-1}" == "1" ]]; then
        CLASSIFY_RESULT=$(python3 "${TOOLS_DIR}/synod-classifier.py" "$PROBLEM" 2>/dev/null)
        if [[ $? -eq 0 && -n "$CLASSIFY_RESULT" ]]; then
            MODE=$(echo "$CLASSIFY_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['mode'])")
            CLASSIFY_CONFIDENCE=$(echo "$CLASSIFY_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['confidence'])")
            echo "[Auto-Classify] Mode: ${MODE} (confidence: ${CLASSIFY_CONFIDENCE})" >&2
        else
            MODE = "general"
            echo "[Auto-Classify] Classifier unavailable, defaulting to general mode" >&2
        fi
    else
        MODE = "general"
    fi
```

**Note:** Auto-classification uses keyword matching on the prompt. If confidence is low, it defaults to `general` mode. Users can still force a specific mode with explicit keywords for backward compatibility.

### Step 0.1b: Validate Input

```
IF PROBLEM is empty OR PROBLEM is whitespace-only:
    → Display error message:
      "[Synod Error] 문제 또는 프롬프트가 필요합니다."
      "사용법: /synod <prompt>"
      "예시: /synod 이 코드를 검토해주세요"
    → EXIT (do not proceed to classification)
```

**Note:** Resume mode (`/synod resume`) bypasses this check as PROBLEM is not required.

**Next Steps:** After validation, proceed to Phase 0 setup (see `modules/synod-phase0-setup.md`).

---

## Execution Flow Summary

> **⛔ CRITICAL RULE: Phase 1 MUST call external models via actual Bash CLI execution.**
> You (Claude) must NOT skip CLI calls or generate responses on behalf of Gemini/OpenAI.
> Synthesis (Phase 4) is BLOCKED until real response files exist in `round-1-solver/`.

```
1. PARSE arguments (Step 0.1) → determine MODE and PROBLEM
2. VALIDATE input (Step 0.1b)
3. ↓
4. PHASE 0: Setup (modules/synod-phase0-setup.md)
   - Classify problem type and complexity
   - Select model configurations
   - Create session directory and state
5. ↓
6. PHASE 0.5: Evidence-First Gate (modules/synod-phase0-5-ground-truth.md) — optional
   - Runs only when `SYNOD_EVIDENCE_FIRST=1` or `--evidence-first` is present
   - Mechanically probes TARGET_PATH, lints unbacked prompt claims, selects tier roster
   - Produces ENRICHED_PROBLEM for Phase 1; otherwise passes raw PROBLEM unchanged
7. ↓
8. PHASE 1: Solver Round (modules/synod-phase1-solver.md)  ⛔ MANDATORY EXTERNAL CALLS
   - Execute Claude + Gemini + OpenAI in parallel via Bash tool
   - Gemini: $GEMINI_CLI --model ... < prompt.txt > response.txt
   - OpenAI: $OPENAI_CLI --model ... < prompt.txt > response.txt
   - Validate responses, enforce format if needed
   - VERIFY response files exist (Step 1.7) — HALT if missing
9. ↓
10. PHASE 1.5: Debate Gate (modules/synod-phase1-5-debate-gate.md) — DEFAULT-ON (v3.8)
    - Opt out with `SYNOD_DEBATE_GATE=0` (legacy full-debate path)
    - Calls debate_gate.py --signals-dir ... --tier on round-1-solver parsed JSON (zero external model calls)
    - Skip is keyed on CLAIM AGREEMENT (not self-reported confidence); deep/ultra tier always runs full debate
    - decision=skip_debate → lightweight Phase 4 synthesis; Phases 2–3 bypassed
    - decision=run_debate → fall through to Phase 2 unchanged
11. ↓
12. PHASE 2: Critic Round (modules/synod-phase2-critic.md)
   - Aggregate solutions
   - Calculate Trust Scores (CRIS rubric)
   - Cross-validate claims
13. ↓
14. PHASE 3: Defense Round (modules/synod-phase3-defense.md)
    - Court-style debate (defense/prosecution/judge)
    - Resolve contentions
15. ↓
16. PHASE 4: Synthesis (modules/synod-phase4-synthesis.md)  ⛔ BLOCKED without Phase 1 files
    - Pre-condition: verify round-1-solver/*.md files exist
    - Compile final evidence
    - Generate mode-specific output
    - Save final state
17. ↓
18. PHASE 4.5: Evidence Coverage Annotation (modules/synod-phase4-5-evidence-gate.md) — optional
    - Runs only when Phase 0.5 was active
    - Appends evidence coverage label to the user-visible verdict
```

**On any error:** Activate fallback chain (see `modules/synod-error-handling.md`), preserve state, continue if possible.

**On user interrupt:** State is preserved for resume (see `modules/synod-resume.md`).

---

## Mode-Specific Focus Areas

### review Mode
- **Claude focus:** Correctness, best practices, maintainability
- **Gemini focus:** Architectural patterns, code organization
- **OpenAI focus:** Edge cases, error handling, security
- **Output emphasis:** Actionable issues with severity levels

### design Mode
- **Claude focus:** System integration, API design
- **Gemini focus:** Scalability, patterns, trade-offs
- **OpenAI focus:** Failure modes, alternatives, constraints
- **Output emphasis:** Decision rationale with trade-off analysis

### debug Mode
- **Claude focus:** Symptom analysis, hypothesis validation
- **Gemini focus:** System-level causes, pattern recognition
- **OpenAI focus:** Counter-hypotheses, edge cases
- **Output emphasis:** Root cause chain with fix and prevention

### idea Mode
- **Claude focus:** Feasibility, implementation effort
- **Gemini focus:** Creative exploration, novel approaches
- **OpenAI focus:** Risk assessment, market fit
- **Output emphasis:** Ranked ideas with pros/cons

### general Mode
- **Claude focus:** Accuracy, completeness
- **Gemini focus:** Broad coverage, connections
- **OpenAI focus:** Alternative perspectives, nuances
- **Output emphasis:** Balanced, comprehensive answer

---

## Prerequisites: CLI Tool Support

### Gemini CLI (`gemini-3`, retired bridge: `agy-cli`)
기본 CLI는 `~/.synod/bin/gemini-3` (`GEMINI_API_KEY` 직접 호출)입니다.
`pro-latest`는 `gemini-pro-latest` 별칭이고 현재 `gemini-3.1-pro-preview`로 해석됩니다.
```bash
$GEMINI_CLI --model pro-latest --thinking high --timeout 240 < prompt.txt
```
- **`--thinking`은 Gemini 3.x에서 네이티브 `thinking_level`로 전달됩니다** (`thinking_budget` 아님).
  `thinking_budget`은 3.x에서 ~5k thought token에서 포화하므로 최고 추론에 도달하지 못합니다.
- 실측(2026-07-25, hard prompt, `gemini-3.1-pro-preview`): `low` → 2,140 thought token / 30.0s,
  `high` → 8,473 / 74.8s. `high`가 API가 허용하는 최대 깊이입니다 (`max`는 `high`로 접힘).
- 그래서 `high`는 deep/ultra(240s/1800s)에서만 씁니다. simple(60s)에는 `low`를 유지하십시오.

### OpenAI CLI (`openai-cli`, retired bridge: `cliproxy-cli`)
기본 CLI는 `~/.synod/bin/openai-cli` (`OPENAI_API_KEY` 직접 호출)입니다.
- **gpt56sol** (기본값): `gpt-5.6-sol`
  ```bash
  $OPENAI_CLI --model gpt56sol --reasoning high < prompt.txt
  ```
- `--reasoning`은 `low|medium|high|xhigh`를 받습니다. 실측(2026-07-25, hard prompt):
  `low` → 1,024 reasoning token / 31.6s, `high` → 6,656 / 120.4s,
  `xhigh` → 11,548 / 190.6s. `xhigh`는 **ultra 티어 전용** — deep(240s)에서는
  190s가 여유가 너무 적어 `high`를 씁니다.
- `xhigh`를 지원하지 않는 모델(`gpt5mini` 등)에 넘기면 `high`로 clamp됩니다.
- **gpt54mini**: `gpt-5.4-mini` — fast tier
- **gpt55** / **o3**: 구 recovery 경로

> **백엔드**: 기본값은 `direct`입니다 (`provider_backend.DEFAULT_BACKEND`).
> `agy-cli`/`cliproxy-cli` 브리지는 **2026-06-30 만료 후 은퇴**했고,
> `SYNOD_PROVIDER_BACKEND=bridge`로만 복구용으로 도달할 수 있습니다.
> 사전 검증: `python3 tools/cutover_check.py`.

### DeepSeek CLI (`deepseek-cli`)
```bash
deepseek-cli --model reasoner --reasoning high < prompt.txt
deepseek-cli --model chat < prompt.txt
```

### Groq CLI (`groq-cli`)
```bash
groq-cli --model 70b < prompt.txt  # 초고속
groq-cli --model mixtral < prompt.txt  # 긴 컨텍스트
```

### Grok CLI (`grok-cli`)
```bash
grok-cli --model grok4 < prompt.txt  # 최고 성능
grok-cli --model fast < prompt.txt  # 빠른 응답
```

### Mistral CLI (`mistral-cli`)
```bash
mistral-cli --model large < prompt.txt
mistral-cli --model codestral < prompt.txt  # 코드 특화
```

---

## Quick Reference

| 명령 | 동작 |
|---------|--------|
| `/synod <prompt>` | **v2.0: 자동 분류** - 프롬프트 내용으로 모드 자동 감지 |
| `/synod 이 코드 리뷰해줘` | → auto-classify → review 모드 |
| `/synod API 설계해줘` | → auto-classify → design 모드 |
| `/synod 에러 수정해줘` | → auto-classify → debug 모드 |
| `/synod 아이디어 좀 줘` | → auto-classify → idea 모드 |
| `/synod resume` | 중단된 세션 계속 (see `modules/synod-resume.md`) |
| `/synod-setup` | 모델 가용성 테스트 및 최적 설정 생성 |
| `/cancel-synod` | 현재 세션 중단 (상태 보존) |

**Legacy (deprecated):** `/synod review: <code>`, `/synod design: <spec>` 등 명시적 모드 키워드도 여전히 동작하지만, deprecated 경고가 표시됩니다.

**환경변수:**

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `SYNOD_V2_AUTO_CLASSIFY` | `1` | `0`으로 설정하면 v1.0 모드 동작 |
| `SYNOD_V2_ADAPTIVE_TIMEOUT` | `0` | `1`로 설정하면 cold-start defaults 기반 적응형 타임아웃 활성화 |
| `SYNOD_DEBATE_GATE` | `1` | Phase 1.5 합의 게이트 (v3.8부터 기본 활성화). `0`=항상 전체 토론 |
| `SYNOD_ANONYMIZE` | `1` | 숙의 익명화 (v3.8부터 기본 활성화). `0`=비활성화 |
