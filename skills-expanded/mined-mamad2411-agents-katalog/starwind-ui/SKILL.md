---
name: starwind-ui
description: Manages Starwind UI components and Astro projects - initializing, adding, searching, fixing, debugging, styling, theming, and composing UI. Provides project context, component docs, CLI guidance, and Starwind-specific composition rules. Applies when working with Starwind UI, Starwind components, Astro + Tailwind CSS v4 UI, starwind.config.json, theme tokens, dark mode, shadcn-style theme migration, or component requests such as Combobox mapping to Select.
allowed-tools: Bash(npx starwind@latest *), Bash(pnpx starwind@latest *), Bash(pnpm dlx starwind@latest *), Bash(yarn dlx starwind@latest *)
---

# Starwind UI

Astro components and design-system primitives installed as source code into the user's project via the Starwind CLI. Starwind UI is designed for Astro v6 and Tailwind CSS v4.

> **IMPORTANT:** Run CLI commands from the user's project root using the project's package runner: `npx starwind@latest`, `pnpx starwind@latest` / `pnpm dlx starwind@latest`, or `yarn dlx starwind@latest`, based on `package.json`, lockfiles, `starwind.config.json`, or user instruction.

Examples below use `npx starwind@latest`, but substitute the correct runner for the project.

## Current Project Context

Build project context from local files before editing:

- `package.json`, lockfiles, and `packageManager` -> package runner and dependency commands.
- `astro.config.*` -> Astro project shape and Tailwind/Vite setup.
- `starwind.config.json` -> `starwind.css`, `componentDir`, base color, and installed component list.
- Active Starwind CSS file -> global tokens, `@theme inline`, `:root`, `.dark`, and sidebar tokens.
- Installed component directory, commonly `src/components/starwind` -> available imports and local source.
- Local component `index.ts` exports -> final authority for component part names when docs and local code differ.

## Principles

1. **Use existing components first.** Check Starwind docs, MCP, search, local components, or registry metadata before writing custom UI.
2. **Compose, don't reinvent.** Settings page = Tabs + Card + form controls. Dashboard = Sidebar + Card + Table + feedback primitives. Searchable select = Select + SelectSearch.
3. **Use built-in variants before custom styles.** `variant="outline"`, `size="sm"`, `size="icon"`, etc.
4. **Use semantic colors and tokens.** `bg-primary`, `text-muted-foreground`, `border-border`, `bg-card`; avoid raw palette utilities when a semantic token exists.
5. **Astro syntax first.** Use `class`, `for`, browser scripts, and `.astro` component imports unless the local project intentionally uses a framework island.

## Critical Rules

These rules are always enforced. Each links to a focused reference file.

### Styling & Tailwind -> [styling.md](./rules/styling.md)

- **`class` is for layout and scoped exceptions.** Do not override component colors or typography with long utility strings when variants or tokens exist.
- **No `space-x-*` or `space-y-*` in new code.** Use `flex` or `grid` with `gap-*`.
- **Use `size-*` when width and height are equal.** `size-10`, not `w-10 h-10`.
- **Use `truncate` shorthand.** Do not spell out `overflow-hidden text-ellipsis whitespace-nowrap`.
- **No manual `dark:` color overrides for global themes.** Change `:root` and `.dark` variables in the active Starwind CSS file.

### Forms & Inputs -> [forms.md](./rules/forms.md)

- **Astro forms use semantic markup, Label, controls, and ARIA.** Starwind does not use shadcn's React `FieldGroup` / `Field` API.
- **Use `for`, not `htmlFor`.** Match `Label for` to the control `id`.
- **Preserve `name` on controls that submit.**
- **`InputGroup` uses `InputGroupInput` or `InputGroupTextarea`.** Never put raw `Input` or `Textarea` inside `InputGroup`.
- **Buttons inside inputs use `InputGroupAddon` and `InputGroupButton`.**
- **Validation pairs `aria-invalid` with `aria-describedby`.** Do not rely on color alone.

### Component Structure -> [composition.md](./rules/composition.md)

- **Items stay inside groups.** `SelectItem` -> `SelectGroup`, `Item` -> `ItemGroup`, `InputOtpSlot` -> `InputOtpGroup`, `Kbd` -> `KbdGroup`.
- **Use `asChild` only when the Starwind component documents it.** Common triggers support it, but verify from current docs or local exports.
- **Dialog, Sheet, and AlertDialog need titles.** Use `DialogTitle`, `SheetTitle`, or `AlertDialogTitle`; `class="sr-only"` is fine when visually hidden.
- **Use full Card composition.** `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`, and `CardAction` when relevant.
- **Button has no `isPending` / `isLoading`.** Compose loading with `Spinner`, `disabled`, and `aria-busy`.
- **`TabsTrigger` belongs inside `TabsList`.**
- **`Avatar` always needs `AvatarFallback`.**

