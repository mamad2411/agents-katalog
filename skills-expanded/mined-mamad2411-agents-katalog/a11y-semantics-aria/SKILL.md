---
name: a11y-semantics-aria
description: Use when choosing between semantic HTML and a div/span+ARIA, or when adding aria-label, aria-labelledby, aria-describedby, aria-live, aria-expanded/controls to any React component. Use before adding onClick to a div/span, or any aria-* attribute.
metadata:
  origin: community (decomposed from frontend-a11y)
allowed-tools: Read, Edit, Grep, Glob
---

# Semantic HTML and ARIA usage

**Rule of thumb: use ARIA only when native HTML semantics can't express the intent. Wrong ARIA is
worse than no ARIA** — it lies to assistive tech about what an element does.

## Prefer semantic elements over div+ARIA

```tsx
// BAD — no role, no keyboard support, no accessible name
<div onClick={handleClick}>Submit</div>
// GOOD
<button type="button" onClick={handleClick}>Submit</button>

// BAD
<div onClick={() => navigate('/home')}>Home</div>
// GOOD — supports right-click, middle-click, keyboard
<a href="/home">Home</a>

// BAD — heading hierarchy skipped h1 -> h4
<h1>Dashboard</h1>
<h4>Recent Activity</h4>
// GOOD — sequential levels
<h1>Dashboard</h1>
<h2>Recent Activity</h2>
```

## aria-label vs aria-labelledby

```tsx
// aria-label: inline string, use when there's no visible label text
<button aria-label="Close modal"><XIcon /></button>

// aria-labelledby: references another element's visible text
<section aria-labelledby="section-title">
  <h2 id="section-title">Recent Orders</h2>
</section>
```

## aria-describedby for supplementary info

```tsx
<button aria-describedby="delete-warning" onClick={handleDelete}>Delete account</button>
<p id="delete-warning">This action cannot be undone.</p>
```

## aria-live for content that updates without navigation

```tsx
// polite: waits for the user's current action to finish before announcing
// assertive: interrupts immediately — reserve for urgent/blocking errors
export function StatusMessage({ message, isError }: { message: string; isError?: boolean }) {
  return (
    <div role="status" aria-live={isError ? 'assertive' : 'polite'} aria-atomic="true">
      {message}
    </div>
  );
}
```

## aria-expanded / aria-controls for disclosure widgets

```tsx
export function Accordion({ title, children }: { title: string; children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const contentId = useId();
  return (
    <div>
      <button aria-expanded={isOpen} aria-controls={contentId} onClick={() => setIsOpen((v) => !v)}>
        {title}
      </button>
      <div id={contentId} hidden={!isOpen}>{children}</div>
    </div>
  );
}
```

## Images and icons

```tsx
// Decorative — hide from screen readers entirely
<img src="/decoration.png" alt="" aria-hidden="true" />
// Meaningful — describe what it conveys, not what it depicts
<img src="/chart.png" alt="Monthly revenue increased 23% from January to March" />
// Icon-only button — label the button, hide the icon from the accessibility tree
<button aria-label="Delete item"><TrashIcon aria-hidden="true" /></button>
```

## Anti-patterns

```tsx
// aria-label on an element with no role does nothing useful — give it a role or use a real element
<div aria-label="Navigation">...</div>

// role="button" without keyboard support — Enter/Space won't activate it
<div role="button" onClick={handleClick}>Submit</div> // missing tabIndex={0} + onKeyDown

// aria-hidden on a focusable element traps keyboard users on an invisible-to-AT control
<button aria-hidden="true">Open</button>

// positive tabIndex creates a tab order independent of visual order — avoid entirely
<button tabIndex={3}>Submit</button>
```

## Related

- `a11y-keyboard-nav` — once a custom widget needs `role`, it also needs the matching keyboard
  handlers (this skill covers only the ARIA attributes, not the `onKeyDown` logic).
- `a11y-forms` — form-specific labeling/error patterns.
