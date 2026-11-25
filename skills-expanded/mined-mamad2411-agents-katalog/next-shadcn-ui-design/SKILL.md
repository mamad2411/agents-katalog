---
name: next-shadcn-ui-design
description: >-
  Enforces consistent UI for this Next.js app using Tailwind CSS v4, shadcn/ui
  (new-york), design tokens, and Lucide icons. Use when building or changing
  pages, layouts, components, styling, forms, navigation, or visual hierarchy;
  when the user asks for UI consistency, theming, or component patterns; or
  when adding interactive elements that should match the design system.
---

# Next.js + shadcn/ui design standards

## Precedence

For product UI in this repository, follow this skill over generic “creative frontend” skills unless the user explicitly asks for a one-off marketing or experimental page.

## Stack (do not fight it)

- **Styling**: Tailwind utility classes only for layout/spacing; semantic colors via tokens (`bg-background`, `text-foreground`, `border-border`, `text-muted-foreground`, `bg-primary`, etc.).
- **Components**: Prefer **shadcn/ui** primitives from `@/components/ui/*`. Add new ones with `npx shadcn@latest add <name>` rather than copying random markup from the web.
- **Class merging**: Use `cn()` from `@/lib/utils` whenever combining conditional or prop-driven classes.
- **Icons**: **Lucide** (`lucide-react`). Size with Tailwind (`size-4`, `h-5 w-5`); keep stroke weight consistent within a view.

## Layout and hierarchy

- Use a **predictable page structure**: optional full-height shell (`min-h-full flex flex-col`), main content in a **max-width** container with consistent horizontal padding (`px-4 md:px-6`).
- **Typography**: Prefer token-based text colors (`text-foreground`, `text-muted-foreground`). Titles: `font-semibold tracking-tight`; body: `text-sm` or `text-base` with `leading-relaxed` for long copy. Use `text-balance` / `text-pretty` on headings and paragraphs where it improves line breaks.
- **Density**: Default to comfortable spacing (`gap-4`, `gap-6`, `space-y-4`). Tighten only inside dense tools (tables, settings lists).

## Surfaces and borders

- Cards and panels: `rounded-xl border border-border bg-card text-card-foreground shadow-sm` (adjust radius/shadow together—do not mix arbitrary `rounded-lg` on cards if the rest of the app uses `rounded-xl`).
- Dividers: `border-border` or `bg-border`; avoid ad-hoc gray hex values.
- Focus: rely on shadcn focus rings (`ring-ring`); do not remove focus styles without a visible replacement.

## Buttons and links

- **Actions**: `Button` from `@/components/ui/button`. Variants: `default` for primary, `outline` or `ghost` for secondary, `destructive` for irreversible actions, `link` for inline text actions.
- **Navigation to routes**: use `next/link` with `Button asChild` when the control should look like a button.
- **External links**: `target="_blank"` with `rel="noreferrer"` (and mention external in label if ambiguous).

## Forms (when added)

- Use shadcn **Label**, **Input**, **Textarea**, **Select**, **Checkbox**, **Switch** from the registry; group with consistent `space-y-2` and describe errors with `text-destructive` / `text-sm`.
- Associate labels with controls (`htmlFor` / `id`); do not rely on placeholder text alone.

## Dark mode

- Theme is **class-based** (`.dark` on an ancestor, typically `html`). Use `next-themes` or a small provider if toggling; keep `suppressHydrationWarning` on `html` when the theme class is set client-side.
- Never hard-code light-only grays for text that must work in dark mode; use tokens.

## Files to respect

- Global theme and Tailwind theme bridge: `src/app/globals.css` (includes a direct import of `shadcn/dist/tailwind.css` because PostCSS does not resolve the package `style` export—if you relocate `globals.css`, update that path).
- shadcn config: `components.json`
- New UI primitives: `src/components/ui/*`

## Anti-patterns

- Raw HTML buttons styled with one-off Tailwind for primary actions when `Button` exists.
- `zinc-500`, `#ccc`, etc., for semantic text/backgrounds instead of tokens.
- Mixing another component library alongside shadcn for the same role (two different “Button” systems).
- Inline `style={{}}` except for truly dynamic values (e.g. progress width).