### Use Components, Not Custom Markup -> [composition.md](./rules/composition.md)

- **Use existing components before custom markup.**
- **Callouts use `Alert`.**
- **Toast uses Starwind `toast` + one `Toaster`, not a custom toast stack.**
- **Use `Separator` instead of raw `hr` or border-only dividers.**
- **Use `Skeleton` for loading placeholders.**
- **Use `Spinner` for active progress.**
- **Use `Badge` for status labels.**
- **Combobox is the Select pattern.** Install `select`, then use `SelectSearch`; do not run `starwind add combobox`.

### Icons -> [icons.md](./rules/icons.md)

- **Prefer the project's existing icon system.** Do not assume Tabler just because Starwind examples often use `@tabler/icons`.
- **Do not import React icon packages in plain Astro components** unless the project uses a React island for that component.
- **Icon-only buttons need an accessible name.** Use `aria-label` or visible text.
- **Let components size common SVG children** unless a specific documented override is needed.

### Customization -> [customization.md](./customization.md)

- **Theme globally through CSS variables first.**
- **Edit the active Starwind CSS file from `starwind.config.json`; do not create a second theme file.**
- **Preserve `@theme inline`, `:root`, `.dark`, sidebar tokens, keyframes, and component-specific variables.**
- **Starwind dark mode is class-based through `.dark`.** Do not switch to a data-theme system unless the app already bridges that model.
- **For shadcn-style theme migration, merge semantic values into Starwind tokens.** See [shadcn-migration.md](./shadcn-migration.md).

### CLI -> [cli.md](./cli.md)

- **Only use documented Starwind commands and flags.**
- **Do not invent shadcn CLI features** such as `info`, `view`, `apply`, presets, templates, `--dry-run`, `--diff`, `--overwrite`, or `--cwd`.
- **`update` overwrites local component changes.** Only update when the user asks or accepts overwrite risk.
- **After `add`, read the added files** and fix alias drift, icon-library drift, missing imports, and rule violations.

## Key Patterns

These are common patterns that differentiate correct Starwind UI code.

```astro
---
import { Button } from "@/components/starwind/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/starwind/card";
import { Input } from "@/components/starwind/input";
import { Label } from "@/components/starwind/label";
import { Spinner } from "@/components/starwind/spinner";
---

<!-- Astro syntax: class + for, not className + htmlFor -->
<div class="grid gap-2">
  <Label for="email">Email</Label>
  <Input id="email" name="email" type="email" aria-invalid="false" />
</div>

<!-- Loading button: compose with Spinner, not isLoading/isPending -->
<Button disabled aria-busy="true">
  <Spinner />
  Saving...
</Button>

<!-- Card composition: header/content parts, not one generic bordered div -->
<Card>
  <CardHeader>
    <CardTitle>Workspace</CardTitle>
  </CardHeader>
  <CardContent>Project settings</CardContent>
</Card>
```

## Component Selection

| Need                         | Use                                                                                                                                |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Button/action                | `button` with documented variants and sizes                                                                                        |
| Form inputs                  | `input`, `textarea`, `label`, `select`, `native-select`, `checkbox`, `radio-group`, `switch`, `slider`, `input-otp`, `input-group` |
| Searchable select / combobox | `select` with `SelectSearch`                                                                                                       |
| Option toggle                | `toggle`; use documented group/patterns if the local project has one                                                               |
| Data display                 | `table`, `card`, `badge`, `avatar`, `item`, `kbd`                                                                                  |
| Navigation                   | `sidebar`, `breadcrumb`, `tabs`, `pagination`, `scroll-area`                                                                       |
| Overlays                     | `dialog`, `sheet`, `alert-dialog`, `popover`, `hover-card`, `tooltip`                                                              |
| Menus                        | `dropdown`, `context-menu`                                                                                                         |
| Feedback                     | `toast`, `alert`, `progress`, `skeleton`, `spinner`                                                                                |
| Media                        | `image`, `video`, `aspect-ratio`, `carousel`                                                                                       |
| Layout/disclosure            | `card`, `separator`, `accordion`, `collapsible`                                                                                    |
| Theme toggle                 | `theme-toggle`                                                                                                                     |

