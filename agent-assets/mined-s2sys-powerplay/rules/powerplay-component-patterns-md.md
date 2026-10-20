---
name: component-patterns
description: Component library patterns — Material Design, Chakra UI, Tailwind CSS component patterns and theming
globs: ["**/*.tsx", "**/*.jsx", "**/*.ts", "**/*.js", "**/*.css", "**/*.scss"]
alwaysApply: false
---

# Component Library Patterns

UI component libraries provide pre-built, accessible, tested components. Master Material Design, Chakra UI, and Tailwind CSS patterns to build consistent, maintainable interfaces.

---

## Material Design Components

**ALWAYS**:
- Use Material Design 3 principles (elevation, typography hierarchy, color system)
- Implement ripple effects for touch feedback
- Maintain 8dp spacing grid (8, 16, 24, 32, 48, 56px)
- Use semantic color tokens (primary, secondary, error, warning, info, success)
- Support light and dark themes with @material/mdc-web or Material-UI

**NEVER**:
- Mix Material with other design systems (consistency breaks)
- Customize Material components beyond theme variables
- Ignore Material accessibility guidelines (WCAG AA minimum)
- Create custom buttons when Material Button exists

### ✅ GOOD Material Design Pattern

```typescript
// Material-UI (React) with theme customization
import { createTheme, ThemeProvider, Button, Card, CardContent, Typography } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: {
      main: '#0066cc',
      light: '#e6f2ff',
      dark: '#004099',
    },
    secondary: {
      main: '#f59e0b',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
    ].join(','),
    h1: { fontSize: '3.5rem', fontWeight: 700 },
    h2: { fontSize: '2.2rem', fontWeight: 700 },
    body1: { fontSize: '1rem', lineHeight: 1.5 },
  },
  spacing: 8, // 8dp grid
  shape: {
    borderRadius: 4, // Material border radius
  },
});

export function MyComponent() {
  return (
    <ThemeProvider theme={theme}>
      <Card elevation={1}>
        <CardContent>
          <Typography variant="h2" component="h2">
            Heading
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {}}
            sx={{ mt: 2 }}
          >
            Click me
          </Button>
        </CardContent>
      </Card>
    </ThemeProvider>
  );
}
```

### ❌ BAD Material Pattern

```typescript
// ❌ Mixing Material with custom styles
const Button = styled.button`
  background: #0066cc;  /* Custom color, not theme */
  padding: 10px;        /* Not on 8dp grid */
  border-radius: 6px;   /* Not Material shape */
`;

// ❌ Creating custom card when Material Card exists
const CustomCard = styled.div`
  background: white;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;
```

---

## Chakra UI Patterns

**ALWAYS**:
- Use Chakra's design tokens (colors, typography, spacing, sizes)
- Build with Box, Flex, Grid for layout (never raw divs)
- Use semantic components (Button, Input, Modal, Drawer, Tabs)
- Customize via theme extension (not inline styles)
- Support responsive design with array/object syntax: `[mobileSize, tabletSize, desktopSize]`

**NEVER**:
- Mix Chakra with Tailwind or Material
- Use inline style objects instead of Chakra's sx prop
- Ignore Chakra's color mode (light/dark) system
- Create custom wrappers for built-in components

### ✅ GOOD Chakra UI Pattern

```typescript
// Chakra UI (React)
import {
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  Heading,
  Stack,
  useColorMode,
  extendTheme,
  ChakraProvider,
} from '@chakra-ui/react';

const theme = extendTheme({
  colors: {
    brand: {
      50: '#e6f2ff',
      500: '#0066cc',
      900: '#004099',
    },
  },
  fonts: {
    body: `'Segoe UI', Roboto, sans-serif`,
    heading: `'Segoe UI', Roboto, sans-serif`,
  },
});

