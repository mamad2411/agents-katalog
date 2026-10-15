---
name: kao-shadcn-base-ui
description: >
  Guide for using styled, accessible React components with shadcn/ui's Base UI variant, which uses
  @base-ui/react as its primitive layer instead of Radix UI. Covers component installation,
  theming with Tailwind CSS v4 and oklch CSS variables, forms with React Hook Form and Zod, and UI
  patterns like buttons, dialogs, dropdowns, data tables, cards, and more. Use this skill whenever
  the user is working with shadcn/ui backed by @base-ui/react, importing from @/components/ui/,
  or building styled React components in a project using this Base UI-based shadcn setup. Also
  trigger when the user mentions shadcn with Base UI, uses the render prop instead of asChild, or
  references data-slot attributes. Even if the user does not explicitly mention shadcn/ui, use this
  skill when they are building React UI in a project that has both shadcn/ui and @base-ui/react
  installed.
license: MIT
metadata:
  author: kaotypr
  version: "2.0.0"
---

# shadcn/ui Component Patterns

## Overview

Expert guide for building accessible, customizable UI components with shadcn/ui, Base UI (`@base-ui/react`), and Tailwind CSS v4.

shadcn/ui is "not a component library — it's how you build your component library." Components are copied into your project as source code you own and can modify freely. This variant uses `@base-ui/react` as its primitive layer instead of Radix UI.

**Important**: shadcn/ui wraps Base UI primitives into styled, themed components under `@/components/ui/`. When building with shadcn/ui, always import from `@/components/ui/*` — never import directly from `@base-ui/react`. Even if you also have a Base UI skill available, the shadcn wrappers are the correct abstraction layer for shadcn/ui projects.

## When to Use

- Setting up a new project with shadcn/ui
- Building forms with React Hook Form and Zod validation
- Creating accessible UI components (buttons, dialogs, dropdowns, sheets)
- Customizing component styling with Tailwind CSS
- Building Next.js, Vite, TanStack Start, React Router, Laravel, or Astro applications with TypeScript

## Constraints and Warnings

- **Always import from `@/components/ui/`**: Never import directly from `@base-ui/react` in application code. The shadcn wrappers handle styling, theming, and Base UI composition internally.
- **Not an NPM Package**: Components are copied to your project; you own the code
- **Registry Security**: Verify the registry source is trusted before installation; review generated component code before production use
- **Client Components**: Most components require `"use client"` directive
- **Base UI Dependency**: Single `@base-ui/react` package provides all primitives, but you interact through shadcn wrappers in `@/components/ui/`
- **Never use `asChild`**: Use the `render` prop instead (Base UI, not Radix)
- **`render` prop with Button**: When using `render` to replace the underlying `<button>` with a non-button element (e.g., `<Link>`, `<a>`), pass `nativeButton={false}`. This applies to Button and components built on it: `AlertDialogAction`, `AlertDialogTrigger`, `DialogTrigger`, etc.
- **Floating components**: `Portal > Positioner > Popup` pattern is handled internally by shadcn wrappers — you don't compose these layers yourself
- **Tailwind CSS v4 Required**: Components use Tailwind v4 with oklch color format
- **Path Aliases**: Configure `@` alias in tsconfig.json for imports
- **Tailwind v4 cursor**: Default cursor changed to `default` in Tailwind v4. To restore pointer cursor on buttons, add to your CSS:
  ```css
  @layer base {
    button:not(:disabled), [role="button"]:not(:disabled) { cursor: pointer; }
  }
  ```

## Quick Start

### New Project

Use the CLI with `--template` for framework-specific scaffolding and `--base` to select the Base UI variant:

```bash
# Next.js
pnpm dlx shadcn@latest init -t next --base base

# Vite
pnpm dlx shadcn@latest init -t vite --base base

# TanStack Start
pnpm dlx shadcn@latest init -t start --base base

# React Router
pnpm dlx shadcn@latest init -t react-router --base base

# Laravel
pnpm dlx shadcn@latest init -t laravel --base base

# Astro
pnpm dlx shadcn@latest init -t astro --base base
```

