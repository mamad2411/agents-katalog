# CleanMateX/CleanMateXSAAS – AI Frontend Instructions  
## Architecture & UI Generation Rules (Final Structure)

You are generating code for **CleanMateX/CleanMateXSAAS**, a multi-tenant SaaS platform built with **Next.js App Router, TypeScript, TailwindCSS, shadcn/ui, Supabase**, and a custom **Cmx UI Design System**.

The **final, authoritative folder structure** is:

- `app/` – Next.js routing only
- `src/ui/` – Global Cmx Design System (reusable UI)
- `src/features/` – Feature modules (domain UI + logic)
- `lib/` – Shared infrastructure (root-level: API, hooks, utils, config)

These rules are **mandatory** for all generated code.

---

## 1. Project Architecture (MUST FOLLOW)

### 1.1 Routing Layer – `app/`

- Contains:
  - `page.tsx`, `layout.tsx`, `template.tsx`
  - `loading.tsx`, `error.tsx`
  - Route groups `(dashboard)`, `(auth)`, etc.
- Responsibilities:
  - Routing and composition only.
  - Compose feature screens and Cmx UI.
- DO NOT:
  - Define reusable primitives.
  - Put business logic here.
  - Put design system components here.

### 1.2 Global UI System – `src/ui/`

- The **Cmx Design System** lives here.
- Contains:
  - `src/ui/foundations/` – tokens, theme, CSS vars
  - `src/ui/primitives/` – `CmxButton`, `CmxInput`, `CmxCard`, etc.
  - `src/ui/forms/` – `CmxForm`, `CmxFormField`, `CmxFormSection`
  - `src/ui/data-display/` – `CmxDataTable`, `CmxKpiCard`, `CmxEmptyState`
  - `src/ui/navigation/` – `CmxAppShell`, sidebar, breadcrumbs, tabs nav
  - `src/ui/layouts/` – major layout shells
  - `src/ui/patterns/` – CRUD shells, list-with-filters, wizards
  - `src/ui/charts/` – Recharts wrappers
  - `src/ui/feedback/` – toast, inline error/success, confirm dialog
  - `src/ui/overlays/` – modals, side panels

- All global reusable components MUST be prefixed with **`Cmx`**.

### 1.3 Feature Modules – `src/features/`

- Domain-level modules live here:
  - `src/features/orders/`
  - `src/features/customers/`
  - `src/features/tenants/`
  - etc.
- Each feature may have:
  - `ui/` – feature-specific components and screens
  - `api/` – API clients for this feature
  - `hooks/` – feature hooks
  - `model/` – types and mappers

Examples:

```text
src/features/orders/
  ui/
    order-list-screen.tsx
    order-filters.tsx
  api/
    orders-api.ts
  hooks/
    use-orders.ts
  model/
    order-types.ts
```

### 1.4 Shared Infrastructure – `lib/` (root-level)

- Contains:
  - `lib/api/` – base API clients
  - `lib/supabase/` – supabase client
  - `lib/hooks/` – generic hooks
  - `lib/utils/` – utilities
  - `lib/config/` – configuration helpers

---

## 2. Path Aliases (use these in imports)

Assume `tsconfig.json` has:

```jsonc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@ui/*": ["src/ui/*"],
      "@features/*": ["src/features/*"],
      "@lib/*": ["lib/*"]
    }
  }
}
```

You MUST use these aliases:

- Global UI (design system):
  ```ts
  import { CmxButton } from '@ui/primitives/cmx-button'
  ```

- Feature UI:
  ```ts
  import { OrderListScreen } from '@features/orders/ui/order-list-screen'
  ```

- Infrastructure:
  ```ts
  import { apiClient } from '@lib/api/client'
  ```

Do not invent other top-level paths like `@/components` or `@/core` unless they map to the above.

---

## 3. Rules for Where Code Goes

### 3.1 Reusable UI → `src/ui/`

- **Mandatory when applicable:** use Global Message Utility (`cmxMessage` / `useMessage()` from `@ui/feedback`) for user-facing success/error/warning/info/confirm feedback. Canonical: `docs/dev/rules/cmx-message.md`. Do not add new legacy toast helpers / `alert()`.

- **Always use `tCommon` for common keys** (save, cancel, delete, edit, create, loading, error, etc.):
  ```ts
  const tCommon = useTranslations('common');
  ```

- **Before adding UI text:** Search `web-admin/messages/en/**` and `web-admin/messages/ar/**`; reuse common keys; run `npm run check:i18n` after i18n changes
  
