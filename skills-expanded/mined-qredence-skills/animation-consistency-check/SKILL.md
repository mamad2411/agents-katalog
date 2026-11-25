---
name: animation-consistency-check
description: "Audits animated components and prototype transitions across a file for consistent easing, duration, and motion character, flagging transitions that feel out of step with the rest of the product's motion language. Use when multiple people or sessions have added animation and it needs to feel cohesive."
---

# Animation Consistency Check

## Purpose
Make sure animated transitions across a file share one coherent motion language, rather than each feeling separately tuned.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- Multiple animated components/transitions exist and need a consistency pass
- Before finalizing motion for a release

## Required Inputs
- The scope of transitions/animated components to review
- Any established motion principle or reference transition to treat as the baseline, if one exists
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Inventory transitions by role before judging values. Compare like with like: navigation, overlay, component state, and micro-interaction.

## Workflow
1. Inventory every prototype transition (trigger -> animation type -> duration/easing) and every animated component (interactive component transitions, Motion-file animations) in scope.
2. Group transitions by role (entrances, exits, in-place state changes, navigational transitions, micro-interactions) since each role should share consistent timing/easing within itself.
3. Compare durations within each role group and flag outliers (e.g. one modal opens in 150ms while every other modal opens in 300ms).
4. Compare easing curves within each role group and flag inconsistency (e.g. most exits use ease-in, but one uses a bouncy spring that feels tonally different).
5. Check that semantically identical interactions (e.g. every primary button's hover state) use identical timing, not just similar-looking timing.
6. Propose a single consistent value per role group when outliers are found, defaulting to whichever value is most prevalent unless there's a clear reason another value is more correct.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Distinguish an intentional, meaningful difference (e.g. a celebratory moment deliberately animated more expressively) from an accidental inconsistency -- ask if unsure.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: A table grouped by transition role: Role | Transitions compared | Outlier(s) found | Recommended consistent value.
