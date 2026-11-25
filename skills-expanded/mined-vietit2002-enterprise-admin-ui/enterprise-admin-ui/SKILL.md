---
name: enterprise-admin-ui
description: Use when building, redesigning or reviewing screens of a management system or internal business app — admin panel, back-office, ERP, CRM, HRM, accounting, inventory, B2B SaaS screens behind a login — including data tables, list and detail pages, create/edit forms, filters, bulk actions, approval workflows, roles and permissions, dashboards, settings or CSV import. Also use when such a screen looks generic or AI-generated. Not for landing pages, marketing sites or portfolios.
license: MIT
---

# Enterprise admin UI

People use management software all day to find records, change them safely and see what needs attention. Build every screen for that job: a familiar layout, dense but readable data, every state designed, and saving that never loses work.

## Scope and precedence

- These rules apply to screens behind a login in business apps. Marketing pages are out of scope.
- If the project already has a design system or a customised component library (shadcn theme, Ant Design, MUI, an internal kit), keep its components and tokens and apply the layout, state and behaviour rules below.
- If the project has no design system, use `assets/tokens.css` (values under Foundations).
- On app screens these rules take precedence over aesthetic skills for density, colour and decoration.

## Workflow

1. **Read `DESIGN.md`** at the project root. If the project has no DESIGN.md and more than one screen, create it from `assets/DESIGN.template.md`, filling product, roles, locale and status vocabulary from the user or the code. A single standalone file needs no DESIGN.md.
2. **Model the work:** the entity (orders, invoices, employees…), the roles using the screen, the 1–3 tasks they come to do, and how many records they see. Before adding an action that changes the workflow (Save draft, server-side export, approval, background job), check that the product supports it (a status, an endpoint, a permission). If it does not, leave the action out and say what is missing; never invent roles, calculations or status transitions.
3. **Pick the page type** below and build its anatomy in order.
4. **Apply** States, Saving, Tables and Foundations.
5. **Verify** with the audit and the checklist at the end.

## Every screen ships with

These are the parts most often left out. Build them even for a quick draft:
- **States:** every list and section that shows data has an empty state with its next action, a skeleton while loading, and an inline error with Retry, reachable through `?state=` (States).
- **One primary action** in the header, for the main task: "Renew contract" on a contract, "Create order" on orders.
- **Confirmation** for delete, terminate and cancel. The dialog names the record and the consequence, and focus starts on Cancel.
- **Single-line rows:** name and code go in separate columns, never stacked in one cell.
- **Dates that matter** show the absolute date and the time left in words ("Expires 28/02/2027 · in 56 days"). Overdue and due-soon items come first.
- **Forms:** labels above fields, an error summary that moves focus to the first invalid field, a sticky Save/Cancel bar and an unsaved-changes warning. Uploads state the accepted types and size limit.
- **Announcements:** success toasts name the record, and status and error messages use `role="status"` or `role="alert"`.

## Page recipes

### List (index of records)
1. Page header: breadcrumb when nested · plural title ("Orders") · one primary action ("Create order") · Import/Export as secondary buttons or in an overflow menu.
2. Saved views or status tabs with counts ("All 96 · Pending 3 · Shipping 6").
3. Filter bar: search + the 2–3 most-used filters, the rest in a "More filters" panel. Applied filters appear as removable chips followed by "Clear all".
4. The table, starting in the first viewport. Summary figures go into tab counts or one text line above the table ("96 orders · 596.722.000 ₫") — the page has no row of KPI cards.
5. Bulk selection: header checkbox (checked / indeterminate / empty). Selecting rows shows a bar with "N selected" and the bulk actions; when results span pages the bar offers "Select all 1.284 matching".
6. Pagination with page size and total.
7. States: first use ("No orders yet" + Create order), no results ("No orders match these filters" + Clear filters), loading skeleton rows, error with Retry.

