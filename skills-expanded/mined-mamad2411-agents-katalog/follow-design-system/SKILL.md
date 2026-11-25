---
name: follow-design-system
description: Fundamental design system principles applicable to every platform (TUI, Web, Desktop, Mobile)
argument-hint: "[scope]"
related:
  - follow-lib-unocss
  - follow-unocss-theme
  - deep-review-codebase
  - use-agents-capture
---

## Goal

Apply universal design system principles across every platform for consistency and maintainability

## Scope

Covers design tokens, component guidelines, and platform-specific adaptations for TUI, Web, Desktop, and Mobile

See also: /deep-review-codebase

## Execute

### 1. Define Design Tokens

> Goal: define visual, interaction, and language tokens

1. Define visual tokens: colors, typography, spacing, shadows, borders
2. Define interaction tokens: transitions, animations, cursors
3. Define language tokens: terminology, tone of voice, iconography
4. If the project uses UnoCSS, do `/follow-lib-unocss` for UnoCSS setup and `/follow-unocss-theme` for the theme.css token layer + enforcement

### 2. Create Component Guidelines

> Goal: build and document reusable components

1. Build reusable components with atomic design (atoms → molecules → organisms)
2. Use design tokens for every component
3. Document every component and pattern
4. Define component variants (sizes, states, colors)
5. Run `/use-agents-capture` to record a screenshot of each component for documentation

### 3. Apply To Platforms

> Goal: adapt tokens and guidelines per platform

1. Adapt tokens to platform constraints (see the table below)
2. If the project is web, do `/deep-review-codebase` for web-specific guidelines
3. If the project has mobile, do `/deep-review-codebase`
4. If the project has TUI, do `/deep-review-codebase`

### 4. Ensure Accessibility

> Goal: review and implement accessibility for every platform

1. Follow WCAG 2.2 guidelines on every platform
2. Support keyboard navigation
3. Support screen readers
4. Check color contrast ratio

### 5. Test And Validate

> Goal: test the design system on every platform

1. Test visual consistency across all platforms
2. Test component reusability
3. Test accessibility compliance
4. Test responsive behavior

## Rules

### 1. Consistency

- Visual consistency: colors, typography, spacing applied uniformly
- Interaction consistency: repeated patterns use the same approach
- Language consistency: terminology, tone of voice applied uniformly

### 2. Scalability

- Component-based: build reusable components
- Token-based: use design tokens (colors, spacing, etc.)
- Documentation: document every component and pattern

### 3. Accessibility

- WCAG compliance: follow the WCAG 2.2 accessibility standard
- Keyboard navigation: support keyboard
- Screen reader support: support screen readers
- Color contrast: correct contrast ratio

### 4. Platform Adaptations

| Platform | Color Palette | Spacing | Typography | Layout |
|----------|--------------|---------|------------|--------|
| TUI | 16 colors | character spacing | monospace only | grid-based |
| Web | full RGB | rem/em units | web fonts | flexbox, grid |
| Desktop | full RGB | platform units | system fonts | native layouts |
| Mobile | full RGB | touch-friendly | system fonts | responsive |

### 5. Naming Conventions

- PascalCase for components
- camelCase for props and variables
- kebab-case for CSS classes
- UPPER_SNAKE_CASE for constants

- Use /deep-review-codebase if needed

## Expected Outcome

- Consistent design tokens
- Reusable component library
- Complete documentation
- Cross-platform consistency
- Accessibility compliance

## Guide

- [Design Systems](https://www.designsystems.com/)
- [Atomic Design](http://atomicdesign.bradfrost.com/)
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
