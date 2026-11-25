---
name: isd-course-estimate
description: Drafts a course estimate and timeline from your own past builds, with effort by phase, three scope options for the same date, review gates placed on the calendar, a table of what drafting with Claude shortens and what it does not, and the scope line the sponsor signs. Use for "run isd-course-estimate", "course estimate", "how long will this course take", "e-learning development timeline", "they want it next week", "AI writes it now so it should be quick", "scope options for the deadline", "estimate a course build", "what can we deliver by the date", part of the Claude for Instructional Designers Pack by 90n.
---

# Course Estimate and Timeline

## When To Use
The sponsor expects it next week "because AI writes it now". Use this when one course is agreed, the date is being discussed, and you need an estimate you can defend line by line. It answers: what does this date buy, what has to wait for a later version, and which parts of the work no drafting tool makes shorter?

## When Not To Use
If the question is who reviews what and who breaks a tie, that is Review and Sign-Off Plan; this estimate only places the gates on the calendar. If nobody has agreed what the course must change, run Course Brief or Action Mapping Workshop first, because there is nothing to size yet.

## Inputs
- The map, the brief or an outline of what the course has to cover, and two or three of your own past builds of similar size, with rough effort per phase, even from memory.
- The date, who fixed it, and when the expert and the reviewers are really available, by role.
If you have none of this, I start from the date and the outline and mark the output as a first draft, with every phase shown as `[no history]`.

## Approach
The five ADDIE phases (analyse, design, develop, implement, evaluate) come from the 1975 Interservice Procedures written at Florida State University (ERIC record ED122022). The estimate lays them against staged review gates, each asking a narrower question than the last: design proof, alpha, beta, gold. The only yardstick is your own history, never a published ratio, because your experts, your reviewers and your authoring tool are what set the pace. The failure it prevents: the first draft arrives in a day, everyone relaxes, and the expert's first free slot is three weeks out.

## Workflow
1. Ask at most three questions: which two or three past builds are closest and what did each phase take, what is different this time (length, number of experts, media, translation), and what happens if the date moves?
2. Build the history table by phase from the past builds, then scale each phase by the stated differences and write the reason next to it. A phase with no history stays `[no history]`. If asked for an hours-per-minute ratio or any benchmark, say plainly that none is used here.
3. Fill the two-column table. Shortens: first drafts of the brief, objectives, storyboard, scripts and questions, the sorting of source material, the first pass of checks. Does not shorten: expert availability, review rounds and their waiting time, the build in your authoring tool, media production, the run-through, the pilot, accessibility testing by a person, sign-off. You adjust the rows to this course.
4. Count backwards from the date through the gates: gold (defects only), beta (were the corrections made, does it work where it will be delivered), alpha (is the full content right), design proof (is this the right structure and treatment, shown on one sample). Put each on the calendar with the reviewer role and the waiting time you expect from experience, shown on its own and not hidden inside a phase.
5. Write three scope options against the same date: small, medium and full. Each says what is in, what is out, which checks it still includes, and its consequence. No option drops the run-through or the checks; if the full option does not fit the date, the table says so. List the risks, one line each, with an owner by role. Then write the scope line: what this date buys, what moves to a later version, and what would move the date. You decide which option you recommend; the sponsor picks.

## Output Format
```markdown
# Course Estimate and Timeline
Course: [working title] | Date asked for: [date] | Fixed by: [role] | Estimate drafted by: [role] | Based on: [past builds, described not named]
## Effort by phase, from your own builds
| Phase | Past build A | Past build B | What is different this time | This course |
|---|---|---|---|---|
| [analyse / design / develop / implement / evaluate, one row each] | [your figure] | [your figure] | [length, experts, media, translation] | [your estimate, or "no history"] |
## What drafting with Claude shortens, and what it does not
| Shortens | Does not shorten |
|---|---|
| [first drafts of the brief, objectives, storyboard, scripts and questions; sorting of source material; first pass of checks] | [expert availability; review rounds and their waiting time; the build in your authoring tool; media production; the run-through; the pilot; accessibility testing by a person; sign-off] |
## Gates, counted back from the date
| Gate | Question it asks | Reviewer role | Sent on | Back by | Waiting time |
|---|---|---|---|---|---|
| [design proof / alpha / beta / gold, one row each] | [the gate's question] | [role] | [date] | [date] | [your figure] |
## Three scope options for the same date
| Option | In | Out, to a later version | Checks included | Consequence | Fits the date |
|---|---|---|---|---|---|
| Small | [content and form] | [what waits] | [list] | [what the sponsor gives up] | [yes / no] |
| Medium | [content and form] | [what waits] | [list] | [consequence] | [yes / no] |
| Full | [content and form] | [nothing, or what waits] | [list] | [consequence] | [yes / no] |
## Scope line
Risks, one line each: [risk] (owner: [role])
This date buys [option]. [What] moves to a later version. The date moves if [condition].
## Decision
[Sponsor] picks one option and signs the scope line by [date]; [designer] books the expert's time the same day.
```

## Done When
- Every phase figure traces to a past build of yours or reads `[no history]`.
- All four gates have dates and a reviewer role, with waiting time shown separately.
- The three options share one date and differ in scope, not in skipped checks, and the scope line fits in three sentences.

## Quality Bar
- No benchmark, ratio or published figure appears anywhere; the history is yours.
- Owners and reviewers are roles; the estimate never tracks an individual's hours or output, and a scaled figure always shows the reason it was scaled.
- The estimate places gates on the calendar and stops there; lanes, rounds and the change rule are set elsewhere.
- Claude drafts the estimate from your own past builds; the checks and the run-through stay in the plan, and the sponsor signs the scope line.

## Next
Run isd-sme-interview-script (SME Interview Script) because expert time is the first thing to book.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
