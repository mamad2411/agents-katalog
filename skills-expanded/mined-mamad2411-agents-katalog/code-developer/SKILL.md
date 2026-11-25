---
name: code-developer
description: Code Developer Skill.
category: meta
tags:
- meta
- code
- developer
---
## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Data & Contract Definition

**BEFORE writing any UI or Component code:**

1.  **Define the Data Model**
    - What does the entity look like in the database?
    - What are the required fields?
    - What are the relationships (1:1, 1:N, N:M)?
    - **Draft the TypeScript Interface/Type definitions first.**

2.  **Establish the Contract (API)**
    - How does the frontend fetch this data?
    - What arguments does the query/mutation require?
    - What are the exact failure states (401, 403, 404, 500)?
    - **Don't guess:** Check the Swagger/OpenAPI spec or backend code.

3.  **Trace the State Lifecycle**
    - Where does this data live? (URL URL params? Server State? Client Store? Local Component?)
    - **Rule:** Lift state up only as high as necessary.
    - **Rule:** Prefer Server State (React Query, SWR) over Global Client State (Redux/Context) for server data.

4.  **Security & Access Control**
    - Who is allowed to see this?
    - Who is allowed to edit this?
    - Does the backend enforce this? (Frontend checks are just UI sugar).

### Phase 2: The "Walking Skeleton"

**Build the pipeline before the pixel:**

1.  **Build the Integration Layer First**
    - Create the API client methods.
    - Create the hook/service to fetch the data.
    - Verify data flows from Backend → Network Tab → Console Log.
    - **Do not build UI elements yet.**

2.  **Verify Error Handling**
    - Force the network request to fail.
    - Does your service catch it?
    - Do you have a typed error object?

3.  **Hardcode the Happy Path**
    - Create a bare-bones, unstyled test component.
    - Render `JSON.stringify(data)` to the screen.
    - Verify the "Walking Skeleton" connects end-to-end.

### Phase 2.5: Modern Frontend Tooling (2026)

**The 2026 frontend landscape:**

1.  **State Management Evolution**
    - **Server State ≠ Client State** (This is the key insight)
    - **Server State:** Use Tanstack Query (React Query), SWR, tRPC
      - Auto-caching, refetching, optimistic updates
      - Don't put API data in Redux/Context/Zustand
    - **Client State:** Use Zustand, Jotai, or Context (for truly local state)
      - UI toggles, form state, theme preference
    - **React 19 Patterns:**
      - Server Components for data fetching (Next.js App Router)
      - `use()` hook for promises
      - Actions for mutations

2.  **Build Tools (Vite Era)**
    - **Vite 6:** 10x faster HMR than Webpack, native ESM
    - **Turbopack:** Next.js native bundler (Rust-based)
    - **Biome:** Unified linter/formatter (replaces ESLint + Prettier)
    - **Bun:** Ultra-fast package manager (3-10x faster than npm)
    - **Anti-Pattern:** Still using Create React App (deprecated 2023)

3.  **TypeScript Best Practices (2026)**
    - **Zod for Runtime Validation:** Type safety at boundaries
      ```typescript
      const UserSchema = z.object({ id: z.number(), email: z.string().email() });
      type User = z.infer<typeof UserSchema>; // DRY
      ```
    - **Type Utilities:** Leverage built-ins (Partial, Pick, Omit, Awaited)
    - **Strict Mode:** Enable `strict: true` in tsconfig
    - **Rule:** No `any` types (use `unknown` if truly dynamic)

### Phase 3: Component Architecture

**Design the structure:**

1.  **Identify Boundaries**
    - **Container/Page:** Handles data fetching, URL parameters, and layout.
    - **Presentational/Leaf:** Receives data via props. Pure functions. No side effects.
    - **Rule:** If a component is > 150 lines, it probably does too much.

2.  **Separation of Concerns**
    - Logic goes in Custom Hooks or Utility functions.
    - Markup (JSX/HTML) stays clean and readable.
    - Styles (CSS/Tailwind) should be consistent.

3.  **Accessibility (a11y) Planning**
    - Semantic HTML elements (`<button>` not `<div>`).
    - Keyboard navigation (Tab index).
    - Aria labels for non-text interactions.

### Phase 4: Implementation & Polish

**Iterative construction:**

1.  **Implement Core Functionality**
    - Build the inputs and display logic.
    - Connect the "Walking Skeleton" data to real inputs.
    - **Use `superpowers:test-driven-development`** for complex logic.

2.  **Handle Loading & Empty States**
    - What does the user see while fetching? (Skeleton/Spinner)
    - What if the list is empty? (Empty state illustration)
    - What if it errors? (Retry button/Toast)

3.  **Defensive Coding**
    - Handle null/undefined values safely (Optional Chaining `?.`).
    - Validate form inputs (Zod/Yup).
    - Prevent double-submissions on buttons.

4.  **Final Polish**
    - Transitions/Animations.
    - Responsive behavior (Mobile/Tablet).
    - Dark mode compliance.

### Phase 4.5: Performance Profiling

**Make it fast:**

1.  **React Performance Tools**
    - **React DevTools Profiler:** Record renders, find expensive components
    - **Why Did You Render:** Debug unnecessary re-renders
      ```bash
      npm i @welldone-software/why-did-you-render
      ```
    - **Million.js:** Auto-optimize React (virtual DOM replacement)

