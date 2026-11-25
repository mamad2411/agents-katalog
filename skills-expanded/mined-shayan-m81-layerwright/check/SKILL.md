---
name: check
description: Check a design or its implementation - compare the code with the Figma frame, or audit the frame itself for Design System use, spacing, contrast and accessibility. Use for /layer:check.
argument-hint: "[frame, or a file/route to compare]"
disable-model-invocation: true
---

# Check

1. `figma_status` with a `title`. Pick the target: the selection, a frame they named, or a code file/route they gave.
2. Code given (or the frame is already implemented): compare them. `code_verify_usage({ file, planId })` for components and tokens, and compare the rendered page with `figma_export_image` of the frame. List differences by importance: layout, sizes and spacing, typography, colour, missing states.
3. Design only: `figma_analyze_design({ target, mode: "critique" })` and `mode: "a11y"`, plus `figma_export_image` to look at it. Report errors first (contrast, touch targets, tiny text), then spacing off the scale, raw colours, near-miss alignment, inconsistent components.
4. Offer to fix: in Figma (`/layer:edit`) or in code. Change nothing without a yes.
