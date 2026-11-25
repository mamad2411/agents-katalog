---
name: sap-review
description: Use when the user wants to review their Claude Code usage, analyze agent effectiveness, or get a periodic digest of how sessions are going. Queries SAP analytics data, scores sessions, and produces actionable insights.
---

# SAP Review — Agent Effectiveness Analysis

## Overview

Analyze Claude Code usage by querying SAP's session tracking database. Produce a structured digest that scores session effectiveness, identifies workflow patterns, and recommends improvements.

**This is an analysis skill, not a feature-building skill.** You query data, interpret it, and report findings.

## When to Use

- User asks to review their agent usage, session effectiveness, or workflow patterns
- Periodic check-in (weekly, after a sprint, after completing a plan)
- User wants to understand token spend relative to outcomes
- User asks "how am I doing?" or "how are my sessions going?"

## Prerequisites

SAP must be installed and recording hook events. Verify with:
```bash
sap status --json
```

If this fails, SAP isn't configured. Help the user set it up before proceeding.

## Phase 1: Ensure Data Is Fresh

Ingest any un-parsed transcripts before analyzing. This populates the `turns` and `tool_calls` tables from JSONL transcript files.

```bash
sap ingest --since 14d --json
```

Use `--force` only if the user suspects data is stale. Otherwise, already-ingested sessions are skipped automatically.

## Phase 2: Collect Data

Run these commands. Use `--json` for all of them so you get structured data to analyze. Adjust `--since` to match the review period (default: 7d for weekly).

**Run in parallel — these are independent:**

```bash
sap analytics summary --since 7d --json
sap analytics sessions --since 7d --json
sap analytics tools --since 7d --json
sap analytics patterns --since 7d --json
```

**For period comparison** (this week vs. last week), use `sap query` with raw SQL since `--since` only supports "since N ago", not date ranges:

```sql
-- This week's session stats (last 7 days)
SELECT
  COUNT(*) as sessions,
  COALESCE(SUM(t.input_tokens + t.output_tokens), 0) as total_tokens,
  COALESCE(AVG(t.input_tokens + t.output_tokens), 0) as avg_tokens_per_turn,
  COUNT(DISTINCT s.session_id) as sessions_with_turns
FROM sessions s
LEFT JOIN turns t ON t.session_id = s.session_id
WHERE s.started_at > (strftime('%s', 'now') - 7*86400) * 1000

-- Last week's session stats (7-14 days ago)
SELECT
  COUNT(*) as sessions,
  COALESCE(SUM(t.input_tokens + t.output_tokens), 0) as total_tokens,
  COALESCE(AVG(t.input_tokens + t.output_tokens), 0) as avg_tokens_per_turn,
  COUNT(DISTINCT s.session_id) as sessions_with_turns
FROM sessions s
LEFT JOIN turns t ON t.session_id = s.session_id
WHERE s.started_at > (strftime('%s', 'now') - 14*86400) * 1000
  AND s.started_at <= (strftime('%s', 'now') - 7*86400) * 1000
```

**For trellis plan progress** (if trellis is available):

Use `trellis status` (MCP tool or CLI) to see what plans moved during the review period. Cross-reference plan completion dates with session timestamps.

## Phase 3: Score and Interpret

### Session Effectiveness Scoring

Score each session from `sap analytics sessions` on these dimensions:

| Signal | Good | Concerning | Weight |
|--------|------|------------|--------|
| **Outcome: committed** | `true` | `false` | High |
| **Outcome: tests_passed** | `true` | `false` or `null` | Medium |
| **Error rate** | < 10% | > 20% | Medium |
| **Token efficiency** | Below 2x period average | Above 3x period average | Medium |
| **Session focus** | Single workspace | (all sessions are single-workspace in SAP) | — |

Classify each session:
- **Productive** — committed AND (tests passed or N/A) AND error rate < 15%
- **Mixed** — some positive signals but gaps (e.g., committed but high error rate, or clean execution but no commit)
- **Spinning** — no commit, high error rate, or token outlier with no outcome

### Aggregate Metrics

Calculate and report:
- **Productivity rate:** % of sessions classified as productive
- **Commit rate:** % of sessions that produced commits
- **Test discipline:** % of sessions where tests were run and passed
- **Error trend:** average error rate this period vs. last
- **Token efficiency:** average tokens per session, trend vs. last period
- **Anti-pattern frequency:** edit-retry and bash-error counts, trend

