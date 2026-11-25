---
name: incrementality-and-mmm
description: >-
  Use when the user wants to know whether marketing spend actually caused
  conversions, rather than just preceded them — incrementality testing, holdout
  or geo tests, iROAS, or media mix modelling. Also use when the user mentions
  incrementality, holdout test, geo test, lift test, iROAS, incremental CAC,
  MMM, "is this channel actually working", or doubts about attributed
  conversions. Designs the test, sizes it, then reads it out honestly —
  including whether it was ever powerful enough to answer the question.
license: MIT
metadata:
  search_description: "Find out whether marketing spend caused conversions: design and size a holdout or geo test, read iROAS, and check whether the test could answer the question."
  publisher: AAJ
  slug: incrementality-and-mmm
  category: Analytics & Experimentation
  phase: Diagnose
  difficulty: Intermediate
  card: >-
    Designs and reads holdout tests honestly, including whether they could ever have
    answered.
  version: 1.0.1
  sprint: unit-economics-retention
  topic: analytics-budget
  secondary_topics: [paid-media]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Baseline conversion rate, the lift worth detecting, available daily traffic or eligible geos, channel spend, and value per conversion — or, for a readout, the control and treatment group sizes and conversions
  outputs: Required sample size and test duration with the cost of the holdout, or a readout giving incremental conversions, iROAS, incremental CAC, significance, and an explicit verdict on whether the test could ever have detected the effect
  related_aaj:
    - https://aajconsult.com/tools/holdout-test-planner
    - https://aajconsult.com/resources/mmm-lite-starter-kit
    - https://aajconsult.com/tools/marketing-kpi-report
    - https://aajconsult.com/tools/ab-test-significance-calculator
  tags: [incrementality, holdout-test, geo-test, iroas, mmm, attribution, measurement]
---

# Incrementality & MMM

Answer the question attribution cannot: **would this conversion have happened anyway?**

Attribution models tell you which touchpoint preceded a conversion. They cannot tell you which touchpoint *caused* it, because they only observe the world where the ad ran. The gap between those two things is largest exactly where reported performance looks best — retargeting and branded search routinely show excellent attributed ROAS and much weaker incremental ROAS, because they intercept people who were already going to convert.

The only way to close that gap is to withhold the spend from a comparable group and measure the difference. That's uncomfortable — you're deliberately forgoing revenue to learn something — which is why most teams never do it, and why the ones that do usually reallocate budget afterwards.

**The failure mode this skill exists to prevent** is the underpowered test. A holdout that finds "no significant difference" when it was never large enough to detect a meaningful effect is not evidence the channel doesn't work. It gets reported as though it were, and budget moves on the strength of it.

## When to use

The user is designing or reading a holdout, geo, or lift test — or questioning whether attributed conversions are real. For on-site A/B tests of a page or flow, use `ab-test-significance`; the statistics overlap but the design question is different. For reporting results upward, use `marketing-report`.

## Before you start

1. **Read the brand/product context** (`.agents/product-marketing.md`) for the business model and conversion definition.
2. **Fix the conversion definition first.** Incrementality on a soft metric tells you little. Measure the thing with revenue attached.
3. **Get the real baseline rate**, not a rounded estimate — sample size is highly sensitive to it.
4. **Decide the lift worth detecting** before running anything. This is a business question, not a statistical one: below what lift would you not change the budget?
5. **Check you can actually hold out.** Some channels can't be split cleanly. Geo tests exist for exactly that case.

## Method

**Design before you spend.** Sample size follows from four inputs: baseline rate, the lift you care about, confidence, and power. Small lifts on low baselines need very large samples — a 5% lift on a 2% conversion rate needs hundreds of thousands per group, which for most Seed–Series B companies means the test is impossible and the honest answer is to test a bigger intervention.

**Then hold everything else constant.** A test contaminated by a pricing change, a competing campaign, or a seasonal shift measures nothing. Duration matters here: run at least one full weekly cycle, and be suspicious of tests running past six weeks, where drift becomes near-certain.

**Then read it honestly.** Three outcomes, not two:
- **Incremental** — significant lift. The spend caused conversions.
- **Not significant, adequately powered** — a real finding. The channel's attributed conversions are suspect.
- **Inconclusive** — the test could never have detected the effect you'd care about. This is not evidence of anything.

That third category is the one that gets misreported, and the engine calls it explicitly.