### Record detail
1. Breadcrumb ending in what people call the record: its number when records are known by number (contracts, orders, invoices: "Contracts / HĐ-2026-0187"), otherwise its name ("Customers / Công ty Minh Phát").
2. Record header: name and ID, status badge with text, at most four key fields, one primary action; every other action sits in an overflow menu (⋯).
3. Body in tabs or titled sections (Overview, Contacts, Orders, Activity).
4. Related lists follow the Tables rules. Every section without data shows an empty state with its next step ("No contacts yet · Add contact").
5. Activity: who did what, with absolute timestamps ("04/11/2026 15:58"); relative time appears only together with the absolute value.
6. Avatars represent people only. Companies, orders and products show a logo or no image.
7. Contact values are links: email `mailto:`, phone `tel:`, website opens in a new tab; the primary contact carries a "Primary" badge.
8. Changes to a record that need sign-off (amendments, revisions, price changes) are listed with number, effective date, a one-line summary, status and who approved them ("Approved by Lê Thu Hà · 12/10/2026"), or "Pending approval".

### Create / edit form
1. One column in titled sections: one field per row. The only exception is two short fields that read as one value (City · Postal code, First name · Last name). Never put three fields in a row or lay unrelated fields out on a grid. Visible labels above fields (`<label class="block">`: an inline label sits beside a narrow field), `*` on required fields, field widths sized to their content, and the input type that matches the value (`email`, `tel`, `date`).
2. Line items (invoice, order): a table with add/remove row, numbers right-aligned with tabular figures, subtotal, tax and total computed below and right-aligned.
3. Every full-page form keeps Save and Cancel in a sticky bottom bar (`sticky bottom-0 border-t bg-card`, no shadow), Cancel then Save at the right; saving follows the Saving section. The bar only sticks if its scrolling ancestor is the one that scrolls: no `overflow-y-auto` on a `min-h-screen` shell (audit `sticky-inert`).
4. "Save draft" is optional: offer it, between Cancel and Save, only when the product stores drafts (a Draft status and an API that saves one) or the user asks for it. A draft keeps the record in Draft status, skips the required-field checks until the final submit, and shows "Draft saved 15:58".

### Dashboard
1. Header: title + date-range control + "Updated 16:30". The header has no greeting and no hero.
2. 4–6 KPI tiles: label, value, signed change with its comparison period ("+12% vs yesterday"). Tiles carry no decorative icons.
3. Charts: bars to compare categories, lines for trends over time, axes labelled with units. Use no pie, donut or gauge.
4. "Needs attention": each item shows a count and links to the list with that filter applied ("7 late shipments" → `/shipments?status=late`).
5. Each widget has its own loading, empty and error state.

### Settings
1. Left navigation that groups the sections (General, Localization, Notifications, Users & roles, Danger zone).
2. Each section is a form with its own Save, or a set of toggles that apply instantly and show "Saved" next to them — one model per section.
3. Localization shows a live preview ("04/11/2026 · 1.250.000 ₫").
4. Danger zone last and visually separated; its destructive actions require typing the name.

### Wizard and import
1. A stepper with named steps; completed steps stay clickable.
2. Import: download template → upload → map columns (auto-matched, required fields marked) → preview with per-row errors, an error count and "Download failed rows" → run with progress that can continue in the background → summary of created / updated / failed with a link to the failed rows.
3. The flow lives on a page or a full-width panel.

### Roles, permissions and approvals
- **Who can act:**
  - The current approver sees Approve (primary) and Reject, which requires a reason.
  - Everyone else sees why they cannot act: "Waiting for Trần Minh Quân (Finance manager)".
- **Attribution:**
  - Records, roles and settings show "Last changed by … on …" and link to their history.
  - The history lists field changes (old → new).
- **Destructive actions** name the object and the impact: "Delete role Sales staff? 12 users will lose these permissions."
- **Permission matrix:**
  - Use a real table with row and column headers.
  - Label every checkbox "<module> – <action>" and give it a 24×24px hit area (its label or cell).
  - Row and column toggles use an indeterminate state.
  - Locked system roles say why they are locked.
  - Save is explicit, with an "Unsaved changes" indicator.
