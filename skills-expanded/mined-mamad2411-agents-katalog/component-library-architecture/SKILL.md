---
name: component-library-architecture  
description: Build production-grade component libraries — shadcn/ui patterns, composition, variants, accessibility
triggers: [component library, design system, shadcn, component architecture, reusable components, UI library]
---

# SKILL: Component Library Architecture

## The shadcn/ui Philosophy

**Not a dependency. A code distribution system.**

```
Traditional libraries:
❌ npm install @ui-lib → locked into their API
❌ Want customization? → Fight CSS overrides
❌ Missing feature? → Wait for maintainers or wrap

shadcn/ui approach:
✅ Copy actual TypeScript code into your project
✅ Own the components completely  
✅ Modify anything without permission
✅ Build your own system with battle-tested foundations
```

## Core Architecture Patterns

### Pattern 1: Composable Primitives (Radix UI)
```tsx
// Base primitive (from Radix UI)
import * as DialogPrimitive from "@radix-ui/react-dialog"

// Your styled wrapper
const Dialog = DialogPrimitive.Root
const DialogTrigger = DialogPrimitive.Trigger

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPrimitive.Portal>
    <DialogPrimitive.Overlay className="fixed inset-0 bg-black/50" />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 translate-x-[-50%] translate-y-[-50%]",
        "w-full max-w-lg rounded-lg bg-white p-6",
        className
      )}
      {...props}
    >
      {children}
    </DialogPrimitive.Content>
  </DialogPrimitive.Portal>
))

// Usage: composable, accessible, customizable
<Dialog>
  <DialogTrigger>Open</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm action</DialogTitle>
    </DialogHeader>
    <p>Are you sure?</p>
    <DialogFooter>
      <Button>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

**Why this pattern:**
- ✅ Accessible by default (ARIA, keyboard nav)
- ✅ Composable (mix and match parts)
- ✅ Predictable API across all components
- ✅ AI-friendly (consistent patterns)

### Pattern 2: Variant System (class-variance-authority)
```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  // Base styles (always applied)
  "inline-flex items-center justify-center rounded-md font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

// Type-safe props
interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)

// Usage
<Button variant="destructive" size="lg">Delete</Button>
<Button variant="ghost">Cancel</Button>
```

**Why variants:**
- ✅ Type-safe (TypeScript autocomplete)
- ✅ Consistent patterns across all components
- ✅ Easy to add new variants
- ✅ Composable (combine multiple variants)

### Pattern 3: CSS Variables for Theming
```css
/* theme.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    /* ... all colors */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    /* ... dark mode colors */
  }
}
```

```tsx
// Components reference CSS variables
<div className="bg-background text-foreground">
  <Button className="bg-primary text-primary-foreground">
    Click me
  </Button>
</div>
```

**Why CSS variables:**
- ✅ Theme switching (light/dark) without JavaScript
- ✅ All components update automatically
- ✅ Copy component from anywhere → matches your theme
- ✅ Easy customization (change one variable → entire system updates)

## Component Composition Patterns

### Compound Components
```tsx
// Card component (compound pattern)
const Card = ({ children, ...props }) => (
  <div className="rounded-lg border bg-card text-card-foreground shadow-sm" {...props}>
    {children}
  </div>
)

const CardHeader = ({ children, ...props }) => (
  <div className="flex flex-col space-y-1.5 p-6" {...props}>{children}</div>
)

const CardTitle = ({ children, ...props }) => (
  <h3 className="text-2xl font-semibold leading-none tracking-tight" {...props}>{children}</h3>
)

const CardDescription = ({ children, ...props }) => (
  <p className="text-sm text-muted-foreground" {...props}>{children}</p>
)

const CardContent = ({ children, ...props }) => (
  <div className="p-6 pt-0" {...props}>{children}</div>
)

const CardFooter = ({ children, ...props }) => (
  <div className="flex items-center p-6 pt-0" {...props}>{children}</div>
)

// Usage
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    Main content here
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### Polymorphic Components (as prop)
```tsx
type AsProp<C extends React.ElementType> = {
  as?: C
}

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P)

type PolymorphicComponentProp<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>

// Text component that can be any HTML element
type TextProps<C extends React.ElementType> = PolymorphicComponentProp<
  C,
  { color?: "default" | "muted" }
>

const Text = <C extends React.ElementType = "span">({
  as,
  color = "default",
  children,
  ...props
}: TextProps<C>) => {
  const Component = as || "span"
  return (
    <Component
      className={cn(color === "muted" && "text-muted-foreground")}
      {...props}
    >
      {children}
    </Component>
  )
}

// Usage
<Text>Default span</Text>
<Text as="p">Paragraph</Text>
<Text as="h1">Heading</Text>
<Text as={Link} href="/home">Link</Text>
```

## File Structure (shadcn/ui standard)
```
components/
├── ui/                    # Core UI primitives
│   ├── button.tsx
│   ├── dialog.tsx
│   ├── input.tsx
│   ├── card.tsx
│   └── ...
├── composed/              # Business components (use ui/)
│   ├── user-card.tsx
│   ├── product-list.tsx
│   └── ...
└── lib/                   # Utilities
    ├── utils.ts           # cn() helper
    └── registry-schema.ts # Component schema
```

## Quality Checks
- [ ] All components use Radix UI primitives (accessible)
- [ ] Variants defined with CVA (type-safe)
- [ ] CSS variables for all colors (themeable)
- [ ] Compound components for complex UI
- [ ] TypeScript strict mode enabled
- [ ] Components are composable (don't require specific hierarchy)
- [ ] No prop drilling (use compound components)
- [ ] Accessibility tested (keyboard nav, screen readers)
