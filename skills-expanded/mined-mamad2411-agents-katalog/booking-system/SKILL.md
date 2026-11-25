---
name: booking-system
description: >-
  Designs UX for the public booking widget and admin portal following
  architecture-booking-system.md. Use when designing reservation flows, admin
  calendar, slot grids, or booking-related UX for public or admin surfaces.
---

# Booking System

## Input

1. `scope`: which surface to address — `public` (reservationBlock / visitor flow), `admin` (portal under `/admin`), or `both`
2. `user_goals`: what the visitor or admin user needs to accomplish (e.g., book a service, manage day calendar, set weekly hours)

## Preconditions

- **Read `architecture-booking-system.md` in full** before any recommendation — it is the source of truth for routes, APIs, data model, booking steps, and file map
- Read `architecture.md` and `docs/theme.md` for tenant theming and block registry rules
- For layout/component names: read `docs/agents/component-catalog.md` and, when relevant, `components/blocks/ReservationBlock.tsx`, `components/admin/`, and `components/admin/admin-copy.ts` (Spanish UI copy)
- Do not invent booking APIs, fields, or steps that contradict `architecture-booking-system.md`

## Booking surfaces (quick reference)

| Surface | Key UX elements |
|---------|-----------------|
| **Public** | 4-step `reservationBlock`: service → date/time (slot grid) → contact details → confirmation |
| **Admin** | `/admin/bookings` (day/week calendar, drawer, manual booking), `/admin/services`, `/admin/availability`, `/admin/settings` (placeholder) |
| **Shared** | Service catalog precedence (admin catalog overrides CMS fallback); slot grid; weekly + date exceptions; booking statuses (`confirmed`, `cancelled`, `no-show`, etc.) |

## Process

1. **Confirm scope** — Map `scope` to public widget, admin portal, or both; state which user type you are designing for (visitor vs. authenticated admin).
2. **Align with architecture** — Cross-check flows, routes, and data fields against `architecture-booking-system.md` (steps, APIs, `AdminBookingService`, schedule model).
3. **Apply UX principles** — Progressive disclosure (4-step widget), clear primary actions per step, feedback on submit/errors, keyboard and focus order for forms and calendars, consistent nav in admin (`AdminShell`).
4. **Accessibility** — WCAG 2.2 AA: labels on all form inputs (step 3 details), error text (3.3.1), contrast on slot grid and calendar states, focus visible on slot buttons and calendar cells, logical focus order across steps and drawer/modal.
5. **Component mapping** — Name existing registry/admin components where applicable; flag gaps (e.g., missing empty state, unclear closed-day behavior) with props/behavior for handoff.
6. **Admin vs. public consistency** — Service names, durations, and availability rules must read the same to visitors and staff; call out copy or status mismatches (admin copy is Spanish per `admin-copy.ts`).

## Output

Success:
```
Recommendation: <direct design answer for the stated scope>
Rationale: <UX principle or architecture constraint per decision; cite architecture-booking-system.md sections when relevant>
Component Map: <numbered sections/steps/screens with component or screen names>
Flows: <step-by-step for public and/or admin, only when scope includes that surface>
Gaps: <needs not covered by current components; precise enough for nextjs-frontend-developer>
Next Step: <one action for nextjs-frontend-developer or create-agent-task if cross-agent work is needed>
```

Failure:
```
FAILED at step <N> — <step name>
Reason: <exact error, e.g., architecture-booking-system.md not found>
Suggested fix: <one-line actionable hint>
```
