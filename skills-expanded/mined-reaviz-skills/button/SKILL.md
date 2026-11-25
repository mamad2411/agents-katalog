# Button

A versatile action trigger component built on Framer Motion with support for variants, colors, sizes, icons, and full theme customization.

## Import

```tsx
import { Button, ButtonGroup } from 'reablocks';
```

## Button Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | `'default' \| 'primary' \| 'secondary' \| 'success' \| 'warning' \| 'error' \| string` | `'default'` | Color variation |
| `variant` | `'filled' \| 'outline' \| 'text' \| string` | `'filled'` | Style variant |
| `size` | `'small' \| 'medium' \| 'large' \| string` | `'medium'` | Size variation |
| `fullWidth` | `boolean` | `false` | Take full width of container |
| `disabled` | `boolean` | `false` | Disable the button |
| `disableAnimation` | `boolean` | `false` | Disable the press animation (Framer Motion `whileTap` scale) |
| `start` | `ReactNode` | — | Element before button content (e.g. icon) |
| `end` | `ReactNode` | — | Element after button content (e.g. icon) |
| `disableMargins` | `boolean` | `false` | Remove margins |
| `disablePadding` | `boolean` | `false` | Remove padding |
| `theme` | `ButtonTheme` | — | Per-instance theme override |
| `className` | `string` | — | Additional CSS classes (merged last, highest priority) |
| `type` | `string` | `'button'` | HTML button type attribute |

Also accepts all standard `HTMLButtonElement` attributes (except Framer Motion drag handlers, which are stripped).

The rendered `<motion.button>` carries a `data-variant` attribute (set to the active variant — group variant takes precedence) so theme classes can target disabled/variant combinations via `data-variant=...` selectors.

## Basic Usage

```tsx
<Button color="primary">Click Me</Button>
```

## Variants

Three built-in style variants:

```tsx
<Button variant="filled" color="primary">Filled</Button>
<Button variant="outline" color="primary">Outline</Button>
<Button variant="text" color="primary">Text</Button>
```

- **filled** — solid background with hover state
- **outline** — border only, no background fill
- **text** — text only, no border or background

Custom variants can be registered through theme extension and used as strings.

## Colors

Six built-in colors, each rendered per-variant:

```tsx
<Button color="default">Default</Button>
<Button color="primary">Primary</Button>
<Button color="secondary">Secondary</Button>
<Button color="success">Success</Button>
<Button color="warning">Warning</Button>
<Button color="error">Error</Button>
```

Use `color="error"` for destructive actions.

## Sizes

```tsx
<Button color="primary" size="small">Small</Button>
<Button color="primary" size="medium">Medium</Button>
<Button color="primary" size="large">Large</Button>
```

## With Icons

Use `start` and `end` props to add icons. Adornment containers are sized automatically by `theme.adornment.sizes[size]`.

```tsx
<Button size="medium" start={<SearchIcon />}>Search</Button>
<Button size="medium" end={<ArrowRightIcon />}>Next</Button>
<Button size="large" start={<PlusIcon />} end={<ChevronIcon />}>Add Item</Button>
```

Icon sizing per size: small = `w-3 h-3`, medium = `w-4 h-4`, large = `w-5 h-5`.

## Full Width

```tsx
<Button color="primary" fullWidth>Full Width Button</Button>
```

## Disabled

Disabled buttons get reduced opacity and `cursor-not-allowed`. The `whileTap` animation is automatically suppressed.

```tsx
<Button disabled color="primary" variant="filled">Disabled Filled</Button>
<Button disabled color="primary" variant="outline">Disabled Outline</Button>
```

## Theme Customization

### Custom Color

```tsx
import { ThemeProvider, theme, extendTheme, PartialReablocksTheme } from 'reablocks';

const customTheme: PartialReablocksTheme = {
  components: {
    button: {
      colors: {
        gradient: {
          filled: 'bg-linear-to-r from-blue-500 to-purple-500 text-white',
          outline: 'border border-blue-500 text-blue-500',
          text: 'text-blue-500'
        }
      }
    }
  }
};

<ThemeProvider theme={extendTheme(theme, customTheme)}>
  <Button color="gradient">Gradient</Button>
</ThemeProvider>
```

### Custom Variant

