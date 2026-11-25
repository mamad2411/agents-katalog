---
name: slop-regression-review
description: "Reviews later AI-generated changes for reintroduced slop patterns and protects the design decisions established by a previous remediation pass."
license: CC-BY-NC-4.0
---

# Slop Regression Review

## Workflow

1. Read the original audit, design direction, changed files, and relevant screenshots/baselines.
2. Review the new diff for arbitrary effects, inconsistent tokens, generic copy, fake content, card bloat, responsive regressions, and interaction shortcuts.
3. Check whether new components conform to existing primitives and semantics.
4. Distinguish deliberate product changes from accidental style drift.
5. Run targeted visual and behavior checks on affected routes.
6. Report only actionable regressions with file/line or screen location and a proposed fix.

## Output

Regressions, severity, evidence, affected scope, and merge-blocking recommendation.

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
