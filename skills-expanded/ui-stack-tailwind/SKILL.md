---
name: ui-stack-tailwind
description: "Building with Tailwind CSS v4 (and v3) without the Tailwind-default look: setup per framework (Vite, Next.js, Astro, Laravel, monorepos), @theme tokens in OKLCH named by role, dark mode with @custom-variant, the layout system as tokens (one container, section spacing, a type scale, stretched rows) and how to fix each preview layout line with classes, state, aria, data, group, peer, has, motion and container-query variants, component recipes (button, field, card, navigation, table, dialog) with every state, motion with --animate-* and starting:, cn with tailwind-merge, cva, class order, @utility, arbitrary values, typography, v3 to v4 migration, and the generated look. Read when the project uses Tailwind."
---

# Tailwind CSS

Tailwind makes the default look very cheap: `bg-gradient-to-r
from-purple-500 to-pink-500`, `rounded-2xl shadow-2xl`, `backdrop-blur` on
every card, slate greys with an indigo accent. Use it to apply the product's
decisions, not the framework's: tokens in the theme, utilities named by
role, a state on every control, components instead of copied class strings.
Version 4 (4.3 in 2026) is current; v3 notes are in section 11.

## 1. Which version, and the setup

- v4: the CSS starts with `@import "tailwindcss";` and the build uses
  `@tailwindcss/vite`, `@tailwindcss/postcss` or `@tailwindcss/cli`. There
  is no `content` list: sources are found automatically (ignoring what
  `.gitignore` ignores), and `@source "../packages/ui"` adds a path.
- v3: a `tailwind.config.js` with `content`, and `@tailwind base;
  @tailwind components; @tailwind utilities;` in the CSS.
- v4 needs Safari 16.4+, Chrome 111+ and Firefox 128+; a product that must
  run on older browsers stays on v3.4.

| Stack | Install | Wire it |
|---|---|---|
| Vite (React, Vue, Svelte, plain) | `npm i tailwindcss @tailwindcss/vite` | `plugins: [tailwindcss()]` in `vite.config.ts`, `@import "tailwindcss";` in the main CSS |
| Next.js | `npm i tailwindcss @tailwindcss/postcss postcss` | `postcss.config.mjs`: `export default { plugins: { "@tailwindcss/postcss": {} } }`; the import in `app/globals.css` |
| Astro | `npx astro add tailwind` (the Vite plugin) | the import in `src/styles/global.css`, imported by the layout |
| Laravel | `npm i tailwindcss @tailwindcss/vite` | the Vite plugin beside `laravel-vite-plugin`; `@source "../../resources/views";` when Blade files are not found |
| No build | `npx @tailwindcss/cli -i src/in.css -o dist/out.css --watch` | the built file linked in HTML; never the CDN script in production |

- Sources: `@import "tailwindcss" source("../src");` sets where classes are
  found; `@source "../packages/ui/src";` adds a package in a monorepo;
  `@source not "../legacy";` leaves a folder out. A class built from strings
  (`` `bg-${tone}` ``) is never found: map to full class names
  (`{ ok: "bg-ok", warn: "bg-warn" }[tone]`).

## 2. Theme first: tokens named by role

The palette, fonts, radii and shadows live in the theme, named by role:
`bg-surface`, `text-muted`, `border-line`, `bg-accent`, not `bg-purple-600`
scattered through the app.

```css
@import "tailwindcss";

@theme {
  --color-*: initial;                    /* the product's colours only, no default palette */
  --color-paper: oklch(0.98 0.006 85);    /* values from DESIGN.md */
  --color-surface: oklch(1 0 0);
  --color-surface-2: oklch(0.955 0.008 85);
  --color-ink: oklch(0.21 0.012 85);
  --color-muted: oklch(0.49 0.012 85);
  --color-line: oklch(0.9 0.008 85);
  --color-accent: oklch(0.5 0.14 40);
  --color-on-accent: oklch(0.99 0.004 85);
  --color-danger: oklch(0.52 0.19 27);
  --font-sans: "Public Sans", ui-sans-serif, system-ui, sans-serif;
  --font-display: "Newsreader", ui-serif, Georgia, serif;
  --text-display: clamp(2rem, 1.4rem + 2.6vw, 3.0625rem);
  --text-display--line-height: 1.1;
  --radius-sm: 4px;
  --radius-md: 8px;
  --shadow-overlay: 0 8px 24px oklch(0.2 0.02 85 / 0.14);
  --ease-out-soft: cubic-bezier(0.22, 0.61, 0.36, 1);
}
```

