---
name: "router-tier-zero-escalation"
description: "ULTRA cost routing: TINY model only. FLAGSHIP BANNED unless 4x TINY failures + EXPLICIT user override. Invoke on model selection."
---

# Router Tier-Zero — NO FLAGSHIP GUARANTEE
**Only 1 model tier by default: TINY.** Cost vs flagship: 50×–200× less.

## 5 MODEL TIERS (USED: ONLY TINY 95% & SMALL 5%)
| Tier | Budget ID | Example Model | Cost per 1M tokens IN/OUT | MAX TOKENS/RESP | WHEN TO USE |
|---|---|---|---|---|---|
| 0 | TINY (DEFAULT) | ministral-3b / gemini-flash-tiny / gpt-4o-mini-turbo | $0.05 / $0.20 | 150 | DEFAULT. ALWAYS START HERE. |
| 1 | SMALL | devstral-medium / claude-haiku / gpt-4o-mini | $0.15 / $0.60 | 250 | 2x TINY FAILS ONLY |
| 2 | MEDIUM | mistral-large / sonnet-4 | $3.00 / $15.00 | 500 | BANNED BY DEFAULT |
| 3 | LARGE | opus-4 | $15.00 / $75.00 | 800 | BANNED |
| 4 | XL FLAGSHIP | largest available | $75.00+ / $300+ | 1200 | **NEVER** unless override |

## ESCALATION RULES (ENFORCED COUNTER)
Internal counter: `TINY_FAIL=0`. Increment when response quality:
- Hallucinates facts verifiable by local check (wrong count, wrong path, wrong math)
- Refuses task when capability exists (template "I cannot")
- Code output has syntax error (run `ast.parse` / `eslint --stdin` post)
- Output length 0 or garbage (non UTF-8)

Escalation Matrix:
| TINY_FAIL | Action |
|---|---|
| 0 → 1 | Retry TINY, same prompt, temp 0.1 lower |
| 1 → 2 | Retry TINY, prompt append `URGENT: VERIFIABLE FACT ONLY.` |
| 2 → 3 | **ONE (1) SMALL call only**. After SMALL call, AUTO RESET TINY_FAIL to 0 for next turn. |
| 3 → 4+ | **STOP. REPLY ERROR:** "4× TINY + SMALL fail. Need user: `MEDIUM_OVERRIDE_CONFIRM_54321` to proceed." NEVER auto-medium after 3. |

## FLAGSHIP (XL) OVERRIDE
FLAGSHIP TIER 4 ONLY POSSIBLE if:
1. User writes **EXACTLY** (3 line block verbatim):
```
FORCE_XL_FLAGSHIP
REASON: <100 chars explaining why TINY cannot do it>
SIGNATURE: USER_CONFIRM_COST_$1.00_MIN
```
2. Total session XL budget already set: `FLAGSHIP_BUDGET_USD = $0.50` max.
3. After 1 XL → back to TINY next turn. Counter TINY_FAIL reset to 0.

## ENFORCEMENT HOOKS (RUN B4 MODEL CALL)
- If session model_distribution: TINY < 92% of calls → FORCE DROP next 3 to TINY.
- Log every model pick + savings: `🧭 TIER:{0/1}|model:...|saved_vs_xl: 99.XX%|fail_counter:{n}`
- Never pick model by "best quality" heuristic. ONLY by fail counter.

## 30 DAY TARGET
- TINY call ratio: ≥ 94%.
- SMALL call ratio: ≤ 6%.
- MEDIUM/LARGE/XL call count: **0** (ZERO).
- Cost: ≤ 0.5% of baseline (flagship default) spend. = 200× savings = **19,900% improvement** (thousands of percent).
