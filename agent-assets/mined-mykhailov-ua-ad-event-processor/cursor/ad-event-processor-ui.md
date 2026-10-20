---
description: Admin UI rebuild contract - cold path, OpenAPI, macro/micro layout, scroll/overflow, AI honesty
globs:
  - api/openapi/**
  - internal/controlplane/*_handlers.go
  - scripts/ci/admin/openapi.sh
  - scripts/ci/admin/web.sh
  - web/**
alwaysApply: false
---

# Admin UI

## Status

Admin SPA: `web/` (React 19 + TypeScript + **Tailwind CSS** + **first-party primitives** in `web/src/components/ui/`). Boot/embed: `internal/controlplane/admin_static_stub/` until `web/dist` ships. HTTP contracts: `api/openapi/`.

| Artifact | Path |
| :--- | :--- |
| HTTP API | `api/openapi/openapi.yaml`, `openapi.bundle.yaml` |
| Domain handlers | `internal/<domain>/handlers.go`, `internal/controlplane/*_bridge.go` |
| Admin static (stub) | `internal/controlplane/admin_static_stub/` via `admin_static_embed.go` |
| Visual reference | `web/DESIGN.md` (tokens, utilities, component catalog) |
| Typography roles | `web/src/lib/admin_typography.ts` |
| Error copy | `web/src/lib/admin_error.ts` |

### Package map (canonical)

| Layer | Path | Role |
| :--- | :--- | :--- |
| Pages | `web/src/pages/` | Route entry; hooks; URL to query params; compose domain sections only |
| Domain UI | `web/src/domains/<domain>/` | Presentational sections, tables, toolbars, sheets |
| System chrome | `web/src/shell/` | `PageLayout`, filters, tables, states, nav |
| UI primitives | `web/src/components/ui/` | Button, Select, Dialog, Sheet, Popover, ... |
| API transport | `web/src/api/*_api.ts`, `web/src/api/client.ts` | Typed fetch; parse JSON |
| Types | `web/src/types/generated/` | OpenAPI-generated TS |
| Theme | `web/src/styles/app.css`, `tailwind.config.ts` | Tailwind only; **no `globals.css`** |
| Hooks | `web/src/hooks/` | `use_session`, shared fetch hooks (no domain business rules) |

Reference implementations:

| Pattern | File |
| :--- | :--- |
| Directory list (campaigns) | `web/src/domains/campaigns/list/campaigns_directory.tsx` |
| Ops dashboard | `web/src/domains/ops/ops_home.tsx` + `ops_page_shell.tsx` |
| App shell | `web/src/app_shell.tsx` |
| Page scaffold | `web/src/shell/page_layout.tsx` |

Cross-ref: `frontend-modular.mdc`, `frontend-patterns.mdc`, `frontend-primitives.mdc`, `frontend-slop.mdc` (mocks, styling, errors, Playwright), `boundaries.mdc`, `cold-path.mdc`, `control-plane.mdc`, `naming.mdc`, `react.mdc`, `anti-slop.mdc`, `quality.mdc`.

### Styling and controls (see `frontend-slop.mdc` for full mandate)

Operator override until tree is cleaned: **one default `Button` height**; **no `truncate` on headings, numbers, or table data cells**; **body prose may wrap**. Legacy rows below that recommend column clamps or mixed button sizes are superseded by `frontend-slop.mdc`.

## Before code

Abstract "implement page X" is invalid without an explicit operator spec. Contracts live in this file, `frontend-modular.mdc`, and `api/openapi/`.

**Doc-only ask:** update rules only; zero `web/` diff unless operator asked to implement.

**Rejected slice:** `git revert`; no compensating wrappers or portals.

## AI laziness and dishonesty (admin UI)

Agents optimize for plausible diffs, not operator intent. Treat these as **lie modes** (`anti-slop.mdc`).

| Failure mode | What agents do | Required behavior |
| :--- | :--- | :--- |
| Doc ask -> code | Operator asks for `.mdc` update; agent edits components | Rules only unless implement asked |
| Piecemeal teardown | Delete/refactor `web/` file-by-file; half tree + broken CI | Remove or recreate `web/` atomically; embed stays in stub |
| History restore | Copy pre-reset `web/` from git without contract | Rebuild from rules + OpenAPI |
| Wrapper stack | `*DirectoryChrome`, `*Workspace`, `*Cluster` over section grid | One section = one domain module; page composes sections |
| Macro layout drift | Page shell built from nested flex columns | Grid for shell + section stack; Flex inside components only |
| Scroll clip lie | `overflow: hidden` on wrong ancestor; content grows unbounded | Follow **Scroll and overflow** below; **VL-10** in `frontend-slop.mdc` |
| Layout drift lie | "Fixed alignment" without **VL-*** catalog ID | **Visual layout drift taxonomy**; grep peer heights in filter band |
| Custom overlay logic | Hand-rolled `[data-dropdown-open]`, manual z-index | First-party overlays (`Overlays` below); **VL-13** |
| Phantom contract | "See prior width contract" with no table in repo | Contract must live in this file |
| Unrun verification | "typecheck passed", "admin_web green" | Paste command + path + exit code (`quality.mdc`) |
| Client logic smuggle | `useMemo` filter/sort over full API payload | Server query params; browser renders page |
| Filter pagination relocation | Move Prev/Next into filter grid; agent wraps or moves **Apply** | **Directory filter row** below; Apply stays direct grid child |
| Double chip chrome | Parent wrapper + chip both bordered | Parent renders chip directly (`Chips` below) |
| Boot HTML drift | Text inside `<div id="root">` | Empty `<div id="root"></div>` only |
| Demo KPIs / trash seed | Round numbers, `Acme`, duplicate row names in grids | **Fixture and seed data** below |

## Cold path first (non-negotiable)

Browser **renders** server output. Logic stays in Go.

| Concern | Server | Browser |
| :--- | :--- | :--- |
| Filter / search | Query params; SQL/CH in handler | Send params; show `items`, `total` |
| Sort | `sort`, `order` on API | Refetch |
| Pagination | `limit`, `offset` or cursor | Controls only |
| List envelope | `items`, `total`, `limit`, `offset`, `freshness`, `filters_applied`, `status_totals`, `sort` | Refetch on param change; no client envelope math |
| KPIs / aggregates | Handler or report row fields | Display |
| Freshness | `stale`, `ch_lag_seconds`, prefer `freshness_label` | Chip text from API |
| Money | Micros + currency or `*_display` from API | Format display fields only |
| Status | `status`, `status_label`, `status_tone` | Map tone enum to chip |
| Export | Server export endpoint or async job | Download link |
| Validation | 400 + field errors from handler | Show API errors |

Forbidden in new `web/src/**`: client-side filter/sort/reduce over full datasets; duplicated report keys; business rules that belong in handlers.

**Rule:** need a derived field -> add to handler DTO in the same PR as the UI field.

## Layer separation

One task = one layer owner (`frontend-modular.mdc`).

| Layer | Path | Owns | Must not |
| :--- | :--- | :--- | :--- |
| Pages | `web/src/pages/` | `useResource` / page hook + `api/*_api.ts`; URL to params; compose domain components | Tailwind layout trees, row formatting, overlay logic, invented fields |
| Domain UI | `web/src/domains/<domain>/` | Sections; macro Grid + micro Flex; `components/ui` primitives | Fetch (except via props/callbacks), cross-page Context, hand-rolled overlays |
| API transport | `web/src/api/*_api.ts` | Typed fetch; parse into generated types | Client filter/sort over full `items[]` |
| System | `web/src/shell/` | Reusable page chrome, directory primitives | Domain-specific API shapes |

Pages pass **props down**; domain sections do not call `fetch` except through callbacks wired at the page boundary.

## API contract workflow

1. Change `api/openapi/` and Go handler together.
2. `bash scripts/ci/admin/openapi.sh`
3. Regenerate TS from OpenAPI into `web/src/types/generated/`.

`live: true` on a route requires `/api/v1` backend (`report_live_routes_gate.sh`).

## Ship order (foundation first)

| Slug | Delivers | Close when |
| :--- | :--- | :--- |
| `admin_contract_gate` | OpenAPI matches handlers | `openapi_gate.sh` green |
| `admin_tokens` | Tailwind utilities in TSX + `tailwind.config.ts` | `app.css` = fonts + `@tailwind` only |
| `admin_shell` | Login, shell, nav, boot | Stub replaced; `TestAdminStaticRoutes` |
| `admin_page_chrome` | `PageLayout` section stack | Badge slot without wrapper chrome |
| `admin_directory_pattern` | One server-paginated list | No client full-list sort |
| `admin_detail_pattern` | One detail + PATCH | Fields subset of Go DTO |
| `admin_report_pattern` | One report page | Keys from OpenAPI/handler |
| `admin_integrations_hub` | Integrations landing | `StubBanner` on 501 |

---

## App shell (macro)

DOM chain from viewport to page content:

```
.admin-app-frame
  .admin-app[.is-sidebar-collapsed]
    aside.admin-sidebar
    .admin-main                    min-height: 0; overflow: hidden
      header.admin-header          breadcrumbs, search, theme, account
      main.admin-content#main-content   flex: 1; min-height: 0; overflow: hidden; padding
        <Outlet />                 route page
```

| Class | Contract |
| :--- | :--- |
| `.admin-main` | `display: flex; flex-direction: column; flex: 1; min-height: 0; overflow: hidden` |
| `.admin-content` | Fills remaining viewport below header; **clips** overflow; pages must scroll inside descendants |
| `.admin-header-breadcrumbs` | Route trail; must not overlap page content (no fixed positioning into content area) |

Forbidden: letting page content grow unbounded inside `.admin-content` without an internal scroll region (causes bottom clip).

---

## Page layout (`PageLayout`)

Canonical scaffold: `web/src/shell/page_layout.tsx`. `PageChrome` is a thin alias (`actions` prop maps to `headerActions`).

```
.admin-page-layout              flex column; flex: 1; min-height: 0
  header.admin-page-header      title, badge, description, headerActions
  .admin-page-workspace         flex column; flex: 1; min-height: 0; L1 surface + border
    .admin-control-panel?       toolbar / filters / section nav (z-index: 5)
    .admin-page-body            grid; flex: 1; min-height: 0; rows: minmax(0,1fr)
      main.admin-page-main      flex column; flex: 1; min-height: 0
      aside.admin-page-aside?   optional right rail
    footer.admin-page-footer?   pagination, export (z-index: 5)
```

### Workspace regions

| Region | Class | Surface | Typical content |
| :--- | :--- | :--- | :--- |
| Workspace shell | `.admin-page-workspace` | L1 | Border + padding around page body |
| Control panel | `.admin-control-panel` | L2 | Campaigns toolbar, Ops nav + actions, filter rows |
| Main | `.admin-page-main` | inherits | Table, stat grids, forms |
| Footer | `.admin-page-footer` | L2 | Pagination, export buttons |

Campaigns control panel variant: `.admin-control-panel:has(.admin-campaigns-toolbar)` drops side/bottom padding so filter row spans full width.

---

## Scroll and overflow (critical)

Viewport height is fixed at `.admin-content`. Every page must either **fill and scroll internally** or **scroll inside `.admin-page-main`**.

### Flex/grid min-height chain

Every flex/grid ancestor between `.admin-content` and the scroll container needs `min-height: 0` (or `minmax(0, 1fr)` for grid rows):

| Node | Required |
| :--- | :--- |
| `.admin-main` | `min-height: 0` |
| `.admin-page-layout` | `min-height: 0; flex: 1` |
| `.admin-page-workspace` | `min-height: 0; flex: 1` |
| `.admin-page-body` | `min-height: 0; flex: 1; grid-template-rows: minmax(0, 1fr)` |
| `.admin-page-main` | `min-height: 0; flex: 1` |

**Failure mode:** `admin-page-body` rows default to `auto` -> main grows with content -> `.admin-content` clips bottom (Ops tables, import sheet, long forms).

### Scroll modes for `.admin-page-main`

| Page kind | Main overflow | Child scroll |
| :--- | :--- | :--- |
| Campaigns directory | `overflow: hidden` | `.admin-campaigns-table-wrap` (`flex: 1; overflow: auto`) with sticky `thead` |
| Ops / stacked sections | `overflow-y: auto` when `:has(.admin-ops-block)` | Blocks use `flex: none`; no inner table scroll |
| Generic long form | `overflow-y: auto` on main or dedicated body wrapper | Single scroll container; sticky header/footer in dialogs |

### Table wrap variants

| Class combo | Use | Scroll | Header |
| :--- | :--- | :--- | :--- |
| `.admin-table-wrap.admin-campaigns-table-wrap` | Campaigns list | `flex: 1; overflow: auto` on wrap | `position: sticky; top: 0` on `th` |
| `.admin-table-wrap.admin-table-wrap--static` | Ops tables, small directory tables | `flex: none; overflow: hidden` (clip to `border-radius`) | `position: static` on `th` (no sticky) |

Rules:

- **Never** use `overflow: visible` on `.admin-table-wrap--static` (header background escapes rounded corners).
- Ops tables: `width: 100%` on table inside static wrap.
- Campaigns table: `width: auto` on `.admin-table.admin-table--campaigns` (column widths sum to content; horizontal scroll in wrap).

### Dialog, sheet, popover scroll

| Surface | Pattern |
| :--- | :--- |
| `Dialog` / `Sheet` (class C) | Fixed header + `flex-1 overflow-y-auto` body + optional sticky footer; bottom padding (`pb-6` / `pb-8`) so last field is not clipped |
| `Popover` / `Select` (class B) | `OverlayRoot` portal; trigger-anchored `position: fixed`; list `max-h-*` + `ui-scrollbar overflow-y-auto` (`PopoverContent` `panelScroll`, `SelectContent` inner div, `CommandList`) |
| `DropdownMenu` (class B) | Same anchor/reposition as Popover; domain adds `max-h-*` wrapper when item count can grow (see `campaign_list_columns_menu.tsx`) |
| Preferences / reset modals | One scroll container; avoid `flex-1` on empty body regions that create phantom scroll gaps |

Forbidden:

- Nested scroll containers fighting each other (outer `overflow: hidden` + inner `flex: 1` without `min-height: 0`).
- `position: sticky` table headers inside `overflow: hidden` static wraps (ops).

---

## Layout (macro Grid, micro Flex)

**Grid** owns macro structure; **Flexbox** owns everything inside a component.

### Macro (CSS Grid)

| Surface | Pattern |
| :--- | :--- |
| App shell | Sidebar + header + content (`admin-app`) |
| Page | `PageLayout` vertical stack |
| Dashboard cards | `grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr))` (`.admin-ops-stat-grid`) |
| Filter field matrix | `grid-cols-[repeat(auto-fill,minmax(12rem,1fr))] gap-4 items-end` -- owned as `CAMPAIGNS_FILTER_ROW` in `filter_panel.tsx`; use `DirectoryFilterForm layout="campaigns"` |

| Rule | Detail |
| :--- | :--- |
| Section owns macro template | `grid-template-columns` / `rows` on section root only |
| One chrome per region | One header, one control panel, one data section, one footer |
| Rhythm | `gap` on section grid between **peer cells** of one matrix only -- not between unrelated bands (`frontend-slop.mdc` **Layout contract**) |

### Micro (Flexbox)

| Pattern | Examples |
| :--- | :--- |
| Control internals | Icon + text, label + hint |
| Action bars | Toolbar button groups, Apply + pagination |
| Alignment | Badge/chip content, footer controls |
| Campaigns toolbar | Flex rows for actions, status chips, filter `FilterPanel` (see `filter_panel.tsx` layout consts) |

| Rule | Detail |
| :--- | :--- |
| Flex is local | Toolbar, footer, chip root -- not page-wide column replacing section grid |
| `gap` in flex/grid | Only between siblings in **one semantic group**; inter-group space uses grid tracks (`1fr`, `auto`), not `justify-between` + large `gap` |
| No layout escape | No `margin-left: auto` / `ms-auto` pushing controls out of assigned cell |
| Action bars | Inner flex row inside one grid cell -- not a second grid template |
| Data rows | Homogeneous server lists use semantic `<table>` via `DirectoryTable` / `OpsTable` -- not CSS Grid matrices (`frontend-slop.mdc` **Layout contract**) |

Full gap / spacer / table decision table: `frontend-slop.mdc` **Layout contract (Flex, Grid, semantic tables)**.

**Visual drift (съезжание):** symptom triage, **VL-*** root causes, and **VL-D1-D5** diagnostic protocol in `frontend-slop.mdc` **Visual layout drift taxonomy**. Do not patch with wrappers or `!` utilities -- fix the catalog row.

Forbidden for page layout:

- Page shell as nested flex columns instead of macro Grid
- `position: fixed` filter panels (inline accordion in flow only)
- Extra wrapper components that only add chrome
- Hand-rolled overlay open state when shadcn covers it

### Section stack (directory)

`PageLayout header` -> `controlPanel` (toolbar + filters) -> `main` (meta + table) -> `footer` (pagination/export).

Ops stack (`OpsPageShell`):

```
controlPanel:
  OpsNav (section tabs)
  actions toolbar (optional)
  filters toolbar (optional)
main:
  OpsStatGrid (optional)
  OpsBlock > OpsTable (repeat)
footer (optional)
```

---

## Directory filter row and pagination

Operator ask: move **Prev/Next** into the **filter grid** (bottom-right). That is **not** permission to relocate **Apply**.

Canonical reference: `web/src/domains/campaigns/list/campaigns_list_toolbar.tsx`; `web/src/shell/filter_panel.tsx`.

### Filter row contract

| Rule | Detail |
| :--- | :--- |
| One filter row grid | `grid-cols-[repeat(auto-fill,minmax(12rem,1fr))]` + `items-end` |
| Field cells | Labeled field block (shadcn `Label` + control) |
| **Apply** | Direct child of filter row grid, after last field; `type="submit"`; **no wrapper** |
| **Prev/Next** | Separate direct grid child after Apply; `PaginationPrevNext` |
| Column width | Pagination cell `w-full`; inner flex splits Prev/Next |
| Button height | Match field controls (`admin_kit.controlHeight` / default `Button`) |
| Footer | Remove duplicate pagination from footer when it lives in filter row |

DOM order:

```
.filterRow (grid)
  .filterField x N
  Button[Apply]
  PaginationPrevNext
```

### Agent failure modes (forbidden)

| What agents do | Correct |
| :--- | :--- |
| Split filters into side column with Apply | Single grid row; all peers |
| Wrap Apply + pagination together | Sibling grid items |
| Second row for Sort/Apply | Same row as other fields |
| Stack Prev/Next above Apply | Pagination is its own cell beside Apply |
| `margin-left: auto` on Apply wrapper | No auto margin on Apply |
| Fixed `width: 5.75rem` on pagination | `width: 100%` of grid column |
| Touch Apply when task is pagination only | Diff Apply line should be zero |

Campaigns toolbar: filter row is `FilterPanel` + `DirectoryFilterForm layout="campaigns"`; actions/summary rows are separate flex bands above the grid.

---

## Data tables

Admin lists are server-paginated. Prefer semantic `<table>` over CSS grid data matrices. **Column lifecycle, reorder/resize performance, and anti-patterns:** `frontend-slop.mdc` (**Directory tables**).

### Markup

| Rule | Detail |
| :--- | :--- |
| Elements | `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>` |
| Wrapper | `.admin-table-wrap` (see scroll variants above) |
| Table class | `.admin-table.admin-table--campaigns` (shared density/typography) |
| Empty / loading | One `<tr colSpan={n}>` or skeleton overlay |
| Numeric columns | `.num` or `tabular-nums` on `th`/`td` |
| Alignment | Name/start; money/status per column class |

Forbidden: bespoke subgrid row factories; `display: table*` CSS pretending to be a table.

### Campaigns column widths

| Rule | Detail |
| :--- | :--- |
| Layout | `table-layout: fixed`; explicit `width` on `col` from `campaign_list_column_widths.ts` probe |
| Table width | `width: auto` on table (sum of columns); horizontal scroll in wrap |
| Long text clip | Only via `campaignListEllipsisTextClass` / `campaignListHeaderLabelClass` (`campaign_list_classes.ts`); same contract for landers fixed table |
| User resize | Commit on `pointerup` only; live width via `col` ref during drag (`frontend-slop.mdc`) |
| Reorder | `moveDataColumn`; `key={columnId}` on cells; no width recompute when only order changes |
| Clamps | `clampCampaignListColumnWidthPx()` until content-based widths ship; do not add new arbitrary caps |
| Persist | `localStorage` key `aed.campaigns.listColumns.v7`; defer write to end of drop if possible |
| Gap bug | Unbounded saved `name` width + `width: 100%` on table causes empty column gap -- never remove content-based sizing |

### Landers column widths

| Rule | Detail |
| :--- | :--- |
| Layout | `table-layout: fixed`; percent widths on `colgroup` in `landers_list_table.tsx` |
| Ellipsis | Same named classes as campaigns (`campaign_list_classes.ts`); no ad-hoc `text-ellipsis` in `domains/creative/` |
| Numeric / dates | `campaignListCellContentClass` or badges -- no ellipsis on counts or relative timestamps |

### Ops tables

Use `OpsTable` (`ops_table.tsx`): static wrap, full width, no sticky header. Section title in `OpsBlock` above table (not inside wrap).

Status chips: consistent `min-w-*` so labels align across rows.

---

## Chips and badges

Defect class: **nested frames** (outer box around inner pill).

| Rule | Detail |
| :--- | :--- |
| One chrome layer | Chip owns border, fill, padding |
| Spacing | Tailwind or shadcn `Badge` variants |
| Vertical center | `inline-flex items-center` |
| Labels from API | `freshness_label`, `status_label` |

---

## Overlays (first-party)

Use primitives in `web/src/components/ui/`: `Select`, `DropdownMenu`, `Dialog`, `Popover`, `Tooltip`, `Sheet`. Implementation: `OverlayRoot` (`createPortal` to `document.body`) + `use_overlay_dismiss` + `floating_overlay_position.ts`. No `@radix-ui/*`.

**Surface taxonomy (A / B / C):** full rules, slop catalog, and repo audit in `frontend-slop.mdc` (**Overlays, scroll surfaces, and control height**). Summary:

| Class | Role | Scroll |
| :--- | :--- | :--- |
| **A Shell dock** | `AppSidebar`, mobile nav `Sheet` | Nav scroll inside aside/sheet; independent from page main |
| **B Anchor float** | Select, combobox, country picker, column menu, short action menus | Portal + fixed coords from trigger; **inner** `ui-scrollbar` list; reposition on ancestor scroll |
| **C Modal / sheet** | Dialog, command palette, import sheet | Backdrop; single body scroll region; three+ dismiss vectors (`frontend-slop.mdc` **UX scenario contract** §2) |

| Rule | Detail |
| :--- | :--- |
| Source | Owned in `web/src/components/ui/`; extend `admin_chrome.ts` |
| Anchor floats (B) | `subscribeFloatingPosition` on open; never leave menu at stale viewport coords while trigger moves |
| Behavior | Escape, click-outside, portal, z-index 60 on floats |
| Style | Tailwind on `className`; no `class-variance-authority` |
| Field width | Trigger `w-full` in grid cell |
| Control height | Same `admin_kit` / `adminChrome.control` height on every control in one filter row |
| Banned | Custom `[data-dropdown-open]`, hand-rolled fixed menus in `domains/`, `@radix-ui/*`, `components.json` |

Date range picker, column menu, import sheet: must not clip bottom of popover/sheet content (see **Dialog, sheet, popover scroll**).

**React loop guard (class B):** `select.tsx`, `popover.tsx`, `dropdown-menu.tsx` must memoize context values, avoid `[ctx,` effect deps, and use `mergeOverlayPosition` before `setPosition` (**OV-*** in `frontend-slop.mdc`; enforced by `ui_slop.sh`).

---

## Fetch and error UI

List lifecycle and charts: `react.mdc` (Hot vs Cold).

| State | Condition | UI |
| :--- | :--- | :--- |
| Render throw | Uncaught error in route subtree | `AppRouteErrorBoundary` on `<Outlet />` in `app_shell.tsx`; clears on `location.key` change (**RB-E***). Root boot in `main.tsx` may use plain `AppErrorBoundary`. |
| Initial load | `fetching && !data && !error` | `PageSkeleton` / grid skeleton |
| Blocking error | `error && !data` | `ErrorBlock`; no empty table |
| Stale revalidate | `data` present + error | Keep rows; toast or banner |
| Timeout | 15 s (`RESOURCE_FETCH_TIMEOUT_MS`) | Clear `fetching` in `finally` |
| Mutation | PATCH/POST | Toast only after 2xx (`apiConfirmed`); errors via `ApiError` -> `ErrorBlock` / `userErrorMessage` (`frontend-slop.mdc` **Mutation validation and error contract**) |
| Empty | `items.length === 0`, filters inactive | `EmptyState` |

Use `admin_error.ts` for operator-facing titles/messages; show technical details only in dev mode (`shouldShowAdminErrorDetails()`). Explicit vs slop catalog: `frontend-slop.mdc` **Explicit error handling vs error slop**.

No silent `catch` -> empty table. No `live: true` without `/api/v1`.

---

## Styling stack (Tailwind + first-party primitives)

| Layer | Path | Role |
| :--- | :--- | :--- |
| Theme | `app.css`, `tailwind.config.ts` | `@tailwind` + minimal base; zinc via `dark:` classes |
| Tokens | `lib/admin_kit.ts`, `lib/admin_chrome.ts` | Named Tailwind constants for shared chrome (`frontend-slop.mdc` **Shared style contracts**) |
| Primitives | `components/ui/` | First-party copies (`web/DESIGN.md`; no `@radix-ui/*`) |
| Utilities | `lib/utils.ts` | `cn()` |
| Domain UI | `domains/<domain>/` | Section layout; import `*_classes.ts` for repeated chrome |
| Pages | `pages/` | Compose only |

| Rule | Detail |
| :--- | :--- |
| New work | Tailwind in TSX; `components/ui` for interactive primitives |
| One owner per node | Tailwind only in TSX; BEM banned (`admin-*__*`, `campaign-*__*`); no `!` overrides patching legacy CSS (`frontend-slop.mdc` **Styling stack**) |
| `cn()` | Merge conditional classes |
| Colors | Theme tokens (`bg-background`, `text-muted-foreground`, `--admin-surface-*`) -- no hard-coded hex in TSX |
| Legacy | `*.module.css` sunsets on touch -- no new CSS Module files |

Forbidden:

- New `*.module.css` or per-domain `*.variants.ts`
- Raw `@radix-ui/*` outside `components/ui/`
- Global BEM under `domains/`
- `style={{}}` for layout (Tailwind instead)
- Pages importing stylesheets or heavy layout `className` trees

Gate: `bash scripts/ci/admin/ui_surface.sh`.

---

## Visual guidelines (simple)

Operator agreement: **one plain admin skin** for all routes. Linear scaffold, basic tables, light depth from surface steps -- not pixel-perfect tracker clones (Keitaro/Binom) and not a second theme per page.

**Priority:** data density and workflow > decoration. Small alignment gaps are acceptable; broken scroll, clipped tables, and invented demo data are not.

Styling source of truth: Tailwind in components + `web/src/styles/app.css` (entry only). **Forbidden:** `globals.css`, monolithic `admin-*` CSS, CSS variable theme soup. Reference: `web/DESIGN.md`. Typography: `web/src/lib/admin_typography.ts`.

### Product stance

| OK | Not required / banned |
| :--- | :--- |
| Dense directory tables, many columns, server pagination | Pixel-perfect copy of external tracker UIs |
| Functional color (status, ROI, GEO, conversion columns) | Per-route CSS skins (`binom-*`, `campaigns-list-workspace`, `tracker-shell--*`) |
| One dark + one light theme via existing toggle | Third "workspace" theme that only applies on campaigns/customers |
| `admin-*` classes and CSS variables | Hard-coded hex/rgb in TSX |
| First-party `components/ui` overlays only | Hand-rolled dropdown positioning in `domains/` |

### Linear layout (fixed scaffold)

Every page uses the same macro skeleton. Do not invent alternate page chrome.

**App shell** (`app_shell.tsx`):

```
+-------------+------------------------------------------+
|             |  admin-header (breadcrumbs, search)      |
| admin-      +------------------------------------------+
| sidebar     |  admin-content                           |
| (nav)       |    PageLayout (see below)                |
|             |                                          |
+-------------+------------------------------------------+
```

**Page** (`PageLayout`):

```
admin-page-header          title, badge, header actions
admin-page-workspace       L1 panel (border + padding)
  admin-control-panel?     filters, section nav, toolbar buttons
  admin-page-body          grid: main [| aside]
    admin-page-main        table / forms / stat blocks
    admin-page-aside?      optional right rail
  admin-page-footer?       pagination, export
```

Rules:

- Sidebar stays left; header stays above content; control panel is **inside** workspace, above main -- never floating over content.
- Main and aside share one row; footer spans full width below body.
- Optional `aside` is content, not a second menu.

### Surfaces and depth

Hierarchy = **shade step + hairline border**, not shadows.

| Level | Token | Use |
| :--- | :--- | :--- |
| 0 | `--admin-surface-0` / `--admin-bg` | Canvas: `admin-main`, page background |
| 1 | `--admin-surface-1` | Workspace shell, sidebar, table wrap, footer, control panel |
| 2 | `--admin-surface-2` | Inputs/buttons inside L1, table header, menu/dialog body |
| 3 | `--admin-surface-3` | Deepest inset: search kbd, column preset chips |

**Nesting rule:** child surface = parent level + 1 (max 3). Example: workspace (L1) -> control panel content (L2) -> input (L2/L3 per globals descendants).

**Borders:** always `1px solid var(--admin-border)` or `var(--admin-border-light)` on panel edges and table rows. Do not remove borders to "flatten" UI.

**Shadows:** no drop shadow on panels, cards, or table wraps. Allowed: `var(--admin-overlay-shadow)` on popovers, dropdowns, dialogs, date picker -- floating layers only.

Formula and OKLCH ladder: `web/DESIGN.md` (**Surface hierarchy**).

### Corners (basic, not pill UI)

| Token | Value | Apply to |
| :--- | :--- | :--- |
| `--admin-radius` | `6px` | Workspace, table wrap, control panel, footer, dialog shell |
| `--admin-radius-sm` | `4px` | Buttons, inputs, selects, calendar cells, small chips |

| Rule | Detail |
| :--- | :--- |
| Default shape | Slightly rounded rectangles -- not `rounded-full` on fields and buttons |
| Table wrap | `border-radius: var(--admin-radius)` + `overflow: hidden` on static wraps (Ops) so header bg respects corners |
| Banned | `rounded-2xl` / heavy pill chrome on new panels; `rounded-md border` ad-hoc wrappers in TSX |
| Consistency | Popover/menu/calendar/date-range use same tokens as column menu (`admin-columns-menu`, `admin-date-range-menu`) |

### Color

| Role | Token / pattern |
| :--- | :--- |
| Brand / primary CTA | `bg-primary`, `text-primary-foreground`; `Button` default variant |
| Body text | `--admin-fg`, `--admin-fg-strong` |
| Secondary / labels | `--admin-muted`, `--admin-fg-secondary` |
| Positive money / OK status | `--admin-positive-fg`, `--admin-status-active-*` |
| Negative money / fail | `--admin-negative-fg`, `--admin-status-*` for paused/archived |
| Row emphasis | `--admin-row-warning-*`, `--admin-row-negative-*`, `--admin-row-selected-*` (subtle; no full-row neon) |
| Metric zero / empty | `--admin-metric-zero-fg` or muted class -- zeros and em-dash must recede |
| Key conversion column | `--admin-metric-conversion-fg` -- slightly stronger weight/color (e.g. Leads) |
| Filter strip | `--admin-filters-bg` on campaigns toolbar filter row |

Use color **only** to encode data or state. Decorative gradients, glow, and per-country random pill colors (except stable GEO badge mapping) are banned.

### Spacing and typography (canonical)

**Single source of truth:** `web/src/lib/admin_spacing.ts` (re-exported from `admin_kit.ts`). Domains import shell roles or `adminKit` / `adminSpacing` / `adminTypography` -- never raw Tailwind scale drift.

#### Gap scale (only these five)

| Token | Tailwind | px | Use |
| :--- | :--- | ---: | :--- |
| `adminSpacing.gap.xs` | `gap-1` | 4 | Icon + label inside one control |
| `adminSpacing.gap.sm` | `gap-1.5` | 6 | Chip inner, tight label row |
| `adminSpacing.gap.md` | `gap-2` | 8 | Button groups, toolbar peers, field label to control |
| `adminSpacing.gap.lg` | `gap-3` | 12 | Section stacks, panel interiors, main column |
| `adminSpacing.gap.xl` | `gap-4` | 16 | Workspace bands, filter matrix, main + aside grid |

**Banned:** `gap-5`, `gap-6`, `gap-7`, `gap-8` in `web/src/domains/**` and `web/src/pages/**` (CI: `ui_slop.sh`).

**Margin:** avoid ad-hoc `m-*` / `mt-*` between bands; use `PageLayout` bands, `adminSpacing.flex.sectionStack`, or grid tracks (`frontend-slop.mdc` **Layout contract**).

#### Inset scale (padding)

| Token | Class | Use |
| :--- | :--- | :--- |
| `adminSpacing.inset.canvas` | `px-6 py-4` | Route canvas (`PageCanvasInset`) |
| `adminSpacing.inset.panel` | `p-4` | Cards, selection panel, section panels |
| `adminSpacing.inset.band` | `px-4 py-2` | Dialog section header, table caption |
| `adminSpacing.inset.bandLg` | `px-4 py-3` | Dialog footer, raised band |
| `adminSpacing.inset.tableCellX` | `px-4` | Table `th` / `td` horizontal |
| `adminSpacing.inset.footer` | `px-6 pt-3` | Page footer band |
| `adminSpacing.inset.emptyState` | `px-6 py-16` | `EmptyState` only |

Control horizontal padding: `adminKit.controlPaddingX` (`px-3`). Do not mix `px-2` on buttons/inputs.

#### Typography roles

| Token | Size / weight | Use |
| :--- | :--- | :--- |
| `adminTypography.pageTitle` | 18px bold | Page `h1` only |
| `adminTypography.sectionTitle` | 13px semibold | Section `h2`, empty state title |
| `adminTypography.panelTitle` | 13px semibold | Aside control panel title |
| `adminTypography.body` | 13px regular | Body, controls, table cells |
| `adminTypography.bodyMuted` | 13px muted | Secondary copy, list meta |
| `adminTypography.label` | 13px medium | Form labels (`FilterField`) |
| `adminTypography.labelMuted` | 13px muted | Definition list labels |
| `adminTypography.caption` | 11px semibold caps | Table headers, column labels |
| `adminTypography.badge` | 12px (`text-xs`) | Status badges only |
| `adminTypography.monoData` | 12px mono | UUID, deployment id, secrets |

**Banned in domains/pages:** `text-sm`, `text-base`, `text-xs`, arbitrary `text-[Npx]` (CI gate). **Banned:** `font-bold` outside page title; use role token.

#### Layout flex presets

| Export | Use |
| :--- | :--- |
| `adminSpacing.flex.buttonGroup` | Refresh + Export + Create cluster |
| `adminSpacing.flex.actionsRowEnd` | Dialog footer actions |
| `adminSpacing.flex.pageHeader` | Title row + header actions |
| `adminSpacing.flex.workspaceFlat` | Page workspace vertical rhythm |
| `adminSpacing.grid.filterMatrix` | Directory filter field grid |
| `COMPACT_TOOLBAR_ROW_CLASS` | Pagination + page size row |

Verify: `bash scripts/ci/admin/ui_slop.sh`

### Typography

| Content | Face | Class |
| :--- | :--- | :--- |
| Labels, names, nav, buttons | Inter Variable | `font-sans`, body default |
| Money, counts, %, ROI, IDs in grids | Inter + tnum | `.num`, `tabular-nums`, `font-numeric`, `admin-tabular-nums` |
| UUID, JSON, URLs, secrets | IBM Plex Mono | `font-mono`, `admin-data-mono`, `ui-code-block` |

| Rule | Detail |
| :--- | :--- |
| Table body | `adminTypography.body` (13px / 18px line) |
| Table header | `adminTypography.caption` (11px semibold caps) |
| Row height | `adminKit.tableRowHeight` (`34px`) |
| Headings | `adminTypography.pageTitle` / `sectionTitle` only; `tracking-tight` on page title |
| Mono misuse | Never `font-mono` for money or KPI columns |

### Controls

Use `web/src/components/ui/*` primitives + `admin_kit.ts` / `admin_chrome.ts` tokens. **No** `.admin-btn` / `.admin-input` BEM classes in TSX or new CSS.

Primitive stack (variant vs action, shell roles, import matrix): `frontend-primitives.mdc`. Frontend patterns (паттерны фронтенда): `frontend-patterns.mdc`.

| Control | Owner | Notes |
| :--- | :--- | :--- |
| Button | `components/ui/button.tsx` | `adminKit.controlHeight` (`min-h-7`); default variant only in domains |
| Text field | `components/ui/input.tsx`, `select.tsx`, `textarea.tsx` | `adminKit.controlText`, `controlRadius` (`rounded-none`) |
| Label | `components/ui/label.tsx` + `FilterField` | `adminKit.fieldLabelClass` |
| Muted hint | `text-muted-foreground` | Secondary copy, column headers |
| Link | `Button variant="link"` or `text-primary` | In-table links only; not for primary actions |

Toolbar pattern (campaigns): `campaigns_list_toolbar.tsx` -- filter row via `DirectoryFilterForm`, summary band, action row (`frontend-slop.mdc` layout contract).

### Tables (visual)

| Rule | Detail |
| :--- | :--- |
| Markup | Semantic `<table>` inside `.admin-table-wrap` |
| Density | Fixed row height; horizontal scroll when many columns; no card-per-row layouts |
| Header | L2 background (`--admin-table-header-bg`); sticky only inside **scrollable** campaigns wrap |
| Ops / small tables | `.admin-table-wrap--static`: full width, no sticky, `overflow: hidden` |
| Hover | `--admin-table-row-hover` on body rows |
| Totals row | `--admin-table-totals-bg` in `tfoot` when present |
| Alignment | Names start-aligned; metrics `.num` end-aligned with tabular figures |

Campaigns: table `width: auto` (sum of columns); column widths from content probe in `campaign_list_column_widths.ts`. Landers: percent `colgroup` + shared ellipsis classes -- see **Landers column widths** and `frontend-slop.mdc` (**Fixed-layout directory tables**).

### Chips, badges, GEO

| Rule | Detail |
| :--- | :--- |
| One chrome layer | Chip owns border + fill; no wrapper box around chip |
| Status | Map API `status_tone` to existing status classes |
| Country | `CountryFlagIcon` -- SVG **16x12**, not emoji; optional ISO code beside flag |
| Nav sections | `OpsNav`, `SectionNav` -- simple text/tabs in control panel, not underline-only links |

### Overlays (look and feel)

First-party primitives skinned via `admin_chrome.ts` / `app.css` domain hooks:

| Surface | Must match |
| :--- | :--- |
| Dropdown / column menu | `campaign-columns-menu`, `adminChrome.floating` |
| Date range | `campaign-date-range-picker` |
| Dialog / sheet | Card surface tokens; `admin-overlay-shadow` where defined |
| Scroll | Class B: inner list scroll; class C: single body scroll; bottom padding so last control is not clipped |

### Data hierarchy in grids

| Value | Treatment |
| :--- | :--- |
| `0`, `—`, empty | Muted (`--admin-metric-zero-fg`) |
| Ordinary metrics | Default `--admin-fg` + tabular nums |
| Primary conversion (e.g. Leads) | Slightly bolder + `--admin-metric-conversion-fg` |
| Profit / ROI | `--admin-positive-fg` / `--admin-negative-fg`; optional subtle row bg via row tone helpers |
| Rates with warning band | `--admin-metric-rate-warn-fg` when server signals warn tone |

All thresholds and tones come from API or shared format helpers -- not hardcoded per-row `if` in TSX for business rules.

### Motion

| Allowed | Banned |
| :--- | :--- |
| `transition-colors` on buttons/rows | Bouncy layout animations |
| Overlay open/close transitions on primitives | Parallax, scale-on-hover on tables |
| `prefers-reduced-motion` respected | Auto-playing chart motion |

### Visual banned list

| Pattern | Why |
| :--- | :--- |
| `campaigns-list-workspace`, `binom-*`, `tracker-shell--workspace` | Competing skins -- use global theme only |
| Emoji country flags | Inconsistent rendering; use SVG |
| Hex colors in TSX | Use CSS variables |
| Nested bordered chip wrappers | Double chrome |
| Box shadow on static panels | Depth = surface step |
| `rounded-full` on inputs/buttons (new code) | Conflicts with simple 4px radius system |
| Decorative icons on every toolbar action | Text labels + density first |
| Demo KPI literals in components | `anti-slop.mdc` fixture rules |

### Visual agent checklist

| Step | Check |
| :--- | :--- |
| 1 | Page uses `PageLayout` linear slots -- no custom shell |
| 2 | Panels use `--admin-surface-*` + `--admin-border`; no ad-hoc `border-gray-*` |
| 3 | Corners: `6px` panels, `4px` controls |
| 4 | Table in `.admin-table-wrap`; Ops uses `--static` variant |
| 5 | Metrics use `.num` / tabular; zeros muted |
| 6 | Overlays match column menu / date picker tokens |
| 7 | No per-route theme CSS; no hex in TSX |
| 8 | Scroll: content not clipped at viewport bottom (`Scroll and overflow` above) |

---

## System components

Import from `web/src/shell/`. Do not duplicate layout in domain files.

### Page shell

| Component | Role |
| :--- | :--- |
| `PageLayout` | Full page scaffold (canonical) |
| `PageChrome` | Alias for `PageLayout` |
| `PageBreadcrumbs` | Route trail in app header |
| `SectionNav` | Pill nav for domain sections |
| `PageToolbar` | Action row |

### Directory pattern

| Component | Role |
| :--- | :--- |
| `FilterPanel`, `DirectoryFilterForm`, `FilterField` | Filter section |
| `FilterApplyButton`, `FilterResetButton` | Submit actions |
| `PaginationPrevNext`, `PaginationPageSize` | Pagination controls |
| `ToggleChipGroup` | Server-driven quick filters |
| `DirectoryListMeta` | "Showing X-Y of Z" |
| `DirectoryTable`, `DirectoryTableSkeleton` | Scrollable semantic table frame |
| `RowActionsMenu` | Row kebab menu |
| `AppliedCustomerBanner`, `CustomerScopeBar` | Customer scope |

### States

| Component | Role |
| :--- | :--- |
| `EmptyState` | No data / no results |
| `ErrorBlock` | Blocking errors |
| `StubBanner` | 501 / not wired |
| `PageSkeleton` | Initial load |

### Hub and KPI

| Component | Role |
| :--- | :--- |
| `HubLinkGrid`, `HubLinkCard` | Domain hub landing |
| `StatPanel`, `StatRow` | KPI tiles |
| `BentoCard` | Settings bento grid |

### Ops-specific (domain)

| Component | Path | Role |
| :--- | :--- | :--- |
| `OpsPageShell` | `ops_page_shell.tsx` | Ops `PageLayout` + nav/actions |
| `OpsTable`, `OpsBlock` | `ops_table.tsx` | Static tables + section titles |
| `OpsStatGrid`, `OpsStatPanel` | `ops_stat_panel.tsx` | Health / summary cards |
| `OpsNav` | `ops_nav.tsx` | Ops section tabs |
| `OpsStatusChip` | `ops_status.tsx` | Pass/warn/fail chips |

---

## Page patterns

### A. Directory list (canonical -- Campaigns)

```
PageLayout
  controlPanel: CampaignsListToolbar (actions, filters, summary)
  main: CampaignsListTable
  footer: pagination + export
```

Reference: `list/campaigns_directory.tsx`. Table fills viewport; scroll inside `.admin-campaigns-table-wrap`.

Filter layouts on `DirectoryFilterForm`:

- `layout="directory"` -- campaigns-shaped wide matrix.
- `layout="auto-fill"` -- `minmax(12rem, 1fr)` (customers, audit, billing).

### B. Domain hub

```
PageChrome / PageLayout
  SectionNav
  HubLinkGrid > HubLinkCard
```

Examples: `fraud_hub.tsx`, `integrations_hub.tsx`.

### C. Ops dashboard

```
OpsPageShell
  OpsStatGrid (optional)
  OpsBlock > OpsTable (repeat)
```

Reference: `ops_home.tsx`. Main scrolls (`:has(.admin-ops-block)`); tables use static wrap.

### D. Settings / forms

```
PageLayout
  read-only panels + PageToolbar
  Dialog / Sheet for mutations
```

### E. Progressive disclosure (Campaigns metrics)

| Tier | Trigger | Surface |
| :--- | :--- | :--- |
| 0 | Table row | Slim columns |
| 1 | Metric cell | `Popover` + chart |
| 2 | Row menu | `Sheet` overview |

Shared: `campaign_metrics_shared.tsx`.

---

## Fixture and seed data (user-visible)

**Scope:** fallbacks, seed catalog, e2e payloads, `?chart_mock=1` dashboard preview. Production pages are API-only.

Canonical catalog: `cmd/admin/seed_catalog.go`. Extend arrays there; no parallel trash catalogs in `web/`.

### Trash naming (forbidden)

| Pattern | Examples (banned) | Required |
| :--- | :--- | :--- |
| Tutorial tokens | `Foo`, `Bar`, `Lorem` | Industry-realistic names |
| Acme / widget | `Acme Corp`, `Test Company` | Names from seed catalog |
| Ordinal labels | `Customer 1`, `Campaign #42` | Semantic names |
| Generic personas | `John Doe`, `Test User` | Role + domain email |
| Placeholder leaks | `TBD`, `N/A` in grid cells | `EmptyState`, `StubBanner`, or omit |

### Round numbers (forbidden in metrics)

| Surface | Banned | Required |
| :--- | :--- | :--- |
| Counts | `10000`, `50000`, `100000` | Irregular digits: `18473`, `902841` |
| Money | Every row `$100.00` | Non-zero cent tails, vary per row |
| Rates | `10.00%`, `50%` on every row | Jagged: `3.17%`, `11.84%` |
| Lag | `60s`, `300s` everywhere | Mixed seconds from handler |

**Exception:** pagination `limit` enums are not KPIs.

### Duplicates (forbidden in one view)

No two rows with same display `name`/`title`/`email`; no column with identical value on every row; no `(customer, campaign)` pair duplicates.

### Verification (fixture touch)

```bash
rg -n '(?i)\b(Acme|Foo|Bar|Baz|Lorem|Test User|Customer [0-9]+|Campaign [0-9]+|John Doe)\b' web/src/ \
  --glob '!**/*.spec.*' --glob '!**/placeholder.ts'