- Each variable makes its utilities: `--color-accent` gives `bg-accent`,
  `text-accent`, `border-accent`; `--text-display` gives `text-display`;
  `--ease-out-soft` gives `ease-out-soft`. They are also CSS variables at
  `:root`, for plain CSS (`var(--color-accent)`) and scripts.
- `--color-*: initial` drops the default palette, so `bg-purple-600` stops
  compiling; leave it out when a library in the project uses those colours.
- Colours in OKLCH: the steps of a role (hover, border, dark) keep the hue
  and move the lightness, so they stay one family.
- The spacing scale is `--spacing: 0.25rem` (a 4px base, what `ui` asks
  for); keep it. Breakpoints are `--breakpoint-*`: add one where the content
  breaks, not per device.
- `@theme inline` when a token's value is another variable (a next/font
  variable, shadcn's `--color-primary: var(--primary)`): the utility then
  reads that variable where it is used, not a value resolved at the root.

## 3. Dark mode and themes

```css
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));

@layer base {
  [data-theme="dark"] {
    color-scheme: dark;
    --color-paper: oklch(0.16 0.006 85);
    --color-surface: oklch(0.2 0.007 85);
    --color-surface-2: oklch(0.24 0.008 85);
    --color-ink: oklch(0.93 0.006 85);
    --color-muted: oklch(0.7 0.01 85);
    --color-line: oklch(0.3 0.008 85);
    --color-accent: oklch(0.72 0.15 45);
    --color-on-accent: oklch(0.18 0.02 45);
  }
}
```

- Dark mode by the class or data-attribute strategy, through the variables:
  utilities read them, so redefining them under the switch changes every
  `bg-paper` and `text-ink` at once, and most elements need no `dark:` class
  at all. `dark:` stays for what is not a colour token (another image, a
  shadow that goes away).
- Without the custom variant, `dark:` follows `prefers-color-scheme` only,
  and a toggle cannot win. The script in `<head>` sets `data-theme` from the
  saved choice or the system before the first paint (`ui-themes`).

## 4. The layout system as tokens

A page built section by section drifts in Tailwind as much as anywhere: one
section `max-w-3xl mx-auto`, the next `max-w-6xl px-8`, gaps of `py-4` here
and `py-32` there, eleven text sizes. The measures in `ui-layout` go into the
theme once, and every section uses the same few classes:

```css
@theme {
  --container-page: 72rem;                     /* max-w-page: the one content width */
  --container-measure: 65ch;                   /* max-w-measure: running text */
  --spacing-gutter: clamp(1rem, 4vw, 2rem);    /* px-gutter */
  --spacing-section: clamp(3rem, 8vw, 6rem);   /* py-section: between sections */
  --text-*: initial;                           /* the product's scale only */
  --text-sm: 0.875rem;  --text-sm--line-height: 1.5;
  --text-base: 1rem;    --text-base--line-height: 1.6;
  --text-lg: 1.25rem;   --text-lg--line-height: 1.5;
  --text-xl: 1.563rem;  --text-xl--line-height: 1.3;
  --text-2xl: 1.953rem; --text-2xl--line-height: 1.2;
  --text-display: clamp(2.441rem, 1.8rem + 3vw, 3.815rem); --text-display--line-height: 1.1;
}

@utility page { width: 100%; max-width: var(--container-page); margin-inline: auto; padding-inline: var(--spacing-gutter); }
```

```html
<section class="py-section">
  <div class="page">
    <h2 class="text-2xl font-display">Selected work</h2>
    <p class="mt-3 max-w-measure text-muted">…</p>
    <ul class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">…</ul>
  </div>
</section>
```

- Every section's content sits in `page`: one left edge, one width. A
  narrower column is `max-w-measure` inside it, left-aligned, never a second
  `mx-auto` box.
- Text sizes come from the scale (`text-sm` to `text-2xl`, and
  `text-display` from section 2); with `--text-*: initial` the other defaults
  stop compiling, so a stray `text-5xl` does nothing and shows at once, and a
  `text-[15px]` is a finding in review. The page title is `text-display`, at
  least twice the body.
