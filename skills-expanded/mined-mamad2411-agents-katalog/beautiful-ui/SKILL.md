---
name: beautiful-ui
description: Build stunning glassmorphism dark-mode interfaces with Next.js and Tailwind CSS v4. Use when creating any frontend UI, component, page, or application. Specializes in glass-like translucent surfaces, luminous color palettes on dark backgrounds, fluid animations with Framer Motion, and premium visual polish. Always generates dark-mode-first, glassmorphic, production-grade code with exceptional aesthetic quality.
---

# Beautiful UI

Build premium glassmorphism interfaces — dark-mode-first, with luminous glass surfaces, fluid animations, and meticulous visual polish using Next.js + Tailwind CSS v4.

## Design DNA

Every interface follows these non-negotiable principles:

1. **Dark mode is the default** — design for dark first, light is optional
2. **Glass is the primary surface** — translucent layers with backdrop-blur over rich backgrounds
3. **Light is a material** — use glows, gradients, and luminance to create depth
4. **Motion is intentional** — every animation serves hierarchy, feedback, or delight
5. **Typography is bold** — distinctive fonts, never generic (no Inter, Roboto, Arial)

## Tailwind v4 Dark Glass Theme

```css
@import "tailwindcss";

@theme {
  /* Dark-first color system using OKLCH */
  --color-background: oklch(10% 0.015 270);
  --color-surface: oklch(14% 0.01 270);
  --color-elevated: oklch(18% 0.012 270);

  --color-foreground: oklch(95% 0.005 270);
  --color-foreground-muted: oklch(65% 0.01 270);
  --color-foreground-subtle: oklch(45% 0.01 270);

  /* Glass surface tokens */
  --color-glass: oklch(100% 0 0 / 0.06);
  --color-glass-hover: oklch(100% 0 0 / 0.1);
  --color-glass-active: oklch(100% 0 0 / 0.14);
  --color-glass-border: oklch(100% 0 0 / 0.12);
  --color-glass-border-hover: oklch(100% 0 0 / 0.2);

  /* Accent — a vibrant hue that glows on dark surfaces */
  --color-accent: oklch(72% 0.19 250);
  --color-accent-hover: oklch(78% 0.17 250);
  --color-accent-muted: oklch(72% 0.19 250 / 0.15);
  --color-accent-foreground: oklch(98% 0.005 270);

  /* Status colors (muted to match dark glass aesthetic) */
  --color-success: oklch(72% 0.17 155);
  --color-warning: oklch(78% 0.15 75);
  --color-destructive: oklch(65% 0.2 25);

  --color-border: oklch(100% 0 0 / 0.08);
  --color-ring: oklch(72% 0.19 250 / 0.5);

  /* Radius — generous for glass surfaces */
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.25rem;
  --radius-2xl: 1.5rem;

  /* Glass-specific animations */
  --animate-glass-in: glass-in 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  --animate-glow-pulse: glow-pulse 3s ease-in-out infinite;
  --animate-fade-up: fade-up 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  --animate-scale-in: scale-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  --animate-shimmer: shimmer 2.5s linear infinite;
  --animate-float: float 6s ease-in-out infinite;

  @keyframes glass-in {
    from { opacity: 0; backdrop-filter: blur(0px); transform: translateY(8px) scale(0.98); }
    to { opacity: 1; backdrop-filter: blur(16px); transform: translateY(0) scale(1); }
  }

  @keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 20px oklch(72% 0.19 250 / 0.15); }
    50% { box-shadow: 0 0 40px oklch(72% 0.19 250 / 0.3); }
  }

  @keyframes fade-up {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @keyframes scale-in {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
  }

  @keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
  }

  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
  }
}

/* Base layer */
@layer base {
  * { @apply border-border; }
  body {
    @apply bg-background text-foreground antialiased;
    font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  }
}

/* Glass utility classes */
@utility glass {
  @apply bg-glass backdrop-blur-xl border border-glass-border;
}

@utility glass-hover {
  @apply hover:bg-glass-hover hover:border-glass-border-hover transition-all duration-200;
}

@utility glass-strong {
  @apply bg-glass backdrop-blur-2xl backdrop-saturate-150 border border-glass-border;
}

@utility glow {
  box-shadow: 0 0 20px oklch(72% 0.19 250 / 0.15),
              0 0 60px oklch(72% 0.19 250 / 0.05);
}

@utility glow-border {
  box-shadow: inset 0 0.5px 0 0 oklch(100% 0 0 / 0.15),
              0 0 20px oklch(72% 0.19 250 / 0.1);
}

@utility text-glow {
  text-shadow: 0 0 30px oklch(72% 0.19 250 / 0.5);
}

@utility noise {
  position: relative;
}
/* Apply noise::after with a tiny noise SVG for texture */
```

