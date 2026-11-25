---
name: impact-needs-assessment-update
description: Refreshes last period's training needs from the evidence this cycle produced, producing needs by role and task with a status each, a split of what training can and cannot fix, and a list of needs dropped with the reason. Use for "run impact-needs-assessment-update", "training needs assessment", "training needs analysis", "learning needs analysis", "TNA", "update our training needs", "needs for next year", "which needs were never needs", part of the Claude Guide for Training Impact Pack by 90n.
---

# Training Needs Assessment Update

## When To Use
You are planning next year from last year's wish list. Use this at the end of a cycle, when the evaluations have told you things the original needs list did not know: barriers that were never about skill, a programme that missed, requests that kept coming for the same task. It answers: which needs still stand, which are new, and which should come off the list because the evidence says they were not needs?

## When Not To Use
For one performance problem examined in depth, use Performance Problem Diagnosis. This skill lists and sorts needs and ranks nothing: to decide what runs within your capacity, use L&D Priority Plan. It also runs no new survey; if you have no evidence from this cycle at all, start with the diagnosis on your most pressing request.

## Inputs
- Last period's needs list, in whatever state it is in.
- This cycle's evidence: barrier lists from the case write-ups, shortfall notes, results tables, comment themes, and the log of requests received.
- The business goals for the next period, in the leadership team's own words. No appraisal scores, performance ratings or named individuals: if they are in a file, remove them before you share it.
If you have none of this, I start from the roles in scope and the business goals, mark every need "unverified", and mark the output as a first draft.

## Approach
Learning needs analysis as the CIPD factsheet "Learning needs analysis" describes it: organisation, team and individual levels viewed together, drawn from several sources. This pack replaces the individual level with role and task and takes no appraisal or performance data, although the factsheet lists them. The judgement is that an evaluation is the best needs data you will ever get, because it shows what happened when you acted on a need. The failure it prevents: a need that a programme already failed to fix is carried over untouched, and the same course is commissioned for the same task.

## Workflow
1. Ask at most three questions: which roles and which period are in scope, which business goals the next period will be judged on, and which pieces of this cycle's evidence you can share.
2. Read three levels together. Organisation: the goals and the capability they call for. Team or workstream: where the evidence shows work stalling. Role and task: what people in the role must do. A need that links to no level above it is flagged, not deleted.
3. Write each need as role, task and the evidence source from this cycle. I use only what is in your files; no new need is proposed because it sounds likely, and the "how many people" cell is yours: I estimate no headcount and no share of a role.
4. Give each need a status: confirmed (this cycle's evidence supports it), new (it appeared this cycle), dropped, or unverified (carried over with no evidence either way). A need resting on one source is flagged "single source".
5. Give every dropped need its reason, one of two: the evidence says it was not a need, or it was a need training could not fix. Dropping is a finding and is shown, not tidied away.
6. Split what remains: training can fix it (skill or knowledge) or it cannot (information, tools, incentives, process). For the second kind, name where it goes: the role that owns the tool, the process or the reward.

## Output Format
```markdown
# Training Needs Assessment Update
Scope: [roles] | Period: [period] | Goals served: [business goals] | Evidence from: [reports used]
## Needs by role and task
| Role | Task | Need | Level it links to | Evidence source this cycle | Status | Flag |
|---|---|---|---|---|---|---|
| [role] | [task] | [need] | [organisation goal, team, role] | [barrier list, shortfall note, request log, results table] | [confirmed, new, unverified] | [single source, or none] |
## Training can fix
| Need | Why it is skill or knowledge | Evidence |
|---|---|---|
| [need] | [reason] | [source] |
## Training cannot fix
| Need | Cause | Where it goes |
|---|---|---|
| [need] | [information, tools, incentives, process] | [owner role] |
## Dropped
| Need as listed last period | Reason | Evidence |
|---|---|---|
| [need] | [not a need, or training could not fix it] | [source] |

Missing: [evidence you expected and did not have, and who could supply it]
## Decision
[L&D lead] agrees the confirmed and new needs with [sponsor or leadership role] by [date], before anything is ranked.
```

## Done When
- Every need names a role and a task and carries exactly one status; confirmed and new needs point to a source from this cycle.
- Every dropped need has one of the two reasons and the evidence behind it.
- Needs training cannot fix sit in their own table with an owner role, not on a course list.
- No priority order, total or rank appears anywhere in the output.

## Quality Bar
- Last period's list is a claim to test, not a baseline to protect.
- Single-source needs are flagged, and "unverified" is an honest status, not a failure.
- Group-level evidence only: comments and cases arrive anonymised and stay that way.
- Needs are stated by role and task from evidence in hand; no named person is rated, and no need or headcount is invented to fill a gap.

## Next
Run impact-ld-priority-plan (L&D Priority Plan) to rank what the refreshed needs call for.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
