---
name: slop-remediation-quality-gate
description: "Verifies an AI-slop remediation pass has actually improved the interface without breaking behavior, accessibility, responsiveness, or product identity."
license: CC-BY-NC-4.0
---

# Slop Remediation Quality Gate

## Workflow

1. Compare the original audit with the proposed changes; every finding should be fixed, deferred with reason, or disproven.
2. Inspect the final UI at matching routes, viewport, theme, and content where possible.
3. Check visual consistency, readable hierarchy, meaningful color, appropriate imagery, and removal of unsupported claims.
4. Test key interactions, loading/empty/error states, forms, navigation, and destructive actions.
5. Check responsive widths, keyboard focus, semantic labels, contrast, and reduced motion.
6. Run relevant build/lint/test commands if available.
7. Record limitations and regressions rather than declaring a blanket pass.

## Output

Pass/fail by category, evidence, checks run, unresolved findings, and release recommendation.

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
