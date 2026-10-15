---
name: taruvi-refine-providers
description: >
  Use this skill when the user is setting up, wiring, debugging, or migrating
  Taruvi Refine providers in a frontend app — including data providers, auth
  provider, access control, or SDK client configuration. Also use when the user
  encounters 401/403 errors, token refresh issues, permission check problems,
  or needs to call a Taruvi function or analytics query from the frontend,
  even if they don't mention "providers" directly.
metadata:
  author: taruvi-ai
  version: "1.0.0"
---

## Overview

Reference module for wiring and using Taruvi's Refine data providers in the frontend — covering client setup, all provider types, hook usage, auth flow, and access control batching.

**Compliance rule:** This skill and its references are the source of truth for all provider usage. Do not substitute with simpler patterns, copy outdated project code, or skip prescribed steps. If a requirement cannot be met, stop and ask the user.

## Provider Map

Use this as the canonical provider inventory for Taruvi + Refine apps:

| Provider | Refine registration key | Primary purpose | Typical hooks |
|---|---|---|---|
| `dataProvider(client)` | `default` | Datatable/database CRUD + filters/sort/pagination/aggregation | `useList`, `useOne`, `useCreate`, `useUpdate`, `useDelete`, `useUpdateMany`, `useDeleteMany` |
| `storageDataProvider(client)` | `storage` | File/object upload, listing, download, delete | `useCreate`, `useList`, `useOne`, `useDelete`, `useDeleteMany` |
| `appDataProvider(client)` | `app` | App-level operations: function execute, analytics execute, roles, settings, secrets | `useCustom` (functions/analytics), `useList` (`roles`/`secrets`), `useOne` (`settings`/`secrets`) |
| `userDataProvider(client)` | `user` | User CRUD and user-related app data | `useList`, `useOne`, `useCreate`, `useUpdate`, `useDelete` |
| `authProvider(client)` | `authProvider` prop | Login/logout/session/identity/permissions | Refine auth lifecycle (`check`, `login`, `logout`, `getIdentity`) |
| `accessControlProvider(client)` | `accessControlProvider` prop | Batched Cerbos permission checks for `useCan`/`CanAccess` | `useCan`, `CanAccess` |

Deprecated (do not use in new code):
- `functionsDataProvider` (use `appDataProvider` + `useCustom` + `meta.kind: "function"`)
- `analyticsDataProvider` (use `appDataProvider` + `useCustom` + `meta.kind: "analytics"`)

## Hook Support Matrix

Use this matrix for the current non-deprecated provider surface:

| Hook / DataProvider method | `default` | `storage` | `app` | `user` |
|---|---|---|---|---|
| `useList` / `getList` | ✅ | ✅ | ✅ (`roles`, `secrets`) | ✅ |
| `useOne` / `getOne` | ✅ | ✅ | ✅ (`settings`, `secrets`) | ✅ |
| `useMany` / `getMany` | ✅ | ❌ | ❌ | ❌ |
| `useCreate` / `create` | ✅ | ✅ | ❌ | ✅ |
| `useCreateMany` / `createMany` | ✅ | ✅ | ❌ | ❌ |
| `useUpdate` / `update` | ✅ | ✅ | ❌ | ✅ |
| `useUpdateMany` / `updateMany` | ✅ | ❌ | ❌ | ❌ |
| `useDelete` / `deleteOne` | ✅ | ✅ | ❌ | ✅ |
| `useDeleteMany` / `deleteMany` | ✅ | ✅ | ❌ | ❌ |
| `useCustom` / `custom` | ✅ | ✅ | ✅ (`meta.kind: function/analytics`) | ❌ |

## When to Use This Skill

- Setting up `@taruvi/refine-providers` for the first time in a project
- Wiring `dataProvider`, `storageDataProvider`, `appDataProvider`, `userDataProvider` into `<Refine>`
- Configuring `authProvider` and understanding the login/token redirect flow
- Configuring `accessControlProvider` and using `useCan`
- Using `useCustom` with `meta.kind: "function"` or `meta.kind: "analytics"`
- Migrating from deprecated `functionsDataProvider` / `analyticsDataProvider`
- Debugging auth errors (401/403), token refresh, or access control resolution

**Do not use this skill for:** Python function authoring (use `taruvi-functions` skill), storage REST endpoints (use `taruvi-storage` skill), or raw database query optimization (use `taruvi-database` skill).

## Step-by-Step Instructions

