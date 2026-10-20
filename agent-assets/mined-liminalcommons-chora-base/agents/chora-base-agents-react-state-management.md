---
sap_id: SAP-023
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 13
progressive_loading:
  phase_1: "lines 1-220"   # Quick Start + Core Workflows
  phase_2: "lines 221-450" # Advanced Workflows
  phase_3: "full"          # Complete including best practices and pitfalls
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 13000
---

# React State Management Patterns (SAP-023) - Agent Awareness

**SAP ID**: SAP-023
**Agent Compatibility**: All AI agents with command execution and file operations
**Last Updated**: 2025-11-05

---

## 📖 Quick Reference

**New to SAP-023?** → Read **[README.md](README.md)** first (12-min read)

The README provides:
- 🚀 **Quick Start** - 5-minute setup (TanStack Query + Zustand + React Hook Form) with three-pillar architecture
- 📚 **Time Savings** - 60% state management time reduction with unified patterns across server, client, and form state
- 🎯 **State Classification** - Decision tree for choosing the right tool (server/client/form)
- 🔧 **TanStack Query v5** - Caching, refetching, optimistic updates, infinite queries for server state
- 📊 **Zustand v4** - Minimal boilerplate, persist middleware, selectors for client state
- 🔗 **Integration** - Works with SAP-020 (Foundation), SAP-021 (Testing), SAP-034 (Database), SAP-035 (File Upload)

This AGENTS.md provides: Agent-specific patterns for React state management workflows.

---

## Quick Start for Agents

This SAP provides workflows for **React state management** using the three-pillar architecture:

1. **Server State** → TanStack Query v5 (API data, caching)
2. **Client State** → Zustand v4 (UI state, preferences)
3. **Form State** → React Hook Form v7 + Zod (forms with validation)

### First-Time Session

1. **Identify state type**: Server (API), Client (UI), or Form
2. **Choose appropriate tool**: TanStack Query, Zustand, or React Hook Form
3. **Install dependencies**: Use version-specific installation commands
4. **Copy templates**: Use provided templates for consistent patterns

### Key Principle

**Different types of state require different tools**. Mixing server and client state causes 30-40% of state bugs.

---

## User Signal Pattern Tables

### Table 1: State Management Setup Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Setup TanStack Query** | "Setup React Query", "Install TanStack Query", "Configure server state" | Execute Workflow 1: Install TanStack Query | TanStack Query v5 installed with QueryClient |
| **Setup Zustand** | "Add Zustand", "Setup client state", "Global state management" | Execute Workflow 2: Create Zustand Store | Zustand v4 store created for UI state |
| **Setup React Hook Form** | "Setup forms", "Add React Hook Form", "Form validation" | Execute Workflow 3: Setup React Hook Form with Zod | React Hook Form v7 + Zod validation configured |
| **Create API query** | "Fetch data from API", "Setup useQuery", "Query endpoint" | Execute Workflow 4: Create TanStack Query Hook | Custom useQuery hook for API endpoint |
| **Create form** | "Create login form", "Build registration form", "Form with validation" | Execute Workflow 5: Create Form with Validation | React Hook Form with Zod schema validation |

### Table 2: State Operation Signals

| User Intent | Example User Phrases | Agent Action | Expected Result |
|------------|---------------------|--------------|----------------|
| **Fetch data** | "Get users from API", "Fetch products", "Query data" | Use useQuery hook | Data fetched with loading/error states |
| **Mutate data** | "Update user", "Create product", "Delete item" | Use useMutation hook | Data mutated with optimistic updates |
| **Update UI state** | "Toggle sidebar", "Change theme", "Update filter" | Update Zustand store | Client state updated globally |
| **Submit form** | "Submit form", "Validate and submit", "Handle form submission" | Use handleSubmit from React Hook Form | Form validated and submitted |
| **Persist state** | "Save preferences", "Remember theme", "Store filters" | Use Zustand persist middleware | State persisted to localStorage |

---

## Workflow 1: Install TanStack Query for Server State (5-10 minutes)

**When to use**: Managing API data (fetching, caching, mutations)

**Prerequisites**:
- React 19 project (Next.js 15 or Vite 7)
- Node.js 18+ and pnpm/npm installed

**Steps**:

