---
name: mindtickle-ui
description: Use when the user asks for Mindtickle UI components, Mindtickle blocks, Base UI composition patterns, or shadcn registry setup in React and Next.js apps.
---

# Mindtickle UI

Mindtickle UI is a shadcn-compatible registry built on Tailwind CSS v4 and Base
UI primitives. Use it to install source components into consumer projects with
`npx shadcn@latest add @mindtickle/<name>`.

> IMPORTANT: Prefer the consumer project's package runner for shadcn commands.
> Examples below use `npx shadcn@latest`, but swap in `pnpm dlx` or `bunx`
> when the project uses pnpm or bun.

## Current Project Context

```json
!`npx shadcn@latest info --json 2>/dev/null || echo '{"error": "No shadcn project found. Run shadcn init first."}'`
```

The project context tells you the actual aliases, installed components,
primitive base (`base` vs `radix`), icon library, package manager, and
resolved file-system paths. Use it before giving setup or import advice.

## Setup

1. If `components.json` is missing, initialize shadcn in Base UI mode:

```bash
npx shadcn@latest init --base base
```

2. Add the Mindtickle registry to `components.json`:

```json
{
  "registries": {
    "@mindtickle": "https://ui.mindtickle.design/registry/r/{name}.json"
  }
}
```

3. Install the theme and utility helpers:

```bash
npx shadcn@latest add @mindtickle/theme @mindtickle/utils
```

## Principles

1. Use existing Mindtickle components before writing custom markup.
2. Follow Base UI composition rules. Mindtickle is not Radix-first.
3. Use semantic tokens and variants before custom classes.
4. Use local reference files before guessing component APIs.

## Critical Rules

### Base UI Patterns → [rules/base-ui.md](./rules/base-ui.md)

- Use `render`, not `asChild`, for Base UI triggers.
- Add `nativeButton={false}` when render targets are not buttons.
- Select requires `items`; Slider single values use scalars.
- Controlled ToggleGroup single values wrap and unwrap arrays.

### Styling → [rules/styling.md](./rules/styling.md)

- Use semantic classes and built-in variants.
- Use `*-muted` surface tokens for subtle backgrounds and hover states.
- Use `gap-*`, `size-*`, and `cn()`; avoid raw colors and manual dark-mode overrides.

### Forms → [rules/forms.md](./rules/forms.md)

- Use `FieldGroup` + `Field` for structured forms.
- Use `InputGroupInput` and `InputGroupTextarea` inside `InputGroup`.
- Validation uses `data-invalid` on the wrapper and `aria-invalid` on the control.

### Icons → [rules/icons.md](./rules/icons.md)

- Use `Icon` for Mindtickle's product icon system.
- Use `data-icon` for inline component icons.
- Do not add icon sizing classes inside shared components.

### Composition → [rules/composition.md](./rules/composition.md)

- Prefer `MainNav`, `GlobalHeader`, and `PageHeader` before custom layouts.
- Group items inside their Group component.
- Overlays need titles; loading buttons are composed with `Spinner`.

## Workflow

1. Refresh project context with `npx shadcn@latest info` when needed.
2. Check installed components from the injected context or the resolved UI path.
3. Search the Mindtickle registry: `npx shadcn@latest search @mindtickle -q "sidebar"`
4. Get docs and example URLs: `npx shadcn@latest docs <component>`
5. Preview before installing: `npx shadcn@latest add @mindtickle/<name> --dry-run`
6. Install: `npx shadcn@latest add @mindtickle/<name>`
7. Compare local customizations with upstream updates: `npx shadcn@latest add @mindtickle/<name> --diff`

## Migration Workflow

For existing shadcn/ui projects, migrate incrementally instead of replacing
everything at once:

1. Inspect the current setup with `npx shadcn@latest info`
2. Add the `@mindtickle` registry and install `@mindtickle/theme` plus
   `@mindtickle/utils`
3. Pick one component or block to migrate at a time
4. Preview the incoming registry item with
   `npx shadcn@latest add @mindtickle/<name> --dry-run`
5. Review exact changes with `--view` and `--diff`
6. Merge carefully so local customizations are preserved

