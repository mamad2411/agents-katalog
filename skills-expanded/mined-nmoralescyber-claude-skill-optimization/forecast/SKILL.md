---
name: forecast
description: Generates weighted sales forecasts with best/likely/worst scenarios, commit vs. upside breakdowns, gap-to-quota analysis, and pipeline coverage assessment. Make sure to use this skill whenever the user says forecast for [period/quarter], what's our number, gap to quota, pipeline coverage, sales forecast, commit and upside, weighted forecast, build a quarterly forecast, or describes wanting a structured revenue projection from pipeline data. Works on CSV pipeline exports, CRM data (HubSpot/Close/Salesforce when connected), or manual inputs. Includes scenario modeling, deal-by-deal weighting, and risk-adjusted projections. Do NOT use for: pipeline hygiene review and deal prioritization (use sales:pipeline-review), individual deal call prep (use sales:call-prep), or financial-statement-grade revenue forecasting that requires GAAP treatment (use finance:financial-statements). Defining characteristic: "weighted sales pipeline projection across a defined period."
---

# Forecast (Sales Pipeline)

Weighted sales forecasts with scenario modeling and gap-to-quota analysis.

## When to use vs. adjacent sales/finance skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Producing a weighted revenue forecast for a period | Reviewing deals for hygiene and prioritization → `sales:pipeline-review` |
| Commit vs. upside split needed | Prepping for a single specific call → `sales:call-prep` |
| Gap-to-quota analysis | GAAP revenue forecasting → `finance:financial-statements` |
| Pipeline coverage check | Building outreach to fill the pipeline → `sales:draft-outreach` |

## Forecast methodology

### Scenario definitions

For every forecast, three scenarios:

- **Worst case** — only deals with ≥80% probability AND in late stage (negotiation/close) AND no current red flag
- **Likely / commit** — weighted: deals × stage probability, conservative weighting (Sales-Forecast-Category committed deals only)
- **Best case** — all of likely + upside deals (mid-stage with positive signal) at full value

The spread between worst and best is the **forecast variance**. Tight spread = high confidence. Wide spread = pipeline is volatile.

### Default stage weighting

Adjust per your CRM stages, but start with:

| Stage | Weighting |
|---|---|
| Prospecting / Discovery | 5-10% |
| Demo / Qualification | 15-25% |
| Proposal / Eval | 35-50% |
| Negotiation | 60-75% |
| Verbal / Verbal Commit | 80-90% |
| Closed Won | 100% |
| Closed Lost | 0% |

These should be calibrated against your historical conversion data — if your "Negotiation" stage actually closes at 50%, use 50%. The default is a starting point.

### Gap-to-quota analysis

```
Quota:                $X
Closed-won this period: $Y
Worst case forecast:    $Z (worst)
Likely forecast:        $L (likely)
Best forecast:          $B (best)
Gap (likely - quota):   $L - $X
Coverage ratio:         (open pipeline value) / (quota - closed)
```

**Coverage ratios to watch:**
- <2.5x — pipeline is thin, urgent build-pipeline action required
- 2.5x-3.5x — adequate, monitor velocity
- 3.5x-4.5x — healthy
- >5x — possibly stuffed pipeline (deals lingering that should close or close-lost)

### Risk adjustments

After raw weighting, apply risk overlays for deals showing:

| Risk signal | Adjustment |
|---|---|
| Single-threaded (one champion) | -15% to weighted value |
| Champion just left or moved roles | -30% |
| Procurement/legal stuck >30 days | -20% |
| Budget questioned in last call | -25% |
| Competitive bake-off announced late | -15% |
| Push from previous quarter | -10% (pushed deals push again) |
| Verbal commit with paper not in hand | -10% (verbal ≠ signed) |

Risks compound — if a deal has 3 risk flags, it's not where the rep thinks it is.

## Output structure

Every forecast produces:

```markdown
# [Period] Forecast — [Date]

## Headline
- Worst:   $X
- Likely:  $Y  
- Best:    $Z
- Quota:   $Q
- Gap:     $Y - $Q (positive = beat plan; negative = at risk)
- Coverage: Nx

## Confidence: [High / Medium / Low]
[Reasoning in one paragraph]

## Top 5 deals driving the number
[Deal | Account | Stage | Value | Weighted | Risks]

## Top 5 deals at risk
[Deal | Account | Risk signal | Recommended action]

## Pipeline coverage by stage
[Bar chart or table: stage → value → weighted value]

## Push risk
[Deals likely to push to next period — explicit list]

## Build-pipeline recommendation
[If coverage <3x: how much new pipeline needed by when, by source]
```

## Cybersecurity sales context (if applicable)

For security/cybersec product sales, additional risk signals:

- **Security questionnaire stuck** — the procurement-side review can take weeks; track it explicitly
- **SOC 2 / ISO requested by prospect** — adds time, doesn't usually kill deals if you have it
- **Pen test required pre-sale** — adds 4-8 weeks, adjust expected close date
- **Compliance officer added late to evaluation** — usually positive signal but extends cycle
- **Customer security incident** — they're either buying urgently or freezing all spend; ASK
- **MSA/DPA negotiation** — often the longest-tail step; track separately

## Anti-patterns

- **"Sandbagging"** — reps systematically under-forecasting; check rep accuracy over 4 quarters
- **"Hockey stick"** — disproportionate close in last week of period; signals stuffed pipeline
- **"Same number every quarter"** — too clean to be real
- **Ignoring push risk** — every quarter has 10-20% deals that will push; model it
- **Single-source forecast** — only rep judgment, no historical conversion math
- **Best-case as commit** — confusing aspiration with prediction
- **Forecast without coverage** — the number can't be hit without enough pipeline

## Output

Produces:
1. The structured forecast above
2. Top deals driving + at-risk lists
3. Coverage analysis
4. Build-pipeline recommendation if needed
5. Confidence level with rationale
6. Suggested follow-up: chain to `sales:pipeline-review` for deal-level work or `sales:draft-outreach` to build pipeline
