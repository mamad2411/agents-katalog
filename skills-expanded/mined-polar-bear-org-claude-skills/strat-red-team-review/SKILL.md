---
name: strat-red-team-review
description: Argues against the leading strategy option and returns a red team review with the assumptions the plan cannot survive losing, the strongest case against it in good faith, the counter-evidence already on file, three sceptic questions, a change-now list and the accepted risks. Use for "run strat-red-team-review", "red team our product strategy", "argue against this plan as hard as you can", "which assumptions can this plan not survive losing?", "poke holes in the strategy before the review", "key assumptions check", "what will a sceptical leader ask?", "what should I change before the review?", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Red Team Review

## When To Use
The plan looks finished and nobody has argued with it yet. That usually means the arguing will happen in the review, in front of the people who decide. Run this on the leading option once the comparison is done. It answers: where is this plan weakest, and what do we change before someone else finds it?

## When Not To Use
If several options are still live, use Decision Matrix first; attacking one option while three are open only tilts the field. If you want the ways it could fail told as stories with signals and responses, use Pre-Mortem Analysis. This review attacks assumptions and reasoning and tells no failure story.

## Inputs
- The plan: the leading option from the Strategic Option Set, its Strategic Bets, or the draft strategy
- The evidence behind it: Scenario Model, Decision Matrix, interview themes, usage data, each with its source
- The review date and who will read the plan (roles)
If you have none of this, I start from the plan in one paragraph, attack only the assumptions it states and mark the output as a first draft.

## Approach
Red teaming as set out in the UK Ministry of Defence Red Teaming Handbook, third edition 2021 (https://www.gov.uk/government/publications/a-guide-to-red-teaming): challenge the assumptions and the reasoning before you commit. It opens with the key assumptions check from the US Government's "A Tradecraft Primer: Structured Analytic Techniques for Improving Intelligence Analysis", 2009 (https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf). Both were written for defence and intelligence work, so the steps here are translated to product strategy. The failure this prevents: a review that corrects the typos while the one claim the whole plan rests on goes unasked, until finance asks it in the room.

## Workflow
1. Ask at most three questions: which assumption the team is least sure of, when the review is and who reads the plan, and whether any part is already fixed (committed or promised).
2. Key assumptions check: restate the plan's assumptions as plain claims, taken from the plan and its evidence, including the ones nobody wrote down. Mark the two or three the plan cannot survive losing. For each: evidence for, evidence against or "none found", and what breaks if it is wrong. Evidence means what customers did, with its source. A belief the team holds strongly is listed as a belief.
3. Strongest case against: one paragraph on why a reasonable person would reject this plan, argued in good faith. No straw arguments, and no failure story.
4. Counter-evidence already on file: a contrary interview theme, a flat segment, a scenario downside. Quote the source. If the files hold none, write "none on file", which is a gap and not a clean bill.
5. Three sceptic questions, each with the weakest current answer the team has. Three sharp ones beat ten generic objections.
6. Change-now list: each change tied to the assumption or reason behind it, with an owner by role. Whatever is not changed is written down as an accepted risk, with the reason it is accepted.

## Output Format
```markdown
# Red Team Review
**Plan:** [leading option] | **Review date:** [date] | **Readers:** [roles] | **Fixed parts:** [what is already committed]
## Assumptions the plan cannot survive losing
| Assumption | Evidence for | Evidence against | If it is wrong |
|---|---|---|---|
| [plain claim] | [source / team belief] | [source / none found] | [what breaks] |
## Strongest case against
[One paragraph, argued in good faith]
## Counter-evidence on file
- [Finding, quoted / none on file] | Source: [file, date] | Touches: [assumption]
## Sceptic questions
1. [Question] | Weakest current answer: [answer]
## Change now
| Change | Reason | Owner (role) |
|---|---|---|
| [change] | [assumption or evidence] | [role] |
## Accepted risks
- [Risk left unchanged, and why it is accepted]
## Decision
[Plan owner role] decides by [date before the review] which changes go in and signs off the accepted risks.
```

## Done When
- Two or three assumptions are marked as ones the plan cannot survive losing, each with evidence for and against or "none found"
- The three sceptic questions each carry the weakest current answer
- Every change-now item has a reason and an owner by role
- Everything left unchanged is listed as an accepted risk

## Quality Bar
- Attack the plan and its assumptions, never the people who wrote it
- Go for the claims the plan rests on, not wording or layout
- Legal, privacy or security risks are flagged, not judged here; check with a qualified adviser
- Counter-evidence comes from files and sources on hand, nothing invented; the plan owner decides which changes go in.

## Next
Run strat-pre-mortem-analysis (Pre-Mortem Analysis) to imagine the changed plan has failed and set signals and responses.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
