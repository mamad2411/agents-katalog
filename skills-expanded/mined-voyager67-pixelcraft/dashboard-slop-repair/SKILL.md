---
name: dashboard-slop-repair
description: "De-generifies AI-built dashboards by removing meaningless stat cards, redundant charts, generic greetings, ungrounded trends, and weak information hierarchy."
license: CC-BY-NC-4.0
---

# Dashboard Slop Repair

## Workflow

1. Determine the dashboard user's job and the decision they make from it.
2. Inventory KPIs, date ranges, filters, charts, tables, status, and alerts.
3. Verify every metric definition and comparison; flag unknown semantics.
4. Establish a hierarchy from primary signal to supporting breakdowns and exceptions.
5. Remove redundant stat tiles, fake mini-charts, and chart-shaped decoration.
6. Replace generic greetings and labels with contextual headings and direct task language.
7. Design stale, loading, empty, partial, and error states.
8. Check data density, table fallbacks, responsive behavior, and focus order.

## Output

Dashboard decision map, removed/reworked patterns, metric questions, implementation changes, and verification.

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