1. **Install TanStack Query v5**:
   ```bash
   pnpm add @tanstack/react-query@^5.73.0
   pnpm add -D @tanstack/react-query-devtools@^5.73.0
   ```

2. **Create QueryClient configuration** (`src/lib/query-client.ts`):
   ```typescript
   import { QueryClient } from '@tanstack/react-query'

   export const queryClient = new QueryClient({
     defaultOptions: {
       queries: {
         staleTime: 1000 * 60 * 5, // 5 minutes
         gcTime: 1000 * 60 * 10,   // 10 minutes (formerly cacheTime)
         retry: 3,
         retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
         refetchOnWindowFocus: false,
         refetchOnReconnect: true,
       },
       mutations: {
         retry: 1,
         retryDelay: 1000,
       },
     },
   })
   ```

3. **Create QueryProvider component** (`src/components/providers/query-provider.tsx`):
   ```typescript
   'use client'

   import { QueryClientProvider } from '@tanstack/react-query'
   import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
   import { queryClient } from '@/lib/query-client'

   export function QueryProvider({ children }: { children: React.ReactNode }) {
     return (
       <QueryClientProvider client={queryClient}>
         {children}
         <ReactQueryDevtools initialIsOpen={false} />
       </QueryClientProvider>
     )
   }
   ```

4. **Wrap app with QueryProvider**:

   **For Next.js 15** (`src/app/layout.tsx`):
   ```typescript
   import { QueryProvider } from '@/components/providers/query-provider'

   export default function RootLayout({ children }: { children: React.ReactNode }) {
     return (
       <html lang="en">
         <body>
           <QueryProvider>{children}</QueryProvider>
         </body>
       </html>
     )
   }
   ```

   **For Vite** (`src/main.tsx`):
   ```typescript
   import { QueryProvider } from './components/providers/query-provider'

   ReactDOM.createRoot(document.getElementById('root')!).render(
     <React.StrictMode>
       <QueryProvider>
         <App />
       </QueryProvider>
     </React.StrictMode>,
   )
   ```

5. **Verify installation**:
   ```bash
   pnpm dev
   # Check React Query Devtools in bottom-left corner
   ```

**Expected outcome**:
- TanStack Query v5 installed and configured
- QueryClient with production-ready defaults (5min staleTime, 3 retries)
- React Query Devtools available in development
- Ready to create useQuery hooks

**Time saved**: 1 hour (manual setup) → 5-10 minutes (template-based)

---

## Workflow 2: Create Zustand Store for Client State (5-10 minutes)

**When to use**: Managing UI state (theme, sidebar, filters, preferences)

**Prerequisites**:
- React 19 project

**Steps**:

1. **Install Zustand v4**:
   ```bash
   pnpm add zustand@^4.5.7
   ```

2. **Create basic Zustand store** (`src/stores/ui-store.ts`):
   ```typescript
   import { create } from 'zustand'
   import { persist } from 'zustand/middleware'

   interface UIState {
     // State
     theme: 'light' | 'dark'
     sidebarOpen: boolean

     // Actions
     setTheme: (theme: 'light' | 'dark') => void
     toggleSidebar: () => void
   }

   export const useUIStore = create<UIState>()(
     persist(
       (set) => ({
         // Initial state
         theme: 'light',
         sidebarOpen: true,

         // Actions
         setTheme: (theme) => set({ theme }),
         toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
       }),
       {
         name: 'ui-storage', // localStorage key
         partialize: (state) => ({ theme: state.theme }), // Only persist theme
       }
     )
   )
   ```

3. **Use store in components**:
   ```typescript
   'use client'

   import { useUIStore } from '@/stores/ui-store'

   export function Sidebar() {
     const { sidebarOpen, toggleSidebar } = useUIStore()

     return (
       <aside className={sidebarOpen ? 'open' : 'closed'}>
         <button onClick={toggleSidebar}>Toggle</button>
       </aside>
     )
   }
   ```

4. **Test store**:
   ```bash
   pnpm dev
   # Toggle sidebar, verify state persists on reload
   ```

**Expected outcome**:
- Zustand v4 store created for UI state
- Persist middleware saves theme to localStorage
- Multiple components can access/update state
- No prop drilling needed

**Time saved**: 30 minutes (manual setup) → 5-10 minutes (template-based)

