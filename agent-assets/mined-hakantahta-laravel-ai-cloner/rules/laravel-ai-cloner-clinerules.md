<!-- AUTO-GENERATED from AGENTS.md — do not edit directly.
     Run `bash scripts/sync-agent-rules.sh` to regenerate. -->

<!-- BEGIN:laravel-agent-rules -->
# This is a Laravel Blade project — NOT React, NOT Next.js

Your training data is saturated with React/Next.js examples. Ignore those instincts here. This template rebuilds websites as **server-rendered Laravel Blade** with **Tailwind CSS v4** and **Alpine.js** for client-side interactivity. There is no React, no JSX, no virtual DOM, no build-time component tree — just Blade templates compiled by PHP and progressively enhanced with Alpine.

Before writing a single line, internalize the "Non-Negotiable Rules" below. When unsure about a Blade directive, a Tailwind v4 token, or an Alpine plugin, read the actual project files (`resources/views`, `resources/css/app.css`, `resources/js/app.js`, `routes/web.php`) instead of guessing.
<!-- END:laravel-agent-rules -->

# Website Reverse-Engineer Template — Laravel Blade Edition

## What This Is
A reusable template for reverse-engineering any website into a clean, modern **Laravel Blade** codebase using AI coding agents. The Laravel + Blade + Tailwind CSS v4 + Alpine.js base is pre-scaffolded — just run `/clone-website <url1> [<url2> ...]`.

## Non-Negotiable Rules
These override anything your training data suggests. Every file you generate MUST obey them:

- **FORBIDDEN — never write or import these:** React, Next.js, Vue, Svelte, JSX/TSX, `useState`, `useEffect`, any React hook, `className`, `.tsx`/`.jsx` files, and JS UI frameworks (shadcn/ui, Radix, MUI, Headless UI). If your instinct produces a `.tsx` file or a `className`, you are doing it wrong.
- **MANDATORY output format:** every template is clean Laravel **Blade** (`.blade.php`). HTML attributes use `class="..."` — **never `className`**.
- **Interactivity & state — Alpine.js ONLY:** every client-side behavior (menu toggles, dropdowns, modals, tabs, accordions, carousels, scroll/reveal effects, form UI state) is built with Alpine.js directives — `x-data`, `x-show`, `x-if`, `x-for`, `x-transition`, `x-collapse`, `x-cloak`, `x-init`, `x-model`, `x-intersect`, `@click`/`x-on:`, `:class`/`x-bind:`, `:style`. No React, no jQuery, no hand-rolled vanilla-JS state machine when Alpine can express it.
- **Output locations:**
  - Reusable UI, layouts, sections, icons → `resources/views/components/` (anonymous Blade components, invoked as `<x-...>`)
  - Full pages → `resources/views/pages/` (each wraps itself in a layout component)
- **Complete, paste-ready code — NEVER snippets:** whether the output is Blade, CSS, or JS, emit the ENTIRE file, valid and working the moment it is saved into the project. No `// ... rest unchanged`, no `{{-- other sections here --}}`, no ellipsis placeholders, no "add this to your file" fragments. A file you produce must run as-is.

## Tech Stack
- **Framework:** Laravel 12 (PHP 8.2+), Blade templating engine
- **Styling:** Tailwind CSS v4 — CSS-first config via `@theme` in `resources/css/app.css` (design tokens as `--color-*` / `--font-*`; **no `tailwind.config.js`, no `postcss.config.js`**)
- **Interactivity:** Alpine.js 3, plus `@alpinejs/collapse` (accordions) and `@alpinejs/intersect` (scroll reveals) — bootstrapped in `resources/js/app.js`
- **Build:** Vite via `laravel-vite-plugin` + `@tailwindcss/vite`
- **Icons:** inline SVGs extracted from the target, saved as anonymous Blade components in `resources/views/components/icons/`
- **Fonts:** self-hosted via `@font-face` in `app.css`, or a privacy CDN (bunny.net) — never `next/font`
- **Formatting:** Laravel Pint for PHP (`pint.json`)

