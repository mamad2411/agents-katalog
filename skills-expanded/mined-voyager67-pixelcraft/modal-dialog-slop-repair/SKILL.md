---
name: modal-dialog-slop-repair
description: "Finds overused or poorly structured AI-built modals, oversized dialog shells, unclear actions, missing focus management, and destructive confirmation noise."
license: CC-BY-NC-4.0
---

# Modal Dialog Slop Repair

## Workflow

1. Decide whether the task truly needs a modal or should be inline/a separate page.
2. Audit dialog title, purpose, content length, action hierarchy, dismissal behavior, and destructive risk.
3. Remove nested panels, decorative headers, redundant close buttons, and unnecessary confirmation layers.
4. Keep primary and secondary actions explicit; label destructive actions plainly.
5. Implement focus entry, focus containment, escape handling where appropriate, and focus return.
6. Check scroll behavior, small screens, and screen reader announcement.
7. Preserve user input when a recoverable validation error occurs.

## Output

Modal necessity decision, content/action repair, keyboard behavior, and viewport checks.

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
