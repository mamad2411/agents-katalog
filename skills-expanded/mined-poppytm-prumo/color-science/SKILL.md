# Color Science for Design Systems

## 1. Purpose
To apply perceptually uniform color spaces (OKLCH/OKLAB) and scientifically rigorous contrast algorithms (WCAG 2.2, APCA) to construct robust, accessible, and wide-gamut design system color palettes.

## 2. Use When
- Designing a new color system or design tokens from scratch.
- Migrating an existing sRGB/HSL palette to CSS Color Module Level 4 (OKLCH, Display P3).
- Generating dynamic theme variants (dark mode, high contrast) using algorithms.
- Auditing UI color contrast for accessibility compliance.

## 3. Do Not Use When
- Creating raster graphic assets or photography edits (use dedicated image manipulation tools).
- Working in environments constrained strictly to legacy CSS (no `color()`, no Custom Properties) without a build step to transpile colors.
- Color choices are purely subjective art direction without systematic scale requirements.

## 4. Required Context
- Target display capabilities (sRGB vs. Display P3).
- Baseline brand colors or aesthetic directives.
- Expected accessibility standards (e.g., WCAG 2.2 AA/AAA, APCA).
- The CSS framework or token architecture being used (e.g., Tailwind CSS v4, custom CSS variables, JSON tokens).

## 5. Procedure
1. **Define Color Primitives in OKLCH:** Establish foundational hues. Use OKLCH notation: `oklch(L C H)` where L = 0-1 (Lightness), C = 0-0.4 (Chroma), H = 0-360 (Hue).
2. **Generate Systematic Palette Scales (50-950):** 
   - Fix lightness ($L$) at each step across different hues to maintain equal perceived brightness.
   - Adjust chroma ($C$) curves to prevent gamut clipping, reducing chroma at extreme high/low lightness.
3. **Map Semantic Intent:** Abstract primitives into semantic tokens (`surface`, `text`, `action`, `status`, `border`).
4. **Validate Contrast Pairs:** Calculate WCAG 2.2 contrast ratios (target 4.5:1 for normal text, 3:1 for large text) and/or APCA Lightness Contrast ($L_c$) between foreground and background tokens.
5. **Compile to CSS Custom Properties:** Generate standard CSS output using `oklch()` and `color-mix()` where applicable. Include sRGB fallbacks using `@supports` or build-tool compilation if supporting legacy browsers.
6. **Audit for Gamut Safety:** Verify out-of-gamut colors on target displays and define gamut-mapping strategies (e.g., relative color syntax or CSS `color()` with fallbacks).

## 6. Decision Rules
- **Luminance Lock:** Tokens sharing the same scale index (e.g., `blue-500` and `red-500`) MUST have the exact same OKLCH Lightness ($L$) value.
- **Interpolation Space:** All color interpolations and gradients MUST be calculated in OKLAB to prevent hue shifts and dead zones.
- **Contrast Baselines:** Semantic text tokens MUST mathematically clear WCAG 2.2 AA at a minimum against their designated surface tokens.
- **Chroma Limits:** Chroma values ($C$) exceeding 0.4 MUST be verified against Display P3 limits; out-of-gamut colors must gracefully degrade via gamut mapping.

## 7. Evidence Required
- A populated `color-audit-report.md` detailing WCAG/APCA values for semantic combinations.
- Visual or JSON verification of consistent lightness values across a palette scale.
- CSS outputs that include valid OKLCH syntax.

## 8. Output Contract
- **Token Files:** JSON or CSS variables implementing the OKLCH palette.
- **Documentation:** A scale reference showing Lightness, Chroma, and Hue for each step.
- **Audit Reports:** Explicit contrast calculations verifying accessibility requirements.

## 9. Stop Conditions
- All required semantic colors exist and map to a uniform primitive scale.
- All text-to-surface contrast ratios pass required guidelines.
- The output format (CSS/JSON) matches the project's technical architecture.

## 10. Escalation Rules
- If brand colors inherently fail contrast guidelines when mapped to the nearest OKLCH uniform step, escalate to design stakeholders for a trade-off discussion.
- If target technical stack cannot support modern CSS colors and build-tool fallbacks are breaking design intent, escalate to engineering leads.
