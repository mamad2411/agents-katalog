---
name: token-usage
description: >
  Guide on correctly using IDS design tokens in React components and CSS.
  Covers import patterns, common mistakes, and practical usage rules for each
  token category. Use when the user asks about design tokens, CSS variables,
  CSS custom properties, spacing values, colour tokens, typography tokens,
  theme tokens, token values, or mentions @iress-oss/ids-tokens in an IDS
  application.
license: Apache-2.0
compatibility: React 18+, TypeScript, @iress-oss/ids-tokens@beta
metadata:
  author: iress
  version: '1.0'
---

# Skill: IDS Token Usage

## Purpose

Guide AI agents on correctly using IDS design tokens in React components and CSS. This skill covers import patterns, common mistakes, and practical usage rules for each token category.

## When to Use

- Generating React components that need colours, spacing, typography, or border-radius values
- Writing custom CSS or inline styles for IDS-based applications
- Reviewing or fixing design token usage in existing code
- Choosing between component props, CSS variables, and the `cssVars` JS object
- Answering questions about available token values and naming conventions

## Workflow

1. **Check if a component prop handles it** — Most IDS components accept `IressCSSProps` (e.g. `p`, `m`, `gap`, `bg`, `color`, `textStyle`). Use props before reaching for tokens directly.
2. **Identify the token category** — Is it colour, spacing, typography, or radius?
3. **Choose the right import** — Use `cssVars` for inline styles, CSS variables for stylesheets. See the import patterns below.
4. **Look up the value** — See [references/token-reference.md](references/token-reference.md) for the full list of available tokens if you need to find a specific value.

## Quick Start

### Installation

> **Important:** IDS v6 is currently in beta. Install with the `@beta` tag:
>
> ```bash
> npm install @iress-oss/ids-tokens@beta
> # If also using IDS React components:
> npm install @iress-oss/ids-components@beta
> ```

### Prerequisites (React only)

If you are using IDS React components, wrap your application in `IressProvider` and import the CSS variables stylesheet:

> **Note:** `IressProvider` already includes `IressModalProvider`, `IressSlideoutProvider`, `IressToasterProvider`, `IressPopoverProvider`, and `IressIconProvider` — you do not need to add these separately. If using `IressShadow`, no additional providers are needed as it includes `IressProvider` internally.

```tsx
import '@iress-oss/ids-tokens/build/css-vars.css';
import { IressProvider } from '@iress-oss/ids-components';

function App() {
  return <IressProvider>{/* your UI */}</IressProvider>;
}
```

> **Non-React usage:** The tokens package works without React. Import the CSS stylesheet or use `cssVars` / `designTokens` directly in any JavaScript or CSS environment.

> **CSP note:** `IressProvider` loads fonts from `fonts.googleapis.com` and `fonts.gstatic.com` at runtime. If your app enforces a Content Security Policy, allowlist these origins in `style-src` and `font-src`. If you use `IressShadow` and your CSP blocks inline styles, add `<meta name="csp-nonce" content="...">` for nonce support. See the CSP Guide at `node_modules/@iress-oss/ids-components/.ai/guides/get-started-content-security-policy.md` for details (requires `@iress-oss/ids-components` to be installed).

### CSS Variables Stylesheet (Recommended for CSS)

The CSS stylesheet is the simplest way to use tokens. Import it once and use `var()` references anywhere in your CSS.

> **Important:** Use the variable names defined in `@iress-oss/ids-tokens/build/css-vars.css` (e.g. `--colour-neutral-10`). Do **not** reference `--iress-*` variables directly — those are set by theme files and are not part of the public token API.

```css
/* Import the stylesheet once in your app root */
@import '@iress-oss/ids-tokens/build/css-vars.css';

/* Use variables anywhere in your CSS */
.card {
  background: var(--colour-neutral-10);
  padding: var(--spacing-4);
  border-radius: var(--radius-3);
  color: var(--colour-neutral-90);
}
```

### `cssVars` Object (Recommended for CSS-in-JS)

For inline styles and CSS-in-JS, use the `cssVars` export. It mirrors the token structure but returns `var()` strings with embedded fallbacks — fully type-safe.

```tsx
import { cssVars } from '@iress-oss/ids-tokens';

// Each leaf is a var() string with a fallback value
cssVars.colour.primary.fill; // 'var(--iress-colour-primary-fill, #003271)'
cssVars.spacing[4]; // 'var(--iress-spacing-4, calc(4 * var(--iress-spacing-100, .25rem)))'
cssVars.radius[1]; // 'var(--iress-radius-1, 0.25rem)'
cssVars.typography.heading[1]; // 'var(--iress-typography-heading-1, 500 calc(...) / 1.33 Ubuntu, ...)'

// Use in inline styles
<div
  style={{
    background: cssVars.colour.neutral[20],
    padding: cssVars.spacing[4],
  }}
>
  Themed content
</div>;
```

