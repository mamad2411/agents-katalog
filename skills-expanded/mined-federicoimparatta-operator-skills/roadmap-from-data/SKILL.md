---
name: roadmap-from-data
description: Use this skill when the user asks to build a product roadmap grounded in behavioral or business data, reprioritize the backlog based on what the numbers say, or turn a dashboard into a sequenced set of bets. Trigger phrases include "build a roadmap from this data", "reprioritize the backlog", "where should we focus next", "roadmap based on usage", "roadmap a partir de datos", "priorizar con data", "data-driven roadmap", "planning from metrics". Produces a roadmap structured as a sequence of bets, each with impact, uncertainty, cost, and kill criteria.
---

# roadmap-from-data

> **Anchor:** A roadmap is a prioritized view of what we want to learn. Data tells you what to learn first.

## When to use

Use this skill when the user needs to convert signals from dashboards, usage logs, support tickets, or interviews into a sequenced set of product bets. Works for:

- A quarterly or semester planning cycle that is overloaded with feature requests.
- A new PM or team inheriting a backlog that lost its narrative.
- A pivot or repositioning that needs a clear sequence of bets.
- A portfolio-level view across multiple product areas.

Do not use when:

- The user is writing a PRD for an already-chosen feature. Use `prd-authoring`.
- The user is pitching a single feature for approval. Use `feature-proposal`.
- The user is scoping a client engagement with fixed deliverables. Use `proposal-scoping`.

## Philosophy

A roadmap is not a forecast. Three handbook concepts apply directly. **Output vs outcomes:** the roadmap is a sequence of changes in user or business behavior, not a list of features. **Product as a portfolio of bets:** each line is a bet with a known size, placed deliberately among others. **Roadmap as conversation, not contract:** the roadmap's purpose is to help the team and the business agree on what to learn first, not to lock commitments against which the team will be measured in a quarter. A roadmap that cannot change when the data changes is theater.

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

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: bet, backlog, roadmap, MVP, feature flag, experiment, OKR, north star, cohort, retention, activation, churn, funnel, sprint, quarter.
- **EN.** Direct US business register. Avoid "strategic" and "transformative" as adjectives for bets.
- Metric names and flag names stay in the language of the data model.

## Method

### Step 1. Decide what you are prioritizing

Roadmaps go wrong when teams confuse what they are prioritizing. Pick one:

- **Outcomes.** Changes in user behavior or business metrics.
- **Bets.** Hypotheses to test, each with a potential outcome.
- **Themes.** Problem areas that contain multiple bets.
- **Features.** Concrete deliverables. Avoid this at the roadmap level; it collapses the conversation back into a backlog.

This skill defaults to **bets**. Themes become groupings. Outcomes become success measures on each bet. Features show up only inside individual bets, not in the roadmap row itself.

### Step 2. Pull the data

Before any opinion, assemble the evidence. Three categories:

- **Behavioral.** Event data, funnels, cohorts, retention curves, session traces.
- **Qualitative.** Interview notes, support themes, sales objections, win-loss patterns.
- **Business.** Revenue by segment, margin, CAC, churn, expansion, pipeline.

For each data source, note:

- What it measures.
- Its freshness.
- Its known biases.
- Whether it is trusted by the team that will read the roadmap.

If a source is mistrusted, say so and include it anyway. Do not hide data the audience could pull themselves.

### Step 3. Cluster signals into problem areas

Group the data into themes. A theme is a cluster of signals that point at a shared user problem or business constraint. Themes are coarse, not features.

For each theme:

- **Name.** Short, names the problem.
- **Signals.** Three to seven pieces of evidence that define it.
- **Scale.** How many users, how much revenue, how frequent.
- **Current hypothesis.** What the team believes is driving the signals.

A theme without signals is an opinion. Drop it.

### Step 4. Convert themes to bets

A bet is a hypothesis that, if true, would move an outcome. For each theme, write one to three candidate bets.

Each bet has:

- **Hypothesis.** If we change X for user Y, metric Z would move by roughly W.
- **Type.** Discovery (learn something), product (ship something), operational (change how we work).
- **Expected outcome.** The metric and direction.
- **Magnitude band.** Rough impact size: small, medium, large.

Two bets on the same theme are candidates, not both commitments. Choose.

