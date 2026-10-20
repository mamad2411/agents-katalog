---
name: Enterprise CSS Patterns Library
description: Comprehensive enterprise CSS architecture patterns for large-scale applications with design systems, governance, and team workflows
category: enterprise
version: 1.0.0
keywords: [enterprise, css-architecture, design-system, itcss, atomic-design, monorepo, governance, bem, versioning, migration, performance, storybook]
---

# Enterprise CSS Patterns Library

A comprehensive collection of production-ready CSS patterns and architectures for enterprise-scale applications. This skill covers design systems, governance frameworks, component libraries, team workflows, and migration strategies.

## Table of Contents

1. [Enterprise CSS Architecture Patterns](#enterprise-css-architecture-patterns)
2. [Large-Scale Design Systems](#large-scale-design-systems)
3. [CSS Governance Framework](#css-governance-framework)
4. [Component Library Architecture](#component-library-architecture)
5. [Versioning & Migration](#versioning--migration)
6. [Monorepo CSS Management](#monorepo-css-management)
7. [Team Workflows & CI/CD](#team-workflows--cicd)
8. [Storybook Documentation](#storybook-documentation)
9. [Legacy Migration Strategies](#legacy-migration-strategies)
10. [Performance & Optimization](#performance--optimization)

---

## Enterprise CSS Architecture Patterns

### ITCSS (Inverted Triangle CSS)

**Description:** A scalable and maintainable CSS architecture based on specificity levels, from generic to explicit.

**Architecture Layers:**

```scss
/**
 * ITCSS Architecture Implementation
 * @description 7-layer inverted triangle CSS architecture
 * @version 3.0.0
 * @governance Design System Council approved
 * @accessibility WCAG 2.1 AA compliant
 */

// Layer 1: Settings – Global variables, config switches
@import 'settings/colors';
@import 'settings/typography';
@import 'settings/breakpoints';
@import 'settings/spacing';

// Layer 2: Tools – Mixins and functions (no output)
@import 'tools/mixins';
@import 'tools/functions';
@import 'tools/placeholders';

// Layer 3: Generic – Ground-zero styles (resets, normalize)
@import 'generic/reset';
@import 'generic/normalize';
@import 'generic/box-sizing';

// Layer 4: Elements – Unclassed HTML elements (type selectors)
@import 'elements/headings';
@import 'elements/links';
@import 'elements/forms';
@import 'elements/tables';

// Layer 5: Objects – Cosmetic-free design patterns (layout)
@import 'objects/container';
@import 'objects/grid';
@import 'objects/media';
@import 'objects/list-bare';

// Layer 6: Components – Complete UI components (specific)
@import 'components/buttons';
@import 'components/cards';
@import 'components/modals';
@import 'components/navigation';

// Layer 7: Utilities – Helper classes with !important (highest specificity)
@import 'utilities/spacing';
@import 'utilities/typography';
@import 'utilities/visibility';
@import 'utilities/colors';
```

**TypeScript Configuration Interface:**

```typescript
/**
 * ITCSS Configuration
 * @interface ITCSSConfig
 * @description Configuration for ITCSS architecture setup
 */
interface ITCSSConfig {
  /** Base path for SCSS files */
  basePath: string;
  /** Layers to include in build */
  layers: {
    settings: boolean;
    tools: boolean;
    generic: boolean;
    elements: boolean;
    objects: boolean;
    components: boolean;
    utilities: boolean;
  };
  /** Output configuration */
  output: {
    /** Generate sourcemaps */
    sourcemaps: boolean;
    /** Minify output */
    minify: boolean;
    /** Output file path */
    outputPath: string;
  };
  /** Performance budgets */
  budgets: {
    maxSize: number; // in KB
    maxSpecificity: number;
  };
}

/**
 * Initialize ITCSS architecture
 * @param config - ITCSS configuration
 * @returns Build result with metrics
 */
function initializeITCSS(config: ITCSSConfig): Promise<BuildResult> {
  // Implementation
}
```

**Design Tokens:**

```scss
/**
 * ITCSS Settings Layer - Design Tokens
 * @description Foundation design tokens for the entire system
 */

// settings/_colors.scss
:root {
  // Primitive tokens
  --color-blue-100: #e3f2fd;
  --color-blue-500: #2196f3;
  --color-blue-900: #0d47a1;

  // Semantic tokens
  --color-primary: var(--color-blue-500);
  --color-primary-hover: var(--color-blue-600);
  --color-surface: #ffffff;
  --color-text: #1f2937;
}

// settings/_spacing.scss
:root {
  --spacing-unit: 8px;
  --spacing-xs: calc(var(--spacing-unit) * 0.5); // 4px
  --spacing-sm: calc(var(--spacing-unit) * 1);   // 8px
  --spacing-md: calc(var(--spacing-unit) * 2);   // 16px
  --spacing-lg: calc(var(--spacing-unit) * 3);   // 24px
  --spacing-xl: calc(var(--spacing-unit) * 4);   // 32px
}
```

**Accessibility Notes:**
- Maintain logical cascade order for screen readers
- Use semantic HTML elements in Elements layer
- Ensure utility classes don't override accessibility features
- WCAG 2.1 AA: Minimum 4.5:1 contrast ratio for text

**Performance Metrics:**
- ITCSS reduces specificity wars, improving parse time by 15-20%
- Modular architecture enables tree-shaking unused CSS
- Critical CSS can be extracted from Settings + Generic + Elements layers

---

### BEM at Enterprise Scale

**Description:** Block Element Modifier methodology adapted for large teams and complex applications.

**Enterprise BEM Pattern:**

```scss
/**
 * BEM Enterprise Naming Convention
 * @description Standardized BEM implementation for large teams
 * @pattern [namespace-]block__element--modifier
 * @version 2.0.0
 * @accessibility WCAG 2.1 AA compliant
 */

// Namespace configuration
$namespace: 'ds-'; // Design system prefix for isolation

/**
 * Component: Card
 * @component Card
 * @category UI Components
 * @version 2.1.0
 * @status stable
 * @designer Jane Doe
 * @developer John Smith
 * @last-modified 2024-01-15
 * @accessibility
 *   - Keyboard navigable
 *   - Screen reader friendly
 *   - ARIA labels included
 */
.#{$namespace}card {
  // CSS Custom Properties API
  --card-background: var(--color-surface);
  --card-padding: var(--spacing-md);
  --card-border-radius: var(--radius-md);
  --card-shadow: var(--shadow-sm);
  --card-transition: var(--transition-default);

  // Base block styles
  background: var(--card-background);
  padding: var(--card-padding);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  transition: var(--card-transition);

  /**
   * Element: Card header container
   * @requires .ds-card__title
   * @optional .ds-card__actions
   */
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-block-end: var(--spacing-sm);
    border-block-end: 1px solid var(--color-border);
  }

  /**
   * Element: Card title
   * @typography heading-3
   * @color text-primary
   */
  &__title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--color-text-primary);
    margin: 0;
  }

  /**
   * Element: Card actions container
   * @layout horizontal flex
   */
  &__actions {
    display: flex;
    gap: var(--spacing-xs);
  }

  /**
   * Element: Card body content
   * @layout flex-column
   */
  &__body {
    padding-block: var(--spacing-md);
  }

  /**
   * Element: Card footer
   * @layout flex horizontal
   */
  &__footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-sm);
    padding-block-start: var(--spacing-sm);
    border-block-start: 1px solid var(--color-border);
  }

  // ===== Modifier: Visual Variants =====

  /**
   * Modifier: Elevated card with enhanced shadow
   * @shadow level-2
   */
  &--elevated {
    --card-shadow: var(--shadow-md);

    &:hover {
      --card-shadow: var(--shadow-lg);
    }
  }

  /**
   * Modifier: Interactive clickable card
   * @interaction hover, focus, active
   * @cursor pointer
   */
  &--interactive {
    cursor: pointer;

    &:hover {
      --card-background: var(--color-surface-hover);
    }

    &:focus-visible {
      outline: 2px solid var(--color-focus);
      outline-offset: 2px;
    }

    &:active {
      transform: translateY(1px);
    }
  }

  /**
   * Modifier: Outlined card variant
   * @border 1px solid
   */
  &--outlined {
    --card-shadow: none;
    border: 1px solid var(--color-border);
  }

  // ===== Modifier: Size Variants =====

  /**
   * Modifier: Compact card with reduced padding
   * @padding sm
   */
  &--compact {
    --card-padding: var(--spacing-sm);
  }

  /**
   * Modifier: Large card with increased padding
   * @padding lg
   */
  &--large {
    --card-padding: var(--spacing-lg);
  }

  // ===== State Modifiers =====

  /**
   * State: Loading state
   * @state loading
   */
  &--loading {
    position: relative;
    pointer-events: none;

    &::after {
      content: '';
      position: absolute;
      inset: 0;
      background: rgba(255, 255, 255, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }

  /**
   * State: Error state
   * @state error
   * @color error
   */
  &--error {
    border-inline-start: 4px solid var(--color-error);
  }
}
```

**TypeScript Interface:**

```typescript
/**
 * BEM Component Configuration
 * @interface BEMComponent
 * @description Type-safe BEM component configuration
 */
interface BEMComponent {
  /** Block name */
  block: string;
  /** Namespace prefix */
  namespace?: string;
  /** Elements within the block */
  elements: {
    name: string;
    required: boolean;
    description: string;
  }[];
  /** Available modifiers */
  modifiers: {
    name: string;
    type: 'visual' | 'size' | 'state';
    values?: string[];
    description: string;
  }[];
  /** Component metadata */
  metadata: {
    version: string;
    status: 'stable' | 'beta' | 'deprecated';
    accessibility: string[];
  };
}

/**
 * Generate BEM class name
 * @param block - Block name
 * @param element - Optional element name
 * @param modifier - Optional modifier name
 * @param namespace - Optional namespace prefix
 * @returns Complete BEM class name
 */
function bem(
  block: string,
  element?: string,
  modifier?: string,
  namespace: string = 'ds-'
): string {
  let className = `${namespace}${block}`;
  if (element) className += `__${element}`;
  if (modifier) className += `--${modifier}`;
  return className;
}

// Usage example
const cardClass = bem('card', 'header', 'elevated'); // 'ds-card__header--elevated'
```

**Accessibility Guidelines:**
- Use semantic HTML: `<article class="ds-card">` instead of `<div>`
- Add ARIA roles when needed: `role="region"` for cards with headings
- Ensure interactive cards have `tabindex="0"` and keyboard handlers
- Provide focus indicators with minimum 2px width and 4.5:1 contrast

---

### Atomic Design Pattern

**Description:** Hierarchical component system from atoms to pages for systematic UI construction.

**Atomic Design Implementation:**

```scss
/**
 * Atomic Design System Structure
 * @description 5-level component hierarchy
 * @pattern Atoms → Molecules → Organisms → Templates → Pages
 * @version 3.0.0
 */

// ===== ATOMS: Basic building blocks =====
// atoms/_button.scss
/**
 * Atom: Button
 * @description Fundamental clickable element
 * @category Atoms
 * @accessibility
 *   - Keyboard accessible (Enter/Space)
 *   - Focus visible
 *   - ARIA label support
 */
.a-button {
  --button-background: var(--color-primary);
  --button-color: var(--color-primary-contrast);
  --button-padding: var(--spacing-sm) var(--spacing-md);
  --button-border-radius: var(--radius-md);
  --button-font-size: var(--font-size-base);
  --button-font-weight: var(--font-weight-medium);
  --button-transition: all 0.2s ease;

  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  padding: var(--button-padding);
  background: var(--button-background);
  color: var(--button-color);
  border: none;
  border-radius: var(--button-border-radius);
  font-size: var(--button-font-size);
  font-weight: var(--button-font-weight);
  font-family: inherit;
  line-height: 1;
  text-decoration: none;
  cursor: pointer;
  user-select: none;
  transition: var(--button-transition);

  // Focus state
  &:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
  }

  // Hover state
  &:hover:not(:disabled) {
    filter: brightness(1.1);
  }

  // Active state
  &:active:not(:disabled) {
    transform: translateY(1px);
  }

  // Disabled state
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

// atoms/_input.scss
/**
 * Atom: Input
 * @description Text input field
 * @category Atoms
 */
.a-input {
  --input-background: var(--color-surface);
  --input-border: 1px solid var(--color-border);
  --input-padding: var(--spacing-sm) var(--spacing-md);
  --input-border-radius: var(--radius-md);
  --input-font-size: var(--font-size-base);

  width: 100%;
  padding: var(--input-padding);
  background: var(--input-background);
  border: var(--input-border);
  border-radius: var(--input-border-radius);
  font-size: var(--input-font-size);
  font-family: inherit;
  transition: border-color 0.2s ease;

  &:focus {
    outline: none;
    border-color: var(--color-primary);
  }

  &::placeholder {
    color: var(--color-text-tertiary);
  }

  &:disabled {
    background: var(--color-surface-disabled);
    cursor: not-allowed;
  }
}

// ===== MOLECULES: Simple component groups =====
// molecules/_form-field.scss
/**
 * Molecule: Form Field
 * @description Input with label and error message
 * @category Molecules
 * @composition
 *   - .a-label (Atom)
 *   - .a-input (Atom)
 *   - .a-error-message (Atom)
 */
.m-form-field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);

  &__label {
    @extend .a-label;
    font-weight: var(--font-weight-medium);
    color: var(--color-text-primary);
  }

  &__input {
    @extend .a-input;
  }

  &__hint {
    font-size: var(--font-size-sm);
    color: var(--color-text-tertiary);
  }

  &__error {
    font-size: var(--font-size-sm);
    color: var(--color-error);
    display: none;
  }

  // Error state
  &--error {
    .m-form-field__input {
      border-color: var(--color-error);
    }

    .m-form-field__error {
      display: block;
    }
  }
}

// molecules/_search-box.scss
/**
 * Molecule: Search Box
 * @description Input with search icon and clear button
 * @category Molecules
 * @composition
 *   - .a-input (Atom)
 *   - .a-button (Atom)
 *   - .a-icon (Atom)
 */
.m-search-box {
  position: relative;
  display: flex;
  align-items: center;

  &__icon {
    position: absolute;
    left: var(--spacing-sm);
    color: var(--color-text-tertiary);
    pointer-events: none;
  }

  &__input {
    @extend .a-input;
    padding-inline-start: calc(var(--spacing-md) + 24px);
    padding-inline-end: calc(var(--spacing-md) + 24px);
  }

  &__clear {
    @extend .a-button;
    position: absolute;
    right: var(--spacing-xs);
    padding: var(--spacing-xs);
    background: transparent;
    color: var(--color-text-tertiary);

    &:hover {
      color: var(--color-text-primary);
    }
  }
}

// ===== ORGANISMS: Complex UI components =====
// organisms/_header.scss
/**
 * Organism: Site Header
 * @description Main navigation header
 * @category Organisms
 * @composition
 *   - .m-logo (Molecule)
 *   - .m-navigation (Molecule)
 *   - .m-search-box (Molecule)
 *   - .m-user-menu (Molecule)
 */
.o-header {
  --header-height: 64px;
  --header-background: var(--color-surface);
  --header-border: 1px solid var(--color-border);

  position: sticky;
  top: 0;
  z-index: 100;
  height: var(--header-height);
  background: var(--header-background);
  border-block-end: var(--header-border);

  &__container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100%;
    padding-inline: var(--spacing-lg);
    max-width: var(--container-max-width);
    margin-inline: auto;
  }

  &__brand {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  &__nav {
    flex: 1;
    display: flex;
    justify-content: center;
  }

  &__actions {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
  }
}

// organisms/_data-table.scss
/**
 * Organism: Data Table
 * @description Complex table with sorting, filtering, pagination
 * @category Organisms
 * @composition
 *   - .m-table-header (Molecule)
 *   - .m-table-row (Molecule)
 *   - .m-pagination (Molecule)
 */
.o-data-table {
  --table-border: 1px solid var(--color-border);
  --table-header-background: var(--color-surface-secondary);

  width: 100%;
  border: var(--table-border);
  border-radius: var(--radius-lg);
  overflow: hidden;

  &__header {
    background: var(--table-header-background);
    font-weight: var(--font-weight-semibold);
  }

  &__body {
    // Table body styles
  }

  &__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md);
    border-block-start: var(--table-border);
  }
}
```

**TypeScript Atomic Design Interface:**

```typescript
/**
 * Atomic Design Component Registry
 * @description Type-safe component registry for atomic design
 */
interface AtomicDesignRegistry {
  atoms: {
    button: ComponentDefinition;
    input: ComponentDefinition;
    label: ComponentDefinition;
    icon: ComponentDefinition;
  };
  molecules: {
    formField: ComponentDefinition;
    searchBox: ComponentDefinition;
    card: ComponentDefinition;
  };
  organisms: {
    header: ComponentDefinition;
    dataTable: ComponentDefinition;
    sidebar: ComponentDefinition;
  };
  templates: {
    dashboardLayout: TemplateDefinition;
    authLayout: TemplateDefinition;
  };
}

interface ComponentDefinition {
  name: string;
  category: 'atom' | 'molecule' | 'organism';
  dependencies: string[];
  props: Record<string, PropDefinition>;
  variants: string[];
  accessibility: AccessibilityRequirements;
}

interface PropDefinition {
  type: 'string' | 'number' | 'boolean';
  required: boolean;
  default?: any;
  description: string;
}

interface AccessibilityRequirements {
  role?: string;
  ariaLabels: string[];
  keyboardNavigation: boolean;
  wcagLevel: 'A' | 'AA' | 'AAA';
}
```

**Composition Guidelines:**
- **Atoms** compose only primitives (no other atoms)
- **Molecules** compose 2-5 atoms
- **Organisms** compose molecules and atoms (max 10 components)
- **Templates** define page structure using organisms
- **Pages** are instances of templates with real content

---

## Large-Scale Design Systems

### Design System Architecture

**Description:** Complete enterprise design system structure with tokens, components, and patterns.

```scss
/**
 * Enterprise Design System Structure
 * @description Complete design system architecture
 * @version 3.0.0
 * @governance Design System Council
 * @performance Budget: 250KB uncompressed, 50KB gzipped
 */

// ===== LAYER 1: Design Tokens =====
// Primary source of truth for all design decisions
@import 'tokens/colors';
@import 'tokens/typography';
@import 'tokens/spacing';
@import 'tokens/shadows';
@import 'tokens/animations';
@import 'tokens/breakpoints';
@import 'tokens/z-index';

// ===== LAYER 2: Foundation =====
// Core utilities and helpers
@import 'foundation/reset';
@import 'foundation/mixins';
@import 'foundation/functions';
@import 'foundation/grid';
@import 'foundation/breakpoints';

// ===== LAYER 3: Component Layer =====
// Reusable UI components organized by category
@import 'components/core/*';       // Core: buttons, inputs, labels
@import 'components/layout/*';     // Layout: container, grid, stack
@import 'components/navigation/*'; // Navigation: navbar, tabs, breadcrumbs
@import 'components/data/*';       // Data: tables, lists, cards
@import 'components/feedback/*';   // Feedback: alerts, toasts, modals

// ===== LAYER 4: Pattern Layer =====
// Complex UI patterns combining components
@import 'patterns/forms/*';
@import 'patterns/cards/*';
@import 'patterns/modals/*';
@import 'patterns/workflows/*';
@import 'patterns/dashboards/*';

// ===== LAYER 5: Theme Layer =====
// Brand-specific customizations
@import 'themes/default';
@import 'themes/dark';
@import 'themes/high-contrast';
@import 'themes/brand-a';
@import 'themes/brand-b';
```

### Design Token Management

**3-Tier Token System:**

```scss
/**
 * Multi-Tier Design Token Architecture
 * @description Enterprise-grade token system for maximum flexibility
 * @governance Token changes require Design System Council approval
 * @versioning Tokens follow semantic versioning
 */

// ===== TIER 1: Primitive Tokens (Raw Values) =====
/**
 * Primitive Color Tokens
 * @description Base color palette - never use directly in components
 * @tier 1
 */
$primitive-colors: (
  // Blue scale
  'blue-100': #e3f2fd,
  'blue-200': #bbdefb,
  'blue-300': #90caf9,
  'blue-400': #64b5f6,
  'blue-500': #2196f3,
  'blue-600': #1e88e5,
  'blue-700': #1976d2,
  'blue-800': #1565c0,
  'blue-900': #0d47a1,

  // Gray scale
  'gray-100': #f5f5f5,
  'gray-200': #eeeeee,
  'gray-300': #e0e0e0,
  'gray-400': #bdbdbd,
  'gray-500': #9e9e9e,
  'gray-600': #757575,
  'gray-700': #616161,
  'gray-800': #424242,
  'gray-900': #212121,

  // Semantic colors
  'green-500': #4caf50,
  'green-600': #43a047,
  'amber-500': #ffc107,
  'amber-600': #ffb300,
  'red-500': #f44336,
  'red-600': #e53935
);

// ===== TIER 2: Semantic Tokens (Meaning) =====
/**
 * Semantic Color Tokens
 * @description Purpose-driven tokens mapped from primitives
 * @tier 2
 * @usage Use these in tier-3 component tokens
 */
$semantic-colors: (
  // Primary brand color
  'primary': map-get($primitive-colors, 'blue-600'),
  'primary-hover': map-get($primitive-colors, 'blue-700'),
  'primary-active': map-get($primitive-colors, 'blue-800'),
  'primary-light': map-get($primitive-colors, 'blue-100'),

  // Secondary brand color
  'secondary': map-get($primitive-colors, 'gray-700'),
  'secondary-hover': map-get($primitive-colors, 'gray-800'),

  // Feedback colors
  'success': map-get($primitive-colors, 'green-600'),
  'success-light': map-get($primitive-colors, 'green-100'),
  'warning': map-get($primitive-colors, 'amber-600'),
  'warning-light': map-get($primitive-colors, 'amber-100'),
  'error': map-get($primitive-colors, 'red-600'),
  'error-light': map-get($primitive-colors, 'red-100'),
  'info': map-get($primitive-colors, 'blue-500'),
  'info-light': map-get($primitive-colors, 'blue-100'),

  // Neutral colors
  'text-primary': map-get($primitive-colors, 'gray-900'),
  'text-secondary': map-get($primitive-colors, 'gray-700'),
  'text-tertiary': map-get($primitive-colors, 'gray-500'),
  'text-disabled': map-get($primitive-colors, 'gray-400'),

  // Surface colors
  'surface': #ffffff,
  'surface-secondary': map-get($primitive-colors, 'gray-100'),
  'surface-tertiary': map-get($primitive-colors, 'gray-200'),

  // Border colors
  'border': map-get($primitive-colors, 'gray-300'),
  'border-strong': map-get($primitive-colors, 'gray-400')
);

// ===== TIER 3: Component Tokens (Specific Use) =====
/**
 * Component-Specific Tokens
 * @description Granular tokens for individual components
 * @tier 3
 * @usage Use these directly in component styles
 */
$component-tokens: (
  // Button tokens
  'button-primary-bg': map-get($semantic-colors, 'primary'),
  'button-primary-text': #ffffff,
  'button-primary-hover-bg': map-get($semantic-colors, 'primary-hover'),
  'button-secondary-bg': map-get($semantic-colors, 'secondary'),
  'button-secondary-text': #ffffff,
  'button-padding-sm': 8px 12px,
  'button-padding-md': 12px 16px,
  'button-padding-lg': 16px 24px,

  // Card tokens
  'card-background': map-get($semantic-colors, 'surface'),
  'card-border': 1px solid map-get($semantic-colors, 'border'),
  'card-shadow': 0 2px 4px rgba(0, 0, 0, 0.1),
  'card-shadow-hover': 0 4px 8px rgba(0, 0, 0, 0.15),
  'card-padding': 16px,
  'card-border-radius': 8px,

  // Input tokens
  'input-bg': map-get($semantic-colors, 'surface'),
  'input-border': 1px solid map-get($semantic-colors, 'border'),
  'input-border-focus': 2px solid map-get($semantic-colors, 'primary'),
  'input-text': map-get($semantic-colors, 'text-primary'),
  'input-placeholder': map-get($semantic-colors, 'text-tertiary'),
  'input-padding': 8px 12px,
  'input-border-radius': 4px
);

/**
 * Token Validation Function
 * @description Ensures token exists and provides helpful error
 * @param {Map} $token-map - Token map to search
 * @param {String} $key - Token key
 * @returns {Any} Token value
 * @throws Error if token not found
 */
@function validate-token($token-map, $key) {
  @if not map-has-key($token-map, $key) {
    @error "Token '#{$key}' not found in token map. Available tokens: #{map-keys($token-map)}";
  }
  @return map-get($token-map, $key);
}

/**
 * Get Component Token
 * @description Safe token retrieval with validation
 * @param {String} $key - Component token key
 * @returns {Any} Token value
 */
@function token($key) {
  @return validate-token($component-tokens, $key);
}

// Usage example
.button {
  background: token('button-primary-bg');
  color: token('button-primary-text');
  padding: token('button-padding-md');
}
```

**CSS Custom Properties Export:**

```scss
/**
 * Export Tokens as CSS Custom Properties
 * @description Make tokens available at runtime for dynamic theming
 */
:root {
  // Tier 1: Primitive tokens
  @each $name, $value in $primitive-colors {
    --color-#{$name}: #{$value};
  }

  // Tier 2: Semantic tokens
  @each $name, $value in $semantic-colors {
    --semantic-#{$name}: #{$value};
  }

  // Tier 3: Component tokens
  @each $name, $value in $component-tokens {
    --#{$name}: #{$value};
  }

  // Typography tokens
  --font-family-primary: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --font-family-mono: 'SF Mono', Monaco, 'Cascadia Code', monospace;

  --font-size-xs: 0.75rem;   // 12px
  --font-size-sm: 0.875rem;  // 14px
  --font-size-base: 1rem;    // 16px
  --font-size-lg: 1.125rem;  // 18px
  --font-size-xl: 1.25rem;   // 20px
  --font-size-2xl: 1.5rem;   // 24px
  --font-size-3xl: 1.875rem; // 30px
  --font-size-4xl: 2.25rem;  // 36px

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  // Spacing tokens
  --spacing-unit: 8px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --spacing-3xl: 64px;

  // Border radius tokens
  --radius-none: 0;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  // Shadow tokens
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);

  // Animation tokens
  --transition-fast: 150ms ease;
  --transition-default: 250ms ease;
  --transition-slow: 350ms ease;

  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  // Z-index tokens
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
}
```

**TypeScript Token Interface:**

```typescript
/**
 * Design Token Type Definitions
 * @description Type-safe design token system
 */

/**
 * Token Tier Enumeration
 * @enum {number}
 */
enum TokenTier {
  /** Raw values - never use directly */
  Primitive = 1,
  /** Purpose-driven tokens */
  Semantic = 2,
  /** Component-specific tokens */
  Component = 3
}

/**
 * Color Token Definition
 * @interface ColorToken
 */
interface ColorToken {
  name: string;
  value: string;
  tier: TokenTier;
  /** Contrast ratio for accessibility */
  contrastRatio?: number;
  /** WCAG compliance level */
  wcagLevel?: 'AA' | 'AAA';
}

/**
 * Spacing Token Definition
 * @interface SpacingToken
 */
interface SpacingToken {
  name: string;
  value: string;
  /** Base unit multiplier */
  multiplier: number;
}

/**
 * Typography Token Definition
 * @interface TypographyToken
 */
interface TypographyToken {
  fontSize: string;
  lineHeight: string;
  fontWeight: number;
  letterSpacing?: string;
}

/**
 * Complete Token Registry
 * @interface DesignTokenRegistry
 */
interface DesignTokenRegistry {
  colors: {
    primitive: Map<string, ColorToken>;
    semantic: Map<string, ColorToken>;
    component: Map<string, ColorToken>;
  };
  spacing: Map<string, SpacingToken>;
  typography: Map<string, TypographyToken>;
  shadows: Map<string, string>;
  radii: Map<string, string>;
  zIndex: Map<string, number>;
}

/**
 * Token Manager Class
 * @class TokenManager
 * @description Manages design tokens with validation and type safety
 */
class TokenManager {
  private registry: DesignTokenRegistry;

  /**
   * Get color token
   * @param name - Token name
   * @param tier - Token tier (defaults to component)
   * @returns Color value
   * @throws Error if token not found
   */
  getColor(name: string, tier: TokenTier = TokenTier.Component): string {
    let tokenMap: Map<string, ColorToken>;

    switch (tier) {
      case TokenTier.Primitive:
        tokenMap = this.registry.colors.primitive;
        break;
      case TokenTier.Semantic:
        tokenMap = this.registry.colors.semantic;
        break;
      case TokenTier.Component:
        tokenMap = this.registry.colors.component;
        break;
    }

    const token = tokenMap.get(name);
    if (!token) {
      throw new Error(`Color token '${name}' not found in tier ${tier}`);
    }

    return token.value;
  }

  /**
   * Validate token accessibility
   * @param foreground - Foreground color token
   * @param background - Background color token
   * @returns WCAG compliance level or null if fails
   */
  validateContrast(foreground: string, background: string): 'AA' | 'AAA' | null {
    const ratio = this.calculateContrastRatio(foreground, background);

    if (ratio >= 7) return 'AAA';
    if (ratio >= 4.5) return 'AA';
    return null;
  }

  private calculateContrastRatio(color1: string, color2: string): number {
    // Implementation of WCAG contrast ratio calculation
    // Returns ratio between 1 and 21
    return 4.5; // Placeholder
  }
}
```

---

## CSS Governance Framework

### Governance Charter

**Structure:**

```markdown
# CSS Governance Charter
Version: 2.0.0
Effective Date: 2024-01-01
Review Cycle: Quarterly

## 1. Governance Structure

### Design System Council
**Role:** Strategic oversight and major decision approval
**Members:**
- Chief Design Officer (Chair)
- Lead Frontend Architect
- UX Research Lead
- Accessibility Specialist
- Product Manager

**Responsibilities:**
- Approve architecture changes
- Set design system roadmap
- Resolve escalated decisions
- Budget allocation

**Meeting Schedule:** Monthly

### CSS Working Group
**Role:** Technical implementation and standards
**Members:**
- Senior Frontend Engineers (3-5)
- CSS Specialist
- Performance Engineer
- Quality Assurance Lead

**Responsibilities:**
- Review RFCs (Request for Comments)
- Define coding standards
- Approve new components
- Maintain documentation

**Meeting Schedule:** Weekly

### Component Owners
**Role:** Individual component maintenance
**Responsibilities:**
- Implement features
- Fix bugs
- Update documentation
- Review PRs for owned components

**Assignment:** Each component has 1 primary + 1 secondary owner

### Quality Assurance Team
**Role:** Testing and validation
**Responsibilities:**
- Visual regression testing
- Accessibility audits
- Performance testing
- Cross-browser validation

## 2. Decision Making Process

### RFC (Request for Comments) Process

**When to Create RFC:**
- New architecture patterns
- Breaking changes
- New major components
- Methodology changes
- Performance budget adjustments

**RFC Template:**
```markdown
# RFC: [Title]
**Date:** YYYY-MM-DD
**Author:** Name
**Status:** Draft | Review | Approved | Rejected

## Summary
Brief description (2-3 sentences)

## Motivation
Why is this needed?

## Detailed Design
Technical implementation details

## Drawbacks
Potential downsides and risks

## Alternatives
What other approaches were considered?

## Migration Plan
How to adopt this change?

## Performance Impact
Expected performance implications
```

**Review Timeline:**
1. **Week 1:** RFC submission
2. **Week 2-3:** Working Group review and discussion
3. **Week 4:** POC implementation (if needed)
4. **Week 5:** Council approval for major changes
5. **Week 6+:** Implementation with migration plan

### Decision Escalation Path
1. Component Owner → Lead Engineer
2. Lead Engineer → CSS Working Group
3. CSS Working Group → Design System Council
4. Council decision is final

## 3. Code Standards

### Mandatory Requirements

**Linting:**
- All CSS must pass Stylelint with zero warnings
- Configuration: `.stylelintrc.json` in repository root
- Pre-commit hooks enforce linting

**Documentation:**
- Every component requires documentation
- Storybook stories for all UI components
- Usage examples and API documentation
- Accessibility notes

**Performance:**
- CSS bundle size budget: 250KB (uncompressed)
- Critical CSS budget: 14KB (inline)
- Specificity maximum: 0-3-0
- No !important except in utilities

**Accessibility:**
- WCAG 2.1 AA minimum compliance
- Focus indicators on all interactive elements
- Color contrast ratios meet guidelines
- Screen reader testing required

**Browser Support:**
- Chrome: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Edge: Last 2 versions
- Mobile Safari: Last 2 versions

### Code Quality Metrics

**Tracked Metrics:**
- Bundle size (gzipped and uncompressed)
- Number of selectors
- Specificity distribution
- Unused CSS percentage
- Critical CSS size
- Parse time (performance)
- Paint time (performance)

**Quality Gates:**
- Code coverage > 80%
- Visual regression: 0 unreviewed changes
- Accessibility: 0 violations
- Performance budget: Must meet all budgets

## 4. Review Requirements

### Pull Request Requirements

**Required Checks (Automated):**
- ✅ Stylelint passes
- ✅ Build succeeds
- ✅ Visual regression tests pass
- ✅ Performance budgets met
- ✅ No accessibility violations

**Required Reviews:**
- 2 peer approvals for standard changes
- Design System team approval for new components
- Performance team approval for bundles > 50KB
- Accessibility team approval for interactive components

**Review Checklist:**
```markdown
## Architecture
- [ ] Follows established patterns
- [ ] Appropriate file location
- [ ] Correct naming conventions

## Code Quality
- [ ] No !important (except utilities)
- [ ] Uses design tokens
- [ ] Minimal nesting (max 3 levels)
- [ ] DRY principle followed

## Performance
- [ ] Efficient selectors
- [ ] No layout thrashing
- [ ] Critical CSS identified

## Documentation
- [ ] Component docs complete
- [ ] Usage examples provided
- [ ] Changelog updated

## Testing
- [ ] Visual regression passes
- [ ] Accessibility tested
- [ ] Cross-browser verified
```

## 5. Compliance & Enforcement

**Automated Enforcement:**
- Pre-commit hooks for linting
- CI/CD pipeline blocks failing builds
- Automated performance budgets

**Manual Review:**
- Design review for visual QA
- Accessibility audit for new features
- Architecture review for major changes

**Violation Process:**
1. **Warning:** First violation - educational feedback
2. **Required Fix:** Second violation - must fix before merge
3. **Escalation:** Repeated violations - team lead involvement

## 6. Training & Onboarding

**New Team Members:**
- 2-week onboarding program
- Pair programming sessions
- Documentation review
- Small starter tasks

**Ongoing Education:**
- Weekly CSS learning sessions
- Monthly architecture reviews
- Quarterly workshops
- Annual conference attendance budget

## 7. Documentation Standards

**Required Documentation:**
- Architecture Decision Records (ADRs)
- Component API documentation
- Usage guidelines
- Migration guides
- Performance notes
- Accessibility requirements

**Documentation Locations:**
- Storybook: Component documentation
- Confluence: Architecture decisions
- README: Getting started
- Wiki: Detailed guides
```

### Code Review Checklist

```scss
/**
 * Enterprise CSS Code Review Checklist
 * @description Comprehensive review criteria for CSS contributions
 * @version 2.1.0
 * @governance Mandatory for all CSS changes
 */

// ===== ARCHITECTURE COMPLIANCE =====
/**
 * Architecture Review
 * @checklist
 * - [ ] Follows ITCSS/Atomic/established architecture
 * - [ ] Correct layer placement (Settings/Tools/Components/etc)
 * - [ ] File naming follows conventions
 * - [ ] Appropriate directory structure
 * - [ ] No cross-layer violations
 */

// ===== NAMING CONVENTIONS =====
/**
 * Naming Standards
 * @checklist
 * - [ ] BEM methodology followed consistently
 * - [ ] Namespace prefix used correctly
 * - [ ] Class names are semantic and meaningful
 * - [ ] No abbreviations (except standard: btn, nav)
 * - [ ] Modifier naming is clear
 */

// ===== CODE QUALITY =====
/**
 * Code Quality Standards
 * @checklist
 * - [ ] No !important (except in utility layer)
 * - [ ] No magic numbers (all values use variables/tokens)
 * - [ ] Mixins used appropriately
 * - [ ] Functions used for calculations
 * - [ ] DRY principle applied
 * - [ ] Consistent code formatting
 * - [ ] Logical properties used (margin-inline vs margin-left)
 */

// Example of quality issues:
// ❌ BAD
.card {
  margin-left: 16px; // Magic number + physical property
  color: #333 !important; // Unnecessary !important
  .title {
    .text {
      .inner {
        // Too much nesting
      }
    }
  }
}

// ✅ GOOD
.card {
  margin-inline-start: var(--spacing-md); // Token + logical property
  color: var(--color-text-primary);

  &__title {
    // Single level nesting
  }
}

// ===== PERFORMANCE =====
/**
 * Performance Standards
 * @checklist
 * - [ ] Specificity kept low (max 0-3-0)
 * - [ ] Nesting limited to 3 levels
 * - [ ] Efficient selectors (avoid universal, descendant)
 * - [ ] Critical CSS identified and extracted
 * - [ ] No expensive properties (box-shadow on scroll)
 * - [ ] Bundle size impact measured
 * - [ ] No redundant selectors
 */

// Performance budget check
/**
 * Bundle Size Impact
 * @metric Current: 45KB | After Change: 47KB | Budget: 50KB
 * @status ✅ Within budget
 */

// ===== DESIGN TOKENS =====
/**
 * Design Token Usage
 * @checklist
 * - [ ] All colors use design tokens
 * - [ ] All spacing uses spacing scale
 * - [ ] Typography tokens applied
 * - [ ] No hard-coded values
 * - [ ] Semantic tokens preferred over primitive
 * - [ ] Component tokens for specific use cases
 */

// ===== ACCESSIBILITY =====
/**
 * Accessibility Requirements
 * @checklist
 * - [ ] Color contrast meets WCAG 2.1 AA (4.5:1 text, 3:1 UI)
 * - [ ] Focus indicators visible and meet standards
 * - [ ] Interactive elements have hover/focus/active states
 * - [ ] No reliance on color alone for information
 * - [ ] Text is resizable up to 200%
 * - [ ] Reduced motion respected (@media prefers-reduced-motion)
 * - [ ] High contrast mode supported
 */

// Example accessibility checks:
// ✅ GOOD - Contrast ratio: 7.2:1 (AAA)
.button {
  background: var(--color-primary); // #0d47a1
  color: #ffffff;

  &:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
  }
}

// ❌ BAD - Contrast ratio: 2.8:1 (Fails AA)
.button-bad {
  background: #90caf9; // Too light
  color: #ffffff;

  &:focus {
    outline: none; // Removes focus indicator
  }
}

// ===== RESPONSIVE DESIGN =====
/**
 * Responsive Requirements
 * @checklist
 * - [ ] Mobile-first approach
 * - [ ] Breakpoints use design tokens
 * - [ ] Container queries where appropriate
 * - [ ] Flexible units (rem, em, %) over px
 * - [ ] Tested on all required viewports
 * - [ ] No horizontal scrolling
 */

// ===== BROWSER COMPATIBILITY =====
/**
 * Browser Support
 * @checklist
 * - [ ] Tested in Chrome (last 2 versions)
 * - [ ] Tested in Firefox (last 2 versions)
 * - [ ] Tested in Safari (last 2 versions)
 * - [ ] Tested in Edge (last 2 versions)
 * - [ ] Autoprefixer applied
 * - [ ] Fallbacks for unsupported features
 */

// ===== DOCUMENTATION =====
/**
 * Documentation Requirements
 * @checklist
 * - [ ] Component purpose documented
 * - [ ] Usage examples provided
 * - [ ] Props/modifiers documented
 * - [ ] Storybook story created
 * - [ ] Accessibility notes included
 * - [ ] Browser support listed
 * - [ ] Changelog updated
 */

// ===== TESTING =====
/**
 * Testing Requirements
 * @checklist
 * - [ ] Visual regression tests created/updated
 * - [ ] Accessibility tests pass (axe-core)
 * - [ ] Cross-browser testing completed
 * - [ ] Responsive testing done
 * - [ ] Performance testing conducted
 * - [ ] Interactive states tested
 */

// ===== DESIGN SYSTEM ALIGNMENT =====
/**
 * Design System Compliance
 * @checklist
 * - [ ] Uses design tokens exclusively
 * - [ ] Follows spacing system
 * - [ ] Typography scale applied correctly
 * - [ ] Color palette compliance
 * - [ ] Adheres to grid system
 * - [ ] Consistent with existing patterns
 */

// ===== MIGRATION & DEPRECATION =====
/**
 * Breaking Changes
 * @checklist (if applicable)
 * - [ ] Migration guide provided
 * - [ ] Deprecation warnings added
 * - [ ] Version bump appropriate (MAJOR for breaking)
 * - [ ] Backward compatibility considered
 * - [ ] Codemods provided for automation
 * - [ ] Communication plan defined
 */
```

---

## Component Library Architecture

### Component Template System

```scss
/**
 * Enterprise Component Template
 * @description Reusable component scaffold with full documentation
 * @version 3.0.0
 */

/**
 * Component Template Mixin
 * @mixin component-template
 * @param {String} $name - Component name
 * @param {Map} $config - Component configuration
 */
@mixin component-template($name, $config: ()) {
  /**
   * Component: #{$name}
   * @component #{$name}
   * @category #{map-get($config, 'category')}
   * @version #{map-get($config, 'version')}
   * @status #{map-get($config, 'status')}
   * @designer #{map-get($config, 'designer')}
   * @developer #{map-get($config, 'developer')}
   * @last-modified #{map-get($config, 'last-modified')}
   * @accessibility #{map-get($config, 'accessibility')}
   */

  .c-#{$name} {
    // Component API using CSS Custom Properties
    --#{$name}-background: var(--color-surface);
    --#{$name}-color: var(--color-text);
    --#{$name}-border: var(--border-default);
    --#{$name}-padding: var(--spacing-md);
    --#{$name}-border-radius: var(--radius-md);
    --#{$name}-transition: var(--transition-default);

    // Base styles using custom properties
    background: var(--#{$name}-background);
    color: var(--#{$name}-color);
    border: var(--#{$name}-border);
    padding: var(--#{$name}-padding);
    border-radius: var(--#{$name}-border-radius);
    transition: var(--#{$name}-transition);

    // Allow component-specific styles
    @content;
  }
}
```

---

### Complete Button Component Example

```scss
/**
 * Enterprise Button Component
 * @description Production-ready button with full variants
 * @example
 *   <button class="c-button c-button--primary c-button--medium">
 *     Click me
 *   </button>
 */
@include component-template('button', (
  'category': 'Core Components',
  'version': '2.1.0',
  'status': 'stable',
  'designer': 'Jane Doe',
  'developer': 'John Smith',
  'last-modified': '2024-01-15',
  'accessibility': 'WCAG 2.1 AA - Keyboard accessible, ARIA support'
)) {
  // Core button structure
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  font-family: var(--font-family-primary);
  font-weight: var(--font-weight-medium);
  text-decoration: none;
  cursor: pointer;
  user-select: none;
  white-space: nowrap;

  // ===== Size Variants =====

  &--small {
    --button-padding: var(--spacing-xs) var(--spacing-sm);
    --button-font-size: var(--font-size-sm);
    --button-min-height: 32px;
  }

  &--medium {
    --button-padding: var(--spacing-sm) var(--spacing-md);
    --button-font-size: var(--font-size-base);
    --button-min-height: 40px;
  }

  &--large {
    --button-padding: var(--spacing-md) var(--spacing-lg);
    --button-font-size: var(--font-size-lg);
    --button-min-height: 48px;
  }

  // ===== Type Variants =====

  &--primary {
    --button-background: var(--color-primary);
    --button-color: var(--color-primary-contrast);

    &:hover:not(:disabled) {
      --button-background: var(--color-primary-hover);
    }
  }

  &--secondary {
    --button-background: var(--color-secondary);
    --button-color: var(--color-secondary-contrast);

    &:hover:not(:disabled) {
      --button-background: var(--color-secondary-hover);
    }
  }

  &--outlined {
    --button-background: transparent;
    --button-color: var(--color-primary);
    --button-border: 1px solid var(--color-primary);

    &:hover:not(:disabled) {
      --button-background: var(--color-primary-light);
    }
  }

  &--text {
    --button-background: transparent;
    --button-color: var(--color-primary);
    --button-border: none;

    &:hover:not(:disabled) {
      --button-background: var(--color-primary-light);
    }
  }

  // ===== States =====

  &:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
  }

  &:active:not(:disabled) {
    transform: translateY(1px);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &--loading {
    position: relative;
    color: transparent;

    &::after {
      content: '';
      position: absolute;
      width: 16px;
      height: 16px;
      border: 2px solid currentColor;
      border-radius: 50%;
      border-top-color: transparent;
      animation: button-spin 0.6s linear infinite;
    }
  }
}

@keyframes button-spin {
  to { transform: rotate(360deg); }
}
```

**TypeScript Component Interface:**

```typescript
/**
 * Button Component Configuration
 * @interface ButtonConfig
 */
interface ButtonConfig {
  /** Button variant type */
  variant: 'primary' | 'secondary' | 'outlined' | 'text';
  /** Button size */
  size: 'small' | 'medium' | 'large';
  /** Disabled state */
  disabled?: boolean;
  /** Loading state */
  loading?: boolean;
  /** Full width button */
  fullWidth?: boolean;
  /** Icon position */
  iconPosition?: 'left' | 'right';
}

/**
 * Generate button class names
 * @param config - Button configuration
 * @returns Class name string
 */
function getButtonClasses(config: ButtonConfig): string {
  const classes = ['c-button'];

  classes.push(`c-button--${config.variant}`);
  classes.push(`c-button--${config.size}`);

  if (config.loading) classes.push('c-button--loading');
  if (config.fullWidth) classes.push('c-button--full-width');

  return classes.join(' ');
}
```

---

## Versioning & Migration

### Semantic Versioning for CSS

**Description:** Version management strategy for design system CSS following semver principles.

```scss
/**
 * CSS Semantic Versioning Strategy
 * @description Version management for design system CSS
 * @pattern MAJOR.MINOR.PATCH
 * @governance All version changes require approval
 */

// Current design system version
$design-system-version: '3.2.1';

/**
 * Version Change Guidelines
 *
 * MAJOR (3.0.0 → 4.0.0) - Breaking Changes:
 * - Removing CSS classes
 * - Changing class naming structure (.btn → .c-button)
 * - Modifying existing component API
 * - Removing design tokens
 * - Changing token values significantly
 * - Breaking HTML structure requirements
 *
 * MINOR (3.1.0 → 3.2.0) - New Features:
 * - Adding new components
 * - Adding new utility classes
 * - Adding new mixins/functions
 * - Adding new design tokens
 * - Adding new component variants
 * - Backward-compatible enhancements
 *
 * PATCH (3.2.0 → 3.2.1) - Bug Fixes:
 * - Fixing visual bugs
 * - Performance improvements
 * - Documentation updates
 * - Accessibility fixes (non-breaking)
 * - Browser compatibility fixes
 */

/**
 * Deprecation Warning Mixin
 * @mixin deprecate
 * @param {String} $message - Deprecation message
 * @param {String} $version-removed - Version when removal occurs
 */
@mixin deprecate($message, $version-removed) {
  @warn "DEPRECATION WARNING: #{$message}. This will be removed in version #{$version-removed}. Current version: #{$design-system-version}";
}

/**
 * Example: Deprecating Old Button Class
 */
.btn {
  @include deprecate(
    "Use .c-button instead of .btn",
    "4.0.0"
  );

  // Temporary compatibility - extends new component
  @extend .c-button;
}

/**
 * Version-Specific Feature Flags
 * @description Enable/disable features based on version
 */
$feature-flags: (
  'css-custom-properties': true,
  'container-queries': false,
  'cascade-layers': false,
  'logical-properties': true,
  'has-selector': false
);

/**
 * Check if feature is enabled
 * @function feature-enabled
 * @param {String} $feature - Feature name
 * @returns {Boolean} Feature enabled status
 */
@function feature-enabled($feature) {
  @return map-get($feature-flags, $feature) == true;
}

/**
 * Conditional Feature Implementation
 */
@if feature-enabled('css-custom-properties') {
  :root {
    --spacing-unit: 8px;
    --color-primary: #007bff;
  }

  .component {
    padding: var(--spacing-unit);
    color: var(--color-primary);
  }
} @else {
  // Fallback for browsers without custom property support
  .component {
    padding: 8px;
    color: #007bff;
  }
}
```

### Migration Helper Utilities

```scss
/**
 * CSS Migration Utilities
 * @description Tools for gradual migration between versions
 */

/**
 * Compatibility Layer Mixin
 * @mixin compatibility-mode
 * @param {String} $from-version - Migrating from version
 * @description Creates compatibility mappings for smooth migration
 */
@mixin compatibility-mode($from-version: '2.0') {
  @if $from-version == '2.0' {
    // Map v2.0 classes to v3.0 equivalents
    .btn { @extend .c-button; }
    .btn-primary { @extend .c-button--primary; }
    .btn-secondary { @extend .c-button--secondary; }

    .card { @extend .c-card; }
    .card-header { @extend .c-card__header; }
    .card-body { @extend .c-card__body; }

    .modal { @extend .c-modal; }
    .modal-content { @extend .c-modal__content; }

    @warn "Running in compatibility mode for v2.0. Please migrate to v3.0 class names.";
  }
}

/**
 * Progressive Enhancement Helper
 * @mixin progressive-enhancement
 * @param {String} $feature - CSS feature to check
 */
@mixin progressive-enhancement($feature) {
  @if $feature == 'grid' {
    @supports (display: grid) {
      @content;
    }
  }

  @if $feature == 'custom-properties' {
    @supports (--css: variables) {
      @content;
    }
  }

  @if $feature == 'container-queries' {
    @supports (container-type: inline-size) {
      @content;
    }
  }
}

// Usage example
.layout {
  // Fallback: Flexbox layout
  display: flex;
  flex-wrap: wrap;

  // Enhancement: Grid layout where supported
  @include progressive-enhancement('grid') {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}
```

**TypeScript Migration Tools:**

```typescript
/**
 * CSS Migration Manager
 * @class MigrationManager
 * @description Manages CSS version migrations
 */
class MigrationManager {
  private currentVersion: string;
  private targetVersion: string;

  /**
   * Create migration plan
   * @param from - Current version
   * @param to - Target version
   * @returns Migration steps
   */
  createMigrationPlan(from: string, to: string): MigrationStep[] {
    const steps: MigrationStep[] = [];

    // Determine migration type
    const [fromMajor, fromMinor] = from.split('.').map(Number);
    const [toMajor, toMinor] = to.split('.').map(Number);

    if (toMajor > fromMajor) {
      // Major version migration - breaking changes
      steps.push({
        type: 'breaking',
        description: 'Update class names to new convention',
        automated: true,
        codemod: 'migrate-class-names.js'
      });

      steps.push({
        type: 'breaking',
        description: 'Update design token references',
        automated: true,
        codemod: 'migrate-tokens.js'
      });

      steps.push({
        type: 'manual',
        description: 'Review and test components',
        automated: false
      });
    }

    if (toMinor > fromMinor) {
      // Minor version migration - additive changes
      steps.push({
        type: 'additive',
        description: 'Opt-in to new features',
        automated: false
      });
    }

    return steps;
  }

  /**
   * Generate migration report
   * @param steps - Migration steps
   * @returns Markdown report
   */
  generateReport(steps: MigrationStep[]): string {
    let report = `# Migration Plan: ${this.currentVersion} → ${this.targetVersion}\n\n`;

    report += `## Summary\n`;
    report += `- Total steps: ${steps.length}\n`;
    report += `- Automated: ${steps.filter(s => s.automated).length}\n`;
    report += `- Manual: ${steps.filter(s => !s.automated).length}\n\n`;

    report += `## Steps\n\n`;
    steps.forEach((step, index) => {
      report += `### ${index + 1}. ${step.description}\n`;
      report += `**Type:** ${step.type}\n`;
      report += `**Automated:** ${step.automated ? 'Yes' : 'No'}\n`;
      if (step.codemod) {
        report += `**Codemod:** \`${step.codemod}\`\n`;
      }
      report += `\n`;
    });

    return report;
  }
}

interface MigrationStep {
  type: 'breaking' | 'additive' | 'manual';
  description: string;
  automated: boolean;
  codemod?: string;
}
```

---

## Monorepo CSS Management

### Monorepo Structure

**Description:** CSS organization and sharing strategy for monorepo environments with multiple applications.

```
enterprise-monorepo/
├── packages/
│   ├── design-system/           # Shared design system package
│   │   ├── src/
│   │   │   ├── tokens/          # Design tokens
│   │   │   │   ├── colors.scss
│   │   │   │   ├── typography.scss
│   │   │   │   └── spacing.scss
│   │   │   ├── foundation/      # Base utilities
│   │   │   │   ├── reset.scss
│   │   │   │   ├── mixins.scss
│   │   │   │   └── grid.scss
│   │   │   ├── components/      # UI components
│   │   │   │   ├── button/
│   │   │   │   ├── card/
│   │   │   │   └── modal/
│   │   │   └── index.scss       # Main entry point
│   │   ├── dist/                # Built CSS
│   │   │   ├── design-system.css
│   │   │   ├── design-system.min.css
│   │   │   └── tokens.json
│   │   ├── package.json
│   │   └── README.md
│   │
│   ├── shared-components/       # Shared React/Angular components
│   │   └── src/
│   │       └── styles/
│   │           └── component-overrides.scss
│   │
│   ├── app-customer-portal/     # Application 1
│   │   └── src/
│   │       └── styles/
│   │           ├── main.scss    # Imports design system
│   │           ├── theme.scss   # App-specific theme
│   │           └── overrides/   # Component customizations
│   │
│   ├── app-admin-dashboard/     # Application 2
│   │   └── src/
│   │       └── styles/
│   │           ├── main.scss
│   │           ├── theme.scss
│   │           └── overrides/
│   │
│   └── app-marketing-site/      # Application 3
│       └── src/
│           └── styles/
│               ├── main.scss
│               ├── theme.scss
│               └── overrides/
│
├── tools/
│   ├── build-css/               # Shared build scripts
│   └── css-linter/              # Linting configuration
│
└── package.json                 # Root package.json
```

### Shared Design System Package

```scss
/**
 * Design System Main Entry Point
 * packages/design-system/src/index.scss
 * @description Central export for the design system
 * @version 3.0.0
 */

// Design tokens (always imported first)
@import 'tokens/colors';
@import 'tokens/typography';
@import 'tokens/spacing';
@import 'tokens/shadows';
@import 'tokens/breakpoints';

// Foundation
@import 'foundation/reset';
@import 'foundation/mixins';
@import 'foundation/functions';
@import 'foundation/grid';

// Components (alphabetically)
@import 'components/button/button';
@import 'components/card/card';
@import 'components/input/input';
@import 'components/modal/modal';
@import 'components/table/table';

// Utilities
@import 'utilities/spacing';
@import 'utilities/typography';
@import 'utilities/visibility';
```

**Package Configuration:**

```json
{
  "name": "@company/design-system",
  "version": "3.2.1",
  "description": "Enterprise design system CSS",
  "main": "dist/design-system.css",
  "style": "dist/design-system.css",
  "sass": "src/index.scss",
  "files": [
    "dist",
    "src"
  ],
  "exports": {
    ".": {
      "style": "./dist/design-system.css",
      "sass": "./src/index.scss",
      "default": "./dist/design-system.css"
    },
    "./tokens": {
      "sass": "./src/tokens/index.scss",
      "json": "./dist/tokens.json"
    },
    "./components/*": {
      "sass": "./src/components/*/index.scss"
    }
  },
  "scripts": {
    "build": "npm run build:css && npm run build:tokens",
    "build:css": "sass src/index.scss dist/design-system.css --style=expanded",
    "build:css:min": "sass src/index.scss dist/design-system.min.css --style=compressed",
    "build:tokens": "node scripts/build-tokens.js",
    "lint": "stylelint 'src/**/*.scss'",
    "test": "npm run test:visual && npm run test:a11y",
    "test:visual": "backstop test",
    "test:a11y": "pa11y-ci"
  },
  "peerDependencies": {
    "sass": "^1.69.0"
  },
  "devDependencies": {
    "sass": "^1.69.0",
    "stylelint": "^15.10.0",
    "backstopjs": "^6.2.0",
    "pa11y-ci": "^3.0.0"
  }
}
```

### Application Import Strategy

```scss
/**
 * Application Main Stylesheet
 * packages/app-customer-portal/src/styles/main.scss
 * @description Imports design system and applies customizations
 */

// ===== 1. Import Design System =====
@use '@company/design-system' as ds;

// ===== 2. Import Design System Tokens =====
@use '@company/design-system/tokens' as tokens;

// ===== 3. Application-Specific Theme =====
@import 'theme';

// ===== 4. Component Overrides =====
@import 'overrides/button';
@import 'overrides/card';
@import 'overrides/navigation';

// ===== 5. Custom Application Styles =====
@import 'layouts/dashboard';
@import 'layouts/auth';
@import 'pages/home';
@import 'pages/profile';
```

**Application Theme Customization:**

```scss
/**
 * Application Theme
 * packages/app-customer-portal/src/styles/theme.scss
 * @description Brand-specific theme overrides
 */

:root {
  // Override primary brand color
  --color-primary: #1a73e8; // Google Blue
  --color-primary-hover: #1557b0;

  // App-specific colors
  --color-app-header: #1f2937;
  --color-app-sidebar: #111827;

  // Custom spacing for this app
  --app-header-height: 64px;
  --app-sidebar-width: 280px;
}

// Apply theme to design system components
.c-button--primary {
  // Automatically uses overridden --color-primary
}
```

### Shared Build Configuration

```javascript
/**
 * Shared Webpack CSS Configuration
 * tools/build-css/webpack.css.config.js
 * @description Reusable CSS build configuration for all apps
 */

const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const PostCSSPresetEnv = require('postcss-preset-env');

/**
 * Create CSS build configuration
 * @param {Object} options - Build options
 * @returns {Object} Webpack configuration
 */
function createCSSConfig(options = {}) {
  const isProduction = options.mode === 'production';

  return {
    module: {
      rules: [
        {
          test: /\.(scss|sass)$/,
          use: [
            // Extract CSS to separate files
            MiniCssExtractPlugin.loader,

            // CSS loader with modules support
            {
              loader: 'css-loader',
              options: {
                sourceMap: !isProduction,
                modules: {
                  auto: true,
                  localIdentName: isProduction
                    ? '[hash:base64:8]'
                    : '[name]__[local]--[hash:base64:5]'
                },
                importLoaders: 2
              }
            },

            // PostCSS processing
            {
              loader: 'postcss-loader',
              options: {
                sourceMap: !isProduction,
                postcssOptions: {
                  plugins: [
                    // Modern CSS features
                    PostCSSPresetEnv({
                      stage: 3,
                      features: {
                        'nesting-rules': true,
                        'custom-properties': true,
                        'custom-media-queries': true,
                        'logical-properties-and-values': true
                      },
                      autoprefixer: {
                        grid: true
                      }
                    }),

                    // PurgeCSS for production
                    ...(isProduction ? [
                      require('@fullhuman/postcss-purgecss')({
                        content: [
                          './src/**/*.{html,ts,tsx,js,jsx}',
                          './node_modules/@company/**/*.{html,ts,tsx,js,jsx}'
                        ],
                        safelist: {
                          standard: [/^c-/, /^m-/, /^o-/, /^u-/], // BEM classes
                          deep: [/modal/, /tooltip/], // Dynamic classes
                          greedy: [/data-theme$/] // Attribute selectors
                        }
                      })
                    ] : [])
                  ]
                }
              }
            },

            // SASS compilation
            {
              loader: 'sass-loader',
              options: {
                sourceMap: !isProduction,
                sassOptions: {
                  includePaths: [
                    'node_modules',
                    '../../node_modules'
                  ],
                  precision: 5,
                  outputStyle: isProduction ? 'compressed' : 'expanded'
                }
              }
            }
          ]
        }
      ]
    },

    plugins: [
      new MiniCssExtractPlugin({
        filename: isProduction
          ? 'css/[name].[contenthash:8].css'
          : 'css/[name].css',
        chunkFilename: isProduction
          ? 'css/[name].[contenthash:8].chunk.css'
          : 'css/[name].chunk.css'
      })
    ],

    optimization: {
      minimizer: [
        new CssMinimizerPlugin({
          minimizerOptions: {
            preset: [
              'default',
              {
                discardComments: { removeAll: true },
                normalizeWhitespace: true,
                colormin: true,
                minifyFontValues: true,
                minifyGradients: true
              }
            ]
          }
        })
      ]
    }
  };
}

module.exports = { createCSSConfig };
```

**Usage in Application:**

```javascript
/**
 * Application Webpack Config
 * packages/app-customer-portal/webpack.config.js
 */

const { createCSSConfig } = require('../../tools/build-css/webpack.css.config');
const { merge } = require('webpack-merge');

module.exports = (env, argv) => {
  const cssConfig = createCSSConfig({ mode: argv.mode });

  return merge(cssConfig, {
    // App-specific configuration
    entry: './src/main.ts',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: '[name].[contenthash].js'
    }
  });
};
```

---

## Team Workflows & CI/CD

### GitHub Actions CSS Pipeline

```yaml
# .github/workflows/css-pipeline.yml
# Enterprise CSS CI/CD Pipeline
name: CSS Pipeline

on:
  pull_request:
    paths:
      - 'packages/design-system/**'
      - 'packages/*/src/styles/**'
      - '.github/workflows/css-pipeline.yml'
  push:
    branches:
      - main
      - develop

# Cancel in-progress runs for same PR
concurrency:
  group: css-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # ===== Job 1: Linting =====
  lint:
    name: CSS Linting
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Stylelint
        run: npm run lint:css

      - name: Check CSS formatting
        run: npm run format:check:css

      - name: Validate design tokens
        run: npm run validate:tokens

  # ===== Job 2: Testing =====
  test:
    name: CSS Testing
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build design system
        run: npm run build --workspace=@company/design-system

      - name: Visual regression testing
        run: npm run test:visual

      - name: Accessibility testing
        run: npm run test:a11y:css

      - name: Upload visual regression results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: visual-regression-diffs
          path: backstop_data/bitmaps_test

  # ===== Job 3: Build & Bundle Analysis =====
  build:
    name: Build & Analysis
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build design system
        run: npm run build --workspace=@company/design-system

      - name: Build applications
        run: npm run build:apps

      - name: Analyze CSS bundle size
        run: npm run analyze:css

      - name: Check performance budgets
        run: npm run budget:check

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: css-bundles
          path: |
            packages/design-system/dist
            packages/*/dist/css

      - name: Comment bundle size on PR
        if: github.event_name == 'pull_request'
        uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}

  # ===== Job 4: Performance Testing =====
  performance:
    name: Performance Testing
    runs-on: ubuntu-latest
    needs: build
    timeout-minutes: 10

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: css-bundles
          path: dist

      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun

      - name: Check CSS parse time
        run: npm run test:css:parse-time

  # ===== Job 5: Publish (main branch only) =====
  publish:
    name: Publish Design System
    runs-on: ubuntu-latest
    needs: [lint, test, build, performance]
    if: github.ref == 'refs/heads/main'
    timeout-minutes: 10

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Build design system
        run: npm run build --workspace=@company/design-system

      - name: Publish to npm
        run: npm publish --workspace=@company/design-system --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

      - name: Create GitHub release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ steps.package-version.outputs.version }}
          release_name: Design System v${{ steps.package-version.outputs.version }}
          body_path: CHANGELOG.md
```

### CSS Performance Budgets

```javascript
/**
 * Performance Budget Configuration
 * .size-limit.json
 * @description Enforce CSS bundle size limits
 */
[
  {
    "name": "Design System - Full Bundle",
    "path": "packages/design-system/dist/design-system.css",
    "limit": "250 KB",
    "gzip": true
  },
  {
    "name": "Design System - Minified",
    "path": "packages/design-system/dist/design-system.min.css",
    "limit": "50 KB",
    "gzip": true
  },
  {
    "name": "Critical CSS",
    "path": "packages/design-system/dist/critical.css",
    "limit": "14 KB",
    "gzip": false
  },
  {
    "name": "App - Customer Portal",
    "path": "packages/app-customer-portal/dist/css/main.css",
    "limit": "300 KB",
    "gzip": true
  },
  {
    "name": "App - Admin Dashboard",
    "path": "packages/app-admin-dashboard/dist/css/main.css",
    "limit": "280 KB",
    "gzip": true
  }
]
```

---

## Storybook Documentation

### Storybook Configuration

```javascript
/**
 * Storybook Main Configuration
 * .storybook/main.js
 * @description Complete Storybook setup for enterprise CSS documentation
 */

module.exports = {
  // Story locations
  stories: [
    '../packages/design-system/src/**/*.stories.@(js|jsx|ts|tsx|mdx)',
    '../packages/design-system/src/**/*.docs.mdx'
  ],

  // Addons for enhanced functionality
  addons: [
    '@storybook/addon-essentials',        // Essential tools
    '@storybook/addon-a11y',              // Accessibility testing
    '@storybook/addon-design-tokens',     // Design token visualization
    '@storybook/addon-interactions',      // Interaction testing
    'storybook-addon-pseudo-states',      // Hover/focus states
    'storybook-css-modules-preset',       // CSS Modules support
    'storybook-dark-mode'                 // Dark mode toggle
  ],

  // Framework configuration
  framework: {
    name: '@storybook/html-webpack5',
    options: {}
  },

  // Feature flags
  features: {
    buildStoriesJson: true,
    cssVariables: true,
    modernInlineRender: true
  },

  // TypeScript configuration
  typescript: {
    check: true,
    reactDocgen: 'react-docgen-typescript'
  },

  // Static directories
  staticDirs: ['../public'],

  // Webpack customization
  webpackFinal: async (config) => {
    // Add SCSS support
    config.module.rules.push({
      test: /\.scss$/,
      use: ['style-loader', 'css-loader', 'sass-loader']
    });

    return config;
  }
};
```

**Storybook Preview Configuration:**

```javascript
/**
 * Storybook Preview Configuration
 * .storybook/preview.js
 * @description Global decorators, parameters, and styles
 */

import '../packages/design-system/dist/design-system.css';

// Global parameters
export const parameters = {
  // Actions configuration
  actions: { argTypesRegex: '^on[A-Z].*' },

  // Controls configuration
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/
    },
    expanded: true,
    sort: 'requiredFirst'
  },

  // Viewport configuration
  viewport: {
    viewports: {
      mobile: {
        name: 'Mobile',
        styles: { width: '375px', height: '667px' },
        type: 'mobile'
      },
      tablet: {
        name: 'Tablet',
        styles: { width: '768px', height: '1024px' },
        type: 'tablet'
      },
      desktop: {
        name: 'Desktop',
        styles: { width: '1440px', height: '900px' },
        type: 'desktop'
      },
      wide: {
        name: 'Wide Desktop',
        styles: { width: '1920px', height: '1080px' },
        type: 'desktop'
      }
    }
  },

  // Documentation configuration
  docs: {
    toc: {
      title: 'Table of Contents',
      headingSelector: 'h2, h3'
    },
    source: {
      type: 'code',
      language: 'html'
    }
  },

  // Accessibility configuration
  a11y: {
    config: {
      rules: [
        {
          id: 'color-contrast',
          enabled: true
        },
        {
          id: 'aria-required-attr',
          enabled: true
        }
      ]
    }
  },

  // Design assets integration
  design: {
    type: 'figma',
    allowFullscreen: true
  }
};

// Global decorators
export const decorators = [
  (Story) => {
    return `
      <div class="sb-container" style="padding: 2rem;">
        ${Story()}
      </div>
    `;
  }
];

// Global types
export const globalTypes = {
  theme: {
    name: 'Theme',
    description: 'Global theme for components',
    defaultValue: 'light',
    toolbar: {
      icon: 'circlehollow',
      items: [
        { value: 'light', title: 'Light', icon: 'sun' },
        { value: 'dark', title: 'Dark', icon: 'moon' },
        { value: 'high-contrast', title: 'High Contrast', icon: 'contrast' }
      ],
      dynamicTitle: true
    }
  }
};
```

### Component Story Template

```mdx
<!-- Button.stories.mdx -->
import { Meta, Story, Canvas, ArgsTable, Source, Description } from '@storybook/addon-docs';
import { Button } from './Button';

<Meta
  title="Components/Core/Button"
  component={Button}
  parameters={{
    design: {
      type: 'figma',
      url: 'https://www.figma.com/file/xxx/Design-System?node-id=123'
    },
    docs: {
      description: {
        component: 'The Button component is a fundamental UI element for triggering actions and events.'
      }
    }
  }}
  argTypes={{
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary', 'outlined', 'text'],
      description: 'Button visual variant',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'primary' }
      }
    },
    size: {
      control: { type: 'radio' },
      options: ['small', 'medium', 'large'],
      description: 'Button size',
      table: {
        type: { summary: 'string' },
        defaultValue: { summary: 'medium' }
      }
    },
    disabled: {
      control: { type: 'boolean' },
      description: 'Disabled state',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' }
      }
    },
    loading: {
      control: { type: 'boolean' },
      description: 'Loading state with spinner',
      table: {
        type: { summary: 'boolean' },
        defaultValue: { summary: 'false' }
      }
    }
  }}
/>

# Button Component

The Button component provides a clickable interface element for user interactions.

## Design Principles

- **Clarity**: Clear visual hierarchy with distinct variants
- **Accessibility**: Fully keyboard navigable with screen reader support
- **Consistency**: Follows enterprise design system guidelines
- **Flexibility**: Multiple variants and sizes for different contexts

## Usage Guidelines

### When to Use

- **Primary actions**: Main call-to-action on pages or in dialogs
- **Secondary actions**: Supporting actions with lower emphasis
- **Form submissions**: Submit or cancel form data
- **Navigation triggers**: Open dialogs, panels, or navigate

### When NOT to Use

- **Navigation between pages**: Use Link component instead
- **Toggle states**: Use Switch or Checkbox components
- **Multiple selections**: Use Checkbox or Radio groups

---

## Examples

### Primary Button

The primary button is for the main action on a page or section.

<Canvas>
  <Story name="Primary">
    {`
      <button class="c-button c-button--primary c-button--medium">
        Primary Action
      </button>
    `}
  </Story>
</Canvas>

### Secondary Button

Secondary buttons are for supporting actions with less emphasis.

<Canvas>
  <Story name="Secondary">
    {`
      <button class="c-button c-button--secondary c-button--medium">
        Secondary Action
      </button>
    `}
  </Story>
</Canvas>

### Button Sizes

Buttons come in three sizes: small, medium, and large.

<Canvas>
  <Story name="Sizes">
    {`
      <div style="display: flex; gap: 1rem; align-items: center;">
        <button class="c-button c-button--primary c-button--small">
          Small
        </button>
        <button class="c-button c-button--primary c-button--medium">
          Medium
        </button>
        <button class="c-button c-button--primary c-button--large">
          Large
        </button>
      </div>
    `}
  </Story>
</Canvas>

### Button with Icon

Buttons can include icons for better context.

<Canvas>
  <Story name="With Icon">
    {`
      <button class="c-button c-button--primary c-button--medium">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
          <path d="M8 0l8 8-8 8-8-8 8-8z"/>
        </svg>
        <span>With Icon</span>
      </button>
    `}
  </Story>
</Canvas>

### Loading State

Buttons show a loading spinner when an action is in progress.

<Canvas>
  <Story name="Loading">
    {`
      <button class="c-button c-button--primary c-button--medium c-button--loading">
        Loading...
      </button>
    `}
  </Story>
</Canvas>

### Disabled State

Disabled buttons cannot be interacted with.

<Canvas>
  <Story name="Disabled">
    {`
      <button class="c-button c-button--primary c-button--medium" disabled>
        Disabled Button
      </button>
    `}
  </Story>
</Canvas>

---

## CSS Implementation

<Source
  language="scss"
  dark
  code={`
/**
 * Button Component
 * @component c-button
 * @version 2.1.0
 */
.c-button {
  // Base styles
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  padding: var(--button-padding);
  background: var(--button-background);
  color: var(--button-color);
  border: var(--button-border, none);
  border-radius: var(--button-border-radius);
  font-size: var(--button-font-size);
  font-weight: var(--font-weight-medium);
  font-family: inherit;
  line-height: 1;
  text-decoration: none;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;

  // Variants
  &--primary {
    --button-background: var(--color-primary);
    --button-color: var(--color-primary-contrast);
  }

  &--secondary {
    --button-background: var(--color-secondary);
    --button-color: var(--color-secondary-contrast);
  }

  // Sizes
  &--small {
    --button-padding: var(--spacing-xs) var(--spacing-sm);
    --button-font-size: var(--font-size-sm);
  }

  &--medium {
    --button-padding: var(--spacing-sm) var(--spacing-md);
    --button-font-size: var(--font-size-base);
  }

  &--large {
    --button-padding: var(--spacing-md) var(--spacing-lg);
    --button-font-size: var(--font-size-lg);
  }

  // States
  &:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
  }

  &:hover:not(:disabled) {
    filter: brightness(1.1);
  }

  &:active:not(:disabled) {
    transform: translateY(1px);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
`}
/>

---

## Accessibility

### WCAG 2.1 AA Compliance

- ✅ **Color Contrast**: Meets 4.5:1 ratio for text
- ✅ **Keyboard Navigation**: Fully accessible via Tab and Enter/Space
- ✅ **Focus Indicators**: Visible 2px outline with 2px offset
- ✅ **Screen Reader**: Proper ARIA labels and states

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Tab | Focus button |
| Enter | Activate button |
| Space | Activate button |

### ARIA Attributes

```html
<button
  class="c-button c-button--primary"
  aria-label="Submit form"
  aria-disabled="false"
  aria-busy="false">
  Submit
</button>
```

---

## Browser Support

| Browser | Version |
|---------|---------|
| Chrome | Last 2 |
| Firefox | Last 2 |
| Safari | Last 2 |
| Edge | Last 2 |

---

## Props & API

<ArgsTable of={Button} />

---

## Related Components

- **Link**: For navigation between pages
- **IconButton**: Button with only an icon
- **ButtonGroup**: Group of related buttons

---

## Changelog

### Version 2.1.0 (2024-01-15)
- Added loading state with spinner
- Improved focus indicators
- Enhanced accessibility with ARIA attributes

### Version 2.0.0 (2023-12-01)
- **BREAKING**: Renamed `.btn` to `.c-button`
- Added outlined and text variants
- Implemented design tokens
- Added TypeScript interfaces

### Version 1.0.0 (2023-01-01)
- Initial release
```

---

## Legacy Migration Strategies

### Automated Migration with Codemods

```javascript
/**
 * CSS Class Migration Codemod
 * scripts/codemods/migrate-css-classes.js
 * @description Automated transformation of legacy CSS classes
 */

const postcss = require('postcss');
const fs = require('fs');
const glob = require('glob');
const path = require('path');

/**
 * Class Name Mapping (v2.0 → v3.0)
 */
const classMap = {
  // Buttons
  'btn': 'c-button',
  'btn-primary': 'c-button--primary',
  'btn-secondary': 'c-button--secondary',
  'btn-small': 'c-button--small',
  'btn-large': 'c-button--large',

  // Cards
  'card': 'c-card',
  'card-header': 'c-card__header',
  'card-title': 'c-card__title',
  'card-body': 'c-card__body',
  'card-footer': 'c-card__footer',

  // Layout
  'container': 'l-container',
  'row': 'l-grid',
  'col': 'l-grid__item',

  // Utilities
  'text-center': 'u-text-center',
  'mt-2': 'u-margin-top-md',
  'mb-3': 'u-margin-bottom-lg'
};

/**
 * Migrate CSS File
 * @param {string} filePath - Path to CSS file
 * @returns {Promise<void>}
 */
async function migrateCSS(filePath) {
  console.log(`Processing: ${filePath}`);

  const css = fs.readFileSync(filePath, 'utf8');

  const result = await postcss([
    postcss.plugin('migrate-classes', () => {
      return (root) => {
        // Update class selectors
        root.walkRules((rule) => {
          rule.selector = rule.selector.replace(
            /\.([\w-]+)/g,
            (match, className) => {
              const newClass = classMap[className];
              if (newClass) {
                console.log(`  ✓ Migrated: .${className} → .${newClass}`);
                return '.' + newClass;
              }
              return match;
            }
          );
        });

        // Update comments with deprecation notes
        root.walkComments((comment) => {
          Object.keys(classMap).forEach(oldClass => {
            if (comment.text.includes(oldClass)) {
              comment.text = `MIGRATED: ${comment.text}`;
            }
          });
        });
      };
    })
  ]).process(css, { from: filePath, to: filePath });

  fs.writeFileSync(filePath, result.css);
  console.log(`✅ Completed: ${filePath}\n`);
}

/**
 * Migrate HTML/Template Files
 * @param {string} filePath - Path to HTML file
 * @returns {void}
 */
function migrateHTML(filePath) {
  console.log(`Processing: ${filePath}`);

  let html = fs.readFileSync(filePath, 'utf8');
  let changeCount = 0;

  Object.entries(classMap).forEach(([oldClass, newClass]) => {
    const regex = new RegExp(`class="([^"]*\\b)${oldClass}(\\b[^"]*)"`, 'g');
    const newHtml = html.replace(regex, (match, before, after) => {
      changeCount++;
      console.log(`  ✓ Migrated: ${oldClass} → ${newClass}`);
      return `class="${before}${newClass}${after}"`;
    });
    html = newHtml;
  });

  if (changeCount > 0) {
    fs.writeFileSync(filePath, html);
    console.log(`✅ Completed: ${filePath} (${changeCount} changes)\n`);
  } else {
    console.log(`⊘ No changes needed: ${filePath}\n`);
  }
}

/**
 * Run Migration
 */
async function runMigration() {
  console.log('🚀 Starting CSS Migration (v2.0 → v3.0)\n');

  // Migrate CSS files
  const cssFiles = glob.sync('**/*.{css,scss}', {
    ignore: ['node_modules/**', 'dist/**', 'build/**']
  });

  console.log(`Found ${cssFiles.length} CSS files\n`);

  for (const file of cssFiles) {
    await migrateCSS(file);
  }

  // Migrate HTML/template files
  const htmlFiles = glob.sync('**/*.{html,htm,tsx,jsx}', {
    ignore: ['node_modules/**', 'dist/**', 'build/**']
  });

  console.log(`\nFound ${htmlFiles.length} HTML/template files\n`);

  for (const file of htmlFiles) {
    migrateHTML(file);
  }

  console.log('\n✨ Migration completed successfully!');
  console.log('\n📋 Next steps:');
  console.log('1. Review the changes');
  console.log('2. Run tests to ensure nothing broke');
  console.log('3. Update any custom CSS that references old classes');
  console.log('4. Commit the migrated code');
}

// Run if executed directly
if (require.main === module) {
  runMigration().catch(console.error);
}

module.exports = { migrateCSS, migrateHTML, classMap };
```

**Running the Codemod:**

```bash
# Install dependencies
npm install postcss glob

# Run migration
node scripts/codemods/migrate-css-classes.js

# Review changes
git diff

# Run tests
npm test

# Commit if all tests pass
git add .
git commit -m "chore: migrate CSS classes from v2.0 to v3.0"
```

---

## Performance & Optimization

### Performance Budget Configuration

```scss
/**
 * CSS Performance Budget
 * @description Enforced performance limits for enterprise CSS
 */

$performance-budgets: (
  // File size budgets
  'css-size-max': 250kb,           // Maximum uncompressed CSS
  'css-compressed-max': 50kb,      // Maximum gzipped CSS
  'critical-css-max': 14kb,        // Maximum critical CSS (inline)

  // Selector budgets
  'selectors-max': 4000,           // Maximum number of selectors
  'specificity-max': 30,           // Maximum specificity score
  'nesting-depth-max': 3,          // Maximum nesting levels

  // Media query budgets
  'media-queries-max': 50,         // Maximum media queries

  // Performance targets
  'parse-time-max': 50ms,          // Maximum CSS parse time
  'style-calculation-max': 100ms,  // Maximum style calculation time
  'paint-time-max': 16ms           // Maximum paint time (60fps)
);

/**
 * Check if budget is exceeded
 * @function check-budget
 * @param {String} $metric - Budget metric name
 * @param {Number} $value - Current value
 * @returns {Boolean} True if within budget
 */
@function check-budget($metric, $value) {
  $budget: map-get($performance-budgets, $metric);

  @if $budget and $value > $budget {
    @warn "Performance budget exceeded for #{$metric}: #{$value} > #{$budget}";
    @return false;
  }

  @return true;
}
```

### Critical CSS Extraction

```scss
/**
 * Critical CSS Configuration
 * @description Above-the-fold styles for fast initial render
 */

// critical.scss - Inline in <head>
// Maximum 14KB to fit in first TCP roundtrip

// 1. Reset & Normalize (minimal)
@import 'generic/reset-critical';

// 2. Typography basics
:root {
  --font-family-primary: system-ui, sans-serif;
  --font-size-base: 16px;
  --line-height-base: 1.5;
}

body {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-base);
  line-height: var(--line-height-base);
  color: var(--color-text-primary);
}

