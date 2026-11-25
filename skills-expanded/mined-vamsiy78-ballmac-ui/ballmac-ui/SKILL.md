---
name: ballmac-ui
description: Build interfaces with Ballmac UI, a shadcn registry (@ballmac) of accessible React 19 and Tailwind v4 components, page blocks and templates that handle loading, empty and error states, right-to-left, reduced motion and platform feel. Use when a project has a components.json, when the user mentions Ballmac or @ballmac, or when asked to build a page, dashboard, settings screen, AI chat, agent console or desktop-app UI with shadcn components.
---

# Ballmac UI

Ballmac UI is a registry you install from with the shadcn CLI. The source lands in the project (`components/ballmac/`), is never imported from a package, and never overwrites `components/ui/`. There are about 250 components, 137 free blocks (finished page sections), 17 multi-page templates, 15 presets (whole design systems), 12 themes, 14 typefaces, 5 motion feels and 4 platform feels. Components built on Radix UI also come in a Base UI version. Read the code you install: it is yours to change.

## 1. Know the project first

Run this before choosing or writing anything:

```bash
node <path-to-this-skill>/scripts/context.mjs
```

It prints JSON: the shadcn style and base library (`radix` or `base-ui`), React, Next.js and Tailwind versions, whether Cache Components is on, which Ballmac items are installed, and the next steps. Believe it over assumptions. If there is no `components.json`, run `npx shadcn@latest init` first.

## 2. Find the right item (do not guess names)

Prefer the MCP server when it is connected (`claude mcp add ballmac -- npx -y @ballmac/mcp`): `search_items`, `list_categories`, `get_item` (props, keys, source), `get_install_command`, `compose_page` (plans a whole page from blocks), `get_quality_rules`, `audit_project`.

Without MCP, use the references in this skill. Open only what you need:

| You need | Read |
| --- | --- |
| A whole page (landing, dashboard, auth, settings, AI, desktop) | [references/pages.md](references/pages.md) |
| A finished section (hero, pricing, table, chat, planner…) | [references/blocks.md](references/blocks.md) |
| A control or building part | [references/components/index.md](references/components/index.md) |
| A multi-page starter | [references/templates.md](references/templates.md) |
| A whole look (presets, themes, typefaces), motion or platform feel | [references/themes.md](references/themes.md) |
| A chart (area, bar, line, pie, radar, radial, scatter) or a chart dashboard | `chart-*` in [references/components/data-display.md](references/components/data-display.md) and `charts-1`…`charts-4` in [references/blocks.md](references/blocks.md) |
| i18n, `useResource`, images, shortcuts, motion presets | [references/helpers.md](references/helpers.md) |
| The quality rules | [references/rules.md](references/rules.md) |

One item's full API and source is public JSON: `https://ui.ballmac.com/r/<name>.json`, and its page is `https://ui.ballmac.com/components/<name>`. Each item says when to use it and when not to; follow that. Prefer a block over assembling the same section from components.

## 3. Install

```bash
npx shadcn@latest add @ballmac/button @ballmac/pricing-1
```

- Items install to `components/ballmac/<name>.tsx`, blocks to `components/ballmac/blocks/<name>/`. Import with `@/components/ballmac/<name>`.
- Dependencies (other Ballmac items, npm packages) install by themselves. Do not add them by hand.
- `@ballmac` is in shadcn's official directory. If the CLI does not know it: `npx shadcn@latest registry add @ballmac=https://ui.ballmac.com/r/{name}.json`.
- Optional look: `npx shadcn@latest add @ballmac/preset-<name>` installs a whole design system (colors, radius, typeface, feel, motion), or `@ballmac/theme` / a named theme for colors only. See themes.md.
- Base UI projects (`context.mjs` reports `base-ui`): add Base UI versions with `npx shadcn@latest add https://ui.ballmac.com/r/base/<name>.json`, or pin the registry once with `npx shadcn@latest registry add @ballmac=https://ui.ballmac.com/r/{style}/{name}.json` and the usual `@ballmac/<name>` picks the right version. Props are the same; style with `data-open`, `data-checked`, `data-active` rather than `data-state`. Guide: https://ui.ballmac.com/docs/guides/base-ui.
- Pro blocks and starters are a separate private registry (`@ballmac-pro`) that needs a licence key in `BALLMAC_LICENSE_KEY`. Only suggest Pro when a free item does not cover the need, and say it is paid.
- After installing, run `npx @ballmac/cli track` once so `npx @ballmac/cli update` can merge new versions into the user's edits later.

