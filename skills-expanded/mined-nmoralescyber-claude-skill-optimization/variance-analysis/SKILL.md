---
name: variance-analysis
description: Explains the WHY behind a financial variance — decomposes the change into volume × price × mix (or rate × efficiency for cost), writes executive narrative, and recommends a clear next action (sustain / investigate / monitor / mitigate). Use this skill whenever the user says explain the variance, decompose this difference, why is [account] different from budget / last quarter / last year / forecast, build a variance waterfall, what's driving the change in [revenue / cost / margin / ARR / NRR / CAC / gross margin], variance commentary for [board / leadership / investors], flux analysis, fluctuation analysis, walk me from period A to period B, or describes wanting to understand WHY a number changed. This is a NARRATIVE-and-DRIVER skill, not a number-production skill — it defers to finance:financial-statements to produce the statements that flag the variance, finance:reconciliation if the variance traces to a tie-out problem, finance:journal-entry if a correcting entry is needed, finance:close-management if the variance comes from a close-cycle context, finance:audit-support if a SOX-relevant control deficiency surfaces, data:build-dashboard for SaaS / operational KPI views (ARR, NRR, CAC), and data:analyze for general data comparison outside finance. Tuned for a Puerto Rico cybersecurity SaaS startup (cyber-insurance premium, SOC 2 audit fees, pen-test fees, GRC tooling, MSSP services, Act 60 tax effects). Defining characteristic: "explain the WHY of a financial variance with driver decomposition, narrative, and a clear next action."
---

# Variance Analysis

Driver decomposition for financial variances — volume × price × mix breakdown, waterfall, executive narrative, action recommendation. Explains the WHY; defers the HOW elsewhere.

## When to use vs. delegate

