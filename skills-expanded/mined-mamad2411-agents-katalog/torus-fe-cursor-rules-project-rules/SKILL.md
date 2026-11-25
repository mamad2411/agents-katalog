# Cursor Project Rules

## Stack

- React 19 + Vite + TypeScript. Prefer hooks and Suspense-ready components; keep server-agnostic.
- React Router 7; nested routes with layout components and Outlet. Prefer NavLink for active styling.
- TanStack Query 5 for data; colocate query hooks with consuming feature.
- Schedule-X and React Table for calendar/table UIs; adapters live in feature folders.
- Temporal polyfill for dates/time; avoid Date for new logic.

## Project Structure

- Components live in src/features/_; route views in src/pages/_; app layout/config in src/app/\*.
- Prefer explicit imports over barrels; keep files focused.

## Components & Types

- Functional components only. Define Props types immediately above component.
- Default export components unless multiple exports are required.
- Write shared API/domain types and reuse across queries, forms, and UI props; avoid any.
- Prefer const and immutability; derive view state from query data and URL params.

## Styling & Theming

- Compose UIs with MUI primitives (Box, Stack, Container, Grid) and sx.
- Respect theme spacing scale; avoid hard-coded px when possible.
- Use Typography variants and palette keys; extract Emotion styled components when styling is complex, keeping theme awareness.

## Data Fetching (TanStack Query)

- Implement feature-scoped useQuery/useMutation hooks. Declare local queryKeys to avoid collisions.
- Centralize QueryClient defaults (retry, staleTime, refetchOnWindowFocus) at app bootstrap.
- Use select in queries to derive lightweight view models.
- Call a typed API client with async functions; throw domain errors for error surfaces.

## Routing

- Register routes in src/app/App.tsx or a dedicated router; group under layout routes to share shells.
- Use prefetch/loader-like patterns or Query prefetching to ensure data before rendering details.
- Prefer relative links in nested routes (to=".", to="..").

## Forms

- Use MUI inputs (TextField, Select, DatePicker); align labels via htmlFor.
- Adopt react-hook-form integrated with mutations; use Controller for MUI compatibility.
- Provide inline validation and disable submit while pending.

## Dates & Scheduling

- Use Temporal for calculations, conversions, and formatting.
- Keep Schedule-X configuration (views, adapters, i18n) inside the feature folder and typed.

## Testing & Quality

- Use Vitest + React Testing Library; colocate tests as \*.test.tsx.
- Mock network via MSW for query tests.
- Run npm run lint before commits; keep accessibility and hook rules green.

## Accessibility & UX

- Ensure proper aria/semantic roles; MUI components should be used as intended.
- Maintain keyboard navigation; respect focus order with Button, Link, form components.
- Provide loading/empty states for query-backed views; handle errors with alerts/snackbars.

## Documentation

- Add short JSDoc for non-obvious utilities; annotate complex component props.
- Update README or feature docs when adding flows affecting routing, API, or env.