---

## Workflow 3: Setup React Hook Form with Zod Validation (10-15 minutes)

**When to use**: Any form with validation (login, registration, checkout)

**Prerequisites**:
- React 19 project
- TypeScript 5.7+

**Steps**:

1. **Install React Hook Form v7 and Zod**:
   ```bash
   pnpm add react-hook-form@^7.54.2 zod@^3.24.1
   pnpm add @hookform/resolvers@^3.10.0
   ```

2. **Create Zod validation schema** (`src/features/auth/schemas/login-schema.ts`):
   ```typescript
   import { z } from 'zod'

   export const loginSchema = z.object({
     email: z
       .string()
       .min(1, 'Email is required')
       .email('Invalid email address'),
     password: z
       .string()
       .min(8, 'Password must be at least 8 characters')
       .regex(/[A-Z]/, 'Password must contain uppercase letter')
       .regex(/[a-z]/, 'Password must contain lowercase letter')
       .regex(/[0-9]/, 'Password must contain number'),
   })

   export type LoginFormData = z.infer<typeof loginSchema>
   ```

3. **Create form component** (`src/features/auth/components/login-form.tsx`):
   ```typescript
   'use client'

   import { useForm } from 'react-hook-form'
   import { zodResolver } from '@hookform/resolvers/zod'
   import { loginSchema, type LoginFormData } from '../schemas/login-schema'

   export function LoginForm() {
     const {
       register,
       handleSubmit,
       formState: { errors, isSubmitting },
     } = useForm<LoginFormData>({
       resolver: zodResolver(loginSchema),
       defaultValues: {
         email: '',
         password: '',
       },
     })

     const onSubmit = async (data: LoginFormData) => {
       try {
         const response = await fetch('/api/auth/login', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify(data),
         })
         if (!response.ok) throw new Error('Login failed')
         // Handle success (redirect, etc.)
       } catch (error) {
         console.error(error)
       }
     }

     return (
       <form onSubmit={handleSubmit(onSubmit)}>
         <div>
           <label htmlFor="email">Email</label>
           <input
             id="email"
             type="email"
             {...register('email')}
             aria-invalid={!!errors.email}
           />
           {errors.email && <p role="alert">{errors.email.message}</p>}
         </div>

         <div>
           <label htmlFor="password">Password</label>
           <input
             id="password"
             type="password"
             {...register('password')}
             aria-invalid={!!errors.password}
           />
           {errors.password && <p role="alert">{errors.password.message}</p>}
         </div>

         <button type="submit" disabled={isSubmitting}>
           {isSubmitting ? 'Logging in...' : 'Log In'}
         </button>
       </form>
     )
   }
   ```

4. **Test form validation**:
   ```bash
   pnpm dev
   # Try submitting with invalid email/password
   # Verify Zod validation errors appear
   ```

**Expected outcome**:
- React Hook Form v7 + Zod validation configured
- Type-safe form with automatic TypeScript inference
- Client-side validation before API call
- 50-70% faster than controlled forms

**Time saved**: 1 hour (manual setup) → 10-15 minutes (template-based)

---

## Workflow 4: Create TanStack Query Hook for API Endpoint (10-15 minutes)

**When to use**: Fetching data from API with caching and automatic refetching

**Prerequisites**:
- TanStack Query installed (Workflow 1)
- API endpoint available

**Steps**:

1. **Create API client** (`src/lib/api-client.ts`):
   ```typescript
   export class APIError extends Error {
     constructor(
       public status: number,
       message: string,
       public data?: unknown,
     ) {
       super(message)
       this.name = 'APIError'
     }
   }

   export async function fetchAPI<T>(
     endpoint: string,
     options?: RequestInit,
   ): Promise<T> {
     const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
       headers: {
         'Content-Type': 'application/json',
         ...options?.headers,
       },
       ...options,
     })

     if (!response.ok) {
       const error = await response.json().catch(() => ({}))
       throw new APIError(response.status, response.statusText, error)
     }

     return response.json()
   }
   ```

