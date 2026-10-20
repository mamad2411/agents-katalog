---
name: reui-gantt-calendar-patterns
description: "reui (keenthemes/reui, MIT) shadcn/Base-UI-native Gantt and Event Calendar component patterns for React. Use when building project-scheduling Gantt views, resource timelines, or booking/event-calendar UIs with @reui/gantt or @reui/event-calendar. Triggers on: gantt chart, shadcn gantt, reui gantt, project scheduling UI, resource timeline, event calendar, booking calendar, GanttEvent, EventCalendarApi, drag-and-drop scheduling, recurring events, RFC 5545 recurrence."
user-invocable: false
allowed-tools: Read, Glob, Grep
---


# reui Gantt + Event Calendar Patterns

reui (`github.com/keenthemes/reui`, MIT license) is a shadcn-compatible component registry.
Its Gantt and Event Calendar primitives are headless-first, Base-UI-or-Radix-backed,
Tailwind-styled scheduling components, distributed via the shadcn CLI ("you own the code" —
components are copied into your own repo, not installed as an opaque npm dependency).

> **MANDATORY**: Before writing any Gantt code, read `references/gantt-api.md` in this skill
> directory. Before writing any Event Calendar code, read `references/event-calendar-api.md`.
> Do NOT guess prop names, hook signatures, or data-shape fields — reui's API is specific and
> will silently break if guessed. Every claim in both reference docs is sourced from
> `docs/recon/reui-gantt-calendar.md`'s evidence-audited citations (8/8 verified, 2026-07-23) —
> if reui's upstream API has since changed, re-run `/recon` against the current docs rather than
> trusting this skill blind.

## When to use which component

| Need | Component | Package |
|------|-----------|---------|
| Project-scheduling Gantt, resource timeline, task dependencies, progress rollups | Gantt | `@reui/gantt` |
| Booking/event calendar, month/week/day/agenda/resource views, recurring events | Event Calendar | `@reui/event-calendar` |

Not the same library as `@nessprim/planby-pro` (EPG/schedule grids) — that package and its
skill were retired 2026-07-23; reui is the fleet default for shadcn-based projects going
forward. If a project already has `@nessprim/planby-pro` code, do not migrate it as part of
using this skill — that is separate, explicitly out-of-scope work.

## Installation

```bash
pnpm dlx shadcn@latest add @reui/gantt            # Gantt
pnpm dlx shadcn@latest add @reui/event-calendar   # Event Calendar
```

Both ship in reui's free "Components" tier (not the paid Blocks/templates tier). Core deps:
`@base-ui/react`, `@date-fns/tz`, `date-fns`; Gantt additionally pulls `class-variance-authority`.
Peer dep: `react`/`react-dom >=18`.

## Core Architecture

Both components use a provider + composable-slots pattern (root component + context, replaceable
child slots), a controlled/uncontrolled dual-prop API (`events`/`defaultEvents`,
`view`/`defaultView`, etc.), and fine-grained subscription hooks (`use*Selector`) for perf.
They share the same RFC-5545-subset recurrence engine (`parseRRuleString`/`expandRecurrence`,
DST-safe, capped at 1000 occurrences/event, throws `GanttRecurrenceError` on unsupported rules
rather than silently mis-expanding).

## Critical Rules (from evidence-audited recon)

1. **The actual component source ships via the shadcn registry JSON** (`public/r/styles/<theme>/*.json`
   in the reui repo) — NOT the `src/index.ts` file under `packages/registry/bases/.../components/`,
   which is a generated preview-loader manifest, not the implementation. If inspecting the reui
   repo directly rather than using the CLI, look at the registry JSON's `files[].content`.
2. **`onEventUpdate` is the single commit gate** for both drag and resize — it can return `false`
   (reject), `void`/`true` (accept), or `{start?, end?, allDay?}` (accept with server-side
   adjustment). `canDropEvent` is the live validity predicate DURING the drag, not the commit gate.
3. **Recurrence expansion caps at 1000 occurrences per event** — do not assume unbounded
   expansion; an unsupported RRULE shape throws `GanttRecurrenceError`, it does not silently
   truncate or guess.
4. Gantt drag is **horizontal-only within a resource row** — it never moves an event across rows;
   row reassignment is a separate `resourceId` mutation via `onEventUpdate`.
5. Event Calendar's Resource view is a distinct 6th view alongside month/week/day/N-day/agenda —
   don't conflate it with the generic "resource timeline" concept from Gantt; they're separate
   components with separate APIs.

## Reference Docs

- `references/gantt-api.md` — full `GanttEvent`/`GanttResource` shapes, composition contract,
  view-config props, callback signatures, hooks, i18n, layout metrics.
- `references/event-calendar-api.md` — full `EventCalendarApi` methods, the 6 views, event
  shape, callbacks, hooks, timezone/recurrence model.
