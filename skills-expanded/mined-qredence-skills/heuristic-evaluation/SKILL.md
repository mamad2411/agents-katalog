---
name: heuristic-evaluation
description: "Evaluates a flow or screen against Jakob Nielsen's 10 usability heuristics (visibility of system status, match with the real world, user control, consistency, error prevention, recognition over recall, flexibility, minimalist design, error recovery, help and documentation) and reports concrete violations. Use for a fast, structured usability pass independent of visual polish."
---

# Heuristic Evaluation

## Purpose
Run a structured usability evaluation of a flow using Nielsen's 10 usability heuristics, independent of visual style.

## Operating Role
Act as a Figma design-file reviewer for this specific skill. Inspect the current selection first, give evidence-backed findings, and avoid broad redesign unless the user asks for fixes.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- When usability, not visual polish, is the concern
- Before user testing, to catch obvious issues cheaply first

## Required Inputs
- The flow (ordered set of screens) to evaluate, or a single screen if that's the scope
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Use heuristics as lenses, not as a generic checklist. Report only issues visible in the selected flow.

## Workflow
Walk the flow once per heuristic and record concrete violations, referencing the specific screen/element:
1. Visibility of system status -- does the user always know what's happening (loading, progress, confirmation)?
2. Match between system and the real world -- does language and iconography match user mental models, not internal jargon?
3. User control and freedom -- is there an obvious way to undo, cancel, or go back at every step?
4. Consistency and standards -- do similar actions look and behave the same way throughout the flow?
5. Error prevention -- are destructive or hard-to-reverse actions confirmed or made hard to trigger by accident?
6. Recognition rather than recall -- are options visible when needed, rather than requiring the user to remember something from an earlier screen?
7. Flexibility and efficiency of use -- are there reasonable shortcuts for repeat/expert users without cluttering the default path?
8. Aesthetic and minimalist design -- is every element earning its place, or is there competing/irrelevant information?
9. Help users recognize, diagnose, and recover from errors -- are error messages specific, in plain language, and paired with a way to fix the problem?
10. Help and documentation -- for complex actions, is contextual help available where it is needed, not just in a separate help center?

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Only report a violation if it is concretely observable in the flow -- do not pad the report with heuristics that have nothing to flag.
- Rate severity (Critical / Moderate / Minor) per Nielsen's standard severity scale so findings can be triaged.

## Finding Quality Rules
- Lead with the highest-impact issues, not the order discovered.
- Tie each finding to a specific frame, layer, component, variable, style, comment, interaction, or supplied source.
- Include severity only when it changes priority: Blocker, High, Medium, or Low.
- Pair every finding with an exact fix, replacement, or next decision.
- Separate confirmed findings from assumptions, recommendations, and unverified areas.

## Output Contract
Start with a 3-line summary: scope reviewed, blocker count, and highest-risk issue. Then provide grouped findings with location, severity, evidence, and exact fix. End with skipped or unverified areas.
- Skill-specific format: One section per heuristic with violations found (or "No issues observed"), each violation rated by severity.
