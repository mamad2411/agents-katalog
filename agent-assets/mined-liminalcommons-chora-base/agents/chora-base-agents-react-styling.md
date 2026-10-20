---
sap_id: SAP-024
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-200"   # Quick Start + Core Workflows
  phase_2: "lines 201-400" # Advanced Workflows
  phase_3: "full"          # Complete including best practices and pitfalls
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 12000
---

## 📖 Quick Reference

**New to SAP-024?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Install Tailwind CSS v4
- 📚 **Time Savings** - 87% reduction
- 🎯 **Feature 1** - Core feature 1
- 🔧 **Feature 2** - Core feature 2
- 📊 **Feature 3** - Core feature 3
- 🔗 **Integration** - Works with SAP-020 (Foundation)

This AGENTS.md provides: Agent-specific patterns for implementing SAP-024.
s.

---

# React Styling Architecture (SAP-024) - Agent Awareness

**SAP ID**: SAP-024
**Agent Compatibility**: All AI agents with command execution and file operations
**Last Updated**: 2025-11-05

---

## Quick Start for Agents

This SAP provides workflows for **React styling** using Tailwind CSS v4, shadcn/ui, and CVA.

### First-Time Session

1. **Choose project type**: Next.js 15 or Vite 7
2. **Install Tailwind CSS v4**: CSS-first configuration with @theme directive
3. **Add shadcn/ui**: Copy-paste component library built on Radix UI
4. **Setup dark mode**: next-themes with SSR support

### Key Technology Stack

- **Tailwind CSS v4**: CSS-first, OKLCH colors, zero runtime overhead
- **shadcn/ui**: Copy-paste components (not npm package)
- **CVA**: Class Variance Authority for type-safe variants
- **next-themes**: Dark mode with SSR support
- **Radix UI**: Accessible primitives (WCAG 2.2 Level AA)

---

## User Signal Pattern Tables

### Table 1: Styling Setup Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Install Tailwind** | "Setup Tailwind CSS", "Add Tailwind v4", "Install styling" | Execute Workflow 1: Install Tailwind CSS v4 | Tailwind CSS v4 installed with CSS-first config |
| **Add shadcn/ui** | "Install shadcn", "Add shadcn/ui", "Setup component library" | Execute Workflow 2: Setup shadcn/ui | shadcn/ui CLI configured, ready to add components |
| **Setup dark mode** | "Add dark mode", "Theme toggle", "Dark theme support" | Execute Workflow 3: Setup Dark Mode | next-themes installed, ThemeProvider configured |
| **Add shadcn component** | "Add Button component", "Install shadcn Card" | Execute Workflow 4: Add shadcn/ui Component | Component copied to src/components/ui |
| **Create variant component** | "Button with variants", "Styled component with CVA" | Execute Workflow 5: Create Component with CVA | Component with type-safe variants using CVA |

### Table 2: Styling Operation Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Apply utility classes** | "Style with Tailwind", "Add padding", "Center div" | Use Tailwind utilities | Tailwind classes applied (px-4, flex, etc.) |
| **Toggle theme** | "Switch to dark mode", "Toggle theme", "Change theme" | Use theme toggle component | Theme toggled between light/dark |
| **Create variant** | "Button primary variant", "Add size variants" | Use CVA to create variants | Type-safe variant props |
| **Make responsive** | "Mobile responsive", "Responsive layout", "Breakpoints" | Use responsive utilities | Responsive classes applied (sm:, md:, lg:) |
| **Add custom color** | "Brand color", "Custom color scheme" | Update @theme in globals.css | Custom colors available as utilities |

---

## Workflow 1: Install Tailwind CSS v4 for Next.js 15 (10-15 minutes)

**When to use**: Setting up Tailwind CSS v4 in Next.js 15 project

**Prerequisites**:
- Next.js 15 project initialized (SAP-020)
- Node.js 18+ and pnpm/npm installed

**Steps**:

1. **Install Tailwind CSS v4**:
   ```bash
   pnpm add tailwindcss@next @tailwindcss/postcss@next
   ```

2. **Create PostCSS configuration** (`postcss.config.mjs`):
   ```javascript
   /** @type {import('postcss-load-config').Config} */
   const config = {
     plugins: {
       '@tailwindcss/postcss': {},
     },
   }

   export default config
   ```

