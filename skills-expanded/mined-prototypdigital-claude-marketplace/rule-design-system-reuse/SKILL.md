---
name: design-system-reuse
description: Reuse existing shared UI components and design tokens before creating new ones.
---

# Design system usage

**Why:** Bespoke components and hardcoded values drift from the design system, breaking visual consistency and theming (dark mode, tokens) and duplicating maintenance.

When building new features or screens:

- Reuse existing shared UI components before introducing new bespoke ones.
- Prefer design tokens and shared theme primitives over hardcoded values.
- Only introduce new UI components if no suitable shared component exists.
- Keep component APIs and naming consistent across the workspace.

## Examples

```tsx
// BAD — bespoke button with hardcoded styles; ignores shared design system
export function SubmitButton() {
  return (
    <button style={{ backgroundColor: '#1a1a2e', color: '#fff', padding: '12px 24px', borderRadius: '4px' }}>
      Submit
    </button>
  )
}

// GOOD — reuses the shared Button component and design tokens
import { Button } from '@/components/ui/Button'

export function SubmitButton() {
  return <Button variant="primary">Submit</Button>
}
```
