---
name: frontend-premium-standards
description: |
  Premium UI/UX engineering standards for React + TypeScript frontends. Apply whenever building
  components, pages, dashboards, landing pages, or any visual interface. Enforces design tokens,
  8pt grid, atomic architecture, Lighthouse targets, and the full premium stack.
  Default: React 18 + TS + Vite + Tailwind + Framer Motion + Zustand + TanStack Query.
---

# Frontend Premium Standards

## Design System Foundation

### Design Tokens (Always use — never hardcode)
```css
:root {
  /* Colors */
  --color-primary: #6366f1;
  --color-primary-hover: #4f46e5;
  --color-surface: #ffffff;
  --color-surface-2: #f8fafc;
  --color-border: #e2e8f0;
  --color-text-primary: #0f172a;
  --color-text-secondary: #64748b;
  --color-error: #ef4444;
  --color-success: #22c55e;

  /* Spacing — 8pt grid */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

### Typography Hierarchy
- H1: 36–48px, weight 700–800, line-height 1.1
- H2: 28–36px, weight 700, line-height 1.2
- H3: 22–28px, weight 600, line-height 1.3
- Body: 16px, weight 400, line-height 1.6
- Caption: 12–14px, weight 400–500, line-height 1.4
- Label: 12–14px, weight 600, uppercase + tracking

### 8pt Grid System
All spacing, sizing, and layout values must be multiples of 4px (4, 8, 12, 16, 24, 32, 48, 64, 96, 128).

## Interactive State Requirements
Every interactive element must implement ALL states:
```tsx
// Required states for every button, input, link, card
const states = {
  default:  "bg-primary text-white",
  hover:    "hover:bg-primary-hover hover:shadow-md transition-all",
  focus:    "focus-visible:ring-2 focus-visible:ring-primary focus-visible:outline-none",
  active:   "active:scale-95 active:shadow-sm",
  disabled: "disabled:opacity-40 disabled:cursor-not-allowed disabled:pointer-events-none",
  loading:  "cursor-wait opacity-70",
}
```

## Dark Mode (Default Required)
```tsx
// Always use CSS variables or Tailwind dark: prefix
// Never hardcode colors for light mode only
<div className="bg-surface dark:bg-surface-dark text-text-primary dark:text-text-primary-dark">
```

## Responsive Breakpoints (Mobile-First)
```
xs:  320px  — minimum support
sm:  640px  — large phones
md:  768px  — tablets
lg:  1024px — small laptops
xl:  1280px — desktops
2xl: 1536px — large screens
```

## Atomic Design Architecture
```
src/
├── components/
│   ├── atoms/          # Button, Input, Badge, Icon, Spinner
│   ├── molecules/      # SearchBar, FormField, Card, Modal
│   ├── organisms/      # Header, Sidebar, DataTable, ProductGrid
│   ├── templates/      # PageLayout, DashboardLayout, AuthLayout
│   └── pages/          # HomePage, DashboardPage, ProfilePage
├── hooks/              # useDebounce, useMediaQuery, useInfiniteScroll
├── stores/             # Zustand stores
├── lib/                # API client, utils, constants
└── types/              # Shared TypeScript types
```

## Component Standards
```tsx
// Every component: typed props, no prop drilling >2 levels
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'danger';
  size: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  isDisabled?: boolean;
  leftIcon?: React.ReactNode;
  onClick?: () => void;
  children: React.ReactNode;
}

// Lazy load routes and heavy components
const Dashboard = lazy(() => import('./pages/Dashboard'));

// Memoize only when measurable cost exists
const expensiveList = useMemo(() => processItems(items), [items]);
const handleSubmit = useCallback(() => onSubmit(data), [data, onSubmit]);
```

## Motion / Animation
```tsx
// Framer Motion — purposeful, not decorative
const variants = {
  hidden: { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.2, ease: 'easeOut' } },
  exit: { opacity: 0, y: -8, transition: { duration: 0.15 } },
};

// Easing standards
// Ease-out: elements entering viewport
// Ease-in: elements leaving
// Spring: drag, physical interactions
// Duration: 150–300ms for micro, 300–500ms for page transitions
```

## Performance Targets
| Metric | Target |
|--------|--------|
| Lighthouse Performance | ≥ 90 |
| Lighthouse Accessibility | ≥ 95 |
| Lighthouse Best Practices | ≥ 90 |
| LCP | < 2.5s |
| CLS | < 0.1 |
| FID / INP | < 100ms |
| Bundle (initial JS) | < 200KB gzip |

## Bundle Analysis
```bash
# Add to vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';
plugins: [visualizer({ open: true, gzip: true })]

# Check before every release
npx vite-bundle-analyzer
```

## Default Stack
```
React 18 + TypeScript (strict) + Vite
Tailwind CSS (design tokens via tailwind.config)
Framer Motion (animation)
Zustand (client state)
TanStack Query v5 (server state, caching)
React Hook Form + Zod (forms + validation)
Lucide React (icons)
Vitest + Testing Library (unit/integration tests)
Playwright (E2E)
```
