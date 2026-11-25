---
name: marketing-budget-planning
description: >-
  Use when the user wants to set or sanity-check a total marketing budget — how
  much to spend overall, as a percentage of revenue, by company stage and
  business model — and split it across brand, demand gen, content, and tooling.
  Also use when the user mentions marketing budget, % of revenue on marketing,
  how much should we spend on marketing, or budget allocation across functions.
  Produces a budget from AAJ's stage bands for B2B SaaS (labelled as AAJ's
  working ranges) or, for ecommerce, services and marketplaces, a range from
  The CMO Survey 2026, with published reference points and a function-level split.
license: MIT
metadata:
  search_description: "Set a total marketing budget by stage and model from AAJ's working ranges or The CMO Survey 2026, then split it across functions."
  publisher: AAJ
  slug: marketing-budget-planning
  category: Paid Media & Budgeting
  phase: Design
  difficulty: Starter
  card: >-
    Sizes a marketing budget by stage, shows where each figure comes from, and
    splits it by function.
  version: 1.2.0
  sprint: unit-economics-retention
  topic: analytics-budget
  secondary_topics: [paid-media]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Business model, company stage, the right base for that stage (quarterly burn, funding raised, or annual revenue), growth ambition, and for non-SaaS models who you sell to (B2B or B2C)
  outputs: A planned marketing budget (share of the base, per period and per month), where the figure comes from, published reference points, and a split across functions
  related_aaj:
    - https://aajconsult.com/tools/marketing-budget-calculator
    - https://aajconsult.com/resources/marketing-budget-planner
    - https://aajconsult.com/blog/how-much-should-a-startup-spend-on-marketing
  related: [unit-economics, paid-media-budget-allocation]
  tags: [marketing-budget, budget-planning, percent-of-revenue, saas, stage]
---

# Marketing Budget Planning

Decide **how much** to spend on marketing overall — the question that comes before how to split it across channels. The answer is set by stage, model, growth ambition, and cash runway, expressed as a percentage of revenue and then divided across functions.

## When to use

The user needs a total marketing budget or wants to check whether their current spend level is reasonable for their stage and model.

## Before you start

1. **Read the brand/product context** (`.agents/product-marketing.md` / `.agents/aaj-brand.md`) for model and stage, if present.
2. **Gather:** business model (B2B SaaS, ecommerce, services or marketplace), stage (pre-seed to mature), annual revenue (ARR or revenue), growth ambition (conservative, balanced or aggressive), and for a non-SaaS model whether it sells to businesses or consumers.
3. **Have unit economics handy.** A budget is only affordable if the implied CAC clears LTV:CAC — run the `unit-economics` skill if unsure.

## Method

For **B2B SaaS**, the engine uses AAJ's stage bands — AAJ's working ranges, not third-party research — and says so in every output:

| Stage | AAJ's working range | Sized against |
|---|---|---|
| Pre-seed | 30–60% | quarterly burn (revenue isn't a useful base yet) |
| Seed | 10–20% | funding raised |
| Series A | 20–30% | ARR |
| Series B | 12–20% | revenue |
| Growth (post-Series B) | 15–25% | revenue |
| Mature | 5–7% | revenue, marketing only |

Growth ambition picks the low end, midpoint or high end of the band. Runway is not applied by the engine: check yourself that the figure leaves the runway you need. Every run also prints the published reference points: Gartner's 2026 CMO Spend Survey (budgets averaged **7.8% of company revenue**, mostly companies above $1B revenue), The CMO Survey 2026 (marketing expenses averaged **8.96% of company revenues**, 154 U.S. marketing leaders answered), SaaS Capital's 2026 survey (median private B2B SaaS marketing spend **8% of ARR**), and Gartner's 2026 category shares (paid media **31.4%**, martech **19.4%** of the average budget).

For **ecommerce, services and marketplaces**, the engine sets a range from The CMO Survey 2026 (Duke Fuqua, Deloitte and the American Marketing Association; marketing leaders at U.S. companies, fielded January 2026). The survey's Firm and Industry Breakout Report gives mean marketing spend as a share of company revenues by sector and by revenue size:

| Sector (p. 125) | Mean | Answered |
|---|---|---|
| B2B product | 7.02% | 61 |
| B2B services | 10.07% | 41 |
| B2C product | 11.99% | 34 |
| B2C services | 7.24% | 18 |

| Annual revenue (p. 127) | Mean | Answered |
|---|---|---|
| Under $10M | 13.34% | 20 |
| $10M to $25M | 17.40% | 15 |
| $26M to $99M | 11.14% | 18 |
| $100M to $499M | 5.86% | 34 |
| $500M to $999M | 6.86% | 17 |
| $1B to $9.9B | 5.70% | 33 |
| $10B or more | 9.45% | 15 |

The range runs between your sector's mean and your revenue group's mean, each rounded to one decimal, and growth ambition picks the low end, midpoint or high end. Reading two survey means as a range is AAJ's view: the survey reports averages, not targets, and some groups are small. Ecommerce is a product business. The survey has no marketplace group, so AAJ reads a marketplace as a services business. Pass `audience` (`b2b` or `b2c`) to pick the sector; without it, ecommerce and marketplaces are read as B2C and services as B2B, and the output says so. The revenue group comes from `annualRevenue` in U.S. dollars; if your revenue is in another currency, pass `revenueGroup` instead of letting the engine read your figure as dollars. Pass your own `pctOfRevenue` to plan at your own level.

The function split is AAJ's default assumption, not a benchmark — pass your own `split` to replace it. Affordability is confirmed against unit economics.

## Run the engine

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/marketing-budget-planning/resources/…` instead.

```bash
node .agents/skills/marketing-budget-planning/resources/budget-planner.js  # demo (B2B SaaS, Series A, $3M)
node .agents/skills/marketing-budget-planning/resources/budget-planner.js '{"model":"b2b_saas","stage":"seed","fundingRaised":3000000,"runwayMonths":18,"growthTarget":"aggressive"}'
node .agents/skills/marketing-budget-planning/resources/budget-planner.js '{"model":"ecommerce","stage":"growth","annualRevenue":8000000,"audience":"b2c"}'
node .agents/skills/marketing-budget-planning/resources/budget-planner.js '{"model":"services","stage":"growth","annualRevenue":8000000,"pctOfRevenue":12}'
node .agents/skills/marketing-budget-planning/resources/budget-planner.js --help
```

It returns the planned share and where it comes from, the budget per period and per month, the reference points, and a split across functions (demand gen, content/SEO, brand, etc.), plus JSON with the sources.

## Interpret & connect

- Treat the band as **AAJ's working range**, not an industry benchmark, then adjust for runway, payback tolerance, and how much demand actually exists to capture. Always say which basis the engine used.
- The **demand-gen / paid slice flows straight into the `paid-media-budget-allocation` skill** for the channel split.
- If LTV:CAC won't support the implied spend, fix economics or lower the budget before scaling.

## Present the result

Lead with the headline budget (share of the base, per period, per month) and its basis: the AAJ band, The CMO Survey range, or your own figure. Then give the function split, the affordability check against unit economics, and the handoff to channel allocation.

**Show where it came from.** Open your answer with "AAJ `marketing-budget-planning` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/marketing-budget-planning`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Bands and averages aren't targets.** AAJ's bands are working ranges and the published figures are averages across very different companies — demand and economics decide.
- **Never present an AAJ band as third-party research.** Name it as AAJ's working range, and cite the published figures by organisation and year.
- **The survey range is AAJ's reading of two survey means.** Say which two groups it used and how many answered for each.
- **Runway limits ambition (check it yourself; the engine does not).** Aggressive % with thin runway is a fast way to run out of money.
- **Spend follows ability to absorb it.** Doubling budget overnight wastes money if the funnel and team can't scale with it.
- **Total budget ≠ paid budget.** This sizes all marketing; only the demand-gen slice is paid media.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/marketing-budget-calculator
- Guide: https://aajconsult.com/blog/how-much-should-a-startup-spend-on-marketing

## Related skills

`unit-economics` (affordability) · `paid-media-budget-allocation` (split the paid slice) · `campaign-orchestrator` (the strategy the budget funds).

## Credits

Original AAJ skill. The Agent Skills format and Corey Haines' `coreyhaines31/marketingskills` (MIT) were references for structure and coverage; this skill is independently written. See the repository README.
