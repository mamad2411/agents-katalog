---
name: project-structure-architect
description: "Use when generating dynamic project structures from PRDs or app ideas. Produces folder hierarchies, component maps, page specs, and site maps for code/design handoff. Consolidates Project Structure Architect and Site Mapper."
version: "1.0"
tags:
  - project-structure
  - folder-hierarchy
  - component-architecture
  - sitemap
  - design-handoff
  - code-organization
---

# Project Structure Architect

## Overview

Generates production-ready project structures from PRDs or app ideas. Produces folder hierarchies, component maps, page specifications, route definitions, and visual site maps. Bridges the gap between requirements and implementation — gives developers and designers a concrete blueprint.

## When to Use

- You have a PRD and need to translate it into a codebase structure
- Starting a new project and need a scaffold plan before writing code
- Planning a component library breakdown for a design system
- Creating a site map for a multi-page application
- Handoff between product/design and engineering teams
- Refactoring: auditing an existing project structure against best practices

## How It Works

1. **Requirements Analysis** — Parse the PRD or idea for pages, features, and data flows.
2. **Route Mapping** — Define URL structure and page hierarchy.
3. **Component Decomposition** — Break pages into reusable components (Atomic Design: atoms → molecules → organisms → templates → pages).
4. **Data Modeling** — Map components to data sources (props, API calls, state).
5. **Folder Architecture** — Generate the directory tree with file-level granularity.

## Steps

### Step 1: Route Map (Site Map)
Generate a tree of all pages/routes:
```
/                           → Landing page
/products                   → Product listing
/products/[id]              → Product detail
/products/[id]/checkout     → Checkout flow
/dashboard                  → User dashboard (auth-gated)
/dashboard/settings         → Account settings
/dashboard/orders           → Order history
/auth/login                 → Login page
/auth/signup                → Signup page
/api/*                      → API routes
```

### Step 2: Component Map
For each page, list components with their hierarchy:
```
LandingPage
├── Navbar (molecule)
│   ├── Logo (atom)
│   ├── NavLinks (molecule)
│   └── CTAButton (atom)
├── HeroSection (organism)
│   ├── HeroHeading (atom)
│   ├── HeroSubtext (atom)
│   ├── HeroCTA (molecule)
│   └── HeroImage (atom)
├── FeaturesGrid (organism)
│   └── FeatureCard[] (molecule)
│       ├── FeatureIcon (atom)
│       ├── FeatureTitle (atom)
│       └── FeatureDescription (atom)
├── TestimonialsCarousel (organism)
└── Footer (organism)
```

### Step 3: Data Flow Mapping
For each component, specify data sources:
| Component | Data Source | Loading State | Error State | Empty State |
|-----------|------------|---------------|-------------|-------------|
| ProductList | `GET /api/products` | Skeleton grid | Error banner + retry | "No products yet" |
| ProductCard | Props from parent | Skeleton card | Fallback image | N/A (only rendered with data) |
| CartBadge | CartContext (client state) | N/A | N/A | Hidden when empty |

### Step 4: Folder Architecture
Generate a complete directory tree:
```
project-root/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (marketing)/        # Public route group
│   │   │   ├── page.tsx        # Landing
│   │   │   ├── products/
│   │   │   │   ├── page.tsx    # Product listing
│   │   │   │   └── [id]/
│   │   │   │       ├── page.tsx      # Product detail
│   │   │   │       └── checkout/
│   │   │   │           └── page.tsx  # Checkout
│   │   │   └── layout.tsx
│   │   ├── (dashboard)/        # Auth-gated route group
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── settings/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── orders/
│   │   │   │       └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── auth/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   ├── api/                # API routes
│   │   │   └── products/
│   │   │       ├── route.ts
│   │   │       └── [id]/
│   │   │           └── route.ts
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                 # shadcn/ui primitives
│   │   ├── layout/             # Navbar, Footer, Sidebar
│   │   ├── marketing/          # Hero, Features, Testimonials
│   │   ├── products/           # ProductCard, ProductGrid
│   │   └── dashboard/          # StatsCard, OrderTable
│   ├── lib/                    # Utilities, API client, auth
│   ├── hooks/                  # Custom hooks
│   ├── types/                  # TypeScript types/interfaces
│   └── config/                 # App configuration
├── public/                     # Static assets
│   └── images/
├── prisma/                     # Database schema
│   └── schema.prisma
├── tests/                      # Test files
│   ├── unit/
│   └── e2e/
└── docs/                       # Project documentation
    └── PRD.md
```

### Step 5: Deliverable Generation
Package the output as:
1. **Route Map** (markdown tree or Mermaid diagram)
2. **Component Tree** (nested markdown with data state annotations)
3. **Folder Structure** (full tree, copy-pasteable into terminal)
4. **File Scaffold Script** (optional: bash script to `mkdir` and `touch` the entire structure)

## Common Pitfalls

- **Over-nesting**: More than 4 levels deep in either files or components is a smell. Flatten when possible.
- **Premature abstraction**: Don't create shared components until you have 3+ uses. Start with page-level components.
- **Ignoring data states**: The structure should account for loading, error, empty, and edge cases — not just the happy path.
- **Route groups without layouts**: Every route group should have a layout.tsx that handles shared concerns (auth check, analytics, metadata).
- **Docs outside the repo**: PRDs and design specs should live in the repo under `/docs` so they're versioned alongside code.

## Source

Consolidates: Project Structure Architect GPT, Site Mapper GPT.
