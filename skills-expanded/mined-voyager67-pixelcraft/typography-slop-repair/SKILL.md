---
name: typography-slop-repair
description: "Fixes AI-looking typography: arbitrary font stacks, too many weights and sizes, shouty uppercase labels, compressed small text, weak hierarchy, and inconsistent number styles."
license: CC-BY-NC-4.0
---

# Typography Slop Repair

## Workflow

1. Inventory font families, sizes, weights, line heights, tracking, text roles, and numeric formatting.
2. Preserve licensed and intentional brand fonts; do not change a real brand typeface for novelty.
3. Establish a small hierarchy for display, page heading, section heading, body, label, caption, and metadata.
4. Use weight sparingly; rely on size, position, spacing, and color for hierarchy.
5. Remove wide tracking on ordinary labels, sentence-case unnecessary uppercase, and avoid small low-contrast text.
6. Align numerals and units consistently; check line wrapping and long-language strings.
7. Verify that type scale is responsive and does not overflow.

## Output

Typography audit, type-role map, token changes, and readability verification.

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
