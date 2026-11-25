---
name: pdes-usability-findings
description: Turns your usability session notes into findings with per task results counted as n of N against the criteria set before testing, what people did beside what they said, an observation sheet by participant id, issues with a proposed 0 to 4 severity and clips to pull. Use for "run pdes-usability-findings", "write up my usability tests", "usability test report", "rate these usability issues", "severity ratings for usability problems", "rainbow spreadsheet", "the tests went well I think", "did my prototype pass", part of the Claude for Product Designers Pack by 90n.
---

# Usability Test Findings

## When To Use
The tests "went well" and your notes say four people failed the core task. Run this straight after your sessions, while the recordings are easy to find and before the friendly debrief becomes the official version. It answers: what happened on each task, which problems matter most, and which moments prove it?

## When Not To Use
If the issues come from your own inspection of the design and not from watching people, they belong in Design Self-Critique. For the standing list of problems across many sources in your product area, use UX Debt Register; this skill reports one round of sessions.

## Inputs
- Session notes, observer grids or transcripts per participant id, with timestamps
- The tasks and the success criteria written before testing
- Who else will rate severity, by role
Use participant ids (P1, P2) and remove names, contact details and anything that identifies a person before pasting.
If you have none of this, I start from the task list and whatever notes exist, and mark the output as a first draft.

## Approach
Severity ratings for usability problems (Nielsen Norman Group, 1994): a 0 to 4 rating from frequency, impact and persistence, with the warning that one rater alone is unreliable. So every rating here is proposed, and your team rates independently before anything is confirmed. Observations go into a rainbow spreadsheet (a public article, 2013): one behaviour per row, one column per participant. Behaviour leads over opinion: a task failed while saying "that was easy" is a failed task. The failure this prevents: you wanted the design to work, so the readout says it did.

## Workflow
1. Ask up to three questions: what were the success criteria per task, written before testing; who else will rate severity; and which tasks matter most to the decision ahead.
2. Count each task as completed, completed with help or not completed, written "[n] of [N]" against those criteria. Never move the bar after seeing the sessions. No percentages from a handful of people.
3. Set what people did beside what they said, task by task. Where the two disagree, behaviour leads and the gap is logged as an observation of its own.
4. Build the sheet: observations as rows, one column per participant id, a mark where that person showed the behaviour. Merge rows that say the same thing in different words. Keep only what was observed; an inference is a question for the next round.
5. Write the issue list, one problem per row: what goes wrong, where, and the evidence (ids, verbatim quotes, timestamps). A symptom seen on three screens may be one cause.
6. Propose severity per issue and write out all three factors: frequency, impact (how hard it is to get past), persistence (once or every time). Scale: 0 not a usability problem; 1 cosmetic, fix if time allows; 2 minor, low priority; 3 major, high priority; 4 catastrophe, fix before release. Mark each "proposed".
7. List the clips to pull: timestamps for every issue proposed at 3 or 4. Then send the issue list to the other raters without your ratings showing, and record the confirmed number.

## Output Format
```markdown
# Usability Test Findings
**Design tested:** [flow, version] | **Sessions:** [N] | **Dates:** [dates] | **Raters:** [roles]
## Task results
| Task | Criterion set before testing | Completed | With help | Not completed | Did beside said |
|---|---|---|---|---|---|
| [task] | [criterion] | [n] of [N] | [n] of [N] | [n] of [N] | [gap, with ids] |
## Observation sheet
| Observed behaviour | P1 | P2 | P[x] |
|---|---|---|---|
| [what was seen] | [x] | [ ] | [x] |
## Issues
| Issue | Where | Evidence (ids, quotes, timestamps) | Frequency | Impact | Persistence | Severity 0 to 4 |
|---|---|---|---|---|---|---|
| [problem] | [screen, step] | P[x] "[verbatim]" [mm:ss] | [n] of [N] | [how hard to get past] | [once / every time] | [proposed] then [confirmed] |
## Clips to pull
- [issue]: P[x] [mm:ss to mm:ss]
## What this round cannot show
[N] people find problems; they do not measure how common a problem is. [Groups not in this round.]
## Decision
[Product manager] decides which issues confirmed at 3 or 4 are fixed before release by [date]; [designer who ran the sessions] proposes the design change for each by [date].
```

## Done When
- Every task shows the three outcomes as "[n] of [N]" against criteria set before testing
- Every issue cites participant ids and at least one timestamp or verbatim quote
- Every severity reads proposed or confirmed, with the three factors written out, and each issue at 3 or 4 has a clip

## Quality Bar
- Behaviour leads; what people said never overrides what they did
- Counts, quotes and timings come from your notes; a gap stays a [placeholder], never a guess
- No commentary on how any participant performed and no labels for people in the shared version
- Issues found by inspection are kept out; this document holds observed sessions only
- Every issue is tied to an observed session; severity rates problems, never the people who met them

## Next
Run pdes-design-handoff-spec (Design Handoff Spec) once the design that goes to engineering is settled.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