```tsx
const customTheme: PartialReablocksTheme = {
  components: {
    button: {
      variants: {
        gradient: 'border rounded-lg'
      },
      colors: {
        primary: {
          gradient: 'bg-linear-to-r from-blue-500 to-purple-500 border-blue-500'
        },
        secondary: {
          gradient: 'bg-linear-to-r from-pink-500 to-purple-500 border-pink-500'
        }
      }
    }
  }
};

<ThemeProvider theme={extendTheme(theme, customTheme)}>
  <Button variant="gradient" color="primary">Gradient Primary</Button>
</ThemeProvider>
```

### Custom Size

```tsx
const customTheme: PartialReablocksTheme = {
  components: {
    button: {
      sizes: {
        xsmall: 'text-xxs px-1 py-0.5',
        xlarge: 'text-xl px-6 py-3'
      }
    }
  }
};
```

### Merging Classes

```tsx
import { extendTheme, mergeThemeClasses, theme } from 'reablocks';

<ThemeProvider theme={extendTheme(theme, customTheme, mergeThemeClasses)}>
  ...
</ThemeProvider>
```

## ButtonTheme Interface

```typescript
interface ButtonTheme {
  base: string;            // Base classes for all buttons
  disabled: string;        // Disabled state (uses data-variant attr selectors)
  fullWidth: string;       // Full-width classes
  group: string;           // Classes when inside ButtonGroup
  groupText: string;       // Classes when inside ButtonGroup with variant="text"
  variants: {              // Per-variant base classes
    filled: string;
    outline: string;
    text: string;
    [key: string]: string; // extensible
  };
  colors: {                // Per-color, per-variant classes
    default:   { filled, outline, text, [key: string]: string };
    primary:   { filled, outline, text, [key: string]: string };
    secondary: { filled, outline, text, [key: string]: string };
    success:   { filled, outline, text, [key: string]: string };
    warning:   { filled, outline, text, [key: string]: string };
    error:     { filled, outline, text, [key: string]: string };
    [key: string]: { filled, outline, text, [key: string]: string };
  };
  sizes: {                 // Per-size classes
    small: string;
    medium: string;
    large: string;
    [key: string]: string;
  };
  iconSizes: {             // Padding presets for icon-only buttons
    small: string;
    medium: string;
    large: string;
    [key: string]: string;
  };
  adornment: {             // Icon adornment configuration
    base: string;
    start: string;         // Start spacing
    end: string;           // End spacing
    sizes: {               // Icon dimensions per size
      small: string;
      medium: string;
      large: string;
      [key: string]: string;
    };
  };
}
```

---

# ButtonGroup

Groups multiple buttons together with shared variant and size. Buttons inside a group have their border-radius adjusted (first gets left radius, last gets right radius).

## ButtonGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'filled' \| 'outline' \| 'text' \| string` | `'filled'` | Shared variant for all child buttons |
| `size` | `'small' \| 'medium' \| 'large' \| string` | `'medium'` | Shared size for all child buttons |
| `children` | `ReactNode` | — | Button elements to group |
| `className` | `string` | — | Additional CSS classes for the group wrapper |

`variant` and `size` are typed as `string` so any custom variant/size registered in the button theme works inside a group.

## ButtonGroup Usage

```tsx
<ButtonGroup variant="filled">
  <Button>One</Button>
  <Button>Two</Button>
  <Button>Three</Button>
</ButtonGroup>
```

### Variants in Groups

```tsx
<ButtonGroup variant="outline">
  <Button>A</Button>
  <Button>B</Button>
  <Button>C</Button>
</ButtonGroup>

<ButtonGroup variant="text">
  <Button>A</Button>
  <Button>B</Button>
  <Button>C</Button>
</ButtonGroup>
```

### Group Sizes

```tsx
<ButtonGroup size="small">
  <Button>S1</Button>
  <Button>S2</Button>
</ButtonGroup>

<ButtonGroup size="large">
  <Button>L1</Button>
  <Button>L2</Button>
</ButtonGroup>
```

**Note:** When a Button is inside a ButtonGroup, the group's `variant` and `size` override the individual button's props. The ButtonGroup uses React Context (`ButtonGroupContext`, exported `ButtonGroupContextProps`) to propagate these values.
