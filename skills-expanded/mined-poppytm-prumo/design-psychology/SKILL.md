# Design Psychology & Cognitive Science Applied to UI/UX

## 1. Purpose
The purpose of this skill is to evaluate, audit, and improve user interfaces and user experiences by rigorously applying principles from cognitive science and design psychology. This includes leveraging Gestalt principles, cognitive load theory, decision-making laws, and models of human attention and memory to optimize behavioral design patterns.

## 2. Use When
- Designing or redesigning user interfaces, navigation menus, and complex forms.
- Conducting UX audits on existing software or websites to identify friction points.
- Optimizing conversion funnels, onboarding flows, or high-stakes interactions.
- Making architectural decisions regarding progressive disclosure and content layout.

## 3. Do Not Use When
- Dealing purely with backend architecture, data models, or infrastructure (unless it directly impacts system response time under the Doherty Threshold).
- Graphic design decisions driven entirely by brand identity rather than usability or cognition.
- When strict regulatory or accessibility requirements (e.g., WCAG) supersede cognitive heuristics, though they often overlap.

## 4. Required Context
- Target user demographics, technical proficiency, and expected mental models.
- The primary tasks and goals the user is attempting to achieve on the interface.
- Screen sizes, interaction modalities (touch, mouse), and physical constraints.
- Existing UI components, style guides, or wireframes.

## 5. Procedure
1. **Identify User Context:** Determine the target user's cognitive profile, prior knowledge (mental models), and the intrinsic complexity of the task.
2. **Audit Gestalt Principles:** Evaluate the interface for Proximity, Similarity, Continuity, Closure, Figure-Ground, Common Fate, and Prägnanz. Group related elements and clearly separate unrelated ones.
3. **Analyze Hick's Law:** Calculate the decision time for menus and choices ($T = a + b \log_2(n+1)$). Apply progressive disclosure and simplify option sets where $n$ is too high.
4. **Verify Fitts's Law:** Measure distance ($D$) and target width ($W$) for primary actions ($T = a + b \log_2(2D/W)$). Ensure CTAs are large enough and appropriately placed (e.g., corners/edges, touch targets $\ge 44 \times 44$px).
5. **Apply Miller's Law:** Chunk information, navigation items, and forms into manageable groups (typically $7 \pm 2$ items) to respect working memory limits.
6. **Minimize Cognitive Load:** Reduce extraneous load by removing non-essential visual elements. Support germane load by providing clear conceptual models.
7. **Highlight Key Actions:** Apply the Von Restorff Effect to make primary CTAs visually distinct and memorable compared to secondary actions.
8. **Leverage Serial Position & Peak-End:** Place critical information at the beginning/end of lists. Ensure the climax of the user journey and the final interaction are satisfying.
9. **Document & Measure:** Record the initial state and document the theoretical impact of the changes using before/after metrics and laws applied.

## 6. Decision Rules
- **Jakob's Law:** Favor conventional patterns over novel ones unless the novel approach provides a mathematically proven improvement in efficiency (e.g., Fitts's Law).
- **Doherty Threshold:** System response must be visually acknowledged within 400ms to maintain user flow; use skeleton screens or optimistic UI for slower operations.
- **Cognitive Load Priority:** If a visual element does not support intrinsic or germane load, it is extraneous and must be removed or minimized.
- **Accessibility Trumps Aesthetics:** Contrast ratios and legibility must meet WCAG standards regardless of Gestalt symmetry or Prägnanz.

## 7. Evidence Required
- A formal Cognitive Audit Report linking specific UI elements to applied psychological laws.
- Calculations or estimations for Hick's Law (menu complexity) and Fitts's Law (target reachability).
- Before-and-after visual comparisons (or wireframe annotations) demonstrating the structural changes.

## 8. Output Contract
- **Cognitive Audit Report:** A structured markdown document detailing issues and recommended fixes.
- **Annotated Designs:** Feedback overlaid on UI/UX assets or specific actionable text instructions for frontend developers.
- **UX Metrics Baseline:** Theoretical or empirical benchmarks for task completion time, error rates, and cognitive friction.

## 9. Stop Conditions
- All primary user flows have been audited against the core cognitive principles.
- Extraneous cognitive load has been minimized.
- Fitts's and Hick's calculations yield acceptable values for the given context.
- Evidence artifacts (reports/checklists) are completed and submitted.

## 10. Escalation Rules
- Escalate to Product/Business stakeholders if applying Hick's Law requires removing functionally mandatory options.
- Escalate to Engineering if the Doherty Threshold (400ms response time) cannot be met due to backend latency.
- Escalate to User Research if the mental model of the target demographic is unknown or disputed.
