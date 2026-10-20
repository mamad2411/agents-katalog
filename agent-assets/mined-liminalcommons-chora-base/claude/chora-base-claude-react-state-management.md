---
sap_id: SAP-023
version: 1.0.0
status: active
last_updated: 2025-11-05
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 9
progressive_loading:
  phase_1: "lines 1-200"   # Quick Start + Core Workflows
  phase_2: "lines 201-350" # Advanced Patterns
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 4000
phase_2_token_estimate: 8000
phase_3_token_estimate: 11000
---

# React State Management Patterns (SAP-023) - Claude-Specific Awareness

**SAP ID**: SAP-023
**Claude Compatibility**: Sonnet 4.5+
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

This CLAUDE.md provides: Claude Code-specific workflows using Bash (installation), Write (hooks/stores), Read (verification).

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for React state management with the three-pillar architecture:

1. **Server State** → TanStack Query v5
2. **Client State** → Zustand v4
3. **Form State** → React Hook Form v7 + Zod

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic state management workflows
2. Use this file for Claude Code tool integration (Bash for installation, Write for hooks/stores, Read for verification)
3. Always identify state type (server/client/form) before choosing tool

### State Classification Commands

```bash
# Install TanStack Query (server state)
Bash: pnpm add @tanstack/react-query@^5.73.0

# Install Zustand (client state)
Bash: pnpm add zustand@^4.5.7

# Install React Hook Form + Zod (form state)
Bash: pnpm add react-hook-form@^7.54.2 zod@^3.24.1
```

---

## Claude Code React State Management Workflows

### Workflow 1: Installing TanStack Query with Bash and Write

```markdown
User: "Setup TanStack Query for API data"

Claude (Phase 1: Install Dependencies - 0-5k tokens):
1. Install TanStack Query:
   Bash: pnpm add @tanstack/react-query@^5.73.0 @tanstack/react-query-devtools@^5.73.0

Claude (Phase 2: Create QueryClient - 5-15k tokens):
2. Create QueryClient configuration:
   Write src/lib/query-client.ts
   ```typescript
   import { QueryClient } from '@tanstack/react-query'

   export const queryClient = new QueryClient({
     defaultOptions: {
       queries: {
         staleTime: 1000 * 60 * 5, // 5 minutes
         gcTime: 1000 * 60 * 10,   // 10 minutes
         retry: 3,
         refetchOnWindowFocus: false,
         refetchOnReconnect: true,
       },
       mutations: {
         retry: 1,
       },
     },
   })
   ```

3. Create QueryProvider component:
   Write src/components/providers/query-provider.tsx
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

Claude (Phase 3: Integrate Provider - 15-25k tokens):
4. Read current layout file:
   Read src/app/layout.tsx

5. Add QueryProvider to layout:
   Edit src/app/layout.tsx
   # Wrap children with <QueryProvider>

6. Verify installation:
   Bash: pnpm dev
   # Check for React Query Devtools in bottom-left corner

Claude (response to user):
"✅ TanStack Query v5 installed!

**Installed**:
- @tanstack/react-query 5.73.0
- React Query Devtools (dev only)

**Configuration**:
- src/lib/query-client.ts - QueryClient with 5min staleTime, 3 retries
- src/components/providers/query-provider.tsx - Provider component
- App wrapped with QueryProvider

**Default behavior**:
- Data cached for 5 minutes (staleTime)
- Automatic retries (3 attempts)
- No refetch on window focus (better UX)

**Next steps**:
1. Create useQuery hooks for API endpoints
2. Add mutations with optimistic updates
3. Use React Query Devtools to inspect cache"

Result: TanStack Query v5 installed and configured, ready for API data management
```

---

### Workflow 2: Creating Zustand Store with Write