### JavaScript Schema (For Metadata / Tooling)

Use the raw `designTokens` schema only when you need to inspect token metadata (descriptions, types, extensions) or iterate programmatically. **For styling, use `cssVars` or CSS variables instead.**

```ts
import { designTokens } from '@iress-oss/ids-tokens';

// Each token is an IressDesignToken object with $value, $type, $description, etc.
designTokens.colour.primary.fill.$value; // '#003271'
designTokens.spacing[4].$value; // 'calc(4 * {spacing.100 || .25rem})'
designTokens.radius[1].$value; // '0.25rem'
designTokens.typography.heading[1].$value; // { fontFamily, fontSize, fontWeight, lineHeight }
```

## Import Patterns

### For CSS Styling

```css
/* In your app entry point */
@import '@iress-oss/ids-tokens/build/css-vars.css';
```

Once imported, all public token variables (e.g. `--colour-*`, `--spacing-*`, `--radius-*`, `--typography-*`) are available globally.

### For CSS-in-JS / Inline Styles

```ts
import { cssVars } from '@iress-oss/ids-tokens';

// Type-safe var() references with fallbacks — use anywhere you need a style value
cssVars.colour.neutral[10]; // 'var(--iress-colour-neutral-10, #FFFFFF)'
cssVars.spacing[4]; // 'var(--iress-spacing-4, ...)'
```

### For Token Metadata / Tooling

```ts
import { designTokens } from '@iress-oss/ids-tokens';

// Access raw token objects for metadata inspection
const { colour, spacing, radius, typography } = designTokens;
```

### Internal Helpers (Theme Editors Only)

> **Note:** These helpers are intended for internal tooling such as theme editors (e.g. Styler). Consumers should use `cssVars` or CSS variables instead.

```ts
// Convert token schema to a nested object of CSS variable references
import { mapTokensToCssVariables } from '@iress-oss/ids-tokens/mapTokensToCssVariables';

// Resolve `{colour.neutral.10}` token references to CSS vars
import { convertReferencesToVariables } from '@iress-oss/ids-tokens/convertReferencesToVariables';
```

## Usage Rules by Category

### Colour

**Always use colour tokens for colours** — never hardcode hex, rgb, or hsl values.

| Use Case          | Token                        | Example                     |
| ----------------- | ---------------------------- | --------------------------- |
| Page background   | `colour.neutral.10`          | `bg="colour.neutral.10"`    |
| Subtle background | `colour.neutral.20`          | `bg="colour.neutral.20"`    |
| Default text      | `colour.neutral.80`          | `color="colour.neutral.80"` |
| Secondary text    | `colour.neutral.70`          | `color="colour.neutral.70"` |
| Borders           | `colour.neutral.30`          | _Use component props_       |
| Primary action    | `colour.primary.fill`        | _Use Button mode="primary"_ |
| Success indicator | `colour.system.success.fill` | _Use Alert/Tag status_      |
| Danger/Error      | `colour.system.danger.fill`  | _Use Alert/Tag status_      |

```tsx
// ✅ Correct
<IressText color="colour.neutral.80">Subtitle</IressText>
<IressStack bg="colour.neutral.20" p="spacing.4">...</IressStack>

// ❌ Wrong — hardcoded colours
<div style={{ color: '#384666' }}>Subtitle</div>
<div style={{ background: '#F5F6F8' }}>...</div>
```

### Spacing

**Use spacing tokens for all spacing** — gaps, padding, margins.

Base unit: 4px (0.25rem). Token value = multiple of base unit.

| Token | Alias  | Value | Use For                  |
| ----- | ------ | ----- | ------------------------ |
| `0`   | `none` | 0     | No space                 |
| `1`   | `xs`   | 4px   | Tight inline spacing     |
| `2`   | `sm`   | 8px   | Default element spacing  |
| `3`   | —      | 12px  | Compact section spacing  |
| `4`   | `md`   | 16px  | Standard section spacing |
| `5`   | —      | 20px  | Medium section spacing   |
| `6`   | `lg`   | 24px  | Section separation       |
| `7`   | —      | 28px  | Large section spacing    |
| `8`   | —      | 32px  | Large group spacing      |
| `10`  | `xl`   | 40px  | Page-level spacing       |

