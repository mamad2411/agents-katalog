---
name: style-responsive-tailwind
description: Builds mobile-first responsive layouts with Tailwind CSS v4 using a consistent design-token scale, breakpoints, dark mode, and Flexbox/Grid; used when styling or fixing responsive UI.
when_to_use: When the user asks to style a UI, make a layout responsive, fix mobile/breakpoint issues, set up Tailwind v4 + shadcn, implement dark mode, or enforce a spacing/color token scale.
---

## When to Use

- Styling a new UI or restyling an existing one (visual/styling layer only).
- Making a layout responsive or fixing mobile/breakpoint breakage (horizontal scroll, overflow, squished grid).
- Setting up Tailwind v4 (`@theme`, CSS-first config) + shadcn/ui, or implementing dark mode.
- Enforcing a spacing/color/radius token scale and killing arbitrary-value sprawl.

Not for component structure/state/props/data flow — that's `build-react-component`. This skill assumes the markup exists and applies the visual layer on top.

## Steps

1. **Confirm the Tailwind version before writing any class.** Open `package.json` (or run `grep -r "tailwindcss" package.json`). v4 = `tailwindcss@^4`, a single `@import "tailwindcss";` line in CSS, and NO `tailwind.config.js`. If you see a `tailwind.config.{js,ts}` with `theme.extend`, it's v3 — STOP and ask before migrating; v3/v4 config is not interchangeable.

2. **Define tokens once in CSS via `@theme`** (v4 is CSS-first, not JS-config). Put them in the global stylesheet, not scattered per-component:
   ```css
   @import "tailwindcss";
   @theme {
     --color-bg: oklch(0.18 0.02 265);
     --color-surface: oklch(0.22 0.02 265);
     --color-accent: oklch(0.62 0.18 265);
     --radius-card: 0.75rem;
     --font-sans: "Inter", system-ui, sans-serif;
   }
   ```
   Every key under `@theme` auto-generates utilities (`bg-bg`, `text-accent`, `rounded-card`, `font-sans`). Use `oklch()` for color — perceptually uniform, predictable dark-mode shifts. Keep Tailwind's built-in spacing scale (`p-4`, `gap-6`); only add tokens for things the default scale lacks.

3. **Style mobile-first: unprefixed = mobile base, prefixes = larger screens.** Write the small-screen layout with no prefix, then layer `sm: md: lg: xl: 2xl:` for overrides. Breakpoints are min-width — `md:flex-row` means "≥768px", NOT "≤". Default breakpoints: `sm 640 / md 768 / lg 1024 / xl 1280 / 2xl 1536`.
   ```html
   <div class="flex flex-col gap-4 md:flex-row md:gap-6">
   ```

4. **Pick Flexbox vs Grid deliberately.** Flexbox = 1D content that flows/wraps (nav bars, button rows, chip lists) — use `flex-wrap` + `gap`. Grid = 2D structured layout (card galleries, dashboards) — prefer `grid grid-cols-[repeat(auto-fit,minmax(16rem,1fr))]` so it reflows WITHOUT breakpoint classes. Reach for explicit `md:grid-cols-3` only when you need fixed column counts per breakpoint.

5. **Never use fixed pixel widths for layout.** No `w-[640px]` on containers. Use fluid `w-full` + a `max-w-*` cap + horizontal auto margins: `w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8`. Fixed sizes belong only on intrinsically-sized things (icons, avatars).

6. **Dark mode = class strategy, controllable.** In v4 add a custom variant so a root class toggles it (don't rely on `prefers-color-scheme` alone — users want a manual switch):
   ```css
   @custom-variant dark (&:where(.dark, .dark *));
   ```
   Then `bg-white dark:bg-bg text-gray-900 dark:text-gray-100`. Toggle by adding/removing `.dark` on `<html>`. Define BOTH light and dark for every color-bearing element in the same edit — half-themed UI is the #1 dark-mode bug.

7. **shadcn/ui integration:** shadcn ships its semantic tokens (`--background`, `--foreground`, `--primary`, `--border`, `--ring`) as CSS vars wired into `@theme inline`. Theme the app by editing those vars under `:root` and `.dark` — do NOT hardcode colors on shadcn components. Run `npx shadcn@latest init` and let it write the vars; then customize values, not the component classes.

8. **Extract repeated utility clusters into components, not `@apply`.** If the same 6+ class string appears ≥3 times (e.g. a card shell), make a component (or a shadcn variant via `cva`). Reserve `@apply` for true global primitives only. Magic numbers and copy-pasted class walls are the thing this skill exists to prevent.

9. **Container queries for component-level responsiveness.** When a component must adapt to ITS container width (sidebar vs main), not the viewport, use `@container` on the parent and `@sm: @md:` on children. This is correct for reusable cards that live in differently-sized slots — viewport breakpoints can't see container width.

## Common Errors

- **Writing v3 config in a v4 project.** `tailwind.config.js` with `theme.extend.colors` is silently ignored in v4 — tokens never generate, utilities resolve to nothing. Define tokens in `@theme` in CSS instead.
- **Dynamic class names get purged.** `` `text-${color}-500` `` is invisible to Tailwind's scanner and produces no CSS. Use full static strings and switch via a lookup map, or use `style={{}}` / CSS vars for truly dynamic values.
- **`@apply` on a v4 utility from another file fails** unless that file sees the theme — prefer components over `@apply`; if you must, ensure `@reference "../app.css";` at the top of the CSS module.
- **Backwards breakpoint logic.** `md:hidden` hides on ≥768px (desktop), shows on mobile. To hide on mobile and show on desktop use `hidden md:block`. Min-width semantics trip everyone.
- **Mobile horizontal scroll** = a child wider than viewport: a fixed `w-[Npx]`, an un-wrapped `flex` row, a `grid-cols-N` with no `min-w-0` on children, or a long unbroken string. Hunt with `* { outline: 1px solid red }` and add `min-w-0` / `break-words` / `flex-wrap`.
- **Dark mode flash (FOUC):** reading theme in a `useEffect` paints light first. Set `.dark` on `<html>` via an inline blocking script before hydration.
- **Color-scheme-only dark mode** ignores the manual toggle. Pair the `@custom-variant` class strategy with `color-scheme: dark` so native form controls/scrollbars also darken.

## Verify

1. **Build/typecheck passes** — `npm run build` (or `dev`) with no Tailwind warnings about unknown utilities. Unknown-utility warnings = a token that didn't generate; fix root cause, don't ignore.
2. **Responsive sweep** — view at 360px, 768px, 1280px. No horizontal scrollbar at any width (`document.documentElement.scrollWidth` must equal `clientWidth`). Use chrome-devtools `resize_page` + `take_screenshot` to capture each, or DevTools device mode.
3. **Dark mode parity** — toggle `.dark` on `<html>` and confirm every surface, text, and border has a defined dark value (no black-on-black, no leftover light borders). Screenshot both modes side by side.
4. **Token audit** — `grep -rE '\[[0-9]+px\]|#[0-9a-fA-F]{3,6}' src/` should return near-zero hits in styling. Arbitrary px/hex outside `@theme` means an unscaled magic number — replace with a token.
5. **No FOUC** — hard-reload in dark mode; the page must NOT flash light before settling.
