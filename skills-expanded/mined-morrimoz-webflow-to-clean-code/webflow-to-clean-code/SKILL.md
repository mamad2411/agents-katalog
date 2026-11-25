---
name: webflow-to-clean-code
description: Converts Webflow-exported HTML/CSS/JS into clean, self-contained static code. Removes Webflow.js, Webflow-hosted assets, and w-* class dependencies; replaces them with project-owned markup, styles, and scripts. Use when importing a Webflow export, stripping w-inline-block and Webflow comments, migrating a Webflow page to any static host or framework, or the user mentions "Webflow export" or "leaving Webflow".
---

# Webflow export → clean code

## When to use

Apply this skill when:

- You have an **exported Webflow project** (zip or folder) and want clean, maintainable HTML/CSS/JS.
- You need to **remove Webflow runtime** (`webflow.js`), Webflow CDN stylesheets, or **`.w-*` class semantics** from a page.
- You are migrating a Webflow page to **any static host** (Vercel, Netlify, GitHub Pages, Firebase, S3, etc.) or framework (Next.js, Astro, plain HTML, etc.).

## One-line success criterion

The output page matches the Webflow version in **intent and visuals**, **does not depend on or mention Webflow**, loads only **your own** CSS/JS, and passes the **verification** checks below.

---

## Workflow (do in order)

### 1) Inventory the Webflow output

- Map **structure you must keep**: forms, element `id`s, `data-*` hooks for tabs/carousels, links, landmarks.
- Map **what you can simplify**: redundant wrappers, Webflow combo classes, unused symbols, duplicate sections.
- Note components that may already exist in your project so you can reuse them instead of re-creating.

### 2) Strip Webflow coupling

Remove every dependency on Webflow's infrastructure and class naming:

- **Delete** `<script src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js">` and `webflow.js` script tags.
- **Delete** `<link rel="stylesheet" href="https://uploads-ssl.webflow.com/...css">` (Webflow CDN stylesheets).
- **Replace** Webflow utility classes you do not own (e.g. `w-inline-block`, `w-clearfix`, `w-container`) with project-owned class names and define equivalent CSS rules yourself.
- **Remove** the `data-wf-page`, `data-wf-site`, and `data-wf-domain` attributes from `<html>`.
- **Delete** HTML comments that explain Webflow internals (e.g. `<!-- [if lte IE 9]>`). Replace with short comments describing *your* behavior only if needed.
- **Do not** add CSS whose only purpose is fighting `.w-*` rules - fix the markup instead.

### 3) Stylesheets

- Audit the exported CSS files. Webflow exports one large `<project-name>.webflow.css` and sometimes a `normalize.css`. You can:
  - **Keep** the Webflow CSS if it is minimal - rename it something project-owned (e.g. `styles/main.css`).
  - **Rewrite** it progressively, moving rules into feature/component files as you clean up the HTML.
- Either way, **rename the file** and update the `<link>` tag so there is no `webflow.css` in production.
- **Order**: base/reset/tokens first, layout next, component overrides last. Page-specific overrides load last.
- **Do not** paste large blocks of CSS that already exist in your project's shared sheets - link the existing file instead.

### 4) JavaScript and interactivity

- Webflow's runtime handles tabs, sliders, dropdowns, and form validation. After removing `webflow.js`, these will not work. You must reimplement or replace each one:
  - **Tabs/accordions**: write a small vanilla JS module or use your framework's equivalent.
  - **Form validation**: use `required`, `type`, and `pattern` HTML attributes plus a small custom handler if needed.
  - **Sliders/carousels**: use a library you own (e.g. Swiper, Splide) or write your own.
- Prefer **one JS module per page** for page-local behavior. Inline small helpers in that module rather than creating tiny one-off files.
- Use `type="module"` on `<script>` tags unless your build pipeline handles bundling.

### 5) Tabs (if applicable)

- If you are replacing Webflow's built-in tab widget, be aware that Webflow uses `w--current` and `w--tab-active` classes to mark active state. When you rewrite the JS, rename these classes to ones you own (e.g. `is-active`) and update HTML and JS together so initial state and click behavior stay in sync.
- The **initial tab** must match both the active link class and active pane class in the HTML - mismatches cause a flash of wrong state on load.

### 6) Forms and controls

