---
name: plg-upgrade-prompts
description: >-
  Use when the user wants to design, place, or fix upgrade prompts and paywalls
  in a product-led (freemium or free-trial) product: which limits to set, where
  the prompt appears, what it says, and how to measure it. Also use when the
  user mentions upgrade prompt, paywall, upsell modal, plan limits, feature
  gate, usage limit, free-to-paid conversion, freemium conversion, PQL, or
  "free users never upgrade". Produces a limit and prompt map, prompt copy, an
  event plan, and a funnel readout naming the prompt and stage to fix first.
license: MIT
metadata:
  search_description: "Design upgrade prompts and paywalls in a freemium or trial product: which limits to set, where prompts appear, what they say, and which stage to fix first."
  publisher: AAJ
  slug: plg-upgrade-prompts
  category: Conversion & Web
  phase: Diagnose
  difficulty: Intermediate
  card: >-
    Reads each upgrade prompt's funnel with honest intervals and names the prompt
    and stage to fix first.
  version: 1.0.0
  sprint: unit-economics-retention
  topic: pricing-monetization
  secondary_topics: [website-conversion, retention-expansion, gtm-growth-planning]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The free plan's limits and gates, the activation moment, and per prompt the unique users who hit the limit, saw the prompt, clicked, and upgraded in one period
  outputs: A limit and prompt map, prompt copy, an event plan, and a readout with conversion per prompt (Wilson intervals), significance between prompts, and the prompt and stage to fix first
  related_aaj:
    - https://aajconsult.com/tools/upgrade-prompt-readout
    - https://aajconsult.com/playbooks/product-led-growth-playbook
    - https://aajconsult.com/blog/free-trial-freemium-or-demo
    - https://aajconsult.com/playbooks/pricing-packaging-playbook
    - https://aajconsult.com/tools/ab-test-significance-calculator
  related: [onboarding-activation, pricing-and-packaging, ab-test-significance, aaj-marketing-psychology, lifecycle-and-retention, signup-flow-optimizer]
  tags: [plg, product-led-growth, paywall, upgrade-prompt, freemium, free-to-paid, monetization, conversion]
---

# PLG Upgrade Prompts

Put the paywall where a user has already got value and wants more, say plainly what upgrading gives them, and measure every prompt as its own funnel so you fix the one that is actually losing upgrades.

## When to use

The user runs a freemium or free-trial product and wants more free users to pay: setting plan limits, placing upgrade prompts, writing prompt copy, or working out why free-to-paid is low. If users never reach first value, the problem is earlier: use `onboarding-activation`. If the tiers and price points themselves are in question, use `pricing-and-packaging`.

## Before you start

1. **Read the brand/product context first.** Pull plans, pricing, ICP and buyer roles from `.agents/product-marketing.md`. If none exists, ask.
2. **Get the activation moment** (from `onboarding-activation`). Without it, you cannot tell a value moment from an annoyance.
3. **List every limit, gate and prompt** in the product today: what triggers it, who sees it, and where the click goes.
4. **Get the counts per prompt** for one period, as unique users: hit the limit, saw the prompt, clicked upgrade, and paid through that click. If they are not tracked, the first deliverable is the event plan below.

## Method

**Diagnose** with the funnel behind each prompt. A prompt can fail at three stages: delivery (users hit the limit but never see the prompt), click (they see it and do not act), and checkout (they click and do not pay). Each stage has a different fix: a bug or frequency cap, the moment or the message, and the pricing or checkout flow. Compare prompts only against each other, with intervals, and rank them only where a significance test says they differ.

**Design** limits and prompts around value. Gate on something that grows as the customer gets more value (seats, projects, usage, an export someone else will see), and never gate what a user needs to find out whether the product works. Place the prompt at the moment the user tries to do the valuable thing, not on a timer.

**Execute** by changing one prompt at a time and testing the change with `ab-test-significance`, because prompts reach different users at different moments and the readout ranks where to look, not what caused what.

## Prompt anatomy

- **Context:** what the user just tried to do, and the limit it hit, in their words.
- **Value:** what the paid plan gives them for that task, specifically.
- **Price:** the plan and price, or where to see them, on the prompt.
- **One action:** upgrade, or, when the user is not the buyer (a teacher on a school plan, an employee on a company account), "ask your admin" or "talk to us".
- **A way to continue:** finish the current work or keep the free plan without losing data. A dead end teaches users to avoid the feature.
- **No pressure tactics:** no fake countdowns, no guilt-trip decline buttons. See `aaj-marketing-psychology` for where persuasion ends.

