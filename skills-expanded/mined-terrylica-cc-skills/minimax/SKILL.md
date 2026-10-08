---
name: minimax
description: MiniMax M-series production wiring patterns for the OpenAI-compatible API at api.minimax.io. TRIGGERS - MiniMax, MiniMax-M2.7, Hailuo
allowed-tools: Read, Bash, Grep, Glob, Write, Edit, WebFetch
---

# MiniMax M-series Production Wiring

OpenAI-compatible chat-completion endpoint at `https://api.minimax.io/v1` with the **M2.7-highspeed reasoning model** (premium tier as of 2026-04-29). LOOKS LIKE OPENAI but **silently drops 6 OpenAI parameters** and exposes `<think>` reasoning traces inside `content`. Beyond chat-completion, the API is MiniMax-native (different URLs, different body shapes, different error envelopes — HTTP 200 + `base_resp.status_code` instead of HTTP 4xx).

The model itself is a **competent qualitative judge + theory explainer + tool orchestrator** for finance/quant work, but **cannot do raw math** on realistic data sizes (saturates reasoning budget) and **hallucinates plausible details** under input uncertainty (6 documented instances). For production: pair it with Python for math, sandbox validators for code, and deterministic detectors for pattern recognition.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues. Source-of-truth campaign archive: `~/own/amonic/minimax/` (read-only reference; do not modify from this skill).

> **🆕 MiniMax-M3 is live (2026-06-01).** This file covers **M2.7**. For M3 — native vision,
> `reasoning_split` clean output, `response_format` acceptance, ~1M input ceiling (reliable retrieval ≤ ~256K) / 524K output cap,
> `n=1`, and the docs-vs-reality discrepancies — use the sibling skill
> [`../m3/SKILL.md`](../m3/SKILL.md) and the evidence doc
> [`../../references/M3-EMPIRICAL.md`](../../references/M3-EMPIRICAL.md). The defensive snippets
> below (`<think>` strip, `base_resp` retry, cached-token reader) apply to M3 unchanged.

---

## When to use M2.7 vs not — the decision table

| Workload                                       | Verdict                     | Why                                                                                        |
| ---------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------ |
| Tagging / classification (5-15 token outputs)  | ✅ Use plain `MiniMax-M2.7` | Plain is 2.5× faster than -highspeed for short outputs (cross-over at ~150 tokens).        |
| Summarization / long-form generation           | ✅ Use `-highspeed`         | -highspeed wins at >150 tokens. ~50 TPS asymptote (NOT the 100 TPS plan claim).            |
| Trade signal JSON output                       | ✅ Production-ready         | 6/6 verified across L1+L2+L3 layers with strict system prompt. Confidence well-calibrated. |
| Financial theory explanation                   | ✅ Graduate-level           | Black-Scholes derivations, FTAP, KKT, vol skew microstructure all correct.                 |
| Long-context retrieval (≤ 30K tokens)          | ✅ 4/4 needle retrieval     | NO "lost in the middle" effect. Perfect retrieval at 10/50/85/98% positions.               |
| Tool orchestration (agent loop)                | ✅ 4/4 correct selection    | Parallel + chained tool calls work. Refuses irrelevant queries gracefully.                 |
| Math / Black-Scholes / Sharpe on N≥50 returns  | ❌ DO NOT USE               | Saturates 8-16K reasoning tokens; route to Python (numpy/scipy/cvxpy).                     |
| QP / constrained optimization (Markowitz)      | ❌ DO NOT USE               | Same saturation pattern. Use scipy.optimize / cvxpy.                                       |
| Risk metrics on realistic data (N=252 returns) | ❌ DO NOT USE               | Even SINGLE metric saturates. Pre-summarize aggregates before passing.                     |
| Chart pattern recognition                      | ❌ DO NOT USE               | Hallucinates patterns in pure noise. Use TA-Lib / CV / classical algos.                    |
| Code generation (final, deployable)            | ⚠️ Scaffold-only            | Compiles 100%, runs 0% on first try (hallucinates library imports). Sandbox-validate.      |
| Vision / image input                           | ❌ NOT SUPPORTED            | M2.7 is text-only. `image_url` silently dropped at INPUT level.                            |
| TTS / video                                    | ⚠️ Plan-gated               | Endpoints exist (`/v1/t2a_v2`, `/v1/video_generation`) but error 2061 on Plus-High-Speed.  |
| Embeddings (bulk RAG)                          | ⚠️ RPM-tight                | `/v1/embeddings` accessible but rate-limited beyond ~5 calls. Use local embeddings.        |

