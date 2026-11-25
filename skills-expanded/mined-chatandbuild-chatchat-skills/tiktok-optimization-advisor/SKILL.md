---
id: tiktok-optimization-advisor
name: tiktok-optimization-advisor
description: "Use this skill when a user wants to evaluate the performance of an active TikTok campaign and get prioritized recommendations for how to optimize it. This is a mid-flight evaluation tool for enterprise activators — it pulls live campaign data, assesses performance against KPI goals and vertical benchmarks, and produces an ordered list of optimization actions the activator (or the TikTok MCP) can execute immediately. Trigger phrases include: \"evaluate the campaign\", \"evaluate campaign performance\", \"optimize my campaign\", \"optimization recommendations\", \"why is my campaign underperforming\", \"how should I optimize\", \"what changes should I make\", \"mid-flight evaluation\", \"what's wrong with my campaign\", \"campaign health check\", \"TikTok optimization\", \"how do I improve performance\", \"campaign isn't hitting goal\", \"too expensive\", \"low CTR\", \"low delivery\", \"creative fatigue\", \"vertical benchmarks for TikTok\", or any request combining campaign performance review with recommended actions."
category: TikTok
version: "1.0.0"
author: "Innovid"
use_case: "Ads Management"
user-invokable: false
---

# TikTok Optimization Advisor

This skill evaluates an active TikTok campaign's mid-flight performance and produces a
prioritized list of optimization actions ordered by expected impact. It is built for
enterprise activation teams advising brand clients on what to change and why, right now.

The primary deliverable is an **actionable recommendation set** — not a narrative report.
Each recommendation is tagged as either MCP-executable (the TikTok MCP can implement it
directly) or manual (requires human action outside the API).

Setup diagnostics are not a standalone audit. They surface only when a structural issue
is the root cause of an observed performance problem.

---

## Step 1: Gather Context

### 1a. Ask the user these questions before pulling any data

Ask all of the following in a single message so the user can respond at once. Frame them
as a numbered list:

1. **Primary KPI goal** — What is the campaign's target metric and goal value?
   (e.g., "CPA: $22", "ROAS: 3.5x", "CTR: 1.0%", "CPM: $8", "CPI: $4")

2. **Vertical / Industry** — What industry is this campaign for?
   (CPG/FMCG | Retail/E-commerce | Entertainment/Media | Finance/Insurance |
   App/Mobile Gaming | Beauty/Personal Care | Automotive | QSR/Food & Beverage |
   Travel/Hospitality | Health & Wellness | B2B/Tech | Other)

3. **End date** — What is the planned campaign end date?
   (Attempt to pull start date from MCP; if end date is not stored in the campaign, ask here)

4. **Total budget** — What is the total campaign budget?
   (Pull from campaign-level MCP data if available; ask if using ad-group-level budgets only)

5. **Organic TikTok presence** — Does the client have an active TikTok account linked to
   this advertiser? (Yes / No / Unsure)

6. **Creative pipeline** — How many new creative assets can the client produce per week?
   (1–2 / 3–5 / 6–10 / 10+)

7. **Prior-flight benchmarks** (optional) — Are there results from a prior TikTok campaign
   for this brand to compare against? If yes, provide any available key metrics.

### 1b. Pull campaign data via TikTok MCP

After gathering user context, pull the following in parallel:

**Setup data:**
- `tiktok_get_campaign_details` → campaign objective, budget_mode, budget, bid_type,
  smart_creative_status
- `tiktok_get_adgroup_details` → per ad group: optimization_goal, audience_type,
  interest_category_ids, bid, budget, placement_type, pixel_id, conversion_event,
  frequency, frequency_schedule
- `tiktok_get_ad_details` → per ad: ad_format, spark_ad_type, call_to_action,
  landing_page_url

**Performance data** (date range: campaign start → today):
- `tiktok_get_reporting` at CAMPAIGN level: spend, budget, impressions, reach, frequency,
  clicks, ctr, cpm, cpv, video_watched_2s, video_watched_6s, video_views_p100,
  conversions, cost_per_conversion, conversion_rate
