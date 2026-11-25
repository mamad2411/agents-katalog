---
name: call-transcript-scan
description: Analyze call transcripts for product feedback using speaker-aware parsing. Use when the user asks to scan call transcripts, analyze customer/merchant calls, or run a feedback scan for a topic.
allowed-tools: mcp__snowflake__run_snowflake_query, mcp__snowflake__describe_object, mcp__snowflake__list_objects, Read, Write, Edit, Glob, Grep
---

# Call Transcript Feedback Scan

Analyze sales/support call transcripts for product-specific customer feedback. Uses a proximity + speaker-aware parsing methodology to isolate what **customers** (not reps) actually say about a product within relevant conversation context.

**Before starting:** Read `gotchas.md` and `runs.log` in this skill folder. Apply known failure patterns.

## Configuration

Before first use, configure the data source in `sql-templates.md`:
- Replace `[YOUR_TRANSCRIPT_TABLE]` with your actual transcript table
- Map your table's columns to the expected fields (transcript, caller, date, account, IDs)
- Add any product-specific signal patterns to `signal-patterns.md`

## Parameters

Collect from the user:

| Parameter | Required | Example |
|-----------|----------|---------|
| `topic` | Yes | "onboarding flow" |
| `keywords` | Yes | "onboard, setup, getting started" |
| `start_date` | Yes | "2026-03-01" |
| `end_date` | Yes | "2026-03-26" |
| `cohort_filter` | No | `PRODUCT_TYPE = 'premium'` |

## Execution Flow

### Phase 1 — Identify Relevant Calls

Run the identification query from `sql-templates.md` (Query 1). Count total calls, calls with transcripts, and distinct accounts matching the topic keywords + date range + cohort filter.

Present the counts to the user before proceeding. If the dataset is very large (>5,000 calls), consider narrowing the date range or adding a cohort filter.

### Phase 2 — Speaker-Aware Signal Detection

This is the core methodology. Run the signal detection query from `sql-templates.md` (Query 2).

**How it works:**
1. Split each transcript into speaker turns using the speaker label pattern (e.g., `Name (H:MM:SS):`)
2. Tag turns that mention any topic keyword
3. For each topic-mentioning turn, build a context window: same turn + next 3 turns
4. Within the context window, identify customer speech (speaker name ≠ CALLER/rep)
5. Apply signal patterns from `signal-patterns.md` to customer speech only
6. Deduplicate: one signal per call per signal type

**Output:** Signal counts per type, total calls with any signal, total calls with no signal.

### Phase 3 — Breakdowns

**Co-occurring signals (Query 3):** Count calls with multiple signal types. Report the top pairs.

**Tenure/cohort breakdown (Query 4, optional):** If the user specifies a tenure/activity table, cross-reference call accounts with product activity data. Break down signals by tenure buckets.

### Phase 4 — Qualitative Sample Pull

For each signal type with >0 calls, pull **5 sample transcripts** (Query 5).

For each sample:
1. Parse the transcript — identify speaker turns around the topic mention
2. Locate the customer speech that triggered the signal
3. Extract 1-3 real customer quotes with enough context
4. Note tenure bucket if available

**Context management:** Process one signal type at a time. Read 5 transcripts per batch.

### Phase 5 — Synthesis & Report

Write the output report to: `reference-docs/feedback/call-scan-{topic-slug}-{YYYY-MM-DD}.md`

Report sections:
1. **Methodology** — topic, keywords, date range, cohort, sample size, data source, coverage caveats
2. **Dataset Summary** — total calls, with transcripts, with customer speech in context, with signals, no signal
3. **Signal Breakdown** — rank, signal, calls, %, accounts (table)
4. **Co-Occurring Signals** — top pairs with counts
5. **Tenure Breakdown** — tenure bucket × signal type (if applicable)
6. **Qualitative Deep Dive** — real customer quotes per signal category
7. **Trend Comparison** — vs. previous run if one exists
8. **Implications** — synthesis of what the data means; actionable takeaways
9. **Data Quality Notes** — known limitations, methodology caveats, coverage gaps

### Phase 6 — Post-Run

1. Append to `runs.log`
2. If new failure patterns discovered, add to `gotchas.md` immediately.

## Important Notes

- **Coverage caveat.** Always note what the transcript data covers and doesn't cover. Not all customer conversations are recorded.
- **Conservative methodology.** Signal rates are lower bounds. The proximity + speaker-aware approach misses indirect objections. This is by design — higher confidence per detected signal.
- **Not a survey.** This is qualitative analysis of calls, not a statistically representative survey.
- **NEVER use AI-generated summaries.** Summaries conflate customer and rep speech. Always use the full transcript with speaker-aware parsing.