3. **Create global stylesheet** (`app/globals.css`):
   ```css
   @import "tailwindcss";

   @theme {
     --color-primary: oklch(0.6 0.2 250);
     --color-secondary: oklch(0.4 0.15 200);
     --color-accent: oklch(0.7 0.25 150);

     --font-sans: system-ui, sans-serif;
     --font-mono: 'Fira Code', monospace;

     --spacing-xs: 0.25rem;
     --spacing-sm: 0.5rem;
     --spacing-md: 1rem;
     --spacing-lg: 1.5rem;
     --spacing-xl: 2rem;
   }

   @layer base {
     body {
       @apply bg-background text-foreground;
     }
   }
   ```

4. **Import global styles in layout** (`app/layout.tsx`):
   ```typescript
   import './globals.css'

   export default function RootLayout({ children }: { children: React.ReactNode }) {
     return (
       <html lang="en">
         <body>{children}</body>
       </html>
     )
   }
   ```

5. **Test Tailwind installation**:
   ```bash
   pnpm dev
   ```

   Create test page (`app/page.tsx`):
   ```typescript
   export default function Home() {
     return (
       <div className="flex items-center justify-center min-h-screen bg-primary text-white">
         <h1 className="text-4xl font-bold">Tailwind CSS v4 Works!</h1>
       </div>
     )
   }
   ```

**Expected outcome**:
- Tailwind CSS v4 installed with CSS-first configuration
- @theme directive for design tokens (OKLCH colors, spacing, fonts)
- Zero-runtime overhead (all CSS generated at build time)
- Ready to use Tailwind utilities

**Time saved**: 1-2 hours (manual setup) → 10-15 minutes (template-based)

---

## Workflow 2: Setup shadcn/ui Component Library (10-20 minutes)

**When to use**: Adding accessible, customizable UI components

**Prerequisites**:
- Tailwind CSS v4 installed (Workflow 1)

**Steps**:

1. **Install shadcn/ui dependencies**:
   ```bash
   pnpm add class-variance-authority clsx tailwind-merge
   pnpm add @radix-ui/react-slot
   ```

2. **Create cn utility** (`lib/utils.ts`):
   ```typescript
   import { clsx, type ClassValue } from 'clsx'
   import { twMerge } from 'tailwind-merge'

   export function cn(...inputs: ClassValue[]) {
     return twMerge(clsx(inputs))
   }
   ```

3. **Initialize shadcn/ui CLI**:
   ```bash
   pnpm dlx shadcn@latest init
   ```

   Answer prompts:
   - Would you like to use TypeScript? **Yes**
   - Which style would you like to use? **New York**
   - Which color would you like to use as base color? **Zinc**
   - Where is your global CSS file? **app/globals.css**
   - Would you like to use CSS variables for colors? **Yes**
   - Where is your tailwind.config.js located? **tailwind.config.ts**
   - Configure the import alias for components? **@/components**
   - Configure the import alias for utils? **@/lib/utils**

4. **Verify components.json created**:
   ```json
   {
     "style": "new-york",
     "tailwind": {
       "config": "tailwind.config.ts",
       "css": "app/globals.css",
       "baseColor": "zinc",
       "cssVariables": true
     },
     "aliases": {
       "components": "@/components",
       "utils": "@/lib/utils"
     }
   }
   ```

5. **Add first component (Button)**:
   ```bash
   pnpm dlx shadcn@latest add button
   ```

   This creates `components/ui/button.tsx` with:
   - Radix UI primitives for accessibility
   - CVA for type-safe variants
   - Tailwind utilities for styling

6. **Test Button component**:
   ```typescript
   import { Button } from '@/components/ui/button'

   export default function Home() {
     return (
       <div className="p-8">
         <Button>Click me</Button>
         <Button variant="secondary">Secondary</Button>
         <Button variant="destructive">Delete</Button>
         <Button variant="outline">Outline</Button>
       </div>
     )
   }
   ```

**Expected outcome**:
- shadcn/ui CLI configured
- cn utility for className merging
- Button component installed and working
- Ready to add more shadcn/ui components

**Time saved**: 1-2 hours (manual component setup) → 10-20 minutes (CLI-based)

---

## Workflow 3: Setup Dark Mode with next-themes (10-15 minutes)

**When to use**: Adding dark mode support with SSR compatibility

**Prerequisites**:
- Tailwind CSS v4 installed (Workflow 1)

**Steps**:

1. **Install next-themes**:
   ```bash
   pnpm add next-themes@^0.4.4
   ```

