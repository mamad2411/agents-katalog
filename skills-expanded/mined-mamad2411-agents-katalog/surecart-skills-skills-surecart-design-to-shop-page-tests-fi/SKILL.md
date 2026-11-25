# Expected emitted prompt (golden)

Given `answers.json` in this directory, the shop-page intake-mode emission should produce the message below.

---

## Closing message (plain prose, above the fenced block)

> I've prepared a Claude Design prompt for your shop page based on your answers. Copy everything in the fenced block below and paste it into [design.claude.com](https://design.claude.com). Once Claude Design produces your export, come back here and paste/attach it — I'll convert it to paste-ready Gutenberg markup.
>
> The prompt asks Claude Design to render ONE canonical product card (not the full grid populated with sample products). If Claude Design tries to render multiple varied cards, that's fine — the converter takes card #1 as the template and discards the rest as visual padding.

## Populated prompt (inside fenced ```md block)

````md
# SureCart Shop Page — Design Brief

## §0. Role + non-negotiable framing

(verbatim from prompt-template.md §0)

## §1. Output contract

(verbatim from prompt-template.md §1)

## §2. Visual vocabulary you may use

(verbatim from prompt-template.md §2)

## §2b. Block-style variations

(verbatim from prompt-template.md §2b)

## §3. Render surfaces (three surfaces)

(verbatim from prompt-template.md §3 — including the placement rule and one-canonical-card rule)

## §4. Style tokens (CSS variables, not raw hex)

```css
:root {
  --sc-accent: var(--wp--preset--color--surecart-brand);
  --sc-text:   var(--wp--preset--color--surecart-text);
  --sc-bg:     var(--wp--preset--color--surecart-bg);
  --sc-display: var(--wp--preset--font-family--surecart-display);
  --sc-body:    var(--wp--preset--font-family--surecart-body);
}
```

Raw `#RRGGBB` is reserved for non-color literals only. The accent resolves to **`surecart-brand`** (`#01824C` — visual reference only).

## §5. Reference design — visual anchor

Use this structural shape as your starting point (paste-tested **aurora-lamp**):

```jsx
{/* SURFACE: PAGE-CHROME */}
<StickyHeader> :: brand-mark + nav + <CartIcon/> </StickyHeader>
<CollectionHero> :: title + subtitle + decorative imagery </CollectionHero>
{/* /SURFACE: PAGE-CHROME */}

{/* SURFACE: FILTER-CHROME */}
<Sort/> <Search/> <FilterTags/>
{/* /SURFACE: FILTER-CHROME */}

{/* SURFACE: PRODUCT-GRID */}
<Grid cols="3">
  <Card>     {/* canonical — render 2-6 visually identical padding cards if needed */}
    <ProductCover useFeaturedImage/>
    <ProductTitle/>
    <ReviewStars/>
    <ProductPrice/>
  </Card>
</Grid>
<NumberedPagination/>
<NoProductsFallback/>
{/* /SURFACE: PRODUCT-GRID */}

{/* SURFACE: PAGE-CHROME */}
<DarkFooter>...</DarkFooter>
{/* /SURFACE: PAGE-CHROME */}
```

## §6. Merchant brief

- **Catalog type:** Physical goods.
- **Grid layout:** 3-up grid.
- **Filter UI:** Tag chips.
- **Card content:** Rating stars (review summary), Numbered pagination.
- **Accent color:** SureCart default (sage green) (preset: `surecart-brand`).
- **Visual reference:** `aurora-lamp`.

Photography, copy tone, product specifics: invent placeholders consistent with the catalog type. Product titles, prices, ratings on cards are server-rendered — use the placeholder components from §2.

## §7. Hard prohibitions

(verbatim from prompt-template.md §7 — 10 rules with constraint-family tags)

## §7b. Extended alias map

(verbatim from prompt-template.md §7b — 13-row map)

## §8. Self-check (advisory only)

(verbatim from prompt-template.md §8)
````

---

## Slot substitution table (for this fixture)

| Slot | Resolved value |
| --- | --- |
| `SQ1_CATALOG_TYPE` | Physical goods |
| `SQ2_ACCENT_DESCRIPTION` | SureCart default (sage green) |
| `ACCENT_PRESET_SLUG` | `surecart-brand` |
| `ACCENT_RESOLVED_HEX` | `#01824C` |
| `SQ3_GRID_LAYOUT` | 3-up grid |
| `GRID_COLS` | 3 |
| `SQ4_FILTER_UI` | Tag chips |
| `FILTER_BLOCKS` | `<Sort/> <Search/> <FilterTags/>` |
| `SQ5_CARD_CONTENT` | Rating stars (review summary), Numbered pagination |
| `CARD_INNER_BLOCKS` | `<ProductTitle/>\n<ReviewStars/>\n<ProductPrice/>` (rating stars included; pagination is page-level, not card-level) |
| `PAGINATION_BLOCK` | `<NumberedPagination/>` |
| `EXEMPLAR_HANDLE` | aurora-lamp |

## Verification

Same harness as the master skill's intake fixtures. Renderer output should match this golden byte-for-byte (after stripping comments-around-the-fenced-block).