Use this especially when teams already have local shadcn component edits they do
not want to overwrite.

## Component Selection

| Need                 | Use                                                        |
| -------------------- | ---------------------------------------------------------- |
| Navigation sidebar   | MainNav (block, Mindtickle-exclusive)                      |
| Page header          | PageHeader (block, Mindtickle-exclusive)                   |
| Site header          | GlobalHeader (block, Mindtickle-exclusive)                 |
| Keyboard shortcuts   | Kbd (Mindtickle-exclusive)                                 |
| Button groups        | ButtonGroup (Mindtickle-exclusive)                         |
| AI text input        | AssistedInput (Mindtickle-exclusive)                       |
| Loading animation    | Spinner, ShimmerDots, ShimmeringText                       |
| Product icons        | Icon (Mindtickle icon system)                              |
| Menus                | DropdownMenu, Menubar, ContextMenu                         |
| Overlays             | Dialog, Sheet, Drawer, AlertDialog                         |
| Forms                | Field, InputGroup, Input, Select, Checkbox, RadioGroup     |

## Registry Snapshot

The current registry contains 58 UI components and 3
flagship layout blocks surfaced by this skill.

## Local References

These reference files are generated from the same MDX docs that power the docs
site, then processed for LLM-friendly local reading:

- [accordion](./references/accordion.md)
- [alert](./references/alert.md)
- [alert-dialog](./references/alert-dialog.md)
- [assisted-input](./references/assisted-input.md)
- [avatar](./references/avatar.md)
- [badge](./references/badge.md)
- [breadcrumb](./references/breadcrumb.md)
- [button](./references/button.md)
- [card](./references/card.md)
- [checkbox](./references/checkbox.md)
- [collapsible](./references/collapsible.md)
- [context-menu](./references/context-menu.md)
- [dialog](./references/dialog.md)
- [drawer](./references/drawer.md)
- [dropdown-menu](./references/dropdown-menu.md)
- [empty](./references/empty.md)
- [field](./references/field.md)
- [global-header](./references/global-header.md)
- [hover-card](./references/hover-card.md)
- [icon](./references/icon.md)
- [input](./references/input.md)
- [input-group](./references/input-group.md)
- [kbd](./references/kbd.md)
- [label](./references/label.md)
- [main-nav](./references/main-nav.md)
- [menubar](./references/menubar.md)
- [page-header](./references/page-header.md)
- [pagination](./references/pagination.md)
- [popover](./references/popover.md)
- [progress](./references/progress.md)
- [radio-group](./references/radio-group.md)
- [resizable](./references/resizable.md)
- [scroll-area](./references/scroll-area.md)
- [select](./references/select.md)
- [separator](./references/separator.md)
- [sheet](./references/sheet.md)
- [shimmering-text](./references/shimmering-text.md)
- [skeleton](./references/skeleton.md)
- [slider](./references/slider.md)
- [spinner](./references/spinner.md)
- [switch](./references/switch.md)
- [table](./references/table.md)
- [tabs](./references/tabs.md)
- [textarea](./references/textarea.md)
- [toggle](./references/toggle.md)
- [toggle-group](./references/toggle-group.md)
- [tooltip](./references/tooltip.md)

## Local Examples

Start from these examples when you need production-flavored layout patterns:

- [main-nav-learner.tsx](./examples/main-nav-learner.tsx)
- [page-header-module.tsx](./examples/page-header-module.tsx)
- [global-header-demo.tsx](./examples/global-header-demo.tsx)
- [field-demo.tsx](./examples/field-demo.tsx)
- [input-group-validation.tsx](./examples/input-group-validation.tsx)
- [dialog-settings.tsx](./examples/dialog-settings.tsx)
- [icon-colors.tsx](./examples/icon-colors.tsx)
- [assisted-input-demo.tsx](./examples/assisted-input-demo.tsx)

## Quick Commands

```bash
# Search the Mindtickle registry
npx shadcn@latest search @mindtickle -q "navigation"

# Preview a component without writing files
npx shadcn@latest add @mindtickle/main-nav --dry-run

# Install a Mindtickle block
npx shadcn@latest add @mindtickle/page-header
```
