# Enterprise DMS + SFA Monorepo — Cursor AI Rules

## Identity
You are working on an Enterprise Distribution Management System (DMS) and Sales Force Automation (SFA) monorepo. This is a production system deployed at `https://dms.jyotirmoyb.com`.

## Tech Stack
- **Monorepo**: pnpm 8.15 workspaces + Turborepo
- **Frontend**: React 18, Vite 5, react-router-dom 6 (HashRouter), TypeScript 5 strict
- **Backend**: 19 Node.js Express microservices behind api-gateway
- **Database**: PostgreSQL with Row-Level Security per tenant
- **State**: React Context (`DataContext.tsx`) with reactive mutations
- **Design**: Centralized tokens in `theme/tokens.ts` — NO Tailwind
- **Build**: `tsc --noEmit && vite build`

## Efficiency Rules
- NEVER scan the entire repository. Focus ONLY on target files + their immediate imports.
- Skip: `node_modules/`, `dist/`, `.turbo/`, `pnpm-lock.yaml`, `__pycache__/`
- When navigating, start from the specific workspace (e.g. `apps/web-admin/src/`).
- If context is missing, ASK for specific file paths.

## Output Format
Always use the file path convention so changes auto-apply:

```typescript filename="apps/web-admin/src/path/to/file.tsx"
// code here
```

For edits, use precise search-and-replace over full rewrites.

## Architecture Quick Reference

### Primary Frontend (apps/web-admin/src/)
```
App.tsx              → Root: HashRouter + Frame Switcher bar
main.tsx             → Entry: ErrorBoundary → DataProvider → App
types/index.ts       → ALL TypeScript interfaces
theme/tokens.ts      → Design system (colors, typography, presets)
data/seed.ts         → Nav items + dropdown constants
context/DataContext.tsx → Global reactive store (useData hook)
services/dbService.ts  → API client (4s timeout, AbortController)
frames/              → 5 Frame containers (Control, DMS, SFA, Governance, Analytics)
pages/               → Domain pages (admin, inventory, sales, finance, analytics)
components/          → Reusable UI (Sidebar, Modal, FormField, StatusBadge, forms/)
```

### Routing: `/#/frame/page`
- `/control/dashboard`, `/control/users`, `/control/tenants`
- `/dms/sku-catalog`, `/dms/stock-ledger`, `/dms/outlet-registry`
- `/sfa/sales-orders`, `/sfa/beat-routes`, `/sfa/field-visits`
- `/governance/invoices`, `/governance/trade-claims`, `/governance/audit-ledger`
- `/analytics/ai-forecast`, `/analytics/reports`

### Roles: admin | agent | distributor | auditor

### Backend (services/)
19 microservices: api-gateway, identity-service, dms-core-service, sfa-service, finance-service, claims-service, pricing-service, audit-service, sync-service, config-service, notification-service, file-service, report-service, integration-service, forecasting-service, recommendation-service, ai-service, ai-gateway-service, schemes-service.

### Shared Packages (packages/)
14 packages: pkg-database, pkg-logger, pkg-validation, pkg-rbac, pkg-crypto, pkg-events, pkg-http, pkg-config-client, pkg-ui-shared, pkg-analytics, pkg-testing, pkg-integrations, pkg-mobile-sync, pkg-config.

## Mandatory Code Rules
1. ALL page state via `useData()` from DataContext — never local fetch + useState.
2. ALL styling via `tokens` from `theme/tokens.ts` — no raw hex colors.
3. ALL types from `types/index.ts` — no `any`.
4. ALL status rendering via `<StatusBadge>`.
5. ALL create/edit flows via modular form modals in `components/forms/`.
6. Dropdown-first forms: use `<select>` with seed constants, not freetext inputs.
7. Auto-increment IDs: `PREFIX-${Date.now().toString(16).slice(-6)}`.
8. Cross-module side effects centralized in DataContext mutations.
9. No hardcoded domain data in components.
10. No silent catch blocks.

## Adding a New Entity Checklist
1. `types/index.ts` — add interface
2. `data/seed.ts` — add constants
3. `context/DataContext.tsx` — add state + mutations
4. `components/forms/` — create modal
5. `pages/<domain>/` — create page component
6. `frames/<Frame>.tsx` — register page
7. `App.tsx` — add route path mapping
8. `data/seed.ts` — add NavItem

## Verify Before Commit
```bash
cd apps/web-admin && npx tsc --noEmit && npx vite build
```
