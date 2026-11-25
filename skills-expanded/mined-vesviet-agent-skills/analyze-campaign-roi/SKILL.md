---
name: analyze-campaign-roi
description: Measure conversion rates, organic search traffic, and CPA of generated content. Use when launching a new campaign, migrating from pixel-only to server-side tracking, or diagnosing attribution gaps.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Analyze Campaign ROI

Use this skill to perform financial engineering and risk analysis of MMO campaigns, combining revenue streams, recurring LTV cohort projections, Blended ROAS, multi-tier affiliate structures, and amortized operational overhead to determine True ROI.

## Legal & Compliance Notice

This skill analyzes financial data only and does not itself execute any platform-facing technique. "Die-rate" here means the observed rate of account restrictions from any cause; factoring it into ROI is a financial modeling practice, not an endorsement of any technique that causes it. See `deploy-mmo-infrastructure`, `manage-mmo-assets`, and `deploy-proxyware-fleet` for the compliance notices covering the underlying infrastructure and asset-management techniques.

## When to Use

- calculating True ROI accounting for ad spend, proxy networks, AI API tokens, and account die-rate replacement costs
- modeling Customer Lifetime Value (LTV) across Day 30/60/90 cohort retention curves for recurring offers
- computing Blended ROAS and Marketing Efficiency Ratio (MER) to reconcile multi-channel attribution gaps
- auditing multi-tier affiliate payout economics (Tier 1 CPA, Tier 2 master overrides, milestone bonuses, clawbacks)
- diagnosing tracking attribution mismatches between trackers and ad networks to guide pause vs scale decisions

## Example (True ROI, LTV Cohort Retention & Blended ROAS)

```python
# True ROI & Blended ROAS calculation accounting for operational overhead
ad_spend = 12500.00
direct_revenue = 28400.00        # Tier 1 direct CPA conversions
rebill_revenue = 9200.00         # Day 30/60 recurring subscription rebills
tier2_override = direct_revenue * 0.05  # 5% master affiliate 2nd tier override
milestone_bonus = 2000.00        # Network volume threshold milestone bonus
gross_revenue = direct_revenue + rebill_revenue + tier2_override + milestone_bonus

# Operational costs & reserve escrow
proxy_cost = 450.00
api_cost = 180.00
account_die_rate = 0.08          # 8% monthly account attrition rate
replace_cost = account_die_rate * 45.00 * 30  # 30 accounts active in rotation
clawback_reserve = gross_revenue * 0.03       # 3% chargeback/refund reserve escrow

total_cost = ad_spend + proxy_cost + api_cost + replace_cost + clawback_reserve
true_net_profit = gross_revenue - total_cost
true_roi = true_net_profit / total_cost

# Blended ROAS & Marketing Efficiency Ratio (MER)
blended_roas = gross_revenue / ad_spend
mer = gross_revenue / (ad_spend + proxy_cost + api_cost)

print(f"True ROI: {true_roi:.2%}, Blended ROAS: {blended_roas:.2f}x, MER: {mer:.2f}x")
```

```python
# Customer Lifetime Value (LTV) 90-day cohort retention projection
def project_cohort_ltv(cac: float, m0_cpa: float, m1_ret: float, m2_ret: float, m3_ret: float, sub_val: float) -> dict:
    d30_ltv = m0_cpa + (m1_ret * sub_val)
    d60_ltv = d30_ltv + (m2_ret * sub_val)
    d90_ltv = d60_ltv + (m3_ret * sub_val)
    payback_days = (cac / (sub_val / 30.0)) if cac > m0_cpa else 0.0
    return {"d30_ltv": d30_ltv, "d60_ltv": d60_ltv, "d90_ltv": d90_ltv, "payback_days": payback_days}

# Automated campaign scaling decision matrix
def evaluate_scaling_action(true_roi: float, blended_roas: float, target_roi: float = 0.35) -> str:
    if true_roi > target_roi and blended_roas >= 2.0:
        return "SCALE: Increase ad spend +20% over 48h while monitoring EMQ"
    elif true_roi > 0.05:
        return "OPTIMIZE: Maintain ad spend; test new creatives and lander angles"
    return "PAUSE: Negative True ROI after operational overhead; halt ad sets"
```

## Core Rules

- **TRUE-ROI-COMPUTATION**: True ROI MUST factor in all direct and operational expenses: ad spend, proxy bandwidth, AI API consumption, account replacement die-rate, and affiliate clawback/chargeback escrow reserves. Never evaluate campaigns solely on raw ad-spend ROAS.
- **LTV-COHORT-RETENTION-MODELING**: For subscription and recurring offers, evaluate performance based on Day 30/60/90 cohort retention curves rather than single-conversion CPA. Compute customer acquisition cost (CAC) payback periods to prevent premature pausing of profitable subscription campaigns.
- **BLENDED-ROAS-AND-MER**: Calculate and monitor both Blended ROAS (`Total Net Revenue / Total Ad Spend`) and Marketing Efficiency Ratio (MER, `Total Revenue / Total Operational & Marketing Spend`) to reconcile cross-channel attribution gaps and dark social conversions.
- **MULTI-TIER-PAYOUT-STRUCTURES**: Account for multi-tier affiliate economics: Tier 1 direct CPA/CPL, Tier 2 master affiliate override percentages (typically 3–10%), volume milestone threshold bonuses, EPC (Earnings Per Click) benchmarks, and clawback reserve holds.
- **DATA-CLASSIFICATION**: Campaign revenue, payout schedules, and ROI metrics are classified as highly sensitive business data. Never log unmasked profit margins or commission rates in insecure logs or public traces.
- **EMQ-BENCHMARK**: Validate that Meta CAPI Event Match Quality (EMQ) remains >= 8.0/10 for lower-funnel events (`Purchase`, `Lead`). EMQ below 7.0 indicates severe signal degradation requiring immediate identity vector repair.
- **EVENT-DEDUPLICATION**: Confirm identical UUID v4 `event_id` between client-side pixel events and server-side S2S postbacks to prevent artificial 2x inflation in conversion counts.
- **CTIT-FRAUD-FILTER**: Exclude conversions with Click-To-Conversion-Time (CTIT) < 2.5 seconds (automated injection) and flag anomalous long-tail distributions (> 7 days) as click hijack IVT.
- **IOS18-AAK-AWARENESS**: Model iOS 18+ AdAttributionKit (AAK) crowd anonymity tiers (0–3) and delayed conversion postback windows; do not assume legacy fixed 7-day click attribution.

