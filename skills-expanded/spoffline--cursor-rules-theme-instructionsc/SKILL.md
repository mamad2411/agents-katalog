---
description: RawVault multi-theme system — data-theme, ThemeProvider, globals.css tokens, useThemeComponents. Use when wiring presets or editing theme provider / themes index.
globs: components/theme-provider/**/*.tsx,components/themes/index.tsx
alwaysApply: false
---

# Theme instructions

For **how presets map to CSS**, **how to add a theme**, and **token vs rv-* usage**, read:

**`.cursor/agents/skills/theme-instructions.md`**

- Editing **`components/themes/<preset>/`** shells: respect that preset’s row in the skill’s preset matrix (Vivid vs Monochrome vs Bauhaus vs Linear).
- **Editorial monochrome only:** `.cursor/agents/skills/minimalist-monochrome.md`.

Delegate **frontend-developer** with `theme-instructions.md` in the handoff when the task is theme-wide, not a single component bug.
