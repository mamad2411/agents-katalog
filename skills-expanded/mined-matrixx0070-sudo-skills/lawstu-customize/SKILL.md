---
name: lawstu-customize
version: 1.0.0
description: Tune how the lawstu skills behave — Socratic intensity, feedback depth, jurisdiction, and output format — without editing the skills.
author: matrixx0070
tags: [law-student, customization, preferences, configuration, tuning]
capabilities: []
---

## When to use

Reach for this when a lawstu skill's default behavior does not fit you — the Socratic drilling is too gentle, the feedback too terse, the citation style wrong, or you want answers scoped to a specific jurisdiction. The skill captures preferences the other lawstu skills read, so you tune once instead of restating every session.

**Not for:** the first-time intake of your courses and goals (see `lawstu-cold-start-interview`), or any change that would weaken the academic-integrity guardrail. This skill cannot be used to make another skill write graded work, supply exam answers, or ghostwrite — those settings are fixed and non-negotiable.

## Method

1. **Name the target.** One skill or a global default. Decision point: if the same tweak applies everywhere (e.g., jurisdiction), set it globally.
2. **Set intensity.** Socratic pressure (gentle → relentless), and how long the skill waits before confirming your answer.
3. **Set feedback depth.** Terse flags vs. detailed coaching; rubric scores on/off.
4. **Set jurisdiction and authority.** Which state's law, majority vs. minority default, UCC vs. common law preference for contracts.
5. **Set output format.** Preferred brief/outline layout, citation style (Bluebook vs. ALWD), and terseness.
6. **Confirm the guardrail is intact.** The skill echoes back that integrity limits remain enforced, then writes the preference set.

## Example

You find `lawstu-socratic-drill` too easy and `lawstu-legal-writing` feedback too thin. You set Socratic intensity to "relentless, no hints until three attempts" and writing feedback to "detailed, paragraph-level." Jurisdiction set to California. Next session both skills apply it automatically — and both still refuse to draft your graded memo.

## Pitfalls

- Turning intensity so high you disengage; calibrate to productive struggle, not despair.
- Setting a jurisdiction you are not actually studying, skewing rule statements.
- Over-terse feedback that hides the *why* of a mistake.
- Expecting customization to unlock ghostwriting — it never will.

## Output format

```
Scope: [skill name / global]
Socratic intensity: [gentle → relentless] | reveal delay
Feedback depth: [terse / detailed] | rubric: on/off
Jurisdiction: [state] | majority/minority default | UCC/common-law
Output: brief/outline layout | citation style | terseness
Guardrail: academic integrity ENFORCED (locked)
```

## Reference

- **Precedence:** these preferences layer on top of the `lawstu-cold-start-interview` profile.
- **IRAC / case-brief / CREAC** layouts are selectable here but their structural integrity is preserved.
- **Bluebook vs. ALWD** citation defaults flow into `lawstu-legal-writing`.
