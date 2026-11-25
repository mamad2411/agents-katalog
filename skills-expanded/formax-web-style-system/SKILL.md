---
name: formax-web-style-system
description: Use for all frontend and web UI tasks by default to apply a business-agnostic desktop web visual style system with medium-strength guardrails; if an existing design system is present, follow it first and use this skill only as a style harmonizer.
---

# Formax Web Style System

## Goal

Apply a business-agnostic visual style system for web interfaces.

Enforce a calm, desktop-grade aesthetic with strong readability, token-first styling, and clear interaction hierarchy.

Do not introduce product workflow assumptions, domain copy assumptions, or business IA decisions.

## Trigger Contract

Use this skill by default for all frontend and web UI tasks.

If the task is not frontend/UI work, do not apply this skill.

If the repository or task provides an existing design system, brand guide, or component library:
- Follow the existing system first.
- Use this skill only to harmonize tone, spacing rhythm, and state clarity.
- Never override explicit local design constraints.

## Workflow

1. Read `references/style-doctrine.md` first to lock the visual direction.
2. Read `references/token-blueprint.md` to define CSS variable layers before proposing UI details.
3. Read `references/layout-patterns.md` when composing desktop layout, density, and responsive fallback.
4. Read `references/component-tone.md` when styling components, states, and interaction emphasis.
5. Read `references/anti-patterns.md` as a final rejection checklist before returning output.
6. Apply all `CRITICAL STYLE OVERRIDES` from the references as mandatory constraints.

For small styling requests, keep output concise but still include token strategy and state clarity.

## Formax Overrides (Mandatory for CSS Rework)

When the task touches CSS in `packages/web-reference-react/**`, do this before editing:
1. Read `.codex/skills/formax-web-css-convergence-workflow/SKILL.md`.
2. Lock a pre-edit intake contract (target model, non-goals, ownership boundary, acceptance checks).
3. Use single-axis passes (geometry -> color -> interaction), avoid mixed multi-axis edits.
4. Validate with:
   - `bun run test -- src/App.test.tsx` (in `packages/web-reference-react`)
5. If and only if the task includes transparency/window layering:
   - Read `docs/contracts/web/window-transparency-construct.md`
   - Run `bun run test:e2e -- e2e/window-transparency.evidence.spec.js --project=chromium` (in `packages/web-reference-react`)

## Output Contract

For each frontend/web UI response, always include these sections (explicit headings):
1. `visual_direction`
2. `tokens`
3. `layout`
4. `component_tone`
5. `responsive_notes`

Inside `tokens`, provide CSS variable categories at minimum for:
- color
- typography
- spacing
- radius
- shadow
- motion

Prefer style system guidance and representative snippets over large hard-coded CSS dumps.

## Guardrails

Never do the following:
- Assume product business flows, user journeys, or domain-specific copy.
- Default to purple-first palettes when not requested.
- Default to dark-mode-first styling when not requested.
- Produce generic template-like SaaS visuals without distinct visual intent.
- Hard-code ad-hoc colors and spacing without a token layer.
- Copy screenshot pixels exactly; preserve mood, not exact geometry.
- Replace required glass-material sidebars with opaque flat fills.
- Use bordered inputs in default state when soft-filled inputs are specified.

Always keep medium constraint strength:
- Strong enough to maintain consistent visual quality.
- Flexible enough to adapt to different frontend tasks and local systems.
