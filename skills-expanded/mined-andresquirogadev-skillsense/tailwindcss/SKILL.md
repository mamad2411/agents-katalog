# Tailwind CSS Skill

You are working with Tailwind CSS. Apply these conventions.

## Core Usage

- Apply styles exclusively through utility classes in JSX/HTML. Avoid writing custom CSS unless absolutely necessary.
- Use Tailwind's responsive prefixes in mobile-first order: base → `sm:` → `md:` → `lg:` → `xl:`.
- Dark mode with `dark:` prefix requires `darkMode: 'class'` in `tailwind.config.ts`.
- Group related utilities logically: layout → spacing → typography → color → effects.

## Configuration (tailwind.config.ts)

- Define the design token system in `theme.extend` — do not overwrite the default theme entirely.
- Use CSS variables in `theme.extend.colors` to support theming: `'primary': 'hsl(var(--primary))'`.
- Add custom animations under `theme.extend.keyframes` and `theme.extend.animation`.
- Use `content` array to configure PurgeCSS correctly: include all files that contain class names.

## Component Patterns

- Extract repeated class strings into a component or use `cva` (class-variance-authority) for variants.
- Use `clsx` or `cn()` (clsx + tailwind-merge) to conditionally apply classes without conflicts.
  ```ts
  import { clsx } from 'clsx';
  import { twMerge } from 'tailwind-merge';
  export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }
  ```
- Never use string interpolation to build class names (`text-${color}-500`) — Tailwind cannot detect these at build time. Use a full class object map instead.

## Typography & Spacing Scale

- Use the spacing scale consistently: 4 = 1rem, 8 = 2rem, etc.
- Use `prose` from `@tailwindcss/typography` for rich-text/markdown content.
- Use `line-clamp-{n}` from `@tailwindcss/line-clamp` (built-in Tailwind v3.3+) to truncate text.

## Tailwind v4 (if used)

- Tailwind v4 uses CSS-first config (`@theme` in CSS) instead of `tailwind.config.ts`.
- Import with `@import "tailwindcss"` in your main CSS file.
- Custom utilities: `@utility`, custom variants: `@variant`.