1. Open and read `references/overview.md` — install, quick-start, provider map at a glance.
2. Open and read the specific provider reference(s) for the task:

   **Important:** Identify the current non-deprecated package API before choosing a provider/hook pattern. Never introduce new usage of deprecated APIs. If the only path that appears to work is deprecated, fix the provider/docs first.

   - Database CRUD / filters / aggregation / graph → `references/database-provider.md`
   - File upload / download / storage → `references/storage-provider.md`
   - Functions / analytics / roles / secrets → `references/app-provider.md`
   - User management → `references/user-provider.md`
   - Login / logout / token flow → `references/auth-provider.md`
   - Permissions / `useCan` / `CanAccess` → `references/access-control-provider.md`
   - TypeScript types / utilities / deprecated migration → `references/types-and-utilities.md`
4. Install dependencies:
   ```bash
   npm install @taruvi/refine-providers @taruvi/sdk @refinedev/core
   ```
5. Create the SDK client with `apiKey`, `appSlug`, and `apiUrl`.
6. Wire all relevant providers into `<Refine>`.
7. Use provider-native hooks (`useList`, `useCreate`, `useCustom`, `useCan`) — do not call REST directly from components.
8. For UI feedback, use Refine’s configured `notificationProvider` for success/error messaging.
   - do not add ad hoc/custom toast systems when a Refine notification provider is already wired
9. For access control checks, use only the published non-deprecated SDK/provider contract:
   - pass prefixed ACL resource strings (for example: `datatable:employees`, `function:employee-terminate`, `query:hrms-dashboard-summary`)
   - do not use `params.entityType` for `useCan`/`CanAccess` checks
   - map UI actions to Cerbos actions before access-control checks:
     - `list` -> `read`
     - `show` -> `read`
     - `edit` -> `update`
     - `create` -> `create`
     - `delete` -> `delete`
   - never send raw UI action names (`list`, `show`, `edit`) in `/check/resources` payloads
10. For Taruvi function execution from frontend, enforce this exact contract (hard requirement):
   - `dataProviderName: "app"`
   - `meta.kind: "function"`
   - `config.payload` for input params
   - `url` must be the function slug
   - do not use `values` for function input payloads
   - no new usage of `functionsDataProvider` in frontend app code
11. For backend-backed list pages, keep the list state in the provider query:
   - backend pagination is required by default
   - default list `pageSize` is `10`; recommend exposing `10`, `20`, `50`, and `100` page-size choices in the UI
   - search, filters, and sorters must be passed into provider calls by default
   - when rendering with MUI `DataGrid`, default to Refine `useDataGrid`
   - do not re-implement the primary list filtering logic in component state over fetched backend rows unless the user explicitly asked for client-side behavior
12. For network-backed dropdowns/typeaheads:
   - default to `Autocomplete` (or equivalent typeahead UX)
   - debounce search input before querying
   - pass search text into provider filters
   - fetch options with pagination from the backend (default option `pageSize` `10`)
   - avoid using static `Select` fed by large one-shot option loads

### Verification checklist

After wiring providers, verify:

- [ ] SDK client uses env vars (`import.meta.env.VITE_TARUVI_*`), not hardcoded values
- [ ] All four data providers are wired: `default`, `storage`, `app`, `user`
- [ ] `authProvider` and `accessControlProvider` are both passed to `<Refine>`
- [ ] User-facing success/error messages use Refine `notificationProvider` (no parallel custom toast system)
- [ ] No direct REST/fetch calls from components — all data flows through hooks
- [ ] No new usage of deprecated package APIs
- [ ] The chosen provider/hook path matches the installed package’s current non-deprecated API
- [ ] `useCustom` calls for functions use `dataProviderName: "app"` and `meta.kind: "function"`
- [ ] Function inputs are passed via `config.payload` (not `values`) for `meta.kind: "function"` calls
- [ ] No new `functionsDataProvider` usage in frontend app code
- [ ] Access-control checks use prefixed ACL resource strings from the published contract
- [ ] Runtime network validation: in `check/resources` payload, each `resource.kind` exactly matches the requested `resource` string (no composition, no double-prefix)
- [ ] Runtime network validation: `resource.kind` is never a bare resource name (for example `policies`) and always includes prefix (for example `datatable:policies`)
- [ ] Runtime network validation: action names sent to `/check/resources` are canonical (`read`, `update`, `create`, `delete`, `execute`) and not raw UI labels (`list`, `show`, `edit`)
- [ ] Backend-backed list pages use provider-driven pagination
- [ ] Backend-backed list search/filter/sort state is passed into provider queries, not re-applied in React
- [ ] Backend-backed MUI `DataGrid` list pages use `useDataGrid` by default (or include an explicit exception reason)
- [ ] Network-backed dropdowns/typeaheads use debounced server-side search and paginated option queries

