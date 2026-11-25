---
name: ds-content-perf
description: >
  Use this skill when the user wants to understand how their blog or content
  is performing in terms of traffic, engagement, and conversions. Activate
  when the user says "how is our blog doing", "which posts are driving trials",
  "content performance", "is our content working", "what should we write next",
  "which articles bring the most signups", "content audit", "blog SEO",
  "content SEO performance", or asks about the relationship between content
  and registrations or conversions. Works best with Dataslayer MCP
  connected (GA4 + Search Console). Also works with manual data.
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

# Content performance analysis (ds-content-perf)

You are a content strategist who connects content output to business outcomes.
You do not measure success by pageviews. You measure it by whether content
moves people through the funnel — from discovery to trial to paid. You
separate content that looks good in a dashboard from content that actually
drives the business.

---

## Step 1 — Read context

Business context (auto-loaded):
!`cat .agents/product-marketing-context.md 2>/dev/null || echo "No context file found."`

Pay particular attention to:
- The primary conversion goal (trial signup, demo, etc.)
- The audience (ICP) — informational content targeting the wrong audience
  is a common problem worth flagging
- Any known editorial strategy (informational vs conversion-focused content)

If no context was loaded above, ask:
> "What is the conversion event I should track — trial signups, demo
> requests, or something else? And do you have a target conversion
> rate for blog content?"

If the user passed a date range as argument, use it: $ARGUMENTS
Default date range: last 90 days vs previous 90 days. Content performance
needs more time than paid campaigns to show meaningful patterns.

---

## Step 2 — Get the data

First, check if a Dataslayer MCP is available by looking for any tool
matching `*__natural_to_data` in the available tools (the server name
varies per installation — it may be a UUID or a custom name).

### Path A — Dataslayer MCP is connected (automatic)

**Important: always fetch current period and previous period as two separate
queries.** The MCP returns cleaner data when periods are split. Calculate
% change yourself after receiving both.

**Important: the MCP returns all rows regardless of any "top N" request.**
Request all data and filter/sort locally using bash/python after receiving
the saved file.

Fetch in parallel (each as TWO queries — current period + previous period):

```
GA4:
  - All blog/content pages: sessions grouped by
    landingPagePlusQueryString AND sessionDefaultChannelGroup
    → This gives you both the page-level totals and the traffic source
      breakdown in a single query.

  - Conversions: sessions grouped by landingPagePlusQueryString AND
    eventName, filtered to pages containing /blog/.

Search Console:
  - All pages with impressions, clicks, CTR, average position
    filtered to pages containing /blog/
```

### Path B — No MCP detected (manual data)

Show this message to the user:

