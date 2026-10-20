---
name: time-calibrate
description: measure your real CC throughput against the time rule's matrix, using lore.db
user-invocable: false
---
<!-- tested with: claude code v2.1.122 -->

# /time-calibrate

re-measure your personal throughput and produce a diff report against the generic baseline in `plugins/cc/rules/time.md`.

## what to do when invoked

1. **check for `~/.claude/lore.db`** via `Bash`:
   ```bash
   test -r "$HOME/.claude/lore.db" && echo present || echo absent
   ```

2. **if absent**, explain and stop:
   - the calibration needs session history in `~/.claude/lore.db`.
   - that database is built by the `lore` plugin from `~/.claude/projects/`.
   - install via `/plugin install lore@anipotts`, run `/lore:graph`, then re-run `/time-calibrate`.
   - do not fail loudly. one-screen message, no stack traces.

3. **if present**, resolve active effort (same precedence as `/time-estimate`) and current model, then run the calibration SQL via `Bash` + `sqlite3 -readonly`.

## calibration SQL

paste into `sqlite3 -readonly ~/.claude/lore.db <<SQL ... SQL` or use a heredoc. all queries are parameter-free and read-only.

```sql
-- A. session-length bucket distribution
SELECT
  CASE
    WHEN duration_wall_seconds < 300 THEN '1_under_5min'
    WHEN duration_wall_seconds < 900 THEN '2_5to15'
    WHEN duration_wall_seconds < 1800 THEN '3_15to30'
    WHEN duration_wall_seconds < 3600 THEN '4_30to60'
    WHEN duration_wall_seconds < 7200 THEN '5_60to120'
    ELSE '6_over120'
  END AS bucket,
  COUNT(*) AS n,
  ROUND(AVG(duration_wall_seconds)/60.0, 1) AS mean_wall_min,
  ROUND(AVG(duration_active_seconds)/60.0, 1) AS mean_active_min,
  ROUND(AVG(tool_use_count), 0) AS mean_tools,
  ROUND(AVG(tool_use_count)*1.0/NULLIF(AVG(duration_active_seconds)/60.0, 0), 2) AS tools_per_active_min,
  ROUND(SUM(CASE WHEN compaction_count>0 THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS pct_compacted
FROM sessions
WHERE is_subagent = 0 AND duration_wall_seconds > 0
GROUP BY bucket
ORDER BY bucket;

-- B. model breakdown with thinking-per-tool proxy (effort pressure)
SELECT
  model,
  COUNT(*) AS n,
  ROUND(AVG(duration_wall_seconds)/60.0, 1) AS wall_min,
  ROUND(AVG(duration_active_seconds)/60.0, 1) AS active_min,
  ROUND(AVG(tool_use_count)*1.0/NULLIF(AVG(duration_active_seconds)/60.0, 0), 2) AS tool_rate,
  ROUND(AVG(CAST(thinking_block_count AS REAL)/NULLIF(tool_use_count, 0)), 2) AS thinking_per_tool
FROM sessions
WHERE is_subagent = 0
  AND duration_active_seconds > 60
  AND tool_use_count > 0
  AND model IS NOT NULL
GROUP BY model
HAVING n > 10
ORDER BY n DESC;

-- C. subagent prevalence
SELECT
  COUNT(*) AS total_subagents,
  COUNT(DISTINCT parent_session_id) AS parents_using,
  ROUND(AVG(duration_seconds)/60.0, 1) AS mean_subagent_active_min
FROM subagents;

-- D. cache hit rate
SELECT ROUND(SUM(total_cache_read_tokens)*1.0/
  SUM(total_cache_read_tokens+total_input_tokens+total_cache_creation_tokens), 4)
  AS cache_read_fraction
FROM sessions
WHERE is_subagent = 0;
```

## diff report shape

present a table comparing measured values to the rule's baseline. label the active effort and primary model for context:

```
calibration for: effortLevel=low (rung 4, user settings), primary=claude-opus-4-6

                        rule baseline    your measured    delta
baseline tool rate      3.0/min          3.19/min         +6%   within
quick-fix tool rate     6.0/min          6.32/min         +5%   within
opus-4.6 low throughput 1.00× (baseline) 1.00×            0%    reference
opus-4.7 low throughput 0.87×            0.84× (n=21)     -3%   low-confidence sample
cache hit rate          95-97%           96.6%            +0    within
```

flag any cell that drifts >15% from the rule. sample sizes under 50 are low-confidence; note them.

## what to emit

- the diff table
- a one-line verdict: "rule still accurate" OR "cells X, Y, Z drifted >15%, consider personal override"
- a note suggesting next re-measurement in ~90 days

## rules

- never modify `lore.db`. read-only only.
- never write a personal override file to the plugin directory. the plugin is shared.
- if the user wants to persist drift findings, suggest a personal note in `~/.claude/rules/` (user scope).