## Glass Component Patterns

### Glass Card (Primary Surface)

```tsx
import { cn } from "@/lib/utils";

export function GlassCard({
  children,
  className,
  glow = false,
  ...props
}: React.HTMLAttributes<HTMLDivElement> & { glow?: boolean }) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-2xl",
        "bg-white/[0.06] backdrop-blur-xl backdrop-saturate-150",
        "border border-white/[0.12]",
        "shadow-[0_8px_32px_rgba(0,0,0,0.4)]",
        glow && "shadow-[0_0_30px_oklch(72%_0.19_250/0.12)]",
        className
      )}
      {...props}
    >
      {/* Top highlight — simulates light hitting glass edge */}
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/25 to-transparent" />
      <div className="relative z-10">{children}</div>
    </div>
  );
}
```

### Glass Button

```tsx
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const glassButtonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-xl font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-40",
  {
    variants: {
      variant: {
        default:
          "bg-white/[0.08] backdrop-blur-lg border border-white/[0.12] text-foreground hover:bg-white/[0.14] hover:border-white/[0.2] active:bg-white/[0.18]",
        accent:
          "bg-accent text-accent-foreground hover:bg-accent-hover shadow-[0_0_20px_oklch(72%_0.19_250/0.25)] hover:shadow-[0_0_30px_oklch(72%_0.19_250/0.35)]",
        ghost:
          "text-foreground-muted hover:text-foreground hover:bg-white/[0.06]",
        outline:
          "border border-white/[0.15] text-foreground hover:bg-white/[0.06] hover:border-white/[0.25]",
      },
      size: {
        sm: "h-9 px-3.5 text-sm",
        default: "h-11 px-5 text-sm",
        lg: "h-12 px-8 text-base",
        icon: "size-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
);

export function GlassButton({
  className,
  variant,
  size,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof glassButtonVariants>) {
  return (
    <button
      className={cn(glassButtonVariants({ variant, size, className }))}
      {...props}
    />
  );
}
```

### Glass Input

```tsx
export function GlassInput({
  className,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        "flex h-11 w-full rounded-xl px-4 text-sm",
        "bg-white/[0.06] backdrop-blur-lg",
        "border border-white/[0.1]",
        "text-foreground placeholder:text-foreground-subtle",
        "focus:outline-none focus:border-white/[0.25] focus:bg-white/[0.1]",
        "focus:ring-2 focus:ring-accent/30",
        "transition-all duration-200",
        className
      )}
      {...props}
    />
  );
}
```

## Background Patterns

Every glassmorphism UI needs a rich background. Use one per page:

### Mesh Gradient Background

