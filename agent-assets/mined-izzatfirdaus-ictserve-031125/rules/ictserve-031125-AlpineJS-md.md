---
applyTo:
  - 'resources/views/**'
  - 'resources/js/**'
  - '**/*.blade.php'
description: |
  Alpine.js 3 reactive directives, state management, plugins, and integration patterns
  for ICTServe project. Lightweight JavaScript framework for interactive UI components.
tags:
  - alpinejs
  - javascript
  - reactive
  - frontend
  - directives
version: '1.2.0'
lastUpdated: '2025-11-30'
---

# Alpine.js 3 — ICTServe Interactive UI Standards

## Overview

Alpine.js is a rugged, minimal tool for composing behavior directly in your markup. It offers the reactive and declarative nature of frameworks like Vue or React at a much lower cost. Alpine.js works by providing a set of directives you can add to your HTML.

| Attribute | Value |
| :--- | :--- |
| **Framework** | Alpine.js 3.14.7 (Latest Stable) |
| **Applies To** | Blade views, Livewire components, interactive UI elements |
| **Traceability** | D13 (UI/UX Frontend Framework), D14 (UI/UX Design Guide) |
| **Bundle Size** | ~17kB minified, ~6.5kB gzipped |

## Core Principles

1. **Declarative Syntax**: Define behavior directly in HTML with `x-` directives.
2. **Reactive State**: Use `x-data` for component state management.
3. **Minimal JavaScript**: Avoid external JS files when Alpine suffices.
4. **Livewire Integration**: Alpine is bundled with Livewire 3 automatically.
5. **Progressive Enhancement**: Start with HTML, enhance with Alpine.
6. **No Build Step**: Works directly in the browser without compilation.

## What is New in Alpine.js 3.14

* Improved TypeScript support with better type definitions.
* Enhanced `x-teleport` for portal-like functionality.
* Better CSP (Content Security Policy) support with `Alpine.csp` build.
* Improved `$id()` magic for generating unique IDs.
* New `x-modelable` directive for custom component inputs.
* Performance optimizations in reactivity system.
* Better error messages and debugging experience.
* Improved memory management for large applications.

## Installation and Setup

### With Livewire 3 (Recommended for ICTServe)

Alpine.js is bundled with Livewire 3. No separate installation is required.

```blade
{{-- In your layout file, Alpine.js loads automatically --}}
@livewireScripts
````

### CDN Installation

For standalone use without Livewire:

```html
<script defer src="[https://cdn.jsdelivr.net/npm/alpinejs@3.14.7/dist/cdn.min.js](https://cdn.jsdelivr.net/npm/alpinejs@3.14.7/dist/cdn.min.js)"></script>
```

```html
<script defer src="[https://cdn.jsdelivr.net/npm/@alpinejs/persist@3.14.7/dist/cdn.min.js](https://cdn.jsdelivr.net/npm/@alpinejs/persist@3.14.7/dist/cdn.min.js)"></script>
<script defer src="[https://cdn.jsdelivr.net/npm/alpinejs@3.14.7/dist/cdn.min.js](https://cdn.jsdelivr.net/npm/alpinejs@3.14.7/dist/cdn.min.js)"></script>
```

### NPM Installation

```bash
npm install alpinejs@3.14.7
```

```javascript
// resources/js/app.js
import Alpine from 'alpinejs'

// Register plugins before starting (if needed)
// import persist from '@alpinejs/persist'
// Alpine.plugin(persist)

// Make Alpine available globally for debugging
window.Alpine = Alpine

// Start Alpine
Alpine.start()
```

### Vite Configuration for Laravel

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import laravel from 'laravel-vite-plugin'

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true,
        }),
    ],
    optimizeDeps: {
        include: ['alpinejs'],
    },
})
```

-----

## Directives Reference

### x-data — Component State

The `x-data` directive declares a new Alpine component and its reactive data.

