---
name: ai-copy-tell-review
description: "Reviews UI and marketing copy for common synthetic-writing tells such as vague superlatives, formulaic parallelism, empty benefits, and repetitive cadence."
license: CC-BY-NC-4.0
---

# Ai Copy Tell Review

## Workflow

1. Read copy in context and identify the audience, intended action, and real product capability.
2. Detect vague intensifiers, generic benefit claims, repetitive sentence templates, excessive three-part lists, inflated adjectives, and unsupported performance claims.
3. Treat these as writing-quality signals only; never infer authorship.
4. Replace abstract language with evidence-backed specifics, concrete examples, user outcomes, or direct instructions.
5. Vary cadence naturally without forcing quirky personality.
6. Retain necessary technical/legal wording and avoid creating unsupported claims.
7. Check that every revised statement is supported by product evidence.

## Output

Flagged phrase, reason, revised version, evidence required, and confidence.

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
