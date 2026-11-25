# Icon System Design & Governance

## 1. Purpose
The exact goal of this skill is to establish and govern a robust, scalable, and accessible icon library architecture. This includes defining icon grid specifications, optical alignment rules, naming conventions, categorization, accessibility standards, versioning, and distribution strategies.

## 2. Use When
- Designing a new icon system from scratch.
- Expanding an existing design system with new iconography.
- Refactoring inconsistent or disorganized icon sets.
- Implementing an icon component library for React, Vue, or Svelte.
- Defining a governance model for SVGs in a front-end codebase.

## 3. Do Not Use When
- Creating complex illustrations (use an illustration skill).
- Designing raster-based assets or photography.
- The project relies entirely on a third-party, pre-packaged icon library (e.g., FontAwesome, Material Icons) without any custom additions or local governance.

## 4. Required Context
- **Brand Guidelines:** Understanding of the brand's visual language (stroke weight, corner radius, tone).
- **Technical Stack:** Knowledge of the distribution targets (React, SVG sprite, raw SVGs).
- **Design Tooling:** Access to the design system source of truth (e.g., Figma).

## 5. Procedure
1. **Define Icon Grid and Keylines:** Establish the standard grid (e.g., 24×24px with 2px padding) and define geometric keylines (circle, square, vertical/horizontal rectangles).
2. **Establish Conventions:** Create standardized naming structures (`{category}/{action-or-object}`) and categorize icons logically.
3. **Design Icons:** Draw icons adhering to the grid, keylines, and optical alignment rules (e.g., triangles extending slightly beyond the grid for optical balance). Maintain consistent stroke or fill styles.
4. **Optimize SVGs:** Process all source SVGs through SVGO to strip unnecessary metadata and optimize paths.
5. **Add Accessibility:** Classify each icon as decorative (`aria-hidden="true"`) or informative (`aria-label="..."` or `<title>`).
6. **Package Distribution:** Bundle the icons as a component library, SVG sprite, or NPM package.
7. **Sync Design Tooling:** Create and publish a Figma library serving as the source-of-truth.
8. **Set Up Governance:** Establish semantic versioning policies for the library (major for removals/changes, minor for additions).
9. **Audit System:** Periodically review the library against the established consistency checks.

## 6. Decision Rules
- **Grid Constraint:** All icons must snap to the defined grid and fit within the designated live area, except for required optical adjustments.
- **Consistency:** Use either stroke or fill entirely across a cohesive set. Do not mix uncoordinated styles.
- **Stroke Width:** If using strokes, they must maintain a consistent width (e.g., 2px).
- **Naming Protocol:** All files must follow the `{category}/{action-or-object}` kebab-case format.
- **A11y Mandate:** No icon should be used as the sole indicator of critical information without a corresponding text label or accessible alternative.

## 7. Evidence Required
- A complete icon grid specification document.
- Optimized, minified SVG files free of `<style>`, `<g>` wrappers (where unnecessary), and design tool cruft.
- Validated categorization and naming structure for the icon set.
- Proof of accessibility integration (ARIA attributes applied).

## 8. Output Contract
- **Icon Grid Specifications:** Defining sizing, keylines, and spacing.
- **Governance Rules:** Naming, versioning, and deprecation policies.
- **Optimized Assets:** Production-ready SVG components or sprites.
- **Design System Documentation:** Comprehensive guides for consumption.

## 9. Stop Conditions
- The icon grid and guidelines are thoroughly documented and validated.
- All icons pass SVGO optimization and accessibility checks.
- A functional distribution pipeline (or packaging mechanism) is configured and tested.

## 10. Escalation Rules
- Escalate to the Design Lead if there are irreconcilable conflicts between the icon style and brand guidelines.
- Escalate to Frontend Architecture if the chosen distribution method conflicts with application performance constraints.
- Escalate to Product Management if there is disagreement on the deprecation of widely used legacy icons.
