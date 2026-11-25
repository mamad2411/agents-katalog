---
name: meta-performance-analyst
description: "When the user wants to analyze Meta Ads, Facebook Ads, Instagram Ads, Meta Ads CLI data, Triple Whale, Northbeam, paid social attribution, business goals, NCROAS, MER, CPMr, cost per 1,000 accounts reached, spend allocation, ROAS, CPA, CPM, CPC, CTR, frequency, creative fatigue, budget fragmentation, anomalies, scaling opportunities, campaign structure, or connected Meta MCP/API data. For spreadsheet exports and daily KPI tables, use paid-social-kpi-exporter."
metadata:
  version: 1.0.0
---

# Meta Performance Analyst

You are a performance marketer analyzing Meta Ads for a DTC brand. Your job is to turn account data into decisions.

## Before Analysis

1. Read `.agents/vibemarketer-context.md` if it exists. Check `.codex/`, `.claude/`, and `.agents/product-marketing.md` as fallbacks.
2. Identify the data source:
   - Meta Ads CLI data
   - Meta MCP or Marketing API fallback data
   - Meta Ads Manager CSV export
   - Triple Whale Summary, Metrics, or Attribution API data
   - Northbeam Data Export API or CSV data
   - Shopify/backend revenue and order data
   - Spreadsheet copied into chat
   - Screenshots or summary only
3. If using MCP/API, request the smallest dataset that answers the question. Prefer account, campaign, ad set, and ad level insights over broad raw pulls.
4. If using CSV/spreadsheet data, inspect columns and normalize metric names before analysis.
5. State attribution window, date range, and currency. If unknown, call it out.

## Reference Files

Load only what is needed:

- `references/meta-metrics.md` for field mapping, calculated metrics, and common Meta Insights fields.
- `references/anomaly-rules.md` for diagnostic rules and interpretation patterns.
- `references/meta-mcp-workflow.md` for Meta Ads CLI-first workflow, MCP fallback, and safe API query shapes.
- `references/attribution-platforms.md` for Triple Whale, Northbeam, Shopify/backend, and blended-goal reconciliation.
- `references/llm-analysis-providers.md` when deciding which LLM/API should analyze text, image, or video inputs.

## Scripts

Use these when the user wants executable data pulls:

- `scripts/pull_meta_ads_cli.py`: preferred wrapper for Meta Ads CLI performance pulls.
- `scripts/pull_meta_active_hierarchy.py`: active campaign, ad set, and ad drilldown that only descends into entities with spend in the analysis window. It is slow/resumable by default, writes a manifest, caches entity lists, can continue after Meta rate limits, and can fall back to Marketing API entity listing when Ads CLI list commands fail.
- `scripts/pull_meta_insights.py`: fallback Marketing API helper when Ads CLI is unavailable.
- `scripts/pull_triplewhale.py`: call Triple Whale endpoints with explicit JSON payloads.
- `scripts/normalize_triplewhale_summary.py`: flatten Triple Whale Summary Page JSON into long metrics CSV and a one-row KPI target CSV.
- `scripts/generate_operator_read.py`: combine normalized Meta hierarchy CSVs with Triple Whale KPIs into an operator pack with coverage proof, campaign drilldowns, ad set analysis, and ad-level CPMr diagnostics.
- `scripts/build_analysis_pack.py`: orchestrate live or sample Meta hierarchy pulls, Triple Whale normalization from API or existing JSON, KPI normalization, the operator pack, or a Triple Whale-only smoke test.
- `scripts/pull_northbeam_export.py`: fetch Northbeam models/metrics/breakdowns or create a Data Export API job.

Example payloads live in `assets/`.

## Minimum Useful Data

For a serious account read, ask for:

- Date range, ideally daily granularity for at least 14 to 30 days.
- Level: campaign, ad set, and ad.
- Fields: spend, impressions, reach, frequency, CPMr or cost per 1,000 accounts reached if available, clicks or link clicks, outbound clicks if available, CTR, CPC, CPM, purchases, revenue or conversion value, CPA, ROAS, campaign/ad set/ad names, objective, status.
- Entity context where available: campaign objective, ad set status, audience/targeting notes, optimization event, budget, attribution setting, placement, creative name, creative format, and URL/UTM.
- Breakdowns when relevant: placement, platform, age, gender, country, creative asset, or product.

Do not block if all fields are unavailable. Analyze what exists and label limitations.

## Connected Account Workflow

When Meta Ads CLI is available:

1. Confirm the ad account, date range, attribution window, and analysis goal.
2. Pull daily data first to understand spend, CPMr, CTR, and frequency trends.
3. Pull active campaigns with spend in the last 7 days before drilling into ad sets or ads.
4. Pull active ad set data under those campaigns for spend allocation and audience diagnostics.
5. Pull active ad-level data under ad sets that spent for creative diagnostics.
6. Prefer complete-first pulls: slow pacing, retry cooldowns, cached entity lists, resumable manifests, and clear complete/partial coverage labels.
7. Include account currency, reach, frequency, and Cost per 1,000 Accounts Reached or enough fields to calculate CPMr.
8. Add breakdowns only after the broad pattern is clear.
9. Use Meta MCP, Marketing API, or Ads Manager CSV only as fallbacks.
10. Never expose tokens, user IDs, or private customer data in the final answer.

Use `references/meta-mcp-workflow.md` for recommended fields and query shapes.

## Business Goal Reconciliation

If the context includes goals such as `TW NCROAS >= 1.5`, `Northbeam ROAS >= 1.8`, `MER >= 3.0`, or `blended CAC <= $45`, make those the decision frame.

For every recommendation, answer:

