---
description: UI/UX rules for TIMER: mobile-first, Shadcn-first, Next Image, dialogs/toasts.
globs: "app/**/*.tsx, components/**/*.tsx"
alwaysApply: false
---

## UI and styling (mobile-first is mandatory)
- Use Shadcn UI components (`@/components/ui/*`) and Tailwind utility classes.
- Mobile-first responsive design: toolbars/action bars stack on mobile (`flex-col`) and row on larger screens (`sm:flex-row`).
- Prefer `w-full sm:w-auto` for toolbar buttons and actions.
- Avoid horizontal scrolling; use `flex-wrap` or vertical stacking.
- Standard radius: `rounded-lg` (avoid `rounded-full` unless truly needed).
- **Floating buttons (mandatory)**: All floating action buttons (buttons with `fixed` positioning, typically mobile thumb-reachable buttons) must use `rounded-full` for consistent circular appearance. Pattern: `fixed bottom-6 left-6 z-50 h-12 w-12 rounded-full ...`

## Icons and images
- Use Lucide icons sized with `size={20}` / `size={16}` / `size={12}` only.
- Never use `<img>`; always use Next.js `Image` from `next/image`.

## Loading and confirmations (mandatory)
- **Always use Skeleton loaders (`Skeleton`) everywhere** - never use full-screen loading overlays or generic spinners for content loading.
- Create skeleton components that match the structure of the actual content (e.g., `TemplateCardSkeleton` for template cards).
- Skeleton loaders should be placed inline where content will appear, maintaining layout stability.
- Never use `confirm()`, `alert()`, `prompt()`; use Shadcn dialogs/alert dialogs and toasts.

## Inputs (mobile UX)
- For time/number inputs use `inputMode=\"numeric\"` and `pattern=\"[0-9:]*\"` when appropriate.
- Prefer wider inputs and larger touch targets on mobile.

## FloatLabel (mandatory)
- **Always use `FloatLabel` component** for all form inputs (`Input`, `Select`, etc.) instead of separate `Label` components.
- FloatLabel provides consistent floating label animation that improves UX and saves vertical space.
- Pattern: Wrap the input/select with `<FloatLabel label="Label text" hasValue={boolean}>...</FloatLabel>`
- The `hasValue` prop determines if the label should be floating (true) or in-place (false).
- Example:
  ```tsx
  <FloatLabel label="Category" htmlFor="category" hasValue={!!value}>
    <Select value={value} onValueChange={setValue}>
      <SelectTrigger id="category">
        <SelectValue />
      </SelectTrigger>
      <SelectContent>...</SelectContent>
    </Select>
  </FloatLabel>
  ```

## Accessibility (WCAG AA compliance - mandatory)
- **Color contrast**: Text must meet WCAG AA contrast ratios:
  - Normal text (≤18pt or ≤14pt bold): minimum 4.5:1 contrast ratio
  - Large text (>18pt or >14pt bold): minimum 3:1 contrast ratio
  - Interactive elements (buttons, links): minimum 3:1 contrast ratio
- **Keyboard navigation**: All interactive elements must be keyboard accessible:
  - Use semantic HTML (`<button>`, `<a>`, `<input>`) instead of `<div>` with onClick
  - Ensure logical tab order
  - Provide visible focus indicators (use `focus-visible` utilities)
- **Focus management**: 
  - Focus must be visible (use `focus-visible:ring-2 focus-visible:ring-offset-2`)
  - Trap focus in modals/dialogs
  - Return focus to trigger element when closing dialogs
- **ARIA labels**: 
  - Use `aria-label` for icon-only buttons and interactive elements without visible text
  - Use `aria-describedby` for form inputs with error messages
  - Use `aria-live` regions for dynamic content updates
- **Form accessibility**:
  - All inputs must have associated `<label>` elements (use Shadcn `Label` component)
  - Error messages must be associated with inputs via `aria-describedby`
  - Required fields must have `aria-required="true"` or `required` attribute
- **Images**: 
  - All `Image` components must have descriptive `alt` text
  - Decorative images should use `alt=""` (empty string)
- **Semantic HTML**: 
  - Use proper heading hierarchy (`h1` → `h2` → `h3`, etc.)
  - Use semantic elements (`<nav>`, `<main>`, `<header>`, `<footer>`, `<section>`)
  - Use `<button>` for actions, `<a>` for navigation
- **Screen reader support**:
  - Provide text alternatives for all non-text content
  - Ensure all functionality is available via keyboard
  - Use `role` attributes only when semantic HTML is insufficient
