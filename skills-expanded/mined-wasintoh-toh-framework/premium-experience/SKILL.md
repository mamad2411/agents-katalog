---
name: premium-experience
version: 1.0.0
description: >
  Premium app generation that creates WOW-factor experiences. Multi-page apps
  with smooth animations, zero TypeScript errors, and production-ready quality.
  Lovable-style experience: one prompt, complete app, instant delight.
  MUST be used alongside vibe-orchestrator for new projects.
triggers:
  - /toh-vibe (new projects)
  - /toh (complex app requests)
  - Any "create app" request
---

# Premium Experience Skill

> **"One prompt. Complete app. Instant WOW."**

Transform any idea into a premium, production-ready application with multiple pages,
smooth animations, and zero errors - all in a single prompt.

---

## 🎯 Core Philosophy

```
PREMIUM = COMPLETE + POLISHED + DELIGHTFUL

User says: "Create expense tracker"

❌ Basic output:
   - 1 page
   - No animations
   - Basic styling
   - "Add more pages later"

✅ Premium output:
   - 5+ pages (Dashboard, Transactions, Reports, Settings, Auth)
   - Smooth page transitions
   - Micro-interactions everywhere
   - Loading skeletons
   - Empty states designed
   - Ready to use immediately
```

---

## 📱 Multi-Page Generation (MANDATORY!)

### Minimum Page Set by App Type

Every new project MUST generate these pages based on app type:

```yaml
saas-app:
  required_pages:
    - "/" (Landing/Marketing page)
    - "/dashboard" (Main dashboard)
    - "/[feature]" (Core feature page)
    - "/settings" (User settings)
    - "/auth/login" (Authentication)
  optional_pages:
    - "/auth/register"
    - "/auth/forgot-password"
    - "/profile"
    - "/pricing"
    - "/help"

ecommerce:
  required_pages:
    - "/" (Homepage with hero + featured)
    - "/products" (Product listing)
    - "/products/[id]" (Product detail)
    - "/cart" (Shopping cart)
    - "/checkout" (Checkout flow)
  optional_pages:
    - "/auth/login"
    - "/orders"
    - "/wishlist"
    - "/search"

ai-chatbot:
  required_pages:
    - "/" (Landing page)
    - "/chat" (Main chat interface)
    - "/chat/[id]" (Chat history)
    - "/settings" (Preferences)
    - "/auth/login"
  optional_pages:
    - "/prompts" (Saved prompts)
    - "/history"

food-restaurant:
  required_pages:
    - "/" (Homepage with hero)
    - "/menu" (Full menu)
    - "/menu/[category]" (Category view)
    - "/cart" (Order cart)
    - "/checkout" (Order placement)
  optional_pages:
    - "/orders" (Order tracking)
    - "/locations"
    - "/about"

education:
  required_pages:
    - "/" (Landing page)
    - "/courses" (Course listing)
    - "/courses/[id]" (Course detail)
    - "/learn/[id]" (Learning interface)
    - "/dashboard" (Progress dashboard)
  optional_pages:
    - "/certificates"
    - "/profile"
    - "/leaderboard"

generic:
  required_pages:
    - "/" (Landing/Home)
    - "/dashboard" (Main interface)
    - "/[main-feature]" (Primary feature)
    - "/settings" (Settings)
    - "/auth/login" (Authentication)
```

### Page Generation Order

```
1. LAYOUT FIRST
   └── app/layout.tsx (with providers, fonts, metadata)
   └── components/layout/Navbar.tsx
   └── components/layout/Sidebar.tsx (if dashboard-style)
   └── components/layout/Footer.tsx (if marketing pages)

2. SHARED COMPONENTS
   └── components/ui/ (shadcn components)
   └── components/shared/ (app-specific shared)

3. FEATURE COMPONENTS
   └── components/features/[feature]/ (feature-specific)

4. PAGES (parallel if possible)
   └── app/page.tsx
   └── app/dashboard/page.tsx
   └── app/[feature]/page.tsx
   └── ...etc

5. AUTH PAGES (last)
   └── app/auth/login/page.tsx
   └── app/auth/register/page.tsx
```

