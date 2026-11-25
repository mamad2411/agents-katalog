---
name: pfp-skill
description: This skill should be used when the user asks to create print front page styles, set up a new newspaper customer theme, write SCSS for Gazette print front pages, create or modify DrEdition content schemas for print, implement skins or modifiers, or develop a processor for edition info rendering.
---

# Print Front Page Styling

Implement print front page themes for Aptoma's Gazette rendering system. Gazette transforms DrEdition print edition data into absolutely-positioned HTML pages, rendered to PDF via PDFreactor. Each customer's visual identity is defined through SCSS stylesheets, DrEdition content schemas, and optional server-side processors.

## Core Concepts

A front page is a flat array of **blocks**, each absolutely positioned within a content area (in mm). Blocks contain **items** — the editorial content (articles, flags, edition info). The rendering pipeline:

1. DrEdition API provides edition data (blocks with items, page settings)
2. The **normalizer** transforms API data into positioned blocks with CSS custom properties
3. An optional **processor** injects dynamic content (dates, logos, issue numbers) into specific blocks
4. The **renderer** produces HTML with inline styles for positioning and CSS classes for theming
5. A **theme stylesheet** (SCSS) provides all visual styling — typography, colors, layout refinements
6. PDFreactor converts the HTML to a print-ready PDF with CMYK colors and embedded fonts

## When to Use This Skill

- Setting up a new customer's print front page from scratch
- Writing or modifying SCSS theme stylesheets for print
- Creating or updating DrEdition content schemas (item and group schemas)
- Implementing skins, modifiers, or layout patterns
- Developing a processor for edition info, logos, or dynamic content
- Debugging print rendering issues (positioning, colors, fonts, PDF output)

## Workflow: New Customer Setup

Follow these steps in order. Each step references detailed documentation in `references/`.

### 1. Create Asset Repository

Create the asset repository from the DrEdition GUI at `https://{customer}.dredition.aptoma.no/#/settings/asset-repos/repo/new`. This creates a new `aptoma-ext/pfp-assets-{clientId}` repository using the bootstrap template (`pfp-assets-bootstrap`), which provides:

```
pfp-assets-{clientId}/
├── package.json              (build scripts, dependencies)
├── config.json
├── schemas/
│   ├── pfp-story.json        (generic article schema)
│   ├── pfp-ref.json          (reference/teaser schema)
│   └── SCHEMAS.md
├── static/
│   └── pfp/                  (logos, fonts, icons)
├── stylesheets/
│   ├── bootstrap.scss        (entry point — rename to {theme}.scss)
│   ├── _mixins.scss          (shared mixins: text-affinity, image-gradient, cmyk)
│   ├── fonts/
│   │   ├── _Inter.scss
│   │   └── _PTSerif.scss
│   └── themes/
│       └── bootstrap/        (rename to {theme}/)
│           ├── _bootstrap.scss
│           ├── _base.scss
│           ├── _skins.scss
│           └── _fonts.scss
└── .gitignore
```

After creation, rename the `bootstrap` theme directory and entry point to match the customer's theme name.

### 2. Define Content Schemas

Create group and item schemas for DrEdition.

**Group schema** defines block-level properties: layout, position, dimensions, modifiers, item defaults. Mark positional fields as `readonly`.

**Item schemas** define article content: text fields (title, pretitle, summary, byline), control fields (skin, textPosition, imagePosition), modifiers, image, caption, adjustments. Create at minimum:
- One generic schema with `x-dredition.printSourceItemType` for article import
- Specialized schemas per skin (cover-story, ref, etc.) without `printSourceItemType`

Reference: [schema-reference.md](references/schema-reference.md)

### 3. Create Templates in DrEdition

In the print front page format:
1. Set page dimensions, margins, columns, baseline from the design spec
2. Create template pages with blocks at the correct positions
3. Set `type`, `title`, `layout`, `itemData` (default skin/type) on each block
4. Configure bleed if needed

### 4. Write SCSS Theme

Create the theme stylesheet. Follow this structure:

