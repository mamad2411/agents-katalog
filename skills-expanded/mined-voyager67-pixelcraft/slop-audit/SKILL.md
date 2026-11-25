---
name: slop-audit
description: "Produces a detailed evidence-based AI-slop audit of one or more UI screens, grouping findings by visual, content, interaction, and implementation symptoms."
license: CC-BY-NC-4.0
---

# Slop Audit

## Workflow

1. Capture the screen context and viewport; list routes and files inspected.
2. Review surface treatments, composition, spacing, type, color, icons, imagery, copy, data displays, interactions, and responsive states.
3. For every finding write: location, observed symptom, user consequence, correction, confidence, and whether the evidence is visual or code-derived.
4. Group repeated symptoms under one root cause (for example, a token scale that causes many spacing defects).
5. Mark unavailable evidence explicitly: untested controls, unseen mobile widths, hidden states, or missing data definitions.
6. End with the five highest-value fixes and a suggested order.

## Output format

1. One-paragraph assessment.
2. Findings table: severity, location, evidence, user impact, confidence, correction.
3. Root causes.
4. Verification gaps.
5. Prioritized remediation plan.

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