2. **Create ThemeProvider component** (`components/providers/theme-provider.tsx`):
   ```typescript
   'use client'

   import { ThemeProvider as NextThemesProvider } from 'next-themes'
   import type { ThemeProviderProps } from 'next-themes'

   export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
     return <NextThemesProvider {...props}>{children}</NextThemesProvider>
   }
   ```

3. **Wrap app with ThemeProvider** (`app/layout.tsx`):
   ```typescript
   import { ThemeProvider } from '@/components/providers/theme-provider'
   import './globals.css'

   export default function RootLayout({ children }: { children: React.ReactNode }) {
     return (
       <html lang="en" suppressHydrationWarning>
         <body>
           <ThemeProvider
             attribute="class"
             defaultTheme="system"
             enableSystem
             disableTransitionOnChange
           >
             {children}
           </ThemeProvider>
         </body>
       </html>
     )
   }
   ```

4. **Create ThemeToggle component** (`components/theme-toggle.tsx`):
   ```typescript
   'use client'

   import { useTheme } from 'next-themes'
   import { Button } from '@/components/ui/button'

   export function ThemeToggle() {
     const { theme, setTheme } = useTheme()

     return (
       <Button
         variant="outline"
         size="icon"
         onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
       >
         <span className="sr-only">Toggle theme</span>
         {theme === 'dark' ? '☀️' : '🌙'}
       </Button>
     )
   }
   ```

5. **Update globals.css for dark mode variables**:
   ```css
   @theme {
     --color-background: oklch(1 0 0);
     --color-foreground: oklch(0.1 0 0);
   }

   @media (prefers-color-scheme: dark) {
     @theme {
       --color-background: oklch(0.1 0 0);
       --color-foreground: oklch(0.98 0 0);
     }
   }

   .dark {
     @theme {
       --color-background: oklch(0.1 0 0);
       --color-foreground: oklch(0.98 0 0);
     }
   }
   ```

6. **Test dark mode**:
   ```bash
   pnpm dev
   ```

   Add ThemeToggle to page:
   ```typescript
   import { ThemeToggle } from '@/components/theme-toggle'

   export default function Home() {
     return (
       <div className="p-8">
         <ThemeToggle />
         <p className="mt-4 text-foreground">Theme should toggle!</p>
       </div>
     )
   }
   ```

**Expected outcome**:
- Dark mode working with theme toggle
- SSR-safe (no flash of unstyled content)
- System theme detection
- Persistent theme selection (localStorage)

**Time saved**: 30 minutes-1 hour (manual setup) → 10-15 minutes (template-based)

---

## Workflow 4: Add shadcn/ui Component (2-5 minutes per component)

**When to use**: Adding pre-built accessible components (Card, Dialog, Input, etc.)

**Prerequisites**:
- shadcn/ui CLI configured (Workflow 2)

**Steps**:

1. **Browse available components**:
   ```bash
   pnpm dlx shadcn@latest add
   ```

   Or visit: https://ui.shadcn.com/docs/components

2. **Add specific component**:
   ```bash
   # Add Card component
   pnpm dlx shadcn@latest add card

   # Add Input component
   pnpm dlx shadcn@latest add input

   # Add Dialog component
   pnpm dlx shadcn@latest add dialog

   # Add Label component
   pnpm dlx shadcn@latest add label
   ```

3. **Use component in page**:
   ```typescript
   import {
     Card,
     CardContent,
     CardDescription,
     CardHeader,
     CardTitle,
   } from '@/components/ui/card'
   import { Input } from '@/components/ui/input'
   import { Label } from '@/components/ui/label'

   export default function Home() {
     return (
       <div className="p-8">
         <Card className="w-full max-w-md">
           <CardHeader>
             <CardTitle>Login</CardTitle>
             <CardDescription>Enter your credentials</CardDescription>
           </CardHeader>
           <CardContent>
             <div className="space-y-4">
               <div>
                 <Label htmlFor="email">Email</Label>
                 <Input id="email" type="email" placeholder="you@example.com" />
               </div>
               <div>
                 <Label htmlFor="password">Password</Label>
                 <Input id="password" type="password" />
               </div>
             </div>
           </CardContent>
         </Card>
       </div>
     )
   }
   ```

**Expected outcome**:
- Component copied to `src/components/ui/`
- Accessible (WCAG 2.2 Level AA via Radix UI)
- Customizable with Tailwind classes
- Type-safe props with TypeScript

