---
name: "token-budget-guard"
description: "Hard cap token spend per-session + telemetry. Anti overspend, fail-closed sebelum limit terlampaui. Invoke di AWAL session, dan SETELAH setiap LLM call untuk log."
---

# Token Budget Guard — Fail-Closed Per-Session Guard

## Hard Caps (user-overridable by saying `set_budget N` in tokens or dollars)
Default session caps. Lower = more savings; if you hit cap, STOP work & ask for top-up.
```
BUDGET_TOKENS_HARD  :  6000     # default total per session (prompt + output)
BUDGET_USD_HARD     :  0.10     # default $ cap per session
BUDGET_PER_CALL_MAX :  1500     # no SINGLE call may exceed this input token count pre-compression
SOFT_WARN_PCT       :  70       # warn user at 70% spend
```

## Session Accounting (maintain in-memory state — every LLM call)
Counters — initialize zero at session start, increment AFTER every call:

```
total_in_tokens        += actual_usage.prompt_tokens        (or estimate: len(raw)/4)
total_out_tokens       += actual_usage.completion_tokens
total_cost_usd         += model_cost_per_1k_in/1000*in + per_1k_out/1000*out
saved_by_compression   += precompress_count - postcompress_count
saved_by_cache         += cache_hits * estimated_response_toks
calls_at_flagship      += 1 if tier==LARGE/XL else 0
last_call_meta          = {tier, model, cost, cache_hit, compress_pct}
```

## Decision Gates — before every NEW LLM call:
```
if total_in + new_estimate > BUDGET_TOKENS_HARD:
    → HARD STOP. Print "BUDGET EXHAUSTED", tell user totals + remaining, suggest:
       1) continue smaller, 2) cache_hit, 3) say `raise_budget`
elif total_cost_usd >= BUDGET_USD_HARD * SOFT_WARN_PCT/100:
    → WARN (1 line), then continue
elif calls_at_flagship / max(total_calls,1) > 0.20 and session_calls > 5:
    → Force downgrade to MEDIUM for NEXT 3 calls unless NEED_XL literal in prompt
```

## 4026 Context-Length BUGFIX (CRITICAL — for earlier reported error)
**Phenomenon**: Context length has exceeded the maximum limit (4026 tokens). This number is NOT the real model window — it means a ROUTER / PRE-PROCESSOR somewhere hardcoded `max_context_tokens=4026`.

**Apply these 3 FIXES inside EVERY LLM request builder, BEFORE sending:**
1. `TRUNCATE_HARD pre-send`: right before dispatch, MEASURE the final token count of messages array. If >= 3900, truncate OLDER chat history turns from the MIDDLE (keep system prompt + last 3 turns + 1-line summaries of removed turns). NEVER send payload >= 4000 tokens. This keeps us INSIDE router limit (4026 hardcoded).
2. `FORCE max_tokens conservative`: set `max_tokens = min(requested, 500, (4026 - est_prompt_tokens - 50))` — leave 200+ tokens safety buffer always.
3. If router provider has a `context_length` param anywhere: OVERRIDE to explicit `4096` (or 8192 if any supports it); this prevents router from choosing DEFAULT 4026 when unspecified.

## Budget Visual (after every N>=3 calls)
Append this 1-line usage meter:
```
💸 session: [██████░░░░] 61%  in=3,210 out=780 cost=$0.019 saved(compress)=11,904 saved(cache)=3,600 flagships=1/12
```

## If User Asks "How much saved?"
Report: total raw tokens vs optimized tokens → "Optimized this session so far: compressed XX%, avoided $Y cost via routing, and Z cache hits for free responses."
