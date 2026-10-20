---
applyTo:
  - 'resources/views/**'
  - 'app/Livewire/**'
  - 'app/Filament/**'
  - '**/*.blade.php'
description: |
  Tailwind CSS 3 utility classes, responsive design, dark mode patterns,
  and component composition for ICTServe project.
tags:
  - tailwind
  - css
  - responsive
  - dark-mode
  - accessibility
version: '1.1.0'
lastUpdated: '2025-11-30'
---

# Tailwind CSS 3 — ICTServe Styling Standards

## Overview

This rule defines Tailwind CSS 3 utility class conventions for ICTServe. It covers responsive design, dark mode support, spacing, typography, component patterns, and accessibility-focused styling aligned with WCAG 2.2 AA.

| Attribute | Value |
| :--- | :--- |
| **Framework** | Tailwind CSS 3.4+ (Latest Stable) |
| **Applies To** | Blade views, Livewire components, Filament customizations |
| **Traceability** | D14 (UI/UX Design Guide), D15 (Accessibility Requirements), WCAG 2.2 AA |

## Core Principles

1. **Utility-First**: Use utility classes before creating custom CSS.
2. **Responsive by Default**: Mobile-first design with breakpoint modifiers.
3. **Dark Mode Support**: Use `dark:` prefix for dark mode variants.
4. **Consistent Spacing**: Use Tailwind's spacing scale (1 unit = 0.25rem).
5. **Accessible Colors**: Ensure sufficient contrast ratios (WCAG 2.2 AA).

## Spacing System

Tailwind Spacing Scale (1 unit = 0.25rem = 4px):

| Class | Size | Pixels | Use Case |
| :--- | :--- | :--- | :--- |
| `p-1` | 0.25rem | 4px | Tight padding |
| `p-2` | 0.5rem | 8px | Small padding |
| `p-4` | 1rem | 16px | Standard padding |
| `p-6` | 1.5rem | 24px | Medium padding |
| `p-8` | 2rem | 32px | Large padding |
| `p-12` | 3rem | 48px | Extra large padding |

### Use Gap for Spacing Lists (NOT Margins)

**Good:**

```html
<div class="flex gap-8">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
````

**Bad:**

```html
<div class="flex">
    <div class="mr-8">Item 1</div>
    <div class="mr-8">Item 2</div>
    <div>Item 3</div>
</div>
```

## Responsive Design (Mobile-First)

### Breakpoint Modifiers

| Prefix | Min Width | Device |
| :--- | :--- | :--- |
| (none) | 0px | Mobile (default) |
| `sm:` | 640px | Small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

### Mobile-First Pattern

```html
<div class="w-full md:w-1/2 lg:w-1/3">
    Content
</div>

<div class="text-sm sm:text-base lg:text-lg">
    Responsive Text
</div>

<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
```

## Dark Mode Support

### Enable Dark Mode

Configuration in `tailwind.config.js`:

```javascript
module.exports = {
  darkMode: 'class', // or 'media' for system preference
  // ... rest of config
}
```

### Dark Mode Classes

```html
<div class="bg-white dark:bg-gray-800">
    Content adapts to dark mode
</div>

<p class="text-gray-900 dark:text-gray-100">
    Text with dark mode variant
</p>

<div class="border border-gray-300 dark:border-gray-700">
    Border adapts to dark mode
</div>
```

### Complete Dark Mode Component

```html
<div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
    <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        Tajuk Kad
    </h2>
    <p class="text-gray-600 dark:text-gray-400">
        Keterangan yang sesuai untuk mod gelap dan terang.
    </p>
    <button class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Tindakan
    </button>
</div>
```

## Layout Patterns

### Flexbox

**Horizontal Layout:**

```html
<div class="flex items-center justify-between gap-4">
    <div>Left</div>
    <div>Center</div>
    <div>Right</div>
</div>
```

**Vertical Layout:**

```html
<div class="flex flex-col gap-4">
    <div>Top</div>
    <div>Middle</div>
    <div>Bottom</div>
</div>
```

**Centered Content:**

```html
<div class="flex items-center justify-center min-h-screen">
    <div>Centered Vertically & Horizontally</div>
</div>
```

### Grid Layout

**Equal Columns:**

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div>Column 1</div>
    <div>Column 2</div>
    <div>Column 3</div>
</div>
```

**Custom Column Widths:**

```html
<div class="grid grid-cols-12 gap-4">
    <div class="col-span-12 md:col-span-8">Main Content (8/12)</div>
    <div class="col-span-12 md:col-span-4">Sidebar (4/12)</div>
</div>
```

**Auto-Fit Grid (Responsive Without Breakpoints):**

