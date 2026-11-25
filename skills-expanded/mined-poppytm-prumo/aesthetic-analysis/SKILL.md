# Aesthetic Movement Analysis & Trend Evaluation

## 1. Purpose
The purpose of this skill is to provide a structured, historically grounded framework for analyzing digital design aesthetics and evaluating their alignment with brand identity, accessibility standards, and technical constraints. It facilitates informed decision-making regarding UI/UX aesthetic choices by contextualizing trends within broader design history.

## 2. Use When
- Establishing or updating a design system or brand guidelines.
- Evaluating the appropriateness of adopting a specific design trend for a new product.
- Conducting competitive analysis of aesthetic choices within a market sector.
- Auditing an existing UI for consistency, trend longevity, and accessibility impact.

## 3. Do Not Use When
- Executing minor component bug fixes or layout adjustments that do not alter the broader aesthetic.
- Dealing strictly with backend infrastructure or data architecture.
- A hard mandate already enforces a specific aesthetic without room for evaluation.

## 4. Required Context
- **Brand Identity Strategy:** Core values, mission, and personality of the brand.
- **Target Demographics:** User base characteristics, technological literacy, and cultural context.
- **Platform Constraints:** Performance budgets, supported devices, and accessibility compliance requirements (e.g., WCAG 2.2).

## 5. Procedure
1. **Historical Contextualization:** Identify the proposed or existing design aesthetic and map it to established historical movements (e.g., Bauhaus, Swiss Grid, Neubrutalism).
2. **Visual Characteristics Analysis:** Deconstruct the aesthetic into its core UI elements (typography, color palettes, spacing, shadows, borders, textures).
3. **Accessibility Impact Assessment:** Evaluate how the visual characteristics affect legibility, contrast ($L = 0.2126 \times R + 0.7152 \times G + 0.0722 \times B$), and cognitive load.
4. **Brand Alignment Evaluation:** Map the psychological and cultural associations of the movement against the brand's core values. Calculate the Brand Alignment Score.
5. **Technical Complexity Analysis:** Assess the feasibility and performance cost of implementing the aesthetic (e.g., heavy use of backdrop-filters in Glassmorphism).
6. **Trend Longevity Prediction:** Position the aesthetic on the Trend Lifecycle (Emergence $\rightarrow$ Peak $\rightarrow$ Mainstream $\rightarrow$ Decline $\rightarrow$ Revival).
7. **Synthesis and Recommendation:** Compile findings into an actionable recommendation using the provided templates.

## 6. Decision Rules
- **Accessibility Invariant:** No aesthetic trend may supersede WCAG AA contrast ratio requirements ($4.5:1$ for normal text, $3:1$ for large text).
- **Brand Fidelity:** An aesthetic scoring below $60\%$ on the Brand Alignment Score must be rejected or heavily modified.
- **Performance Constraint:** If an aesthetic (e.g., Glassmorphism) causes frame rates to drop below 60fps on P50 devices, graceful degradation fallbacks must be strictly enforced.

## 7. Evidence Required
- Completed `aesthetic-evaluation.md` template.
- Documented Brand Alignment Score with justification.
- Contrast ratio and accessibility validations for the primary visual characteristics.

## 8. Output Contract
- A structured evaluation report detailing the aesthetic's characteristics, historical roots, and practical implications.
- A quantifiable Brand Alignment Score.
- Explicit technical implementation guidelines or fallbacks for the chosen aesthetic.

## 9. Stop Conditions
- The aesthetic evaluation report is fully populated and reviewed.
- An insurmountable accessibility blocker is identified, immediately disqualifying the aesthetic.
- The brand alignment score conclusively supports or rejects the aesthetic choice.

## 10. Escalation Rules
- Escalate to the Design Lead if there is a fundamental conflict between a stakeholder-mandated aesthetic and accessibility compliance.
- Escalate to Engineering Lead if the performance implications of the chosen aesthetic require significant architectural changes.
