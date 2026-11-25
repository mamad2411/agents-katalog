---
name: primereact-docs
description: Use when writing, configuring, or debugging PrimeReact v11 UI code — components and their props, theming and design tokens (@primeuix/themes), unstyled/PassThrough styling, Tailwind mode, forms, overlays, menus, data components, or headless hooks. Also use for PrimeReact version questions (v10 vs v11 APIs, migration, renamed/removed components). Provides the real v11 docs locally so answers come from the docs, not guesses (Claude mostly knows v10).
---

# PrimeReact v11 Docs

Local mirror of the **PrimeReact v11** documentation (from the official
`primereact.dev` docs — `llms.txt` index + per-page `.md`), plus a v10→v11
version guardrail. Ground every PrimeReact answer in these files instead of
recalling APIs from memory — v11 is a ground-up rewrite and Claude's training
mostly reflects v10.

## Always start here

1. **Read `overview.md`** — the v11 mental models (four usage modes, design-token
   theming, compound components, headless hooks, PassThrough) and gotchas.
2. **Check the installed version** — `primereact` in the project's `package.json`.
   - `11.x` → v11 is released (GA); use the mirrored v11 docs in `references/`.
   - `10.x` or lower → the API differs substantially; see `migration.md` and rely
     on your v10 knowledge for names/imports the v11 docs would get wrong.

## Version guardrail — STOP before writing a renamed/removed API

If the project is on **v11** and you are about to write any of these v10 names,
you are using training-memory APIs that were renamed/removed — open `migration.md`:

- `Calendar` → `DatePicker`, `Dropdown` → `Select`, `InputSwitch` → `Switch`,
  `OverlayPanel` → `Popover`, `Sidebar` → `Drawer`, `InputTextarea` → `Textarea`,
  `Chips` → `InputTags`, `TabView`/`TabPanel` → `Tabs`, `Steps` → `Stepper`.
- `import 'primereact/resources/themes/*.css'` (gone — theming is now
  `@primeuix/themes` design tokens via `PrimeReactProvider`).

A few v10 components are **not yet ported to v11** (Chart, Editor, TreeSelect,
CascadeSelect, MultiStateCheckbox, TriStateCheckbox, and the MegaMenu/SlideMenu/
TabMenu/PanelMenu/TieredMenu family). If a component has no page under
`references/` (check `INDEX.md`), say so and use v10 guidance — don't invent a
v11 API. (DataTable, AutoComplete, Select, TreeTable, PickList and OrderList
**are** in v11 — see `references/styled/components/`.)

## Task → which docs to read

Default to the **styled** variant (batteries-included) unless the project uses
unstyled/primitive, headless hooks, or Tailwind. Paths mirror the site:
`references/<variant>/components/<comp>.md`, `references/<variant>/guides/...`.

| Task | Read |
|---|---|
| **Getting started / install** | `references/styled/guides/introduction.md`, `references/styled/guides/installation/*` |
| **Configuration / provider** | `references/styled/guides/configuration.md` |
| **Theming / design tokens / presets / dark mode** | `references/styled/guides/theming/styled.md` |
| **Unstyled / PassThrough** | `references/styled/guides/misc/passthrough.md`, `references/styled/guides/theming/unstyled.md` |
| **Tailwind mode** | `references/styled/guides/theming/tailwind.md`, `references/tailwind/**` |
| **A specific styled component** | `references/styled/components/<component>.md` |
| **Unstyled compound primitives** | `references/primitive/components/<component>.md` |
| **Headless component hooks** | `references/headless/components/<component>.md` |
| **Standalone hooks** (`@primereact/hooks`) | `references/hooks/<use-name>.md`, `references/hooks/gettingstarted/*` |
| **Icons** | `references/styled/guides/icons/*` |
| **Accessibility** | `references/<variant>/guides/misc/accessibility.md` |
| **v10 → v11 migration / version mismatch** | `migration.md` |

## Anything else

Open `INDEX.md` for the full topic list, or grep for a symbol:
`grep -rni "definePreset" skills/primereact-docs/references/`.

## Provenance

`SOURCE.md` records the source (official `primereact.dev` endpoints) + sync date.
A daily GitHub Action refreshes the mirror; for the very latest, confirm against
`primereact.dev`.
