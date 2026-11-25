# Frontend Web Engineering

## Purpose
Build accessible, performant browser interfaces with semantic HTML, full keyboard operability, WCAG 2.2 AA conformance, resilient data fetching, and Lighthouse scores of 90 or above across performance, accessibility, best practices, and SEO.

## Use when
- Implementing React, Vue, Svelte, or server-rendered pages, forms, routing, or client-side state.
- Remediating accessibility defects: missing labels, keyboard traps, focus loss, contrast failures, or screen-reader gaps.
- Wiring UI to REST/GraphQL endpoints with loading, empty, error, and retry states.
- Reducing bundle size, eliminating layout shift, or fixing Core Web Vitals regressions.

## Do not use when
- Implementing server endpoints, auth middleware, or API contracts without UI changes (use `backend-api`).
- Measuring full-page performance budgets, waterfalls, and RUM analytics without changing components (use `performance-web`).
- Tuning database queries behind the UI without touching the frontend (use `database-review`).

## Required context
- Wireframes or design tokens: spacing scale, color palette with contrast ratios, typography, breakpoints.
- API contracts for every wired endpoint: shapes, error codes, pagination cursors, rate limits.
- Browser and device matrix: evergreen Chrome, Safari, Firefox plus one mid-tier Android device such as Moto G54.
- Accessibility target: WCAG 2.2 AA, verified with axe-core and manual keyboard plus screen-reader passes.

## Procedure
1. **Mark up semantically first**: use header, nav, main, section, button, and native form controls; verify the heading outline and landmarks with axe-core before adding any ARIA.
2. **Guarantee keyboard operability**: every interactive element reachable by Tab, operable with Enter/Space/Escape/arrows, visible focus ring with 3:1 contrast, focus trapped in modals and restored on close, skip-to-content link present.
3. **Build resilient forms and data states**: label every input explicitly, validate on submit with inline errors linked via aria-describedby, debounce search at 250 ms, render loading skeletons, empty states, error panels with retry, and optimistic updates with rollback.
4. **Fetch data defensively**: use SWR or React Query with 30 s stale-while-revalidate, 2 s request timeouts, typed error mapping to user messages, and pagination cursors matching the backend-api contract.
5. **Enforce performance budgets**: initial route JavaScript under 200 KB gzip, images served AVIF/WebP with explicit width/height, fonts with font-display swap and subsetting, CLS under 0.1 verified in Lighthouse mobile emulation.
6. **Verify with automation and humans**: run vitest component tests, Playwright flows on Chromium/WebKit/Firefox, axe-core with zero serious violations, Lighthouse 90+ on all four categories, then execute scripts/verify.sh from the repo root.

## Decision rules
- **Native before custom**: native button, select, and dialog elements win over div-based widgets in every case.
- **Keyboard parity mandatory**: any pointer interaction must have an equivalent keyboard path; keyboard traps are release blockers.
- **No layout shift by default**: every media element reserves space; late-injected content uses skeletons, never pushes content.
- **Budgets are gates, not goals**: exceeding 200 KB initial JS or dropping below Lighthouse 90 fails the build.
- **Never ship silent failures**: every fetch path renders an explicit error with a retry action and logs to telemetry.

## Evidence required
- Playwright run logs across Chromium, WebKit, and Firefox with zero failures.
- axe-core report with zero serious or critical violations plus keyboard test notes.
- Lighthouse reports (mobile + desktop) at 90 or above in all four categories.
- Passing execution log from scripts/verify.sh.

## Output contract
- Accessible component or page implementation with semantic markup, keyboard support, and resilient states.
- Updated tests: vitest units, Playwright flows, axe checks wired into CI.
- Performance and accessibility evidence meeting the stated budgets.

## Stop conditions
- All flows implemented with Lighthouse 90+, zero axe serious violations, and Playwright green on three engines.
- Design tokens or API contract missing, blocking faithful implementation.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to Design lead if wireframes conflict with WCAG contrast or touch-target minimums (24x24 CSS px).
- Escalate to backend-api owner if endpoint shapes, error codes, or pagination break the UI contract.
