# Skill: RawVault theme system (instructions)

## When to use this skill

- Adding or renaming a **theme preset** (vivid / monochrome / bauhaus / linear).
- Wiring **ThemeButton / ThemeCard / ThemeInput** via `useThemeComponents()`.
- Editing **`app/globals.css`** blocks `:root[data-theme="…"]`.
- Debugging **wrong colors or fonts after theme switch** (next-themes vs legacy classes).
- User asks **how themes work** in this repo or **which file to touch** for a theme change.

**Handoff:**  
*Act as frontend-developer. Use `.cursor/agents/skills/theme-instructions.md` for theme architecture. For Minimalist Monochrome visuals only, also attach `minimalist-monochrome.md`.*

---

## Architecture (mental model)

1. **next-themes** sets **`data-theme`** on `<html>` to **`{themeName}-{mode}`** (e.g. `monochrome-light`, `bauhaus-dark`). See `NextThemesProvider` (`attribute="data-theme"`).
2. **`ThemeProvider`** parses that string → **`themeName`** (`vivid` | `monochrome` | `bauhaus` | `linear`) + **`mode`** (`light` | `dark`). It also applies **per-preset knobs**: `primaryColor`, `borderRadius`, `animation`, and compatibility classes `theme-{name}` on `document.documentElement`.
3. **CSS tokens** for each visual live in **`app/globals.css`** under `:root[data-theme="vivid-light"]`, `monochrome-dark`, etc. Tailwind maps semantic names (`background`, `foreground`, `primary`, …) and project **`--rv-*`** vars where used.
4. **Per-theme React shells** live in **`components/themes/<preset>/`**. **`useThemeComponents()`** in **`components/themes/index.tsx`** switches `ThemeButton` / `ThemeCard` / `ThemeInput` by `themeName`. **Default** branch = **Vivid** (shadcn-forward).

**Flow:** User picks preset → `data-theme` updates → CSS variables swap → optional `useThemeComponents()` picks the right shell component.

---

## Preset matrix (quick reference)

| `themeName` | `data-theme` examples | Fonts (headline / body) | Radius (preset) | Personality |
|-------------|------------------------|-------------------------|-----------------|-------------|
| **vivid** | `vivid-light`, `vivid-dark` | Outfit / Inter | shadcn default | Modern SaaS, blue sidebar accent, soft UI |
| **monochrome** | `monochrome-light`, `monochrome-dark` | Playfair / Source Serif | **0** | Editorial B&W, inversion, lines — see **`minimalist-monochrome.md`** |
| **bauhaus** | `bauhaus-light`, `bauhaus-dark` | Space Grotesk | **0** | R/Y/B primaries, **hard shadow** buttons (4px offset), mechanical hover/active |
| **linear** | `linear-light`, `linear-dark`* | Inter | **8–16px** | Cinematic dark glass, purple primary, ambient blobs in CSS |

\*Linear light/dark share one token block in CSS; both keys exist for next-themes.

---

## Token layers (what to use in code)

| Layer | Where | Use when |
|-------|--------|----------|
| **shadcn semantic** | `bg-background`, `text-foreground`, `border-border`, `bg-primary`, `text-primary-foreground`, `bg-card`, `text-muted-foreground` | Default styling; works across presets if tokens are set in globals for that `data-theme`. |
| **`--rv-*` (Tailwind `rv-*`)** | `bg-rv-bg`, `text-rv-text`, `border-rv-border`, `bg-rv-primary`, `bg-rv-surface` | Bauhaus/Monochrome/Linear shells often use these for **preset-specific** layout (file grid, cards). |
| **ThemeProvider state** | `useTheme().primaryColor`, `borderRadius` | User overrides from **ThemePanel**; may differ from pure CSS preset — respect when building custom controls. |

**Rule:** Prefer semantic tokens for portable UI; use `--rv-*` when matching an existing theme shell (e.g. Bauhaus buttons already use `rv-border` for shadow).

