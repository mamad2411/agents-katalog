---
name: analyze-context-router
description: "Analyze memory retrieval logs for routing accuracy, false negatives, token efficiency, and system health. Use when the user wants to evaluate how well the memory loader is performing, check retrieval quality, audit retrieval routing, or identify improvement opportunities. Triggers on \"analyze memory retrieval\", \"how's the memory loader doing\", \"memory retrieval analysis\", \"check retrieval quality\", \"memory loader performance\"."
disable-model-invocation: true
---

# Memory Retrieval Analysis

> **Requires the `multiplai-context` plugin.** This skill analyzes that plugin's runtime artifacts — the `context-router-*.log` retrieval logs, `context-router.py` hook, and `memory-catalog.json`. Without multiplai-context installed and active, there are no logs to analyze.

Analyze the memory retrieval log files to assess routing quality, identify failure modes, and track improvement over time. Uses a watermark file to partition pre/post-fix data so metrics reflect only the current system behavior.

## Key Files

| File | Purpose |
|------|---------|
| `$CLAUDE_CONFIG_DIR/context-router-*.log` | Daily retrieval logs (7-day retention) |
| `$CLAUDE_CONFIG_DIR/context-router-watermark.json` | Analysis watermark: last analysis timestamp, baseline metrics, deployment info |
| `$CLAUDE_CONFIG_DIR/hooks/context-router.py` | The retrieval hook source (for recommending code changes) |
| `$CLAUDE_CONFIG_DIR/memory/memory-catalog.json` | File catalog used for routing (for recommending catalog changes) |

## Workflow

### Step 1: Read Watermark

Read `$CLAUDE_CONFIG_DIR/context-router-watermark.json`. Extract:
- `deployed_at` — timestamp of last improvement deployment
- `last_analysis` — timestamp of last analysis run
- `baseline_metrics` — metrics from the previous analysis (for delta comparison)

If no watermark exists, this is the first run. Analyze all available logs and create the watermark at the end.

### Step 2: Discover and Filter Logs

Glob `$CLAUDE_CONFIG_DIR/context-router-*.log` to find all available log files.

**Filtering rule:** Only analyze log entries with timestamps AFTER the watermark's `last_analysis`. This prevents re-analyzing data from prior runs.

If fewer than 50 events exist post-watermark, warn the user:
> "Only N events since last analysis on DATE. Recommend waiting for more data, or I can include pre-watermark data with a clear partition marker."

If the user agrees to include older data, partition the report into "pre-fix" and "post-fix" sections using `deployed_at` as the boundary.

**IMPORTANT:** Delegate the heavy log parsing to a general-purpose agent to protect the main context window from massive log files. The agent should return aggregated metrics, not raw log content.

### Step 3: Quantitative Analysis

Compute across 7 dimensions:

1. **Volume** — events/day, events/session, sessions/day, total events
2. **Routing rates** — NONE%, routed-to-files%, EVAL:true%
3. **File distribution** — load frequency per memory file, files never loaded in period
4. **Token cost** — median and max retrieval size in bytes, estimated tokens (~4 chars/token), total retrieval bytes for period
5. **Dedup effectiveness** — count of `[DEDUP skipped:]` entries in log annotations, which files were deduped most
6. **Pre-filter rates** — count of SKIPPED entries by reason (short-continuation, machine-prompt, url-only)
7. **Error rate** — any ERROR entries in `$CLAUDE_CONFIG_DIR/memory-error.log`

### Step 4: Qualitative Sampling

Sample from the filtered log entries:

**Routed entries (10-15 samples across the period):**
- For each, read the PROMPT and ROUTING lines
- Grade routing as: **correct**, **over-broad** (loaded unnecessary files), or **wrong** (loaded clearly irrelevant files)
- Note any patterns in over-broad or wrong routing

**NONE entries with personal signals (5-10 samples):**
- Search NONE-routed entries for personal keywords: Alex, Sam, frustrated, worried, stressed, moving, relocating, visa, taxes, job search, budget, savings
- Grade each as: **correct NONE** (truly no memory needed) or **false negative** (should have loaded a file)
- This directly measures whether the personal-context routing fix is working

### Step 5: Delta Comparison

Compare current metrics against `baseline_metrics` from the watermark. Compute deltas for:

| Metric | Baseline | Current | Delta |
|--------|----------|---------|-------|
| NONE rate % | from watermark | computed | +/- |
| Routed rate % | from watermark | computed | +/- |
| EVAL:true rate % | from watermark | computed | +/- |
| False negatives (estimated) | from watermark | from sampling | +/- |
| Max retrieval bytes | from watermark | computed | +/- |
| Never-loaded files | from watermark | computed | list diff |

Flag any metric that moved in the wrong direction (e.g., false negatives increased, max retrieval exceeded the 15K cap).

### Step 6: Report

Output a structured report to the conversation (not a file, unless the user asks):

```
## Memory Retrieval Analysis Report
**Period:** YYYY-MM-DD to YYYY-MM-DD | **Events:** N | **Sessions:** N

### Metrics vs Baseline
[delta comparison table from Step 5]

### Top Findings
- [numbered list of key observations, improvements, and remaining issues]

### Routing Quality (Sampled)
- Correct: N/M (X%)
- Over-broad: N/M (X%)
- Wrong: N/M (X%)

### False Negative Check
- Checked N NONE entries with personal keywords
- False negatives found: N [list if any]

### Dedup Effectiveness
- [dedup stats if available]

### Recommendations
- [concrete, actionable items — reference specific files/lines if proposing code changes]
```

### Step 7: Update Watermark

Write updated `$CLAUDE_CONFIG_DIR/context-router-watermark.json`:
- Set `last_analysis` to current UTC timestamp
- Set `baseline_metrics` to current analysis metrics
- **Preserve** `deployed_at` and `deployed_commit` from original watermark (these are historical facts about the last code deployment, not analysis metadata)
- Update `notes` with a one-line summary of this analysis

## Guidelines

- **Context protection:** Always delegate log parsing to an agent. Logs can be 100K+ — never load them into the main conversation.
- **Aggregates only:** The report should contain aggregated metrics and selected examples, never raw log dumps.
- **Actionable recommendations:** If recommending changes, reference specific lines in `$CLAUDE_CONFIG_DIR/hooks/context-router.py` or entries in `$CLAUDE_CONFIG_DIR/memory/memory-catalog.json`.
- **Honest grading:** Don't inflate routing quality grades. If a routing decision is questionable, call it out. The point is to find problems.
- **Watermark discipline:** Always read watermark before analysis, always update after. This is the mechanism that prevents stale data from polluting future runs.
