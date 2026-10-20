---
name: theme-patterns-reference
description: Comprehensive theme system patterns reference - design tokens, multi-brand, CSS variables, inheritance, and testing
searchable: true
tags: [theme, design-tokens, css-variables, multi-brand, theming, styled-components, accessibility]
---

# Theme System Patterns Reference

Complete reference for enterprise-grade theme systems with design tokens, multi-brand support, and dynamic theming.

## Table of Contents

1. [Design Token Architecture](#design-token-architecture)
2. [Theme Provider Patterns](#theme-provider-patterns)
3. [CSS Custom Properties](#css-custom-properties)
4. [Multi-Brand Systems](#multi-brand-systems)
5. [Theme Switching](#theme-switching)
6. [Theme Inheritance](#theme-inheritance)
7. [CSS-in-JS Integration](#css-in-js-integration)
8. [Theme Testing](#theme-testing)
9. [Best Practices](#best-practices)

---

## Design Token Architecture

### Three-Tier Token System

The foundation of scalable theming: **Primitives** → **Semantic** → **Component**

#### 1. Primitive Tokens (Base Values)

Raw, context-free values that form the foundation.

```typescript
/**
 * Primitive Color Tokens
 * @description Base color palette with 11-step scales
 */
interface ColorPrimitives {
  brand: {
    50: '#eff6ff';   // Lightest
    100: '#dbeafe';
    200: '#bfdbfe';
    300: '#93c5fd';
    400: '#60a5fa';
    500: '#3b82f6';  // Main brand color
    600: '#2563eb';
    700: '#1d4ed8';
    800: '#1e40af';
    900: '#1e3a8a';
    950: '#172554';  // Darkest
  };

  neutral: {
    0: '#ffffff';    // Pure white
    50: '#f9fafb';
    100: '#f3f4f6';
    200: '#e5e7eb';
    300: '#d1d5db';
    400: '#9ca3af';
    500: '#6b7280';
    600: '#4b5563';
    700: '#374151';
    800: '#1f2937';
    900: '#111827';
    950: '#030712';
    1000: '#000000'; // Pure black
  };

  // Feedback colors
  success: ColorScale;  // Green
  warning: ColorScale;  // Amber/Yellow
  error: ColorScale;    // Red
  info: ColorScale;     // Blue
}

/**
 * Primitive Spacing Tokens
 * @description Base spacing scale (8px grid)
 */
interface SpacingPrimitives {
  0: '0';
  1: '0.25rem';   // 4px
  2: '0.5rem';    // 8px
  3: '0.75rem';   // 12px
  4: '1rem';      // 16px
  5: '1.25rem';   // 20px
  6: '1.5rem';    // 24px
  8: '2rem';      // 32px
  10: '2.5rem';   // 40px
  12: '3rem';     // 48px
  16: '4rem';     // 64px
  20: '5rem';     // 80px
  24: '6rem';     // 96px
}

/**
 * Primitive Typography Tokens
 * @description Base typography scale
 */
interface TypographyPrimitives {
  fontFamily: {
    sans: 'Inter, system-ui, sans-serif';
    serif: 'Georgia, serif';
    mono: 'Fira Code, Consolas, monospace';
  };

  fontSize: {
    xs: '0.75rem';    // 12px
    sm: '0.875rem';   // 14px
    base: '1rem';     // 16px
    lg: '1.125rem';   // 18px
    xl: '1.25rem';    // 20px
    '2xl': '1.5rem';  // 24px
    '3xl': '1.875rem'; // 30px
    '4xl': '2.25rem'; // 36px
    '5xl': '3rem';    // 48px
  };

  fontWeight: {
    light: 300;
    normal: 400;
    medium: 500;
    semibold: 600;
    bold: 700;
    extrabold: 800;
  };

  lineHeight: {
    none: 1;
    tight: 1.25;
    snug: 1.375;
    normal: 1.5;
    relaxed: 1.625;
    loose: 2;
  };
}
```

#### 2. Semantic Tokens (Purpose-Driven)

Map primitives to meaningful purposes.

```typescript
/**
 * Semantic Color Tokens
 * @description Purpose-driven color mappings
 */
interface SemanticColors {
  // Background tokens
  background: {
    primary: 'neutral.0';      // Main background
    secondary: 'neutral.50';   // Subtle background
    tertiary: 'neutral.100';   // Card/panel background
    inverse: 'neutral.900';    // Dark mode background
    overlay: 'rgba(0,0,0,0.5)'; // Modal overlays
    elevated: 'neutral.0';     // Elevated surfaces (cards)
  };

  // Foreground tokens
  foreground: {
    primary: 'neutral.900';    // Primary text
    secondary: 'neutral.600';  // Secondary text
    tertiary: 'neutral.400';   // Tertiary/disabled text
    disabled: 'neutral.300';   // Disabled state
    inverse: 'neutral.0';      // Text on dark backgrounds
    brand: 'brand.600';        // Brand-colored text
  };

  // Border tokens
  border: {
    default: 'neutral.200';    // Default border
    subtle: 'neutral.100';     // Subtle divider
    strong: 'neutral.300';     // Strong border
    focus: 'brand.500';        // Focus ring
    error: 'error.500';        // Error state
  };

  // Interactive tokens
  interactive: {
    primary: {
      default: 'brand.500';
      hover: 'brand.600';
      active: 'brand.700';
      disabled: 'neutral.300';
      focus: 'brand.500';
      loading: 'neutral.400';
    };
    secondary: {
      default: 'neutral.600';
      hover: 'neutral.700';
      active: 'neutral.800';
      disabled: 'neutral.200';
      focus: 'neutral.600';
      loading: 'neutral.300';
    };
  };
}
```

#### 3. Component Tokens (Component-Specific)

Tokens for specific component needs.

```typescript
/**
 * Component Tokens
 * @description Component-specific token overrides
 */
interface ComponentTokens {
  button: {
    primary: {
      background: 'interactive.primary.default';
      backgroundHover: 'interactive.primary.hover';
      text: 'foreground.inverse';
      borderRadius: 'radii.base';
      paddingX: 'spacing.4';
      paddingY: 'spacing.2';
    };
    secondary: {
      background: 'background.secondary';
      border: 'border.default';
      text: 'foreground.primary';
    };
  };

  input: {
    background: 'background.primary';
    border: 'border.default';
    borderHover: 'border.strong';
    borderFocus: 'border.focus';
    text: 'foreground.primary';
    placeholder: 'foreground.tertiary';
    paddingX: 'spacing.3';
    paddingY: 'spacing.2';
    borderRadius: 'radii.sm';
  };

  card: {
    background: 'background.elevated';
    border: 'border.subtle';
    shadow: 'shadows.md';
    borderRadius: 'radii.lg';
    padding: 'spacing.6';
  };
}
```

---

## Theme Provider Patterns

### React Context Theme Provider

Complete theme management with React Context.

```typescript
/**
 * Theme Provider with Context
 * @description Manages theme state and provides utilities
 */
import React, { createContext, useContext, useState, useEffect, useMemo } from 'react';

interface ThemeContextValue {
  theme: Theme;
  setTheme: (theme: Theme | string) => void;
  toggleTheme: () => void;
  currentThemeName: string;
  availableThemes: string[];
  systemPreference: 'light' | 'dark' | null;
  resolveToken: (path: string) => any;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export const ThemeProvider: React.FC<{
  children: React.ReactNode;
  defaultTheme?: string;
  themes: Record<string, Theme>;
  persistPreference?: boolean;
  storageKey?: string;
}> = ({
  children,
  defaultTheme = 'light',
  themes,
  persistPreference = true,
  storageKey = 'app-theme',
}) => {
  const [currentThemeName, setCurrentThemeName] = useState(defaultTheme);
  const [systemPreference, setSystemPreference] = useState<'light' | 'dark' | null>(null);

  // Detect system color scheme preference
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      setSystemPreference(e.matches ? 'dark' : 'light');
    };

    setSystemPreference(mediaQuery.matches ? 'dark' : 'light');
    mediaQuery.addEventListener('change', handleChange);

    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  // Load persisted theme
  useEffect(() => {
    if (!persistPreference) return;

    const saved = localStorage.getItem(storageKey);
    if (saved && themes[saved]) {
      setCurrentThemeName(saved);
    }
  }, [persistPreference, storageKey, themes]);

  // Apply theme to DOM
  useEffect(() => {
    const theme = themes[currentThemeName];
    if (!theme) return;

    // Apply CSS custom properties
    const root = document.documentElement;
    Object.entries(generateCSSVariables(theme)).forEach(([key, value]) => {
      root.style.setProperty(key, value);
    });

    // Apply theme class
    document.body.className = document.body.className
      .replace(/theme-[\w-]+/g, '')
      .concat(` theme-${currentThemeName}`);

    // Persist preference
    if (persistPreference) {
      localStorage.setItem(storageKey, currentThemeName);
    }
  }, [currentThemeName, themes, persistPreference, storageKey]);

  const value = useMemo(
    () => ({
      theme: themes[currentThemeName],
      setTheme: (themeOrName: Theme | string) => {
        if (typeof themeOrName === 'string') {
          setCurrentThemeName(themeOrName);
        }
      },
      toggleTheme: () => {
        const themeNames = Object.keys(themes);
        const currentIndex = themeNames.indexOf(currentThemeName);
        const nextIndex = (currentIndex + 1) % themeNames.length;
        setCurrentThemeName(themeNames[nextIndex]);
      },
      currentThemeName,
      availableThemes: Object.keys(themes),
      systemPreference,
      resolveToken: (path: string) => {
        return path.split('.').reduce((obj, key) => obj?.[key], themes[currentThemeName]);
      },
    }),
    [themes, currentThemeName, systemPreference]
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

/**
 * useTheme Hook
 * @description Access theme context
 */
export const useTheme = (): ThemeContextValue => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};
```

---

## CSS Custom Properties

### Dynamic CSS Variable Management

Runtime CSS variable management system.

```typescript
/**
 * CSS Variable Manager
 * @description Runtime CSS custom property management
 */
class CSSVariableManager {
  private prefix: string;
  private root: HTMLElement;
  private cache: Map<string, string>;

  constructor(prefix = '--app') {
    this.prefix = prefix;
    this.root = document.documentElement;
    this.cache = new Map();
  }

  /**
   * Set CSS Variable
   */
  setVariable(name: string, value: string): void {
    const varName = name.startsWith('--') ? name : `${this.prefix}-${name}`;
    this.root.style.setProperty(varName, value);
    this.cache.set(varName, value);
  }

  /**
   * Set Multiple Variables
   */
  setVariables(variables: Record<string, string>): void {
    Object.entries(variables).forEach(([name, value]) => {
      this.setVariable(name, value);
    });
  }

  /**
   * Get CSS Variable
   */
  getVariable(name: string): string | null {
    const varName = name.startsWith('--') ? name : `${this.prefix}-${name}`;
    return this.cache.get(varName) ||
           getComputedStyle(this.root).getPropertyValue(varName).trim() ||
           null;
  }

  /**
   * Remove CSS Variable
   */
  removeVariable(name: string): void {
    const varName = name.startsWith('--') ? name : `${this.prefix}-${name}`;
    this.root.style.removeProperty(varName);
    this.cache.delete(varName);
  }

  /**
   * Export All Variables
   */
  exportVariables(): Record<string, string> {
    return Object.fromEntries(this.cache);
  }
}

/**
 * React Hook for CSS Variables
 */
export const useCSSVariable = (name: string, defaultValue?: string) => {
  const [value, setValue] = useState<string>(() => {
    const varName = `--${name}`;
    const computed = getComputedStyle(document.documentElement)
      .getPropertyValue(varName)
      .trim();
    return computed || defaultValue || '';
  });

  const updateValue = (newValue: string) => {
    document.documentElement.style.setProperty(`--${name}`, newValue);
    setValue(newValue);
  };

  return [value, updateValue] as const;
};
```

### Generate CSS Variables from Theme

```typescript
/**
 * Generate CSS Variables from Theme Object
 * @description Converts nested theme object to flat CSS variables
 */
function generateCSSVariables(
  theme: Theme,
  prefix = '--theme'
): Record<string, string> {
  const variables: Record<string, string> = {};

  const processTokens = (tokens: any, path: string[] = []) => {
    Object.entries(tokens).forEach(([key, value]) => {
      const currentPath = [...path, key];

      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        processTokens(value, currentPath);
      } else {
        const variableName = `${prefix}-${currentPath.join('-')}`;
        variables[variableName] = String(value);
      }
    });
  };

  processTokens(theme);
  return variables;
}

/**
 * Example Output:
 * {
 *   '--theme-colors-primary-500': '#3b82f6',
 *   '--theme-colors-primary-600': '#2563eb',
 *   '--theme-spacing-4': '1rem',
 *   '--theme-typography-fontSize-base': '1rem',
 *   ...
 * }
 */
```

---

## Multi-Brand Systems

### Brand Configuration Architecture

```typescript
/**
 * Brand Configuration
 * @description Complete brand identity and theme
 */
interface BrandConfig {
  id: string;
  name: string;
  theme: BrandTheme;
  assets: BrandAssets;
  metadata: {
    title: string;
    description: string;
    domain: string;
  };
}

interface BrandTheme {
  colors: {
    primary: ColorScale;
    secondary: ColorScale;
    accent: ColorScale;
    neutral: ColorScale;
  };
  typography: {
    fontFamilies: {
      heading: string;
      body: string;
      mono: string;
    };
    fontSizes: TypographyScale;
  };
  spacing: SpacingScale;
  components: ComponentOverrides;
}

interface BrandAssets {
  logo: {
    light: string;
    dark: string;
    mark: string;
    wordmark: string;
  };
  favicon: string;
  icons: Record<string, string>;
}

/**
 * Brand Manager
 * @description Manages multiple brand configurations
 */
class BrandManager {
  private brands: Map<string, BrandConfig>;
  private activeBrand: string | null;

  constructor() {
    this.brands = new Map();
    this.activeBrand = null;
  }

  /**
   * Register Brand
   */
  registerBrand(config: BrandConfig): void {
    this.brands.set(config.id, config);
  }

  /**
   * Activate Brand
   */
  activateBrand(brandId: string): void {
    const brand = this.brands.get(brandId);
    if (!brand) throw new Error(`Brand "${brandId}" not found`);

    this.activeBrand = brandId;
    this.applyBrandTheme(brand);
  }

  /**
   * Apply Brand Theme
   */
  private applyBrandTheme(brand: BrandConfig): void {
    // Apply CSS variables
    const cssVars = generateCSSVariables(brand.theme);
    Object.entries(cssVars).forEach(([key, value]) => {
      document.documentElement.style.setProperty(key, value);
    });

    // Apply brand class
    document.body.className = document.body.className
      .replace(/brand-[\w-]+/g, '')
      .concat(` brand-${brand.id}`);

    // Update meta tags
    const themeColorMeta = document.querySelector('meta[name="theme-color"]');
    if (themeColorMeta) {
      themeColorMeta.setAttribute('content', brand.theme.colors.primary[500]);
    }

    // Update favicon
    const favicon = document.querySelector('link[rel="icon"]');
    if (favicon) {
      favicon.setAttribute('href', brand.assets.favicon);
    }

    // Update title
    document.title = brand.metadata.title;
  }

  /**
   * Get Active Brand
   */
  getActiveBrand(): BrandConfig | null {
    return this.activeBrand ? this.brands.get(this.activeBrand) || null : null;
  }
}
```

---

## Theme Switching

### Smooth Theme Transitions

```typescript
/**
 * Theme Switcher with Transitions
 * @description Hot-swappable themes with smooth animations
 */
class ThemeSwitcher {
  private currentTheme: string;
  private themes: Map<string, Theme>;

  constructor(initialTheme = 'light') {
    this.currentTheme = initialTheme;
    this.themes = new Map();
  }

  /**
   * Switch Theme with Transition
   */
  async switchTheme(
    themeName: string,
    options: {
      duration?: number;
      easing?: string;
      beforeSwitch?: () => Promise<void>;
      afterSwitch?: () => Promise<void>;
    } = {}
  ): Promise<void> {
    const {
      duration = 300,
      easing = 'ease-in-out',
      beforeSwitch,
      afterSwitch,
    } = options;

    const nextTheme = this.themes.get(themeName);
    if (!nextTheme) throw new Error(`Theme "${themeName}" not found`);

    // Before switch hook
    if (beforeSwitch) await beforeSwitch();

    // Apply transition
    await this.applyTransition(
      this.themes.get(this.currentTheme)!,
      nextTheme,
      { duration, easing }
    );

    this.currentTheme = themeName;

    // After switch hook
    if (afterSwitch) await afterSwitch();
  }

  /**
   * Apply Theme Transition
   */
  private async applyTransition(
    fromTheme: Theme,
    toTheme: Theme,
    config: { duration: number; easing: string }
  ): Promise<void> {
    const { duration, easing } = config;

    // Create transition CSS
    const transitionCSS = `
      * {
        transition:
          color ${duration}ms ${easing},
          background-color ${duration}ms ${easing},
          border-color ${duration}ms ${easing},
          box-shadow ${duration}ms ${easing};
      }
    `;

    // Inject transition styles
    const styleElement = document.createElement('style');
    styleElement.textContent = transitionCSS;
    document.head.appendChild(styleElement);

    // Apply new theme
    this.applyThemeToDOM(toTheme);

    // Remove transition styles after animation
    await new Promise(resolve => setTimeout(resolve, duration));
    document.head.removeChild(styleElement);
  }

  /**
   * Apply Theme to DOM
   */
  private applyThemeToDOM(theme: Theme): void {
    const cssVars = generateCSSVariables(theme);
    Object.entries(cssVars).forEach(([key, value]) => {
      document.documentElement.style.setProperty(key, value);
    });
  }
}
```

### Transition Presets

```typescript
/**
 * Theme Transition Presets
 */
export const transitionPresets = {
  // Fade transition
  fade: {
    duration: 300,
    easing: 'ease-in-out',
    beforeSwitch: async () => {
      document.body.style.opacity = '0';
      await new Promise(r => setTimeout(r, 150));
    },
    afterSwitch: async () => {
      document.body.style.opacity = '1';
    },
  },

  // Slide transition
  slide: {
    duration: 400,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
    beforeSwitch: async () => {
      document.body.style.transform = 'translateX(-100%)';
      await new Promise(r => setTimeout(r, 200));
    },
    afterSwitch: async () => {
      document.body.style.transform = 'translateX(0)';
    },
  },

  // Morph transition
  morph: {
    duration: 500,
    easing: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    beforeSwitch: async () => {
      document.body.style.filter = 'blur(10px)';
      document.body.style.transform = 'scale(0.95)';
      await new Promise(r => setTimeout(r, 250));
    },
    afterSwitch: async () => {
      document.body.style.filter = 'blur(0)';
      document.body.style.transform = 'scale(1)';
    },
  },
};
```

---

## Theme Inheritance

### Theme Extending and Variants

```typescript
/**
 * Theme Inheritance System
 * @description Extend and compose themes
 */
class ThemeInheritance {
  private baseThemes: Map<string, Theme>;

  /**
   * Extend Theme
   * @description Create new theme extending from base
   */
  extendTheme(baseName: string, extensions: Partial<Theme>): Theme {
    const base = this.baseThemes.get(baseName);
    if (!base) throw new Error(`Base theme "${baseName}" not found`);

    return this.deepMerge(base, extensions);
  }

  /**
   * Deep Merge Objects
   */
  private deepMerge(target: any, source: any): any {
    const output = { ...target };

    Object.keys(source).forEach(key => {
      if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
        if (target[key]) {
          output[key] = this.deepMerge(target[key], source[key]);
        } else {
          output[key] = source[key];
        }
      } else {
        output[key] = source[key];
      }
    });

    return output;
  }
}

/**
 * Generate Theme Variants
 */
export class ThemeVariantGenerator {
  /**
   * Generate Dark Variant
   */
  static generateDarkVariant(lightTheme: Theme): Theme {
    return {
      ...lightTheme,
      colors: {
        ...lightTheme.colors,
        background: {
          primary: '#0a0a0a',
          secondary: '#1a1a1a',
          tertiary: '#2a2a2a',
          elevated: '#3a3a3a',
        },
        foreground: {
          primary: '#ffffff',
          secondary: '#e0e0e0',
          tertiary: '#a0a0a0',
          disabled: '#606060',
        },
      },
    };
  }

  /**
   * Generate Density Variants
   */
  static generateDensityVariants(baseTheme: Theme) {
    return {
      comfortable: {
        ...baseTheme,
        spacing: scaleSpacing(baseTheme.spacing, 1.25),
      },
      default: baseTheme,
      compact: {
        ...baseTheme,
        spacing: scaleSpacing(baseTheme.spacing, 0.875),
      },
      dense: {
        ...baseTheme,
        spacing: scaleSpacing(baseTheme.spacing, 0.75),
      },
    };
  }

  /**
   * Generate High Contrast Variant
   */
  static generateHighContrastVariant(baseTheme: Theme): Theme {
    return {
      ...baseTheme,
      colors: {
        ...baseTheme.colors,
        background: {
          primary: '#000000',
          secondary: '#000000',
        },
        foreground: {
          primary: '#ffffff',
          secondary: '#ffffff',
          tertiary: '#ffff00',
        },
        border: {
          default: '#ffffff',
          focus: '#00ffff',
        },
      },
    };
  }
}
```

---

## CSS-in-JS Integration

### Styled Components Theming

```typescript
/**
 * Styled Components Theme Integration
 */
import styled, { ThemeProvider, createGlobalStyle } from 'styled-components';

// Extend DefaultTheme
declare module 'styled-components' {
  export interface DefaultTheme {
    colors: ColorTokens;
    typography: TypographyTokens;
    spacing: SpacingScale;
    breakpoints: Breakpoints;
    shadows: ShadowScale;
  }
}

/**
 * Global Theme Styles
 */
export const GlobalThemeStyles = createGlobalStyle`
  :root {
    ${({ theme }) => css`
      ${Object.entries(theme.colors.primary).map(([key, value]) => `
        --color-primary-${key}: ${value};
      `).join('')}
    `}
  }

  body {
    font-family: ${({ theme }) => theme.typography.fonts.body};
    color: ${({ theme }) => theme.colors.foreground.primary};
    background-color: ${({ theme }) => theme.colors.background.primary};
  }
`;

/**
 * Themed Component Example
 */
export const ThemedButton = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: ${({ theme }) => theme.spacing[3]} ${({ theme }) => theme.spacing[4]};
  border-radius: ${({ theme }) => theme.radii.base};
  font-family: ${({ theme }) => theme.typography.fonts.body};

  ${({ variant = 'primary', theme }) => {
    if (variant === 'primary') {
      return css`
        background-color: ${theme.colors.interactive.primary.default};
        color: ${theme.colors.foreground.inverse};

        &:hover {
          background-color: ${theme.colors.interactive.primary.hover};
        }
      `;
    }
    return css`
      background-color: ${theme.colors.background.secondary};
      color: ${theme.colors.foreground.primary};
    `;
  }}
`;
```

---

## Theme Testing

### WCAG Contrast Validation

```typescript
/**
 * Theme Contrast Checker
 * @description Validate WCAG contrast ratios
 */
export class ThemeContrastChecker {
  /**
   * Check Contrast Ratio
   */
  static checkContrast(foreground: string, background: string): {
    ratio: number;
    aa: boolean;         // WCAG AA (4.5:1)
    aaa: boolean;        // WCAG AAA (7:1)
    largeAA: boolean;    // Large text AA (3:1)
    largeAAA: boolean;   // Large text AAA (4.5:1)
  } {
    const ratio = this.getContrastRatio(foreground, background);

    return {
      ratio,
      aa: ratio >= 4.5,
      aaa: ratio >= 7,
      largeAA: ratio >= 3,
      largeAAA: ratio >= 4.5,
    };
  }

  /**
   * Validate Entire Theme
   */
  static validateTheme(theme: Theme): ValidationReport {
    const issues: ContrastIssue[] = [];
    const warnings: ContrastWarning[] = [];

    // Check text on backgrounds
    Object.entries(theme.colors.foreground).forEach(([fgKey, fgColor]) => {
      Object.entries(theme.colors.background).forEach(([bgKey, bgColor]) => {
        const contrast = this.checkContrast(fgColor, bgColor);

        if (!contrast.aa) {
          issues.push({
            type: 'error',
            foreground: `foreground.${fgKey}`,
            background: `background.${bgKey}`,
            ratio: contrast.ratio,
            required: 4.5,
          });
        } else if (!contrast.aaa) {
          warnings.push({
            type: 'warning',
            foreground: `foreground.${fgKey}`,
            background: `background.${bgKey}`,
            ratio: contrast.ratio,
            recommendation: 'Consider improving for AAA compliance',
          });
        }
      });
    });

    return {
      valid: issues.length === 0,
      issues,
      warnings,
      summary: {
        totalChecks: Object.keys(theme.colors.foreground).length *
                    Object.keys(theme.colors.background).length,
        failures: issues.length,
        warnings: warnings.length,
      },
    };
  }

  /**
   * Get Contrast Ratio (WCAG formula)
   */
  private static getContrastRatio(color1: string, color2: string): number {
    const l1 = this.getLuminance(color1);
    const l2 = this.getLuminance(color2);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  }

  /**
   * Get Relative Luminance
   */
  private static getLuminance(color: string): number {
    const rgb = this.hexToRgb(color);
    const [r, g, b] = rgb.map(val => {
      val = val / 255;
      return val <= 0.03928
        ? val / 12.92
        : Math.pow((val + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }

  /**
   * Hex to RGB
   */
  private static hexToRgb(hex: string): number[] {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result
      ? [
          parseInt(result[1], 16),
          parseInt(result[2], 16),
          parseInt(result[3], 16),
        ]
      : [0, 0, 0];
  }
}
```

---

## Best Practices

### 1. Token Organization

✅ **DO:**
- Use three-tier token system (primitive → semantic → component)
- Maintain consistent naming conventions
- Document all tokens with JSDoc
- Version your token files

❌ **DON'T:**
- Mix semantic meanings in primitives
- Use hard-coded values in components
- Skip documentation
- Change token names without deprecation

### 2. Performance

✅ **DO:**
- Use CSS custom properties for runtime theming
- Implement theme caching
- Lazy load theme variants
- Minimize runtime calculations

❌ **DON'T:**
- Recalculate themes on every render
- Load all themes upfront
- Use inline styles for theming
- Skip memoization

### 3. Accessibility

✅ **DO:**
- Validate all contrast ratios (WCAG AA minimum)
- Provide high contrast variants
- Support system preference detection
- Test with screen readers

❌ **DON'T:**
- Skip contrast validation
- Use color alone to convey information
- Ignore reduced motion preferences
- Assume one theme fits all needs

### 4. Multi-Brand Strategy

✅ **DO:**
- Design flexible token architecture
- Use brand inheritance for shared values
- Create brand-agnostic components
- Document brand switching patterns

❌ **DON'T:**
- Hard-code brand values
- Create brand-specific component variants
- Skip brand validation
- Duplicate common tokens

### 5. Developer Experience

✅ **DO:**
- Provide TypeScript definitions
- Create theme preview tools
- Add theme validation in CI/CD
- Generate theme documentation

❌ **DON'T:**
- Skip type safety
- Rely on manual testing only
- Forget to document breaking changes
- Mix theme concerns with business logic

---

## Quick Reference

### Token Resolution Order

```
Component Token → Semantic Token → Primitive Token
```

### Theme Switching Strategies

1. **CSS Custom Properties** - Best for runtime switching
2. **Class-based** - Good for static themes
3. **JavaScript Object** - Full control, more overhead
4. **Hybrid** - CSS vars + JS state management

### Color Contrast Requirements

- **WCAG AA Normal Text**: 4.5:1
- **WCAG AAA Normal Text**: 7:1
- **WCAG AA Large Text**: 3:1
- **WCAG AAA Large Text**: 4.5:1

### Common Token Scales

- **Colors**: 11-step scale (50-950)
- **Spacing**: Powers of 2 (4px, 8px, 16px, 32px...)
- **Font Sizes**: Modular scale (1.125, 1.25, 1.5...)
- **Shadows**: 5-step scale (none, sm, md, lg, xl)

---

This reference covers all major theme system patterns. Use it as a quick lookup for implementing scalable, maintainable, and accessible theming systems.