**Time saved**: 20-30 minutes (manual component creation) → 2-5 minutes (CLI-based)

---

## Workflow 5: Create Component with CVA Variants (15-20 minutes)

**When to use**: Creating custom components with type-safe variants

**Prerequisites**:
- CVA installed (from Workflow 2)

**Steps**:

1. **Create Badge component with CVA** (`components/ui/badge.tsx`):
   ```typescript
   import { cva, type VariantProps } from 'class-variance-authority'
   import { cn } from '@/lib/utils'

   const badgeVariants = cva(
     'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
     {
       variants: {
         variant: {
           default: 'bg-primary text-primary-foreground hover:bg-primary/80',
           secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
           destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/80',
           outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
         },
         size: {
           sm: 'px-2 py-0.5 text-xs',
           md: 'px-2.5 py-0.5 text-sm',
           lg: 'px-3 py-1 text-base',
         },
       },
       defaultVariants: {
         variant: 'default',
         size: 'md',
       },
     }
   )

   export interface BadgeProps
     extends React.HTMLAttributes<HTMLDivElement>,
       VariantProps<typeof badgeVariants> {}

   export function Badge({ className, variant, size, ...props }: BadgeProps) {
     return <div className={cn(badgeVariants({ variant, size }), className)} {...props} />
   }
   ```

2. **Use Badge component with variants**:
   ```typescript
   import { Badge } from '@/components/ui/badge'

   export default function Home() {
     return (
       <div className="p-8 space-y-4">
         <Badge>Default</Badge>
         <Badge variant="secondary">Secondary</Badge>
         <Badge variant="destructive">Destructive</Badge>
         <Badge variant="outline">Outline</Badge>

         <Badge size="sm">Small</Badge>
         <Badge size="md">Medium</Badge>
         <Badge size="lg">Large</Badge>
       </div>
     )
   }
   ```

**Expected outcome**:
- Type-safe variant props with TypeScript
- Automatic className merging with cn utility
- Composable variants (variant + size)
- IntelliSense support for variant options

**Time saved**: 1 hour (manual variant implementation) → 15-20 minutes (CVA pattern)

---

## Best Practices

### 1. Use @theme Directive for Design Tokens

**Pattern**:
```css
/* ✅ GOOD: Design tokens in @theme */
@theme {
  --color-primary: oklch(0.6 0.2 250);
  --spacing-md: 1rem;
  --font-sans: system-ui, sans-serif;
}

/* ❌ BAD: Hardcoded values in components */
.button {
  background: #3b82f6;
  padding: 1rem;
}
```

**Why**: @theme creates reusable utilities, single source of truth

---

### 2. Use OKLCH Color Space for Better Perceptual Uniformity

**Pattern**:
```css
/* ✅ GOOD: OKLCH colors */
@theme {
  --color-primary: oklch(0.6 0.2 250);  /* Lightness, Chroma, Hue */
}

/* ❌ BAD: HSL colors */
--color-primary: hsl(250, 80%, 60%);  /* Less perceptually uniform */
```

**Why**: OKLCH provides consistent perceived brightness across hues

---

### 3. Use shadcn/ui for Accessibility Foundation

**Pattern**:
```typescript
// ✅ GOOD: shadcn/ui component (built on Radix UI)
import { Dialog } from '@/components/ui/dialog'

// ❌ BAD: Custom dialog without accessibility
<div className="modal">  // Missing ARIA attributes, focus trap, etc.
```

**Why**: shadcn/ui components have WCAG 2.2 Level AA accessibility built-in

---

### 4. Use CVA for Type-Safe Variants

**Pattern**:
```typescript
// ✅ GOOD: CVA for type-safe variants
const buttonVariants = cva('base-classes', {
  variants: {
    variant: { primary: 'bg-primary', secondary: 'bg-secondary' },
  },
})

// ❌ BAD: String concatenation
const className = variant === 'primary' ? 'bg-primary' : 'bg-secondary'
```

**Why**: CVA provides TypeScript inference and composable variants

---

### 5. Use next-themes for SSR-Safe Dark Mode

**Pattern**:
```typescript
// ✅ GOOD: next-themes with suppressHydrationWarning
<html lang="en" suppressHydrationWarning>
  <ThemeProvider attribute="class" defaultTheme="system">

// ❌ BAD: Direct theme in localStorage (flash on load)
const [theme, setTheme] = useState(() => localStorage.getItem('theme'))
```

