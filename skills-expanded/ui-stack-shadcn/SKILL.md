---
name: ui-stack-shadcn
description: "Building with shadcn/ui without the shadcn-default look: owned source and components.json, the CLI (init, add, diff, info, docs, presets, migrations), the base library (Base UI, Radix or React Aria), theming its CSS variables in OKLCH for both themes, style, radius, fonts and density set from the direction, variants with cva and data-slot, composing the sidebar, data table, forms with Field, command palette, toasts and calendar, keeping the primitives accessible, the Tailwind v4 setup, registries, and the traps. Read when the project uses shadcn/ui (a components.json and components/ui)."
---

# shadcn/ui

The components are copied into the project (`components/ui/`), built on a
headless library, Tailwind and `cva`. Untouched, they give the look everyone
recognises: neutral grey, the default radius, a dashboard of identical
cards. The source is the project's own: this is how to add, theme, extend
and compose it so it looks like the product and stays accessible. Tailwind
itself is in `ui-stack-tailwind`, React in `ui-stack-react`.

## 1. Read the setup first

- `components.json` holds what the CLI works from: `style` (the base and
  the visual style, such as `base-nova` or `radix-vega`; `new-york` in many
  older Radix projects), `tailwind.css` (the file holding the theme),
  `tailwind.baseColor`, the `aliases`, and any `registries`.
- The base is the headless library underneath: Base UI (the default for new
  projects since July 2026), Radix (most existing projects, still
  supported) or React Aria. It decides how parts compose: Radix uses
  `asChild`, Base UI a `render` prop, and code copied from another base's
  docs breaks. `npx shadcn@latest docs dialog` prints the docs for this
  project's base.
- `lib/utils.ts` exports `cn`: from the `cn` package since September 2026
  (`export { cn } from "cn"`), `clsx` with `tailwind-merge` before;
  `npx shadcn@latest migrate cn` moves an older project over.
- `npx shadcn@latest info` prints the framework, the config, the CSS
  variables and the installed components.

## 2. Use what is there, add with the CLI

- Before writing a part, check `components/ui/`: Button, Card, Dialog,
  Sheet, Drawer, DropdownMenu, Popover, Tooltip, Tabs, Table, Field, Input,
  InputGroup, Select, NativeSelect, Combobox, Checkbox, Switch, Badge,
  Skeleton, Empty, Spinner, Sidebar, Command, Calendar, and the toasts.
- Add a missing one with `npx shadcn@latest add <name>` rather than writing
  it by hand, then adjust it to the project. `--dry-run` shows what it
  would write; `--diff` compares an edited file with the registry's current
  version; `--overwrite` throws the project's edits away.
- A new project: `npx shadcn@latest init` (Base UI; `-b radix` or `-b aria`
  for the others; `-t next`, `-t vite` and others scaffold an app), or a
  preset built on shadcn/create: `init --preset <code>` sets colours,
  fonts, radius and icons in one go.
- One component library: do not bring in another alongside it.

## 3. The theme: make it the product's

The theme is the CSS variables in the file `components.json` names:
`--background`, `--foreground`, `--card`, `--popover`, `--primary`,
`--secondary`, `--muted`, `--accent`, `--destructive`, `--border`,
`--input`, `--ring`, `--radius`, `--chart-1` to `--chart-5` and the
`--sidebar-*` set, surfaces paired with a `-foreground`, in `:root` and again
in `.dark`. Set them from DESIGN.md: the palette, the radius, the fonts.
Leaving the defaults is leaving the direction unset.

```css
@import "tailwindcss";
@import "tw-animate-css";
@custom-variant dark (&:is(.dark *));

:root {
  --radius: 0.375rem;
  --background: oklch(0.985 0.006 85);  /* values from DESIGN.md */
  --foreground: oklch(0.21 0.012 85);
  --primary: oklch(0.47 0.13 155);
  --primary-foreground: oklch(0.98 0.01 155);
  --muted-foreground: oklch(0.5 0.012 85);
  --border: oklch(0.9 0.008 85);
  --ring: oklch(0.47 0.13 155);
  /* ...and every other variable */
}
.dark {
  --background: oklch(0.16 0.008 85);
  --foreground: oklch(0.93 0.008 85);
  --primary: oklch(0.72 0.14 155);
  --primary-foreground: oklch(0.18 0.02 155);
  /* ...the full dark set */
}
@theme inline {
  --color-background: var(--background); /* the generated mapping, a line per token */
  --font-sans: var(--font-public-sans);
  --radius-sm: calc(var(--radius) * 0.6);
}
```

