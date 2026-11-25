---
name: onboarding-ui-slop-repair
description: "Repairs generic onboarding flows with excessive steps, vague progress, forced personalization, fake welcome screens, and unclear setup completion."
license: CC-BY-NC-4.0
---

# Onboarding Ui Slop Repair

## Workflow

1. Identify the user's first meaningful success and the minimum steps needed to reach it.
2. Audit each screen for redundant questions, premature permission prompts, forced profile completion, and generic welcome copy.
3. Remove steps that don't change the product experience or fulfill a required obligation.
4. Explain why sensitive or optional information is requested; provide skip paths where appropriate.
5. Show honest progress and define what completion means.
6. Save progress safely and provide recovery if a step fails.
7. Check keyboard, screen reader, mobile, and returning-user paths.

## Output

Onboarding journey, unnecessary steps, revised sequence, trust/consent risks, and state coverage.

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
