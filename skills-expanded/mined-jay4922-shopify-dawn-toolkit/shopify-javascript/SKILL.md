---
name: shopify-javascript
description: The team's authoritative standard for theme JavaScript in Dawn-fork Shopify projects — the single shared assets/custom.js file, guarded custom elements, theme-editor (shopify:section:*) compatibility, AJAX cart interactions, Swiper 11 sliders, DOM/event optimization, error handling, and memory-leak prevention. Use this skill whenever writing or editing any section JavaScript, custom.js, sliders/carousels, accordions, drawers, modals, or cart interactions — even if the user just says "make this interactive" or "add a slider". BUILD-TIME guidance; the qa agent audits JS against this same file.
---

# Shopify Theme JavaScript Standard

Single source of truth for all team-authored JS. The build follows it; the `qa` agent audits against it.

## The one-file rule (load-bearing for linting)

- **All team-authored JS lives in ONE shared file: `assets/custom.js`.** One file for every section's JS, appended per section with a clear header: `/* ===== custom-hero-slider ===== */`.
- The `custom` prefix is load-bearing: ESLint/Prettier are configured to lint ONLY `custom*` files and ignore Dawn's originals (standard configs: `tailwind-css/references/eslint.config.mjs` and `.prettierignore`, copied to the theme root at init). Never create per-section JS files, never put logic in `{% javascript %}` tags (it escapes linting), never edit Dawn's original JS.
- Verify the ignore-glob actually covers `custom.js` (no dash) and not just `custom-*.js` (with a dash) — run `npx eslint assets/custom.js` directly after any change to `eslint.config.mjs`'s ignore patterns. A 0-error pre-commit result can mean the file was silently never scanned, not that it's clean.
- Loaded ONCE in `layout/theme.liquid`: `<script src="{{ 'custom.js' | asset_url }}" defer="defer"></script>`. Sections never add their own script tags. If the tag isn't there yet, add it once.

## Custom-element architecture (mandatory)

Because `custom.js` loads on every page, every component must be a custom element with a guard so its logic runs only where its element exists:

```js
/* ===== custom-hero-slider ===== */
if (!customElements.get("custom-hero-slider")) {
  customElements.define(
    "custom-hero-slider",
    class extends HTMLElement {
      connectedCallback() {
        this.slider = this.querySelector(".swiper");
        this.onResize = debounce(() => this.recalc(), 150);
        window.addEventListener("resize", this.onResize);
        this.init();
      }
      disconnectedCallback() {
        window.removeEventListener("resize", this.onResize);
        this.swiper?.destroy(true, true); // free listeners + DOM refs
      }
      init() {
        /* ... */
      }
    },
  );
}
```

- Init in `connectedCallback()`, tear down in `disconnectedCallback()`. This pairing is how the theme editor stays stable and how you avoid leaks.
- Never add top-level code that runs unconditionally at file scope (no bare `document.querySelector` init). Everything hangs off an element.
- Scope queries to the instance: `this.querySelector(...)`, never `document.querySelector(...)` — this is what lets multiple instances of the same section coexist on one page.

## Theme-editor compatibility

- Handle `shopify:section:load` (re-init on add/reorder) and `shopify:section:unload` (destroy). With custom elements, `connectedCallback`/`disconnectedCallback` fire automatically on these — prefer that over manual event wiring, but add explicit `shopify:section:*` listeners for anything the callbacks don't cover (e.g. re-init a Swiper after a block reorder).
- The section must survive add → configure → reorder → remove in the customizer with zero console errors.

## AJAX & cart interactions

- Use the Shopify AJAX Cart API (`/cart/add.js`, `/cart/change.js`, `/cart/update.js`) via `fetch`. Read routes from Dawn's global `routes` object — never hardcode `/cart/...` paths (breaks on localized stores).
- Always `await` and check `response.ok`; parse JSON in a `try/catch`; surface a user-visible error on failure, never a silent catch.
- After a mutation, re-render from the returned cart state and publish Dawn's `PUB_SUB_EVENTS.cartUpdate` so the cart drawer/count stay in sync — don't manually poke unrelated DOM.
- Debounce quantity-stepper input; disable the add button while a request is in flight to prevent double-submits.

