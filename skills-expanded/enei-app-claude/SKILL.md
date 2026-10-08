# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

Package manager is **pnpm** (not npm/yarn).

```bash
pnpm dev              # Start development server
pnpm build            # Production build (injects NEXT_PUBLIC_COMMIT_HASH and NEXT_PUBLIC_BUILD_TIME)
pnpm start            # Start production server
pnpm lint             # ESLint
pnpm test             # Jest tests
pnpm test -- --testPathPattern="UserBill"  # Run tests matching a pattern
pnpm test:watch       # Watch mode
pnpm test:coverage    # Coverage report (70% threshold on branches/functions/lines/statements)
pnpm codegen          # Generate GraphQL types (requires enei-api running on localhost:3004)
```

## Path Aliases

Defined in `tsconfig.json` and mirrored in `jest.config.js`:

| Alias | Path |
|-------|------|
| `@components/*` | `components/*` |
| `@core/*` | `core/*` |
| `@utils/*` | `utils/*` |
| `@config/*` | `config/*` |
| `@styles/*` | `styles/*` |
| `@public/*` | `public/*` |

## Architecture

Next.js 15 + React 18 + TypeScript (strict mode) application for Taiwan energy billing management. Uses Apollo Client for GraphQL, Material-UI for UI, React Hook Form + Yup for forms.

### GraphQL Integration

- **Codegen**: `pnpm codegen` generates types in `core/graphql/types.ts` and fragment matchers in `core/graphql/possibleTypes.ts` from the API schema at `http://localhost:3004/graphql` (codegen.yml). The API must be running locally.
- **Operations**: `core/graphql/queries/` (33 files), `core/graphql/mutations/` (48 files), `core/graphql/fragment/` (19 fragments)
- **Apollo Client**: Configured in `core/graphql/index.ts` with `offsetLimitPagination` cache policies for 14+ paginated query types. Uses `credentials: 'include'` for cookie-based auth.
- **Custom hooks**: `utils/hooks/queries/` and `utils/hooks/mutations/` wrap Apollo operations. Base `useQuery` (in `utils/hooks/useQuery.ts`) auto-shows `toast.error` on errors. Base `useMutation` (in `utils/hooks/useMutation.ts`) enables `awaitRefetchQueries`.
- **Pattern**: Queries use fragment-based composition (`gql` template with `${FRAGMENT}` interpolation).

### Component Patterns

Components are organized by domain under `components/`. Consistent naming:

- `[Feature].tsx` — main component
- `[Feature]Dialog.tsx` — create/edit dialog (wraps content in `DialogErrorBoundary`)
- `[Feature]Panel.tsx` — list/table view with pagination and search
- `[Feature]ConfigDialog/` — sub-feature configuration
- `__tests__/` — component tests

Dialog components follow this pattern: `DialogErrorBoundary` wrapper → GraphQL data fetch → React Hook Form with Yup resolver → MUI `Controller` fields → mutation on submit with toast notifications.

### Form Handling

- Declarative field configs in `core/fieldConfigs/` define form fields with type, validation, and rendering info
- `utils/hooks/useValidatedForm.ts` — integrates React Hook Form with Yup
- `utils/hooks/useCreateOrUpdate.ts` — handles create vs edit mode switching
- Field types defined in `core/types/fieldConfig.ts` (14 types including TEXT, DATE, NUMBER, SELECT, etc.)
- Includes Taiwan-specific validators: UBN (統一編號), phone numbers

### Authentication

- `core/context/auth/` — `AuthProvider` with reducer pattern, ME query polls hourly
- `components/AuthGuard.tsx` — role-based access control wrapper
- JWT via cookies (credentials: 'include'), automatic logout on auth errors

### State Management

- **Server state**: Apollo Client cache (no Redux)
- **Auth state**: React Context (`core/context/auth/`)
- **Task progress**: React Context (`core/context/task-progress/`)
- **Local state**: React hooks

### Testing

- Jest + React Testing Library with jsdom environment
- Test utilities in `utils/test-utils.tsx` — custom `render` with Apollo MockedProvider, `createMockResponse` helper
- Setup in `jest.setup.ts` — mocks for Next.js router, `window.matchMedia`, `IntersectionObserver`, `react-toastify`, `react-to-print`
- Test files go in `__tests__/` directories or as `.test.tsx` files

### Key Environment Variables

- `NEXT_PUBLIC_API_BASE_URL` — GraphQL API endpoint (default: `http://localhost:3004` for local, staging uses `https://api-staging.annealenergy.com`)
- `ANALYZE=true` — enables webpack bundle analyzer

### Other Notes

- Business logic comments are in 繁體中文 (Traditional Chinese); code and variable names in English
- `date-fns` pinned to v2 due to MUI date picker compatibility
- SVG imports as React components via `@svgr/webpack` (configured in `next.config.js`)
- `ahooks` package is transpiled in Next.js config
- Toast notifications via `react-toastify`
- Route transition progress bar via `nprogress`
