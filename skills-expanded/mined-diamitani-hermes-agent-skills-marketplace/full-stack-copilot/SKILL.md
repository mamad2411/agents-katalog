---
name: full-stack-copilot
description: "Use when scaffolding React, Tailwind, shadcn/ui components or full-stack apps from prompts. Generates deployment-ready code with modern stack defaults. Consolidates Full Stack Copilot, PlaceCode, and Horizon UI Copilot."
version: "1.0"
tags:
  - react
  - tailwind
  - shadcn
  - nextjs
  - full-stack
  - code-generation
  - scaffolding
---

# Full Stack Copilot

## Overview

Generates deployment-ready React + Tailwind + shadcn/ui code from prompts. Scaffolds components, pages, and full-stack applications with modern defaults (Next.js App Router, TypeScript, Prisma/Supabase). Produces code you can actually run — not pseudocode.

## When to Use

- User needs a React component built from a description
- Scaffolding a full-stack CRUD app with auth
- Building a shadcn/ui dashboard or admin panel
- Converting a wireframe description into Tailwind markup
- Rapid prototyping of UI flows
- Generating production components with loading/error/empty states

## How It Works

1. **Intent Parsing** — Determine scope: single component vs. page vs. full app.
2. **Stack Assignment** — Apply sensible defaults based on project type.
3. **Component Generation** — Produce components following modern React patterns.
4. **Wiring** — Connect components to data, state, and routes.
5. **Quality Gates** — Verify accessibility, responsiveness, and state coverage.

## Steps

### Step 1: Scope Assessment
Classify the request:
- **Component**: Single reusable UI piece (button, card, modal, form)
- **Page**: Full page with multiple components and layout
- **Flow**: Multi-page sequence (auth flow, checkout, onboarding)
- **App**: Complete application with auth, DB, routes, and deployment

### Step 2: Stack Defaults
Apply these defaults unless the user specifies otherwise:
```yaml
framework: Next.js 14+ (App Router)
language: TypeScript (strict mode)
styling: Tailwind CSS v3.4+
ui_library: shadcn/ui (Radix primitives)
database: Supabase or Prisma + PostgreSQL
auth: NextAuth.js v5 or Supabase Auth
state: React Server Components + client hooks where needed
forms: react-hook-form + zod validation
hosting: Vercel (default)
```

### Step 3: Component Generation Rules
Every component must include:
- **TypeScript interfaces** for all props
- **Loading state** (skeleton or spinner)
- **Error state** (error boundary or inline error)
- **Empty state** (when data is empty/null)
- **Responsive breakpoints** (mobile-first Tailwind classes)
- **Accessibility** (aria labels, keyboard navigation, focus management)
- **Comments** for non-obvious logic only

### Step 4: Component Template
```tsx
"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

interface ComponentNameProps {
  /** Description of the prop */
  data: DataType;
  /** Optional className for styling overrides */
  className?: string;
  /** Loading state override */
  isLoading?: boolean;
  /** Error message to display */
  error?: string | null;
}

export function ComponentName({
  data,
  className,
  isLoading = false,
  error = null,
}: ComponentNameProps) {
  if (isLoading) return <ComponentSkeleton className={className} />;
  if (error) return <ErrorDisplay message={error} />;
  if (!data || data.length === 0) return <EmptyState message="No items found" />;

  return (
    <div className={cn("container mx-auto px-4", className)}>
      {/* Component content */}
    </div>
  );
}
```

### Step 5: Full-Stack App Scaffolding
Follow this order:
1. **Init project**: `npx create-next-app@latest --typescript --tailwind --app`
2. **Install shadcn/ui**: `npx shadcn-ui@latest init`
3. **Add core components**: Button, Input, Card, Dialog, DropdownMenu, Table, Form, Toast
4. **Set up auth**: Install NextAuth/Supabase, create middleware, generate login/signup pages
5. **Set up database**: Create Prisma schema or Supabase tables
6. **Build layout**: Root layout, navigation, footer, metadata
7. **Build pages**: Start with the primary user flow
8. **Add API routes**: Create/read/update/delete endpoints
9. **Wire everything**: Connect components to data, add loading states
10. **Deploy**: `vercel deploy` or equivalent

### Step 6: Deliver Code
For each request, deliver:
1. The component/page file(s) with full code
2. Import instructions (which shadcn components to install first)
3. Brief usage example showing props and common configurations
4. Notes on any assumptions made

## Common Pitfalls

- **Forgetting 'use client'**: shadcn/ui components using hooks need the directive. Server components can't use them.
- **Missing shadcn component installs**: Always list the `npx shadcn-ui@latest add [component]` commands before the code.
- **No error boundaries**: A single unhandled error in production takes down the whole page.
- **Hardcoded values**: Colors, spacing, breakpoints, and content should use Tailwind tokens and configuration, not magic numbers.
- **Ignoring Layout Shift**: Images without explicit width/height cause Cumulative Layout Shift (CLS). Always add `sizes` and proper dimensions.
- **Over-fetching in Server Components**: Don't fetch all data server-side if it blocks the first paint. Use Suspense boundaries and streaming.

## Source

Consolidates: Full Stack Copilot GPT, PlaceCode GPT, Horizon UI Copilot GPT.
