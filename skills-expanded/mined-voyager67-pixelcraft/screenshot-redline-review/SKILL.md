---
name: screenshot-redline-review
description: "Performs a visual redline pass from screenshots or browser captures, mapping visible AI-slop patterns to precise implementation changes."
license: CC-BY-NC-4.0
---

# Screenshot Redline Review

## Workflow

1. Record screenshot dimensions, theme, state, and known viewport; do not assume unseen behavior.
2. Divide the screen into regions: navigation, header, primary content, supporting content, actions, and footer.
3. Annotate spacing, alignment, hierarchy, typography, contrast, effects, icons, imagery, and content issues with exact visible locations.
4. Distinguish pixel-level defects from systemic design problems.
5. Map each redline to likely source components/styles when code is available.
6. Provide change descriptions that can be implemented and verified.
7. When comparing before/after, use equivalent viewport, state, and data.

## Output

Redline checklist, implementation mapping, uncertainty from screenshot-only evidence, and acceptance criteria.

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