```scss
// Theme styles don't need product scoping unless multiple products share
// a theme. Use .print-product--{NAME} for product-specific overrides.

// 1. CSS custom properties (colors, fonts, spacing)
:root {
  --baseline: 11pt;
  --color-brand: #005593;

  @media print {
    --color-brand: cmyk(100%, 50%, 0%, 25%);
  }
}

// 2. PDFreactor image settings
.image-content {
  -ro-image-resampling: 220dpi;
  -ro-image-recompression: jpeg(85%);
}

// 3. Base element bindings (title, summary → CSS vars)
.item {
  .title {
    font-family: var(--title-font-family);
    font-weight: var(--title-font-weight);
    font-size: var(--title-font-size);
    line-height: var(--title-line-height);
  }
}

// 4. Skin styles
.item--skin-cover-story {
  --title-font-family: 'PublicoHeadline';
  --title-font-weight: 700;
  --title-font-size: 66pt;
  --title-line-height: calc(var(--title-font-size) + 2pt);
}

// 5. Modifier styles
.item--text-color-white {
  --text-color: var(--color-white);
}

// 6. Block-specific styles
.block--logo { ... }
```

Reference: [scss-patterns.md](references/scss-patterns.md), [html-structure.md](references/html-structure.md)

### 5. Develop Processor (if needed)

Create a processor when blocks need dynamic content (dates, issue numbers, logos, volume calculations).

```typescript
export function process(context, block, content, attributes) {
    if (block.name === 'Logo') {
        attributes.class = attributes.class + ' block--logo';
        content += `<div class="edition-info">...</div>`;
    }
    return [content, attributes];
}
```

Match blocks by `block.name` (most common) or `block.contentType`. Register in `src/lib/processors/index.ts`.

Reference: [processor-guide.md](references/processor-guide.md)

### 6. Test and Verify

1. Push asset repo, wait for asset builder
2. Open preview URL: `/preview?editionId={id}&apikey={key}&userId={userId}`
3. Verify: page dimensions, block positions, typography, colors, images, print output
4. Generate PDF through Brokkr and verify CMYK colors, font embedding, bleed, image quality

## HTML Structure Summary

The renderer produces this structure (full reference in [html-structure.md](references/html-structure.md)):

```
body.product--{name}.print-product--{name}.day--{day}
  style (base + theme CSS, @page rule)
  div.frontpage
    div.content-area
      div.block.block--{type}.block--{modifier}  [positioned absolutely]
        div.item.item--skin-{skin}.item--{modifier}
          div.header
          div.text
            div.pretitle
            div.title
            div.subheadline
            div.summary
            div.byline
            div.text-meta (section, pageRef)
          div.image
            div.image-content  [background-image]
            div.image-caption
```

All positioning uses CSS custom properties (`--block-width`, `--block-top`, `--item-width`, etc.) consumed by base styles.

## Skin System

Skins are the primary styling mechanism. Each skin value in the schema produces an `item--skin-{name}` class on the item div. The preferred pattern is to define typography bindings once at the `.item` level using CSS custom properties, then set values per skin.

### Typography Binding Pattern

Bind element styles to CSS custom properties at `.item`, then set values per skin. This keeps specificity flat and makes skins composable with modifiers.

```scss
// Bind once
.item {
  .title {
    font-family: var(--title-font-family);
    font-weight: var(--title-font-weight);
    font-size: var(--title-font-size);
    line-height: var(--title-line-height);
  }
  .summary {
    font-family: var(--summary-font-family);
    font-weight: var(--summary-font-weight);
    font-size: var(--summary-font-size);
    line-height: var(--summary-line-height);
  }
}

// Set per skin
.item--skin-cover-story {
  --title-font-family: 'PublicoHeadline';
  --title-font-weight: 700;
  --title-font-size: 66pt;
  --title-line-height: calc(var(--title-font-size) + 2pt);
  --summary-font-family: 'PublicoText';
  --summary-font-weight: 400;
  --summary-font-size: 16pt;
  --summary-line-height: calc(var(--summary-font-size) + 5pt);
}

.item--skin-ref {
  --title-font-family: 'Inter';
  --title-font-weight: 400;
  --title-font-size: 18pt;
  --title-line-height: calc(var(--title-font-size) + 2pt);
}
```

### Line-Height Strategy

When multiple sizes share a consistent offset (e.g. leading is always fontSize + 2pt), use `calc()` so line-height scales with dynamic title resizing:

```scss
--title-line-height: calc(var(--title-font-size) + 2pt);
```

When sizes use a consistent ratio, use a unitless value:

```scss
--title-line-height: 1.2;
```

When neither pattern applies, use explicit values per skin.

### Style Variants Within a Skin

Use modifier classes to create variants within a skin:

```scss
.item--skin-cover-story {
  // Default cover story
  &.item--style-oppslag {
    .title {
      font-family: PublicoHeadline-Medium;
    }
  }

  // Extra-large variant
  &.item--style-oppslag-xl {
    --title-font-size: 78pt;
    .title {
      font-family: Graphik;
      font-weight: 700;
      text-transform: uppercase;
    }
  }
}
```

### Text-on-Image Layout

For items where text overlays the image, combine `item--text-on-image` modifier with `text-affinity()` and `image-gradient()` mixins:

```scss
.item--skin-cover-story {
  &.item--text-on-image {
    .text {
      position: absolute;
      z-index: 2;
      width: var(--text-width, auto);
    }

    .image {
      position: absolute;
      top: 0; bottom: 0; width: 100%; height: 100%;
    }
  }

  @include text-affinity();     // Position .text per text-pos modifier
  @include image-gradient();    // Gradient overlay adapting to text position
}
```

### Flex Ordering

Control visual order of text and image independently of HTML source order:

```scss
.item--skin-cover-story {
  .image {
    order: 1;          // Image first visually
    flex-grow: 1;
  }
  .text {
    order: 2;          // Text second visually
  }
}
```

### Editor Integration Properties

Set CSS custom properties to configure interactive behavior in the DrEdition preview editor:

```scss
.item--skin-cover-story {
  .title {
    --text-resizable: true;
    --text-font-size-field: titleFontSize;
    --text-line-height-field: titleLineHeight;
    --text-resize-min: 8pt;
    --text-resize-max: 128pt;
  }

  --text-position-options: top bottom left center right;
  --text-position-default: bottom-left;
  --image-resize: width;
}
```

## Modifier System

Modifiers from the item schema produce classes and CSS custom properties on the item div.

### Class Generation Rules

| Schema Type | Schema Value | Result |
|------------|-------------|--------|
| Boolean `true` | `"text-on-image": true` | Class `item--text-on-image` |
| Boolean `false` | `"text-on-image": false` | No class (omitted) |
| String | `"text-color": "white"` | Class `item--text-color-white` |
| `--` prefixed key | `"--gradient-start": "rgba(0,0,0,0.8)"` | Inline style `--gradient-start: rgba(0,0,0,0.8)` |

### Color Modifier Pattern

Define text color as a modifier with screen/print values:

```scss
.item--text-color-white {
  --text-color: var(--color-white);
  --gradient-start: rgba(0, 0, 0, 0.8);
  --gradient-end: rgba(0, 0, 0, 0);
}

.item--text-color-black {
  --text-color: var(--color-black);
  --gradient-start: rgba(255, 255, 255, 0.8);
  --gradient-end: rgba(255, 255, 255, 0);
}
```

This pattern makes gradient overlays automatic — the `image-gradient()` mixin reads from `--gradient-start` and `--gradient-end`.

### Section Color Modifier Pattern

Map section colors to a CSS variable for consistent theming:

```scss
.item--section-color-blue  { --section-color: var(--color-brand-blue); }
.item--section-color-red   { --section-color: var(--color-red); }
.item--section-color-green { --section-color: var(--color-green); }
```

### Combining Skins and Modifiers

Nest modifier overrides within skins for skin-specific behavior:

```scss
.item--skin-cover-story {
  &.item--text-shadow {
    .title, .pretitle {
      text-shadow: 0 0 16pt var(--text-shadow-color);
    }
  }
}
```

### Block-Level Modifiers

Block modifiers produce `block--{key}` or `block--{key}-{value}` classes. Common uses:

```scss
// Divider lines between blocks
.block--divider-left {
  border-left: var(--divider-width, 0.5pt) solid var(--color-black);
}

.block--divider-right {
  border-right: var(--divider-width, 0.5pt) solid var(--color-black);
}

// Item count modifier (auto-generated: block--items-{n})
.block--items-1 .item { /* single item layout */ }
.block--items-3 .item { /* three-item layout adjustments */ }
```

