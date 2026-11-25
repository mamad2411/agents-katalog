---
name: impact-success-measures-agreement
description: Drafts the agreement a sponsor signs before a training programme is built, producing a table of agreed measures with source, data owner and voucher, the sponsor's own definitions of worked, partly and did not, the decision the evidence will feed, and a sign-off block. Use for "run impact-success-measures-agreement", "success measures", "how will we know the training worked", "agree success criteria with the sponsor", "return on expectations", "define success before we build", "what does success look like", "training success metrics", part of the Claude Guide for Training Impact Pack by 90n.
---

# Success Measures Agreement

## When To Use
The build is about to start and nobody has agreed how anyone will know it worked. Use this after the behaviours are mapped and before design begins, while the sponsor still cares enough to answer. It answers: what result does the sponsor expect, what will "worked", "partly" and "did not" mean, and which decision will the evidence feed?

## When Not To Use
If nobody has said what people will do differently, run Critical Behaviours Map first. This agreement names no instruments and no collection dates: where the before figures live is Training Baseline Plan, and who collects what is Kirkpatrick Data Collection Plan. If the sponsor will not engage, send the draft marked "proposed" and keep a note that it was never signed.

## Inputs
- Your Critical Behaviours Map, or the goal and the behaviours in any form.
- Your notes from the sponsor conversation, above all the answer to "what would success look like?", and the report where the sponsor already sees the result, with its owner.
If you have none of this, I start from the sponsor's request and mark the output "proposed, first draft". In Claude Docs (beta) the agreement becomes a document both sides can comment on and sign; a plain chat works too.

## Approach
Return on expectations, as set out by Kirkpatrick Partners: agree with business stakeholders what the programme should accomplish before designing it, and plan from the result down. The CDC Program Evaluation Framework (2024) adds the step of focusing the evaluation questions, and utilisation-focused evaluation, the approach developed by Michael Quinn Patton, adds the rule that the primary intended users and their intended use guide every other choice. The judgement: a measure nobody would act on is decoration. The failure this prevents: the report lands, the number rose a little, and the sponsor and L&D find out in that meeting that they never meant the same thing by "worked".

## Workflow
1. Ask at most three questions, together: what result does the sponsor expect, in their words, and on which report do they already see it; who will read the evidence and which decision will it feed, by when; and who owns each figure.
2. Start with the intended users and use: who reads the evidence, and whether it feeds a decision to continue, change, stop or scale. If no decision hangs on it, tell the sponsor before going further; an evaluation with no reader is a cost.
3. Plan from the result down. First the result, in the sponsor's words and on the sponsor's own report. Then the leading indicators that should move first, because results lag and attention moves on. Then the critical behaviours, taken from the map as worded.
4. Write one row per agreed measure: a definition tight enough that the data owner would calculate it the same way twice, the unit, the source, the data owner and the voucher. A row with no source or owner reads "[no voucher yet]" and cannot carry a verdict.
5. Set three verdicts per measure, before the build: what "worked", "partly" and "did not" will mean. The figures are the sponsor's, or the cell says "[to agree]". I never suggest a threshold, not even as a starting point; I draft the question you put to the sponsor.
6. Run the dress rehearsal with the sponsor, measure by measure: "if the figure came out at [this], what would you decide?" If no answer would change a decision, the measure is dropped. I prepare the questions; the answers go in as the sponsor gave them.
7. Close with what will not be measured and so cannot be claimed later, the reporting dates, and the sign-off block for the sponsor, the L&D lead and the data owner. Unsigned means "proposed", and the header says so.

## Output Format
```markdown
# Success Measures Agreement
Programme: [name] | Sponsor: [name, role] | L&D lead: [name, role] | Status: [proposed / signed on date]
## Intended users and use
Read by: [roles] | Feeds the decision to [continue / change / stop / scale] | Decided by: [name, role] on [date] | Reported: [leading indicators on date; final results on date]
## Agreed measures
| Kind | Agreed measure | Definition | Unit | Source | Data owner | Voucher |
|---|---|---|---|---|---|---|
| Result | [in the sponsor's words] | [how it is calculated, for which group] | [unit] | [report or system] | [name, role] | [name / no voucher yet] |
| [Leading indicator / Critical behaviour, as worded in the map] | [measure] | [definition] | [unit] | [source] | [name, role] | [name] |
## What the verdicts will mean
| Agreed measure | Worked | Partly | Did not | Dress rehearsal: at [figure], the sponsor would |
|---|---|---|---|---|
| [measure] | [sponsor's figure / to agree] | [sponsor's figure / to agree] | [sponsor's figure / to agree] | [decision, in the sponsor's words] |
## Not measured, so not claimed
- [What is not measured]: [why not]. No report will say [claim ruled out].
## Sign-off
- Sponsor: [name], for the result, the verdicts and the decision. Signed [date / not yet].
- L&D lead: [name], for the behaviours and the reporting dates. Signed [date / not yet].
- Data owner: [name], for the definitions and the sources. Signed [date / not yet].
## Decision
[Sponsor name] signs or amends this agreement by [date, before the build starts]. Until then every line reads "proposed".
```

## Done When
- The result is in the sponsor's words and sits on a report that already exists.
- Every agreed measure has a definition, a unit, a source, a data owner and a voucher, or says what is missing.
- Every measure kept has three verdicts and a dress rehearsal answer that would change a decision.
- The "not measured" list is written, and the status line is true.

## Quality Bar
- Measures describe groups: a count, a share or an average for a role or a cohort. No measure is a rating of a person.
- A measure dropped in the dress rehearsal stays dropped; it does not creep back as "nice to have".
- No benchmark, industry norm or typical figure appears anywhere. An empty cell marked "[to agree]" is a finished cell.
- The agreement holds no instruments and no collection dates, only the dates on which something is reported.
- Every threshold is the sponsor's; Claude drafts the agreement, and named people sign it and stand behind each figure.

## Next
Run impact-training-baseline-plan (Training Baseline Plan) to capture the before figures while there is still time.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
