---
name: ui-stack-plain
description: "Building with plain HTML, CSS and a little JavaScript, no framework and no build step: file layout, the document head, cascade layers, tokens as custom properties, modern CSS (grid, clamp, container queries, :has, nesting), a small reset, component classes, light and dark themes with color-scheme and a toggle, progressive enhancement with ES modules, native dialog, details and popover, forms that really submit, images with srcset, SVG icons, fonts, performance budgets, and when to move to Astro or a framework. Read when the project uses plain HTML and CSS, or a page of content needs nothing more."
---

# Plain HTML, CSS and JavaScript

The right stack for a page of content: nothing to build, nothing to break.
It still needs structure, or it becomes one long file of one-off styles. The
naive version adds jQuery for a menu, builds HTML from strings, fakes its
form and goes blank when its script fails. This keeps a static site tidy
with what browsers do natively in 2026.

## 1. Files

- One page: `index.html`, `styles.css`, and `script.js` only when something
  must behave. Assets in `assets/` or `img/`.
- Several pages, or CSS past about 400 lines:

```text
index.html  about.html  contact.html   one file per page
css/tokens.css  css/base.css  css/components.css   each linked from <head>
js/main.js                             entry module; js/menu.js, js/forms.js
img/  fonts/  favicon.svg
```

## 2. The document

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[Page] | [Site name]</title>
  <meta name="description" content="[What this page offers, in one sentence]">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/tokens.css"> <!-- then base.css, components.css -->
  <script type="module" src="js/main.js"></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header>...</header> <main id="main">...</main> <footer>...</footer>
