---
name: tailwindcss-style
description: "Ship beautiful sites fast with Tailwind CSS — responsive/state variants, safe dynamic class patterns, component extraction, and conventions for maintainable utility-first styling."
metadata:
  openclaw:
    emoji: "🎐"
    source: "https://github.com/MengTo/Skills"
---

# Tailwind CSS — Utility-First Styling Skill

## When to use
- Rapid prototyping and production styling
- Utility-first approach without writing custom CSS
- Consistent design systems with design tokens
- Responsive, state-driven UI with minimal CSS files

## Key concepts
- **Utility classes**: `text-lg`, `bg-blue-500`, `p-4`, `rounded-xl`
- **Responsive prefixes**: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`
- **State variants**: `hover:`, `focus:`, `active:`, `disabled:`, `group-hover:`
- **Dark mode**: `dark:bg-gray-900`, `dark:text-white`
- **Arbitrary values**: `w-[320px]`, `text-[#bada55]`, `grid-cols-[1fr_2fr]`

## Best practices
1. **Don't fight Tailwind**: Use utilities, not `@apply` everywhere
2. **Extract components, not classes**: Create React/Vue components, not `@apply` blocks
3. **Safe dynamic classes**: Never concatenate class names dynamically — use full class strings
4. **Consistent spacing**: Use the default scale (4, 8, 12, 16...) for rhythm
5. **Responsive mobile-first**: Start with base, add `md:` and `lg:` overrides

## Common patterns
```html
<!-- Responsive card -->
<div class="rounded-xl bg-white p-6 shadow-lg dark:bg-gray-800
            sm:flex sm:items-center sm:gap-6">
  <img class="h-24 w-24 rounded-full object-cover" src="..." alt="..." />
  <div class="mt-4 sm:mt-0">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Title</h3>
    <p class="text-sm text-gray-500 dark:text-gray-400">Description</p>
  </div>
</div>
```

## Pitfalls
- Dynamically building class names (`bg-${color}-500`) → purged by build tool
- Overusing `@apply` → defeats purpose of utility-first
- Not configuring `content` paths → classes not generated

## Tips for AI Agents
- Always use full class strings, never string interpolation for colors.
- Ask about Tailwind version (v3 vs v4) — configuration differs significantly.
- Default to mobile-first responsive design.
