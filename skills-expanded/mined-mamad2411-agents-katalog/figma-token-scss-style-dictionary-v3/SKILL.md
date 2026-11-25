---
tags: [frontend, figma, token, scss, style, dictionary]
name: figma-token-scss-style-dictionary-v3
description: Figma Tokens Studio JSON → split files → Style Dictionary v3 → SCSS variables, typography classes, and composition classes
category: frontend
trigger: When setting up a Figma-to-SCSS token pipeline with Style Dictionary v3 and @tokens-studio/sd-transforms
version: 0.1.0-draft
source_project: lucida-ui
---

# Figma Token → SCSS (Style Dictionary v3)

Build pipeline that converts Figma Tokens Studio export into SCSS variables and utility classes.

## When to use

- Project uses SCSS-based design system (e.g. with Ant Design overrides)
- Tokens are managed in Figma Tokens Studio and exported as a single JSON
- Need base/theme/semantic/component token layers with `@import` auto-wiring

## Pipeline

1. **Split** — `split-files.js` reads monolithic `tokens.json` and fans out to `tokens/{group}/{name}.json`
2. **Build** — `build.js` runs Style Dictionary v3 with custom transforms and formats:
   - Glob source files by layer (base, theme, semantic, component)
   - Register transforms: `hslhsl`, `typography/shorthand`, `border/shorthand`, `shadow/shorthand`, `size/px`, `size/letterspacing`, `type/fontWeight`, `color/hexrgba`, `resolveMath`
   - Register formats: `css/variables` (SCSS vars), `css/typographyClasses` (`.st-*` classes), `css/compositionClasses` (composition → CSS properties)
   - Auto-append `@import` statements to layer index files (`_base.scss`, `_themes.scss`, `_extend.scss`, `_semantic.scss`)
3. **Output** — SCSS files at `packages/sirius/src/styles/tokens/`

## Key patterns

See `content.md` for full implementation reference.