## Commands
- `php artisan serve` — Start the PHP dev server (http://127.0.0.1:8000)
- `npm run dev` — Start Vite with HMR (watches CSS, JS, and Blade)
- `npm run build` — Production asset build
- `php artisan view:cache` — Compile every Blade template; use this to surface Blade syntax errors
- `php artisan view:clear` — Clear compiled Blade cache
- `./vendor/bin/pint` — Format PHP files
- `composer install && npm install` — Install PHP + JS dependencies

## Code Style — match this exactly
- **Blade only.** `{{ $var }}` for auto-escaped output; `{!! $html !!}` reserved for trusted pre-rendered HTML (e.g. inline SVG strings), never for raw user text.
- **`class=""`, never `className`.** All HTML attributes are **double-quoted**. When an Alpine expression contains its own strings, use single quotes inside the double-quoted attribute: `:class="scrolled ? 'bg-black' : 'bg-white'"`.
- **Anonymous components** are the default: declare inputs with `@props([...])` (defaults for optional props), render children via `{{ $slot }}`, and merge caller-supplied classes with `$attributes->merge([...])` / `$attributes->class([...])` / `@class([...])`. **No `tailwind-merge`** — use Laravel's native attribute helpers. Avoid class-based `app/View/Components` unless a component genuinely needs PHP logic.
- **Component naming:** kebab-case files (`stat-card.blade.php`), nested folders map to dotted tags (`components/layouts/app.blade.php` → `<x-layouts.app>`, `components/icons/arrow-right.blade.php` → `<x-icons.arrow-right>`).
- **Alpine idioms:** small inline `x-data="{ open: false }"` objects for local state; a named factory function (defined in an inline `<script>` in the layout, or in `resources/js/`) for complex/reused behavior referenced as `x-data="heroSection()"`. Write `x-transition` in the **long explicit form** with Tailwind classes:
  ```blade
  x-transition:enter="transition ease-out duration-200"
  x-transition:enter-start="opacity-0 -translate-y-2"
  x-transition:enter-end="opacity-100 translate-y-0"
  x-transition:leave="transition ease-in duration-150"
  x-transition:leave-start="opacity-100 translate-y-0"
  x-transition:leave-end="opacity-0 -translate-y-2"
  ```
  Always pair `x-show` with `x-cloak`. Use `x-collapse` for accordions. It is idiomatic to embed Blade (`{{ }}`, `@foreach` loop indices) inside Alpine `:class`/`x-show` expressions.
- **Tailwind:** utility classes in the markup, mobile-first responsive prefixes (`sm: md: lg:`), arbitrary values when the design needs them (`bg-[#0f172a]`, `w-[140%]`, `shadow-[0_20px_60px_rgba(0,0,0,0.15)]`, `blur-[140px]`). Custom design tokens, keyframes, and component utility classes live in `resources/css/app.css` (`@theme`, `@keyframes`, `@layer`). No inline `style=""` except dynamic Alpine `:style` bindings.
- **4-space indentation** for all Blade/PHP/CSS/JS.
- **Assets:** reference images with `{{ asset('images/...') }}` (files in `public/`); never Next.js `<Image>` or imports.
- **Localization-ready:** if the target/reference implies i18n, wrap copy in `{{ __('key') }}` backed by `lang/{tr,en}.json`; otherwise inline the real extracted text verbatim.

## Design Principles
- **Pixel-perfect emulation** — match the target's spacing, colors, typography exactly
- **No personal aesthetic changes during emulation phase** — match 1:1 first, customize later
- **Real content** — use actual text and assets from the target site, not placeholders
- **Beauty-first** — every pixel matters

## Project Structure
```
resources/
  views/
    components/         # Anonymous Blade components (invoked as <x-...>)
      layouts/          # Page shells (<x-layouts.app>) — full <!DOCTYPE html> docs with {{ $slot }}
      sections/         # Page sections: hero, features, footer, ... (<x-sections.hero>)
      ui/               # Small primitives: button, card, badge, ... (<x-ui.button>)
      icons/            # Extracted SVGs as components (<x-icons.arrow-right>)
    pages/              # Full page templates; each wraps itself in <x-layouts.app>
  css/
    app.css             # Tailwind v4 entry: @import 'tailwindcss' + @theme tokens + custom CSS
  js/
    app.js              # Alpine bootstrap: import Alpine + plugins, Alpine.start()
  fonts/                # Self-hosted font files (declared via @font-face in app.css)
routes/
  web.php               # Route::view('/uri', 'pages.name')->name(...) OR controller → view('pages.name')
public/
  images/               # Downloaded images from the target site
  videos/               # Downloaded videos from the target site
  <favicons, site.webmanifest, og images>
lang/                   # tr.json / en.json (+ per-locale PHP files) when the site is localized
docs/
  research/             # Inspection output (design tokens, components, layout, behaviors)
  design-references/    # Screenshots and visual references
scripts/                # Node asset-download scripts (run with the Vite toolchain's node)
```

Routing pattern: a page view lives at `resources/views/pages/home.blade.php` and is served by `Route::view('/', 'pages.home')->name('home');` in `routes/web.php`. The page opens with `<x-layouts.app title="..." :meta-description="...">`, drops in `<x-sections.*>` components, and closes with `</x-layouts.app>`.

## MOST IMPORTANT NOTES
- When launching Claude Code agent teams, ALWAYS have each teammate work in their own worktree branch and merge everyone's work at the end, resolving any merge conflicts smartly since you are basically serving the orchestrator role and have full context to our goals, work given, work achieved, and desired outcomes.
- After editing `AGENTS.md`, run `bash scripts/sync-agent-rules.sh` to regenerate platform-specific instruction files.
- After editing `.claude/skills/clone-website/SKILL.md`, run `node scripts/sync-skills.mjs` to regenerate the skill for all platforms.

# Website Inspection Guide

## How to Reverse-Engineer Any Website

This guide outlines what to capture when inspecting a target website via Chrome MCP or browser DevTools.

## Phase 1: Visual Audit

### Screenshots to Capture
- [ ] Every distinct page — desktop, tablet, mobile
- [ ] Dark mode variants (if applicable)
- [ ] Light mode variants (if applicable)
- [ ] Key interaction states (hover, active, open menus, modals)
- [ ] Loading/skeleton states
- [ ] Empty states
- [ ] Error states

### Design Tokens to Extract
- [ ] **Colors** — background, text (primary/secondary/muted), accent, border, hover, error, success, warning
- [ ] **Typography** — font family, sizes (h1-h6, body, caption, label), weights, line heights, letter spacing
- [ ] **Spacing** — padding/margin patterns (look for a scale: 4px, 8px, 12px, 16px, 24px, 32px, etc.)
- [ ] **Border radius** — buttons, cards, avatars, inputs
- [ ] **Shadows/elevation** — card shadows, dropdown shadows, modal overlay
- [ ] **Breakpoints** — when does the layout shift? (inspect with DevTools responsive mode)
- [ ] **Icons** — which icon library? custom SVGs? sizes?
- [ ] **Avatars** — sizes, shapes, fallback behavior
- [ ] **Buttons** — all variants (primary, secondary, ghost, icon-only, danger)
- [ ] **Inputs** — text fields, textareas, selects, checkboxes, toggles

## Phase 2: Component Inventory

For each distinct UI component, document:
1. **Name** — what would you call this component?
2. **Structure** — what HTML elements / child components does it contain?
3. **Variants** — does it have different sizes, colors, or states?
4. **States** — default, hover, active, disabled, loading, error, empty
5. **Responsive behavior** — how does it change at different breakpoints?
6. **Interactions** — click, hover, focus, keyboard navigation
7. **Animations** — transitions, entrance/exit animations, micro-interactions

### Common Components to Look For
- Navigation (top bar, sidebar, bottom bar)
- Cards / list items
- Buttons and links
- Forms and inputs
- Modals and dialogs
- Dropdowns and menus
- Tabs and segmented controls
- Avatars and user badges
- Loading skeletons
- Toast notifications
- Tooltips and popovers

## Phase 3: Layout Architecture

- [ ] **Grid system** — CSS Grid? Flexbox? Fixed widths?
- [ ] **Column layout** — how many columns at each breakpoint?
- [ ] **Max-width** — main content area max-width
- [ ] **Sticky elements** — header, sidebar, floating buttons
- [ ] **Z-index layers** — navigation, modals, tooltips, overlays
- [ ] **Scroll behavior** — infinite scroll, pagination, virtual scrolling

## Phase 4: Technical Stack Analysis

You inspect the target's stack only to **understand its behavior** — not to copy it. Whatever the source is built with, our rebuild is **always Laravel Blade + Tailwind CSS v4 + Alpine.js** (see mapping below).

- [ ] **Framework** — React? Vue? Angular? Check `__NEXT_DATA__`, `__NUXT__`, `ng-version` (informational — we do NOT reproduce the framework)
- [ ] **CSS approach** — Tailwind (utility classes), CSS Modules, Styled Components, Emotion, vanilla CSS
- [ ] **State management** — Redux, React Query, Zustand, Pinia (informational — client state becomes Alpine `x-data`)
- [ ] **API patterns** — REST, GraphQL (check network tab for `/graphql` requests)
- [ ] **Font loading** — Google Fonts, self-hosted, system fonts
- [ ] **Image strategy** — CDN, lazy loading, srcset, WebP/AVIF
- [ ] **Animation library** — Framer Motion, GSAP, CSS transitions only

### Our Rebuild Target (always the same, regardless of source)

| What the target uses | What we build it as |
| --- | --- |
| React / Next.js / Vue / Angular components | Anonymous Blade components (`resources/views/components/`, `<x-...>`) |
| JSX / TSX | Blade (`.blade.php`), `class=""` (never `className`) |
| `useState` / `useEffect` / Redux / Zustand / reactive stores | Alpine.js `x-data` / `x-init` / `x-model` |
| Client interactivity (dropdowns, modals, tabs, accordions, carousels) | Alpine.js (`x-show`, `x-if`, `x-transition`, `x-collapse`, `@click`, `:class`) |
| Framer Motion / GSAP / JS scroll animations | Alpine (`x-intersect`, scroll listeners) + Tailwind transitions + CSS `@keyframes` in `app.css` |
| CSS-in-JS / CSS Modules / utility CSS | Tailwind CSS v4 utilities + `@theme` tokens in `resources/css/app.css` |
| `next/font`, styled fonts | `@font-face` in `app.css` (self-hosted) or a CDN `<link>`, exposed as `--font-*` tokens |
| `next/image`, `<img>`, CDN images | Downloaded to `public/`, referenced with `{{ asset('images/...') }}` |
| Page routes / file-based routing | `resources/views/pages/*.blade.php` + `Route::view()` in `routes/web.php` |

## Phase 5: Documentation Output

After inspection, create these files in `docs/research/`:
1. `DESIGN_TOKENS.md` — All extracted colors, typography, spacing
2. `COMPONENT_INVENTORY.md` — Every component with structure notes
3. `LAYOUT_ARCHITECTURE.md` — Page layouts, grid system, responsive behavior
4. `INTERACTION_PATTERNS.md` — Animations, transitions, hover states, and the Alpine.js mechanism each will use
5. `TECH_STACK_ANALYSIS.md` — What the site uses and its Laravel Blade / Tailwind v4 / Alpine.js equivalent (per the Phase 4 mapping)
