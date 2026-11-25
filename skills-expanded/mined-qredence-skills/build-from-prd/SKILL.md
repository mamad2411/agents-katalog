---
name: build-from-prd
description: "Reads a product requirements document (PRD) and produces the corresponding Figma design -- screens, states, and flow -- reusing existing design system components wherever possible and flagging any requirement that has no corresponding pattern yet. Use when a PRD or spec exists and needs to become an actual design, especially when paired with a connector to the requirements source."
---

# Build From PRD

## Purpose
Turn a written product requirement into a structured Figma design that reuses the existing design system.

## Operating Role
Act as a Figma design-file producer for this specific skill. Create or structure the requested artifact in the file when enough context exists; otherwise return the smallest useful plan and ask only for blocking inputs.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A PRD, spec, or detailed ticket exists and needs a first-pass design
- Pair with a connector to the requirements source so the agent can read the live requirements

## Required Inputs
- The PRD/spec content (via connector or pasted text)
- The target file/page to build in, and which library is canonical for components
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Extract screens, states, data needs, and acceptance criteria before creating or changing frames.
- Use existing components and patterns in the file before drawing new UI.

## Workflow
1. Read the PRD and extract: user goal, explicit requirements (must-haves), open questions/edge cases mentioned, and any explicit UI direction given.
2. Break the requirement into discrete screens/states needed to satisfy it end to end, including non-happy-path states called out or implied (errors, empty, permissions-denied, etc.) -- cross-check against states-completeness-check once a first draft exists.
3. For each screen, build using existing components and variables from the canonical library first; only introduce new/custom elements where no existing pattern satisfies the requirement, and call those out explicitly as new patterns needing design system review.
4. Reflect every explicit requirement in the design directly, and note in a callout or comment any requirement that's ambiguous or that you made an assumption about, so it can be confirmed rather than silently guessed.
5. Assemble the discrete screens into a connected flow (invoke prototype-from-flow logic) matching the order of operations implied by the PRD.
6. List every requirement from the PRD next to the screen/element that satisfies it, and separately list anything in the PRD that could not be confidently translated into UI (e.g. a backend-only requirement, or a requirement too vague to design against).

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Do not silently drop a requirement that's hard to design for -- surface it instead of omitting it.
- Do not invent product decisions the PRD leaves open; flag them as open questions.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return the created or proposed Figma structure first, then list assumptions, variants/states covered, and follow-up decisions. If changes were applied, include exactly what changed.
- Skill-specific format: A traceability list (Requirement -> Screen/element it is addressed by) plus an "Open questions / assumptions" list.