- `tiktok_get_reporting` at ADGROUP level: spend, budget, impressions, clicks, ctr, cpm,
  video_watched_6s, video_views_p100, conversions, cost_per_conversion, reach, frequency
- `tiktok_get_reporting` at AD level: spend, impressions, clicks, ctr, cpm,
  video_watched_2s, video_watched_6s, video_views_p100, likes, comments, shares,
  conversions, cost_per_conversion, frequency

---

## Step 2: Evaluate Performance

Run all of the following calculations against the pulled data. These feed directly into
the recommendation generation in Step 3 — flag every metric that is out of range.

### Pacing

```
days_elapsed = today - campaign_start_date
total_days = campaign_end_date - campaign_start_date
expected_spend = (days_elapsed / total_days) × total_budget
pacing_ratio = actual_spend / expected_spend
projected_total = (actual_spend / days_elapsed) × total_days
```

| Pacing Ratio | Status |
|---|---|
| 0.90–1.10 | ✅ On Track |
| 0.75–0.89 or 1.11–1.20 | ⚠️ Off Pace |
| < 0.75 or > 1.20 | 🔴 Action Required |

### KPI vs. Goal

```
kpi_performance_ratio = actual_kpi / goal_kpi
days_remaining_ratio = days_remaining / total_days
```

Flag when performance is >20% off goal with <40% of flight remaining.

### Creative Health

| Metric | Formula | Benchmark | Flag If... |
|---|---|---|---|
| Hook Rate (2s) | video_watched_2s / impressions | 30–40% | < 25% → rework hook |
| 6s Retention Rate | video_watched_6s / video_watched_2s | 65–75% | < 55% → content loses viewers after hook |
| 6s View Rate (absolute) | video_watched_6s / impressions | 25–30% | < 20% → combined hook + early content issue |
| Video Completion Rate | video_views_p100 / impressions | 30–40% | < 20% → length or content issue |
| Frequency (creative-level) | frequency per AD, last 7 days | < 3 | ≥ 3.5 → fatigue risk; ≥ 5 → rotate now |
| CTR trend | 3-day rolling | 0.5–1.5% (varies) | Declining 3+ consecutive days → fatigue |
| Engagement Rate | (likes+comments+shares) / impressions | 3–6% | < 2% → weak resonance |

> **Metric disambiguation:** The "6s retention rate" (video_watched_6s / video_watched_2s)
> and the "6s view rate" (video_watched_6s / impressions) measure different things and
> should not be conflated. Use the retention rate to isolate whether the hook or the early
> content is the problem; use the absolute view rate for top-line creative health reporting.
> The "40%+" figure appearing in some 2025 sources refers to a top-quartile aspirational
> target for absolute 6s view rate, not the average benchmark.

### Setup Issue Check (Root Cause Only)

Run the following checks. **Do not surface these as a standalone section.** Only use them
to explain a performance problem that was already identified above. A setup issue earns a
place in the recommendations only if it is actively contributing to a flagged metric.

| Check | Best Practice | Flag If Relevant |
|---|---|---|
| Optimization goal alignment | Must match campaign objective (routing table below) | 🔴 if misaligned AND performance is off |
| Pixel present + firing | Required for conversion/AEO objectives | 🔴 if missing and CPA is off-target or delivery is low |
| Cost Cap timing | Only after 50+ weekly conversions | ⚠️ if set early AND delivery is constrained |
| Creative count per ad group | 3–5 minimum | 🔴 if < 3 AND fatigue or delivery is flagged |
| CBO enabled | For 3+ ad groups | ⚠️ if disabled AND budget is concentrating unevenly |
| Smart Creative | Enabled | 💡 if disabled AND creative performance variance is high |
| iOS + Android mixed | Separate ad groups required | 🔴 if mixed AND CPI/attribution is off |
| Budget per ad group | ≥ 50× CPI target (app) / ≥ 20× CPA (web) | 🔴 if below floor AND campaign is stuck in learning |
| Audience scope | Broad for awareness; targeted for conversion | ⚠️ if mismatched AND CPM/CTR is off-benchmark |
| Conversion event depth | Match to available volume | ⚠️ if deep-funnel event used with <50 weekly conversions |
| UTM parameters | Required on all landing page URLs | ⚠️ if missing AND traffic quality is unmeasurable |

