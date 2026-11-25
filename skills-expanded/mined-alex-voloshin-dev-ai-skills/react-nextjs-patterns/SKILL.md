---
name: react-nextjs-patterns
description: Use this skill when the agent is implementing frontend code in Next.js projects, reviewing React or Next.js pull requests, onboarding to App Router conventions, or designing a frontend architecture that needs canonical React/Next.js patterns — for canonical React and Next.js conventions covering Next.js App Router routing and rendering, React Server Components vs Client Components boundary, TypeScript strict-mode discipline, Tailwind CSS and shadcn/ui styling, React Query and Server Actions data fetching, Core Web Vitals performance optimization, WCAG 2.2 accessibility, Next.js metadata API and structured data for SEO, unit testing with Vitest and React Testing Library, and end-to-end testing with Playwright.
disable-model-invocation: true
---

# React + Next.js Patterns

Knowledge layer for the `frontend-engineer` agent and any other agent or skill that needs canonical React and Next.js conventions. Auto-loaded via the `skills:` frontmatter on `frontend-engineer`. Read this when authoring, reviewing, or onboarding to Next.js App Router code — it codifies routing, RSC vs Client Component boundaries, TypeScript discipline, styling, data fetching, performance, accessibility, SEO, and testing patterns used across the project.

## Project Architecture (Next.js App Router)

- Use the `app/` directory with file-based routing: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`
- Group related routes with `(group)` folders — no URL impact, clean organization
- Use `route.ts` for API endpoints (GET, POST, PUT, DELETE, PATCH handlers)
- Dynamic routes: `[param]` for single, `[...param]` for catch-all, `[[...param]]` for optional catch-all
- Parallel routes (`@slot`) and intercepting routes (`(.)`, `(..)`) for modals and complex layouts
- `middleware.ts` at project root for auth guards, redirects, headers, i18n

## React Server Components

Decision tree — Server Component by default; switch to Client Component only when one of the following is required:

- `useState`, `useReducer`, or any other React state hook
- `useEffect` or other browser-lifecycle hooks
- Event handlers (`onClick`, `onChange`, etc.)
- Browser APIs (`window`, `document`, `localStorage`, `IntersectionObserver`)
- Third-party libraries that depend on the above

Rendering rules:

- **Server Components**: default. Async data fetching, zero client JS, direct database/API access
- **Client Components**: `'use client'` directive at the narrowest boundary — push it down to leaf components, never wrap entire pages
- **Streaming**: use `loading.tsx` and `<Suspense>` to progressively render UI. Wrap slow data-dependent sections in Suspense boundaries
- **Server Actions**: `'use server'` for form mutations and data writes. Validate all inputs with Zod. Use `revalidatePath()` / `revalidateTag()` after mutations
- **Static vs Dynamic**: prefer static generation. Use `dynamic = 'force-dynamic'` or `revalidate` only when data must be fresh
- **Hybrid pattern**: server parent fetches data, passes serializable props to a client child that needs interactivity

## TypeScript Patterns

- Enable `strict: true`, `noUncheckedIndexedAccess: true` in `tsconfig.json`
- No `any` — use `unknown`, strict generics, or explicit types
- Define explicit return types for functions and components
- Use discriminated unions for state machines and API responses
- Prefer `interface` for object shapes, `type` for unions and intersections
- Use the `satisfies` operator for type-safe configuration objects
- Zod for runtime validation of external data (API responses, form inputs, URL params, Server Action inputs)
- Group imports: `react` → `next` → third-party → `@/` local → relative

## React Component Patterns

- Functional components only — no class components
- Destructure props with a TypeScript interface
- Use `forwardRef` when wrapping native elements or building design-system components
- Composition over configuration: use `children`, render props, or slots instead of complex prop APIs
- Co-locate component, types, and test in the same directory

State management:

- Local state: `useState` for simple values, `useReducer` for complex state logic
- URL state: `useSearchParams`, `usePathname`, `useRouter` from `next/navigation`
- Server state: React Query (`@tanstack/react-query`) with `useQuery`, `useMutation`, `useInfiniteQuery`
- Global state: React Context for theme/auth. Avoid Context for frequently changing data — use React Query or Zustand
- Form state: React Hook Form + Zod resolver for complex forms; Server Actions with `useActionState` for simple forms

Hooks:

- Custom hooks: prefix with `use`, single responsibility, return typed values
- Never call hooks conditionally
- Cleanup effects: always return a cleanup function in `useEffect` when subscribing to external resources
- Prefer `useMemo`/`useCallback` only when profiling shows a measurable benefit — do not optimize prematurely

## Styling (Tailwind + shadcn/ui)

- **Tailwind CSS**: utility-first. Use `cn()` helper (from `clsx` + `tailwind-merge`) for conditional classes. No inline styles.
- **shadcn/ui**: default component library. Customize via Tailwind theme, not component internals
- **Responsive**: mobile-first breakpoints (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`)
- **Dark mode**: `class` strategy with `next-themes`. Design for both light and dark from the start
- **Design tokens**: define colors, spacing, typography in `tailwind.config.ts` or CSS variables
- **Animations**: prefer CSS transitions and `tailwindcss-animate`. Use Framer Motion only for complex choreography

