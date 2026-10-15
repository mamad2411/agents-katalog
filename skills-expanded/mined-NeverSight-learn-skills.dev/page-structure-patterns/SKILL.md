---
name: page-structure-patterns
description: Base requirements for page structure, states, and layout patterns that apply to ALL screens in React/Next.js applications
license: MIT
---

# Page Structure Base Requirements

Every screen in the application MUST follow these base patterns. This checklist applies regardless of page type.

## Page State Checklist

### Loading State ✓
Every page that fetches data MUST have a loading state.

```tsx
// REQUIRED: Loading state component
if (isLoading) {
  return <PageLoading message="Loading items..." />;
}

// Standard PageLoading implementation
function PageLoading({ message = 'Loading...' }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-deep">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-text-secondary">{message}</p>
      </div>
    </div>
  );
}
```

### Error State ✓
Every page MUST handle error cases gracefully.

```tsx
// REQUIRED: Error state with recovery path
if (error || !data) {
  return (
    <PageError
      title="Item Not Found"
      message={error || 'The requested item could not be found.'}
      backLink="/items"
      backLabel="Back to Items"
    />
  );
}

// Standard PageError implementation
function PageError({ title, message, backLink, backLabel = 'Go Back' }) {
  return (
    <div className="min-h-screen flex items-center justify-center p-8 bg-surface-deep">
      <div className="bg-red-900/20 border border-red-600/30 rounded-xl p-8 max-w-md text-center">
        <h2 className="text-xl font-semibold text-red-400 mb-2">{title}</h2>
        <p className="text-text-secondary mb-6">{message}</p>
        {backLink && (
          <Link href={backLink} className="inline-block bg-surface-raised hover:bg-border text-white px-6 py-2 rounded-lg">
            {backLabel}
          </Link>
        )}
      </div>
    </div>
  );
}
```

### Empty State ✓
Pages with lists/collections MUST show meaningful empty states.

```tsx
// REQUIRED: Empty state with action
{items.length === 0 && (
  <EmptyState
    icon={<EmptyIcon className="w-16 h-16 text-text-muted" />}
    title={hasFilters ? 'No items match your filters' : 'No items yet'}
    message={hasFilters ? 'Try adjusting your search' : 'Create your first item to get started'}
    action={!hasFilters && (
      <Button variant="primary" onClick={handleCreate}>
        Create First Item
      </Button>
    )}
  />
)}
```

## Page Layout Structure

### Standard Page Layout
EVERY page MUST use the consistent PageLayout wrapper.

```tsx
// REQUIRED: Consistent page structure
return (
  <PageLayout
    title="Page Title"                    // REQUIRED
    subtitle="Optional description"        // Optional
    backLink="/parent"                    // Required for detail pages
    backLabel="Back to Parent"            // Required if backLink provided
    headerContent={<ActionButtons />}      // Optional: Primary actions
    maxWidth="default"                    // 'narrow' | 'default' | 'wide' | 'full'
  >
    {/* Page content */}
  </PageLayout>
);
```

### Header Content Guidelines
| Page Type | Header Content |
|-----------|----------------|
| List Page | Create/Add button |
| Detail Page | Edit + Delete buttons |
| Create Page | None (actions in form) |
| Settings | None |

## Responsive Breakpoints

### Standard Breakpoints
```css
/* Mobile first */
sm: 640px   /* Small tablets */
md: 768px   /* Tablets */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
2xl: 1536px /* Extra large */
```

### Grid Patterns by Screen Size
```tsx
// List pages: Responsive grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">

// Detail pages: Sidebar on desktop
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div className="lg:col-span-1">Sidebar</div>
  <div className="lg:col-span-2">Main content</div>
</div>
```

## Typography Hierarchy

### Required Text Classes
```
h1 (Page Title):     text-3xl font-bold text-white
h2 (Section Title):  text-lg font-semibold text-white
h3 (Card Title):     text-base font-medium text-white
Body:                text-sm text-text-primary
Secondary:           text-sm text-text-secondary
Muted:               text-xs text-text-muted
Mono/Data:           font-mono text-sm
```

## Spacing System

### Consistent Spacing
```
Page padding:        p-6
Card padding:        p-5
Section gap:         mb-6
Element gap:         gap-4
Inline gap:          gap-2
```

## Color Semantic Usage

### Required Color Mapping
| Usage | Color Class |
|-------|-------------|
| Primary actions | bg-accent, text-accent |
| Success states | text-emerald-400, bg-emerald-500/20 |
| Warning states | text-amber-400, bg-amber-500/20 |
| Error states | text-red-400, bg-red-500/20 |
| Info states | text-cyan-400, bg-cyan-500/20 |
| Muted/disabled | text-text-muted, opacity-50 |

## Accessibility Requirements

### ARIA Requirements
```tsx
// Loading states
<div role="status" aria-live="polite">Loading...</div>

// Error messages
<div role="alert">Error message</div>

// Interactive elements
<button aria-label="Delete item">
  <TrashIcon />
</button>

// Form fields
<input
  id="email"
  aria-invalid={hasError}
  aria-describedby={hasError ? 'email-error' : undefined}
/>
```

### Keyboard Navigation
- All interactive elements must be focusable
- Tab order must be logical
- Escape closes modals/dropdowns
- Enter activates buttons/links

## Data Fetching Pattern

### Standard Data Loading
```tsx
function Page() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('/api/items');
        const result = await response.json();
        if (result.success) {
          setData(result.data);
        } else {
          setError(result.error || 'Failed to load');
        }
      } catch {
        setError('Failed to connect to server');
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  // REQUIRED: Handle all states
  if (isLoading) return <PageLoading />;
  if (error || !data) return <PageError message={error} />;
  return <PageContent data={data} />;
}
```

## Required Page Metadata

### Next.js Head
```tsx
// Every page should set appropriate title
<Head>
  <title>{pageTitle} | AppName</title>
</Head>
```

## Audit Checklist

When reviewing ANY page, verify:

### Critical (Must Fix)
- [ ] Has loading state - users see blank/broken page without it
- [ ] Has error state with recovery path - users get stuck without it
- [ ] Meets ARIA requirements - accessibility violation
- [ ] Keyboard navigable - accessibility violation

### Major (Should Fix)
- [ ] Has empty state (if applicable) - confusing without guidance
- [ ] Uses PageLayout wrapper - inconsistent experience
- [ ] Has appropriate title/subtitle - navigation confusion
- [ ] Has back navigation (if detail page) - users get trapped
- [ ] Responsive at all breakpoints - mobile users blocked

### Minor (Nice to Have)
- [ ] Header actions follow guidelines - consistency
- [ ] Follows typography hierarchy - visual polish
- [ ] Uses semantic colors correctly - visual polish