```markdown
User: "Create Zustand store for theme and sidebar state"

Claude (Phase 1: Install Zustand - 0-5k tokens):
1. Install Zustand:
   Bash: pnpm add zustand@^4.5.7

Claude (Phase 2: Create Store - 5-20k tokens):
2. Create Zustand store with persist middleware:
   Write src/stores/ui-store.ts
   ```typescript
   import { create } from 'zustand'
   import { persist } from 'zustand/middleware'

   interface UIState {
     theme: 'light' | 'dark'
     sidebarOpen: boolean
     setTheme: (theme: 'light' | 'dark') => void
     toggleSidebar: () => void
   }

   export const useUIStore = create<UIState>()(
     persist(
       (set) => ({
         theme: 'light',
         sidebarOpen: true,
         setTheme: (theme) => set({ theme }),
         toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
       }),
       {
         name: 'ui-storage',
         partialize: (state) => ({ theme: state.theme }),
       }
     )
   )
   ```

Claude (Phase 3: Test Store - 20-30k tokens):
3. Create example component to test store:
   Write src/components/theme-toggle.tsx
   ```typescript
   'use client'

   import { useUIStore } from '@/stores/ui-store'

   export function ThemeToggle() {
     const { theme, setTheme } = useUIStore()

     return (
       <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
         {theme === 'light' ? '🌙' : '☀️'}
       </button>
     )
   }
   ```

4. Verify store works:
   Bash: pnpm dev
   # Toggle theme, verify persists on reload

Claude (response to user):
"✅ Zustand store created!

**Store**: src/stores/ui-store.ts
- Theme state (light/dark)
- Sidebar state (open/closed)
- Persist middleware (saves theme to localStorage)

**Usage**:
```typescript
import { useUIStore } from '@/stores/ui-store'

const { theme, setTheme } = useUIStore()
```

**Benefits**:
- No prop drilling (global state)
- Persistent theme (localStorage)
- Simple API (no reducers, no actions)
- Type-safe with TypeScript

**Test**: Theme toggle component created, verify theme persists on reload"

Result: Zustand v4 store created for UI state, theme persists to localStorage
```

---

### Workflow 3: Creating React Hook Form with Zod using Write

```markdown
User: "Create login form with email/password validation"

Claude (Phase 1: Install Dependencies - 0-5k tokens):
1. Install React Hook Form and Zod:
   Bash: pnpm add react-hook-form@^7.54.2 zod@^3.24.1 @hookform/resolvers@^3.10.0

Claude (Phase 2: Create Zod Schema - 5-15k tokens):
2. Create Zod validation schema:
   Write src/features/auth/schemas/login-schema.ts
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
       .regex(/[0-9]/, 'Password must contain number'),
   })

   export type LoginFormData = z.infer<typeof loginSchema>
   ```

Claude (Phase 3: Create Form Component - 15-35k tokens):
3. Create login form component:
   Write src/features/auth/components/login-form.tsx
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
     })

     const onSubmit = async (data: LoginFormData) => {
       const response = await fetch('/api/auth/login', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(data),
       })
       if (!response.ok) throw new Error('Login failed')
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

4. Test form validation:
   Bash: pnpm dev
   # Try invalid email/password, verify Zod validation

Claude (response to user):
"✅ Login form with Zod validation created!

**Files created**:
- src/features/auth/schemas/login-schema.ts - Zod schema
- src/features/auth/components/login-form.tsx - Form component

**Validation rules**:
- Email: Required, valid email format
- Password: Min 8 chars, uppercase + number required

**Benefits**:
- Type-safe form with automatic TypeScript inference
- Client-side validation before API call
- 50-70% faster than controlled forms (uncontrolled inputs)
- Single source of truth (Zod schema → TypeScript types)

**Test**: Try submitting with invalid data to see Zod validation errors"

Result: Login form with Zod validation created, type-safe and performant
```

---

## Claude-Specific Tips

### Tip 1: Always Read Layout Before Adding QueryProvider

**Pattern**:
```markdown
# Before adding QueryProvider:
Read src/app/layout.tsx
# Check existing providers, structure

# Then add QueryProvider:
Edit src/app/layout.tsx
# Wrap children with <QueryProvider>
```

**Why**: Preserve existing provider structure, avoid breaking changes

---

### Tip 2: Use Write for New Stores/Hooks, Read Before Editing

**Pattern**:
```markdown
# New store → Use Write:
Write src/stores/ui-store.ts
# Full store implementation

# Modify existing store → Read then Edit:
Read src/stores/ui-store.ts
Edit src/stores/ui-store.ts
# old_string: theme: 'light'
# new_string: theme: 'dark'
```

**Why**: Write for new files, Edit for targeted changes

---

### Tip 3: Test State Management Immediately with Bash

**Pattern**:
```markdown
# After creating store/hook:
Write src/stores/ui-store.ts

# Immediately test:
Bash: pnpm dev