**Optimization Goal Routing Table** (for alignment check above):

| Campaign Objective | Correct Optimization Goals |
|---|---|
| Reach / Brand Awareness | REACH, VIDEO_VIEW |
| Traffic | LANDING_PAGE_VIEW, CLICK |
| App Install | APP_INSTALL |
| App Event Optimization | IN_APP_EVENT |
| Web Conversion | CONVERSION |
| Lead Generation | LEAD_GENERATION |

---

## Step 3: Generate Optimization Recommendations

This is the primary output. Run four analysis passes, then merge, deduplicate, and rank
into a single prioritized action list.

For the detailed recommendation menus, consult [`reference/recommendation-playbooks.md`](reference/recommendation-playbooks.md). Run all four passes against that file:

- **Pass A — Objective-based:** select entries matching the campaign objective (Reach/Views, Traffic, App Install/AEO, Web Conversion/Lead Gen).
- **Pass B — Audience-based:** apply checks based on `audience_type` and targeting configuration.
- **Pass C — Creative:** apply checks based on creative health signals from Step 2.
- **Pass D — Vertical-specific:** apply the playbook entry for the campaign's industry vertical.

Pull the candidate actions from each pass, then merge and rank them as described below.

### Merging and Ranking All Recommendations

After completing all four passes, compile the final action list:

1. **Deduplicate** — if multiple passes surface the same recommendation, list it once at
   the highest severity level across all passes.
2. **Cap at 7 items** — rank by expected impact. Structural blockers (missing pixel, wrong
   optimization goal) always outrank creative issues. Bid strategy fixes outrank audience
   expansion.
3. **Severity order:** 🔴 (act today) > ⚠️ (this week) > 💡 (consider for next sprint)
4. **Execution tag:** Mark each item as one of:
   - 🤖 **MCP-executable** — can be implemented directly via the TikTok MCP (bid changes,
     budget adjustments, enabling Smart Creative/Smart Targeting/CBO, pausing ads or ad
     groups, updating optimization goals, audience targeting changes, frequency cap settings)
   - 👤 **Manual** — requires human action outside the API (creating new creatives, linking
     an organic account for Spark Ads, setting up pixel tracking, Brand Lift Studies via
     TikTok rep, legal review of ad copy)
5. **Format each item as:**
   - **Priority:** [rank] | [severity emoji]
   - **Action:** specific change in plain language
   - **Where:** campaign name / ad group name / ad name
   - **Why it matters:** performance signal that triggered this + expected business impact
   - **Root cause (if structural):** only include if a setup issue is the underlying driver
   - **How to implement:** step-by-step instructions
   - **Execution:** 🤖 MCP-executable or 👤 Manual

---

## Step 4: Generate the Output

Ask the user what format they want for the output: a structured list in chat, a **docx**
document, or a **pptx** deck.

Regardless of format, the output has three sections in this order:

### Section 1 — Performance Summary

A brief (3–5 sentence) assessment of where the campaign stands. Lead with the highest-
severity finding. Cover: pacing status, KPI vs. goal, and top creative health signal.
If setup issues are contributing to performance problems, name them here. Close with
a one-sentence verdict: "The campaign is [on track / at risk / off-course] with [X days]
remaining."

Include a compact data table:

| | Actual | Goal / Benchmark | Status |
|---|---|---|---|
| Spend to date | | | |
| Pacing ratio | | On track = 0.90–1.10 | |
| Primary KPI | | [user-provided goal] | |
| [Top 2–3 creative metrics vs. benchmark] | | | |

### Section 2 — Optimization Actions (Primary Deliverable)

The full prioritized action list from Step 3. This is the core output — everything else
supports it.

Present as a numbered list, 1–7, ordered by expected impact.

