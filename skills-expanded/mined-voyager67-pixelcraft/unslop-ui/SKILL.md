---
name: unslop-ui
description: "Turns generic, AI-looking interfaces into coherent, product-specific UI through an evidence-based audit and ordered redesign passes. Use when asked to unslop, polish, or redesign an existing screen while preserving product behavior."
license: CC-BY-4.0
metadata:
  attribution: "Adapted from Unslop by Damir Sokolovsky"
  source: "https://github.com/heydamir/unslop"
---

# Unslop UI

This skill adapts the core approach of **Unslop by Damir Sokolovsky** for cross-agent use. The original work is licensed CC BY 4.0; attribution and the original license are preserved in `THIRD_PARTY_NOTICES.md`. This adaptation has been rewritten and extended for product-agnostic ChatGPT/Codex workflows. It is not an official Unslop release and does not imply endorsement.

## Purpose

Turn generic, inconsistent, or visually noisy interfaces into deliberate product experiences. Diagnose first, derive a direction from the product, make high-impact corrections in ordered passes, and verify the result.

## Use when

- A screen feels interchangeable, template-driven, or visually noisy.
- The user asks to polish, redesign, clean up, or “unslop” UI.
- There are generic gradients/glows, excessive cards, emoji icons, arbitrary spacing, weak hierarchy, empty marketing copy, meaningless charts, or incomplete states.

## Core rules

- Inspect the rendered interface and source implementation when possible.
- Evaluate observable design quality, not whether a human or AI authored it.
- Preserve existing product behavior, content, information architecture, and authentic brand assets unless a finding justifies change.
- Do not fabricate data, proof, testimonials, metrics, capabilities, customers, or visual evidence.
- If the user says “just do it”, proceed. Otherwise present audit and direction before substantial redesign.
- If browser/image tools are unavailable, state the review is code-based or screenshot-based.

## Workflow

### 1. Understand the product

Identify the product, audience, primary screen task, current brand signals, stack, and constraints. Find the source components, routes, styles, tokens, and assets that produce the screen.

### 2. Inspect and audit

Inspect rendered output at the relevant viewport. Audit spacing/alignment, color/surfaces, icons, copy, typography, layout, component details, imagery, motion, interactions, accessibility, and responsive behavior. For every issue, record its location, observed evidence, user impact, confidence, and specific correction.

### 3. Select intervention size

- **No meaningful slop:** say so and offer at most three refinements; do not redesign for novelty.
- **Light polish:** keep the current direction and fix observed inconsistencies.
- **Heavy slop:** derive and apply a new coherent direction, preserving real product and brand constraints.

### 4. Establish a product-specific direction

Write five decisions:

- **Product:** what it does and for whom.
- **Character:** two or three specific words; avoid generic words like modern, clean, sleek, or premium.
- **World:** the product's real-world context, materials, or environment.
- **Moments:** one or two places where rich visual detail belongs because the content deserves it.
- **Signature:** one repeatable detail that plausibly belongs to this product.

Keep existing brand elements when they are genuine and effective. Avoid inventing a style based on trends.

### 5. Fix in ordered passes

1. **Spacing:** make groups, alignments, repeated row sizes, and section rhythm coherent.
2. **Color:** use semantic roles, protect readability, keep chrome quiet, and use accents intentionally.
3. **Icons:** use one coherent icon system; remove emoji used as generic interface symbols.
4. **Copy:** replace filler, unsupported hype, vague labels, and fake claims with factual task language.
5. **Typography:** define a small readable scale, weights, line heights, and numeric formats.
6. **Layout:** restore a clear scan path and correct proportions without destroying information architecture.
7. **Details:** refine borders, radii, shadows, charts, tables, buttons, and component states.
8. **Visuals:** prefer real product content or relevant imagery; do not add decorative blobs as a substitute for meaning.
9. **Motion:** keep only motion that explains state, feedback, or spatial relationships; respect reduced motion.

Complete each pass consistently across the screen before moving on. Adapt values to the existing system rather than blindly applying fixed numbers.

### 6. Verify

Re-render where possible. Check desktop/tablet/mobile, overflow, visible focus, keyboard use, text contrast, loading/empty/error/success states, and preserved interactions. Run relevant build/tests if available. Do not claim checks that were not performed.

### 7. Report

Describe the direction, issues fixed by pass, files changed, verification performed, and remaining risks. Distinguish screenshot review, source review, and runtime testing.

## Output

Provide a concise before/after summary, files changed, checks actually performed, and unresolved issues.

## Completion bar

The screen should feel like it belongs to this product. It should be more legible, coherent, specific, trustworthy, and usable—not merely more decorated.