```tsx
export function MeshBackground() {
  return (
    <div className="fixed inset-0 -z-10 bg-background">
      {/* Primary gradient orb */}
      <div className="absolute top-[-20%] left-[-10%] h-[600px] w-[600px] rounded-full bg-[oklch(45%_0.15_270)] opacity-30 blur-[120px]" />
      {/* Secondary orb */}
      <div className="absolute bottom-[-10%] right-[-5%] h-[500px] w-[500px] rounded-full bg-[oklch(50%_0.18_200)] opacity-20 blur-[100px]" />
      {/* Accent orb */}
      <div className="absolute top-[40%] right-[20%] h-[300px] w-[300px] rounded-full bg-[oklch(60%_0.2_320)] opacity-15 blur-[80px]" />
      {/* Subtle noise texture */}
      <div className="absolute inset-0 opacity-[0.03]" style={{ backgroundImage: "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")" }} />
    </div>
  );
}
```

### Dot Grid Background

```tsx
export function DotGridBackground() {
  return (
    <div className="fixed inset-0 -z-10 bg-background">
      <div
        className="absolute inset-0 opacity-[0.15]"
        style={{
          backgroundImage: "radial-gradient(oklch(100% 0 0 / 0.3) 1px, transparent 1px)",
          backgroundSize: "24px 24px",
        }}
      />
      {/* Radial fade so dots don't tile harshly */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_0%,var(--color-background)_70%)]" />
    </div>
  );
}
```

## Animation Patterns

Use Framer Motion for orchestrated animations. CSS for simple hover/transitions.

### Staggered Glass Cards

```tsx
import { motion } from "framer-motion";

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.08 } },
};

const item = {
  hidden: { opacity: 0, y: 20, filter: "blur(4px)" },
  show: {
    opacity: 1, y: 0, filter: "blur(0px)",
    transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] },
  },
};

export function CardGrid({ cards }: { cards: CardData[] }) {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
    >
      {cards.map((card) => (
        <motion.div key={card.id} variants={item}>
          <GlassCard className="p-6">
            {/* card content */}
          </GlassCard>
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### Interactive Glass Hover

```tsx
<motion.div
  whileHover={{
    scale: 1.02,
    boxShadow: "0 0 30px oklch(72% 0.19 250 / 0.2)",
  }}
  whileTap={{ scale: 0.98 }}
  transition={{ type: "spring", stiffness: 400, damping: 25 }}
  className="glass rounded-2xl p-6 cursor-pointer"
>
  {children}
</motion.div>
```

## Motion Spec

| Interaction | Duration | Easing |
|-------------|----------|--------|
| Hover state | 150ms | `ease-out` |
| Button press | 100ms | `ease-out` |
| Card entrance | 400-500ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Modal open | 300ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Page transition | 400ms | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Stagger delay | 60-100ms | — |
| Glow pulse | 3s | `ease-in-out` (infinite) |
| Float | 6s | `ease-in-out` (infinite) |

**Spring config for interactive elements:** `{ stiffness: 400, damping: 25, mass: 0.8 }`

**Performance rules:**
- Only animate `transform`, `opacity`, `filter`, `box-shadow` (GPU-accelerated)
- Respect `prefers-reduced-motion` — disable all non-essential motion
- Keep UI interaction durations under 500ms

## Typography

Choose distinctive, characterful fonts. Pair a display font with a refined body font.

**Strong pairings for dark glass aesthetics:**
- **Space Age**: Orbitron (display) + DM Sans (body)
- **Editorial Glow**: Playfair Display (display) + Outfit (body)
- **Neo-Geometric**: Sora (display) + Plus Jakarta Sans (body)
- **Monospace Hacker**: JetBrains Mono (display) + Geist Sans (body)
- **Elegant Precision**: Cormorant Garamond (display) + Geist Sans (body)

**Next.js font loading:**
```tsx
import { Sora, Plus_Jakarta_Sans } from "next/font/google";

const display = Sora({ subsets: ["latin"], variable: "--font-display" });
const body = Plus_Jakarta_Sans({ subsets: ["latin"], variable: "--font-body" });