rg -n '\b(10000|50000|100000|1_000_000)\b' web/src/domains/ --glob '*.tsx'
```

---

## Product honesty

`StubBanner` on 501; toast after 2xx; form fields match PATCH DTO; no demo KPIs; no `(skeleton)` user copy; fixture rules above.

Report naming: canonical `silent-reject-*` routes/fields; no user-visible "Ghost" when API uses `silent_reject_*`.

---

## Server static embed

| Rule | Detail |
| :--- | :--- |
| Embed path | `internal/controlplane/admin_static_stub/` |
| Boot marker | Empty `<div id="root"></div>` in `index.html` / `login.html` |
| Replace | Same PR as `web/dist` when `admin_shell` ships dist |

---

## Verification

```bash
bash scripts/ci/admin/openapi.sh
bash scripts/ci/admin/web.sh
go test ./internal/controlplane/ -run TestAdminStaticRoutes -count=1
cd web && npm run typecheck
bash scripts/ci/admin/ui_surface.sh
```

UI PR must paste commands actually run.

Layout regression checks (manual):

- Ops home: scroll to bottom of Doctor checks; table corners flush with wrap radius.
- Campaigns: table fills viewport; horizontal scroll; no gap between Name and metrics.
- Import sheet / Preferences dialog: last field visible above fold when scrolled.

---

## Agent checklist

| Step | Action |
| :--- | :--- |
| 0 | `frontend-slop.mdc` **Agent execution protocol**: scoped `rg`, catalog IDs, report format — no subjective praise |
| 0b | RBAC: server `RequirePermission` on every new `/api/v1` route; client nav/role is UX only (`control-plane.mdc` **RBAC**) |
| 0c | Layout drift: triage to **VL-*** + **VL-D3** grep; no wrapper/`!` patches (`frontend-slop.mdc` **Visual layout drift taxonomy**) |
| 1 | Confirm operator spec + OpenAPI route/handler contract |
| 2 | Follow cold path; no client list business logic |
| 3 | Handler/DTO before UI field |
| 4 | Use `PageLayout` section stack; respect **Scroll and overflow** |
| 5 | Campaigns table: scrollable wrap + column clamps; Ops: static wrap |
| 6 | Chip: one chrome layer; overlays: shadcn only |
| 7 | Apply/pagination filter row rules if touching directory toolbar |
| 8 | Seed/fallback: no trash names, round KPIs, duplicate rows |
| 9 | Paste verification commands actually run |
| 10 | Operator stop -> revert; no wrapper stacks |
| 11 | **Visual guidelines (simple):** linear layout, admin tokens, no per-route skins |
| 12 | Scroll/overflow + fixture rules when touching layout or seed data |

## Related rules

`frontend-modular.mdc`, `anti-slop.mdc`, `cold-path.mdc`, `control-plane.mdc`, `development.mdc`, `quality.mdc`, `react.mdc`, `structure.mdc`, `web/DESIGN.md`.
