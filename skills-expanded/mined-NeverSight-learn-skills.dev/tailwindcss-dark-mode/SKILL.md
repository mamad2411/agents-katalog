---
name: tailwindcss-dark-mode
description: "Use this skill when implementing or debugging dark mode in Tailwind CSS v4. Covers the `dark:` variant, default `prefers-color-scheme` behavior, selector-driven dark mode with `@custom-variant dark`, `.dark` and `data-theme` strategies, three-way system/light/dark toggles, localStorage, server-rendered theme classes, and avoiding FOUC. Triggers on: dark mode, dark:, prefers-color-scheme, .dark, data-theme, theme toggle, system theme, localStorage theme, FOUC."
license: MIT
---

Tailwind's `dark:` variant applies utilities when dark mode is active. By default it follows the user's `prefers-color-scheme`, but you can override it with `@custom-variant dark` for manual toggles.

## Quick Start

```html
<div class="bg-white text-gray-950 dark:bg-gray-950 dark:text-white">
  <!-- ... -->
</div>
```

Manual class-based dark mode:

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
```

```html
<html class="dark">
  <body>
    <div class="bg-white dark:bg-black">...</div>
  </body>
</html>
```

**Related skills:** `tailwindcss-states-variants`, `tailwindcss-functions-directives`, `tailwindcss-colors`, `tailwindcss-compatibility`.

## Core Patterns

### Default system dark mode

No custom CSS is needed when dark mode should follow the OS:

```html
<article class="bg-white p-6 text-gray-950 shadow-sm dark:bg-gray-900 dark:text-white dark:shadow-none">
  <!-- ... -->
</article>
```

### Class-driven dark mode

Use a custom dark variant:

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
```

Toggle the class on an ancestor:

```html
<html class="dark">
  <!-- dark:* utilities apply inside -->
</html>
```

### Data-attribute dark mode

```css
@import "tailwindcss";

@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));
```

```html
<html data-theme="dark">
  <div class="bg-white dark:bg-gray-950">...</div>
</html>
```

### Three-way theme toggle

Use one stored setting with three states:

- `light` - force light class/attribute off
- `dark` - force dark class/attribute on
- system - remove stored preference and follow `matchMedia("(prefers-color-scheme: dark)")`

Apply the theme before first paint where possible:

```html
<script>
  const preference = localStorage.theme;
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  document.documentElement.classList.toggle("dark", preference === "dark" || (!preference && systemDark));
</script>
```

For server-rendered apps, render the class or attribute on `html` from a cookie to avoid a flash.

## Common Mistakes

### [HIGH] Defining a manual toggle but not overriding `dark`

Adding `class="dark"` does nothing if the `dark` variant is still using `prefers-color-scheme`. Add `@custom-variant dark`.

### [HIGH] Running theme JavaScript after render

If the page paints light before JavaScript switches to dark, users see a flash. Inline the initial script in `head` or render the theme on the server.

### [MEDIUM] Styling only backgrounds

Dark mode needs foreground, border, ring, shadow, divide, placeholder, and interactive state colors too. Audit the whole component, not just `bg-*`.

## API Reference

- Dark mode: `https://tailwindcss.com/docs/dark-mode`
- Custom variants: `https://tailwindcss.com/docs/functions-and-directives#custom-variant-directive`
- Color utilities: `https://tailwindcss.com/docs/colors`
