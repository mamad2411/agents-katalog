# Responsive Design Strategy & Implementation

## 1. Purpose
To implement responsive, adaptive, and fluid web interfaces that provide an optimal user experience across all devices and screen sizes. This skill enforces modern CSS techniques such as container queries, fluid typography, logical properties, and content-first breakpoints over rigid, device-specific media queries.

## 2. Use When
- Building new front-end components or layouts.
- Refactoring legacy codebases that rely heavily on fixed breakpoints or absolute units.
- Implementing design systems that require component-level adaptivity.
- Optimizing media assets for different resolutions and viewports.

## 3. Do Not Use When
- Developing for environments with strictly fixed resolutions (e.g., specific hardware kiosks), unless future-proofing is required.
- Building purely backend or non-visual services.
- The project mandates a strict older browser support matrix that precludes the use of modern CSS features (e.g., `clamp()`, `@container`) and no polyfill strategy is in place.

## 4. Required Context
- Understanding of the target audience's primary devices and network conditions.
- Access to the content or content schema to determine natural breaking points.
- Core design tokens (color, typography scales, spacing scales).
- Knowledge of WCAG 2.1+ requirements, particularly SC 1.4.10 Reflow.

## 5. Procedure
1. **Audit Content:** Analyze the content flow to identify natural breakpoints where the layout breaks or becomes hard to read, rather than relying on predefined device widths.
2. **Implement Fluid Foundations:** Use CSS `clamp()`, `min()`, and `max()` functions for typography and spacing to create a fluid foundation that scales smoothly between minimum and maximum bounds.
3. **Define Grid Systems:** Implement responsive CSS Grid and Flexbox layouts using fractional units (`fr`) and auto-placement techniques.
4. **Implement Container Queries:** Apply `@container` rules for component-level responsiveness, ensuring components adapt to their immediate container's `inline-size`.
5. **Optimize Images:** Use `<picture>`, `srcset`, and `sizes` attributes for responsive images. Ensure appropriate loading strategies (`loading="lazy"`, `fetchpriority="high"`).
6. **Apply Progressive Enhancement:** Ensure core content and functionality are accessible without JavaScript or advanced CSS. Use `@supports` feature queries to layer on advanced styles.
7. **Test Across Environments:** Validate the layout across various viewports, orientations, and zoom levels (up to 400%). Use device throttling to simulate real-world conditions.
8. **Validate WCAG Reflow:** Ensure no horizontal scrolling occurs at 320px equivalent width (400% zoom on a 1280px display), except for components requiring it (e.g., data tables).

## 6. Decision Rules
- **Content over Devices:** Breakpoints MUST be determined by content needs, not arbitrary device widths.
- **Fluid over Fixed:** Preference MUST be given to fluid units (`vw`, `rem`, `clamp`) over fixed units (`px`) for layout dimensions and typography.
- **Component over Page:** Component adaptivity MUST use container queries instead of media queries when the component's layout depends on its container space.
- **Logical over Physical:** Use logical properties (`margin-inline`, `padding-block`) instead of physical properties (`margin-left`, `padding-top`) to support internationalization.
- **Touch Targets:** Minimum touch target size MUST be 44x44px.

## 7. Evidence Required
- **Visual Testing:** Screenshots or recordings of the UI scaling across multiple viewports and orientations.
- **Accessibility Audit:** Documentation confirming successful WCAG 1.4.10 Reflow validation.
- **Performance Audit:** Evidence of optimized image delivery and appropriate resource loading priorities.

## 8. Output Contract
- CSS code utilizing modern fluid and responsive techniques (`clamp()`, container queries).
- HTML structures implementing responsive images (`<picture>`, `srcset`).
- Fully responsive components that adapt seamlessly without horizontal scroll up to 400% zoom.

## 9. Stop Conditions
- All content is accessible and readable at a viewport width of 320px.
- The layout reflows successfully at 400% zoom on a 1280px screen without horizontal scrolling (excluding accepted exceptions).
- Component-level container queries are functioning as intended in target browsers.
- Images scale appropriately and load efficiently based on device capabilities.

## 10. Escalation Rules
- Escalate to Design if content cannot naturally reflow within the provided design constraints.
- Escalate to Architecture if legacy browser support requirements prevent the use of core responsive technologies without severe performance penalties.
- Escalate to Product if performance budgets for image delivery cannot be met due to asset size constraints.
