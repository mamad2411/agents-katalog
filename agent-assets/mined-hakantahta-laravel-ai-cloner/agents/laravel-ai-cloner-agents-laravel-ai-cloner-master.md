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

@docs/research/INSPECTION_GUIDE.md
