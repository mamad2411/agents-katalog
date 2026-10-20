---
description: Design system rules that prevent generic AI-looking interfaces
globs: "**/*.{tsx,jsx,vue,svelte,astro,html,css,scss,dart}"
alwaysApply: false
---

# Design System

Works with `10-design-rules.mdc` (hard bans) and `05-accessibility.mdc` (accessibility always wins a conflict).

## Existing system first
- Find the project's tokens before styling (CSS variables, Tailwind theme, MUI/Chakra theme, Flutter `ThemeData`). Extend them. Do not introduce a parallel palette.
- Map semantic roles onto existing tokens instead of renaming them. Add a missing role in every theme mode.
- If existing code breaks these rules, flag it. Do not rip it out unless the task covers it.

## Do not use by default
Excessive rounded cards, gradients, purple/blue "AI" gradients, gradient text, glassmorphism, oversized hero sections, floating cards, heavy shadows, constant animation, pills everywhere, generic SaaS dashboards, repetitive identical card grids, decorative elements with no meaning, padding used to fill space, generic marketing copy (see `20-copy-rules.mdc`), emoji as UI icons, Inter/Poppins/Roboto picked by default.

## Typography
- Choose fonts on purpose. Reuse the project's fonts if they are established.
- For new systems, pick from: Geist, Manrope, Plus Jakarta Sans, DM Sans, Instrument Sans, IBM Plex Sans, Sora, Space Grotesk, Source Sans 3. One display + one text face.
- Coherent scale (e.g. 12/14/16/18/24/32/48). Body 16px minimum, line-height 1.5 to 1.7, measure 60 to 75 characters.

## Color tokens
Every surface resolves to semantic tokens: background, surface, elevated surface, primary, secondary, accent, text, muted text, border, success, warning, error, info, focus.
- Restrained palette: neutrals plus one accent. Color carries meaning, not decoration.
- Check contrast for every text/background pair in every theme mode (see `05-accessibility.mdc`).

## Spacing and radius
- One spacing scale (4px or 8px base). No one-off values.
- Radius from a small scale (0, 4, 6, 8px) chosen per project. Never round everything.

## Elevation
- Prefer borders, dividers and background shifts over shadows. A shadow means the element floats (menus, dialogs). Max two elevation levels.

## Icons
- One coherent family (lucide, Heroicons, Phosphor, Material Symbols for Flutter/MUI). No emoji icons. No mixing families.

## Layout
- Choose layout from the user task: reading favors columns and measure, comparison favors tables, scanning favors lists, workflows favor clear step order.
- Use grid and flex with clear alignment, proximity, hierarchy and vertical rhythm. Responsive containers with a max width.
- Vary section composition. Three identical cards in a row is a smell, not a default.
