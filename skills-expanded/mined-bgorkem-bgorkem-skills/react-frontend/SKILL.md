---
name: react-frontend
description: >
  Build responsive, client-side React single-page web apps (SPA) with Vite,
  TypeScript, and Tailwind CSS, designed for both mobile and desktop browsers.
  Use when creating or editing a React SPA, a component, a hook, a page/route,
  responsive layouts, or browser UI. This skill is for CLIENT-SIDE SPAs ONLY —
  no server-side rendering. Enforces React best practices, the Rules of Hooks,
  strict TypeScript, ESLint React rules, and SOLID principles. Triggers:
  "react component", "build a website/UI", "responsive design", "tailwind",
  "SPA", "custom hook", "react page/screen", "react-router".
---

# React Frontend Skill (Client-Side Responsive SPA)

Build production-quality **client-side React single-page web applications** that
run entirely in the browser: Vite + React 18/19, TypeScript (strict), Tailwind
CSS, and `react-router-dom`. The UI is **responsive** — it must look and work
well on **mobile browsers and desktop browsers** alike.

**This skill is for client-side SPAs only.** All rendering happens in the
browser; there is no server-rendering step. Data is fetched client-side after
the app mounts. Scope is web only: responsive websites for browsers, not native
apps.

---

## 0. Scope guardrails

- **Client-side SPA only.** One HTML shell, JavaScript renders everything in the
  browser after load. No server rendering of any kind.
- **Bundler is Vite** (`vite`, `@vitejs/plugin-react`). Dev: `npm run dev`.
  Build: `npm run build`. Preview: `npm run preview`.
- **Routing is `react-router-dom`** (v6+), client-side route matching.
- **Target both form factors:** design responsive layouts that work from small
  mobile-browser viewports up to large desktop screens.
- Fetch data client-side (e.g. `fetch`/`axios` inside hooks or a data-fetching
  library). No server data-loading conventions.

---

## 1. Project structure

Group by responsibility. Keep components thin; push logic into services/hooks.

```
src/
├── main.tsx              # Vite entry — mounts <App/> into #root
├── App.tsx               # Root component: providers + <RouterProvider/>
├── router.tsx            # react-router route tree (createBrowserRouter)
├── components/           # Reusable UI — presentational where possible
│   ├── common/           # Buttons, inputs, layout primitives, shared
│   └── <feature>/        # Feature-scoped components (auth/, cart/, ...)
├── pages/                # Route-level screens, one folder per route area
│   └── <Page>/           # Page.tsx + Page.test.tsx + local parts
├── layouts/              # Shared shells (RootLayout, AuthLayout) for routes
├── hooks/                # Custom hooks (useX) — reusable stateful logic
├── services/             # Business logic, API clients, data access (no JSX)
│   └── <domain>/         # Split by domain (api/, auth/, ...)
├── store/ (optional)     # Cross-cutting client state (Context or Zustand)
├── types/                # Shared TypeScript types & interfaces
├── utils/                # Pure helper functions
├── styles/               # index.css (Tailwind entry) + globals
└── assets/               # Static images, fonts, icons
```

Module rules:
- **Separation of concerns:** components render; services decide; hooks bridge.
  Components MUST NOT contain business logic, calculations, or validation that
  belongs in `services/`.
- One route → one folder under `pages/`, colocating its test and local-only
  subcomponents. Promote a component to `components/` only when reused.
- Barrel `index.ts` exports per folder for clean imports.
- Colocate tests with code (`Component.test.tsx` or `__tests__/`).

### Router setup (react-router)

```tsx
// router.tsx
import { createBrowserRouter } from "react-router-dom";
import { RootLayout } from "./layouts/RootLayout";
import { HomePage } from "./pages/Home/HomePage";

export const router = createBrowserRouter([
  {
    element: <RootLayout />,          // shared shell (nav, error boundary)
    children: [
      { path: "/", element: <HomePage /> },
      // lazy-load route chunks to keep the initial bundle small:
      {
        path: "/dashboard",
        lazy: async () => ({ Component: (await import("./pages/Dashboard/DashboardPage")).DashboardPage }),
      },
    ],
  },
]);
```

Use `<Outlet/>` in layouts, `<NavLink/>`/`useNavigate` for navigation, and route
`errorElement` (or an error boundary) for fallback UI.

### Naming conventions

