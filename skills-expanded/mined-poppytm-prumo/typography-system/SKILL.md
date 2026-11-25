# Typography System Skill

## 1. Purpose
The purpose of this skill is to establish robust, scalable typography systems for digital design, incorporating modular scales, fluid typography, variable fonts, type hierarchy, font pairing, vertical rhythm, and typographic tokens.

## 2. Use When
- Designing a new design system or component library
- Implementing typography CSS architecture from scratch
- Refactoring legacy typography into fluid, scalable tokens
- Establishing typographic rules for digital products

## 3. Do Not Use When
- Designing print materials where absolute units (pt/mm) take precedence over responsive units
- Generating dynamic text rendering in `<canvas>` or WebGL applications (different constraints apply)
- Making one-off stylistic text tweaks without system implications

## 4. Required Context
- Target viewports and devices for fluid scaling min/max boundaries
- Brand guidelines (preferred typefaces)
- Accessibility requirements (WCAG contrast, zoom requirements)
- Understanding of project scale (marketing vs. dense data-heavy UI)

## 5. Procedure
1. **Select modular scale ratio** based on project type.
   - Example: Major Third (1.25) for marketing, Minor Second (1.067) for dense UI.
2. **Define type ramp** with `clamp()` fluid sizing.
   - Example: `clamp(1rem, 0.5rem + 2vw, 2rem)`.
3. **Configure variable font axes** and OpenType features.
   - Optimize for performance (one file) and enable features like `liga`, `kern`, `tnum`.
4. **Establish vertical rhythm baseline**.
   - Typically using a 4px or 8px baseline grid to dictate line-heights and margins.
5. **Create typographic design tokens** in DTCG format.
6. **Validate readability**.
   - Minimum 16px body text size.
   - Line length between 45-75 characters (`ch` units).
7. **Test across viewports and zoom levels**.

## 6. Decision Rules
- **Rule 1 (Readability):** Base body text MUST be at least 16px (1rem).
- **Rule 2 (Line Length):** Text blocks MUST NOT exceed 75ch.
- **Rule 3 (Units):** Fluid typography MUST use `rem` for base and `vw/vh` for fluid calculations, avoiding hardcoded `px`.
- **Rule 4 (Hierarchy):** Type systems SHOULD define 6-8 distinct semantic levels (Display, H1-H4, Body, Caption, Code).

## 7. Evidence Required
- Defined type scales with mathematical backing.
- Token definitions exported in standard format.
- Code preview showing fluid scaling behavior across mobile to desktop widths.

## 8. Output Contract
Produces a comprehensive typography specification including:
- Typeface selections (with pairing rationale)
- Fluid `clamp()` values for all text styles
- Defined vertical rhythm scale
- DTCG-compatible JSON token files or CSS Custom Properties

## 9. Stop Conditions
- Required font files cannot be legally licensed for web use.
- The selected typeface lacks necessary glyphs or language support for the target audience.
- Accessibility standards for minimum contrast or zoom up to 200% are not met.

## 10. Escalation Rules
- Escalate if brand guidelines enforce inaccessible font choices (e.g., extremely thin weights as default body text).
- Escalate if variable fonts drastically increase payload size beyond acceptable performance budgets without WOFF2 compression benefits.