```html
{{-- Simple boolean state --}}
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open">Content here</div>
</div>

{{-- Multiple properties --}}
<div x-data="{ name: '', email: '', age: 0 }">
    {{-- Component content --}}
</div>

{{-- With methods --}}
<div x-data="{ 
    count: 0, 
    increment() { this.count++ }, 
    decrement() { this.count-- }, 
    reset() { this.count = 0 } 
}">
    <button @click="decrement">-</button>
    <span x-text="count"></span>
    <button @click="increment">+</button>
    <button @click="reset">Reset</button>
</div>

{{-- With getters --}}
<div x-data="{ 
    firstName: 'John', 
    lastName: 'Doe', 
    get fullName() { return this.firstName + ' ' + this.lastName } 
}">
    <p x-text="fullName"></p>
</div>
```

**Reusable Components with Alpine.data()**:

```javascript
document.addEventListener('alpine:init', () => {
    Alpine.data('dropdown', () => ({
        open: false,
        toggle() {
            this.open = !this.open
        },
        close() {
            this.open = false
        },
        init() {
            console.log('Dropdown initialized')
        },
        destroy() {
            console.log('Dropdown destroyed')
        }
    }))
})
```

```html
{{-- Use the reusable component --}}
<div x-data="dropdown">
    <button @click="toggle">Menu</button>
    <div x-show="open" @click.outside="close">
        Dropdown content
    </div>
</div>
```

### x-init — Initialization

Run code when component initializes.

```html
{{-- Simple initialization --}}
<div x-data="{ message: '' }" x-init="message = 'Hello World'">
    <p x-text="message"></p>
</div>

{{-- Async initialization --}}
<div x-data="{ users: [] }" x-init="users = await (await fetch('/api/users')).json()">
    <template x-for="user in users" :key="user.id">
        <p x-text="user.name"></p>
    </template>
</div>

{{-- Using $nextTick for DOM operations --}}
<div x-data="{ show: false }" x-init="show = true; $nextTick(() => $refs.input.focus())">
    <input x-ref="input" x-show="show">
    <span x-show="show">Ready!</span>
</div>
```

### x-show — Visibility Toggle

Toggle element visibility while keeping it in the DOM (toggles `display: none`).

```html
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    
    {{-- Default transition --}}
    <div x-show="open" x-transition>
        Fades in and out
    </div>
    
    {{-- Scale transition --}}
    <div x-show="open" x-transition.scale>
        Scales in and out
    </div>

    {{-- Important modifier --}}
    <div x-show.important="open">
        Uses !important on display property
    </div>
</div>
```

### x-if — Conditional Rendering

Completely add or remove elements from the DOM. Must be used on a `<template>` tag.

```html
<div x-data="{ show: false }">
    <button @click="show = !show">Toggle</button>
    
    <template x-if="show">
        <p>This element is completely removed when hidden</p>
    </template>
</div>
```

> **When to use x-if vs x-show:**
>
> * Use `x-show` for frequent toggles (better performance).
> * Use `x-if` when you need the element completely removed (e.g., stopping video playback, heavy initial render).

### x-for — List Rendering

Iterate over arrays and objects. Must be used on a `<template>` tag.

```html
{{-- Simple array --}}
<div x-data="{ items: ['Apple', 'Banana', 'Orange'] }">
    <ul>
        <template x-for="item in items" :key="item">
            <li x-text="item"></li>
        </template>
    </ul>
</div>

{{-- With index --}}
<div x-data="{ items: ['First', 'Second', 'Third'] }">
    <ul>
        <template x-for="(item, index) in items" :key="index">
            <li><span x-text="index + 1"></span>: <span x-text="item"></span></li>
        </template>
    </ul>
</div>

{{-- Range --}}
<template x-for="i in 10">
    <span x-text="i"></span>
</template>
```

### x-on — Event Handling

Listen to DOM events. Shorthand: `@`.