| Kind | Convention | Example |
|------|-----------|---------|
| Components | PascalCase | `NavBar`, `ProductCard` |
| Component files | PascalCase | `NavBar.tsx` |
| Hooks | camelCase, `use` prefix | `useCart` |
| Utilities/functions | camelCase | `formatPrice` |
| Types/Interfaces | PascalCase | `CartItem` |
| Constants | UPPER_SNAKE_CASE | `MAX_ITEMS` |

---

## 2. TypeScript standards (strict, non-negotiable)

- `"strict": true` in `tsconfig.json`. Also enable `noUncheckedIndexedAccess`.
- **Never** exclude test files from type-checking — tests are type-checked too.
- **No `any`.** Use precise types, generics, or `unknown` + type guards.
- Prefer `type` for unions/props, `interface` for extendable object shapes.
- Type component props explicitly; give optional props defaults.
- Model async/domain state with discriminated unions instead of boolean soup:
  ```ts
  type RemoteData<T> =
    | { status: "idle" }
    | { status: "loading" }
    | { status: "success"; data: T }
    | { status: "error"; error: Error };
  ```
- Run `tsc --noEmit` as a gate — **zero errors before commit.**

---

## 3. React best practices

**Components**
- Function components + hooks only. No class components.
- Keep components small and single-purpose. Extract when a component grows past
  ~150 lines or mixes concerns.
- Prefer presentational (props-in, JSX-out) components; isolate stateful/
  container logic in hooks or wrapper components.
- Every list item needs a stable, unique `key` (never the array index for
  dynamic lists).

**Rules of Hooks (enforced)**
- Only call hooks at the **top level** — never inside conditions, loops, or
  nested functions.
- Only call hooks from React function components or other custom hooks.
- Custom hooks start with `use`.
- These are enforced by lint (see §7). See the Rules of Hooks reference below.

**State & data**
- Lift state only as high as needed; keep it local otherwise.
- Derive, don't duplicate — compute from existing state instead of syncing
  copies with effects.
- `useEffect` is for synchronizing with external systems (subscriptions, DOM,
  network), not for reacting to state you could compute during render. Always
  provide correct dependency arrays and cleanup functions.
- Reach for a data-fetching library (e.g. `@tanstack/react-query`) for server
  state; use Context or a small store (Zustand) for cross-cutting client state.
  Don't put fetched data in global stores you have to hand-sync.

**Performance**
- Memoize deliberately: `React.memo`, `useMemo`, `useCallback` where profiling
  shows a real cost — not by reflex.
- Code-split routes with `lazy` / `React.lazy` + `<Suspense>` to keep the
  initial browser bundle small (matters most on mobile networks).
- Stabilize props passed to memoized children.

**Reliability & UX**
- Wrap route trees in an **error boundary** (or route `errorElement`); render
  fallback UI.
- Always handle loading, empty, and error states — never assume data exists.
- Clean up subscriptions, timers, and listeners in effect cleanup.

**Accessibility**
- Semantic HTML first (`button`, `nav`, `main`, `label`).
- Touch targets ≥ 44×44px for mobile; visible focus states; label every input.
- Test keyboard navigation and screen-reader flow.

---

## 4. Responsive design with Tailwind (mobile & desktop)

Design **mobile-first**: style the smallest viewport with unprefixed utilities,
then layer breakpoints upward for tablet and desktop. The same SPA must serve
both mobile browsers and desktop browsers.

- Base = mobile browser. Add `sm:`, `md:`, `lg:`, `xl:` for larger screens —
  never the reverse.
  ```tsx
  // 1 col on phones, 2 on tablet, 3 on desktop
  <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3" />
  ```
- Fluid sizing: `w-full`, `max-w-*`, `flex-wrap`, `min-h-dvh`, container queries
  where useful.
- Touch-friendly on mobile, pointer-friendly on desktop: generous padding,
  `active:` and `hover:` states, but never rely on hover-only affordances.
- Test both ends: narrow mobile viewport and wide desktop viewport.
- Compose class strings with `clsx` (+ `tailwind-merge` to dedupe conflicts).
  Don't hand-concatenate template strings.
- Centralize the design system in `tailwind.config.js` (`theme.extend` colors,
  spacing, fonts). **No hardcoded hex/px in components** — use tokens.
- Prefer utilities over ad-hoc CSS; drop to `@layer` only for genuinely reusable
  component classes.

---

## 5. SOLID principles applied to React/TS

**S — Single Responsibility.** One reason to change per unit. A component
renders; a hook manages one slice of behavior; a service owns one domain. Split
a component that both fetches and renders and formats.

