---
name: table-density-repair
description: "Repairs AI-generated tables with weak alignment, inconsistent number formatting, needless card wrappers, excessive controls, and unreadable mobile behavior."
license: CC-BY-NC-4.0
---

# Table Density Repair

## Workflow

1. Identify the table's primary lookup, comparison, or action task.
2. Audit columns, labels, units, number formatting, sort/filter controls, row density, and column priority.
3. Remove redundant wrappers and decorative sparklines that do not support comparison.
4. Align text left and numeric values consistently; use tabular numbers where suitable.
5. Define empty/loading/error states and accessible row/column headers.
6. Make overflow discoverable or transform the table into a mobile-appropriate list with retained data relationships.
7. Check keyboard navigation and focus in interactive cells.

## Output

Column map, density defects, responsive strategy, and accessibility verification.

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
