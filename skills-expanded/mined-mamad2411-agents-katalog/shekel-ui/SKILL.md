---
name: shekel-ui
description: Design system for building warm, editorial-style web applications. Sealed grid layouts, Newsreader/Nunito Sans/Cascadia Code typography, oklch color tokens, and detailed component patterns. Extends shadcn/ui. Use when building or modifying any UI — dashboards, master-detail views, tables, charts, or any web application.
user-invocable: false
---

# Shekel UI Design System

A complete design system for building warm, structured web applications. This skill defines the aesthetic, layout, and component patterns. Every new page, component, or modification must follow these rules.

## Philosophy

- **Warm editorial** — cream (`#FBF6F0`) + white palette, Newsreader serif headings, warm dark mode
- **Hermetically sealed** — every section is a bordered cell. No floating cards. Borders go edge-to-edge.
- **Three-font system** — Newsreader Variable (headings, weight 400), Nunito Sans Variable (body), Cascadia Code (mono)
- **Defined and structured** — everything has clear visual boundaries, consistent padding, predictable hierarchy
- **Light touch** — transitions only on interactive elements, animations are subtle (6px slide, 300ms), no visual noise

## Getting Started

If you're building a new app or adding to an existing one, start with the **workflow**:

| Document | When to read |
|----------|-------------|
| [workflow.md](./workflow.md) | **Start here** — project scaffolding, decision tree, implementation order |
| [design-system.md](./design-system.md) | Colors, fonts, spacing, borders, dark mode tokens |
| [patterns.md](./patterns.md) | Page layout, sealed grids, split tables, metric cards, charts, animations |
| [components.md](./components.md) | Sidebar, list items, metric cards, tables, chart tooltips, toasts, code blocks |

## shadcn/ui Foundation

This skill extends shadcn/ui. See [./shadcn/SKILL.md](./shadcn/SKILL.md) for component APIs, CLI usage, and composition rules. All shadcn rules apply — shekel-ui adds the aesthetic layer on top.

Key shadcn rules that are always enforced:
- Use `gap-*` not `space-x/y-*`
- Use semantic colors (`bg-background`, `text-muted-foreground`) not raw Tailwind colors
- Use `cn()` for conditional classes
- Use `Separator` component not `border-t` divs
- Icons use `HugeiconsIcon` component with icon data from `@hugeicons/core-free-icons`
- Icons in buttons use `data-icon="inline-start"` attribute

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | React + Vite |
| Runtime | Bun |
| Routing | react-router-dom |
| Styling | Tailwind CSS v4 + shadcn/ui |
| Fonts | @fontsource-variable/newsreader, @fontsource-variable/nunito-sans, @fontsource/cascadia-code |
| Icons | @hugeicons/react + @hugeicons/core-free-icons |
| Charts | Recharts (lazy loaded via React.lazy) |
| Data fetching | TanStack React Query |
| Animations | motion-number (AnimateNumber), CSS keyframes |
| Toasts | Sonner |
