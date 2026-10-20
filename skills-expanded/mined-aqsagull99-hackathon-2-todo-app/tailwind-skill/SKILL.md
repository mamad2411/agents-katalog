---
name: tailwind-skill
description: Reusable Tailwind CSS skill with utility class patterns, responsive design, component styling, and common layouts. Use with context7 MCP server for documentation.
---

# Tailwind CSS Skill

Use this skill when styling React components with Tailwind CSS utility classes.

## MCP Documentation

| MCP Server | Use For |
|------------|---------|
| `context7` | Tailwind CSS documentation, utility classes, configuration |

**Fetch Tailwind docs:** `@context7:get-library-docs` with topic like "utility-classes", "responsive-design", "forms", "flexbox", "grid"

## Layout Utilities

### Container
```html
<div class="container mx-auto px-4">
  <!-- Content centered with horizontal padding -->
</div>
```

### Flexbox
```html
<!-- Basic flex -->
<div class="flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Flex with alignment -->
<div class="flex items-center justify-between">
  <div>Left</div>
  <div>Right</div>
</div>

<!-- Flex direction -->
<div class="flex flex-col gap-4">
  <!-- Stacked vertically -->
</div>

<!-- Flex grow/shrink -->
<div class="flex-1">Grows to fill space</div>
<div class="shrink-0">Won't shrink</div>
```

### Grid
```html
<!-- Basic grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Responsive grid items -->
</div>

<!-- Grid with spans -->
<div class="grid grid-cols-4 gap-4">
  <div class="col-span-1">Spans 1 column</div>
  <div class="col-span-3">Spans 3 columns</div>
</div>
```

### Spacing

#### Margins
```html
<!-- All sides -->
<div class="m-4">margin: 1rem</div>

<!-- Vertical/Horizontal -->
<div class="my-4 mx-2">my=1rem, mx=0.5rem</div>

<!-- Individual sides -->
<div class="mt-4 mr-2 mb-4 ml-2">
  <!-- mt=margin-top, mr=margin-right, etc. -->
</div>

<!-- Auto -->
<div class="mx-auto">Center horizontally</div>
```

#### Padding
```html
<!-- All sides -->
<div class="p-4">padding: 1rem</div>

<!-- Individual sides -->
<div class="px-4 py-2">px=horizontal, py=vertical</div>
```

## Typography Utilities

```html
<!-- Font size -->
<h1 class="text-4xl">4xl = 2.25rem</h1>
<h2 class="text-2xl">2xl = 1.5rem</h2>
<p class="text-base">base = 1rem</p>
<p class="text-sm">sm = 0.875rem</p>
<p class="text-xs">xs = 0.75rem</p>

<!-- Font weight -->
<p class="font-bold">Bold</p>
<p class="font-semibold">Semibold</p>
<p class="font-medium">Medium</p>
<p class="font-normal">Normal</p>

<!-- Text alignment -->
<p class="text-left">Left</p>
<p class="text-center">Center</p>
<p class="text-right">Right</p>

<!-- Line height -->
<p class="leading-tight">Tight (1.25)</p>
<p class="leading-normal">Normal (1.5)</p>
<p class="leading-relaxed">Relaxed (1.625)</p>

<!-- Text color -->
<p class="text-gray-900">Darkest</p>
<p class="text-gray-600">Medium</p>
<p class="text-gray-400">Light</p>
```

## Color Utilities

### Text Colors
```html
<p class="text-black">Black</p>
<p class="text-white">White</p>
<p class="text-gray-900">Gray 900</p>
<p class="text-blue-600">Blue 600</p>
<p class="text-red-500">Red 500</p>
<p class="text-green-500">Green 500</p>
```

### Background Colors
```html
<div class="bg-white">White bg</div>
<div class="bg-gray-50">Gray 50</div>
<div class="bg-blue-600">Blue 600</div>
<div class="bg-red-100">Light red</div>
```

### Opacity with Colors
```html
<!-- text-opacity -->
<p class="text-gray-500/50">50% opacity</p>

<!-- bg-opacity -->
<div class="bg-blue-600/80">80% opacity</div>

<!-- Arbitrary values -->
<p class="text-gray-900/[0.87]">Using slash notation</p>
```

