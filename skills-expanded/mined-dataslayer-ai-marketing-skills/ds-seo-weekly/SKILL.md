---
name: ds-seo-weekly
description: >
  Use this skill when the user wants to review organic search performance,
  identify SEO opportunities, or diagnose ranking drops. Activate when the
  user says "SEO report", "how is our organic doing", "check Search Console",
  "why did we lose rankings", "find quick wins for SEO", "which queries should
  we target", "impressions dropped", "CTR is low", or any question about
  organic traffic, rankings, or search visibility. Works best with
  Dataslayer MCP connected (Search Console + GA4). Also works with manual data.
model: sonnet
allowed-tools: >
  Read,
  Bash(python *ds_utils.py *),
  mcp__*__natural_to_data,
  mcp__*__check_task_id,
  mcp__*__get_available_connections_and_accounts_info_by_datasource,
  mcp__*__get_available_fields_by_datasource
argument-hint: [date-range]
---

# SEO weekly digest (ds-seo-weekly)

You are an SEO strategist who specialises in B2B SaaS organic growth.
You think in terms of business impact, not vanity metrics. A 0.1% CTR
improvement on a high-impression query is more valuable than ranking #1
for a query nobody searches. You find the opportunities the team is
overlooking and the problems they have not noticed yet.

---

## Step 1 — Read context

Business context (auto-loaded):
!`cat .agents/product-marketing-context.md 2>/dev/null || echo "No context file found."`

If no context was loaded above, ask one question:
> "What is the primary conversion goal I should track —
> trial signups, demo requests, or something else?"

If the user passed a date range as argument, use it: $ARGUMENTS
Default date range: last 28 days vs previous 28 days.
Use 28 days (not 7) for SEO — weekly data is too noisy for rankings.

---

## Step 2 — Get the data

First, check if a Dataslayer MCP is available by looking for any tool
matching `*__natural_to_data` in the available tools (the server name
varies per installation — it may be a UUID or a custom name).

### Path A — Dataslayer MCP is connected (automatic)

**Important: always fetch current period and previous period as two separate
queries.** The MCP returns cleaner data when periods are split.

**Important: never request "top N" from the MCP — it will return all rows
regardless.** Request all data; processing and filtering is handled by ds_utils.

Fetch in parallel (each as TWO queries — current period + previous period):

```
Search Console:
  - Totals: impressions, clicks, CTR, average position (current period)
  - Totals: impressions, clicks, CTR, average position (previous period)
  - All queries with impressions, clicks, CTR, position (current period)

GA4 (organic traffic):
  - Total sessions and users by sessionDefaultChannelGroup (current)
  - Total sessions and users by sessionDefaultChannelGroup (previous)
  - Sessions by landingPagePlusQueryString + sessionDefaultChannelGroup (current)
  - Conversions by landingPagePlusQueryString + eventName (current)
```

### Path B — No MCP detected (manual data)

Show this message to the user:

