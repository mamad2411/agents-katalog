---
name: web-artifacts-builder
description: Use this skill when building multi-component web applications, interactive dashboards, complex React apps with state management, or any web artifact that requires routing, multiple views, or sophisticated UI interactions. Trigger on keywords: build a web app, dashboard, multi-page, React app, interactive tool, web application, complex UI, build a tool that.
---

# Web Artifacts Builder

## When to Use This Skill

Use for complex, multi-component applications. For simple single components, use `frontend-design` instead.

Signs you need this skill:
- Multiple views or pages
- Global state management
- Complex user interactions with multiple data flows
- Dashboard with multiple widgets
- Form wizard with multiple steps

---

## Technology Stack

### Recommended Stack (2026)
```
Framework:    Next.js 15 (App Router) or React 19
Styling:      Tailwind CSS v4
Components:   shadcn/ui (accessible primitives)
State:        Zustand (client) + TanStack Query (server)
Forms:        React Hook Form + Zod
Animation:    Motion (formerly Framer Motion)
Icons:        Lucide React
```

---

## Application Architecture

```
src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── [feature]/
│       └── page.tsx
├── components/
│   ├── ui/                 # shadcn/ui components
│   └── [feature]/          # Feature-specific components
├── lib/
│   ├── utils.ts            # Shared utilities
│   └── validations.ts      # Zod schemas
├── hooks/                  # Custom React hooks
├── stores/                 # Zustand stores
└── types/                  # TypeScript types
```

---

## shadcn/ui Component Usage

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
```

Always use shadcn/ui primitives for standard UI elements — they're accessible by default and consistent.

---

## State Management Pattern

```typescript
// Zustand store
import { create } from 'zustand'

interface AppStore {
  user: User | null
  setUser: (user: User | null) => void
  
  selectedItems: string[]
  toggleItem: (id: string) => void
  clearSelection: () => void
}

export const useAppStore = create<AppStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  
  selectedItems: [],
  toggleItem: (id) => set((state) => ({
    selectedItems: state.selectedItems.includes(id)
      ? state.selectedItems.filter(i => i !== id)
      : [...state.selectedItems, id]
  })),
  clearSelection: () => set({ selectedItems: [] })
}))
```

---

## Data Fetching Pattern

```typescript
// TanStack Query for server state
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
    staleTime: 5 * 60 * 1000 // 5 minutes
  })
}

export function useCreateUser() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CreateUserInput) => 
      fetch('/api/users', { method: 'POST', body: JSON.stringify(data) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    }
  })
}
```

---

## Build Checklist

Before shipping any web artifact:
- [ ] Mobile responsive (test at 375px, 768px, 1280px)
- [ ] Keyboard navigable
- [ ] Loading states for async operations
- [ ] Empty states for lists/tables
- [ ] Error states with recovery options
- [ ] Form validation with clear error messages
- [ ] No console errors or warnings
- [ ] TypeScript types complete (no `any`)
