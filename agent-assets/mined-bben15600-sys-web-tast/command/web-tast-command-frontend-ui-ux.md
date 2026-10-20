# Frontend UI/UX Skill

## Before You Build

Answer these four questions before touching code:
1. **What is the user's primary task?** (One task per screen/component)
2. **What state does the component have?** (default / loading / error / empty / success)
3. **What is the interaction contract?** (hover / focus / active / disabled / selected)
4. **What are the edge cases?** (long text, RTL, no data, overflow)

## Component Architecture

### Layered structure
```
Page           — data fetching, routing, layout composition
  Section      — semantic grouping, spacing
    Component  — self-contained UI unit with own state
      Primitive — button, input, icon (no business logic)
```

### State machine approach
Every component handles all states:
```tsx
type Status = 'idle' | 'loading' | 'success' | 'error' | 'empty';

function DataTable({ status, data, error }: Props) {
  if (status === 'loading') return <TableSkeleton />;
  if (status === 'error')   return <ErrorState message={error} onRetry={refetch} />;
  if (status === 'empty')   return <EmptyState />;
  return <Table data={data} />;
}
```

## Interaction Design

### Hover / Focus / Active / Disabled
```css
/* Consistent state system */
.btn { background: var(--primary); }
.btn:hover { filter: brightness(1.08); }
.btn:focus-visible { outline: 2px solid var(--primary); outline-offset: 3px; }
.btn:active { transform: scale(0.98); }
.btn:disabled { opacity: 0.45; cursor: not-allowed; pointer-events: none; }
```

### Loading feedback
```tsx
// Loading within an action — never block the UI
<button disabled={isPending} onClick={submit}>
  {isPending ? <Spinner size={16} /> : null}
  {isPending ? 'Saving…' : 'Save'}
</button>
```

**Rule:** If async operation takes > 300ms, show a skeleton or spinner. If > 2s, show a progress indicator with cancel option.

### Optimistic updates
```tsx
// Update UI immediately, roll back on error
const [items, setItems] = useState(serverItems);
const handleDelete = async (id: string) => {
  setItems(prev => prev.filter(i => i.id !== id)); // immediate
  try { await api.delete(id); }
  catch { setItems(serverItems); toast.error('Delete failed'); } // rollback
};
```

## Form Patterns

```tsx
// Complete form field
<FormField>
  <label htmlFor="email">Email address</label>
  <input
    id="email" type="email" autoComplete="email"
    aria-invalid={!!errors.email} aria-describedby="email-error"
  />
  <span id="email-help">We'll never share your email.</span>
  {errors.email && (
    <span id="email-error" role="alert" className="error">
      {errors.email}
    </span>
  )}
</FormField>
```

Rules:
- Validate on blur, not on keystroke.
- Show error message below the field, not at page top.
- Required field = asterisk (*) with `aria-required="true"`.
- Never use placeholder as the only label.

## Responsive Design

```css
/* Mobile-first, 3 breakpoints */
/* Compact:  0–639px  */
/* Medium:  640–1023px */
/* Wide:    1024px+   */

.layout {
  display: grid;
  grid-template-columns: 1fr;            /* compact: single column */
}
@media (min-width: 640px) {
  .layout { grid-template-columns: 1fr 1fr; }
}
@media (min-width: 1024px) {
  .layout { grid-template-columns: 240px 1fr; } /* sidebar + content */
}
```

Rules:
- `min-height: 100dvh` (not `100vh`) for mobile viewport.
- No horizontal overflow on mobile — always `overflow-x: hidden` on body.
- Touch targets minimum `44×44px`.
- Font size minimum `16px` body (prevents iOS auto-zoom).

## Accessibility (Non-Negotiable)

```tsx
// Icon button must have label
<button aria-label="Close dialog">
  <XIcon aria-hidden="true" />
</button>

// Skip link
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to content
</a>

// Live region for dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Focus management after modal open
useEffect(() => {
  if (isOpen) firstFocusableRef.current?.focus();
}, [isOpen]);
```

Checklist:
- [ ] Color contrast ≥ 4.5:1 for body text
- [ ] All interactive elements keyboard-navigable
- [ ] No information conveyed by color alone
- [ ] All images have alt text (empty string if decorative)
- [ ] Modal traps focus while open
- [ ] Animations respect `prefers-reduced-motion`

## Animation Guidelines

```css
/* Duration: match interaction weight */
--duration-micro:    100ms; /* hover, toggle */
--duration-standard: 200ms; /* component transitions */
--duration-page:     300ms; /* page/panel transitions */

/* Easing */
--ease-enter: cubic-bezier(0, 0, 0.2, 1);   /* decelerate */
--ease-exit:  cubic-bezier(0.4, 0, 1, 1);   /* accelerate */
--ease-standard: cubic-bezier(0.4, 0, 0.2, 1); /* both */

@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after { transition-duration: 0.01ms !important; }
}
```

## Performance Checklist

- [ ] Images use `loading="lazy"` below the fold
- [ ] Images declare `width` + `height` to prevent layout shift (CLS)
- [ ] Fonts use `font-display: swap`
- [ ] List of 50+ items uses virtualization
- [ ] Heavy components code-split with `React.lazy()`
- [ ] No layout thrashing (batch DOM reads before writes)
- [ ] `useCallback` / `useMemo` only where profiler shows a bottleneck

## Error States

Every error state must include:
1. What happened (clear, non-technical language)
2. Why it happened (when knowable)
3. What to do next (retry / go back / contact support)

```tsx
<ErrorState
  title="Couldn't load your data"
  description="Check your internet connection and try again."
  action={<button onClick={refetch}>Try again</button>}
/>
```
