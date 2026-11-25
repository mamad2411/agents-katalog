---
name: cyc-explore
description: "Settle an open decision by comparing genuinely different options or building a throwaway prototype, then recommend one. Use when the user asks \"which approach\", \"what are my options\", or \"what should this look like\", when earlier options were rejected, or when a design fork would be expensive to reverse."
---

# Explore to decide

Exploration exists to answer a question. **No decision, no prototype.** Follow the [handoff contract](../../docs/skill-contract.md).

## The core loop

1. **Write the question at the top.** "Should finished homework disappear or move to a collapsed section?" If you cannot write the question, go back to [Frame](../cyc-frame/SKILL.md).
2. **Classify it: observable or preference?** If building something small would show the answer (performance, feel, whether it fits), build it instead of asking. If it is pure taste or business priority, lay out the options and ask.
3. **Generate options that differ in kind.** Different journey, data boundary, architecture, or narrative. Two color schemes of the same layout do not count. Three options is usually right.
4. **Choose the prototype branch.**
   - **Logic question** (state model, algorithm, API shape): a small script or test file that exercises each option with realistic data.
   - **UI question:** mount the variants on the real page behind a simple switch, using realistic content. A real page beats a blank canvas.
   Label every prototype as throwaway and put the question in its first line.
5. **Compare against the same criteria.** A small table, one row per option, the task's criteria as columns, plus what the prototype showed.
6. **Recommend one.** Give a clear pick and the reason. The user wants a strong read, not a menu. Leave the choice with them only when it depends on their taste or priorities.
7. **When all options are rejected, find out why first.** Extract the reason, add it to the frame as a criterion, then generate new options.

## Done when

- The question is written.
- Options differ in kind, and each is compared on the same criteria.
- Any prototype answers the question and is labeled throwaway.
- There is a recommendation with a reason, or a named taste decision for the user.

## Anti-patterns

| Name | The tell | Fix |
| --- | --- | --- |
| Menu without a pick | "Here are three options" and nothing more | Recommend one |
| Cosmetic variants | Options differ in naming, color, or copy | Vary the structure |
| Prototype creep | The throwaway is being made production-ready | Stop; hand the decision to Design |
| Exploring a settled question | Options generated when the user already chose | Respect the decision |

## Handoff

Pass the recommendation, comparison, and what the prototype could not show (persistence, scale, real data) to the stage returned by `run next`: [Challenge](../cyc-challenge/SKILL.md) in Explore, [Verify](../cyc-verify/SKILL.md) in Evaluate, or [Build](../cyc-build/SKILL.md) in Experience. A recommendation does not authorize implementation on an advisory route. Quarantine throwaway prototypes; remove only artifacts created for this exploration, preserving user work.