- OKLCH keeps steps predictable: hold the hue, move lightness and a little
  chroma per role. Neutrals take a chroma of 0.005 to 0.015 toward the
  accent's hue, not the `0 0` grey of the default.
- Every `-foreground` reaches 4.5:1 on its surface in both themes, and
  `--ring` 3:1 on the background (`ui-themes`).
- A new role (success, warning) is a pair (`--warning`,
  `--warning-foreground`) in `:root` and `.dark`, mapped in `@theme inline`
  (`--color-warning: var(--warning);`); then `bg-warning` works.
- `--chart-1` to `--chart-5` come from the palette, lighter on dark
  (`ui-part-charts`).
- Dark mode: `next-themes` (`attribute="class"`, `defaultTheme="system"`,
  `disableTransitionOnChange`) and `suppressHydrationWarning` on `<html>`.

## 4. Not the default look

| The default | Make it |
|---|---|
| Zinc or neutral greys (chroma 0) | Neutrals tinted toward the palette, or a tinted base colour (stone, olive, mauve, mist, taupe) |
| `--radius: 0.625rem` on every part | The direction's radius: about 0.25rem for a dense tool, 0.75rem for a soft consumer product; the scale follows |
| The init style's spacing | A style chosen for the product: Nova or Mira for dense tools, Maia soft and roomy, Lyra sharp and technical, Vega the classic |
| The template's font | The direction's faces through `--font-sans` and a heading variable |
| A faint grey focus ring | `--ring` from the accent at 3:1 |
| A grid of Cards, each a number and a green delta | The screen built around its decision (`ui-page-dashboard`) |
| A Badge on everything, a Dialog for every edit | Badges for status only; a page or a Sheet for long edits |

## 5. Variants and slots

- A new variant goes into the component's `cva` definition (`variant`,
  `size`), used by name, not a pile of classes overriding it at each use:

```tsx
const buttonVariants = cva("...the generated base classes...", {
  variants: {
    variant: {
      default: "bg-primary text-primary-foreground hover:bg-primary/90",
      outline: "border bg-background hover:bg-accent hover:text-accent-foreground",
      quiet: "text-muted-foreground hover:text-foreground", // added for this product
    },
    size: { default: "h-9 px-4", sm: "h-8 px-3", lg: "h-10 px-6", icon: "size-9" },
  },
  defaultVariants: { variant: "default", size: "default" },
});
```

- `className` at a call site is for layout (margin, width, grid placement),
  not for restyling the component.
- Parts carry `data-slot` attributes (`data-slot="card-header"`): style a
  slot from its parent (`*:data-[slot=card]:shadow-none`) instead of
  forking the component.
- A change the whole product needs (every input taller, every card flat) is
  made once in `components/ui/`, not at each use. New parts are composed
  from the primitives, not forked from them.

## 6. Composing the blocks

- **Sidebar**: `SidebarProvider` around the shell, `Sidebar
  collapsible="icon"` for a rail on narrower desktops, `SidebarInset` for
  the content, `SidebarTrigger` in the top bar; on phones it opens as a
  sheet. `--sidebar-width` (16rem by default) fits `ui-layout`'s 224 to
  256px.
- **Data table**: TanStack Table (`useReactTable` with the core, sorted,
  filtered and paginated row models) drawn with the `Table` primitives; the
  toolbar and footer as in `ui-part-tables`.
- **Forms**: `Field`, `FieldLabel`, `FieldDescription` and `FieldError`
  with react-hook-form's `Controller` and a zod schema through
  `zodResolver`, or TanStack Form; `data-invalid` on the Field,
  `aria-invalid` on the control, the submit disabled while submitting. The
  older `Form` wrapper still works where a project has it.