- **Attachments** show name, type and size, with Preview and Download.

### Report and printable document (`references/reports-print.md`)
1. **Report:**
   - the title states the measure and period ("Revenue · October 2026");
   - a basis line gives currency, tax basis and "Updated …";
   - period presets come first in the filters;
   - every comparison names its base ("+12.4% vs Sep 2026") and a missing base shows "—";
   - a totals row equals the sum of what is shown.
2. **Document** (invoice, payslip, quotation):
   - an A4 sheet on screen, with status and actions in the page header;
   - a print stylesheet that hides the shell, repeats the table header and never splits rows;
   - legible in black and white.

### Calendar, board and tree
- **Calendar** (`references/calendars.md`):
  - weeks start on the locale's first day;
  - today is marked with text;
  - entries show person and type in text, with pending as dashed plus the word "Pending";
  - multi-day entries are one bar per week row;
  - daily counts ("3 of 8 off");
  - a keyboard grid and a list view.
- **Board** (`references/boards.md`):
  - a bounded height, so columns scroll with sticky headers;
  - counts and limits ("5 / 6");
  - every card movable without dragging, with an announcement and Undo;
  - details in a side panel;
  - a Board · List switch.
- **Tree and split view** (`references/trees.md`):
  - tree or treegrid roles, arrows, Home/End;
  - a parent equals the sum of its children;
  - the expanded state persists and the selection lives in the URL;
  - the detail panel shows the path.

## States

Design every state of every data region:

| State | Show |
|---|---|
| First use | One sentence on what belongs here + the primary action |
| No results | "No X match …" + Clear filters (different from first use) |
| Loading | Skeleton rows or blocks in the final layout; a spinner only inside a button or a small card |
| Error | What failed + Retry, keeping data that is still valid |
| Long job (>10 s) | Progress with counts ("Importing 340 of 1.200"), continues in the background, ends with a summary |
| Partial failure | "48 updated, 2 failed" + the failed items |

**Mock data:** when the page uses mock data, build every state in code and reach each one through the URL. In Next.js, read `?state=` in a client component under `<Suspense>` (`react-shadcn.md`); with `cacheComponents` on in `next.config`, a page that awaits `searchParams` needs `<Suspense>` above it (`loading.tsx` counts) or `next build` fails. Keep a server page that already builds.
- no parameter: a skeleton on first load that resolves to data within about 500 ms; a filter that matches nothing shows the no-results state;
- `?state=empty`: the empty state with its next action;
- `?state=error`: the error state with Retry;
- `?state=loading`: the skeleton, held.

## Saving

- **Save button:** it stays enabled until the user submits. During the request it is disabled and shows a spinner.
- **Validation:**
  - Validate a field when it loses focus, and every field on submit.
  - With 3 or more errors, show a summary at the top that links to each field, and move focus to the first invalid field.
- **Actions:** every full-page form and editable matrix keeps Save and Cancel in a sticky bottom bar with a top border and no shadow.
- **Unsaved changes:**
  - Track them, show "Unsaved changes" beside the actions, and confirm before leaving the page.
  - Use `beforeunload` plus in-app navigation.
- **Failure:** keep the user's input when saving fails, and show each server error next to its field.
- **Success:** a short toast naming the record ("Invoice INV-1043 saved"). Errors stay inline until fixed.

## Tables

- **Row height:** every row is one line, 40px (32px compact): `h-10` or `py-2.5` for text cells, `py-1` for cells that hold a 32px input or button. Secondary data (email, phone, SKU, description, item count) gets its own column or lives on the detail page.
- **Numbers:**
  - Numbers, amounts and quantities are right-aligned with tabular figures (`tabular-nums`). Their column header is right-aligned too.
  - A sortable numeric header: `<th class="px-3 text-right" aria-sort="…"><button class="inline-flex flex-row-reverse items-center gap-1 text-right">Total (VND) <svg …/></button></th>` — the cell holds the padding, the button has none and keeps `text-right` (buttons centre their text), so the label ends at the same edge as the numbers even when it wraps.
  - Currency is formatted with `Intl.NumberFormat` for the project locale.
  - This applies to every table, including tables inside detail pages and forms.
