---
name: design-system-slop-repair
description: "Repairs inconsistent, overgrown, and token-poor design systems that produce repetitive AI UI slop across multiple pages."
license: CC-BY-NC-4.0
---

# Design System Slop Repair

## Workflow

1. Inspect existing tokens and components before proposing a new system.
2. Map color, type, spacing, radius, borders, elevation, icons, and motion to semantic roles.
3. Detect duplicates, arbitrary one-off values, unused variants, and conflicting defaults.
4. Identify components that differ visually despite serving the same task, plus components forced into one pattern despite distinct needs.
5. Normalize foundational tokens and a small set of reusable primitives.
6. Document exceptions so brand moments and density variations remain intentional.
7. Migrate incrementally and verify representative screens after each foundational change.

## Output

Current-state audit, target token/component map, prioritized migration, exceptions, and regression checks.

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
