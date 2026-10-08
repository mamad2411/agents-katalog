# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Dev server (http://localhost:4400)
npm start

# Dev build (use this to check for errors — faster feedback than prod)
npx ng build --configuration=development

# Production build
npm run build

# Watch mode
npm run watch

# Tests
npm test
```

The backend API runs separately at `http://localhost:5200/api` (configured in `src/environments/environment.ts`).

## Architecture Overview

**HOMSys** (Head Office Monitoring System) is an Angular 19 standalone-component SPA for Ram Foods. There are no NgModules — every component is standalone with its own `imports` array.

### Layout Shell

`AppLayoutComponent` is the authenticated shell wrapping every page. It composes:
- `TopbarComponent` — brand bar, shows the active tab label
- `AppTabBarComponent` — browser-style tab strip (see Tab System below)
- `PageToolbarComponent` — action toolbar (Save, Edit, Delete, Find, Search, etc.)
- `ModulebarComponent` / `SidebarComponent` — module/page navigation
- `<router-outlet>` — page content

The layout is only mounted for authenticated routes. The login page is a separate top-level route.

### Tab System (`TabBarService`)

Tabs are key-based, not route-based. A tab has `{ key, label, route, icon, state? }`.

- **Default tabs** (e.g. `/users`, `/users/list`) — created automatically by `TabBarService`'s `NavigationEnd` subscription. The tab key equals the URL.
- **Edit tabs** (e.g. `/users#42`) — created by the page component calling `tabBar.openTab()`. The service skips auto-creation when `userId`, `roleId`, `companyId`, or `departmentId` is present in `history.state`.
- `switchToDefaultTab(route)` — used by Cancel: closes the active edit tab and activates/creates the "New" tab.
- `updateTabState(key, state)` — saves arbitrary state onto a tab (used for draft form preservation).
- `registerDirtyChecker(key, fn)` / `isTabDirty(key)` — dirty-check callbacks called by `AppTabBarComponent` before closing a tab (shows a PrimeNG confirm dialog if dirty).

`onSameUrlNavigation: 'reload'` is set in `app.config.ts` so that navigating to the same URL fires `NavigationEnd` — this is how same-route tab switching works.

### Toolbar System (`GlobalToolbarService`)

Each page component calls `globalToolbar.set(ToolbarConfig)` in `ngOnInit` (and again whenever state changes like entering edit mode) and `globalToolbar.clear()` in `ngOnDestroy`.

`PageToolbarComponent` reads this signal-based config and renders buttons reactively. Supported actions: `save`, `add`, `edit`, `delete`, `list`, `find`, `search`, `print`, `export`, `import`.

- **`find`** — icon-only button for form pages; triggers a lookup by the name/username field (requires `*` wildcard in the input, e.g. `allen*`).
- **`search`** — live-filter input box for list pages only.

### Feature Page Pattern

Every feature has a **form page** (`/entity`) and a **list page** (`/entity/list`).

**Form pages** (`user-page`, `role-page`, `company-page`, `department-page`) follow this pattern:
- `currentTabKey` tracks active tab (`'/users'` for new, `'/users#42'` for edit)
- `private navSub?: Subscription` subscribes to `NavigationEnd` for same-route tab switching
- `handleNavState()` reads `history.state` (NOT `router.getCurrentNavigation()` — that returns null in `ngOnInit`) to decide new vs edit mode
- `loadEntity()` calls `tabBar.openTab({ key: '/entity#id', label: 'Edit — name', state: { entityId } })`
- `clearSelection()` (Cancel) calls `tabBar.switchToDefaultTab('/entity')` if was in edit mode
- `resetFormOnly()` resets without touching tabs — called internally when navigating back to "new" state
- **Draft preservation**: `ngOnDestroy` saves `{ draftForm: form.value }` to the tab state when the new-entry form has data; `handleNavState` restores it on return
- **Dirty checking**: `registerDirtyChecker(tabKey, () => ...)` wired in `ngOnInit`, `loadEntity`, `resetFormOnly`, and `ngOnDestroy`

**List pages** use signal-based filtering (no PrimeNG `filterGlobal`):
- `allEntities = signal([])`, `searchTerm = signal(initialSearch)`, `filteredEntities = computed(...)`
- `initialSearch` read from `history.state.searchTerm` at construction time (supports pre-filtered navigation from Find)
- Table binds `[value]="filteredEntities()"`
- Double-click or Edit button navigates with `router.navigate(['/entity'], { state: { entityId: id } })`

**Find lookup logic** (form pages):
- Input must contain `*` (e.g. `allen*`) — no `*` means create intent, Find does nothing
- Strips `*`, does exact-match case-insensitive lookup via `getAll()`
- Exact match → `loadEntity()` (opens edit tab)
- No match → `router.navigate(['/entity/list'], { state: { searchTerm: term } })`

### Auth & Security

- `AuthService` stores access token in memory, refresh token and user info in `localStorage`
- `authInterceptor` attaches `Bearer` token; `errorInterceptor` handles 401 by triggering token refresh
- `authGuard` protects all routes under the layout shell
- `routeRoleGuard` checks `route.data.permission` against `AuthService.hasPermission(key)` — permissions come from the backend JWT claims

### Adding a New Feature Page

When adding a new route/module, wire up all four of:
1. `ROUTE_META` entry in `tab-bar.service.ts`
2. Module sidebar entry
3. Route in `app.routes.ts`
4. `routeRoleGuard` `data: { permission: '...' }`

Follow the form-page and list-page patterns above (signal filtering, `handleNavState`, dirty checker registration, draft preservation).

### Export & Import

**Export** (`ExportService`): call `exportService.exportToPdf(columns, rows, title)`, `.exportToExcel(columns, rows, filename)`, or `.exportToCsv(columns, rows, filename)`. List pages wire this to the `export` toolbar action.

**Import** (`ImportDialogComponent`): reusable dialog in `src/app/shared/import-dialog/`. List pages include it with an `#importDialog` template reference and call `importDialog.open()` from the `import` toolbar action. It emits parsed rows on success for the page to process.

### Theme & Styling

Custom PrimeNG theme in `src/app/core/theme/homsys-theme.ts` with Ram Foods burgundy branding (`#800000`). Component styles use inline SCSS. Global styles are in `src/styles.scss`.
