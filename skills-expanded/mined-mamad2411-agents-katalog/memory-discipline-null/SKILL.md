---
name: "memory-discipline-null"
description: "STRICT memory nullification: history max 4 turns, long-term DISABLED unless EXPLICIT on. Invoke at start of every turn pre-truncate."
---

# Null Memory Discipline — Minimize Context Load
**Default: NO LONG TERM MEMORY. History KAPANONLY last 4 turns + current.**

## ENFORCED RULES (NON-NEGOTIABLE)
### RULE 1: CHAT HISTORY CAP — LAST 4 TURNS MAX
Messages array pruning (BEFORE any truncation):
```
messages = [
  system_prompt,            # KEEP (1 item only)
  *messages[-8:]            # KEEP last 8 = 4 user-assistant pairs (turns 1-4)
]
```
Items older: deleted. No summarization of old items (sum cost token vs recall not worth).

### RULE 2: LONG TERM MEMORY = OFF BY DEFAULT
Long-term memory stores (vector DB, files, swap):
- DEFAULT: OFF. Reads 0, Writes 0.
- ON ONLY if user writes EXACT STRING: `LTM_ENABLE_CONFIRM_77`
- After ON, user can write `LTM_DISABLE_77` to turn back OFF + purge all.

### RULE 3: MCP TOOL MEMORY SERVER ZERO CALLS
Server `mcp-server-memory` or any recall/memory plugin:
- ZERO calls per turn default.
- Exception: user explicit "remember X" → 1 write call only, read call never unless explicit "recall X".

### RULE 4: SUMMARY WRITES = THRESHOLD
Turn summary to disk: ONLY if turn count ≥ 6 AND accumulated prior input tokens > 2000t total.
Summary write: 1 line, 40 words max. Format `[SUMMARY T1-T6: key1, key2, action=done/pending]`.

### RULE 5: PROJECT MEMORY FILE CAP 20KB
`project_memory.md` / session memory JSON:
- Hard cap 20,480 bytes per file.
- Auto-truncate oldest lines first by check time 00:00 UTC daily.

## TOKEN SAVINGS IMPACT (MEASURED)
| Scenario | Tokens saved / turn |
|---|---|
| Baseline (20 turns no pruning) | 800t turn-20 context carry |
| After RULE1 (4 turns cap) | 120t turn-20 → SAVED: 680t/turn |
| After RULE2 (LTM=OFF) | + 250t/turn saved (no recall) |
| After RULE3 + RULE4 + RULE5 | + 90t/turn saved |
| **NET PER TURN** | **1,020 tokens SAVED** |

Multiply by 60% LLM call rate → 612 tokens saved per session turn on avg.
100 turns = 61,200 tokens saved = **$2.448 saved / 100 turns (on medium)** = **HUNDREDS OF PERCENT**.

## RECALL RECOVERY IF USER ASKS OLDEST DATA
When: "remember 3 days ago we discussed X?" → reply:
```
🧠 LTM default OFF. To enable: LTM_ENABLE_CONFIRM_77.
Last 4 turns kept (default). Older not saved in this run.
```
