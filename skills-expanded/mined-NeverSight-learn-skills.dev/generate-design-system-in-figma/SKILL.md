---
name: generate-design-system-in-figma
description: >-
  Builds a complete, production-grade design system in Figma using the remote
  Figma MCP server. Creates Color Styles, Text Styles, Effect Styles, Number
  Variables, and all 14 components (Accordion, Button, Callout, Card, Dropdown,
  Checkbox, Chip, Input, Tabs, Navigation, Radio Button, Tile, Tooltip, Toggle)
  with full variant/state coverage. Use when the user asks to create, build, or
  set up a design system in Figma, or mentions tokens, components, or a Figma
  library.
when_to_use: >-
  Trigger on: "create design system in Figma", "build Figma library", "set up
  tokens in Figma", "add components to Figma", "build the design system",
  "create color styles", "create text styles", or any combination of Figma +
  design system work.
disable-model-invocation: false
---

# Figma Design System Builder

This skill orchestrates building a complete design system in Figma using the **remote Figma MCP server** (`https://mcp.figma.com/mcp`). It defines WHAT to build and in what order. The `figma-use` and `figma-generate-library` skills (from the Figma plugin) govern HOW to call the Plugin API.

## Prerequisites — Load These First

Before ANY `use_figma` call:
1. Load the `figma-use` skill — Plugin API rules (return pattern, colors, fonts, page switching)
2. Load the `figma-generate-library` skill — Phase workflow, state management, naming conventions

The full design system specification lives in [design-system-spec.md](references/design-system-spec.md). Load it during Phase 0 discovery.

---

## MCP Server

This skill requires the **Figma remote MCP server**. Confirm it is connected before starting:
- Server URL: `https://mcp.figma.com/mcp`
- The user must authenticate via Figma's OAuth flow in their MCP client (Cursor: connect via Settings → MCP)
- Available tools via MCP: `use_figma`, `get_figma_data`, `get_metadata`, `get_screenshot`, `search_design_system`

If not connected, direct the user to: https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/

---

## Build Order (Critical — Never Deviate)