- Spacing from the 4px scale: `gap-2`/`gap-3` inside a component, `gap-6`
  between items, `mt-8`/`mt-12` between groups, `py-section` between
  sections. A heading sits closer to what follows (`mt-3`) than to what came
  before.
- Rows of cards share a height: a grid stretches its items by default
  (`grid auto-rows-fr` when every row should match), and each card is
  `flex flex-col` with its action `mt-auto`.
- The first section clears the header: `pt-section`, or the header's height
  when it is sticky (`scroll-mt-16` on anchored sections too).

### The `preview` layout lines, in classes

| Line | Fix |
|---|---|
| sections start at N left edges / content widths differ | Wrap each section's content in `page`; remove its own `max-w-*`, `mx-auto`, `px-*` |
| blocks a few pixels off the edge | A `pl-*`, `ml-*`, border or `-mx-*` on one block: remove it, or move it inside |
| the first content sits 0px from the top | `pt-section` on the first section, or header padding |
| sections run into each other | `py-section` on every section |
| elements overlap | A fixed `w-*`/`h-*` or negative margin at this width: `shrink-0` on the media, `flex-col` below `sm:` |
| still invisible after scrolling | An `opacity-0` start that a class never removed: start visible, animate with `motion-safe:` and `starting:` (section 8) |
| N font sizes / weak h1 | Only the scale; `text-display` for the title, `text-2xl` for section heads |
| body text is 13px | `text-base` (16px) for body copy, `text-sm` only for secondary text |
| paragraph lines run long | `max-w-measure` on running text |
| boxes side by side with different heights | `items-stretch` (the grid default), `flex flex-col` in each box, `mt-auto` on its action |
| N different text colours | `text-ink`, `text-muted`, `text-accent` and state colours only |

## 5. Variants: states, structure, containers

States on every control: `hover:`, `focus-visible:`, `disabled:`, and the
ARIA and data attributes the component already sets:

```html
<button class="inline-flex h-10 items-center gap-2 rounded-md bg-accent px-4 font-medium text-on-accent
  hover:bg-accent/90 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent
  disabled:cursor-not-allowed disabled:opacity-50 aria-busy:cursor-progress">Save changes</button>
<input class="h-10 rounded-md border border-line bg-surface px-3 aria-invalid:border-danger user-invalid:border-danger">
```

- Never `outline-none` without a `focus-visible` style. In v4 the old
  `outline-none` is `outline-hidden` (it keeps an outline in forced-colours
  mode); either needs the visible replacement.
- `aria-expanded:`, `aria-selected:`, `data-[state=open]:` (or `data-open:`
  for a present attribute) style the state the component exposes; no
  second class to keep in sync. v3 writes `aria-[invalid=true]:`.
- Parents and siblings: `group` with `group-hover:` or
  `group-focus-within:`, `peer` with `peer-checked:`, `has-[input:checked]:`
  for a parent that changes with its content, `not-last:` and `*:` for
  children.
- `motion-safe:` on animations and transform transitions;
  `motion-reduce:transition-none` where a library adds its own
  (`motion-stacks`).
- Mobile-first: unprefixed for the phone, `sm:` `md:` `lg:` as it widens,
  `max-md:` for below. Rearrange (`flex-col md:flex-row`, `order-*`), do not
  duplicate markup behind `hidden md:block`.
- Container queries for a component placed at different widths: `@container`
  on the parent, `@md:grid-cols-2` on the child; named ones with
  `@container/card` and `@md/card:`.
- Page container: `mx-auto max-w-6xl px-4 sm:px-6`, text `max-w-prose`;
  inside an app shell, no `mx-auto` (`ui-layout`).

## 6. Recipes, with every state

