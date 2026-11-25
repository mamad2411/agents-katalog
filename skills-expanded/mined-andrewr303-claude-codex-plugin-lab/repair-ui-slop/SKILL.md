---
name: repair-ui-slop
description: >-
  Use when the user asks to fix, redesign, polish, improve, or remove AI-slop,
  generic, or template-like patterns from existing UI, including mixed requests
  that also add new UI. May edit only the authorized scope; applies the Prevent
  workflow to genuinely new portions.
---

# Repair UI Slop

Repair the originating defect in existing UI while preserving everything outside the authorized seam.

## Mutation boundary

Before editing, write an **explicit allowlist** of paths and operations. Record **Protected invariants** for routes, copy, data, forms, analytics, SEO, accessibility behavior, auth, integrations, dependencies, package state, and unaffected surfaces. Read broadly enough to understand the seam, but mutate only the allowlist. Treat an attempted out-of-scope mutation as failure even when denied, reverted, or absent from the final diff.

Do not install dependencies, change frameworks, replace a design system, or alter auth without explicit authority. Do not deploy. Do not use the network. Do not write externally or take outward action. Do not fabricate copy, claims, metrics, users, data, or assets. Stop and request authority when the causal correction cannot fit inside the allowlist.

Repair is primary for any request that changes existing UI. Route a read-only request to Audit and a wholly new surface to Prevent. For mixed work, **Repair remains primary** and uses the **Prevent procedure** only for **genuinely new portions**.

## Load the contracts

Apply [source priority and design contracts](../../references/source-priority.md) before deciding what is wrong. Use [anti-slop rules](../../references/anti-slop-rules.md) to distinguish hard failures from contextual signals. Use [craft and state gates](../../references/craft-and-state-gates.md) for structure, interaction, responsiveness, accessibility, motion, and render coverage. Follow the [evidence contract](../../references/evidence-contract.md) for every completion claim and receipt.

## Diagnose before changing

1. **Capture the current failure** with the literal expected and actual behavior, affected viewport or state, and available source or render evidence.
2. Inspect nearest instructions, maintained project knowledge, entrypoints, global styles, tokens, primitives, typography, motion, and the real execution path.
3. Restate the explicit allowlist and Protected invariants. Snapshot relevant files or manifests before mutation.
4. Identify the **originating layer**: **content**, **structure**, **token**, **primitive**, **component**, **state**, **responsive**, **accessibility**, or **integration**. A visible symptom may have more than one candidate cause; falsify the plausible alternatives with source or runtime evidence.
5. For a repeated card, pill, gradient, glow, display scale, rounded surface, motion treatment, or other contextual signal, require:

```text
signal -> evidence -> product conflict -> exceptions considered -> smallest coherent correction
```

A signal alone is never a defect. Preserve an intentional pattern supported by content, interaction, hierarchy, brand, or the local system.

## Patch the cause

Apply the **smallest coherent patch** at the originating layer. Reuse project-native tokens, primitives, helpers, naming, and motion. Preserve semantic HTML, keyboard behavior, visible focus, contrast, touch targets, reflow, reduced motion, and every relevant loading, empty, error, success, stale, disabled, hover, and pressed state.

Do not decorate around a structural or state defect. Do not broaden a component repair into a page redesign. Do not perform speculative cleanup.

### Multi-surface approval gate

A shared cause does not itself authorize a shared rewrite. Make a **project-native system change** across multiple surfaces only when that exact scope is **separately approved**, every surface is allowlisted, and protected invariants are explicit. Otherwise repair the authorized surface and report the adjacent evidence without mutating it.

### Mixed existing and new work

Diagnose and repair the existing portion first. For genuinely new portions, apply the Prevent procedure: infer the proportional design contract, reuse the existing system, define real content and state bounds, implement only the new portion, and render-check it in context. Do not let the new portion trigger an unapproved redesign of its parent.

## Search and verify the seam

After the patch, perform a bounded **nearby same-defect search** through the affected primitive, component family, state handler, responsive rule, accessibility behavior, or integration edge. Fix another occurrence only when it is in the allowlist; otherwise report it as unverified adjacent scope.

Re-run the **original case**, focused checks, primary interaction, keyboard path, and all **affected states and breakpoints**. Compare post-change manifests to the explicit allowlist and prove every protected canary remains byte-identical. Render or screenshot-inspect each affected viewport and state; source inspection cannot establish visual completion. If rendering is blocked, name the blocker and leave render verification unverified.

## Handoff

Return this **Before/after receipt**:

```text
Delivered behavior:
Mutation boundary:
Before evidence:
Originating layer and falsified alternatives:
Smallest causal patch:
Changed paths and operations:
Protected-invariant evidence:
Nearby same-defect search:
Checks performed and exact results:
Rendered viewports, states, and interactions:
Unverified items:
Remaining risk:
```

Use exact evidence language. Never upgrade static checks to `render verified` or `verified end-to-end`.
