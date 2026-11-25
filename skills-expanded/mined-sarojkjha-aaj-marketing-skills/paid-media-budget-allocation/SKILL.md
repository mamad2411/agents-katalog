---
name: paid-media-budget-allocation
description: >-
  Use when the user wants to plan, split, or optimize a paid advertising budget
  across channels (Google, Microsoft, LinkedIn, Meta, TikTok, YouTube, Amazon,
  Capterra/G2, and more) to hit a CAC target or a customer goal. Also use when
  the user mentions ad budget allocation, channel mix, media plan, paid spend
  split, CAC target, marginal CAC, diminishing returns, or "how should I split
  my ad spend." Produces a defensible per-channel allocation with projected
  customers, blended CAC, LTV:CAC, payback, and pacing.
license: MIT
metadata:
  search_description: "Split a paid ad budget across Google, LinkedIn, Meta and more to hit a CAC target or customer goal, with projected customers, blended CAC and payback."
  publisher: AAJ
  slug: paid-media-budget-allocation
  category: Paid Media & Budgeting
  phase: Design
  difficulty: Intermediate
  card: >-
    Splits spend across channels to hit a CAC target, with diminishing returns
    modelled.
  version: 1.1.0
  sprint: unit-economics-retention
  topic: paid-media
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Business model, monthly budget OR CAC target OR customer goal, LTV, and per-channel CPC / click-to-lead % / lead-to-customer % (or cost-per-lead for directories)
  outputs: A per-channel budget split with projected customers, blended CAC, LTV:CAC, ROAS, payback, and weekly/daily pacing
  related_aaj:
    - https://aajconsult.com/tools/paid-media-budget-allocator
    - https://aajconsult.com/playbooks/paid-media-budget-allocation-playbook
  related: [unit-economics, marketing-budget-planning, ab-test-significance]
  tags: [paid-media, ppc, budget, cac, channel-mix, media-planning, ltv-cac]
---

# Paid Media Budget Allocation

Allocate a paid advertising budget across channels by **cost per customer**, not gut feel — funding each channel until the cost of its *next* customer reaches the target, so the marginal cost of a customer is roughly equal everywhere. This is the most customers a given budget can buy.

## Before you start

1. **Read the brand/product context first.** If a context file exists (e.g. `.agents/product-marketing.md`, `.agents/aaj-brand.md`, or similar), read it for the product, audience, pricing, and positioning. If none exists, ask the user for the essentials below before allocating.
2. **Establish the unit economics.** You need: business model (B2B SaaS / ecommerce / local-services / marketplace), average contract or order value, gross margin, and gross-margin **LTV** per customer. If LTV is unknown, help the user estimate it (or invoke the `unit-economics` skill) before continuing.
3. **Confirm the objective** — one of: a fixed **monthly budget**, a **CAC target**, or a **customer goal**.

## Method

1. **Set the CAC ceiling from LTV.** David Skok's SaaS guidance puts LTV:CAC **above 3:1** ([SaaS Metrics 2.0](https://www.forentrepreneurs.com/saas-metrics-2/)). Work backwards: ceiling ≈ LTV ÷ 3. This is the most you should pay per customer from ads (blended). Note this is *paid-media* CAC; fully-loaded CAC is higher.
2. **Pick the channel set for the model.** Don't run every channel — pick the 3–5 where the buyer actually researches and purchases. See `resources/channel-benchmarks.md` for the default set per model.
3. **Get a base CAC per channel** from the funnel inputs (formula below). This is the cost per customer at efficient, modest spend.
4. **Allocate against diminishing returns.** Each channel gets more expensive as you scale (you exhaust the best-matched audience), so the cheapest channel is *not* where all the budget goes. Fund each channel until the cost of its next customer hits the target, then stop. Channels whose first customer already costs more than the target drop out — correctly.
5. **Present the split** with projected customers, blended CAC, LTV:CAC, ROAS, payback, and pacing, plus guardrails.

## The math

For each channel:

```
Cost per lead (CPL)   = CPC ÷ (click→lead %)
Base CAC              = CPL ÷ (lead→customer %)
  · Pay-per-lead channels (Capterra/G2): CPL is a direct input, so Base CAC = CPL ÷ (lead→customer %)

Saturation (diminishing returns), with cap = scale headroom, DR = aggressiveness:
  customers(spend)    = (cap / (BaseCAC · DR)) · ln(1 + DR · spend / cap)
  marginalCAC(spend)  = BaseCAC · (1 + DR · spend / cap)        # cost of the NEXT customer
  spendForMarginal(λ) = 0 if λ ≤ BaseCAC, else (cap / DR) · (λ / BaseCAC − 1)
```

Allocation by objective:
- **Budget:** binary-search a single marginal-CAC level λ so the sum of `spendForMarginal(λ)` across channels equals the budget (water-filling).
- **CAC target T:** set each channel's spend to `spendForMarginal(T)`.
- **Customer goal G:** binary-search λ so total customers equal G.

DR presets: **gentle 0.4 · moderate 0.8 (default) · aggressive 1.5.**

## Run the engine (preferred in a coding agent)

Don't approximate the water-filling by hand — run the bundled engine for exact numbers.

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/paid-media-budget-allocation/resources/…` instead.

```bash
# Demo: B2B SaaS, 30k USD budget
node .agents/skills/paid-media-budget-allocation/resources/allocation-engine.js

# Custom — pass a JSON config
node .agents/skills/paid-media-budget-allocation/resources/allocation-engine.js '{"model":"saas","mode":"budget","budget":30000,"diminishingReturns":"moderate","channels":[{"key":"capterra","model":"cpl","cpl":90,"l2c":22,"cap":8000}]}'

# Schema and channel keys
node .agents/skills/paid-media-budget-allocation/resources/allocation-engine.js --help
```

The engine prints a per-channel table plus a JSON block you can parse. Always seed the per-channel inputs with the user's own account data; the defaults exist so the engine runs.

## Channel defaults

To run on the user's numbers alone, add `"onlyListedChannels": true`: the engine then uses only the channels listed (each needs `cpc`, `cvr`, `l2c` and `cap`, or `cpl`, `l2c` and `cap`), no preset LTV, ACV or margin, and skips LTV:CAC, ROAS or payback when their input is missing. The default channel set per business model and placeholder CPC / conversion / close-rate numbers are in `resources/channel-benchmarks.md`. They are AAJ's illustrative defaults, not benchmarks, and aren't traced to a published survey. Say so whenever an output still uses them, and replace them with the client's own numbers before anyone budgets from the result.

## Present the result

Use the format in `resources/output-format.md`: the split (channel, $, %, customers, CAC), the blended summary (customers, CAC, LTV:CAC, ROAS, payback), weekly/daily pacing, and a short "what this means" with guardrails.

**Show where it came from.** Open your answer with "AAJ `paid-media-budget-allocation` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/paid-media-budget-allocation`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Optimize on customers/revenue, not cost-per-lead.** Cheap leads that never close are the most expensive thing in paid media.
- **Don't pour everything into the cheapest channel** — average CAC hides diminishing returns; the next customer there may already cost more than elsewhere.
- **Right-size the channel count.** Three to five channels funded above their learning minimums beat many channels starved of budget. If two or more channels would get under about 1,500 USD a month, recommend consolidating (the engine flags this; 1,500 USD is this engine's rule of thumb, not a platform minimum).
- **Mind attribution and lag.** In B2B, deals close weeks after the click — track ROAS to 90 days and year one, not month one.
- **Rebalance monthly, not daily.** Large budget swings reset platform learning; give a change two to four weeks.
- **Be explicit that this is paid-media CAC.** Fully-loaded CAC (salaries, tools, content) is higher, so LTV:CAC and payback here reflect ad efficiency only.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/paid-media-budget-allocator
- Full method (the "why"): https://aajconsult.com/playbooks/paid-media-budget-allocation-playbook

## Related skills

`unit-economics` (LTV and the CAC ceiling) · `marketing-budget-planning` (how much to spend in total) · `ab-test-significance` (prove a channel's lift before scaling) · `marketing-report` (measure customers, not form fills).

## Credits

Original AAJ skill. The Agent Skills format and the broader marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written and grounded in AAJ's own tool and methodology. See the repository README for the full reference list.
