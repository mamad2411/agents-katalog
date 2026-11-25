---
name: canon-cards
description: Use when designing, auditing, or refactoring card components, card grids, item tiles, product cards, or any bounded content container. Covers when a card is appropriate, internal layout, padding, shadows vs borders, interactive cards, hover states, image ratios, content hierarchy, and card grid spacing. Trigger when the user mentions card, tile, item, product card, grid, or thumbnail.
---

# CANON · Cards

Cards group related content into a single, visually distinct unit. Overused, they turn any page into a scrapbook.

## When a card is appropriate

| Use a card | Don't use a card |
|---|---|
| Item has media + title + description + actions | Item is a single line of text |
| Users scan a grid of similar items | Items flow as prose or a list |
| Each item needs its own actions | One shared action applies to many items |
| Content is self-contained | Content connects narratively to siblings |

If the "card" has no border, no shadow, and no background — it's just a layout block. Don't call it a card.

## Card structure

```html
<article class="card">
  <a href="/products/123" class="card-media">
    <img src="..." alt="" width="400" height="300">
  </a>
  <div class="card-body">
    <h3 class="card-title"><a href="/products/123">ThinkPad X1 Carbon</a></h3>
    <p class="card-desc">14" · 16GB RAM · 512GB</p>
    <div class="card-meta">$1,499</div>
  </div>
  <div class="card-actions">
    <button>Add to cart</button>
  </div>
</article>
```

- `<article>` when the card represents a standalone piece of content.
- Otherwise `<div>` or `<li>` (inside a grid).
- Avoid wrapping the whole card in a single `<a>` — it makes interactive children inaccessible.

## Padding

| Card size | Padding |
|---|---|
| Compact (128–200px tall) | 12px |
| **Default** (200–320px) | 16–20px |
| Large (320px+) | 24px |
| Dense (dashboard stat card) | 16px |

Padding stays consistent across all sides. Don't lopside it unless there's a media bleed.

## Media + content — the bleed rule

Cards with images usually bleed the image edge-to-edge, content gets padding. This reads as polished.

```
┌─────────────────────┐
│                     │  ← image bleeds
│      [image]        │
│                     │
├─────────────────────┤
│ 16px padding        │
│ Title               │  ← content padded
│ Description         │
│ $49                 │
│ 16px padding        │
└─────────────────────┘
```

## Shadows vs borders — pick one, not both

| Style | Feel | Use |
|---|---|---|
| Border only | Flat, editorial | Content-heavy grids, dashboards |
| Shadow only | Layered, elevated | E-commerce, interactive cards |
| Border + subtle shadow | Engineered, dense | Data cards in dense UIs |
| Nothing (background fill only) | Minimal | Dense grids on tinted canvas |

Strong shadow + strong border is always wrong — two treatments fighting.

Shadow spec (elevation 1, resting cards):
```css
box-shadow:
  0 1px 2px rgb(0 0 0 / 0.04),
  0 2px 6px rgb(0 0 0 / 0.04);
```

Hover elevation (interactive cards only):
```css
box-shadow:
  0 2px 4px rgb(0 0 0 / 0.05),
  0 8px 20px rgb(0 0 0 / 0.08);
transform: translateY(-1px);
transition: transform 150ms ease-out, box-shadow 150ms ease-out;
```

## Interactive cards

A card is "interactive" if clicking anywhere on it triggers an action.

Rules:
- Add `cursor: pointer` to the card.
- Real focus target must be a `<a>` or `<button>` inside — not the card wrapper.
- Use CSS to stretch the real anchor across the card:
  ```css
  .card { position: relative; }
  .card-title a::after {
    content: '';
    position: absolute;
    inset: 0;
  }
  ```
- Interactive children (secondary buttons) need `position: relative; z-index: 1` to stay clickable above the stretched link.
- Hover state on the whole card indicates interactivity.
- Focus ring wraps the card, not just the title link, when that anchor is stretched.

## Image ratios

Pick one ratio per card grid. Never mix 16:9 and 4:3 cards in the same grid — breaks alignment.

