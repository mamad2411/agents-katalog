# Agent Context for opus4.6

## Project Overview
**Name:** opus4.6  
**Type:** Next.js 16 application with React 19  
**Framework:** Next.js with App Router  
**Language:** TypeScript  
**Styling:** Tailwind CSS v4  
**UI Library:** shadcn/ui with Base UI and Radix UI primitives  

## Tech Stack

### Core
- **Next.js**: 16.1.4 (App Router)
- **React**: 19.2.3
- **TypeScript**: ^5
- **Node**: v20+

### Styling & UI
- **Tailwind CSS**: v4 (PostCSS-based)
- **shadcn/ui**: 3.8.3
- **Base UI**: 1.1.0 (MUI)
- **Radix UI**: 1.4.3
- **class-variance-authority**: 0.7.1
- **tailwind-merge**: 3.4.0
- **tw-animate-css**: 1.4.0
- **next-themes**: 0.4.6

### UI Components & Libraries
- **Hugeicons**: React icon library (1.1.4)
- **cmdk**: Command menu (1.1.1)
- **sonner**: Toast notifications (2.0.7)
- **vaul**: Drawer component (1.1.2)
- **react-resizable-panels**: Resizable layouts (4.6.0)
- **embla-carousel-react**: Carousel component (8.6.0)
- **recharts**: Charts and data visualization (2.15.4)
- **react-day-picker**: Date picker (9.13.0)
- **input-otp**: OTP input (1.4.2)

### Fonts
- **Geist Sans & Geist Mono**: Vercel's font family
- **Public Sans**: Google Font (primary font via `--font-sans`)

## Project Structure

```
opus4.6/
├── app/
│   ├── layout.tsx          # Root layout with font configuration
│   ├── page.tsx            # Home page (renders ComponentExample)
│   └── globals.css         # Global styles
├── components/
│   ├── ui/                 # shadcn/ui components (50+ components)
│   ├── component-example.tsx
│   └── example.tsx
├── hooks/
│   └── use-mobile.ts       # Mobile detection hook
├── lib/
│   └── utils.ts            # Utility functions (cn, etc.)
├── public/                 # Static assets
├── components.json         # shadcn/ui configuration
├── tsconfig.json          # TypeScript config with @/* path alias
├── next.config.ts         # Next.js configuration
└── package.json

```

## Key Configurations

### TypeScript
- **Target:** ES2017
- **Module:** ESNext with bundler resolution
- **JSX:** react-jsx (React 19)
- **Strict mode:** Enabled
- **Path alias:** `@/*` → `./*`

### Package Management
- Uses **Bun** (bun.lock present) and **Yarn** (yarn.lock present)
- Ignored scripts: `sharp`, `unrs-resolver`
- Trusted dependencies: `sharp`, `unrs-resolver`

### Scripts
- `dev`: Start development server
- `build`: Production build
- `start`: Start production server
- `lint`: Run ESLint

## Development Guidelines

### Component Development
1. All UI components follow shadcn/ui patterns
2. Use the `@/` alias for imports
3. Components use TypeScript with proper typing
4. Tailwind CSS for styling with class-variance-authority for variants
5. Theme support via next-themes

### Font Configuration
- Primary font: Public Sans (variable: `--font-sans`)
- Secondary fonts: Geist Sans and Geist Mono
- Fonts are loaded via `next/font/google`

### UI Component Library
The project includes a comprehensive shadcn/ui component library:
- **Layout:** Sidebar, Resizable, Scroll Area, Separator, Sheet, Direction
- **Navigation:** Tabs, Breadcrumb, Navigation Menu, Menubar
- **Forms:** Input, Input Group, Input OTP, Textarea, Select, Native Select, Checkbox, Radio Group, Switch, Calendar, Field
- **Feedback:** Alert, Alert Dialog, Dialog, Drawer, Toast (Sonner), Spinner, Progress, Skeleton, Empty
- **Display:** Card, Badge, Avatar, Table, Accordion, Collapsible, Carousel, Chart, Aspect Ratio, Kbd
- **Overlay:** Popover, Tooltip, Hover Card, Dropdown Menu, Context Menu, Command, Combobox
- **Buttons:** Button, Button Group, Toggle, Toggle Group

### Styling Approach
- Tailwind CSS v4 with PostCSS
- Custom animations via tw-animate-css
- Theme-aware components using next-themes
- Utility-first CSS with component composition

### Data Visualization
- Uses Recharts for charts and graphs
- Pre-configured chart component in `components/ui/chart.tsx`

## Commands

### Development
```bash
bun dev          # Start dev server (preferred)
npm run dev      # Alternative with npm
yarn dev         # Alternative with yarn
```

### Production
```bash
bun run build    # Build for production
bun start        # Start production server
```

### Linting
```bash
bun run lint     # Run ESLint
```

## Important Notes

1. **React 19:** Uses the latest React version - be aware of potential breaking changes
2. **Next.js 16:** App Router only, no Pages Router
3. **Tailwind v4:** PostCSS-based, different from v3
4. **Font Loading:** Three fonts configured but Public Sans is the primary variable
5. **Component Library:** Extensive pre-built UI components via shadcn/ui
6. **Package Managers:** Both Bun and Yarn lock files present - prefer Bun for consistency
7. **ESLint Config:** Uses flat config (eslint.config.mjs) with Next.js preset

## Current State
- Fresh Next.js installation with extensive shadcn/ui component library
- Main page renders `ComponentExample` component
- Ready for application development with complete UI component foundation
- No backend/API routes currently defined
- No database or state management configured yet

## Agent Instructions
When working on this project:
- Use TypeScript for all code
- Follow shadcn/ui component patterns and conventions
- Use the `@/` import alias consistently
- Prefer Bun for package management
- Test changes with `bun dev` before committing
- Ensure all components are properly typed
- Use existing UI components from `components/ui/` before creating new ones
- Maintain consistency with Tailwind CSS utility classes
- Support both light and dark themes via next-themes
