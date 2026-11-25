---
name: ux-diagnose
description: "Classify observed UI/UX problems into actionable root-cause categories, identify relevant Laws of UX, and route to remediation. Use for vague usability complaints, confusing screens, screenshots, UX debugging, or when unsure which UX skill applies."
---

# Diagnose a UI/UX issue

## Scope

Use this skill to classify the **observed user failure**, not to recite psychology laws.

## Procedure

1. Establish user goal, surface, device/input modality, interaction state and evidence. If only a screenshot is present, do **not** infer unobserved behavior as fact.
2. Read `references/issue_taxonomy.json` for candidate classes. Assign one primary class, up to two secondary classes and at most three relevant Laws of UX from `references/principles.json`. Use a class that directly describes the likely repair, not a remote psychological association.
3. Use `references/articles.json` for relevant nuanced exceptions, especially novelty versus familiarity, active-user onboarding, complexity transfer, cognitive load and peak/end moments. Read only matching entries—never dump the catalog into the answer.
4. Before prescribing a fix, check `references/cross-law-conflicts.json` for competing heuristics; consult the matching category entries in `references/remediation-recipes.json` for concrete implementation and acceptance tests. Distinguish evidence from mechanism. If more than one explanation fits, specify a discriminating test and state uncertainty.
5. Give an observable fix, likely tradeoff and a verification case. For implementation, consult the relevant specialist skill's `references/playbook.md`; for a full audit use `ux-review`; for coding use `ux-build`.

## Severity

- **Blocker:** core task impossible, data loss, security/privacy/consent hazard, or severe accessibility exclusion.
- **High:** substantial task failure, recurring major error, or high-cost recovery.
- **Medium:** meaningful friction, delay or confusion with workable recovery.
- **Low:** polish or minor inconvenience without material task harm.

Prioritize observed harm, frequency and persistence; a rare but catastrophic problem can outrank frequent minor friction. Avoid invented frequency and severity measurements.

## Output

Concise finding: `ID | symptom | evidence grade | primary class (+secondary) | relevant law(s) and why | impact/confidence | proposed repair | test`. For structured exchange, match `references/issue-record.schema.json` (categories and laws use IDs).

## Boundaries

Laws are explanatory heuristics, not automatic proofs. Accessibility, security, truthful status and user consent supersede optimization and aesthetics. Do not optimize dark patterns or fabricate metrics.
