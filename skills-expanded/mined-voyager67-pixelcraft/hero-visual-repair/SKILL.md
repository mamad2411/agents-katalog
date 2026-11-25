---
name: hero-visual-repair
description: "Recognizes generic AI hero visuals and rebuilds the first screen around product meaning, composition, credible imagery, and clear text placement."
license: CC-BY-NC-4.0
---

# Hero Visual Repair

## Workflow

1. Identify what the hero must communicate in the first few seconds.
2. Inspect the current image, background, text safe area, product preview, CTA, and visual focal point.
3. Flag generic abstract blobs, random 3D objects, stock-photo clichés, floating UI-card collages, and unrelated imagery.
4. Choose a better visual from actual product output, a relevant object/environment, a functional diagram, or a restrained typographic composition.
5. Place text in calm space, maintain contrast, and avoid stacking too many competing actions.
6. Check crop behavior, alt text, image focal point, and mobile stacking.
7. Generate imagery only when the user has requested it or approved the specific image component; do not generate a substitute for missing product evidence.

## Output

Hero purpose, visual diagnosis, composition plan, image brief if needed, and responsive checks.

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
