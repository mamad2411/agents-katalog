---
name: cr-tailwind-style
description: Tailwind styling preferences. Use when writing or refactoring UI with Tailwind, especially for layout, spacing, responsive behavior, and component-level styling decisions.
---

# Tailwind Style

Use these defaults unless the component or design system requires something else.

## Principles

- Keep Tailwind classes inline when they describe component-local structure and positioning.
- Keep styling isolated to the component by default.
- Keep class lists lean.
- Default to simple, readable utility classes over style cleverness.
- Prefer practical, readable utility usage over class soup.
- Prefer canonical Tailwind utilities over arbitrary values.
- Prefer semantic tokens over repeated magic numbers.
- Keep typography styling simple unless the design system truly requires more.
- Do not override size, tracking, leading, color, and weight all at once without a strong reason.
- Do not customize every typography and spacing property by default.

## Layout and Spacing

- Prefer `flex` or `grid` for layout.
- Prefer `flex`/`grid` + `gap-*` over spacing hacks.
- Prefer `gap-*` for spacing between children.
- Avoid `space-x-*` and `space-y-*` by default.
- Use width, alignment, padding, and responsive utilities directly where the layout is defined.

## Styling Boundaries

- Keep structural styling in the JSX for the component that owns it.
- Do not extract style abstractions for simple one-off cases.
- Prefer inline conditional classes over variant systems such as `cva` unless the complexity is clearly justified.
- If reuse is real, prefer extracting a component over extracting detached class maps.
- Avoid building a style system on top of Tailwind unless the complexity is justified.
- If a design token or semantic utility should exist globally, prefer adding it once instead of repeating arbitrary values across components.

## Variants and Responsiveness

- Keep responsive, dark-mode, and print classes inline at the point of use.
- Make responsive behavior obvious in the component.
- Do not hide simple variant logic behind unnecessary helpers.

## Visual Design Defaults

- Add only the classes needed to express layout, hierarchy, and the intended UI.
- Do not add decorative polish by default unless the request or surrounding code calls for it.
- Favor clean, restrained styling over over-designed utility stacks.
- Default to plain, functional UI. Less is more.
- When typography components or sensible defaults already exist, rely on them instead of overriding font size, tracking, leading, color, and weight in every usage.
- If no typography component exists, prefer simple canonical classes like `text-4xl`, `font-semibold`, or no extra typography classes at all unless they are clearly needed.
- Avoid arbitrary values like `text-[16px]`, `tracking-[-0.02em]`, `leading-[1.05]`, custom rgba values, or one-off border colors unless there is a strong design-system reason.
- Prefer semantic tokens like `border-stroke`, `z-max`, or standard Tailwind scales over duplicated magic numbers.

## Examples

### Prefer `gap` for spacing

```tsx
<div className="flex flex-col gap-4">
  <Label />
  <Input />
  <Hint />
</div>
```

### Avoid `space-*` by default

```tsx
<div className="flex flex-col space-y-4">
  <Label />
  <Input />
  <Hint />
</div>
```

### Prefer inline local structure

```tsx
<div className="flex items-center justify-between gap-4 rounded-md border px-4 py-3">
  <span>Notifications</span>
  <Switch />
</div>
```

### Prefer simple typography

```tsx
<h1 className="text-center text-4xl font-semibold">
  Ask anything. We&apos;ll find the answer.
</h1>
```

### Avoid over-customized typography

```tsx
<h1 className="mx-auto max-w-3xl text-[clamp(2.25rem,5vw,3.5rem)] leading-[1.05] font-semibold tracking-[-0.04em] text-balance">
  Ask anything. We&apos;ll find the answer.
</h1>
```

### Prefer semantic tokens over arbitrary values

```tsx
<header className="sticky top-0 inset-x z-max border-b border-stroke bg-white/90 backdrop-blur-xl">
```

### Avoid repeated magic numbers and one-off colors

```tsx
<header className="sticky top-0 z-50 border-b border-[#e8e8e5] bg-[rgba(247,247,245,0.9)] backdrop-blur-xl supports-[backdrop-filter]:bg-[rgba(247,247,245,0.82)]">
```

### Avoid unnecessary variant indirection

```tsx
const buttonVariants = cva('inline-flex items-center rounded-md px-3 py-2', {
  variants: {
    variant: {
      primary: 'bg-black text-white',
      secondary: 'border border-slate-300',
    },
  },
});
```

Prefer inline conditional classes first unless the component complexity clearly justifies this.

## Output Checklist

Before finishing, check:

- Did I use `gap` instead of `space-*`?
- Are classes mostly local, structural, and readable?
- Is styling kept inside the component unless reuse clearly justifies extraction?
- Did I avoid unnecessary Tailwind indirection?
- Did I avoid arbitrary values when canonical utilities or semantic tokens would work?
- Did I avoid over-customizing typography, spacing, or colors without a strong reason?
- Did I avoid adding extra polish that was not asked for?