Additional init flags:
- `--monorepo` — scaffold for monorepo setups
- `--rtl` — enable right-to-left support
- `-p, --preset [name]` — use a preset config (name, URL, or code)
- `-d, --defaults` — use default config without prompts

### Install Components

```bash
# Individual components
pnpm dlx shadcn@latest add button input form card dialog select

# All components at once
pnpm dlx shadcn@latest add --all
```

### Required Dependencies

```json
{
  "dependencies": {
    "@base-ui/react": "^1.2.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "@phosphor-icons/react": "^2.1.7",
    "tailwind-merge": "^2.0.0"
  }
}
```

## CLI Commands

Beyond `init` and `add`, the CLI provides:

```bash
# Preview components before installing
pnpm dlx shadcn@latest view button card dialog

# Search registries
pnpm dlx shadcn@latest search @shadcn -q "button"

# Fetch component docs from CLI
pnpm dlx shadcn@latest docs button

# Display project info (framework, CSS vars, installed components)
pnpm dlx shadcn@latest info

# Build registry JSON files
pnpm dlx shadcn@latest build

# Migrations
pnpm dlx shadcn@latest migrate icons    # migrate icon library
pnpm dlx shadcn@latest migrate radix    # migrate to unified radix-ui package
pnpm dlx shadcn@latest migrate rtl      # add RTL support (ml-4 → ms-4, etc.)
```

## CSS Variables & Theming

shadcn/ui uses **oklch** color format with a background/foreground naming convention. The `--primary` variable is the background color; `--primary-foreground` is the text color used on that background.

```css
:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.546 0.198 38.228);
  --chart-4: oklch(0.596 0.151 343.253);
  --chart-5: oklch(0.546 0.158 49.157);
  --sidebar-background: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.556 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);
  --ring: oklch(0.439 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.698 0.141 24.311);
  --chart-4: oklch(0.676 0.172 171.196);
  --chart-5: oklch(0.578 0.192 302.85);
}
```

Available base colors: Neutral, Stone, Zinc, Mauve, Olive, Mist, Taupe.

### Adding Custom Colors

Use `@theme inline` directive (Tailwind v4) to register custom CSS variables as colors:

```css
:root {
  --warning: oklch(0.84 0.16 84);
  --warning-foreground: oklch(0.28 0.07 46);
}
.dark {
  --warning: oklch(0.41 0.11 46);
  --warning-foreground: oklch(0.99 0.02 95);
}
@theme inline {
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
}
```

Then use as `bg-warning text-warning-foreground` in your components.

## Core Components

shadcn/ui provides **59 components**: Accordion, Alert, Alert Dialog, Aspect Ratio, Avatar, Badge, Breadcrumb, Button, Button Group, Calendar, Card, Carousel, Chart, Checkbox, Collapsible, Combobox, Command, Context Menu, Data Table, Date Picker, Dialog, Direction, Drawer, Dropdown Menu, Empty, Field, Hover Card, Input, Input Group, Input OTP, Item, Kbd, Label, Menubar, Native Select, Navigation Menu, Pagination, Popover, Progress, Radio Group, Resizable, Scroll Area, Select, Separator, Sheet, Sidebar, Skeleton, Slider, Sonner, Spinner, Switch, Table, Tabs, Textarea, Toast, Toggle, Toggle Group, Tooltip, Typography.

All components are available in both Radix UI and Base UI variants, selectable via `--base` flag during init.

### Button

```bash
pnpm dlx shadcn@latest add button
```

```tsx
import { Button } from "@/components/ui/button";

// Variants: default, destructive, outline, secondary, ghost, link
// Sizes: xs, sm, default, lg, icon, icon-xs, icon-sm, icon-lg
<Button variant="destructive" size="sm">Delete</Button>
```

**Icons in buttons** — use the `data-icon` attribute:

```tsx
<Button>
  <PlusIcon data-icon="inline-start" />
  Add Item
</Button>

<Button>
  Settings
  <GearIcon data-icon="inline-end" />
</Button>
```

