---
name: interaction-state-repair
description: "Finds polished-looking but fake or incomplete interactions in AI-built UI and adds coherent behavior for focus, loading, disabled, success, empty, and error states."
license: CC-BY-NC-4.0
---

# Interaction State Repair

## Workflow

1. Inventory every control, link, menu, tab, dropdown, switch, dialog, and form action.
2. Confirm each control has a real, coherent action; remove dead buttons and placeholder links.
3. Define trigger, expected response, state transition, feedback, and recovery for each interaction.
4. Implement disabled/loading/success/error states and prevent duplicate submissions.
5. Ensure destructive actions have proportionate confirmation or undo.
6. Make keyboard, pointer, and touch behavior consistent.
7. Test failures and empty results, not just the happy path.

## Output

Interaction inventory, state matrix, broken controls, behavior fixes, and test scenarios.

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
