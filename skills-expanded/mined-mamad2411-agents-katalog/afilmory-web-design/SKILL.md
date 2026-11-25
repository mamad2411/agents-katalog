---
name: afilmory-web-design
description: >
  Use when writing, reviewing, or restyling any UI in apps/web or packages/ui —
  the Afilmory gallery SPA. Triggers on creating or editing a React component,
  panel, modal, drawer, button, badge, chip, overlay, tooltip, or viewer chrome;
  on choosing colors, backdrop blur, border radius, shadows, z-index, spacing,
  or transitions; on adding an icon; and on any request to "make it look right",
  match the glass aesthetic, or audit UI against the design system. Does NOT
  apply to be/apps/dashboard (separate admin system), apps/mobile (native
  Swift), or apps/site (Astro marketing).
---

# Afilmory Web Design System

**Full normative spec: `/DESIGN.md` at the repo root. Read it before non-trivial UI work.**
This file is the fast path: the recipe, the lookup tables, and the red lines.

## Core principle

> The photograph is the only light source. Everything else is glass in front of it.

Dark-only. Depth comes from stacked translucency, not drop shadows. Accent is derived from the
current photo, not from a brand. Controls that aren't needed right now sit at `opacity-0`.

## The surface recipe

Every floating surface is these four things together. Missing one is what makes a component look
foreign:

```tsx
<div className="bg-material-medium rounded-xl border border-accent/20 backdrop-blur-2xl">
```

1. a `bg-material-*` fill
2. a `backdrop-blur-*` matched to its role
3. a hairline border (`border-accent/20`, or `border-white/10` over a photo)
4. a radius matched to container size

Motion on top of that: `transition={Spring.presets.smooth}` from `@afilmory/utils`.

## Quick reference

**Color — semantic tokens only.** Hierarchy = walk down one family, never change hue.

| Need | Use |
| --- | --- |
| Text | `text-text` → `-secondary` → `-tertiary` → `-quaternary` |
| Control / hairline fill | `bg-fill` → `-secondary` → `-tertiary` → `-quaternary` |
| Translucent surface | `bg-material-ultra-thin` … `-medium` … `-ultra-thick`, `-opaque` |
| Accent tint | `border-accent/20`, `bg-accent/5`, `hover:bg-accent/10` |
| Accent solid | `bg-accent`, `hover:bg-accent/90` (primary button, active toggle only) |
| Over a photograph | `text-white`, `border-white/10`, `hover:bg-black/40` |

**Blur — by role, three steps only.**

| Role | Class |
| --- | --- |
| Floating panel, menu, popover, toast, viewer chrome | `backdrop-blur-2xl` |
| Secondary control sitting on a photo | `backdrop-blur-md` |
| Scrim behind a modal | `backdrop-blur-sm` |
| Fade band under fixed top/bottom chrome | `<LinearBlur side="top" tint="var(--color-background)" />` |

**Radius — by container size. Items are one step tighter than their container.**

| Radius | Use |
| --- | --- |
| `rounded-full` | Circular icon buttons, pill badges, chips, grab handles |
| `rounded-2xl` | Large floating containers — dialog, hover-card, toast, hero |
| `rounded-xl` | Menus, tooltips, mid-size panels |
| `rounded-lg` | Control containers — segments, inputs, header buttons |
| `rounded-md` / `-sm` | Items inside a control container |

**Motion — two systems, split by what moves.**

| Moving | Use |
| --- | --- |
| Position, size, layout, gestures, enter/exit | `Spring.presets.smooth` (default) / `.snappy` (controls) / `.bouncy` (sparingly) |
| Opacity, color only | `duration-200` (default), `duration-300` (slow fade), `duration-150` (press) |

**z-index — two tiers, no other values exist.**

| Surface tier (`fixed` / portal) | Intra-surface tier |
| --- | --- |
| `z-30` page chrome · `z-40` scrim · `z-50` modal surface · `z-60` popper from a surface · `z-70` toast + tooltip | `z-1` hairline · `z-10` decoration · `z-20` badges, nav arrows · `z-30` chrome bar inside the surface |

**Sizing.** Icon buttons are `size-8` (default) or `size-7` (dense). Header is `h-12`. Type scale
is dense — `text-sm` and `text-xs` carry almost all UI; `text-base`+ is for headings and empty
states. Metadata is `text-xs text-text-secondary`.

**Icons.** `<i className="i-mingcute-..." />`. `i-simple-icons-*` for third-party brand marks only.

**Placement.** Knows about photos → `apps/web/src/modules/<domain>/`. Doesn't → `packages/ui`.
Pages are thin routing shells. Merge classes with `clsxm`.

**State.** Anything shareable goes in the URL — filters as search params, open photo as
`/photos/:photoId`. Ephemeral UI state goes in a colocated Jotai atom, not prop drilling.

## Red lines

These are binary. There is no case where the surrounding code justifies them.

- **No raw hex, `rgb()`, or `gray-*`/`zinc-*`/`slate-*` for chrome.** Only exception: a
  third-party brand mark's own color.
- **No hand-written `dark:` pair** (`text-gray-900 dark:text-gray-50`). The app is dark-only and
  UIKit tokens already resolve per scheme — writing the pair means you picked the wrong token.
- **No light mode, theme toggle, or `prefers-color-scheme` branch** for chrome.
- **No new `cubic-bezier` or duration-only tween for spatial motion.** Use a `Spring` preset.
- **No z-index outside the two tiers above.** If something must sit above a tooltip, the stacking
  is wrong, not the number.
- **No fourth blur step.** `backdrop-blur-xl` / `-3xl` / `-lg` in the tree are known deviations.
- **No new `lucide-react` import.** Use `i-mingcute-*`.
- **No comments and no JSDoc** in the component you write (repo-wide rule in `AGENTS.md`).

## Do not copy these — known deviations

Older files contradict the rules above. Proximity is not permission.

| File | What's wrong |
| --- | --- |
| `packages/ui/src/button/Button.tsx` | Vendored Tremor — `gray-*` ramps, hand-rolled `dark:` pairs |
| `packages/utils/src/cn.ts` | `focusRing` hardcodes `outline-blue-500` instead of accent |
| `apps/web/src/modules/gallery/ActionPanel.tsx:25` | `bg-white/80 dark:bg-black/80 border-zinc-200` |
| `packages/ui/src/dialog/dialog.tsx` | `z-100000000`; context-menu uses `z-10060`, tooltip `z-9999` |
| `packages/ui/src/select/index.tsx`, `sonner.tsx` | `backdrop-blur-background` — not a real class, compiles to nothing |
| `Button.tsx`, `modal/Dialog.tsx` | `shape-squircle` is a no-op in `apps/web` (only defined in the dashboard's CSS) |

Full list with rationale: `/DESIGN.md` §13.

## Before you finish

1. No raw hex / neutral ramp / hand-written `dark:` pair.
2. Blur step matches role and pairs with a `bg-material-*`.
3. Radius matches container size; inner items one step tighter.
4. Spatial motion uses a `Spring` preset; only opacity/color uses `duration-*`.
5. z-index from the two tiers.
6. New view state reflected in the URL.
7. `focusRing` + accessible name on interactive elements — global CSS kills the default outline.
8. Zero comments, zero JSDoc.
9. `pnpm lint <changed paths>` and `pnpm --filter web type-check` pass.
