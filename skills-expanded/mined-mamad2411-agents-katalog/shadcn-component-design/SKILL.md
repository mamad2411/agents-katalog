---
name: shadcn-component-design
description: Use when designing, composing, or extending shadcn/ui components — covering CVA variant patterns, Radix primitive wiring, custom component authoring, compound components, and accessibility integration.
---

# shadcn/ui Component Design

## Specialization

Provide expert-level guidance for designing, composing, and extending shadcn/ui components — covering CVA (`class-variance-authority`) variant patterns, Radix UI primitive integration, custom component authoring on top of shadcn base components, compound component patterns, and accessibility annotation.

This skill covers component-level design. Project installation and wiring is handled by `shadcn-setup`. CSS variable theming is handled by `shadcn-theming`. Form field composition is handled by `shadcn-forms`. Quality gate review is handled by `shadcn-quality-gate`.

## Trigger Conditions

- Designing a new UI component that extends or composes shadcn/ui primitives.
- Creating a custom variant for an existing shadcn component (Button, Badge, Alert, Card, etc.).
- Implementing a compound component pattern (e.g., `Card.Header`, `Dialog.Body`) from Radix primitives.
- Auditing shadcn component usage for accessibility gaps, prop-drilling anti-patterns, or Radix misuse.
- Adding new components not yet in the shadcn registry using Radix primitives directly.
- Establishing cross-project component conventions: naming, export contracts, variant taxonomy.

## When Not to Use

- Project setup and `components.json` configuration (use `shadcn-setup`).
- CSS variable and theme token customization (use `shadcn-theming`).
- Form patterns with `react-hook-form` + `zod` integration (use `shadcn-forms`).
- Quality gate sign-off for a release candidate (use `shadcn-quality-gate`).

## Inputs

- Target component or component slice being designed or extended.
- Variant requirements (size, color, intent, state).
- Framework in use (React 18+, Next.js App Router, Remix, Astro + React).
- RSC constraints if applicable (must flag which components require `"use client"`).
- Accessibility requirements and WCAG target level (default: 2.2 AA).
- Design tokens available (from `shadcn-theming` or design system artifact).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Component source | Fully typed TSX component with `cn()` helper, `cva()` variants, and `forwardRef` pattern where appropriate |
| CVA variant schema | All variant keys, value options, default variant, and compound variant rules documented |
| Radix primitive wiring | Primitive import, `asChild` use rationale, slot pattern, and forwarded prop contract |
| RSC boundary annotation | `"use client"` directives declared for every component that uses browser APIs, event handlers, or React state |
| `cn()` usage record | All conditional classes use `cn()` from `@/lib/utils`; no raw string concatenation |
| Accessibility annotation | ARIA role, keyboard interaction, focus management, and screen-reader label coverage for each interactive component |
| Export contract | Named exports from `@/components/ui/<component>` following registry conventions |
| Readiness summary | Known edge cases, deferred variants, and open accessibility items |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Create one styled component with a default variant | Component renders, variant applies, no console errors |
| L2 Practical Delivery | Deliver a component with full variant taxonomy | All variants defined in CVA, typed, and rendered correctly |
| L3 Radix Integration | Implement a complex interactive component from Radix primitives | Primitive wiring correct, keyboard interaction tested, ARIA pattern verified |
| L4 Expert Standardization | Reusable cross-project component conventions | CVA schema taxonomy, export contract, and a11y baseline documented for any project |

## Core Patterns

### CVA Variant Pattern

```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  // Base classes — always applied
  "inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
    )
  }
)
Button.displayName = "Button"
```

### Radix `asChild` Pattern

Use `asChild` when the consumer needs to supply their own underlying element (e.g., wrapping a Next.js `Link` with a Button):

```tsx
<Button asChild>
  <Link href="/dashboard">Go to Dashboard</Link>
</Button>
```

- `asChild` merges props onto the child element using Radix `Slot`.
- Only use `asChild` when the component explicitly supports it via `Slot`.
- Never use `asChild` on components that own critical ARIA roles internally.

### Compound Component Pattern

```tsx
// Card compound component (matches shadcn registry pattern)
const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("rounded-xl border bg-card text-card-foreground shadow", className)} {...props} />
  )
)
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
)
CardHeader.displayName = "CardHeader"
```

Named exports keep components discoverable and tree-shakeable. Avoid default exports.

### RSC Boundary Rules

| Component trait | Boundary decision |
|---|---|
| Uses `useState`, `useEffect`, custom hooks | `"use client"` required |
| Uses Radix interactive primitives (Dialog, DropdownMenu, Popover) | `"use client"` required |
| Pure presentational (Card, Badge, Separator) | Server component safe — no directive needed |
| Uses `onClick`, `onChange`, or other event handlers | `"use client"` required |
| Wraps a client component inside a server component | Allowed; pass server-rendered content as children |

### Adding Components Not in the Registry

When a required component is not available via `npx shadcn add`:

1. Identify the closest Radix primitive (e.g., `@radix-ui/react-slider` for Slider).
2. Install the primitive: `npm install @radix-ui/react-slider`.
3. Author the component following the shadcn pattern: Radix primitive + CVA variants + `cn()` + `forwardRef`.
4. Place in `@/components/ui/<component>.tsx`.
5. Export from the shared index if a multi-export pattern is established.
6. Document in the source catalog that this is a custom component, not from the registry.

## Accessibility Requirements

All interactive components must satisfy:

- **Keyboard**: full keyboard operability per WAI-ARIA Authoring Practices Guide pattern for the component type.
- **Focus management**: `focus-visible:ring-2 focus-visible:ring-ring` on all focusable elements.
- **ARIA roles**: inherited from Radix primitives when using them; manually assigned for custom components.
- **Screen reader labels**: all icon-only buttons include `aria-label`; all form inputs are labeled.
- **Reduced motion**: animations use `motion-safe:` or `prefers-reduced-motion` media queries.

## Pragmatic Stop Rule

Stop when every component has a valid CVA schema, typed export contract, RSC boundary annotated, and accessibility requirements met. Deferred variants and open items must be recorded in the readiness summary.
