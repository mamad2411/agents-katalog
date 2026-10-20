---
name: CSS Methodologies Patterns Library
description: Comprehensive patterns for BEM, OOCSS, SMACSS, ITCSS, and CUBE CSS with selection guides and implementation strategies
category: architecture
version: 1.0.0
keywords: [bem, oocss, smacss, itcss, cube-css, css-architecture, naming-conventions, scalable-css, methodologies]
---

# CSS Methodologies Patterns Library

A complete guide to CSS naming conventions and architectural methodologies for building scalable, maintainable stylesheets. This skill covers BEM, OOCSS, SMACSS, ITCSS, CUBE CSS, and provides selection criteria for choosing the right methodology.

## Table of Contents

1. [BEM (Block Element Modifier)](#bem-block-element-modifier)
2. [OOCSS (Object-Oriented CSS)](#oocss-object-oriented-css)
3. [SMACSS (Scalable and Modular Architecture)](#smacss-scalable-and-modular-architecture)
4. [ITCSS (Inverted Triangle CSS)](#itcss-inverted-triangle-css)
5. [CUBE CSS (Composition Utility Block Exception)](#cube-css-composition-utility-block-exception)
6. [Methodology Comparison & Selection](#methodology-comparison--selection)
7. [Implementation Strategies](#implementation-strategies)
8. [Team Adoption & Training](#team-adoption--training)

---

## BEM (Block Element Modifier)

### Overview

**Description:** BEM is a component-based approach that creates clear relationships between HTML and CSS using a strict naming convention.

**Pattern:** `.block__element--modifier`

**Best For:**
- Component libraries
- React/Vue/Angular applications
- Teams new to CSS methodologies
- Projects requiring clear component boundaries

### Core Patterns

```scss
/**
 * BEM Naming Convention
 * @description Complete BEM pattern with all variations
 * @accessibility WCAG 2.1 AA compliant
 */

/* ===== Basic BEM Structure ===== */

/**
 * Block: Standalone entity that is meaningful on its own
 * @block card
 * @description Container for content with header, body, footer
 */
.card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

/**
 * Element: Part of a block that has no standalone meaning
 * @element card__header
 * @parent card
 * @description Header section of the card
 */
.card__header {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card__title {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.card__actions {
  display: flex;
  gap: var(--spacing-xs);
}

.card__body {
  padding: var(--spacing-md);
}

.card__footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
}

/**
 * Modifier: Variation or state of a block or element
 * @modifier card--elevated
 * @description Card with enhanced shadow for emphasis
 */
.card--elevated {
  box-shadow: var(--shadow-lg);
}

.card--interactive {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-xl);
  }
}

.card--compact {
  .card__header,
  .card__body,
  .card__footer {
    padding: var(--spacing-sm);
  }
}

/**
 * Element Modifier
 * @modifier card__header--colored
 * @description Colored header variant
 */
.card__header--primary {
  background: var(--color-primary);
  color: var(--color-primary-contrast);
}

.card__header--dark {
  background: var(--color-surface-dark);
  color: var(--color-text-dark);
}
```

### Advanced BEM Patterns

```scss
/**
 * Product Card - Complete BEM Example
 * @component product-card
 * @description E-commerce product card with all BEM patterns
 */
.product-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

  /* ===== Elements ===== */

  &__image-wrapper {
    position: relative;
    padding-top: 75%; // 4:3 aspect ratio
    background: var(--color-surface-secondary);
  }

  &__image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  &__badge {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 4px 8px;
    background: var(--color-error);
    color: white;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;

    /* Badge modifiers */
    &--new {
      background: var(--color-success);
    }

    &--sale {
      background: var(--color-warning);
    }

    &--featured {
      background: var(--color-primary);
    }
  }

  &__content {
    padding: 16px;
  }

  &__category {
    font-size: 12px;
    color: var(--color-text-tertiary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0 0 8px;
  }

  &__title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 8px;
    color: var(--color-text-primary);

    /* Title modifiers */
    &--truncate {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    &--clamp-2 {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }

  &__description {
    color: var(--color-text-secondary);
    font-size: 14px;
    line-height: 1.5;
    margin: 0 0 12px;
  }

  &__rating {
    display: flex;
    align-items: center;
    gap: 4px;
    margin: 0 0 12px;
  }

  &__stars {
    display: flex;
    gap: 2px;
  }

  &__star {
    width: 16px;
    height: 16px;
    color: var(--color-warning);

    &--empty {
      color: var(--color-border);
    }
  }

  &__rating-count {
    font-size: 12px;
    color: var(--color-text-tertiary);
    margin-left: 4px;
  }

  &__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-top: 1px solid var(--color-border);
  }

  &__price {
    font-size: 20px;
    font-weight: bold;
    color: var(--color-text-primary);

    /* Price modifiers */
    &--discounted {
      color: var(--color-error);
    }
  }

  &__price-original {
    font-size: 14px;
    color: var(--color-text-tertiary);
    text-decoration: line-through;
    margin-left: 8px;
  }

  &__button {
    padding: 8px 16px;
    background: var(--color-primary);
    color: var(--color-primary-contrast);
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;

    &:hover:not(&--disabled) {
      background: var(--color-primary-hover);
      transform: translateY(-1px);
    }

    &:active:not(&--disabled) {
      transform: translateY(0);
    }

    &--secondary {
      background: var(--color-secondary);
      color: var(--color-secondary-contrast);

      &:hover {
        background: var(--color-secondary-hover);
      }
    }

    &--disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }

  /* ===== Block Modifiers ===== */

  &--horizontal {
    display: flex;

    .product-card__image-wrapper {
      flex: 0 0 200px;
      padding-top: 0;
      height: 200px;
    }

    .product-card__content {
      flex: 1;
    }

    .product-card__footer {
      border-top: none;
      border-left: 1px solid var(--color-border);
      flex-direction: column;
      justify-content: center;
    }
  }

  &--featured {
    border: 2px solid var(--color-primary);

    .product-card__badge {
      background: var(--color-primary);
    }
  }

  &--out-of-stock {
    opacity: 0.6;
    position: relative;

    &::after {
      content: 'Out of Stock';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(0, 0, 0, 0.8);
      color: white;
      padding: 12px 24px;
      border-radius: 4px;
      font-weight: 600;
    }
  }
}
```

### BEM with JavaScript

```scss
/**
 * BEM JavaScript Hooks
 * @description Separating styling from JavaScript selectors
 * @convention Use .js- prefix for JavaScript hooks
 */

/* CSS for styling - Uses BEM classes */
.accordion {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.accordion__item {
  border-bottom: 1px solid var(--color-border);

  &:last-child {
    border-bottom: none;
  }

  /* State modifier */
  &--active {
    .accordion__content {
      max-height: 500px;
    }

    .accordion__icon {
      transform: rotate(180deg);
    }
  }
}

.accordion__trigger {
  width: 100%;
  padding: var(--spacing-md);
  background: var(--color-surface);
  border: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: background 0.2s ease;

  &:hover {
    background: var(--color-surface-hover);
  }
}

.accordion__title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  text-align: left;
}

.accordion__icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.accordion__content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.accordion__content-inner {
  padding: var(--spacing-md);
}
```

**JavaScript Implementation:**

```typescript
/**
 * Accordion Component
 * @description JavaScript interaction using .js- hooks
 */

class Accordion {
  private accordion: HTMLElement;
  private items: NodeListOf<HTMLElement>;

  constructor(element: HTMLElement) {
    this.accordion = element;
    this.items = element.querySelectorAll('.js-accordion-item');
    this.init();
  }

  /**
   * Initialize accordion
   */
  private init(): void {
    this.items.forEach((item) => {
      const trigger = item.querySelector('.js-accordion-trigger');

      trigger?.addEventListener('click', () => {
        this.toggle(item);
      });
    });
  }

  /**
   * Toggle accordion item
   * @param item - Accordion item element
   */
  private toggle(item: HTMLElement): void {
    const isActive = item.classList.contains('accordion__item--active');

    // Close all items if needed
    if (!this.accordion.hasAttribute('data-allow-multiple')) {
      this.closeAll();
    }

    // Toggle current item
    if (isActive) {
      item.classList.remove('accordion__item--active');
    } else {
      item.classList.add('accordion__item--active');
    }
  }

  /**
   * Close all accordion items
   */
  private closeAll(): void {
    this.items.forEach((item) => {
      item.classList.remove('accordion__item--active');
    });
  }
}

// Initialize all accordions
document.querySelectorAll('.js-accordion').forEach((element) => {
  new Accordion(element as HTMLElement);
});
```

**HTML:**

```html
<!-- BEM with JavaScript Hooks -->
<div class="accordion js-accordion" data-allow-multiple="false">
  <div class="accordion__item js-accordion-item">
    <button class="accordion__trigger js-accordion-trigger">
      <span class="accordion__title">What is BEM?</span>
      <span class="accordion__icon">▼</span>
    </button>
    <div class="accordion__content">
      <div class="accordion__content-inner">
        BEM stands for Block Element Modifier, a naming convention for CSS classes.
      </div>
    </div>
  </div>

  <div class="accordion__item js-accordion-item">
    <button class="accordion__trigger js-accordion-trigger">
      <span class="accordion__title">Why use BEM?</span>
      <span class="accordion__icon">▼</span>
    </button>
    <div class="accordion__content">
      <div class="accordion__content-inner">
        BEM provides a clear structure and prevents naming collisions.
      </div>
    </div>
  </div>
</div>
```

### BEM TypeScript Interface

```typescript
/**
 * BEM Component Configuration
 * @interface BEMComponentConfig
 * @description Type-safe BEM component structure
 */
interface BEMComponentConfig {
  /** Block name */
  block: string;

  /** Optional namespace prefix */
  namespace?: string;

  /** Elements within the block */
  elements: BEMElement[];

  /** Block modifiers */
  modifiers: BEMModifier[];

  /** Component metadata */
  metadata: {
    version: string;
    status: 'stable' | 'beta' | 'deprecated';
    accessibility: AccessibilityLevel;
  };
}

interface BEMElement {
  /** Element name */
  name: string;

  /** Whether element is required */
  required: boolean;

  /** Element description */
  description: string;

  /** Element modifiers */
  modifiers?: BEMModifier[];
}

interface BEMModifier {
  /** Modifier name */
  name: string;

  /** Modifier type */
  type: 'visual' | 'size' | 'state' | 'layout';

  /** Allowed values (if applicable) */
  values?: string[];

  /** Modifier description */
  description: string;
}

type AccessibilityLevel = 'A' | 'AA' | 'AAA';

/**
 * BEM Class Name Generator
 * @function bemClass
 * @description Generate BEM class names programmatically
 *
 * @param block - Block name
 * @param element - Optional element name
 * @param modifier - Optional modifier name or object
 * @param namespace - Optional namespace prefix
 * @returns Complete BEM class name
 *
 * @example
 * bemClass('card') // 'card'
 * bemClass('card', 'header') // 'card__header'
 * bemClass('card', null, 'featured') // 'card--featured'
 * bemClass('card', 'title', 'large') // 'card__title--large'
 * bemClass('card', null, null, 'ui') // 'ui-card'
 */
function bemClass(
  block: string,
  element?: string | null,
  modifier?: string | string[] | null,
  namespace?: string
): string {
  let className = namespace ? `${namespace}-${block}` : block;

  if (element) {
    className += `__${element}`;
  }

  if (modifier) {
    if (Array.isArray(modifier)) {
      // Multiple modifiers
      modifier.forEach((mod) => {
        className += ` ${className}--${mod}`;
      });
    } else {
      className += `--${modifier}`;
    }
  }

  return className;
}

// Usage examples
const cardClass = bemClass('card'); // 'card'
const headerClass = bemClass('card', 'header'); // 'card__header'
const featuredClass = bemClass('card', null, 'featured'); // 'card--featured'
const titleClass = bemClass('card', 'title', 'large'); // 'card__title--large'
const multipleModifiers = bemClass('card', null, ['featured', 'interactive']); // 'card--featured card--interactive'
const namespacedClass = bemClass('card', null, null, 'ui'); // 'ui-card'
```

---

## OOCSS (Object-Oriented CSS)

### Overview

**Description:** OOCSS separates structure from skin and container from content, promoting reusability through object-based patterns.

**Core Principles:**
1. Separate structure from skin
2. Separate container from content

**Best For:**
- Large-scale applications
- Design systems
- Teams familiar with OOP
- Projects requiring maximum reusability

### Core Patterns

```css
/**
 * OOCSS Principle 1: Separate Structure from Skin
 * @description Structure defines layout, skin defines appearance
 * @pattern Create base objects, extend with skin classes
 */

/* ===== Structure Objects ===== */

/**
 * Media Object
 * @object media
 * @description Flexible media object for images + content
 * @accessibility Semantic HTML recommended
 */
.media {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
}

.media-figure {
  flex-shrink: 0;
}

.media-body {
  flex: 1;
  min-width: 0; /* Prevent overflow */
}

/**
 * Stack Object
 * @object stack
 * @description Vertical spacing between elements
 */
.stack > * + * {
  margin-top: var(--stack-space, var(--spacing-md));
}

.stack--small > * + * {
  margin-top: var(--spacing-sm);
}

.stack--large > * + * {
  margin-top: var(--spacing-lg);
}

/**
 * Cluster Object
 * @object cluster
 * @description Horizontal grouping with wrapping
 */
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--cluster-gap, var(--spacing-md));
  align-items: center;
}

/* ===== Skin Objects ===== */

/**
 * Box Skin
 * @object box
 * @description Visual container styling
 */
.box {
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  background: var(--color-surface);
}

.box--primary {
  background: var(--color-primary);
  color: var(--color-primary-contrast);
}

.box--secondary {
  background: var(--color-secondary);
  color: var(--color-secondary-contrast);
}

.box--bordered {
  border: 2px solid var(--color-border);
  background: transparent;
}

.box--shadow {
  box-shadow: var(--shadow-md);
}

/**
 * Text Skin
 * @object text
 * @description Text styling variations
 */
.text--primary {
  color: var(--color-text-primary);
}

.text--secondary {
  color: var(--color-text-secondary);
}

.text--muted {
  color: var(--color-text-tertiary);
}

.text--success {
  color: var(--color-success);
}

.text--error {
  color: var(--color-error);
}

/* ===== OOCSS Composition ===== */

/**
 * Combining Structure and Skin
 * @example Using media object with box skin
 */
<div class="media box box--bordered">
  <div class="media-figure">
    <img src="avatar.jpg" alt="User" />
  </div>
  <div class="media-body">
    <h3>John Doe</h3>
    <p class="text--secondary">Software Engineer</p>
  </div>
</div>
```

### OOCSS Principle 2: Separate Container from Content

```css
/**
 * Content-Independent Styling
 * @description Components should look the same regardless of container
 */

/* ❌ BAD: Location-dependent styling */
.sidebar h3 {
  font-size: 16px;
  color: #333;
}

.content h3 {
  font-size: 18px;
  color: #000;
}

/* ✅ GOOD: Content-independent styling */
.heading--primary {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.heading--secondary {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

/* Use anywhere without location dependency */
<div class="sidebar">
  <h3 class="heading--secondary">Sidebar Title</h3>
</div>

<div class="content">
  <h3 class="heading--primary">Main Title</h3>
</div>
```

### OOCSS Layout Objects

```css
/**
 * Layout Objects
 * @description Reusable layout patterns
 */

/* Container Object */
.container {
  width: 100%;
  max-width: var(--container-width, 1200px);
  margin-inline: auto;
  padding-inline: var(--container-padding, var(--spacing-md));
}

.container--narrow {
  --container-width: 800px;
}

.container--wide {
  --container-width: 1400px;
}

/* Grid Object */
.grid {
  display: grid;
  gap: var(--grid-gap, var(--spacing-md));
}

.grid--2cols {
  grid-template-columns: repeat(2, 1fr);
}

.grid--3cols {
  grid-template-columns: repeat(3, 1fr);
}

.grid--4cols {
  grid-template-columns: repeat(4, 1fr);
}

.grid--responsive {
  grid-template-columns: repeat(auto-fit, minmax(var(--grid-min, 250px), 1fr));
}

/* Flexbox Object */
.flex {
  display: flex;
  gap: var(--flex-gap, var(--spacing-md));
}

.flex--center {
  align-items: center;
  justify-content: center;
}

.flex--between {
  justify-content: space-between;
  align-items: center;
}

.flex--column {
  flex-direction: column;
}

.flex--wrap {
  flex-wrap: wrap;
}
```

### OOCSS TypeScript Pattern

```typescript
/**
 * OOCSS Component System
 * @description Type-safe OOCSS object composition
 */

interface OOCSSObject {
  /** Object type */
  type: 'structure' | 'skin' | 'layout';

  /** Object name */
  name: string;

  /** CSS classes */
  classes: string[];

  /** Can be composed with */
  composable: string[];
}

/**
 * OOCSS Class Builder
 * @class OOCSSBuilder
 * @description Build OOCSS class combinations
 */
class OOCSSBuilder {
  private classes: Set<string> = new Set();

  /**
   * Add structure class
   * @param structure - Structure object name
   * @returns Builder instance for chaining
   */
  structure(structure: 'media' | 'stack' | 'cluster' | 'grid' | 'flex'): this {
    this.classes.add(structure);
    return this;
  }

  /**
   * Add skin class
   * @param skin - Skin object name and variant
   * @returns Builder instance for chaining
   */
  skin(skin: string): this {
    this.classes.add(skin);
    return this;
  }

  /**
   * Add layout class
   * @param layout - Layout object name
   * @returns Builder instance for chaining
   */
  layout(layout: string): this {
    this.classes.add(layout);
    return this;
  }

  /**
   * Build final class string
   * @returns Space-separated class names
   */
  build(): string {
    return Array.from(this.classes).join(' ');
  }
}

// Usage
const cardClasses = new OOCSSBuilder()
  .structure('media')
  .skin('box box--bordered')
  .build();

console.log(cardClasses); // 'media box box--bordered'
```

---

## SMACSS (Scalable and Modular Architecture)

### Overview

**Description:** SMACSS categorizes CSS rules into five types: Base, Layout, Module, State, and Theme.

**Categories:**
1. **Base** - Default styles
2. **Layout** - Major page sections
3. **Module** - Reusable components
4. **State** - State-based styles
5. **Theme** - Color schemes and theming

**Best For:**
- Large applications
- Multi-theme projects
- Teams needing clear categorization
- Projects with complex state management

### Category 1: Base Rules

```css
/**
 * SMACSS Base Rules
 * @category base
 * @description Default element styles without classes
 */

/* ===== Reset & Normalize ===== */
html {
  box-sizing: border-box;
  font-size: 16px;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}

body {
  margin: 0;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.5;
  color: var(--color-text-primary);
  background: var(--color-background);
}

/* ===== Typography Base ===== */
h1, h2, h3, h4, h5, h6 {
  margin: 0 0 0.5em;
  font-weight: 600;
  line-height: 1.2;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.75rem; }
h4 { font-size: 1.5rem; }
h5 { font-size: 1.25rem; }
h6 { font-size: 1rem; }

p {
  margin: 0 0 1em;
}

/* ===== Links Base ===== */
a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.2s ease;

  &:hover {
    color: var(--color-primary-hover);
    text-decoration: underline;
  }

  &:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
  }
}

/* ===== Forms Base ===== */
button, input, select, textarea {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
}

button {
  cursor: pointer;
}

/* ===== Images Base ===== */
img {
  max-width: 100%;
  height: auto;
  display: block;
}
```

### Category 2: Layout Rules

```scss
/**
 * SMACSS Layout Rules
 * @category layout
 * @description Major page sections
 * @convention Prefix with .l- or #
 */

/* ===== Main Layout Structure ===== */

/**
 * Header Layout
 * @layout l-header
 * @description Fixed main header
 */
.l-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--header-height, 60px);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  z-index: var(--z-header, 100);

  &.is-scrolled {
    box-shadow: var(--shadow-sm);
  }
}

/**
 * Sidebar Layout
 * @layout l-sidebar
 * @description Fixed sidebar navigation
 */
.l-sidebar {
  position: fixed;
  left: 0;
  top: var(--header-height, 60px);
  width: var(--sidebar-width, 250px);
  height: calc(100vh - var(--header-height, 60px));
  background: var(--color-surface-secondary);
  border-right: 1px solid var(--color-border);
  overflow-y: auto;
  transition: transform 0.3s ease;

  &.is-collapsed {
    width: var(--sidebar-width-collapsed, 60px);
  }

  @media (max-width: 768px) {
    transform: translateX(-100%);

    &.is-open {
      transform: translateX(0);
    }
  }
}

/**
 * Main Content Layout
 * @layout l-main
 * @description Main content area
 */
.l-main {
  margin-top: var(--header-height, 60px);
  margin-left: var(--sidebar-width, 250px);
  min-height: calc(100vh - var(--header-height, 60px));
  padding: var(--spacing-lg);
  transition: margin-left 0.3s ease;

  &.has-collapsed-sidebar {
    margin-left: var(--sidebar-width-collapsed, 60px);
  }

  @media (max-width: 768px) {
    margin-left: 0;
  }
}

/**
 * Footer Layout
 * @layout l-footer
 * @description Site footer
 */
.l-footer {
  margin-left: var(--sidebar-width, 250px);
  padding: var(--spacing-xl) var(--spacing-lg);
  background: var(--color-surface-secondary);
  border-top: 1px solid var(--color-border);
}

/* ===== Grid Layout System ===== */
.l-grid {
  display: grid;
  gap: var(--spacing-md);

  &--2cols {
    grid-template-columns: repeat(2, 1fr);
  }

  &--3cols {
    grid-template-columns: repeat(3, 1fr);
  }

  &--sidebar-main {
    grid-template-columns: 300px 1fr;
  }

  @media (max-width: 768px) {
    &--2cols,
    &--3cols,
    &--sidebar-main {
      grid-template-columns: 1fr;
    }
  }
}
```

### Category 3: Module Rules

```scss
/**
 * SMACSS Module Rules
 * @category module
 * @description Reusable components
 * @convention No prefix required
 */

/* ===== Button Module ===== */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary);
  color: var(--color-primary-contrast);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover:not(.is-disabled) {
    background: var(--color-primary-hover);
    transform: translateY(-1px);
  }

  &:active:not(.is-disabled) {
    transform: translateY(0);
  }

  /* Button variants */
  &--secondary {
    background: var(--color-secondary);
    color: var(--color-secondary-contrast);

    &:hover:not(.is-disabled) {
      background: var(--color-secondary-hover);
    }
  }

  &--outline {
    background: transparent;
    border: 2px solid var(--color-primary);
    color: var(--color-primary);

    &:hover:not(.is-disabled) {
      background: var(--color-primary);
      color: var(--color-primary-contrast);
    }
  }

  /* Button sizes */
  &--small {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: var(--font-size-sm);
  }

  &--large {
    padding: var(--spacing-md) var(--spacing-lg);
    font-size: var(--font-size-lg);
  }
}

/* ===== Navigation Module ===== */
.nav {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: var(--spacing-sm);

  &--vertical {
    flex-direction: column;
  }

  &--horizontal {
    flex-direction: row;
  }
}

.nav-item {
  /* Nav item styles */
}

.nav-link {
  display: block;
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--color-text-primary);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;

  &:hover {
    background: var(--color-surface-hover);
    color: var(--color-primary);
  }

  &.is-active {
    background: var(--color-primary-light);
    color: var(--color-primary);
    font-weight: 500;
  }
}

/* ===== Card Module ===== */
.card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);

  &--bordered {
    border: 1px solid var(--color-border);
    box-shadow: none;
  }

  &--elevated {
    box-shadow: var(--shadow-md);
  }
}

.card-header {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

.card-body {
  padding: var(--spacing-md);
}

.card-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border);
  background: var(--color-surface-secondary);
}
```

### Category 4: State Rules

```css
/**
 * SMACSS State Rules
 * @category state
 * @description State-based styles
 * @convention Prefix with .is- or data-state
 * @important Use !important to ensure state overrides
 */

/* ===== Visibility States ===== */
.is-hidden {
  display: none !important;
}

.is-visible {
  display: block !important;
}

.is-visually-hidden {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}

/* ===== Interaction States ===== */
.is-disabled {
  opacity: 0.5 !important;
  pointer-events: none !important;
  cursor: not-allowed !important;
}

.is-loading {
  position: relative !important;
  pointer-events: none !important;
  color: transparent !important;
}

.is-loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border: 2px solid currentColor;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

.is-active {
  background: var(--color-primary-light) !important;
  color: var(--color-primary) !important;
}

.is-selected {
  background: var(--color-primary) !important;
  color: var(--color-primary-contrast) !important;
}

/* ===== Status States ===== */
.is-success {
  border-color: var(--color-success) !important;
  background: var(--color-success-light) !important;
}

.is-warning {
  border-color: var(--color-warning) !important;
  background: var(--color-warning-light) !important;
}

.is-error {
  border-color: var(--color-error) !important;
  background: var(--color-error-light) !important;
}

/* ===== Collapse States ===== */
.is-expanded {
  max-height: 1000px !important;
}

.is-collapsed {
  max-height: 0 !important;
  overflow: hidden !important;
}

/* ===== Open/Close States ===== */
.is-open {
  display: block !important;
}

.is-closed {
  display: none !important;
}
```

### Category 5: Theme Rules

```css
/**
 * SMACSS Theme Rules
 * @category theme
 * @description Color schemes and visual themes
 * @convention Prefix with .theme- or data-theme
 */

/* ===== Light Theme (Default) ===== */
:root,
[data-theme="light"] {
  --color-background: #ffffff;
  --color-surface: #ffffff;
  --color-surface-secondary: #f9fafb;
  --color-surface-hover: #f3f4f6;

  --color-text-primary: #1f2937;
  --color-text-secondary: #6b7280;
  --color-text-tertiary: #9ca3af;

  --color-border: #e5e7eb;
  --color-divider: #d1d5db;

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}

/* ===== Dark Theme ===== */
[data-theme="dark"] {
  --color-background: #0f172a;
  --color-surface: #1e293b;
  --color-surface-secondary: #334155;
  --color-surface-hover: #475569;

  --color-text-primary: #f1f5f9;
  --color-text-secondary: #cbd5e1;
  --color-text-tertiary: #94a3b8;

  --color-border: #334155;
  --color-divider: #475569;

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
}

/* ===== High Contrast Theme ===== */
[data-theme="high-contrast"] {
  --color-background: #000000;
  --color-surface: #000000;
  --color-surface-secondary: #1a1a1a;

  --color-text-primary: #ffffff;
  --color-text-secondary: #ffffff;
  --color-text-tertiary: #cccccc;

  --color-border: #ffffff;
  --color-divider: #ffffff;

  --color-primary: #ffff00;
  --color-primary-contrast: #000000;
}

/* ===== Brand Themes ===== */
[data-theme="brand-blue"] {
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-primary-light: #dbeafe;
  --color-primary-contrast: #ffffff;
}

[data-theme="brand-green"] {
  --color-primary: #10b981;
  --color-primary-hover: #059669;
  --color-primary-light: #d1fae5;
  --color-primary-contrast: #ffffff;
}
```

---

## ITCSS (Inverted Triangle CSS)

### Overview

**Description:** ITCSS organizes CSS in layers from generic to explicit, managing specificity through layer ordering.

**7 Layers (Generic → Specific):**
1. **Settings** - Variables and configuration
2. **Tools** - Mixins and functions
3. **Generic** - Reset and normalize
4. **Elements** - Base HTML elements
5. **Objects** - Layout patterns
6. **Components** - UI components
7. **Utilities** - Helper classes

**Best For:**
- Enterprise applications
- Design systems
- Large teams
- Long-term maintainability

### Layer 1: Settings

```scss
/**
 * ITCSS Layer 1: Settings
 * @layer settings
 * @description Global variables and configuration
 * @no-output This layer generates no CSS
 */

/* ===== Color Settings ===== */
$color-primary: #3b82f6;
$color-primary-hover: #2563eb;
$color-primary-light: #dbeafe;

$color-secondary: #6b7280;
$color-success: #10b981;
$color-warning: #f59e0b;
$color-error: #ef4444;

/* ===== Typography Settings ===== */
$font-family-primary: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
$font-family-mono: 'SF Mono', Monaco, 'Cascadia Code', monospace;

$font-size-xs: 0.75rem;   // 12px
$font-size-sm: 0.875rem;  // 14px
$font-size-base: 1rem;    // 16px
$font-size-lg: 1.125rem;  // 18px
$font-size-xl: 1.25rem;   // 20px

$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;

/* ===== Spacing Settings ===== */
$spacing-unit: 8px;

$spacing-xs: $spacing-unit * 0.5;  // 4px
$spacing-sm: $spacing-unit * 1;    // 8px
$spacing-md: $spacing-unit * 2;    // 16px
$spacing-lg: $spacing-unit * 3;    // 24px
$spacing-xl: $spacing-unit * 4;    // 32px
$spacing-2xl: $spacing-unit * 6;   // 48px

/* ===== Breakpoint Settings ===== */
$breakpoint-sm: 640px;
$breakpoint-md: 768px;
$breakpoint-lg: 1024px;
$breakpoint-xl: 1280px;
$breakpoint-2xl: 1536px;

/* ===== Border Radius Settings ===== */
$radius-sm: 4px;
$radius-md: 8px;
$radius-lg: 12px;
$radius-xl: 16px;
$radius-full: 9999px;

/* ===== Shadow Settings ===== */
$shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
$shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
$shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
$shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);

/* ===== Z-Index Settings ===== */
$z-dropdown: 1000;
$z-sticky: 1020;
$z-fixed: 1030;
$z-modal-backdrop: 1040;
$z-modal: 1050;
$z-popover: 1060;
$z-tooltip: 1070;
```

### Layer 2: Tools

```scss
/**
 * ITCSS Layer 2: Tools
 * @layer tools
 * @description Mixins and functions
 * @no-output This layer generates no CSS
 */

/* ===== Spacing Function ===== */
@function spacing($level) {
  @return $spacing-unit * $level;
}

/* ===== Responsive Mixin ===== */
@mixin respond-to($breakpoint) {
  @media (min-width: $breakpoint) {
    @content;
  }
}

/* ===== Truncate Mixin ===== */
@mixin truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ===== Visually Hidden Mixin ===== */
@mixin visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* ===== Focus Ring Mixin ===== */
@mixin focus-ring($offset: 2px) {
  &:focus-visible {
    outline: 2px solid $color-primary;
    outline-offset: $offset;
  }
}

/* ===== Aspect Ratio Mixin ===== */
@mixin aspect-ratio($width, $height) {
  position: relative;

  &::before {
    content: '';
    display: block;
    padding-top: ($height / $width) * 100%;
  }

  > * {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
}
```

### Layer 3: Generic

```css
/**
 * ITCSS Layer 3: Generic
 * @layer generic
 * @description Reset and normalize styles
 */

* {
  box-sizing: border-box;
}

html, body, div, span, applet, object, iframe,
h1, h2, h3, h4, h5, h6, p, blockquote, pre,
a, abbr, acronym, address, big, cite, code,
del, dfn, em, img, ins, kbd, q, s, samp,
small, strike, strong, sub, sup, tt, var,
b, u, i, center,
dl, dt, dd, ol, ul, li,
fieldset, form, label, legend,
table, caption, tbody, tfoot, thead, tr, th, td,
article, aside, canvas, details, embed,
figure, figcaption, footer, header, hgroup,
menu, nav, output, ruby, section, summary,
time, mark, audio, video {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}

article, aside, details, figcaption, figure,
footer, header, hgroup, menu, nav, section {
  display: block;
}

ol, ul {
  list-style: none;
}

blockquote, q {
  quotes: none;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
}
```

### Layer 4: Elements

```scss
/**
 * ITCSS Layer 4: Elements
 * @layer elements
 * @description Base HTML element styles (no classes)
 */

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: $font-family-primary;
  font-size: $font-size-base;
  font-weight: $font-weight-normal;
  line-height: 1.5;
  color: var(--color-text-primary, #1f2937);
  background: var(--color-background, #ffffff);
}

h1, h2, h3, h4, h5, h6 {
  margin: 0 0 spacing(2);
  font-weight: $font-weight-semibold;
  line-height: 1.2;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.75rem; }
h4 { font-size: 1.5rem; }
h5 { font-size: 1.25rem; }
h6 { font-size: 1rem; }

p {
  margin: 0 0 spacing(2);
}

a {
  color: $color-primary;
  text-decoration: none;
  transition: color 0.2s ease;

  &:hover {
    color: $color-primary-hover;
    text-decoration: underline;
  }

  @include focus-ring;
}

button {
  font-family: inherit;
  font-size: inherit;
  cursor: pointer;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}
```

### Layer 5: Objects

```scss
/**
 * ITCSS Layer 5: Objects
 * @layer objects
 * @description Layout patterns (prefix: o-)
 */

/* Container Object */
.o-container {
  width: 100%;
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: spacing(2);

  @include respond-to($breakpoint-lg) {
    padding-inline: spacing(4);
  }
}

/* Grid Object */
.o-grid {
  display: grid;
  gap: spacing(3);

  &--2cols {
    grid-template-columns: repeat(2, 1fr);
  }

  &--3cols {
    grid-template-columns: repeat(3, 1fr);
  }

  &--responsive {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }

  @media (max-width: $breakpoint-md) {
    &--2cols,
    &--3cols {
      grid-template-columns: 1fr;
    }
  }
}

/* Media Object */
.o-media {
  display: flex;
  align-items: flex-start;
  gap: spacing(2);

  &__figure {
    flex-shrink: 0;
  }

  &__body {
    flex: 1;
    min-width: 0;
  }
}

/* Stack Object */
.o-stack > * + * {
  margin-top: var(--stack-space, #{spacing(2)});
}
```

### Layer 6: Components

```scss
/**
 * ITCSS Layer 6: Components
 * @layer components
 * @description UI components (prefix: c-)
 */

/* Button Component */
.c-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: spacing(1);
  padding: spacing(1) spacing(2);
  background: $color-primary;
  color: white;
  border: none;
  border-radius: $radius-md;
  font-weight: $font-weight-medium;
  cursor: pointer;
  transition: all 0.2s ease;

  @include focus-ring;

  &:hover:not(:disabled) {
    background: $color-primary-hover;
    transform: translateY(-1px);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &--secondary {
    background: $color-secondary;
  }

  &--small {
    padding: spacing(0.5) spacing(1);
    font-size: $font-size-sm;
  }
}

/* Card Component */
.c-card {
  background: var(--color-surface, white);
  border-radius: $radius-lg;
  overflow: hidden;
  box-shadow: $shadow-sm;

  &__header {
    padding: spacing(2);
    border-bottom: 1px solid var(--color-border, #e5e7eb);
  }

  &__body {
    padding: spacing(2);
  }

  &__footer {
    padding: spacing(2);
    border-top: 1px solid var(--color-border, #e5e7eb);
  }
}
```

### Layer 7: Utilities

```scss
/**
 * ITCSS Layer 7: Utilities
 * @layer utilities
 * @description Helper classes (prefix: u-)
 * @important Use !important for utilities
 */

/* Text Utilities */
.u-text-center { text-align: center !important; }
.u-text-left { text-align: left !important; }
.u-text-right { text-align: right !important; }

.u-truncate {
  @include truncate;
}

/* Spacing Utilities */
.u-mt-0 { margin-top: 0 !important; }
.u-mt-1 { margin-top: spacing(1) !important; }
.u-mt-2 { margin-top: spacing(2) !important; }
.u-mt-3 { margin-top: spacing(3) !important; }

.u-mb-0 { margin-bottom: 0 !important; }
.u-mb-1 { margin-bottom: spacing(1) !important; }
.u-mb-2 { margin-bottom: spacing(2) !important; }
.u-mb-3 { margin-bottom: spacing(3) !important; }

/* Display Utilities */
.u-hidden { display: none !important; }
.u-block { display: block !important; }
.u-flex { display: flex !important; }
.u-grid { display: grid !important; }

/* Visually Hidden */
.u-visually-hidden {
  @include visually-hidden;
}
```

---

## CUBE CSS (Composition Utility Block Exception)

### Overview

**Description:** CUBE CSS focuses on composition, utilities, blocks, and exceptions for a progressive enhancement approach.

**4 Layers:**
1. **Composition** - Layout and structure
2. **Utility** - Single-purpose helpers
3. **Block** - Components (data attributes)
4. **Exception** - State overrides (data attributes)

**Best For:**
- Modern CSS projects
- Progressive enhancement
- Flexible component systems
- Projects valuing CSS-first approach

### Composition Layer

```css
/**
 * CUBE CSS Composition Layer
 * @layer composition
 * @description Layout and structural patterns
 */

/* ===== Stack Composition ===== */
.stack {
  display: flex;
  flex-direction: column;
}

.stack > * + * {
  margin-top: var(--stack-space, 1.5rem);
}

.stack--small > * + * {
  --stack-space: 0.5rem;
}

.stack--large > * + * {
  --stack-space: 3rem;
}

/* ===== Cluster Composition ===== */
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--cluster-space, 1rem);
  align-items: center;
}

.cluster--small {
  --cluster-space: 0.5rem;
}

.cluster--large {
  --cluster-space: 2rem;
}

/* ===== Sidebar Composition ===== */
.sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sidebar-gap, 1rem);
}

.sidebar > :first-child {
  flex-basis: var(--sidebar-width, 20rem);
  flex-grow: 1;
}

.sidebar > :last-child {
  flex-basis: 0;
  flex-grow: 999;
  min-width: var(--sidebar-content-min, 50%);
}

/* ===== Switcher Composition ===== */
.switcher {
  display: flex;
  flex-wrap: wrap;
  gap: var(--switcher-gap, 1rem);
}

.switcher > * {
  flex-grow: 1;
  flex-basis: calc((var(--switcher-threshold, 30rem) - 100%) * 999);
}

/* ===== Grid Composition ===== */
.grid {
  display: grid;
  gap: var(--grid-gap, 1rem);
  grid-template-columns: repeat(
    auto-fit,
    minmax(var(--grid-min, 250px), 1fr)
  );
}

/* ===== Center Composition ===== */
.center {
  box-sizing: content-box;
  max-width: var(--center-max, 60rem);
  margin-inline: auto;
  padding-inline: var(--center-padding, 1rem);
}

/* ===== Frame Composition ===== */
.frame {
  aspect-ratio: var(--frame-ratio, 16 / 9);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.frame > * {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### Utility Layer

```css
/**
 * CUBE CSS Utility Layer
 * @layer utility
 * @description Single-purpose helper classes
 */

/* ===== Flow Utility ===== */
.flow > * + * {
  margin-top: var(--flow-space, 1em);
}

/* ===== Region Utility ===== */
.region {
  padding-top: var(--region-space, 3rem);
  padding-bottom: var(--region-space, 3rem);
}

/* ===== Wrapper Utility ===== */
.wrapper {
  max-width: var(--wrapper-max, 70rem);
  margin-inline: auto;
  padding-inline: var(--wrapper-padding, 1rem);
  position: relative;
}

/* ===== Color Utilities ===== */
.bg-primary { background: var(--color-primary); }
.bg-secondary { background: var(--color-secondary); }
.bg-surface { background: var(--color-surface); }

.text-primary { color: var(--color-primary); }
.text-secondary { color: var(--color-text-secondary); }
.text-muted { color: var(--color-text-tertiary); }

/* ===== Typography Utilities ===== */
.font-bold { font-weight: 700; }
.font-medium { font-weight: 500; }
.font-normal { font-weight: 400; }

.text-xs { font-size: 0.75rem; }
.text-sm { font-size: 0.875rem; }
.text-base { font-size: 1rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }

/* ===== Spacing Utilities ===== */
.gap-small { gap: 0.5rem; }
.gap-medium { gap: 1rem; }
.gap-large { gap: 2rem; }

/* ===== Border Utilities ===== */
.rounded-small { border-radius: 4px; }
.rounded-medium { border-radius: 8px; }
.rounded-large { border-radius: 12px; }
.rounded-full { border-radius: 9999px; }

/* ===== Shadow Utilities ===== */
.shadow-small { box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); }
.shadow-medium { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
.shadow-large { box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1); }
```

### Block Layer

```css
/**
 * CUBE CSS Block Layer
 * @layer block
 * @description Components using data attributes
 */

/* ===== Button Block ===== */
[data-component="button"] {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  padding: 0.5em 1em;
  background: var(--button-bg, var(--color-primary));
  color: var(--button-color, white);
  border: var(--button-border, none);
  border-radius: var(--button-radius, 8px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover:not([data-state="disabled"]) {
    filter: brightness(1.1);
    transform: translateY(-1px);
  }

  &:active:not([data-state="disabled"]) {
    transform: translateY(0);
  }
}

[data-variant="secondary"][data-component="button"] {
  --button-bg: var(--color-secondary);
}

[data-variant="outline"][data-component="button"] {
  --button-bg: transparent;
  --button-color: var(--color-primary);
  --button-border: 2px solid var(--color-primary);
}

/* ===== Card Block ===== */
[data-component="card"] {
  background: var(--card-bg, var(--color-surface));
  border-radius: var(--card-radius, 12px);
  padding: var(--card-padding, 1rem);
  box-shadow: var(--card-shadow, 0 2px 4px rgba(0, 0, 0, 0.1));
}

[data-variant="bordered"][data-component="card"] {
  --card-shadow: none;
  border: 1px solid var(--color-border);
}

[data-variant="elevated"][data-component="card"] {
  --card-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

/* ===== Input Block ===== */
[data-component="input"] {
  width: 100%;
  padding: 0.5em 0.75em;
  background: var(--input-bg, var(--color-surface));
  border: var(--input-border, 1px solid var(--color-border));
  border-radius: var(--input-radius, 6px);
  font-size: inherit;
  font-family: inherit;
  transition: border-color 0.2s ease;

  &:focus {
    outline: none;
    border-color: var(--color-primary);
  }
}

/* ===== Navigation Block ===== */
[data-component="nav"] {
  display: flex;
  gap: var(--nav-gap, 1rem);
}

[data-orientation="vertical"][data-component="nav"] {
  flex-direction: column;
}

[data-component="nav-link"] {
  display: block;
  padding: 0.5em 1em;
  color: var(--link-color, var(--color-text-primary));
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;

  &:hover {
    background: var(--link-hover-bg, var(--color-surface-hover));
  }
}
```

### Exception Layer

```css
/**
 * CUBE CSS Exception Layer
 * @layer exception
 * @description State overrides using data attributes
 */

/* ===== Disabled State ===== */
[data-state="disabled"] {
  opacity: 0.5;
  pointer-events: none;
  cursor: not-allowed;
}

/* ===== Loading State ===== */
[data-state="loading"] {
  position: relative;
  pointer-events: none;
  color: transparent;
}

[data-state="loading"]::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border: 2px solid currentColor;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 0.6s linear infinite;
}

/* ===== Active State ===== */
[data-state="active"] {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: 500;
}

/* ===== Selected State ===== */
[data-state="selected"] {
  background: var(--color-primary);
  color: white;
}

/* ===== Error State ===== */
[data-state="error"] {
  border-color: var(--color-error);
  background: var(--color-error-light);
}

/* ===== Success State ===== */
[data-state="success"] {
  border-color: var(--color-success);
  background: var(--color-success-light);
}

/* ===== Open/Closed States ===== */
[data-state="open"] {
  display: block;
}

[data-state="closed"] {
  display: none;
}

/* ===== Expanded/Collapsed States ===== */
[data-state="expanded"] {
  max-height: 1000px;
  overflow: visible;
}

[data-state="collapsed"] {
  max-height: 0;
  overflow: hidden;
}
```

---

## Methodology Comparison & Selection

### Comparison Matrix

```typescript
/**
 * CSS Methodology Comparison
 * @description Feature comparison of major methodologies
 */

interface MethodologyFeatures {
  name: string;
  namingConvention: 'strict' | 'flexible' | 'data-attributes';
  specificity: 'low' | 'medium' | 'high';
  learningCurve: 'easy' | 'moderate' | 'steep';
  scalability: 'small' | 'medium' | 'large';
  teamSize: 'solo' | 'small' | 'large';
  bestFor: string[];
  limitations: string[];
}

const methodologies: MethodologyFeatures[] = [
  {
    name: 'BEM',
    namingConvention: 'strict',
    specificity: 'low',
    learningCurve: 'easy',
    scalability: 'large',
    teamSize: 'large',
    bestFor: [
      'Component libraries',
      'React/Vue/Angular apps',
      'Clear component boundaries',
      'Teams new to CSS methodologies'
    ],
    limitations: [
      'Verbose class names',
      'Can become unwieldy with deep nesting',
      'No built-in theming strategy'
    ]
  },
  {
    name: 'OOCSS',
    namingConvention: 'flexible',
    specificity: 'low',
    learningCurve: 'moderate',
    scalability: 'large',
    teamSize: 'large',
    bestFor: [
      'Maximum CSS reusability',
      'Design systems',
      'Large applications',
      'OOP-familiar teams'
    ],
    limitations: [
      'Requires strong discipline',
      'Can lead to class bloat',
      'Separation can be unclear'
    ]
  },
  {
    name: 'SMACSS',
    namingConvention: 'flexible',
    specificity: 'medium',
    learningCurve: 'moderate',
    scalability: 'large',
    teamSize: 'large',
    bestFor: [
      'Large applications',
      'Multi-theme projects',
      'Clear categorization needed',
      'State-heavy applications'
    ],
    limitations: [
      'Category boundaries can blur',
      'Requires team agreement',
      'State management can be tricky'
    ]
  },
  {
    name: 'ITCSS',
    namingConvention: 'flexible',
    specificity: 'low',
    learningCurve: 'steep',
    scalability: 'large',
    teamSize: 'large',
    bestFor: [
      'Enterprise applications',
      'Design systems',
      'Large teams',
      'Long-term maintainability'
    ],
    limitations: [
      'Complex file structure',
      'Steep learning curve',
      'Requires tooling'
    ]
  },
  {
    name: 'CUBE CSS',
    namingConvention: 'data-attributes',
    specificity: 'low',
    learningCurve: 'moderate',
    scalability: 'medium',
    bestFor: [
      'Modern CSS projects',
      'Progressive enhancement',
      'Flexible component systems',
      'CSS-first approach'
    ],
    limitations: [
      'Less established',
      'Data attributes can be verbose',
      'Smaller community'
    ]
  }
];
```

### Selection Decision Tree

```typescript
/**
 * Methodology Selection Guide
 * @function selectMethodology
 * @description Help choose the right CSS methodology
 *
 * @param projectType - Type of project
 * @param teamSize - Team size
 * @param experience - Team's CSS experience level
 * @returns Recommended methodology
 */
function selectMethodology(
  projectType: ProjectType,
  teamSize: TeamSize,
  experience: ExperienceLevel
): string {
  // Component library or design system
  if (projectType === 'component-library') {
    return teamSize === 'large' ? 'BEM + ITCSS' : 'BEM';
  }

  // Enterprise application
  if (projectType === 'enterprise-app') {
    return experience === 'advanced' ? 'ITCSS' : 'SMACSS';
  }

  // Modern web app
  if (projectType === 'modern-app') {
    return experience === 'advanced' ? 'CUBE CSS' : 'BEM';
  }

  // Multi-theme application
  if (projectType === 'multi-theme') {
    return 'SMACSS';
  }

  // Small project
  if (teamSize === 'solo' || teamSize === 'small') {
    return 'BEM';
  }

  // Default recommendation
  return 'BEM';
}

type ProjectType = 'component-library' | 'enterprise-app' | 'modern-app' | 'multi-theme' | 'small-project';
type TeamSize = 'solo' | 'small' | 'medium' | 'large';
type ExperienceLevel = 'beginner' | 'intermediate' | 'advanced';
```

---

## Implementation Strategies

### Hybrid Approach

```scss
/**
 * Hybrid Methodology Implementation
 * @description Combining BEM + ITCSS for best results
 */

// ITCSS Layer 1: Settings
$color-primary: #3b82f6;

// ITCSS Layer 2: Tools
@mixin respond-to($breakpoint) {
  @media (min-width: $breakpoint) { @content; }
}

// ITCSS Layer 5: Objects (OOCSS-inspired)
.o-media {
  display: flex;
  gap: 1rem;
}

.o-media__figure {
  flex-shrink: 0;
}

.o-media__body {
  flex: 1;
}

// ITCSS Layer 6: Components (BEM naming)
.c-product-card {
  background: white;
  border-radius: 8px;

  &__image {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  &__title {
    font-size: 18px;
    font-weight: 600;
  }

  &--featured {
    border: 2px solid $color-primary;
  }
}

// ITCSS Layer 7: Utilities
.u-text-center { text-align: center !important; }
```

### Linting Configuration

```javascript
/**
 * Stylelint Configuration for BEM
 * .stylelintrc.json
 */
{
  "plugins": [
    "stylelint-selector-bem-pattern"
  ],
  "rules": {
    "plugin/selector-bem-pattern": {
      "preset": "bem",
      "componentName": "[A-Z]+",
      "componentSelectors": {
        "initial": "^\\.{componentName}(?:-[a-z]+)?$",
        "combined": "^\\.combined-{componentName}-[a-z]+$"
      },
      "utilitySelectors": "^\\.util-[a-z]+$"
    },
    "selector-class-pattern": [
      "^[a-z]([a-z0-9-]+)?(__([a-z0-9]+-?)+)?(--([a-z0-9]+-?)+){0,2}$",
      {
        "message": "Class names must follow BEM pattern"
      }
    ],
    "selector-max-id": 0,
    "selector-max-specificity": "0,3,0",
    "max-nesting-depth": 3
  }
}
```

---

## Team Adoption & Training

### Onboarding Checklist

```markdown
# CSS Methodology Onboarding

## Week 1: Understanding
- [ ] Read methodology documentation
- [ ] Review code examples
- [ ] Understand naming conventions
- [ ] Learn file organization

## Week 2: Practice
- [ ] Complete practice exercises
- [ ] Refactor sample components
- [ ] Review with senior developer
- [ ] Set up linting tools

## Week 3: Implementation
- [ ] Start with small components
- [ ] Get code reviews
- [ ] Ask questions
- [ ] Document learnings

## Week 4: Mastery
- [ ] Implement complex components
- [ ] Help review others' code
- [ ] Contribute to docs
- [ ] Share best practices
```

---

## Summary

This CSS Methodologies Patterns Library provides:

- ✅ **Complete methodology coverage**: BEM, OOCSS, SMACSS, ITCSS, CUBE CSS
- ✅ **Production-ready examples**: Real-world component implementations
- ✅ **TypeScript interfaces**: Type-safe methodology configurations
- ✅ **Selection guides**: Decision trees and comparison matrices
- ✅ **Implementation strategies**: Hybrid approaches and best practices
- ✅ **Team adoption**: Training materials and onboarding checklists
- ✅ **Swagger documentation**: Full API docs for all patterns
- ✅ **WCAG 2.1 AA compliance**: Accessibility throughout

Choose the methodology that best fits your team, project, and requirements. Remember: consistency is more important than perfection.