```tsx
<Controller name="email" control={form.control} render={({ field, fieldState }) => (
  <Field data-invalid={fieldState.invalid}>
    <FieldLabel htmlFor={field.name}>Work email</FieldLabel>
    <Input {...field} id={field.name} type="email" aria-invalid={fieldState.invalid} />
    {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
  </Field>
)} />
```

- **Command**: `CommandDialog` (cmdk) for a keyboard palette in apps with
  many places or actions, beside the navigation, never instead of it.
- **Toasts**: the base's own (`toast` in Base UI projects since July 2026,
  called as `toast.add({ title })`; Sonner in Radix projects,
  `toast.success(...)`), the `Toaster` once in the root layout. An error
  the user must act on stays inline (`ui-part-notifications`).
- **Dates**: `Calendar` (react-day-picker) in a `Popover`; a native date
  input is often better on phones.
- **Overlays**: `Dialog` for a short decision, `Sheet` for editing beside a
  list, `Drawer` as a bottom sheet on phones, `AlertDialog` for a
  destructive confirm (`ui-part-dialogs`).

## 7. Keep what the primitives give

- A title in every Dialog and Sheet (`DialogTitle`, hidden with `sr-only`
  when the design shows none); a label on every field; the `Trigger`
  components rather than `onClick` on a `div`.
- `asChild` or `render` only onto a component that spreads its props and
  accepts a `ref`, or the trigger loses its handlers and focus.
- Icon-only buttons get an `aria-label` or `sr-only` text; icons are
  `aria-hidden`.
- A tooltip is never the only place for information, and never on a
  disabled button (it gets no pointer or focus events): say in text why it
  is disabled.
- After editing a primitive, work every menu, select, combobox and dialog
  from the keyboard: arrows move, `Esc` closes, focus returns.

## 8. Tailwind, and registries

- Tailwind v4: the CSS imports `tailwindcss` and `tw-animate-css` (formerly
  `tailwindcss-animate`), declares `@custom-variant dark`, and maps the
  variables in `@theme inline`; `tailwind.config` stays empty in
  `components.json`. A project on Tailwind v3 keeps its v3 components (HSL
  variables, `tailwind.config.js`): upgrade Tailwind first
  (`ui-stack-tailwind`), then the components.
- Components shared across a team's projects go in a registry:
  `registry.json` lists them, `npx shadcn@latest build` writes JSON to
  `public/r/`. A named registry in `components.json` (`"registries": {
  "@team": "https://[host]/r/{name}.json" }`) installs with
  `npx shadcn@latest add @team/data-grid`; a private one reads its token
  from an environment variable, never from the file.

## 9. Traps

- The same Button restyled in ten places with long `className`s: a variant.
- Arbitrary values over the tokens (`bg-[#0f766e]`, `rounded-[14px]`,
  `h-[38px]`): a token or a variant instead.
- `add --overwrite` over an edited file; `--diff` first.
- A Radix-style part (`asChild`) pasted into a Base UI project, or the
  reverse.
- Upgrading by re-adding everything: run the documented migrations
  (`npx shadcn@latest migrate --list`) and diff the rest.
- A toast for every event, a Dialog for a long form, a Card around every
  section.

## Check it

- `npx shadcn@latest info`: the base, style and components are what you
  think they are.
- `npx shadcn@latest add <name> --diff` on an edited primitive before
  updating it.
- Build, lint and type-check as for the framework (`ui-stack-next`,
  `ui-stack-react`).
- `preview` in both themes: each `-foreground` pair and the ring as
  rendered; `ui_check` for `rounded-full`, `shadow-xl` and raw colours.
- The keyboard through every overlay you touched.

## Avoid

The untouched zinc theme and default radius; a second component library;
hand-written copies of components the CLI provides; restyling at each call
site instead of a variant; arbitrary values over tokens; overwriting edited
primitives; code from another base's docs; a Dialog without a title;
tooltips on disabled buttons; a dashboard of identical Cards with a number
and a green delta; a Badge on everything; Dialogs for what should be a page.
