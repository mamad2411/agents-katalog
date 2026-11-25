---
name: visual-asset-slop-audit
description: "Audits images, stock art, illustrations, textures, and product screenshots for generic, irrelevant, inconsistent, or misleading visual assets."
license: CC-BY-NC-4.0
---

# Visual Asset Slop Audit

## Workflow

1. Inventory visual assets and where/how they appear.
2. Judge relevance to the product's real subject, material, audience, and task.
3. Flag generic stock imagery, unrelated abstract objects, inconsistent illustration styles, low-resolution assets, and screenshots that do not match the current product.
4. Verify that product screenshots show real or clearly labeled sample UI and do not expose private customer information.
5. Check crop, focal point, contrast, loading, alt text, and licensing/attribution provenance where known.
6. Recommend the smallest replacement set; do not swap assets merely for novelty.

## Output

Asset inventory, issue, evidence, provenance status, recommendation, and privacy/licensing risks.

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