### Tool Pattern Analysis

From `sap analytics tools`, look for:
- **High-failure tools:** tools with success_rate < 80% — what's going wrong?
- **Tool sequences:** common 2-tool sequences that correlate with productive vs. spinning sessions
- **Edit tool health:** edit-retry anti-pattern frequency (high = prompts are unclear or code understanding is weak)
- **Bash error frequency:** bash-error anti-pattern (high = commands being guessed rather than verified)

## Phase 4: Report

Present findings in this structure:

### Digest Format

```
## Weekly SAP Review — [date range]

### Summary
- X sessions across Y workspaces
- Z% productive, W% mixed, V% spinning
- Total tokens: N (trend: +/-% vs last period)

### Effectiveness
[Per-workspace breakdown if multiple workspaces]
- Commit rate: X%
- Test pass rate: X%
- Average error rate: X%
- Token efficiency: X tokens/session (trend)

### What's Working
[Patterns from productive sessions — tools, sequences, session lengths that correlate with good outcomes]

### What to Improve
[Anti-patterns, high-error tools, spinning sessions — specific, actionable]

### Recommendations
[2-3 concrete suggestions based on the data]
```

### Interpretation Guidelines

- **Don't over-index on single sessions.** One spinning session in a week of productive ones is normal.
- **Look for trends, not absolutes.** Error rate going down matters more than the current number.
- **Context matters.** A session with no commit but lots of Read/Grep calls might be research, not spinning.
- **Token outliers need investigation.** Check what workspace/task — complex tasks legitimately use more tokens.
- **Anti-patterns are signals, not verdicts.** A few edit-retries happen; a pattern of them means something.

## Useful Ad-Hoc Queries

If the standard analytics don't answer a question, use `sap query` with these templates:

```sql
-- Sessions by day with outcome
SELECT
  date(started_at/1000, 'unixepoch', 'localtime') as day,
  COUNT(*) as sessions,
  SUM(CASE WHEN state = 'stopped' THEN 1 ELSE 0 END) as completed
FROM sessions
WHERE started_at > (strftime('%s', 'now') - 7*86400) * 1000
GROUP BY day ORDER BY day

-- Most expensive sessions (by total tokens)
SELECT
  s.session_id,
  s.workspace,
  SUM(t.input_tokens + t.output_tokens) as total_tokens,
  COUNT(t.id) as turns,
  date(s.started_at/1000, 'unixepoch', 'localtime') as day
FROM sessions s
JOIN turns t ON t.session_id = s.session_id
WHERE s.started_at > (strftime('%s', 'now') - 7*86400) * 1000
GROUP BY s.session_id
ORDER BY total_tokens DESC
LIMIT 5

-- Tool failure details for a specific tool
SELECT tool_name, error_message, COUNT(*) as occurrences
FROM tool_calls
WHERE success = 0
  AND created_at > (strftime('%s', 'now') - 7*86400) * 1000
GROUP BY tool_name, error_message
ORDER BY occurrences DESC
LIMIT 20

-- Workspace activity heatmap (sessions per workspace per day)
SELECT
  s.workspace,
  date(s.started_at/1000, 'unixepoch', 'localtime') as day,
  COUNT(*) as sessions
FROM sessions s
WHERE s.started_at > (strftime('%s', 'now') - 7*86400) * 1000
GROUP BY s.workspace, day
ORDER BY s.workspace, day
```

## SAP Database Schema Reference

Five tables — all timestamps are Unix milliseconds:

- **sessions** — `session_id, workspace, cwd, transcript_path, state, started_at, ended_at, last_event_at, last_tool, last_tool_detail, ingested_at`
- **events** — `id, session_id, event_type, data (JSON), created_at`
- **turns** — `id, session_id, turn_number, prompt_text, input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, model, tool_call_count, started_at, ended_at, duration_ms`
- **tool_calls** — `id, session_id, turn_id, tool_use_id, tool_name, tool_input_summary, success (0/1/null), error_message, created_at`
- **workspaces** — `cwd, repo_name, branch, workspace, resolved_at`

Session states: `active`, `idle`, `attention`, `stopped`

## Key Principles

- **Data over intuition.** Query first, interpret second.
- **Trends over snapshots.** One bad session means nothing; a pattern of them means everything.
- **Actionable over comprehensive.** 2-3 specific recommendations beat a wall of numbers.
- **No judgment.** This is about tuning workflow, not grading performance.
