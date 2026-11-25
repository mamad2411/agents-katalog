---
name: prototype-from-flow
description: "Produces a prototype connection plan from a described user flow, flow diagram, PRD, or set of designed screens. Use when screens exist or a flow is described and the team needs a clear map of frames, triggers, actions, branches, overlays, and missing screens before manual prototype wiring. This is a planning/specification skill, not an interaction-editing skill."
---

# Prototype From Flow

## Purpose
Turn a described or diagrammed flow into a clear prototype wiring specification that a designer can apply manually or use later when Figma Agent supports interaction editing.

## Operating Role
Act as a Figma prototype planning reviewer, not as a prototype editor. Inspect visible frames, labels, annotations, and any supplied flow source. Produce a precise connection map and call out missing screens, ambiguous destinations, and unsupported assumptions.

## Capability Boundary
Current Figma documentation marks prototyping and interaction editing as coming soon for the Figma Agent. Do not claim that you created, wired, tested, or modified prototype interactions unless the current session explicitly shows that capability is available. Default to plan-only output.

## Supported Context
- Start from the current selection. If nothing is selected, use the current page for planning and ask before expanding to a whole file.
- Use visible Figma context first: frames, components, instances, variables, styles, layers, labels, annotations, existing prototype settings if visible, comments, and sections.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, only when the answer changes the flow map materially.

## Activation Boundary
Use this skill when:
- Screens are designed but not yet connected into a prototype.
- A PRD, flow diagram, FigJam-style flow, or written user flow needs to become a prototype plan.
- A team needs a manual wiring checklist before design review, usability testing, or stakeholder demo setup.

Do not use this skill to generate new UI screens, perform broad design critique, or edit prototype wiring directly.

## Required Inputs
- The flow definition: ordered steps, decision points, or source material.
- The intended starting frame.
- The frames/screens in scope.
- Any states or branches that matter, such as logged in/out, empty/full, error/success, permissions, or cancel/back paths.

If a needed input can be inferred from visible context, proceed and label the assumption.

## Workflow
1. Identify the start, end, and core user goal of the flow.
2. Map each flow step to an existing frame. If no matching frame exists, mark it as `Missing frame` rather than inventing one.
3. Identify every decision point and branch, including error, cancel, back, empty, permission, and success paths that are explicitly described or clearly implied.
4. For each connection, specify:
   - source frame
   - source element or hotspot
   - trigger
   - action
   - destination frame or overlay
   - transition/animation recommendation
   - rationale or evidence
5. For overlays, specify intended placement, dismissal behavior, background treatment, and whether outside-click close is safe.
6. Flag ambiguous connections where labels, frame names, or flow logic do not make the destination clear.
7. Order the plan into a manual wiring checklist: happy path first, then branches, overlays, back/cancel paths, and reset/start-frame setup.

## Decision Rules
- Prefer `Navigate to` for ordinary screen-to-screen transitions.
- Prefer `Open overlay` for modals, menus, drawers, popovers, and contextual panels.
- Prefer `Back` only when the return destination should follow navigation history.
- Prefer `Scroll to` for same-page anchors or long-page jumps.
- Recommend `Smart animate` only when source and destination frames clearly share corresponding layers.
- Do not add speculative routes. If the flow source does not mention a branch and visible UI does not imply it, list it as a question.

## Guardrails
- Do not say "wired," "created connections," "tested the prototype," or "set the starting frame" unless those actions were actually supported and completed.
- Do not silently skip a described branch because the destination screen is missing.
- Do not treat a polished happy path as complete when required error, cancel, empty, or back paths are absent.
- Keep adjacent work as follow-up: screen design, state design, visual critique, motion spec, and accessibility review are separate tasks.

## Output Contract
Start with a short status line: `Prototype plan only` or `Prototype changes applied` if the environment truly supports them.

Then return:
1. **Scope and assumptions** - frames reviewed, starting frame, flow source, and assumptions.
2. **Connection map** - table with `From | Element | Trigger | Action | To | Transition | Notes`.
3. **Missing or ambiguous pieces** - missing frames, unclear destinations, unresolved state logic, or branches needing product decisions.
4. **Manual wiring checklist** - ordered steps a designer can follow in Figma.
5. **Follow-up checks** - prototype QA, motion spec, state completeness, or handoff notes when relevant.