**Loading state** with Spinner:

```tsx
<Button disabled>
  <Spinner /> Saving...
</Button>
```

**Button as a link** — must pass `nativeButton={false}` when rendering a non-button element:

```tsx
import Link from "next/link";
import { Button } from "@/components/ui/button";

<Button nativeButton={false} render={<Link href="/signup" />}>
  Get Started
</Button>
```

This also applies to `AlertDialogAction`, `AlertDialogTrigger`, `DialogTrigger`, etc.:

```tsx
<AlertDialogAction nativeButton={false} render={<Link href="/next-step" />}>
  Continue
</AlertDialogAction>
```

**Rounded buttons**: use `rounded-full` class.

**ButtonGroup**: Group related buttons together:

```tsx
import { ButtonGroup } from "@/components/ui/button"

<ButtonGroup>
  <Button variant="outline">Left</Button>
  <Button variant="outline">Center</Button>
  <Button variant="outline">Right</Button>
</ButtonGroup>
```

### Input & Label

```bash
pnpm dlx shadcn@latest add input label
```

```tsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

<div className="grid w-full max-w-sm items-center gap-1.5">
  <Label htmlFor="email">Email</Label>
  <Input type="email" id="email" placeholder="Email" />
</div>
```

### Field (Accessible Form Fields)

The `Field` component provides structured, accessible form markup:

```tsx
import { Field, FieldLabel, FieldError, FieldDescription } from "@/components/ui/field"
import { Input } from "@/components/ui/input"

<Field data-invalid={fieldState.invalid}>
  <FieldLabel htmlFor={field.name}>Email</FieldLabel>
  <Input {...field} aria-invalid={fieldState.invalid} />
  <FieldDescription>We'll never share your email.</FieldDescription>
  {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
</Field>
```

### Forms with Validation

```bash
pnpm dlx shadcn@latest add form
```

```tsx
"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import {
  Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"

const formSchema = z.object({
  username: z.string().min(2, { message: "Username must be at least 2 characters." }),
  email: z.string().email({ message: "Please enter a valid email address." }),
})

export function ProfileForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { username: "", email: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-8">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="shadcn" {...field} />
              </FormControl>
              <FormDescription>Your public display name.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

**Validation modes**: onChange, onBlur, onSubmit (default), onTouched, all.

**Dynamic arrays** with `useFieldArray`:

```tsx
const { fields, append, remove } = useFieldArray({
  control: form.control,
  name: "items",
})

{fields.map((field, index) => (
  <FormField key={field.id} control={form.control} name={`items.${index}.value`}
    render={({ field }) => (
      <FormItem>
        <FormControl><Input {...field} /></FormControl>
        <Button type="button" onClick={() => remove(index)}>Remove</Button>
      </FormItem>
    )}
  />
))}
<Button type="button" onClick={() => append({ value: "" })}>Add Item</Button>
```

**Select in form** — use `onValueChange` and `defaultValue`:

```tsx
<FormField
  control={form.control}
  name="role"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Role</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select a role" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          <SelectItem value="admin">Admin</SelectItem>
          <SelectItem value="user">User</SelectItem>
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
```

**Checkbox in form** — use `checked` and `onCheckedChange`:

```tsx
<FormField
  control={form.control}
  name="notifications"
  render={({ field }) => (
    <FormItem className="flex flex-row items-start space-x-3 space-y-0">
      <FormControl>
        <Checkbox checked={field.value} onCheckedChange={field.onChange} />
      </FormControl>
      <div className="space-y-1 leading-none">
        <FormLabel>Email notifications</FormLabel>
      </div>
    </FormItem>
  )}
/>
```

**Switch in form** — use `checked` and `onCheckedChange`:

```tsx
<FormField
  control={form.control}
  name="emailNotifications"
  render={({ field }) => (
    <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
      <div className="space-y-0.5">
        <FormLabel className="text-base">Email Notifications</FormLabel>
        <FormDescription>Receive emails about account activity.</FormDescription>
      </div>
      <FormControl>
        <Switch checked={field.value} onCheckedChange={field.onChange} />
      </FormControl>
    </FormItem>
  )}