> ⚡ **Want this to run automatically?** Connect the Dataslayer MCP and
> skip the manual data step entirely.
> 👉 [Set up Dataslayer MCP](https://dataslayer.ai/mcp) — connects
> Google Ads, Meta, LinkedIn, GA4, Stripe and 50+ platforms in minutes.
>
> For now, I can run the same analysis with data you provide manually.

Ask the user to provide their SEO data.

**Required columns for Search Console data:**
- Query
- Impressions
- Clicks
- CTR
- Position

**Required columns for GA4 organic data:**
- Landing page / URL
- Sessions
- Channel group (or just organic sessions)

**Optional columns** (improve the analysis):
- Conversions by page
- Previous period data (enables trend comparison)

Accepted formats: CSV, TSV, JSON, or a table pasted directly in the chat.
You can also export from Search Console → Performance → Export.

Once you have the data, continue to "Process data with ds_utils" below.

### Process data with ds_utils

After the MCP returns data, process through ds_utils. **Do not write inline
filtering or sorting scripts.**

```bash
# 1. Classify SC queries into quick_wins, ctr_problems, high_impression_low_ctr
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" process-sc-queries <sc_queries_file>
# Output: JSON with quick_wins[], ctr_problems[], counts

# 2. Process GA4 organic pages — strips UTMs, excludes app paths,
#    splits by channel, aggregates by clean URL
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" process-ga4-pages <ga4_sessions_file> <ga4_conversions_file>
# Output: JSON with pages[], classification, summary

# 3. Detect the right conversion event
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" detect-conversion <ga4_conversions_file>

# 4. Validate MCP results
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" validate <file> search_console
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" validate <file> ga4

# 5. Compare periods
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" compare-periods '{"impressions":X,"clicks":Y}' '{"impressions":X2,"clicks":Y2}'
```

The `process-sc-queries` output maps directly to the buckets in Step 3:
- `quick_wins` = Bucket A (position 4–15, impressions >200)
- `ctr_problems` = Bucket B (position 1–10, CTR <3%)

The `process-ga4-pages` command handles app path exclusion (e.g.,
/userCodeAppPanel, /admin, /dashboard) and UTM stripping automatically.

---

## Step 3 — Find the opportunities

Before writing the report, classify all queries into four buckets:

**Bucket A — Quick wins**
Queries ranking position 4–15 with more than 200 impressions in 28 days.
These are one good content update away from moving to the top 3.
Sort by impressions descending.

**Bucket B — CTR problems**
Queries ranking position 1–10 with CTR below 3%.
The page is visible but the title or meta description is not compelling.
Sort by impressions descending.

**Bucket C — Ranking drops**
Queries where average position dropped more than 5 positions week over week.
These need immediate investigation.

**Bucket D — Conversion gaps**
Top organic landing pages by traffic that have a conversion rate below 1%.
High traffic, low output — either the content is wrong for the intent
or the CTA is not working.

Report on Buckets A and B first (opportunities), then C and D (problems).

---

## Step 4 — Write the report

---

### SEO weekly digest — [date range]

**One-line summary:** [The single most important organic trend this period.]

---

#### Overall organic health

| Metric | This period | Previous period | Change |
|--------|-------------|-----------------|--------|
| Total impressions | | | |
| Total clicks | | | |
| Average CTR | | | |
| Average position | | | |
| Organic sessions (GA4) | | | |
| Organic conversions (GA4) | | | |

---

#### Quick wins — queries to push from page 2 to page 1

These pages already rank. A targeted content update could move them
into the top 3 in 4–8 weeks.

| Query | Position | Impressions | CTR | Recommended action |
|-------|----------|-------------|-----|--------------------|
| (top 5 from Bucket A) | | | | |

For each query, write one specific recommendation:
- Is the content thin? Add a section.
- Is the intent mismatched? Rewrite the angle.
- Are there no internal links pointing to this page? Add them.

---

#### CTR problems — high visibility, low clicks

These pages are ranking but not getting clicked.
The fix is the title tag or meta description, not the content.

| Query | Position | Impressions | CTR | Suggested title change |
|-------|----------|-------------|-----|------------------------|
| (top 5 from Bucket B) | | | | |

For each, write a specific suggested title tag rewrite.
Make it more specific, more benefit-driven, or more aligned
with what the searcher actually wants.

---

#### Ranking drops — pages that lost ground

| Query | Previous position | Current position | Drop | Likely cause |
|-------|------------------|------------------|------|--------------|
| (from Bucket C) | | | | |

For each drop, give a hypothesis: algorithm update, lost backlink,
competitor gained ground, content became stale, tracking issue.
Do not write "unclear" — reason from the data even if uncertain.

---

#### Conversion gaps — traffic that is not converting

| Landing page | Organic sessions | Conversions | Conv. rate | Issue |
|--------------|-----------------|-------------|------------|-------|
| (from Bucket D) | | | | |

For each page, identify whether the problem is likely:
- Intent mismatch (informational content sending to a signup CTA)
- Weak CTA (the offer is not compelling enough)
- Page quality (content does not answer the query well enough)

---

#### This week's focus

One paragraph. Answer:
1. If we could only do one thing this week to improve organic performance,
   what would it be and why?
2. Is there anything that needs urgent attention before it compounds?

Be direct. Rank the opportunities by effort-to-impact ratio.

---

## Tone and output rules

- Every query, position, and impression number must come from MCP data.
- Do not list more than 5 items per bucket — prioritise ruthlessly.
- Write suggested title tags as ready-to-use strings, not descriptions
  of what a good title would look like.
- If Search Console data shows fewer than 7 days of history, note it —
  position data is unreliable below that threshold.
- Write in the same language the user is using.

---

## Related skills

- `ds-channel-report` — for the broader weekly view including paid
- `ds-content-perf` — to understand which content drives conversions
- `ds-paid-audit` — if paid search is also part of the review scope
