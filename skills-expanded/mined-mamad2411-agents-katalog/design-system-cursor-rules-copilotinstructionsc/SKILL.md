---
description:
globs:
alwaysApply: true
---

# Design System Project Instructions

## Overview

This repository contains our design system - a collection of reusable components, design tokens, and guidelines that ensure consistency across our products.

## Repository Structure

- `libs/ui/` - Main UI components library
- `libs/ui/src/lib/tokens/` - Design tokens (colors, typography, spacing)
- `libs/ui/src/lib/styles/` - Global styles and themes
- `docs/` - Documentation
- `e2e/` - End-to-end tests (Playwright)
- `src/app/` - Demo application

## Core Development Principles

### 1. Angular Modern Patterns

- Use **standalone components** exclusively
- Use **signal()** for state management (NO async pipe)
- Use **input() and output()** signals instead of @Input()/@Output() decorators
- Use **control flow syntax** (@if, @for) instead of structural directives
- Apply **OnPush** change detection strategy for all components

### 2. Type Safety

- **NO `any` types** - enforce strict typing everywhere
- Explicitly declare types for all variables
- Use strongly typed props with default values
- Document allowed values using JSDoc comments

### 3. Component Architecture

- Components must be **atomic and minimal** (smallest possible units)
- Follow **strict separation of concerns**: logic in TS, style in SCSS, clean templates
- Export all components from `index.ts` files
- Implement `trackBy` functions for `@for` loops
- **Prefer directives to shape components** (like Angular Material pattern)

### 4. Directive-First Approach

- **Use directives to modify component behavior and appearance**
- Create **attribute directives** for styling variants (e.g., `appButtonVariant="primary"`)
- Create **structural directives** for conditional rendering patterns
- Create **host binding directives** for dynamic properties
- **Examples:**
  - `appButtonSize="large"` instead of `[size]="'large'"`
  - `appButtonColor="primary"` instead of `[color]="'primary'"`
  - `appButtonDisabled` instead of `[disabled]="true"`
  - `*appButtonLoading` for loading state
  - `*appButtonIcon="iconName"` for icon variants

### 5. Styling & Theming

- **SCSS-based styling** (no Tailwind or CSS-in-JS)
- Apply theme colors using CSS variables: `color: var(--color-text)`
- Support both light and dark themes
- Use CSS custom properties for theme tokens

### 6. Accessibility

- Meet **WCAG 2.1 AA** accessibility standards
- Include appropriate ARIA attributes
- Support keyboard navigation
- Document accessibility considerations

## Component Development Checklist

### Required Files

- ✅ Component TypeScript file (`.component.ts`)
- ✅ Component template (`.component.html`)
- ✅ Component styles (`.component.scss`)
- ✅ Unit tests (`.component.spec.ts`)
- ✅ Storybook stories (`.stories.ts`)
- ✅ **Directives for variants** (`.directive.ts`)

### Documentation Requirements

- ✅ JSDoc comments for all inputs/outputs
- ✅ Usage examples in Storybook
- ✅ Props/inputs tables
- ✅ Accessibility considerations
- ✅ Edge cases and limitations
- ✅ **Directive usage examples**

### Naming Conventions

- ✅ Consistent input/output naming across components
- ✅ Consistent prop naming conventions
- ✅ Follow Angular naming conventions
- ✅ **Directive naming: `appComponentVariant` pattern**

## Project Structure (Current)

```
design-system/
├── libs/ui/                              # Main UI library
│   ├── src/lib/
│   │   ├── buttons/                      # Button components
│   │   │   ├── button/                   # Basic button
│   │   │   └── directives/               # Button directives
│   │   ├── data-display/                 # Data display components
│   │   │   ├── badge/                    # Badge component
│   │   │   └── table/                    # Table with directives
│   │   ├── feedback/                     # Feedback components
│   │   │   └── alert/                    # Alert component
│   │   ├── form/                         # Form components
│   │   │   ├── text-input/               # Text input
│   │   │   ├── select/                   # Select component
│   │   │   └── toggle/                   # Toggle component
│   │   ├── navigation/                   # Navigation components
│   │   │   └── tabs/                     # Tabs component
│   │   ├── modal/                        # Modal system
│   │   ├── card/                         # Card component
│   │   ├── tokens/                       # Design tokens
│   │   │   ├── colors.ts
│   │   │   ├── spacing.ts
│   │   │   └── typography.ts
│   │   └── styles/                       # Global styles
│   │       ├── _variables.scss
│   │       ├── _mixins.scss
│   │       └── themes/
│   │           ├── _light.scss
│   │           └── _dark.scss
├── docs/                                 # Documentation
├── e2e/                                  # E2E tests
└── src/app/                              # Demo application
```

## Nx Workspace Guidelines

### Available Tools

- Use `nx_workspace` tool to understand workspace architecture
- Use `nx_docs` tool for Nx-specific documentation
- Use `nx_generators` to see available generators
- Use `nx_visualize_graph` to understand task dependencies

### Common Commands

```bash
# Generate new component
npx nx g @nx/angular:component button --project=ui --export

# Generate new directive
npx nx g @nx/angular:directive button-variant --project=ui --export

# Run tests
npx nx test ui

# Build library
npx nx build ui

# Run Storybook
npx nx storybook ui

# Run e2e tests
npx nx e2e e2e
```

## Architecture Best Practices

### State Management

- Use **component-local signals** for simple state
- Create **signal-based services** for shared state
- Implement **computed signals** for derived values

### Component Communication

- Use **inputs/outputs** for parent-child communication
- Use **signals** for component-to-component communication
- Create **specialized services** for complex interactions

### Directive Patterns

- **Attribute directives** for styling and behavior variants
- **Structural directives** for conditional rendering
- **Host binding directives** for dynamic properties
- **Follow Angular Material patterns** for directive naming and usage
- **Examples:**

  ```html
  <!-- Preferred: Using directives -->
  <button appButton appButtonVariant="primary" appButtonSize="large">
    Click me
  </button>

  <!-- Avoid: Using inputs for variants -->
  <app-button [variant]="'primary'" [size]="'large'"> Click me </app-button>
  ```

### Performance

- Use **OnPush** change detection strategy
- Implement **trackBy** functions for loops
- Avoid unnecessary template expressions
- Lazy load complex components when possible

### Testing

- Unit tests must cover public API and edge cases
- Component tests should simulate real user interactions
- Use Storybook for visual regression testing
- **Test directives separately** from components

## Getting Started

### Prerequisites

- Node.js (v18+)
- npm or yarn
- Angular CLI (v20+)

### Setup Commands

```bash
# Install dependencies
npm install

# Install Storybook
npm install --save-dev @nx/storybook

# Generate Storybook configuration
npx nx g @nx/angular:storybook-configuration ui

# Generate stories for components
npx nx g @nx/angular:stories --project=ui
```

## Versioning & Release

- Follow **Semantic Versioning** (SemVer)
- Maintain detailed changelog
- Include migration guides for breaking changes
- Create deprecation paths for API changes
