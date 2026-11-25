---
name: responsive-slop-repair
description: "Finds and fixes responsive slop such as desktop UI squeezed into mobile, overflow, hidden content, awkward stacking, and broken fixed elements."
license: CC-BY-NC-4.0
---

# Responsive Slop Repair

## Workflow

1. Inspect existing breakpoints and render at narrow, medium, and wide widths.
2. Identify horizontal overflow, clipped text, awkward wrapping, overlapping fixed controls, tiny desktop-scaled charts, and hidden priority content.
3. Reflow according to task order, not just CSS stacking order.
4. Replace dense multi-column layouts with appropriate mobile patterns, not uniformly scaled-down desktop patterns.
5. Keep key actions reachable and targets comfortably operable.
6. Test tables, navigation, dialogs, sticky headers, cards, media, and long content.
7. Check zoom/reflow and keyboard order.
8. Re-test all changed breakpoints.

## Output

Viewport matrix, overflow/root causes, fixes, and actual test environment.

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
