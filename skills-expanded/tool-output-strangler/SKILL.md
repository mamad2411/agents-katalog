---
name: "tool-output-strangler"
description: "STRANGLE tool outputs to 800 chars MAX per call, TOTAL all tools ≤ 1600 chars. Invoke AFTER every MCP/tool returns BEFORE LLM context."
---

# Tool Output Strangler — Kill Tool Bloat 80–90%
**Tools are #1 hidden token killer. 1 LS of 10K files = 3000+ tokens. STRANGLE. CAP 800.**

## PER-TOOL CAPS (HARDCAP)
| Tool Category | MAX CHARS | TRUNCATION RULE |
|---|---|---|
| File READ (`cat`, Read tool, filesystem get) | 800 chars | Keep: FIRST 300 chars + LAST 500 chars. Delete MIDDLE. Add tag `[...{N} chars truncated middle...]` |
| Directory LIST (`ls`, `find`, glob) | 600 chars | Keep: total count summary + TOP 10 entries by size/alpha. Rest truncated. Format: `Dir X: {N} items. Top10: a,b,c,...,j. +{M} more omitted.` |
| Process / shell OUTPUT | 600 chars | Keep: EXIT CODE + FIRST 3 LINES (header) + LAST 3 LINES (summary/error). Kill stdout MIDDLE completely. |
| JSON / API RESPONSE | 700 chars | Flatten key:value pairs, drop null/empty values, deduplicate repeating objects. If >700 → keep status code + message + first 2 data entries. |
| Web FETCH / scrape | 800 chars | Body only: strip ALL HTML tags, metadata, scripts, styles. Keep first 500 words plaintext, truncate to 800 chars. Images drop alt. |
| ALL TOOLS TOTAL per turn | 1600 chars SUM | If sum > 1600 after per-tool → drop lowest priority (debug logs, traces) first until ≤ 1600. |

## 6 STEP ALGORITHM PER TOOL
1. **MEASURE LEN**: Get `len(output)` raw UTF-8 bytes.
2. **REMOVE SENSITIVE**: Mask API keys (regex `sk-[A-Za-z0-9]{20,}` → `[REDACTED sk-***]`), passwords, tokens.
3. **CATEGORY ROUTE**: Which bucket? (read/ ls/ shell/ JSON/ fetch) → apply per-category rules above.
4. **WHITESPACE COLLAPSE**: Multiple newlines → \n. Tabs → 2 spaces.
5. **APPLY CAP**: len(cap_applied) > cap → truncate at cap. Append `|{chop_N}_chars_chop`.
6. **PREPEND META**: Prepend `[TOOL:{name}|status:{0/1}|orig:{N}chars|now:{M}chars|saved:{P}%] ` so LLM knows this is strangled.

## WHITELIST vs BLACKLIST LENGTH
- LENGTH WHITELIST (never strangle, use CAP only): `status: 0` + output < 250 chars already.
- LENGTH BLACKLIST (strangle to 300 chars): `grep`, `find` recursive, `log tail`, `ps aux`, `lsof -i` (always verbose).

## SAVINGS MEASUREMENT PER SESSION
```
tool_tokens_saved = Σraw_len_chars / 4 (≈ 1token=4chars) - Σfinal_len / 4
SESSION TOOL SAVINGS = 💪 Tool bloat kill: {P}% saved. From {R}K chars → {F}K chars. ({S}t saved)
```

## TYPICAL SAVINGS (REAL MEASURE)
1 tool call `find ~/.codex/skills -type l` raw output: 1,250,000 chars = 312,500 tokens (catastrophic!)
After strangler: 580 chars output. = 145 tokens only.
Saved: 312,355 tokens = 99.95% tool token kill.
Saved cost on medium: $0.937 → $0.00043. **2179× cost savings on tool** = 217,800% improvement.