- **Text and headers:** text is left-aligned. Headers are in sentence case with normal letter spacing.
- **Row actions:** one or two visible, the rest in an overflow menu named after the record ("Actions for order DH-1043").
- **Default order:**
  - When the rows carry a due or expiry date (certificates, contracts, invoices, inspections, tasks), the table opens with the rows that need attention first: expired or overdue, then due soon, then the rest, each group by date.
  - The status badge says which group a row is in ("Expired", "Expires in 12 days").
  - Other tables open newest first.

## Foundations

Use these values when the project has no design system; `assets/tokens.css` implements them. In a single HTML file with the Tailwind CDN, use the Tailwind palette classes named here (slate-600, blue-700 …); such a page needs neither `references/tokens.md` nor `assets/tokens.css`. Token class names such as `bg-sidebar` work only with the config in `tokens.md`. Add `[hidden] { display: none !important; }` to the page's `<style>` so the `hidden` attribute always wins over `flex` and `grid` classes.

| Area | Value |
|---|---|
| Font | System UI stack; weights 400/500/600. 14px (`text-sm`): body, table cells, field labels (`text-sm font-medium`), help text and error messages. 12px (`text-xs`): captions, badges, nav group labels, timestamps under a title. 20–24px: page title |
| Text colour | Body `#0f172a`. Secondary text `#475569` (slate-600) or darker; slate-500 only on white or slate-50; slate-400 and lighter never carry text. Re-check 4.5:1 on tinted and dark surfaces. White text sits only on 700-shade fills (blue-600 and red-600 also pass), not on -500 fills or on green, emerald, amber, teal or sky-600. Badge text uses the 700–800 shade on the 50 background, or the `-subtle` token pair. |
| Case | Sentence case for titles, labels, table headers, tabs and buttons |
| Spacing | 4px base: 4, 8, 12, 16, 24, 32 |
| Controls | 32px high (40px for touch) |
| Radius | 4px controls, 6px cards, 8px dialogs; fully rounded only for badges and chips |
| Surfaces | Page and cards white or slate-50; cards have a 1px border and no shadow; shadows belong to menus, popovers, dialogs and toasts |
| Shell | Light neutral sidebar with a subtle active background; the single accent colour marks primary buttons, links, focus and selection: DESIGN.md's accent, or `#1d4ed8` (blue-700) when DESIGN.md has none |
| Status | One vocabulary for the whole app, five tones, always with text: neutral (Draft, Archived), info (Pending, In progress), success (Completed, Paid), warning (Due soon, Needs attention), danger (Failed, Rejected, Overdue). Map every entity status to a tone in DESIGN.md. |
| Icons | One icon set (lucide with shadcn), 16px |

## Template tells to remove

| Seen in AI-built admin screens | Build instead |
|---|---|
| ALL-CAPS tracked labels and table headers (`uppercase tracking-wide`) | Sentence case, normal tracking, sizes from Font above |
| Dark navy sidebar with an indigo accent | Light neutral sidebar; accent only on primary actions and selection |
| A different colour for every status | The five-tone status vocabulary |

## Review mode

When the user asks to review or audit existing screens, report findings instead of rewriting code:

1. Run the audit (see Verify) on each screen and map every violation to its source line.
2. Walk the page recipe for the screen type, the manual checklist and `references/anti-patterns.md`; each miss is a finding.
3. Write one finding per line: `path/to/file.tsx:42 — <rule> — <fix>`, for example `app/orders/page.tsx:88 — numeric-align — add text-right tabular-nums to the Total header and cells`.
4. Group the findings by level, most severe first: `data` (lost or wrong data: saving, destructive actions) → `states` (missing states) → `a11y` (contrast, names, targets) → `layout` (density and alignment) → `tells` (template tells).
5. End with the count per level, e.g. `data 1 · states 2 · a11y 3 · layout 4 · tells 2`. Change code when the user asks for fixes.

