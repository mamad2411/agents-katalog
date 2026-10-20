---
description: Admin SPA modular monolith - Tailwind, first-party primitives, layer isolation, package map
globs:
  - web/**
  - api/openapi/**
  - scripts/ci/check_ui*.sh
  - scripts/ci/admin/web.sh
alwaysApply: false
---

# Frontend Modular Monolith

## Purpose

Admin UI (`web/`) is a **modular monolith in the browser**: one SPA build (`web/dist`), domain folders as compile-time modules. Stack: **React 19 + TypeScript + Tailwind CSS + first-party primitives** (`web/src/components/ui/`).

Same invariants as Go `cmd/control` (`modular-monolith.mdc`, `structure.mdc`):

- Thin composition root (`pages/`)
- Domain-owned UI (`domains/<domain>/`)
- Shared primitives (`components/ui/`) — no shadcn, no `@radix-ui/*`
- No ceremony trees (`dto/`, `usecase/`, `providers/`)
- Cold path first: server owns filter/sort/aggregate (`ui.mdc`, `cold-path.mdc`)

**Quality reference:** `lead-intent-processor` — `internal/crm/{admin,store,webhook}` owns CRM surface; `internal/app` (~18 prod `.go`) wires only. Admin SPA mirrors that split: `pages/` = wire, `domains/<domain>/` = product.

**Agent audits:** mandatory toolchain + catalog IDs in `frontend-slop.mdc` **Agent execution protocol** — no subjective "best practices" reviews.

Cross-ref: `ui.mdc` (macro Grid / micro Flex layout, styling stack), `frontend-patterns.mdc` (паттерны фронтенда; composition, effects, races, errors, async), `frontend-primitives.mdc` (Button/Input stack), `react.mdc` (Hot vs Cold runtime), `frontend-hot-path.mdc` (suboptimal ops, scale regimes), `boundaries.mdc` (coupling limits), `naming.mdc`.

## Status

| Fact | State |
| :--- | :--- |
| `web/` tree | Active — React 19 + TSX + Tailwind + first-party `components/ui/` |
| Styling | Tailwind utilities in TSX; BEM banned; legacy `*.module.css` removed on touch |
| Contract | `api/openapi/` + generated TS types |
| Embed | `internal/controlplane/admin_static_stub/` until `web/dist` ships |

New pages follow this file + `ui.mdc` + `web/DESIGN.md`.

## Isolation levels (coupling limits)

One agent task = **one layer owner**. Crossing layers without explicit `Depends on` is a boundary violation (`boundaries.mdc`).

| Level | Path | Owns | Must not own |
| :--- | :--- | :--- | :--- |
| L0 Contract | `api/openapi/`, Go `*_handlers.go` | Query params, DTO, **S1-S7 validation before persist**, SQL/CH | `web/src` pages (unless PR closes both) |
| L1 Transport | `web/src/api/*_api.ts` | HTTP, abort, parse JSON to typed snapshot | `useMemo` filter/sort over full `items[]`; owning UI prefs state |
| L2 Composition | `web/src/pages/*` | Section compose, URL → fetch params, route entry; pass props to `domains/<domain>/` | Tailwind layout on pages, business rules, invented API fields |
| L3 Domain UI | `web/src/domains/<domain>/` | Macro Grid / micro Flex; semantic `<table>`; **one primary path per intent** | Cross-page Context, server logic, hand-rolled overlays, duplicate mutation entry points |
| L4 Shared chrome | `web/src/shell/`, `web/src/components/ui/` | Nav, login, PageChrome; UI primitives | Domain-specific API shapes |
| L5 Theme | `app.css`, `tailwind.config.ts`, `lib/admin_kit.ts`, `lib/admin_chrome.ts` | `@tailwind` entry; zinc palette; **named Tailwind constants** for cross-route chrome (`frontend-slop.mdc` **Shared style contracts**) | Domain-specific layout rules in `app.css` BEM |
| L6 Static embed | `web/src/static/` | `track.js` snippet (not admin) | Admin React imports |

### Hard FE/BE boundary

| Concern | Server | Browser |
| :--- | :--- | :--- |
| Filter, search, sort | Query params + handler | Pass params; render `items` |
| Pagination, totals | `limit`, `offset`, `total` | Controls only |
| Labels, money | `*_label`, `*_display`, micros | Map tone enum; format display fields |
| Validation | 400 + field map | Show API errors |
| Export / long jobs | Async endpoint + poll | Job id + poll UI |

Forbidden: React Context for list filter state; root `FilterProvider`; client KPI math; hand-written TS types diverging from OpenAPI.

### Entity ID parity (seeds, E2E, fixtures)

Browser code has **no** mock API intercept. Entity id rules still apply to Playwright fixtures, seed display strings, and any hardcoded rows:

| Need | Use | Never |
| :--- | :--- | :--- |
| Catalog row `n` in fixtures | `seedDeterministicUuid('<kind>', n)` aligned with Go seed | `devUuid()`, `00000000-...-000N`, `padStart(12,'0')` |
| Runtime create in tests | `newRandomUuid()` | Static reused id per request |
| `user_id`, `customer_id`, `campaign_id` FK | UUID from seed helpers | `"buyer-1"`, `"user-1"`, integer strings |

Parity: `go test ./cmd/admin/ -run TestSeedCatalog_deterministicUUIDsAreRealistic` vs TS seed helpers when both exist.

### Styling ownership (BEM banned; Tailwind only)

BEM (`admin-*__*`, `campaign-*__*`) is **banned** -- not a sunset path. New and touched UI: Tailwind in TSX + `components/ui` primitives only. One DOM node = one styling owner; never stack `app.css` BEM hooks with Tailwind utilities on the same element.

Pure CSS in `app.css` only for Tailwind entry, scrollbar pseudo-elements, and similar cases where utilities cannot apply (`frontend-slop.mdc` **Styling stack**).

Legacy collision taxonomy and file audit: `frontend-slop.mdc` **Styling stack**.

## Target package map

```
web/
  tailwind.config.ts
  src/
    pages/                 # compose only; <= ~120 lines; no styling
    domains/
      <domain>/            # customers, campaigns, billing, …
        *.tsx              # Tailwind className in TSX
    shell/                 # login, nav, layout chrome
    components/
      ui/                  # first-party primitives (Button, Select, Dialog, Table, …)
    api/
      <domain>_api.ts      # fetch + parse only
      use_resource.ts      # shared fetch hook (not domain logic)
    types/
      generated/openapi.d.ts
      index.ts             # thin re-exports only
    lib/
      admin_chrome.ts      # shared zinc class tokens for primitives
      utils.ts             # cn() — clsx + tailwind-merge
    styles/
      app.css              # @tailwind + fonts + minimal base only
    static/
      track.js
```

### Banned trees and patterns

| Pattern | Why | Replacement |
| :--- | :--- | :--- |
| `web/src/dto/`, `usecase/`, `providers/` | Ceremony hides contracts | `api/` + `domains/<domain>/` |
| `web/src/models/` with business rules | Duplicate server logic | Delete on migrate; server DTO only |
| `web/src/components/` monolith (non-shadcn) | No domain boundary | `domains/<domain>/` + `components/ui/` |
| New `*.module.css` | Legacy CSS Modules stack | Tailwind in TSX |
| New `*.variants.ts` per domain file | CVA sprawl | `admin_chrome.ts` tokens inside `components/ui/` only |
| BEM `__` under `web/src/domains` | Unscoped global classes | Tailwind utilities |
| Dual state writers on one resource | Leaf `save*` / `useState` + owner hook for same prefs, filter, or selection | Single owner + `onXChange` up (`frontend-slop.mdc` **State ownership**) |
| Unguarded user refetch | Refresh handler bumps deps or calls API with no coalesce window | Owner `useCoalescedCallback` or inline guard (`frontend-slop.mdc` **User action coalescing**) |
| Duplicate UX mutation path | Two controls same intent (e.g. Create + Wizard) without mutex | One primary; script table (`frontend-slop.mdc` **UX scenario contract**) |
| Raw `@radix-ui/*`, `class-variance-authority`, `components.json` | shadcn stack | First-party `web/src/components/ui/` only |
| Global `btn--*` on pages | Layout escape | `<Button>` from `components/ui/button` |
| Product-prefixed static (`ad-event-processor-track.js`) | Legacy token | `track.js`, export `trackEvent` (`naming.mdc`) |

## Domain module shape (exemplar)

One admin domain = one `domains/<domain>/` folder + one `api/<domain>_api.ts` + one or more thin `pages/*`.

```
domains/campaigns/
  list/                         # campaigns directory, table, columns, metrics cells
    campaigns_directory.tsx
    campaigns_list_table.tsx
    campaign_list_columns.ts
  editor/                       # campaign editor, wizard, clone, panels
    campaign_editor.tsx
    campaign_wizard_panel.tsx
  report/                       # per-campaign report tables
    campaign_report_directory.tsx

domains/customers/
  customers_directory.tsx       # section: toolbar + table + footer
  customers_grid.tsx            # <Table> from shadcn + Tailwind columns

components/ui/
  button.tsx
  table.tsx
  select.tsx

api/customers_api.ts

pages/customers_page.tsx        # <CustomersDirectory /> + useResource + URL params
```

Rules:

- Pages fetch via `api/*_api.ts` + `use_resource.ts`; pass typed props into section components — no layout styling on pages.
- Section owns macro Grid / micro Flex via Tailwind (`ui.mdc` Layout).
- Presentational: `domains/<domain>/` components accept props and render markup only.
- Interactive primitives from `components/ui/` — owned in-repo; extend `admin_chrome.ts` tokens.
- `cn()` from `web/src/lib/utils.ts`.
- Cold list pages: server pagination + `items.map()` (`react.mdc` Cold path). Hot rules only for charts/streaming.

List fetch lifecycle (abort, ticker isolation, charts): `react.mdc`.

## Migration from legacy tree

| Legacy | Action |
| :--- | :--- |
| `web/src/components/*` (non-shadcn) | Move to `domains/<domain>/` or replace with shadcn |
| Legacy `web/src/ui/*` tree | Migrated to `domains/` + `shell/`; shadcn in `components/ui/` |
| `*.module.css` | Convert to Tailwind on touch; delete file when unused |
| `web/src/styles/tokens.css` | Delete; use `tailwind.config.ts` + utilities in TSX |
| `web/src/lib/cn.ts` | Rename/merge to `lib/utils.ts` (shadcn default) |
| Client `sortRows` / `filter` in pages | Replace with server query params + refetch |
| CSS Grid / subgrid data matrices | Semantic `<table>` + `overflow-x-auto` (`ui.mdc`) |
| Custom `[data-dropdown-open]` overlays | shadcn `Select` / `DropdownMenu` / `Popover` (`ui.mdc`) |

Ship order: `admin_contract_gate` → `admin_shell` → `admin_directory_pattern` for first list page → replicate pattern.

## Verification

```bash
cd web && npm run typecheck
bash scripts/ci/admin/ui_surface.sh
bash scripts/ci/admin/web.sh
```

Milestone PR: paste verification commands (`ui.mdc`).

## Agent checklist

| Step | Action |
| :--- | :--- |
| 1 | One layer owner per task |
| 2 | Handler/DTO before UI field |
| 3 | New UI under `domains/<domain>/`; primitives from `components/ui/` |
| 4 | No client list business logic |
| 5 | No new CSS Modules; Tailwind + shadcn only |
| 6 | Repeated chrome (table header, filter grid, control height): extract to `admin_kit` / `admin_chrome` / shell `const` / `*_classes.ts` -- do not copy-paste utility chains (`frontend-slop.mdc` **Shared style contracts**) |
| 7 | `typecheck` + surface gate on touched paths |

## Related rules

`ui.mdc`, `frontend-patterns.mdc`, `frontend-primitives.mdc`, `react.mdc`, `boundaries.mdc`, `anti-slop.mdc`, `modular-monolith.mdc`, `structure.mdc`.