## Key Fields

- **`starwind.config.json`** -> source of `starwind.css`, `componentDir`, base color, and installed component list.
- **`starwind.css`** -> active Starwind CSS file for theme variables. Always edit this file for global theme work.
- **`componentDir`** -> component install root. The Starwind subdirectory is commonly `src/components/starwind`.
- **`components`** -> installed component names when present in config.
- **`packageManager` / lockfiles** -> use this for the Starwind runner and dependency installs.
- **`astro.config.*`** -> confirms Astro/Vite/Tailwind setup.
- **Local `index.ts` exports** -> exact import names for installed component parts.
- **Icon imports in nearby files** -> preferred icon package and import style.

## Component Docs, Examples, And Usage

Use the freshest Starwind context available:

```bash
npx starwind@latest docs button dialog select --json
```

Then fetch and read the returned docs or Markdown URLs before implementing. When tools are available, prefer Starwind MCP `starwind_docs` for live docs and `starwind_add` for install command generation. Local project source remains the final authority for already-installed components.

**When creating, fixing, debugging, or using a component, always read the relevant docs or local component source first.** Do not guess props, events, or composition from memory.

## Workflow

1. **Get project context** -> read `package.json`, lockfiles, Astro config, `starwind.config.json`, active Starwind CSS, installed component directory, and local exports.
2. **Check installed components first** -> do not import components that have not been added, and do not re-add ones already installed unless the user asked to update.
3. **Find components** -> use Starwind MCP, `npx starwind@latest search`, docs, `llms.txt`, `llms-full.txt`, `ai-manifest.json`, or installed registry metadata.
4. **Get docs and examples** -> use Starwind MCP or `npx starwind@latest docs <component> --json`, then fetch the docs content.
5. **Install missing components** -> use `npx starwind@latest add <component>` with the correct package runner and documented flags.
6. **Review added files** -> read new component/block files before wiring them in. Fix import aliases, icon imports, missing subcomponents, Astro syntax, and Critical Rules violations.
7. **Compose before editing internals** -> use documented props, variants, `class`, semantic tokens, and wrappers before changing installed component source.
8. **Keep changes scoped** -> preserve project patterns and avoid unrelated refactors.

## Updating Components

Starwind components are local source files after installation.

> **CAUTION:** `npx starwind@latest update` overwrites local component changes.

When the user asks to update a component while preserving local changes:

1. Read the local component files and where they are imported.
2. Read current docs or source for the target component.
3. Decide whether to manually merge the needed upstream changes or ask approval to run `update`.
4. Use `npx starwind@latest update <component>` only when the user asks for it or accepts overwrite risk.
5. Use `update --all` only when the user explicitly wants every installed component updated.

## Quick Reference

```bash
# Initialize Starwind UI
npx starwind@latest init
npx starwind@latest init --defaults
npx starwind@latest init --pro

# Add components
npx starwind@latest add button card dialog
npx starwind@latest add select
npx starwind@latest add theme-toggle

# Add all components
npx starwind@latest add --all

# Search components and Pro blocks
npx starwind@latest search select
npx starwind@latest search hero --json
npx starwind@latest search pricing --plan free --category pricing --limit 10 --json

# Get docs references
npx starwind@latest docs button dialog select --json

# Configure Starwind Pro in an existing project
npx starwind@latest setup
npx starwind@latest setup --yes

# Update or remove components
npx starwind@latest update button
npx starwind@latest remove button
```

## Detailed References

- [rules/forms.md](./rules/forms.md) -> labels, controls, InputGroup, Select, validation
- [rules/composition.md](./rules/composition.md) -> groups, overlays, Card, Tabs, Avatar, Toast, Separator, Skeleton, Spinner, Badge, Button loading
- [rules/icons.md](./rules/icons.md) -> Astro icon imports, icon buttons, icon-library drift
- [rules/styling.md](./rules/styling.md) -> semantic colors, variants, class, spacing, size, truncate, dark mode, z-index
- [cli.md](./cli.md) -> Starwind commands, flags, Pro setup, and missing shadcn CLI features
- [customization.md](./customization.md) -> theming, CSS variables, dark mode, extending components
- [shadcn-migration.md](./shadcn-migration.md) -> mapping shadcn-style theme tokens to Starwind
- [mcp.md](./mcp.md) -> MCP and AI docs source priority

Load only the references needed for the current task.
