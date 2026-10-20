---
description: Run CSS, Styling, and Tailwind Configuration Check
globs: ['**/*.tsx', '**/*.css', 'tailwind.config.ts']
---

# Frontend: Styling Architecture

<audit_rules>

- You MUST enforce the use of design tokens (theme colors, spacing) from the Tailwind config.
- You MUST flag and reject the use of arbitrary Tailwind values (e.g., `w-[32px]`, `text-[14px]`) unless absolutely necessary for a one-off edge case.
- You MUST verify that z-indexes are managed centrally (e.g., in Tailwind config) rather than hardcoded arbitrarily (e.g., `z-[999]`).
- You MUST ensure semantic HTML tags are used alongside classes (`<main>`, `<nav>`, `<article>`, `<aside>`) instead of just `<div>`.
  </audit_rules>

<example_good>

```tsx
<button className='rounded-md bg-primary px-4 py-2 text-primary-foreground'>Submit</button>
```

</example_good>

<example_bad>

```tsx
// BAD: Arbitrary values and hardcoded colors
<button className='z-[999] rounded-[5px] bg-[#FF5733] px-[15px] py-[8px] text-white'>Submit</button>
```

</example_bad>
