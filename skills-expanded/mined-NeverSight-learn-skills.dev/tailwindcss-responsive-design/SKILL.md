---
name: tailwindcss-responsive-design
description: "Use this skill when building responsive Tailwind CSS v4 interfaces. Covers mobile-first breakpoints (`sm`, `md`, `lg`, `xl`, `2xl`), max breakpoint ranges, arbitrary min/max media variants, custom `--breakpoint-*` variables, container queries with `@container`, max/named containers, `@container-size`, custom `--container-*` sizes, and container query units. Triggers on: responsive, breakpoint, mobile first, sm:, md:, lg:, max-md, min-[...], max-[...], @container, @container-size, @sm, @max-md, container query."
license: MIT
---

Tailwind responsive variants are mobile-first. Unprefixed utilities apply at all sizes; breakpoint-prefixed utilities apply at that breakpoint and up.

## Quick Start

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

```html
<section class="mx-auto max-w-md p-4 sm:max-w-2xl sm:p-6 lg:max-w-5xl lg:p-8">
  <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
    <!-- cards -->
  </div>
</section>
```

**Related skills:** `tailwindcss-states-variants`, `tailwindcss-theme`, `tailwindcss-spacing-sizing`, `tailwindcss-flex-grid`.

## Core Patterns

### Default breakpoints

| Prefix | Minimum width |
|---|---|
| `sm` | `40rem` / `640px` |
| `md` | `48rem` / `768px` |
| `lg` | `64rem` / `1024px` |
| `xl` | `80rem` / `1280px` |
| `2xl` | `96rem` / `1536px` |

Use unprefixed classes for the base mobile layout:

```html
<div class="text-center sm:text-left">
  <!-- centered on mobile, left-aligned at sm and up -->
</div>
```

### Breakpoint ranges

Stack a min breakpoint with a `max-*` variant:

```html
<div class="md:max-xl:flex">
  <!-- flex only from md up to before xl -->
</div>
```

Target one-off media ranges with arbitrary variants:

```html
<div class="min-[320px]:text-center max-[600px]:bg-sky-50">
  <!-- ... -->
</div>
```

### Custom breakpoints

Define breakpoints with `--breakpoint-*` theme variables:

```css
@import "tailwindcss";

@theme {
  --breakpoint-xs: 30rem;
  --breakpoint-3xl: 120rem;
}
```

Use the new prefixes:

```html
<div class="xs:grid 3xl:max-w-7xl">
  <!-- ... -->
</div>
```

Use `rem` when extending the default breakpoint scale so sorting stays predictable.

### Container queries

Use container queries when component layout depends on parent size rather than viewport size:

```html
<article class="@container rounded-lg border p-4">
  <div class="flex flex-col gap-4 @md:flex-row">
    <img class="h-32 w-full rounded object-cover @md:w-48" alt="" />
    <div>
      <h2 class="text-lg font-semibold">Card title</h2>
      <p class="text-sm/6 text-gray-600">Card body.</p>
    </div>
  </div>
</article>
```

Container queries are also mobile-first.

### Max and range container queries

```html
<div class="@container">
  <div class="flex flex-row @max-md:flex-col @sm:@max-lg:gap-6">
    <!-- ... -->
  </div>
</div>
```

### Named containers

```html
<section class="@container/main">
  <aside class="@lg/main:block hidden">Sidebar</aside>
</section>
```

Use names when nested containers make "nearest container" behavior ambiguous.

### Size containers

Tailwind CSS v4.3 adds `@container-size` for container queries that need block-size units like `cqb` or `cqh`:

```html
<div class="@container-size">
  <div class="h-[50cqb]">
    <!-- ... -->
  </div>
</div>
```

Named size containers use `@container-size/{name}`.

### Custom container sizes

```css
@theme {
  --container-8xl: 96rem;
}
```

Then use `@8xl:` as a container query variant.

## Common Mistakes

### [HIGH] Treating `sm:` as mobile

Wrong:

```html
<div class="sm:text-center"></div>
```

This centers text at `sm` and above, not below `sm`.

Correct:

```html
<div class="text-center sm:text-left"></div>
```

### [MEDIUM] Using viewport breakpoints for reusable cards

If a card can live in different layout slots, use `@container` so it responds to its own available width.

### [MEDIUM] Using `px` for custom breakpoints beside defaults

Use `rem` with the default breakpoint scale unless replacing all breakpoints.

## API Reference

- Responsive design: `https://tailwindcss.com/docs/responsive-design`
- Theme variables: `https://tailwindcss.com/docs/theme`
- v4.3 release notes for `@container-size`: `https://tailwindcss.com/blog/tailwindcss-v4-3`
