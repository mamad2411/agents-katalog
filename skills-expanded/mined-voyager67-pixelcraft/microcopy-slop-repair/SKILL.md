---
name: microcopy-slop-repair
description: "Rewrites generic, hype-heavy, repetitive, or robotically phrased UI copy into concise and product-specific interface language."
license: CC-BY-NC-4.0
---

# Microcopy Slop Repair

## Workflow

1. Gather all visible strings and group them by role: headings, labels, actions, helper text, status, errors, empty states, and confirmations.
2. Flag generic filler such as “Welcome back”, “Unlock your potential”, “Seamless experience”, vague feature blurbs, and redundant exclamation marks.
3. Rewrite labels around the user's task and action; use concrete nouns and verbs.
4. Preserve factual meaning, legal conditions, product terminology, and accessibility context.
5. Make errors explain what happened and how to recover; make empty states explain what is absent and what the user can do next.
6. Keep claims verifiable and avoid overpromising.
7. Check consistent voice, capitalization, punctuation, and localization expansion.

## Output

Before/after copy table, rationale, terminology decisions, and claims requiring confirmation.

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