```html
{{-- Basic click --}}
<button @click="alert('Hello')">Say Hi</button>

{{-- Accessing event object --}}
<button @click="console.log($event)">Log Event</button>

{{-- Key Modifiers --}}
<input @keyup.enter="submitForm">
<input @keyup.escape="closeModal">

{{-- Event Modifiers --}}
<form @submit.prevent="submitData">...</form>
<button @click.stop="doSomething">Stop Propagation</button>
<button @click.once="init">Run Once</button>
<div @scroll.window="handleScroll">Window Scroll</div>
<div @click.outside="close">Click Outside</div>

{{-- Debounce/Throttle --}}
<input @input.debounce.500ms="fetchResults">
<div @scroll.throttle.100ms="handleScroll">
```

### x-model — Two-Way Binding

Synchronize data with form inputs.

````html
{{-- Text Input --}}
<div x-data="{ message: '' }">
    <input x-model="message">
    <span x-text="message"></span>
</div>

{{-- Checkbox (Boolean) --}}
<input type="checkbox" x-model="agreed">

{{-- Checkbox (Array) --}}
<input type="checkbox" value="red" x-model="colors">
<input type="checkbox" value="blue" x-model="colors">

{{-- Radio --}}
<input type="radio" value="yes" x-model="answer">
<input type="radio" value="no" x-model="answer">

{{-- Select --}}
<select x-model="selectedCountry">
    <option>Malaysia</option>
    <option>Singapore</option>
</select>

{{-- Modifiers --}}
<input x-model.lazy="msg">      <input x-model.number="age">    <input x-model.debounce="q">    ```

### x-text and x-html — Content Binding

```html
{{-- x-text: Safe (escaped) --}}
<span x-text="username"></span>

{{-- x-html: Raw HTML (Be careful of XSS) --}}
<div x-html="articleContent"></div>
````

### x-bind — Attribute Binding

Dynamically bind HTML attributes. Shorthand: `:`.

```html
<img :src="imageUrl" :alt="imageAlt">
<button :disabled="isLoading">Submit</button>
<div :class="{ 'hidden': !open, 'active': isActive }"></div>
<div :style="{ color: 'red', display: show ? 'block' : 'none' }"></div>
```

### x-ref — Element References

Get direct access to DOM elements via `$refs`.

```html
<div x-data>
    <input x-ref="searchInput">
    <button @click="$refs.searchInput.focus()">Focus Input</button>
</div>
```

### x-cloak — Hide Until Loaded

Prevent "flash of unstyled content" (FOUC).

```css
/* Add to global CSS */
[x-cloak] { display: none !important; }
```

```html
<div x-data x-cloak>
    This content remains hidden until Alpine initializes.
</div>
```

### x-effect — Reactive Side Effects

Run code whenever reactive dependencies change.

```html
<div x-data="{ count: 0 }" x-effect="console.log('Count is ' + count)">
    <button @click="count++">Increment</button>
</div>
```

### x-teleport — Portal Content

Render content in a different DOM location (e.g., modals).

```html
<div x-data="{ open: false }">
    <button @click="open = true">Open Modal</button>

    <template x-teleport="body">
        <div x-show="open">
            Modal Content attached to Body
        </div>
    </template>
</div>
```

### x-id — Scoped Unique IDs

Generate unique IDs for accessibility (ARIA).

```html
<div x-data x-id="['text-input']">
    <label :for="$id('text-input')">Username</label>
    <input :id="$id('text-input')" type="text">
</div>
```

-----

## Magic Properties

