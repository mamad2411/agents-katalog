---
name: design-diagnose
description: "Diagnose visual composition and art-direction problems in UI screenshots or code, including hierarchy, color, typography, and layout. Use when a page looks visually inconsistent or unpolished."
---

# Diagnose visual design issues

## Scope

Use **visual evidence first**, not taste labels. This skill explains *why* a composition does not convey the intended message. If an observed issue is primarily interaction friction route to `ux-diagnose`; if it is an accessibility barrier route to `wcag-diagnose` too.

## Procedure

1. Record the surface and audience, user task, design intent, brand constraints, viewport/theme, and observations. Do not infer click behavior, responsive failures or screen-reader behavior from one image.
2. Load `references/issue_taxonomy.json`: select **one primary** of ten practical repair categories and zero to two secondary ones. Use `references/principles.json` to associate at most three of the original seven composition principles. `references/elements.json` helps describe the material causing the issue (color, texture, space, etc.).
3. Distinguish symptoms from mechanism: for example, "CTA disappears against photo" -> hierarchy/contrast or image treatment, **not** automatically a color-theory problem. Compare alternatives using the appropriate article summary in `references/articles.json` and Gestalt concepts where relevant.
4. Read `references/cross_principle_conflicts.json` for at least one relevant tradeoff. Filter `references/remediation_recipes.json` to matching category/observation. Load only the matching `design-*` specialist's `references/playbook.md` when implementing.
5. Propose the smallest coherent repair that preserves the underlying user task. Test at relevant widths/themes, through grayscale, with real copy and content length. Never claim a design "fails" a subjective principle as if it were a technical standard.

## Evidence grades and prioritization

- **Confirmed:** screenshot or browser/code observation directly supports the issue; observational limits explicitly stated.
- **Hypothesis:** design mechanism inferred; discriminate with a screen comparison, brief check, measured contrast or user test.
- Prioritize a blocked task or inaccessible content over a weak aesthetic; after those, prioritize task-relevant salience, reproducible confusion and cross-screen visual drift over personal preference.

## Output

`finding ID | observed symptom | evidence/uncertainty | primary category | relevant design principle(s) | user/brand impact | smallest repair | competing tradeoff | acceptance test`. For machine-readable records use `references/finding.schema.json`.

## Boundaries

Digital Polo articles provide design heuristics, not normative accessibility standards. User goals, truthful interface state, consent and applicable WCAG criteria outrank aesthetic optimization. If appropriate, activate `ux-*` and `wcag-*` alongside this skill. Do not bulk-load the whole article catalog into output.
