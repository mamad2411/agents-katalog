---
name: spacing-rhythm-repair
description: "Detects arbitrary margins, padding, gaps, row heights, and alignment drift that make AI-built interfaces feel uneven; repairs the spacing rhythm."
license: CC-BY-NC-4.0
---

# Spacing Rhythm Repair

## Workflow

1. Inspect spacing tokens and rendered repetition across navigation, forms, lists, cards, sections, and page edges.
2. Identify one-off values, inconsistent same-level gaps, misaligned columns, and padding unrelated to density.
3. Derive a compact spacing scale from the existing design; use a consistent base grid where appropriate rather than forcing every value into one rule.
4. Make repeated components share dimensions and alignment.
5. Use smaller gaps within groups and larger gaps between groups.
6. Recheck after typography and layout changes because content wrapping changes rhythm.

## Output

Spacing defects, chosen scale, component-level normalizations, and viewport verification.

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