## Suggested Process

1. **Ingestion & Reconciliation**: Pull conversion, payout, and rebill data from affiliate network APIs and trackers (Voluum, Binom, Keitaro). Reconcile against ad platform reported spend.
2. **True Cost Aggregation**: Calculate comprehensive cost stack: paid ad spend, proxy pool subscriptions, AI API token usage, and amortized account replacement costs based on historical die-rate.
3. **LTV Cohort Analysis**: Model 30/60/90-day retention curves for subscription offers, estimating future rebills, churn probabilities, and CAC payback durations.
4. **Blended ROAS & MER Calculation**: Compute blended performance metrics across all active traffic channels to establish the true campaign efficiency multiplier.
5. **Multi-Tier & Clawback Modeling**: Factor in Tier 2 override commissions, network volume milestone bonuses, and withhold a 3–5% reserve for chargebacks and refunds.
6. **Decision Matrix Generation**: Formulate mathematically grounded recommendations: scale budget (+20% increments), re-allocate ad sets, renegotiate payout tiers, or pause unprofitable angles.

## Checklist

- [ ] Ingested conversion and payout data reconciled across tracker and ad networks.
- [ ] True ROI calculation incorporates ad spend, proxy costs, API fees, and account replacement die-rate.
- [ ] LTV cohort retention curves modeled for Day 30, Day 60, and Day 90 recurring rebills.
- [ ] Blended ROAS and Marketing Efficiency Ratio (MER) computed across all active channels.
- [ ] Multi-tier affiliate payout structures (Tier 1 CPA, Tier 2 override, milestone bonuses) accounted for.
- [ ] Clawback and refund escrow reserve (3–5%) factored into net profit projections.
- [ ] Meta CAPI EMQ scores verified >= 8.0/10 for core conversion events.
- [ ] CTIT fraud filter applied; sub-2.5s programmatic conversions excluded from ROI calculations.
- [ ] Sensitive margin and payout data protected from exposure in plaintext logs.
- [ ] Actionable scale, pause, or optimize recommendations tied directly to True ROI thresholds.

## Output Contracts

When the campaign ROI analysis is completed for financial handoff or orchestration planning, emit:

- **`contracts/schemas/mmo-roi-report.json`** specifying campaign ID, gross revenue breakdown, operational cost stack, True ROI, Blended ROAS, MER, LTV cohort projections, multi-tier commissions, and scaling directives.
- **`contracts/schemas/data-analysis-report.json`** for general data analysis and reporting handoffs.
- Markdown summary detailing cohort retention curves, payback periods, and operational risk factors.

Skip emission for single-campaign one-off queries that do not cross role boundaries.

## Failure Modes

- **Hidden operational cost blindspot**: Omitting proxy bandwidth, API usage, or account replacement costs leads to running campaigns with apparent positive ROAS that are actually cash-flow negative. Mitigation: enforce full operational cost accounting in True ROI formula.
- **Premature subscription pause**: Pausing high-CPA subscription campaigns that achieve positive ROI only after Day 60/90 rebills. Mitigation: model full LTV cohort retention curves before making pause decisions.
- **Attribution mismatch distortion**: Pixel and S2S postback mismatch creates 2x double-counting, falsely doubling reported ROAS. Mitigation: verify UUID v4 `event_id` deduplication across all platforms.
- **Unbudgeted affiliate clawbacks**: Affiliate network retroactively reverses commissions due to chargebacks, turning profitable months negative. Mitigation: deduct 3-5% clawback reserve escrow from all gross revenue calculations.
- **CTIT bot inflation**: Programmatic click injection inflates conversion counts without delivering real buyers. Mitigation: exclude CTIT < 2.5s conversions as invalid traffic (IVT).

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Campaign financial data, payout agreements, and ROI margins are strictly confidential; never transmit unencrypted metrics over public channels.
- **ASI04 Supply Chain**: Affiliate network APIs and financial reporting SDKs must be authenticated and validated against verified endpoints; reject untrusted reporting endpoints.
- **ASI05 RCE Guard**: Never construct analytical SQL queries, BI dashboard commands, or financial calculations from untrusted external query parameters.
- **ASI07 Inter-Agent Communication**: ROI metrics and scaling directives must be emitted via `contracts/schemas/mmo-roi-report.json` for consumption by task planners and growth managers.
- **ASI09 Human-Agent Trust Exploitation**: Always disclose cohort retention assumptions, clawback reserve rates, and die-rate risk factors transparently when recommending ad spend scaling.

## Related Skills

- **setup-tracking-system**: Configure the S2S and postback tracking architecture analyzed by this skill.
- **analyze-data**: Perform exploratory statistical and cohort data analysis outside MMO performance contexts.
- Companion reference: `references/multi-touch-attribution-and-cpa-analytics.md`
- Companion example: `examples/campaign-roi-and-roas-dashboard.py`
