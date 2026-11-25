---
name: isd-review-plan
description: Drafts the review rules for one course before the build, with who reviews what at each gate, a lane for every reviewer, one named decider, rounds and dates, the change rule for late requests and the sign-off table. Use for "run isd-review-plan", "who signs off the course", "six reviewers and nobody breaks a tie", "the revisions never end", "reviewers contradict each other", "legal rewrote what the expert approved", "late change requests after approval", "review and sign-off plan", part of the Claude for Instructional Designers Pack by 90n.
---

# Review and Sign-Off Plan

## When To Use
Six people will review the course and nobody has said who breaks a tie. Use this before the build starts, while everyone still agrees on the scope and nobody has a comment to defend. It answers: who looks at what, at which gate, inside which lane, who decides when two of them disagree, and what a late request costs.

## When Not To Use
If comments are already arriving and need sorting, run SME Review Round, which runs one round under these rules. For effort and the calendar as a whole, use Course Estimate and Timeline; for the final record at release, Release Sign-Off Record.

## Inputs
- The course, its release date, the sponsor by role, every reviewer by role with what each one cares about, and what happened in the last review that went badly, if one did
If you have none of this, I start from the release date and the reviewer roles you name, and mark the output as a first draft.

## Approach
Staged review gates: design proof, alpha, beta, gold, each asking a narrower question than the last, so the room for change shrinks as the cost of change grows. The plan is written once, before anyone has seen a screen, because rules agreed in calm are the only ones that hold in week six. The failure it prevents is the course where legal and the expert undo each other's edits in turn, and the sponsor reopens the objectives two days before release because no page said they were closed.

## Workflow
1. Ask up to three questions: who sponsors the course, which reviewer roles must sign, and the release date.
2. Set the four gates and the one question each asks. Design proof: is this the right structure and treatment, shown on one sample? Alpha: is the full content right? Beta: were the corrections made, and does it work in the real delivery setting? Gold: defects only. A comment that answers an earlier gate's question is out of step, and the plan says so in advance.
3. Give each reviewer one lane per gate: the expert for accuracy, legal or compliance, brand, accessibility, a learner representative, the sponsor. A reviewer comments only inside the lane. You judge which gates each role really needs; not everyone reviews everything. Legal points go to a qualified adviser, never settled in the plan.
4. Name one decider by role who resolves conflicting comments within a turnaround you set. Reviewers advise; the decider decides. If nobody will take the role, stop here and take that to the sponsor: it is the finding.
5. Set rounds per gate and dates, counted back from release; both are yours, and I propose no number. Silence after the window counts as approval only if the sponsor agrees that rule in advance, in writing.
6. Write the change rule for anything asked after a signed gate: new content costs time, budget, or a cut elsewhere, and the sponsor picks one in writing. Then note which check feeds each gate, and lay out the sign-off table that the release record will later fill.

## Output Format
```markdown
# Review and Sign-Off Plan
## Gates
| Gate | The one question | What is shown | Check that feeds it | Rounds | Window (dates) |
|---|---|---|---|---|---|
| Design proof | Right structure and treatment? | [One sample] | [None yet] | [n] | [Dates] |
| Alpha | Is the full content right? | [Full draft] | [For example AI Content Accuracy Check, Designer Run-Through] | [n] | [Dates] |
| Beta | Corrections made, works in the real setting? | [Corrected build] | [For example Accessibility Check, Learner Pilot Test] | [n] | [Dates] |
| Gold | Defects only | [Final build] | [Release Sign-Off Record] | [n] | [Dates] |
## Lanes
| Reviewer role | Comments only on | Design proof | Alpha | Beta | Gold |
|---|---|---|---|---|---|
| Expert | Accuracy | [yes / no] | [yes / no] | [yes / no] | [yes / no] |
| Legal or compliance | [Lane; check with a qualified adviser] | [yes / no] | [yes / no] | [yes / no] | [yes / no] |
| Brand | [Lane] | [yes / no] | [yes / no] | [yes / no] | [yes / no] |
| Accessibility | [Lane] | [yes / no] | [yes / no] | [yes / no] | [yes / no] |
| Learner representative | Fit to the task and the setting | [yes / no] | [yes / no] | [yes / no] | [yes / no] |
| Sponsor | Goal and scope | [yes / no] | [yes / no] | [yes / no] | [yes / no] |
## Decider and rules
Decider: [name, role] resolves conflicting comments within [turnaround you set]. Silence after the window: [counts as approval, agreed by the sponsor on [date] / does not]. Change rule: after a signed gate, new content costs [time / budget / a cut elsewhere]; the sponsor picks one in writing.
## Sign-off table
| Gate | Role | Name | Date | Version | Decision |
|---|---|---|---|---|---|
| [Gate] | [Role] | [Name] | [Date] | [Version] | [approved / approved with changes / not approved] |
## Decision
[Sponsor name, role] approves the gates, the lanes, the decider and the change rule by [date], before the build starts.
```

## Done When
- Every reviewer has a lane and the gates they attend, and nobody reviews everything
- One decider is named, with a turnaround, and the sponsor has agreed the silence rule or struck it
- The change rule and the sign-off table are in the plan before anything is built

## Quality Bar
- Every number of rounds, date and turnaround is yours; none is proposed as a norm
- The plan lists roles, lanes and decisions, and never a tally or rating of reviewers
- Claude drafts the plan; one named person decides at each gate, and that name is agreed before the build.

## Next
Run isd-measurable-objectives (Measurable Learning Objectives), since the first thing reviewers sign is what the course must achieve.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