## Sliders

- **Swiper 11 only** (not Flickity, no jQuery). Initialize per instance inside the custom element; destroy in `disconnectedCallback`.
- Reserve slider height in CSS so init causes no layout jump (see `performance` skill, CLS).
- Accessibility: enable Swiper's keyboard + a11y modules, aria-labels on prev/next, accessible pagination, and respect `prefers-reduced-motion` (no forced autoplay under it) — see `ada-accessibility` skill.
- **Any element using `h-full`/`w-full` inside a `.swiper-slide` must explicitly declare `box-sizing: border-box` in its own scoped CSS.** Swiper's own stylesheet sets `.swiper-wrapper { box-sizing: content-box }`, which can leak into descendants and make a percentage-height card overflow its `h-full` reference by exactly its own padding+border — invisible from reading the code, only visible on a live render. Don't rely on Tailwind's global Preflight reaching elements nested inside Swiper's DOM.

## DOM & performance

- Cache DOM references in `connectedCallback`; don't re-query in hot paths (scroll/resize/input handlers).
- Debounce/throttle scroll and resize handlers (Dawn's global `debounce` is available). Prefer `IntersectionObserver` over scroll math for reveal/lazy behavior.
- Batch DOM writes; avoid layout thrashing (read then write, don't interleave).
- No external libraries unless bundle size is justified and recorded in the brief.

## Error handling & guards

- Guard every optional element with `?.` so a section never throws if a setting is off or a block is absent.
- No unhandled promise rejections; every `fetch` chain has a `catch`.
- Never assume an element exists because the markup "should" have it — the merchant may have emptied a setting.

## Memory-leak prevention

- Every listener added in `connectedCallback` (or elsewhere) is removed in `disconnectedCallback` — use **named handlers**, not anonymous inline functions, so they can be removed.
- Destroy third-party instances (Swiper, observers, timers/intervals) on disconnect. Disconnect any `IntersectionObserver`/`MutationObserver` you create.
- Don't retain references to removed DOM nodes in module-level variables.

## Lint gate (enforced on commit — must pass)

`const`/`let` only, `prefer-const`, `===` always, curly braces always, template literals, no `console.log`/`debugger`/`alert`, max nesting depth 4, no shadowing, no use-before-define, no loop functions, no duplicate imports, no unsafe optional chaining, `array-callback-return`, no useless returns. Dawn globals declared readonly and safe to use: `Shopify`, `routes`, `trapFocus`, `debounce`, `PUB_SUB_EVENTS`.



# Swiper Slider (project standard)

**Rule:** any slider = Swiper.js Core. Never a custom JS slider, CSS scroll-snap,
or another library. Base it on https://swiperjs.com/demos and match the Figma
exactly (visible slides, spacing, arrow/pagination position, direction, effect).

**This section follows the one-file rule above — there is no separate `swiper-init.js` file and no per-section inline `<script>` tag.** Every slider is its own guarded custom element appended to `assets/custom.js` (same pattern as the `custom-hero-slider` example earlier in this file), reading its Swiper config from a `<script type="application/json">` tag the section renders. Only Swiper the *library* (not team code) loads separately — see step 1.

## 1. Load the Swiper library once, from the official CDN (in `layout/theme.liquid`, before `</head>`)

**Do not vendor Swiper into `assets/` (no `swiper.min.js`/`swiper-bundle.min.js` committed to the repo).** Load it from Swiper's official CDN, and always the `.min.` build — never the unminified/bundle-with-everything variant — to keep the payload small:

```liquid
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js" defer></script>
```

Add these once if not already present; never add a second `<link>`/`<script>` pair per section. (If the project's `assets/` currently has locally-bundled Swiper files and `theme.liquid` points at those instead of the CDN, that's drift from this rule — flag it and switch to the CDN links above rather than adding to the local copies.)

## 2. Slider custom element — appended to `assets/custom.js`

No separate init file. Each slider gets its own guarded custom element block, following the exact `connectedCallback`/`disconnectedCallback` pattern from the top of this skill:

```js
/* ===== custom-swiper-slider ===== */
if (!customElements.get('custom-swiper-slider')) {
  customElements.define(
    'custom-swiper-slider',
    class extends HTMLElement {
      connectedCallback() {
        this.swiperEl = this.querySelector('.swiper');
        this.init();
        if (window.Shopify && Shopify.designMode) {
          this.onSelect = () => this.swiper?.autoplay?.stop();
          this.onDeselect = () => this.swiper?.autoplay?.start();
          this.addEventListener('shopify:section:select', this.onSelect);
          this.addEventListener('shopify:section:deselect', this.onDeselect);
        }
      }
      disconnectedCallback() {
        this.swiper?.destroy(true, true);
        this.removeEventListener('shopify:section:select', this.onSelect);
        this.removeEventListener('shopify:section:deselect', this.onDeselect);
      }
      init() {
        if (typeof Swiper === 'undefined' || !this.swiperEl) return;
        var tag = this.querySelector('script[data-swiper-config]');
        var cfg = {};
        try { cfg = JSON.parse(tag ? tag.textContent : '{}'); } catch (e) {}
        var next = this.querySelector('.swiper-button-next'),
            prev = this.querySelector('.swiper-button-prev'),
            pg = this.querySelector('.swiper-pagination');
        if (next && prev) cfg.navigation = Object.assign({}, cfg.navigation, { nextEl: next, prevEl: prev });
        if (pg && cfg.pagination) cfg.pagination = Object.assign({ el: pg }, cfg.pagination);
        cfg.a11y = Object.assign({ enabled: true }, cfg.a11y);
        cfg.keyboard = Object.assign({ enabled: true }, cfg.keyboard);
        if (cfg.autoplay && window.matchMedia('(prefers-reduced-motion: reduce)').matches) delete cfg.autoplay;
        this.swiper = new Swiper(this.swiperEl, cfg);
      }
    },
  );
}
```

The section's markup wraps everything in `<custom-swiper-slider>` (scoped to `section.id` isn't needed — the custom element already scopes queries to `this`, per the "Custom-element architecture" rule above, so multiple instances on one page never clash).

## 3. Section markup (`.swiper > .swiper-wrapper > .swiper-slide`, no extra nesting)

Options come from settings as JSON. Slides-per-view is mobile-first (base = mobile,
`breakpoints` raise it). Arrows use the reusable SVGs via `inline_asset_content`.

```liquid
<custom-swiper-slider class="slider slider--{{ section.id }}">
  <div class="swiper">
    <script type="application/json" data-swiper-config>
      {
        "loop": {{ section.settings.loop }},
        "speed": {{ section.settings.speed }},
        "spaceBetween": {{ section.settings.space_between }},
        "slidesPerView": {{ section.settings.mobile_slides }},
        "grabCursor": true
        {%- if section.settings.pagination != 'none' -%}
          , "pagination": { "type": {{ section.settings.pagination | json }}, "clickable": true }
        {%- endif -%}
        {%- if section.settings.autoplay -%}
          , "autoplay": { "delay": {{ section.settings.autoplay_delay }}, "pauseOnMouseEnter": true }
        {%- endif -%}
        , "breakpoints": {
          "768": { "slidesPerView": {{ section.settings.tablet_slides }} },
          "1024": { "slidesPerView": {{ section.settings.desktop_slides }} }
        }
      }
    </script>
    <div class="swiper-wrapper">
      {%- for block in section.blocks -%}
        <div class="swiper-slide" {{ block.shopify_attributes }}>
          {%- if block.settings.image -%}{{ block.settings.image | image_url: width: 1200 | image_tag: loading: 'lazy' }}{%- endif -%}
        </div>
      {%- endfor -%}
    </div>
    {%- if section.settings.pagination != 'none' -%}<div class="swiper-pagination"></div>{%- endif -%}
  </div>
  {%- if section.settings.navigation -%}
    <button type="button" class="swiper-button-prev" aria-label="Previous">{{ 'icon-slider-left.svg' | inline_asset_content }}</button>
    <button type="button" class="swiper-button-next" aria-label="Next">{{ 'icon-slider-right.svg' | inline_asset_content }}</button>
  {%- endif -%}
</custom-swiper-slider>
```

## 4. Theme Editor settings (add only what the design uses)

`{% schema %}` settings → Swiper options: `loop`, `speed`, `space_between`,
`desktop_slides` / `tablet_slides` / `mobile_slides`, `navigation` (checkbox),
`pagination` (select: none / bullets / fraction / progressbar), `autoplay` +
`autoplay_delay`, and `direction`. Give the section a `slide` block and a preset.

## Autoplay rules

- Add the `autoplay` object **only** when autoplay is on; otherwise omit it.
- Always set `delay` (ms) — 4000–6000 reads well. Set it from a setting.
- Use `pauseOnMouseEnter: true` and `disableOnInteraction: false` so it pauses on
  hover but resumes after the user swipes (don't kill autoplay permanently on the
  first touch).
- Pair autoplay with `loop: true` so it doesn't stop dead on the last slide.
- Respect motion preferences: skip autoplay when the user prefers reduced motion —
  `if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) delete cfg.autoplay;`
- In the Theme Editor, stop autoplay while a section is selected so the merchant
  can edit the slide they're on.

```json
{ "loop": true, "autoplay": { "delay": 5000, "pauseOnMouseEnter": true, "disableOnInteraction": false } }
```

## Pagination rules

- Render `.swiper-pagination` and add the `pagination` object **only** when a type
  other than `none` is selected.
- Types: `bullets` (default), `fraction`, `progressbar` — match the Figma.
- For bullets, set `clickable: true`. Use `dynamicBullets: true` when there are
  many slides so the dot row stays compact.
- Keep `el` scoped to the instance (`this.querySelector` inside the custom element already does this) so multiple
  sliders don't share one pagination element.

```json
{ "pagination": { "type": "bullets", "clickable": true, "dynamicBullets": true } }
```

## 5. Reusable arrows (save as `assets/icon-slider-left.svg` / `icon-slider-right.svg`)

`currentColor` lets CSS recolor them: `.swiper-button-prev, .swiper-button-next { color: #0c2c67; }`

```xml
<!-- icon-slider-left.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-19.04 0 75.803 75.803" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M660.313,383.588a1.5,1.5,0,0,1,1.06,2.561l-33.556,33.56a2.528,2.528,0,0,0,0,3.564l33.556,33.558a1.5,1.5,0,0,1-2.121,2.121L625.7,425.394a5.527,5.527,0,0,1,0-7.807l33.556-33.559A1.5,1.5,0,0,1,660.313,383.588Z" transform="translate(-624.082 -383.588)"/></svg>
```

```xml
<!-- icon-slider-right.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-19.04 0 75.804 75.804" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M833.068,460.252a1.5,1.5,0,0,1-1.061-2.561l33.557-33.56a2.53,2.53,0,0,0,0-3.564l-33.557-33.558a1.5,1.5,0,0,1,2.122-2.121l33.556,33.558a5.53,5.53,0,0,1,0,7.807l-33.557,33.56A1.5,1.5,0,0,1,833.068,460.252Z" transform="translate(-831.568 -384.448)"/></svg>
```

## Checklist

Swiper Core loaded from official CDN (`.min.` build, not vendored into `assets/`) ·
slider is a guarded custom element inside `assets/custom.js` (no separate init
file, no per-section `<script>`) · correct markup · options in Theme Editor ·
responsive per breakpoint · multiple instances work · arrows use bundled SVGs ·
keyboard + ARIA · `box-sizing: border-box` on any `h-full`/`w-full` element inside
a `.swiper-slide` · minimal scoped CSS · matches Figma exactly.