```html
<!-- Field: the label names it, the hint and the error describe it -->
<div class="grid gap-1.5">
  <label for="email" class="text-sm font-medium text-ink">Email</label>
  <input id="email" type="email" aria-describedby="email-hint email-error" aria-invalid="true"
    class="h-10 rounded-md border border-line bg-surface px-3 text-base text-ink placeholder:text-muted
           focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-accent
           aria-invalid:border-danger disabled:bg-surface-2 disabled:text-muted">
  <p id="email-hint" class="text-sm text-muted">We send the receipt here.</p>
  <p id="email-error" class="text-sm text-danger">Enter an address like name@example.com.</p>
</div>

<!-- Card: the whole card is the link; the title is the name, the action sits at the bottom -->
<article class="group relative flex flex-col rounded-md border border-line bg-surface p-5
                hover:border-ink/30 has-focus-visible:outline-2 has-focus-visible:outline-accent">
  <h3 class="text-lg font-medium"><a href="/work/ledger" class="after:absolute after:inset-0 focus:outline-none">Ledger</a></h3>
  <p class="mt-2 text-muted">…</p>
  <span class="mt-auto pt-4 text-sm text-accent group-hover:underline">Read the case</span>
</article>

<!-- Navigation: the current page is marked for everyone, not by colour alone -->
<a href="/work" aria-current="page"
   class="rounded-sm px-2 py-1 text-muted hover:text-ink aria-[current=page]:font-medium
          aria-[current=page]:text-ink aria-[current=page]:underline underline-offset-4">Work</a>

<!-- Table: scrolls in its own box on a phone; numbers right-aligned in tabular figures -->
<div class="overflow-x-auto rounded-md border border-line">
  <table class="w-full text-sm">
    <thead class="bg-surface-2 text-left text-muted"><tr><th scope="col" class="px-4 py-2 font-medium">Invoice</th>
      <th scope="col" class="px-4 py-2 text-right font-medium">Amount</th></tr></thead>
    <tbody class="divide-y divide-line"><tr class="hover:bg-surface-2">
      <td class="px-4 py-3">INV-0042</td><td class="px-4 py-3 text-right tabular-nums">Rp 1.250.000</td></tr></tbody>
  </table>
</div>

<!-- Dialog: the native element, its backdrop, and an entry that respects reduced motion -->
<dialog class="m-auto w-full max-w-md rounded-md bg-surface p-6 text-ink shadow-overlay backdrop:bg-ink/40
               opacity-100 transition-[opacity,translate] duration-200 starting:open:opacity-0
               starting:open:translate-y-2 motion-reduce:transition-none">…</dialog>
```

- Every control has hover, `focus-visible`, disabled, and the ARIA state it
  exposes; a busy button says so (`aria-busy`, a spinner, its text kept).
- Touch targets reach 44px on a phone: `h-11` or `min-h-11`, or padding on
  an icon button (`p-2.5` around a 24px icon).
- Buttons: one filled primary per view (`bg-accent text-on-accent`), the
  rest outline (`border border-line`) or plain (`hover:bg-surface-2`). Their
  variants live in one `cva` (section 7), not in copied strings.

## 7. Components, cn and class order

- A class group that repeats becomes a component (a React, Vue or Svelte
  component, or a partial), not a copy and not `@apply` everywhere. Keep
  `@apply` for base element styles and markup you do not control (HTML from
  a CMS).
- Variants with `cva` (class-variance-authority) or a small map keyed by
  variant (the Button in `ui-stack-react`); merge a caller's classes with
  `cn()` (clsx and tailwind-merge) so a caller's `px-6` replaces the default
  rather than both applying:

```ts
// lib/cn.ts
import { clsx, type ClassValue } from "clsx";
import { extendTailwindMerge } from "tailwind-merge";

// tailwind-merge knows only the default theme: name custom text sizes, or it
// reads text-display as a colour and drops it beside text-muted.
const twMerge = extendTailwindMerge({ extend: { theme: { text: ["display"] } } });

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

- tailwind-merge 3 is for Tailwind 4 (2 for 3). The `cn` package (from the
  shadcn team, September 2026) replaces clsx and tailwind-merge together:
  `export { cn } from "cn"`, and `createCn` from `cn/config` takes the same
  `extend` for custom tokens.
- `@utility` for a custom utility that takes variants:
  `@utility focus-ring { outline: 2px solid var(--color-accent);
  outline-offset: 2px; }`, then `focus-visible:focus-ring`.
- In a Vue or Svelte `<style>` block, `@reference "../app.css";` first, so
  `@apply` and theme values resolve without emitting Tailwind twice.
- Keep class order readable: layout, box, type, colour, state, responsive.
  The Prettier plugin sorts them, including inside `cn()` and `cva()`:

```json
{
  "plugins": ["prettier-plugin-tailwindcss"],
  "tailwindStylesheet": "./src/app.css",
  "tailwindFunctions": ["cn", "cva", "clsx"]
}
```

## 8. Motion

```css
@theme {
  --animate-rise: rise 480ms var(--ease-out-soft) both;
  @keyframes rise {
    from { opacity: 0; translate: 0 12px; }
  }
}
```

- Animate `opacity` and `translate`/`scale` only: `transition-[opacity,translate]`,
  never `transition-all` (it animates layout and colours you did not mean).
  Durations and easing from tokens (`duration-200 ease-out-soft`).
- Entry without JavaScript: `starting:` (`@starting-style`) for elements that
  appear (a dialog, a popover, an item added to a list); `motion-safe:` on
  every animation, `motion-reduce:` to turn a library's off.
- Content is visible in the markup; an animation only moves it into place.
  A reveal that starts at `opacity-0` needs the class that ends it to be
  certain to arrive, or the content stays hidden (`motion-reveal`).

## 9. Values, prose

- Use the scale. Arbitrary values (`w-[347px]`, `text-[#1f2937]`,
  `mt-[13px]`) are the exception with a reason, not the way to match a
  mock-up; a value needed twice is a token.