export function MyComponent() {
  const { colorMode } = useColorMode();
  
  return (
    <ChakraProvider theme={theme}>
      <Card>
        <CardHeader>
          <Heading size="md">Title</Heading>
        </CardHeader>
        <CardBody>
          <Stack spacing={4}>
            <Box
              p={[2, 4, 6]}  /* Responsive padding: mobile, tablet, desktop */
              bg={colorMode === 'light' ? 'white' : 'gray.800'}
            >
              Content
            </Box>
            <Button colorScheme="brand">Action</Button>
          </Stack>
        </CardBody>
      </Card>
    </ChakraProvider>
  );
}
```

### ❌ BAD Chakra Pattern

```typescript
// ❌ Ignoring Chakra's responsive syntax
<Box style={{ padding: '20px', backgroundColor: '#fff' }}>
  Content
</Box>

// ❌ Creating custom button instead of using Chakra Button
const CustomButton = styled.button`
  background: #0066cc;
  padding: 12px 24px;
`;

// ❌ Not using Chakra theme
<Box bg="#0066cc" p="20px">
  {/* Magic colors, not theme tokens */}
</Box>
```

---

## Tailwind CSS Patterns

**ALWAYS**:
- Use utility classes exclusively (never inline styles)
- Configure custom tokens in tailwind.config.js (colors, spacing, fonts)
- Use CSS-in-JS (Tailwind + @apply) for complex components
- Support dark mode with dark: prefix
- Use responsive prefixes: sm:, md:, lg:, xl:, 2xl:
- Configure content paths correctly for JIT compilation

**NEVER**:
- Mix Tailwind with CSS-in-JS styled-components
- Use arbitrary values when tokens exist
- Hardcode colors (use theme tokens)
- Ignore dark mode support

### ✅ GOOD Tailwind CSS Pattern

```typescript
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6f2ff',
          500: '#0066cc',
          900: '#004099',
        },
        success: '#10b981',
        danger: '#ef4444',
      },
      spacing: {
        xs: '4px',
        sm: '8px',
        base: '16px',
        lg: '24px',
      },
      fontFamily: {
        base: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
    },
  },
  darkMode: 'class',
  plugins: [],
};

// Component with Tailwind
export function Card({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return (
    <div
      className={`
        bg-white dark:bg-gray-900
        rounded-lg shadow-md
        p-6
        border border-gray-200 dark:border-gray-700
        ${className}
      `}
    >
      {children}
    </div>
  );
}

// Usage: responsive, dark-mode aware
export function MyComponent() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 py-8 px-4 sm:px-6 lg:px-8">
      <Card className="max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Title
        </h2>
        <button
          className={`
            px-6 py-3
            bg-primary-500 hover:bg-primary-600 active:bg-primary-700
            text-white font-semibold rounded-lg
            focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
            dark:focus:ring-offset-gray-900
            transition-colors duration-200
            disabled:opacity-50 disabled:cursor-not-allowed
          `}
        >
          Click me
        </button>
      </Card>
    </div>
  );
}
```

### ❌ BAD Tailwind Pattern

```typescript
// ❌ Inline styles instead of Tailwind
<div style={{ padding: '20px', backgroundColor: '#0066cc' }}>
  Content
</div>

// ❌ Arbitrary colors instead of theme tokens
<button className="bg-[#0066cc] text-white">
  {/* Should use bg-primary-500 */}
</button>

// ❌ Not using responsive prefixes
<div className="p-20 text-2xl">
  {/* Same padding/text on all screen sizes */}
</div>

// ❌ Missing dark mode
<div className="bg-white text-black">
  {/* No dark: variant */}
</div>
```

---

## Component API Design

**ALWAYS**:
- Accept typed props: `ComponentProps<'button'>` extends
- Provide size variants: sm, md, lg (don't accept arbitrary sizes)
- Provide color/intent variants: primary, secondary, danger, success, warning
- Support disabled, loading, error states
- Forward refs for access to underlying DOM element
- Document prop types with JSDoc or TypeScript generics

**NEVER**:
- Accept style prop (use className or CSS variables)
- Create props that duplicate library props
- Leave ref behavior inconsistent

### ✅ GOOD Component API

```typescript
import { forwardRef, ComponentPropsWithoutRef } from 'react';

