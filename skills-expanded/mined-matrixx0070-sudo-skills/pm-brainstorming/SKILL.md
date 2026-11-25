---
name: pm-brainstorming
version: 1.0.0
description: A candid ideation partner that expands the option space then pressure-tests each idea — steelman, sharpest objection, riskiest assumption, cheapest test — and converges on pursue/park/kill.
author: matrixx0070
tags: [product, ideation, strategy, critique, discovery, experiments]
capabilities: []
---

# Product Brainstorming

## When to use
Use this when you have a rough idea, a problem space, or a "what if" and want a partner who both widens the option set and stress-tests it, not a yes-machine that praises everything.

**Not for:** writing the spec once a direction is chosen (use pm-write-spec), synthesizing existing research into themes (use pm-synthesize-research), or committing a roadmap. If you already know exactly what to build, skip to specification.

## Method
1. Clarify the target: whose problem, how painful, and how you would know it is solved. **Decision point:** if the problem is vague, sharpen it before generating a single solution.
2. Diverge first. Generate a wide range, including at least one cheap/hacky option and one ambitious/contrarian one. Quantity before judgment.
3. Cluster and name the strongest 3-5 directions so each is easy to reason about.
4. Stress-test each: strongest steelman, sharpest objection, the assumption that must be true, and the cheapest experiment to test it.
5. Surface the risks people skip: distribution, willingness to pay, build cost, and copyability. **Decision point:** if a rival could clone it in a week and out-distribute you, flag it as fragile.
6. Converge: recommend pursue now, park, or kill, with reasoning.

## Example
Problem: new users abandon before their first "aha". Ideas cluster into (a) interactive onboarding tour, (b) pre-populated demo workspace, (c) concierge setup call. Pressure-test (b): assumption = users trust sample data enough to explore; risk = feels fake and lowers trust; cheapest test = ship a demo workspace to 5% and watch time-to-first-action. Recommendation: pursue (b), park (a), kill (c) on cost-to-scale.

## Pitfalls
- Converging too early on the first plausible idea, skipping divergence.
- Steelmanning every idea equally instead of naming weak ones as weak and saying why.
- Ignoring distribution and willingness-to-pay, over-indexing on build feasibility.
- Testing with an expensive full build when a fake-door or Wizard-of-Oz would answer the question.

## Output format
```
# Brainstorm: [problem] — [date]
Reframed problem statement: one sentence.

## Idea set (clustered)
- [cluster name]: [idea, 1-2 lines]

## Pressure-test
| Idea | Key assumption | Biggest risk | Cheapest test |
| --- | --- | --- | --- |

## Recommendation
- Pursue: [idea] — why
- Park: [idea] — why
- Kill: [idea] — why

## Open questions to resolve before committing
- ...
```
