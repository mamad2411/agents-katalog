---
name: idea-discovery
description: Micro-SaaS idea funnel - pain-first sourcing, idea cards, evaluation matrix, shortlist. From "what to build" to 2-3 candidates worth audience research.
---

# /idea-discovery [niche|seed]

Owner: **growth-lead**; sourcing by **market-researcher**; audience sanity by
**audience-researcher**.

## Sequence
1. Seed: user's domains of expertise, interests, unfair advantages (ask — founder fit is a
   scoring criterion), or a niche/idea argument, or winners from `/brainstorm`.
2. Pain mining (market-researcher): community complaints, 1-3-star reviews of incumbent
   tools, job-board tasks, workflow gaps. Each candidate pain → idea card
   (template: idea-card.md) with evidence rung (anecdote/pattern/behavioral/payment) and
   source (URL + date, or `hypothesis — verify`).
3. Alternatives per card: what the audience does today, what it costs them (money or hours),
   switching friction. Paid incumbents = budget evidence.
4. Evaluation matrix across cards: pain severity × frequency, WTP evidence rung, audience
   reachability (watering holes exist?), competition density, effort-to-MVP (weeks class),
   founder fit. Scores justified; sensitivity note if the leader is fragile.
5. Shortlist 2-3; per shortlisted idea the cheapest next validation step from
   `constraints/validation-methods.yaml`. The user picks which advance to `/audience-research`.

## Output
`product/ideas/idea-cards/IC-NNN-<name>.md` per candidate; `product/ideas/evaluation.md`
matrix + shortlist; picks recorded; next: `/audience-research <idea>`.