</body>
</html>
```

- A real `<title>` and `<meta name="description">` on every page; a
  canonical link, and Open Graph tags with an absolute image URL on pages
  that get shared (`frontend-seo`).
- Landmarks: `header`, `nav`, `main`, `footer`; one `h1`; headings in order.
- `type="module"` scripts are deferred (no `DOMContentLoaded` wrapper
  needed); a classic script gets `defer`.

## 3. CSS, in layers and in this order

`@layer reset, tokens, base, layout, components, utilities;` as the first
line of the first stylesheet. A later layer wins whatever the selectors, so
a utility beats a component without `!important`; CSS outside any layer
beats them all, so keep none, or only overrides of third-party CSS.

1. **Tokens** in `:root`: colours by role (`--paper`, `--ink`, `--muted`,
   `--line`, `--accent`), the spacing scale (`--s-1` to `--s-9`), radii,
   the type scale with `clamp()` for display sizes, font stacks.
2. **Reset and base**: `*, *::before, *::after { box-sizing: border-box; }`,
   body margin 0, `img, svg { max-width: 100%; height: auto; display:
   block; }`, `font: inherit` on form controls, `[hidden] { display: none
   !important; }` (a component's `display` would otherwise override it),
   body font and colour from the tokens, a visible `:focus-visible`.
3. **Layout**: `.container` (max-width, side padding), the grid, sections.
4. **Components**: one class per part and its pieces (`.card`,
   `.card__title`), modifiers for variants (`.btn--primary`), states from
   attributes (`[aria-expanded="true"]`). Every value from a token; the same
   markup repeated keeps the same classes, so the CSS styles it once.
5. **Utilities**: a few single-purpose classes (`.visually-hidden`), last.

Media queries mobile-first (`@media (min-width: 48em)`), nested in the
component they change, not in one block at the end. Motion only inside
`@media (prefers-reduced-motion: no-preference)` (`motion-stacks`).

## 4. Tokens and themes

```css
@layer tokens {
  :root {
    color-scheme: light dark;
    /* values from DESIGN.md: light first, dark second */
    --paper: light-dark(#f7f4ee, #0e0f11);
    --ink: light-dark(#18170f, #ebeae6);
    --muted: light-dark(#5b584f, #9c9a94);
    --line: light-dark(#dcd6c8, #2a2b30);
    --accent: light-dark(#9a3412, #fb923c);
    --on-accent: light-dark(#ffffff, #18170f);
    --s-1: 0.25rem; --s-2: 0.5rem; --s-3: 0.75rem; --s-4: 1rem; --s-5: 1.5rem;
    --s-6: 2rem; --s-7: 3rem; --s-8: 4rem; --s-9: 6rem; --radius-1: 4px; --radius-2: 8px;
    --step-1: 1.25rem; --step-2: clamp(1.5rem, 1.25rem + 1vw, 1.95rem);
    --step-3: clamp(1.95rem, 1.4rem + 2.4vw, 3.05rem);
    --font-text: "Public Sans", system-ui, sans-serif;
    --font-display: "Newsreader", Georgia, serif;
  }
  :root[data-theme="light"] { color-scheme: light; }
  :root[data-theme="dark"] { color-scheme: dark; }
}
```

- `light-dark()` (Baseline 2024) picks by the element's `color-scheme`: the
  system setting by default, a saved `data-theme` when there is one. Colours
  only; a shadow or an image per theme goes in an override block.
- Without it, a dark theme overrides only the tokens (`[data-theme="dark"]
  { --paper: ...; }`), with `prefers-color-scheme` as the default.
- A saved choice is applied before the first paint by a script at the top
  of `<head>` setting `data-theme` from `localStorage` (`ui-themes`).

## 5. Modern CSS worth using

- Grids that fit without breakpoints: `repeat(auto-fit, minmax(min(100%,
  18rem), 1fr))`; the `min()` keeps one column from overflowing at 360px.
- `clamp()` for fluid type and space; `min-height: 100dvh`, never `100vh`.
- Container queries for a component placed at different widths, `:has()`
  for a parent that changes with its content, nesting one level deep.
- `text-wrap: balance` on headings, `pretty` on paragraphs; `:user-invalid`
  to flag a field once it is left wrong; `scroll-margin-top` for anchors.

```css
@layer components {
  .card { container-type: inline-size; border: 1px solid var(--line); border-radius: var(--radius-2); }
  .card__body {
    display: grid; gap: var(--s-3); padding: var(--s-5);
    @container (min-width: 36rem) { grid-template-columns: 12rem 1fr; }
  }
  .card__title { font: 600 var(--step-1)/1.25 var(--font-display); text-wrap: balance; }
  .card:has(.card__media) .card__body { padding-block-start: var(--s-3); }
}
```

## 6. JavaScript adds behaviour

- The page reads and works without it; script adds behaviour (a menu, a
  copy button, a form that submits without reload).
- ES modules (or an IIFE in a classic script), no bundler, no globals:
  `js/main.js` imports what the page uses. Event delegation on a parent for
  repeated items. `aria-expanded` and `hidden` toggled with the visuals.
- Content rendered by script comes from a `<template>`, filled with
  `textContent`, never HTML built in strings (an injection hole).
- No framework or jQuery for a menu and a form.

```js
// js/menu.js, for <nav data-menu> with <button aria-controls="site-links" aria-expanded="false" hidden>;
// main.js calls it on each [data-menu]. Without script the links show and the button stays hidden.
export function initMenu(nav) {
  const button = nav.querySelector("[aria-controls]");
  const list = document.getElementById(button.getAttribute("aria-controls"));
  const narrow = matchMedia("(width < 48em)");
  const isOpen = () => button.getAttribute("aria-expanded") === "true";
  const sync = () => { button.hidden = !narrow.matches; list.hidden = narrow.matches && !isOpen(); };
  const set = (open) => { button.setAttribute("aria-expanded", String(open)); sync(); };
  button.addEventListener("click", () => set(!isOpen()));
  nav.addEventListener("keydown", (e) => { if (e.key === "Escape" && isOpen()) { set(false); button.focus(); } });
  narrow.addEventListener("change", sync);
  sync();
}
```

## 7. Native elements before scripts

| Need | Element | What it gives, without a library |
|---|---|---|
| A modal (a confirm, a short form) | `<dialog>` opened with `showModal()` | Focus moved in, the page behind inert, `Esc`, `::backdrop` |
| A disclosure, an FAQ | `<details>` and `<summary>`; a shared `name` for one open at a time | Keyboard and state, with no script |
| A floating menu or panel | `popover` and a button with `popovertarget` | Top layer, light dismiss, `Esc`, with no script |

A `<form method="dialog">` inside a dialog closes it; `@starting-style`
animates opening and closing (`motion-interface`).

## 8. Forms that really submit

- A form posts to a real endpoint: the site's own backend, or a form
  service (Formspree, Netlify Forms, Basin) named in the README. Never a
  handler that shows a thank-you and sends nothing.
- A label on every field, the right `type`, `autocomplete`, `inputmode` and
  `required`: the browser validates and fills; messages in words beside the
  field (`ui-part-forms`).
- Script upgrades it to send without reload: the same endpoint, progress on
  the button, the result in a `role="status"` region.

```js
// js/forms.js, for <form action="..." method="post" data-enhance> with a [role=status] inside
export function enhanceForm(form) {
  const status = form.querySelector("[role=status]");
  const button = form.querySelector("[type=submit]");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    button.disabled = true;
    status.textContent = "Sending...";
    const init = { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } };
    try {
      const response = await fetch(form.action, init);
      if (!response.ok) throw new Error(String(response.status));
      form.reset();
      status.textContent = "Sent. [What happens next]";
    } catch {
      status.textContent = "It did not send. Check your connection and try again.";
    }
    button.disabled = false;
  });
}
```

## 9. Images, icons, fonts

- Images: `width` and `height`, `alt` on every one, `loading="lazy"` below
  the fold (the first view's largest image gets `fetchpriority="high"`
  instead), `srcset` and `sizes` for photographs, AVIF with a JPEG fallback:

```html
<picture>
  <source type="image/avif" srcset="img/shop-800.avif 800w, img/shop-1600.avif 1600w" sizes="(min-width: 64em) 50vw, 100vw">
  <img src="img/shop-800.jpg" srcset="img/shop-800.jpg 800w, img/shop-1600.jpg 1600w" sizes="(min-width: 64em) 50vw, 100vw"
       width="1600" height="1067" alt="[What the photo shows]" loading="lazy" decoding="async">
</picture>
```

- Icons: inline SVG `<symbol>`s at the top of `<body>`, used as `<svg
  class="icon" aria-hidden="true"><use href="#i-phone"/></svg>`, fetched
  exactly with the `icon` tool, drawn in `currentColor`. No icon fonts.
- Fonts: a system stack, or one or two families self-hosted as WOFF2 with
  `font-display: swap`, the face above the fold preloaded (`as="font"
  type="font/woff2" crossorigin`); or the provider's CSS with `preconnect`,
  `display=swap` and only the weights used.

## 10. Performance, and when to move on

- Budget for a content page: HTML, CSS and script under about 100 KB
  compressed, script under 30 KB and none of it render-blocking, the first
  view's largest image under about 200 KB, two font families at most.
- The same header pasted into more than about five pages, or a blog with
  lists and tags: Astro (layouts and components, no JavaScript by default)
  or Eleventy, keeping the tokens and CSS. Shared state, sign-in or live
  data: a framework (`ui-stack-react`, `ui-stack-vue`, `ui-stack-svelte`).

## Check it

- Look at it with the `preview` tool, giving the HTML file's `path`, and
  run `ui_check`. `path` opens the file as `file://`, where Chrome refuses
  ES modules and `fetch`: for a page with `type="module"`, use `url`
  `http://localhost:8000/` and `start` `python3 -m http.server 8000`.
- `npx html-validate "*.html"` for broken markup (unclosed elements,
  duplicate ids, a `for` pointing at nothing).
- JavaScript off: the content, the navigation and the form still work.
  Tab from the top: the skip link first, focus visible on every control.

## Avoid

One stylesheet of one-off values; raw colours in components; `!important`
where a layer would do; a `div` with a click handler; jQuery for a menu; a
page blank without its script; HTML built from strings holding data; a form
that thanks the user and sends nothing; images without dimensions; lazy
loading on the first view's main image; icon fonts; a chain of `@import`s;
one header maintained by hand in fifteen files.
