---
name: card-bloat-repair
description: "Finds and fixes over-cardification: unnecessary panels, nested cards, stat tiles, pill containers, and surfaces that fragment content without adding structure."
license: CC-BY-NC-4.0
---

# Card Bloat Repair

## Workflow

1. Count and classify card-like containers by semantic purpose.
2. Identify nested cards, cards containing one label/value, decorative stat tiles, and repeated panels around content that already has grouping.
3. Ask whether each container provides comparison, action, independent ownership, or meaningful separation.
4. Replace unnecessary boxes with spacing, dividers, headings, lists, tables, or a shared surface.
5. Preserve cards for genuinely independent objects, actions, or scannable groups.
6. Normalize padding, border, radius, and internal hierarchy for remaining cards.

## Quality checks

Ensure the result does not become an unstructured wall of text. Retain grouping through whitespace and alignment.

## Output

Removed/retained card inventory, rationale, layout changes, and density check.

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
