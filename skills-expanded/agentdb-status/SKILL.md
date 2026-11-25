---
name: agentdb-status
description: Show AgentDB health — pattern count, embedder status, cache hit rate, learning gain since init. Use when the user asks "is agentdb working?", "how many memories?", "show agentdb stats", or after long-running sessions to confirm state.
---

# AgentDB Status

Reports the live state of the AgentDB Cognitive Container backing this session.

## When to use

- User asks "what's in agentdb?", "is the memory working?", "show stats"
- Debugging recall quality — high miss rate? cache cold?
- Before / after a long session to see how much was learned
- CI smoke check before deploying an agent that depends on AgentDB

## Steps

1. Call `agentdb_pattern_stats` to get pattern count, hit rate, recent insert/search latencies.
2. If available, call `agentdb_reflexion_stats` for episode count and per-task win rates.
3. Call `agentdb_bandit_stats` (if `agentdb-learning` is installed) for arm reward summaries.
4. Render a compact table:
   ```
   patterns        12,847
   episodes           384
   skills              22
   hit rate          94.2%
   avg search       0.83 ms
   learning gain   +18% since init
   storage           38 MB (.rvf)
   ```
5. If any number looks off (zero patterns, hit rate <50%, latency >10ms), flag it and link to the relevant ADR / docs.

## Don't

- Don't dump the raw stats JSON — readers want the summary.
- Don't infer "broken" from a fresh init (zero patterns is correct on day 0).
