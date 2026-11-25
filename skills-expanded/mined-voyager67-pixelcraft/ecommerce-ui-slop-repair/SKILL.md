---
name: ecommerce-ui-slop-repair
description: "Repairs generic e-commerce UI patterns such as fake urgency, redundant product cards, ambiguous pricing, noisy badges, weak filters, and low-trust checkout affordances."
license: CC-BY-NC-4.0
---

# Ecommerce Ui Slop Repair

## Workflow

1. Identify shopping task: browse, compare, evaluate, configure, or purchase.
2. Audit product title, images, price, availability, variants, shipping/returns, reviews, and seller details for clarity and source accuracy.
3. Remove fabricated scarcity, false countdowns, unsupported ratings, and decorative “bestseller” badges.
4. Improve filter/sort semantics and compare affordances; keep selected filters visible.
5. Make total cost, variants, and next action clear before checkout.
6. Check cart, stock error, promo, shipping, and payment states.
7. Preserve trust, keyboard support, and mobile purchase flow.

## Output

Trust-risk findings, browse/compare/purchase fixes, evidence needed, and state verification.

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
