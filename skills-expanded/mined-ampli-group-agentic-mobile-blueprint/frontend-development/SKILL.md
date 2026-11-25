---
name: frontend-development
description: Next.js frontend app development patterns with App Router, Tailwind CSS v4, Zustand, and TanStack Query. Use when creating pages, components, or API routes in the frontend app.
---

# Frontend Development

## Stack

Next.js 16 (App Router, Turbopack), React 19, Tailwind CSS v4, Zustand 5, TanStack Query v5, react-hook-form + Zod 4, TypeScript strict mode.

## Imports

Use `@/` path alias for `src/`: `@/lib/supabase`, `@/components/Button`.

## Client vs Server

Mark interactive/stateful components with `'use client'`. Default is server component.

## Styling

Tailwind CSS v4 with `@theme` tokens in `src/app/globals.css`:

```css
@import 'tailwindcss';

@theme {
  --color-cream: #FCFAF7;
  --color-slate-deep: #1B2030;
  --color-emerald-glow: #10B981;
}
```

Add new design tokens in `@theme`, not in config files.

## Supabase Clients

Three clients for different contexts:

| Import | Use for | Context |
|--------|---------|---------|
| `@/lib/supabase` | General public queries | Client, graceful fallback if env missing |
| `@/lib/supabase-browser` | Auth flows (login, signup) | Client (`'use client'`) |
| `@/lib/supabase-admin` | Admin operations | Server-only, `createAdminClient()` |

```tsx
// Client component — auth flow
import { supabaseBrowser } from '@/lib/supabase-browser';

// Server component / action — admin
import { createAdminClient } from '@/lib/supabase-admin';
const supabase = createAdminClient();
```

## State Management

Zustand with `persist` middleware. Use `partialize` to persist only selected fields:

```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useMyStore = create(
  persist(
    (set) => ({
      value: '',
      setValue: (v: string) => set({ value: v }),
    }),
    { name: 'my-store', partialize: (s) => ({ value: s.value }) }
  )
);
```

## Providers

Composed in `src/app/layout.tsx`. Order: `QueryProvider` → `PostHogProvider` → children. Add new providers inside `QueryProvider`.

## Forms

Use react-hook-form + `@hookform/resolvers` + Zod for validation:

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({ email: z.string().email() });

const { register, handleSubmit } = useForm({
  resolver: zodResolver(schema),
});
```

## Environment Variables

Public: `NEXT_PUBLIC_*`. Server-only: no prefix (e.g. `SUPABASE_SERVICE_ROLE_KEY`).
