---
name: visual-creative-subagent
description: >-
  Generate one isolated visual/creative concept pass as a self-contained
  browser-renderable showcase using HTML/CSS/JS with domain-appropriate
  libraries. Domains: data-vis (charts/graphs), animation (motion/physics),
  graphic-design (generative art/3D/illustration). Each pass is written
  from scratch by the AI agent, not stamped from a template.
---

# Visual Creative Subagent

Use this skill for one pass only. Do not blend with other pass outputs.

## Inputs (via Task agent prompt)
- `domain` - One of: `data-vis`, `animation`, `graphic-design`
- `styleId` - Style within the domain (e.g., "bar-chart", "particle-systems", "globe-3d")
- `pass` - Pass number
- `outputDir` - Where to write generated files
- `stylePalette` - Colors, fonts, design tokens
- `styleDirection` - Creative brief text
- `libraryDirective` - Which CDN library to use (from library-catalog.json)
- `mockData` - Sample data (for data-vis passes)
- `sceneDescription` - What to render (for animation/graphic-design passes)
- `antiRepeat` - Explicit list of things NOT to repeat from prior passes

## Hard Requirements
1. Generate a self-contained HTML showcase page (not an app with navigation).
2. The visualization/animation/graphic must render immediately on page load.
3. Each pass must be visually distinct from every other pass in the same style.
4. Use plain HTML/CSS/JS with the specified CDN library.
5. Include responsive behavior for desktop and mobile.
6. Write EVERY line of code from scratch — no shared templates.
7. The showcase must be interactive where appropriate (tooltips, controls, hover effects).

## Page Structure
Every pass produces a single showcase page with these regions:

### Header Bar
- Domain badge (e.g., "DATA VIS", "ANIMATION", "GRAPHIC DESIGN")
- Style name and pass number
- Library badge showing which library powers this pass

### Main Showcase Area
- Fills 80%+ of the viewport
- The visualization, animation, or graphic renders here
- Must be responsive — scales/adapts to viewport size

### Controls Panel
- **Data-vis**: Filter dropdowns, sort toggles, dataset switcher
- **Animation**: Play/pause button, speed slider, reset button
- **Graphic-design**: Regenerate/randomize button, parameter sliders

### Info Footer
- Technical details: library name, version, render method (Canvas/SVG/WebGL)
- Data source description (for data-vis)
- Brief technique description

## Domain-Specific Guidelines

### Data Visualization
- Use the provided `mockData` faithfully — do not invent different data
- Chart colors must use `stylePalette`, not library defaults
- Include axis labels, legend, title, and tooltips
- Show at least 2 views of the data (e.g., chart + summary table, or chart + sparklines)
- Animated entrance for chart elements
- Responsive: chart reflows on mobile, labels don't overflow

### Animation
- Animation must loop continuously or play indefinitely
- Use `requestAnimationFrame` or library animation loops
- Target 60fps — no jank or frame drops
- Include visible play/pause controls
- The animation fills the showcase area
- For physics: add click/drag interactivity

### Graphic Design
- Render a complete composition — not a sketch or placeholder
- For generative art: include a "Regenerate" button with new random seed
- For 3D: include orbit controls or auto-rotation
- For illustrations: render at high resolution
- Display the random seed or generation parameters

## Quality Standards
1. **No blank canvas**: Visible content must render immediately on load
2. **Responsive**: Works on desktop (1536px) and mobile (390px)
3. **Performance**: Smooth rendering, no memory leaks, no console errors
4. **Polish**: Professional presentation, consistent spacing, clean typography
5. **Working interactivity**: All controls and hover states must function
6. **Library loaded**: CDN script must load successfully (use valid URLs from catalog)
7. **Palette applied**: Colors must match the provided palette, not library defaults

## Files
- `index.html` - Complete HTML with CDN library tags and showcase structure
- `style.css` - Full CSS with responsive breakpoints
- `app.js` - Library initialization, rendering, interaction logic
- `README.md` - Concept overview, library usage, technique description
- `validation/handoff.json` - Domain/style/library metadata

## Mandatory Workflow: Plan → Generate → Validate → Fix Loop

**The subagent itself (NOT the orchestrator) owns the full validation lifecycle. A pass is not complete until the subagent has validated and visually reviewed its own output.**

### Phase 1: Plan
- Review all inputs (domain, style, palette, brief, library directive, anti-repeat)
- Read the library-catalog.json for correct CDN URLs
- Plan design approach

### Phase 2: Pre-validate CDN URLs
Before writing HTML, verify every CDN URL resolves:
```bash
curl -s -o /dev/null -w "%{http_code}" "<CDN_URL>"
```
- Non-200 → find alternative URL/version from catalog or CDN provider
- Check `note` fields in library-catalog.json for version-specific issues (e.g., UMD vs ESM)

### Phase 3: Generate
- Write all files with verified CDN URLs only

### Phase 4: Validate (Playwright)
The **subagent** runs the Playwright validation script (not the orchestrator):
```bash
node .claude/skills/visual-creative-subagent/scripts/validate-visuals-playwright.mjs --pass-dir <outputDir>
```

### Phase 5: Review Screenshots
The **subagent** reads the generated PNG screenshots and visually assesses them. Failure conditions:
- Blank/black canvas (library load failure or JS error)
- Missing primary content (visualization/animation/graphic not visible)
- Text unreadable (poor contrast, wrong font, overlap)
- Layout broken (overflow, misalignment)
- Controls missing
- Mobile broken

### Phase 6: Fix and Re-validate (Loop, max 3 cycles)
If failures detected → fix root cause → re-run Phase 4 → re-review Phase 5.
After 3 cycles, document remaining issues in `validation/handoff.json` under `unresolvedIssues`.

### Phase 7: Complete
Write final `validation/handoff.json` with:
- `validationPassed`: boolean
- `fixCycles`: number of fix iterations performed
- `cdnUrlsVerified`: true
- `screenshotsReviewed`: true

### Required Screenshots Per Pass
- `validation/desktop/showcase.png` — Full-page screenshot at 1536x960
- `validation/desktop/showcase-viewport.png` — Viewport-only screenshot
- `validation/mobile/showcase.png` — Full-page screenshot at 390x844 (2x scale)
- `validation/mobile/showcase-viewport.png` — Viewport-only screenshot
- `validation/report.playwright.json` — Structured report

**Completion gate:** A pass is NOT complete until screenshots exist on disk AND the subagent has visually reviewed them AND no failure conditions remain.