For each item:
```
[#] [🔴/⚠️/💡] ACTION TITLE
Where: [campaign / ad group / ad name]
Why it matters: [performance signal → business impact]
Root cause: [only if structural — e.g., "Cost Cap was set before 50 conversions/week"]
Depends on: [only if this action cannot safely run before another action completes —
  e.g., "Complete action 3 first (new creative must be live before pausing the only
  active ad in this group)". Omit this field if the action is fully independent.]
How to implement: [step-by-step]
Execution: [🤖 MCP-executable / 👤 Manual]
```

**Sequencing rule:** Before finalizing the action list, scan all items for execution
dependencies — cases where acting on item N before item M would break delivery, reset
learning, or make item N ineffective. Common dependency patterns:
- Pausing the only active ad in an ad group before a replacement is live → ad group
  goes dark. Always note: "Complete action [X] (new creative) before executing this."
- Enabling Smart Creative while underperforming ads are still active → Smart Creative
  has no winners to weight toward. Note dependency on creative clean-up action.
- Raising a bid while creative fatigue is causing the CTR drop → bid change won't help
  if the algorithm is serving a fatigued ad. Note the creative action should run first.
Any action with a dependency must include the `Depends on` field. An action without
the field is implicitly safe to execute immediately and independently.

### Section 3 — Supporting Data

Include only the tables relevant to the recommendations above. Omit anything that was
clean and not referenced in the action list.

Suggested tables (include as relevant):
- Pacing by ad group (spend vs. budget, days remaining)
- Creative performance ranked by primary KPI efficiency (hook rate, 6s view rate, VCR,
  CTR, frequency, conversions/cost)
- Setup flags table (only items that contributed to recommendations; omit if none)

---

## Output Standards

- Lead every section with the highest-severity finding
- Tone: confident, clear, client-ready — not jargon-heavy. Written for brand stakeholders,
  not media traders. Translate platform terms (e.g., "oCPM" → "cost-per-thousand-impression
  bidding optimized toward your goal")
- All % figures rounded to one decimal place; currency to two decimals
- Never fabricate data or benchmarks — use only what was pulled from MCP or provided by user
- Always note the data pull timestamp and reporting window
- Flag when data is preliminary (campaigns < 72 hours old may have attribution lag)
- Flag when a recommendation requires platform access beyond what the activation team has
  (e.g., Brand Lift Studies require a TikTok rep; some Smart+ features require account-level
  enablement)
- Frame every recommendation in terms of business impact first, platform mechanics second
- For MCP-executable items: after delivering the action list, offer to execute any 🤖 items
  immediately if the user confirms

---

## Common Pitfalls to Avoid

- **Don't surface setup diagnostics as a standalone section** — only name a setup issue
  when it is the root cause of a performance problem already identified in the data.
- **Don't flag broad targeting as a problem on awareness campaigns** — it is correct.
  Only flag narrow targeting on awareness objectives.
- **Don't recommend Cost Cap before 50+ weekly conversions** — it will under-deliver.
- **Don't treat iOS and Android as interchangeable** — always flag combined ad groups.
- **Don't skip the vertical benchmark comparison** — raw numbers without context are
  meaningless. A 0.6% CTR is good for Finance and poor for Gaming.
- **Don't surface more than 7 recommendations** — prioritize ruthlessly.
- **Don't recommend creative refreshes without accounting for pipeline capacity** — if the
  client can only produce 1–2 assets per week, name which single creative to prioritize.
- **Don't omit the execution tag** — every recommendation must be tagged 🤖 or 👤.
  This is what enables the activator to decide whether to act directly or delegate to the MCP.
- **Don't issue actions that interact without calling out the dependency** — if executing
  action N before action M would break delivery or make N ineffective (e.g., pausing the
  only ad in a group before a replacement is live), the dependent action must include a
  `Depends on` field naming the prerequisite. An action without this field signals it is
  safe to execute immediately and independently.

---

## Reference Material

Supporting reference files (consult as needed; not loaded by default):

- [`reference/recommendation-playbooks.md`](reference/recommendation-playbooks.md) — detailed objective, audience, creative, and vertical recommendation menus (Passes A–D).
- [`reference/benchmarks.md`](reference/benchmarks.md) — platform-level benchmark context for interpreting performance.
- [`reference/sources.md`](reference/sources.md) — official TikTok and third-party best-practice sources.
