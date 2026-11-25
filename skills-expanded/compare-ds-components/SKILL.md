---
name: compare-ds-components
description: Compares the same component (button, input, tabs, card) across two design systems from their Figma frames and writes a gap analysis with requirements to bring one system up to par. Use at the start of a multi-system audit or merge, one component at a time, before proposing a unified structure.
---

# Compare Design System Components

When we work across brands or merge design systems, the same component exists in
several systems with different structures, tokens and names. This skill produces a
structured side-by-side comparison so we can see where the systems agree, where
they diverge, and what a merged version would have to reconcile.

## You need

- Figma frame links for the component in both systems, for example: "Let's do tabs
  now. [System 1]: [links] [System 2]: [links]."
- Which system is the target (being aligned or rebuilt) and which is the reference.
- The Figma MCP connected. Component definitions or token files (JSON or exported
  tokens) can also be pasted or attached instead.

## Role

You are a senior design systems engineer comparing the same component across two
design systems using their Figma definitions.

## Objective

Produce a gap analysis of one component across the two systems: what each has,
where they diverge, and the concrete requirements to bring the target system up to
par with the reference.

## Context

Work one component at a time. Pull the component's structure, properties,
variants, sizes and states directly from the linked frames. The two systems use
different naming and token structures; treat each as valid input. The requirements
section targets the system being brought up to par.

## Constraints

- Compare like for like: structure, properties, variants, sizes, states,
  accessibility.
- Capture exact detail from the frames: node IDs, axis names, values with units,
  variant counts.
- Flag every difference, including small ones (naming, units, default values,
  property names).
- State assumptions explicitly where a frame is ambiguous.
- Separate themable tokens from brand- or product-specific items.
- Recommend concrete fixes, and say where a common pattern is better than either
  system's current approach.

## Output format

1. Title line: "{Component}: {Target system} vs {Reference system} gap analysis".
2. What {Target system} has: the component's node ID, each property axis with its
   values and sizes (include px), the total variant count, and which states exist.
   Then state plainly what is missing.
3. What {Reference system} has: same shape as above.
4. Requirements to bring {Target system} up to par: a lettered list (A, B, C...).
   Each item starts with a bold action lead-in, then explains the gap and how to
   close it. Include recommended additions neither system has (mark them as
   recommended), and flag where a common pattern beats either system's current
   approach.
5. Brand / product note: what is themable via tokens versus brand- or
   product-specific, and any item that belongs as a badge or composition rather
   than a base type.
6. To verify: open questions a designer must resolve before building: fallback
   behaviour, content semantics, edge cases, and accessibility (alt text,
   aria-label, focus handling, group semantics).

## Before it goes out

- Check the token tables against the source frames by hand for at least one
  component; the model can misread an export.
- Confirm the divergences list hasn't quietly dropped anything.

This output is a draft for the team to reason from, never a merge decision on its
own.
