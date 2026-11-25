---
name: mobile-ui-slop-repair
description: "Improves mobile interfaces that look like desktop layouts compressed into a phone, with cramped cards, tiny charts, oversized headers, and awkward navigation."
license: CC-BY-NC-4.0
---

# Mobile Ui Slop Repair

## Workflow

1. Inspect the mobile task and likely one-handed interaction context.
2. Identify desktop assumptions: permanent sidebars, multi-column KPI grids, tiny controls, horizontal carousels hiding essential content, hover-only hints, and fixed footers obscuring fields.
3. Prioritize mobile information and action sequence.
4. Convert navigation to a compact, labeled pattern; preserve access to all essential destinations.
5. Make data views readable through summaries, progressive disclosure, or horizontally scrollable tables with clear affordance.
6. Use appropriately sized touch targets and safe-area spacing.
7. Check keyboard behavior for mobile browser use and screen reader semantics.

## Output

Mobile-specific findings, new flow/layout, responsive states, and tested widths.

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
