---
name: slop-severity-triage
description: "Ranks AI-slop findings by user harm, trust impact, visibility, recurrence, and repair effort. Use after a slop audit to decide what to fix first."
license: CC-BY-NC-4.0
---

# Slop Severity Triage

## Triage model

Score each finding against: task obstruction, user confusion, trust/factual risk, accessibility impact, screen prominence, recurrence across routes, and estimated effort. Use judgement, not false precision.

- **P0 / blocker:** misleading or fabricated claims/data, broken critical task, exposed private information, severe accessibility barrier, or destructive interaction risk.
- **P1 / high:** prominent hierarchy failure, unreadable content, critical responsive failure, or repeated inconsistency that materially impairs use.
- **P2 / medium:** visible generic styling, excess decoration, copy ambiguity, moderate density issues, or inconsistent states.
- **P3 / polish:** minor alignment, subtle token drift, or low-impact decoration.

## Workflow

1. Merge duplicate symptoms into root-cause findings.
2. Assign severity with a one-sentence rationale and evidence.
3. Estimate blast radius: one element, one component, one route, or system-wide.
4. Identify quick fixes versus systemic repairs.
5. Sequence fixes to avoid rework (tokens before component overrides; copy before final layout; layout before motion).
6. Note dependencies and risks; do not rank cosmetic cleanup above factual or task-critical defects.

## Output

Prioritized backlog with severity, impact, affected scope, effort band, dependencies, and first action.

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