# Verify in browser:
# - Toggle theme
# - Check localStorage
# - Reload page to verify persistence
```

**Why**: Catch configuration errors early

---

### Tip 4: Create Zod Schema Before Form Component

**Pattern**:
```markdown
# Step 1: Zod schema first
Write src/features/auth/schemas/login-schema.ts
# Define validation rules

# Step 2: Form component second
Write src/features/auth/components/login-form.tsx
# Import schema, use zodResolver
```

**Why**: Schema defines types, form component uses inferred types

---

### Tip 5: Use Bash to Verify React Query Devtools

**Pattern**:
```markdown
# After installing TanStack Query:
Bash: pnpm dev

# Check console output for:
# "React Query Devtools installed"

# Verify in browser:
# - Look for React Query icon in bottom-left corner
# - Click to open devtools panel
```

**Why**: Devtools critical for debugging cache, queries, mutations

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Wrapping App with QueryProvider

**Problem**: Install TanStack Query but forget to add QueryProvider

**Fix**: Always read and edit layout file
```markdown
# ❌ BAD: Install but don't add provider
Bash: pnpm add @tanstack/react-query
Write src/lib/query-client.ts
# Forget to wrap app

# ✅ GOOD: Install and add provider
Bash: pnpm add @tanstack/react-query
Write src/lib/query-client.ts
Read src/app/layout.tsx
Edit src/app/layout.tsx
# Add <QueryProvider>
```

**Why**: TanStack Query requires QueryProvider to work

---

### Pitfall 2: Using Edit Instead of Write for New Stores

**Problem**: Try to edit non-existent store file

**Fix**: Use Write for new files
```markdown
# ❌ BAD: Edit non-existent file
Edit src/stores/ui-store.ts
# File doesn't exist, error

# ✅ GOOD: Write new file
Write src/stores/ui-store.ts
# Create complete store
```

**Why**: Edit requires existing file

---

### Pitfall 3: Not Installing @hookform/resolvers for Zod

**Problem**: Install react-hook-form and zod, forget @hookform/resolvers

**Fix**: Install all three packages
```markdown
# ❌ BAD: Missing resolver
Bash: pnpm add react-hook-form zod
# zodResolver won't work

# ✅ GOOD: Install resolver
Bash: pnpm add react-hook-form zod @hookform/resolvers
```

**Why**: zodResolver requires @hookform/resolvers package

---

### Pitfall 4: Creating Form Without Zod Schema First

**Problem**: Create form component, then add Zod validation later

**Fix**: Create schema first, form second
```markdown
# ❌ BAD: Form first, schema later
Write src/features/auth/components/login-form.tsx
Write src/features/auth/schemas/login-schema.ts
# Types don't match, need to refactor

# ✅ GOOD: Schema first, form second
Write src/features/auth/schemas/login-schema.ts
Write src/features/auth/components/login-form.tsx
# Import LoginFormData type from schema
```

**Why**: Schema defines types, form uses inferred types

---

### Pitfall 5: Not Testing Store Persistence After Creation

**Problem**: Create Zustand store with persist middleware, don't test

**Fix**: Verify persistence works
```markdown
# After creating store:
Write src/stores/ui-store.ts

# Test persistence:
Bash: pnpm dev
# Toggle theme in browser
# Reload page
# Verify theme persists
```

**Why**: Persist middleware can silently fail with SSR

---

## Support & Resources

**SAP-023 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic React state management workflows
- [Capability Charter](capability-charter.md) - React state management problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contracts and patterns
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

- **1.0.0** (2025-11-05): Initial CLAUDE.md for SAP-023
  - 3 workflows: Installing TanStack Query with Bash/Write, Creating Zustand Store with Write, Creating React Hook Form with Zod using Write
  - Tool patterns: Bash for installation and testing, Write for stores/hooks/components, Read for layout verification, Edit for provider integration
  - 5 Claude-specific tips: Read layout before adding provider, Write for new stores and Read before editing, test immediately with Bash, create Zod schema first, verify React Query Devtools
  - 5 common pitfalls: Not wrapping app with QueryProvider, using Edit for new stores, not installing resolvers, creating form without schema, not testing persistence
  - Focus on three-pillar state architecture (server/client/form)

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic React state management workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [adoption-blueprint.md](adoption-blueprint.md) for installation
4. Install: `pnpm add @tanstack/react-query zustand react-hook-form zod`
