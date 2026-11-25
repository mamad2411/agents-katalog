---
name: visual-cliche-detection
description: "Finds generic visual clichés that make an interface feel interchangeable, including overused gradients, floating panels, glass cards, stock hero compositions, and ornamental badges."
license: CC-BY-NC-4.0
---

# Visual Cliche Detection

## Workflow

1. Describe the overall visual concept in one sentence without naming trends.
2. Identify repeated motifs: gradient wash backgrounds, glows, blur glass, excessive pill badges, floating card stacks, generic abstract blobs, ornamental grids, and identical three-card feature sections.
3. Check whether each motif communicates product meaning or merely fills space.
4. Compare repeated patterns against the product's real domain, audience, data, and brand assets.
5. Keep motifs that are purposeful and coherent; remove or simplify only those with no functional or identity role.
6. Propose product-specific alternatives using real content, an actual workflow, meaningful diagrams, or a relevant material/visual cue.

## False positives

A gradient or glass material can be legitimate brand language. Judge its use, not its mere presence.

## Output

Cliché, evidence, why it feels generic, confidence, keep/change decision, and a product-relevant alternative.

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