- Any component that is:
  - Reused across multiple features
  - Generic in nature (button, input, table, layout, etc.)
  belongs in `src/ui/` and uses `Cmx` prefix.

Examples:
- `CmxButton`
- `CmxInput`
- `CmxForm`
- `CmxDataTable`
- `CmxPageHeader`
- `CmxListWithFilters`

### 3.2 Feature-Specific UI → `src/features/<module>/ui`

- Components that contain business/domain logic, such as:
  - `OrderStatusBadge`
  - `CustomerTierBadge`
  - `OrderListScreen`
  - `TenantSettingsForm`
- These must live in:
  - `src/features/orders/ui/...`
  - `src/features/customers/ui/...`

### 3.3 Routes → `app/`

- Only use `app/` for:
  - Composing feature screens
  - Handling routing, layouts, segment-specific logic

Example:

```tsx
// app/dashboard/orders/page.tsx
import { OrderListScreen } from '@features/orders/ui/order-list-screen'

export default async function OrdersPage() {
  return <OrderListScreen />
}
```

---

## 4. Theming & Styling Rules

### 4.1 Theme Engine

- Theme (colors, radius, density, dark mode, etc.) is controlled by a Theme Settings Engine.
- `ThemeProvider` sets DOM attributes on `<html>`:
  - `class="dark"` (for dark mode)
  - `data-accent="blue" | "emerald" | "violet"`
  - `data-radius="sm" | "md" | "lg"`
  - `data-density="compact" | "comfortable" | "spacious"`

### 4.2 Styling – DO and DO NOT

DO:

- Use CSS variables and theme tokens:
  - `rgb(var(--cmx-primary-rgb))`
  - `rgb(var(--cmx-border-rgb))`
- Use Tailwind for layout/spacing/typography:
  - `flex`, `grid`, `gap-4`, `p-4`, `text-sm`, etc.

DO NOT:

- Hardcode brand colors:
  - `text-blue-500`, `bg-red-500`, etc.
- Use hex codes directly in components:
  - `#1d4ed8`, `#ef4444`, etc.
- Use shadcn/ui directly inside features – always wrap as Cmx in `src/ui` first.

---

## 5. Import Rules (CRITICAL)

### From `src/ui` (global design system):

```ts
import { CmxButton } from '@ui/primitives/cmx-button'
import { CmxDataTable } from '@ui/data-display/cmx-datatable'
import { CmxPageHeader } from '@ui/navigation/cmx-page-header'
```

### From `src/features` (domain UI):

```ts
import { OrderListScreen } from '@features/orders/ui/order-list-screen'
import { CustomerForm } from '@features/customers/ui/customer-form'
```

### From `lib` (infra):

```ts
import { supabaseClient } from '@lib/supabase/client'
import { apiClient } from '@lib/api/client'
```

### NEVER:

- Import UI from `app/*`:
  - `import X from '@/app/components/...` → FORBIDDEN
- Invent `components/` or `shared/` or `common/` top-level UI folders.
- Mix `src/ui` and `components/ui`. There is only `src/ui`.

---

## 6. Behavior Rules for Generated Code

When generating any new component:

1. Decide: **global reusable UI** vs **feature-specific UI**.
2. If reusable:
   - Place in `src/ui/` under the correct subfolder.
   - Prefix name with `Cmx`.
3. If feature-specific:
   - Place in `src/features/<module>/ui/`.
4. Import:
   - From `@ui/*` for Cmx components.
   - From `@features/*` for feature UI.
   - From `@lib/*` for infra.

When generating pages/routes in `app/`:

- Only compose from `src/features` + `src/ui` + `lib`.
- Do not declare new primitives or design system elements in `app/`.

---

## 7. Example End-to-End Wiring

### UI primitive (global):

```tsx
// src/ui/primitives/cmx-button.tsx
export function CmxButton() {
  // implementation using Tailwind + CSS tokens
}
```

### Feature screen:

```tsx
// src/features/orders/ui/order-list-screen.tsx
import { CmxListWithFilters } from '@ui/patterns/cmx-list-with-filters'
import { CmxDataTable } from '@ui/data-display/cmx-datatable'

export function OrderListScreen() {
  // compose filters + datatable
}
```

### Route:

```tsx
// app/dashboard/orders/page.tsx
import { OrderListScreen } from '@features/orders/ui/order-list-screen'

export default function OrdersPage() {
  return <OrderListScreen />
}
```

Follow these rules consistently for ALL frontend code generation in CleanMateX/CleanMateXSAAS.
