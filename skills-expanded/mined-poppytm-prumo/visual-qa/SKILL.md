---
name: visual-qa
description: Visual quality assurance, design-to-code parity verification (Figma specs), typography vertical rhythm, 4pt/8pt spatial grid audit, and cross-DPR asset sharpness.
---

# Visual Quality Assurance (Visual QA) Contract

## 1. Purpose
Inspect, audit, and certify the visual fidelity of implemented user interfaces against canonical design specifications (Figma, Sketch, Adobe XD). Enforce exact token alignment, 4pt/8pt spatial rhythm, typographic vertical cadence, responsive layout stability, and high-DPR asset rendering sharpness.

---

## 2. Use When
- Performing pre-merge Design QA on newly implemented components or views.
- Validating design-to-code parity during design system component authoring.
- Auditing visual bugs reported by users (misaligned icons, truncated labels, broken flex wraps).
- Verifying cross-device layout consistency across standard breakpoints (320px to 4K).

---

## 3. Do Not Use When
- Setting up automated headless image-diffing gates in CI (use `visual-regression`).
- Conducting heuristic usability evaluations or user journey mapping (use `ui-ux-review` or `user-flows`).
- Refactoring backend business logic or state machines.

---

## 4. Required Context
Before performing a Visual QA audit, obtain:
1. **Canonical Design Specification**: Figma file link, design tokens specification, or exported component redlines.
2. **Target Breakpoints**: Mobile (320px, 375px), Tablet (768px), Desktop (1024px, 1440px), Ultrawide (>1920px).
3. **Typography & Spatial Scales**: Pinned line heights, font sizes, letter spacing, and 4pt/8pt grid definitions.
4. **Active Theme**: Light, Dark, or Brand-specific theme variants.

---

## 5. Procedure

### Step 1: Spatial Grid & Alignment Audit
1. Overlay an 8px / 4px baseline grid on the implemented UI.
2. Verify all margins, paddings, and component dimensions snap cleanly to token increments ($4\text{px}, 8\text{px}, 12\text{px}, 16\text{px}, 24\text{px}, 32\text{px}, 48\text{px}, 64\text{px}$).
3. Check alignment: text baselines, icon optical centers relative to adjacent labels, and column gutters.

### Step 2: Typographic Hierarchy & Vertical Rhythm
1. Verify implemented font family matches token declaration across all headings, body, and code elements.
2. Verify font weight, size (`rem`), line height (`unitless` or `rem`), and letter spacing (`tracking`).
3. Check for text truncation edge cases: long internationalized strings, multi-line titles, and line clamps (`line-clamp-2`).

### Step 3: Color, Surface & Elevation Fidelity
1. Inspect background surfaces, borders, dividers, and shadows across all implemented components.
2. Verify that colors resolve directly to semantic design tokens rather than hardcoded hex approximations.
3. Validate elevation layers: box shadows match token blur radius, spread, and opacity.

### Step 4: Asset & Iconography Rendering Quality
1. Verify all icons and illustrative graphics are rendered as scalable vectors (`<svg>`) rather than rasterized images.
2. For raster images, verify that responsive `srcset` supplies `@2x` and `@3x` assets for high-DPI (Retina) displays.
3. Verify icon stroke widths remain crisp and visually balanced with adjacent text.

### Step 5: Responsive Fluidity & Edge Breakpoint Inspection
1. Resize the viewport dynamically from 320px to 1920px:
   - Verify layout transitions smoothly across responsive breakpoints without awkward horizontal jumps.
   - Verify no horizontal scrollbars appear at 320px width (WCAG 1.4.10 compliance).
   - Ensure touch targets maintain minimum $44 \times 44\text{ px}$ (or $24\text{ px}$ with spacing) on touch screens.

---

## 6. Decision Rules
1. **Zero Off-Grid Dimensions**: Arbitrary values (e.g. `margin: 13px; padding: 7px;`) are strictly prohibited; all spacing must resolve to the 4pt/8pt token scale.
2. **Optical vs. Geometric Centering**: Icons with asymmetric visual weight (e.g. play triangle) must be optically centered, not purely geometrically centered.
3. **No Pixelated Icons**: Any icon rendered in low-resolution raster format (`.png`, `.jpg`) on high-DPI screens is a visual defect.
4. **Token Parity Over Hardcoded Hacks**: If an implemented color differs by even 1% from design, it must be aligned with the canonical token rather than patched with a local override.

---

## 7. Evidence Required
- **Visual QA Scorecard**: Matrix recording Parity %, Spacing Compliance, Typography Compliance, and Asset Sharpness.
- **Side-by-Side Redline Comparison**: Screenshots comparing Figma spec overlay against implemented DOM.
- **Punch List**: Prioritized list of visual bugs with exact CSS remediation instructions.

---

## 8. Output Contract
A production Visual QA deliverable must contain:
1. Visual QA Audit Report (`templates/visual-qa-report.md`).
2. Tabular punch list of discrepancies with screenshot references and CSS fixes.
3. Design Sign-Off status (Approved | Approved with Minor Punch List | Rejected).

---

## 9. Stop Conditions
- 100% of target views inspected across all defined breakpoints.
- All spatial and typographic discrepancies logged with exact CSS remedies.
- Design parity score computed.

---

## 10. Escalation Rules
- Escalate to Design Lead if implemented content length inherently breaks designed Figma layout (e.g. design assumes 3-word title, but real data contains 25 words).
- Escalate to Frontend Architect if third-party embedded widgets cannot be styled to conform to brand design tokens.