2. **Create query hook** (`src/features/users/queries/use-users.ts`):
   ```typescript
   import { useQuery } from '@tanstack/react-query'
   import { fetchAPI } from '@/lib/api-client'

   export interface User {
     id: string
     email: string
     name: string
   }

   export function useUsers() {
     return useQuery({
       queryKey: ['users'],
       queryFn: () => fetchAPI<User[]>('/api/users'),
       staleTime: 1000 * 60 * 5, // 5 minutes
     })
   }

   export function useUser(userId: string) {
     return useQuery({
       queryKey: ['users', userId],
       queryFn: () => fetchAPI<User>(`/api/users/${userId}`),
       enabled: !!userId, // Only run if userId provided
     })
   }
   ```

3. **Use query in component** (`src/features/users/components/user-list.tsx`):
   ```typescript
   'use client'

   import { useUsers } from '../queries/use-users'

   export function UserList() {
     const { data: users, isLoading, error } = useUsers()

     if (isLoading) return <div>Loading users...</div>
     if (error) return <div>Error: {error.message}</div>
     if (!users) return null

     return (
       <ul>
         {users.map((user) => (
           <li key={user.id}>
             {user.name} ({user.email})
           </li>
         ))}
       </ul>
     )
   }
   ```

4. **Test query**:
   ```bash
   pnpm dev
   # Verify data loads, caches for 5 minutes
   # Check React Query Devtools for cache status
   ```

**Expected outcome**:
- Custom useUsers and useUser hooks
- Automatic caching (5 minute staleTime)
- Loading/error states handled
- Type-safe API responses

**Time saved**: 30-45 minutes (manual setup) → 10-15 minutes (template-based)

---

## Workflow 5: Create Mutation with Optimistic Updates (15-20 minutes)

**When to use**: Creating, updating, or deleting data with instant UI feedback

**Prerequisites**:
- TanStack Query installed (Workflow 1)
- Query hook created (Workflow 4)

**Steps**:

1. **Create mutation hook** (`src/features/users/mutations/use-create-user.ts`):
   ```typescript
   import { useMutation, useQueryClient } from '@tanstack/react-query'
   import { fetchAPI } from '@/lib/api-client'
   import type { User } from '../queries/use-users'

   interface CreateUserInput {
     email: string
     name: string
   }

   export function useCreateUser() {
     const queryClient = useQueryClient()

     return useMutation({
       mutationFn: (input: CreateUserInput) =>
         fetchAPI<User>('/api/users', {
           method: 'POST',
           body: JSON.stringify(input),
         }),

       // Optimistic update
       onMutate: async (newUser) => {
         // Cancel outgoing refetches
         await queryClient.cancelQueries({ queryKey: ['users'] })

         // Snapshot previous value
         const previousUsers = queryClient.getQueryData<User[]>(['users'])

         // Optimistically update cache
         queryClient.setQueryData<User[]>(['users'], (old) => [
           ...(old || []),
           { id: 'temp-id', ...newUser }, // Temporary ID
         ])

         // Return context with snapshot
         return { previousUsers }
       },

       // On success, replace temp ID with real ID
       onSuccess: (newUser) => {
         queryClient.setQueryData<User[]>(['users'], (old) =>
           old?.map((user) =>
             user.id === 'temp-id' ? newUser : user
           )
         )
       },

       // On error, rollback
       onError: (error, newUser, context) => {
         if (context?.previousUsers) {
           queryClient.setQueryData(['users'], context.previousUsers)
         }
       },

       // Always refetch after mutation
       onSettled: () => {
         queryClient.invalidateQueries({ queryKey: ['users'] })
       },
     })
   }
   ```

2. **Use mutation in component** (`src/features/users/components/create-user-form.tsx`):
   ```typescript
   'use client'

   import { useForm } from 'react-hook-form'
   import { useCreateUser } from '../mutations/use-create-user'

   interface CreateUserFormData {
     email: string
     name: string
   }

   export function CreateUserForm() {
     const { register, handleSubmit, reset } = useForm<CreateUserFormData>()
     const createUser = useCreateUser()

     const onSubmit = (data: CreateUserFormData) => {
       createUser.mutate(data, {
         onSuccess: () => {
           reset()
           alert('User created!')
         },
         onError: (error) => {
           alert(`Error: ${error.message}`)
         },
       })
     }

     return (
       <form onSubmit={handleSubmit(onSubmit)}>
         <input {...register('email')} placeholder="Email" required />
         <input {...register('name')} placeholder="Name" required />
         <button type="submit" disabled={createUser.isPending}>
           {createUser.isPending ? 'Creating...' : 'Create User'}
         </button>
       </form>
     )
   }
   ```

