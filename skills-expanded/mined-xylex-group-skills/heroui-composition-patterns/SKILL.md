---
name: heroui-composition-patterns
description: >
  Build flexible HeroUI v3 UI with composition: framework-agnostic styles from
  @heroui/styles, polymorphic styling via buttonVariants/linkVariants and BEM,
  compound components (dot notation, .Root, named exports), mixing variants,
  custom components and tv() extensions, render prop for custom DOM/Motion/Next
  Link, and Next/React Router/Vue/Svelte integration. Keywords: HeroUI composition,
  compound components, buttonVariants, BEM classes, render prop, mergeProps,
  ButtonRootProps, Link.Icon slots. Use when the user runs /heroui-composition-patterns.
---

# HeroUI Composition Patterns (v3)

Composition patterns for flexible, customizable HeroUI components: change the rendered element, compose parts, keep full markup control.

**Source:** https://heroui.com/en/docs/react/getting-started/composition

## Apply the Skill

- Read `references/composition.md` for full code samples (custom variants, `render` prop, Vue).
- Use when styling non-HeroUI hosts (Next.js `Link`, React Router `Link`, native `<a>`), composing multi-part components, or extending variants with `tv`.
- For semantic variant *meaning* (primary/secondary/tertiary), also use `heroui-design-principles`.
- For install/CLI/framework scaffold, use `heroui-cli` / `heroui-frameworks` / `heroui-react`.

## Non-Negotiables

| Do | Don't |
|----|--------|
| Prefer compound parts (`Alert.Title`, etc.) over flat mega-props | Flatten compound UIs into one-off prop bags |
| Use `@heroui/styles` for non-React or style-only | Pull `@heroui/react` just for class strings in Vue/Svelte |
| Pass slots manually when root is custom (`slots.base()`, BEM) | Assume child context works without HeroUI Root |
| Prefer named types: `ButtonRootProps` or `Button["RootProps"]` | Use removed `Button.RootProps` namespace types |
| `render` prop: same element type, single root DOM, spread `domProps` | Swap `<button>` for `<a>` without matching expectations; fragments as root |
| Merge extra props with `mergeProps` when needed | Drop required DOM/ARIA props from `render` |

## Work in This Order

1. **Need behavior + a11y?** Use `@heroui/react` components (compound pattern).
2. **Need look only on a foreign host?** Prefer `*Variants` from `@heroui/styles`, or BEM classes if simplest.
3. **Custom router link with full Link API?** Prefer `render` on `Link` / `Button` over reimplementing press/focus.
4. **Domain wrapper?** Compose primitives (Button + Tooltip) or thin wrappers with `buttonVariants`.
5. **Design-system extension?** `tv({ extend: buttonVariants, … })` + typed props via `VariantProps` + `Omit<ButtonRootProps, "className">`.

## Decision Rules

### Styles package vs React package

```tsx
// Framework-agnostic (Vue, Svelte, style-only)
import { buttonVariants } from "@heroui/styles";

// Same functions re-exported
import { buttonVariants } from "@heroui/react";
```

Use `@heroui/styles` when avoiding React dependencies.

### Polymorphic styling (pick one)

| Approach | When |
|----------|------|
| **BEM** (`button button--primary`) | Simplest; no type safety; any HTML/framework |
| **Variant functions** (`buttonVariants({ variant, size })`) | Type-safe; sizes/variants; preferred for TS apps |
| **`render` prop** | Keep HeroUI behavior/a11y on a custom element (Motion, Next Link) |

**Button BEM cheatsheet:**

- Base: `.button`
- Variants: `.button--primary` | `--secondary` | `--tertiary` | `--danger` | `--ghost`
- Sizes: `.button--sm` | `--md` | `--lg`
- Icon-only: `.button--icon-only`

### Custom root + compound children

When the root is not HeroUI's Root, **children lose context slots**. Pass classes yourself:

```tsx
const slots = linkVariants();

<NextLink className={slots.base()} href="/about">
  About
  <Link.Icon className={slots.icon()} />
</NextLink>
```

Or BEM: `link` + `link__icon`.

### Compound component syntax (all valid)

1. **Recommended:** `<Alert>` + `<Alert.Icon />` (no `.Root`)
2. **Explicit:** `<Alert.Root>` …
3. **Named exports:** `AlertRoot`, `AlertIcon`, …
4. **Mixed:** `Alert` + `AlertTitle` named imports together

Simple components (`Button`) follow the same: `Button` / `Button.Root` / `ButtonRoot`.

### Mixing variant functions

You may style a `Link` with `buttonVariants` (or combine patterns) when the visual system should look like another component.

### Custom variants (`tv` extend)

```tsx
import { buttonVariants, tv } from "@heroui/styles";
import type { ButtonRootProps } from "@heroui/react";
import type { VariantProps } from "tailwind-variants";

const myButtonVariants = tv({
  extend: buttonVariants,
  variants: { /* radius, size, variant overrides */ },
  defaultVariants: { /* … */ },
});

type MyButtonProps = Omit<ButtonRootProps, "className"> &
  VariantProps<typeof myButtonVariants> & { className?: string };
```

### `render` prop rules

Applies on components that support `render` (e.g. Button, Link):

1. Always render the **expected element type** (dev warning on mismatch).
2. **Single** root DOM node (no fragments).
3. Always spread provided props onto that DOM node; merge with `mergeProps` if needed.

```tsx
// Motion
<Button
  render={(domProps, { isPressed }) => (
    <motion.button {...domProps} animate={{ scale: isPressed ? 0.9 : 1 }} />
  )}
>
  Press me
</Button>

// Next.js Link host
<Link
  render={({ ref, ...domProps }) => (
    <NextLink {...domProps} ref={ref as React.Ref<HTMLAnchorElement>} href="/privacy-policy" />
  )}
>
  Privacy Policy
</Link>
```

### Framework integration

| Stack | Pattern |
|-------|---------|
| Next.js Link | `buttonVariants` / BEM on `next/link`, or `Link` + `render` → NextLink |
| React Router | Same with `to=` instead of `href` |
| Vue / Svelte / others | `import { buttonVariants } from '@heroui/styles'` only |

## Anti-Patterns

- Importing full React tree in non-React apps for styles alone
- Expecting `Link.Icon` to get styles without slot/`className` when root is custom
- `Button.RootProps` type (removed) — use `ButtonRootProps` or `Button["RootProps"]`
- Using BEM/variants when you still need `onPress`/focus management — use the React component or `render`
- Dropping `domProps` / ref in `render` implementations
- Rendering wrong tag or multiple roots inside `render`

## Reference Map

- Full samples: `references/composition.md`
- Official docs: https://heroui.com/en/docs/react/getting-started/composition
- Raw MDX: https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(handbook)/composition.mdx
- Related handbook: Styling, Animation; Components catalog
- Sibling skills: `heroui-design-principles`, `heroui-react`, `heroui-frameworks`, `heroui-cli`
