---
name: deep-insights
description: Retro analysis of Claude Code sessions over arbitrary windows (bypasses /insights 200-session cap via chunking). TRIGGER when user says "/deep-insights", "deep insights", "monthly retro", "quarterly retro", or needs insights over a window the built-in command can't reach.
version: 1.0.0
allowed-tools: Bash, Read, Write, Glob, Grep, Agent, AskUserQuestion
---

# Deep Insights

Reusable `/insights`-style analysis that runs against a user-specified window of any size. The built-in `/insights` hard-caps at 200 newly-parsed sessions per run — for a heavy user, that reaches back only a week or so. This skill chunks arbitrary windows and dispatches the same four-section analysis.

## Prerequisites

- The `agents` plugin from this marketplace (ships the `worker` and `thinker` subagent types this skill dispatches). Install it alongside this one.
- Nothing else — the session scanner and prompt templates are bundled with this skill.

## When to use

- User explicitly says `/deep-insights`, "run deep insights", "analyze my sessions from <date> to <date>".
- User asks for a retro covering more than ~1 week (monthly, quarterly).
- User asks to re-run `/insights` against a specific window, not the default.
- `/insights` has already been run for a recent window and the user wants an older, non-overlapping companion.

## Inputs

Parse `$ARGUMENTS`:

- `--start YYYY-MM-DD` (required)
- `--end YYYY-MM-DD` (default: today)
- `--sample-top N` (default: 25) — number of top discussion-density sessions to deep-read
- `--out-path <path>` (default: `~/deep-insights-<start>-<end>.md`)
- `--force-overlap` — analyze sessions already covered by `/insights` cache (default: skip)

If `--start` is missing, ask for it before proceeding.

## Pipeline

### 1. Filter sessions by window

```bash
find ~/.claude/projects -name "*.jsonl" -newermt "<start>" ! -newermt "<end>" > /tmp/deep-insights-sessions.txt
```

Record count. If >1500 sessions, warn the user and block pending confirmation via AskUserQuestion: "Proceed with {N} sessions, or narrow the window?" Do not silently proceed with oversized input.

### 2. Rank by discussion density

```bash
# Compute span from start/end
SPAN=$(( ( $(date -j -f "%Y-%m-%d" "<end>" +%s) - $(date -j -f "%Y-%m-%d" "<start>" +%s) ) / 86400 + 1 ))
python3 "${CLAUDE_SKILL_DIR}/scripts/session-scanner" --days $SPAN --top 200 > /tmp/deep-insights-ranked.txt
```

Filter the ranked output to sessions within the window (scanner may return sessions outside if span is loose).

### 3. Load baseline (dedup)

Read the current inventory so suggestions don't duplicate existing work:

```bash
ls ~/.claude/skills/ > /tmp/di-skills.txt
ls ~/.claude/commands/ > /tmp/di-commands.txt
ls ~/.claude/agents/ > /tmp/di-agents.txt
ls ~/.claude/rules/ > /tmp/di-rules.txt
cat ~/.claude/CLAUDE.md > /tmp/di-claude-md.txt
```

If `~/.claude/usage-data/session-meta/` exists, read any prior `/insights` reports in the window (unless `--force-overlap`). Sessions already covered get excluded from the sample set.

### 4. Sample top N sessions

