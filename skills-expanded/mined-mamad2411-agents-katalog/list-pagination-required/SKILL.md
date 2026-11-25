---
name: list-pagination-required
description: Use whenever building or reviewing any list/table UI (a `@for`/`*ngFor`/`.map()` rendering rows from an array) in any app — enforces adding pagination instead of rendering the full collection unpaginated. Triggers on "lista", "tabla", "listado", building a new page/view with a list of records, or reviewing one that has none.
allowed-tools: Read, Edit, Grep, Glob
---

# List Pagination Required

Any list of records that can grow unbounded (transactions, bills, backups, reconciliation lines, catalog rows...) ships with pagination from the start. Retrofitting it later means the list already shipped slow and someone already complained.

## Rule

Before considering a list/table view done:

1. **Check the project already has a pagination component before building one.**
   - Angular apps (e.g. dar-money-mind): `apps/web/src/app/shared/components/pagination/pagination.component.ts` — `ZardPaginationComponent`, selector `app-pagination`. API: `page` (input, required), `pageCount` (input, required), `testId` (input, optional), `pageChange` (output `number`). Already used in `credit-periods`, `debts`, `incomes`, `accounts-receivable`, `gmail-review`, `transactions` — copy that usage pattern, don't reinvent it.
   - Lit/web-component apps (e.g. backup-dashboard, anything consuming `@arayaroma/photon`): `ph-pagination` from `photon/src/components/pagination/pagination.ts`. API: `page` (number prop), `totalPages` (number prop), `summary` (string prop, optional), fires `ph-page-change` CustomEvent with `detail.page`. Import via `@arayaroma/photon/elements` (side-effect registers the element) and use `<ph-pagination .page=${...} .totalPages=${...} @ph-page-change=${...}>`.
   - Any other stack (React, etc.): no existing component yet — port the same shape (`page`/`totalPages` or `pageCount`, one "page changed" callback/event) rather than inventing a different API. Note it here once built so the next session finds it.

2. **Server-side pagination beats client-side slicing** when the backing list can grow past a couple hundred rows (anything backed by a DB table with no natural cap — transactions, bills, backups). Client-side slicing (paginate an array already fully loaded) is acceptable only for lists that are inherently small and bounded (e.g. a period's reconciliation lines, a card's categories) — don't add server pagination machinery there, just slice.

3. **Never ship a bare unbounded list.** If a list view has no pagination and no hard upper bound on row count, that's a defect to flag — not a style preference. Add pagination before calling the view done, using whichever component from step 1 matches the stack.

4. **Match the existing page-size convention** in that codebase (check a sibling paginated page for its default `pageSize`/`limit`) rather than picking an arbitrary number per view. dar-money-mind's convention (see `debts.page.ts`): `readonly pageSize = 20;`, `pageCount = computed(() => Math.max(1, Math.ceil(items().length / pageSize)))`, `paged = computed(() => items().slice((page()-1)*pageSize, page()*pageSize))`.

This applies to every new list you build going forward — check this skill before writing the template for a list/table, not after the user points out it's missing.
