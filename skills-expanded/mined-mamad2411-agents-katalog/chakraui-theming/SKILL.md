---
name: chakraui-theming
description: Customize Chakra UI v3 theme, tokens, and design system. Use when the user wants to customize the theme, create design tokens, semantic tokens, component recipes, slot recipes, or modify colors/spacing/typography at the theme level. Triggers for "customize theme", "change colors", "create design tokens", "override component styles", "add brand colors", "define custom components", or when working with createSystem, defineConfig, or theme configuration files.
---

# Chakra UI v3 Theming Skill

## Quick Reference

### Core Architecture
- **defineConfig**: Define the system configuration
- **createSystem**: Create the styling engine from config
- **defaultConfig**: Built-in tokens and recipes (merge with this)
- **defaultBaseConfig**: Conditions and style properties only (start from scratch)

### Basic Setup
```tsx
import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react"

const config = defineConfig({
  theme: {
    tokens: { colors: {}, spacing: {} },
    semanticTokens: { colors: {} },
    recipes: {},
    slotRecipes: {},
  },
})

export const system = createSystem(defaultConfig, config)
```

### Token Definition
```tsx
tokens: {
  colors: {
    brand: {
      50: { value: "#e6f2ff" },
      500: { value: "#3b82f6" },
      950: { value: "#001a33" },
    },
  },
  spacing: {
    gutter: { value: "12px" },
  },
}
```

### Semantic Token Definition
```tsx
semanticTokens: {
  colors: {
    danger: { 
      value: { base: "{colors.red.500}", _dark: "{colors.red.300}" } 
    },
    bg: {
      DEFAULT: { value: "{colors.white}" },
      subtle: { value: "{colors.gray.50}" },
    },
  },
}
```

### Color Palette for colorPalette prop
```tsx
semanticTokens: {
  colors: {
    brand: {
      solid: { value: "{colors.brand.500}" },
      contrast: { value: "{colors.white}" },
      fg: { value: "{colors.brand.700}" },
      muted: { value: "{colors.brand.100}" },
      subtle: { value: "{colors.brand.200}" },
      emphasized: { value: "{colors.brand.300}" },
      focusRing: { value: "{colors.brand.500}" },
    },
  },
}
```

### Recipe Definition
```tsx
import { defineRecipe } from "@chakra-ui/react"

const buttonRecipe = defineRecipe({
  base: { display: "flex" },
  variants: {
    variant: {
      solid: { bg: "blue.500", color: "white" },
      outline: { borderWidth: "1px", borderColor: "blue.500" },
    },
    size: {
      sm: { padding: "2", fontSize: "sm" },
      lg: { padding: "4", fontSize: "lg" },
    },
  },
  defaultVariants: { variant: "solid", size: "sm" },
})
```

### Slot Recipe Definition
```tsx
import { defineSlotRecipe } from "@chakra-ui/react"

const checkboxSlotRecipe = defineSlotRecipe({
  slots: ["root", "control", "label"],
  base: {
    root: { display: "flex", alignItems: "center", gap: "2" },
    control: { borderWidth: "1px", borderRadius: "sm" },
    label: { marginStart: "2" },
  },
  variants: {
    size: {
      sm: { control: { width: "4", height: "4" }, label: { fontSize: "sm" } },
      md: { control: { width: "5", height: "5" }, label: { fontSize: "md" } },
    },
  },
})
```

### Config Options
| Option | Description |
|--------|-------------|
| `cssVarsRoot` | Root element for CSS variables (default: `:where(:root, :host)`) |
| `cssVarsPrefix` | Prefix for CSS variables (default: `chakra`) |
| `globalCss` | Global styles to apply |
| `preflight` | CSS reset (true/false or `{ scope: ".selector" }`) |
| `strictTokens` | Enforce token-only values (throws TS error for raw values) |
| `conditions` | Custom selectors and media query conditions |
| `theme` | Theme configuration (tokens, recipes, etc.) |