---

## Checklist: add a new named preset

1. **Type + presets** — Extend `ThemeName` / `THEME_PRESETS` in `ThemeProvider.tsx` (and any theme picker UI).
2. **next-themes** — Ensure new value `"{name}-light"` / `"{name}-dark"` is a valid `data-theme` string.
3. **globals.css** — Duplicate a full `:root[data-theme="…"]` block for light and dark; set `--font-*`, `--background`, `--primary`, `--rv-*` as needed.
4. **Shell components** — Add `components/themes/<name>/{Button,Card,Input}.tsx` (or reuse Vivid with token-only theme if shells are identical).
5. **index.tsx** — New `case "<name>": return { ThemeButton, ThemeCard, ThemeInput }`.
6. **Docs** — Add one row to the preset matrix in **this file**; if the preset has a long design spec, add a dedicated skill (like `minimalist-monochrome.md`).

---

## Checklist: fix “theme looks wrong”

1. Inspect **`<html data-theme="…">`** — typo = wrong block in globals.
2. Check **light vs dark** — each preset has two `:root[data-theme=…]` blocks; dark must redefine surfaces/text/border.
3. **Hardcoded colors** in JSX — replace with tokens or `rv-*` so they track the active preset.
4. **Shadcn primitive** — If only default theme looks right, the active `data-theme` block may be missing `--card`, `--popover`, `--sidebar-*`, etc. (compare **vivid-light** completeness).
5. **Monochrome-only hacks** — Workspace/file UI may branch on `themeName === "monochrome"`; changing preset name requires updating those branches.

---

## Per-preset implementation notes

### Vivid (default)

- Reference implementation for **complete** shadcn token set.
- Gradients / blue accents acceptable here — **not** in Monochrome.

### Monochrome

- **Authoritative visual spec:** `.cursor/agents/skills/minimalist-monochrome.md`.
- Zero radius at preset level; inversion patterns on cards/lists.

### Bauhaus

- **Full design spec + checklist:** `.cursor/agents/skills/bauhaus-theme.md` (constructivist palette, motion, layout, accordion pattern).
- **Primary red** `#D02020`, **secondary blue** `#1040C0`, **accent yellow** `#F0C020`; black borders; **no radius** on preset (or `rounded-full` for circles).
- Buttons/cards: **offset box-shadow** + press simulation (see `bauhaus/Button.tsx`, `bauhaus/Card.tsx`).
- Global texture: `.texture-bauhaus-dots` in globals — optional for sections.

### Linear / modern dark

- **Full spec:** `.cursor/agents/skills/linear-modern-dark.md` (blobs, spotlight, shadows, motion, bento).
- Glassy **rgba** surfaces; **indigo** `#5E6AD2`; radius **8px / 16px**.
- **globals.css:** grid + radial depth + noise + animated blobs; DOM needs **`.bg-blob-2`** for secondary blob.

---

## Key file paths

| Concern | Path |
|---------|------|
| Theme resolution + knobs | `components/theme-provider/ThemeProvider.tsx` |
| next-themes wiring | `components/theme-provider/NextThemesProvider.tsx` |
| Component switch | `components/themes/index.tsx` |
| Token definitions | `app/globals.css` (search `THEME:` section comments) |
| Theme picker / preset list | `components/theme-editor/` or panel using `setThemeName` |

---

## Boundaries

- **Backend / API** — Theme is client + CSS only unless persisting user preference (already via existing flows).
- **Do not** copy Monochrome rules (no color, no radius) onto Vivid/Linear without explicit user request.

---

## Success criteria

- Switching preset + mode updates **all** major surfaces consistently.
- New shells register in **one place** (`index.tsx`) and tokens in **globals** for both modes.
- Agents know **which skill** to open: **this file** for wiring/tokens; **minimalist-monochrome.md** for editorial B&W only.
