---
name: wcag-diagnose
description: "Classify accessibility barriers against selected WCAG 2.2 or 2.1 criteria; route repairs by root cause, with WCAG 3.0 draft ideas strictly advisory. Use on unclear accessibility complaints, screenshots, keyboard and screen-reader defects."
---

# Diagnose an accessibility barrier (WCAG 2.1 / 2.2)

## Scope

Read `references/standard-selection.md` and `references/standards.json` first. The W3C recommendation for the **selected version** is authoritative; catalogs are operational summaries. Use `references/issue_taxonomy.json`, followed by that version's criterion entries. Do not preload all the references or every specialist.

## Procedure

1. Establish task, affected page/route, component, state, input modality, device, viewport, browser and AT; distinguish observed evidence from inference. A screenshot cannot prove keyboard or screen-reader behavior.
2. Resolve **standard + level** (explicit requirement > project policy > WCAG 2.2 AA). Cite that choice in the finding. Load `references/2.2/criteria.json` for 2.2 or `references/2.1/criteria.json` for 2.1; exclude criteria above the level. The taxonomy spans versions and is not a conformance list by itself.
3. Classify the problem under one primary barrier category and relevant secondary categories. Map only to applicable criteria with evidence. States: confirmed failure, suspected failure needing manual verification, pass, not applicable, not tested.
4. Differentiate closely related criteria using `references/cross_criterion_conflicts.json`; consult version-matched Understanding and Techniques pages for exceptions. Techniques are informative, not required approaches.
5. Select relevant entries in `references/remediation_recipes.json` and, if needed, the matching specialist `references/playbook.md`. Propose concrete repair and discriminatory verification, not an invented accessibility result.
6. When WCAG 3.0 is explicitly requested, read `references/3.0/draft-guidance.json` and report **draft advisory** observations separately, with the dated snapshot; never blend them into the selected version's conformance matrix.

## Result

`Finding ID | selected WCAG version / level | observed symptom | route/state | evidence vs inference | applicable SC | classification | impact | practical repair | verification steps | confidence`. Use `references/finding.schema.json` for JSON; the criterion must be valid **for that version**, not merely in the schema's combined enumeration.

4.1.1 Parsing is **not** a WCAG 2.2 criterion and is considered always satisfied for HTML/XML in the updated 2.1 recommendation. Fix harmful semantics under the relevant other criteria. Never assert legal compliance or automated certification.
