---
alwaysApply: true
---
# goielts - Project Rules

- Always start with ( === 🔥 Rules Applied 🔥 === ) when you read this rule to let me know that rule applied.

## Project Overview
IELTS exam preparation web application built with Next.js 16 and React 19.

## Tech Stack
- **Framework**: Next.js 16 (App Router with React Server Components)
- **Language**: TypeScript (strict mode)
- **Package Manager**: Bun (use `bun` and `bunx`, NOT npm)
- **Styling**: Tailwind CSS v4 with CSS variables
- **UI Components**: shadcn/ui (new-york style)
- **Icons**: Lucide React
- **Forms**: React Hook Form + Zod validation
- **Animations**: tw-animate-css
- **API Framework**: Hono
- **Database**: MongoDB with Mongoose

## Project Structure
```
src/
├── app/
│   ├── api/[[...route]]/route.ts  # Central Hono router
│   └── ...                         # Next.js pages and layouts
├── components/
│   └── ui/                         # shadcn/ui components (do not modify directly)
├── hooks/
│   └── useTranslate.ts             # Translation hook
├── lib/
│   ├── mongodb.ts                  # MongoDB connection
│   └── utils.ts                    # Utility functions
├── models/
│   └── [ModelName]/
│       ├── [modelName]Schema.ts    # MongoDB schema
│       └── route.ts                # Hono API routes
└── i18n/
    └── locales/
        ├── ar.json                 # Arabic translations
        └── en.json                 # English translations
```

## Path Aliases
Use `@/*` for imports from `src/`:
```typescript
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import dbConnect from "@/lib/mongodb"
```

---

## Development Workflow

### MongoDB Schema Creation

1. Create new MongoDB schemas in:
   ```
   /src/models/[ModelName]/[modelName]Schema.ts
   ```
   Example: `/src/models/Users/userSchema.ts`

2. Use TypeScript interfaces to define your schema type

### API Route Implementation

1. Create route files in:
   ```
   /src/models/[ModelName]/route.ts
   ```
   Example: `/src/models/Payment/route.ts`

2. Always follow this template for route files:

```typescript
import { Hono } from 'hono'
import dbConnect from '@/lib/mongodb'
import mongoose from 'mongoose'
import { z } from 'zod'

// Replace with your model import
import YourModel, { IYourModel } from './YourModelSchema'

// Define your validation schema
const validationSchema = z.object({
    // Add your schema fields here
})

const app = new Hono()

// Create new item
app.post('/add-item', async (c) => {
    try {
        await dbConnect()
        const data = await c.req.json()
        const userId = c.req.query('userId')

        if (!userId) {
            return c.json(
                {
                    success: false,
                    error: 'User ID is required',
                },
                400
            )
        }
        // Implementation here
    } catch (error) {
        return c.json(
            {
                success: false,
                error: 'Internal server error',
                details:
                    error instanceof Error ? error.message : 'Unknown error',
            },
            500
        )
    }
})

// Get all items
app.get('/items', async (c) => {
    try {
        await dbConnect()
        const page = parseInt(c.req.query('page') || '1')
        const limit = parseInt(c.req.query('limit') || '10')
        const searchTerm = c.req.query('search') || ''

        // Implementation here
    } catch (error) {
        return c.json(
            {
                success: false,
                error: 'Internal server error',
                details:
                    error instanceof Error ? error.message : 'Unknown error',
            },
            500
        )
    }
})

// Get single item
app.get('/item/:id', async (c) => {
    try {
        await dbConnect()
        const id = c.req.param('id')

        // Implementation here
    } catch (error) {
        return c.json(
            {
                success: false,
                error: 'Internal server error',
                details:
                    error instanceof Error ? error.message : 'Unknown error',
            },
            500
        )
    }
})

// Update item
app.post('/update-item/:id', async (c) => {
    try {
        await dbConnect()
        const data = await c.req.json()
        const id = c.req.param('id')
        const userId = c.req.query('userId')

        // Implementation here
    } catch (error) {
        return c.json(
            {
                success: false,
                error: 'Internal server error',
                details:
                    error instanceof Error ? error.message : 'Unknown error',
            },
            500
        )
    }
})

// Delete item
app.delete('/delete-item/:id', async (c) => {
    try {
        await dbConnect()
        const id = c.req.param('id')
        const userId = c.req.query('userId')

        // Implementation here
    } catch (error) {
        return c.json(
            {
                success: false,
                error: 'Internal server error',
                details:
                    error instanceof Error ? error.message : 'Unknown error',
            },
            500
        )
    }
})

export default app
```

### Route Registration

After creating a new route file, update the central router in:
```
/src/app/api/[[...route]]/route.ts
```

Add your new route to the Hono app instance:

```typescript
import { Hono } from 'hono'
import { handle } from 'hono/vercel'

import users from '@/models/Users/route'
import subscriptions from '@/models/Subscription/route'
// ... other imports
import yourNewRoute from '@/models/YourNewModel/route'

const app = new Hono().basePath('/api')

const routes = app
    .route('/users', users)
    .route('/subscriptions', subscriptions)
    // ... other routes
    .route('/your-new-endpoint', yourNewRoute)

export const GET = handle(app)
export const POST = handle(app)
export const PATCH = handle(app)
export const DELETE = handle(app)

export type AppType = typeof routes
```

---

## Translations

Use the translation hook:
```typescript
import { useTranslate } from '@/hooks/useTranslate'

const { t } = useTranslate()
```

Translation files:
- Arabic: `src/i18n/locales/ar.json`
- English: `src/i18n/locales/en.json`

---

## Code Style & Conventions

### Components
- Use function declarations for components (not arrow functions)
- Export components as named exports
- Use `React.ComponentProps<"element">` for extending HTML element props
- Place component-specific types inline, shared types in separate files

### Styling
- Use Tailwind CSS utility classes
- Use `cn()` helper from `@/lib/utils` for conditional classes
- Leverage CSS variables defined in `globals.css` for theming
- Follow mobile-first responsive design

### UI Components
- Use shadcn/ui components from `@/components/ui/`
- Add new shadcn components via: `bunx shadcn@latest add <component>`
- Do not modify files in `@/components/ui/` directly
- Create wrapper components if customization is needed

### Forms
- Use React Hook Form with Zod schemas for validation
- Use shadcn Form components for form fields
- Define Zod schemas near the form component

### Server vs Client Components
- Default to Server Components (no directive needed)
- Add `"use client"` only when using:
  - React hooks (useState, useEffect, etc.)
  - Browser APIs
  - Event handlers
  - Client-side libraries

## Commands
```bash
bun dev          # Start development server
bun run build    # Build for production
bun run lint     # Run ESLint
```

## Pre-Commit Checklist

Before pushing code to the repository, ensure:

1. MongoDB schemas follow the correct path structure
2. API routes follow the template structure
3. Routes are properly registered in the central router
4. MongoDB connection is being used correctly

## Best Practices
- Keep components small and focused
- Colocate related files (component, styles, tests)
- Use semantic HTML elements
- Ensure accessibility (ARIA labels, keyboard navigation)
- Handle loading and error states appropriately