---

## ✨ Animation System (MANDATORY!)

### Required Animations

Every premium app MUST have these animations:

```typescript
// 1. PAGE TRANSITIONS
// Every page should fade in smoothly

// components/motion/PageTransition.tsx
"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

export function PageTransition({ children }: { children: ReactNode }) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
```

```typescript
// 2. STAGGERED LIST ANIMATIONS
// Lists should animate in one by one

// components/motion/StaggerContainer.tsx
"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export function StaggerContainer({ children }: { children: ReactNode }) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="show"
    >
      {children}
    </motion.div>
  );
}

export function StaggerItem({ children }: { children: ReactNode }) {
  return <motion.div variants={itemVariants}>{children}</motion.div>;
}
```

```typescript
// 3. CARD HOVER EFFECTS
// Cards should lift on hover

// Usage in any card component
<motion.div
  whileHover={{ y: -4, boxShadow: "0 10px 40px -10px rgba(0,0,0,0.2)" }}
  transition={{ duration: 0.2 }}
  className="..."
>
  {/* Card content */}
</motion.div>
```

```typescript
// 4. BUTTON PRESS EFFECTS
// Buttons should feel tactile

// Usage on buttons
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  className="..."
>
  {children}
</motion.button>
```

```typescript
// 5. NUMBER COUNTING ANIMATION
// Stats should count up

// components/motion/CountUp.tsx
"use client";

import { useEffect, useRef, useState } from "react";
import { useInView } from "framer-motion";

interface CountUpProps {
  end: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
}

export function CountUp({ end, duration = 2, prefix = "", suffix = "" }: CountUpProps) {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (!isInView) return;
    
    let startTime: number;
    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / (duration * 1000), 1);
      setCount(Math.floor(progress * end));
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [isInView, end, duration]);

  return <span ref={ref}>{prefix}{count.toLocaleString()}{suffix}</span>;
}
```

### Animation Timing Guidelines

```css
/* Standard timings */
--duration-fast: 150ms;      /* Micro-interactions */
--duration-normal: 200ms;    /* Button/hover states */
--duration-slow: 300ms;      /* Page transitions */
--duration-slower: 500ms;    /* Complex animations */

/* Easing functions — no spring/bounce (AVOID-LIST) */
--ease-out: cubic-bezier(0.33, 1, 0.68, 1);      /* Most animations */
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);   /* Symmetric motion */
```

### Animation Rules

```
DO:
✅ Use subtle animations (y: 20 max, scale: 1.02 max)
✅ Keep durations short (150-300ms)
✅ Use ease-out for most animations
✅ Animate on scroll (useInView)
✅ Stagger lists (100ms between items)

DON'T:
❌ Bounce animations (too playful)
❌ Long durations (>500ms feels slow)
❌ Large movements (y: 100+ is jarring)
❌ Animate everything (be selective)
❌ Block interaction during animation
```

---

## 🎨 Premium UI Components

### Required Shared Components

Every premium app MUST have these components:

```
components/
├── layout/
│   ├── Navbar.tsx           # Responsive navigation
│   ├── Sidebar.tsx          # Dashboard sidebar (if applicable)
│   ├── Footer.tsx           # Marketing footer (if applicable)
│   └── MobileMenu.tsx       # Mobile navigation drawer
│
├── motion/
│   ├── PageTransition.tsx   # Page fade-in
│   ├── StaggerContainer.tsx # List animations
│   ├── FadeIn.tsx           # Simple fade-in wrapper
│   └── CountUp.tsx          # Number animation
│
├── feedback/
│   ├── LoadingSpinner.tsx   # Generic loading
│   ├── Skeleton.tsx         # Content skeleton
│   ├── EmptyState.tsx       # Empty state with illustration
│   └── ErrorBoundary.tsx    # Error fallback
│
├── shared/
│   ├── Logo.tsx             # Brand logo
│   ├── Avatar.tsx           # User avatar with fallback
│   ├── Badge.tsx            # Status badges
│   └── SearchInput.tsx      # Global search (if applicable)
│
└── ui/                      # shadcn/ui components
    └── (generated by shadcn)
```

