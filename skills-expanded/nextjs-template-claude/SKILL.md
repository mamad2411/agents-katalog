# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Development Commands

```bash
pnpm dev          # Start development server (http://localhost:3000)
pnpm build        # Production build
pnpm build:analyze # Production build with bundle analyzer (ANALYZE=true)
pnpm start        # Start production server
pnpm lint         # Run ESLint
```

## Architecture

This is a Next.js 16 application using the App Router with a feature-based architecture.

### Directory Structure

- `app/` - Next.js App Router pages and layouts
- `lib/features/` - Feature modules (self-contained domain logic)
- `lib/utilities/` - Shared utility functions

### Feature Module Structure

Features are self-contained modules located in `lib/features/`. Each feature can contain:

```
feature-name/
├── api/           # Data layer
│   ├── logic/     # Business logic functions
│   └── models/    # TypeScript types and enums
├── components/    # React UI components
├── hooks/         # Custom React hooks
└── contexts/      # React Context providers
```

### Component Conventions

Components live in their own directories with associated state files:
- `{component-name}.tsx` - Main component
- `{component-name}-loading.tsx` - Loading/skeleton state
- `{component-name}-errored.tsx` - Error state
- `{component-name}-empty.tsx` - Empty state
- `index.ts` - Barrel export

### Path Aliases

`@/*` maps to the project root (configured in tsconfig.json).

## Key Dependencies

- **SWR** - Data fetching and caching
- **usehooks-ts** - TypeScript React hooks utilities
- **Tailwind CSS v4** - Styling