| Ratio | Use |
|---|---|
| 1:1 | Profile cards, products where shape varies |
| 4:3 | Editorial, photography |
| 16:9 | Video thumbnails, hero content |
| 3:4 | Books, portrait products |
| 2:1 | Landscape banners |

Always declare width and height attributes on `<img>` to prevent CLS (canon-performance).

## Card grids — spacing

| Grid | Gap |
|---|---|
| Dense dashboard cards | 12–16px |
| **Default content cards** | 16–24px |
| Marketing, hero content | 24–40px |

Don't mix gaps in a single grid. Column gap usually matches row gap; slight row-larger is OK for information-heavy cards.

## Hierarchy inside a card

Readers scan cards in Z-pattern (on wide cards) or F-pattern (on tall cards). Put the identifying info first.

```
Title (primary)          ← bold, 16–20px
Metadata (secondary)     ← muted, 13–14px
Description (optional)   ← body, 14px
Actions / price          ← bottom-anchored
```

Keep to **4 hierarchical levels max** per card. More and each level loses meaning.

## Content truncation

- Titles: 1–2 lines max, then ellipsis.
- Descriptions: 2–3 lines, then ellipsis.
- Use `-webkit-line-clamp` for multi-line clamp.
- Keep card heights **equal** in a grid — `align-items: stretch`, not content-driven.

## Loading skeletons

Skeleton shape matches the card.

```
┌──────────────────┐
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒  │  ← image skeleton (same ratio)
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒  │
├──────────────────┤
│ ▒▒▒▒▒▒▒▒         │  ← title skeleton
│ ▒▒▒▒             │  ← meta skeleton
│ ▒▒▒▒▒▒▒▒▒▒       │
└──────────────────┘
```

Shimmer 1000–1500ms. Contrast 1.2:1.5:1 between skeleton and background (canon-states).

## Empty cards — skip

If a card has no data, don't render it. An empty card with a placeholder "No data" is always worse than one fewer card.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Wrapping the whole card in `<a>` | Interactive children become inaccessible |
| Border + heavy shadow | Two treatments fighting |
| Mixed image ratios in one grid | Breaks alignment, looks sloppy |
| 5+ hierarchical levels | Nothing is primary |
| Padding different on top vs bottom | Imbalanced, amateurish |
| Hover that resizes the card | Layout shift, pointer slips off |
| Cards of different heights in a grid | Ragged bottom edge |
| Hidden actions revealed only on hover | Broken on touch |
| Card click target < 44px on mobile | Hit target fail |
| Absolute-positioning for stretched link but forgetting `z-index` on secondary buttons | Secondary buttons stop working |
| Text clamped without full-text access | Users can't read truncated content |

## Decision tree

```
Does each item have rich, varied content (image + title + description + actions)?
  ├─ No → Use a list or table
  └─ Yes → Card is appropriate

Interactive (click anywhere on card)?
  ├─ No → Static card, individual buttons inside
  └─ Yes → Stretched-link pattern, hover state on card

Grid layout?
  ├─ Yes → Equal heights, one ratio, consistent gap
  └─ No → Single card or list of cards

Dense UI (dashboard)?
  ├─ Yes → Border + flat, 12–16px padding
  └─ No → Shadow, 16–20px padding
```

## Audit checklist

- [ ] Card uses `<article>` or appropriate semantic wrapper
- [ ] Not wrapping the entire card in a single `<a>`
- [ ] Border OR shadow, not both strong
- [ ] Image ratio consistent across grid
- [ ] Image has `width` and `height` attributes
- [ ] Padding consistent on all sides
- [ ] Grid items equal height
- [ ] Interactive cards use stretched-link pattern with z-index on children
- [ ] Hover state doesn't resize
- [ ] Mobile hit target ≥ 44px
- [ ] ≤ 4 levels of hierarchy inside the card
- [ ] Skeleton loading matches card shape
- [ ] Truncated text has full-text access (tooltip or detail page)

## Sources

- WCAG 2.2 · 2.5.5 Target Size, 2.4.7 Focus Visible, 1.4.10 Reflow
- Refactoring UI · "Depth is more than blur", "Use shadows to communicate elevation"
- Apple HIG · Collections, Lists and Tables
- Material Design 3 · Cards
- Adam Silver · "Design for real content" (truncation guidance)
