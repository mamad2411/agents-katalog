# Navigation

Navigation system with two components: **NavigationBar** (container) and **NavigationButton** (items). Supports vertical/horizontal layout, animated active indicators, and `start`/`end` slot props for non-button content.

## Import

```tsx
import { NavigationBar, NavigationButton } from 'reablocks';
```

## NavigationBar Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `direction` | `'vertical' \| 'horizontal'` | `'vertical'` | Layout direction |
| `start` | `ReactNode` | — | Content rendered in the start slot (top for vertical, left for horizontal) |
| `end` | `ReactNode` | — | Content rendered in the end slot (bottom for vertical, right for horizontal) |
| `children` | `ReactNode` | — | `NavigationButton` items rendered in the main navigation area |
| `className` | `string` | — | Class names for the outer `<nav>` element |
| `classNameStart` | `string` | — | Class names for the start slot wrapper |
| `classNameNavigation` | `string` | — | Class names for the main navigation area |
| `classNameEnd` | `string` | — | Class names for the end slot wrapper |
| `theme` | `NavigationTheme` | — | Per-instance theme override |

The outer element is a `<nav>` with `role="navigation"`.

## NavigationButton Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'ghost' \| 'underline'` | `'ghost'` | Button style variant |
| `active` | `boolean` | — | Active state — animates a layout-id selection indicator |
| `animated` | `boolean` | `true` | Disable Framer Motion layout animation when `false` |
| `animationLayoutId` | `string` | `'selected-nav-button'` | Custom `layoutId` to scope the active indicator (use a unique id when multiple navs are mounted) |
| `disabled` | `boolean` | — | Disabled state |
| `onClick` | `() => void` | — | Click handler |
| `className` | `string` | — | Additional CSS classes for the inner button |
| `theme` | `NavigationTheme` | — | Per-instance theme override |
| `children` | `ReactNode` | — | Button content (icon + label) |

## Vertical Navigation (Default)

```tsx
<NavigationBar
  direction="vertical"
  start={<Logo />}
  end={<UserMenu />}
>
  <NavigationButton active onClick={() => navigate('/')}>
    <HomeIcon /> Home
  </NavigationButton>
  <NavigationButton onClick={() => navigate('/settings')}>
    <SettingsIcon /> Settings
  </NavigationButton>
</NavigationBar>
```

## Horizontal Navigation

```tsx
<NavigationBar direction="horizontal">
  <NavigationButton variant="underline" active>Home</NavigationButton>
  <NavigationButton variant="underline">About</NavigationButton>
  <NavigationButton variant="underline">Contact</NavigationButton>
</NavigationBar>
```

## Scoping the active indicator

When multiple `NavigationBar`s are on the same page, set `animationLayoutId` so the active highlight does not animate across instances:

```tsx
<NavigationBar>
  <NavigationButton active animationLayoutId="primary-nav">Home</NavigationButton>
  <NavigationButton animationLayoutId="primary-nav">Docs</NavigationButton>
</NavigationBar>
```

## Button Variants

- **ghost** — Background highlight on hover/active, rounded selection indicator behind the content
- **underline** — Bottom border indicator on active, no background

Variants are extensible — add new keys via theme customization, then pass `variant="myVariant"`.

## NavigationTheme Interface

```typescript
interface NavigationButtonVariantConfigTheme {
  content: string;     // Button content styling
  active: string;      // Active state classes
  selection: string;   // Selection indicator (animated layoutId target)
  disabled: string;    // Disabled state classes
}

interface NavigationTheme {
  bar: {
    base: string;                                   // Outer nav (flex, padding, border, bg)
    direction: { horizontal: string; vertical: string };
    start: string;                                  // Start slot wrapper
    navigation: string;                             // Main nav area (flex-1, gap)
    end: string;                                    // End slot wrapper
  };
  button: {
    base: string;                                   // Wrapper around the motion button
    variant: {
      ghost: NavigationButtonVariantConfigTheme;
      underline: NavigationButtonVariantConfigTheme;
      [key: string]: NavigationButtonVariantConfigTheme;
    };
  };
}
```

The `variant` map is open — extend it through `extendTheme` to register custom variants.