// In layout.tsx body:
<body className={`${display.variable} ${body.variable} font-body`}>
```

```css
@theme inline {
  --font-display: var(--font-display), system-ui;
  --font-body: var(--font-body), system-ui;
}
```

**Scale (1.25 ratio):**
- `text-xs`: 0.64rem — captions, badges
- `text-sm`: 0.8rem — labels, metadata
- `text-base`: 1rem — body text
- `text-lg`: 1.25rem — subheadings
- `text-xl`: 1.563rem — section titles
- `text-2xl`: 1.953rem — page titles
- `text-3xl`: 2.441rem — hero (mobile)
- `text-4xl`: 3.052rem — hero (desktop)
- `text-5xl`: 3.815rem — display

Headlines: tight tracking (`-0.02em` to `-0.04em`), bold weight.
Body: default tracking, regular weight, `leading-relaxed`.

## Color Strategy

Dark glassmorphism thrives on **contrast between deep backgrounds and luminous accents**.

**Accent palette options** (swap `--color-accent` in the theme):
- **Electric Blue**: `oklch(72% 0.19 250)` — tech, modern, trustworthy
- **Violet Glow**: `oklch(68% 0.2 290)` — creative, premium
- **Cyan Neon**: `oklch(80% 0.16 195)` — futuristic, sharp
- **Emerald**: `oklch(72% 0.17 160)` — fresh, organic
- **Rose Gold**: `oklch(72% 0.14 15)` — warm, luxurious
- **Amber**: `oklch(80% 0.15 75)` — warm, energetic

**Rules:**
- One dominant accent per interface — secondary accents are desaturated or opacity-reduced
- Glass surfaces pick up ambient color from background gradient orbs
- Text on glass must pass WCAG AA (4.5:1) — use `text-foreground` not `text-foreground-subtle` for primary content
- Status colors (success/warning/destructive) are muted to not compete with accent

## Next.js Specifics

### Layout with Glass Shell

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={`${display.variable} ${body.variable} font-body antialiased`}>
        <MeshBackground />
        <div className="relative z-10 min-h-screen">
          <GlassNavbar />
          <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
```

### Glass Navbar

```tsx
export function GlassNavbar() {
  return (
    <nav className="sticky top-0 z-50 border-b border-white/[0.08] bg-background/60 backdrop-blur-xl backdrop-saturate-150">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo + nav items */}
      </div>
    </nav>
  );
}
```

### Page Transitions

```tsx
// components/page-transition.tsx
"use client";
import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from "next/navigation";

export function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0, y: 12, filter: "blur(4px)" }}
        animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        exit={{ opacity: 0, y: -8, filter: "blur(4px)" }}
        transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

## Quality Checklist

### Glass & Visual
- [ ] Background has gradient orbs or mesh — never flat solid
- [ ] Glass surfaces have `backdrop-blur-xl` + border + top highlight
- [ ] Accent color has a visible glow on hover/focus
- [ ] Noise/grain texture overlay at low opacity for depth
- [ ] No pure white or pure black surfaces — always tinted

### Animation
- [ ] Page load has staggered entrance animations
- [ ] Interactive elements have hover + active states with spring physics
- [ ] Modals/overlays animate in with scale + fade
- [ ] `prefers-reduced-motion` respected

### Typography
- [ ] Display font is distinctive (not Inter/Roboto/Arial)
- [ ] Headings have tight tracking, body has relaxed leading
- [ ] Font loaded via `next/font` with variable CSS

### Accessibility
- [ ] Text contrast >= 4.5:1 on glass surfaces (test with backdrop)
- [ ] Focus rings visible (use `ring-accent/50`)
- [ ] Touch targets >= 44px
- [ ] Keyboard navigation for all interactive elements
- [ ] Alt text on images, aria-labels on icon buttons

### Performance
- [ ] Animations use GPU properties only (transform, opacity, filter)
- [ ] Images use `next/image` with proper sizing
- [ ] Fonts preloaded, no layout shift
- [ ] `backdrop-blur` limited to visible elements (avoid stacking)

## References

For additional patterns, see:
- **references/glass-patterns.md** — Advanced glassmorphism component recipes
- **references/animation-recipes.md** — Framer Motion orchestration patterns