### Step 5. Size each bet on three axes

Every bet gets three scores, ranked within the portfolio, not in absolute terms.

- **Impact.** If the bet pays off, how much it moves the outcome.
- **Uncertainty.** How confident the team is about the causal link. High uncertainty does not disqualify a bet; it changes the validation method.
- **Cost.** Effort to validate first, then effort to ship if it validates.

High impact, high uncertainty, low cost is the shape of the best bets. Move those to the top.

### Step 6. Sequence the bets

Sequencing is not just prioritization. Consider:

- **Dependency.** Which bet unlocks which.
- **Learning order.** Which bet, if it fails, invalidates others.
- **Calendar constraints.** Quarterly, regulatory, seasonal, or commercial gates.
- **Team shape.** Which teams can run which bets concurrently.
- **Risk distribution.** Do not concentrate all high-uncertainty bets in one window.

The output of this step is a sequence per team, not a single list.

### Step 7. Name kill criteria per bet

Every bet in the sequence carries a kill criterion. Without it, nothing ever leaves the roadmap.

- **Signal.** Behavioral, qualitative, or economic.
- **Threshold.** Concrete.
- **Check point.** When we look.

A roadmap where every bet survives every quarter is a roadmap that has stopped learning.

### Step 8. Write the roadmap as a conversation

The delivered roadmap has three parts:

1. **Theme-level narrative.** Two to four paragraphs. What we believe about the product based on the data. Which themes matter most and why.
2. **Sequence.** Bets in order per team, per window, with confidence bands.
3. **Cadence.** How and when the roadmap is revised. Monthly, after every major experiment, or on explicit trigger.

Do not ship a roadmap as a Gantt chart. Gantt implies contract; this skill rejects the contract framing.

### Step 9. Review cadence and change policy

- **Cadence.** When the roadmap is re-examined with fresh data.
- **Trigger.** Which signals, outside the cadence, would cause an early revision.
- **Who decides.** The one person who can change the sequence between cadences.
- **How changes are communicated.** Channel, audience, lead time.

### Step 10. Stress-test before handoff

Read the roadmap as three adversarial readers:

- **An engineer.** Can they see which bets their team will run, and roughly when.
- **A skeptic.** Can they see why this sequence and not another.
- **Finance.** Can they see which bets depend on spend and which do not.

If any of the three cannot, fix it.

## Templates

- `templates/en/roadmap-brief.md`: full roadmap brief with themes, sequence, and cadence.
- `templates/en/bet-card.md`: single bet card for use inside the brief or standalone.
- `templates/es/roadmap-brief.md`: brief completo de roadmap con temas, secuencia, y cadencia.
- `templates/es/bet-card.md`: tarjeta de una apuesta para usar dentro del brief o sola.

## Related skills

- `prd-authoring`: move to it once a bet is chosen and the feature needs a spec.
- `feature-proposal`: use it when pitching a single bet for approval, not sequencing the portfolio.
- `proposal-scoping`: use it when the work is a client engagement with fixed deliverables.
- `ticket-triage`: use it to clear the backlog at the ticket level once the roadmap sets direction.

## Anti-patterns

This skill must never produce:

- A roadmap that is a list of features with dates.
- A theme with no supporting signals.
- A bet with no hypothesis or expected outcome.
- A sequence that names no dependencies and no risk distribution.
- A roadmap without a review cadence.
- A roadmap where every bet is high-confidence low-cost. That is a backlog, not a roadmap.
- A roadmap framed as a commitment the team will be measured on as a deliverable schedule.
- A roadmap that treats customer asks as ranked bets without analysis.
- A roadmap that ships with no kill criteria on any bet.

## Checklist before delivery

- [ ] The unit of prioritization is bets, themes, or outcomes, not features.
- [ ] Evidence for each theme is named and dated.
- [ ] Every bet has hypothesis, expected outcome, and magnitude band.
- [ ] Every bet has impact, uncertainty, and cost scored within the portfolio.
- [ ] Sequence considers dependency, learning order, calendar, team shape, risk.
- [ ] Every bet has a kill criterion.
- [ ] Roadmap reads as a narrative, not a schedule.
- [ ] Review cadence, trigger, and decision owner are named.
- [ ] No buzzwords from the voice rules appear.