type ButtonSize = 'sm' | 'md' | 'lg';
type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost';

interface ButtonProps extends ComponentPropsWithoutRef<'button'> {
  /** Visual variant */
  variant?: ButtonVariant;
  /** Size preset */
  size?: ButtonSize;
  /** Loading state (disables button) */
  isLoading?: boolean;
  /** Error message shown below button */
  error?: string;
  /** Full width button */
  fullWidth?: boolean;
  /** Icon to show left of text */
  icon?: React.ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      error,
      fullWidth = false,
      icon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    };

    const variantClasses = {
      primary: 'bg-primary-500 text-white hover:bg-primary-600',
      secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 dark:bg-gray-800',
      danger: 'bg-red-500 text-white hover:bg-red-600',
      ghost: 'bg-transparent text-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900',
    };

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        <button
          ref={ref}
          disabled={disabled || isLoading}
          className={`
            inline-flex items-center gap-2
            font-semibold rounded-lg
            transition-colors duration-200
            focus:outline-none focus:ring-2 focus:ring-offset-2
            disabled:opacity-50 disabled:cursor-not-allowed
            ${sizeClasses[size]}
            ${variantClasses[variant]}
            ${fullWidth ? 'w-full justify-center' : ''}
          `}
          {...props}
        >
          {isLoading && <Spinner size={size} />}
          {icon && !isLoading && icon}
          {children}
        </button>
        {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
      </div>
    );
  }
);

Button.displayName = 'Button';
```

---

## Theme Customization

**ALWAYS**:
- Define all colors, typography, spacing in theme config
- Use CSS variables or design tokens (never hardcoded values)
- Support light and dark themes consistently
- Document all theme tokens
- Allow theme override at app root

**NEVER**:
- Hardcode colors in components
- Create multiple theme files (single source of truth)
- Use arbitrary values for spacing/sizes

### ✅ GOOD Theme Setup

```typescript
// themes/tokens.ts
export const tokens = {
  colors: {
    primary: '#0066cc',
    secondary: '#f59e0b',
    danger: '#ef4444',
    success: '#10b981',
    
    // Semantic colors
    text: {
      primary: '#111827',
      secondary: '#6b7280',
      muted: '#9ca3af',
    },
    bg: {
      primary: '#ffffff',
      secondary: '#f9fafb',
      tertiary: '#f3f4f6',
    },
  },
  spacing: [4, 8, 12, 16, 24, 32, 48, 64],
  typography: {
    fontFamily: {
      base: 'system-ui, -apple-system, sans-serif',
      mono: 'Monaco, Menlo, monospace',
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.25rem',
      xl: '1.5rem',
    },
  },
};

// App.tsx with theme provider
import { ThemeProvider } from './context/ThemeContext';

export function App() {
  return (
    <ThemeProvider tokens={tokens}>
      <Main />
    </ThemeProvider>
  );
}
```

---

## Component Library Checklist

- [ ] Material Design 3, Chakra UI, or Tailwind CSS chosen
- [ ] Theme tokens defined (colors, typography, spacing)
- [ ] Light and dark mode support
- [ ] All components typed with TypeScript
- [ ] Component props documented
- [ ] Size and variant presets defined
- [ ] Accessibility checked (WCAG AA)
- [ ] Responsive behavior tested (mobile, tablet, desktop)
- [ ] Error/loading/disabled states implemented
- [ ] Icons library integrated
- [ ] Documentation/Storybook setup
- [ ] Consistent naming convention

---

## Summary

Good component libraries:
1. **Consistent** — Single design system (Material, Chakra, or Tailwind)
2. **Themed** — Design tokens, light/dark modes
3. **Typed** — Full TypeScript support
4. **Accessible** — WCAG AA compliance built-in
5. **Responsive** — Mobile-first, all breakpoints
6. **Documented** — Clear prop APIs, usage examples

Choose one library and master its patterns for consistency.
