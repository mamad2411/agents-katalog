---
name: content-density-repair
description: "Balances information density when AI-built interfaces are either excessively sparse with decorative whitespace or overcrowded with repeated cards and labels."
license: CC-BY-NC-4.0
---

# Content Density Repair

## Workflow

1. Identify the user's task, scan pattern, and information needed at the point of action.
2. Measure meaningful content versus decorative space, repeated labels, cards, summaries, and empty gaps.
3. Find both extremes: sparse screens padded with generic marketing fluff and dense screens with no grouping or prioritization.
4. Consolidate repeated facts, promote the most useful information, and move secondary details to progressive disclosure where appropriate.
5. Use tables/lists for comparable information and prose for explanation; do not card-wrap every item.
6. Preserve reading order, accessibility, and mobile usability.
7. Verify the page still has enough context and does not hide critical details.

## Output

Density diagnosis, retained/removed content, revised grouping, and scan-time rationale.

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
