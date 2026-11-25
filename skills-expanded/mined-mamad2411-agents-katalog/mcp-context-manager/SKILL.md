---
name: "mcp-context-manager"
description: "Auto compress dan truncate output MCP tools sebelum inject kembali ke context. Cegah pembengkakan 1 tool output = 10K token. Invoke SETELAH SETIAP MCP/tool call return, SEBELUM hasil dikirim balik ke LLM."
---

# MCP Context Manager — Tool Output Shrinking

## Problem
A single tool/MCP call can return 5,000–50,000 chars = 1,200–12,000 tokens → blows context instantly → triggers 4026 error. This is the #1 hidden cause of context bloat (users never see this happening; it's injected into messages[] before LLM).

## Mandatory Pipeline — AFTER EVERY tool/MCP call:
```
  Raw tool output
       │
       ▼  1. TRUNCATE_HARD
       │  If > 4000 chars → slice to [0..1500] + "… [TRUNCATED: show_next_chunk? tool=X offset=L for rest]"
       │
       ▼  2. DROP_METADATA_NOISE
       │  Strip: debug fields (timestamps, versions, pid, request_id), null keys, empty arrays,
       │         HTTP headers in full, verbose Python stack trace frames (keep last 3)
       │
       ▼  3. STRUCTURE_COLLAPSE
       │  JSON: keep only the top-level keys the user actually asked about. Unknown keys go to "<dropped N other keys>"
       │  Shell: keep stdout head+tail 25 lines each + 1 summary line of stderr if nonzero
       │  File read: keep signatures/imports; collapse 3-line-or-more code blocks not relevant
       │
       ▼  4. INLINE_SUMMARY
       │  Prepend single line summary of what this tool actually returned
       │    e.g. "curl result: HTTP 200, returned 132 products — first 7 shown below."
       │
       ▼  5. FINAL_TOKEN_GUARD
          If STILL > 1200 chars → re-run step 2 more aggressively, then step 1 with slice 1000
```

## Output Format Wrapper
Always wrap processed result in:
```
<tool_result name="tool-name" chars="NNNN" tokens="≈NNN" truncated="true|false">
  1-sentence inline summary
  ─────────────────────────────
  PROCESSED BODY (<= 1200 chars, already metadata-stripped + collapsed)
</tool_result>
```

## Special Cases
- **Browser DOM snapshots** (huge): keep only elements tagged with aria roles or event handlers, drop every div with only className, keep max 250 elements total
- **SQL / query results**: keep column names + first/last 10 rows only, with annotation "[N rows total, M shown]"
- **Git diff / logs**: keep the hunk headers + actual code changes; drop unchanged context lines from diff to 3 above/below each change (diff -U3 default is often 10, wasteful)

## 4026 Safety
After processing ALL pending tool results for a turn, SUM their token sizes. If sum > 2000 tokens → further summarise oldest results into a 2-line-per-call audit line instead of keeping full body.

Target single-turn tool payload injected back ≤ 2500 tokens ALWAYS. This leaves ~1300 for system + chat + model response in a 4026 window, guaranteeing no overflow.
