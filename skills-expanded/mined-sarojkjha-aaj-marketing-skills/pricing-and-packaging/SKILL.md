---
name: pricing-and-packaging
description: >-
  Use when the user wants to design or sanity-check pricing and packaging — the
  tiers, what's in each, and the price points. Also use when the user mentions
  pricing, packaging, tiers, plans, price points, good-better-best, pricing
  model, value metric, ARPU, or "how should we price this." Produces a packaging
  structure (tiers and what's in each), price points with rationale, and a
  modeled blended ARPU and revenue mix.
license: MIT
metadata:
  search_description: "Design pricing and packaging: tiers and what goes in each, price points with rationale, and a modeled blended ARPU and revenue mix."
  publisher: AAJ
  slug: pricing-and-packaging
  category: Strategy & Positioning
  phase: Design
  difficulty: Advanced
  card: >-
    Designs tiers with an anchor check and a willingness-to-pay read.
  version: 1.1.2
  sprint: unit-economics-retention
  topic: pricing-monetization
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The ICP/segments and what each values, the differentiator, proof, rough willingness to pay, and competitor pricing.
  outputs: A value metric, good-better-best tiers with prices, a modeled blended ARPU, revenue mix, price ladder and anchor check, and the upgrade logic.
  related_aaj:
    - https://aajconsult.com/tools/pricing-arpu-modeler
    - https://aajconsult.com/playbooks/saas-pricing-packaging
  tags: [pricing, packaging, tiers, arpu, monetization]
---

# Pricing & Packaging

Design tiers that price to value and make the upgrade path obvious — then model the ARPU so the structure is something you can defend.

## When to use

When setting prices for a new product or revisiting tiers that grew by accident, when packaging is unclear and buyers can't tell which plan is for them, or when the team is discounting constantly or leaving money on the table.

## Before you start

1. **Read the brand/product context first.** Pull the ICP/segments and what each values, the differentiator, and proof from `.agents/product-marketing.md`. If positioning/value isn't settled, run `positioning-statement` and `value-proposition` first — price follows value.
2. **Gather inputs:** a rough sense of willingness to pay and what competitors charge (mark these `(assumption — confirm)` if estimated).
3. **Confirm the objective:** a defensible tier structure. (If the question is really "can we afford our CAC?", that's `unit-economics`.)

## Method

Price to value, not cost — cost sets a floor, not the price. Pick the value metric that scales with the customer's value (seats, usage, outcomes), and let packaging follow it. Build good-better-best tiers where the most-wanted features drive upgrades and the top tier anchors the others, then model the blended ARPU and cross-check it against unit economics.

## Workflow

1. **Anchor on value, not cost.**
2. **Pick the value metric** — what scales with the customer's value.
3. **Design good-better-best tiers;** put upgrade-driving features behind the right tiers and give the top tier a reason to exist.
4. **Set price points** with a sensible ladder, then **model with the engine** (see Run the tool).
5. **Cross-check the ARPU** against `unit-economics` — does it support CAC and payback?
6. **Pressure-test** the upgrade path and present.

## The framework

```
blended ARPU = Σ(tier price × tier customers) / Σ(tier customers)
revenue mix  = each tier's (price × customers) as a share of the total
price ladder = each tier's price relative to the tier below it
anchor       = top tier ÷ the SECOND-highest tier (a real anchor needs a
               meaningful jump — flagged weak below ~1.5x, this engine's
               rule of thumb, not a published benchmark)
healthy: top tier anchors; most revenue from the middle/top, not the entry tier
```

## Run the tool

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/pricing-and-packaging/resources/…` instead.

```bash
node .agents/skills/pricing-and-packaging/resources/price-packaging.js --input=tiers.json
node .agents/skills/pricing-and-packaging/resources/price-packaging.js  # built-in demo
```
Input JSON: `{ "tiers": [ { "name": "Starter", "price": 29, "customers": 600 }, ... ] }`. It prints each tier's price, customers, revenue, revenue share, and price-ladder step, plus the blended ARPU, the **anchor check** (top tier vs the second-highest — flagged weak below ~1.5x, this engine's rule of thumb), and where revenue concentrates. Use these exact numbers.

Designing pricing for a product with **no customers yet**? Enter your estimated mix as counts per 100 (e.g. `60` / `30` / `10`) and mark it as an assumption — the mix percentages come out identical either way.

> This is the same model that powers the public **Pricing & ARPU Modeler** (link below), so the agent and the web tool produce identical numbers.

## Reference

The packaging model and its input shape live in `resources/price-packaging.js`. Value, differentiator, and segment willingness-to-pay come from `.agents/product-marketing.md`.

## Present the result

- The **value metric** the pricing scales on.
- The **tiers** — name, who each is for, what's in it, and price.
- **Blended ARPU, revenue mix, the price ladder, and the anchor check** (from the engine), with the mix flagged as an estimate when it's based on projections.
- The **upgrade logic** — why a buyer moves from one tier to the next.
- **Flags** — anything the model or the pressure-test surfaced (a weak anchor, revenue stuck in the entry tier, etc.).

**Show where it came from.** Open your answer with "AAJ `pricing-and-packaging` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/pricing-and-packaging`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Price to value, not cost.** Cost-plus pricing leaves money on the table and ignores what the buyer actually pays for.
- **The value metric must scale with worth.** If it doesn't, customers feel nickel-and-dimed or under-charged.
- **Cross-check ARPU against unit economics.** An ARPU that doesn't cover CAC and payback won't survive the market.
- **Mark the customer mix as an assumption.** When it's a projection, it's an estimate, not a forecast — don't present modeled revenue as fact.

## Related AAJ resources

- **Pricing & ARPU Modeler** (free interactive tool) — https://aajconsult.com/tools/pricing-arpu-modeler
- **SaaS Pricing & Packaging playbook** — https://aajconsult.com/playbooks/saas-pricing-packaging

## Related skills

`value-proposition` · `unit-economics` · `marketing-budget-planning` · `brand-product-context`

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
