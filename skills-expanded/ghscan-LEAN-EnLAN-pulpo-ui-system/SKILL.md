# pulpo-ui-system — Frontend Skill for OpenCode / Gentle AI

## Trigger

Load this skill when ANY of these conditions are detected:
- User asks to build, modify, or review UI components, pages, or layouts
- User mentions: frontend, UI, component, page, design, CSS, layout, responsive, animation, visual, style, theme
- File context includes: `.css`, `.scss`, `.tsx`, `.jsx`, `.vue`, `.svelte`, `.html`, `.astro`
- User sends screenshots or design assets for review
- User asks to verify design quality, check accessibility, or review UI

## Behavior

When triggered, load and enforce:

1. **`rules/design-rules.md`** — Hard constraints. Every banned item is a FAIL.
2. **`taste/taste-system.md`** — Emotional modes. Pick one before designing.
3. **`agents/opencode-system-prompt.md`** — Full agent training prompt.
4. **`layouts/layout-primitives.md`** — Layout building blocks.
5. **`textures/texture-system.md`** — Texture layers.
6. **`fonts/font-policy.md`** — Font choices.

## Process Enforcement

The agent MUST follow this sequence:
1. Analyze references → 2. Structure → 3. Typography → 4. Texture → 5. Effects → 6. Refinement

Skipping any step is a violation. Jumping straight to code is a violation.

## Anti-Slop Check

Before delivering any visual work, verify:
- No banned aesthetics (glassmorphism, bento, gradients, giant rounded corners)
- No generic patterns (hero sections, feature grids, testimonial carousels)
- No debug artifacts (console.log, TODO, commented code)
- No placeholder content (lorem ipsum, fake data)
- Every element is justified

## Location

This skill lives at: `~/.config/opencode/skills/pulpo-ui-system/SKILL.md`
The repo lives at: `~/pulpo-ui-system/`
The skill references are relative to the repo root.
