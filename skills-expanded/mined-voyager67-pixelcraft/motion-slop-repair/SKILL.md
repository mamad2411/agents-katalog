---
name: motion-slop-repair
description: "Removes gratuitous animation, pulsing, parallax, hover theatrics, and scroll effects while preserving motion that explains state or spatial relationships."
license: CC-BY-NC-4.0
---

# Motion Slop Repair

## Workflow

1. Inventory transitions, auto-playing motion, loops, scroll effects, parallax, hover animation, and entrance choreography.
2. Ask what information each motion conveys: state change, cause/effect, orientation, progress, or feedback.
3. Remove decorative loops and delayed motion that competes with reading or task completion.
4. Standardize duration, easing, and distance for related interactions.
5. Respect `prefers-reduced-motion` and provide non-animated equivalents.
6. Check animation performance and avoid layout-shifting transitions.
7. Verify that state changes remain understandable without motion.

## Output

Motion inventory, keep/remove/reduce decisions, reduced-motion implementation, and checks.

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