```tsx
// ✅ Correct — use full token path
<IressStack gap="spacing.4" p="spacing.6">...</IressStack>
<IressInline gap="spacing.2">...</IressInline>

// ✅ Also correct — use token aliases
<IressStack gap="md" p="lg">...</IressStack>
<IressInline gap="sm">...</IressInline>

// ❌ Wrong — arbitrary values
<div style={{ gap: '15px', padding: '25px' }}>...</div>
```

> **Note:** There is no `spacing[9]` token. Valid spacing values: `spacing.0` through `spacing.10` (excluding 9), or aliases: `none`, `xs`, `sm`, `md`, `lg`, `xl`.
>
> **Positive vs negative spacing:** Padding props (`p`, `px`, `py`, `pb`, `pl`, `pr`, `pt`) only accept positive spacing tokens. Margin props (`m`, `mx`, `my`, `mb`, `ml`, `mr`, `mt`) also accept negative values (e.g., `-spacing.2`, `-sm`) for overlapping elements.

### Border Radius

**Use radius tokens for all rounded corners.**

| Token      | Value | Semantic Use                     |
| ---------- | ----- | -------------------------------- |
| `radius.0` | 0     | Square/sharp corners             |
| `radius.1` | 4px   | Buttons, form inputs, tags       |
| `radius.2` | 8px   | General purpose                  |
| `radius.3` | 12px  | Cards, panels, layout containers |
| `radius.4` | 16px  | Pills, badges                    |

```tsx
// ✅ Correct — IDS components already have correct radius
<IressButton>Submit</IressButton>  // radius.1 built in
<IressCard>...</IressCard>         // radius.3 built in

// Manual radius only when building custom layout
<IressStack borderRadius="radius.3">Custom panel</IressStack>
```

### Typography

**Use IressText for all text rendering** instead of raw headings or paragraphs.

| Element        | `textStyle` value           | Font   | Size            | Weight |
| -------------- | --------------------------- | ------ | --------------- | ------ |
| h1             | `typography.heading.1`      | Ubuntu | 1.5rem (24px)   | 500    |
| h2             | `typography.heading.2`      | Ubuntu | 1.25rem (20px)  | 500    |
| h3             | `typography.heading.3`      | Ubuntu | 1.125rem (18px) | 500    |
| h4             | `typography.heading.4`      | Ubuntu | 1rem (16px)     | 500    |
| h5             | `typography.heading.5`      | Ubuntu | 1rem (16px)     | 400    |
| body (default) | `typography.body.md`        | Inter  | 0.875rem (14px) | 400    |
| body strong    | `typography.body.md.strong` | Inter  | 0.875rem (14px) | 600    |
| small text     | `typography.body.sm`        | Inter  | 0.75rem (12px)  | 400    |
| small strong   | `typography.body.sm.strong` | Inter  | 0.75rem (12px)  | 600    |
| code           | `typography.code`           | Space  | 1rem (16px)     | 400    |

**All `textStyle` values:** `typography.heading.1` – `.5`, `typography.body.sm` (+ `.regular`, `.medium`, `.strong`, `.em`), `typography.body.md` (+ `.regular`, `.medium`, `.strong`, `.em`), `typography.code`, `inherit`.

```tsx
// ✅ Correct
<IressText element="h1">Page Title</IressText>
<IressText>Body paragraph text</IressText>
<IressText textStyle="typography.body.sm.strong">Small bold label</IressText>

// ❌ Wrong — raw HTML elements lose IDS typography
<h1>Page Title</h1>
<p style={{ fontFamily: 'Inter', fontSize: '14px' }}>Text</p>
```

## CSS Variables in Custom Styles

**This is the recommended approach** for any custom styling beyond what IDS component props provide.

