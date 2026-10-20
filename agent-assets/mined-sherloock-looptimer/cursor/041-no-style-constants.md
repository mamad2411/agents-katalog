---
description: Never extract Tailwind classes into constants; keep styles inline.
globs: "app/**/*.tsx, components/**/*.tsx, lib/constants/**/*.ts"
alwaysApply: true
---

## No style constants (critical)
- **NEVER** extract full Tailwind class strings into constants.
- Always keep Tailwind classes inline in the JSX where they are used.
- Extracting styles to constants creates a maintenance nightmare and breaks the ability to see and modify styles at a glance.

### Bad (do NOT do this):
```ts
const CARD_CLASS = "mx-auto w-full max-w-md rounded-2xl border p-4";
<div className={CARD_CLASS}>...</div>
```

### Good (always do this):
```tsx
<div className="mx-auto w-full max-w-md rounded-2xl border p-4">...</div>
```

## What you CAN extract to constants:
- Magic values: durations, thresholds, pixel values used in calculations
- Configuration: color hex codes, API endpoints, storage keys
- Labels and text content
- Numeric spacing values if used in calculations (not class strings)

## Exception:
- If you need a reusable component variant system, use proper component composition or Tailwind's `@apply` directive in CSS, not string constants.
