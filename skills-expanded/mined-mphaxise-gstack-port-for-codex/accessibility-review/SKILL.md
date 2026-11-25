---
name: accessibility-review
description: Review interfaces and product flows for WCAG-oriented accessibility, assistive technology paths, cognitive load, motion, language, and inclusive use.
---

# Accessibility Review

Use this skill when the user asks whether a UI, workflow, document, or product experience is accessible.

This is a Praneet-specific hand-port enhancement. It expands the existing design and QA layer so accessibility is a first-class quality bar, not a footnote.

## Workflow

1. Identify the experience and supported platforms.
2. Check evidence:
   - source code
   - screenshots
   - running UI
   - design docs
   - existing accessibility tests
3. Review core areas:
   - keyboard and focus order
   - screen reader labels and semantics
   - color contrast and non-color affordances
   - text scaling and responsive layout
   - motion sensitivity
   - form labels, errors, and recovery
   - cognitive load and plain language
   - localization and reading direction when relevant
   - mobile Dynamic Type or platform equivalents
4. Report findings with severity, evidence, and recommended fix.
5. Route follow-up:
   - `design-review` for visual polish
   - `qa` for flow verification
   - `responsible-design-review` for harm or exclusion risks

## Guardrails

- Do not claim WCAG compliance from a superficial scan.
- Do not rely only on color contrast when interaction semantics are unknown.
- If assistive technology testing was not run, say so.
