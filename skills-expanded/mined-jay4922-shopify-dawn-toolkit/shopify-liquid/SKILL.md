---
name: shopify-liquid
description: The team's authoritative Shopify Liquid coding standard for Dawn-fork themes, combined with Shopify's official theme architecture and Liquid language reference — section/snippet file structure, schema (settings, blocks, the mandatory color/background + padding + custom_class trio), Liquid syntax/filters/objects/tags, metafields, metaobjects, product cards, collection handling, cart logic, and translation/localization standards. Use whenever building, editing, or reviewing any Liquid section, snippet, block, or template; whenever a schema is written or changed; and whenever the user mentions sections, blocks, snippets, metafields, metaobjects, product cards, collections, or cart — even if they just say "build this section" or "add a setting". BUILD-TIME guidance; the qa agent audits against this same file.
---

# Shopify Liquid — Team Coding Standard + Platform Reference

Single source of truth for Liquid. Build follows it; `qa` agent audits against it. For CSS see `tailwind-css`, for section JS see `shopify-javascript`, for headings/JSON-LD see `seo`, for image-loading see `performance` — this file cross-references, doesn't duplicate.

**Base: Dawn-fork conventions. Target: Online Store 2.0, JSON templates.**

**Precedence rule:** Part 1 (Team Workflow) is HOW we build — it always wins. Part 2 (Platform Reference) is Shopify's official language/architecture reference — consult it for syntax, filters, objects, and tags. Where the platform reference describes a generic pattern that conflicts with a team rule (e.g. `{% javascript %}` usage, i18n filters), the team rule applies.

🚨 MANDATORY: CALL `learn_shopify_api` ONCE WHEN WORKING WITH LIQUID THEMES (if the Shopify MCP is available).

---

# PART 1 — TEAM WORKFLOW (how we build)

## Zero-tolerance syntax gate (before marking any section `built`)

**Pre-flight check (do this first, every section using `color_scheme`):** grep the file for every `color-{{ section.settings.color_scheme }}` (or `color-{{ block.settings.color_scheme }}`) occurrence and confirm `gradient` sits directly beside it on the same element. Dawn's `.color-scheme-N` class only sets the scoped CSS custom properties — the actual `background: rgb(var(--color-background))` paint comes from the separate `.gradient` class. Dropping `gradient` renders a scheme with no visible background at all, with no error anywhere. This has already recurred 3 times across different sections in this project — check it proactively instead of waiting to notice a flat/missing background on render.


A shipped `{{ }}`/`{% %}` syntax error is never acceptable. Check every file touched, every time:

1. **Literal brace collisions.** Any `{{`/`}}`/`{%`/`%}` NOT meant as live Liquid (copy quoting code/handlebars, a pasted CSS/JS snippet in a comment, JSON-LD sample text) MUST be wrapped in `{% raw %}...{% endraw %}`. Liquid parses every `{{`/`{%` regardless of surrounding context.
2. **No nested output tags** — never `{{ }}` inside `{{ }}`, never a raw `{%` tag inside a `{{ }}` expression. `{% assign %}` first, then output the variable.
3. **Every opener has its matching closer** — walk top to bottom: `if/endif`, `unless/endunless`, `for/endfor`, `case/endcase`, `capture/endcapture`, `schema/endschema`, `style/endstyle`, `stylesheet/endstylesheet`. A missing `end*` breaks the whole section.
4. **`{% schema %}` JSON must actually parse** — no trailing commas, no `//`/`/* */` comments, no unescaped `"` in strings. Mentally (or via `python3 -c "import json,sys; json.load(sys.stdin)"`) parse it before shipping. Validate section schemas against `schemas/section.json`, block schemas against `schemas/theme_block.json` where available.
5. **Run `shopify theme check`** on touched files as the final gate — same check as the pre-commit hook and `qa` agent, don't wait for either to catch it first.

## File structure

- One section = one file in `sections/`, kebab-case matching the brief handle (`## Hero Banner` → `sections/hero-banner.liquid`).
- Scaffold: Liquid + `{% schema %}` + `{% stylesheet %}` (only if needed). **Section JS never in `{% javascript %}`** — goes in shared `assets/custom.js` (`shopify-javascript` skill). This overrides Shopify's generic per-component `{% javascript %}` guidance.
- Reusable markup in `snippets/`, included via `{% render %}` — never `{% include %}` (deprecated, leaks scope).
- Every **newly-created** snippet gets a `{% doc %}` LiquidDoc header documenting purpose, `@param`s, and an `@example` (see Part 2 → LiquidDoc) — this is a hard requirement for new files. Existing snippets without one are a backlog item, not a build blocker; add the header opportunistically when you're already editing that file, don't treat its absence elsewhere as license to skip it on new work.
- `{% liquid %}` tags for multi-line logic; assign variables at the top before markup.
- `assets/` is flat; never touch `assets/application.css.liquid` (auto-generated).
- **"Never edit Dawn's original files" has one standing carve-out: retrofitting the mandatory schema trio (color/background, padding, `custom_class`) onto a Dawn-named section the project actually uses** (e.g. `sections/custom-liquid.liquid`) — that's expected, in-place modification, not a violation. It does NOT extend to rewriting a Dawn section's markup/behavior wholesale; that still needs a net-new `custom-*` file so Dawn's original stays a diffable reference.

