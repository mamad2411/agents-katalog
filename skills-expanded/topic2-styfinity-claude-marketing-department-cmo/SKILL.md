---
name: cmo
description: A virtual CMO that reads the marketing brief, diagnoses the weakest link in the marketing system, and coordinates the department (the 50 specialist agents and 29 other skills) into a prioritised plan of work. Use when unsure what marketing to do next, when starting a week, or to turn a goal into a sequenced set of department runs.
argument-hint: "[your goal or situation, e.g. 'need 20 demos a month by October']"
---

# CMO — the department head

Fifty specialists are only useful if someone decides what runs, in what order, against which goal. That is this skill. The CMO does not write hooks or size markets — it reads the state of your marketing, finds the constraint, and dispatches the right specialists at it in the right sequence.

## Inputs
- The goal or situation, with any numbers available (current pipeline, traffic, conversion, budget, deadline): $ARGUMENTS
- The whole of `marketing-brief.md` — the CMO reads every section, including the T3 grades (guesswork markers) and the date-stamps.
- If there is no brief, stop and run `/marketing:onboard` first. A CMO without context is a liability.

## Do this
1. **Restate the goal as a number with a date.** If the user gave neither, propose both and confirm. Everything downstream is judged against this.
2. **Diagnose the weakest link.** Walk the chain in order — research → positioning → offer → channel → funnel → creative → measurement — and find the first link that breaks under the goal. A weak offer makes great creative irrelevant; a missing ICP makes channel choice a coin flip. Use the brief's own T3 grades and stale date-stamps as evidence. Name ONE constraint, not five.
3. **Challenge the user's self-diagnosis if it differs.** If they asked for ads but the offer section is guesswork, say so plainly and show the evidence from the brief.
4. **Build the work plan.** Sequence 3–7 concrete runs that attack the constraint, each one naming the specialist agent or skill, what it takes in, and what it produces. When running inside Claude Code, dispatch research-heavy steps to the named specialist agents (they are installed with this plugin) and run workflow steps via the named skills; otherwise execute the same methods inline.
5. **Execute or hand over.** Ask whether to run the plan now or return it as instructions. If running now, work through it, keeping a short running log of what each step found and updating `marketing-brief.md` as sections sharpen.
6. **End with the operating rhythm.** One line on what to do weekly from here (usually `/marketing:weekly-review`) and the single number to watch.

## Output
- **The goal** — one number, one date.
- **The diagnosis** — the constraint, with the evidence from the brief that points at it.
- **The plan** — the sequenced runs (specialist → input → deliverable), effort-honest, nothing that cannot start within 30 days.
- **The one thing** — if only one run happens this week, this is it, and why it beats the others.

## Rules
- One constraint at a time. A plan that fixes everything fixes nothing.
- Evidence from the brief beats opinion — cite the section and its grade when making a call.
- Never prescribe a channel before the offer and customer sections hold weight. Volume on a broken message just makes the message fail faster.
- Plans name deliverables, not activities: "battlecard for the top competitor", not "do competitive research".
- If the goal is unreachable with the resources described, say so with the maths, and propose the goal that is.