### Block Name Selectors

Each block has a `name` attribute from the template. Use `[name='...']` attribute selectors for block-specific styles that go beyond type/modifier classes. This coupling is intentional — block names are stable template identifiers:

```scss
[name='Logo'] { background-size: contain; }
[name='Cover 1'] .title { font-size: 72pt; }
```

### Field-Level Property Classes

Schema properties matching `{field}--{qualifier}` produce additional classes on the field's div:

```json
{ "title--weight": { "type": "string", "enum": ["bold", "light"] } }
```

With value `"bold"` → the `.title` div gets classes `title title--weight-bold`.

Style accordingly:

```scss
.title--weight-bold { font-weight: 700; }
.title--weight-light { font-weight: 300; }
```

Content containing `<strong>` tags automatically gets `title--has-strong`.

## Key CSS Custom Properties

| Property | Source | Purpose |
|----------|--------|---------|
| `--block-width/height/top/left` | Normalizer | Block positioning |
| `--item-width/height/top/left` | Normalizer | Item positioning (freeplaced) |
| `--page-width/height` | Renderer | Full page dimensions |
| `--margin-top/right/bottom/left` | Renderer | Page margins |
| `--grid-column-count/gap` | Renderer | Column grid |
| `--title-font-size` | Adjustments | Dynamic title sizing |
| `--font-size`, `--line-height` | Adjustments | On `.title` div directly |
| `--text-horizontal/vertical-offset` | Item data | Text position offsets |
| `--object-position-x/y` | AOI / adjustments | Image focus point |
| `--object-background-size` | Adjustments | Image sizing (default: `cover`) |
| `--image-width/height` | Adjustments | Fixed image dimensions |
| Modifier `--` keys | Item modifiers | Gradient colors, custom values |

## Layout Types

Blocks use one of four layout modes, determined by the group schema's `layout` field:

| Layout | CSS | Behavior |
|--------|-----|----------|
| `single` | Block dimensions inherited | One item fills the block |
| `row` | `display: flex; flex-direction: row` | Items share width equally. `item--text-only` and `item--fixed-width` get `flex-grow: 0` |
| `column` | `display: flex; flex-direction: column` | Items share height equally. `item--text-only` and `item--fixed-height` get `flex-grow: 0` |
| `box` | Items `position: absolute` | Each item positioned independently via CSS variables |

## Print-Specific Requirements

- **CMYK colors**: Define RGB for screen, CMYK for print via `@media print`
- **Font embedding**: Use `-ro-font-embedding-type: all` in `@font-face`
- **Image quality**: Set `-ro-image-resampling: 220dpi` and `-ro-image-recompression: jpeg(85%)`. Disable for PNGs with `.image-content[style*='.png']`.
- **Overprint**: Content area enables CMYK overprint by default. Disable on elements with non-black text over images (`-ro-pdf-overprint: none`).
- **Page size**: Handled by inline `<style>` from the renderer. Do not set `@page` in theme CSS.
- **Bleed**: Configured in the print front page format, not in CSS.
- **Logos**: Use SVG for screen and PDF for print, switching via `@media print` on a CSS custom property.

## Available Mixins

### `text-affinity()`

Position `.text` container based on `item--text-pos-*` modifier. Generates rules for six positions: `top-left`, `bottom-left`, `top-center`, `bottom-center`, `top-right`, `bottom-right`. Uses `--text-vertical-offset` and `--text-horizontal-offset` CSS variables.

### `image-gradient()`

Add directional gradient overlay that adapts to text position. Reads from `--gradient-start`, `--gradient-end`, and `--gradient-size` CSS variables. Direction adapts automatically based on text position.

Requires modifiers in the item schema:

```json
{
  "gradient": { "type": "string", "enum": ["vertical", "horizontal"] },
  "gradient-size": { "type": "string", "enum": ["25", "50", "75", "100"] }
}
```

### `cmyk($name, $c, $m, $y, $k)`

Convenience shortcut for declaring a CSS custom property with approximated RGB for screen and CMYK for print. Use only when exact RGB values are not available — explicit `@media print` blocks with known RGB and CMYK values produce more accurate results.

```scss
@include cmyk(--color-brand, 100%, 50%, 0%, 25%);
```
