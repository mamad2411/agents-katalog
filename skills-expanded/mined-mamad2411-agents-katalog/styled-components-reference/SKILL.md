---
description: Comprehensive Styled Components v6+ quick reference - themes, patterns, animations, TypeScript, SSR, and performance
---

# Styled Components v6+ Quick Reference

Complete reference library for Styled Components patterns, theming, animations, TypeScript integration, and best practices.

## Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Basic Component Patterns](#basic-component-patterns)
3. [Theme System](#theme-system)
4. [Component Composition](#component-composition)
5. [Responsive Design](#responsive-design)
6. [Animation Library](#animation-library)
7. [TypeScript Patterns](#typescript-patterns)
8. [Performance Optimization](#performance-optimization)
9. [SSR Configuration](#ssr-configuration)
10. [Best Practices](#best-practices)

---

## Installation & Setup

### Package Installation

```bash
# Install styled-components and TypeScript types
npm install styled-components
npm install -D @types/styled-components

# For SSR support
npm install babel-plugin-styled-components
```

### Basic Setup

```typescript
// App.tsx
import { ThemeProvider } from 'styled-components';
import { lightTheme } from './theme';
import GlobalStyles from './GlobalStyles';

const App = () => (
  <ThemeProvider theme={lightTheme}>
    <GlobalStyles />
    {/* Your app components */}
  </ThemeProvider>
);
```

---

## Basic Component Patterns

### Simple Styled Component

```typescript
import styled from 'styled-components';

const Button = styled.button`
  padding: 12px 24px;
  background-color: ${({ theme }) => theme.colors.primary};
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;
```

### Component with Props

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  fullWidth?: boolean;
}

const Button = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  /* Size variants */
  ${({ size = 'medium' }) => {
    switch (size) {
      case 'small':
        return `padding: 8px 16px; font-size: 14px;`;
      case 'large':
        return `padding: 16px 32px; font-size: 18px;`;
      default:
        return `padding: 12px 24px; font-size: 16px;`;
    }
  }}

  /* Variant colors */
  ${({ variant = 'primary', theme }) => {
    switch (variant) {
      case 'secondary':
        return `
          background-color: ${theme.colors.secondary};
          &:hover { background-color: ${theme.colors.secondaryHover}; }
        `;
      case 'danger':
        return `
          background-color: ${theme.colors.danger};
          &:hover { background-color: ${theme.colors.dangerHover}; }
        `;
      default:
        return `
          background-color: ${theme.colors.primary};
          &:hover { background-color: ${theme.colors.primaryHover}; }
        `;
    }
  }}

  /* Full width */
  width: ${({ fullWidth }) => (fullWidth ? '100%' : 'auto')};
`;
```

### Transient Props (v5.1+)

```typescript
// Use $ prefix for props that shouldn't be passed to DOM
interface ButtonProps {
  $isActive?: boolean;
}

const Button = styled.button<ButtonProps>`
  background: ${({ $isActive }) => ($isActive ? 'blue' : 'gray')};
`;

// Usage: <Button $isActive={true} />
```

---

## Theme System

### Complete Theme Interface

```typescript
export interface Theme {
  colors: {
    primary: string;
    primaryHover: string;
    primaryActive: string;
    secondary: string;
    secondaryHover: string;
    secondaryActive: string;
    success: string;
    warning: string;
    danger: string;
    info: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
    border: string;
    divider: string;
  };
  typography: {
    fontFamily: {
      primary: string;
      secondary: string;
      monospace: string;
    };
    fontSize: {
      xs: string;
      sm: string;
      base: string;
      lg: string;
      xl: string;
      '2xl': string;
      '3xl': string;
      '4xl': string;
    };
    fontWeight: {
      light: number;
      normal: number;
      medium: number;
      semibold: number;
      bold: number;
    };
    lineHeight: {
      tight: number;
      normal: number;
      relaxed: number;
      loose: number;
    };
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    '2xl': string;
    '3xl': string;
    '4xl': string;
  };
  breakpoints: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    '2xl': string;
  };
  shadows: {
    none: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    '2xl': string;
  };
  animations: {
    duration: {
      fast: string;
      normal: string;
      slow: string;
    };
    easing: {
      easeIn: string;
      easeOut: string;
      easeInOut: string;
      linear: string;
    };
  };
  borderRadius: {
    none: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    full: string;
  };
  zIndex: {
    dropdown: number;
    sticky: number;
    fixed: number;
    modal: number;
    popover: number;
    tooltip: number;
  };
}
```

### Light Theme Example

```typescript
export const lightTheme: Theme = {
  colors: {
    primary: '#007bff',
    primaryHover: '#0056b3',
    primaryActive: '#004085',
    secondary: '#6c757d',
    secondaryHover: '#5a6268',
    secondaryActive: '#545b62',
    success: '#28a745',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#17a2b8',
    background: '#ffffff',
    surface: '#f8f9fa',
    text: '#212529',
    textSecondary: '#6c757d',
    border: '#dee2e6',
    divider: '#e9ecef',
  },
  typography: {
    fontFamily: {
      primary: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      secondary: 'Georgia, "Times New Roman", Times, serif',
      monospace: '"Fira Code", "Courier New", Courier, monospace',
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
    },
    fontWeight: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
      loose: 2,
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
    '3xl': '4rem',
    '4xl': '6rem',
  },
  breakpoints: {
    xs: '320px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
  shadows: {
    none: 'none',
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
  },
  animations: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
    },
    easing: {
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      linear: 'linear',
    },
  },
  borderRadius: {
    none: '0',
    sm: '0.25rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
    full: '9999px',
  },
  zIndex: {
    dropdown: 1000,
    sticky: 1020,
    fixed: 1030,
    modal: 1040,
    popover: 1050,
    tooltip: 1060,
  },
};
```

### Dark Theme Example

```typescript
export const darkTheme: Theme = {
  ...lightTheme,
  colors: {
    primary: '#0d6efd',
    primaryHover: '#0a58ca',
    primaryActive: '#084298',
    secondary: '#adb5bd',
    secondaryHover: '#8a9199',
    secondaryActive: '#6c757d',
    success: '#198754',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#0dcaf0',
    background: '#0d1117',
    surface: '#161b22',
    text: '#e6edf3',
    textSecondary: '#8b949e',
    border: '#30363d',
    divider: '#21262d',
  },
};
```

### TypeScript Theme Extension

```typescript
// styled.d.ts
import 'styled-components';
import { Theme } from './theme';

declare module 'styled-components' {
  export interface DefaultTheme extends Theme {}
}
```

### Global Styles

```typescript
import { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html {
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  body {
    font-family: ${({ theme }) => theme.typography.fontFamily.primary};
    font-size: ${({ theme }) => theme.typography.fontSize.base};
    line-height: ${({ theme }) => theme.typography.lineHeight.normal};
    color: ${({ theme }) => theme.colors.text};
    background-color: ${({ theme }) => theme.colors.background};
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  h1, h2, h3, h4, h5, h6 {
    font-weight: ${({ theme }) => theme.typography.fontWeight.bold};
    line-height: ${({ theme }) => theme.typography.lineHeight.tight};
    color: ${({ theme }) => theme.colors.text};
  }

  a {
    color: ${({ theme }) => theme.colors.primary};
    text-decoration: none;
    transition: color 0.2s;

    &:hover {
      color: ${({ theme }) => theme.colors.primaryHover};
      text-decoration: underline;
    }
  }

  code {
    font-family: ${({ theme }) => theme.typography.fontFamily.monospace};
    background-color: ${({ theme }) => theme.colors.surface};
    padding: 2px 6px;
    border-radius: 4px;
  }

  ::selection {
    background-color: ${({ theme }) => theme.colors.primary};
    color: white;
  }
`;

export default GlobalStyles;
```

---

## Component Composition

### Extending Components

```typescript
// Base button
const BaseButton = styled.button`
  display: inline-flex;
  align-items: center;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
`;

// Primary button extends base
const PrimaryButton = styled(BaseButton)`
  background-color: ${({ theme }) => theme.colors.primary};
  color: white;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primaryHover};
  }
`;

// Outline button extends base
const OutlineButton = styled(BaseButton)`
  background-color: transparent;
  color: ${({ theme }) => theme.colors.primary};
  border: 2px solid ${({ theme }) => theme.colors.primary};

  &:hover {
    background-color: ${({ theme }) => theme.colors.primary};
    color: white;
  }
`;
```

### Polymorphic Components

```typescript
interface TextProps {
  as?: 'p' | 'span' | 'div' | 'label';
  variant?: 'body' | 'caption' | 'overline';
}

const Text = styled.p<TextProps>`
  margin: 0;

  ${({ variant = 'body', theme }) => {
    switch (variant) {
      case 'caption':
        return `font-size: ${theme.typography.fontSize.sm};`;
      case 'overline':
        return `
          font-size: ${theme.typography.fontSize.xs};
          text-transform: uppercase;
          letter-spacing: 0.1em;
        `;
      default:
        return `font-size: ${theme.typography.fontSize.base};`;
    }
  }}
`;

// Usage: <Text as="span" variant="caption">Text</Text>
```

### Using attrs

```typescript
const Input = styled.input.attrs<{ $size?: 'small' | 'large' }>(props => ({
  type: 'text',
  placeholder: props.$size === 'small' ? 'Small' : 'Large',
}))<{ $size?: 'small' | 'large' }>`
  padding: ${({ $size }) => ($size === 'small' ? '4px' : '12px')};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius.md};
`;
```

---

## Responsive Design

### Media Query Helpers

```typescript
import { css } from 'styled-components';

export const media = {
  up: (breakpoint: keyof Theme['breakpoints']) => (styles: string) => css`
    @media (min-width: ${({ theme }) => theme.breakpoints[breakpoint]}) {
      ${styles}
    }
  `,

  down: (breakpoint: keyof Theme['breakpoints']) => (styles: string) => css`
    @media (max-width: ${({ theme }) => theme.breakpoints[breakpoint]}) {
      ${styles}
    }
  `,

  between: (
    min: keyof Theme['breakpoints'],
    max: keyof Theme['breakpoints']
  ) => (styles: string) => css`
    @media (min-width: ${({ theme }) => theme.breakpoints[min]}) and
           (max-width: ${({ theme }) => theme.breakpoints[max]}) {
      ${styles}
    }
  `,
};
```

### Responsive Grid

```typescript
interface GridProps {
  columns?: number;
  gap?: keyof Theme['spacing'];
}

const Grid = styled.div<GridProps>`
  display: grid;
  gap: ${({ theme, gap = 'md' }) => theme.spacing[gap]};

  /* Mobile: 1 column */
  grid-template-columns: 1fr;

  /* Tablet: 2 columns */
  @media (min-width: ${({ theme }) => theme.breakpoints.md}) {
    grid-template-columns: repeat(2, 1fr);
  }

  /* Desktop: Full columns */
  @media (min-width: ${({ theme }) => theme.breakpoints.lg}) {
    grid-template-columns: repeat(${({ columns = 3 }) => columns}, 1fr);
  }
`;
```

### Responsive Card

```typescript
const Card = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border: 1px solid ${({ theme }) => theme.colors.border};
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing.md};

  @media (min-width: ${({ theme }) => theme.breakpoints.md}) {
    padding: ${({ theme }) => theme.spacing.lg};
  }

  @media (min-width: ${({ theme }) => theme.breakpoints.lg}) {
    padding: ${({ theme }) => theme.spacing.xl};
  }
`;
```

---

## Animation Library

### Keyframe Animations

```typescript
import { keyframes } from 'styled-components';

// Fade in
export const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

// Slide in from bottom
export const slideInUp = keyframes`
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
`;

// Slide in from top
export const slideInDown = keyframes`
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
`;

// Scale in
export const scaleIn = keyframes`
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
`;

// Rotate
export const rotate = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

// Pulse
export const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

// Bounce
export const bounce = keyframes`
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
`;

// Shimmer (for skeleton loaders)
export const shimmer = keyframes`
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
`;
```

### Animated Components

```typescript
import { css } from 'styled-components';

interface AnimatedContainerProps {
  animation?: 'fadeIn' | 'slideInUp' | 'slideInDown' | 'scaleIn';
  duration?: string;
  delay?: string;
}

const AnimatedContainer = styled.div<AnimatedContainerProps>`
  ${({ animation = 'fadeIn', duration = '0.3s', delay = '0s', theme }) => {
    let anim = fadeIn;

    switch (animation) {
      case 'slideInUp':
        anim = slideInUp;
        break;
      case 'slideInDown':
        anim = slideInDown;
        break;
      case 'scaleIn':
        anim = scaleIn;
        break;
    }

    return css`
      animation: ${anim} ${duration} ${theme.animations.easing.easeOut} ${delay} both;
    `;
  }}
`;
```

### Loading Spinner

```typescript
const Spinner = styled.div`
  width: 40px;
  height: 40px;
  border: 4px solid ${({ theme }) => theme.colors.border};
  border-top-color: ${({ theme }) => theme.colors.primary};
  border-radius: 50%;
  animation: ${rotate} 1s linear infinite;
`;
```

### Skeleton Loader

```typescript
interface SkeletonProps {
  width?: string;
  height?: string;
}

const Skeleton = styled.div<SkeletonProps>`
  width: ${({ width = '100%' }) => width};
  height: ${({ height = '20px' }) => height};
  border-radius: 4px;
  background: linear-gradient(
    90deg,
    ${({ theme }) => theme.colors.surface} 0%,
    ${({ theme }) => theme.colors.border} 50%,
    ${({ theme }) => theme.colors.surface} 100%
  );
  background-size: 1000px 100%;
  animation: ${shimmer} 2s infinite linear;
`;
```

---

## TypeScript Patterns

### Generic Components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  gap?: keyof Theme['spacing'];
}

const StyledList = styled.ul<{ gap: keyof Theme['spacing'] }>`
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: ${({ theme, gap }) => theme.spacing[gap]};
`;

function List<T>({ items, renderItem, gap = 'md' }: ListProps<T>) {
  return (
    <StyledList gap={gap}>
      {items.map((item, index) => (
        <li key={index}>{renderItem(item, index)}</li>
      ))}
    </StyledList>
  );
}
```

### Type-Safe Theme Utilities

```typescript
import { DefaultTheme } from 'styled-components';

export const spacing = (key: keyof DefaultTheme['spacing']) => {
  return ({ theme }: { theme: DefaultTheme }) => theme.spacing[key];
};

export const color = (key: keyof DefaultTheme['colors']) => {
  return ({ theme }: { theme: DefaultTheme }) => theme.colors[key];
};

export const fontSize = (key: keyof DefaultTheme['typography']['fontSize']) => {
  return ({ theme }: { theme: DefaultTheme }) => theme.typography.fontSize[key];
};

// Usage
const Component = styled.div`
  padding: ${spacing('lg')};
  color: ${color('primary')};
  font-size: ${fontSize('xl')};
`;
```

---

## Performance Optimization

### Do's

```typescript
// ✅ GOOD: Create component once
const GoodDiv = styled.div<{ color: string }>`
  color: ${({ color }) => color};
`;

const GoodComponent = ({ color }: { color: string }) => {
  return <GoodDiv color={color}>Text</GoodDiv>;
};

// ✅ BETTER: Use predefined variants
const variants = {
  primary: css`color: ${({ theme }) => theme.colors.primary};`,
  secondary: css`color: ${({ theme }) => theme.colors.secondary};`,
};

const BestDiv = styled.div<{ variant: 'primary' | 'secondary' }>`
  ${({ variant }) => variants[variant]}
`;
```

### Don'ts

```typescript
// ❌ BAD: Creating component in render
const BadComponent = ({ color }: { color: string }) => {
  const DynamicDiv = styled.div`
    color: ${color};
  `;
  return <DynamicDiv>Text</DynamicDiv>; // New component every render!
};
```

### Memoization

```typescript
import { memo, useMemo } from 'react';

const OptimizedComponent = memo<Props>(({ items, onItemClick }) => {
  const sortedItems = useMemo(() => {
    return [...items].sort();
  }, [items]);

  return (
    <Container>
      {sortedItems.map(item => (
        <Item key={item} onClick={() => onItemClick(item)}>
          {item}
        </Item>
      ))}
    </Container>
  );
});

OptimizedComponent.displayName = 'OptimizedComponent';
```

### Code Splitting

```typescript
import { lazy, Suspense } from 'react';
import { Skeleton } from './components';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

const App = () => (
  <Suspense fallback={<Skeleton height="200px" />}>
    <HeavyComponent />
  </Suspense>
);
```

---

## SSR Configuration

### Next.js App Router (13+)

```typescript
// app/registry.tsx
'use client';

import React, { useState } from 'react';
import { useServerInsertedHTML } from 'next/navigation';
import { ServerStyleSheet, StyleSheetManager } from 'styled-components';

export default function StyledComponentsRegistry({
  children,
}: {
  children: React.ReactNode;
}) {
  const [styledComponentsStyleSheet] = useState(() => new ServerStyleSheet());

  useServerInsertedHTML(() => {
    const styles = styledComponentsStyleSheet.getStyleElement();
    styledComponentsStyleSheet.instance.clearTag();
    return <>{styles}</>;
  });

  if (typeof window !== 'undefined') return <>{children}</>;

  return (
    <StyleSheetManager sheet={styledComponentsStyleSheet.instance}>
      {children}
    </StyleSheetManager>
  );
}
```

```typescript
// app/layout.tsx
import StyledComponentsRegistry from './registry';
import { ThemeProvider } from 'styled-components';
import { lightTheme } from './theme';
import GlobalStyles from './GlobalStyles';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <StyledComponentsRegistry>
          <ThemeProvider theme={lightTheme}>
            <GlobalStyles />
            {children}
          </ThemeProvider>
        </StyledComponentsRegistry>
      </body>
    </html>
  );
}
```

### Next.js Pages Router

```typescript
// pages/_document.tsx
import Document, { DocumentContext, Html, Head, Main, NextScript } from 'next/document';
import { ServerStyleSheet } from 'styled-components';

export default class MyDocument extends Document {
  static async getInitialProps(ctx: DocumentContext) {
    const sheet = new ServerStyleSheet();
    const originalRenderPage = ctx.renderPage;

    try {
      ctx.renderPage = () =>
        originalRenderPage({
          enhanceApp: (App) => (props) =>
            sheet.collectStyles(<App {...props} />),
        });

      const initialProps = await Document.getInitialProps(ctx);

      return {
        ...initialProps,
        styles: (
          <>
            {initialProps.styles}
            {sheet.getStyleElement()}
          </>
        ),
      };
    } finally {
      sheet.seal();
    }
  }

  render() {
    return (
      <Html>
        <Head />
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
```

### Babel Configuration

```json
{
  "presets": ["next/babel"],
  "plugins": [
    [
      "babel-plugin-styled-components",
      {
        "ssr": true,
        "displayName": true,
        "fileName": true,
        "minify": true,
        "transpileTemplateLiterals": true,
        "pure": true
      }
    ]
  ]
}
```

---

## Best Practices

### Naming Conventions

```typescript
// ✅ DO: Semantic names
const ArticleHeader = styled.header``;
const NavigationLink = styled.a``;

// ❌ DON'T: Generic names
const Div1 = styled.div``;
const StyledComponent = styled.div``;
```

### Transient Props

```typescript
// ✅ DO: Use $ prefix for style-only props
interface ButtonProps {
  $isActive?: boolean;
}

const Button = styled.button<ButtonProps>`
  background: ${({ $isActive }) => ($isActive ? 'blue' : 'gray')};
`;

// ❌ DON'T: Pass non-standard props to DOM
const BadButton = styled.button<{ isActive?: boolean }>`
  background: ${({ isActive }) => (isActive ? 'blue' : 'gray')};
`;
// React warning: Unknown prop 'isActive'
```

### Theme Usage

```typescript
// ✅ DO: Use theme values
const ThemedButton = styled.button`
  color: ${({ theme }) => theme.colors.primary};
  padding: ${({ theme }) => theme.spacing.md};
`;

// ❌ DON'T: Hardcode values
const HardcodedButton = styled.button`
  color: #007bff;
  padding: 16px;
`;
```

### Component Location

```typescript
// ✅ DO: Define outside render
const Container = styled.div``;

const MyComponent = () => {
  return <Container>Content</Container>;
};

// ❌ DON'T: Create in render
const BadComponent = () => {
  const Container = styled.div``; // Created every render!
  return <Container>Content</Container>;
};
```

### Reusable Styles

```typescript
// ✅ DO: Use css helper for snippets
const truncateText = css`
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
`;

const TruncatedText = styled.p`
  ${truncateText}
  max-width: 200px;
`;
```

---

## Common Component Patterns

### Container

```typescript
const Container = styled.div<{ maxWidth?: string }>`
  max-width: ${({ maxWidth = '1200px' }) => maxWidth};
  margin: 0 auto;
  padding: 0 ${({ theme }) => theme.spacing.lg};
`;
```

### Flex Container

```typescript
interface FlexProps {
  direction?: 'row' | 'column';
  justify?: 'flex-start' | 'center' | 'space-between' | 'space-around';
  align?: 'flex-start' | 'center' | 'flex-end' | 'stretch';
  gap?: keyof Theme['spacing'];
}

const Flex = styled.div<FlexProps>`
  display: flex;
  flex-direction: ${({ direction = 'row' }) => direction};
  justify-content: ${({ justify = 'flex-start' }) => justify};
  align-items: ${({ align = 'stretch' }) => align};
  gap: ${({ theme, gap = 'md' }) => theme.spacing[gap]};
`;
```

### Modal Overlay

```typescript
const Overlay = styled.div<{ $isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: ${({ $isOpen }) => ($isOpen ? 'flex' : 'none')};
  align-items: center;
  justify-content: center;
  z-index: ${({ theme }) => theme.zIndex.modal};
  animation: ${fadeIn} 0.2s ease-out;
`;

const Modal = styled.div`
  background: ${({ theme }) => theme.colors.surface};
  border-radius: ${({ theme }) => theme.borderRadius.lg};
  padding: ${({ theme }) => theme.spacing.xl};
  max-width: 500px;
  width: 90%;
  box-shadow: ${({ theme }) => theme.shadows['2xl']};
  animation: ${scaleIn} 0.2s ease-out;
`;
```

### Badge

```typescript
interface BadgeProps {
  variant?: 'success' | 'warning' | 'danger' | 'info';
}

const Badge = styled.span<BadgeProps>`
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: ${({ theme }) => theme.borderRadius.full};
  font-size: ${({ theme }) => theme.typography.fontSize.xs};
  font-weight: ${({ theme }) => theme.typography.fontWeight.semibold};
  text-transform: uppercase;

  ${({ variant = 'info', theme }) => {
    const colors = {
      success: theme.colors.success,
      warning: theme.colors.warning,
      danger: theme.colors.danger,
      info: theme.colors.info,
    };

    return `
      background-color: ${colors[variant]};
      color: white;
    `;
  }}
`;
```

---

## Quick Reference Checklist

### Setup Checklist
- [ ] Install styled-components and types
- [ ] Create theme files (light/dark)
- [ ] Extend TypeScript DefaultTheme
- [ ] Create GlobalStyles component
- [ ] Setup ThemeProvider
- [ ] Configure SSR (if using Next.js)

### Component Checklist
- [ ] Use transient props ($prefix) for style-only props
- [ ] Define components outside render functions
- [ ] Use theme values instead of hardcoded
- [ ] Add proper TypeScript typing
- [ ] Include focus states for accessibility
- [ ] Implement responsive breakpoints
- [ ] Add transitions for interactive elements

### Performance Checklist
- [ ] Memoize expensive computations
- [ ] Use React.memo for components
- [ ] Use predefined variants instead of dynamic styles
- [ ] Lazy load heavy components
- [ ] Minimize styled component re-creation

### Accessibility Checklist
- [ ] Add focus-visible styles
- [ ] Include ARIA labels
- [ ] Ensure proper contrast ratios
- [ ] Support keyboard navigation
- [ ] Add disabled state styling

This reference covers the essential patterns and best practices for Styled Components v6+. Use it as a quick lookup for common tasks and patterns.
