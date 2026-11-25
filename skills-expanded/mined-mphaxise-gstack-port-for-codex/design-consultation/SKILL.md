---
name: design-consultation
description: Design-system creation and direction-setting for Codex. Use when a project needs a stronger visual point of view, design principles, or a reusable design language.
---

# Design Consultation

Use this skill when the user wants a design direction, design system, or a stronger visual language before polishing or implementation.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Load `PRODUCT.md`, `DESIGN.md`, or equivalent project context when present. Read the actual tokens, theme, and one representative component.
2. Identify the product, audience, platform, register, constraints, existing brand cues, and anti-references.
3. Propose a cohesive design direction across:
   - aesthetic
   - typography
   - color
   - spacing
   - layout
   - motion
4. Identify deliberate risks worth taking so the product does not collapse into generic AI output.
5. If the user wants a saved source of truth, create or update root `PRODUCT.md` and `DESIGN.md`, or preserve the repository's established equivalent location.
6. Use `design-quality` for the shared context schema and final quality gates.

## Guardrails

- Do not generate a design system that ignores the actual product or audience.
- Avoid default-safe palettes and generic component language when the project needs a stronger identity.
- Preserve established systems when the repo already has one.
- Treat Impeccable-inspired anti-patterns as context-aware defaults, with documented exceptions for legitimate product or brand needs.

## Outputs

Always include:

- design thesis
- visual direction
- design principles
- constraints or anti-goals
- recommended next artifacts to create
- source files and rendered evidence used