3. **Test optimistic update**:
   ```bash
   pnpm dev
   # Create user, verify instant UI update
   # Disable network, create user, see rollback on error
   ```

**Expected outcome**:
- Optimistic updates (instant UI feedback)
- Automatic rollback on error
- Cache invalidation after mutation
- 90% perceived performance improvement

**Time saved**: 1-2 hours (manual implementation) → 15-20 minutes (template-based)

---

## Best Practices

### 1. Separate Server State from Client State

**Pattern**:
```typescript
// ✅ GOOD: Server state with TanStack Query
const { data: users } = useUsers()

// ✅ GOOD: Client state with Zustand
const { theme } = useUIStore()

// ❌ BAD: Mixing in useState
const [users, setUsers] = useState([])  // Should use TanStack Query
const [theme, setTheme] = useState('light')  // Should use Zustand
```

**Why**: TanStack Query handles caching, refetching, retries automatically. Zustand provides global state without prop drilling.

---

### 2. Use Zod for Type-Safe Form Validation

**Pattern**:
```typescript
// ✅ GOOD: Zod schema with automatic TypeScript types
const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})
type LoginFormData = z.infer<typeof loginSchema>

// ❌ BAD: Manual validation with any
const validate = (data: any) => {
  if (!data.email) return 'Email required'
  // Runtime errors, no type safety
}
```

**Why**: Zod provides runtime validation + TypeScript types from single source of truth.

---

### 3. Use Optimistic Updates for Instant UX

**Pattern**:
```typescript
// ✅ GOOD: Optimistic update
useMutation({
  onMutate: async (newItem) => {
    await queryClient.cancelQueries({ queryKey: ['items'] })
    const previous = queryClient.getQueryData(['items'])
    queryClient.setQueryData(['items'], (old) => [...old, newItem])
    return { previous }
  },
  onError: (err, newItem, context) => {
    queryClient.setQueryData(['items'], context.previous)
  },
})

// ❌ BAD: Wait for server response
useMutation({
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['items'] })
  },
})
```

**Why**: Optimistic updates provide instant feedback (perceived 90% faster).

---

### 4. Use Query Keys for Cache Management

**Pattern**:
```typescript
// ✅ GOOD: Hierarchical query keys
queryKey: ['users']           // List
queryKey: ['users', userId]   // Detail
queryKey: ['users', userId, 'posts']  // Nested

// Invalidate all users queries
queryClient.invalidateQueries({ queryKey: ['users'] })

// ❌ BAD: Flat query keys
queryKey: ['usersList']
queryKey: ['userDetail']
// Hard to invalidate related queries
```

**Why**: Hierarchical keys enable targeted cache invalidation.

---

### 5. Persist UI State with Zustand Middleware

**Pattern**:
```typescript
// ✅ GOOD: Persist middleware
export const useUIStore = create<UIState>()(
  persist(
    (set) => ({ theme: 'light', setTheme: (theme) => set({ theme }) }),
    { name: 'ui-storage', partialize: (state) => ({ theme: state.theme }) }
  )
)

// ❌ BAD: Manual localStorage
const [theme, setTheme] = useState(() => {
  return localStorage.getItem('theme') || 'light'
})
useEffect(() => {
  localStorage.setItem('theme', theme)
}, [theme])
```

**Why**: Zustand persist middleware handles SSR hydration, serialization automatically.

---

## Common Pitfalls

### Pitfall 1: Mixing Server and Client State in useState

**Problem**: Use useState for API data, causing cache duplication and stale data

**Symptom**: Data refetched on every mount, no caching, inconsistent state

**Fix**: Use TanStack Query for server state
```typescript
// ❌ BAD: Server state in useState
const [users, setUsers] = useState([])
useEffect(() => {
  fetch('/api/users').then((res) => res.json()).then(setUsers)
}, [])

// ✅ GOOD: Server state with TanStack Query
const { data: users } = useUsers()
```

**Why**: TanStack Query provides caching, refetching, retry logic automatically

---

### Pitfall 2: Not Using Optimistic Updates for Mutations