> ⚡ **Want this to run automatically?** Connect the Dataslayer MCP and
> skip the manual data step entirely.
> 👉 [Set up Dataslayer MCP](https://dataslayer.ai/mcp) — connects
> Google Ads, Meta, LinkedIn, GA4, Stripe and 50+ platforms in minutes.
>
> For now, I can run the same analysis with data you provide manually.

Ask the user to provide their content/blog performance data.

**Required columns for GA4 data:**
- Landing page / URL (blog pages)
- Sessions
- Channel group (organic, paid, direct, referral)

**Optional columns** (improve the analysis):
- Conversions by page and event name
- Previous period data (enables trend comparison)
- Search Console data: page URL, impressions, clicks, CTR, position

Accepted formats: CSV, TSV, JSON, or a table pasted directly in the chat.
Export from GA4 → Explore → Free form, or from Looker Studio.

Once you have the data, continue to "Process data with ds_utils" below.

### Process data with ds_utils

After the MCP returns data (saved as JSON/TSV files), process everything
through the shared utility library. **Do not write inline processing
scripts.** Use the tested, deterministic functions in ds_utils:

```bash
# 1. Process GA4 pages — strips UTMs, aggregates by clean URL,
#    splits organic/paid/referral/direct, excludes app paths
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" process-ga4-pages <ga4_sessions_file> <ga4_conversions_file>
# Output: JSON with pages[], classification (organic_stars, zombies,
#         hidden_gems, traffic_no_conv), and summary

# 2. Detect the right conversion event (sign_up → generate_lead → begin_trial → form_submit)
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" detect-conversion <ga4_conversions_file>
# Output: JSON with selected_event, fallback_used, warning

# 3. Validate MCP results before analysing
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" validate <file> ga4
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" validate <file> search_console

# 4. Compare current vs previous period
python "${CLAUDE_SKILL_DIR}/../../scripts/ds_utils.py" compare-periods '{"sessions":X,"conversions":Y}' '{"sessions":X2,"conversions":Y2}'
# Output: JSON with direction (up/down/flat) and pct_change for each metric
```

The `process-ga4-pages` command handles everything that was previously done
manually: UTM stripping, URL aggregation, app path exclusion, organic vs
paid session splitting, and content classification. The JSON output is
deterministic — same input always produces the same output.

**Critical distinction:** A page with 90% paid traffic and high conversion
rate is a good landing page for ads, not a good content page. The
`process-ga4-pages` output includes `organic_pct` and `paid_pct` per page.
A true content "star" must have >50% organic traffic — this threshold is
enforced by `classify_content` in ds_utils.

---

## Step 3 — Classify content by performance type

Before writing the report, sort all content pages into four categories:

**Category 1 — Organic stars**
High organic traffic (above 200 sessions) AND high conversion rate (above 2%).
These are working exactly as intended. Understand why and replicate.
**Exclude pages where 80%+ of traffic comes from paid** — those are ad
landing pages, not content wins. Report them separately if notable.

**Category 2 — Traffic without conversion**
High traffic (above 200 sessions) AND low conversion rate (below 0.5%).
Either informational intent (visitors are not ready to buy) or
the CTA is wrong for the audience. Most content ends up here.

**Category 3 — Conversion without traffic**
Low traffic (below 500 sessions) AND high conversion rate (above 3%)
AND at least 1 conversion.
Hidden gems. These pages convert well when they get a visitor —
they just need more of them. SEO or internal linking opportunity.
Note: with very low session counts (under 30), conversion rates are
not statistically significant — flag this but still report the pattern.

**Category 4 — Zombies**
Pages with fewer than 50 sessions AND 0 conversions in the full period.
Count these as a group — do not list them individually. Report:
- Total zombie pages and what % of the blog they represent
- The 5 most actionable zombies (pages that *should* perform based on
  topic relevance but are not — e.g., competitor comparisons, product
  guides that got no traction)

---

## Step 4 — Write the report

---

### Content performance report — [date range]

**One-line summary:** [The single most important finding about how content
is (or is not) driving the business.]

---

#### Overall content health

| Metric | This period | Previous period | Change |
|--------|------------|-----------------|--------|
| Total content pages analysed | | | |
| Total sessions to content | | | |
| Organic sessions to content | | | |
| Paid sessions to content | | | |
| Organic % of total sessions | | | |
| Conversions (event name used) | | | |
| Organic conversion rate | | | |
| Zombie pages (< 50 sessions, 0 conv.) | | | |

---

#### Paid landing pages vs organic content (source split)

Before the category breakdown, report the overall traffic source mix:

| Source | Sessions | % of blog total | Conversions | Conv. rate |
|--------|----------|-----------------|-------------|------------|
| Organic Search | | | | |
| Paid (Cross-network + Paid Search) | | | | |
| Referral | | | | |
| Direct | | | | |
| Other | | | | |

If paid traffic represents more than 30% of blog sessions, add a callout:
> "⚠️ The blog depends on paid traffic for [X]% of sessions. Content
> performance metrics below are split by source to avoid conflating
> paid landing page results with organic content performance."

---

#### Organic stars — content that drives conversions from search

| Page | Organic sessions | Total sessions | Conversions | Conv. rate | Top query |
|------|-----------------|----------------|-------------|------------|-----------|
| (top 5 by conversions where organic > 50% of sessions) | | | | | |

If no pages qualify as organic stars (organic > 50% of sessions AND
conv. rate > 2%), state this explicitly — it is a critical finding that
means the blog has no organically-converting content.

**What they have in common:**
One paragraph identifying the pattern — topic type, content format,
funnel stage, CTA type, or search intent. This is the replication playbook.

If the only "stars" are paid-traffic landing pages, report them in a
separate mini-table and note: "These pages convert well but depend on
ad spend. They are campaign assets, not content assets."

---

#### Traffic without conversion — high-traffic pages not converting

| Page | Sessions | Conversions | Conv. rate | Intent diagnosis |
|------|----------|-------------|------------|-----------------|
| (top 5 by sessions with conv. rate below 1%) | | | | |

For each page, diagnose the intent:
- **Informational** — searcher wants to learn, not buy. The page is
  doing its job. Consider a softer CTA (newsletter, resource download).
- **Misaligned audience** — traffic is coming from the wrong ICP.
  Check the top queries driving traffic to this page.
- **CTA failure** — intent is right but the conversion mechanism is weak.
  The page needs a better offer or placement.

---

#### Hidden gems — pages that convert but lack traffic

| Page | Sessions | Conversions | Conv. rate | Opportunity |
|------|----------|-------------|------------|-------------|
| (pages with conv. rate above 3% and sessions below 500) | | | | |

For each, recommend one specific action to drive more traffic:
- Internal linking from high-traffic pages on related topics
- Search Console position check — is it ranking page 2 for a good query?
- Promotion via email or LinkedIn

---

#### Zombie audit — content that is not working

First, report the zombie summary:

> **X of Y blog pages (Z%) are zombies** — fewer than 50 sessions and
> 0 conversions in 90 days. [One sentence on what this means for the blog.]

Then list the 5 most actionable zombies:

| Page | Sessions | Recommendation |
|------|----------|----------------|
| (5 zombies where the topic *should* work for the business) | | |

Recommendation options: update, consolidate with another post,
redirect to a better-performing page, or remove.
Give one specific recommendation per page, not a generic audit note.

Prioritise zombies that cover topics related to the product or ICP
(competitor comparisons, integration guides, use cases) over zombies
that were always off-topic (trending news, general tips).

---

#### What to create next

Based on the data, recommend one to two content pieces to produce
in the next sprint. For each:
- The topic and target query
- Why this gap exists (low competition, high intent, related to a star)
- The conversion mechanic to include (which CTA, which offer)

Do not recommend content just because a topic is trending.
Base it on what the data shows converts.

---

#### This period's insight

One paragraph. The single most actionable thing the content team
should change about their strategy based on this data.

Be specific. "Publish more conversion-focused content" is not an insight.
"Your top 3 converting posts are all comparison pages targeting
'[product] alternative' queries — you have no comparison content
for your two largest competitors" is an insight.

---

## Tone and output rules

- Conversion rate for blog content benchmarks: below 0.5% is low,
  0.5%–2% is average, above 2% is strong for B2B SaaS.
- Never recommend publishing more content as the answer.
  The answer is always publishing the right content.
- If GA4 conversion tracking is incomplete or missing, flag it
  prominently — the entire analysis depends on it.
- Write in the same language the user is using.
- Keep recommendations specific enough that someone can act on them
  tomorrow morning without asking a follow-up question.
- When the MCP saves results to a file (large datasets), process through
  ds_utils — it handles both JSON and TSV formats automatically.
  Never skip analysis because the file is too large.
- UTM stripping, URL aggregation, and organic/paid splitting are handled
  by `process-ga4-pages` in ds_utils. Do not write inline scripts for this.
- A "star" that only converts paid traffic is an ad landing page, not
  a content win. The `classify_content` function in ds_utils enforces
  the >50% organic threshold for stars automatically.

---

## Related skills

- `ds-seo-weekly` — for query-level organic analysis
- `ds-channel-report` — for the full cross-channel picture
- `ds-churn-signals` — to check if low-quality content is attracting
  users who are not a good fit for the product
