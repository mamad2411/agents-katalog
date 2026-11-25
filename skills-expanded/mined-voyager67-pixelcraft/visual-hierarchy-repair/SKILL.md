---
name: visual-hierarchy-repair
description: "Repairs flat or chaotic AI-built hierarchy by clarifying primary task, scan path, grouping, contrast, scale, and information density."
license: CC-BY-NC-4.0
---

# Visual Hierarchy Repair

## Workflow

1. State the primary user question or action for the screen.
2. Sort elements into primary, secondary, supporting, and peripheral roles.
3. Trace a natural scan path and identify competing focal points, oversized labels, equal-weight cards, and hidden actions.
4. Use position, whitespace, grouping, scale, and semantic structure before adding color or decorative emphasis.
5. Make related content visually related and unrelated sections distinct.
6. Preserve meaningful density in data-heavy screens; avoid turning everything into giant whitespace.
7. Check hierarchy at narrow widths and under zoom.

## Output

Intended scan path, hierarchy defects, reordering/scaling changes, and density trade-offs.

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