**Problem**: Wait for server response before updating UI, slow UX

**Symptom**: 1-2 second delay before UI updates, feels sluggish

**Fix**: Use onMutate for optimistic updates
```typescript
// ❌ BAD: Wait for server
useMutation({
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
})

// ✅ GOOD: Optimistic update
useMutation({
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] })
    const previous = queryClient.getQueryData(['todos'])
    queryClient.setQueryData(['todos'], (old) => [...old, newTodo])
    return { previous }
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previous)
  },
})
```

**Why**: Optimistic updates provide instant feedback (90% perceived improvement)

---

### Pitfall 3: Using Controlled Forms for All Inputs

**Problem**: Use useState for every form input, 50-70% performance penalty

**Symptom**: Slow typing, lag on complex forms

**Fix**: Use React Hook Form with uncontrolled inputs
```typescript
// ❌ BAD: Controlled inputs (re-render on every keystroke)
const [email, setEmail] = useState('')
<input value={email} onChange={(e) => setEmail(e.target.value)} />

// ✅ GOOD: Uncontrolled inputs with React Hook Form
const { register } = useForm()
<input {...register('email')} />
```

**Why**: Uncontrolled inputs don't trigger re-renders on every keystroke

---

### Pitfall 4: Not Using Zod Schema for Validation

**Problem**: Manual validation logic, runtime errors, no type safety

**Symptom**: TypeScript types don't match validation, bugs in production

**Fix**: Use Zod schema with zodResolver
```typescript
// ❌ BAD: Manual validation
const onSubmit = (data) => {
  if (!data.email) return alert('Email required')
  if (!data.email.includes('@')) return alert('Invalid email')
  // Runtime errors, no type safety
}

// ✅ GOOD: Zod schema
const loginSchema = z.object({
  email: z.string().email('Invalid email'),
})
type LoginFormData = z.infer<typeof loginSchema>

const { handleSubmit } = useForm<LoginFormData>({
  resolver: zodResolver(loginSchema),
})
```

**Why**: Zod provides runtime validation + TypeScript types from single source

---

### Pitfall 5: Not Persisting UI State with Zustand

**Problem**: UI state (theme, preferences) lost on page reload

**Symptom**: User sets dark theme, reloads page, reverts to light theme

**Fix**: Use Zustand persist middleware
```typescript
// ❌ BAD: No persistence
export const useUIStore = create<UIState>((set) => ({
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}))

// ✅ GOOD: Persist to localStorage
export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      theme: 'light',
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'ui-storage' }
  )
)
```

**Why**: Persist middleware handles SSR hydration, serialization automatically

---

## Support & Resources

**SAP-023 Documentation**:
- [Capability Charter](capability-charter.md) - React state management problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts for TanStack Query, Zustand, React Hook Form
- [Awareness Guide](awareness-guide.md) - Detailed workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**External Resources**:
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Zustand Docs](https://zustand-demo.pmnd.rs)
- [React Hook Form Docs](https://react-hook-form.com)
- [Zod Docs](https://zod.dev)

**Related SAPs**:
- [SAP-020 (react-foundation)](../react-foundation/) - React project setup
- [SAP-021 (react-testing)](../react-testing/) - Testing patterns
- [SAP-022 (react-linting)](../react-linting/) - Linting and formatting
- [SAP-024 (react-styling)](../react-styling/) - Styling strategies

---

## Version History

- **1.0.0** (2025-11-05): Initial AGENTS.md for SAP-023
  - 5 workflows: Install TanStack Query, Create Zustand Store, Setup React Hook Form with Zod, Create TanStack Query Hook, Create Mutation with Optimistic Updates
  - 2 user signal pattern tables: State Management Setup Signals, State Operation Signals
  - 5 best practices: Separate server/client state, Zod validation, optimistic updates, query keys, persist middleware
  - 5 common pitfalls: Mixing state types, no optimistic updates, controlled forms, manual validation, not persisting UI state
  - Focus on three-pillar architecture (server/client/form state)

---

**Next Steps**:
1. Review [protocol-spec.md](protocol-spec.md) for technical contracts
2. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
3. Install: `pnpm add @tanstack/react-query zustand react-hook-form zod`
4. Choose template based on state type (server, client, or form)