**O — Open/Closed.** Extend via props, composition, and `children` — not by
editing a component for every new case. Use variant props / config maps over
sprawling `if/else`. Compound components (`<Menu><Menu.Item/></Menu>`) add
behavior without rewrites.

**L — Liskov Substitution.** A specialized component must honor its base
contract. If `<IconButton>` wraps `<Button>`, it must accept the same props and
behave as a button (forward `ref`, `onClick`, `disabled`, `type`). Don't strip
or contradict inherited props.

**I — Interface Segregation.** Keep props interfaces narrow and focused. Don't
force a component to take a giant `config` object it half-ignores. Split fat
prop types; pass only what each component needs.

**D — Dependency Inversion.** Components depend on abstractions, not concretions.
Inject dependencies (API client, storage) via props, context, or hook
parameters rather than importing a concrete singleton deep in the tree. This is
what makes components testable — swap a real service for a mock at the seam.

```tsx
// D + I: component depends on an injected abstraction, not a hard import
interface UserRepository { getUser(id: string): Promise<User>; }

function useUser(repo: UserRepository, id: string) {
  // hook owns the stateful logic (SRP); repo is swappable (DIP)
}
```

---

## 6. DRY & code quality

- **Before writing logic, search for an existing implementation.** Never
  duplicate business logic, validation, calculations, or API patterns.
- On finding duplication: stop, extract to a shared `service`/`util`/`hook`,
  update all call sites, re-test.
- "Every piece of knowledge has a single, authoritative representation."
- Meaningful names; small focused functions; proper error handling everywhere.

---

## 7. Testing (Vitest) & linting (ESLint)

**Testing — Vitest** (native to the Vite toolchain) + React Testing Library:
- Use `vitest` + `@testing-library/react` + `@testing-library/user-event` +
  `@testing-library/jest-dom`, with `jsdom` as the test environment.
- Query by role/label (user-facing), not implementation details.
- Colocate tests; keep them deterministic; mock external deps in unit tests.
- Cover new logic as you write it; follow Arrange–Act–Assert.
- Target meaningful coverage on services/hooks (the logic), not just snapshots.
- Run with `vitest run` (CI) / `vitest` (watch); `vitest --coverage` for reports.

```ts
// vite.config.ts — test block
/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: { environment: "jsdom", setupFiles: "./src/test/setup.ts", globals: true },
});
```

**Linting — ESLint with React rules (enforced):**
- Enable **`eslint-plugin-react-hooks`** — enforces the Rules of Hooks and the
  exhaustive-deps check. This is mandatory; do not disable `rules-of-hooks`.
- Include `eslint-plugin-react` (React best-practice rules) and, for Vite HMR,
  `eslint-plugin-react-refresh`.
- Lint must pass with zero errors; treat `react-hooks/exhaustive-deps` warnings
  as bugs to fix, not to suppress.

```
eslint  eslint-plugin-react  eslint-plugin-react-hooks  eslint-plugin-react-refresh  prettier
```

### Tooling baseline

```
vite  @vitejs/plugin-react  react  react-dom  react-router-dom
typescript  tailwindcss  postcss  autoprefixer  clsx  tailwind-merge
vitest  @testing-library/react  @testing-library/user-event  @testing-library/jest-dom  jsdom
eslint  eslint-plugin-react  eslint-plugin-react-hooks  eslint-plugin-react-refresh  prettier
```

---

## 8. Pre-commit gate (all must pass)

```bash
tsc --noEmit        # zero type errors
npm run lint        # zero ESLint errors (incl. rules-of-hooks)
vitest run          # all tests green
npm run build       # production build succeeds
```

---

## Workflow when building

1. Confirm it's a client-side Vite SPA. Fetch data client-side.
2. Locate existing components/hooks/services to reuse (DRY).
3. Design the seam: what's a component vs. hook vs. service (SRP/DIP).
4. Build mobile-first responsive; verify on mobile and desktop viewports.
5. Follow the Rules of Hooks; type everything strictly; handle
   loading/empty/error/a11y.
6. Colocate a Vitest test. Run the pre-commit gate.

---

## References

- React best practices — https://vercel.com/blog/introducing-react-best-practices
- React testing (dotfiles) — https://awesomeskill.ai/skill/dotfiles-react-testing
- Rules of Hooks — https://legacy.reactjs.org/docs/hooks-rules.html
- ESLint plugin for React Hooks — https://react.dev/reference/eslint-plugin-react-hooks
