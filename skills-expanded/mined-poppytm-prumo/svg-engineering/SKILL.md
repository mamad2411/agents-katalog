# SVG Engineering & Optimization

## 1. Purpose
Provides structured guidelines for authoring, optimizing, and deploying SVG assets in web environments. Focuses on producing clean, performant, themeable, and accessible vector graphics through standardized viewBoxes, `currentColor` inheritance, and strict SVGO optimization pipelines.

## 2. Use When
- Creating or processing UI icon sets.
- Implementing vector illustrations that require theming or CSS styling.
- Optimizing raw SVGs exported from design tools (Figma, Illustrator, Sketch).
- Building SVG sprite sheets or component libraries.
- Implementing complex SVG filters, masks, or declarative animations.
- Employing procedural or algorithmic SVG generation.

## 3. Do Not Use When
- Handling photographic or highly complex, continuous-tone imagery (use WebP/AVIF).
- Building complex 3D scenes (use WebGL/Canvas).
- Rendering thousands of constantly moving particles (use Canvas API).

## 4. Required Context
- Understanding of the target display size and grid (e.g., 24x24 base for UI icons).
- Knowledge of the project's color theming strategy (to apply `currentColor`).
- Target browser support matrix for SMIL animations or specific SVG filters.
- Awareness of screen reader accessibility requirements for the specific context (decorative vs. informative).

## 5. Procedure
1. **Grid & Dimensions**: Standardize on a unified grid. For UI icons, enforce `viewBox="0 0 24 24"`. Use whole-number coordinates to prevent anti-aliasing blur. Remove fixed `width` and `height` attributes to ensure responsiveness.
2. **Semantic Structure**: Group related paths logically with `<g>`. Include `<title>` and `<desc>` elements as needed for meaningful graphics.
3. **Theming**: Replace fixed color values (e.g., `#000000`) with `fill="currentColor"` or `stroke="currentColor"` where elements should inherit text color.
4. **Optimization**: Run the SVG through an SVGO pipeline. Crucial configuration: set `removeViewBox: false` and `removeDimensions: true`. Strip out editor metadata and redundant groups.
5. **Accessibility**:
   - For decorative icons: Add `aria-hidden="true"` and `focusable="false"`.
   - For meaningful icons: Add `role="img"` and `aria-labelledby="[title-id] [desc-id]"`, ensuring corresponding elements have unique IDs.
6. **Deployment**: Package SVGs via inline component wrappers (e.g., React/Vue components) or as an SVG Sprite sheet (`<symbol>` + `<use>`) using the `icon-{category}-{name}` ID convention.

## 6. Decision Rules
- **Rule of ViewBox Preservation**: SVGO must NEVER strip the `viewBox` attribute. Removing it breaks relative scaling.
- **Rule of CurrentColor**: Single-color UI icons MUST use `currentColor` to allow CSS control. Multi-color illustrations should use CSS custom properties (variables) for configurable colors.
- **Rule of Integer Coordinates**: Anchor major path nodes on integer coordinates in the viewBox grid to ensure pixel-perfect crispness.
- **Rule of Reduced Motion**: Any declarative SVG animation must respect the `prefers-reduced-motion` media query, pausing or replacing the animation with a static state.

## 7. Evidence Required
- Code review verifying structural integrity, presence of accessibility attributes, and usage of `currentColor`.
- SVGO optimization reports showing reduction in file size and removal of cruft.
- Visual QA confirming no rendering regressions or sub-pixel blurring at 1x scale.
- Screen reader tests confirming correct announcements for non-decorative SVGs.

## 8. Output Contract
Produces valid, optimized `.svg` files or SVG-wrapping component code. Outputs must lack inline dimensions, retain their viewBox, support CSS styling, and pass automated accessibility checks.

## 9. Stop Conditions
Halt processing if:
- SVGO optimization unexpectedly distorts path geometry.
- An SVG contains nested base64 raster images that cannot be vectorized.
- The path data is excessively complex resulting in an unmanageable file size (>100KB for an icon).

## 10. Escalation Rules
Escalate to Design/Product if:
- Provided raw SVGs cannot be effectively optimized without unacceptable loss of visual fidelity.
- Brand guidelines dictate fixed colors that conflict with the `currentColor` theming strategy.
- Complex procedural SVG generation requires advanced mathematical algorithms beyond standard pathing.
