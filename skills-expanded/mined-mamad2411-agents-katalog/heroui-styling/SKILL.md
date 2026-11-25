---
name: heroui-styling
description: >
  Style HeroUI v3 components with className, inline style, BEM classes, data-state
  attributes, render-prop dynamic classes, Tailwind utilities, CSS Modules, CSS-in-JS
  (styled-components, Emotion), tailwind-variants wrappers, and scrollbar utilities
  from @heroui/styles. Keywords: HeroUI styling, BEM, button--primary, className
  render prop, scrollbar-thin, @layer components, CSS Modules. Use when the user
  runs /heroui-styling.
---

# HeroUI Styling (v3)

Flexible styling for HeroUI components: Tailwind utilities, BEM / data attributes, CSS-in-JS, and render props for dynamic styles.

**Source:** https://heroui.com/en/docs/react/getting-started/styling  
**Raw MDX:** https://raw.githubusercontent.com/heroui-inc/heroui/refs/heads/v3/apps/docs/content/docs/en/react/getting-started/(handbook)/styling.mdx

## Apply the Skill

- Read `references/styling.md` for full samples (wrappers, Emotion, CSS Modules).
- Prefer **semantic variants + theme tokens** over one-off colors when possible (`heroui-design-principles`).
- For polymorphic / foreign hosts (`buttonVariants`, BEM on Next Link), also use `heroui-composition-patterns`.
- For enter/exit and `data-pressed` motion, also use `heroui-animation-and-transitions`.
- For CSS variables / theme tokens / scrollbar modes, see Theming docs (and future `heroui-theming` if present).

## Non-Negotiables

| Do | Don't |
|----|--------|
| Use `className` (and optional `style`) on all components | Assume only BEM works or only Tailwind works |
| Style states with **data attributes** (`data-hovered`, `data-pressed`, …) | Rely solely on `:hover` when React Aria state attrs exist |
| Global overrides in `@layer components` with BEM | Fight specificity with unlayered `!important` soup |
| Scroll utilities from HeroUI (`scrollbar`, `scrollbar-thin`, …) on custom overflow | Invent ad-hoc scrollbar CSS that ignores `--scrollbar-*` tokens |
| Extend with `tv({ extend: buttonVariants })` for wrappers | Fork component source for simple visual variants |
| Check per-component CSS class docs for complete BEM maps | Guess element names (`__trigger` vs `__button`) |

## Work in This Order

1. **Defaults** — Semantic `variant` / `size` props first.
2. **Local tweak** — `className` Tailwind utilities (or `style` for one-offs).
3. **State** — Data attributes or `className={({ isPressed }) => …}` / children render props.
4. **Global skin** — BEM under `@layer components` or theme variables.
5. **Reusable product API** — `tv` extend + typed wrapper component.
6. **Scoped / CSS-in-JS** — CSS Modules, styled-components, Emotion when the stack requires it.

## Decision Rules

### Basic surfaces

```tsx
<Button className="bg-purple-500 hover:bg-purple-600">Custom Button</Button>
<Button style={{ backgroundColor: "#8B5CF6" }}>Styled Button</Button>
```

### Scrollbars (`@heroui/styles`)

HeroUI scroll slots use `@apply scrollbar`. On your own overflow containers:

| Utility | Effect |
|---------|--------|
| `scrollbar` | HeroUI thumb (`--scrollbar-*` theme vars) |
| `scrollbar-thin` | Themed thin scrollbar |
| `scrollbar-default` | OS / browser scrollbars |
| `scrollbar-none` | Hidden |

Subtree mode: `data-scrollbar` on an ancestor — details in Theming docs.

```tsx
<div className="scrollbar h-64 overflow-y-auto">{/* long content */}</div>
```

### State-based styling

```css
.button[data-hovered="true"],
.button:hover {
  background: var(--accent-hover);
}

.button[data-pressed="true"],
.button:active {
  transform: scale(0.97);
}

.button[data-focus-visible="true"],
.button:focus-visible {
  outline: 2px solid var(--focus);
}
```

### Render props

```tsx
// Dynamic classes
<Button className={({ isPressed }) => (isPressed ? "bg-blue-600" : "bg-blue-500")}>
  Press me
</Button>

// Dynamic content + classes
<Button>
  {({ isHovered, isPressed }) => (
    <>
      <Icon
        icon="gravity-ui:heart"
        className={isPressed ? "text-red-500" : "text-neutral-400"}
      />
      <span className={isHovered ? "underline" : ""}>Like</span>
    </>
  )}
</Button>
```

### BEM

| Kind | Pattern | Examples |
|------|---------|----------|
| Block | `.block` | `.button`, `.accordion` |
| Element | `.block__element` | `.accordion__trigger`, `.accordion__panel` |
| Modifier | `.block--mod` | `.button--primary`, `.button--lg`, `.accordion--outline` |

Global customization:

```css
@layer components {
  .button {
    @apply font-semibold uppercase;
  }
  .button--primary {
    @apply bg-indigo-600 hover:bg-indigo-700;
  }
  .button--gradient {
    @apply bg-gradient-to-r from-purple-500 to-pink-500;
  }
}
```

### Wrapper components (`tv` extend)

```tsx
import { Button as HeroButton, type ButtonProps } from "@heroui/react";
import { buttonVariants, tv, type VariantProps } from "@heroui/styles";

const customButtonVariants = tv({
  extend: buttonVariants,
  base: "font-medium transition-all",
  variants: {
    intent: {
      primary: "bg-blue-500 hover:bg-blue-600 text-white",
      secondary: "bg-gray-200 hover:bg-gray-300",
      danger: "bg-red-500 hover:bg-red-600 text-white",
    },
    size: {
      small: "text-sm px-2 py-1",
      medium: "text-base px-4 py-2",
      large: "text-lg px-6 py-3",
    },
  },
  defaultVariants: { intent: "primary", size: "medium" },
});
```

Type with `VariantProps` + `Omit<ButtonProps, "className">` + optional `className`.

### CSS-in-JS / CSS Modules / responsive

- **styled-components:** `styled(Button)\`…\``
- **Emotion:** `css\`…\`` → `className={buttonStyles}`
- **CSS Modules:** `styles.button` from `*.module.css`
- **Responsive:** Tailwind breakpoints (`md:`, `lg:`) or media queries on BEM blocks

### Component class cheatsheet

| Component | Classes (partial) |
|-----------|-------------------|
| **Button** | `.button`, `.button--{variant}`, `.button--{size}`, `.button--icon-only` |
| **Accordion** | `.accordion`, `.accordion__item`, `.accordion__trigger`, `.accordion__panel`, `.accordion--outline` |

Full maps: component docs (CSS Classes sections) and [`@heroui/styles/components`](https://github.com/heroui-inc/heroui/tree/main/packages/styles/components).

## Anti-Patterns

- Hardcoding brand colors everywhere instead of tokens / semantic variants
- Overriding without `@layer components` (order fights Tailwind)
- Ignoring data attributes for hover/press/focus-visible
- Building custom scrollbars that break theme `--scrollbar-*` tokens
- Using CSS Modules BEM names that diverge from HeroUI’s real class names when targeting slots

## Reference Map

- Full samples: `references/styling.md`
- Official: https://heroui.com/en/docs/react/getting-started/styling
- Related: Animation, Theming, Components
- Sibling skills: `heroui-composition-patterns`, `heroui-animation-and-transitions`, `heroui-design-principles`, `heroui-react`
