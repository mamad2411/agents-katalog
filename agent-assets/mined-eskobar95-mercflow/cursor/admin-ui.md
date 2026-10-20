---
description: Rules for working inside packages/admin-ui. Apply when editing or creating admin UI components, pages, or styles.
globs: ["packages/admin-ui/**/*"]
alwaysApply: false
---

# Admin UI Rules

## Design Philosophy

The MercFlow admin UI is inspired by Shopify Admin: light, clean, and spacious. Every design decision should reduce cognitive load and increase clarity. When in doubt, add more whitespace — not less.

**Reference:** Shopify Polaris design system (for inspiration only — do not import it).

---

## Design Tokens

All visual values come from `packages/design-tokens`. Never hardcode values.

```ts
// ❌ Wrong
className="bg-[#f4f6f8] text-[#1a1a1a] rounded-[6px]"

// ✅ Correct
className="bg-surface text-content-primary rounded-md"
```

The token system exposes:

| Category | CSS variable prefix | Tailwind class prefix |
|---|---|---|
| Backgrounds | `--color-surface-*` | `bg-surface-*` |
| Text | `--color-content-*` | `text-content-*` |
| Borders | `--color-border-*` | `border-border-*` |
| Interactive | `--color-interactive-*` | varies |
| Spacing | `--spacing-*` | standard Tailwind scale |
| Radius | `--radius-*` | `rounded-*` |

If a token you need does not exist, add it to `packages/design-tokens` first — do not work around it.

---

## Component Architecture

### Hierarchy

```
Radix UI primitives
    ↓
MercFlow base components  (packages/admin-ui/src/components/ui/)
    ↓
MercFlow feature components  (packages/admin-ui/src/components/*)
    ↓
Pages  (packages/admin-ui/src/pages/*)
```

- **Base components** (`/components/ui/`): Thin wrappers around Radix primitives with MercFlow token-based styling. Examples: `Button`, `Input`, `Badge`, `Card`, `Dialog`.
- **Feature components** (`/components/`): Domain-specific components composed from base components. Examples: `ProductContentTab`, `SEOPreview`, `MediaGallery`.
- **Pages** (`/pages/`): Route-level components. Compose feature components. Contain no business logic — delegate to hooks.

### Naming conventions

| Type | Convention | Example |
|---|---|---|
| Components | PascalCase | `ProductContentTab.tsx` |
| Hooks | camelCase with `use` prefix | `useProductContent.ts` |
| Utilities | camelCase | `formatSeoTitle.ts` |
| Types/interfaces | PascalCase with descriptive name | `ProductContentFields.ts` |

### File structure within a feature

```
components/product-content/
├── ProductContentTab.tsx     ← Main export
├── SEOPreview.tsx            ← Sub-component
├── MediaGalleryManager.tsx   ← Sub-component
├── hooks/
│   └── useProductContent.ts
├── types.ts
└── index.ts                  ← Re-exports public API only
```

---

## Navigation Rules

MercFlow replaces Medusa's modal-heavy navigation with page-based routing.

### When to use a PAGE (not a modal)

Use a dedicated page with URL routing when:
- The user is navigating to a primary entity (product, category, order, customer)
- The form has more than 4 fields
- The user might need to deep-link or share the URL
- The action is the primary purpose of the interaction

### When to use a MODAL (dialog)

Use a modal only for:
- Destructive action confirmation ("Are you sure you want to delete?")
- Short, focused forms with 1–3 fields (e.g., rename, add tag)
- Contextual actions that don't deserve their own URL (e.g., quick status change)

### Page transitions

All page navigations use a **shared** transition. **`AdminShell` wraps the router `<Outlet />` with `PageTransition`**, keyed by the active `location` so the enter animation runs on every route change. **Page components** under `src/pages/` should export **content only** — do not wrap them in `PageTransition` (avoids double application). Do not implement custom per-page transition effects; extend the shared `PageTransition` / shell integration instead.

---

## List Views

All list views (products, orders, customers, categories) follow this structure:

```
ListPage
├── ListHeader (title, primary action button)
├── ListFilters (search, filter chips)
├── DataTable
│   ├── Column definitions (typed)
│   ├── Sortable columns
│   └── Row actions (dropdown, not inline buttons)
└── Pagination
```

Rules:
- Every list view must support keyboard navigation
- Row actions go in a `...` dropdown — never render more than one inline action button per row
- Empty states must have a helpful message and a primary action (not just "No results")
- Loading states use skeleton loaders — never spinners on full-page loads

---

## Accessibility

- All interactive elements must be keyboard accessible
- Use semantic HTML — `<button>` for actions, `<a>` for navigation, `<nav>` for navigation regions
- Every form input must have an associated `<label>` (not placeholder-only)
- Color must never be the sole means of conveying information
- All images and icons used as content must have descriptive `alt` text or `aria-label`

---

## TipTap Rich Text Editor

MercFlow uses TipTap v2 as the rich text editor for content fields.

**Standard extension set** (do not add extensions without explicit instruction):
- `StarterKit` (bold, italic, headings H2–H4, lists, blockquote, code)
- `Link` (with `openOnClick: false`)
- `Image` (via media upload, not URL input)
- `CharacterCount`

**Output format:** JSON (stored as `jsonb` in PostgreSQL). Never store HTML directly.

**Rendering:** A separate `RichTextRenderer` utility converts stored JSON to HTML for storefront use.

```tsx
// ❌ Wrong — do not store HTML
content: "<p>Hello</p>"

// ✅ Correct — store TipTap JSON
content: { type: "doc", content: [...] }
```
