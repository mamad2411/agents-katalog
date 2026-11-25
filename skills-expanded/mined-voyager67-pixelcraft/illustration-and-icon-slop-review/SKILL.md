---
name: illustration-and-icon-slop-review
description: "Finds inconsistent illustration languages, random 3D icon sets, mismatched stroke styles, and decorative icon clutter in AI-built interfaces."
license: CC-BY-NC-4.0
---

# Illustration And Icon Slop Review

## Workflow

1. Inventory icons and illustrations by family, stroke/fill, perspective, material, scale, and color.
2. Separate utility iconography from editorial/brand illustration.
3. Detect mixtures that have no system rationale: outline plus glossy 3D, mismatched perspectives, random gradients, and mixed corner treatments.
4. Select a coherent family appropriate to product character and platform.
5. Replace meaningless symbols with semantic icons or remove them.
6. Keep illustration style consistent across empty states, onboarding, and marketing where shared identity is intended.
7. Check asset provenance, accessible names, and display at different densities.

## Output

Style inventory, inconsistencies, proposed visual language, and replacement map.

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
