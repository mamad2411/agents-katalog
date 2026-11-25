---
name: visual-regression-guard
description: "Creates a repeatable visual regression check for anti-slop redesigns so later AI edits do not reintroduce generic styles or damage established layouts."
license: CC-BY-NC-4.0
---

# Visual Regression Guard

## Workflow

1. Select stable representative routes, viewport sizes, themes, and UI states.
2. Capture baseline screenshots under controlled content and state.
3. Define meaningful invariants: spacing tokens, brand palette, typography roles, icon family, card usage, layout landmarks, and key visual moments.
4. Compare new captures against baseline using screenshot diffs and human review.
5. Triage diffs: intended improvements, dynamic data, harmless rendering noise, or regression.
6. Check DOM/semantic behavior as well as pixels; pixel similarity alone is not quality.
7. Update baselines only after human review and a documented reason.

## Output

Baseline matrix, diff summary, accepted changes, regressions, and reproducible steps.

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
