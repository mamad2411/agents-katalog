---
name: form-ui-slop-repair
description: "Repairs generic and incomplete AI-built forms, including placeholder-only labels, excessive fields, unclear validation, weak errors, and ambiguous submit actions."
license: CC-BY-NC-4.0
---

# Form Ui Slop Repair

## Workflow

1. Identify the form's objective and the minimum information needed.
2. Flag placeholder text used instead of persistent labels, unnecessary fields, ambiguous required markers, and unexplained input formats.
3. Group related fields and provide concise instructions only where needed.
4. Use appropriate input types, autocomplete, input modes, and native semantics.
5. Associate validation errors with fields; explain how to correct them.
6. Preserve entered values after recoverable errors and provide clear submission feedback.
7. Prevent accidental duplicate submission and clarify irreversible outcomes.
8. Test keyboard, screen reader names, mobile layout, and long validation messages.

## Output

Field audit, simplified form structure, validation/state changes, and accessibility test notes.

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