## Schema rules

- Every section: `{% schema %}` with `name`, `tag`, `class`, `settings`, `presets` (required for "Add section" to show it).
- **Every section MUST include these three — no exceptions:**
  1. **Background color**, per Figma design:
     - `color_scheme` (default `scheme-1`) when the merchant should freely pick background (rich-text, generic blocks). Apply `color-{{ section.settings.color_scheme }} gradient` on root. Default must match Figma's exact hex, not "closest available" — check `config/settings_data.json` color_schemes; add a new `scheme-N` with exact hex if none match rather than flagging a mismatch as a deviation and shipping it anyway.
     - `bg_color` (type `color`, default = exact Figma token hex) when Figma specifies a fixed brand background not meant to be merchant-editable via scheme picker. Apply in `{% style %}` as `background-color: {{ section.settings.bg_color }};`.
  2. Padding: `padding_top`, `padding_bottom`, `padding_top_mobile`, `padding_bottom_mobile` (range, px, grouped under Desktop/Mobile headers).
  3. `custom_class` (type `text`, label "Extra CSS Class").
- Padding output — never static padding on the section root:
  ```liquid
  {% style %}
    .section-{{ section.id }}-padding {
      padding-top: {{ section.settings.padding_top }}px;
      padding-bottom: {{ section.settings.padding_bottom }}px;
      /* only when using bg_color: */
      background-color: {{ section.settings.bg_color }};
    }
    @media screen and (max-width: 989px) {
      .section-{{ section.id }}-padding {
        padding-top: {{ section.settings.padding_top_mobile }}px;
        padding-bottom: {{ section.settings.padding_bottom_mobile }}px;
      }
    }
  {% endstyle %}
  ```
  Root carries both classes: `class="section-{{ section.id }}-padding {{ section.settings.custom_class }}"`. With `color_scheme`, also add `color-{{ section.settings.color_scheme }} gradient` (omit with `bg_color`).

### Always pair a plain class with every `{{ section.id }}`-scoped class

Every element that carries an id-scoped hook (`.dp-title-{{ section.id }}`, `.sfaq-item-{{ section.id }}`, `.section-{{ section.id }}-padding`, etc.) MUST also carry a plain, un-scoped class with the same semantic name (no `{{ section.id }}` suffix) — e.g. `class="dp-title dp-title-{{ section.id }}"`, `class="sfaq-item sfaq-item-{{ section.id }}"`.

**Why:** `{{ section.id }}` renders as a long store-generated string (e.g. `template--22649928450179__custom_simple_faq_DpzfcE`), so on live devtools every class name becomes `sfaq-answer-inner-template--22649928450179__custom_simple_faq_DpzfcE` with no readable anchor — nothing in the inspector tells you which section file or which element to open. A plain sibling class (`sfaq-answer-inner`) is instantly greppable in the codebase and instantly recognizable in devtools, while the id-scoped class stays for CSS that needs per-instance settings (colors, custom padding, etc.) — keep using the id-scoped one in `{% style %}` selectors, don't move colors/settings-driven rules onto the plain class, since the plain class is shared across every instance of the section on the page.

Apply this to every new section and snippet going forward, and retrofit it opportunistically whenever an existing section is touched for an unrelated change.

**Also mark the matching CSS rule with a one-line comment naming the plain class**, directly above the id-scoped selector in the style tag:

```css
/* .dp-title */
.dp-title-{{ section.id }} {
  color: {{ section.settings.title_color }};
}
```

This lets a dev search the source file for the plain name (`.dp-title`) shown in devtools and land directly on its rule, instead of hunting through every `-{{ section.id }}` selector. Never write the literal Liquid tag delimiters inside a CSS comment (see the error log entry on brace-collision) — only the plain CSS class name/selector text is safe to put in these comments.

### Setting design (Shopify good practices, adopted)

- **Single-CSS-property settings → CSS variables** on the element, consumed in `{% stylesheet %}`:
  ```liquid
  <div class="collection" style="--gap: {{ section.settings.gap }}px">
  {% stylesheet %}
    .collection { gap: var(--gap); }
  {% endstylesheet %}
  ```
- **Multi-CSS-property settings → CSS classes** driven by a `select`:
  ```liquid
  <div class="collection {{ section.settings.layout }}">
  ```
  with option values being the class names (`collection--full-width`, `collection--narrow`).
- **Mobile column layouts** → `select` with values `"1"`/`"2"` (`columns_mobile`), not a range.

### Schema hygiene

