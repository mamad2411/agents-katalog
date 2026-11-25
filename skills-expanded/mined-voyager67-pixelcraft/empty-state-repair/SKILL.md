---
name: empty-state-repair
description: "Replaces generic empty-state filler and decorative illustrations with clear explanations, next actions, and honest zero-data states."
license: CC-BY-NC-4.0
---

# Empty State Repair

## Workflow

1. Inspect empty states for first-use, no-results, no-activity, filtered-empty, and permission-restricted conditions.
2. Determine why the state exists; do not use one generic illustration/copy for every case.
3. Explain what is empty in the current context using direct language.
4. Provide one relevant next action where possible, or a clear way to change filters/search.
5. Never invent records, sample activity, or false progress to make the screen feel populated.
6. Keep illustration secondary; use product-relevant visuals only when they clarify the state.
7. Check keyboard, screen reader, and responsive presentation.

## Output

State classification, revised copy/action, removed decoration, and state coverage.

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