| Property | Description |
| :--- | :--- |
| **$el** | The current DOM element. |
| **$refs** | Access elements marked with `x-ref`. |
| **$store** | Access global stores defined via `Alpine.store`. |
| **$watch** | Watch a property for changes: `$watch('open', value => console.log(value))`. |
| \*\*$dispatch** | Dispatch browser events: `$dispatch('custom-event', { data: 123 })\`. |
| **$nextTick** | Execute code after Alpine updates the DOM. |
| **$root** | The root element of the component. |
| **$data** | The current data object proxy. |
| **$id** | Generate unique IDs (see x-id). |
| **$wire** | Access the underlying Livewire component (Livewire context only). |

-----

## Official Plugins

### Persist (Local Storage)

Persist state across page loads.

```html
<div x-data="{ count: $persist(0) }">...</div>
<div x-data="{ theme: $persist('light').as('user-theme') }">...</div>
```

### Intersect (Viewport Detection)

Detect when elements enter/leave the viewport.

```html
<div x-intersect="shown = true">Load when visible</div>
<div x-intersect:enter="animateIn" x-intersect:leave="animateOut"></div>
```

### Collapse (Height Animation)

Smooth height animations for accordions/toggles.

```html
<div x-show="open" x-collapse>
    <div class="p-4">Smoothly expands/collapses</div>
</div>
```

### Focus (Focus Management)

Trap focus (great for modals).

```html
<div x-show="modalOpen" x-trap="modalOpen">
    </div>
```

### Mask (Input Masking)

Format inputs automatically.

```html
<input x-mask="99/99/9999" placeholder="DD/MM/YYYY">
<input x-mask="RM 99.99">
```

### Morph (DOM Diffing)

Update DOM elements smoothly without full replacement.

```javascript
Alpine.morph(el, newHtml)
```

### Anchor (Floating UI)

Position floating elements (tooltips, dropdowns) relative to anchors.

```html
<div x-data="{ open: false }">
    <button x-ref="trigger" @click="open = !open">Toggle</button>
    <div x-anchor.bottom="$refs.trigger" x-show="open">
        Floating Content
    </div>
</div>
```

### Sort (Drag and Drop)

Native drag and drop sorting.

```html
<ul x-sort>
    <li x-sort:item="1">Item 1</li>
    <li x-sort:item="2">Item 2</li>
</ul>
```

-----

## Alpine.js with Livewire 3 Integration

### Entangle — Two-Way Sync

Share state between Alpine and PHP (Livewire).

```blade
<div x-data="{ count: @entangle('count') }">
    <button @click="count++">Increment</button>
</div>

{{-- Defer updates --}}
<div x-data="{ count: @entangle('count').live }"></div>
```

### Accessing Livewire Methods via $wire

```html
<button @click="$wire.save()">Save to Database</button>
<button @click="$wire.set('name', 'John')">Set Name</button>
<span x-text="$wire.get('status')"></span>
```

### Wire Modeling

```html
<input x-model="$wire.name">
```

-----

## Compliance Checklist

When implementing Alpine.js components in ICTServe projects, verify:

* [ ] Use `x-data` to define component state.
* [ ] Use `@` shorthand for event listeners.
* [ ] Use `:` shorthand for attribute binding.
* [ ] Include `x-cloak` to prevent flash of unstyled content.
* [ ] Use `x-show` for frequent toggles, `x-if` for conditional DOM insertion.
* [ ] Add `.debounce` modifier to search and filter inputs.
* [ ] Use `@click.outside` to close dropdowns and modals.
* [ ] Include appropriate ARIA attributes for accessibility.
* [ ] Use `x-trap` (Focus plugin) for focus management in modals.
* [ ] Test keyboard navigation (Tab, Enter, Escape, Arrow keys).
* [ ] Extract reusable logic with `Alpine.data()` or `Alpine.store()`.
* [ ] Ensure components work without JavaScript (Progressive Enhancement) where possible.

| Field | Value |
| :--- | :--- |
| **Status** | Active for ICTServe Alpine.js 3 development |
| **Version** | 1.2.0 |
| **Last Updated** | 2025-11-30 |
| **Alpine.js Version** | 3.14.7 |
| **Compatibility** | Livewire 3.x, Laravel 12.x |
