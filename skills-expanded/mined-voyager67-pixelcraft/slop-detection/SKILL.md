---
name: slop-detection
description: "Detects observable AI-slop patterns in UI screenshots, live interfaces, and frontend code without claiming to determine authorship. Use for first-pass recognition across a product surface."
license: CC-BY-NC-4.0
---

# Slop Detection

## Workflow

1. Establish the product, audience, primary task, route, viewport, and available evidence.
2. Inspect the rendered UI first when possible, then trace suspicious patterns to source components and styles.
3. Scan these signal families: template convergence; decorative effects; excessive cards and pills; random spacing/radii; type hierarchy; emoji/icon inconsistency; generic copy; unsupported proof; placeholder charts/data; incomplete interaction states; responsive breakage; accessibility regressions; generic imagery.
4. For each signal, quote or describe the exact visible evidence and location. Explain why it harms clarity, trust, coherence, or usability.
5. Assign confidence (high/medium/low) and note benign explanations, such as legitimate brand language, data density, or platform conventions.
6. Separate confirmed defects from style preferences and from uncertain suspicions.
7. Recommend a minimal repair sequence based on user impact, not the number of patterns found.

## Do not

Do not use AI-content detectors, metadata guesses, or stereotypes to infer the creator. Do not diagnose “AI-generated” from purple gradients, sans-serif fonts, or rounded cards alone.

## Output

A signal inventory with location, evidence, confidence, impact, benign alternative, and recommended next step.

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