| Use this skill when... | Delegate to... |
|---|---|
| Explaining WHY a number changed | (this skill) |
| Building a waterfall visualization spec | (this skill) |
| Writing variance commentary for leadership / board / investors | (this skill) |
| Recommending sustain / investigate / monitor / mitigate | (this skill) |
| Producing the statements that flag the variance | `finance:financial-statements` |
| The variance traces to a rec problem (a tie-out broke) | `finance:reconciliation` |
| A correcting JE is needed once cause is known | `finance:journal-entry` |
| Variance arises during the close cycle | `finance:close-management` (orchestrator) |
| SOX / control-deficiency root cause | `finance:audit-support` |
| SaaS / operational KPI view (ARR, NRR, CAC, payback, magic #) | `data:build-dashboard` |
| General non-finance data comparison | `data:analyze` |

If the request is "produce the statement and explain the flux," chain `finance:financial-statements` first, then this skill.

## The variance lifecycle (canonical chain)

```
finance:close-management   →   finance:financial-statements   →   THIS SKILL (variance-analysis)
                                            │
                                            └─ on tie-out anomaly →  finance:reconciliation
                                            └─ on correcting entry →  finance:journal-entry
                                            └─ on SOX-flag        →  finance:audit-support
                                            └─ on SaaS-KPI view   →  data:build-dashboard
```

## Driver decomposition framework

Every variance has 1–4 quantified drivers + a narrative. Pick the right framework for the line.

### Revenue: Volume × Price × Mix

```
Revenue variance ≈
   ΔVolume × Prior Price                    (volume effect)
 + Prior Volume × ΔPrice                    (price effect)
 + (Mix shift effect on weighted ASP)       (mix effect)
 + Residual / interaction                   (cross-term — keep small)
```

- **Volume** — units / customers / seats / endpoints / events
- **Price** — average selling price (ARPU, ARPA, ASP)
- **Mix** — share of higher-vs-lower-priced SKUs (e.g., Enterprise vs. SMB tier)
- **Residual** — the cross-term from interacting volume × price changes; if > 5% of total variance, surface it; do NOT silently bury it in another bucket

### Cost: Volume × Rate × Efficiency

```
Cost variance ≈
   ΔVolume × Prior Rate                     (volume effect — more activity)
 + Prior Volume × ΔRate                     (rate effect — vendor / inflation)
 + (Efficiency variance: actual vs. standard usage at standard rate)
```

### Margin: chain the two

Margin variance = Revenue variance ÷ Revenue − Cost variance ÷ Revenue, decomposed into operating leverage (fixed-cost absorption) and mix.

### Worked decomposition — revenue (cybersec SaaS example)

Period A (Q4): 100 customers × $5,000 ARPA = $500,000 MRR
Period B (Q1): 120 customers × $5,400 ARPA = $648,000 MRR
Total variance: +$148,000 (+29.6%)

Calculate each driver against the prior baseline:

```
Volume effect = (120 − 100) × $5,000               = +$100,000   (67.6% of total)
Price effect  = 100 × ($5,400 − $5,000)            = +$ 40,000   (27.0% of total)
Residual      = (120 − 100) × ($5,400 − $5,000)    = +$  8,000   ( 5.4% of total)
                                                     ─────────
                                                     +$148,000  ✓
```

Mix effect (separate cut): if 20 of the 120 customers are Enterprise tier at $9,000 ARPA (vs. 5 of 100 prior), Mix = (Δ tier-share × Δ price-per-tier) — surface as its own bar in the waterfall.

**Residual rule:** if residual is > 5% of total variance, name it explicitly — do NOT silently merge into Volume or Price. Label as "interaction effect" and explain ("more customers AND higher prices interact: +$8K").

### Worked decomposition — cost (cybersec example)

Cyber-insurance Q4 = $29,000; Q1 = $48,000. Volume = 1 policy in both periods.

```
Volume effect     = (1 − 1) × $29,000              = $       0
Rate effect       = 1 × ($48,000 − $29,000)        = +$19,000   (100% of variance)
Efficiency        = N/A (single policy, no usage variance)
                                                     ─────────
                                                     +$19,000
```

Sub-decompose Rate: $17K of the $19K rate increase is base-renewal hardening; $2K is the $5M tower add-on. Surface as two separate items in the per-driver explanation.

### SaaS-specific (surface SEPARATELY from GAAP narrative)

GAAP variance and SaaS-metric variance answer different questions. Always produce both.

| Metric | Drivers (decompose into these) |
|---|---|
| **ARR variance** | New ARR (new logos) + Expansion ARR − Churned ARR − Contracted ARR (the four NRR drivers) |
| **NRR variance** | Expansion rate + cross-sell − gross churn − downgrade |
| **Gross retention variance** | Logo churn × ACV; segment-cut |
| **CAC variance** | ΔS&M spend ÷ ΔNew-customer count; sales-spend, marketing-spend, sales-cycle length |
| **CAC payback variance** | CAC change ÷ gross-margin-adjusted ARR per customer |
| **Magic number variance** | (Net new ARR × 4) ÷ S&M spend prior quarter — efficiency of growth investment |
| **Gross margin variance** | Hosting cost / customer + support cost / customer + services attach + COGS mix |
| **Cloud cost variance** | Usage growth × prior rate + committed-use savings change + region/service mix |

## Cybersecurity / PR cost-variance taxonomy

Common cost lines for a PR cybersec SaaS — name them when explaining flux. Each gets its own driver pattern.

| Line | Typical drivers |
|---|---|
| **Cyber-insurance premium** | Renewal rate hike, coverage limit change, claim history, control posture (MFA / EDR / IR plan adoption) |
| **SOC 2 audit fees** | Type I → Type II transition, audit-period length, scope changes (added Trust Services Criteria), auditor change |
| **Pen-test fees (we are buyer)** | Scope (apps, network, social-eng), retest volume, premium for niche vendor, customer-driven pen tests vs. our annual |
| **GRC tooling** | Seats, modules added (vendor risk, policy, audit evidence), tier upgrade, vendor change |
| **Compliance headcount** | New hire (GRC analyst, vCISO retainer), allocation shift between R&D and G&A |
| **Hosting / cloud (AWS/GCP/Azure)** | Usage growth, region expansion, committed-use savings expiring, new managed services adopted, egress |
| **Threat intel feeds** | New feed added, tier upgrade, renewal price hike |
| **Bug-bounty payouts** | Severity mix, scope change, program maturation |
| **Hacienda / IVU true-ups** | Rate change, exemption status change, prior-period adjustment |
| **PR payroll-side employer costs** (SUTA, FUTA, ASUME, SINOT, choferil) | Headcount, wage-base change, rate change |

## Action framework (always recommend ONE)

| Direction | Magnitude | Recommendation | Reasoning |
|---|---|---|---|
| Favorable | < 5% | **Sustain** | Within noise; document the driver to repeat |
| Favorable | 5–15% | **Sustain + verify non-recurring** | Was it a one-time benefit? Note in narrative |
| Favorable | > 15% | **Investigate** | Big positive flux is often a timing or estimate change, not real performance |
| Unfavorable | < 5% | **Monitor** | Add to watchlist; revisit next period |
| Unfavorable | 5–15% | **Mitigate** | Specific corrective action with owner + due date |
| Unfavorable | > 15% | **Escalate + Mitigate** | Founder / board awareness; root-cause now, not next month |
| Either | Trend (3+ periods same direction) | **Re-baseline** | Update budget/forecast; the variance reveals the plan was wrong |

Never end a variance write-up without one of: **Sustain / Verify / Monitor / Mitigate / Investigate / Escalate / Re-baseline**.

## Standard variance-analysis output

```markdown
# Variance: [Line item] — [Period A] vs. [Period B]   ($ in [units], [reporting currency])

## Headline
- Period A: $X
- Period B: $Y
- Variance: $Y − $X = $Z   (Favorable / Unfavorable)
- Variance %: Z / X = N%
- Materiality threshold tripped: YES / NO   (threshold: $___ or __% of [base])

## Driver decomposition

| Driver | Impact ($) | Impact (%) | Direction | Confidence |
|---|---|---|---|---|
| Volume     | $A | n% | Fav / Unfav | High / Med / Low |
| Price/Rate | $B | n% | Fav / Unfav | High / Med / Low |
| Mix        | $C | n% | Fav / Unfav | High / Med / Low |
| Residual / interaction | $D | n% | — | — |
| **Total**  | **$Z** | **n%** | | |

## Per-driver explanation
- **Volume** — [what changed in units / customers / consumption; cite source]
- **Price/Rate** — [list-price change, discount discipline, vendor price action]
- **Mix** — [tier / segment / SKU shift; cite the cohort cut]
- **Residual** — [if > 5%, explain the cross-term honestly]

## Multi-period context (do not skip)
| Period | Value | Δ vs prior | Trend | 
| t-3 | | | |
| t-2 | | | |
| t-1 | | | |
| t   | | | |
[Is this a blip or a pattern? Name it.]

## SaaS metric view (if revenue-side)
- ARR end-of-period: $___ ; Δ: New $__ + Exp $__ − Churn $__ − Contract $__
- NRR: __% ; GRR: __%
- CAC: $___ ; Payback: ___ months
- Magic number: ___

## Narrative (executive — 3-4 sentences)
[Tie drivers to business reality. Name the customer / cohort / vendor / contract that drove it. Avoid "due to market conditions."]

## Recommended action
[ONE of: Sustain / Verify non-recurring / Monitor / Mitigate / Investigate / Escalate / Re-baseline]
[Owner + due date if action is anything other than Sustain or Monitor]

## Waterfall spec
[See Waterfall section below — pass to data:build-dashboard for the chart]
```

## Waterfall visualization spec

Pass this spec to `data:build-dashboard` (or `data:create-viz` for a one-off).

```
Bars in this order:
  [1] Period A starting value         (anchor bar)
  [2] Volume effect                   (Δ bar, color = direction)
  [3] Price/Rate effect               (Δ bar)
  [4] Mix effect                      (Δ bar)
  [5] Residual                        (Δ bar — only if material)
  [6] Period B ending value           (anchor bar)

Convention: green = favorable, red = unfavorable, grey = anchors.
Label every bar with $ value AND % of starting value.
```

## Narrative quality — write like a CFO, not a textbook

A variance narrative is read in 20 seconds by a board member or founder. Every sentence earns its place.

### Structure (3-4 sentences, in this order)

1. **What changed and how big** — direction, $, % vs. base, materiality.
2. **Why (top 1-2 drivers in business terms)** — name the customer / cohort / vendor / contract / regulation. NOT "due to volume."
3. **What it means** — is it a one-time, a trend, a structural shift, or a control failure?
4. **What we're doing about it** — the chosen action verb (Sustain / Verify / Monitor / Mitigate / Investigate / Escalate / Re-baseline) with owner.

### Tone rules

- **Specific over generic.** "Lost the ACME renewal ($240K ARR) to a competitor on price after a December RFP" beats "competitive pressure."
- **Causal language.** Use "because," "driven by," "offset by." Avoid "due to" without a noun.
- **Numbers in-line.** "+$120K Volume / −$45K Price / +$10K Mix = +$85K" beats "mostly volume."
- **Name the human / system / contract.** A real noun should anchor every driver.
- **Acknowledge confidence.** If a driver is estimated, say so — "preliminary; subject to Q3 cohort cut."
- **No throat-clearing.** Cut "It is important to note that," "As you can see," "moving forward."
- **PR / cybersec realism.** Reference Hacienda rate change, Act 60 effect, cyber-insurance renewal cycle, SOC 2 audit window, MSSP retainer ramp BY NAME when relevant.

### Worked example — favorable revenue beat

> Q1 ARR ended at $4.2M, +$340K (+8.8%) vs. plan and +$520K (+14%) vs. Q4. The beat was almost entirely Volume (+$295K, 87% of the variance) — three Enterprise SOC-monitoring deals (BancoPR, MMM, AcmeFin) closed in March that were forecast for Q2. Price was −$22K (Enterprise tier discounting at 12% vs. 9% planned); Mix was +$67K from upsell into the IR-retainer add-on. Trend: this is the second consecutive quarter of pull-in from later quarters — pipeline coverage is real, but Q2 plan now needs a re-baseline. **Action: Re-baseline Q2 ARR plan; CFO + Head of Sales own by [date].**

### Worked example — unfavorable cost variance

> Cyber-insurance premium hit $48K in March, +$19K (+66%) vs. budget. Driver is Rate (+$17K, 89%) — the renewal came in at $48K vs. $29K prior on the back of a 2024 industry-wide hardening cycle and our adding $5M of cyber-tower limit. Volume effect (+$2K) is one extra D&O endorsement. This is a structural shift, not a one-time. **Action: Mitigate — broker bake-off in Q2 (target 3 quotes), and accelerate MFA + EDR adoption evidence to soften 2026 renewal. Owner: Founder + GRC lead by May 30.**

### What good looks like vs. what bad looks like

| Bad | Good |
|---|---|
| "Revenue was up due to favorable market conditions." | "Revenue was up $340K (+8.8%) on three pulled-in Enterprise SOC deals (BancoPR, MMM, AcmeFin)." |
| "Cyber-insurance increased materially." | "Cyber-insurance premium rose $19K (+66%) on a 2024 industry-wide rate hardening; our $5M tower add-on contributed +$2K." |
| "Mix shift drove the variance." | "Mix shift drove +$67K — IR-retainer attach grew from 18% to 27% of new logos." |
| "We will continue to monitor." | "Mitigate: broker bake-off in Q2 (3 quotes), MFA+EDR evidence ready by May 30. Owner: Founder + GRC." |

## Common variance patterns (pattern → likely diagnosis)

### Revenue
| Pattern | Diagnosis | Action |
|---|---|---|
| Beat on volume + flat price | Strong sales execution | Sustain |
| Beat on price + flat volume | Pricing power; verify not one-time | Verify non-recurring |
| Beat on volume + price down | Discounting to hit number | Mitigate (pricing review) |
| Miss on volume + flat price | Sales execution; pipeline thin | Investigate |
| Miss on volume + price up | Lost deals on price | Mitigate (pricing review) |
| Mix to lower tier | Down-market drift | Investigate |
| Mix to higher tier | Successful upsell / land-expand | Sustain |
| ARR up but NRR down | Gross-add carrying weak retention | Mitigate (retention) |
| Logo growth + ARR flat | Down-market or contraction | Investigate |

### Cost
| Pattern | Diagnosis | Action |
|---|---|---|
| Volume up, rate flat | Scaling proportionally | Monitor |
| Volume flat, rate up | Vendor/inflation | Investigate |
| Volume up, efficiency down | Scaling poorly | Mitigate |
| Cyber-insurance premium up sharply | Renewal hike or scope change | Investigate (broker review) |
| Cloud cost up, usage flat | Committed-use expired or service mix shift | Investigate (FinOps review) |
| SOC 2 fees up | Type II transition or scope add | Verify (one-time) |

### Margin
| Pattern | Diagnosis | Action |
|---|---|---|
| Margin up, revenue up | Operating leverage | Sustain |
| Margin up, revenue down | Cost discipline (good if sustainable) | Verify |
| Margin down, revenue up | Growth investment (verify intentional) | Verify |
| Margin down, revenue down | Bad combo | Escalate |

## Anti-patterns

- **Variance without driver decomposition** — Δ$ alone is noise.
- **Made-up drivers** — claiming "mix shift" without showing the cohort cut.
- **Ignoring residual / interaction term** — additive decomp leaves a cross-term; if > 5% of total, name it.
- **Generic narrative** — "due to market conditions" / "macro headwinds" tells leadership nothing actionable.
- **One-period variance only** — always include 3-4 prior periods so reader can see trend vs. blip.
- **Favorable variance celebrated, unfavorable explained away** — same rigor for both directions.
- **Conflating GAAP P&L variance with SaaS-metric variance** — they answer different questions; produce BOTH.
- **No recommended action** — every variance write-up ends with one of seven verbs (Sustain / Verify / Monitor / Mitigate / Investigate / Escalate / Re-baseline).
- **Missing materiality threshold** — what counts as a variance worth analyzing should be stated, not implicit.
- **Doing the data work in this skill** — if you need to query the warehouse or build a dashboard, hand off to `data:build-dashboard` or `data:analyze`.
- **Doing the rec work in this skill** — if the variance is "the AR aging doesn't match the GL," hand off to `finance:reconciliation`.

## Output of a variance-analysis run

1. Headline: $ and %, materiality flag
2. Driver decomposition table with confidence per driver
3. Per-driver explanation with cited sources (customer, cohort, contract, vendor)
4. Multi-period context table (3-4 prior periods)
5. SaaS-metric view (separate from GAAP) when revenue-side
6. Executive narrative (3-4 sentences, business reality)
7. Recommended action (one of seven verbs) + owner + due date
8. Waterfall spec (passed to `data:build-dashboard`)
9. Suggested chain: `data:build-dashboard` for the visual; `finance:journal-entry` if a correcting entry is needed; `finance:reconciliation` if root cause is a tie-out break; `finance:audit-support` if a SOX-relevant control issue surfaced.