```html
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
    <div>Card 1</div>
    <div>Card 2</div>
    <div>Card 3</div>
</div>
```

## Typography

### Text Sizes

```html
<h1 class="text-4xl font-bold">Heading 1</h1>
<h2 class="text-3xl font-semibold">Heading 2</h2>
<h3 class="text-2xl font-semibold">Heading 3</h3>
<p class="text-base">Body text (16px default)</p>
<small class="text-sm">Small text (14px)</small>
```

### Font Weights

```html
<p class="font-thin">Thin (100)</p>
<p class="font-light">Light (300)</p>
<p class="font-normal">Normal (400)</p>
<p class="font-medium">Medium (500)</p>
<p class="font-semibold">Semibold (600)</p>
<p class="font-bold">Bold (700)</p>
<p class="font-extrabold">Extra Bold (800)</p>
```

### Text Colors (Accessible)

**Light Mode:**

```html
<p class="text-gray-900">Primary text (highest contrast)</p>
<p class="text-gray-600">Secondary text</p>
<p class="text-gray-400">Muted text</p>
```

**Dark Mode:**

```html
<p class="dark:text-gray-100">Primary text (dark mode)</p>
<p class="dark:text-gray-400">Secondary text (dark mode)</p>
<p class="dark:text-gray-600">Muted text (dark mode)</p>
```

## Color System

### Semantic Colors (ICTServe Palette)

```html
<button class="bg-blue-600 text-white">Primary Action</button>

<div class="bg-green-100 border border-green-500 text-green-700 p-4">
    Operasi berjaya!
</div>

<div class="bg-amber-100 border border-amber-500 text-amber-700 p-4">
    Amaran: Sila semak maklumat.
</div>

<div class="bg-red-100 border border-red-500 text-red-700 p-4">
    Ralat: Sesuatu tidak kena.
</div>

<div class="bg-cyan-100 border border-cyan-500 text-cyan-700 p-4">
    Maklumat: Nota penting.
</div>
```

## Component Patterns

### Card Component

```html
<div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-md overflow-hidden">
    <div class="p-6">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
            Tajuk Kad
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
            Keterangan kad yang ringkas dan jelas.
        </p>
        <button class="px-4 py-2 bg-blue-600 text-white rounded">
            Tindakan
        </button>
    </div>
</div>
```

### Button Variants

```html
<button class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded">
    Primary
</button>

<button class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded">
    Secondary
</button>

<button class="border border-blue-600 text-blue-600 hover:bg-blue-50 font-medium py-2 px-4 rounded">
    Outline
</button>

<button class="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded">
    Delete
</button>

<button class="bg-gray-400 text-white font-medium py-2 px-4 rounded cursor-not-allowed opacity-50" disabled>
    Disabled
</button>
```

### Form Input

```html
<div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
        Nama Aset
    </label>
    <input type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600">
    <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
        Nama penuh aset yang ingin didaftarkan.
    </p>
</div>

<div class="mb-4">
    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
        E-mel
    </label>
    <input type="email" class="mt-1 block w-full rounded-md border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:ring-red-500">
    <p class="mt-1 text-sm text-red-600">
        Format e-mel tidak sah.
    </p>
</div>
```

### Badge Component

```html
<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
    Tersedia
</span>

<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200">
    Dipinjam
</span>

<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">
    Dilupuskan
</span>
```

### Alert Component

```html
<div class="bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500 p-4">
    <div class="flex">
        <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
            </svg>
        <div class="ml-3">
            <p class="text-sm font-medium text-green-800 dark:text-green-200">
                Aset berjaya didaftarkan!
            </p>
        </div>
    </div>
</div>

<div class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4">
    <div class="flex">
        <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            </svg>
        <div class="ml-3">
            <p class="text-sm font-medium text-red-800 dark:text-red-200">
                Ralat: Kod aset telah wujud.
            </p>
        </div>
    </div>
</div>
```

### Modal/Dialog

```html
<div aria-modal="true" aria-labelledby="modal-title" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>

    <div class="flex items-center justify-center min-h-screen p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-lg w-full p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Padam Aset
            </h3>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
                Adakah anda pasti mahu memadam aset ini? Tindakan ini tidak boleh dibatalkan.
            </p>
            <div class="flex justify-end gap-3">
                <button class="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300">
                    Batal
                </button>
                <button class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                    Padam
                </button>
            </div>
        </div>
    </div>
</div>
```

## Accessibility (WCAG 2.2 AA)

### Focus States (Required)

Always include visible focus indicators:

**Good:**

```html
<button class="focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
    Button with Focus State
</button>
```

**Bad:**

```html
<button class="outline-none">
    Button WITHOUT Focus State
</button>
```

### Color Contrast