- **Custom checkboxes**: Webflow generates a hidden native `<input>` + visible div combo. Port it as a native `<input type="checkbox">` with a visible sibling and proper `<label>` association, using `:focus-visible` for keyboard styles.
- **Do not** hide the native `<input>` with `z-index: -1` in a way that breaks focus or click - use a visually-hidden pattern that preserves accessibility.
- **Decorative elements** (e.g. visual checkbox next to a real one): use `aria-hidden="true"` and `tabindex="-1"` so screen readers and keyboards ignore them.

### 7) Images, icons, and media

- Webflow exports assets into an `images/` folder. **Copy every asset** your page uses into your project's asset directory (e.g. `public/assets/images/`, `static/`, `assets/`).
- **Update all `src` and `href` references** to point to your project's paths - not `../images/…` or Webflow CDN URLs (`https://uploads-ssl.webflow.com/...`).
- Use **root-relative URLs** (e.g. `/assets/images/hero.png`) for portability across pages and hosting configs.
- Check for Webflow-generated Lottie JSON files (`animations/`) - copy those too if the page uses them, and swap the CDN Lottie loader for a self-hosted or npm-installed version.

### 8) Responsive layout

- Webflow uses `max-width: 940px` and `max-width: 1280px` as common container widths - keep these if the design requires them, or adjust to match your design system.
- Check every media query breakpoint in the exported CSS. Webflow's default breakpoints are: `991px` (tablet), `767px` (landscape phone), `479px` (portrait phone). Rename or reorganize as needed.
- `max-width` alone does not center a grid child - pair with `margin: 0 auto` or `justify-self: center` as needed.
- Tighten horizontal padding on small screens; set explicit mobile padding when the design requires it.

### 9) Meta and `<head>` cleanup

- Remove or update the `<title>` and `<meta name="description">` Webflow left.
- Remove `<meta name="generator" content="Webflow">`.
- Remove Webflow's Open Graph placeholders if they point to `webflow.io` domains.
- Keep `<meta name="viewport" content="width=device-width, initial-scale=1">`.

### 10) Verification (before calling it done)

Run this grep from your project root to catch remaining Webflow coupling (adjust the file paths):

```bash
grep -rn \
  "webflow\.js\|webflow\.css\|webflow\.io\|uploads-ssl\.webflow\.com\|d3e54v103j8qbb\|w-inline-block\|w-clearfix\|w-container\|w--current\|w--tab-active\|data-wf-page\|data-wf-site\|generator.*Webflow" \
  ./public ./src ./pages ./app 2>/dev/null || echo "Clean!"
```

Also check manually:

- **Responsive breakpoints**: resize the browser at 480px, 768px, 992px, 1280px.
- **Keyboard focus**: tab through all forms and interactive elements.
- **No layout broken** by missing Webflow utility classes (look for invisible or collapsed elements).
- **Images loading**: no 404s in the network panel.
- **JS behavior**: tabs, forms, carousels, dropdowns all work without `webflow.js`.

---

## File touch map (generic)

| Area | What to do |
|------|------------|
| Page HTML | Remove Webflow `<script>`/`<link>` tags, attributes, and comments; rename classes |
| Stylesheets | Rename `*.webflow.css` → project name; audit and clean rules |
| JavaScript | Replace Webflow runtime behavior with your own modules |
| Assets | Copy from `images/` export into your project asset folder; update paths |
| `<head>` | Remove Webflow meta tags; update title, description, OG tags |

---

## Do not

- Do **not** leave Webflow CDN CSS or JS loading in production - the page will depend on Webflow's infrastructure indefinitely.
- Do **not** leave `w-*` class names as the **only reason layout works** - rename them or replace with your own rules.
- Do **not** cite Webflow in production CSS comments as the authority for a rule.
- Do **not** keep the `<meta name="generator" content="Webflow">` tag.
- Do **not** reference Webflow export paths (`images/`, `documents/`) directly - copy assets into your project.

---

## References

- [Webflow: Exporting code](https://university.webflow.com/lesson/export-your-code) - official export docs; production code should not depend on exported Webflow infrastructure.
- [MDN: Writing accessible forms](https://developer.mozilla.org/en-US/docs/Learn/Forms/How_to_structure_a_web_form) - for replacing Webflow's form markup.
- [Splide](https://splidejs.com/) / [Swiper](https://swiperjs.com/) - drop-in replacements for Webflow's built-in slider if needed.
