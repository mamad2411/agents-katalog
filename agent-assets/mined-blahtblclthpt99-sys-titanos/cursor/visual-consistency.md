---
description: TitanOS visual consistency — one design language everywhere
alwaysApply: true
---

# Visual Consistency

Everything should use the same design language.

## Standardize

Typography · Spacing · Margins · Padding · Border radius · Card sizes · Button sizes · Icons · Colors · Elevation · Animations · Transitions · Modals · Dialogs · Tooltips · Menus

## Source of truth

- Tokens: `src/index.css` (`--space-*`, `--radius-*`, `--duration-*`, `--shadow-*`)
- Recipes: `src/lib/design-system.js` (`TYPE`, `ICON_SIZE`, `CONTROL`, `SURFACE`, `RADIUS`, `ELEVATION`)
- Primitives: `components/ui/*` + `PageShell` / `PageHeader` / `Card` / `Button`

## Rules

| Concern | Use |
|---|---|
| Page chrome | `PageShell` + `PageHeader` — not ad-hoc `px-4 py-6 max-w-*` |
| Surfaces | `titan-surface` / `<Card>` — **not** `glass` / stacked `bg-card+border+shadow` |
| Radius | controls `rounded-md`; cards/overlays `rounded-lg` (token); pills `rounded-full`. No `rounded-3xl` in app UI |
| Type | `text-title` / `text-heading` / `text-body` / `text-caption` — avoid `text-[10px]` for primary UI |
| Spacing | `page-pad`, card `p-4 md:p-5`, `gap-3`/`gap-4` or `stack-*` |
| Buttons | `<Button>` / `buttonVariants` — 44px default tap target |
| Icons | `ICON_SIZE` sm\|md\|lg (16/20/24) |
| Color | semantic tokens (`primary`, `muted`, `destructive`, `success`). Brand `titan-*` for logos/marketing only |
| Elevation | `shadow-soft` default · `shadow-lift` hover/overlay — never `shadow-md`/`lg`/`xl` in new code |
| Motion | `duration-fast` \| `base` \| `slow` only (≤250ms); honor reduce-motion |
| Overlays | Dialog / Sheet / Dropdown / Tooltip / Popover from `components/ui` — don’t restyle radius/shadow per page |

## Definition of done

Incomplete if a screen invents its own type scale, surface recipe, overlay chrome, or motion durations outside the tokens above.