**Why**: next-themes prevents flash of unstyled content on SSR

---

## Common Pitfalls

### Pitfall 1: Forgetting suppressHydrationWarning on <html>

**Problem**: Flash of unstyled content on dark mode

**Fix**: Add suppressHydrationWarning
```typescript
// ❌ BAD: No suppressHydrationWarning
<html lang="en">

// ✅ GOOD: Prevent hydration warning
<html lang="en" suppressHydrationWarning>
```

**Why**: Theme applied via JS after hydration, causes mismatch warning

---

### Pitfall 2: Not Installing @tailwindcss/postcss for Tailwind v4

**Problem**: Tailwind v4 CSS not processed

**Fix**: Install correct PostCSS plugin
```bash
# ❌ BAD: Old plugin
pnpm add tailwindcss autoprefixer

# ✅ GOOD: Tailwind v4 PostCSS plugin
pnpm add tailwindcss@next @tailwindcss/postcss@next
```

**Why**: Tailwind v4 requires new @tailwindcss/postcss plugin

---

### Pitfall 3: Using HSL Instead of OKLCH for Colors

**Problem**: Inconsistent perceived brightness across hues

**Fix**: Use OKLCH color space
```css
/* ❌ BAD: HSL (blue looks brighter than red at same lightness) */
--color-red: hsl(0, 80%, 60%);
--color-blue: hsl(240, 80%, 60%);

/* ✅ GOOD: OKLCH (consistent perceived brightness) */
--color-red: oklch(0.6 0.2 0);
--color-blue: oklch(0.6 0.2 240);
```

**Why**: OKLCH provides perceptually uniform colors

---

### Pitfall 4: Not Using cn Utility for className Merging

**Problem**: Conflicting Tailwind classes (last one wins)

**Fix**: Use cn utility from shadcn/ui
```typescript
// ❌ BAD: String concatenation (conflicts)
<div className={`p-4 ${className}`} />  // p-4 might be overridden

// ✅ GOOD: cn utility (proper merging)
<div className={cn('p-4', className)} />  // Correctly merges/overrides
```

**Why**: cn uses tailwind-merge to intelligently merge classes

---

### Pitfall 5: Installing shadcn/ui as npm Package

**Problem**: Trying to install shadcn/ui via npm install

**Fix**: Use shadcn CLI to copy components
```bash
# ❌ BAD: shadcn/ui is not an npm package
pnpm add shadcn/ui

# ✅ GOOD: Use CLI to copy components
pnpm dlx shadcn@latest add button
```

**Why**: shadcn/ui is copy-paste library, not npm package

---

## Support & Resources

**SAP-024 Documentation**:
- [Capability Charter](capability-charter.md) - React styling problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts for Tailwind v4, shadcn/ui, CVA
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs)
- [shadcn/ui Docs](https://ui.shadcn.com)
- [CVA Docs](https://cva.style/docs)
- [next-themes Docs](https://github.com/pacocoursey/next-themes)
- [Radix UI Docs](https://www.radix-ui.com)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-022 (react-linting)](../react-linting/) - Linting and formatting
- [SAP-023 (react-state-management)](../react-state-management/) - State patterns
- [SAP-025 (react-performance)](../react-performance/) - Performance optimization

---

## Version History

- **1.0.0** (2025-11-05): Initial AGENTS.md for SAP-024
  - 5 workflows: Install Tailwind CSS v4, Setup shadcn/ui, Setup Dark Mode, Add shadcn/ui Component, Create Component with CVA Variants
  - 2 user signal pattern tables: Styling Setup Signals, Styling Operation Signals
  - 5 best practices: @theme directive, OKLCH colors, shadcn/ui for accessibility, CVA for variants, next-themes for dark mode
  - 5 common pitfalls: Missing suppressHydrationWarning, wrong PostCSS plugin, HSL instead of OKLCH, not using cn utility, installing shadcn as package
  - Focus on Tailwind v4 CSS-first configuration and shadcn/ui integration

---

**Next Steps**:
1. Review [protocol-spec.md](protocol-spec.md) for technical contracts
2. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
3. Install: `pnpm add tailwindcss@next @tailwindcss/postcss@next next-themes class-variance-authority clsx tailwind-merge`
4. Run: `pnpm dlx shadcn@latest init`
