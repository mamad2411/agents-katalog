# Skill: Layout Design Patterns & Composition

## 1. Purpose
To establish robust, responsive, and visually balanced spatial compositions using standardized grid systems, layout primitives, and cognitive viewing patterns (Z-pattern, F-pattern, Gutenberg Diagram).

## 2. Use When
- Designing or implementing page-level architectures.
- Constructing responsive components and UI sections.
- Defining a spacing and alignment system.
- Refactoring complex, nested layouts into composable primitives.

## 3. Do Not Use When
- Dealing with micro-interactions and animations.
- Implementing non-visual business logic or backend architectural design.
- Applying superficial styling (typography, colors) without structural changes.

## 4. Required Context
- Understanding of the underlying content model and density.
- Target audience viewport constraints and interaction modalities.
- Available CSS capabilities (Grid, Flexbox, Container Queries).

## 5. Procedure
1. **Analyze Content Density**: Evaluate text heaviness vs. visual asset prevalence.
2. **Select Composition Pattern**: 
   - Apply *F-Pattern* for text-heavy, scanning-oriented views (e.g., Dashboards).
   - Apply *Z-Pattern* for low-density, conversion-oriented views (e.g., Landing Pages).
   - Utilize *Gutenberg Diagram* dynamics for distinct reading gravity.
3. **Establish Grid System**: Define standard columns (e.g., 4/8/12), gutters, and margins. Ensure mathematical proportionality.
4. **Define Spacing Scale**: Choose a base unit (e.g., 4px or 8px) and build a geometric progression scale ($S_n = S_0 \times 1.5^n$ or linear geometric multipliers).
5. **Implement Layout Primitives**: Build agnostic components (`Stack`, `Cluster`, `Center`, `Sidebar`, etc.) using modern CSS features without domain-specific constraints.
6. **Apply Responsive Strategy**: Favor intrinsic sizing and *Container Queries* (`@container`) over arbitrary viewport breakpoints. Break when the content dictates.
7. **Test Reflow**: Validate layout integrity at micro (mobile) and macro (ultrawide) extremes.

## 6. Decision Rules
- **Rule of Intrinsic Layout**: Components should dictate their own breakpoints based on content width, rather than screen width (`clamp()`, `min()`, `max()`, `minmax()`).
- **Separation of Concerns**: Layout primitives must not handle cosmetics (color, font-family). They only manage flow, space, and alignment.
- **Golden Ratio ($\varphi$)**: Use $\varphi \approx 1.618$ for harmonious macro-proportions when appropriate.
- **Micro-Spacing**: Spacing within components (padding/gap) must follow the established geometric token scale.

## 7. Evidence Required
- Code validates against standard structural primitives (e.g., flex-basis, grid-template-columns).
- Responsive tests demonstrating fluid content reflow across breakpoints without horizontal scrolling.
- Filled `layout-spec.md` with explicit token mapping.

## 8. Output Contract
- Composable UI structures defined by atomic CSS classes or primitive React/Vue components.
- Container-query-first responsive behavior.
- Documented spacing tokens.

## 9. Stop Conditions
- All interface mockups are successfully represented through composable primitives.
- No content overflows its designated container on varied viewports.
- Spacing rhythm passes visual and programmatic checks.

## 10. Escalation Rules
- Escalate to Design Lead if the provided content cannot fit the prescribed grid mathematically.
- Escalate to Architecture if legacy browsers require extensive polyfills for CSS Grid or Container Queries.
