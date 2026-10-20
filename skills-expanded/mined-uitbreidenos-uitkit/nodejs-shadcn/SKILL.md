---
name: "shadcn"
description: "shadcn/ui: install components, customise variants, theming with CSS variables, compose compound components, extend with custom primitives"
---

# shadcn/ui Skill

## When to activate
- Adding shadcn/ui components to a Next.js or React project
- Customising the style or behaviour of an existing shadcn component
- Adding new colour themes or extending the default theme
- Building compound UI patterns on top of shadcn primitives (Dialog + Form, etc.)
- Understanding why a shadcn component is breaking or rendering incorrectly

## When NOT to use
- Projects using a different component library (MUI, Chakra) — don't mix
- When you need a component shadcn doesn't have — check Radix UI primitives directly
- Non-React projects — shadcn is React-only

## Why shadcn for AI generation

shadcn/ui copies raw component source into your repo rather than hiding it behind an npm package. This means Claude can read, understand, and surgically modify the exact component code. There are no black-box overrides — every button, dialog, and input is a plain file in `components/ui/`. This makes shadcn the most AI-legible component library available.

## Instructions

### Installation (new project)

```bash
# Next.js
npx shadcn@latest init

# Options prompted:
# Style: Default (or New York)
# Base color: Slate (or Zinc, Stone, Gray, Neutral)
# CSS variables: Yes
```

### Add components

```bash
# Add individual components
npx shadcn@latest add button
npx shadcn@latest add card dialog input label
npx shadcn@latest add form          # includes react-hook-form integration
npx shadcn@latest add table         # includes TanStack Table
npx shadcn@latest add data-table    # full data table with pagination/sorting

# Add all at once
npx shadcn@latest add button card dialog input form table badge avatar
```

### File structure after init

```
components/
└── ui/
    ├── button.tsx      # each component lives here — editable source
    ├── card.tsx
    ├── dialog.tsx
    ├── input.tsx
    └── ...
lib/
└── utils.ts           # cn() helper (clsx + tailwind-merge)
app/
└── globals.css        # CSS variables for theming
```

### Using components

```tsx
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'

export function ProductCard({ product }: { product: Product }) {
  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>{product.name}</CardTitle>
        <CardDescription>{product.description}</CardDescription>
      </CardHeader>
      <CardContent className="flex items-center justify-between">
        <span className="text-2xl font-bold">${product.price}</span>
        <Badge variant="secondary">{product.category}</Badge>
        <Button>Add to cart</Button>
      </CardContent>
    </Card>
  )
}
```

### Customising component variants

```typescript
// components/ui/button.tsx — add a new variant
import { cva } from 'class-variance-authority'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
        // ─── Custom variants ──────────────────────────────────────────
        success: 'bg-green-600 text-white hover:bg-green-700',
        warning: 'bg-yellow-500 text-white hover:bg-yellow-600',
        brand: 'bg-orange-500 text-white hover:bg-orange-600 shadow-[3px_3px_0_#0a0a0a] border-2 border-black',
      },
      size: {
        default: 'h-9 px-4 py-2',
        sm: 'h-8 px-3 text-xs',
        lg: 'h-10 px-8',
        xl: 'h-12 px-10 text-base',   // custom size
        icon: 'h-9 w-9',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
)

// Usage
<Button variant="brand" size="xl">Get Started</Button>
<Button variant="success">Confirm</Button>
```

### Theming with CSS variables

```css
/* app/globals.css */
@layer base {
  :root {
    /* Override defaults to match your brand */
    --background: 0 0% 100%;
    --foreground: 224 71.4% 4.1%;
    --primary: 220.9 39.3% 11%;       /* change this for brand color */
    --primary-foreground: 210 20% 98%;
    --accent: 220 14.3% 95.9%;
    --accent-foreground: 220.9 39.3% 11%;
    --border: 220 13% 91%;
    --radius: 0.5rem;                  /* border-radius scale */
  }

  /* Orange brand theme */
  :root[data-theme="orange"] {
    --primary: 24.6 95% 53.1%;         /* orange-500 */
    --primary-foreground: 60 9.1% 97.8%;
    --accent: 24.6 95% 95%;
    --ring: 24.6 95% 53.1%;
  }

  .dark {
    --background: 224 71.4% 4.1%;
    --foreground: 210 20% 98%;
    --primary: 210 20% 98%;
    --primary-foreground: 220.9 39.3% 11%;
  }
}
```

### Form with react-hook-form integration

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'

const formSchema = z.object({
  email:    z.string().email('Enter a valid email'),
  password: z.string().min(8, 'Minimum 8 characters'),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: '', password: '' },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    await signIn(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input placeholder="you@example.com" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <FormField control={form.control} name="password" render={({ field }) => (
          <FormItem>
            <FormLabel>Password</FormLabel>
            <FormControl><Input type="password" {...field} /></FormControl>
            <FormDescription>Must be at least 8 characters.</FormDescription>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit" className="w-full" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Signing in...' : 'Sign in'}
        </Button>
      </form>
    </Form>
  )
}
```

### Dialog pattern

```tsx
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

export function DeleteDialog({ onConfirm }: { onConfirm: () => void }) {
  const [open, setOpen] = useState(false)

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="destructive" size="sm">Delete</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you sure?</DialogTitle>
          <DialogDescription>This action cannot be undone.</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="destructive" onClick={() => { onConfirm(); setOpen(false) }}>Delete</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

### Data table with TanStack Table

```tsx
import { DataTable } from '@/components/ui/data-table'
import { ColumnDef } from '@tanstack/react-table'

const columns: ColumnDef<User>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'email', header: 'Email' },
  {
    accessorKey: 'role',
    header: 'Role',
    cell: ({ row }) => <Badge>{row.getValue('role')}</Badge>,
  },
  {
    id: 'actions',
    cell: ({ row }) => (
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon"><MoreHorizontal /></Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem onClick={() => editUser(row.original)}>Edit</DropdownMenuItem>
          <DropdownMenuItem className="text-red-600" onClick={() => deleteUser(row.original.id)}>Delete</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    ),
  },
]

<DataTable columns={columns} data={users} />
```

## Example

**User:** Build a settings page with a profile form (name, email, avatar upload), a danger zone card with a delete account dialog, and a theme toggle.

**Expected output:**
- `app/settings/page.tsx` — layout with sections
- `components/profile-form.tsx` — shadcn Form + Input + Avatar + Button
- `components/delete-account-dialog.tsx` — Dialog with confirmation input
- `components/theme-toggle.tsx` — Button toggling dark/light via next-themes

---
