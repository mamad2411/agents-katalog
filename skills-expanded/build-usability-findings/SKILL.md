---
name: build-usability-findings
description: Turns your session notes into Usability Test Findings with completed, completed with help and not completed per task against the criteria set before testing, what people did beside what they said, a sheet with one observation per row, problems with a proposed severity and the moments to show. Use for "run build-usability-findings", "read my usability test notes", "what did the user tests show", "rate these usability problems", "write up the prototype sessions", "the sessions went well I think", "which problems matter most", "what should I change after testing", part of the Claude for Product Builders Pack by 90n.
---

# Usability Test Findings

## When To Use
The sessions "went well" and your notes say four people could not finish the main task. Run it after a round with real target users, while the notes and recordings are easy to find. It answers: what happened on each task, which problems matter most, and what should change in the prototype?

## When Not To Use
If no real user has seen the prototype yet, run Prototype Heuristic Review, which finds likely problems and never reports a finding. To say whether the belief held against its pass line, run Prototype Learning Card. This skill describes what happened per task and stops there.

## Inputs
- Session notes or observer grids per participant code, with time marks, and the prototype version each person saw.
- The test plan: the tasks and the success criteria written before testing.
- Before you paste: replace names with codes (P1, P2) and remove contact details, employers and anything that identifies a person.
If you have none of this, I start from the task list and whatever notes exist, and mark the output as a first draft.

## Approach
Severity ratings for usability problems (Nielsen Norman Group, https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/): frequency, impact and persistence give a rating from 0 to 4, set by more than one rater because one rater alone is too unreliable to trust. Observations are collected in a rainbow spreadsheet (Smashing Magazine, 2013, https://www.smashingmagazine.com/2013/04/rainbow-spreadsheet-collaborative-ux-research-tool/): observations as rows, participants as columns. Behaviour outranks opinion: a task abandoned while saying "this is easy" is still not completed. The failure this prevents: a polite debrief that carries a broken flow into the next demo.

## Workflow
1. Ask at most three questions: what were the success criteria per task, written before testing; who else will rate severity; which tasks matter most to the belief on the test card?
2. Per task, count completed, completed with help and not completed, each as "[n] of [N]" against those criteria. The bar never moves after the data. The pilot with a colleague is not counted.
3. Per task, set what people did beside what they said. Where the two disagree, behaviour leads and the gap is itself logged.
4. Build the sheet: one observation per row, one column per participant code, a mark where that participant showed it. Merge rows that describe the same behaviour in different words.
5. Write the problem list: the problem, where it happens, and the evidence (participant codes, exact words, time marks). One problem per row. A symptom seen on three screens may be one cause.
6. Propose a severity per problem from frequency, impact (how hard it is to get past) and persistence (once or every time): 0 not a problem, 1 cosmetic, 2 minor, 3 major, 4 catastrophe. Mark each "proposed". At least one more person rates independently before any is confirmed.
7. End on the prototype: one line per problem on what to change, and the moments to show, with time marks for every problem rated 3 or 4. Clips are shown only within the consent given.

## Output Format
```markdown
# Usability Test Findings
**Round:** [number] | **Sessions:** [N] real target users | **Prototype version:** [label] | **Raters:** [roles]
## Task results
| Task | Criterion set before testing | Completed | With help | Not completed | Did beside said |
|---|---|---|---|---|---|
| [task] | [criterion] | [n] of [N] | [n] of [N] | [n] of [N] | [gap, with codes] |
## Observation sheet
| Observation | P1 | P2 | P[x] |
|---|---|---|---|
| [what was seen] | [x] | [ ] | [x] |
## Problems and severity
| Problem | Where | Evidence (codes, exact words, time marks) | Frequency | Impact | Persistence | Severity 0 to 4 |
|---|---|---|---|---|---|---|
| [problem] | [screen, step] | P[x] "[exact words]" [time mark] | [n] of [N] | [note] | [once / every time] | [rating], [proposed / confirmed] |
## What to change in the prototype
| Problem | Change | Why | Moment to show (problems rated 3 or 4, within the consent given) |
|---|---|---|---|
| [problem] | [change] | [evidence] | P[x], [time mark to time mark] |
## Decision
[The builder, by role] confirms the severity ratings with a second rater and chooses which problems go into the iteration plan by [date].
```

## Done When
- Every task shows completed, with help and not completed as "[n] of [N]" against criteria written before testing.
- Every problem cites participant codes and at least one time mark or exact quote.
- Every severity is marked proposed or confirmed with the raters named by role, and every problem rated 3 or 4 has a change proposed and a moment to show.

## Quality Bar
- Severity uses the 0 to 4 scale with frequency, impact and persistence written out, never a gut label.
- Severity rates problems, never the people who met them. No commentary on how any one participant performed.
- Counts are "[n] of [N]" for this round and this version. Five sessions give no percentages.
- Every finding comes from a real session; no completion count, quote or reaction is invented or predicted.

## Next
Run build-iteration-plan (Prototype Iteration Plan) to choose what changes before the next round and track which version each person saw.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
