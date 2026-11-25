---
name: wcag-pointer-and-touch
description: "Fix WCAG 2.1/2.2 touch/gesture alternatives, pointer cancellation, voice-visible label matching, motion activation, target size and WCAG 2.2 AA minimums and concurrent inputs. Use for mobile and pointer access problems."
---

# Pointer, touch and motion input

## Scope

**Trigger:** Gesture alternatives, cancellation, visible label alignment, target size, motion sensors. **Diagnosis question:** Is an alternative input route missing or a pointer target difficult to operate?

Base WCAG 2.1 criteria: **2.5.1, 2.5.2, 2.5.3, 2.5.4, 2.5.5, 2.5.6**. See the detailed operational guidance in `references/playbook.md`. For every targeted SC, read the matching entry in the selected `../wcag-diagnose/references/2.2/criteria.json` or `../wcag-diagnose/references/2.1/criteria.json`, including its normative link, applicability/exception warning and method. A standard's original text always prevails over these notes.

## Procedure

1. Reproduce observed barrier on actual page/component, state, input modality and user task. Distinguish a confirmed fail from suspected fail or non-applicable SC.
2. Use playbook differential diagnosis to choose the specific requirement, not a catch-all accessibility label. Consult `../wcag-diagnose/references/cross_criterion_conflicts.json` when several SCs appear related.
3. Implement the smallest robust remediation, preferring native semantics and accessible functionality over superficial ARIA or test suppression. Check normal, focused, disabled, loading and error states relevant to this feature.
4. Verify with criterion-specific steps from the catalog and playbook, including manual/assistive-technology checks where required. Record evidence and browser/AT context; automated tool output alone is not WCAG conformance proof.
5. For comprehensive review use `wcag-review`; for implementation orchestration use `wcag-build`; for post-change assurance use `wcag-validate`.

## Failure discipline

WCAG 2.2 AA 24 CSS-px target-size/spacing rule differs from 2.1 AAA 44 CSS-px target size. Never label an item as a failure under the selected WCAG version from visual appearance alone when behavioral evidence is required. Distinguish A/AA/AAA and applicability exceptions. Report exact user harm, criterion ID, practical repair and test. Do not assert legal compliance.

## WCAG version selection (required)

Before classifying a normative failure, resolve **standard + level** according to `../wcag-diagnose/references/standard-selection.md`. Precedence: explicit task/contract > consuming-project `.frontend-a11y.json` or unambiguous project policy > **WCAG 2.2 AA**. Record the chosen version and level. Read `../wcag-diagnose/references/standards.json` and the versioned criterion catalog through `wcag-diagnose` (2.2: `2.2/criteria.json`; 2.1: `2.1/criteria.json`). Never apply 2.2-only criteria to 2.1; never test 4.1.1 Parsing in 2.2. **WCAG 3.0** is an opt-in, dated Working Draft research lens only; its guidance is never an active 2.x conformance criterion. If project sources conflict, disclose and resolve before a conformance statement.

**WCAG 2.2 additions:** 2.5.7 AA: author-created drag operations need a single-pointer, non-drag alternative unless an exception applies; keyboard-only alternatives do not suffice. 2.5.8 AA: at least 24×24 CSS-px hit areas or applicable spacing/other exceptions; measure actual hit regions.