## Data Fetching (React Query + Server Actions)

- **Server Components**: `fetch()` with built-in Next.js caching and revalidation, or direct DB/ORM calls
- **Route Handlers**: `app/api/**/route.ts` — use for webhook endpoints, third-party integrations, client-side API calls
- **React Query**: wrap app in `QueryClientProvider`. Place query hooks in `hooks/` directory. Use query key factories: `['entity', params]`
- **Server Actions**: for mutations (create, update, delete). Validate with Zod. Return typed result objects, not raw data. Use `revalidatePath` / `revalidateTag` to invalidate cache
- **Error handling**: use `error.tsx` boundaries. Return structured errors from API routes (`{ error: string, code: number }`)
- **Loading states**: `loading.tsx` for route-level, `<Suspense fallback={...}>` for component-level
- **No data fetching in Client Components**: fetch in Server Components or Route Handlers; pass data down as serializable props

## Performance (Core Web Vitals)

- **LCP** (Largest Contentful Paint): optimize hero images with `next/image` `priority` prop. Preload critical fonts via `next/font`
- **INP** (Interaction to Next Paint): keep Client Components small. Defer non-critical JS with `next/dynamic` + `ssr: false`
- **CLS** (Cumulative Layout Shift): reserve space for dynamic content. Set explicit image dimensions — `next/image` with `width`/`height` or `fill`

Optimization checklist:

- Minimize `'use client'` surface — push it down to leaf components
- `next/dynamic` for heavy components not needed on initial render
- `React.lazy` + `Suspense` for code splitting within Client Components
- Images: `next/image` with responsive `sizes`, WebP/AVIF formats, `placeholder="blur"`
- Bundle analysis: `@next/bundle-analyzer` to identify large dependencies
- Prefetch: `<Link>` prefetches by default in viewport. Disable with `prefetch={false}` for low-priority links

## Accessibility (WCAG 2.2 AA)

- Semantic HTML: `<main>`, `<nav>`, `<section>`, `<article>`, `<header>`, `<footer>`, `<button>`, `<a>`
- All interactive elements keyboard-navigable (Tab, Enter, Escape, Arrow keys)
- ARIA attributes only when semantic HTML is insufficient — prefer native elements
- Color contrast: minimum 4.5:1 for normal text, 3:1 for large text
- Focus management: visible focus indicators, trap focus in modals, restore focus on close
- Alt text for all informational images. Decorative images: `alt=""`
- Forms: associate `<label>` with inputs. Use `aria-describedby` for error messages

## SEO and Metadata

- Use `generateMetadata()` in `page.tsx` and `layout.tsx` for dynamic metadata
- Implement `sitemap.ts` and `robots.ts` at app root
- Semantic HTML heading hierarchy (`h1` → `h2` → `h3`, no skipping levels)
- Structured data: JSON-LD via `<script type="application/ld+json">`
- Open Graph and Twitter Card meta tags for social sharing
- Canonical URLs to prevent duplicate content

## Security (Client/Server Boundary)

- Validate all Server Action inputs with Zod — never trust client data
- Use the `server-only` package to prevent server code from leaking to client bundles
- No secrets on the client: API keys, tokens, credentials stay in `route.ts`, Server Actions, middleware
- Sanitize user-generated HTML with DOMPurify before rendering with `dangerouslySetInnerHTML`
- CSP headers via `next.config.js` or middleware
- CSRF protection: Next.js Server Actions include built-in CSRF tokens
- Auth middleware: protect routes in `middleware.ts`, not in components

## Testing (Vitest + Playwright)

- **Unit tests**: Vitest + React Testing Library. Test behavior, not implementation
- **Integration tests**: page-level flows with MSW for API mocking
- **E2E tests**: Playwright for critical user journeys
- **What to test**: user interactions, form validation, error states, conditional rendering, accessibility
- **What NOT to test**: implementation details, internal state, CSS classes, snapshot tests (fragile)
- **Test structure**: Arrange → Act → Assert. Use `screen.getByRole` over `getByTestId`. Prefer `userEvent` over `fireEvent`
- **Accessibility testing**: include axe-core checks in E2E flows for critical pages

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `Agent(frontend-engineer)` invocation | Auto-loaded via `skills:` frontmatter |
| `/develop` with frontend work package | Spawned frontend-engineer agent loads this |
| `/code-review` on React/Next.js PRs | Reviewer references these patterns |
| `/architecture-design` (frontend service) | Architect references rendering boundaries, data flow |
| `/seo-review` on pages | SEO engineer references metadata + Core Web Vitals sections |
| `/bugfix` on UI defects | Developer references RSC boundary, hydration, a11y |

## Integration

- **Consumed by**: `frontend-engineer` agent (primary), `ui-ux-designer` (when reviewing implementation), `seo-engineer` (when auditing pages), `qa-engineer` (when writing component/E2E tests)
- **Companion knowledge**: `context-engineering` skill (for AI-feature frontends), `owasp-coverage` skill (client/server boundary security)
- **External references**: Next.js App Router docs, React docs, Tailwind CSS docs, shadcn/ui docs, WCAG 2.2, Web Vitals (web.dev)
