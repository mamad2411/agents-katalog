---
name: orbyn-astryx
description: "Build, theme and review React UI with Meta's Astryx design system (@astryxdesign): pages from its templates, its components and tokens, a house style as an Astryx theme. Versions change only via Dependabot, never by hand. Use when a project uses or adopts Astryx."
---

# Astryx

Follow the consuming project's instructions and requested scope; use the
[portable defaults](../orbyn-workflow/references/project-policy.md) only where guidance is missing.

Astryx is Meta's MIT-licensed design system: React 19 or later, styles authored with
StyleX and shipped as prebuilt CSS, themes as CSS custom properties, page templates,
150+ components and a CLI that prints its own documentation. [UI design](../orbyn-ui-design/SKILL.md)
still owns the product decisions; this skill owns how they are built in Astryx.

## Before you start

1. **Confirm it fits.** A project uses Astryx when its `package.json` lists an
   `@astryxdesign/*` package. Adopting it in a new or existing app is a stack choice:
   check React 19+, the styling already in use and the migration cost with
   [stack selection](../orbyn-stack-selection/SKILL.md), and get the user's decision.
2. **Find the project's CLI.** Use the project's installed invocation: its package
   script (`pnpm astryx`, `npm run astryx --`) or local binary. That version's
   answers match the installed components. With no installed CLI, read the
   [bundled docs](references/upstream/astryx-docs/docs/README.md) (CLI 0.7.12) and say
   which version they describe; do not fetch a different CLI just to look something up.

## Build a page

Follow Astryx's own order. Each step is a read-only CLI call until you write code:

1. `astryx build "<idea>"`: the closest page template (or the app shell), two
   alternatives, and the blocks and components for what it lacks.
2. `astryx template <name> <path>`: scaffold it, keep its frame and spacing, replace
   the content. This writes files; it is part of the change you were asked to make.
3. `astryx component <Name>`: props, examples and the import path for every component
   you use. Import each from its own entry.

Astryx's rules, which this library adopts for Astryx projects: start every page from
a template; no raw `div` layout where a component exists; no `style={{}}`; tokens,
never magic values; keep a native element only when its semantics are needed and
Astryx has none. `astryx search`, `astryx docs <topic>` and `astryx doctor` answer the
rest. For anything the designs and templates do not settle, get a design draft first,
as the [lead contract](../orbyn-workflow/references/lead-contract.md#get-a-design-draft-first) says.

## Theme it

A theme is token overrides, not a fork. Map the project's look, or the
[Orbyn house style](../orbyn-ui-design/references/house-style/README.md) when it has
none, into `defineTheme({extends: <built theme>, ...})`: colours, type, radius,
spacing and elevation to their token families, component changes through the
`components` field and `astryx theme targets`. Generate shades with the palette
command rather than by hand. Run `astryx theme build` for server-rendered apps when you
change a theme; after an upgrade, the Dependabot PR rebuilds it. Eject (`swizzle`) a component only when a theme
override cannot express the change, and say why.

Astryx owns light and dark: switch with its `Theme` component's `mode` (`light`, `dark`
or `system`), not with our `data-theme` attribute and script, and never both. Our
outcome rules still hold: no flash of the wrong theme and nothing restyling after
load, which in an Astryx app means wiring the built theme CSS, since a runtime theme's
component overrides flash on hydration.

## Where these rules override Astryx's setup

1. **Never update Astryx by hand.** Do not run `astryx upgrade`, `astryx init` (in any
   form, including `--features agents` and `--user`), a global CLI install, or a
   package-manager bump of `@astryxdesign/*`, StyleX or a theme package, even when the
   CLI or `astryx doctor` suggests it. Versions move only through the project's
   Dependabot pull requests, which bump every `@astryxdesign/*` package to one release
   together; that PR rebuilds custom themes (`astryx theme build`) and refreshes agent
   docs. If something looks stale or missing, report it and point to the open
   Dependabot PR or ask the owner to open one; do not fix it in your change.
2. **Project agent files belong to the project.** `init` writes a managed block into
   `AGENTS.md` or `CLAUDE.md`, and a global install links a skill into folders such as
   `~/.claude/skills/astryx`. Leave both to the owners. If Astryx's own global
   `astryx` skill is loaded, treat it as reference; this skill's rules govern.
3. **Adopting Astryx is a decision, not a step.** Adding it to an app that lacks it
   goes through [stack selection](../orbyn-stack-selection/SKILL.md) and the owner.
4. **The hosted docs are optional.** Astryx's docs site serves an MCP endpoint. Adding
   that MCP server to a host is a configuration change: ask first.
5. **Our checks still apply.** Verify in a real render: light and dark, the widths in
   [design rules](../orbyn-ui-design/references/design-rules.md), and for a desktop app
   the built window's chrome. Review Astryx code with its rubric (`astryx docs
   is-my-code-good`), marking anything you could not see `not inspected`.

## Source and updates

The agent docs of [meta/astryx](https://github.com/meta/astryx/tree/c86484dc57847e7c4d1127810ff1422bc2174d4d/packages/cli/assets/docs)
are bundled unmodified at `c86484d` (CLI 0.7.12), MIT, with the license and a
`snapshot.json` of file hashes. They are `.mjs` modules the CLI prints; read their
`prose`, `list` and `code` entries, and prefer the project's installed CLI whenever
they differ. Never edit or re-download them by hand: `scripts/upstream_watch.py`
opens an issue when Astryx releases, and the refresh goes through
[upstream review](../orbyn-upstream-review/SKILL.md) in a reviewed PR.