## Verify

- **Audit:** run `node <this skill's folder>/scripts/audit-cli.mjs <url or file.html> --type list` (or `detail`, `form`, `dashboard`, `settings`, `wizard`, `report`, `document`, `calendar`, `board`, `tree`). It opens the page in a headless Chrome or Edge at 1440×900 and prints the score; exit code 1 means an ✗ error, a failed state or check, or a required check not verified. With mock data, add `--states`: it also opens `?state=empty`, `?state=error` and `?state=loading` and checks each one. Add `--checks` to use the page as a person would: a search that matches nothing, Export, Print and Delete are each checked, and a check the page has no control for prints `?` (not verified), never a pass. Pass check names (comma-separated: `search,export,print,confirm,live-region`) to `--require` for what the task asks the screen to do (a missing control then fails) and to `--not-applicable` for what it rules out. It clicks Delete only with `--disposable`. Add `--disposable` only for mock data or a test copy you can reset, never for a page connected to real data: a localhost frontend can still call a production API. Without it, `? confirm` means Delete was not checked, not that it passed.
  - In a browser console, paste `scripts/audit.js`, then run `enterpriseAdminAudit({ pageType: 'list' })`.
  - With Playwright, use `page.addScriptTag({ path })` then `page.evaluate(...)`.
  - Fix every ✗ error and review every ! warning.
- **Manual checklist:**
  - [ ] Every list and related list has first-use, no-results, loading and error states
  - [ ] Form fields sit one per row, except a pair that reads as one value
  - [ ] Save stays enabled until submit; the error summary and unsaved-changes warning exist
  - [ ] Filters show as chips with Clear all; the bulk bar offers "Select all N matching"
  - [ ] Destructive actions name the object and the impact
  - [ ] Records show who changed them and when
  - [ ] Unavailable actions say why
  - [ ] Dashboard deltas state their period; attention items link to filtered lists

## References

| Read | When |
|---|---|
| `references/tables.md` | any table: density, alignment, selection, pagination, inline edit |
| `references/filters-search.md` | filter bars, chips, saved views, search, URL state |
| `references/forms.md` | forms, line items, validation, save models |
| `references/feedback-states.md` | empty/loading/error states, toasts vs banners, confirmations, long jobs |
| `references/permissions-audit.md` | roles, approvals, audit history, status vocabulary |
| `references/dashboards-charts.md` | dashboards, KPI tiles, charts |
| `references/navigation-layout.md` | app shell, sidebar, page header, breadcrumbs, settings navigation |
| `references/tokens.md` | applying tokens in shadcn, Tailwind v3/v4 or plain CSS; changing the accent |
| `references/data-formatting.md` | numbers, money, dates, time zones, empty values, vi-VN formats |
| `references/bulk-import-export.md` | select-all-matching, partial failures, CSV import, export |
| `references/accessibility.md` | WCAG 2.2 AA checklist: keyboard, focus, names, live regions, targets |
| `references/anti-patterns.md` | template tells with the fix for each; reviewing AI-built screens |
| `references/react-shadcn.md` | React with shadcn/ui: TanStack Table, react-hook-form + zod, URL state, Sidebar |
| `references/reports-print.md` | reports (periods, comparisons, totals, export) and printable documents (invoices, payslips) |
| `references/calendars.md` | calendars and schedules: leave, shifts, bookings; week start, multi-day bars, coverage |
| `references/boards.md` | Kanban boards: columns, cards, moving without drag, transitions, side-panel details |
| `references/trees.md` | trees and split views: chart of accounts, org charts, categories; keyboard and persistence |
| `assets/templates/` | optional: working single-file list, detail and form pages to start from; each passes `audit-cli.mjs --checks` |