2.  **Core Web Vitals (Google Ranking Factors)**
    - **LCP (Largest Contentful Paint):** <2.5s
      - Fix: Preload hero images, remove render-blocking scripts
    - **FID/INP (Interaction):** <100ms
      - Fix: Code splitting, lazy load heavy components
    - **CLS (Cumulative Layout Shift):** <0.1
      - Fix: Set width/height on images, reserve space for dynamic content
    - **Tool:** Lighthouse CI (automated performance regression tests)

3.  **Bundle Analysis**
    - **webpack-bundle-analyzer / vite-plugin-visualizer**
      ```bash


## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "I'll just put the `fetch` call inside the `useEffect` for now."
- "I'll fix the TypeScript `any` types later."
- "I'll handle errors globally, I don't need a `try/catch` here."
- "Just copy-paste that other component and tweak it."
- "I'll add the loading state after I get it working."
- "Why is this re-rendering 50 times? Whatever, it works."
- "I'm not sure where this prop comes from, just drill it down."
- **Writing CSS/Styles before data is successfully logging to console.**

**ALL of these mean: STOP. Return to Phase 1.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Where is the data coming from?" - You skipped Phase 1.
- "Is this accessible?" - You ignored semantic HTML in Phase 3.
- "This feels slow/janky." - You botched the State Lifecycle or re-renders.
- "What happens if the API is down?" - You missed Phase 2 (Error Handling).
- "Why are we passing props down 5 levels?" - Bad Component Architecture.

**When you see these:** STOP. Return to Phase 3.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll add types later" | You never will. 'Any' breeds runtime errors. |
| "It's just a prototype" | Prototypes become production code. Build it right. |
| "Styling is easier to do as I go" | Distracts from logic flaws. Data first, pixels second. |
| "I don't need a custom hook for this" | Mixing UI and Data logic makes code untestable. |
| "The backend handles validation" | Frontend validation saves roundtrips and UX frustration. |
| "A11y takes too long" | Fixing a lawsuit or rewriting for a11y later takes longer. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Data & Contract** | Define Interface, API check, State plan | Typed interfaces, clear data source |
| **2. Walking Skeleton** | API Client, Logs, Error handling | Data logs to console, Errors caught |
| **3. Architecture** | Container vs Presentational, Semantic HTML | Clean component tree, readable JSX |
| **4. Implementation** | UI Logic, Loading States, Polish | Fully interactive, handled edge cases |

## When Process Reveals "Backend Blockers"

If systematic investigation reveals the Backend API is missing or broken:

1.  **Mock it immediately.**
2.  Define the expected JSON structure (Phase 1).
3.  Create a mock function that returns that JSON after a delay.
4.  Continue development (Phase 2-4) using the mock.
5.  Swap the mock for the real API endpoint when ready.

**Do not stop development waiting for backend.**

## Supporting Techniques

- **`superpowers:test-driven-development`** - For complex validation or state logic.
- **`superpowers:clean-code`** - For keeping components small and readable.
- **Feature Flagging** - For merging code safely before it's 100% ready.

## Real-World Impact

From development cycles:
- **Data-First approach:** Features land with 90% fewer integration bugs.
- **UI-First approach:** constant "rewrites" when data shape changes.
- **Mocking:** Allows frontend/backend to work in parallel without blocking.
The above content shows the entire, complete file contents of the requested file.

## 🛠️ Recommended Frontend Stack (2026)

### Core Framework
- **React 19:** Server Components, Actions, use() hook
- **Next.js 15:** App Router (React Server Components)
- **TypeScript 5.6:** Essential for scale

### State Management
- **Server State:** Tanstack Query, tRPC (type-safe)
- **Client State:** Zustand (simple), Jotai (atomic)
- **Forms:** React Hook Form + Zod validation

### Styling
- **Tailwind CSS 4:** Utility-first, fast
- **shadcn/ui:** Copy-paste components (not npm package)
- **CSS Modules:** For component-scoped styles

### Build Tools
- **Vite 6:** Dev server (fast HMR)
- **Turbopack:** Production bundler (Next.js)
- **Biome:** Linter + Formatter (Rust-based)
- **Bun:** Package manager (faster than npm/pnpm)

### Testing
- **Vitest:** Unit tests (Vite-native)
- **Playwright:** E2E tests (cross-browser)
- **Testing Library:** Component tests

### Avoid
- **Create React App:** Deprecated, use Vite
- **Redux:** Overkill for most apps, use Tanstack Query + Zustand
- **Moment.js:** Huge bundle, use date-fns or Temporal API

## 📚 Learning Resources

### Books
- *Designing Data-Intensive Applications* (Kleppmann) - Understand backend data flows
- *Refactoring UI* (Wathan) - Visual design for developers

### Documentation
- React 19 Docs (react.dev) - Official React documentation
- MDN Web Docs - Web platform reference
- TypeScript Handbook - Type system deep dive

### Communities
- **Reactiflux Discord:** 200k+ React developers
- **Frontend Masters:** High-quality video courses
- **This Week In React:** Newsletter (Sébastien Lorber)
