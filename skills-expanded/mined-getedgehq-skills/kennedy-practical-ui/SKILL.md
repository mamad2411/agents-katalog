---
name: kennedy-practical-ui
description: "Design and critique web or mobile interfaces using Erik Kennedy's practical UI method. Use for screen design, visual redesign, component refinement, or focused UI design practice."
---

# Practical UI Design through Learn UI Design and Design Hacks

Based on Erik Kennedy's public method. Not affiliated with or endorsed by Erik Kennedy.

## When to use

Use this skill to design a concrete web or mobile screen, improve an existing interface, explain a visual problem, or practice a specific UI technique. It is especially useful when a developer or UX designer needs actionable decisions about attention, layout, controls, typography, color, and component coherence. Work with the actual content and task rather than delivering an abstract aesthetics lecture. [S1][S5]

Choose the output that matches the request: an implemented screen, an annotated design specification, a prioritized critique, or a controlled practice exercise. Preserve the user's platform, brand constraints, existing component system, and intended scope. For practice, reproduce a reference to study its decisions; for production, apply the learned relationships to the user's own interface. [S6][S7]

This package synthesizes Kennedy's public essays. It does not reproduce his paid curriculum. The cited heuristics inform judgment; the package's evidence recording, state coverage, and delivery format are operational additions. Read the relevant sections of the method as decisions arise. Use the examples to understand application, not as universal token sets.

## Procedure

1. **Frame the task.** Identify the screen, user goal, frequent actions, constraints, available artifacts, and requested deliverable. Record assumptions in [templates/output-template.md](templates/output-template.md). For critique, ground each finding in an observable element; for practice, define one capability to improve. See the scope rules in [references/method.md](references/method.md#scope-and-evidence).

2. **Rank attention.** Write the intended first, second, and third things a user should notice. Use action frequency as an initial proxy for importance, then account for essential information. Squint at or blur the existing screen and compare its actual emphasis. Follow [references/method.md](references/method.md#attention-and-teaching). [S5]

3. **Study a targeted reference when needed.** Choose a strong example of the specific element causing trouble. In practice mode, recreate and compare it; in production, extract transferable relationships without importing unrelated interaction assumptions. Use [references/method.md](references/method.md#learning-through-controlled-practice). [S2][S6]

4. **Establish layout without decorative rescue.** For a clean interface, start in grayscale. Test roomier spacing within controls, between elements, and between groups. Align meaningful edges and let content determine widths. Consult [references/method.md](references/method.md#layout-spacing-and-alignment) for colorful and dense interface exceptions. [S1][S10]

5. **Map controls to consequences.** Identify the object or region changed by every action. Put item actions near items and regional actions above their region. Check long lists and reachability; compensate for necessary distance with visibility and explicit association. Follow [references/method.md](references/method.md#locality-and-reachability). [S4][S5]

6. **Select controls from the choices.** Consider option count, selection semantics, immediate versus submitted changes, and likely values. Compare visible alternatives before choosing a dropdown. Use the decision table in [references/method.md](references/method.md#control-selection). [S5]

7. **Balance text emphasis.** Establish readable body text and distinguishable, reusable roles. Combine stronger and quieter properties instead of making every label shout. Inspect long headings and hover geometry using [references/method.md](references/method.md#typography-and-states). [S2][S10]

8. **Derive functional color variations.** Assign colors to roles, then vary a base hue through saturation and brightness. Inspect rendered combinations and measure text contrast rather than equating HSB brightness with readability. Follow [references/method.md](references/method.md#color-variations). [S3][S7]

9. **Resolve coherence on one component.** Refine a representative button or similar element before expanding. Match letterforms, corner character, inline icon strokes, color personality, and dimensional cues. Consult [references/method.md](references/method.md#component-coherence-and-light). [S1][S7]

10. **Add imagery and identity where useful.** Protect image text with a reliable backing or tonal treatment across crops. Add a recurring brand motif only after fundamentals work. Teach unfamiliar features through concrete examples. See [references/method.md](references/method.md#imagery-and-motifs) and the illustrations in [examples/worked-examples.md](examples/worked-examples.md). [S2][S5][S9]

11. **Reframe stalled solutions.** List constants shared by unsuccessful iterations. Sensibly change form, position, or representation, then verify that the action or information still means what users expect. Use [references/method.md](references/method.md#reframing). [S8]

12. **Review and deliver evidence.** Apply [checklists/review-checklist.md](checklists/review-checklist.md), revise failures, and fill [templates/output-template.md](templates/output-template.md). Deliver the requested artifact, its key rationale, reusable decisions, and relevant state or viewport evidence. Mark unavailable checks pending; do not claim unobserved success.

## Files in this skill

- [SKILL.md](SKILL.md): Entry point, use cases, and the agent's main loop.
- [references/method.md](references/method.md): Detailed principles, decisions, exceptions, and explicit warnings.
- [references/sources.md](references/sources.md): Numbered public sources actually fetched and their contributions.
- [examples/worked-examples.md](examples/worked-examples.md): Invented before and after illustrations with rule annotations.
- [templates/output-template.md](templates/output-template.md): Fill-in delivery format with guidance for each field.
- [checklists/review-checklist.md](checklists/review-checklist.md): Pass/fail review gates and common fixes.