---

## Top 10 production rules

1. **Always set a system prompt — it's at-most break-even, often net-positive.** Long instructions in `messages[0]` get ~70% billing rate AND replace MiniMax's hidden ~30-token default. Detailed instructions belong in system role, NEVER user content.

2. **Strip `<think>...</think>` from `content` before displaying.** M-series exposes its reasoning trace inside the content string. Production: `re.sub(r"<think>[\s\S]*?</think>\s*", "", content)`. Server-side stripping for billing on assistant replay (multi-turn doesn't double-bill).

3. **`max_tokens` ≥ 1024 for non-trivial tasks. 512 is a silent-empty footgun.** Reasoning consumes budget BEFORE visible content. Branch on `finish_reason == "length"` defensively.

4. **Trust capability params, suspect control params.** Honored: `tools`, `messages`, `max_tokens`, `temperature`, `stream`. Silently dropped: `stop`, `tool_choice`, `response_format`, streaming `usage`, `image_url`, `messages[].name`.

5. **For JSON output, prompt-engineer it — `response_format` is silently dropped.** Strict system prompt + `temperature=0.2` + `max_tokens=4096` + `try/except json.loads` = 100% reliability (6/6 verified).

6. **Plain `MiniMax-M2.7` for short-output workloads (<150 visible tokens); `-highspeed` for long-form.** "Highspeed" is COUNTERINTUITIVELY slower for short outputs (Karakeep tagging at 5-15 tokens: plain is 2.5× faster).

7. **Caching is COST-only on MiniMax, not LATENCY.** Add `cache_control: {type: "ephemeral"}` to system messages for ~95% input-token cost reduction; don't expect interactive-UX latency benefits. Activates at ~600+ prompt_tokens. Prefix-match works (varied user + stable system gets ~70% hit rate).

8. **Route financial math to Python — M2.7 saturates on QP / numerical integration / Sharpe on N≥50 returns.** Pre-summarize aggregates (mean / stdev / n) and pass them; M2.7 handles the final-step formula. Define financial primitives as TOOLS for agent-loop orchestration.

9. **NEVER trust M2.7-generated code without sandbox validation.** `compile()` is INSUFFICIENT. M2.7 invents library imports (`SMA`, `RSI`, `BollingerBands` from `backtesting.lib` — none exist). Run in subprocess + capture exit code + iterative repair on failure.

10. **NO HTTP 429 — rate-limited responses are HTTP 200 + `base_resp.status_code=1002`.** Standard retry middleware that watches HTTP status WILL NOT catch this. Use code-prefix-based handler: `1xxx` family = retry with backoff; `2xxx` family = fix request, don't retry.

---

## Canonical Tier F agentic stack (quant-LLM workflow)

```
F4: long-context retrieval         → M2.7 finds facts from filings/research
        ↓
F2: structured judgment as JSON    → M2.7 emits trade signal
        ↓
F6: tool orchestration             → M2.7 selects + calls tools (parallel + chained)
        ↓
F1+F8+F9: Python math layer        → numpy/scipy/cvxpy compute deterministically
        ↓
F3: textbook explanation           → M2.7 narrates the result with theory
        ↓
F5: sandbox-validated code         → M2.7 scaffolds; subprocess validates
```

**The pattern**: M2.7 for judgment / theory / orchestration; Python for math / validation / pattern detection. Never mix "explain + compute" in one prompt for complex problems — saturation is the failure mode.

| Primitive    | M2.7's role                                  | Python's role                                   | Verdict             |
| ------------ | -------------------------------------------- | ----------------------------------------------- | ------------------- |
| F1 Math      | ❌ saturates                                 | ✅ scipy/numpy compute                          | Python only         |
| F2 JSON      | ✅ 6/6 trade signals across scenarios        | parse + execute                                 | M2.7 + Py           |
| F3 Theory    | ✅ graduate-level Black-Scholes / FTAP / KKT | render markdown                                 | M2.7 only           |
| F4 Long-ctx  | ✅ 4/4 needle retrieval at 27K tokens        | ❌ pre-tag Items client-side (anti-fabrication) | M2.7 + Py guard     |
| F5 Codegen   | scaffold only — invents library imports      | ✅ subprocess validation MANDATORY              | M2.7 + Py validator |
| F6 Tools     | ✅ 4/4 orchestration + parallel calls        | execute the tool bodies                         | M2.7 + Py           |
| F7 Patterns  | ❌ hallucinates in random walks              | ✅ TA-Lib / CV / classical algos                | Python only         |
| F8 Optim     | ❌ saturates on QP                           | ✅ scipy.optimize / cvxpy                       | Python only         |
| F9 Risk      | ❌ saturates on N=252 returns                | ✅ numpy returns/drawdowns                      | Python only         |
| F10 Mandarin | ✅ matches/exceeds English on quant content  | translate + pass through                        | M2.7 (with caveats) |

---

## Defensive code snippets (copy-paste ready)

### Strip `<think>` tags + handle finish_reason

```python
import re

def parse_minimax_response(response: dict) -> tuple[str, str | None]:
    """Returns (visible_content, error_class).
    error_class is None for normal responses; set when finish_reason indicates issues."""
    choice = response["choices"][0]
    raw_content = choice.get("message", {}).get("content", "")
    finish = choice.get("finish_reason")

    # Strip reasoning trace
    visible = re.sub(r"<think>[\s\S]*?</think>\s*", "", raw_content).strip()

    # Defensive: detect saturation (per iter-36/37 — empty visible + length finish)
    if finish == "length" and len(visible) < 50:
        usage = response.get("usage", {})
        reasoning_tokens = (usage.get("completion_tokens_details") or {}).get("reasoning_tokens", 0)
        max_tokens = usage.get("completion_tokens", 0)
        if reasoning_tokens >= max_tokens * 0.95:
            return visible, "saturated"
    if finish == "length":
        return visible, "truncated"
    return visible, None
```

### Production-ready JSON output (no `response_format` reliance)

```python
SYSTEM_PROMPT = """You are a trading signal generator. Output ONLY a JSON object with these exact 5 fields:
{
  "action": "long" | "short" | "flat",
  "confidence": <0.0 to 1.0>,
  "reasoning": "<one sentence explaining the setup>",
  "stop_loss_pct": <number, 0 if action=flat>,
  "take_profit_pct": <number, 0 if action=flat>
}
No markdown, no prose before or after, no code fences. Just the JSON object."""

# call with temperature=0.2, max_tokens=4096, model="MiniMax-M2.7-highspeed"
# then: signal = json.loads(parse_minimax_response(resp)[0])
```

### Cache-friendly system prompt with prefix-match

```python
def build_messages(user_input: str, stable_system: str) -> list[dict]:
    """stable_system varies per service but is constant per call. Cached after first call,
    re-used across varying user_input (~70% hit rate on prefix match)."""
    return [
        {
            "role": "system",
            "content": stable_system,
            "cache_control": {"type": "ephemeral"},  # Anthropic-style; honored by MiniMax
        },
        {"role": "user", "content": user_input},
    ]

# For short system prompts (<300 tokens), pad to ≥600 to ACTIVATE caching.
# Counterintuitive: more bytes = lower billable tokens once cached.
```

### Rate-limit-aware retry (no HTTP 429 — parse base_resp)

```python
import time

def call_with_retry(client_fn, body: dict, max_attempts: int = 5) -> dict:
    """MiniMax returns HTTP 200 + base_resp.status_code=1002 on rate limit.
    Standard HTTP-status-based middleware will NOT catch this."""
    for attempt in range(max_attempts):
        resp = client_fn(body)
        base_resp = resp.get("base_resp", {})
        code = base_resp.get("status_code", 0)
        if code == 0:
            return resp
        if code == 1002:  # rate limit
            time.sleep(2 ** attempt)
            continue
        if code in (1004, 2013, 2061):  # auth / params / plan-gated — don't retry
            raise RuntimeError(f"MiniMax error {code}: {base_resp.get('status_msg')}")
        raise RuntimeError(f"Unknown MiniMax error {code}: {base_resp.get('status_msg')}")
    raise RuntimeError("MiniMax rate limit persisted across max attempts")
```

### Cached-token reader (handles both API shapes)

```python
def get_cached_tokens(usage: dict) -> int:
    """MiniMax uses BOTH OpenAI-style (auto-cache) and Anthropic-style (explicit cache_control).
    Production parsers must handle BOTH variants."""
    pt_details = usage.get("prompt_tokens_details") or {}
    return (
        pt_details.get("cached_tokens", 0)               # OpenAI shape
        or usage.get("cache_read_input_tokens", 0)       # Anthropic shape
        or 0
    )
```

---

## 11 documented failure modes — defenses

### Hallucination (6 instances) — fabricates plausible details under input uncertainty

| Domain                | What was fabricated                                             | Defense                                       |
| --------------------- | --------------------------------------------------------------- | --------------------------------------------- |
| JSON enforcement      | Returned JSON-shaped natural language without `response_format` | Prompt-engineer; try/except json.loads        |
| Vision input          | Deliberated about missing image instead of refusing             | Don't use M2.7 for vision; pre-OCR            |
| 10-K source citations | Invented "Source: ITEM 3" attributions                          | Pre-tag inputs client-side; validate post-hoc |
| Library imports       | `SMA`, `RSI` from `backtesting.lib` (do not exist)              | Sandbox-execute; iterative repair             |
| Chart patterns        | "Descending Triangle bullish breakout" in PURE GBM noise        | Use TA-Lib / CV; don't ask M2.7               |
| Confidence handling   | (Counter-example — calibration WAS correct; pattern is broader) | Cross-validate with deterministic alts        |

**Detection heuristic**: `reasoning_tokens > 2.5× baseline` correlates with hallucination (per iter-35). Flag for review.

### Saturation (4 instances) — exhausts reasoning budget on impossible math

| Task            | Budget | Symptom                                 | Defense                                  |
| --------------- | ------ | --------------------------------------- | ---------------------------------------- |
| Sharpe (N=10)   | 4K     | Empty visible; succeeded at 16K budget  | Pre-summarize; route to Python           |
| Black-Scholes   | 16K    | N(d1)/N(d2) computation never converged | Don't use M2.7; use scipy.stats.norm.cdf |
| Markowitz QP    | 8K     | KKT solve attempted; budget exhausted   | Use scipy.optimize / cvxpy               |
| Sortino (N=252) | 8K     | Per-value tracking burned tokens        | Pre-summarize aggregates                 |

**Detection heuristic**: `is_saturated = (finish_reason=='length' AND len(visible)<50 AND reasoning_tokens >= 0.95*max_tokens)`. Don't retry with higher budget — route to Python instead.

### Cross-language asymmetry (1 instance)

| Query          | English response                           | Mandarin response                             |
| -------------- | ------------------------------------------ | --------------------------------------------- |
| Tiananmen 1989 | Full historical narrative incl. "massacre" | Graceful deflection ("我不太清楚...换个话题") |

**Defense**: detect non-substantive responses (short + uncertainty language) for amonic services with multilingual users. Financial use cases unlikely to bite. International `api.minimax.io` applies Chinese-language-specific filtering on politically-sensitive content; English equivalents unfiltered.

---

## API surface map (Plus-High-Speed plan)

| Endpoint           | URL                              | Body shape                              | Plan-gated? | Notes                                           |
| ------------------ | -------------------------------- | --------------------------------------- | ----------- | ----------------------------------------------- |
| Chat completion    | `/v1/chat/completions`           | OpenAI-compat (6 silent-dropped params) | No          | Primary interface                               |
| Models catalog     | `/v1/models`                     | OpenAI-compat                           | No          | 7 models on this tier                           |
| Embeddings         | `/v1/embeddings`                 | MiniMax (`texts`/`type`/`vectors`)      | RPM-gated   | Multi-min cooldown; impractical for bulk RAG    |
| Files (CRUD)       | `/v1/files/{list,upload,delete}` | Sub-resource verbs                      | No          | Full CRUD; int64 file_id (JS precision risk)    |
| TTS                | `/v1/t2a_v2`                     | MiniMax-native                          | Yes         | All 6 speech models gated (2061)                |
| Video              | `/v1/video_generation`           | MiniMax-native, async                   | Yes         | task_id polling pattern (untested)              |
| Vision (image_url) | (drops at input)                 | OpenAI-compat                           | N/A         | NOT supported on M2.7 — text-only model         |
| Web search MCP     | `tools: [{type: "web_search"}]`  | OpenAI-compat                           | Yes         | First HTTP 400 in campaign (2013 "not support") |

---

## Operational facts

| Topic                  | Fact                                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------- |
| Concurrency sweet spot | `p=10` for chat-completion (true parallelism, ~5x throughput vs serial). p=20 only buys 25% more.       |
| TPS asymptote          | ~50 tokens/sec on highspeed (NOT the 100 TPS plan claim). Use 40 TPS for production capacity baseline.  |
| Min latency floor      | ~1.5s per call (network + tokenization + reasoning preamble) — can't go below regardless of prompt size |
| Context ceiling        | 200K tokens (between 142K and 262K). Safe operating: 100K. Token-byte ratio: 3.6 chars/token English    |
| Cache activation       | Auto-cache at ~600+ prompt_tokens; explicit `cache_control` works; ~70% hit rate on prefix match        |
| Cache TTL              | ≥ 3 minutes (zero decay across 185s tested); upper bound likely 5min                                    |
| Stream chunk shape     | Coarse-grained (~125 chars/chunk, ~2/sec). Not per-token. `<think>` splits across chunks.               |
| Mandarin token cost    | 1.4-1.5× English for equivalent semantic content (BPE behavior on CJK)                                  |

---

## OPS tooling — model-upgrade detection

The campaign produced an active tripwire: when MiniMax ships a new model, scheduled polling detects it and exits non-zero to force re-verification. See `scripts/minimax-check-upgrade` (ported in iter-16) and `references/model-upgrade-detection.md`.

```bash
# After install + lock-snapshot setup:
~/path/to/minimax-check-upgrade
# Exit 0 = no change (live matches locked snapshot)
# Exit 1 = upgrade detected (review diff before bumping lock)
# Exit 2 = fetch error
```

Recommended: schedule daily via launchd/cron. Add to CI as a pre-merge gate to refuse changes when the catalog has drifted without explicit lock review.

---

## Deep references (drill into these for specifics)

- `references/RETROSPECTIVE.md` — the 41-iteration retrospective (TL;DR, top 10 rules, agentic stack, full failure-mode catalog, API surface, operational facts, open questions)
- `references/quirks.md` — use-case-organized critical findings (5 production-must-knows up front)
- `references/api-patterns/INDEX.md` — navigable TOC of 40 per-endpoint pattern docs
- `references/api-patterns/<endpoint>.md` — minimum-viable request/response shape, idiomatic snippets, known failure modes, reproducer commands, full provenance per probe
- `references/fixtures/` — selected raw API responses for diffing against future API changes
- `scripts/minimax-check-upgrade` — model-upgrade detection executable
- `templates/launchd-check-upgrade.plist` — daily polling plist template

---

## Quick-start for new amonic services

```bash
# 1. Set environment
export OPENAI_BASE_URL=https://api.minimax.io/v1
export OPENAI_API_KEY=<from 1Password>
export MINIMAX_MODEL=MiniMax-M2.7              # for tagging-style services
# OR: export MINIMAX_MODEL=MiniMax-M2.7-highspeed   # for long-form services

# 2. Verify wiring
curl -sS -X POST "$OPENAI_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"model": "MiniMax-M2.7", "messages": [{"role": "user", "content": "Reply OK"}], "max_tokens": 200}' \
  | python3 -m json.tool | head -20

# 3. Add cache_control to your stable system prompt for ~95% input cost reduction (see snippet above)
# 4. Add the strip-<think> + finish_reason check to your response parser
# 5. Add base_resp.status_code rate-limit handler (no HTTP 429)
# 6. If using mise: schedule check-upgrade as a pre-merge CI gate
```

---

## Provenance

Distilled from the 41-iteration `minimax-m27-explore` autonomous-loop campaign at `~/own/amonic/minimax/`:

- 40 verified hands-on pattern docs (`api-patterns/*.md`)
- 1 quirks consolidation (`quirks/CLAUDE.md` — iter-11)
- 1 retrospective (`RETROSPECTIVE.md` — iter-42)
- 1 OPS tool with launchd plist (`bin/minimax-check-upgrade` + `config/plists/`)
- ~50 API response fixtures
- ~155 Non-Obvious Learnings, 35 critical findings, 11 documented failure modes, 4 error code families, 6 compat envelope categories

Campaign verified against `MiniMax-M2.7-highspeed` between 2026-04-28 and 2026-04-29. Re-verify against new model versions via `mise run minimax:check-upgrade`.

## Post-Execution Reflection

0. **Locate yourself.** — Confirm this SKILL.md is the canonical file before any edit.
1. **What failed?** — A wiring snippet stopped working, a parameter that was reported "silently dropped" now succeeds, or a `base_resp.status_code` mapping changed. Update the affected pattern doc + the table here so the next reader doesn't repeat the failure.
2. **What drifted?** — `mise run minimax:check-upgrade` flagged a new model version, the OpenAI-compat envelope changed shape, or rate-limit / cache_control semantics shifted. Update the locked-snapshot pointer and the impacted sections.
3. **Log it.** — Append a dated line under "Provenance" (or a new "Evolution log" section) with trigger + fix + evidence so future iters can audit drift.
