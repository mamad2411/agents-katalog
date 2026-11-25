---
name: chart-slop-repair
description: "Repairs decorative or misleading chart components, rainbow palettes, meaningless sparklines, unexplained axes, and dashboard chart clutter."
license: CC-BY-NC-4.0
---

# Chart Slop Repair

## Workflow

1. Identify the decision or question each chart is supposed to support.
2. Verify data source, metric definition, units, time range, aggregation, and missing-data behavior.
3. Remove charts that repeat a headline number without adding trend, comparison, distribution, or relationship insight.
4. Choose chart type based on task; use tables for exact values and avoid misleading truncated axes or 3D effects.
5. Use color only to distinguish meaningful series or highlight a specific signal.
6. Add accessible labels, units, legends, source/freshness cues, and text/table alternatives.
7. Verify responsiveness, empty/error states, and number formatting.

## Output

Chart-by-chart purpose, data validity, design defects, replacement, and accessibility checks.

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
