---
description: Admin UI primitives stack - kit, chrome, components/ui, shell roles; variant vs action; no duplicate controls
globs:
  - web/src/components/ui/**
  - web/src/shell/**
  - web/src/lib/admin_kit.ts
  - web/src/lib/admin_chrome.ts
  - web/src/domains/**
  - web/src/pages/**
alwaysApply: false
---

# Frontend primitives

## Purpose

Subset of `frontend-patterns.mdc` **Pattern 6** — visual controls only. One **Button** (or **Input**) everywhere: shared physics (height, focus, hover, disabled, loading), different **variants** (color), different **roles** (Primary, Apply), different **actions** (`onClick` in domain/workspace). Domains must not reimplement hover or control height.

Full SPA pattern (паттерны фронтенда; composition, effects, races, errors, async/cancel): `frontend-patterns.mdc`.

Cross-ref: `frontend-modular.mdc` (layer map), `ui.mdc` (controls table, overlays), `frontend-slop.mdc` (**Shared style contracts**, **VL-11** height drift), `docs/CONTROL_PLANE_UI_SCOPE.md` (KEEP surfaces, **Export Hub**).

## Stack (bottom to top)

| Layer | Path | Owns | Example |
| :--- | :--- | :--- | :--- |
| T1 Tokens | `web/src/lib/admin_kit.ts` | `controlHeight`, `buttonShell`, `focusRing`, `fieldLabelClass` | `min-h-7`, `px-3`, label caps |
| T2 Variant chrome | `web/src/lib/admin_chrome.ts` | `buttonVariantClass`, `adminChrome.control`, badge maps | `variant="brand"` hover colors |
| T3 Primitive | `web/src/components/ui/*` | HTML behavior: `loading`, `asChild`, `disabled`, `type` | `button.tsx`, `input.tsx`, `select.tsx` |
| T4 Shell role | `web/src/shell/*` | Semantic preset of variant + shape; field chrome | `PrimaryActionButton`, `FilterField` |
| T5 Domain | `web/src/domains/<domain>/` | Label text, `onClick`, `value`/`onChange`, layout grid | Save handler from workspace hook |
| T6 Page | `web/src/pages/*` | Wire: `<Directory {...useWorkspace()} />` | No styling |

**Rule:** color and interaction chrome change only at T1-T3 (or T4 role). **Action** (what happens on click) lives at T5-T6 only.

## Primitives catalog

Extended control primitives beyond `Button` / `Input`. Paths are T3 (`components/ui`) or T4 (`shell` role). Domains import T4 or T3 only -- not `admin_chrome`.

| Primitive | T3 path | T4 shell role | Modes / notes |
| :--- | :--- | :--- | :--- |
| AdminError | `lib/admin_error.ts` (copy, `userErrorMessage`) | `shell/error_block.tsx`, `shell/admin_error_page.tsx` | blocking (page), inline (`ErrorBlock`), mutation (`actionError` slot); use `panelError` for 403/501 |
| DropdownMenu | `components/ui/dropdown-menu.tsx` | use as-is | overlay class B; scroll + reposition per `ui.mdc` / **VL-13** |
| Calendar / DateRange | `components/ui/calendar.tsx` (day grid), `components/ui/datetime_picker.tsx` (`CalendarPicker`) | `shell/toolbar_date_range_picker.tsx`, `shell/filter_date_range.tsx` | One popover field: `CalendarPicker` with `mode` (`date` / `datetime` / `month`) and `showTime` (hour/minute panel; default true when `mode="datetime"`). `DatePicker` = `mode="date"`. `DatetimePicker` accepts `showTime={false}` for day-only UI while keeping `YYYY-MM-DDTHH:mm` wire. Domains must not fork calendar markup. |
| RadioGroup | `components/ui/radio-group.tsx` | `FilterField` wrapper in `shell/filter_panel.tsx` | directory filter rows and editor forms |
| SearchableSelect | `Popover` + `Input` / `Command` in `components/ui` | `shell/searchable_filter_select.tsx` | filter combobox; country/customer pickers reuse same shell |
| ControlPlaneSelectTable | — | `shell/control_plane_select_table.tsx` | CP directory list: Select | Name | Actions (via `renderActions`); single selection |
| DirectorySelectOverviewTable | — | `shell/directory_select_overview_table.tsx` | Select + Name + Actions + Overview dialog; pass `recordById`, `buildOverviewFields`, `directoryRecordMap` |
| DirectoryOverviewDialog | — | `shell/directory_overview_dialog.tsx` | Row Overview modal: label/value fields, optional footer (export, deep links) |
| DirectoryRowActionsMenu | — | `shell/directory_row_actions_menu.tsx` | Actions column menu; first item Overview when `onOverview` set |
| ControlPlaneSelectionPanel | — | `shell/control_plane_selection_panel.tsx` | Aside control panel; actions disabled until row selected |
| FileUploadField | — | `shell/file_upload_field.tsx` | Hidden native file input; outline trigger; selected name + Clear |
| FieldGroup | — | `shell/field_group.tsx` | Bordered panel with label legend; not `<fieldset>` |
| CollapsibleSection | — | `shell/collapsible_section.tsx` | Ghost button + chevron; `aria-expanded`; not `<details>` |

## Spacing and typography (canonical)

**Source:** `web/src/lib/admin_spacing.ts` (`adminSpacing`, `adminTypography`); re-exported from `admin_kit.ts`.

| Layer | May use raw Tailwind gap/p/text? |
| :--- | :--- |
| `lib/admin_spacing.ts`, `lib/admin_kit.ts`, `lib/admin_chrome.ts` | Yes (defines tokens) |
| `components/ui/*`, `shell/*` | Only via `adminSpacing` / `adminTypography` |
| `domains/*`, `pages/*` | **No** -- shell layout exports, `FilterField`, primitives |

Gap scale: `xs` (4px), `sm` (6px), `md` (8px), `lg` (12px), `xl` (16px) only. Banned in domains: `gap-5+`, `text-sm`, `text-base`, `text-xs`, `text-[Npx]`. CI: `bash scripts/ci/admin/ui_slop.sh`.

Full tables: `ui.mdc` **Spacing and typography (canonical)**.

New repeated chrome: extend `admin_spacing.ts` or this catalog before copying markup in `domains/`.

## Export Hub UI

Control Plane report routes do not mount heavy `DirectoryTable` bodies. Pattern:

| Surface | Required |
| :--- | :--- |
| Frozen / export-only report page | `ExportOnlyReportStub` (Phase B shell) + `StubBanner` explaining async export |
| Primary CTA | Link or button to Export Hub with pre-filled query |
| Deep link helper | `buildExportHubHref({ reportKey, customerId, from, to, format })` -> `/exports?...` (Phase C); until then `buildReportJobsHref` -> `/reports/jobs?...` |
| Reference | `web/src/pages/report_export_stub_page.tsx` + `web/src/shell/report_export_stub_route.tsx` |

**Banned on CP report routes:** client-held report tables, `useMemo` aggregate over full report payloads, fake empty rows when export is the only supported path.

Catalog keys: `web/src/lib/report_paths.ts` (`TYPED_*_REPORT_KEYS`, `EXPORT_ONLY_REPORT_KEYS`). Scope: `docs/CONTROL_PLANE_UI_SCOPE.md` (**Export Hub**).

## Button: one base, many configs

Canonical implementation: `web/src/components/ui/button.tsx`.

| Concern | Where | Domains |
| :--- | :--- | :--- |
| Shell (size, padding, focus ring) | `adminKit.buttonShell` + shared Tailwind on `Button` | Never copy |
| Hover / border / fill | `buttonVariantClass[variant]` in `admin_chrome.ts` | Use `variant=` only |
| Loading spinner, `aria-busy` | `Button` `loading` prop | Pass `loading={saving}` |
| Link styled as button | `Button asChild` + `Link` | Not manual `buttonVariants()` on `<a>` |
| Business action | `onClick` / `type="submit"` in domain | Not `SaveCampaignButton` component |

### Variants (`ButtonVariant`)

Defined in `admin_chrome.ts`: `default`, `brand`, `accent`, `secondary`, `outline`, `ghost`, `destructive`, `link`.

| Need | Use |
| :--- | :--- |
| Primary CTA (Save, Create, Invite) | `PrimaryActionButton` or `variant="brand"` |
| Secondary (Clone, Close) | `SecondaryActionButton` or `variant="secondary"` / `outline` |
| Danger (Void, Delete) | `variant="destructive"` |
| Text link in prose | `variant="link"` |

New visual style = **new row in `buttonVariantClass`**, not `className="bg-..."` in a domain file.

### Shell role wrappers

`web/src/shell/action_buttons.tsx` — thin presets over `Button`:

| Export | Default | Use |
| :--- | :--- | :--- |
| `PrimaryActionButton` | `variant="brand"` | Main mutation on a page or dialog |
| `SecondaryActionButton` | `variant="outline"`, `shape="pill"` | Secondary row actions |
| `FilterApplyButton` | `type="submit"`, `variant="brand"` | Directory filter forms |
| `FilterResetButton` | `variant="outline"` | Clear filters |

Prefer role exports on **KEEP** pages when the intent is semantic (Apply vs Save), not when only color differs arbitrarily.

**Banned:** domain-specific `*ActionButton.tsx` that only sets `variant` (e.g. `CloneCampaignButton`). Use `Button` / shell role + props.

## Input and fields: one control string

Canonical text control: `adminChrome.control` applied in `components/ui/input.tsx`, `select.tsx`, `textarea.tsx`.

| Concern | Where |
| :--- | :--- |
| Height, border, focus, invalid ring | `adminChrome.control` / `admin_kit` |
| `type`, `name`, `value`, validation attrs | Domain / primitive props |
| Label + `htmlFor` + gap | `FilterField` (`shell/filter_panel.tsx`) or `Label` + `Input` |

Patterns:

```tsx
// Filter / directory row
<FilterField htmlFor="customer-id" label="Customer ID">
  <Input id="customer-id" value={draft} onChange={...} />
</FilterField>

// Editor field (same primitive, same control class)
<Label htmlFor="campaign-editor-name">Name</Label>
<Input id="campaign-editor-name" value={form.name} onChange={...} />
```

**Banned in `domains/`:**

- Import `admin_chrome` or `buttonVariantClass` for one-off styling
- Raw `<button>` / `<input>` with Tailwind hover chains (use `Button` / `Input`)
- Second field wrapper (`FormField`, `DomainInput`) that duplicates `FilterField` without promoting to `shell/`

`InputWithIcon` (`shell/form_shell.tsx`) is allowed for search-style inset; new inset patterns extend `adminChrome.controlFieldGroup`, do not fork control height.

## Action vs variant (mental model)

| Layer | Question | Example |
| :--- | :--- | :--- |
| Variant | How does it look? | `outline`, `destructive` |
| Role | What UX slot? | `FilterApplyButton` |
| Action | What does it do? | `onSave`, `onClone`, `POST` via workspace |
| State | Can it run now? | `disabled`, `loading`, RBAC gate |

Workspace hook (`use_*_workspace.ts`) owns **action state** (`saving`, `error`). Primitive owns **pending UI** (`loading`).

## Page-level composition (no duplicate lifecycle)

Directory pages share the same **lifecycle**, not the same **markup copy**:

1. Scope gate -> `EmptyState` if required id missing
2. `fetching && !hasSnapshot` -> `PageSkeleton`
3. Blocking error -> `ErrorBlock`
4. Content inside `PageLayout` / `PageChrome` / `OpsPageShell`

Extract repeated lifecycle to `shell/` (e.g. `DirectoryPageShell`) on touch; do not copy the four `if` blocks into every new KEEP list.

API error presentation: `panelRouteError` pattern (`integrations_nav.tsx` today) — one helper in `shell/panel_error.tsx`, not `*_panelError` per domain.

## Import matrix

| From | May import |
| :--- | :--- |
| `components/ui/*` | `admin_kit`, `admin_chrome`, `lib/utils` |
| `shell/*` | `components/ui/*`, `admin_kit`, `admin_chrome` |
| `domains/*` | `components/ui/*`, `shell/*` — **not** `admin_chrome` |
| `pages/*` | `domains/*`, hooks — **not** `components/ui` for new chrome |

## Control Plane scope

Active primitive work targets **KEEP** routes (`docs/CONTROL_PLANE_UI_SCOPE.md`): customers, campaigns, team, settings, ops, audit, integrations.

| Do on KEEP touch | Defer (FREEZE) |
| :--- | :--- |
| Replace raw controls with `Button` / `Input` / shell roles | Mass-unify 40+ report directories |
| Use `FilterApplyButton` in filter rows | New automation/RTB-specific button wrappers |
| Align field height via default primitives | Cosmetic variant sprawl in dashboards |

## Lie modes (never)

| Lie | Reality | Fix |
| :--- | :--- | :--- |
| "Same button" with different hover in two domains | Copy-pasted Tailwind on `className` | One `variant` in `admin_chrome.ts` |
| `PrimaryActionButton` and `Button variant="brand"` mixed for same intent | Visual drift across KEEP pages | Pick role export for that intent |
| `SaveFooButton` component | Action baked into UI layer | `onClick` + `PrimaryActionButton` |
| `h-8` on one control in a filter row | **VL-11** height drift | Default `Button` / `Input` only |
| Domain imports `admin_chrome` | Bypasses primitive boundary | Extend `components/ui` |

## Agent checklist

| Step | Action |
| :--- | :--- |
| 1 | New control look -> `buttonVariantClass` or `adminChrome.control`, not domain `className` |
| 2 | New repeated intent -> `shell/action_buttons.tsx` or `FilterField`, not domain copy |
| 3 | Mutation -> workspace hook; UI gets `loading`/`disabled` only |
| 4 | Link as button -> `Button asChild` + `Link` |
| 5 | KEEP page touch -> prefer shell roles over raw `variant=` when intent is standard |
| 6 | `rg "from '@/lib/admin_chrome'" web/src/domains` must stay empty on PR |

## Verification

```bash
cd web && npm run typecheck
rg "from '@/lib/admin_chrome'" web/src/domains
rg '<button |<input ' web/src/domains --glob '*.tsx'
bash scripts/ci/admin/ui_slop.sh
```

Primitives catalog and Export Hub (on touch):

```bash
rg "from '@/lib/admin_chrome'" web/src/domains
rg "SearchableFilterSelect|DateRangePicker|DropdownMenu|RadioGroup" web/src/shell web/src/domains --glob '*.tsx'
rg "buildReportJobsHref|buildExportHubHref|ExportOnlyReportStub" web/src
rg "DirectoryTable" web/src/pages/customer_report_page.tsx web/src/pages/report_runner_page.tsx
```

## Related rules

`frontend-modular.mdc`, `frontend-slop.mdc`, `ui.mdc`, `react.mdc`, `anti-slop.mdc`.
