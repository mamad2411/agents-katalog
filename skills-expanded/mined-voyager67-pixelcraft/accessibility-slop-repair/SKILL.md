---
name: accessibility-slop-repair
description: "Finds accessibility failures frequently introduced by decorative AI UI: low-contrast text, icon-only buttons, missing labels, fake controls, focus traps, and color-only status."
license: CC-BY-NC-4.0
---

# Accessibility Slop Repair

## Workflow

1. Check semantic landmarks, heading order, labels, names, roles, and form associations.
2. Navigate with keyboard; verify focus visibility, logical sequence, and operable menus/dialogs.
3. Check color contrast and ensure status is not communicated by color alone.
4. Inspect icon-only controls, charts, motion, tooltips, tabs, tables, and dynamic status announcements.
5. Check form errors, disabled states, validation messages, and recovery guidance.
6. Respect reduced motion and prevent flashing or unnecessary animation.
7. Run automated scans where possible and manually verify high-risk paths.
8. Report the scope and criteria checked; never claim full WCAG conformance from a superficial scan.

## Output

Findings, fixes, exact manual/automated checks, and remaining unknowns.

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