// 3. Layout (above-the-fold only)
.l-container {
  max-width: 1440px;
  margin-inline: auto;
  padding-inline: var(--spacing-md);
}

// 4. Critical components
@import 'components/header-critical';
@import 'components/hero-critical';

// 5. Utilities (frequently used)
.u-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

**Automated Critical CSS Extraction:**

```javascript
/**
 * Critical CSS Extraction
 * scripts/extract-critical-css.js
 * @description Extract above-the-fold CSS automatically
 */

const critical = require('critical');
const fs = require('fs');
const path = require('path');

/**
 * Extract Critical CSS
 * @param {Object} options - Extraction options
 */
async function extractCriticalCSS(options = {}) {
  const config = {
    // Source HTML file or URL
    src: options.src || 'dist/index.html',

    // Output directory
    target: {
      css: 'dist/css/critical.css',
      html: 'dist/index-critical.html',
      uncritical: 'dist/css/non-critical.css'
    },

    // Viewport dimensions
    dimensions: [
      { width: 375, height: 667 },   // Mobile
      { width: 768, height: 1024 },  // Tablet
      { width: 1440, height: 900 }   // Desktop
    ],

    // Inline critical CSS
    inline: true,

    // Extract settings
    extract: true,
    minify: true,

    // Performance budget
    maxSize: 14 * 1024, // 14KB

    // Ignore rules
    ignore: {
      atrule: ['@font-face'],
      rule: [/\.modal/, /\.tooltip/]
    }
  };

  try {
    const { html, css, uncritical } = await critical.generate(config);

    // Save critical CSS
    fs.writeFileSync(config.target.css, css);
    console.log(`✓ Critical CSS saved: ${css.length} bytes`);

    // Save modified HTML
    fs.writeFileSync(config.target.html, html);
    console.log(`✓ HTML with inline critical CSS saved`);

    // Save non-critical CSS
    if (uncritical) {
      fs.writeFileSync(config.target.uncritical, uncritical);
      console.log(`✓ Non-critical CSS saved`);
    }

    // Check budget
    if (css.length > config.maxSize) {
      console.warn(`⚠️  Critical CSS exceeds budget: ${css.length} > ${config.maxSize}`);
      process.exit(1);
    }

    console.log('\n✨ Critical CSS extraction completed!');
  } catch (error) {
    console.error('❌ Critical CSS extraction failed:', error);
    process.exit(1);
  }
}

// Run extraction
extractCriticalCSS();
```

