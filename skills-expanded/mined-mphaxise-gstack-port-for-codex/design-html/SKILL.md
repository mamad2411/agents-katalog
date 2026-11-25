---
name: design-html
description: Design-to-implementation workflow for Codex. Use when an approved design should become real HTML, CSS, or framework-native UI code.
---

# Design HTML

Use this skill when the user has an approved design direction and wants it translated into implementation code.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Confirm the design source:
   - approved mockup
   - design doc
   - existing UI direction
   - written description
2. Load `PRODUCT.md`, `DESIGN.md`, or the established equivalent plus the real tokens and representative components.
3. Translate the design into the repo's actual UI stack.
4. Cover responsive behavior, interaction states, loading, empty, error, overflow, reduced motion, and accessibility paths that apply.
5. Inspect the rendered result at narrow, medium, and wide sizes when browser evidence is available.
6. Run the optional Impeccable detector through `design-quality` when it is already installed. Use the manual quality gates when it is unavailable.
7. Re-check the changed surface and report remaining visual or runtime risk.

## Guardrails

- Do not ship a one-viewport mockup disguised as finished UI.
- Preserve the repo's existing framework and design conventions.
- Avoid generic boilerplate layouts when the design calls for a stronger point of view.
- Never install Impeccable implicitly or claim detector coverage from source review alone.

## Outputs

Always include:

- source design used
- implementation approach
- responsive considerations
- what was verified
- detector or manual-gate status
- remaining visual risks