For each of the top `--sample-top` (default 25):

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/session-scanner" --transcript <session-id> --outfile /tmp/di-cache/<id>.md
```

Write to `~/.claude/usage-data/deep-insights-cache/<start>-<end>/` so re-runs don't re-extract.

### 5. Facet extraction (parallel, sonnet workers)

Read `${CLAUDE_SKILL_DIR}/prompts/facet_extraction.txt` yourself first — dispatched workers run with their own cwd and can't resolve a bare `prompts/...` path, so never ask a worker to read it. Inline its full contents into each worker's dispatch prompt.

Dispatch `worker` agents in parallel batches of 5. Each worker processes one session:

**Prompt template (per worker)**: the inlined `facet_extraction.txt` content, followed by the session transcript path. Instruct the worker: return JSON matching the template's schema — do not summarize or editorialize, extraction only, JSON only (no prose preamble, no markdown fences), ≤150 lines, ≤120 chars per line.

Collect all JSON to `/tmp/di-cache/facets.jsonl`.

**Resilience**: any worker failing retries up to 2x (60s then 120s timeout tiers). If a worker still fails after 2 retries, log it and continue aggregation without it — don't let one bad session block the whole run.

### 6. Aggregate

Inline Python (via Bash) to roll up:
- Goal category counts (total sessions per category)
- Tool use distribution (top 20)
- Friction cluster counts (top 10 patterns)
- Satisfaction signal ratios (fully-achieved vs partial vs not)
- Cross-session patterns (recurring phrasing, repeated tasks)

Write to `/tmp/di-cache/aggregate.json`.

### 7. Analyze (parallel agent dispatch)

Read all 6 prompt files below yourself first (`${CLAUDE_SKILL_DIR}/prompts/<file>`) — same reason as step 5, dispatched agents can't resolve the bare path. Dispatch 6 sub-agents **in a single message** (one tool call per agent). Each gets:
- The aggregate JSON
- The baseline dedup lists
- The inlined contents of one of the 6 prompt files below

| Agent | Prompt file | Output target |
|---|---|---|
| `worker` | `project_areas.txt` | 3–6 project clusters |
| `worker` | `interaction_style.txt` | narrative (2 paragraphs) |
| `worker` | `whats_working.txt` | 3 impressive workflows |
| `worker` | `friction_points.txt` | 3 friction categories |
| `thinker` | `future_opportunities.txt` | 3 horizon workflows |
| `worker` | `memorable_moment.txt` | one-line headline |

Each prompt MUST include the dedup instruction:
```
EXCLUDE suggestions that already exist in <baseline lists>. Only propose NEW artifacts.
```

### 8. Rollup + render

Main session synthesizes an "at a glance" summary using `${CLAUDE_SKILL_DIR}/prompts/at_a_glance.txt` with all 6 outputs in context. Render the final markdown:

```markdown
---
date: <today>
type: deep-insights
window: <start> → <end>
---

# Deep Insights — <start> → <end>

## At a glance

<4-part summary: what's working / what's hindering / quick wins / ambitious workflows>

## Project areas

<from project_areas agent>

## Interaction style

<from interaction_style agent>

## What's working

<from whats_working agent>

## Friction

<from friction_points agent>

## Suggestions (new artifacts only)

<synthesized from friction + working; cross-check against baseline>

## On the horizon

<from future_opportunities agent>

## Fun ending

<from memorable_moment agent>

---

## Coverage

- Sessions in window: <N>
- Sampled in depth: <top_N>
- Dedup: excluded <K> suggestions already present in rules/skills/commands
```

### 9. Write output

Use native `Write` tool to `--out-path`.

### 10. Cleanup

Leave the cache at `~/.claude/usage-data/deep-insights-cache/<start>-<end>/` for future re-runs. Remove `/tmp/di-*` temp files.

## Cost model

- Facet extraction: 25 sessions × ~2k tokens = 50k input
- Aggregate analysis: 6 parallel agent calls × ~3k tokens = 18k input
- Rollup: 1 synthesis call with all sections in context ≈ 8k input
- Total: ~75k input, ~15k output
- On subscription: no per-call cost. On API: ~$0.50 at Sonnet pricing for extraction + Opus for horizon.

## Prompt pack

Bundled at `prompts/`, reverse-engineered from Claude Code's own built-in `/insights` prompts:

- `facet_extraction.txt` — per-session extraction schema
- `project_areas.txt` — aggregate → project clusters
- `interaction_style.txt` — aggregate → narrative
- `whats_working.txt` — aggregate → workflows
- `friction_points.txt` — aggregate → friction categories
- `future_opportunities.txt` — aggregate → horizon workflows
- `memorable_moment.txt` — aggregate → headline
- `at_a_glance.txt` — all sections → 4-part summary

Also bundled but not yet wired into the pipeline above (available for extension): `summarize_chunk.txt` (chunk summarization for very long transcripts), `model_behavior_improvements.txt` and `product_improvements.txt` (additional analysis angles mirroring other `/insights` sections).

## Resilience

All sub-agent dispatches:
- 60s / 120s tiered timeouts
- Up to 2 retries
- Partial results on failure: annotate `[AGENT X FAILED — continuing]` in the final report and skip that section cleanly rather than aborting

## What this skill does NOT do

- Does not emit HTML (markdown-only for v1).
- Does not auto-invoke on a schedule — user-triggered only. If you want monthly retro automation, wrap in `/loop 30d /deep-insights --start ...`.
- Does not share state with `/insights` cache — it writes to its own cache dir. Dedup reads `/insights` output if present but doesn't update it.
- Does not replace `/insights` for short recent windows — the built-in is faster when it covers your window.

## Integration

- Invokes: `worker` agents (sonnet, 5 per batch), `thinker` agent (opus, for horizon section) — both from this marketplace's `agents` plugin.
- Reads: bundled `scripts/session-scanner`, bundled `prompts/`.
- Writes: report to `--out-path`, cache to `~/.claude/usage-data/deep-insights-cache/`.
- Related: built-in `/insights` (newer-window).
