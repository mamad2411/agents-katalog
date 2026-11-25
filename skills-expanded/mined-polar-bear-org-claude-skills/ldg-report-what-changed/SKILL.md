---
name: ldg-report-what-changed
description: Drafts a one-page report for executives with the bottom line first, the chain of evidence level by level, what else changed in the same period, what blocked use, what cannot be claimed, and the decision asked. Use for "run ldg-report-what-changed", "training impact report", "l&d report", "report to executives", "training report for leadership", "training effectiveness report", "one page impact summary", "did the training improve anything", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Report What Changed

## When To Use
Leaders ask whether it improved anything and the report shows completions. You hold forms, a follow-up, perhaps a measure that moved, and a slot of a few minutes with people who will read one page at most. Run this to answer the question they are really asking: did the problem we were asked to fix move, how sure are we, and what do you need from us now?

## When Not To Use
If the evidence of use has not been collected, there is little to report: run Check Use on the Job first. If the question is what the team should keep, fix or retire, that is the team's own review: run Review the Programme. The working behind a return figure belongs in Estimate the Training ROI.

## Inputs
- The original request and the result agreed with the sponsor, from the evaluation plan if there is one
- The evidence you hold by level: feedback summary, checks, the follow-up on use, group work measures, any ROI range, each with its date
- What else changed in the same period, and the decision you need from the readers
If you have none of this, I start from what was asked for and the one piece of evidence you trust most, and mark the output as a first draft.

## Approach
The page puts the bottom line up front, from US Army Regulation 25-50 on correspondence: the main point at the beginning, active voice, understood in a single rapid reading. Under it, the chain of evidence across the Kirkpatrick levels. The judgement is in the middle of the page: saying how sure you are, and what you are not claiming, is what makes the first two sentences believable. The failure it prevents: a slide of completion rates and a satisfaction average, a nod from the executive team, and a budget round three months later in which nobody can say what the programme did.

## Workflow
1. Ask three questions: what was the programme asked to change, what decision do you want from the readers, and who signs off what counts as proof before the page goes out?
2. Lay the evidence out top down: result (Level 4) and leading indicators, behaviour (Level 3), learning (Level 2), reaction (Level 1), each with its source and date. A level with no evidence is written as "missing", never padded.
3. Move completions and attendance into a reach line. They show who was reached and are never offered as impact.
4. List what else changed in the same period (tools, process, staffing, targets), so that nothing is over-claimed and a flat result is not pinned on the training or on people.
5. Take what blocked use from the barrier list, with who could remove each barrier. This is often the part executives can act on that day.
6. Write the bottom line last, in two or three sentences: what was asked for, what changed, how sure we are, in one of three words (shown, likely, not shown). No adjectives.
7. State plainly what we cannot claim, then the decision asked, with options. Draft it in Claude Docs (beta), or as a short deck in Claude Slides (beta) that downloads as PowerPoint or PDF, or in any document.

## Output Format
```markdown
# What Changed Report
Programme: [name] | Period: [dates] | For: [readers] | Proof signed off by: [name]
## Bottom line
[What was asked for.] [What changed.] [How sure we are: shown / likely / not shown, and on what evidence.]
## Chain of evidence
| Level | What we found | Shown / likely / not shown / missing | Source and date |
|---|---|---|---|
| Result and leading indicators | [group figure, yours] | [word] | [report, date] |
| Behaviour on the job | [finding] | [word] | [follow-up, date] |
| Learning | [finding] | [word] | [checks, date] |
| Reaction | [finding] | [word] | [form, date] |

Reach, not impact: [completions, attendance]
## What else changed in the period
- [tool, process, staffing or target] and its likely pull on the result
## What blocked use
- [barrier, from the barrier list] | who could remove it: [role]
## What we cannot claim
- [claim the data does not support, and why]
## Decision
[Executive name] decides by [date] between [option A], [option B] and [option C], and names who removes [barrier].
```

## Done When
- The bottom line stands alone: a reader who stops after it knows what changed and how sure we are
- Every level has a source and a date, or reads "missing"
- Completions appear only on the reach line
- The page names what else changed and what cannot be claimed, ends on one decision with options and a date, and fits one page

## Quality Bar
- Certainty in words (shown, likely, not shown), never a percentage of confidence nobody measured
- Group-level results only; no team or person is singled out, and small groups stay suppressed
- No figure, quote or finding beyond your evidence; a weak result goes in the bottom line the week it is known, not softened further down
- Claude drafts the page from your evidence; a named person decides what counts as proof, and nothing is claimed that the data cannot show

## Next
Run ldg-review-the-programme (Review the Programme) to decide what happens to the programme.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
