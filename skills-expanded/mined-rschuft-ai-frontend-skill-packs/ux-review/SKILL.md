---
name: ux-review
description: "Review or audit existing user interfaces, UX journeys, screenshots, prototypes, or code for usability issues; produce evidence-graded, prioritized findings linked to Laws of UX and testable remediation."
---

# Perform a user-centered UX review

## Scope

Use for reviews, audits, critique and issue triage **without assuming permission to change code**.

Read `references/evidence-and-priority.md` when you need to grade evidence, resolve conflicting interpretations, or rank complex findings.

## Procedure

1. Identify audience, task goals, critical journeys, product constraints, responsive modes and available evidence. If artifacts exist, inspect them; don't guess from descriptions that conflict with artifacts.
2. Walk the journey in goal order: entry, locate, decide, act, wait, errors/recovery, completion, return. For each observed failure, apply the taxonomy from `../ux-diagnose/references/issue_taxonomy.json` and the relevant domain playbook.
3. Inspect cross-cutting accessibility, semantics, keyboard/motion, loading/error states and trust. Keep aesthetics separate from usability. Do not claim WCAG conformance from a screenshot.
4. Report only substantiated or clearly marked hypothesized findings. Record exact screen/component or step and concrete expected-versus-actual behavior. Limit each finding to 1 primary class + up to 2 supporting laws when possible.
5. Rank by user harm (including low-frequency severe harms), observed frequency, persistence and recovery cost. Separate fixes that remove the cause from visual patches.
6. For each finding: proposed change, tradeoff, and a measurable/observable acceptance check. Offer quick wins and systemic changes without pretending untested suggestions are validated.

Default output: a short executive diagnosis, then an ordered issue table with `ID, evidence, location, user impact, primary class, law, severity, confidence, fix, validation`. Do not produce counts or decorative scores merely to signal thoroughness. If the user requested JSON, use the issue-record schema. Cite the exact law URL when relying on it.
