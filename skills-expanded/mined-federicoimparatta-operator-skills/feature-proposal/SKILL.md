---
name: feature-proposal
description: Use this skill when the user asks to pitch a feature, propose a product bet, write a one-pager, or make the case for investing in a piece of product work before committing to a full PRD. Trigger phrases include "pitch a feature", "feature proposal", "make the case for X", "write a one-pager", "propuesta de feature", "proponer un producto", "make the case", "pitch this to leadership". Produces a proposal structured as a bet request, not a spec, with explicit cost to validate and kill criteria.
---

# feature-proposal

> **Anchor:** A feature proposal is a bet request, not a design review.

## When to use

Use this skill when the user needs to convince a reader, usually leadership or a product council, to invest in validating or building something. Works for:

- A feature idea that has momentum but no commitment.
- A strategic bet the team wants to place before opening a PRD.
- A one-pager to push a decision off the queue.
- A counter-proposal to a scoped feature the team thinks is misframed.

Do not use when:

- The feature is committed and needs spec detail. Use `prd-authoring`.
- The feature is being scoped for a client delivery. Use `proposal-scoping`.
- The user is writing a roadmap. Use `roadmap-from-data`.

## Philosophy

A feature proposal is a bet under uncertainty, written down so a group can decide whether to take it. Four handbook concepts apply. **Output vs outcomes:** the proposal promises a user or business change, not a shipping artifact. **Product as a portfolio of bets:** the proposal names the size of the bet and its place in the portfolio. **Reduce uncertainty, not scope:** the proposal's first product is not the feature itself, it is the cheapest way to learn whether the bet is worth placing. **Discovery is a practice:** the proposal carries evidence from the work already done to disqualify easy ideas.

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

- **ES.** Rioplatense register. Vos over tú. Keep standard terms in English: feature, bet, backlog, MVP, prototype, churn, funnel, retention, stakeholder, aha moment, north star metric.
- **EN.** Direct US business register. A proposal is not a sales page. Do not describe the feature as revolutionary, game-changing, or best-in-class.
- Match the language of the reader who decides, not the author.

## Method

### Step 1. Open with the problem, not the feature

Three to five sentences. No solution yet. Answer:

- **Who feels it.** A specific user type or segment.
- **How it shows up in the product today.** A moment or a data point.
- **What they do instead.** The current workaround, substitute, or resignation.
- **Why it matters to the company.** Revenue, retention, strategic position, or cost.

If the problem can only be understood with a solution attached, the problem is not yet clear.

### Step 2. State the bet in one paragraph

Format:

> We propose to invest **X effort** to test the hypothesis that **solution class Y** would move **metric Z** for **user W**. If the test shows **signal S**, we would commit to a full build.

Solution class is deliberately fuzzy. "A guided onboarding" is a class. "A 5-step wizard in the top-right" is a spec and does not belong here.

### Step 3. Name the user

One paragraph. The user the feature serves, with enough specificity that the reader can picture them. Include segment size when known. If the feature serves multiple users, pick one as primary and justify it.

### Step 4. Evidence for the problem

Three to seven data points or observations that support the problem statement. Each one is one line.

- Interview from [date] with [role].
- Support ticket volume on [topic], [count] over [window].
- Dashboard showing [metric] at [value].
- Experiment [X] that failed with signal [Y].

Mark each bullet as **validated** or **inferred**. Unvalidated inference is fine at this stage; dishonest framing is not.

### Step 5. Proposed direction

Two to four paragraphs on the direction, not the spec. Answer:

- What the user would do that they cannot do today.
- What changes in the product at a conceptual level.
- What the team would not build, even if tempted.

A proposal that contains screens is trying too hard. Screens belong in a PRD.

### Step 6. Expected impact

The size of the prize if the bet pays off.

- **Primary metric.** The one metric that would move.
- **Direction and magnitude.** Up or down, by roughly how much.
- **Time to move.** Weeks or quarters.
- **Second-order effects.** Positive or negative. Name both.

Do not stack speculative metrics. One primary metric. Everything else is supporting.

### Step 7. Cost to validate, not cost to build

The cost that matters at this stage is validation. Options:

- **User research.** Number of interviews. Weeks of effort.
- **Prototype.** High-fidelity or low. Engineering or design cost.
- **Experiment.** A/B, holdback, painted-door, or concierge. Effort and minimum audience.
- **Internal dogfood.** Who. For how long.

Name the one method you propose. Explain why the alternatives are wrong for this bet.

### Step 8. Kill criteria for the validation

Write the signal that would kill the bet before it becomes a PRD.

- Behavioral. "Less than 20% of shown users click."
- Qualitative. "Users in research call it confusing three times out of five."
- Economic. "Unit margin drops below X at the simulated price point."

A validation with no kill criteria validates nothing.

### Step 9. The ask

One paragraph. What the reader must decide, and by when.

- **Decision.** Approve validation, approve full build, park, kill.
- **By.** A date or a meeting.
- **Blocker removed if approved.** What this unlocks.
- **Risk of delay.** What happens if this sits for a quarter.

### Step 10. Open questions

Short list, with owner and deadline. Keep it honest. A proposal with no open questions is pretending.

## Templates

- `templates/en/proposal.md`: full feature proposal.
- `templates/en/one-pager.md`: short proposal for fast-moving leadership forums.
- `templates/es/proposal.md`: propuesta completa de feature.
- `templates/es/one-pager.md`: propuesta corta para foros de decisión rápida.

## Related skills

- `prd-authoring`: move to it once the bet is approved and the feature needs spec detail.
- `proposal-scoping`: use it instead when the feature is a client delivery, not an internal bet.
- `roadmap-from-data`: use it when the question is sequencing many bets, not pitching one.
- `red-team-review`: run it against the proposal before commitment to find where the bet breaks.

## Anti-patterns

This skill must never produce:

- A proposal that opens with a screen or a solution.
- A proposal that promises a metric without naming how it would be measured.
- A proposal that collapses validation cost into build cost.
- A proposal that claims "we have validated this" without evidence.
- A proposal that cites competitors as the only rationale.
- A proposal with no kill criteria.
- A proposal that asks for approval on multiple possible directions at once.
- A proposal longer than two pages for a one-pager-grade audience.
- A proposal that reads as advocacy rather than analysis.

## Checklist before delivery

- [ ] Problem is described without a solution attached.
- [ ] The bet is a single paragraph in the step 2 format.
- [ ] User is named with segment size when known.
- [ ] Evidence list marks each item as validated or inferred.
- [ ] Proposed direction is conceptual, not a spec.
- [ ] Impact has a single primary metric with direction, magnitude, and time.
- [ ] Cost to validate is named, not cost to build.
- [ ] Kill criteria are concrete.
- [ ] Ask is specific: decision, by when, consequences.
- [ ] No buzzwords from the voice rules appear.
