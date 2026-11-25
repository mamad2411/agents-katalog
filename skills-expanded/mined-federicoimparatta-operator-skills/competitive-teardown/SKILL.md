---
name: competitive-teardown
description: Use this skill when the user asks to study a competitor's product surface, flow, or feature by inspecting what they actually shipped. Trigger phrases include "competitive teardown", "competitor analysis", "teardown of X", "análisis de competencia", "tear apart their onboarding", "how does competitor X do Y". Produces a structured teardown grounded in observed behavior, not marketing claims. Works in English and Rioplatense Spanish.
---

# competitive-teardown

> **Anchor:** Discovery is a practice. Study what they shipped, not what they claim.

## When to use

Use this skill when the user needs to take apart a competitor's product to understand a specific surface or flow, compare it against their own product, and find the gap they can credibly own. Works for:

- A competitor surface or flow the team keeps hearing about and wants to understand firsthand.
- A feature decision that needs a grounded view of how others solved the same problem.
- A positioning question that needs evidence of what rivals bet on and what they ignored.

Do not use when:

- The user wants to synthesize user research or interviews. Use `interview-synthesis` instead.
- The user is making a buying decision about a tool or vendor, not a competitive study. Use `vendor-evaluation`.

## Philosophy

Discovery is a practice, not a phase. A teardown is discovery aimed at a competitor instead of a user. The discipline is the same: observe before you conclude, and trust behavior over narrative.

Marketing pages tell you what a company wants you to believe. The shipped product tells you what they actually decided. A teardown closes that gap. It walks the real flow, notes the real decisions, and reads the tradeoffs the team made under pressure. The output is not a feature list. It is a map of bets: what they committed to, what they skipped, and the seam in between where your product can win. A teardown that only restates the competitor's pitch has failed. The value is in what the competitor would not put on a slide.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: onboarding, flow, feature, paywall, churn, funnel, stakeholder, rollout, AB test, KPI. Do not translate those to Spanish equivalents that no one uses in meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the audience that will read the teardown, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. Scope: which surface or flow, not the whole company

Pick one surface or one flow. Onboarding, the upgrade path, the empty state, the core create-loop. A teardown of "the whole product" is a brochure, not a teardown. Name the surface in one line and hold to it.

### Step 2. Walk the actual flow and note decisions

Go through the flow as a real user would. At each step, record the decision the competitor made, not just what the screen shows. A required field is a decision. A skipped step is a decision. Default values, copy tone, and the order of asks are all decisions. Capture friction and where they removed it.

### Step 3. Feature matrix vs your product on the dimensions that matter to the user

Build a comparison on the dimensions a user actually feels, not every feature that exists. Compare the competitor against your product. Mark where each one is stronger, weaker, or absent. Drop dimensions no user would notice. Use `templates/en/feature-matrix.md`.

### Step 4. What they bet on and what they ignored

Read the tradeoffs. Every product invests heavily in some things and accepts cost on others. Name what the competitor clearly prioritized and what they let slide. The gaps are as informative as the strengths.

### Step 5. The gap you can credibly own

Find the seam. Where is the competitor weak in a way that matches your strength or your users' need. Be honest about credibility: a gap you cannot deliver on is not a gap you own. State the wedge in one sentence.

### Step 6. What not to copy and why

Name the parts that look good but would be wrong for your product. A competitor's choice fits their users, their stage, and their constraints, not yours. Write down what you are deliberately not copying and the reason, so no one relitigates it later.

## Templates

- `templates/en/teardown-report.md`: structured teardown of a single surface or flow.
- `templates/en/feature-matrix.md`: comparison table of competitor versus your product.
- `templates/es/teardown-report.md`: teardown estructurado de una superficie o flow.
- `templates/es/feature-matrix.md`: tabla comparativa del competidor contra tu producto.

## Related skills

- `feature-proposal`: use it when the teardown surfaces a gap worth turning into a pre-scoping bet.
- `roadmap-from-data`: use it to fold teardown findings into roadmap priorities alongside usage data.
- `interview-synthesis`: use it when the question is about user research and interviews, not a competitor study.
- `vendor-evaluation`: use it when the work is a buying decision about a tool or vendor, not a competitive study.

## Anti-patterns

This skill must never produce:

- A teardown that restates the competitor's marketing claims as fact.
- A teardown of the whole company instead of one surface or flow.
- A feature matrix with dimensions no user would ever notice.
- A teardown that lists features without naming the decisions behind them.
- A teardown that finds a gap the user's product cannot credibly deliver on.
- A teardown that skips the "what not to copy" section and treats the competitor as a checklist.
- A teardown that confuses what the competitor says with what the competitor shipped.
- A teardown written as a sales pitch for the user's own product.
- A teardown that mixes English and Spanish inconsistently within a single section.
- A teardown that cites "industry best practice" without a concrete observed reason.

## Checklist before delivery

- [ ] Scope is one surface or flow, named in a single line.
- [ ] Each flow step records a decision, not just a screenshot description.
- [ ] Feature matrix dimensions are ones a user actually feels.
- [ ] The bets-and-ignored section names both what they prioritized and what they let slide.
- [ ] The gap you can credibly own is a single sentence and is honestly deliverable.
- [ ] The "what not to copy" section names at least one item with a reason.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] Document reads cleanly to a stranger who never saw the competitor's product.