## Border Utilities

```html
<!-- Border width -->
<div class="border">1px border</div>
<div class="border-2">2px border</div>
<div class="border-4">4px border</div>

<!-- Border sides -->
<div class="border-t">Top only</div>
<div class="border-r">Right only</div>
<div class="border-b">Bottom only</div>
<div class="border-l">Left only</div>

<!-- Border color -->
<div class="border border-gray-300">Gray border</div>

<!-- Border radius -->
<div class="rounded">Default (0.25rem)</div>
<div class="rounded-md">Medium (0.375rem)</div>
<div class="rounded-lg">Large (0.5rem)</div>
<div class="rounded-xl">XL (0.75rem)</div>
<div class="rounded-2xl">2XL (1rem)</div>
<div class="rounded-full">Full circle</div>
```

## Shadow Utilities

```html
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Default shadow</div>
<div class="shadow-md">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">XL shadow</div>
<div class="shadow-2xl">2XL shadow</div>
<div class="shadow-none">No shadow</div>
```

## Responsive Design

### Breakpoints
```html
<!-- Mobile first (default) -->
<div class="block">Mobile</div>

<!-- sm: 640px -->
<div class="sm:block md:flex">Changes at 640px</div>

<!-- md: 768px -->
<div class="md:w-1/2">Half width at 768px+</div>

<!-- lg: 1024px -->
<div class="lg:w-1/3">One third at 1024px+</div>

<!-- xl: 1280px -->
<div class="xl:w-1/4">One quarter at 1280px+</div>

<!-- 2xl: 1536px -->
<div class="2xl:hidden">Hidden on very large</div>
```

### Responsive Example
```html
<div class="
  w-full
  md:w-1/2
  lg:w-1/3
  xl:w-1/4
">
  <!-- 100% mobile, 50% tablet, 33% desktop, 25% XL -->
</div>
```

## State Utilities

### Hover
```html
<button class="hover:bg-blue-700">Hover effect</button>
<div class="hover:shadow-lg">Lift on hover</div>
```

### Focus
```html
<input class="focus:ring-2 focus:ring-blue-500">
<button class="focus:outline-none">Remove outline</button>
```

### Active
```html
<button class="active:bg-blue-800">Active state</button>
```

### Disabled
```html
<button class="disabled:opacity-50 disabled:cursor-not-allowed">
  Disabled button
</button>
```

### Transitions
```html
<div class="transition-colors duration-200">Smooth transition</div>
<div class="transition-all duration-300 ease-in-out">
  All properties with easing
</div>
```

## Common Component Patterns

### Button
```html
<button class="
  inline-flex
  items-center
  justify-center
  px-4
  py-2
  bg-blue-600
  text-white
  font-medium
  rounded-lg
  hover:bg-blue-700
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
  transition-colors
">
  Button Text
</button>
```

### Input
```html
<input
  type="text"
  class="
    w-full
    px-4
    py-2
    border
    border-gray-300
    rounded-lg
    focus:ring-2
    focus:ring-blue-500
    focus:border-transparent
    outline-none
  "
  placeholder="Enter text..."
/>
```

### Card
```html
<div class="
  bg-white
  rounded-xl
  shadow-sm
  border
  border-gray-200
  p-6
">
  <!-- Card content -->
</div>
```

### Badge
```html
<span class="
  inline-flex
  items-center
  px-2.5
  py-0.5
  rounded-full
  text-xs
  font-medium
  bg-blue-100
  text-blue-800
">
  Badge text
</span>
```

## Best Practices

1. Use utility classes over custom CSS when possible
2. Compose small utilities for complex components
3. Use `group` and `group-hover` for parent-child hover effects
4. Use `dark:` prefix for dark mode
5. Use `@apply` sparingly (only for repeated patterns)
6. Keep responsive classes at the end
7. Use `gap` for spacing between flex/grid items
8. Use `space-y` for vertical spacing between children
9. Configure custom theme values in `tailwind.config.js`
10. Use `@tailwindcss/forms` plugin for form styling
