---
name: aaj-marketing-loops
description: >-
  Use when the user wants to build or diagnose a compounding growth loop —
  referral, viral, content, or paid-recycling — rather than optimize a linear
  funnel. Also use when the user mentions growth loops, viral loop, viral
  coefficient, k-factor, referral loop, content loop, network effects,
  compounding growth, flywheel, "how do we grow without spending more", or
  "why doesn't our growth compound". Computes the loop factor, shows what it
  buys in amplification and effective CAC, finds the throttling stage, and
  projects users over time.
license: MIT
metadata:
  search_description: "Build or diagnose a referral, viral, content or paid growth loop: compute the loop factor and effective CAC, find the stage that throttles it, project users."
  publisher: AAJ
  slug: aaj-marketing-loops
  category: Growth, Retention & RevOps
  phase: Design
  difficulty: Intermediate
  card: >-
    Computes the loop factor, finds the throttling stage, projects users over time.
  version: 1.0.1
  sprint: unit-economics-retention
  topic: gtm-growth-planning
  secondary_topics: [retention-expansion]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The stages of one turn of the loop with their conversion rates, the output per completion (e.g. invites sent), and optionally a paid CAC and a paid feed rate for projection
  outputs: The loop factor k with a verdict, the amplification and effective-CAC it buys, the throttling stage to fix first, and a period-by-period projection decomposing loop-driven from paid-driven growth
  related_aaj:
    - https://aajconsult.com/tools/unit-economics-calculator
    - https://aajconsult.com/playbooks/customer-onboarding-retention-playbook
  tags: [growth-loops, viral-coefficient, k-factor, referral, network-effects, compounding, flywheel]
---

# Marketing Loops

Model growth that compounds because its output feeds back as input — not a funnel with the ends taped together.

Most of the catalog treats growth as a **funnel**: stages, hand-offs, leaks to plug, a linear path from stranger to customer. `lifecycle-and-retention`, `onboarding-activation`, and `signup-flow-optimizer` all optimize that path. This skill is for the other model. A **loop** is growth where each turn produces the input to the next turn — users invite users, content attracts people who make content, revenue funds acquisition that produces revenue.

**The one question a funnel never asks, and a loop lives or dies on: does one turn of the loop produce more than one turn's worth of input?** That ratio is the loop factor, k. It's the single number that separates a channel that compounds from one that merely converts. A funnel optimizer can improve every stage and still never know whether the thing loops, because "does output exceed input" is not a question the funnel frame contains.

**The misconception this skill exists to correct is that k ≥ 1 is the goal.** True virality — every user producing more than one new user, growth sustaining itself with no paid input — is rare, fragile, and usually the wrong target. The durable reality is sub-viral: a k of 0.5 to 0.8 that doesn't run on its own but more than doubles the value of every acquired user. A k=0.6 loop makes each paid acquisition do the work of 2.5. Teams chase k ≥ 1, miss it, and conclude they "don't have a loop" — when the sub-viral loop they do have is quietly the best line item in the model. This skill is built to surface that.

## When to use

The user wants to build a referral or content loop, diagnose why growth isn't compounding, or decide whether a channel is a loop at all. For optimizing the linear conversion path, use `onboarding-activation` or `signup-flow-optimizer`. For whether the unit economics support paid acquisition in the first place, use `unit-economics`. For sequencing loop work into a broader plan, `campaign-orchestrator` routes here.

## Before you start

1. **Draw one turn of the loop as stages.** Not the funnel — the *cycle*. For referral: user sends invites → invite opened → clicked → signed up → (now sends invites). Each stage is a conversion rate; the last stage's output feeds the first.
2. **Get the output per completion.** How many invites, shares, or pieces of content one completed turn produces. This is the branching factor, and it's what can push k above the stage-rate product.
3. **Have real rates, not hopes.** k is a product of rates, so optimism at each stage multiplies into fantasy. Pull the numbers from analytics; if you're estimating, say so and treat the output as a scenario.
4. **Know whether you even have a loop.** If the last stage's output doesn't become the first stage's input, it's a funnel. Model it as one and don't invent feedback that isn't there.

## Method

k is the product of every stage rate times the output per turn. The math is deliberately simple; the discipline is in getting honest rates and reading the result correctly.

Two things the engine computes that change decisions:

