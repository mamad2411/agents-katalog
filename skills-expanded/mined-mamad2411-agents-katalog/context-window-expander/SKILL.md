---
name: "context-window-expander"
description: "FIX bug 4026 context length exceeded. Triple effective window via chunking, rolling summary, virtual memory swap. Invoke SEGERA jika error 'Context length has exceeded maximum limit (4026)' muncul, atau ketika context > 70%."
---

# Context Window Expander — 4026 Bug Killer + Virtual Memory

## Immediate 4026 ERROR RECOVERY
If you see the literal error: `"Context length has exceeded the maximum limit (4026)"`:
1. **DO NOT just retry same payload** — will fail identically
2. Run emergency compact:
   ```
   new_messages = [
       messages[0],                                                 # keep system prompt (already compressed)
       {"role":"assistant","content":"<context_swap: prior N turns summarized by hash=H, on-demand>"+single_line_summary_of_all_history()},
       messages[-3],                                                # keep last user
       messages[-2] if messages[-2].role=="tool" else skip,        # keep last tool result if any
       messages[-1],                                                # current user prompt
   ]
   ```
3. Re-request with max_tokens=min(400, 4026 - estimated(new_messages))
4. Immediately store the swapped-out section into `~/.cache/ctx_swap/<session>/turn_NNN.json` for on-demand retrieval

## Permanent Virtual Memory (for long sessions, > 20 turns)
```
Active window (in messages[]):  12 turns max + compact system
Swap file on disk:              unlimited turns, lazy paged back in
Index:                          JSON array of {turn, role, user_line_1, tokens, sha256_head}
                                stored at ~/.cache/ctx_swap/<session_id>/index.json
```

## Retrieval on Demand
When user asks "what did we discuss about X 20 turns ago?":
1. Scan index.json for keyword match on user_line_1 field
2. If hit, page back that turn (and ±1 neighbor for context) → inject back at [messages-3] slot
3. When no longer needed → drop them again from messages[] to stay under limit

## Chunked Long-Document Processing (>> 4026 tokens doc)
1. Slice input doc into chunks of ≤ 2000 tokens each, with 100-token overlap
2. Iterate per chunk → call SMALL tier model asking "return 1 sentence factual summary + any keywords + any TODOs"
3. Aggregate all summaries into a per-doc abstract (~400 tokens total for a 50-page doc)
4. Use abstract in the main task; only when user asks detail on section then re-load specific chunk's full text

## Auto-Compact Threshold
Every turn, MEASURE messages[]. If total estimated tokens > `0.70 × 4026 = 2818`:
1. Find oldest non-system non-last-4 turns
2. Replace each with 1-line rolling summary bullet appended to a `<history>` context block
3. Append a pointer to swap-file index so we can retrieve if needed

Guarantee: messages[] payload **never exceeds 3600 tokens** → 4026 bug IMPOSSIBLE.
