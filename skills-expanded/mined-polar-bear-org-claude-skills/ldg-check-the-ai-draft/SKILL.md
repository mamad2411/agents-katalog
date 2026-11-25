---
name: ldg-check-the-ai-draft
description: Checks an AI-drafted course before release, tracing every factual claim to an approved source or flagging it, aligning objective, practice and check row by row, and recording five accessibility checks, a learning-myth and bias scan, the update owner and the expert sign-off. Use for "run ldg-check-the-ai-draft", "check AI generated training content", "AI content review", "fact check this course", "quality check before release", "QA checklist for e-learning", "the course looks right but teaches nothing", "SME sign-off record", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Check the AI Draft

## When To Use
AI drafts the course, AI reviews it, and no person checks that it teaches anything. Use this on any draft (storyboard, built course, job aid, knowledge check) before a learner sees it. It gives the expert a short list of what to confirm and fix, and gives you a record of who released which version.

## When Not To Use
To plan who reviews what and in which round, use Plan the Reviews; this is the check itself, on paper. It does not replace putting the draft in front of learners, which is Run the Learner Walkthrough, nor a test with real assistive technology.

## Inputs
- The draft with its version, the approved sources (procedure, policy, the expert's notes) and the design document or the objectives.
- The accessibility level you work to (A or AA), the signing expert and the update owner.
If you have none of this, I start from the draft alone, flag every claim as untraced, and mark the output as a first draft.

## Approach
Two checks carry this: accessibility against WCAG 2.2 (W3C) at the level you set, and alignment of objective, practice and check against the design document, row by row. The rule that matters: Claude flags, the expert fixes. A polished tone is not evidence. The failure this prevents: a fluent module where a step of the procedure has quietly changed order, the reviewer reads it in ten minutes, finds nothing ugly, and it goes live.

## Workflow
1. Ask at most three questions: which sources count as approved, which accessibility level (A or AA), and who signs.
2. Accuracy: list every factual claim (numbers, rules, steps, names) with its location. Trace each to an approved source and the place in it. Status is traced, untraced or conflicts. I never correct a fact; I show what the source says beside what the draft says.
3. Alignment: per objective, note the level of the practice and of the check. Flag a recall check under an apply objective, and any screen that serves no objective.
4. Teaching check: does each objective have practice with feedback, or only content? An objective with content only is flagged to the designer. This is the row that answers "looks right, teaches nothing".
5. Accessibility, five items: text alternatives (1.1.1), captions (1.2.2), contrast (1.4.3), keyboard (2.1.1), visible focus (2.4.7). Result is pass, fail or "cannot check here", which is an honest answer for anything I cannot see in the file. Legal conformance: check with a qualified adviser.
6. Myth and bias scan: unsupported learning claims (for example matching content to "learning styles"), and stereotyped examples, names or roles. Each is flagged with its location for a person to judge. Then record the update owner, the review date and the expert sign-off: name, role, version, date, and release or fix first.

## Output Format
```markdown
# AI Draft Check
Draft: [name, version] | Approved sources: [list] | Accessibility level: [A or AA] | Update owner: [name] | Review date: [date]
This check does not replace a learner trying the draft.
## Accuracy
| Claim | Location | Approved source and place | Status | For the expert |
|---|---|---|---|---|
| [claim] | [screen or page] | [source, section] | [traced, untraced, conflicts] | [what the source says] |
## Alignment and teaching
| Objective (level) | Practice (level) | Feedback on the practice | Check (level) | Flag |
|---|---|---|---|---|
| [objective] | [activity, or content only] | [yes or no] | [item] | [none, level mismatch, no practice, no objective] |
## Accessibility, myth and bias
| Item | Result | Where | Owner |
|---|---|---|---|
| Text alternatives (1.1.1) | [pass, fail, cannot check here] | [screen] | [name] |
| Captions (1.2.2) | [result] | [screen] | [name] |
| Contrast (1.4.3) | [result] | [screen] | [name] |
| Keyboard (2.1.1) | [result] | [screen] | [name] |
| Visible focus (2.4.7) | [result] | [screen] | [name] |
| Myth or bias flag: [claim or example] | [unsupported, stereotyped] | [screen] | [who judges] |
## Expert sign-off
Expert: [name] | Role: [role] | Version: [version] | Date: [date] | Call: [release or fix first]
## Decision
[Expert name] releases the draft or returns it for fixes by [date]; [update owner name] reviews it again by [date].
```

## Done When
- Every factual claim is traced or flagged, with its location.
- Every objective row shows its practice, its feedback and its check.
- The five accessibility items each carry a result, and the sign-off names an expert, a version and a date.

## Quality Bar
- No fact is silently corrected; a conflict shows both versions.
- "Cannot check here" is never rounded up to a pass.
- The check says once, in plain words, that it does not replace a learner trying the draft.
- Claude checks and flags; a named expert signs the draft off before any learner sees it.

## Next
Run ldg-run-the-learner-walkthrough (Run the Learner Walkthrough), because a draft that passes on paper can still lose a learner.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
