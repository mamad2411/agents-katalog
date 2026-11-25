---
name: unit-economics
description: >-
  Use when the user wants to calculate or sanity-check unit economics — LTV,
  CAC, the LTV:CAC ratio, and CAC payback — for a subscription, ecommerce, or
  services business. Also use when the user mentions lifetime value, customer
  acquisition cost, payback period, churn, contribution margin, or "are our
  unit economics healthy / can we afford to spend more." Produces the metrics
  plus a verdict against named reference points (Skok, Bessemer) and what to fix.
license: MIT
metadata:
  search_description: "Calculate LTV, CAC, the LTV:CAC ratio and CAC payback for a subscription, ecommerce or services business, with a verdict against named reference points."
  publisher: AAJ
  slug: unit-economics
  category: Analytics & Experimentation
  phase: Diagnose
  difficulty: Starter
  card: >-
    Computes LTV, CAC, payback and the ratio, then returns a verdict against
    named reference points.
  version: 1.2.0
  sprint: unit-economics-retention
  topic: analytics-budget
  secondary_topics: [pricing-monetization]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Business model, revenue per customer (ARPA/ACV/AOV), gross margin, retention or churn, and CAC (or ad spend + customers)
  outputs: LTV, CAC, LTV:CAC, CAC payback, and a verdict against the 3:1 and payback reference points, with sources
  related_aaj:
    - https://aajconsult.com/tools/unit-economics-calculator
    - https://aajconsult.com/blog/ltv-cac-which-number-to-fix
  related: [paid-media-budget-allocation, marketing-budget-planning]
  tags: [unit-economics, ltv, cac, ltv-cac, payback, churn, saas-metrics]
---

# Unit Economics & LTV:CAC

Establish whether a business can profitably acquire customers — the foundation under every budget and growth decision. Get **LTV**, **LTV:CAC**, and **CAC payback**, then judge them against named reference points. This is usually the first thing to run before any paid-media or budget work.

## When to use

The user needs to compute or validate unit economics, set a CAC ceiling, or answer "can we afford to spend more?"

## Before you start

1. **Read the brand/product context first** (`.agents/product-marketing.md` / `.agents/aaj-brand.md`) for model and pricing, if present.
2. **Gather inputs for the model:**
   - **Subscription:** monthly revenue per account (ARPA), or MRR and the number of paying customers so the engine works ARPA out; gross margin %, monthly churn % (or average lifetime in months), and CAC. Pass churn as a percentage: 3 for 3%, 0.9 for 0.9%. Values below 0.1 are rejected as likely proportions; for churn that low, pass lifetime in months.
   - **Ecommerce:** average order value, gross margin %, orders per year, retention in years, and CAC.
   - **Services / contract:** average contract value, gross margin %, retention in years, and CAC.
   - If CAC isn't known, supply ad spend and customers acquired to derive blended CAC.
   - Optional: the LTV:CAC ratio the founder wants to hold (`"targetLtvCac"`, default 3, David Skok's reference point).

## The math

```
Subscription:  LTV = (ARPA_monthly × grossMargin%) ÷ monthlyChurn%
               CAC payback (months) = CAC ÷ (ARPA_monthly × grossMargin%)
Ecommerce:     LTV = AOV × grossMargin% × ordersPerYear × retentionYears
Services:      LTV = ACV × grossMargin% × retentionYears
Everywhere:    LTV:CAC = LTV ÷ CAC
               CAC ceiling = the lower of  LTV ÷ target ratio
                                       and monthly gross profit × payback-bar months
               (the payback part applies only when a payback bar does)
```

Always use **gross-margin** LTV (revenue × margin), not revenue LTV — revenue you don't keep can't pay back acquisition.

## Run the engine

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/unit-economics/resources/…` instead.

```bash
node .agents/skills/unit-economics/resources/unit-economics.js  # demo (subscription)
node .agents/skills/unit-economics/resources/unit-economics.js '{"model":"ecommerce","aov":80,"grossMargin":60,"ordersPerYear":3,"retentionYears":2,"cac":40}'
node .agents/skills/unit-economics/resources/unit-economics.js --help
```

It prints LTV, LTV:CAC, payback, and a verdict, plus a JSON block.

## Interpret the result

- **LTV:CAC above 3:1** is David Skok's reference point for SaaS ([SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/)); he notes the best SaaS businesses sometimes reach 7 or 8. Below 3:1, fix economics before scaling spend. For ecommerce and services the engine shows 3:1 as a SaaS reference point, not a benchmark for those models. A very high ratio can mean under-investment if demand exists — that's AAJ's read, not a benchmark.
- **CAC payback:** Skok puts the line at 12 months for SaaS. Bessemer's guideline ([Scaling to $100 Million](https://www.bvp.com/atlas/scaling-to-100-million), 2021) varies by segment: under 12 months for SMB, 18 for mid-market, 24 for enterprise — set `"segment"` to use it. There is no sourced payback guideline in this skill for ecommerce or services; set `"paybackTargetMonths"` from your own cash runway to get a verdict.
- **CAC ceiling:** the most you can pay to win a customer and still hold the ratio target and, where a bar applies, the payback bar. The engine names which one sets it. It is arithmetic on the inputs, not a benchmark; a founder raising the target ratio lowers the ceiling.
- The biggest LTV levers are usually **retention/churn and margin**, not ARPA. A small churn improvement compounds through LTV.

## Present the result

Lead with the three numbers (LTV, LTV:CAC, payback), then the verdict and the CAC ceiling, then the one or two highest-leverage fixes. State that LTV is gross-margin based.

**Show where it came from.** Open your answer with "AAJ `unit-economics` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/unit-economics`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Use gross-margin LTV**, never revenue LTV.
- **Be honest about churn.** Early-stage churn estimates are often optimistic; if unsure, model a range.
- **Blended vs paid CAC.** Blended CAC (all new customers ÷ all S&M) flatters paid efficiency; for channel decisions use paid CAC. Say which you used.
- **Don't over-trust a single ratio.** A healthy LTV:CAC with 24-month payback can still strain a cash-tight business.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/unit-economics-calculator

## Related skills

`paid-media-budget-allocation` (uses the CAC ceiling this produces) · `marketing-budget-planning` · `lifecycle-and-retention` (the biggest LTV lever).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