### Loading State Pattern

```typescript
// EVERY page should have loading state

// app/dashboard/loading.tsx
import { Skeleton } from "@/components/ui/skeleton";

export default function DashboardLoading() {
  return (
    <div className="space-y-6 p-6">
      {/* Stats skeleton */}
      <div className="grid grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <Skeleton key={i} className="h-32 rounded-xl" />
        ))}
      </div>
      
      {/* Chart skeleton */}
      <Skeleton className="h-64 rounded-xl" />
      
      {/* Table skeleton */}
      <div className="space-y-2">
        {[...Array(5)].map((_, i) => (
          <Skeleton key={i} className="h-12 rounded-lg" />
        ))}
      </div>
    </div>
  );
}
```

### Empty State Pattern

```typescript
// components/feedback/EmptyState.tsx
import { LucideIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="rounded-full bg-muted p-4 mb-4">
        <Icon className="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-muted-foreground mb-4 max-w-sm">{description}</p>
      {actionLabel && onAction && (
        <Button onClick={onAction}>{actionLabel}</Button>
      )}
    </div>
  );
}
```

---

## 🛡️ Zero Error Guarantee

### TypeScript Strict Rules

```typescript
// tsconfig.json MUST have these
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

### Pre-Generation Checklist

Before generating ANY code, verify:

```
□ All imports are valid (no typos)
□ All types are defined
□ All props have types
□ No `any` type used
□ All async functions have error handling
□ All optional chaining where needed (?.)
□ All nullish coalescing where needed (??)
□ All arrays initialized before use
□ All state has initial values
```

### Common Error Prevention Patterns

```typescript
// ❌ BAD: Will error if data is undefined
{data.items.map(item => ...)}

// ✅ GOOD: Safe with fallback
{(data?.items ?? []).map(item => ...)}
```

```typescript
// ❌ BAD: Type error on undefined
function UserCard({ user }) { ... }

// ✅ GOOD: Proper typing
interface UserCardProps {
  user: User;
}
function UserCard({ user }: UserCardProps) { ... }
```

```typescript
// ❌ BAD: Unhandled async
const data = await fetch(...);

// ✅ GOOD: With error handling
try {
  const data = await fetch(...);
  if (!data.ok) throw new Error('Failed to fetch');
  return data.json();
} catch (error) {
  console.error('Fetch error:', error);
  return null;
}
```

### Required Type Definitions

Every project MUST have:

```typescript
// types/index.ts
export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  createdAt: Date;
}

// types/[feature].ts
export interface [Feature] {
  id: string;
  // ... feature-specific fields
  createdAt: Date;
  updatedAt: Date;
}

// types/api.ts
export interface ApiResponse<T> {
  data: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}
```

---

## 🎁 WOW Factor

**WOW = the DESIGN.md signature element executed well + the craft floor.**

Spend boldness in **ONE place** — the signature element declared in root
`DESIGN.md` §1 (distinctive hero treatment, unusual data display, strong
typographic motif) — and keep everything else quiet. WOW is never a checklist
of decorations (gradient text, floating shapes, hover glows, confetti are
AVOID-LIST tells — see `design-craft/AVOID-LIST.md`).

```yaml
wow:
  signature_element:   # the ONE bold move, from DESIGN.md — flagship page only
    - Executed with full craft: motion, spacing, typography all serve it
  craft_floor:         # quiet everywhere else — this is what reads "premium"
    - Responsive at every breakpoint (320px+)
    - focus-visible rings on every interactive element
    - Skeletons matching the real layout on every page
    - Empty states with a real sentence + next action
    - Realistic domain content, zero placeholder text
