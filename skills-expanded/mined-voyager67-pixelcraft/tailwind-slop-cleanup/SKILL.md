---
name: tailwind-slop-cleanup
description: "Cleans AI-generated Tailwind CSS marked by arbitrary values, class soup, duplicated utilities, inconsistent spacing, and fragile responsive overrides."
license: CC-BY-NC-4.0
---

# Tailwind Slop Cleanup

## Workflow

1. Inspect source components, Tailwind config/theme, custom CSS, and rendered output.
2. Find repeated arbitrary values, conflicting utilities, long conditional class expressions, and breakpoint overrides that fight one another.
3. Consolidate recurring values into theme tokens or component variants when justified.
4. Replace one-off classes with consistent utilities while preserving intentional optical adjustments.
5. Simplify responsive classes and check specificity/ordering behavior.
6. Do not remove classes based only on text search when dynamic composition or variants are involved.
7. Run build, lint, and visual checks after cleanup.

## Output

Problem patterns, representative before/after, token decisions, and tests actually run.

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
