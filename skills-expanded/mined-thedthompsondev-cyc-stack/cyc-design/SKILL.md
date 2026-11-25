---
name: cyc-design
description: "Choose the shape of a change (data, interfaces, and the steps to build it) before writing logic. Use before any change that adds state, changes a data shape or interface, spans several files, or after a build shows the current design is wrong."
---

# Design the change

Get the shape right before the logic. Most rework comes from a wrong data shape or interface, not a wrong line of code. Follow the [handoff contract](../../docs/skill-contract.md).

For web interface creation or visual redesign, use the [frontend design method](frontend-design/SKILL.md) alongside this one. Its decision sheet (archetype, type, palette, signature element, rejection condition) is the visual counterpart of the caller sketch and data shape below; the architectural questions here still apply when state or interfaces change. A narrow UI repair should preserve the existing identity and use only relevant checks.

## The core loop

1. **Write the caller's code first.** Sketch how the change will be used from the outside: the call site, the component props, the API request. Then derive the types and signatures from that usage. If the sketch is awkward to call, the interface is wrong.
2. **Name the data shape.** Write the actual type or record, including what old data looks like and how it maps into the new shape. "Add `finished: boolean`, defaulting to `false` when missing on load."
3. **Resolve consequential alternatives.** When ownership or the public contract remains uncertain, compare genuinely different shapes against the requirements and choose with a reason. A cosmetic variation is not an alternative. Reuse a sound established project pattern without manufacturing another design; name the pattern and why it fits. For large or risky unresolved choices, independent alternatives can help answer a specific question.
4. **Screen ownership and boundaries.** Use the [architecture questions and counter-cases](../../docs/code-quality.md#choose-a-structure-that-protects-the-contract). Locate authoritative state and repeated policy; check that the interface hides meaningful decisions and legitimate callers cannot bypass its invariant. Preserve meaningful adapters, domain helpers, and compatibility behavior. Do not split or remove code solely because of its length, caller count, or execution order.
5. **Check the whole experience, not only the part.** Walk the user's complete path through the change. A section that is better on its own can make the whole page or flow feel disconnected. If the design improves one step but breaks the flow between steps, it is not done.
6. **Reuse before you add.** Prefer the project's existing store, helper, or pattern when it meets the requirement. A new dependency or layer needs a reason tied to a criterion.
7. **Slice it vertically.** Order the build as thin end-to-end slices (a tracer bullet first: one path working through every layer), each with the check from Verify's matrix that proves it.
8. **Write the scrap conditions.** What observation during build would mean this design is wrong? Examples: the same workaround needed twice, an escape-hatch type (`any`, casts), a sudden need for locks.

## Done when

- The caller sketch and data shape are written down.
- Consequential design uncertainty was resolved through a concrete comparison, or the fitting project pattern is identified.
- Every acceptance criterion maps to a slice and a check.
- For user-facing changes, the full journey was walked and still holds together.
- Scrap conditions are listed.
- Build could proceed without inventing a product decision.

For a one-file change, this can be five lines. Do not inflate it.

## Output

Chosen approach and why; alternatives considered and why not; data shape and legacy mapping; caller sketch; ordered slices with checks; scrap conditions; open decisions for the user.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Logic first | Writing functions before the type exists | Stop and write the shape |
| Unexamined choice | An uncertain ownership or contract decision is asserted without evidence | Compare a real alternative against the requirement |
| Horizontal plan | "Step 1: all the types. Step 2: all the UI" | Reorder as vertical slices |
| Polished fragment | One component improved; the page now feels stitched together | Walk the whole journey |
| Infrastructure for its own sake | New service or library with no criterion needing it | Reuse the existing mechanism |

## Handoff

Pass the design to [Build](../cyc-build/SKILL.md). If the design changes a shared dependency, update the [impact map](../cyc-impact/SKILL.md) first. If build hits a scrap condition, come back here with the observation; keep what still holds.