```
Phase 0 — DISCOVERY (no writes yet)
  0a. Read design-system-spec.md fully (including Sections 5 + 6)
  0b. Inspect target Figma file: pages, existing styles, variables, components
  0c. Search subscribed libraries (search_design_system) for reusable assets
  0d. Domain discovery: ask the user about their product type, core user
      flows, and any specific components they need beyond the base 14.
      Propose domain-specific components (justified by real user flows).
  0e. Lock scope: confirm exact token set + base 14 + domain-specific
      component list with user
  ✋ CHECKPOINT: Present full plan, await explicit approval

Phase 1 — FOUNDATIONS: Tokens & Styles
  1a. Color Styles (Color Palette — NOT variables)
      → Shades → Neutrals → Primary → Gradients → Error → Accents
  1b. Number Variables (Spacing + Container Dimensions)
      Collection "Spacing": 2xs, xs, sm, md, lg, xl, 2xl, 3xl, 4xl
      Collection "Dimensions": max-content-width, breakpoints, border-radius scale
  1c. Text Styles (Typography)
      → Header R/B → Body Large R/U/B → Body Medium R/U/B →
        Body Small R/B → Body XSmall R/B → Body XXSmall R/U/B → Micro R
  1d. Effect Styles (Elevation)
      → Level 0 (none) → Level 1 → Level 2 → Level 3 → Level 4
  → Validate: all styles/variables created, scopes set, code syntax set
  ✋ CHECKPOINT: Show token summary, await approval

Phase 2 — FILE STRUCTURE
  2a. Page skeleton: Cover → Getting Started → Foundations → --- → Components → --- → Utilities
  2b. Foundations docs: color swatches, type specimens, spacing scale bars, elevation demo
  ✋ CHECKPOINT: Show page list + screenshot

Phase 3 — COMPONENTS (one at a time, dependency order)
  Build order (atoms → molecules → organisms):
  1.  Radio Button     (atom — no deps)
  2.  Checkbox         (atom — no deps)
  3.  Toggle           (atom — no deps)
  4.  Chip             (atom — no deps)
  5.  Tooltip          (atom — no deps)
  6.  Button           (atom — no deps)
  7.  Input            (atom — no deps)
  8.  Dropdown         (uses Input + Chip)
  9.  Tabs             (uses Button/typography)
  10. Accordion        (uses Typography + Dividers)
  11. Tile             (uses Icon + Typography)
  12. Callout          (uses Typography + Icons)
  13. Card             (uses Button + Input + Callout + Chip)
  14. Navigation       (uses Button + Input + Avatar)

  15+. Domain-specific components (identified in Phase 0d)
       Built in dependency order — components with fewer base-component
       dependencies first. Must compose base components via instance swap,
       not rebuild internals.

  Per component (base and domain-specific):
    3a. Create dedicated page
    3b. Load heroicons-svg-reference.md, create needed icon components
        for this component (see Section 7 of design-system-spec.md for
        which icons each component requires)
    3c. Build base component with auto-layout + variable bindings (spacing, color, radius)
    3d. Create all variant combinations via combineAsVariants, grid-layout result
    3e. Add component properties (TEXT, BOOLEAN, INSTANCE_SWAP)
    3f. VISUAL VERIFICATION LOOP (mandatory, max 3 iterations):
        i.   Take screenshot of the component (get_screenshot)
        ii.  Analyze the screenshot for visual defects:
             - Are all icons visible and rendered as vectors (not blank, not Unicode text)?
             - Are checked/selected/on states showing their inner indicators
               (checkmark inside checkbox, dot inside radio, check inside toggle thumb)?
             - Is auto-layout producing correct spacing and alignment?
             - Are text labels readable and not clipped or overflowing?
             - Are colors correct (fills, borders, backgrounds)?
             - Does the component look like a real production UI control?
        iii. If defects found → generate a targeted fix script, execute it,
             go back to step (i)
        iv.  If no defects → proceed to checkpoint
        v.   If 3 iterations exhausted and still broken → STOP, report
             defects to user with screenshot, ask for guidance
    3g. Validate structure with get_metadata
    ✋ CHECKPOINT per component — show screenshot, await approval before next

Phase 4 — QA & INTEGRATION
  4a. Accessibility audit (contrast ratios, min touch targets 44×44px)
  4b. Naming audit (no duplicates, consistent casing)
  4c. Unresolved bindings audit (no hardcoded fills/strokes)
  4d. Final screenshots per page
  ✋ CHECKPOINT: Complete sign-off
```

---

## Token Quick Reference

Load [design-system-spec.md](references/design-system-spec.md) for exact definitions. Summary:

### Color Styles (not variables — Styles panel)
| Group | Contents |
|-------|----------|
| Shades | Pure white, pure black, dark/5%, dark/30% |
| Neutrals | 8-step scale, near-white → dark gray |
| Primary | Base + vivid variant |
| Gradients | 3+ stops for button states |
| Error | Light tint (backgrounds) + dark shade (text/icons) |
| Accents | Light tint, dark shade, success color, link color |

### Number Variables
| Collection | Tokens |
|------------|--------|
| Spacing | 2xs · xs · sm · md · lg · xl · 2xl · 3xl · 4xl |
| Dimensions | max-content-width · breakpoint/mobile · breakpoint/tablet · breakpoint/desktop · breakpoint/wide · radius/none · radius/sm · radius/md · radius/lg · radius/full |

### Text Styles
Header (R, B) · Body Large (R, U, B) · Body Medium (R, U, B) · Body Small (R, B) · Body XSmall (R, B) · Body XXSmall (R, U, B) · Micro (R)

### Effect Styles
Elevation 0 → 1 → 2 → 3 → 4 (no shadow → max shadow)

---

## Component Quick Reference

Load [design-system-spec.md](references/design-system-spec.md) for full anatomy, states, and variants. Summary:

| # | Component | Key Variants / States | Required Icons (Heroicons) |
|---|-----------|----------------------|---------------------------|
| 1 | Accordion | Closed · Open | `chevron-down` |
| 2 | Button | Primary · Secondary · Outline · Full-width · Default · Small · Default/Hover/Focused/Active/Loading/Disabled | `arrow-path` (loading) |
| 3 | Callout | Inline status · Bubble | `information-circle`, `exclamation-triangle`, `check-circle`, `tag`, `clock`, `currency-dollar` |
| 4 | Card | Media Card · Compact Media · Action Card · Summary Card | `heart`, `share`, `ellipsis-horizontal`, `chevron-left`, `chevron-right`, `bookmark`, `photo` |
| 5 | Dropdown | No label · With label · With leading icon · Default/Hover/Selected + Open menu | `chevron-down`, `check` |
| 6 | Checkbox | Standalone · With label · With label+description · Unchecked/Checked/Indeterminate · Default/Large | `check` (checked), `minus` (indeterminate) |
| 7 | Chip | Standard · Compact · Default/Hover/Focused/Muted/Selected | `x-mark` (removable) |
| 8 | Input | No label · With label · Floating label · Trailing icon · Textarea · Default/Hover/Focused/Filled/Error/Disabled | `eye`, `eye-slash`, `exclamation-circle`, `magnifying-glass`, `x-circle`, `calendar` |
| 9 | Tabs | Underline (icon+label or label, 2 sizes) · Pill · Default/Hover/Active/Disabled/Selected | `home`, `globe-alt`, `bookmark`, `squares-2x2` |
| 10 | Navigation | Top Navbar · Bottom Bar · Sidebar/Drawer · Breadcrumb · Mega Menu | `bars-3`, `magnifying-glass`, `bell`, `cog-6-tooth`, `user-circle`, `home`, `chevron-right` |
| 11 | Radio Button | Standalone · With label · With label+description · Unselected/Selected/Disabled | _(none — Ellipse node for inner dot)_ |
| 12 | Tile | Standard (icon+label) · Icon-only · Detail (icon+title+desc) · Default/Hover/Focused/Selected | `home`, `cog-6-tooth`, `chart-bar`, `document-text`, `star`, `globe-alt` |
| 13 | Tooltip | Light · Dark · Without title · With title · Arrow: Top/Bottom/Left/Right | `x-mark` |
| 14 | Toggle | Standalone · With label · With label+description · Off/On/Disabled Off/Disabled On | `check` (on-state thumb) |
| 15+ | Domain-specific | Identified during Phase 0d based on product type and user flows. Compose base components. | Per component spec |

---

## Key Rules (Enforced from figma-use / figma-generate-library)

