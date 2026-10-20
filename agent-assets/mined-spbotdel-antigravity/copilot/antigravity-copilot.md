# AI Coding Guidelines for Family Tree Visualization Project

## Project Overview
This is a static web application for interactive genealogy visualization using GEDCOM files. The app parses family data, builds descendant trees, and renders them with D3.js in a dark-themed interface.

## Architecture
- **Main Entry Point**: `index.html` contains all CSS, JavaScript, and HTML in a single file
- **Data Flow**: GEDCOM file → `parseGedcom()` → `buildDescendantsTree()` → D3.js tree layout → SVG rendering
- **Key Components**:
  - GEDCOM parser (inline function)
  - Tree builder (recursive descendant traversal)
  - D3 renderer with zoom/pan controls
  - Info panel for person details
  - Responsive design with collapsible panels

## Key Files
- `index.html`: Complete application with inline styles and scripts
- `3.ged`: Sample GEDCOM data file
- `js/*.js`: Modular versions of parsing/building/rendering functions (currently unused)
- `css/style.css`: Additional styles (not loaded)
- `check-ids.html`, `test.js`: Development utilities for GEDCOM validation

## Development Workflow
- **No Build Process**: Open `index.html` directly in a browser
- **Testing**: Use browser dev tools; run `check-ids.html` or `test.js` for data validation
- **Data Loading**: App fetches `./3.ged` on load; modify `fetch("./3.ged")` for different files

## Code Patterns
- **Inline Everything**: CSS variables, JS functions, and HTML structure in `index.html`
- **State Management**: Global variables (`data`, `currentId`, `svg`, etc.) for app state
- **D3 Integration**: Uses `d3.tree()` with custom `nodeSize` and `separation` functions
- **Constants**: Config values like `CARD_W = 230`, `NODE_Y = 250` control layout
- **Event Handling**: Direct DOM manipulation with `onclick` and `addEventListener`
- **Russian Comments**: Code comments and UI text in Russian

## Specific Conventions
- **Person Cards**: Fixed size 230x90px with gender-based colors (`--male`, `--female`)
- **Tree Layout**: Vertical spacing `NODE_Y = 250`, horizontal `NODE_X = COUPLE_TOTAL_H + 14`
- **Zoom Limits**: Scale extent [0.1, 3] with identity transform tracking
- **Panel Behavior**: Info panel toggles based on screen orientation (`isPortrait()`)
- **Focus Handling**: `focusRawId` vs `focusResolvedId` for tree centering logic

## Common Tasks
- **Add New GEDCOM Field**: Extend `parseGedcom()` to handle additional tags, update person object structure
- **Modify Layout**: Adjust `CARD_W`, `CARD_H`, `NODE_X`, `NODE_Y` constants and re-render
- **Change Styling**: Update CSS variables in `:root` for theme changes
- **Add Interactions**: Attach event listeners to SVG elements using D3 selections
- **Debug Rendering**: Check `lastRenderedRoot` and `lastTransform` in console

## Dependencies
- **D3.js v7**: Tree layout, zoom behavior, SVG manipulation
- **Font Awesome 6.4.0**: Icons for controls
- **Google Fonts (Inter)**: Typography
- **No Build Tools**: Pure vanilla JS/CSS

## Gotchas
- Tree rendering requires valid GEDCOM with family relationships
- Cyclic references in data cause recursion warnings
- SVG viewBox and transform handling for responsive zoom
- Info panel positioning uses CSS custom properties for width (`--panel-w: 360px`)