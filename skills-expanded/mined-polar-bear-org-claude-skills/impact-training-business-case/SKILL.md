---
name: impact-training-business-case
description: Builds the budget case for one programme, producing the problem with its evidence, the options including doing nothing, the full cost, the expected benefit as a range from your own figures or left blank, the risks and the ask. Use for "run impact-training-business-case", "training business case", "business case for training", "budget for a training programme", "justify the training budget", "L&D budget request", "cost of doing nothing", "ask finance for training budget", part of the Claude Guide for Training Impact Pack by 90n.
---
# Training Business Case
## When To Use
You need budget for the next programme, and "people liked the last one" will not get it. Use this once the programme is chosen and sits above your capacity line but outside your budget. It answers the question the budget holder will ask: what is the problem, what are the choices, what does each cost all in, what do you expect back, and when will we know?

## When Not To Use
If you are still comparing ways to fix one problem and nothing is chosen, write the shorter memo with Non-Training Options. To report what a programme that already ran returned, use Training ROI Range: that looks back, this looks forward. To rank many programmes against each other, use L&D Priority Plan.

## Inputs
- The performance problem and the evidence for it: the diagnosis, and the results table from the last programme if there was one.
- Your cost figures for each option, any benefit figures and assumptions with where each came from, and the budget holder (role) with the date they decide. Claude Docs (beta) suits a written case; Claude Slides (beta) in the same conversation gives matching slides.
If you have none of this, I start from the problem in one line and the programme you propose, leave every cost and benefit blank, and mark the output as a first draft.

## Approach
The structure comes from HM Treasury: the Green Book (2026) on appraisal and its "Guidance on developing business cases", used here as six plain parts: need, options, costs, benefits, risks, delivery. Two of its habits matter most. The short list always keeps "business as usual" and a "do minimum" option, and it corrects for optimism bias, the tendency to be over-optimistic about costs, time and benefits. This is a way to lay out a case, not a rule you must follow. The failure it prevents: a single glowing option with a round uplift nobody can source, which finance takes apart in one question.

## Workflow
1. Ask at most three questions: what problem the programme is meant to fix and the evidence for it, which cost and benefit figures you hold and their sources, and who decides on the budget and by when.
2. State the need: the performance problem and its evidence, with claim strength (shown, suggested, unknown). Evidence from the last programme is quoted from its results table, not from memory.
3. Set out at least three options: business as usual (doing nothing, with what that costs), do minimum (the smallest move that would meet the goal), and the proposed programme. Each is described as fairly as the one you prefer, and costed in full: design, delivery, participants' time away from work, tools, evaluation. Your figures or blank. A missing line is shown as missing, never absorbed.
4. State the expected benefit as a range, low to high, from your own figures, with every assumption listed beside its source. If you have no figures, the benefit stays blank and the case says what would be needed to estimate it. I supply no uplift and no average.
5. Guard against optimism: where in doubt, take the lower benefit and the higher cost. Then name the one or two assumptions that would change the answer if they moved, and by how much they would need to move.
6. List the risks with owners, the delivery plan (who, by when), the measures and the date proof will arrive, taken from or leading to a Success Measures Agreement. End on the ask: amount, decision owner, date.

## Output Format
```markdown
# Training Business Case
Programme: [programme] | Prepared by: [named person] | For: [budget holder, role] | Date: [date] | The ask in one line: [amount] to [do what] for [roles], decided by [date]
## The need
| Problem, by role and task | Evidence | Source and voucher | Claim strength |
|---|---|---|---|
| [problem] | [your figure or finding] | [source, name] | [shown, suggested, unknown] |
## Options
| Option | What changes in the work | Full cost | Expected benefit, low to high | Strongest reason against |
|---|---|---|---|---|
| Business as usual | [nothing; what continues] | [cost of the problem, or blank] | [none] | [reason] |
| Do minimum | [smallest move] | [your figure] | [your range, or blank] | [reason] |
| Proposed programme | [change] | [your figure] | [your range, or blank] | [reason] |

Cost lines behind each figure: design [figure], delivery [figure], participants' time [figure], tools [figure], evaluation [figure], each with its [source] or left blank.
## Benefit assumptions
| Assumption | Low | High | Source | Changes the answer if it moves? |
|---|---|---|---|---|
| [assumption] | [your figure] | [your figure] | [source, or "none: benefit left blank"] | [yes, no] |
## Risks and delivery
| Risk or milestone | Owner | Date |
|---|---|---|
| [risk, or step] | [named owner] | [date] |

Proof: measures [from the agreement, or "to agree"] | First evidence due: [date] | Verdict due: [date]
## Decision
[Budget holder] approves, reduces or declines [amount] by [date]; [named person] owns the ask and reports on the proof dates.
```

## Done When
- The options table holds business as usual, do minimum and the proposal, each with a reason against.
- Every cost and benefit cell holds your figure with a source, or is blank and listed as missing; participants' time is costed or the case says it is not.
- The assumptions that would change the answer are named, the proof date exists, and the ask has an amount, an owner and a date.

## Quality Bar
- A benefit with no source is not rounded into the case: "we cannot estimate this yet" is an allowed line, and doing nothing is costed as honestly as the programme.
- Benefits are stated for roles and groups, never as expected gains from named people.
- Procurement, contract or employment points raised by an option: check with a qualified adviser.
- Every cost and benefit is the user's figure or left blank; no return, uplift or benchmark is invented, and a named person owns the ask.

## Next
Run impact-training-request-brief (Training Request Brief), because an approved case becomes the next request to question.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
