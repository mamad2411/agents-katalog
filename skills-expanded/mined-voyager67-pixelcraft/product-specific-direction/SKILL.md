---
name: product-specific-direction
description: "Derives a distinctive visual direction from an existing product so AI-assisted redesigns stop collapsing into generic template aesthetics."
license: CC-BY-NC-4.0
---

# Product Specific Direction

## Workflow

1. Inspect product purpose, audience, primary task, content, existing brand assets, and current interface.
2. Identify which visual choices feel generic versus which are authentic product constraints or established brand behavior.
3. Write five direction notes: product, character, world/material, meaningful visual moments, and one signature detail.
4. Propose a palette and typography direction only after the character is clear.
5. Define what must be preserved and what generic patterns should be avoided.
6. Check that the direction is usable across dense app screens, marketing pages, and mobile.
7. Present the direction before implementation unless the user asked to proceed immediately.

## Output

Direction sheet, rationale, preserve/change list, and anti-patterns specific to the product.

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
