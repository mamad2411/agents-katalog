---
name: button-cta-slop-repair
description: "Fixes generic or misleading buttons and calls to action, including vague labels, duplicate primaries, decorative button variants, and weak action feedback."
license: CC-BY-NC-4.0
---

# Button Cta Slop Repair

## Workflow

1. Inventory action controls and the result each one produces.
2. Replace vague verbs (“Go”, “Submit”, “Continue”) with specific labels when context is not sufficient.
3. Reduce competing primary buttons; make hierarchy reflect the most important next step.
4. Distinguish navigation links from actions and destructive operations.
5. Normalize height, padding, icon use, radius, and states within the component system.
6. Ensure disabled/loading states are understandable and success/failure feedback is real.
7. Check keyboard focus and touch targets.

## Output

CTA inventory, label revisions, primary/secondary hierarchy, state corrections, and checks.

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
