---
description: Component-first protocol for admin-ui. Apply when adding any UI to packages/admin-ui — before writing any JSX. Ensures reuse over duplication.
globs: ["packages/admin-ui/**/*"]
alwaysApply: false
---

# Component-First Protocol

Before writing a single line of JSX, run this lookup. No exceptions.

---

## The 3-step lookup

### Step 1 — Does a base component already exist?

Check `packages/admin-ui/src/components/ui/` first.

Current base components:
- `Button` (variants: primary, secondary, destructive, ghost)
- `Input` (text, search, number)
- `Card` (container, header, body, footer)
- `Badge` (status, count)
- `Dialog` (confirm, form)
- `Skeleton` (loading placeholders)
- `DataTable` (list view with sort, filter, pagination)
- `PageTransition` (route-level enter animation — do not use directly in pages)

If a base component covers the need → **use it as-is**. Do not wrap it in another component unnecessarily.

### Step 2 — Does a feature component already exist that is close?

Check `packages/admin-ui/src/components/` for domain-specific components.

Current feature components:
- `product-content/` — ProductContentTab, SEOPreview, MediaGalleryManager
- `category-content/` — CategoryContentTab
- `content-locale/` — LocaleSelector, LocaleSwitcher
- `layout/` — AdminShell, Sidebar, PageHeader

If a similar feature component exists:
- **Reuse it** if it exactly fits the need
- **Add a prop/variant** if it needs a minor extension (e.g., a new `variant` or optional `footer` slot)
- **Do NOT copy-paste and rename** — that creates divergence

### Step 3 — Does nothing exist? Build a new component.

Only build a new component when Steps 1 and 2 find nothing reusable.

When building new:
- Place it in `components/<feature-area>/` — never inline inside a `pages/` file
- Follow the file structure from `admin-ui.mdc` (main export + sub-components + hooks/ + types.ts + index.ts)
- Use only base components (`/components/ui/`) and design tokens — never hardcoded values

---

## Decision flowchart

```
Need UI for X?
    │
    ▼
Does a base component in /ui/ cover it?
    YES → use it directly
    NO  ↓
Does a feature component exist with similar structure?
    YES, exact match → use it directly
    YES, close match → extend with a new prop/variant
    NO  ↓
Build a new feature component in components/<feature-area>/
    Never inline it in a page file
```

---

## Hard rules

```tsx
// ❌ Never — inline component inside a page
export default function ProductsPage() {
  function ProductRow({ product }) { ... }  // defined inside page
  return <table>{products.map(p => <ProductRow key={p.id} product={p} />)}</table>
}

// ✅ Correct — component in its own file
// components/product-list/ProductRow.tsx
export function ProductRow({ product }: { product: Product }) { ... }

// pages/products/index.tsx
import { ProductRow } from "@/components/product-list/ProductRow"
```

```tsx
// ❌ Never — hardcoded values
className="bg-[#f4f6f8] text-[14px] rounded-[6px] p-[16px]"

// ✅ Correct — design tokens
className="bg-surface text-sm rounded-md p-4"
```

```tsx
// ❌ Never — inline business logic in a page
export default function ProductsPage() {
  const [products, setProducts] = useState([])
  useEffect(() => {
    fetch("/api/products").then(r => r.json()).then(setProducts)
  }, [])
  // ...
}

// ✅ Correct — logic in a hook
// hooks/useProducts.ts
export function useProducts() { ... }

// pages/products/index.tsx
const { products, isLoading } = useProducts()
```

---

## Variation guide

When extending an existing component, prefer:
1. **New prop with default** — `variant?: "default" | "compact"` — backward compatible
2. **Optional render prop / slot** — `footer?: ReactNode` — composable
3. **New sub-component** — `DataTable.EmptyState` — co-located, discoverable

Never:
- Change a component's existing prop interface in a breaking way
- Add Guapo-specific logic inside a base component (keep base components generic)
