---
name: tailwindcss-source-detection
description: "Use this skill when Tailwind CSS v4 is not generating expected classes or when configuring source scanning. Covers plain-text class detection, complete class names, dynamic class pitfalls, mapping props to static class strings, ignored files, `@source`, `source()` import base paths, `source(none)`, `@source not`, `@source inline()` safelisting, brace expansion, and excluding generated classes. Triggers on: missing class, class not generated, dynamic class, bg-${color}, @source, safelist, source(none), source inline, source not, scan files, content config."
license: MIT
---

Tailwind scans source files as plain text and generates CSS for tokens that map to known utilities. It does not parse JavaScript, JSX, Vue, Svelte, or template expressions.

## Quick Start

Wrong:

```jsx
<button className={`bg-${color}-600 hover:bg-${color}-500`} />
```

Correct:

```jsx
const colorVariants = {
  blue: "bg-blue-600 hover:bg-blue-500",
  red: "bg-red-600 hover:bg-red-500",
};

<button className={colorVariants[color]} />;
```

**Related skills:** `tailwindcss-core-concepts`, `tailwindcss-functions-directives`, `tailwindcss-custom-styles`, `tailwindcss-installation`.

## Core Patterns

### Keep class names complete

Tailwind only sees complete class strings:

```html
<div class="{{ error ? 'text-red-600' : 'text-green-600' }}"></div>
```

This is detectable because both full class names exist in the source.

### Files scanned by default

Tailwind scans project source files and skips common non-source locations such as:

- files ignored by `.gitignore`
- `node_modules`
- binary files
- CSS files
- common lock files

If an external package or unusual directory contains classes, register it explicitly.

### Register sources

```css
@import "tailwindcss";

@source "../node_modules/@acmecorp/ui-lib";
```

Set the base path for automatic detection:

```css
@import "tailwindcss" source("../src");
```

Disable automatic detection and register everything explicitly:

```css
@import "tailwindcss" source(none);

@source "../admin";
@source "../shared";
```

Exclude a path:

```css
@source not "../src/components/legacy";
```

### Safelist generated classes

Use `@source inline()` when a class must be generated even though it is not present in content:

```css
@source inline("underline");
@source inline("{hover:,focus:,}underline");
```

Brace expansion can generate ranges:

```css
@source inline("{hover:,}bg-red-{50,{100..900..100},950}");
```

Exclude generated classes explicitly:

```css
@source not inline("{hover:,focus:,}bg-red-{50,{100..900..100},950}");
```

## Debug Checklist

1. Confirm the CSS entry imports Tailwind and is loaded by the app.
2. Confirm the class exists as a complete string in a scanned file.
3. Check `.gitignore`, `node_modules`, generated files, and external package locations.
4. Add `@source` for external/shared UI packages.
5. Use `@source inline()` only when static class strings or source registration are not possible.

## Common Mistakes

### [HIGH] Looking for a v3 `content` array in v4

Tailwind v4 uses automatic source detection and `@source`. Do not add old `content` configuration unless working in a v3 project or a legacy `@config` migration.

### [HIGH] Building class names with interpolation

Interpolation creates strings Tailwind never sees. Map props to static class strings.

### [MEDIUM] Safelisting too broadly

Safelisting large ranges bloats CSS. Prefer explicit class maps or targeted `@source inline()` patterns.

## API Reference

- Detecting classes in source files: `https://tailwindcss.com/docs/detecting-classes-in-source-files`
- Functions and directives: `https://tailwindcss.com/docs/functions-and-directives#source-directive`
