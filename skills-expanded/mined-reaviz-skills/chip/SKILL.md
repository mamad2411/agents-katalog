# Chip

Compact element for tags, filters, labels, or selections. Supports colors, variants, sizes, adornments, and interactive states (clickable, selectable). Uses `forwardRef` and keyboard accessibility (Enter/Space).

## Import

```tsx
import { Chip, DeletableChip } from 'reablocks';
```

## Chip Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | `'default' \| 'primary' \| 'secondary' \| 'success' \| 'warning' \| 'error' \| 'info' \| string` | `'default'` | Color variant |
| `variant` | `'filled' \| 'outline' \| string` | `'filled'` | Style variant |
| `size` | `'small' \| 'medium' \| 'large' \| string` | `'medium'` | Size variant |
| `selected` | `boolean` | — | Selected state (applies the variant's `selected` styles when clickable) |
| `disabled` | `boolean` | — | Disabled state |
| `disableMargins` | `boolean` | — | Remove default margins |
| `start` | `ReactElement \| string` | — | Content before the label |
| `end` | `ReactElement \| string` | — | Content after the label |
| `theme` | `ChipTheme` | — | Per-instance theme override |
| `className` | `string` | — | Additional CSS classes |

Also accepts all standard `HTMLDivElement` attributes including `onClick`. Children are wrapped in a `<div>` styled by `theme.label`.

## Basic Usage

```tsx
<Chip color="primary">Label</Chip>
```

## Variants

```tsx
<Chip variant="filled">Filled</Chip>
<Chip variant="outline">Outline</Chip>
```

## Colors

All seven colors work with every variant:

```tsx
<Chip color="default">Default</Chip>
<Chip color="primary">Primary</Chip>
<Chip color="secondary">Secondary</Chip>
<Chip color="success">Success</Chip>
<Chip color="warning">Warning</Chip>
<Chip color="error">Error</Chip>
<Chip color="info">Info</Chip>
```

## Sizes

```tsx
<Chip size="small">Small</Chip>
<Chip size="medium">Medium</Chip>
<Chip size="large">Large</Chip>
```

## Adornments

Use `start` and `end` to add icons or text before/after the label. Adornment containers are sized via `theme.adornment.sizes[size]`:

```tsx
<Chip start={<StarIcon />}>With Icon</Chip>
<Chip end={<ArrowIcon />}>With End</Chip>
<Chip start="$" end={<CloseIcon />}>Both</Chip>
```

## Clickable

When `onClick` is provided, the chip becomes a button: `role="button"`, `tabIndex={0}`, and `Enter`/`Space` keyboard handling. The color's `selectable` styles (hover + selected) apply only when `onClick` is present.

```tsx
<Chip variant="outline" onClick={() => handleClick()}>
  Clickable
</Chip>
```

## Selected State

```tsx
<Chip
  variant="outline"
  color="primary"
  selected={isSelected}
  onClick={() => setIsSelected(!isSelected)}
>
  Toggle Me
</Chip>
```

## DeletableChip

`DeletableChip` is a wrapper that injects a delete button into the `end` slot. It accepts all `ChipProps` except `end`.

```tsx
import { DeletableChip } from 'reablocks';

<DeletableChip
  variant="filled"
  color="success"
  onDelete={() => removeItem(id)}
>
  Removable
</DeletableChip>
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `onDelete` | `() => void` | — | Called when the delete icon is clicked |
| `deleteIcon` | `ReactElement` | `<CloseIcon />` | Custom delete icon |

The delete button styles come from `theme.deleteButton.base` + `theme.deleteButton[size]`.

## ChipTheme Interface

```typescript
interface ThemeColor {
  base?: string;
  variants?: {
    filled?: string;
    outline?: string;
    [key: string]: string;
  };
  selectable?: {
    base?: string;                  // Applied on hover when clickable (e.g. cursor-pointer)
    variants?: {
      filled?:  { base?: string; selected?: string };
      outline?: { base?: string; selected?: string };
      [key: string]: { base?: string; selected?: string };
    };
  };
}

interface ChipTheme {
  base: string;                     // Inline-flex container, transitions, font
  label: string;                    // Inner wrapper around children (flex items-center)
  focus: string;                    // focus-visible ring/outline
  disabled: string;                 // Disabled state (opacity, cursor)
  adornment: {
    base: string;                   // Adornment container (flex)
    start: string;                  // Start adornment spacing
    end: string;                    // End adornment spacing
    sizes: {
      small: string;                // Icon sizing per chip size
      medium: string;
      large: string;
      [key: string]: string;
    };
  };
  variants: {
    filled: string;
    outline: string;
    [key: string]: string;
  };
  colors: {
    default?: ThemeColor;
    primary?: ThemeColor;
    secondary?: ThemeColor;
    success?: ThemeColor;
    warning?: ThemeColor;
    error?: ThemeColor;
    info?: ThemeColor;
    [key: string]: ThemeColor;
  };
  sizes: {
    small: string;
    medium: string;
    large: string;
    [key: string]: string;
  };
  deleteButton: {                   // Used by DeletableChip's injected close button
    base: string;
    sizes: { small: string; medium: string; large: string; [key: string]: string };
  };
}
```

`theme.label` styles the children wrapper — customize it (font weight, color, padding) without touching `theme.base`.
