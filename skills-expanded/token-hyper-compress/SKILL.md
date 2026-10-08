---
name: "token-hyper-compress"
description: "Aggresif kompresi prompt 70-95% sebelum dikirim ke LLM: hapus kata sampah, parafrase kalimat, dedup history, sistem prompt micro-compact. Invoke sebelum SETIAP LLM call atau sebelum context > 10% window."
---

# Token Hyper-Compress — 90% Reduction Engine

## Layer-1 Inline Algorithm (NO LIBRARY NEEDED — run inside prompt crafting)
For EVERY piece of text going into system/user/assistant messages, apply these 12 transforms in order:

### A. System Prompt (reduce 80–95%)
1. **Strip boilerplate**: remove all "you are a helpful assistant", "think step by step", disclaimers, ethical lines unless task explicitly needs them
2. **Micro-compact**: rewrite rules to short imperative phrases, colon-separated. Example:
   - ❌ `Before writing code you must always first read the file with the Read tool to ensure you have the latest content`
   - ✅ `Read files BEFORE edit`
3. **Deduplicate**: if same rule appears twice (system prompt + skill repeat), keep ONE copy only, shortest version
4. **Unused skills prune**: if session only needs 2 skills but system lists 50+, keep only the 2 active ones and collapse rest to a one-liner fallback

### B. Chat History (reduce 60–90%)
5. **Turn collapse**: merge consecutive messages <50 tokens from same role into a single concatenated message
6. **Old turn pruning**: beyond turn 8, keep ONLY:
   - Final answer of assistant (50 char summary max)
   - First line of user question
   - Drop everything else from turns 1..8
7. **Reference pointer**: for long docs pasted by user → replace full doc with `<ref: filename/hash, Nk chars> + 200 char abstract`. On cache miss or detail questions only then re-inject via tool
8. **Whitespace kill**: collapse all multi-newline to single, strip trailing/leading, drop tab indentation beyond 2 levels (it's structurally same for LLM)

### C. User Query (reduce 30–60%)
9. **Greeting/pleasantry strip**: remove "hi", "hello", "thanks in advance", "could you please if you don't mind" → keep only the task imperative
10. **Normalize spelling**: 1 pass of obvious typos + normalise contractions (don't → do not only if needed; usually keep contractions — shorter)
11. **Dedup intent**: user asking same thing 3 ways → keep the most specific phrasing, drop other two (annotate: "(paraprases condensed)")

### D. Tool / MCP Output (reduce 80–95%)
12. **Structured summarization** (run AFTER tool call, BEFORE injecting result into context):
    - JSON → prune all keys that are null/empty/zero/default
    - Logs → keep first 3 + last 3 lines + single line error summary; drop 90% of log lines in between
    - File reads → if > 200 lines: only keep function signatures/imports (top 40 + tail 10 lines); annotate rest with `<omitted N lines, use Read offset:L to retrieve>`

## Apply Inline Every LLM Call
```
📊 COMPRESSION STATS REPORT (append after EVERY turn — lets user see savings)
  Input tokens  (raw) :  NNNN
  Input tokens  (opt) :  NNNN
  Reduction            :  XX.X%
  Running session saved:  NNNNNN tokens  ($NN.NN est.)
```

## Target
- Average compression across all message types: ≥70%
- System prompts specifically: ≥85%
