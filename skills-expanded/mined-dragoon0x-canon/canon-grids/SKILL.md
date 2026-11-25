---
name: canon-grids
description: Use when designing or implementing CSS Grid or Flexbox layouts, choosing between the two, building responsive grids, dashboard layouts, or card grids. Covers the 1D vs 2D decision, grid template areas, auto-fill vs auto-fit, subgrid, and alignment. Trigger when the user mentions grid, CSS grid, flexbox, layout grid, columns, or responsive grid.
---

# CANON · Grids

Grid is for 2D layout (rows AND columns). Flexbox is for 1D layout (row OR column). Pick the right tool and the layout writes itself.

## Grid vs Flexbox decision

| Use Grid when | Use Flexbox when |
|---|---|
| Layout has rows AND columns | Layout is a single row or single column |
| You need items to align both axes | You need items to distribute along one axis |
| Complex page layout | Navbar, toolbar, button group |
| Card grids with equal-height rows | Inline icon + text alignment |
| Dashboard with mixed-size tiles | Centering something |

Using Grid for a toolbar or Flexbox for a 3×4 card grid is possible but harder than necessary.

## Grid template patterns

### Equal columns (auto-responsive)
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}
```

### Fixed sidebar + fluid content
```css
.layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  grid-template-areas: "sidebar main";
}
```

### Dashboard with mixed sizes
```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.widget-large { grid-column: span 2; grid-row: span 2; }
.widget-wide { grid-column: span 2; }
```

## auto-fill vs auto-fit

| Keyword | Behavior |
|---|---|
| `auto-fill` | Creates as many columns as fit. Empty tracks remain (keeps grid structure). |
| `auto-fit` | Creates as many columns as fit. Empty tracks collapse (items stretch). |

Use `auto-fill` when you want consistent column count. Use `auto-fit` when you want items to stretch to fill available space.

## Gap

Use `gap` (not margin hacks). Follow `canon-spatial` spacing scale.

| Context | Gap |
|---|---|
| Dense dashboard | 12–16px |
| Card grid | 16–24px |
| Marketing sections | 24–40px |
| Sidebar + content | 24–32px |

## Alignment

```css
/* Align all items in the grid */
.grid { align-items: start; justify-items: center; }

/* Align one item */
.item { align-self: end; justify-self: stretch; }

/* Distribute space */
.grid { justify-content: space-between; align-content: start; }
```

## Subgrid

When a child grid should inherit the parent's column/row tracks:

```css
.parent { display: grid; grid-template-columns: 1fr 2fr 1fr; }
.child { display: grid; grid-template-columns: subgrid; grid-column: 1 / -1; }
```

Supported in modern browsers. Use for: card internals aligning with the parent grid, table-like alignment across card rows.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Flexbox for a 2D card grid | Heights don't align across rows |
| Grid for centering a single element | Overkill — flexbox in 2 lines |
| Margin-based spacing instead of `gap` | Inconsistent, double margins at edges |
| Fixed px column widths without fluid fallback | Breaks on resize |
| `float` for layout in 2024+ | Deprecated pattern, hack |

## Audit checklist

- [ ] Grid used for 2D layouts, Flexbox for 1D
- [ ] Spacing uses `gap`, not margin hacks
- [ ] Gap values from `canon-spatial` scale
- [ ] Responsive grid uses `auto-fill`/`auto-fit` with `minmax()`
- [ ] No `float`-based layouts
- [ ] Equal-height rows in card grids
- [ ] Sidebar layouts use grid-template-columns

## Sources

- MDN · CSS Grid Layout, Flexbox
- Rachel Andrew · "Grid by Example"
- `canon-spatial` for spacing values
- `canon-responsive` for breakpoint strategy