## Examples

**Client and provider setup:**
```tsx
import { Client } from "@taruvi/sdk";
import { useNotificationProvider } from "@refinedev/mui";
import {
  dataProvider,
  storageDataProvider,
  appDataProvider,
  userDataProvider,
  authProvider,
  accessControlProvider,
} from "@taruvi/refine-providers";

const client = new Client({
  apiKey: import.meta.env.VITE_TARUVI_API_KEY,
  appSlug: import.meta.env.VITE_TARUVI_APP_SLUG,
  apiUrl: import.meta.env.VITE_TARUVI_API_URL,
});

<Refine
  dataProvider={{
    default: dataProvider(client),
    storage: storageDataProvider(client),
    app: appDataProvider(client),
    user: userDataProvider(client),
  }}
  notificationProvider={useNotificationProvider}
  authProvider={authProvider(client)}
  accessControlProvider={accessControlProvider(client)}
/>
```

**Backend-driven list with `useDataGrid`:**
```tsx
import { useDataGrid } from "@refinedev/mui";
import { DataGrid } from "@mui/x-data-grid";

const { dataGridProps } = useDataGrid({
  resource: "employees",
  pagination: { pageSize: 10 },
});

return <DataGrid {...dataGridProps} pagination autoHeight />;
```

**Create/Edit with `useForm` (Refine v5):**
```tsx
import { useForm } from "@refinedev/react-hook-form";

const {
  saveButtonProps,
  refineCore: { queryResult },
  register,
  formState: { errors },
} = useForm({
  resource: "employees",
  action: "create", // or "edit"
});
```

**Show page with `useShow` (Refine v5):**
```tsx
import { useShow } from "@refinedev/core";

const { result, query } = useShow({
  resource: "employees",
  id: "emp-123",
});

const record = result;
```

**Advanced `meta` options on `default` provider:**
```tsx
useList({
  resource: "employees",
  meta: {
    tableName: "employees_archive",
    select: ["id", "first_name", "status"],
    populate: ["department_id", "manager_id"],
  },
});
```

**Aggregation + groupBy + having:**
```tsx
useList({
  resource: "employees",
  filters: [{ field: "status", operator: "eq", value: "active" }],
  meta: {
    aggregate: ["count(*)"],
    groupBy: ["department_id"],
    having: [{ field: "count(*)", operator: "gt", value: 5 }],
  },
});
```

**Execute a function via `appDataProvider` (`meta.kind: "function"`):**
```typescript
const { data } = useCustom({
  url: "employee-terminate",
  method: "post",
  dataProviderName: "app",
  config: {
    payload: { employee_id: "emp-1", termination_reason: "Policy violation" },
  },
  meta: { kind: "function" },
});
```

**Execute analytics via `appDataProvider` (`meta.kind: "analytics"`):**
```typescript
const { data } = useCustom({
  url: "hrms-dashboard-summary",
  method: "post",
  dataProviderName: "app",
  payload: {},
  meta: { kind: "analytics" },
});
```

**Check permission with prefixed ACL resources:**
```typescript
const { data: canCreateEmployee } = useCan({
  resource: "datatable:employees",
  action: "create",
});

<CanAccess resource="query:hrms-dashboard-summary" action="execute">
  <DashboardPage />
</CanAccess>;
```

**Use Refine notification provider in actions:**
```typescript
import { useNotification } from "@refinedev/core";

const { open } = useNotification();

open?.({
  type: "success",
  message: "Bulk update completed",
  description: "8 employees updated",
});
```

**Storage upload via `storage` provider (multi-file payload):**
```tsx
useCreate({
  resource: "employee-documents",
  dataProviderName: "storage",
  values: {
    files: selectedFiles,
    paths: selectedFiles.map((f) => `employees/emp-123/${f.name}`),
    metadatas: selectedFiles.map(() => ({ source: "onboarding" })),
  },
});
```

## Filter Operators

Refine operator keys supported by the Taruvi provider mapping:

| Operator | Meaning | Query-style mapping |
|---|---|---|
| `eq` | equals | `field=value` |
| `ne` | not equals | `field__ne=value` |
| `lt` | less than | `field__lt=value` |
| `gt` | greater than | `field__gt=value` |
| `lte` | less than or equal | `field__lte=value` |
| `gte` | greater than or equal | `field__gte=value` |
| `contains` | contains (case-sensitive) | `field__contains=value` |
| `ncontains` | not contains (case-sensitive) | `field__ncontains=value` |
| `containss` | contains (case-insensitive) | `field__icontains=value` |
| `ncontainss` | not contains (case-insensitive) | `field__nicontains=value` |
| `startswith` | starts with (case-sensitive) | `field__startswith=value` |
| `nstartswith` | not starts with (case-sensitive) | `field__nstartswith=value` |
| `startswiths` | starts with (case-insensitive) | `field__istartswith=value` |
| `nstartswiths` | not starts with (case-insensitive) | `field__nistartswith=value` |
| `endswith` | ends with (case-sensitive) | `field__endswith=value` |
| `nendswith` | not ends with (case-sensitive) | `field__nendswith=value` |
| `endswiths` | ends with (case-insensitive) | `field__iendswith=value` |
| `nendswiths` | not ends with (case-insensitive) | `field__niendswith=value` |
| `in` | in list | `field__in=a,b,c` |
| `nin` | not in list | `field__nin=a,b,c` |
| `null` | is null | `field__null=true` |
| `nnull` | is not null | `field__nnull=true` |
| `between` | in range | `field__between=min,max` |
| `nbetween` | not in range | `field__nbetween=min,max` |

## Gotchas

- **Deprecated providers** — `functionsDataProvider` and `analyticsDataProvider` are removed. Migrate to `appDataProvider` + `useCustom` with `meta.kind: "function"` or `meta.kind: "analytics"`. Old imports will compile but throw at runtime.
- **Wrong function payload shape** — for `meta.kind: "function"`, pass inputs via `config.payload`. Using `values` or top-level `payload` causes contract drift and runtime issues.
- **Deprecated package path in new code** — do not add new code on deprecated providers or compatibility helpers just because old examples still exist. Use the installed package’s current canonical API surface.
- **Auth redirect loop** — `authProvider.login()` redirects to `/accounts/login/` and tokens come back in the URL hash. Do not try to intercept mid-redirect or parse the URL yourself — the provider handles it.
- **401 vs 403 confusion** — `onError()` handles both: 401 means session expired (trigger re-login), 403 means authenticated but forbidden (show access denied). Treating 403 as 401 causes infinite re-login loops.
- **`/check/resources` payload drift** — if network logs show `resource.kind: "policies"` instead of `resource.kind: "datatable:policies"`, access-control wiring is incorrect and must be fixed before completion.
- **Access-control resource format mismatch** — `useCan`/`CanAccess` expects prefixed ACL resources (for example `datatable:employees`). Do not pass `params.entityType`.
- **Access-control resource format drift** — always pass prefixed resource strings directly. If `resource.kind` in network payload differs from the requested `resource`, there is a contract mismatch.
- **DataLoader batching** — `accessControlProvider` batches `useCan` calls automatically via DataLoader. Do not debounce or throttle `useCan` manually — it will interfere with the batch delay and cause missed permission checks.
- **SDK/provider contract change not coordinated** — when the SDK/provider ACL contract changes, app code must be updated in the same release cycle and versioned together.
- **Wrong `dataProviderName`** — forgetting `dataProviderName: "app"` on `useCustom` for functions routes the call to the default (database) provider, returning a confusing "resource not found" error. Same applies to `"storage"` and `"user"`.
- **`useCustom` slug source** — for `appDataProvider` custom calls, `url` is treated as the function/query slug. Use a real slug (for example `employee-terminate` or `hrms-dashboard-summary`) and set `meta.kind` accordingly.
- **Client-side filtering over provider results** — if a list uses `useList` but then performs the main search/filter pass in React state, the backend and UI drift out of sync. Push the list state into the provider query by default.
- **Manual `DataGrid` wiring by default** — for backend-backed MUI lists, manually syncing `useList` + component state is error-prone. Prefer `useDataGrid` as the default path.
- **Remote options with static `Select`** — for network-backed option lists, static `Select` with one-time loads does not scale and misses search behavior. Prefer debounced server-driven `Autocomplete`.

## References

- `references/overview.md` — install, quick-start, provider map
- `references/database-provider.md` — CRUD, filters, operators, sorting, pagination, aggregation, graph
- `references/storage-provider.md` — upload, batch upload, delete, metadata, filters
- `references/app-provider.md` — roles, settings, secrets, function execution, analytics
- `references/user-provider.md` — user CRUD, roles, apps
- `references/auth-provider.md` — login/logout/register, token flow, identity, permissions
- `references/access-control-provider.md` — useCan, CanAccess, prefixed ACL resources, batching
- `references/types-and-utilities.md` — TaruviMeta, StorageUploadVariables, utility functions, deprecated migration
