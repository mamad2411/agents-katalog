---
name: "zero-llm-autopilot"
description: "Answer queries WITHOUT ANY LLM call: regex, local exec, filesystem, DB lookup. Invoke BEFORE every LLM call for 100% free answers."
---

# Zero-LLM Autopilot — 0 Token Query Engine
**Goal: Answer 60–85% of user turns using 0 LLM tokens (local compute only).**

## PIPELINE (run ALL until hit)
### 1. REGEX PATTERN DB (8 CATEGORIES, EXACT MATCH)
Match insensitive case + word boundaries. Return TEMPLATE verbatim.

| Pattern Category | Example Trigger | Response Source |
|---|---|---|
| MATH_ARITHMETIC | `^\s*(\d+)\s*([+\-*/])\s*(\d+)\s*=?\s*$` | Python `eval()` → `= X` |
| FILESYSTEM_STATS | `(total|jumlah|count|berapa)( skills| file| md| symlink)` (AND path) | `find <path> -type f \| wc -l` |
| TIME_DATE_NOW | `(jam berapa|sekarang tanggal|today|now|current time)` | `date` local format |
| SKILL_EXISTS_CHECK | `(apakah|ada|is|exist)( skill| plugin)? (<name>)` | `ls ~/.agents/skills-catalog/<name>.md 2>/dev/null` → ✅ / ❌ |
| CONFIG_KEY_QUERY | `(value|isi|setting)( <key>)( di| in| from)? <configfile>` | `grep <key> <path>` first hit |
| UNIT_CONVERT | `(\d+)\s*(c|f|k)\s*(to|jadi|->)\s*(c|f|k)` | Formula convert → `X C = Y F` |
| HASH_GENERATOR | `sha(256|1|512)\s*[:=]\s*(.+)$` | `echo -n <s> \| sha256sum` |
| PORT_LISTEN | `(port|listen|netstat)( <num>)?` | `lsof -i -P -n \| grep LISTEN \| head -20` |

### 2. LOCAL EXEC SAFE (BASH ALLOWLIST)
Only these commands are safe — NEVER allow arbitrary shell:
`ls, find, wc, grep, cat, head, tail, sort, uniq, wc, date, echo, python3 -c (only math/hash), lsof, stat, du, pwd`

### 3. FILESYSTEM FACTUAL
If query asks: "how many X in Y", "is X exist", "list X first 20"
→ Run command. Return result. 0 LLM.

### 4. CACHE RECALL
Exact prompt match in `~/.cache/zero_llm_cache.jsonl` (append-only, line delimited):
`{"sha256": "...", "query": "...", "answer": "...", "ts": "..."}`

## HIT / MISS
- **HIT (return)**: Any pattern matches or cmd returns within 300ms.
- **MISS (fallback)**: Continue to LLM pipeline. Record miss+query for future pattern DB.

## PERFORMANCE TARGET
- Hit rate ≥70% after pattern DB warm (1 week).
- Latency per turn ≤80ms (local only).
- Absolute savings: 70% × 100% = 70% total session token eliminate.