- **Colors 0–1 range**, not 0–255
- **Never `ALL_SCOPES`** — set explicit scopes per variable type
- **Semantic variables alias to primitives** — never duplicate raw values
- **INSTANCE_SWAP for icons**, never a variant per icon
- **Variant matrix ≤ 30** — split sub-component if exceeded
- **Sequential `use_figma` calls** — never parallelize
- **Never hallucinate node IDs** — always read from state ledger
- **State ledger persisted to disk**: `/tmp/dsb-state-{RUN_ID}.json`
- **Validate before proceeding** — `get_metadata` after create, `get_screenshot` after each component
- **Anti-patterns enforced** — Section 6 of design-system-spec.md lists banned patterns (no emojis, no Inter, no #000000, no fabricated data, Heroicons only, etc.). Load and enforce during every phase.
- **All icons MUST be Heroicons SVGs** — created via `figma.createNodeFromSvg()` with actual SVG path data from [heroicons-svg-reference.md](references/heroicons-svg-reference.md). Never use Unicode symbols (`✓`, `▼`, `×`, `☰`, etc.), never use text nodes as icons, never leave blank/empty icon placeholder frames. Every icon slot in every component must contain a visible, correctly rendered Heroicons SVG vector.
- **Visual Verification Loop is mandatory** — after building each component, take a screenshot, analyze it for visual defects (blank icons, misaligned states, missing inner indicators for checked/selected states, clipped text), and fix any issues before proceeding to the user checkpoint. Maximum 3 fix iterations per component.

---

## Heroicons SVG Implementation

Every icon in the design system MUST be a Heroicons SVG vector node — never a Unicode character, never a text node, never a blank frame.

### Mandatory steps for every component that uses icons

1. **Load the reference.** At the start of each component build (step 3b), load [heroicons-svg-reference.md](references/heroicons-svg-reference.md) and identify which icons this component needs from the "Required Icons" column in the Component Quick Reference table above.

2. **Create icon components.** For each needed icon, create it as a Figma `ComponentNode` using the helper function from the reference file. This makes icons available for INSTANCE_SWAP properties.

```javascript
// Example: creating the check icon as a component
const checkSvg = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="1.5" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5"/></svg>`;
const checkComp = createHeroiconComponent(checkSvg, 'check', 24);
```

3. **Embed icons inside components.** Place icon instances or SVG nodes as children of the appropriate frame, centered via auto-layout. For stateful icons (checkbox check, toggle check, radio dot), the icon MUST be a child of the control's box/thumb frame — never floating outside or adjacent to it.

4. **Recolor after import.** SVGs import with black strokes. Use the `recolorIcon()` helper from the reference to change stroke colors (e.g. white for check icons inside filled checkboxes, primary color for active states).

5. **Size proportionally.** Icons inside small controls (checkbox, toggle thumb) should be sized proportionally — typically 12x12 or 16x16 inside 20x20 or 24x24 containers. Full-size icons (navigation, tile, input trailing) remain at 24x24 or 20x20.

### Stateful control icons — critical patterns

| Control | State | What goes INSIDE the control frame |
|---|---|---|
| Checkbox | Checked | White `check` SVG (12-16px), centered inside filled box |
| Checkbox | Indeterminate | White `minus` SVG (12-16px), centered inside filled box |
| Checkbox | Unchecked | Nothing — empty box with border only |
| Radio Button | Selected | Filled Ellipse node (10px), centered inside outer circle |
| Radio Button | Unselected | Nothing — empty circle with border only |
| Toggle | On | White `check` SVG (12px), centered inside thumb circle |
| Toggle | Off | Nothing — plain thumb circle |

---

## Visual Verification Loop (Mandatory)

After each component is built (after step 3e), the following verification loop MUST be executed before presenting the component to the user for approval.

### The loop (max 3 iterations)

```
1. Take screenshot → get_screenshot of the component page/region
2. Analyze the screenshot for these specific defects:
   a. ICONS: Are all icons visible vector shapes? (Not blank frames,
      not Unicode text characters, not invisible/zero-opacity nodes)
   b. STATEFUL CONTROLS: Do checked checkboxes show a checkmark INSIDE
      the box? Do selected radio buttons show a dot INSIDE the circle?
      Do on-state toggles show a check INSIDE the thumb?
   c. LAYOUT: Is auto-layout producing correct spacing? Are elements
      aligned properly? No overlapping nodes?
   d. TEXT: Are labels readable? Not clipped, not overflowing their
      containers? Correct font styles applied?
   e. COLORS: Are fills, borders, and backgrounds using the correct
      color styles? Are hover/active states visually distinct?
   f. OVERALL: Does the component look like a real, production-quality
      UI control that a designer would ship?
3. If defects found:
   → Write a targeted fix script addressing ONLY the broken parts
   → Execute the fix
   → Go back to step 1
4. If no defects found:
   → Proceed to the user checkpoint
5. If 3 iterations exhausted and still broken:
   → STOP
   → Present the screenshot to the user
   → List the remaining defects
   → Ask for guidance before continuing
```

### Common defects to watch for

- Checkbox checked state with no visible checkmark (or checkmark outside the box)
- Radio button selected state with no visible inner dot (or dot outside the circle)
- Toggle on-state with no visible indicator inside the thumb
- Accordion chevron rendered as a Unicode `▼` text node instead of an SVG vector
- Dropdown chevron rendered as text instead of SVG
- Tooltip close button rendered as a text `×` instead of an SVG x-mark
- Card action icons (heart, share) as blank frames with no visible content
- Navigation hamburger icon as three manually drawn lines instead of a `bars-3` SVG
- Any icon slot containing an empty frame with no children

---

## Additional Resources

- Full design system specification: [design-system-spec.md](references/design-system-spec.md)
- Heroicons SVG reference (all icon SVG markup): [heroicons-svg-reference.md](references/heroicons-svg-reference.md)
- Plugin API rules: load `figma-use` skill
- Phase workflow & state management: load `figma-generate-library` skill
- Remote MCP server setup: https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/
