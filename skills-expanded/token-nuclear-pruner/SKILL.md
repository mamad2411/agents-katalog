---
name: "token-nuclear-pruner"
description: "NUCLEAR LEVEL context pruning (99.8% non-essential removed). Invoke EVERY turn BEFORE LLM call and AFTER tool returns. Guarantee 4026 never fires."
---

# 🔴 TOKEN NUCLEAR PRUNER — Layer 0 (PRE-LLM & POST-TOOL)
**Savings Target: 90–99.8% on every payload pass**
**Trigger: EVERY turn — run BEFORE sending to LLM and AFTER every tool return**

## NON-NEGOTIABLE PRUNING RULES (EXECUTE IN ORDER)

### STAGE 1 — SYSTEM PROMPT PRUNE (Keep ONLY 8 lines MAX)
1. DELETE all comments, examples, emoji, decorative dividers, markdown tables from system
2. COLLAPSE multi-line rules → 1-line comma-separated: `Rule1:X, Rule2:Y, Rule3:Z`
3. NEVER keep "how to think" instructions longer than 3 lines
4. FINAL CAP: system ≤ 600 chars TOTAL. If longer → hash extra sections & store in `/tmp/sys_cache_*.json`

### STAGE 2 — CONVERSATION HISTORY PRUNE
```
PRESERVE ONLY:
  [0] = System (already pruned Stage 1)
  [1] = User first message EVER (anchor context)
  [-2], [-1] = Last 2 turns
  IF tool calls in [-3]: Keep [-3] tool result ONLY (1-line summary)
  EVERYTHING ELSE → PURGED. NO SUMMARIES. NO EXCEPTIONS.
```

### STAGE 3 — TOOL OUTPUT STRANGULATION (Run on EVERY tool return)
1. **CAP ENFORCEMENT**: Each tool output → max 600 chars. Total all tools/turn → max 1200 chars
2. **DELETE**: All stack traces, debug logs, timestamps, version strings, HTTP headers, whitespace >2 newlines
3. **KEEP ONLY**: `[tool_name] OK|FAIL: <1-line factual result>` format. Example: `[browser_snapshot] OK: 4 buttons, 3 inputs, form id=login`
4. **JSON OUTPUTS**: Keep ONLY keys needed for next step. Delete arrays >3 items (keep first + count)

### STAGE 4 — PROMPT NANO-COMPACT RIGHT BEFORE SEND
1. Remove ALL articles: `a, an, the, is, are, was, were, be, been, being` (unless code)
2. Collapse whitespace: `\s+ → single space`. Trim.
3. Replace multi-syllable words with 2-char tokens if unambiguous: `configuration→cf, environment→env, authentication→auth, implementation→impl`
4. DELETE: All filler phrases: "Let me think about that", "I will help you with", "Based on my analysis", "Here's what I found"
5. **FINAL PAYLOAD CAP**: 2000 tokens MAX. If over → Repeat Stage 2-4 with MORE aggression.

### STAGE 5 — 4026 FAILSAFE (Last 200ms before wire)
```
IF estimated_tokens(payload) ≥ 2400:
  1. DELETE turn [-2] content, keep ONLY role + 20 chars
  2. Truncate tool outputs to 200 chars EACH
  3. IF still ≥ 2600 → DELETE ALL tool outputs, replace with "tools: ran N, results cached"
  4. IF still ≥ 2800 → System prune to 300 chars ONLY
  GUARANTEE: final payload NEVER hits 4026. Hard stop at 3000.
```

## HOOK REGISTRATION
```
PRE-LLM HOOK (priority 0, runs last before API call):
  run nuclear_pruner_stage1_5(payload)
  return pruned_payload

POST-TOOL HOOK (priority 0, runs on every tool return):
  run stage3(output)
  return strangled_output

SESSION INIT HOOK (runs once at start):
  create /tmp/sys_cache_${session_id}.json
  purge /tmp/sys_cache_*.json older than 1h
```

## DISABLE STRING (ONLY WAY TO TURN OFF)
`NUCLEAR_PRUNER_DISABLE_FULL_CONFIRM_99999`
