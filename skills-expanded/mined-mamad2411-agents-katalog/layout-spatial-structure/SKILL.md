---
name: layout-spatial-structure
description: This skill should be used when the user is building or reviewing page layouts, grid systems, column structures, card grids, sidebar layouts, CSS Grid or Flexbox decisions, element alignment, spatial composition, or responsive grid strategies. Covers the 12-column grid, 8-point spacing system, Gestalt proximity principle, visual weight distribution, and layout patterns from Material Design and Bootstrap.
version: 1.0.0
---

# The Grid Is the Architecture — Everything Else Is Decoration

Every professional layout is built on a grid. The grid is not a suggestion — it is the structural skeleton that makes alignment effortless, spacing predictable, and responsive behavior automatic. Material Design, Bootstrap, and every major design system converge on the same fundamentals: a 12-column grid with an 8-point spacing system.

## 12-Column Grid Anatomy

| Component | Purpose | Typical Value |
|-----------|---------|---------------|
| **Columns** | Content containers; 12 divides evenly by 2, 3, 4, 6 | 12 columns |
| **Gutters** | Space between columns; consistent rhythm | 16px–32px (24px default) |
| **Margins** | Outer breathing room on left/right edges | 16px mobile, 24px tablet, auto-center desktop |
| **Container** | Max-width wrapper preventing ultra-wide lines | 1200px–1440px |

**Grid adherence rule:** >90% of element edges must align to grid lines. Audit by overlaying a 12-column grid on any screen — misaligned elements are immediately visible.

## CSS Grid vs Flexbox Decision Table

| Use Case | Choose | Reason |
|----------|--------|--------|
| Page-level layout (header, sidebar, main, footer) | **CSS Grid** | Two-dimensional control over rows and columns |
| Card grids with uniform items | **CSS Grid** | `auto-fit`/`auto-fill` with `minmax()` handles responsiveness |
| Navigation bars, button groups | **Flexbox** | One-dimensional alignment with wrapping |
| Centering a single element | **Flexbox** | `justify-content` + `align-items` in three lines |
| Overlapping elements or complex placement | **CSS Grid** | Named grid areas and explicit row/column placement |
| Unknown number of items in a row | **Flexbox** | `flex-wrap` distributes naturally |

**Default rule:** Start with CSS Grid for layout, drop to Flexbox for component-level alignment.

## Spacing System

Use the constrained 4px/8px spacing scale defined in the `whitespace-density` skill. All grid gutters, margins, and padding must come from that scale. Never use arbitrary spacing values.

## Gestalt Proximity in Layouts

Apply the Gestalt proximity rule (see `whitespace-density` skill for the full ≤50% rule and spacing tokens) to all layout decisions. Internal spacing within a grid region must be visibly tighter than spacing between regions.

## Card Layout Patterns

Use CSS Grid `auto-fit` with `minmax()` for responsive card grids (see `responsive-design` skill for fluid grid techniques).

**Minimum card width:** 280px for content cards, 200px for thumbnail cards. Set `gap` using the spacing scale.

## Scanning Patterns

Place layout regions to support natural eye scanning. See the `visual-hierarchy` skill for F-pattern and Z-pattern rules — layout determines *where* regions go, hierarchy determines *what draws attention* within them.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Random widths (347px, 513px) | No grid alignment; looks accidental | Snap to column spans or percentages |
| Mixing grid systems (12-col + 10-col) | Conflicting rhythms; nothing aligns | One grid system per project |
| Equal internal and external spacing | Groups are indistinguishable; flat hierarchy | Apply Gestalt proximity rule (see `whitespace-density` skill) |
| Hardcoded pixel widths on responsive layouts | Breaks on every viewport | Use `fr`, `%`, `minmax()`, or container queries |
| Nesting grids more than 2 levels deep | Compounding gutters create unpredictable spacing | Flatten structure; use subgrid |

## Cross-Media Notes

- **Presentations:** Establish slide margins (10% of slide width). Align all text and images to a 2-column or 3-column invisible grid. Consistent placement across slides creates professionalism.
- **CVs/Resumes:** Use a clear 2-column layout (sidebar + main) or single-column with consistent left alignment. Section spacing should follow the proximity rule — related items grouped tightly.
- **Dashboards:** Use a 12-column grid with card-based widgets. Each widget snaps to column spans (3, 4, 6, or 12 columns). Maintain consistent gutter width.

## Examples

Working implementations in `examples/`:
- **`examples/grid-and-card-layout.md`** — Complete 12-column grid setup, responsive card grid with CSS Grid auto-fit, Tailwind configuration, and React component

## Review Checklist

When reviewing or building layouts:

- [ ] Page uses a 12-column grid (or documented alternative) with consistent gutters
- [ ] Container has a max-width (1200px–1440px) and is centered
- [ ] All spacing values come from the spacing scale (see `whitespace-density` skill)
- [ ] CSS Grid used for page layout; Flexbox used for component-level alignment
- [ ] Card grids use `auto-fit`/`auto-fill` with `minmax()` for responsive reflow
- [ ] >90% of element edges align to grid lines
- [ ] Gestalt proximity rule applied (see `whitespace-density` skill)
- [ ] No hardcoded pixel widths on elements that must be responsive
- [ ] Mobile layouts collapse to single column with maintained spacing scale
