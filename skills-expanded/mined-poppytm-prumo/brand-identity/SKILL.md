# Brand Identity Design & Governance

## 1. Purpose
The exact goal of this skill is to establish, document, and govern a unified Brand Identity System. This includes scalable logo designs, precise color palettes, consistent typography hierarchies, and cohesive brand guidelines that ensure distinctiveness, reproducibility, and memorability across all touchpoints.

## 2. Use When
- Designing a new brand identity from scratch.
- Refreshing or rebranding an existing visual identity.
- Establishing formal brand guidelines for third-party use.
- Auditing current brand usage for consistency across platforms.
- Creating responsive logo systems (Hero, Compact, Micro).

## 3. Do Not Use When
- Developing specific marketing campaigns without touching core brand elements.
- Generating random illustrations unrelated to brand identity.
- Designing a one-off asset that does not need to adhere to brand guidelines.
- Focusing purely on functional UI/UX layout without styling considerations.

## 4. Required Context
- A clearly defined brand strategy (positioning, core values, personality).
- Understanding of the target audience and market context.
- Knowledge of the chosen Brand Architecture (Monolithic, Endorsed, or Pluralistic).
- Access to current design tokens (if existing) and creative briefs.

## 5. Procedure
1. **Define Brand Strategy:** Analyze brand positioning, values, and personality traits.
2. **Design Logo System:** Create the core logo and responsive variants (Hero, Compact, Micro, Favicon). Ensure scalability and single-color reproducibility.
3. **Establish Color Palette:** Define primary, secondary, accent, and neutral colors using accessible OKLCH tokens.
4. **Define Typography System:** Select primary and secondary typefaces. Establish hierarchy (headings, body, captions).
5. **Create Imagery & Iconography Style Guide:** Specify the visual language, photography direction, and icon grid systems.
6. **Document Brand Voice & Tone:** Outline communication principles and tone variations for different contexts.
7. **Build Brand Guidelines Document:** Compile all rules (clear space, minimum size, color usage, do's and don'ts) into a comprehensive manual.
8. **Audit for Consistency:** Perform a brand audit across digital touchpoints to ensure compliance with the guidelines.

## 6. Decision Rules
- **Logo Usage:** Logos must maintain defined clear space (e.g., $1\times$ the width of the main icon) and minimum size thresholds.
- **Color Accessibility:** Brand colors used for text must meet WCAG AA contrast ratios (minimum 4.5:1 for normal text).
- **Architecture:** Sub-brands in an endorsed architecture must visually reflect the parent brand's core traits.
- **Responsiveness:** Always provide a simplified logo version for small sizes (e.g., $<32$px).

## 7. Evidence Required
- A complete Brand Guidelines document conforming to the specified template.
- Vector files for all logo variants (SVG, AI, or EPS).
- Color contrast validation reports for all text/background combinations.
- A completed consistency audit report with zero critical violations.

## 8. Output Contract
- **Brand Guidelines Document:** A comprehensive specification detailing logo rules, colors, typography, voice, and imagery.
- **Responsive Logo Assets:** Hero, Compact, and Micro versions of the logo.
- **Design Tokens:** OKLCH values for the color palette mapped to logical roles.
- **Brand Audit Report:** Evaluation of brand application across platforms.

## 9. Stop Conditions
- Brand guidelines are approved by relevant stakeholders.
- The logo system reproduces successfully in full color, black/white, and at favicon sizes.
- The consistency audit returns no critical or unmitigated violations.

## 10. Escalation Rules
- Escalate if requested brand colors fail minimum accessibility contrast requirements and stakeholders refuse adjustments.
- Escalate if brand naming or visual elements infringe on existing trademarks.
- Escalate if sub-brand requirements conflict fundamentally with the established monolithic brand architecture.