### Theme Properties
| Property | Description |
|----------|-------------|
| `breakpoints` | Responsive breakpoints |
| `keyframes` | CSS animation keyframes |
| `tokens` | Design tokens (colors, spacing, fonts, etc.) |
| `semanticTokens` | Context-aware tokens (light/dark mode) |
| `textStyles` | Typography style presets |
| `layerStyles` | Layer/container style presets |
| `animationStyles` | Animation style presets |
| `recipes` | Single-slot component recipes |
| `slotRecipes` | Multi-slot component recipes |

## Common Theming Patterns

### Custom Brand Colors
```tsx
const config = defineConfig({
  theme: {
    tokens: {
      colors: {
        brand: {
          50: { value: "#eff6ff" },
          100: { value: "#dbeafe" },
          200: { value: "#bfdbfe" },
          300: { value: "#93c5fd" },
          400: { value: "#60a5fa" },
          500: { value: "#3b82f6" },
          600: { value: "#2563eb" },
          700: { value: "#1d4ed8" },
          800: { value: "#1e40af" },
          900: { value: "#1e3a8a" },
          950: { value: "#172554" },
        },
      },
    },
    semanticTokens: {
      colors: {
        brand: {
          solid: { value: "{colors.brand.500}" },
          contrast: { value: "{colors.white}" },
          fg: { value: "{colors.brand.700}" },
          muted: { value: "{colors.brand.100}" },
          subtle: { value: "{colors.brand.50}" },
          emphasized: { value: "{colors.brand.200}" },
          focusRing: { value: "{colors.brand.500}" },
        },
      },
    },
  },
})
```

### Extending Component Variants
```tsx
const buttonRecipe = defineRecipe({
  variants: {
    size: {
      xl: { fontSize: "lg", px: "6", py: "3" },
    },
    variant: {
      ghost: { bg: "transparent", _hover: { bg: "gray.100" } },
    },
  },
})
```

### Custom Animations
```tsx
const config = defineConfig({
  theme: {
    keyframes: {
      shakeX: {
        "0%, 100%": { transform: "translateX(-100%)" },
        "50%": { transform: "translateX(100%)" },
      },
    },
    tokens: {
      animations: {
        shakeX: { value: "shakeX 1s ease-in-out infinite" },
      },
    },
  },
})
```

### Global Font Family
```tsx
const config = defineConfig({
  globalCss: {
    html: {
      fontFamily: "Inter, sans-serif",
    },
  },
})
// OR
const config = defineConfig({
  theme: {
    tokens: {
      fonts: {
        body: { value: "Inter, sans-serif" },
        heading: { value: "Poppins, sans-serif" },
        mono: { value: "Fira Code, monospace" },
      },
    },
  },
})
```

## Best Practices

1. **Use semantic tokens** for colors that adapt to color mode (light/dark)
2. **Create color palettes** for use with `colorPalette` prop (solid, contrast, fg, muted, subtle, emphasized, focusRing)
3. **Extend defaultConfig** rather than starting from scratch unless necessary
4. **Run typegen** after theme changes: `npx @chakra-ui/cli typegen ./theme.ts`
5. **Use token reference syntax** for composite values: `border="1px solid {colors.red.300}"`
6. **Define DEFAULT** for nested tokens to allow shorthand usage

## Detailed References

- **[tokens.md](references/tokens.md)** - Design tokens (colors, spacing, sizes, typography, shadows, etc.)
- **[semantic-tokens.md](references/semantic-tokens.md)** - Semantic tokens, conditional tokens, color palettes
- **[recipes.md](references/recipes.md)** - Component recipes, variants, compound variants
- **[slot-recipes.md](references/slot-recipes.md)** - Multi-slot recipes, compound components
- **[customization.md](references/customization.md)** - Theme configuration, conditions, utilities

## Full Reference

- **[llms-theming.txt](references/llms-theming.txt)** - Full reference of all Theming "very large File 3300+ lines".
