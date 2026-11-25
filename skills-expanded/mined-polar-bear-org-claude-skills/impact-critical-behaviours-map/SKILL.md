---
name: impact-critical-behaviours-map
description: Maps a sponsor's goal to the few observable actions on the job that would move it, producing one measurable goal in the sponsor's words, a behaviours table with the cause and the fix for each, and a proof table showing how each behaviour would be seen at work. Use for "run impact-critical-behaviours-map", "action mapping", "critical behaviours", "critical behaviors for this training", "what should people do differently", "they need to understand X", "from know to do", "observable behaviours", part of the Claude Guide for Training Impact Pack by 90n.
---

# Critical Behaviours Map

## When To Use
The sponsor says "they need to understand X" and nobody has said what people will do differently. Use this once the problem is agreed and before anyone sets measures or opens your authoring tool. It answers one question: which few actions on the job would move the sponsor's number, and how would anyone see them happening?

## When Not To Use
If nobody has checked whether the gap is a skill gap at all, run Performance Problem Diagnosis first; the map assumes a goal worth acting on. It holds no thresholds and no sign-off on measures: that is Success Measures Agreement. For awareness content with no measure behind it the map is weak; say so to the sponsor instead of inventing a goal.

## Inputs
- The sponsor's request or goal in their own words, and the measure they already watch, with the report it sits on.
- The role in scope, and the list of what the sponsor thinks people should "know" or "understand".
- Your diagnosis or options memo if you have one, with the cause behind each gap.
If you have none of this, I start from the sponsor's one-line request and mark the output as a first draft.

## Approach
Action mapping, from its originator's public page: commit to a measurable business goal, identify what people must do to reach it and the best fix for each action, and keep training only where practice is needed. The Kirkpatrick Model, as set out by Kirkpatrick Partners, adds that Level 3 rests on a few critical behaviours, supported by the performance environment. The judgement is in the cutting: a short list you can see in the work beats a long one nobody will look for. The failure this prevents: a programme built on "understand the new process", evaluated months later by people who cannot say what understanding would have looked like on a Tuesday afternoon.

## Workflow
1. Ask at most three questions, together: which number should move and by when, in the sponsor's words; which role must act differently; and who knows the work well enough to confirm the behaviours (an expert or an experienced manager, as a role).
2. Write one goal: "[measure] will [change] by [date] as [role] [do what]". The measure and the target are the sponsor's. If the target is not set, the bracket stays open and becomes a question for the sponsor; I never supply one. Two goals means two maps.
3. List what people in the role must do, as verbs someone could watch. Rewrite "understand", "know" and "be aware of" by asking "what would they do if they understood it?", and cut whatever survives no rewrite. I mark my own guesses so the expert can confirm or strike them.
4. Keep the few that matter most for the goal. You decide how many; test each with "if people did only this, would the number move?". The others stay visible as "listed, not kept".
5. For each kept behaviour, write why it is not happening now, taken from your diagnosis or marked "assumed", and the fix: training, job aid or process change. Only skill and knowledge causes stay on the training path; the others get an owner role so they are not lost.
6. Fill the proof table: what an observer would see, what trace the behaviour leaves in a record the work already produces, where the occasion comes up and how often (your estimate). A behaviour with no visible sign and no trace is rewritten until it has one, or flagged "cannot be seen, so cannot be evidenced".
7. Add the cut list to the same table: everything the sponsor asked for that links to no behaviour, with one reason each, so the sponsor can object now and not after the build.

## Output Format
```markdown
# Critical Behaviours Map
Programme: [name] | Role in scope: [role] | Sponsor: [role] | Confirms the behaviours: [role] | Status: [first draft / confirmed on date]
## Goal
[measure] will [change] by [date] as [role] [do what]. Measure and target: [the sponsor's own, or "open: ask the sponsor"]
## Critical behaviours
| # | Behaviour (a verb someone could watch) | Why it is not happening now | Evidence, or "assumed" | Fix | On the training path? |
|---|---|---|---|---|---|
| 1 | [role] [checks X before Y] | [cause] | [source / assumed] | [training / job aid / process change, with owner role] | [yes / no] |
## Seen at work
| # | What an observer would see | Trace it leaves in a record | Where the occasion comes up | How often |
|---|---|---|---|---|
| 1 | [visible action] | [existing record, read for the group / none] | [situation] | [your estimate] |
## Listed, not kept, and cut
| Item | Kind | Reason |
|---|---|---|
| [action, topic or "must know"] | [action not critical for this goal / request that links to no behaviour] | [reason] |
## Decision
[Sponsor, role] and [expert, role] confirm the goal and the critical behaviours, or amend them, by [date]. [L&D lead] then takes them into the measures agreement.
```

## Done When
- There is exactly one goal, with the sponsor's measure and a date, and every kept behaviour links to it.
- Every behaviour starts with a verb someone could watch; no "understand", "know" or "be aware of" remains.
- Every kept behaviour has a cause (with evidence or "assumed"), a fix and a filled "seen at work" row.
- The cut list exists and the sponsor has seen it.

## Quality Bar
- A behaviour is specific enough that two observers in the same room would agree on whether it happened.
- A trace is a record the work already produces, read for a group; the map never proposes logging what one individual does.
- Guesses are marked, and a person who knows the work confirms the list. Claude drafts; people in the work correct.
- No target, frequency or figure comes from Claude. An open bracket beats a guess.
- The map holds no thresholds and no course design; both come after it.
- The goal and its measure are the sponsor's; the map describes what a role does, never how a named person performs.

## Next
Run impact-success-measures-agreement (Success Measures Agreement) to turn the goal and behaviours into measures the sponsor signs.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