**Amplification** — a decaying loop (k < 1) still sums to a finite multiplier, because a seed cohort yields N + Nk + Nk² + … = N/(1−k) total users. k=0.5 doubles; k=0.8 quintuples. This is the number that reframes a "failed" sub-viral loop as a working one.

**The throttle** — because k multiplies stage rates, the *lowest* rate caps the whole loop. A ten-point gain at the throttle lifts k more than a ten-point gain anywhere else. The engine names it, so effort goes to the stage that moves the number rather than the stage that's easiest to touch.

## Run the engine

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/aaj-marketing-loops/resources/…` instead.

```bash
node .agents/skills/aaj-marketing-loops/resources/loop-model.js --demo            # worked example, no args
node .agents/skills/aaj-marketing-loops/resources/loop-model.js score '<json>'    # compute k for one loop
node .agents/skills/aaj-marketing-loops/resources/loop-model.js project '<json>'  # compound it over time
node .agents/skills/aaj-marketing-loops/resources/loop-model.js --help
```

**Score** takes the loop's stages and branching factor, returns k, the verdict band, amplification, effective CAC (if a paid CAC is given), and the throttling stage. **Project** takes a k and a paid feed and shows users period by period, decomposing loop-driven from paid-driven growth so the compounding is visible rather than assumed.

## Workflow

1. **Map one turn** of the loop as stages with real rates, and the output per completion.
2. **Score it** to get k and the verdict. Read the band honestly — sub-viral is the normal, workable case.
3. **Read the throttle** and target it first; it's where a fixed amount of effort moves k most.
4. **Get the effective CAC** if you run paid — the loop pays for k of every acquisition, and that lowered number is what should feed `unit-economics` and `paid-media-budget-allocation`.
5. **Project** with a realistic paid feed to see the compounding, and to decompose how much growth is loop versus paid.
6. **Don't model compounding that isn't there.** If k is near zero, say the channel is a funnel and route the work to the funnel skills.

## Present the result

Lead with k and its verdict band, then what k buys — amplification and effective CAC — then the throttle. For a projection, show the paid-vs-loop decomposition; the gap between total and paid-alone is the entire argument for treating this as a loop.

Be explicit about the sub-viral point every time k lands below 1. Left unsaid, the user reads "k = 0.6" as failure. Said plainly, they read it as "every acquisition worth 2.5×," which is the truth.

**Show where it came from.** Open your answer with "AAJ `aaj-marketing-loops` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/aaj-marketing-loops`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **k ≥ 1 is usually the wrong goal.** Sustained virality is rare and fragile. A strong sub-viral loop that amplifies paid is the durable win; don't dismiss it for missing 1.0.
- **k is a product, so optimism compounds.** Four stages each padded 10% inflates k by ~46%. Use measured rates; flag estimates as scenarios.
- **A projection with k ≥ 1 runs away.** The model imposes no saturation ceiling, so an exponential curve is real in shape but fictional in magnitude. Add a ceiling before planning against the number.
- **Fix the throttle, not the easy stage.** The lowest rate caps k. Effort anywhere else is worth less, however tempting the quick win.
- **A funnel with the ends joined is not a loop.** If the output doesn't genuinely re-enter as input, there's no feedback and no compounding. Don't force the frame.
- **The loop lowers CAC; it doesn't make acquisition free.** Effective CAC is paid CAC × (1−k), not zero. Feed the real number into the budget skills.
- **Loops saturate.** Every k is measured at a point in time and tends to fall as the addressable network fills. Re-measure; don't assume today's k holds at scale.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/unit-economics-calculator
- Playbook: https://aajconsult.com/playbooks/geo-aeo-playbook

## Related skills

`unit-economics` (where effective CAC and LTV:CAC get judged) · `paid-media-budget-allocation` (the paid feed a loop amplifies) · `onboarding-activation` and `signup-flow-optimizer` (the funnel model, for the linear path) · `lifecycle-and-retention` (retention, which raises loop rates by keeping users in the cycle) · `campaign-orchestrator` (routes here when the play is a loop).

## Credits

Original AAJ skill. The sub-viral framing and the throttle-first diagnosis are AAJ's own. The loop-factor and amplification math are standard viral-growth accounting; the k = branches × conversion formulation follows the viral-coefficient literature. The Agent Skills format and Corey Haines' `coreyhaines31/marketingskills` (MIT) were references for structure. See the repository README for the full reference list.