## 4. Build to these rules from the first draft

These are what `npx @ballmac/cli check` flags; the full list with fixes is [references/rules.md](references/rules.md).

1. **States are not optional.** Anything that loads data shows loading, empty and error. A Ballmac block takes `state` (`"loading" | "ready" | "empty" | "error"`, forms also `"submitting" | "success"`) plus `onRetry`. Drive it with `useResource` or `stateOf(query)` from `@/lib/ballmac/use-resource`; do not build your own skeleton.
2. **Tokens, not colours.** Use `bg-background`, `text-muted-foreground`, `border-border`, `bg-primary`, `chart-1…5`. No hex, `rgb()` or named colours; no `dark:` unless a token cannot express it.
3. **Logical direction.** `ms-` `me-` `ps-` `pe-` `start-` `end-` `text-start`, never `ml-` `mr-` `pl-` `pr-` `left-` `text-left`. Directional icons get `rtl:rotate-180`. Code, terminals and keys stay `dir="ltr"`.
4. **Names for controls.** Icon-only buttons need `aria-label`; every input a label; images `alt`. Keep the focus ring (`focus-visible:ring-[3px]`); never `outline-none` alone.
5. **Motion respects the user.** Use the motion presets (`@/lib/ballmac/motion`) or Tailwind transitions; anything endless stops under `prefers-reduced-motion`.
6. **Links and triggers are styled directly**, not with `asChild`: `<a className={buttonVariants({ variant: "outline" })}>` and `<DialogTrigger className={buttonVariants()}>`. This works in Radix and Base UI projects alike. Charts: pass data to `ChartArea`, `ChartBar` and the rest and let the chart frame supply the table view, patterns and states; do not hand-assemble Recharts.
7. **Images go through `Media`** (`@/lib/ballmac/media`) in blocks and pages, with real `alt`.
8. **Text for people goes through `msg`** when you build a reusable component (`useMessages()` from `@/lib/ballmac/i18n`); page copy in your own screens is just content. One `I18nProvider` translates every built-in string.
9. **Cache Components (Next.js 16.4 default).** Never read `Date.now()`, `new Date()`, `Math.random()` or `crypto.randomUUID()` while rendering; use an effect, an event handler, or pass the value in. Do not read `params`, `searchParams`, `cookies()` or `headers()` at the top of a page outside `<Suspense>`.
10. **Phones first.** No fixed widths wider than 360 px; grids that must shrink use `grid grid-cols-1` and `min-w-0`; filter rows `flex-wrap`.

## 5. Verify before you say it is done

```bash
npx @ballmac/cli check            # source audit; add --url http://localhost:3000 to also run axe in a real browser
npx tsc --noEmit
```

Fix every `error`, and look at each `warn`. For UI you changed, load it at 390 px and 1280 px, in light and dark, and with `dir="rtl"`. Say what you checked.

## Things that go wrong

- Re-implementing a block from primitives when one exists: search first.
- Editing files under `components/ui/` to match Ballmac: do not; the two sets live side by side.
- Wrapping a Ballmac `Dialog` or `Sheet` opened from state without returning focus: copy `useReturnFocus` (`@/lib/ballmac/return-focus`) the way the shipped blocks do.
- Animating a number a screen reader must read: show the static value to assistive tech and animate an `aria-hidden` copy.
- Claiming a theme "matches" without applying it: install the theme or set the CSS variables, then look at it.
