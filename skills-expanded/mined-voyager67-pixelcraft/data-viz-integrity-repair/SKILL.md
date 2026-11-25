---
name: data-viz-integrity-repair
description: "Reviews charts and data visualizations for misleading scale, arbitrary color, fake sample numbers, unexplained units, inaccessible encodings, and visual noise."
license: CC-BY-NC-4.0
---

# Data Viz Integrity Repair

## Workflow

1. Trace every data series to a supplied source or clearly labeled sample dataset.
2. Verify metric definitions, aggregation, units, missing values, and time windows.
3. Check axis start/scale, binning, truncation, sorting, and visual encoding for misleading implications.
4. Match chart form to the comparison/trend/distribution question.
5. Use color consistently and add labels/markers so meaning survives grayscale or color-vision differences.
6. Provide exact values and an accessible table or text equivalent.
7. Label freshness and source when those details matter.

## Output

Data provenance status, analytic validity, visual corrections, and accessible equivalent.

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