- Labels: translation keys (`"t:sections.<handle>.settings.<id>.label"`) for i18n projects; plain English strings acceptable for single-market/single-locale projects (check project `CLAUDE.md` first — don't mix conventions in one project).
- Setting ids: snake_case, descriptive. Sensible `default` for every setting so the section renders complete out of the box.
- **Range settings — Shopify upload validation:** `(max−min) % step === 0` AND `(default−min) % step === 0`, or upload fails. Safe: `step:2` (max 100/150/200), `step:5` (max 50/100/150), `step:10` (max 100/200). Standard `max:150` padding → `step:5`, not `step:4` (150/4 = 37.5, rejected).
- Repeatable content = blocks; `"max_blocks"` when the design implies a limit. `{{ block.shopify_attributes }}` on each block's root (required for theme-editor selection).
- Merchant-editable text: `richtext`/`inline_richtext` for copy, `text` for labels. Images: `image_picker` (+focal point). Links: `url`. Products/collections: native resource pickers, never text ids.
- Prefer theme color schemes/global typography over one-off pickers. Group with `header` settings. Setting bloat is a defect.
- Never add a section header label or "VIEW ALL" link unless explicitly visible in Figma for that section.

## Liquid rules

- User-facing strings follow the project's i18n choice: `{{ 'key' | t }}` or plain string, per above. On i18n projects, follow Part 2 → Translation standards fully (every string via `| t`, keys in `locales/en.default.json`, sentence case).
- Guard before rendering: `{% if section.settings.heading != blank %}`; fallback where sensible: `{{ section.settings.title | default: 'Default Title' }}`.
- Comment complex logic with `{% comment %}`.
- No nested `for` over large resources (products × variants). `for` loops cap at 50 iterations — paginate anything that can exceed 50 items (see Part 2 → paginate).
- Never access `all_products` with dynamic handles in loops.
- `{%- -%}` whitespace control on control-flow tags. Escape output landing in attributes: `| escape`.
- `{% assign %}` once, not recomputed inside loops. Never name a variable the same as a predefined Liquid object (it overrides the object).
- For logic requiring more than one logical operator, use nested `if`s — Liquid has no parentheses and no ternaries.
- **Never leave a purely-structural `<div>` with no text content.** Dawn's `base.css` ships `div:empty, p:empty, a:empty { display: none; }` — silently collapses ANY empty element (spacer, overlay-tint div, `aria-hidden` placeholder) to zero size, even though the Liquid/CSS looks correct in review. Only shows up on the live render. Give it real content (`&#8203;`) or restructure as a `::before`/`::after` on a non-empty parent.

## Metafields & metaobjects

- Read through the resource, never guess shape: `{{ product.metafields.custom.subtitle.value }}`. `list.*`/reference types return objects/arrays via `.value` — loop them, don't print the raw handle.
- Always guard: `{% if product.metafields.custom.subtitle != blank %}`.
- Type-aware rendering: `rich_text_field` → `| metafield_tag`; file/image reference → resolve then `image_url`/`image_tag`; `date` → `| date`; `money` → `| money`.
- Metaobjects: fetch via a reference metafield or `shop.metaobjects.<type>.values`; access fields as `entry.field_key.value`. Never hardcode GIDs.
- Record which fields/definitions a section depends on in the brief's Dependencies & risks.

## Product cards & collections

- **Always render Dawn's own `snippets/card-product.liquid`** (`{% render 'card-product', card_product: product, ... %}`) for any section that shows product details — one card, reused everywhere. Never write custom product-card markup and never create another card snippet unless it is genuinely necessary (a Figma requirement `card-product` cannot support even after adding settings/CSS to it).
- **"No match — build from scratch" is not sufficient justification on its own.** The brief entry must name the specific thing `card-product` cannot do even after extension (a layout `card-product` structurally can't produce, a data field it has no slot for) — not just that no existing section happened to look the same. Before creating a new card snippet, check `card-product` isn't already forked elsewhere in the project (grep `snippets/` for other `*-card*`/`*-product*` files) — a second undocumented fork means the first one should have been fixed instead of repeated.
- Prefer extending `card-product` (new setting, new CSS class, an optional block) over forking it — a fork drifts out of sync with Dawn updates and doubles the maintenance surface.
- Prices always through money filters (`{{ price | money }}`); handle compare-at, price ranges (`price_varies` → `'products.product.price.from_price_html' | t`), sold-out (`product.available`). Never raw price math in markup.
- Collection loops: paginate (`{% paginate collection.products by 24 %}`), respect settings limits, handle empty collection gracefully (`{% else %}` inside the `for`).
- Native `collection`/`product` resource pickers in schema; never a free-text handle.

### Quick add setting (mandatory on product-related sections)

Any section that lists/grids products (collection grids, featured collection, related products, etc.) **and renders `card-product`** must expose the same **Quick add** control Dawn's own sections ship, wired straight into `card-product`'s `quick_add` param — don't invent a different control or omit it. If a section uses a custom card snippet under the exception above, it still needs some equivalent add-to-cart affordance in its schema (even a simple `show_quick_add` checkbox) — don't silently drop the capability just because the card isn't `card-product`:

```json
{
  "type": "select",
  "id": "quick_add",
  "default": "none",
  "label": "t:sections.main-collection-product-grid.settings.quick_add.label",
  "options": [
    { "value": "none", "label": "t:sections.main-collection-product-grid.settings.quick_add.options.option_1" },
    { "value": "standard", "label": "t:sections.main-collection-product-grid.settings.quick_add.options.option_2" },
    { "value": "bulk", "label": "t:sections.main-collection-product-grid.settings.quick_add.options.option_3" }
  ]
}
```

Reuse the existing `t:sections.main-collection-product-grid.settings.quick_add.*` translation keys (already in `locales/en.default.schema.json`) rather than adding new ones — the label/options text must match Dawn's other product sections exactly so the customizer stays consistent.

### Two-image-picker pattern (background + product overlay)

When a hero card shows a background photo AND a floating product image, use two separate settings:

```json
{ "type": "image_picker", "id": "image", "label": "Background image" },
{ "type": "image_picker", "id": "product_image", "label": "Product overlay image",
  "info": "PNG with transparent bg works best." }
```

Scope the background tag with its own class (e.g. `.fsb-bg-img`) so a broad `img` selector doesn't force `object-fit: cover` onto the overlay (needs `contain`). See `tailwind-css` → Three-layer image stacking.

### Text anchor position in hero cards

Check Figma for anchor: heading at top → `position: absolute; top: 0`; text at bottom → `bottom: 0`. Heading top + buttons bottom → two absolutely-positioned divs (`.text-top`/`.text-bottom`), never one flex with `justify-content: space-between` (collapses when content is short).

## Cart logic

- Mutations go through the AJAX Cart API from `assets/custom.js` — Liquid renders initial state, JS handles add/update/remove/re-render.
- Render line items from `cart.items`, always money filters + `item.final_line_price`. Respect `cart.item_count` for empty state.
- Cart/line-item/selling-plan data renders server-side; don't rely on JS for rankable/visible content.
- Never trust client-supplied quantities without `| escape`; quantity inputs use `min`/`step` matching product rules.
- **Remove the add-to-cart loading spinner sitewide.** Every Dawn-fork build strips the spinner from every add-to-cart button (PDP `product-form`, quick add, quick-order-list, featured-product) — never leave Dawn's default spinner behavior in place. In practice: delete/hide the `{% render 'loading-spinner' %}`/`.loading__spinner` markup in `snippets/buy-buttons.liquid` (and any other buy-button variant) and remove the matching `classList.add('loading')` / `.loading__spinner` toggle calls in the relevant JS (`assets/product-form.js`, `assets/quick-add.js`, `assets/quick-order-list.js`) — don't just hide it with CSS, since the JS still gates on the class. Keep the button's `disabled` state during the add request so double-submits are still prevented.

## Meta description fallback (pages with no admin field)

`layout/theme.liquid` only outputs `<meta name="description">` when `page_description` is present (populated from the admin's SEO fields on products/collections/pages/blog posts/articles). Templates with no admin SEO field — search, cart, 404, and any other template lacking one — render with NO meta description at all unless a fallback is added directly in `theme.liquid`.

- Before building/finalizing `theme.liquid`, check every template in `templates/` for one with no admin-editable SEO description (search, cart, 404 are the standing known cases — re-check the rest of the list per project, since apps/custom templates can add more).
- Add a `{% case request.page_type %}` (or `{% if template == "..." %}`) fallback in `theme.liquid` right where `page_description` is currently checked, providing a static, translated description for each such template:
  ```liquid
  {% if page_description %}
    <meta name="description" content="{{ page_description | escape }}">
  {% else %}
    {% case request.page_type %}
      {% when 'search' %}
        <meta name="description" content="{{ 'meta.search.description' | t | escape }}">
      {% when 'cart' %}
        <meta name="description" content="{{ 'meta.cart.description' | t | escape }}">
      {% when '404' %}
        <meta name="description" content="{{ 'meta.404.description' | t | escape }}">
    {% endcase %}
  {% endif %}
  ```
- Add the matching keys to `locales/en.default.json` (never hardcode the English string inline — same translation rule as everywhere else in this file).
- This is additive to `snippets/meta-tags.liquid`'s existing `og:description` fallback (`page_description | default: shop.description`) — that filter already covers Open Graph/social; this rule is specifically about the `<meta name="description">` tag search engines read, which has no such fallback today.

## Theme-editor compatibility

- Section renders correctly through add/reorder/remove in customizer. Listen for `shopify:section:load`/`unload` where JS holds state (`shopify-javascript` skill).
- Every setting a merchant might reasonably change is exposed; everything else stays out of schema.
- Test empty states: no blocks, blank settings, missing image → degrade gracefully, never broken markup.
- Referencing color settings inside `{% style %}` tags gives live theme-editor updates without page refresh — another reason the padding/bg pattern uses `{% style %}`.

## Cross-references

- Images/lazy-loading/CLS → `performance`.
- Headings/semantic HTML/JSON-LD/link `rel` → `seo`.
- Section JS (custom elements, Swiper, cart AJAX) → `shopify-javascript`.
- CSS architecture/tokens/`!important` → `tailwind-css`.
- Build-time accessibility → `ada-accessibility`.

---

# PART 2 — PLATFORM REFERENCE (Shopify official)

## Theme Architecture

**Key principle: focus on generating snippets, blocks, and sections; users may create templates using the theme editor.**

### Directory structure

```
.
├── assets          # Static assets (CSS, JS, images, fonts, etc.)
├── blocks          # Reusable, nestable, customizable components (theme blocks)
├── config          # Global theme settings and customization options
├── layout          # Top-level wrappers for pages (layout templates)
├── locales         # Translation files for theme internationalization
├── sections        # Modular full-width page components
├── snippets        # Reusable Liquid code or HTML fragments
└── templates       # JSON templates combining sections and blocks
```

#### `sections`
- `.liquid` files creating reusable modules customizable by merchants.
- Can include blocks that merchants add/remove/reorder within the section.
- Made customizable via the required `{% schema %}` tag; validate against the `schemas/section.json` JSON schema.
- Examples: hero banners, product grids, testimonials, featured collections.

#### `blocks` (theme blocks directory)
- `.liquid` files for reusable small components customizable by merchants (needn't be full-width).
- Can nest other blocks; merchants add/remove/reorder content within a block.
- Customizable via `{% schema %}`; validate against `schemas/theme_block.json`.
- Must have a `{% doc %}` header if statically rendered via `{% content_for 'block', id: '42', type: 'block_name' %}`.
- **Team note:** our Dawn-fork projects primarily use *section-scoped blocks* defined inside the section's own `{% schema %}` (Part 1). Only use the `blocks/` directory pattern on projects whose base theme already ships it (Horizon-style) — check the project `CLAUDE.md`.

#### `snippets`
- Reusable fragments rendered in blocks, sections, and layouts via `{% render %}`.
- For logic that's reused but NOT directly merchant-edited in the theme editor.
- Accept parameters when rendered; must have a `{% doc %}` header.
- Examples: buttons, meta-tags, css-variables, form elements, product cards.

#### `layout`
- Overall HTML structure (`<head>`/`<body>`), wraps templates; global nav, cart drawer, footer, CSS/JS assets, meta tags.
- Must include `{{ content_for_header }}` in `<head>` and `{{ content_for_layout }}` for page content.

#### `config`
- `config/settings_schema.json` defines global theme settings (validate with `schemas/theme_settings.json`).
- `config/settings_data.json` holds the data for those settings (including color schemes — see Part 1 background rule).

#### `assets`
- Static files referenced via `asset_url`. Shopify recommends keeping only `critical.css` and files needed on every page here, preferring `{% stylesheet %}`/`{% javascript %}` tags per component. **Team override:** section JS lives in shared `assets/custom.js` (Part 1); `assets/` is flat; never touch `assets/application.css.liquid`.

#### `locales`
- Translation JSON files by language code (`en.default.json`, `fr.json`); strings accessed via `{{ 'key' | t }}`. Validate with `schemas/translations.json`.

#### `templates`
- JSON files defining which sections/blocks appear on each page type and their order — merchants customize layouts without code changes.

### CSS & JavaScript tags

- `{% stylesheet %}` and `{% javascript %}` are only supported in `snippets/`, `blocks/`, and `sections/`. Each file may have at most ONE of each.
- **Liquid is NOT rendered inside `{% stylesheet %}` or `{% javascript %}`** — including Liquid there causes syntax errors. Dynamic CSS (setting-driven values) goes in `{% style %}` instead (Part 1 padding pattern).
- Team: `{% stylesheet %}` only when the section needs scoped static CSS; JS → `assets/custom.js`.

### LiquidDoc

Snippets and statically-rendered blocks must include a LiquidDoc header documenting purpose and parameters:

```liquid
{% doc %}
  Renders a responsive image that might be wrapped in a link.

  @param {image} image - The image to be rendered
  @param {string} [url] - An optional destination URL for the image

  @example
  {% render 'image', image: product.featured_image %}
{% enddoc %}
```

Content inside `{% doc %}` is never rendered; Liquid inside is parsed but not executed. Enables code completion, linting, and inline docs.

## Liquid language

### Delimiters

- `{{ ... }}` — output, prints a value.
- `{{- ... -}}` — output with whitespace trimmed around it.
- `{% ... %}` — logic/control tag (if, for, assign…), prints nothing.
- `{%- ... -%}` — logic tag with whitespace trimmed.

A dash after `{%`/`{{` or before `%}`/`}}` trims adjacent spaces/newlines.

### Operators

Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`. Logical: `and`, `or`. `contains` — string contains substring, or array contains string (strings only, not objects in arrays).

**Condition principles:**
- ALWAYS use nested `if` conditions when logic needs more than one logical operator.
- Parentheses are NOT supported. Ternaries are NOT supported — always `{% if cond %}`.

```liquid
{% if product.type == "Shirt" or product.type == "Shoes" %} ... {% endif %}
{% if product.tags contains "Hello" %} ... {% endif %}
{% unless condition %} ... {% endunless %}
{% case variable %}{% when 'a' %} a {% else %} other {% endcase %}
```

`{% else %}` works inside `if`, `unless`, `case`, and `for` (for-else runs when the array is empty — use it for empty collection states).

### Variables

```liquid
{% assign my_variable = 'value' %}
{% capture my_variable %} Contents {% endcapture %}
{% increment counter %}   {% decrement counter %}
```

- `increment`/`decrement` variables are scoped to the layout/template/section file (shared into snippets rendered from it) and are independent from `assign`/`capture` variables.
- Predefined Liquid objects can be overridden by same-named variables — never reuse an object name.

### Filter chaining

Filters chain left-to-right; each passes its return value to the next when types match:

```liquid
{{ "hello world" | upcase | split: " " | last }}  {# → "WORLD" #}
```

### Filters reference

#### Array
`compact`, `concat: array`, `find: string, string`, `find_index`, `first`, `has`, `join`, `last`, `map: string`, `reject`, `reverse`, `size`, `sort`, `sort_natural`, `sum`, `uniq`, `where: string, string`

#### Cart
`item_count_for_variant: {variant_id}`, `line_items_for: object`

#### Collection
`link_to_type`, `link_to_vendor`, `sort_by: string`, `url_for_type`, `url_for_vendor`, `within: collection`, `highlight_active_tag`

#### Color
`brightness_difference`, `color_brightness`, `color_contrast`, `color_darken: n`, `color_desaturate: n`, `color_difference`, `color_extract`, `color_lighten: n`, `color_mix: string, n`, `color_modify: string, n`, `color_saturate: n`, `color_to_hex`, `color_to_hsl`, `color_to_oklch`, `color_to_rgb`, `hex_to_rgba`

#### Customer
`customer_login_link`, `customer_logout_link`, `customer_register_link`, `avatar`, `login_button`

#### Date / Default
`date: format`; `default: value`, `default_errors`, `default_pagination`

#### Font
`font_face`, `font_modify: string, string`, `font_url`

#### Format
`json`, `structured_data`, `unit_price_with_measurement`, `weight_with_unit`

#### Hosted files
`asset_img_url`, `asset_url`, `file_img_url`, `file_url`, `global_asset_url`, `shopify_asset_url`

#### HTML
`time_tag`, `inline_asset_content`, `highlight`, `link_to`, `placeholder_svg_tag`, `preload_tag: as:`, `script_tag`, `stylesheet_tag`

#### Localization
`currency_selector`, `t` (translate), `format_address`

#### Math
`abs`, `at_least`, `at_most`, `ceil`, `divided_by`, `floor`, `minus`, `modulo`, `plus`, `round`, `times`

#### Media
`external_video_tag`, `external_video_url`, `image_tag`, `media_tag`, `model_viewer_tag`, `video_tag`, `image_url: width:, height:` (modern — prefer over deprecated `img_url`/`*_img_url` variants)

#### Metafield
`metafield_tag`, `metafield_text`

#### Money
`money`, `money_with_currency`, `money_without_currency`, `money_without_trailing_zeros`

#### Payment
`payment_button`, `payment_terms`, `payment_type_img_url`, `payment_type_svg_tag`

#### String
`append`, `prepend`, `capitalize`, `upcase`, `downcase`, `escape`, `escape_once`, `lstrip`, `rstrip`, `strip`, `strip_html`, `strip_newlines`, `newline_to_br`, `remove`, `remove_first`, `remove_last`, `replace`, `replace_first`, `replace_last`, `slice`, `split`, `truncate: n`, `truncatewords: n`, `url_decode`, `url_encode`, `url_escape`, `url_param_escape`, `camelize`, `handleize`, `pluralize: singular, plural`, hashes (`md5`, `sha1`, `sha256`, `hmac_sha1`, `hmac_sha256`, `blake3`), base64 (`base64_encode/decode`, `base64_url_safe_encode/decode`)

#### Tag
`link_to_add_tag`, `link_to_remove_tag`, `link_to_tag`

### Objects reference

#### Global objects (available everywhere)
`collections`, `pages`, `all_products`, `articles`, `blogs`, `cart`, `closest`, `content_for_header`, `customer`, `images`, `linklists`, `localization`, `metaobjects`, `request`, `routes`, `shop`, `theme`, `settings`, `template`, `additional_checkout_buttons`, `all_country_option_tags`, `canonical_url`, `content_for_additional_checkout_buttons`, `content_for_index`, `content_for_layout`, `country_option_tags`, `current_page`, `handle`, `page_description`, `page_image`, `page_title`, `powered_by_link`, `scripts`

#### Per-page objects
- `/article`: `article`, `blog` · `/blog`: `blog`, `current_tags`
- `/cart`: `cart` · `/checkout`: `checkout`
- `/collection`: `collection`, `current_tags`
- `/customers/account` & `/addresses`: `customer` · `/customers/order`: `customer`, `order`
- `/gift_card.liquid`: `gift_card`, `recipient`
- `/metaobject`: `metaobject` · `/page`: `page`
- `/product`: `product`, `remote_product`
- `/robots.txt.liquid`: `robots` · `/search`: `search`

### Tags reference

#### content_for
Requires a type: render theme blocks (`'blocks'`) or a single static block (`'block'`).
```liquid
{% content_for 'blocks' %}
{% content_for 'block', type: "slide", id: "slide-1" %}
```

#### form
Requires a type; some types need an extra parameter. Types: `activate_customer_password`, `cart`, `contact`, `create_customer`, `currency`, `customer`, `customer_address`, `customer_login`, `guest_login`, `localization`, `new_comment`, `product`, `recover_customer_password`, `reset_customer_password`, `storefront_password`.
```liquid
{% form 'form_type' %} content {% endform %}
```

#### layout
```liquid
{% layout name %}
```

#### assign / capture
Any basic type, object, or property. Caution: variables with an object's name override the object.

#### comment / doc / raw
- `{% comment %}` — content not output; Liquid inside parsed but not executed.
- `{% doc %}` — LiquidDoc (see above).
- `{% raw %}` — output `{{`/`{%` literally (the team syntax-gate escape hatch).

#### for / break / continue / cycle / tablerow
- `for` caps at **50 iterations** — beyond that, use `paginate`.
- Every `for` has a `forloop` object; `for`-`else` handles empty arrays.
- `cycle` (inside `for` only) outputs values in a repeating pattern (odd/even rows).
- `tablerow` must be wrapped in `<table>` tags; has a `tablerowloop` object.

#### paginate
Required to iterate arrays >50 items. Paginatable: `article.comments`, `blog.articles`, `collections`, `collection.products`, `customer.addresses`, `customer.orders`, `metaobject_definition.values`, `pages`, `product.variants`, `search.results`, and `article_list`/`collection_list`/`product_list` settings. Inside it you get the `paginate` object and `default_pagination` filter. Hard limit: item 25,000 — filter the array further to reach beyond.
```liquid
{% paginate array by page_size %}
  {% for item in array %} ... {% endfor %}
{% endpaginate %}
```

#### render
Snippets can't access variables created outside them — pass them as parameters (`{% render 'snippet', key: value %}`). They CAN access global objects and objects directly accessible in context (e.g. `product` in product templates, `section` inside sections). `{% include %}` can't be used inside a rendered snippet (and is deprecated everywhere — team rule).

#### liquid / echo
`{% liquid %}` — multi-line logic, one tag per line, no delimiters. Output values inside it with `echo` (supports filters):
```liquid
{% liquid
  assign width = width | default: image.width
  echo image | image_url: width: width | image_tag
%}
```

#### section / sections
- `{% section 'name' %}` — render a single section statically.
- `{% sections 'name' %}` — render a section group in layout files.

#### style vs stylesheet / javascript
- `{% style %}` — Liquid IS rendered inside; color settings referenced here live-update in the theme editor without refresh. Use for setting-driven CSS (team padding/bg pattern).
- `{% stylesheet %}` / `{% javascript %}` — one each per file max; Liquid NOT rendered inside. (Team: JS goes to `custom.js` instead.)

## Translation development standards (i18n projects)

Applies when the project `CLAUDE.md` specifies i18n (Part 1 rule). On single-locale projects, plain strings are acceptable.

- **Every user-facing text** uses translation filters: `{{ 'sections.featured_collection.title' | t }}` — never hardcoded copy.
- **Update `locales/en.default.json`** with all new keys. Only add English; translators handle other languages.
- **Interpolate with variables**, never concatenate strings:
  ```liquid
  {{ 'products.price_range' | t: min: product.price_min | money, max: product.price_max | money }}
  ```
  ```json
  { "products": { "price_range": "From {{ min }} to {{ max }}" } }
  ```
- **Sentence case** for all user-facing text including titles, headings, button labels (`Featured collection`, not `Featured Collection`).
- Escape variables unless they output HTML: `{{ variable | escape }}`.

### Locale file structure

```
locales/
├── en.default.json          # English strings (required)
├── en.default.schema.json   # English theme-editor schema strings (required)
├── fr.json / fr.schema.json # per additional language (IETF tags, e.g. en-GB, fr-CA)
```

- **Locale files** (`*.json`): storefront strings.
- **Schema locale files** (`*.schema.json`): theme-editor setting strings, organized category → group → description.

### Key organization

- Descriptive, hierarchical keys; **maximum 3 levels deep**; snake_case; group related translations.
- Keep text concise for UI elements; consider character limits; consistent terminology.

```json
{
  "general": {
    "accessibility": { "skip_to_content": "Skip to content", "close": "Close" }
  },
  "products": {
    "add_to_cart": "Add to cart",
    "price": { "regular": "Regular price", "sale": "Sale price", "unit": "Unit price" }
  }
}
```

---

# PART 3 — CANONICAL EXAMPLES

### Team-standard section scaffold (Dawn-fork)

Every new section starts from this shape — mandatory trio, `{% style %}` padding block, guarded output, blocks with `shopify_attributes`, presets:

```liquid
{% style %}
  .section-{{ section.id }}-padding {
    padding-top: {{ section.settings.padding_top }}px;
    padding-bottom: {{ section.settings.padding_bottom }}px;
  }
  @media screen and (max-width: 989px) {
    .section-{{ section.id }}-padding {
      padding-top: {{ section.settings.padding_top_mobile }}px;
      padding-bottom: {{ section.settings.padding_bottom_mobile }}px;
    }
  }
{% endstyle %}

<div class="hero-banner section-{{ section.id }}-padding color-{{ section.settings.color_scheme }} gradient {{ section.settings.custom_class }}">
  {%- if section.settings.heading != blank -%}
    <h2 class="hero-banner__heading">{{ section.settings.heading }}</h2>
  {%- endif -%}

  {%- for block in section.blocks -%}
    <div class="hero-banner__item" {{ block.shopify_attributes }}>
      {%- if block.settings.text != blank -%}
        {{ block.settings.text }}
      {%- endif -%}
    </div>
  {%- endfor -%}
</div>

{% schema %}
{
  "name": "Hero Banner",
  "tag": "section",
  "class": "section",
  "settings": [
    {
      "type": "inline_richtext",
      "id": "heading",
      "label": "Heading",
      "default": "Hero Banner"
    },
    {
      "type": "color_scheme",
      "id": "color_scheme",
      "label": "Color scheme",
      "default": "scheme-1"
    },
    { "type": "header", "content": "Desktop Padding" },
    {
      "type": "range",
      "id": "padding_top",
      "label": "Padding top",
      "min": 0,
      "max": 150,
      "step": 5,
      "unit": "px",
      "default": 50
    },
    {
      "type": "range",
      "id": "padding_bottom",
      "label": "Padding bottom",
      "min": 0,
      "max": 150,
      "step": 5,
      "unit": "px",
      "default": 50
    },
    { "type": "header", "content": "Mobile Padding" },
    {
      "type": "range",
      "id": "padding_top_mobile",
      "label": "Padding top (mobile)",
      "min": 0,
      "max": 150,
      "step": 5,
      "unit": "px",
      "default": 30
    },
    {
      "type": "range",
      "id": "padding_bottom_mobile",
      "label": "Padding bottom (mobile)",
      "min": 0,
      "max": 150,
      "step": 5,
      "unit": "px",
      "default": 30
    },
    {
      "type": "text",
      "id": "custom_class",
      "label": "Extra CSS Class"
    }
  ],
  "blocks": [
    {
      "type": "item",
      "name": "Item",
      "settings": [
        {
          "type": "richtext",
          "id": "text",
          "label": "Text"
        }
      ]
    }
  ],
  "presets": [
    { "name": "Hero Banner" }
  ]
}
{% endschema %}
```

### Snippet with LiquidDoc (Shopify pattern, team-adopted)

```liquid
{% doc %}
  Renders a responsive image that might be wrapped in a link.

  When `width`, `height` and `crop` are provided, the image renders
  with a fixed aspect ratio.

  @param {image} image - The image to be rendered
  @param {string} [url] - An optional destination URL for the image
  @param {string} [css_class] - Optional class added to the image wrapper
  @param {number} [width] - Highest resolution width to render
  @param {number} [height] - Highest resolution height to render
  @param {string} [crop] - Crop position

  @example
  {% render 'image', image: product.featured_image %}
  {% render 'image', image: product.featured_image, url: product.url %}
{% enddoc %}

{% liquid
  unless height
    assign width = width | default: image.width
  endunless

  if url
    assign wrapper = 'a'
  else
    assign wrapper = 'div'
  endif
%}

<{{ wrapper }}
  class="image {{ css_class }}"
  {% if url %}
    href="{{ url }}"
  {% endif %}
>
  {{ image | image_url: width: width, height: height, crop: crop | image_tag }}
</{{ wrapper }}>

{% stylesheet %}
  .image {
    display: block;
    position: relative;
    overflow: hidden;
    width: 100%;
    height: auto;
  }
  .image > img {
    width: 100%;
    height: auto;
  }
{% endstylesheet %}
```

### Theme block example (only for projects using the `blocks/` directory)

```liquid
{% doc %}
  Renders a text block.

  @example
  {% content_for 'block', type: 'text', id: 'text' %}
{% enddoc %}

<div
  class="text {{ block.settings.text_style }}"
  style="--text-align: {{ block.settings.alignment }}"
  {{ block.shopify_attributes }}
>
  {{ block.settings.text }}
</div>

{% stylesheet %}
  .text {
    text-align: var(--text-align);
  }
  .text--title {
    font-size: 2rem;
    font-weight: 700;
  }
  .text--subtitle {
    font-size: 1.5rem;
  }
{% endstylesheet %}

{% schema %}
{
  "name": "t:general.text",
  "settings": [
    {
      "type": "text",
      "id": "text",
      "label": "t:labels.text",
      "default": "Text"
    },
    {
      "type": "select",
      "id": "text_style",
      "label": "t:labels.text_style",
      "options": [
        { "value": "text--title", "label": "t:options.text_style.title" },
        { "value": "text--subtitle", "label": "t:options.text_style.subtitle" },
        { "value": "text--normal", "label": "t:options.text_style.normal" }
      ],
      "default": "text--title"
    },
    {
      "type": "text_alignment",
      "id": "alignment",
      "label": "t:labels.alignment",
      "default": "left"
    }
  ],
  "presets": [{ "name": "t:general.text" }]
}
{% endschema %}
```