```

### Premium Design Details

```yaml
shadows:
  cards: "shadow-sm hover:shadow-lg transition-shadow"
  modals: "shadow-2xl"
  dropdowns: "shadow-lg"

borders:
  cards: "border border-border/50"
  inputs: "border border-input focus:ring-2 focus:ring-primary/20"

backgrounds:   # solid surfaces from DESIGN.md tokens — no decorative gradients
  page: "bg-background"
  card: "bg-card"
  muted: "bg-muted/50"

hover_states:
  cards: "hover:border-primary/50 transition-colors"
  buttons: "hover:brightness-110 transition-[filter]"
  links: "hover:text-primary transition-colors"
```

---

## 📋 Pre-Delivery Verification

### Final Checklist (MANDATORY!)

Before delivering to user, verify ALL:

```
BUILD CHECK:
□ `npm run build` passes with 0 errors
□ `npm run lint` passes with 0 warnings
□ All pages render without errors

PAGES CHECK (minimum 5):
□ Homepage/Landing created
□ Main feature page created
□ Dashboard/Detail page created
□ Settings page created
□ Auth page created (at least login)

ANIMATION CHECK:
□ Page transitions working
□ List animations working
□ Card hover effects working
□ Button press feedback working
□ Loading states animated

RESPONSIVE CHECK:
□ Mobile layout works (320px+)
□ Tablet layout works (768px+)
□ Desktop layout works (1024px+)
□ No horizontal scroll

QUALITY CHECK:
□ No TypeScript errors
□ No console errors
□ No missing images (use placeholders)
□ No broken links
□ Loading states present
□ Empty states designed
```

---

## 🚀 Quick Start Template

When starting a new project, use this structure:

```
project/
├── app/
│   ├── layout.tsx          # Root layout with providers
│   ├── page.tsx            # Landing/Home
│   ├── loading.tsx         # Global loading
│   ├── error.tsx           # Global error
│   ├── not-found.tsx       # 404 page
│   │
│   ├── dashboard/
│   │   ├── page.tsx        # Dashboard
│   │   └── loading.tsx     # Dashboard skeleton
│   │
│   ├── [feature]/
│   │   ├── page.tsx        # Feature list
│   │   ├── [id]/page.tsx   # Feature detail
│   │   └── loading.tsx     # Feature skeleton
│   │
│   ├── settings/
│   │   └── page.tsx        # Settings
│   │
│   └── auth/
│       ├── login/page.tsx  # Login
│       └── register/page.tsx # Register
│
├── components/
│   ├── layout/             # Layout components
│   ├── motion/             # Animation components
│   ├── feedback/           # Loading, empty, error states
│   ├── features/           # Feature-specific components
│   ├── shared/             # Shared components
│   └── ui/                 # shadcn/ui
│
├── lib/
│   ├── utils.ts            # Utility functions
│   └── mock-data.ts        # Realistic mock data
│
├── stores/
│   └── use-[feature].ts    # Zustand stores
│
├── types/
│   ├── index.ts            # Shared types
│   └── [feature].ts        # Feature types
│
└── providers/
    └── providers.tsx       # All providers wrapped
```

---

## 🌐 Internationalization Note

All code, comments, and documentation should be in **English**.

Only user-facing content (mock data, UI text) should match the user's language:

```typescript
// Code: Always English
interface ProductCardProps {
  product: Product;
}

// Mock data: Match user language
const mockProducts = [
  // Thai user
  { name: "กาแฟลาเต้", price: 65 },
  // English user
  { name: "Caffe Latte", price: 65 },
];
```

---

*Premium Experience Skill v1.0.0 - One Prompt, Complete App, Instant WOW*
