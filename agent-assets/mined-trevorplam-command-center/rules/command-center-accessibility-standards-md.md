---
description: Run Accessibility (a11y) Standards Check
globs: ['src/components/**/*.tsx', 'src/app/**/*.tsx', '**/*.stories.tsx']
---

# Frontend: Accessibility (a11y) Standards

<audit_rules>

- You MUST ensure all interactive elements have semantic HTML roles (e.g., `<button>`, `<a>`, `<input>`) and are NOT just `<div>`s with click handlers.
- You MUST verify that all `<img>` elements have descriptive `alt` text. For decorative images, use `alt=""` and `role="presentation"`.
- You MUST enforce proper ARIA attributes: `aria-label` or `aria-labelledby` for icon-only buttons, `aria-expanded` for toggle components, and `aria-live` for dynamic content regions.
- You MUST ensure forms have proper `<label>` association (either wrapping or using `htmlFor`/`for` attributes).
- You MUST verify keyboard navigation: all interactive elements must be focusable and operable via Tab/Enter/Space/Arrow keys.
- You MUST flag insufficient color contrast. Ensure text meets WCAG AA standards (4.5:1 for normal text, 3:1 for large text).
  </audit_rules>

<example_good>

```tsx
// Accessible button with icon
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline'

export function SearchButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      aria-label='Search products'
      className='rounded-md p-2 hover:bg-gray-100 focus:ring-2 focus:ring-blue-500'
    >
      <MagnifyingGlassIcon className='h-5 w-5' />
    </button>
  )
}

// Accessible form field
export function EmailField() {
  return (
    <div>
      <label htmlFor='email'>Email Address</label>
      <input
        id='email'
        type='email'
        required
        aria-describedby='email-error'
        className='rounded border px-3 py-2'
      />
      <div id='email-error' className='text-sm text-red-500' aria-live='polite' />
    </div>
  )
}
```

</example_good>

<example_bad>

```tsx
// BAD: Clickable div without keyboard support or semantic meaning
<div onClick={() => navigate()} className="cursor-pointer">
  <img src="/search.png" /> {/* BAD: Missing alt text */}
</div>

// BAD: Label not associated with input
<div>
  <label>Email Address</label> {/* BAD: No htmlFor */}
  <input type="email" className="border rounded" />
</div>
```

</example_bad>
