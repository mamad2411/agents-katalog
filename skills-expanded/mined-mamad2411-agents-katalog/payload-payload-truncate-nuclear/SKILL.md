---
name: "payload-payload-truncate-nuclear"
description: "NUCLEAR payload truncate: MAX 2500 tokens FINAL SEND. Invoke LAST in pipeline before LLM call. GUARANTEE no 4026, no overflow EVER."
---

# Payload Nuclear Truncator — HARD CAP 2500 TOKENS
**NO EXCEPTIONS. If over → chop. Guarantee: NEVER send >2500t (input).**

## TOKEN BUDGET ALLOCATION (2500 TOTAL MAX)
Split input tokens 2500 into 3 buckets FIXED:
| Bucket | Max Tokens | Priority Keep |
|---|---|---|
| SYSTEM PROMPT | 450 | HIGHEST (never truncate) |
| TURN HISTORY (user + assistant alternating) | 1250 | Keep: first turn + last 3 turns + middle compressed summary |
| TOOL OUTPUTS (if multi tool turn) | 800 | Keep: tool-status code + first + last 100 chars each. Truncate MIDDLE. |

## 5 STEP PROCESS
1. **MEASURE**: Encode messages[] with tiktoken cl100k_base. Count tokens. IF ≤2500: pass through. DONE.
2. **DROP LONG TOOL OUTPUTS FIRST**: Each tool.call >250 chars → strip to 250 chars. Delete tool.call[i] if duplicate tool_name+status of previous.
3. **HISTORY COLLAPSE**: Keep turn[0] (initial system/user) + turns[-3:] (last 3 turns). All others: merge into ONE compressed summary line: `[HIST n-turns collapsed: key_points=comma_separated_6_words]`
4. **SYSTEM PROMPT TRIM LAST**: IF still >2500 after steps 1-3 → prune system prompt lines BOTTOM-UP until ≤ 450t. KEEP top 5 lines (SOUL contract + activation rules).
5. **CHOP HARD**: If STILL >2500 after all 4 steps → remove assistant messages in pairs, oldest first, until exactly 2480 tokens reached. STOP.

## 2 FAILSAFE (before API call)
### FAILSAFE 1 (JSON SIZE CHECK)
`JSON.stringify(messages).length > 12500 bytes` → loop step 4 removal (2 turns per iteration) until ≤12,500 bytes. 5 bytes per token rough ratio.

### FAILSAFE 2 (PER CALL max_tokens conservative)
On the API request `max_tokens`: set to `min(requested, 150, (4026 - input_tokens - 50))`. Always leave 200t buffer. Buffer ensures 4026 NEVER hit by input+output sum.

## ERROR 4026 STATISTICS (TRACK)
Increment counter `~/.cache/truncation_counter.json` each run:
```json
{
  "turns_processed": 0,
  "truncations_applied": 0,
  "max_tokens_sent_seen": 0,
  "4026_error_avoided": 0
}
```
Report every 100 turns: `🔪 Trunc: {T}/{TP} turns. Max seen: {M}t. 4026 avoided: {E}.`

## BOUNDARY TEST
Hardcoded test: Input 20,000 tokens 50-turn long chat. After truncator: output messages = 24XX tokens. Range: 2400–2490. **Never >2499**.

## RECOVERY IF QUALITY DROP
If truncation caused wrong answer → turn next user says: `RECALL_FULL_CONTEXT_99` → load from disk swap (see context-window-expander) & answer with full (but compressed to 2500).