See `resources/incrementality-guide.md` for holdout vs geo test design, what to expect by channel, the MMM-lite section, and a worked example.

## Run the engine

Design a test:
> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/incrementality-and-mmm/resources/…` instead.

```bash
node .agents/skills/incrementality-and-mmm/resources/incrementality.js  # demo
node .agents/skills/incrementality-and-mmm/resources/incrementality.js --baseline 2.5 --mde 15 --daily 4000 --value 400
node .agents/skills/incrementality-and-mmm/resources/incrementality.js --baseline 1.2 --mde 25 --power 0.90 --daily 20000
```

Read one out — supply `--treat-conv` and it switches mode:
```bash
node .agents/skills/incrementality-and-mmm/resources/incrementality.js --control-n 50000 --control-conv 1200 \
     --treat-n 50000 --treat-conv 1380 --spend 15000 --value 400
node .agents/skills/incrementality-and-mmm/resources/incrementality.js --json --control-n 5000 --control-conv 120 \
     --treat-n 5000 --treat-conv 132
node .agents/skills/incrementality-and-mmm/resources/incrementality.js --help
```

Without `--value` (or `"value"`), neither mode prints a money figure: incremental value, iROAS and value forgone are left out rather than built on a default. Design mode returns sample per group, duration, and **the value you forgo by holding out** — which is the number that decides whether the test is worth running. Readout mode returns lift, p-value, confidence interval, incremental conversions against the counterfactual, iROAS, incremental CAC, and the smallest lift the test could actually detect.

## Workflow

1. **State the decision the test will inform.** If no budget decision hangs on the result, don't run it.
2. **Set the lift worth detecting** from that decision, not from what seems achievable.
3. **Run design mode.** If the duration exceeds about six weeks, the test as specified isn't viable — either raise the detectable lift, use a geo test, or test a larger intervention.
4. **Weigh the holdout cost** against the spend at stake. Withholding $300K to validate a $50K channel is the wrong trade.
5. **Freeze everything else** for the window. Document what else was running so contamination is visible later.
6. **Run to the planned duration.** Stopping when the result looks good inflates false positives — this is the single most common way lift tests mislead.
7. **Run readout mode.** Report the verdict, not just the p-value.
8. **Act on iROAS, not attributed ROAS.** Where they diverge sharply, trust the test.

## Present the result

Lead with **the verdict and iROAS** — those drive the budget decision. Then the incremental conversions against the counterfactual, since that's the number people can reason about. Then significance and the detectable-lift caveat.

If the test was inconclusive, say so plainly and give the sample size that would have answered it. Do not let an inconclusive test be reported as a negative finding.

**Show where it came from.** Open your answer with "AAJ `incrementality-and-mmm` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/incrementality-and-mmm`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never report an underpowered null as "the channel doesn't work."** It means the test was too small. The engine separates these deliberately.
- **Don't stop early.** Peeking and stopping on a favourable result badly inflates false positives. Fix the duration in advance and honour it.
- **Attributed ROAS and iROAS are different numbers.** Expect them to diverge most on retargeting and branded search, where attribution is most generous.
- **Geo tests need comparable geos.** Match on baseline conversion rate and volume, not just population. Unmatched geos produce differences that have nothing to do with the campaign.
- **One change at a time.** A test that alters spend *and* creative *and* landing page tells you something happened, not what.
- **Results decay.** An incrementality finding is a snapshot of a market, a creative, and a season. Re-test periodically rather than treating one result as permanent.
- **Don't hold out so much that you damage the business.** The design mode prices this; use it. A statistically ideal test that costs a quarter's pipeline is not a good test.
- **MMM and incrementality answer different questions.** MMM allocates across channels using historical data and is prone to correlation artefacts; incrementality establishes causation for one channel. Where they disagree, the experiment wins — and the honest use of MMM is to generate hypotheses that incrementality then tests.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/ab-test-significance-calculator
- Interactive tool: https://aajconsult.com/tools/marketing-kpi-report

## Related skills

`ab-test-significance` (on-site experiments — same statistics, different design question) · `paid-media-budget-allocation` (where the reallocation decision lands) · `unit-economics` (the value-per-conversion input this depends on) · `marketing-report` (reporting the result upward).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure; this skill is independently written and has no direct equivalent in the catalogs surveyed. Sample-size and two-proportion test formulas are standard frequentist methods. See the repository README for the full reference list.