Minimum Contrast Ratios (WCAG 2.2 AA):

* Normal text: 4.5:1
* Large text (18px+ or 14px+ bold): 3:1

**Accessible Color Combinations:**

```html
<p class="text-gray-900 bg-white">Black on White (21:1)</p>
<p class="text-white bg-blue-600">White on Blue-600 (4.5:1)</p>
```

**Inaccessible:**

```html
<p class="text-gray-400 bg-white">Gray-400 on White (2.8:1) — FAILS</p>
```

### Screen Reader Support

Use Semantic HTML + ARIA:

```html
<button aria-label="Close menu" class="...">
    ...
</button>

<svg aria-hidden="true" class="...">...</svg>

<button aria-busy="true" class="...">
    Sedang memuatkan...
</button>
```

### Screen Reader Only Text

```html
<span class="sr-only">Maklumat untuk pembaca skrin sahaja</span>
```

## Animations and Transitions

### Smooth Transitions

```html
<button class="transition duration-150 ease-in-out hover:bg-blue-700">
    Hover Me
</button>

<div class="opacity-0 hover:opacity-100 transform hover:scale-105 transition-all duration-300">
    Fade & Scale
</div>
```

### Loading Spinner

```html
<svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
    </svg>
```

### Respect Reduced Motion Preference

```html
<div class="transition-transform duration-300 motion-reduce:transition-none">
    Animation disabled if user prefers reduced motion
</div>
```

## Custom Utilities (Extend Tailwind)

### Add Custom Colors

Configuration in `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        'motac': {
          '50': '#eff6ff',
          '100': '#dbeafe',
          '500': '#3b82f6',
          '600': '#2563eb',
          '700': '#1d4ed8',
        },
      },
    },
  },
}
```

**Usage:**

```html
<button class="bg-motac-600 text-white">
    MOTAC Brand Button
</button>
```

## Performance Best Practices

### Purge Unused CSS

Vite handles this automatically:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './resources/**/*.blade.php',
    './resources/**/*.js',
    './app/Filament/**/*.php',
  ],
}
```

### Avoid @apply in Production

Use utility classes directly instead of `@apply` directive to maintain small file sizes.

### Use JIT Mode

JIT (Just-In-Time) mode is default in Tailwind 3.

```javascript
// tailwind.config.js
module.exports = {
  // mode: 'jit', // No longer needed in v3 (enabled by default)
}
```

## Common Pitfalls

### Avoid These Patterns

**Using Inline Styles Instead of Utilities:**

```html
<div style="padding: 16px; background: white;">Bad</div>

<div class="p-4 bg-white">Good</div>
```

**Overusing @apply Directive:**

```css
/* ❌ BAD: styles.css */
.btn {
    @apply bg-blue-600 text-white px-4 py-2 rounded;
}
```

**Missing Dark Mode Variants:**

```html
<div class="bg-white text-gray-900">No dark mode</div>

<div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">With dark mode</div>
```

**Poor Color Contrast:**

```html
<p class="text-gray-400 bg-white">Low contrast (WCAG fail)</p>

<p class="text-gray-900 bg-white">High contrast (WCAG pass)</p>
```

**No Focus States:**

```html
<button class="outline-none">No visible focus</button>

<button class="focus:ring-2 focus:ring-blue-500">Visible focus</button>
```

## References and Resources

* **Tailwind CSS 3 Documentation**: [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
* **Tailwind UI Components**: [https://tailwindui.com](https://tailwindui.com)
* **Heroicons (Free SVG icons)**: [https://heroicons.com](https://heroicons.com)
* **Color Contrast Checker**: [https://webaim.org/resources/contrastchecker/](https://webaim.org/resources/contrastchecker/)
* **ICTServe Traceability**: D14 (UI/UX Design Guide), D15 (Accessibility Requirements), WCAG 2.2 AA

## Compliance Checklist

When using Tailwind CSS, ensure:

* [ ] Use utility classes instead of custom CSS.
* [ ] Apply mobile-first responsive design.
* [ ] Include dark mode variants with `dark:` prefix.
* [ ] Use `gap` utilities for spacing (not margins) in flex/grid.
* [ ] Ensure WCAG 2.2 AA color contrast (4.5:1 for text).
* [ ] Add visible focus states to all interactive elements.
* [ ] Use semantic HTML with ARIA attributes.
* [ ] Include `sr-only` class for screen reader text.
* [ ] Respect `motion-reduce` preference for animations.
* [ ] Test across mobile, tablet, and desktop breakpoints.

| Field | Value |
| :--- | :--- |
| **Status** | ✅ Active for ICTServe Tailwind CSS 3 development |
| **Version** | 1.1.0 |
| **Last Updated** | 2025-11-30 |
