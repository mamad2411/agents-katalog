# Advertising Design & Visual Persuasion

## 1. Purpose
The exact goal of this skill is to empower the creation of high-converting visual advertising assets by applying established psychological models (like AIDA), visual persuasion principles (Ethos, Pathos, Logos), and systematic testing approaches (A/B testing).

## 2. Use When
- Designing social media ads (Facebook, Instagram, LinkedIn).
- Creating display network banners (Google Ads).
- Designing email header graphics and marketing templates.
- Structuring landing page hero sections for lead generation.
- Formulating A/B tests for visual assets.

## 3. Do Not Use When
- Developing long-form content or purely organic, non-promotional material.
- Coding backend infrastructure or functional application features.
- Generating purely artistic explorations without a clear conversion goal.

## 4. Required Context
Before using this skill, ensure you have:
- Brand guidelines (colors, typography, logo usage).
- Target audience demographic and psychographic profiles.
- A clear conversion goal (e.g., Lead capture, purchase, signup).
- The platform context and asset specifications (aspect ratios, safe zones).

## 5. Procedure
1. **Analyze Brief:** Review the goal, audience, and platform constraints.
2. **Apply AIDA Structure:**
   - **Attention:** Select a high-contrast hero image or bold typography.
   - **Interest:** Structure visual hierarchy to guide the eye; use infographics or subheadings.
   - **Desire:** Employ lifestyle imagery or social proof to build emotional connection.
   - **Action:** Design a high-contrast, prominent Call-to-Action (CTA).
3. **Map Visual Persuasion:** Ensure Ethos (trust signals), Pathos (emotional resonance), and Logos (clarity, data) are present.
4. **Draft Layout:** Position elements considering natural eye flow (F-pattern or Z-pattern).
5. **Optimize CTA:** Ensure minimum 44x44px touch target (if mobile), strong color contrast (WCAG AA at minimum), and action-oriented copy.
6. **Formulate Testing Plan:** Propose an A/B testing strategy isolating a single variable (e.g., CTA color vs. CTA text).
7. **Validate:** Check against `checks/advertising-design-checklist.md`.

## 6. Decision Rules
- **Contrast:** The CTA must have the highest visual weight and contrast ratio (ideally $CR \ge 4.5:1$) against its background.
- **Hierarchy:** No more than 3 levels of typographical hierarchy (Headline, Subheadline/Body, CTA/Microcopy).
- **Whitespace:** Active whitespace must be used to group related elements and isolate the CTA.
- **A/B Testing:** A test must isolate exactly *one* variable to maintain statistical validity.

## 7. Evidence Required
- A completed `ad-design-spec.md` for each asset.
- A filled out `advertising-design-checklist.md`.
- Mathematical validation of CTA contrast ratio (e.g., using WCAG guidelines).

## 8. Output Contract
- Visual design specification detailing layout, typography, color palette, and asset placement.
- A defined A/B testing hypothesis.
- Clear rationale based on the AIDA model.

## 9. Stop Conditions
- The creative brief lacks a primary conversion goal.
- Brand assets are missing or contradictory.
- Requested layout violates platform specifications (e.g., Facebook\'s 20% text rule, if applicable/strictly enforced).

## 10. Escalation Rules
- Escalate if the requested visual approach fundamentally conflicts with established brand safety guidelines.
- Escalate if requested A/B tests require multivariate testing beyond the scope of simple visual A/B tools.
