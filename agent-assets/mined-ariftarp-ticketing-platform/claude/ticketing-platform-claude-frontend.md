# CLAUDE.md — frontend

> Loaded when working inside `frontend/`. See root `CLAUDE.md` for shared conventions.

Next.js (App Router, TypeScript), pnpm. Talks **only** to the gateway
(`http://localhost:8080`), never to a service directly.

Screens (per `docs/user-flow.md`): `/login`, `/register`, `/events`, `/events/[eventId]`,
`/events/[eventId]/seats`, `/checkout/[bookingId]`, `/checkout/[bookingId]/confirm`, `/tickets`.
Admin (`/admin/events`) is Phase 14, optional/last.

State management: plain React state + small custom hooks (`useCountdown`, `useSeatSelection`,
`useBookingPolling`) — no Redux/SWR/React Query, per the Phase 10 architecture review. JWT held in
`localStorage` via the root `SessionProvider` context. `apiClient.ts` wraps `fetch` with RFC 7807
error parsing.

Note: `fetchMyBookings()` decodes the JWT's `sub` claim client-side to call
`GET /api/v1/bookings?userId=`, since booking does not parse JWTs itself.

## Visual design system

Every screen uses the "control panel" design tokens/utility layer defined in `app/globals.css`
(dark surfaces, single electric-cyan accent, four semantic status colors, a monospace face
reused for anything data-shaped — prices, seat/ticket ids, countdowns). See
`.claude/agents/ui-designer.md` for the full rationale and per-screen direction before restyling
anything — reuse the existing `.panel`/`.btn-*`/`.input-field`/`.label-mono`/`.value-mono`
utility classes rather than inventing new ad hoc styling.

## E2E tests (Playwright)

`e2e/*.spec.ts`, config in `playwright.config.ts`. Unlike the Vitest unit suite (pure logic, no
DOM rendering), these run a real browser against a real `pnpm dev` instance on `:3000` — some of
them (`booking-flow.spec.ts`, `admin-flow.spec.ts`) also need the full backend (gateway on
`:8086`/whatever `NEXT_PUBLIC_API_BASE_URL` points at, plus auth/event/booking/payment/
notification and their Postgres/Kafka/Redis infra) actually running, since they exercise the real
checkout saga and the real ADMIN role gate rather than mocking either. `visual-smoke.spec.ts`
only needs the frontend dev server. Start what's needed, then `npx playwright test` (add
`--ui`/`--headed` for debugging). `admin-flow.spec.ts` promotes its own throwaway test user to
ADMIN via a direct `docker exec ticketing-postgres psql` statement — there's no product-level way
to do this, since registration only ever assigns `USER`.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