/>
```

### Card

```bash
pnpm dlx shadcn@latest add card
```

```tsx
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card Description</CardDescription>
  </CardHeader>
  <CardContent><p>Card Content</p></CardContent>
  <CardFooter><p>Card Footer</p></CardFooter>
</Card>
```

### Dialog

```tsx
"use client"

import {
  Dialog, DialogContent, DialogDescription, DialogHeader,
  DialogTitle, DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

<Dialog>
  <DialogTrigger render={<Button variant="outline" />}>
    Edit Profile
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
      <DialogDescription>Make changes to your profile here.</DialogDescription>
    </DialogHeader>
    {/* form content */}
  </DialogContent>
</Dialog>
```

Features: custom close button via `showCloseButton={false}`, sticky footer, scrollable content.

### AlertDialog (Confirmation Modal)

```tsx
"use client"

import {
  AlertDialog, AlertDialogTrigger, AlertDialogContent, AlertDialogHeader,
  AlertDialogFooter, AlertDialogTitle, AlertDialogDescription,
  AlertDialogAction, AlertDialogCancel,
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"

<AlertDialog>
  <AlertDialogTrigger render={<Button variant="outline" />}>
    Delete Item
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
      <AlertDialogDescription>
        This action cannot be undone.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction>Continue</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Popover

```tsx
"use client"

import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"

<Popover>
  <PopoverTrigger render={<Button variant="outline" />}>
    Open Popover
  </PopoverTrigger>
  <PopoverContent side="top" align="center">
    <p className="text-sm">Popover content here.</p>
  </PopoverContent>
</Popover>
```

### DropdownMenu

```tsx
"use client"

import {
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
  DropdownMenuSeparator, DropdownMenuLabel, DropdownMenuGroup,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"

<DropdownMenu>
  <DropdownMenuTrigger render={<Button variant="outline" />}>
    Open Menu
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuLabel>My Account</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuGroup>
      <DropdownMenuItem>Profile</DropdownMenuItem>
      <DropdownMenuItem>Settings</DropdownMenuItem>
    </DropdownMenuGroup>
    <DropdownMenuSeparator />
    <DropdownMenuItem variant="destructive">Log out</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

For submenus, checkboxes, and radio items, use `DropdownMenuSub`, `DropdownMenuCheckboxItem`, `DropdownMenuRadioGroup`, `DropdownMenuRadioItem`.

### Select

```bash
pnpm dlx shadcn@latest add select
```

```tsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

<Select>
  <SelectTrigger className="w-[180px]">
    <SelectValue placeholder="Select a fruit" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="apple">Apple</SelectItem>
    <SelectItem value="banana">Banana</SelectItem>
  </SelectContent>
</Select>
```

### Table

```bash
pnpm dlx shadcn@latest add table
```

```tsx
import {
  Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table"

<Table>
  <TableCaption>A list of recent invoices.</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead>Invoice</TableHead>
      <TableHead>Status</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell className="font-medium">INV001</TableCell>
      <TableCell>Paid</TableCell>
      <TableCell className="text-right">$250.00</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

### Charts

Built on **Recharts** with `ChartContainer` and `ChartConfig` for consistent theming. See `references/chart.md` for full chart examples (bar, line, area, pie).

```tsx
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import { ChartContainer, ChartTooltipContent } from "@/components/ui/chart"

const chartConfig = {
  desktop: { label: "Desktop", color: "var(--chart-1)" },
} satisfies import("@/components/ui/chart").ChartConfig

<ChartContainer config={chartConfig} className="min-h-[200px] w-full">
  <BarChart accessibilityLayer data={chartData}>
    <CartesianGrid vertical={false} />
    <XAxis dataKey="month" tickLine={false} axisLine={false} />
    <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
    <ChartTooltip content={<ChartTooltipContent />} />
  </BarChart>
</ChartContainer>
```

### Toast (Sonner)

```bash
pnpm dlx shadcn@latest add sonner
```

Add `<Toaster />` to your root layout, then use the `toast()` function:

```tsx
import { toast } from "sonner"

toast("Event created", {
  description: "Friday, March 14, 2026",
  action: { label: "Undo", onClick: () => console.log("Undo") },
})
```

## Dark Mode

### Next.js (using next-themes)

```bash
pnpm add next-themes
```

Create `components/theme-provider.tsx`:

```tsx
"use client"
import * as React from "react"
import { ThemeProvider as NextThemesProvider } from "next-themes"

export function ThemeProvider({ children, ...props }: React.ComponentProps<typeof NextThemesProvider>) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}
```

Wrap in `app/layout.tsx`:

```tsx
<html lang="en" suppressHydrationWarning>
  <body>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      {children}
    </ThemeProvider>
  </body>
</html>
```

### Vite

Create a `ThemeProvider` using React context + localStorage + `prefers-color-scheme` media query. Supports "light", "dark", "system" themes. Persist choice in localStorage.

## Customizing Components

Since you own the code, customize directly. Components use `cva` (class-variance-authority) for variant styling and `cn()` for class merging. Example `button.tsx`:

```tsx
"use client"
import { Button as ButtonPrimitive } from "@base-ui/react/button"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils/ui-utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors outline-none",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/80",
        destructive: "bg-destructive/10 text-destructive hover:bg-destructive/20",
        outline: "border border-input bg-background hover:bg-muted",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-muted hover:text-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 gap-1.5 px-2.5",
        xs: "h-7 gap-1 px-2 text-xs",
        sm: "h-8 gap-1 px-2.5 text-sm",
        lg: "h-10 gap-1.5 px-2.5",
        icon: "size-9",
        "icon-xs": "size-7",
        "icon-sm": "size-8",
        "icon-lg": "size-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

function Button({ className, variant = "default", size = "default", ...props }:
  ButtonPrimitive.Props & VariantProps<typeof buttonVariants>) {
  return (
    <ButtonPrimitive data-slot="button" className={cn(buttonVariants({ variant, size, className }))} {...props} />
  )
}
export { Button, buttonVariants }
```

## Next.js Integration

- Add `"use client"` to interactive components
- Add `<Toaster />` to root layout for toast notifications
- Use `cn()` from `@/lib/utils` for class merging
- Wrap interactive shadcn components in Client Components when used in Server Components
- Configure `rsc: true` in `components.json` for React Server Components support

## RTL Support

Enable RTL during initialization or migrate an existing project:

```bash
# New project
pnpm dlx shadcn@latest init --rtl

# Existing project
pnpm dlx shadcn@latest migrate rtl
```

The migration converts physical CSS properties to logical ones (`ml-4` becomes `ms-4`, `pr-2` becomes `pe-2`, etc.) so layouts work correctly in both LTR and RTL contexts.

## Key Differences from Standard shadcn/ui

| Standard shadcn/ui | This Project (Base UI variant) |
|---|---|
| Multiple `@radix-ui/*` packages | Single `@base-ui/react` package |
| `asChild` prop | `render` prop |
| `data-[state=open]` | `data-open` |
| `data-[state=active]` (tabs) | `data-[active]` (tabs) |
| Direct Portal usage | `Portal > Positioner > Popup` (handled by wrappers) |
| `Slot` from `@radix-ui/react-slot` | `render={<Component />}` prop |
| No `data-slot` convention | `data-slot` attributes on all wrappers |
| `lucide-react` icons | `@phosphor-icons/react` icons |
| HSL color format (legacy) | oklch color format |

For detailed Base UI primitive API and patterns, consult the `kao-base-ui` skill.

## components.json

The `components.json` file configures paths, aliases, and settings:

```json
{
  "style": "new-york",
  "rsc": true,
  "tailwind": {
    "config": "",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

## References

For detailed examples and API docs, see:
- `references/chart.md` — Chart component examples
- `references/ui-reference.md` — Full component API reference
- `references/reference.md` — Additional component patterns
- `references/learn.md` — Learning guide for newcomers
