---
name: multi-page-consistency-review
description: "Finds cross-route AI design drift, inconsistent components, typography, spacing, icon usage, navigation, and repeated generic sections across an application."
license: CC-BY-NC-4.0
---

# Multi Page Consistency Review

## Workflow

1. Select representative routes, states, and viewport sizes; document what was not reviewed.
2. Compare global shell, page headings, content width, section spacing, control sizes, card patterns, forms, tables, and states.
3. Identify shared component drift and route-specific exceptions.
4. Determine whether differences are intentional, due to user roles, or accidental.
5. Fix shared root causes before editing every page individually.
6. Keep the product's distinct workflows intact; don't force all pages into one layout template.
7. Verify a representative route from each affected pattern after the changes.

## Output

Route matrix, cross-page patterns, canonical rules, root-cause fixes, and coverage gaps.

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
