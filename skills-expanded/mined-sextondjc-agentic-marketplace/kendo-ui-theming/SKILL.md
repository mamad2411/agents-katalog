---
name: kendo-ui-theming
description: Use when customizing Kendo UI themes using SASS variables, design tokens, ThemeBuilder, or CSS overrides — covering brand palette mapping, dark mode, multi-theme support, and upgrade-safe theme governance.
---

# Kendo UI Theming

## Specialization

Design and implement Kendo UI visual customization through SASS variable overrides, ThemeBuilder-generated themes, CSS custom property tokens, and upgrade-safe theme management — grounded in official Kendo UI theming documentation.

## Trigger Conditions

- Applying a brand palette to Kendo UI components via SASS variable overrides.
- Using Kendo UI ThemeBuilder to generate a custom theme.
- Implementing dark mode or light/dark theme switching for Kendo UI components.
- Upgrading Kendo UI and reconciling SASS variable changes after a version bump.
- Maintaining a shared Kendo UI theme package across multiple projects in a monorepo.
- Overriding per-component styles without breaking other widget visual contracts.
- Reviewing CSS specificity conflicts between custom styles and Kendo UI theme classes.
- Integrating Kendo UI SASS theming into a build pipeline (Webpack, Vite, custom).

## Scope Boundaries

In scope:

- Kendo UI default themes: Default, Bootstrap, Material, Fluent — variable contracts and override strategy.
- SASS variable override pattern: `@import` ordering, variable scope, and override precedence.
- Kendo UI ThemeBuilder workflow: generating, downloading, and integrating a custom theme.
- CSS custom properties approach for runtime theme switching.
- Dark mode implementation: CSS media query strategy and class-based theme toggle.
- Multi-theme support: conditional theme loading or CSS class-scoped theme overrides.
- Build pipeline integration: SASS compilation step, source maps, and production output.
- Upgrade-safety: tracking breaking SASS variable renames across Kendo UI versions.

Out of scope:

- Component behavior customization (see `kendo-ui-core`).
- Design token governance across non-Kendo UI components (see relevant UI library skills).
- CI enforcement of theme conformance (see `kendo-ui-ci-integration`).

## Inputs

- Kendo UI base theme in use (Default, Bootstrap, Material, Fluent, or custom).
- Kendo UI version in use.
- Brand palette: primary color, accent, text, background, border tokens.
- Dark mode requirement: yes/no, toggle mechanism.
- Build toolchain: Webpack, Vite, Gulp, or direct SASS CLI.
- Existing theme overrides file (if applicable).

## Required Outputs

- SASS variable override file with documented token-to-brand mapping.
- Build pipeline integration step (SASS compilation with correct import order).
- Dark mode implementation pattern: media query or class-based toggle.
- Upgrade impact assessment: SASS variable names changed in the target Kendo UI version.
- Multi-theme loading strategy (if applicable).
- CSS specificity audit: no `!important` escalation without documented exception.

## Core Patterns

### SASS Override Pattern

```scss
// 1. Override variables BEFORE importing the Kendo UI theme
$kendo-color-primary: #0078d4;
$kendo-color-primary-hover: #106ebe;
$kendo-border-radius: 4px;
$kendo-font-family: "Segoe UI", sans-serif;

// 2. Import the base theme
@import "@progress/kendo-theme-default/scss/all";
```

### ThemeBuilder Integration

```bash
# Install the Kendo UI SASS theme package
npm install @progress/kendo-theme-default

# Download ThemeBuilder output as custom-theme.scss
# Place at src/styles/kendo-custom-theme.scss
# Import in your entry stylesheet instead of the default theme
```

### Dark Mode via CSS Class Toggle

```scss
// Light theme (default)
@import "@progress/kendo-theme-default/scss/all";

// Dark overrides scoped to .k-dark class on <html> or <body>
.k-dark {
    $kendo-color-bg: #1b1b1b;
    $kendo-color-text: #ffffff;
    // Re-include affected component partials with new variable values
    @import "@progress/kendo-theme-default/scss/grid/theme";
    @import "@progress/kendo-theme-default/scss/button/theme";
}
```

### Runtime Token Switching (CSS Custom Properties)

```css
:root {
    --kendo-color-primary: #0078d4;
    --kendo-color-bg: #ffffff;
}

[data-theme="dark"] {
    --kendo-color-primary: #60cdff;
    --kendo-color-bg: #1b1b1b;
}
```

## Upgrade Safety Checklist

- Check Kendo UI release notes for renamed or removed SASS variables before upgrading.
- Run SASS compilation after upgrade and treat any `Undefined variable` error as a blocking finding.
- Validate ThemeBuilder output against the new Kendo UI version — regenerate if variable contracts changed.
- Review CSS custom property names — Progress periodically adds CSS variable support to replace hard-coded SASS outputs.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Apply brand primary color via single SASS variable override | Grid, buttons, and focused widgets reflect the brand color |
| L2 Practical | Full brand palette mapped to SASS variables with build pipeline integration | SASS compiles without errors; all Kendo UI components reflect brand |
| L3 Hardening | Dark mode toggle + upgrade-safe theme governance | Dark mode verified across Grid, Chart, and form widgets; upgrade checklist complete |
| L4 Expert Standardization | Shared Kendo UI theme package in a monorepo with version-locked contracts | Theme package is consumed by two or more projects with documented upgrade governance |
