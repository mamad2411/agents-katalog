---
name: color-system-repair
description: "Repairs arbitrary color usage, over-saturated accents, gradients, low contrast, inconsistent semantic colors, and AI-style rainbow interfaces."
license: CC-BY-NC-4.0
---

# Color System Repair

## Workflow

1. Extract colors from code and inspect their actual roles in the rendered UI.
2. Group tokens into background, surface, raised surface, border, primary text, secondary text, muted text, accent, and semantic status.
3. Find unmotivated hues, multiple competing accents, random colored icons, tinted chrome, and repeated gradients.
4. Preserve the brand accent and use it intentionally; neutralize decorative surface color where it competes with data/content.
5. Define semantic success, warning, danger, and information states consistently.
6. Check WCAG contrast for text and interactive boundaries; do not rely on color alone to communicate status.
7. Verify light/dark variants and selected/hover/focus states.

## Output

Color role map, orphan colors, retained brand colors, fixes, and contrast results.

## Non-negotiable rules

- Judge the interface that exists, not assumptions about who or what produced it. AI authorship cannot be reliably inferred from generic visual patterns alone.
- Treat “AI slop” as a shorthand for observable quality problems: generic patterns, weak hierarchy, arbitrary decoration, vague copy, fabricated-looking content, inconsistent systems, or incomplete states.
- A pattern is a signal, not proof. Record evidence, confidence, and plausible benign explanations. Do not label a screen “AI-generated” as a factual finding.
- Preserve user goals, factual content, product behavior, existing brand assets, and working accessibility unless the evidence supports a change.
- Never invent metrics, reviews, customer logos, endorsements, product claims, features, integrations, or data to make a screen look more convincing.
- Inspect rendered output when tools allow it. If you only inspect source code or a screenshot, state that limitation.
- Make the smallest effective change first. Do not replace an existing coherent visual language just to make the result look different.
- Never expose secrets or private information found in a repository. If a secret is detected, do not repeat its value; report only the file and line, stop short of publishing it, and recommend revocation/rotation.

## Completion report

State the signals found, evidence and confidence, fixes made, files changed, checks actually run, and unresolved issues. Distinguish visual review, code review, and runtime testing.