> **Using Panda CSS?** If your project uses [Panda CSS](https://panda-css.com), use the `@iress-oss/ids-theme-preset` package instead of manually referencing CSS variables. It provides a Panda CSS preset with the full IDS token system, giving you type-safe token usage via Panda's `css()` function, utilities, and recipes. See [references/theme-preset.md](references/theme-preset.md) for setup.

### In CSS / SCSS

```css
.custom-card {
  /* Colour tokens */
  background: var(--colour-neutral-10);
  border: 1px solid var(--colour-neutral-30);
  color: var(--colour-neutral-90);

  /* Spacing tokens */
  padding: var(--spacing-4);
  gap: var(--spacing-2);

  /* Radius tokens */
  border-radius: var(--radius-3);

  /* Typography tokens (composite shorthand) */
  font: var(--typography-body-md-regular);
}
```

### In CSS-in-JS / Inline Styles

```tsx
import { cssVars } from '@iress-oss/ids-tokens';

// cssVars gives you the same var() references, but type-safe in JS
<div
  style={{
    background: cssVars.colour.neutral[10],
    border: `1px solid ${cssVars.colour.neutral[30]}`,
    color: cssVars.colour.neutral[80],
    padding: cssVars.spacing[4],
    gap: cssVars.spacing[2],
    borderRadius: cssVars.radius[3],
  }}
>
  Custom card
</div>;
```

### CSS Variable Naming Convention

Variables in `tokens/build/css-vars.css` follow this pattern:

```
--{category}-{path}
```

Examples:

- `--colour-primary-fill`
- `--spacing-4`
- `--radius-1`
- `--typography-heading-1` (shorthand)
- `--typography-heading-_1-fontSize` (decomposed, underscore prefix before token name)

> **Note:** Theme files define `--iress-{category}-{path}` override variables that are referenced as fallback defaults inside the css-vars.css public variables. Use the `--{category}-{path}` public variables in your own CSS — never the `--iress-*` theme overrides directly.

## Common Mistakes

### 1. Hardcoded Values Instead of Tokens

```tsx
// ❌ Wrong
<div style={{ background: '#F5F6F8', padding: '16px', borderRadius: '12px' }}>

// ✅ Correct
<IressStack bg="colour.neutral.20" p="spacing.4" borderRadius="radius.3">
```

### 2. Using Raw HTML Elements

```tsx
// ❌ Wrong — loses IDS typography and theming
<h2>Section Title</h2>
<p>Body text</p>

// ✅ Correct — uses IDS tokens automatically
<IressText element="h2">Section Title</IressText>
<IressText>Body text</IressText>
```

### 3. Recreating Component Styling

```tsx
// ❌ Wrong — manually styling a button
<button style={{
  background: '#003271',
  color: '#FFFFFF',
  borderRadius: '4px',
  padding: '8px 16px'
}}>Submit</button>

// ✅ Correct — IDS handles all styling via mode
<IressButton mode="primary">Submit</IressButton>
```

### 4. Using Wrong Colour Semantic

```tsx
// ❌ Wrong — using primary fill for background
<IressStack bg="colour.primary.fill">Content</IressStack>

// ✅ Correct — use surface variants for backgrounds
<IressStack bg="colour.primary.surface">Content</IressStack>
```

### 5. Non-Existent Token Values

```tsx
// ❌ Wrong — spacing 9 doesn't exist
<IressStack gap="spacing.9">...</IressStack>

// ✅ Correct — use 8 or 10
<IressStack gap="spacing.8">...</IressStack>
```

## Responsive Patterns

Layout components accept responsive objects for spacing props:

```tsx
// Responsive gap: 2 on mobile, 4 on tablet, 6 on desktop
<IressStack gap={{ base: 'spacing.2', md: 'spacing.4', lg: 'spacing.6' }}>
  ...
</IressStack>

// Or use aliases
<IressStack gap={{ base: 'sm', md: 'md', lg: 'lg' }}>
  ...
</IressStack>

// Hide on small screens
<IressStack hideBelow="md">Desktop only</IressStack>
```

## Decision Table: Component Props vs CSS Variables vs cssVars

| Situation                        | Use                                                         |
| -------------------------------- | ----------------------------------------------------------- |
| Spacing on IDS layout components | Props: `gap`, `p`, `m`                                      |
| Colours on IDS components        | Props: `bg`, `color`                                        |
| Custom CSS / SCSS                | CSS variables (`var(--colour-*)`, `var(--spacing-*)`, etc.) |
| Inline styles / CSS-in-JS        | `cssVars` object (`cssVars.colour.neutral[10]`)             |
| Custom CSS with Panda CSS        | `@iress-oss/ids-theme-preset` preset                        |
| Theming / overrides              | CSS variables on custom properties                          |
| Internal theme editors           | `mapTokensToCssVariables()` helper                          |

**General Rule:** Prefer component props when available. For custom styling, use CSS variables in stylesheets or `cssVars` in JavaScript. Only use `mapTokensToCssVariables` / `convertReferencesToVariables` for internal tooling like theme editors.

## Common Mistakes to Avoid

For the full list of common anti-patterns (disabled buttons, redundant textStyle, legacy slot attributes, raw HTML, hardcoded values), read the Common Mistakes guide at `node_modules/@iress-oss/ids-components/.ai/guides/foundations-common-mistakes.md` (requires `@iress-oss/ids-components` to be installed).

## Complete Token Reference

Every available colour, spacing, radius, and typography token with CSS variable names and default values. See [references/token-reference.md](references/token-reference.md).

## Theming

How themes override tokens via CSS variables, scoped theming, and guidance for AI agents. See [references/theming.md](references/theming.md).

## Cross-References

For styling props guides, package references, and links to component-level documentation, see [references/cross-references.md](references/cross-references.md). These require `@iress-oss/ids-components` to be installed.
