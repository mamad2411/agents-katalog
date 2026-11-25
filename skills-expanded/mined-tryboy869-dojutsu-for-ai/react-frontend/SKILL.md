---
name: react-frontend
description: "Apply when building React components, pages, SPAs, or UI systems. Covers: component architecture, state management, hooks patterns, performance, accessibility, and styling with Tailwind. Trigger for: React, Next.js, component, UI, frontend, SPA."
---

# REACT FRONTEND — Production Standards 2025

## Component Architecture

### Single Responsibility (non-negotiable)
```tsx
// ❌ God component
function Dashboard() { /* auth + fetch + render + modal = untestable */ }

// ✅ Composed
function Dashboard() {
  return <DashboardLayout><JobList /><MetricsPanel /></DashboardLayout>
}
```

### Props — Always typed, minimal surface
```tsx
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'danger' | 'ghost'
  disabled?: boolean
  isLoading?: boolean
}
// No "any", no prop drilling > 2 levels → use context or state manager
```

## State Management Decision Tree
- **Local UI state** → `useState` (open/close, form fields)
- **Async server state** → `TanStack Query` (fetch, cache, refetch)
- **Global shared state** → `Zustand` (auth, theme, cart)
- **URL state** → `useSearchParams` (filters, pagination)
- **NEVER** → Redux for new projects in 2025

## Hooks Patterns

### Data fetching (TanStack Query)
```tsx
function JobList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['jobs', filters],
    queryFn: () => fetchJobs(filters),
    staleTime: 30_000,
  })
  if (isLoading) return <Skeleton />
  if (error) return <ErrorBoundary error={error} />
  return <ul>{data.map(job => <JobCard key={job.id} {...job} />)}</ul>
}
```

### Custom hook — encapsulate logic, not JSX
```tsx
function useJobSubmit() {
  const mutation = useMutation({
    mutationFn: submitJob,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['jobs'] }),
  })
  return { submit: mutation.mutate, isPending: mutation.isPending }
}
```

## Performance Rules
- `React.memo()` only after profiling — not by default
- `useCallback` / `useMemo` only for expensive operations or stable refs
- Dynamic imports for routes: `const Page = lazy(() => import('./Page'))`
- Images: always `width` + `height` attributes (prevent CLS)
- Lists: always `key` prop that is a **stable unique ID** (never array index)

## Accessibility (MANDATORY)
```tsx
// Buttons must have text or aria-label
<button aria-label="Close dialog" onClick={onClose}><XIcon /></button>

// Forms must have associated labels
<label htmlFor="email">Email</label>
<input id="email" type="email" required />

// Color contrast: 4.5:1 minimum for normal text
```

## Forbidden Patterns
❌ `useEffect` for data fetching (use TanStack Query)
❌ `index` as key in dynamic lists
❌ Inline styles for anything beyond one-off overrides
❌ `any` type in TypeScript
❌ Nested ternaries in JSX (extract to variable or component)
❌ React SPA for content sites (use Next.js/Astro instead)
