---
name: react-design-mean
description: "React frontend architecture for MEAN stack apps. Use when designing component trees, page layouts, routing strategies, state management, and UI patterns for React applications."
---

# React Design Mean

## Purpose

Design React frontend architectures for MEAN stack applications. Produce component hierarchies, page layouts, routing plans, state management strategies, and UI patterns that frontend developers implement directly.

## Key Patterns

### Component Architecture (Atomic Design)
- Atoms: Button, Input, Spinner, Badge
- Molecules: SearchBar, FormField, NavLink
- Organisms: Navbar, UserCard, PostList, CommentForm
- Templates: DashboardLayout, PublicLayout
- Pages: HomePage, LoginPage, DashboardPage

### Folder Structure
- src/components/common/ — Reusable atoms + molecules
- src/components/layout/ — Layout components (Navbar, Sidebar, Footer, PageWrapper)
- src/components/features/ — Feature-specific organisms
- src/pages/ — One per route
- src/hooks/ — Custom hooks (useAuth, useFetch, useForm)
- src/context/ — React Context providers
- src/services/ — API client and service layer
- src/utils/ — Utility functions
- src/constants/ — App-wide constants

### Routing Strategy (React Router v6)
- Public routes wrapped in PublicLayout (Navbar + Footer)
- Protected routes wrapped in ProtectedRoute + DashboardLayout
- Nested layouts using Outlet
- 404 catch-all route

### State Management Strategy
- Local state: useState for component-specific state
- Context API: useContext for global lightweight state (auth, theme)
- Server state: Custom useFetch hook for API data (caching, loading, error)
- URL state: useSearchParams for filters, pagination, search

### Auth Pattern
- AuthContext provides: user, login(), logout(), isAuthenticated
- ProtectedRoute checks auth and redirects to /login
- API interceptor attaches JWT token to every request
- Token refresh handled transparently in interceptor

## Conventions

- Functional components only — no class components
- File naming: PascalCase for components, camelCase for hooks/utils
- One component per file, co-locate styles and tests
- Custom hooks prefix with "use"
- Pages are thin — compose feature components, don't contain business logic
- Loading states: every async operation shows a spinner/skeleton
- Error states: every data fetch has error UI with retry option
- Empty states: every list has an empty state message
- Responsive design: mobile-first approach

## Knowledge Strategy

- **Patterns to capture:** Component hierarchies that scaled well, routing patterns, state management decisions
- **Examples to collect:** Page layouts, auth flow implementations, reusable hook patterns
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
