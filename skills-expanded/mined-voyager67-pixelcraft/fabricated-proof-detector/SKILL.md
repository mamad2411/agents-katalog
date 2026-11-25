---
name: fabricated-proof-detector
description: "Finds unsupported testimonials, logos, customer counts, ratings, benchmark claims, trust badges, and fictional metrics in AI-built UI and marketing pages."
license: CC-BY-NC-4.0
---

# Fabricated Proof Detector

## Workflow

1. Inventory all claims that imply adoption, customer satisfaction, performance, security, compliance, integrations, awards, or business outcomes.
2. Identify displayed counts, charts, logos, quotes, ratings, and badges that act as proof.
3. Trace each item to an explicit source in supplied data or repository content.
4. Mark unsupported claims as unverified, not automatically false; request evidence or replace with neutral copy.
5. Remove fabricated placeholders from production-facing UI; use clearly labeled sample data in demos.
6. Ensure comparison claims have a defined baseline, date range, unit, and methodology.
7. Check footnotes, disclaimers, and consent for testimonials/logos where supplied.

## Safety rule

Never make fake proof more convincing. If a secret or private customer record appears in evidence, do not reproduce it in the report.

## Output

Claim inventory, evidence status, risk, and recommended removal or substantiation.

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
