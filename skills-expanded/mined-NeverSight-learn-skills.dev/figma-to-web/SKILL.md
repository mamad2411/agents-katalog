---
name: figma-to-web
description: Pixel-perfect Figma design to web code restoration workflow. Use this skill whenever the user asks to implement a UI from a Figma design, reproduce a design, do UI restoration (UI还原), compare a page with a Figma mockup, or fix visual differences between implementation and design. Also trigger when the user provides a Figma URL and asks to build it, or when they mention "design spec", "pixel perfect", "match the design", or similar phrases. This skill orchestrates Playwright MCP, Figma MCP, and Chrome DevTools MCP for systematic comparison and iteration.
---

# Figma-to-Web: Pixel-Perfect UI Restoration

A systematic workflow for translating Figma designs into web code with pixel-level accuracy. This skill enforces a strict compare-and-iterate loop so nothing is missed.

## Prerequisites

The following MCP servers must be available:
- **Playwright MCP** — browser automation and screenshots
- **Figma MCP** (`figma-ai-bridge`) — design data and image export
- **Chrome DevTools MCP** — runtime style/layout inspection

## Core Workflow

Execute these phases **in order**. Do not skip steps.

### Phase 1: Gather Design Data

1. **Parse the Figma URL** — extract `fileKey` and `nodeId` from the URL.
   - URL format: `figma.com/design/<fileKey>/...?node-id=<nodeId>`
   - Convert `node-id` URL param format (e.g. `34-4675`) to API format (e.g. `34:4675`)

2. **Fetch Figma node tree** — call `get_figma_data` with appropriate depth (start with 3, increase if needed).
   - Record: component hierarchy, text content, key style tokens
   - Pay attention to `globalVars.styles` — these contain exact colors, fonts, spacing, border-radius, layout modes

3. **Export Figma screenshot** — call `download_figma_images` for the target node as PNG.
   - Note: exported PNGs are 2x by default. Actual pt size = px / 2.
   - For icons/vectors, also export as SVG when needed.

4. **Extract key design tokens** from the Figma data:
   - Font family, weight, size, line-height, text-case
   - Colors (fill, stroke) — note rgba vs hex
   - Spacing (padding, gap, margin) from layout data
   - Border radius, border width/color
   - Component dimensions (width, height)

### Phase 2: Implement

5. **Write the component code** based on the extracted design tokens.
   - Map Figma styles to Tailwind classes or CSS values
   - Use exact color values from the design (e.g. `#03B2BD`, not approximations)
   - Use exact font sizes and weights
   - Use exact spacing values
   - For SVG icons, use the exported SVG paths directly from Figma

6. **Common Figma-to-Tailwind mappings** — refer to `references/style-mapping.md` for detailed conversion rules.

### Phase 3: Screenshot & Compare

7. **Take a page screenshot** — use Playwright MCP `browser_take_screenshot` with `fullPage: true`.

8. **Visual comparison** — place the Figma export and page screenshot side by side. Systematically check:

   | Check Area | What to Compare |
   |---|---|
   | **Layout** | Element positions, alignment, spacing between elements |
   | **Typography** | Font size, weight, line-height, letter-spacing, text color, text-transform |
   | **Colors** | Background, text, border, icon fill/stroke colors |
   | **Spacing** | Padding, margin, gap between elements |
   | **Borders** | Radius, width, color, style |
   | **Icons/Images** | Size, color, position, correct icon shape |
   | **Buttons/CTAs** | Height, padding, border-radius, text style, background |
   | **Responsive** | Check at design's intended viewport width |

9. **List all differences** — create a numbered list of every discrepancy found, no matter how small.

### Phase 4: Inspect & Diagnose

10. **Use Chrome DevTools MCP** when the visual comparison reveals differences that need deeper investigation:
    - `take_screenshot` — get current rendered state
    - `evaluate_script` — query computed styles on specific elements
    - Check for inherited styles, specificity issues, or framework overrides

### Phase 5: Fix & Iterate

11. **Fix each difference** from the list created in step 9.
    - Make targeted edits — change only what's needed
    - After fixing, take a new screenshot and re-compare

12. **Repeat phases 3-5** until no visible differences remain or the user confirms it's acceptable.

## Important Rules

- **Never guess colors** — always use the exact hex/rgba values from Figma data
- **Never approximate spacing** — use the exact pixel values from the design
- **Check icon details** — SVG viewBox, fill vs stroke, correct path data
- **Font rendering** — web fonts may render slightly differently; focus on size/weight/color accuracy
- **State variations** — if the design shows multiple states (hover, active, disabled, different data states), implement all of them
- **Responsive behavior** — check if the Figma file has multiple frame sizes; implement responsive breakpoints accordingly

## Figma Data Interpretation Tips

- `layout.mode: "row"` → `flex` with `flex-direction: row`
- `layout.mode: "column"` → `flex` with `flex-direction: column`
- `layout.gap` → `gap` in CSS
- `layout.padding` → CSS padding (format: "top right bottom left")
- `sizing.horizontal: "hug"` → `width: fit-content` / Tailwind `w-fit`
- `sizing.horizontal: "fill"` → `width: 100%` / Tailwind `w-full` or `flex-1`
- `sizing.horizontal: "fixed"` → use `dimensions.width`
- `textStyle.textCase: "TITLE"` → `text-transform: capitalize`
- `textStyle.textCase: "UPPER"` → `text-transform: uppercase`
- `fills` reference style IDs in `globalVars.styles` — look up the actual color values there
- `borderRadius: "100px"` on buttons → Tailwind `rounded-full`

## When Design Data is Ambiguous

If Figma node tree doesn't provide enough detail:
1. Increase `depth` parameter in `get_figma_data`
2. Export sub-components as separate images for closer inspection
3. Ask the user for clarification on interactive behaviors not visible in static designs

## Output Checklist

Before declaring the restoration complete, verify:
- [ ] All text content matches the design
- [ ] All colors are exact matches (use DevTools color picker to verify)
- [ ] Spacing and alignment match within 1-2px tolerance
- [ ] Icons are correct shape, size, and color
- [ ] Border radius values match
- [ ] Font sizes and weights match
- [ ] Layout structure (flex directions, alignments) matches
- [ ] Button/CTA styles match (height, padding, border-radius, colors)