- A CSS variable as a value: `w-(--sidebar-width)` in v4 (`w-[--sidebar-width]`
  was v3). `size-10` for equal width and height; `min-h-dvh`, never
  `h-screen` on a section.
- Long text from Markdown or a CMS: `@plugin "@tailwindcss/typography";`
  and `prose` on the wrapper (65ch), styled from the tokens with element
  modifiers (`prose-headings:font-display prose-a:text-accent`) and
  `dark:prose-invert` or token overrides for the dark theme.

## 10. The generated look

Gradient text (`bg-clip-text text-transparent`), purple-to-pink gradients,
`rounded-full` on everything, `shadow-2xl` cards, `backdrop-blur` on
several surfaces, `uppercase tracking-widest` eyebrows over every heading,
slate or zinc greys with an indigo accent, `rounded-2xl shadow-xl` on every
card, `ring-1 ring-white/10` glass panels on a dark gradient, `h-screen`
heroes, `text-gray-400` body text that fails contrast. `ui_check` finds
them.

## 11. From v3 to v4

- `npx @tailwindcss/upgrade` (Node 20+) on a clean branch, then read the
  diff: it moves the config into CSS, rewrites renamed classes and swaps
  the build plugin.
- Renamed: `shadow-sm` to `shadow-xs` and `shadow` to `shadow-sm` (the same
  shift for `rounded`, `blur` and `drop-shadow`), `outline-none` to
  `outline-hidden`, `ring` to `ring-3`, `bg-gradient-to-r` to
  `bg-linear-to-r`, `flex-shrink-0` to `shrink-0`, `bg-opacity-50` to a
  colour with `/50`.
- Changed defaults: `border` and `ring` are `currentColor` (give them a
  colour), `ring` is 1px, placeholders are the text colour at half opacity,
  buttons have `cursor: default`, and `hover:` applies only where the device
  can hover.
- `!` goes at the end (`bg-accent!`), stacked variants read left to right,
  and JS plugins load with `@plugin`; a JS config that must stay loads with
  `@config "./tailwind.config.js"`.
- In v3 itself: `theme.extend` in `tailwind.config`, pointing at CSS
  variables (`colors: { ink: "var(--ink)" }`), so a dark theme swaps the
  variables, not every class.

## Check it

- `preview` at 360, 768 and 1440px: its `layout` lines clear (section 4),
  both themes.
- `ui_check` for the generated look and raw values; `grep -rnE
  "\[#[0-9a-fA-F]|-\[[0-9.]+px\]" src` for arbitrary colours and sizes.
- A misspelt class fails silently (it generates nothing): look at the
  rendered page with the `preview` tool, in both themes.
- Prettier on changed files, so class order stays sorted and diffs small.

## Avoid

The default palette in components (`bg-purple-600`, `text-gray-500`);
arbitrary values where a token exists; `@apply` to rebuild components in
CSS; `outline-none` with no focus style; `dark:` on every element instead of
tokens; `hidden md:block` duplicates of the same markup; `cn` without a
merge that knows the custom tokens; `h-screen` sections; the generated look
above; sections with their own width or padding instead of `page`; text
sizes outside the scale; `transition-all`; content that starts hidden.