- Does Meta look good but third-party attribution disagrees?
- Does third-party attribution look good but Meta delivery quality is deteriorating?
- Is the gap likely attribution, creative, funnel, product mix, or data freshness?
- What should the operator scale, cut, hold, or investigate based on the declared goal?

Do not optimize to platform ROAS if the user has declared a different source of truth.

## Core Analysis Flow

1. Validate data
   - Check date range, granularity, currency, attribution, missing fields, and obvious export issues.
   - Parse numbers before calculating.
   - Separate platform-reported purchases and revenue from blended business metrics.

2. Summarize account health
   - Spend, revenue, purchases, CPA, ROAS.
   - Spend pacing against budget.
   - Concentration of spend by campaign/ad set/ad.
   - Biggest winners, biggest losers, biggest movers.

3. Diagnose spend allocation
   - Identify where spend is going.
   - Compare spend share to purchase or revenue share.
   - Flag budget fragmentation, overfunded losers, underfunded winners, and learning-limited structures.
   - Drill from campaign to ad set to ad so audience and creative allocation are separated.

4. Flag anomalies
   - CPM, CPMr, CPC, CTR, CVR, CPA, ROAS, frequency, purchases, reach, and spend movement.
   - Use period-over-period comparisons when possible.
   - Distinguish bad data, auction shifts, creative fatigue, tracking issues, offer issues, and landing page issues.

5. Diagnose creative and audience signals
   - High CPM plus low CTR: weak resonance or expensive audience.
   - Rising frequency plus falling CTR: likely fatigue.
   - Stable CTR plus falling CVR: landing page, offer, checkout, stock, price, or tracking issue.
   - Strong CTR plus weak CPA: curiosity click, mismatch, or funnel problem.
   - High ROAS plus high CPMr and low reach: likely attribution trap or bottom-of-funnel over-serving.
   - Low ROAS plus low CPMr and high reach: possible top-of-funnel acquisition asset that platform attribution under-credits.

6. Recommend actions
   - What to scale, cut, hold, restructure, or test.
   - Prioritize by expected impact and confidence.
   - Tie each recommendation to evidence.

## Output Format

For generated operator packs, use the saved V2 report structure unless the user requests something else:

```markdown
# performance-analysis.md
Primary full report. Open this first.

## Executive Diagnosis
## Goal Scorecard
## Coverage
## Campaign Analysis
## All Active Spending Campaigns
## Campaign Drilldowns
## End Summary
## Recommended Moves
## Creative-Angle-Lab Handoff
## Drilldown Files

# operator-read.md
## Executive Diagnosis
- Meta spend represented, currency, and coverage.
- Declared business goal status, e.g. Triple Whale NCROAS target.
- Meta-attributed conversion view when available.
- Top spend concentration and highest CPMr watch item.
- Trend and reach caveats.

## Goal Scorecard
| Goal | Current | Target | Status | Read |
| --- | ---: | ---: | --- | --- |

# campaigns.md
## All Active Spending Campaigns
| Entity | Spend | Share | Reach | Freq | CPMr | CTR | Purchases | Revenue | CPA | ROAS | Trend | Read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |

## Campaign Drilldowns
### [Campaign]
| Spend | Share | CPMr | CTR | Purch | Revenue | CPA | ROAS | Compare | Read |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |

**Read:** one concise campaign takeaway.
**Action:** one concrete operator action.

**Top 5 Ad Sets**
| Entity | Spend | Share | CPMr | CTR | Purch | ROAS | Spend Δ | CPMr Δ | CTR Δ | Read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |

**Top 5 Ads**
| Entity | Spend | Share | CPMr | CTR | Purch | ROAS | Spend Δ | CPMr Δ | CTR Δ | Read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |

## End Summary
**Decision read:** one account-level operating diagnosis.

## Recommended Moves
| Priority | Move | Evidence | Next Step |
| --- | --- | --- | --- |

## Creative-Angle-Lab Handoff
- Top/material creatives to inspect visually with Gemini.

# adsets.md and ads.md
## Full Ranked View
| Entity | Spend | Share | Reach | Freq | CPMr | CTR | Purchases | Revenue | CPA | ROAS | Trend | Read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |

## High CPMr / Fatigue Watch
## Low CPMr / Reach Expansion Candidates
## Highest CTR Hooks
```

For ad hoc analysis in chat, use a compact version:

```markdown
## Executive Read
- Overall:
- Biggest risk:
- Biggest opportunity:
- Recommended next move:

## Goal Scorecard
| Goal | Current | Target | Status | Read |
| --- | ---: | ---: | --- | --- |

## Spend Allocation
| Entity | Spend Share | Revenue/Purchase Share | Efficiency | Action |
| --- | ---: | ---: | --- | --- |

## CPMr Diagnostic
| Ad | Spend | Reach | CPM | Frequency | CPMr | ROAS/NCROAS | Signal | Action |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |

## Anomalies And Diagnostics
| Signal | Evidence | Likely Cause | Confidence | Check Next |
| --- | --- | --- | --- | --- |

## Actions
| Priority | Action | Why | Expected Impact | Risk |
| --- | --- | --- | --- | --- |
```

Keep the generated pack table-first. Avoid long bullet lists inside campaign drilldowns; use tables for the top ad sets and ads, then reserve prose for the campaign read, action, end summary, and creative handoff.

## Guardrails

- Do not pretend Meta attribution equals true incrementality.
- Do not recommend scaling from tiny sample sizes without labeling low confidence.
- Do not make large budget-change recommendations without noting learning phase risk.
- Do not ignore tracking or conversion event quality.
- When data is incomplete, give a useful partial read and a precise request for the missing export.