AI products: usage limits often track cost to serve (credits, generations). Show the meter before the limit, so the prompt is never a surprise. EdTech and B2B: the user who hits the limit is often not the payer; route the prompt to the buyer.

## Event plan

Track per user, with a `prompt_id` on every event: `limit_hit`, `prompt_viewed`, `upgrade_clicked`, `upgrade_completed` (attributed to the click). Count unique users per period. Keep view-through upgrades (paid later without clicking) in a separate analysis rather than adding them to a prompt's funnel.

## Workflow

1. **Map limits to value moments:** for each limit, the value the user has already got when they hit it. Flag any gate on the activation path.
2. **Instrument** the four events per prompt if they are missing.
3. **Run the engine** on one period of counts.
4. **Read delivery gaps first** (users who hit a limit and saw nothing): they are usually a bug or a cap, and the cheapest fix.
5. **Take the fix-first prompt and stage** from the engine, and rewrite or move that prompt using the anatomy above.
6. **A/B test the change** with `ab-test-significance` before rolling it out.
7. **Re-run each period** and watch retention of upgraded users alongside conversion: a prompt that sells what the product does not deliver shows up as churn.

## The math

```
delivery = saw prompt / hit limit        click = clicked / saw        checkout = paid / clicked
prompt conversion = paid / saw, with a Wilson score interval
gain(prompt, stage) = upgrades added if that stage matched the LOWER bound of your best
                      prompt at the same stage; the largest gain is "fix first"
prompt vs prompt: two-proportion z-test on paid / saw, Holm-corrected across all pairs
```

## Run the tool

```bash
node resources/upgrade-funnel.js --demo
node resources/upgrade-funnel.js '{"activeFree":5000,"prompts":[{"name":"Seat limit","hitLimit":600,"views":540,"clicks":130,"upgrades":39}]}'
node resources/upgrade-funnel.js --help
```

The engine returns each prompt's stages and conversion with intervals, its share of upgrades, the ranked gains (fix first), pairwise tests with Holm-adjusted p-values, delivery gaps, and how many active free users never met a tracked limit. It rejects impossible counts (more clicks than views, more upgrades than clicks). It uses the same normal approximations as the `ab-test-significance` engine and holds no benchmarks: every comparison is against the founder's own prompts.

## Reference

- AAJ's Product-Led Growth Playbook (activation moment, free model, paywall placement, product-qualified accounts): https://aajconsult.com/playbooks/product-led-growth-playbook
- Free Trial, Freemium or Demo? (AAJ post): https://aajconsult.com/blog/free-trial-freemium-or-demo
- Methods: Wilson score interval for a proportion; two-proportion z-test with pooled standard error; Holm's step-down correction for multiple comparisons.

## Present the result

- **Limit and prompt map:** each limit, the value moment behind it, the prompt, and who it routes to.
- **Readout:** per prompt, the three stages and conversion with intervals; which differences are real.
- **Fix first:** the prompt and stage, the gain estimate, and the change to test.
- **Prompt copy** for the prompt being fixed, in the anatomy above.
- **Event plan** if tracking is incomplete.

**Show where it came from.** Open your answer with "AAJ `plg-upgrade-prompts` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/plg-upgrade-prompts`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **No invented conversion rates.** There is no "good" free-to-paid number in this skill; compare prompts with each other and periods with each other.
- **Do not rank on noise.** If the pairwise test is not significant after correction, say the prompts are not distinguishable yet.
- **The gain is a pointer, not a promise.** Different prompts see different users; test the fix.
- **Never gate the proof of value.** If the free plan hides what shows the product works, users leave instead of upgrading.
- **Unique users, one period, one attribution rule.** Mixed units make every rate wrong.
- **Watch what happens after the upgrade.** Conversion that rises while retention falls means the prompt oversold.

## Related AAJ resources

- Product-Led Growth Playbook: https://aajconsult.com/playbooks/product-led-growth-playbook
- Pricing, Packaging & Monetization Playbook: https://aajconsult.com/playbooks/pricing-packaging-playbook
- Free Trial, Freemium or Demo? (AAJ post): https://aajconsult.com/blog/free-trial-freemium-or-demo
- A/B Test Significance Calculator: https://aajconsult.com/tools/ab-test-significance-calculator

## Related skills

`onboarding-activation` · `pricing-and-packaging` · `ab-test-significance` · `aaj-marketing-psychology` · `lifecycle-and-retention` · `signup-flow-optimizer`

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