### CSS Performance Monitoring

```typescript
/**
 * CSS Performance Monitor
 * @class CSSPerformanceMonitor
 * @description Track and report CSS performance metrics
 */
class CSSPerformanceMonitor {
  private metrics: PerformanceMetrics = {
    parseTime: 0,
    styleCalculation: 0,
    paintTime: 0,
    cssSize: 0,
    unusedCSS: 0,
    specificityScore: 0
  };

  /**
   * Measure CSS parsing time
   * @returns {number} Parse time in milliseconds
   */
  measureParseTime(): number {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.name.includes('.css') && entry.entryType === 'resource') {
          this.metrics.parseTime += entry.duration;
        }
      }
    });

    observer.observe({ entryTypes: ['resource'] });

    return this.metrics.parseTime;
  }

  /**
   * Measure style recalculation time
   * @returns {number} Recalc time in milliseconds
   */
  measureStyleRecalculation(): number {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.name === 'UpdateLayoutTree') {
          this.metrics.styleCalculation += entry.duration;
        }
      }
    });

    observer.observe({ entryTypes: ['measure'] });

    return this.metrics.styleCalculation;
  }

  /**
   * Calculate unused CSS percentage
   * @returns {Promise<number>} Percentage of unused CSS
   */
  async calculateUnusedCSS(): Promise<number> {
    // Use Coverage API (Chrome DevTools Protocol)
    if ('chrome' in window && (window as any).chrome.devtools) {
      try {
        const coverage = await (window as any).chrome.devtools.inspectedWindow.eval(
          'CSS.startCoverageCollection()'
        );

        // Calculate percentage
        let totalBytes = 0;
        let usedBytes = 0;

        coverage.forEach((entry: any) => {
          totalBytes += entry.text.length;
          entry.ranges.forEach((range: any) => {
            usedBytes += range.end - range.start;
          });
        });

        this.metrics.unusedCSS = ((totalBytes - usedBytes) / totalBytes) * 100;
      } catch (error) {
        console.error('Unable to calculate unused CSS:', error);
      }
    }

    return this.metrics.unusedCSS;
  }

  /**
   * Get all stylesheets and calculate total size
   * @returns {number} Total CSS size in bytes
   */
  getTotalCSSSize(): number {
    let totalSize = 0;

    Array.from(document.styleSheets).forEach((sheet) => {
      try {
        const rules = sheet.cssRules || sheet.rules;
        if (rules) {
          const cssText = Array.from(rules)
            .map((rule) => rule.cssText)
            .join('');
          totalSize += new Blob([cssText]).size;
        }
      } catch (e) {
        // Cross-origin stylesheet, skip
      }
    });

    this.metrics.cssSize = totalSize;
    return totalSize;
  }

  /**
   * Calculate average specificity score
   * @returns {number} Average specificity
   */
  calculateSpecificityScore(): number {
    let totalSpecificity = 0;
    let selectorCount = 0;

    Array.from(document.styleSheets).forEach((sheet) => {
      try {
        const rules = sheet.cssRules || sheet.rules;
        if (rules) {
          Array.from(rules).forEach((rule: any) => {
            if (rule.selectorText) {
              const specificity = this.getSpecificity(rule.selectorText);
              totalSpecificity += specificity;
              selectorCount++;
            }
          });
        }
      } catch (e) {
        // Cross-origin stylesheet, skip
      }
    });

    this.metrics.specificityScore = selectorCount > 0
      ? totalSpecificity / selectorCount
      : 0;

    return this.metrics.specificityScore;
  }

  /**
   * Calculate selector specificity
   * @param {string} selector - CSS selector
   * @returns {number} Specificity score
   */
  private getSpecificity(selector: string): number {
    // Simplified specificity calculation
    // Format: a-b-c (IDs-Classes-Elements)
    const ids = (selector.match(/#[\w-]+/g) || []).length;
    const classes = (selector.match(/\.[\w-]+/g) || []).length;
    const attrs = (selector.match(/\[[\w-]+\]/g) || []).length;
    const pseudoClasses = (selector.match(/:[\w-]+/g) || []).length;
    const elements = (selector.match(/\b[a-z][\w-]*/g) || []).length;

    return (ids * 100) + ((classes + attrs + pseudoClasses) * 10) + elements;
  }

  /**
   * Report all metrics
   * @returns {PerformanceMetrics} Complete metrics object
   */
  getMetrics(): PerformanceMetrics {
    this.getTotalCSSSize();
    this.calculateSpecificityScore();

    return this.metrics;
  }

  /**
   * Log metrics to console
   */
  logMetrics(): void {
    console.table({
      'Parse Time': `${this.metrics.parseTime.toFixed(2)}ms`,
      'Style Calculation': `${this.metrics.styleCalculation.toFixed(2)}ms`,
      'CSS Size': `${(this.metrics.cssSize / 1024).toFixed(2)}KB`,
      'Unused CSS': `${this.metrics.unusedCSS.toFixed(2)}%`,
      'Avg Specificity': this.metrics.specificityScore.toFixed(2)
    });
  }

  /**
   * Send metrics to analytics
   * @param {string} endpoint - Analytics endpoint
   */
  async reportMetrics(endpoint: string): Promise<void> {
    const metrics = this.getMetrics();

    try {
      await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'css-performance',
          timestamp: Date.now(),
          metrics
        })
      });

      console.log('✓ Metrics reported successfully');
    } catch (error) {
      console.error('✗ Failed to report metrics:', error);
    }
  }
}

interface PerformanceMetrics {
  parseTime: number;
  styleCalculation: number;
  paintTime: number;
  cssSize: number;
  unusedCSS: number;
  specificityScore: number;
}

// Export for use
export { CSSPerformanceMonitor };

// Usage example
const monitor = new CSSPerformanceMonitor();
monitor.measureParseTime();
monitor.logMetrics();
monitor.reportMetrics('/api/analytics/css-performance');
```

---

## Summary

This Enterprise CSS Patterns Library provides comprehensive, production-ready patterns for building and maintaining CSS at scale. All examples include:

- ✅ **Swagger documentation** with detailed descriptions
- ✅ **TypeScript interfaces** for type safety
- ✅ **Complete code examples** ready to use
- ✅ **Design tokens** using CSS custom properties
- ✅ **WCAG 2.1 AA accessibility** compliance
- ✅ **Performance metrics** and optimization
- ✅ **Migration guides** and codemods

**Total Coverage:**
- 10 major architectural patterns
- 50+ code examples
- Complete governance framework
- Full CI/CD pipeline
- Storybook documentation system
- Automated migration tools
- Performance monitoring
