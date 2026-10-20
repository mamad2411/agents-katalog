# UI COMPONENTS KNOWLEDGE BASE

**Generated:** 2026-03-03
**Commit:** current
**Scope:** `src/components/ui`

## OVERVIEW
Atomic UI system based on shadcn/ui, customized with Liquid Glass design tokens and Radix UI primitives.

## WHERE TO LOOK
| Component Type | Files | Purpose |
|------|----------|-------|
| Layout | `card.tsx`, `separator.tsx`, `tabs.tsx` | Structural containers and grouping |
| Inputs | `button.tsx`, `input.tsx`, `select.tsx`, `checkbox.tsx` | User interaction and form controls |
| Feedback | `alert.tsx`, `progress.tsx`, `skeleton.tsx`, `sonner.tsx` | Status indicators and loading states |
| Overlays | `dialog.tsx`, `drawer.tsx`, `sheet.tsx`, `tooltip.tsx` | Contextual information and modal flows |
| Navigation | `pagination.tsx`, `tabs.tsx`, `dropdown-menu.tsx` | Wayfinding and view switching |

## CONVENTIONS
- **Variants**: Use `button-variants.ts` for shared button styles across components.
- **Composition**: Prefer `asChild` (Radix Slot) for polymorphic components to avoid prop drilling.
- **Styling**: Use `cn()` utility for all conditional class merging.
- **Accessibility**: Every interactive component must maintain Radix UI keyboard and screen reader defaults.
- **Motion**: Apply `transition-all duration-300` for hover and active states to match Liquid Glass feel.

## ANTI-PATTERNS
- **Direct Tailwind**: Don't use raw Tailwind classes for colors; use CSS variables (e.g., `bg-primary` not `bg-blue-600`).
- **Inline Logic**: Keep complex state logic in hooks or feature components, not in these atomic UI files.
- **Hardcoded Strings**: No Indonesian or English strings in UI components; pass them as props.
- **Shadow Overrides**: Avoid overriding `shadow-soft` or `shadow-sm` manually; use the design system tokens.
- **Z-Index**: Never hardcode `z-[9999]`; use the standard overlay layers provided by Radix primitives.
