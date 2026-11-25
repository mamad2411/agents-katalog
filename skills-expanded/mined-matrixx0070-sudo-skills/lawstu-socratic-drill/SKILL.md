---
name: lawstu-socratic-drill
version: 1.0.0
description: Run a live Socratic drill — the skill questions you relentlessly on a doctrine until you find the rule's edges yourself.
author: matrixx0070
tags: [law-student, socratic, active-recall, doctrine, drill]
capabilities: []
---

## When to use

Reach for this when you want to *stress-test* your grasp of a doctrine rather than review it passively. You pick a topic; the skill takes the professor's seat and asks escalating questions, withholding answers so you do the reasoning. It confirms or corrects only after you commit.

**Not for:** getting the doctrine explained to you from scratch (start with your casebook and `lawstu-case-brief`). It also will not answer a graded question on your behalf — the whole method is that *you* produce the answer. Not for timed exam simulation (see `lawstu-exam-forecast`) or flat memorization (see `lawstu-flashcards`).

## Method

1. **Name the target doctrine** and your current confidence (1-5). Decision point: below 3, read first; the drill sharpens understanding, it does not create it.
2. **Warm-up recall.** The skill asks you to state the rule and elements cold, then flags gaps without filling them yet.
3. **Escalate.** Each correct answer earns a harder question: exceptions, splits of authority, then boundary hypotheticals that change one fact.
4. **Force the "why."** After every rule statement, expect "why does the law draw the line there?" — policy is the deep end.
5. **Corner the edge case.** The drill pushes until you hit a fact pattern you cannot resolve; that gap is your study target.
6. **Debrief.** The skill summarizes what you nailed, what wobbled, and what to re-read.

## Example

Topic: adverse possession. You state the elements confidently. Drill: "Open and notorious — is a hidden underground encroachment enough?" You hesitate. It presses: "Why require notoriety at all?" You reach "to give the true owner notice to eject." Now you own the *reason*, so the boundary hypo resolves itself.

## Pitfalls

- Peeking for the answer instead of committing — the productive struggle is the learning.
- Reciting elements without the policy that generates them.
- Treating every split of authority as settled; note majority vs. minority.
- Quitting at the first wrong answer; the drill wants the edge, not comfort.

## Output format

```
Doctrine | starting confidence /5
Transcript: Q → your answer → confirm/correct
Boundary reached: [the hypo you couldn't resolve]
Debrief: solid | wobbly | re-read list
Ending confidence /5
```

## Reference

- **Socratic method:** questioning to the boundary of a rule; answers are earned, not given.
- **IRAC** disciplines each answer — issue, rule, application, conclusion — even in rapid drilling.
- **Bar framing:** the exceptions and authority splits surfaced here are exactly the MBE distractor traps (`lawstu-bar-prep-questions`).
